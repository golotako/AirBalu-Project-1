'''
This is a SQLite3 database for the Airbalu project,With Flask app.
We will use this database to store the users' data.
Or delete it and create a new one.'''

# import variables
import sqlite3
import logging

#import flask
from flask import Flask, render_template, request, redirect, url_for, flash,request,session
import requests
import random

# create logging

logging.basicConfig(filename='airbalu.log',level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')




# create a database connection
c=sqlite3.connect('airbalu.db')
# create cursor
cursor=c.cursor()
# create table
cursor.execute("""CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    password VARCHAR(20),
                    full_name VARCHAR(50),
                    real_id VARCHAR(12) UNIQUE
                    
                    )""")
# commit changes
c.commit()
# make new table
cursor.execute("""CREATE TABLE Tickets (
                        ticket_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        flight_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        )""")
c.commit()
# make new table
cursor.execute("""CREATE TABLE Flights (
                        flight_id INTEGER PRIMARY KEY,
                        timestamp datetime,
                        remaining_seats INTEGER,
                        origin_country_id INTEGER,
                        destination_country_id INTEGER,
                        FOREIGN KEY (origin_country_id) REFERENCES Countries(country_id),
                        FOREIGN KEY (destination_country_id) REFERENCES Countries(country_id),
                        FOREIGN KEY (flight_id) REFERENCES Tickets(flight_id)
                        )""")
c.commit()
# make new table
cursor.execute("""CREATE TABLE Countries (
                        country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name varChar (50)
                        )""")

# commit changes
c.commit()

#insert countries into the table Countries
cursor.execute("""INSERT INTO Countries (name) VALUES ('Israel')""")
cursor.execute("""INSERT INTO Countries (name) VALUES ('United States')""")
cursor.execute("""INSERT INTO Countries (name) VALUES ('England')""")
cursor.execute("""INSERT INTO Countries (name) VALUES ('France')""")
cursor.execute("""INSERT INTO Countries (name) VALUES ('Japan')""")
cursor.execute("""INSERT INTO Countries (name) VALUES ('Singapore')""")
cursor.execute("""INSERT INTO Countries (name) VALUES ('UEA')""")
c.commit()

#insert flights into the table Flights
cursor.execute("""INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (1000,'2020-01-01 00:00:00',100,1,2)""")
cursor.execute("""INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (2000,'2020-01-01 00:00:30',100,1,3)""")
cursor.execute("""INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (3000,'2020-01-01 00:01:00',100,1,4)""")
cursor.execute("""INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (4000,'2020-01-01 00:01:30',100,1,5)""")
cursor.execute("""INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (5000,'2020-01-01 00:02:00',100,1,6)""")
cursor.execute("""INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (6000,'2020-01-01 00:02:30',100,1,7)""")
c.commit()

#insert admin user to user table
cursor.execute ("""INSERT INTO users (email,password,full_name,real_id) VALUES ('admin@admin.com','admin','admin','123456789')""")
c.commit()
#close the connection
c.close()




app= Flask(__name__)

# Home page
@app.route('/')
def home():
    logging.info('Home page was loaded')
    return render_template('home.html')

# About page
@app.route('/Aboutus')
def about():
    logging.info('About page was loaded')
    return render_template('Aboutus.html')

# Contact page
@app.route('/Contactus')
def contact():
    logging.info('Contact page was loaded')
    return render_template('Contactus.html')


'*********************************'
# from here until the another ** comment is the client side
'*********************************'


# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # set secret key
    app.secret_key = 'mysecret'
    # if request method is post
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        real_id = request.form.get('real_id')
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
        cursor.execute('INSERT INTO users (email, full_name, password, real_id) VALUES (?, ?, ?, ?)', (email, full_name, password, real_id))
        db.commit()
        logging.info('User registered')
        return redirect(url_for('afterregister'))
    return render_template('register.html')

# after register page
@app.route('/afterregister')
def afterregister():
    logging.info('After register page was loaded')
    return render_template('afterregister.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        account = cur.fetchone()
        if account:
            session['logged_in'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            session['full_name'] = account[3]
            session['real_id'] = account[4]
            logging.info('User logged in')
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    return render_template('login.html')

# logout page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('full_name', None)
    session.pop('real_id', None)
    logging.info('User logged out')
    return redirect(url_for('home'))



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    logging.info('Dashboard page was loaded')
    return render_template('dashbord.html',full_name=session['full_name'])

@app.route('/destination', methods=['GET'])
def destination():
    logging.info('Destination page was loaded')
    return render_template('destination.html')



#build book page
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        email = request.form['email']
        full_name = request.form['full_name']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND full_name = ?', (email, full_name))
        account = cur.fetchone()
        if account:  # if account exists
            destination_country_id = request.form['destination_country_id']
            how_many_seats = request.form['seatnumber']
            with sqlite3.connect('airbalu.db') as db:
                cursor = db.cursor()
                if destination_country_id == '2':
                    cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(random.randint(1,100),account[0],1000))
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    db.commit()
                    logging.info('User booked ticket to country 2')
                    return redirect(url_for('dashboard'))
                elif destination_country_id == '3':
                    cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(random.randint(1,100),account[0],2000))
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    db.commit()
                    logging.info('User booked ticket to country 3')
                    return redirect(url_for('dashboard'))
                elif destination_country_id == '4':
                    cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(random.randint(1,100),account[0],3000))
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    db.commit()
                    logging.info('User booked ticket to country 4')
                    return redirect(url_for('dashboard'))
                elif destination_country_id == '5':
                    cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(random.randint(1,100),account[0],4000))
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    db.commit()
                    logging.info('User booked ticket to country 5')
                    return redirect(url_for('dashboard'))
                elif destination_country_id == '6':
                    cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(random.randint(1,100),account[0],5000))
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    db.commit()
                    logging.info('User booked ticket to country 6')
                elif destination_country_id == '7':
                    cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(random.randint(1,100),account[0],6000))
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    db.commit()
                    logging.info('User booked ticket to country 7')
                    return redirect(url_for('dashboard'))
                else:
                    logging.error('User tried to book a ticket to a country that does not exist')
                    return redirect(url_for('book'))
    return render_template('book.html')


