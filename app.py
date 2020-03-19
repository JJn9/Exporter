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
        opts, args = getopt.getopt(argv,"hi:o:p:",["ifile=","ofile=", "dpool="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -n <devicepool>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile> -n <devicename>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-p", "--dpool"):
            deviceName = arg

    read_CSV(inputfile, outputfile, deviceName)

#Cette fonction lis le csv source, le filtre selon les paramètre donnés puis enregistre le résultat dans un nouveau fichier
def read_CSV(sourceFile, endFile, deviceName):
    print(deviceName)
    df = pd.concat(( [chunk[chunk['Device Pool'] == deviceName] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))
    df.filter(['Device Name','Device Type', 'Device Protocol', 'Device Pool', 'Description', 'Location', 'Media Resource Group List',
     'User Hold MOH Audio Source', 'Network Hold MOH Audio Source', 'Device User Locale', 'Softkey Template', 'Module 1', 'Module 2', 'Phone Button Template',
     'Owner User ID', 'Directory Number 1', 'Route Partition 1', 'Alerting Name 1', 'Display 1', 'External Phone Number Mask 1', 'Call Pickup Group 1', 'Line CSS 1', 
     'Forward All CSS 1', 'Forward No Answer Ring Duration 1', 'Forward No Answer Internal Destination 1', 'Forward No Answer External Destination 1', 'Busy Trigger 1',
     'Forward Busy Internal Destination 1', 'Forward Busy External Destination 1']).to_csv(endFile, index_label="id")


if __name__ == '__main__':
    main(sys.argv[1:])
