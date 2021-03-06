import os
from flask import Flask, request, flash, redirect, abort
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import vcf
import json

api = Flask(__name__)
client = MongoClient("mongodb://spider:man@db:27017")
db = client.Allele_variant_DB.Variants

UPLOAD_FOLDER = os.path.join(api.root_path, "Uploaded_vcfs")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'vcf'}


@api.route('/', methods=['GET', 'POST'])
def receive_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):  # and vcf.Reader(open(file.stream, 'r'))
            filename = secure_filename(file.filename)
            file.save(os.path.join(api.config['UPLOAD_FOLDER'], filename))
            vcf_dict = filter_vcf(file.filename)
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


@api.route("/receive/<filename>", methods=["POST"])
def receive_file_https(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")
    if not allowed_file(filename):
        abort(400, "only vcf files allowed as input")

    # write data to local vcf file
    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as fp:
        fp.write(request.data)

    vcf_dict = filter_vcf(filename)
    return json.dumps(vcf_dict)


# Accept filename and return dictionary containing filtered vcs
def filter_vcf(vcf_filename):
    vcf_reader = vcf.Reader(open(os.path.join(api.config['UPLOAD_FOLDER'], vcf_filename), 'r'))
    new_vcflist = {}
    for i, record in enumerate(vcf_reader):
        entry = {"CHROM": record.CHROM, "POS": record.POS, "REF": record.REF, "ALT": str(record.ALT[0])}
        if db.find_one(entry) is not None:
            new_vcflist[str(i)] = entry
    return new_vcflist


if __name__ == '__main__':
    api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    api.run(host='0.0.0.0')
