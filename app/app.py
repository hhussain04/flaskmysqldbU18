from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from functools import wraps
import secrets
import sys
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'silverdawncoaches'

app.secret_key = secrets.token_hex(16)
ADMIN_PASSWORD = "root"
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/exit')
def exit_app():
    sys.exit(0) 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        session['next'] = request.url
        return redirect(url_for('login'))
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = session.get('next', url_for('index'))
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(next_page)
        else:
            error = 'Invalid password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/new_information')
def new_information():
    return render_template('new_information.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['surname']
        email = request.form['email']
        address_line_1 = request.form['address_line_1']
        address_line_2 = request.form['address_line_2']
        city = request.form['city']
        postcode = request.form['postcode']
        phone_number = request.form['phone_number']
        special_notes = request.form['special_notes']

        # Insert data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO customer (first_name, last_name, email, address_line_1, address_line_2, city, postcode, phone_number, special_notes)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',  
                       (first_name, last_name, email, address_line_1, address_line_2, city, postcode, phone_number, special_notes))
        mysql.connection.commit()
        cursor.close()

        return render_template('add/customer.html', success=True)

    return render_template('add/customer.html')

@app.route('/add_trip', methods=['GET', 'POST'])
@login_required
def add_trip():
    if request.method == 'POST':
        # Get form data
        destination_id = request.form['destination']
        coach_id = request.form['coach']
        driver_id = request.form['driver']
        trip_date = request.form['trip_date']

        # Insert data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO trip (destination_id, 
                       coach_id, driver_id, 
                       trip_date)
                          VALUES (%s, %s, %s, %s)''',
                       (destination_id, coach_id, 
                        driver_id, trip_date))
        mysql.connection.commit()
        cursor.close()

        return render_template('add/trip.html', success=True)

    # Fetch existing destinations, coaches, and drivers
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT destination_id, destination_name FROM destination')
    destinations = cursor.fetchall()
    cursor.execute('SELECT coach_id, coach_registration FROM coach')
    coaches = cursor.fetchall()
    cursor.execute('SELECT driver_id, CONCAT(driver_first_name, " ", driver_last_name) AS name FROM driver')
    drivers = cursor.fetchall()
    cursor.close()

    return render_template('add/trip.html', destinations=destinations, coaches=coaches, drivers=drivers)

@app.route('/add_destination', methods=['GET', 'POST'])
@login_required
def add_destination():
    if request.method == 'POST':
        try:
            # Get form data
            destination_name = request.form['destination_name']
            destination_hotel = request.form['destination_hotel']
            destination_city = request.form['destination_city']
            destination_cost = request.form['destination_cost']
            number_of_days = request.form['number_of_days']

            # Insert data into the database
            cursor = mysql.connection.cursor()
            cursor.execute('''INSERT INTO destination (destination_name, destination_hotel, destination_city,
                           destination_cost, number_of_days)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (destination_name, destination_hotel, destination_city, destination_cost, number_of_days))
            mysql.connection.commit()
            cursor.close()

            return render_template('add/destination.html', success=True)
        except Exception as e:
            return str(e), 500

    return render_template('add/destination.html')

