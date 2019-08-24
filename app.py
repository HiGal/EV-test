import os
import logging
import glob
from flask import Flask, render_template, request, flash, redirect
from detection import detect_cup

logging.basicConfig(filename='logs.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ALLOWED_EXTENSIONS = {'ogv', 'avi', 'mp4'}
UPLOAD_FOLDER = 'video/'

app = Flask(__name__)
app.secret_key = 'some secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload_and_detect():
    if request.method == "POST":
        os.system('rm  static/imgs/absent/*.png')
        os.system('rm  static/imgs/presence/*.png')
        if 'inputFile' not in request.files:
            logging.info('No file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['inputFile']
        if file.filename == '':
            logging.info('No selected file')
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = "1." + file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logging.info('File was successfully saved')
            detect_cup('video/' + filename, 'static/video/' + filename)
            logging.info('File was successfully processed')
            flash('File was successfully processed')
            return redirect(request.url)
        else:
            logging.info('Incorrect format of file')
            flash('Incorrect format of file. Please choose proper format type')
            return redirect(request.url)
    return render_template('home.html')


@app.route('/result')
def result():
    absent_paths = sorted(glob.glob('static/imgs/absent/*.png'))
    presence_paths = sorted(glob.glob('static/imgs/presence/*.png'))
    return render_template('result.html', absent_paths=absent_paths, presence_paths=presence_paths)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
