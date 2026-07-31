# Task 2 – BMI Calculator (Beginner Tier)

## Objective
A command-line tool that calculates Body Mass Index (BMI) from user-provided
weight and height, and classifies the result into a standard BMI category.

## Tech Stack
- Python 3 (no external libraries)

## Features
- Prompts user for weight (kg) and height (m)
- Input validation: rejects non-numeric input and values ≤ 0, and
  re-prompts until valid
- Calculates BMI using the standard formula: `weight / (height ** 2)`
- Classifies BMI into Underweight / Normal / Overweight / Obese
- Displays the result rounded to 2 decimal places

## How to Run
```bash
python bmi_calculator.py
```

## Example
```
BMI Calculator
--------------------
Enter your weight in kg: 70
Enter your height in m: 1.75
--------------------
Your BMI is: 22.86
Category: Normal
```
