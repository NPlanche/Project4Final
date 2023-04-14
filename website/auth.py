#Store all the views 
from flask import Blueprint, render_template, request

#Blueprint of our application
#all urls 
auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html', b=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    return render_template('signup.html')





