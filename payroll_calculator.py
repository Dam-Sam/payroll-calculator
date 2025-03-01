import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

yearly_rates_file = "yearly_rates.json"

def load_json(file):
    try:
        with open(file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("JSON file not found!")
    except json.JSONDecodeError:
        print("Error reading JSON file!")
    return data


def calculate_payroll(income):
    # CPP Constants
    cpp_rate = round(rates["cpp"]["cpp_rate"]/100, 4)
    cpp_max_earnings = round(rates["cpp"]["maximum_earnings"], 2)
    cpp_exemption = round(rates["cpp"]["basic_exemption"], 2)
    cpp_pen_earnings = round(rates["cpp"]["pensionable_earnings"], 2)
    cpp_max_contri = round(rates["cpp"]["max_contribution_employee"], 2)
    
    # CPP 2 Constants
    cpp2_rate = 0.04  # Additional CPP contribution rate
    cpp2_threshold = 68500  

    # EI Constants
    ei_rate = 0.0164
    ei_employe_rate = 1.4
    ei_max = 1002.45  

    # Income Tax Brackets (Federal)
    federal_brackets = rates["federal_tax"]["bracket"]
    federal_rates = rates["federal_tax"]["rates"]
    federal_constants = rates["federal_tax"]["constants"]
    
    # Income Tax Brackets (Ontario)
    ontario_brackets = rates["ontario_tax"]["bracket"]
    ontario_rates = rates["ontario_tax"]["rates"]
    ontario_constants = rates["ontario_tax"]["constants"]

    def calculate_tax(income, brackets, rates, constants):
        tax = 0
        for i in range(len(brackets) - 1):
            if income > brackets[i]:
                taxable_income = min(income, brackets[i + 1]) - brackets[i]
                tax += taxable_income * rates[i] - constants[i]
        return tax

    #///Federal Tax Deduction///
    federal_tax = calculate_tax(income, federal_brackets, federal_rates, federal_constants)
    
    # CPP Calculation
    cpp_contribution = max(0, min((income - cpp_exemption/12) * cpp_rate, cpp_max_earnings))
    print(cpp_contribution)
    cpp2_contribution = max(0, (income - cpp2_threshold) * cpp2_rate) if income > cpp2_threshold else 0
    cpp_employer_contibution = cpp_contribution
    
    # EI Calculation
    ei_contribution = min(income * ei_rate, ei_max)

    # Income Tax Calculation

    federal_tax = calculate_tax(income, federal_brackets, federal_rates)
    ontario_tax = calculate_tax(income, ontario_brackets, ontario_rates)

    total_deductions = cpp_contribution + cpp2_contribution + ei_contribution + federal_tax + ontario_tax
    net_income = income - total_deductions

    return {
        "Gross Income": income,
        "CPP Deduction": round(cpp_contribution, 2),
        "CPP2 Deduction": round(cpp2_contribution, 2),
        "EI Deduction": round(ei_contribution, 2),
        "Federal Tax": round(federal_tax, 2),
        "Ontario Tax": round(ontario_tax, 2),
        "Total Deductions": round(total_deductions, 2),
        "Net Income": round(net_income, 2)
    }

# def on_calculate():
#     try:
#         income = float(entry_income.get())
#         payroll = calculate_payroll(income)
        
#         # Clear previous results
#         for row in result_table.get_children():
#             result_table.delete(row)

#         # Insert new results
#         for key, value in payroll.items():
#             result_table.insert("", "end", values=(key, f"${value:,.2f}"))

#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter a valid numeric income.")

# def export_to_pdf():
#     try:
#         income = float(entry_income.get())
#         payroll = calculate_payroll(income)
        
#         pdf_filename = "payroll_report.pdf"
#         c = canvas.Canvas(pdf_filename, pagesize=letter)
#         c.setFont("Helvetica", 12)
        
#         # Title
#         c.drawString(200, 750, "Payroll Calculation Report")
#         c.line(50, 740, 550, 740)  # Underline

#         # Data Output
#         y_position = 720
#         for key, value in payroll.items():
#             c.drawString(100, y_position, f"{key}: ${value:,.2f}")
#             y_position -= 20
        
#         c.save()
#         messagebox.showinfo("Success", f"Payroll report exported as '{pdf_filename}'.")

#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter a valid numeric income.")

#Load Yearly Rates
rates = load_json(yearly_rates_file)
print(calculate_payroll(2750))

# # GUI Setup
# root = tk.Tk()
# root.title("Ontario Payroll Calculator")
# root.geometry("450x500")
# root.resizable(False, False)

# # Labels & Entry
# tk.Label(root, text="Enter Total Income:", font=("Arial", 12)).pack(pady=10)
# entry_income = tk.Entry(root, font=("Arial", 12))
# entry_income.pack()

# # Buttons
# frame_buttons = tk.Frame(root)
# frame_buttons.pack(pady=10)

# btn_calculate = tk.Button(frame_buttons, text="Calculate", command=on_calculate, font=("Arial", 12))
# btn_calculate.grid(row=0, column=0, padx=5)

# btn_export = tk.Button(frame_buttons, text="Export to PDF", command=export_to_pdf, font=("Arial", 12))
# btn_export.grid(row=0, column=1, padx=5)

# # Table for Results
# columns = ("Category", "Amount")
# result_table = ttk.Treeview(root, columns=columns, show="headings", height=8)
# result_table.heading("Category", text="Category")
# result_table.heading("Amount", text="Amount")
# result_table.pack(pady=10, fill="both", expand=True)

# # Run GUI
# root.mainloop()
