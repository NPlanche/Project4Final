#Store all the views 
from flask import Blueprint, render_template, request, flash

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
    
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #Check if the information is Valid
        if len(email) < 4:
            #send the user an message
            flash('Email must be more that 4 characters', category='error')
        elif len(first_name) < 2:
             #send the user an message
            flash('First Name must be more that 1 characters', category='error')
       
        elif password1 != password2:
             #send the user an message
            flash('Passwords don\'t match.', category='error')
       
        elif len(password1) < 7:
             #send the user an message
            flash('Password must be more that 7 characters', category='error')
       
        else:
            #add user to the database
            flash('Account Created', category='success')
    
    return render_template('signup.html')