@app.route('/add_driver', methods=['GET', 'POST'])
@login_required
def add_driver():
    if request.method == 'POST':
        # Get form data
        driver_firstname = request.form['first_name']
        driver_lastname = request.form['last_name']

        # Insert data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO driver (driver_first_name, driver_last_name)
                          VALUES (%s, %s)''',
                       (driver_firstname, driver_lastname))
        mysql.connection.commit()
        cursor.close()

        return render_template('add/driver.html', success=True)

    return render_template('add/driver.html')

@app.route('/add_coach', methods=['GET', 'POST'])
@login_required
def add_coach():
    if request.method == 'POST':
        # Get form data
       
        reg_number = request.form['reg_number']
        print(reg_number)
        num_of_seats = request.form['seating_capacity']
        
        # Insert data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO coach (coach_registration, num_of_seats)
                          VALUES (%s, %s)''',
                       (reg_number, num_of_seats))
        mysql.connection.commit()
        cursor.close()

        return render_template('add/coach.html', success=True)

    return render_template('add/coach.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()

    columns = []
    results = []
    selected_table = None
    selected_column = None

    if request.method == 'POST':
        selected_table = request.form['table']
        selected_column = request.form['column']
        search_value = request.form['search']
        
    elif request.method == 'GET':
        selected_table = request.args.get('table')
        selected_column = request.args.get('column')
        search_value = request.args.get('search')

    print(f"Selected Table: {selected_table}")
    print(f"Selected Column: {selected_column}")
    print(f"Search Value: {search_value}")

    if selected_table:
        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        columns = [column['Field'] for column in cursor.fetchall()]

    if selected_table and selected_column:
        if search_value:
            if selected_column == '*':
                query = f"SELECT * FROM {selected_table} WHERE CONCAT_WS(' ', {', '.join(columns)}) LIKE %s"
                cursor.execute(query, (f"%{search_value}%",))
            else:
                query = f"SELECT {selected_column} FROM {selected_table} WHERE {selected_column} LIKE %s"
                cursor.execute(query, (f"%{search_value}%",))
        else:
            if selected_column == '*':
                query = f"SELECT * FROM {selected_table}"
            else:
                query = f"SELECT {selected_column} FROM {selected_table}"
            cursor.execute(query)
        
        results = cursor.fetchall()
        print(f"Query: {query}")
        print(f"Results: {results}")

    return render_template('search.html', tables=tables, columns=columns, 
                           results=results, selected_table=selected_table, 
                           selected_column=selected_column)

@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    # Fetch all necessary data for the form (used in both GET and POST)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get customers for dropdown
    cursor.execute('SELECT customer_id, CONCAT(first_name, " ", last_name) AS customer_name FROM customer')
    customers = cursor.fetchall()
    
    # Get destinations for potential filtering
    cursor.execute('SELECT destination_id, destination_name FROM destination')
    destinations = cursor.fetchall()
    
    # Get trips with seat information
    cursor.execute('''SELECT trip.trip_id, trip.destination_id, trip.trip_date, coach.num_of_seats 
                      FROM trip 
                      JOIN coach ON trip.coach_id = coach.coach_id''')
    trips = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        # Process form data
        trip_id = request.form['trip_date']
        customer_id = request.form['customer']
        special_notes = request.form.get('special_notes', '')
        selected_seats = request.form.getlist('selected_seats')
        print(selected_seats)
        selected_seats = selected_seats[0].split(',')
        num_people = len(selected_seats)
        print(num_people)

        # Calculate booking cost
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''SELECT destination_cost FROM destination 
                          JOIN trip ON destination.destination_id = trip.destination_id 
                          WHERE trip.trip_id = %s''', (trip_id,))
        destination = cursor.fetchone()
        destination_cost = destination['destination_cost']
        booking_cost = num_people * destination_cost
        booking_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Insert booking
        try:
            cursor.execute('''INSERT INTO booking 
                            (trip_id, num_of_people, customer_id, booking_cost, special_request, booking_date)
                            VALUES (%s, %s, %s, %s, %s, %s)''',
                           (trip_id, num_people, customer_id, booking_cost, special_notes, booking_date))
            mysql.connection.commit()
            success = True
        except Exception as e:
            success = False
            print(f"Error: {e}")
        finally:
            cursor.close()

        return render_template('add/booking.html',
                               success=success,
                               customers=customers,
                               destinations=destinations,
                               trips=trips)

    # GET request - show empty form
    return render_template('add/booking.html',
                           customers=customers,
                           destinations=destinations,
                           trips=trips)

@app.route('/get_booked_seats')
def get_booked_seats():
    trip_id = request.args.get('trip_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT SUM(num_of_people) AS booked_seats FROM booking WHERE trip_id = %s''', (trip_id,))
    result = cursor.fetchone()
    cursor.close()

    booked_seats = result['booked_seats'] if result['booked_seats'] is not None else 0

    return jsonify({'booked_seats': booked_seats})
    

if __name__ == "__main__":
    app.run(debug=True)