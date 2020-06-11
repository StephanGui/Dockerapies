import os
import sys
from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import vcf
import json

app = Flask(__name__)
client = MongoClient("mongodb://spider:man@db:27017")
db = client.Allele_variant_DB.Variants

os.makedirs(os.path.join(app.root_path, "Uploaded_vcfs"))
UPLOAD_FOLDER = "Uploaded_vcfs"
ALLOWED_EXTENSIONS = {'vcf'}


@app.route('/', methods=['GET', 'POST'])
def receive_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file, flush=True)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):  # and vcf.Reader(open(file.stream, 'r'))
            filename = secure_filename(file.filename)
            print(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            vcf_dict = filter_vcf(file)
            return json.dumps(vcf_dict)

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


def filter_vcf(vcfpath):
    print(vcfpath, flush=True)
    vcf_reader = vcf.Reader(open(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], vcfpath.filename), 'r'))
    new_vcflist = {}
    for i, record in enumerate(vcf_reader):
        entry = {"CHROM": record.CHROM, "POS": record.POS, "REF": record.REF, "ALT": str(record.ALT[0])}
        cursor = db.find_one(entry)
        if cursor is not None:
            new_vcflist[str(i)] = entry
    return new_vcflist


if __name__ == '__main__':
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host='0.0.0.0')
