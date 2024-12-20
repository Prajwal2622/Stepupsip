from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from io import StringIO, BytesIO
import csv

app = Flask(__name__)

# Function to calculate SIP returns
def calculate_sip_returns_with_step_up_percentage(initial_investment, step_up_percentage, rate_of_return, months, step_up_frequency):
    monthly_rate = rate_of_return / 100 / 12

    if step_up_frequency == 'monthly':
        step_up_interval = 1
    elif step_up_frequency == 'quarterly':
        step_up_interval = 3
    elif step_up_frequency == 'half-yearly':
        step_up_interval = 6
    elif step_up_frequency == 'annually':
        step_up_interval = 12
    else:
        raise ValueError("Invalid step-up frequency")

    total_value = 0
    total_investment = 0
    monthly_data = []

    current_investment = initial_investment

    for month in range(1, months + 1):
        if month > 1 and (month - 1) % step_up_interval == 0:
            current_investment *= (1 + step_up_percentage / 100)

        total_investment += current_investment
        future_value = current_investment * ((1 + monthly_rate) ** (months - month + 1))
        total_value += future_value
        monthly_data.append([month, round(current_investment, 2), round(future_value, 2)])

    total_returns = total_value - total_investment
    return round(total_investment, 2), round(total_returns, 2), round(total_value, 2), monthly_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data
    initial_investment = float(request.form['initial_investment'])
    step_up_percentage = float(request.form['step_up_percentage'])
    rate_of_return = float(request.form['rate_of_return'])
    months = int(request.form['months'])
    step_up_frequency = request.form['step_up_frequency']

    # Perform SIP calculation
    total_investment, total_returns, total_value, monthly_data = calculate_sip_returns_with_step_up_percentage(
        initial_investment, step_up_percentage, rate_of_return, months, step_up_frequency)

    # Convert data to DataFrame and CSV string
    df = pd.DataFrame(monthly_data, columns=['Month', 'Monthly Investment', 'Future Value'])
    output = StringIO()
    df.to_csv(output, index=False)
    csv_data = output.getvalue()

    # Render result page and pass the CSV data as a hidden field
    return render_template('index.html',
                           total_investment=total_investment,
                           total_returns=total_returns,
                           total_value=total_value,
                           csv_data=csv_data)


@app.route('/signup', methods=['POST'])
def signup():
    # Capture email from the form
    email = request.form['email']
    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Append email to a CSV file
    try:
        with open("emails.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([email])
    except Exception as e:
        return jsonify({"error": "Failed to save email. " + str(e)}), 500

    return jsonify({"success": "Thank you for signing up!"})


@app.route('/download_csv', methods=['POST'])
def download_csv():
    # Retrieve CSV data from the hidden form field
    csv_data = request.form['csv_data']
    buffer = BytesIO()
    buffer.write(csv_data.encode())
    buffer.seek(0)

    return send_file(buffer, mimetype='text/csv', as_attachment=True, download_name='SIP_data.csv')


if __name__ == '__main__':
    app.run(debug=True)
