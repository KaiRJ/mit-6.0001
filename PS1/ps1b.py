current_savings = 0
portion_down_payment = 0.25
r = 0.04

annual_salary = float(input("What is your annual salary?: £"))
monthly_salary = annual_salary / 12

portion_saved = float(input("What portion of your salary is saved?: "))
monthly_saved = monthly_salary * portion_saved

total_cost = float(input("What is the cost of your dream home?: "))
down_payment = total_cost * portion_down_payment

semi_annual_raise = float(input("What is the semi-annual salary raise?: "))

months = 0
while current_savings < down_payment:
    months+=1
    current_savings += current_savings * r/12
    current_savings += monthly_saved

    if months % 6 == 0:
        monthly_saved += monthly_saved * semi_annual_raise

print(f"It will take you {months} months.")