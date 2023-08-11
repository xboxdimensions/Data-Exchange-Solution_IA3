import sqlite3
import requests
from flask import redirect, render_template, request
from flask_login import (UserMixin, current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, login_manager
from app.db import get_db
from config import password, username  # Get sensitive info

proxies = {'http': f'http://{username}:{password}@proxy.eq.edu.au:80',
           'https': f'http://{username}:{password}@proxy.eq.edu.au:80'}  # Proxy Details
url = f"https://api.fda.gov/food/enforcement.json?limit=1000&sort=report_date:desc"  # FDA API

context = app.app_context()
context.push()


class User(UserMixin): #Define User class and details
    def __init__(self, email):
        self.email = email
    def get_id(self):
        return self.email


@login_manager.user_loader #Loads users based on email supplied
def load_user(user_id):
    db = get_db()
    user_search = db.execute(
        'SELECT email FROM users WHERE email == ?', (user_id,)).fetchone()
    if user_search:
        user = User(user_search[0]) #Create instance of User class
        return user


@app.route('/logout')
def logout(): #Logs the user out
    logout_user() 
    return redirect('/login')


@app.route("/register", methods=["POST", "GET"]) #Declare route and allowed methods (GET/POST)
def index():
    if current_user.is_authenticated:
        return redirect('/')        
    else:
        db = get_db()
        error = None #Text to display if errors occurred.
        if request.method == "POST": #If form is posted
            password = request.form.get("password")
            repeat = request.form.get("repeat") #Get form information
            email = request.form.get("email")
            if password == repeat: #Checks if passwords matched for the user to verify 
                try: #Attempt to add the user’s email + password into the database
                    db.execute("INSERT INTO users (email,passwordHash) VALUES (?,?)", #Registers user
                                (email, generate_password_hash(password, method='pbkdf2:sha512'),)) #Creates passwordhash using specific salt
                    db.commit() #Saves database
                    login_user(User(email)) #Logs the user in
                    return redirect("/") #Redirects to main page
                except sqlite3.IntegrityError: #Since emails are unique, the query will fail if existing emails are entered
                    error = 'Email already taken - Try logging in'
            else:
                error = 'Passwords entered do not match'
    return render_template('register.html', error=error)


@app.route('/login', methods=["POST", "GET"])
def login():
    db = get_db()
    if current_user.is_authenticated: #If users is already logged in
        return redirect('/')        #Go to main page
    else:
        error = None
        if request.method == "POST":
            email = request.form.get("email") #Get data input
            password_entered = request.form.get("password")
            query = db.execute( #Checks if email exists
                "SELECT email,passwordHash FROM users WHERE email ==?", (email,)).fetchone()
            if query:
                if check_password_hash(query['passwordHash'], password_entered): #Check if password is correct
                    login_user(User(email)) #Log user in
                    return redirect('/') #Go to Main Page
                else:
                    error = 'Invalid Credentials'
            else:
                error = 'Invalid Credentials'
    return render_template('login.html', error=error,title='Login')


@app.route('/', methods=["POST", "GET"]) # "/" route and accepted methods
@login_required
def main():
    distpat = ''
    year = 0 #Default values
    db = get_db()
    r = requests.get(url, proxies=proxies)  # Gets API information
    records = r.json()['results'] # assigns the data list inside the JSON to variable
    for info in records:  # Iterates between all records
        result = db.execute(
            'SELECT * FROM FDA_Data WHERE event_id = ?', (info["event_id"],))  # Checks if there is data for the specific time already
        if not result.fetchall(): #If event_id is not present in the database yet
            db.execute('INSERT INTO FDA_Data (event_id, recalling_firm,distribution_pattern, product_description, product_quantity,reason_for_recall, recall_initiation_date, status)'  # Add Required Data to FDA_Data SQL database
                       'VALUES (?,?,?,?,?,?,?,?);', (info["event_id"], info["recalling_firm"], info["distribution_pattern"], info["product_description"],info["product_quantity"],info["reason_for_recall"], info["recall_initiation_date"], info['status']))
            db.commit()  # Save Database
    if request.method == "POST":
        distpat = request.form.get('distpat')
        try:
            year = int(request.form.get('year')) 
        except:
            year = 0 #If the year is none
    query = db.execute(
        'SELECT event_id, recalling_firm, distribution_pattern, product_description, product_quantity, reason_for_recall, recall_initiation_date, status FROM FDA_Data ' #Relevant data
        'WHERE CAST(SUBSTR(recall_initiation_date, 1, 4) AS UNSIGNED) >= ? ' #Where the first 4 numbers (year) are greater than filter
        'AND (CASE WHEN ? != "" THEN distribution_pattern LIKE "%" || ? || "%" ELSE 1 END)', #Filter if distpat is none or something
        (year, distpat, distpat)
    ).fetchall()
    return render_template('main.html', records=query, distpat=distpat, year=year,title="FDA Information")

context.pop()
