import os
import json
from flask import Flask, flash, request, redirect, url_for
from module.database import Database
import face_recognition

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "mys3cr3tk3y"
db = Database()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        token = request.form['token']
        user_data = db.getuser(token)
        user_id = user_data[0]
        db.logapicall(user_id)
        # Face match
        image1 = request.files['image1']
        image2 = request.files['image2']

        image1fc = face_recognition.load_image_file(image1)
        image2fc = face_recognition.load_image_file(image2)

        image1_face_encoding = face_recognition.face_encodings(image1fc)[0]
        image2_face_encoding = face_recognition.face_encodings(image2fc)[0]
        known_faces = [
            image1_face_encoding
        ]
        results = face_recognition.compare_faces(known_faces, image2_face_encoding)
        responseObj = { "process":"finish", "facematched": format(results[0]) }
        responseJson = json.dumps(responseObj) 
        return responseJson
    except:
        responseObj = { "process":"incomplete", "facematched": "False"}
        responseJson = json.dumps(responseObj) 
        return responseJson
    # data = db.read(None)

    # return json.dumps(data)
    # if request.method == 'POST':
    #     image1 = request.files['image1']
    #     image2 = request.files['image2']

    #     image1fc = face_recognition.load_image_file(image1)
    #     image2fc = face_recognition.load_image_file(image2)

    #     try:
    #         image1_face_encoding = face_recognition.face_encodings(image1fc)[0]
    #         image2_face_encoding = face_recognition.face_encodings(image2fc)[0]
    #     except IndexError:
    #         print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    #         quit()

    #     known_faces = [
    #         image1_face_encoding
    #     ]

    #     # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    #     results = face_recognition.compare_faces(known_faces, image2_face_encoding)
    #     responseObj = { "facematched": format(results[0]) }
    #     responseJson = json.dumps(responseObj)        
    # return responseJson 
    #"face matched? {}".format(results[0])

app.run(host='0.0.0.0', port=5001)