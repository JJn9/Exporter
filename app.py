import os, csv, json
import io
import pandas as pd
import numpy as np
import sys, getopt

#Cette fonction récupère les arguments passés via le cmd et les enregistre dans des variables
def main(argv):
    inputfile = ''
    outputfile = ''
    devicePool = ''
    css = ''
    dirNumber = ''
    routePartition = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:p:c:n:r:",["ifile=","ofile=", "dpool=", "css=", "dnumber=", "route="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -p <devicepool> -c <CSS> -n <directorynumber> -r <routepartition>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile> -p <devicepool> -c <CSS> -n <directorynumber> -r <routepartition>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-p", "--dpool"):
            devicePool = arg
        elif opt in ("-c", "--css"):
            css = arg
        elif opt in ("-n", "--dnumber"):
            dirNumber = arg
        elif opt in ("-r", "--route"):
            routePartition = arg

    read_CSV(inputfile, outputfile, devicePool, css, dirNumber, routePartition)

#Cette fonction lis le csv source, le filtre selon les paramètre donnés puis enregistre le résultat dans un nouveau fichier
def read_CSV(sourceFile, endFile, devicePool, css, dirNumber, routePartition):
    if devicePool == '' and css == '' and dirNumber == '' and routePartition == '':
        print('Set values')

    elif devicePool != '' and css == '' and dirNumber != '' and routePartition == '':
        df = pd.concat(( [chunk[(chunk['Directory Number 1'].str[:4] == dirNumber) & (chunk['Device Pool'].str.contains(devicePool))] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))
        
    elif devicePool == '' and css == '' and dirNumber != '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Directory Number 1'].str[:4] == dirNumber) & (chunk['Route Partition 1'] == routePartition)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool == '' and css != '' and dirNumber == '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['CSS'] == css) & (chunk['Route Partition 1'] == routePartition)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool == '' and css != '' and dirNumber != '' and routePartition == '':
        df = pd.concat(( [chunk[(chunk['Directory Number 1'].str[:4] == dirNumber) & (chunk['CSS'] == css)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css == '' and dirNumber == '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Device Pool'].str.contains(devicePool)) & (chunk['Route Partition 1'] == routePartition)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css != '' and dirNumber == '' and routePartition == '':
        df = pd.concat(( [chunk[(chunk['Device Pool'].str.contains(devicePool)) & (chunk['CSS'] == css)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool == '' and css != '' and dirNumber == '' and routePartition == '':
        df = pd.concat(( [chunk[(chunk['CSS'] == css)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool == '' and css == '' and dirNumber != '' and routePartition == '':
        df = pd.concat(( [chunk[(chunk['Directory Number 1'].str[:4] == dirNumber)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool == '' and css == '' and dirNumber == '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Route Partition 1'] == routePartition)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css == '' and dirNumber == '' and routePartition == '':
        df = pd.concat(( [chunk[chunk['Device Pool'].str.contains(devicePool)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css != '' and dirNumber == '' and routePartition == '':
        df = pd.concat(( [chunk[(chunk['Device Pool'].str.contains(devicePool)) & (chunk['CSS'] == css)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css != '' and dirNumber != '' and routePartition == '':
        df = pd.concat(( [chunk[chunk['Device Pool'].str.contains(devicePool) & chunk['CSS'] == css & chunk['Directory Number 1'].str[:4] == dirNumber] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool == '' and css != '' and dirNumber != '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Route Partition 1'] == routePartition) & (chunk['CSS'] == css) & (chunk['Directory Number 1'].str[:4] == dirNumber)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css == '' and dirNumber != '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Route Partition 1'] == routePartition) & (chunk['Device Pool'].str.contains(devicePool)) & (chunk['Directory Number 1'].str[:4] == dirNumber)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css != '' and dirNumber == '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Route Partition 1'] == routePartition) & (chunk['Device Pool'].str.contains(devicePool)) & (chunk['CSS'] == css)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))

    elif devicePool != '' and css != '' and dirNumber != '' and routePartition != '':
        df = pd.concat(( [chunk[(chunk['Device Pool'].str.contains(devicePool)) & (chunk['CSS'] == css) & (chunk['Directory Number 1'].str[:4] == dirNumber) & (chunk['Route Partition 1'] == routePartition)] for chunk in pd.read_csv(sourceFile, iterator=True, chunksize=10**4)]))
    

    if not df.empty:
        try:
            df = df.replace(r'^\s*$', np.nan, regex=True)
            for i, row in df.iterrows():
                cols = [ f'Directory Number {i}' for i in range(1, 5) ]
                df['Multi-line'] = df[cols].apply(lambda row: 'Yes' if row.notna().sum() >= 2 else 'No', axis=1)

                    
            df.filter(['Device Name','Device Type', 'Device Protocol', 'Device Pool', 'Directory Number 1', 'Directory Number 2', 'Directory Number 3', 'Directory Number 4', 'CSS', 'Description', 'Location', 'Media Resource Group List',
                        'User Hold MOH Audio Source', 'Network Hold MOH Audio Source', 'Device User Locale', 'Softkey Template', 'Module 1', 'Module 2', 'Phone Button Template',
                        'Owner User ID', 'Directory Number 1', 'Route Partition 1', 'Alerting Name 1', 'Display 1', 'External Phone Number Mask 1', 'Call Pickup Group 1', 'Line CSS 1', 
                        'Forward All CSS 1', 'Forward No Answer Ring Duration 1', 'Forward No Answer Internal Destination 1', 'Forward No Answer External Destination 1', 'Busy Trigger 1',
                        'Forward Busy Internal Destination 1', 'Forward Busy External Destination 1', 'Multi-line']).to_csv(endFile, index_label="id")
            cpg_match(endFile)
        except Exception as e:
            print(e)
    else:
        print("Error check your values")

    
def cpg_match(phone_file):
    phone_file = pd.read_csv(phone_file)
    writer = pd.ExcelWriter('final.xlsx', engine='xlsxwriter')
    df = pd.DataFrame()
    for cpg in phone_file['Call Pickup Group 1']:
        if not pd.isna(cpg):
            df = df.append(pd.concat(([chunk[chunk['CPG NAME'].str.contains(cpg)] for chunk in pd.read_csv('callpickupgroup.csv', iterator=True, chunksize=10 ** 4)])))
    if not df.empty:
        try:
            df = df.replace(r'^\s*$', np.nan, regex=True)
            df.filter(['CPG NUMBER', 'DESCRIPTION', 'ROUTE PARTITION', 'CPG NAME', 'CPG NOTIFICATION POLICY',
                    'CPG NOTIFICATION TIMER', 'CALLING PARTY INFO', 'ASSOCIATED CPG NAME 1']).to_csv('phoneref.csv',
                                                                                                        index_label="id")
        except Exception as e:
            print(e)
    else:
        print("Error check your values")
        
    dfs = {'phone': pd.read_csv('test.csv'), 'CPG': pd.read_csv('phoneref.csv')}
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
   


if __name__ == '__main__':
    main(sys.argv[1:])
