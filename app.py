from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DB_URL = os.environ.get("DATABASE_URL")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        product = request.form.get('product')

        try:
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, name TEXT, phone TEXT, address TEXT, product TEXT);")
            cur.execute("INSERT INTO orders (name, phone, address, product) VALUES (%s, %s, %s, %s)", (name, phone, address, product))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("Database error:", e)
        return redirect('/thankyou')
    return render_template('order.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
