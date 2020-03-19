import os, csv, json
import io
import pandas as pd
import sys, getopt

#Cette fonction récupère les arguments passés via le cmd et les enregistre dans des variables
def main(argv):
    inputfile = ''
    outputfile = ''
    deviceName = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:n:",["ifile=","ofile=", "dname="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -n <devicename>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile> -n <devicename>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-n", "--dname"):
            deviceName = arg

    read_CSV(inputfile, outputfile, deviceName)

#Cette fonction lis le csv source, le filtre selon les paramètre donnés puis enregistre le résultat dans un nouveau fichier
def read_CSV(sourceFile, endFile, deviceName):
    print(deviceName)
    df = pd.concat(( [chunk[chunk['Device Pool'] == deviceName] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))
    df.filter(['Device Name','Services Provisioning',  'Device Pool', 'Description']).to_csv(endFile, index_label="id")


if __name__ == '__main__':
    main(sys.argv[1:])
