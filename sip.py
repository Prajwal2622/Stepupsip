import csv

def calculate_sip_returns_with_step_up_percentage(initial_investment, step_up_percentage, rate_of_return, months, step_up_frequency):
    
    # Convert the annual rate of return to a monthly rate (as a decimal)
    monthly_rate = rate_of_return / 100 / 12
    
    # Determine step-up interval in months based on frequency
    if step_up_frequency == 'monthly':
        step_up_interval = 1
    elif step_up_frequency == 'quarterly':
        step_up_interval = 3
    elif step_up_frequency == 'half-yearly':
        step_up_interval = 6
    elif step_up_frequency == 'annually':
        step_up_interval = 12
    else:
        raise ValueError("Invalid step-up frequency. Choose 'monthly', 'quarterly', 'half-yearly', or 'annually'.")

    total_value = 0
    total_investment = 0
    monthly_data = []

    current_investment = initial_investment  # Set the initial investment amount

    for month in range(1, months + 1):
        # Step up the investment only at specified intervals (monthly, quarterly, etc.)
        if month > 1 and (month - 1) % step_up_interval == 0:
            current_investment *= (1 + step_up_percentage / 100)
        
        total_investment += current_investment
        # Compound the investment for the remaining months
        future_value = current_investment * ((1 + monthly_rate) ** (months - month + 1))
        total_value += future_value
        
        # Store the monthly details: month number, investment, and future value
        monthly_data.append([month, round(current_investment, 2), round(future_value, 2)])

    total_returns = total_value - total_investment
    return round(total_investment, 2), round(total_returns, 2), round(total_value, 2), monthly_data

def write_to_csv(filename, data, total_investment, total_returns, total_value):
   
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Month", "Monthly Investment", "Future Value"])
        # Write monthly data
        writer.writerows(data)
        # Write summary at the end
        writer.writerow([])
        writer.writerow(["Total Investment", total_investment])
        writer.writerow(["Total Returns", total_returns])
        writer.writerow(["Final Value (Investment + Returns)", total_value])

# Example usage
initial_investment = 10000  # Initial SIP amount
step_up_percentage = 20     # Step-up percentage each interval
rate_of_return = 18        # Annual rate of return in percentage
months = 48                # Duration of SIP in months
step_up_frequency = 'quarterly'  # Choose 'monthly', 'quarterly', 'half-yearly', or 'annually'

# Calculate SIP returns with step-up
total_investment, total_returns, total_value, monthly_data = calculate_sip_returns_with_step_up_percentage(
    initial_investment, step_up_percentage, rate_of_return, months, step_up_frequency
)

# Output results
print(f"Total Investment: ₹{total_investment}")
print(f"Total Returns: ₹{total_returns}")
print(f"Final Value (Investment + Returns): ₹{total_value}")

# Write results to CSV
csv_filename = "sip_step_up_results.csv"
write_to_csv(csv_filename, monthly_data, total_investment, total_returns, total_value)
print(f"Results written to {csv_filename}")