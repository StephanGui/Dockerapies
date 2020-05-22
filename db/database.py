from flask_pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")

mydb = myclient["myDatabase"]

mycol = mydb["customers"]