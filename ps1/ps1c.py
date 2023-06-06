total_months = 36
r = 0.04
semi_annual_raise = 0.07
total_cost = 1e6
portion_down_payment = 0.25
down_payment = total_cost * portion_down_payment

def compute_total_savings(total_months, monthly_saved, r, semi_annual_raise):
    total_savings = 0
    for month in range(total_months):
        total_savings += total_savings * r/12
        total_savings += monthly_saved

        if month % 6 == 0:
            monthly_saved += monthly_saved * semi_annual_raise

    return total_savings

annual_salary = float(input("What is your annual salary?: £"))
monthly_salary = annual_salary / 12
max_total_savings = compute_total_savings(total_months, monthly_salary, r, semi_annual_raise)

if (max_total_savings > down_payment): # Possilbe to buy house in 3 years
    epsilon = 100
    numGuesses = 0
    max = 10000
    min = 0
    portion_saved = ((max + min) // 2) / 10000
    print(f"portion_saved = {portion_saved}")
    while True:
        numGuesses += 1
        total_savings = compute_total_savings(total_months, monthly_salary*portion_saved, r, semi_annual_raise)
        if abs(total_savings - down_payment) < epsilon:
            break
        elif total_savings > down_payment:
            max = int(portion_saved * 10000)
        else:
            min = int(portion_saved * 10000)
        portion_saved = ((max + min) // 2) / 10000

    print(f"Best savings rate: {portion_saved}")
    print(f"Steps in bisection search: {numGuesses}")
else: # Not possilbe to buy house in 3 years
    print('It is not possible to pay the down payment in three years.')











