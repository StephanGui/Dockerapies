from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import sys


app = Flask(__name__)
client = MongoClient("mongodb://root:example@db:27017")
db = client.test_DB

@app.route('/')
def home_page():
    print(db.list_collection_names(), file=sys.stderr)
    return render_template("index.html")

@app.route('/banaan')
def hello_world():
    item_doc= {
        'name': request.form['name'],
        'description': request.form['description']
    }
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
