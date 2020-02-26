import os
import boto3
import face_recognition
from PIL import Image
from flask import Flask, render_template
from pymongo import MongoClient
from pymongo import errors

app = Flask(__name__, template_folder='.')


@app.route('/image_recognition/')
def image_recognition_call():
    try:
        print("Request received...")
        passport_path = r'C:\Users\Public\passport\\'
        test_image_path = r"C:\Users\Public\test\test.jpg"
        path = r'C:\Users\Public\image'
        pass_path = r'C:\Users\Public\passport'

        # Remove pre-files from folder
        remove_files(pass_path)
        # download files from S3 to the paths
        download_files(passport_path, test_image_path)

        # detect faces from a group photo
        face_detection(test_image_path)

        # now face recognition
        face_recognition_project(path, pass_path)

        print("Request served...")
        return render_template('index.html')

    except Exception:
        print("Inside Exception")
        return render_template('error.html')


def download_files(passport_path, test_image_path):
    ACCESS_KEY = 'Your_Access_Key'
    SECRET_KEY = 'Your_Secret_Key'
    # downloading files from S3
    s3 = boto3.client('s3',    aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    list_images = s3.list_objects(Bucket='neelbucket1')['Contents']
    print(list_images)
    for key in list_images:
        print(key['Key'])
        s3.download_file('neelbucket1', key['Key'],
                         passport_path + key['Key'])
    print('downloading passport images done')
    list_images = s3.list_objects(Bucket='neelbucket2')['Contents']
    for key in list_images:
        s3.download_file('neelbucket2', key['Key'],
                         test_image_path)
    print('downloading test images done')


def remove_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    print("Folder is now empty")


def face_detection(test_image_path):
    print("Detecting faces...")
    image = face_recognition.load_image_file(test_image_path)
    print("Progress")
    face_locations = face_recognition.face_locations(image)
    i = 0
    print('Total found faces are', len(face_locations))
    folder = r'C:\Users\Public\image'
    remove_files(folder)
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print(
            "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                  right))

        # Access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        # pil_image.show()
        print('Saving image {}'.format(i))
        pil_image.save(r'C:\Users\Public\image\\{}.jpg'.format(i))
        i = i + 1


def face_recognition_project(path, pass_path):
    pass_files = os.listdir(pass_path)
    print("face recognition...")
    img_files = os.listdir(path)
    print(len(img_files))
    try:
        print("Trying to connect Mongo DB")
        client = MongoClient(
            "mongodb://admin:adminpassword@neelmongoserver-shard-00-00-kwu6r.mongodb.net:27017,neelmongoserver-shard-00-01-kwu6r.mongodb.net:27017,neelmongoserver-shard-00-02-kwu6r.mongodb.net:27017/test?ssl=true&replicaSet=NeelMongoServer-shard-0&authSource=admin&retryWrites=true&w=majority")
        print("DB Connected")
        db = client.get_database("softwaredevelopmentproject")
        result = db.student
        for pass_file in pass_files:
            res = True
            print("matching for ", pass_file)
            known_image = face_recognition.load_image_file(pass_path + "\\" + pass_file)
            name = pass_file
            for img in img_files:
                print("Scanning file ", img)
                unknown_image = face_recognition.load_image_file(
                    r"C:\Users\Public\image\{}".format(img))
                known_encoding = face_recognition.face_encodings(known_image)[0]
                a = face_recognition.face_encodings(unknown_image)
                if len(a) <= 0:
                    return 0
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.5)
                print(results)
                if results[0]:
                    print(pass_file, " is matched!")
                    result.update_one({"imageName": name}, {"$set": {"presence": "True"}})
                    print('Student data updated')
                else:
                    print(pass_file, " is not matched!")

    except errors.OperationFailure as error:
        print("Failed to read data from mongo DB ".format(error))


if __name__ == "__main__":
    app.run(debug=True)
