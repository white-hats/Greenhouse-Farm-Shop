from flask import Flask, render_template,flash,redirect, url_for, session, request, logging
from flaskext.mysql import MySQL
from wtforms import Form, StringField , TextAreaField ,PasswordField , validators, BooleanField
from passlib.hash import sha256_crypt
import mysql.connector
from Crypto.Hash import SHA256

app = Flask(__name__)
app.debug = True

#initializing  MYSQL
mysql = MySQL()

#Config MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Avevor0244166433'
app.config['MYSQL_DATABASE_DB'] = 'greenfarm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

class RegisterForm(Form):
    name = StringField('')
    username = StringField('')
    email = StringField('')
    password = PasswordField('', [validators.EqualTo('confirm',message ='passwords do not match')])
    confirm = PasswordField('')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        #Create cursor
        mysql.get_db()
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO users (fullname, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))
        #commit to Database
        mysql.get_db().commit()
        #Close connection
        cursor.close()
        flash("You are now Registered and you can now login", 'success')
        return redirect(url_for('login'))
        return render_template('login.html')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        #GET FORM FIELDS
        log_email = request.form['Email']
        log_password = request.form['Password']
        #Create cursor
        cursor = mysql.get_db().cursor()
        #GET user by Email
        result = cursor.execute("SELECT * FROM users WHERE email = %s", log_username)
        if result > 0:
            data = cursor.fetchone()
            cursor.execute("SELECT password FROM users WHERE email = %s", log_username)
            for row in cursor.fetchall():
            #Compare passwords
                if sha256_crypt.verify(log_password, row[0]):
                    session['logged_in'] = True
                    session['Email'] = log_username
                    flash('Logged in Succesfully', 'success')
                    return redirect(url_for('index'))
                    return render_template('home.html')
                else:
                    error = 'Username not found'
                    return render_template('login.html', error = error)
                    #Close connection
                    cursor.close()
            else:
                error = 'Username not found'
                return render_template('login.html', error= error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/fruits')
def fruits():
    return render_template('fruits.html')

@app.route('/veges')
def veges():
    return render_template('veges.html')

@app.route('/legumes')
def legumes():
    return render_template('legumes.html')

@app.route('/farmers')
def farmers():
    return render_template('farmers.html')

class FarmerForm(Form):
    name = StringField('')
    username = StringField('')
    email = StringField('')
    password = PasswordField('', [validators.EqualTo('confirm',message ='passwords do not match')])
    confirm = PasswordField('')
    tel = StringField('')

@app.route('/farmerRegister')
def farmerRegister():
    form = FarmerForm(request.form)
    if request.method == 'POST' and form.validate():
        farmer_name = form.name.data
        farmer_username = form.username.data
        farmer_email = form.email.data
        farmer_phone = form.tel.data
        farmer_password = sha256_crypt.encrypt(str(form.password.data))
        #Create cursor
        mysql.get_db()
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO users (fullname, username, email, password, phoneNo) VALUES(%s, %s, %s, %s, %s)", (farmer_name, farmer_username, farmer_email, farmer_password, farmer_phone))
        #commit to Database
        mysql.get_db().commit()
        #Close connection
        cursor.close()
        flash("You are now Registered and you can now login", 'success')
        return redirect(url_for('farmerLogin'))
        return render_template('farmerLogin.html')
    return render_template('farmerRegister.html')

@app.route('/farmerLogin')
def farmerLogin():
    if request.method=='POST':
        #GET FORM FIELDS
        farmer_email = request.form['Email']
        farmer_password = request.form['Password']
        #Create cursor
        cursor = mysql.get_db().cursor()
        #GET user by Email
        result = cursor.execute("SELECT * FROM farmers WHERE email = %s", farmer_email)
        if result > 0:
            data = cursor.fetchone()
            cursor.execute("SELECT password FROM farmers WHERE email = %s", farmer_email)
            for row in cursor.fetchall():
            #Compare passwords
                if sha256_crypt.verify(famer_password, row[0]):
                    session['logged_in'] = True
                    session['Email'] = farmer_email
                    flash('Logged in Succesfully', 'success')
                    return redirect(url_for('index'))
                    return render_template('/farmerRegister')
                else:
                    error = 'Username not found'
                    return render_template('farmerLogin.html', error = error)
                    #Close connection
                    cursor.close()
            else:
                error = 'Username not found'
                return render_template('/farmerLogin', error= error)
    return render_template('farmerLogin.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
