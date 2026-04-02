from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
import os
from urllib.parse import urlparse
 
app = Flask(__name__)
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:ygaGBwFeLvWAprSQxTSdpjDLmsNfgSOf@hopper.proxy.rlwy.net:34893/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:ygaGBwFeLvWAprSQxTSdpjDLmsNfgSOf@hopper.proxy.rlwy.net:34893/railway"
 
url = urlparse(db_url)
 


app = Flask(__name__)

# MySQL Database Configuration (XAMPP Default)


def get_db_connection():
    return mysql.connector.connect(host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port)

@app.route('/')
def index():
    # READ: Fetch all records [cite: 37, 38]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', customers=customers)

@app.route('/add', methods=['POST'])
def add_customer():
    # CREATE: Insert new data [cite: 35, 36]
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (name, mobile, amount, location) VALUES (%s, %s, %s, %s)", 
                       (name, mobile, amount, location))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_customer():
    # UPDATE: Modify existing record [cite: 39, 40]
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customer SET mobile=%s, amount=%s, location=%s WHERE name=%s", 
                   (mobile, amount, location, name))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<name>')
def delete_customer(name):
    # DELETE: Remove record [cite: 41, 42]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE name = %s", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=5001)