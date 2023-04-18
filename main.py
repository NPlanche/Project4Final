import os
import traceback
from flask import Flask, redirect, request, send_file,render_template,session,url_for

#from PIL import Image
from google.cloud import storage
from pathlib import Path

#request
import requests
from urllib import parse

#Encode and Decode
import base64

#Log In 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import path
from flask_login import LoginManager

#sql server
import pymssql
##from PIL.ExifTags import TAGS
##import sys

app = Flask(__name__)

#Session Secret Key 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#Login
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            passwordHash = password # encriptar password 
            
            print('Email:', email)
            print('Password:', password)
            
            conn = pymssql.connect(server='s23.winhost.com',
                       user='DB_127521_jkeepon_user', 
                       password='ndp1999', 
                       database='DB_127521_jkeepon'
                       )  
            cursor = conn.cursor()  
            cursor.execute("SELECT * FROM Users WHERE Email='"+email+"' AND passwordHash = '" +passwordHash+"'")  
            row = cursor.fetchone()
            exist = False  
            while row:  
                exist = True
                row = cursor.fetchone()
            conn.close()
            if exist:
                session['email'] = email
                print('The user in session in login:', email)
                return redirect(url_for('index'))
              
    return render_template("login.html")

#Register
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        passwordHash = password # encriptar password 
        
        print('Email:', email)
        print('Password:', password)
        
        conn = pymssql.connect(server='s23.winhost.com',
                    user='DB_127521_jkeepon_user', 
                    password='ndp1999', 
                    database='DB_127521_jkeepon'
                    )  
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM Users WHERE Email='"+email+"'")  
        row = cursor.fetchone()
        exist = False  
        while row:  
            exist = True
            row = cursor.fetchone()
        if exist:
            conn.close()
            return redirect('/register')
            
        cursor = conn.cursor()  
        cursor.execute("INSERT Users (Email, PasswordHash) VALUES ('"+email+"'"+",'"+passwordHash+"')")  
        conn.commit()         
           
        conn.close()
        session['email'] = email
        print('The user in session in register:', email)
        return redirect(url_for('index'))
              
    return render_template("signup.html")

#Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#Home
@app.route('/')
def index():
    print("GET /")
    
    # check if the users has logged in or not
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        return redirect('/login')
    else:
        #Use Email to save picture
        user_email = session['email']
        user_email = user_email.replace('%40',"@")
        
        r  = request
        base_url = request.base_url
        
        
        a = request.args
        f = request.full_path
        print(f"Full path: {f}")
        substring = f[0:8]
        
        url = base_url + f
        
        if (substring == '/?image=') and (len(f) > len(substring)) :
            
            urlBase = 'https://storage.googleapis.com/project2database/static/image/'+user_email+'/'
            query = parse.parse_qs(parse.urlparse(url).query)
            query_def_name = query['image'][0]
            query_def_size = query['size'][0]
            query_def_location = query['location'][0]
            query_def_type = query['type'][0]

            
            #Name
            name_string_withemail = string_decode(query_def_name)
            string_to_replace = user_email + '/'
            string_to_replace = string_to_replace.replace('@','%40')
            name_string = name_string_withemail.replace(string_to_replace, '')
            
            src = urlBase + name_string
            print(f"URL: {src}")
            
            #Size
            size_string = string_decode(query_def_size)
            
            #Location 
            location_string = string_decode(query_def_location)
            
            #Type
            type_string = string_decode(query_def_type)
            
            
            
            index_html =""" <style>
            
            .image{
                display: block;
                width: 400px;
                height: 365px;
                padding: 15px;
            }
            
            .container{
                padding:200px 0px;            
            }
            
            .styled-table {
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }
            
            .styled-table thead tr {
                background-color: #2B3467;
                color: #ffffff;
                text-align: left;
            }
            
            .styled-table caption{
                
                text-align: left;
                text-size: 150px;
            }
            
            .styled-table th,
            .styled-table td {
                padding: 12px 15px;
                max-width: 350px;
                overflow-y:hidden;
            }
            
            .styled-table tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            .styled-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #2B3467;
            }
            
            .styled-table tbody tr.active-row {
                font-weight: bold;
                color: #009879;
            }
            
                    button {
                    font-family: 'Source Sans Pro', sans-serif;
                    font-weight: 900;
                    padding: 15px 15px;
                    font-size: 0.7rem;
                    position: relative;
                    width:10%
                    overflow: hidden;
                    border: 0;
                    cursor: pointer;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    background-color :  #FFFFFF;
                    color:  #343a40;
                    border:2px solid #2B3467;
                    
                    }
                    button:hover{
                    color:#FFFFFF;
                    background-color:#B22727;
                    border:2px solid #FFFFFF;
                    }
            
            </style>
            <div class = "container">
                <table>
                    <tr>
                        <td>
                        <img class='image' src='"""
            index_html+= src + "'></td> <td><table class='styled-table'> <caption><h2>Metadata</h2></caption> <thead><tr><th>Category</th><th>Data</th></tr></thead><tbody><tr><td>Filename</td><td>"+name_string+"</td></tr><tr><td>Type</td><td>"+type_string+"</td></tr><tr><td>Size</td><td>"+size_string+"</td></tr><tr><td>Location</td><td>"+location_string+"</td></tr></tbody></table></td></tr> <tr><td></td> <td> <a type='button' href='/delete/"+user_email+"/"+ name_string +"'><button>Delete</button></a></tr></table></div>"""  


            return index_html
        else:
            print("html principal")

            index_html="""<style>
            
            form{
                font-family: "Raleway", Arial, sans-serif
            }
            
            .image{
                margin:5px;
                border: 1px solid #ccc;
                width: 225px;
                height: 225px;
            }
            *{
                background-color: #90EE90;
            }
            
            button{
                background-color: lightgray;
            }
            </style>
            <a href="/logout">logout</a>
            <form method="post" enctype="multipart/form-data" action="/upload" method="post">
                <div>
                    <label for="file">Choose file to upload</label>
                    <input type="file" id="file" name="form_file" accept="image/jpeg"/>
                </div>
                <div>
                    <button>Submit</button>
                </div>
                <hr>
                <h1 class='title'>Gallery</h1>
            
            
        </form>"""
        
        #Use Email to save picture
        user_email = session['email']
        storage_client = storage.Client('Project 2')
        #get the bucket
        bucket = storage_client.get_bucket(app.config['BUCKET'])
        #blobs = bucket.list_blobs(prefix='static/image/')
        blobs = bucket.list_blobs(prefix='static/image/'+user_email+'/')

        for blob in blobs:
            if not blob.name.endswith('/'):
                
                image_url = blob.public_url
                urlBase = 'https://storage.googleapis.com/project2database/static/image/'+user_email+'/'
                image_name = image_url[61:len(image_url)]
                
                #Encoding
                base64_name = string_encode(image_name) 
                
                #Encoding 
                #Size
                size = str(blob.size)
                base64_size = string_encode(size) 
                
                #Encoding
                #Location
                location = str(blob.public_url)
                base64_location = string_encode(location) 
                
                #Encoding
                #Type
                type = str(blob.content_type)
                base64_type = string_encode(type) 
                
                index_html += "<a href='"+ base_url +"/?image="+ base64_name +"&size="+base64_size+"&location="+base64_location+"&type="+base64_type+"'><img class='image' src='" + blob.public_url + "'></a>"

        return index_html

