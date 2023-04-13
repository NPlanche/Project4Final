import os
import traceback
import pyrebase
from flask import Flask, redirect, request, send_file

#from PIL import Image
from google.cloud import storage
from pathlib import Path


#request
import requests
from urllib import parse

#Encode and Decode
import base64

##from PIL.ExifTags import TAGS
##import sys

app = Flask(__name__)



@app.route('/')
def index():
    print("GET /")
       
    r  = request
    base_url = request.base_url
    a = request.args
    f = request.full_path
    print(f"Full path: {f}")
    substring = f[0:8]
    
    url = base_url + f
    
    if (substring == '/?image=') and (len(f) > len(substring)) :
        
        urlBase = 'https://storage.googleapis.com/project2database/static/image/'
        query = parse.parse_qs(parse.urlparse(url).query)
        query_def_name = query['image'][0]
        query_def_size = query['size'][0]
        query_def_location = query['location'][0]
        query_def_type = query['type'][0]

        
        #TODO: Make encoding and decoding functions
        #Name
        base64_name_bytes = query_def_name.encode("ascii")
            
        name_string_bytes = base64.b64decode(base64_name_bytes)
        name_string = name_string_bytes.decode("ascii")
            
        print(f"Decoded Name: {name_string}")
        
        src = urlBase + name_string
        print(f"URL: {src}")
        
        #Size
        base64_size_bytes = query_def_size.encode("ascii")
            
        size_string_bytes = base64.b64decode(base64_size_bytes)
        size_string = size_string_bytes.decode("ascii")
            
        print(f"Decoded Size: {size_string}")
        
        #Location 
        base64_location_bytes = query_def_location.encode("ascii")
            
        location_string_bytes = base64.b64decode(base64_location_bytes)
        location_string = location_string_bytes.decode("ascii")
            
        print(f"Decoded Location: {location_string}")
        
        #Type
        base64_type_bytes = query_def_type.encode("ascii")
            
        type_string_bytes = base64.b64decode(base64_type_bytes)
        type_string = type_string_bytes.decode("ascii")
            
        print(f"Decoded Location: {type_string}")
        
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
        
        </style>
        <div class = "container">
            <table>
                <tr>
                    <td>

                    <img class='image' src='"""
        index_html+= src + "'></td> <td><table class='styled-table'> <caption><h2>Metadata</h2></caption> <thead><tr><th>Category</th><th>Data</th></tr></thead><tbody><tr><td>Filename</td><td>"+name_string+"</td></tr><tr><td>Type</td><td>"+type_string+"</td></tr><tr><td>Size</td><td>"+size_string+"</td></tr><tr><td>Location</td><td>"+location_string+"</td></tr></tbody></table></td></tr></table></div>"""
        
        
        
        
        
        
        
             
       
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
        
        
        
        


    # for file in list_files():
    #     index_html += "<img class='image' src=\" /static/image/"+ file + "\">"
    
    storage_client = storage.Client('Project 2')
    #get the bucket
    bucket = storage_client.get_bucket(app.config['BUCKET'])

    blobs = bucket.list_blobs(prefix='static/image/')
    for blob in blobs:
        if not blob.name.endswith('/'):
            # This blob is not a directory!
            #index_html += "<img class='image' src='" + blob.public_url + "'>"
             #To Do: This goes to a black page (get metadata )
                
            image_url = blob.public_url
            urlBase = 'https://storage.googleapis.com/project2database/static/image/'
            image_name = image_url[61:len(image_url)]
            
            #Encoding 
            #sample_string = "GeeksForGeeks is the best"
            name_bytes = image_name.encode("ascii")
            base64_name_bytes = base64.b64encode(name_bytes)
            base64_name = base64_name_bytes.decode("ascii")
            
            print(f"Encoded Name: {base64_name}")
            
            #Encoding 
            #Size
            size = str(blob.size)
            size_bytes = size.encode("ascii")
            
            base64_size_bytes = base64.b64encode(size_bytes)
            base64_size = str(base64_size_bytes.decode("ascii"))
            
            print(f"Encoded Size: {base64_size}")
            
            #Encoding
            #Location
            location = str(blob.public_url)
            location_bytes = location.encode("ascii")
            
            base64_location_bytes = base64.b64encode(location_bytes)
            base64_location = str(base64_location_bytes.decode("ascii"))
            
            print(f"Encoded Location: {base64_location}")
            
            #Encoding
            #Type
            type = str(blob.content_type)
            type_bytes = type.encode("ascii")
            
            base64_type_bytes = base64.b64encode(type_bytes)
            base64_type = str(base64_type_bytes.decode("ascii"))
            
            print(f"Encoded Type: {base64_type}")
            
            
            
            
            
            index_html += "<a href='"+ base_url +"/?image="+ base64_name +"&size="+base64_size+"&location="+base64_location+"&type="+base64_type+"'><img class='image' src='" + blob.public_url + "'></a>"


            
        
    return index_html


@app.route('/upload', methods = ['POST'])
def upload():    
    try:
        print("POST /upload")
        file = request.files['form_file']
        #file.save(os.path.join("./files", file.filename))
        file.save(os.path.join("./static/image/", file.filename))

        save_picture(file.filename)
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


app.config['BUCKET'] = 'project2database'
app.config['UPLOAD_FOLDER'] = './static/image/'

def save_picture(picture_fn):
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_fn)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(app.config['BUCKET'])
    blob = bucket.blob('static/image/'+ picture_fn)
    blob.upload_from_filename(picture_path)

    return picture_path

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

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=(os.environ.get("PORT", 8080)))