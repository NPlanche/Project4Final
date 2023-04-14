#Store all the views 
from flask import Blueprint, render_template

#Blueprint of our application
#all urls 

views = Blueprint('views',__name__)

#define route
#home
@views.route('/')
#when / is hit def will run
def home():
    return render_template('home.html')

