import os
from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import pymongo
import vcf

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'.vcf'}


@app.route('/', methods=['GET', 'POST'])
def receive_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename) and vcf.Reader(file):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_flow(file)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def main_flow(vcf_file):
    read_vcf("/home/sander/Desktop/WinLinShare/example.vcf")


def read_vcf(vcfpath):
    vcf_reader = vcf.Reader(open(vcfpath, 'r'))
    for record in vcf_reader:
        print(record.INFO['NS'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
