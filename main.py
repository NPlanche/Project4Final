import os
import traceback
from flask import Flask, redirect, request, send_file

#from PIL import Image
from google.cloud import storage
from pathlib import Path

#request
import requests
from urllib import parse
import urllib.request


#Metadata
from PIL import Image
from PIL.ExifTags import TAGS



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
    substring = f[0:8]
    
    url = base_url + f
    
    if (substring == '/?image=') and (len(f) > len(substring)) :
        query_def=parse.parse_qs(parse.urlparse(url).query)['image'][0]
        urlBase = 'https://storage.googleapis.com/project2database/static/image/'
        src = urlBase + query_def
        
        print("query def", query_def)
        
        #Getting metadata
        # Changes start 
                
        #Metadata Labes
        metdata_filename = "trial"
        metdata_size = "0" 
        metdata_height = "0"
        metdata_width = "0"
        metdata_format = "0"      
        metdata_mode = "0" 
        metdata_animated = "0"
        metdata_frames = "0"
        
        
        #Metadata of Image
        # path to the image 
        imagePath = src
        print("Image Path",imagePath)
        urllib.request.urlretrieve(
        imagePath,
        query_def)
        # #Read image Data with PIL
        
        imageData = Image.open(query_def)
        
        #Extract metadata
        info_dict = {
                    "Filename": imageData.filename,
                    "Image Size": imageData.size,
                    "Image Height": imageData.height,
                    "Image Width": imageData.width,
                    "Image Format": imageData.format,
                    "Image Mode": imageData.mode,
                    "Image is Animated": getattr(imageData, "is_animated", False),
                    "Frames in Image": getattr(imageData, "n_frames", 1)
                }
        item = 0
        for label,value in info_dict.items():
            print(f"{label:25}: {value}")
            
            if item == 0:
                metdata_filename = f"{label:25}: {value}"
            elif item == 1:
                metdata_size = f"{label:25}: {value}" 
            elif item == 2:
                metdata_height = f"{label:25}: {value}"
            elif item == 3:
                metdata_width = f"{label:25}: {value}" 
            elif item == 4:
                metdata_format = f"{label:25}: {value}"       
            elif item == 5:
                metdata_mode = f"{label:25}: {value}" 
            elif item == 6:
                metdata_animated = f"{label:25}: {value}" 
            else:
                metdata_frames = f"{label:25}: {value}" 
            item=item+1


        # extract EXIF data
        exifdata = imageData.getexif()
        
        # iterating over all EXIF data fields
        for tag_id in exifdata:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
                metdata2 = f"{tag:25}: {data}"
            
        # Changes end
        
        
        
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
        
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
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
        index_html+= src + "'></td> <td><table class='styled-table'><thead><tr><th>Metadata</th></tr></thead><tbody><tr><td>"+metdata_filename+"</td></tr><tr><td>"+metdata_size+"</td></tr><tr><td>"+metdata_height+"</td></tr><tr><td>"+metdata_width+"</td></tr><tr><td>"+metdata_format+"</td></tr><tr><td>"+metdata_mode+"</td></tr><tr><td>"+metdata_animated+"</td></tr><tr><td>"+metdata_frames+"</td></tr></tbody></table></td></tr></table></div>"""

        
        
        
        
             
       
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
            index_html += "<a href='"+ base_url +"/?image="+ image_name +"'><img class='image' src='" + blob.public_url + "'></a>"


            
        
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