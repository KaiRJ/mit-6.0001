total_months = 36
r = 0.04
semi_annual_raise = 0.07
total_cost = 1e6
portion_down_payment = 0.25
down_payment = total_cost * portion_down_payment

def compute_savings(total_months, monthly_saved, r, semi_annual_raise):
    current_savings = 0
    for month in range(total_months):
        current_savings += current_savings * r/12
        current_savings += monthly_saved

        if month % 6 == 0:
            monthly_saved += monthly_saved * semi_annual_raise

    return current_savings


annual_salary = float(input("What is your annual salary?: £"))
monthly_salary = annual_salary / 12

epsilon = 100
numGuesses = 0
low = 0.0
high = 1.0
portion_saved = (high + low) / 2
total_saved = compute_savings(total_months, monthly_salary*portion_saved, r, semi_annual_raise)
while ( abs(total_saved - down_payment) > epsilon ):
    numGuesses += 1
    if total_saved > down_payment:
        high = portion_saved
    else:
        low = portion_saved
    portion_saved = (high + low) / 2
    total_saved = compute_savings(total_months, monthly_salary*portion_saved, r, semi_annual_raise)

print(f"Best savings rate: {portion_saved}")
print(f"Steps in bisection search: {numGuesses}")







