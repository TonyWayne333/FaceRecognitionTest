from PIL import Image
# import face_recognition_models
import face_recognition
import os
from flask import Flask, render_template
#from flask_mysqldb import MySQL
from flask import Flask, session
import boto3
import traceback
# app = Flask(__name__, template_folder='.')

# app.config['MYSQL_HOST'] = 'projectsem8.c1lzaol9u5w9.us-east-2.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'Admin'
# app.config['MYSQL_PASSWORD'] = 'Password'
# app.config['MYSQL_DB'] = 'details'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
# mysql = MySQL()
# mysql.init_app(app)


# @app.route("/", methods=['GET'])
def hello():
    try:
        #print("Request received...")
        # downloading files from S3
        # s3 = boto3.client('s3')
        # count = 0;
        # list = s3.list_objects(Bucket='neelbucket1')['Contents']
        # for key in list:
            # s3.download_file('neelbucket1', key['Key'],
                            # r'C:\Users\Public\passport\\' + key[
                               #  'Key'])
        #print('downloading passport images done')
        # list = s3.list_objects(Bucket='neelbucket2')['Contents']
        # for key in list:
          #  s3.download_file('neelbucket2', key['Key'],
           #                  r'C:\Users\Public\test\test.jpg')
        #print('downloading passport images done')
        # Load the jpg file into a numpy array
        print("Detecting faces...")
        image = face_recognition.load_image_file(r"C:\Users\Public\test\test.jpg")
        folder = r'C:\Users\Public\image'
        print("Progress")
        face_locations = face_recognition.face_locations(image)
        i = 0
        print('Total found faces are', len(face_locations))
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        print("Folder is now empty")
        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location
            print(
                "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                      right))

            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            # pil_image.show()
            print('Saving image {}'.format(i))
            pil_image.save(r'C:\Users\Public\image\\{}.jpg'.format(i))
            i = i + 1

        # now face recognition
        i = 0

        path = r'C:\Users\Public\image'
        passPath = r'C:\Users\Public\passport'
        passfiles = os.listdir(passPath)
        print("face recognition...")
        imgfiles = os.listdir(path)
        print(len(imgfiles))
        name = "s"
        for passfile in passfiles:
            res = 'false'
            print("matching for ", passfile)
            known_image = face_recognition.load_image_file(passPath + "\\" + passfile)
            name = passfile
            for img in imgfiles:
                print("Scanning file ", img)
                unknown_image = face_recognition.load_image_file(
                    r"C:\Users\Public\image\{}".format(img))
                known_encoding = face_recognition.face_encodings(known_image)[0]
                a = face_recognition.face_encodings(unknown_image)
                if (len(a) <= 0):
                    # return render_template('error.html')
                    return 0
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.5)
                print(results)
                if results[0] == True:
                    res = 'true'
                    print(passfile, " is matched!")
                   # print("Updating into database...")
                    # print(res)
                    # print(name)
                    # cur = mysql.connection.cursor()  # Execute
                    # cur.execute("UPDATE students SET  Result = (%s) WHERE FileName = (%s) ", (res, name))

                    # Commit to DB
                    # mysql.connection.commit()
                    # break
                else:
                    print(passfile, " is not matched!")

        # now storing in the database

        # Close connection
        # cur.close()
        print("Request served...")
        # return render_template('index.html')
    # except Exception:
      #  traceback.print_exc()
       # return render_template('errorInternal.html')
    except Exception:
        return False


if __name__ == "__main__":
    #this will call Face Recognition Method
    hello()


