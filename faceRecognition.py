from PIL import Image
import face_recognition
import os
import boto3


def hello():
    try:
        print("Request received...")
        passportpath = r'C:\Users\Public\passport\\'
        testimagepath = r"C:\Users\Public\test\test.jpg"
        path = r'C:\Users\Public\image'
        passPath = r'C:\Users\Public\passport'

        #download files from S3 to the paths
        downloadfiles(passportpath, testimagepath)

        #detect faces from a group photo
        facedetection(testimagepath)

        # now face recognition
        facerecognition(path, passPath)

        print("Request served...")

    except Exception:
        return False


def downloadfiles(passportpath, testpath):
    # downloading files from S3
    s3 = boto3.client('s3')
    list = s3.list_objects(Bucket='neelbucket1')['Contents']
    print(list)
    for key in list:
        print(key['Key'])
        s3.download_file('neelbucket1', key['Key'],
                         passportpath + key['Key'])
    print('downloading passport images done')
    list = s3.list_objects(Bucket='neelbucket2')['Contents']
    for key in list:
        s3.download_file('neelbucket2', key['Key'],
                         testpath)
    print('downloading test images done')


def removefiles(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    print("Folder is now empty")

def facedetection(testimagepath):
    print("Detecting faces...")
    image = face_recognition.load_image_file(testimagepath)
    print("Progress")
    face_locations = face_recognition.face_locations(image)
    i = 0
    print('Total found faces are', len(face_locations))
    folder = r'C:\Users\Public\image'
    removefiles(folder)
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


def facerecognition(path, passPath):
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
            if len(a) <= 0:
                return 0
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.5)
            print(results)
            if results[0]:
                print(passfile, " is matched!")
            else:
                print(passfile, " is not matched!")


if __name__ == "__main__":
    # this will call Face Recognition Method
    hello()
