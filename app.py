app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        conn = pymysql.connect(
            host='database-1.cte684ksi589.ap-south-1.rds.amazonaws.com',    # e.g., mydb.xxxxx.us-east-1.rds.amazonaws.com
            user='admin',
            password='admin123',
            database='myappdb'
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# Home route
@app.route('/')
def home():
    html_form = """
    <h1>Welcome to Laptop Orders!</h1>
    <form action="/order" method="POST">
        Name: <input type="text" name="name" required><br>
        Laptop: <input type="text" name="laptop" required><br>
        Price: <input type="number" name="price" required><br>
        <input type="submit" value="Order">
    </form>
    """
    return render_template_string(html_form)

# Order submission route
@app.route('/order', methods=['POST'])
def order_laptop():
    try:
        name = request.form.get('name')
        laptop = request.form.get('laptop')
        price = request.form.get('price')

        if not name or not laptop or not price:
            return "Error: All fields are required!", 400

        conn = get_db_connection()
        if conn is None:
            return "Error: Could not connect to the database.", 500

        cursor = conn.cursor()
        sql = "INSERT INTO orders (customer_name, laptop_model, price) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, laptop, price))
        conn.commit()
        cursor.close()
        conn.close()

        return f"Thank you {name}, your order has been placed successfully!"

    except Exception as e:
        print(f"Error processing order: {e}")
        return f"Internal Server Error: {e}", 500

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)