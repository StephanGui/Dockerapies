import vcf


def main(vcfpath):
    vcfpath = "/home/sander/Desktop/WinLinShare/example.vcf"
    vcf_reader = vcf.Reader(open(vcfpath, 'r'))
    for record in vcf_reader:
        print(record.INFO['NS'])


if __name__ == '__main__':
    main()
