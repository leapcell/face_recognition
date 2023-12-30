from flask import Flask, render_template, request, redirect
import base64
from io import BytesIO
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_faces_in_image(file_stream):
    import face_recognition
    img = face_recognition.load_image_file(file_stream)
    faces = face_recognition.face_locations(img)
    result = []
    for i in range(len(faces)):
        top, right, bottom, left = faces[i]

        faceImage = img[top:bottom, left:right]
        final = Image.fromarray(faceImage)
        buffered = BytesIO()
        final.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        result.append(img_str)
    return result

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload_image():
    if request.method == 'GET':
        return render_template('index.html')
    
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and not allowed_file(file.filename):
        # The image file seems valid! Detect faces and return the result.
        params = {"message": "File type not allowed"}
        return render_template('index.html', **params)

    faces = detect_faces_in_image(file)
    params = {"faces": faces}
    return render_template('index.html', **params)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)
