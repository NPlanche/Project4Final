import os
import traceback
from flask import Flask, redirect, request, send_file

#from PIL import Image
from google.cloud import storage
from pathlib import Path

#request
import requests
from urllib import parse

##from PIL.ExifTags import TAGS
##import sys

app = Flask(__name__)



@app.route('/')
def index():
    print("GET /")
       
    #r  = request
    #base_url = request.base_url
    #a = request.args
    #f = request.full_path
    #substring = f[0:8]
    
    #url = base_url + f
    
    #if (substring == '/?image=') and (len(f) > len(substring)) :
    if (1 == 2) :
        query_def=parse.parse_qs(parse.urlparse(url).query)['image'][0]
        urlBase = 'https://storage.googleapis.com/project2database/static/image/'
        src = urlBase + query_def
        index_html =""" <style>
        

        .image{
            display: block;
            width: 300px;
            height: 300px;
        }
        
        .container{
            padding:200px 0px;            
        }
        
        </style>
        <div class = "container">
            <table>
                <tr>
                    <td>

                    <img class='image' src='"""
        index_html+= src + "'></td> <tr></div> """       
       
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
        
        
        
        
    #old index html
    hola="""<style>
    
    form{
        font-family: "Raleway", Arial, sans-serif
    }
    
    .image{
        margin:5px;
        border: 1px solid #ccc;
        width: 225px;
        height: 225px;
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
            index_html += "<img class='image' src='" + blob.public_url + "'>"
             #To Do: This goes to a black page (get metadata )
                
            image_url = blob.public_url
            urlBase = 'https://storage.googleapis.com/project2database/static/image/'
            image_name = image_url[61:len(image_url)]
            #index_html += "<a href='"+ base_url +"/?image="+ image_name +"'><img class='image' src='" + blob.public_url + "'></a>"


            
        
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
    ##except:
        ##traceback.print_exc()
        #change later
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
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