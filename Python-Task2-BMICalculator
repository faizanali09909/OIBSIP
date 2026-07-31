def get_positive_float(prompt):
    while True:
        value = input(prompt)
        try:
            value = float(value)
            if value <= 0:
                print("Please enter a positive number greater than zero.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main():
    print("BMI Calculator")
    print("-" * 20)

    weight = get_positive_float("Enter yuor weight in kg: ")
    height = get_positive_float("Enter your height in m: ")

    bmi = weight/ (height **2)
    category = classify_bmi(bmi)
    
    print("-" *20)
    print(f"Your BMI is: {round(bmi, 2)}")
    print(f"Category: {category}")

if __name__ == "__main__":
    main()
