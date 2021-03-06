from pymongo import MongoClient
import vcf
import os

myclient = MongoClient("mongodb://spider:man@localhost:27017")
mydb = myclient["Allele_variant_DB"]
mycol = mydb["Variants"]

"""
Opens the VCF.
"""
def vcf_parser():
    vcf_reader = vcf.Reader(open(os.path.join(os.path.split(os.path.abspath(__file__))[0], "gnomad_test.vcf"), 'r'))
    return vcf_reader

"""
filters the records in vcf file. 
Does not add the records to list if 
not found in patients with cancer 
or if in more than 1% of population.

:param vcf_reader - the vcf file parsed.
:return list_of_dict - list of dictionaries containing allele variant info
"""
def filter_records(vcf_reader):
    list_of_dict = []
    for record in vcf_reader:
        # check of er mensen zijn met deze variant en cancer
        if record.INFO['AC'][0] - record.INFO['non_cancer_AC'][0] >= 1:
            # frequency check (kleiner dan 0.01)
            if 0 < float(record.INFO['AF'][0]) <= 0.01:
                dict_entry = {"CHROM": record.CHROM,
                              "POS": record.POS,
                              "REF": record.REF,
                              "ALT": str(record.ALT[0])
                              }
                list_of_dict.append(dict_entry)
    return (list_of_dict)

"""
adds list of dictionary to the column "Variants"
:param list_of_dict - a list of dictionary entries containing info about allele variant
"""
def fill_dictionary(list_of_dict):
    mycol.insert_many(list_of_dict)


if __name__ == "__main__":
    try:
        vcf_reader = vcf_parser()
        list_of_dict = filter_records(vcf_reader)
        fill_dictionary(list_of_dict)
    except TypeError:
        print("Het document bevat geen lijsten of is niet het juiste formaat")
    except FileNotFoundError:
        print("Het bestand bestaat niet")
