from pymongo import MongoClient
import sys

myclient = MongoClient("mongodb://root:example@localhost:27017")

mydb = myclient["test_DB"]
mycol = mydb["genes"]

mydict = [{ "chromosome": "12", "position": "29312", "nucleotide": "A", "change": "G"},
          {"chromosome": "12", "position": "23421", "nucleotide": "C", "change": "G"},
          {"chromosome": "12", "position": "213423", "nucleotide": "A", "change": "T"},
          {"chromosome": "12", "position": "12353", "nucleotide": "C", "change": "T"},
          {"chromosome": "12", "position": "984732", "nucleotide": "G", "change": "A"}
         ]

mycol.insert_many(mydict)

print("bananen zijn groen!!!!$$$$$$$$$$$$$")
for x in mycol.find():
    print(x)
