#Store all the views 
from flask import Blueprint, render_template

#Blueprint of our application
#all urls 
auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html', b=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/signup')
def signup():
    return render_template('signup.html')





