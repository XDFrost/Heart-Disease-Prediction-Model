from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail



app = Flask(__name__)


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

    
local_server = params['local_server']


if(local_server == "True"):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_URI']   


app.secret_key = params['secret_key']


app.config.update(                                       # Sending mail
    MAIL_SERVER = params['MAIL_SERVER'],                 # Default gmail server
    MAIL_PORT = params['MAIL_PORT'],                     # Default gmail port
    MAIL_USE_SSL = True,                                 # Using authentication
    MAIL_USERNAME = params['MAIL_USERNAME'],             # fetching mail
    MAIL_PASSWORD = params['MAIL_PASSWORD'],             # fetching app pass
)
mail = Mail(app)  


db = SQLAlchemy(app)


class users(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    Phone_num = db.Column(db.String(80), nullable=False)
    Mail_id = db.Column(db.String(80), unique = True, nullable=False)


class contact(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    contact_name = db.Column(db.String(220), nullable=False)
    contact_email = db.Column(db.String(220), nullable=False)
    contact_phone_num = db.Column(db.String(220), nullable=False)
    contact_message = db.Column(db.String(220), nullable=False)


@app.route('/')
def index():
    return render_template('initial_page.html', params = params)


@app.route('/login_page', methods = ['GET', 'POST'])
def login_page():
    if(request.method == 'POST'):
        # Fetching entry
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        user = users.query.filter_by(Username = Username).first()
        if(user):
            if(user.Password == Password):
                return render_template('home_page.html', params = params)
            flash('Invalid Username or Password. Please Check your Username or Password.')
            return render_template('login_page.html', params = params)
        else:
            flash('You are not registered. Please Sign Up.')
            return render_template('login_page.html', params = params)
                
    return render_template('login_page.html', params = params)


@app.route('/signup_page', methods = ['GET', 'POST'])
def signup_page():
    if(request.method == 'POST'):
        # Fetching entry
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        Phone_num = request.form.get('Phone_num')
        Mail_id = request.form.get('Mail_id')
        user = users.query.filter_by(Username = Username).first()
        mail = users.query.filter_by(Mail_id = Mail_id).first()
        if(user):
            flash('Username already exists. Please try another Username.')
            return render_template('signup.html', params = params)
        elif(mail):
            flash('Mail Id already exists. Please try another Mail Id.')
            return render_template('signup.html', params = params)
        else:
            # Add entry to the database
            entry = users(Username = Username, Password = Password, Phone_num = Phone_num, Mail_id = Mail_id)
            db.session.add(entry)
            db.session.commit()
            return render_template('home_page.html', params = params)
        
    return render_template('signup.html', params = params)


@app.route('/home_page', methods = ['GET', 'POST'])
def home_page():
    return render_template('home_page.html', params = params)


@app.route('/contact_page', methods = ['GET', 'POST'])
def contact_page():
    if(request.method == "POST"):
        # Fetching entry
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        contact_phone_num = request.form.get('contact_phone_num')
        contact_message = request.form.get('contact_message')
        
        # Add entry to the database
        entry = contact(contact_name = contact_name, contact_email = contact_email, contact_phone_num = contact_phone_num, contact_message = contact_message)
        db.session.add(entry)
        db.session.commit()
    
        #sending mail
        mail.send_message('CONTACT MESSAGE RECEIVED',
                          sender = params['MAIL_USERNAME'],
                          recipients = [contact_email, params['MAIL_USERNAME']],
                          body = "Here are your contents: " + "\n" + "\n" + 
                          "Name: " + contact_name + "\n" +
                          "Email: " + contact_email + "\n" +
                          "Phone number: " + contact_phone_num + "\n" +
                          "Message sent: " + contact_message)
        
        return render_template('home_page.html', params = params)
        
    return render_template('contact_page.html', params = params)


if __name__ == '__main__':
    app.run(debug=True)
    