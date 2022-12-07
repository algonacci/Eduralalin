import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import module as md

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict_image', methods=["GET", "POST"])
def predict_image():
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            result, confidence = md.predict_image(image_path)
            return render_template('upload_image.html',
                                   image=image_path,
                                   result=result,
                                   confidence=confidence)
        else:
            return render_template('upload_image.html',
                                   alert="Please upload an image in PNG/JPG format!")
    else:
        return render_template('upload_image.html')


@app.route('/realtime_camera')
def realtime_camera():
    return render_template('realtime_camera.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