#Upload Image
@app.route('/upload', methods = ['POST'])
def upload():   
     
    try:
        print("POST /upload")
        file = request.files['form_file']
        #file.save(os.path.join("./files", file.filename))
        file.save(os.path.join("./static/image/", file.filename))
        
        #Use Email to save picture
        user_email = session['email']

        save_picture(file.filename, user_email)
        download_picture()
        print("///////////////////////////////////Download was a Success////////////////////////////")
    except:
        traceback.print_exc()
        #change later
    # except Exception as err:
    #     print(f"Unexpected {err=}, {type(err)=}")
    return redirect('/')

@app.route('/static/image/')
def list_files():
    print("GET /static/image/")
    files = os.listdir('./static/image/')
    print(files)
    jpegs = []
    for file in files:
        print(file)
        print(file.endswith(".jpeg"))
        if file.endswith(".jpeg"):
            jpegs.append(file)
    print(jpegs)
    return jpegs

@app.route('/static/image/<filename>')
def get_file(filename):
    print("GET /static/image/"+filename)
    return send_file('./static/image/'+filename)

@app.route('/delete/<email>/<name>')
def delete_image(email,name):
    
    #user 
    user_email = session['email']
    user_email = user_email.replace("%40","@")
    
    storage_client = storage.Client('Project 2')
    
    #get the bucket
    bucket = storage_client.get_bucket(app.config['BUCKET'])
    
    blob = bucket.blob('static/image/'+email+'/'+ name)

    blob.delete()
    print("Image Deleted")
    return redirect(url_for('index'))

app.config['BUCKET'] = 'project2database'
app.config['UPLOAD_FOLDER'] = './static/image/'

#Save image to the bucket
def save_picture(picture_fn,email):
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_fn)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(app.config['BUCKET'])
    blob = bucket.blob('static/image/'+email+'/'+ picture_fn)
    blob.upload_from_filename(picture_path)

    return picture_path

#download an image local folder
def download_picture():
    
    print("Download Inages from Bucket")

    s_c = storage.Client('Project 2')
    #get the bucket
    b = s_c.get_bucket(app.config['BUCKET'])

    #///////////////////////////// Download Bucket Forlder with the all the images ////////////////////////

    folder_name_on_gcs = 'static/image/'

    # Create the directory locally
    Path(folder_name_on_gcs).mkdir(parents=True, exist_ok=True)

    blobs = b.list_blobs(prefix=folder_name_on_gcs)
    for blob in blobs:
        if not blob.name.endswith('/'):
            # This blob is not a directory!
            print(f'Downloading file [{blob.name}]')
            blob.download_to_filename(f'./{blob.name}')

    #////////////////////////////
    return folder_name_on_gcs

#Encode and Decode
def string_decode(query_def_size):
    base64_size_bytes = query_def_size.encode("ascii")        
    size_string_bytes = base64.b64decode(base64_size_bytes)
    size_string = size_string_bytes.decode("ascii")        
    print(f"Decoded: {size_string}")
    return size_string
    
def string_encode(query_def_size):
    name_bytes = query_def_size.encode("ascii")
    base64_name_bytes = base64.b64encode(name_bytes)
    base64_name = base64_name_bytes.decode("ascii")        
    print(f"Encoded: {base64_name}")
    return base64_name

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=(os.environ.get("PORT", 8080)))