# contact page
@app.route('/Contactus', methods=['GET', 'POST'])
def Contact():
    logging.info('Contact page was loaded')
    return render_template('Contactus.html')


# display user flights in myflight page
@app.route('/myflight', methods=['GET', 'POST'])
def myflight():
    con=sqlite3.connect('airbalu.db')
    cur=con.cursor()
    cur.execute('SELECT * FROM Tickets WHERE user_id = ?', (session['id'],))
    account = cur.fetchall()
    logging.info('User flights were loaded')
    return f'Ticket ID: {account[0][0]} User ID: {account[0][1]} Flight ID: {account[0][2]}'

# delete flight
@app.route('/remove', methods=['GET','DELETE','POST'])
def remove():
    if request.method == 'POST':
        email=request.form['email']
        full_name=request.form['full_name']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND full_name = ?', (email, full_name))
        account = cur.fetchone()
        if account:
            how_many_seats = request.form['seatnumber']
            destination_country_id = request.form['destination_country_id']
            with sqlite3.connect('airbalu.db') as db:
                cursor = db.cursor()
                # check if the user has booked the flight
                cursor.execute('SELECT * FROM Tickets WHERE user_id = ?', (account[0],))
                flight = cursor.fetchone()
                if flight:
                    cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats + ? WHERE destination_country_id = ?', (how_many_seats, destination_country_id))
                    cursor.execute('DELETE FROM Tickets WHERE user_id = ?', (account[0],))
                    db.commit()
                    logging.info('User deleted flight')
                    return redirect(url_for('dashboard'))
                else:
                    logging.error('User tried to delete a flight that does not exist')
                    return redirect(url_for('dashboard'))
    return render_template('remove.html')


