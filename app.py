from flask import Flask, request, render_template,redirect, url_for
import mysql.connector
from datetime import date

app = Flask(__name__)

# Connect Flask to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",  # Replace with your MySQL password if you have one
    database="electricity_db"
)

# Route to display the bill form
@app.route('/')
def home():
    return render_template('bill_form.html')

# Route to handle bill calculation
@app.route('/calculate_bill', methods=['POST'])
def calculate_bill():
    user_id = request.form['user_id']
    units = float(request.form['units'])
    
    # Check if User ID exists in the users table
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        return f"Error: User ID {user_id} does not exist! Please enter a valid User ID."

    # Bill calculation logic
    rate_per_unit = 5  # Example: Rs. 5 per unit
    bill_amount = units * rate_per_unit
    
    # Insert the bill into the database
    cursor.execute("INSERT INTO bills (user_id, units_consumed, bill_amount, billing_date) VALUES (%s, %s, %s, %s)",
                   (user_id, units, bill_amount, date.today()))
    db.commit()
    cursor.close()

    return redirect(url_for('view_bills'))
    
   # return f"Bill Generated Successfully for User ID {user_id}! Amount: Rs. {bill_amount}"

# Route to display all bills in a table
@app.route('/view_bills')
def view_bills():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bills")
    bills = cursor.fetchall()
    cursor.close()
    return render_template('view_bills.html', bills=bills)

if __name__ == "__main__":
    app.run(debug=True)
