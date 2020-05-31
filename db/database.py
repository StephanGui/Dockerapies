from pymongo import MongoClient
import vcf
import os
import sys

# myclient = MongoClient("mongodb://root:example@localhost:27017")

vcf_reader = vcf.Reader(open(os.path.join(os.path.split(os.path.abspath(__file__))[0], "gnomad_test.vcf"), 'r'))
for record in vcf_reader:

    if float(record.INFO['non_cancer_AF'][0]) < 0.01:
        # todo add to mongoDB

# mydb = myclient["test_DB"]
# mycol = mydb["genes"]
#
# mydict = [{"chromosome": "12", "position": "29312", "nucleotide": "A", "change": "G"},
#           {"chromosome": "12", "position": "23421", "nucleotide": "C", "change": "G"},
#           {"chromosome": "12", "position": "213423", "nucleotide": "A", "change": "T"},
#           {"chromosome": "12", "position": "12353", "nucleotide": "C", "change": "T"},
#           {"chromosome": "12", "position": "984732", "nucleotide": "G", "change": "A"}
#           ]
#
# mycol.insert_many(mydict)
#
# print("bananen zijn groen!!!!$$$$$$$$$$$$$")
# for x in mycol.find():
#     print(x)
