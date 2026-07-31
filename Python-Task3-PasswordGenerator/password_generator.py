import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox
 
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
 

AMBIGUOUS_CHARS = "0Ool1I|"
 
 
class PasswordGenerator:
    """Handles the actual password generation logic, kept separate from the UI."""
 
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"
 
    def _strip_ambiguous(self, char_set: str) -> str:
        return "".join(c for c in char_set if c not in AMBIGUOUS_CHARS)
 
    def generate(self, length: int, use_upper: bool, use_lower: bool,
                 use_digits: bool, use_symbols: bool, exclude_ambiguous: bool) -> str:
 
        selected_types = []
        pool = ""
 
        for flag, char_set in [
            (use_upper, self.uppercase),
            (use_lower, self.lowercase),
            (use_digits, self.digits),
            (use_symbols, self.symbols),
        ]:
            if flag:
                chars = self._strip_ambiguous(char_set) if exclude_ambiguous else char_set
                if not chars:
                    continue
                selected_types.append(chars)
                pool += chars
 
        if len(selected_types) < 2:
            raise ValueError("Select at least 2 character types.")
        if length < 8:
            raise ValueError("Password length must be at least 8 characters.")
        if length < len(selected_types):
            raise ValueError(
                f"Length must be at least {len(selected_types)} to include one of each selected type."
            )
 

        password_chars = [secrets.choice(char_set) for char_set in selected_types]
 

        remaining = length - len(password_chars)
        password_chars += [secrets.choice(pool) for _ in range(remaining)]
 

        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
 
        return "".join(password_chars)
 
    @staticmethod
    def assess_strength(password: str, type_count: int) -> tuple[str, str]:
        """Returns (label, color) based on length + character diversity."""
        length = len(password)
 
        score = 0
        score += 1 if length >= 8 else 0
        score += 1 if length >= 12 else 0
        score += 1 if length >= 16 else 0
        score += type_count  # 2, 3, or 4 types selected
 
        if score <= 3:
            return "Weak", "#e74c3c"
        elif score <= 5:
            return "Medium", "#f39c12"
        else:
            return "Strong", "#27ae60"
 
 
class PasswordGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("460x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
 
        self.generator = PasswordGenerator()
        self.history: list[str] = []
 
        self._build_ui()
 

 
    def _build_ui(self):
        pad = {"padx": 16, "pady": 8}
 
        title = tk.Label(
            self.root, text="🔐 Password Generator",
            font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#cdd6f4"
        )
        title.pack(pady=(16, 4))
 

        self.password_var = tk.StringVar(value="")
        display_frame = tk.Frame(self.root, bg="#1e1e2e")
        display_frame.pack(fill="x", **pad)
 
        self.password_entry = tk.Entry(
            display_frame, textvariable=self.password_var,
            font=("Consolas", 14), justify="center",
            state="readonly", readonlybackground="#313244", fg="#a6e3a1",
            relief="flat", bd=8
        )
        self.password_entry.pack(fill="x", ipady=8)
 

        strength_frame = tk.Frame(self.root, bg="#1e1e2e")
        strength_frame.pack(fill="x", padx=16, pady=(4, 8))
 
        self.strength_label = tk.Label(
            strength_frame, text="Strength: —", font=("Segoe UI", 10, "bold"),
            bg="#1e1e2e", fg="#cdd6f4", anchor="w"
        )
        self.strength_label.pack(fill="x")
 
        self.strength_canvas = tk.Canvas(
            strength_frame, height=10, bg="#313244", highlightthickness=0
        )
        self.strength_canvas.pack(fill="x", pady=(4, 0))
 

        length_frame = tk.Frame(self.root, bg="#1e1e2e")
        length_frame.pack(fill="x", **pad)
 
        tk.Label(
            length_frame, text="Password Length (min 8):",
            bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10)
        ).pack(anchor="w")
 
        self.length_var = tk.IntVar(value=16)
        length_control = tk.Frame(length_frame, bg="#1e1e2e")
        length_control.pack(fill="x", pady=(4, 0))
 
        self.length_slider = tk.Scale(
            length_control, from_=8, to=64, orient="horizontal",
            variable=self.length_var, bg="#1e1e2e", fg="#cdd6f4",
            troughcolor="#313244", highlightthickness=0, showvalue=False,
            command=lambda _=None: self.length_spin_var.set(self.length_var.get())
        )
        self.length_slider.pack(side="left", fill="x", expand=True)
 
        self.length_spin_var = tk.IntVar(value=16)
        self.length_spinbox = tk.Spinbox(
            length_control, from_=8, to=64, width=5,
            textvariable=self.length_spin_var, font=("Segoe UI", 10),
            command=self._sync_length_from_spinbox
        )
        self.length_spinbox.pack(side="left", padx=(8, 0))
        self.length_spinbox.bind("<KeyRelease>", lambda e: self._sync_length_from_spinbox())
 

        types_frame = tk.LabelFrame(
            self.root, text="Character Types (select at least 2)",
            bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10, "bold")
        )
        types_frame.pack(fill="x", padx=16, pady=8)
 
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
 
        checks = [
            ("Uppercase (A-Z)", self.use_upper),
            ("Lowercase (a-z)", self.use_lower),
            ("Numbers (0-9)", self.use_digits),
            ("Symbols (!@#$...)", self.use_symbols),
        ]
        for text, var in checks:
            cb = tk.Checkbutton(
                types_frame, text=text, variable=var,
                bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
                activebackground="#1e1e2e", activeforeground="#cdd6f4",
                anchor="w"
            )
            cb.pack(fill="x", padx=8, pady=2)
 
        ambiguous_cb = tk.Checkbutton(
            types_frame, text="Exclude ambiguous characters (0, O, l, 1, I)",
            variable=self.exclude_ambiguous,
            bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
            activebackground="#1e1e2e", activeforeground="#cdd6f4",
            anchor="w"
        )
        ambiguous_cb.pack(fill="x", padx=8, pady=(6, 4))
 
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(fill="x", padx=16, pady=8)
 
        generate_btn = tk.Button(
            btn_frame, text="Generate Password", command=self.generate_password,
            bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        generate_btn.pack(fill="x", ipady=6)
 
        copy_btn = tk.Button(
            btn_frame, text="📋 Copy to Clipboard", command=self.copy_to_clipboard,
            bg="#313244", fg="#cdd6f4", font=("Segoe UI", 10),
            relief="flat", cursor="hand2"
        )
        copy_btn.pack(fill="x", ipady=4, pady=(8, 0))
 

        history_frame = tk.LabelFrame(
            self.root, text="History (last 5, this session only)",
            bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10, "bold")
        )
        history_frame.pack(fill="both", expand=True, padx=16, pady=(8, 16))
 
        self.history_listbox = tk.Listbox(
            history_frame, font=("Consolas", 9), bg="#313244", fg="#a6e3a1",
            relief="flat", selectbackground="#89b4fa", height=5
        )
        self.history_listbox.pack(fill="both", expand=True, padx=6, pady=6)
        self.history_listbox.bind("<<ListboxSelect>>", self._copy_history_selection)
 

 
    def _sync_length_from_spinbox(self):
        try:
            value = int(self.length_spin_var.get())
            value = max(8, min(64, value))
            self.length_var.set(value)
        except (ValueError, tk.TclError):
            pass
 
    def generate_password(self):
        length = self.length_var.get()
        type_count = sum([
            self.use_upper.get(), self.use_lower.get(),
            self.use_digits.get(), self.use_symbols.get()
        ])
 
        try:
            password = self.generator.generate(
                length=length,
                use_upper=self.use_upper.get(),
                use_lower=self.use_lower.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get(),
                exclude_ambiguous=self.exclude_ambiguous.get(),
            )
        except ValueError as e:
            messagebox.showerror("Invalid Selection", str(e))
            return
 
        self.password_var.set(password)
        self._update_strength(password, type_count)
        self._add_to_history(password)
 
        # Auto-copy on generation
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
 
    def _update_strength(self, password: str, type_count: int):
        label, color = self.generator.assess_strength(password, type_count)
        self.strength_label.config(text=f"Strength: {label}")
 
        self.strength_canvas.delete("all")
        width = self.strength_canvas.winfo_width() or 400
        fill_ratio = {"Weak": 0.33, "Medium": 0.66, "Strong": 1.0}[label]
        self.strength_canvas.create_rectangle(
            0, 0, width * fill_ratio, 10, fill=color, outline=""
        )
 
    def _add_to_history(self, password: str):
        self.history.insert(0, password)
        self.history = self.history[:5]
        self.history_listbox.delete(0, tk.END)
        for pw in self.history:
            self.history_listbox.insert(tk.END, pw)
 
    def _copy_history_selection(self, event):
        selection = self.history_listbox.curselection()
        if not selection:
            return
        password = self.history_listbox.get(selection[0])
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
            self.strength_label.config(text=f"Strength: (copied '{password[:6]}...' to clipboard)")
 
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("No Password", "Generate a password first.")
            return
        if not CLIPBOARD_AVAILABLE:
            messagebox.showwarning(
                "pyperclip not installed",
                "Run: pip install pyperclip\nThen restart the app."
            )
            return
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
 
 
def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
 
 
if __name__ == "__main__":
    main()
