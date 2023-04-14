#Store all the views 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

#Blueprint of our application
#all urls 
auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            #filter the user by their email 
            user = User.query.filter_by(email=email).first()
            if user:
                # compare passwords ie. if the hashes are the same
                if check_password_hash(user.password, password):
                    #success message
                    flash('Logged in successfully!', category='success')
                    #remembers that this user is logged in
                    login_user(user, remember=True)
                    #rediret to home
                    return redirect(url_for('views.home'))
                else:
                    #message error 
                    flash('Incorrect password, try again.', category='error')
            else:
                #error the email does not exists
                flash('Email does not exist.', category='error')

        return render_template("login.html", user=current_user)
    
    
@auth.route('/logout')
#cannot access this unless you are looged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #Check if the information is Valid
        #Search for the given email in the database (only one email per user)
        user = User.query.filter_by(email=email).first()
        #if the email does exist send them an error
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
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
            #get all the information for the new user 
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            #add a new user to the database
            db.session.add(new_user)
            #send to the database
            db.session.commit()
            #remembers the user that is logged in
            login_user(new_user, remember=True)
            #message
            flash('Account created!', category='success')
            #redirect the user to the home page
            return redirect(url_for('views.home'))
                            
    return render_template('signup.html', user=current_user)