'****************************************'
# Here is the rest web service part, Powerd by admin user
'****************************************'

# log in as admin to access the admin page
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    app.secret_key="apple"
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        account = cur.fetchone()
        if account:
            session['logged_in'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            session['full_name'] = account[3]
            session['real_id'] = account[4]
            logging.info('Admin logged in')
            return redirect(url_for('admindashboard'))
        else:
            logging.error('Admin tried to log in with wrong credentials')
            return render_template('adminlogin.html')
    return render_template('adminlogin.html')

# admin dashboard

@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    if 'logged_in' in session:
        logging.info('Admin dashboard was loaded')
        return render_template('admindashboard.html')
    return redirect(url_for('adminlogin'))

# flight  page
@app.route('/flights', methods=['GET', 'POST'])
def flight():
    logging.info('Flight page was loaded')
    return render_template('flight.html')



# get all flights
@app.route('/getflight', methods=['GET', 'POST'])
def getflight():
    con=sqlite3.connect('airbalu.db')
    cur=con.cursor()
    cur.execute('SELECT * FROM Flights')
    account = cur.fetchall()
    logging.info('All flights were loaded')
    return f'{account}'

# add flight
@app.route('/addflight', methods=['GET', 'POST'])
def addflight():
    if request.method == 'POST':
        flight_id = request.form['flight_id']
        timeStamp=request.form['timestamp']
        remaining_seats = request.form['remaining_seats']
        origin_country_id = request.form['origin_country_id']
        destination_country_id = request.form['destination_country_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO Flights (flight_id,timestamp,remaining_seats,origin_country_id,destination_country_id) VALUES (?,?,?,?,?)',(flight_id,timeStamp,remaining_seats,origin_country_id,destination_country_id))
            db.commit()
            logging.info('Flight was added')
            return redirect(url_for('admindashboard'))
    return render_template('addflight.html')

# get flight by id
@app.route('/getidf', methods=['GET', 'POST'])
def getidf():
    if request.method == 'POST':
        flight_id = request.form['flight_id']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM Flights WHERE flight_id = ?', (flight_id,))
        account = cur.fetchall()
        logging.info('Flight by id  was loaded')
        return f'{account}'
    return render_template('getidf.html')

# change flight
@app.route('/changeflight', methods=['GET', 'POST'])
def changeflight():
    if request.method == 'POST':
        flight_id = request.form['flight_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Flights WHERE flight_id = ?', (flight_id,))
            account = cursor.fetchone()
            if account:
                flight_id_new = request.form['flight_id_new']
                timestamp_new = request.form['timestamp_new']
                remaining_seats_new = request.form['remaining_seats_new']
                origin_country_id_new = request.form['origin_country_id_new']
                destination_country_id_new = request.form['destination_country_id_new']
                cursor.execute('UPDATE Flights SET flight_id = ?, timestamp = ?, remaining_seats = ?, origin_country_id = ?, destination_country_id = ? WHERE flight_id = ?', (flight_id_new,timestamp_new,remaining_seats_new,origin_country_id_new,destination_country_id_new,flight_id))
                cursor.execute('UPDATE Tickets SET flight_id = ? WHERE flight_id = ?', (flight_id_new,flight_id))
                db.commit()
                logging.info('Flight was changed')
                return redirect(url_for('admindashboard'))
            else:
                logging.error('Admin tried to change a flight that does not exist')
                return redirect(url_for('admindashboard'))
    return render_template('changeflight.html')

# delete flight
@app.route('/deleteflight', methods=['GET', 'POST'])
def deleteflight():
    if request.method == 'POST':
        flight_id = request.form['flight_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Flights WHERE flight_id = ?', (flight_id,))
            account = cursor.fetchone()
            if account:
                cursor.execute('DELETE FROM Flights WHERE flight_id = ?', (flight_id,))
                cursor.execute('DELETE FROM Tickets WHERE flight_id = ?', (flight_id,))
                db.commit()
                logging.info('Flight was deleted')
                return redirect(url_for('admindashboard'))
            else:
                logging.error('Admin tried to delete a flight that does not exist')
                return redirect(url_for('admindashboard'))
    return render_template('deleteflight.html')

# users page
@app.route('/users', methods=['GET', 'POST'])
def users():
    logging.info('Users page was loaded')
    return render_template('users.html')

# get all users
@app.route('/getusers', methods=['GET', 'POST'])
def getusers():
    con=sqlite3.connect('airbalu.db')
    cur=con.cursor()
    cur.execute('SELECT * FROM Users')
    account = cur.fetchall()
    logging.info('All users were loaded')
    return f'{account}'

# get user by id
@app.route('/getidu', methods=['GET', 'POST'])
def getidu():
    if request.method == 'POST':
        user_id = request.form['user_id']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
        account = cur.fetchall()
        logging.info('User by id  was loaded')
        return f'{account}'
    return render_template('getidu.html')

# add user
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        user_id=request.form['user_id']
        password=request.form['password']
        email=request.form['email']
        full_name=request.form['full_name']
        real_id=request.form['real_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO Users (id,password,email,full_name,real_id) VALUES (?,?,?,?,?)',(user_id,password,email,full_name,real_id))
            db.commit()
            logging.info('User was added')
            return redirect(url_for('admindashboard'))
    return render_template('adduser.html')

# change user
@app.route('/changeuser', methods=['GET', 'POST'])
def changeuser():
    if request.method == 'POST':
        user_id = request.form['user_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
            account = cursor.fetchone()
            if account:
                user_id_new = request.form['user_id_new']
                password_new = request.form['password_new']
                email_new = request.form['email_new']
                full_name_new = request.form['full_name_new']
                real_id_new = request.form['real_id_new']
                cursor.execute('UPDATE Users SET id = ?, password = ?, email = ?, full_name = ?, real_id = ? WHERE id = ?', (user_id_new,password_new,email_new,full_name_new,real_id_new,user_id))
                cursor.execute('UPDATE Tickets SET user_id = ? WHERE user_id = ?', (user_id_new,user_id))
                db.commit()
                logging.info('User was changed')
                return redirect(url_for('admindashboard'))
            else:
                logging.error('Admin tried to change a user that does not exist')
                return redirect(url_for('admindashboard'))
    return render_template('changeuser.html')

# delete user
@app.route('/deleteuser', methods=['GET', 'POST'])
def deleteuser():
    if request.method == 'POST':
        user_id = request.form['user_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
            account = cursor.fetchone()
            if account:
                cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
                cursor.execute('DELETE FROM Tickets WHERE user_id = ?', (user_id,))
                db.commit()
                logging.info('User was deleted')
                return redirect(url_for('admindashboard'))
            else:
                logging.error('Admin tried to delete a user that does not exist')
                return redirect(url_for('admindashboard'))
    return render_template('deleteuser.html')

# tickets page
@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    logging.info('Tickets page was loaded')
    return render_template('tickets.html')

# get all tickets
@app.route('/getticket', methods=['GET', 'POST'])
def gettickets():
    con=sqlite3.connect('airbalu.db')
    cur=con.cursor()
    cur.execute('SELECT * FROM Tickets')
    account = cur.fetchall()
    logging.info('All tickets were loaded')
    return f'{account}'

# get ticket by id
@app.route('/getidt', methods=['GET', 'POST'])
def getidt():
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM Tickets WHERE ticket_id = ?', (ticket_id,))
        account = cur.fetchall()
        logging.info('Ticket by id  was loaded')
        return f'{account}'
    return render_template('getidt.html')

# add ticket
@app.route('/addticket', methods=['GET', 'POST'])
def addticket():
    if request.method == 'POST':
        ticket_id=request.form['ticket_id']
        user_id=request.form['user_id']
        flight_id=request.form['flight_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO Tickets (ticket_id,user_id,flight_id) VALUES (?,?,?)',(ticket_id,user_id,flight_id))
            cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats - 1 WHERE flight_id = ?', (flight_id,))
            db.commit()
            logging.info('Ticket was added')
            return redirect(url_for('admindashboard'))
    return render_template('addticket.html')

# delete ticket
@app.route('/deleteticket', methods=['GET', 'POST'])
def deleteticket():
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Tickets WHERE ticket_id = ?', (ticket_id,))
            account = cursor.fetchone()
            if account:
                cursor.execute('DELETE FROM Tickets WHERE ticket_id = ?', (ticket_id,))
                cursor.execute('UPDATE Flights SET remaining_seats = remaining_seats + 1 WHERE flight_id = ?', (account[2],))
                db.commit()
                logging.info('Ticket was deleted')
                return redirect(url_for('admindashboard'))
            else:
                logging.error('Admin tried to delete a ticket that does not exist')
                return redirect(url_for('admindashboard'))
    return render_template('deleteticket.html')

# countries page
@app.route('/countries', methods=['GET', 'POST'])
def countries():
    logging.info('Countries page was loaded')
    return render_template('countries.html')

# get all countries
@app.route('/getcountries', methods=['GET', 'POST'])
def getcountries():
    con=sqlite3.connect('airbalu.db')
    cur=con.cursor()
    cur.execute('SELECT * FROM Countries')
    account = cur.fetchall()
    logging.info('All countries were loaded')
    return f'{account}'

# get country by id
@app.route('/getidc', methods=['GET', 'POST'])
def getidc():
    if request.method == 'POST':
        country_id = request.form['country_id']
        con=sqlite3.connect('airbalu.db')
        cur=con.cursor()
        cur.execute('SELECT * FROM Countries WHERE country_id = ?', (country_id,))
        account = cur.fetchall()
        logging.info('Country by id  was loaded')
        return f'{account}'
    return render_template('getidc.html')

# add country
@app.route('/addcountry', methods=['GET', 'POST'])
def addcountry():
    if request.method == 'POST':
        country_id=request.form['country_id']
        country_name=request.form['name']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO Countries (country_id,name) VALUES (?,?)',(country_id,country_name))
            db.commit()
            logging.info('Country was added')
            return redirect(url_for('admindashboard'))
    return render_template('addcountry.html')

# change country
@app.route('/changecountry', methods=['GET', 'POST'])
def changecountry():
    if request.method == 'POST':
        country_id = request.form['country_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Countries WHERE country_id = ?', (country_id,))
            account = cursor.fetchone()
            if account:
                country_id_new = request.form['country_id_new']
                country_name_new = request.form['name_new']
                cursor.execute('UPDATE Countries SET country_id = ?, name = ? WHERE country_id = ?', (country_id_new,country_name_new,country_id))
                try:
                    cursor.execute('UPDATE Flights SET destination_country_id = ? WHERE destination_country_id = ?', (country_id_new,country_id))
                    db.commit()
                except:

                    db.commit()
                    logging.info('Country was changed')
                    return redirect(url_for('admindashboard'))
            else:
                    logging.error('Admin tried to change a country that does not exist')
                    return redirect(url_for('admindashboard'))
    return render_template('changecountry.html')

# delete country
@app.route('/deletecountry', methods=['GET', 'POST'])
def deletecountry():
    if request.method == 'POST':
        country_id = request.form['country_id']
        with sqlite3.connect('airbalu.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Countries WHERE country_id = ?', (country_id,))
            account = cursor.fetchone()
            if account:
                cursor.execute('DELETE FROM Countries WHERE country_id = ?', (country_id,))
                cursor.execute('DELETE FROM Flights WHERE destination_country_id = ?', (country_id,))
                db.commit()
                logging.info('Country was deleted')
                return redirect(url_for('admindashboard'))
            else:
                logging.error('Admin tried to delete a country that does not exist')
                return redirect(url_for('admindashboard'))
    return render_template('deletecountry.html')

