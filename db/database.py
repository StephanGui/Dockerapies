from pymongo import MongoClient
import vcf
import os
import sys

myclient = MongoClient("mongodb://root:example@localhost:27017")
mydb = myclient["Allele_variant_DB"]
mycol = mydb["Variants"]

vcf_reader = vcf.Reader(open(os.path.join(os.path.split(os.path.abspath(__file__))[0], "gnomad_test.vcf"), 'r'))
for record in vcf_reader:
    if record.INFO['AC'][0] - record.INFO['non_cancer_AC'][0] >= 1:
        if 0 < float(record.INFO['AF'][0]) < 0.01:
            for letter in record.ALT:
                subst_nucl = str(letter)
            dict_entry = {}
            dict_entry = {"chromosome": record.CHROM,
                       "position": record.POS,
                       "Ref_nuc": record.REF,
                       "Alt_nuc": subst_nucl
                       }
            print(dict_entry)
            mycol.insert_one(dict_entry)

print("bananen zijn groen!!!!$$$$$$$$$$$$$")
for x in mycol.find():
    print(x)
