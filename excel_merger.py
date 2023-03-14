#!/usr/bin/env python3

'''
Merge multiple excel files into one xlsx
'''

import os
import subprocess
import sys
import pandas as pd


def main(files_list, output):
    for i, f in enumerate(files_list):
        if(f.endswith('.xls')):
            if(os.path.exists(f + 'x')):
                print("File", f + 'x', "Already exists")
            else:
                subprocess.check_call(['libreoffice', '--headless', '--convert-to', 'xlsx', f])
            files_list[i] = f + 'x'
    print(files_list)

    dfood = pd.DataFrame()
    for f in files_list:
        data = pd.read_excel(f, sheet_name='Food')
        dfood = pd.concat([dfood, data], ignore_index=True)
    
    dfex = pd.DataFrame()
    for f in files_list:
        data = pd.read_excel(f, sheet_name='Exercise')
        dfex = pd.concat([dfex, data], ignore_index=True)

    dfmeas = pd.DataFrame()
    for f in files_list:
        data = pd.read_excel(f, sheet_name='Measurements')
        dfmeas = pd.concat([dfmeas, data], ignore_index=True)

    with pd.ExcelWriter(output) as writer:
        dfood.to_excel(writer, sheet_name="Food", index=False)
        dfex.to_excel(writer, sheet_name="Exercise", index=False)
        dfmeas.to_excel(writer, sheet_name="Measurements", index=False)
    print("File", output, "generated.")


if len(sys.argv) < 3:
    print("Uso: ", sys.argv[0], "file1 file2 [file3 ...] [-o output_file]");
else:
    i = 1
    file_list = []
    output_file = 'MyNetDiary_All.xlsx'
    while(i < len(sys.argv)):
        if(sys.argv[i] == '-o'):
            output_file = sys.argv[i+1]
            if not output_file.endswith('.xlsx'):
                output_file += '.xlsx'
            i=i+2
            continue
        file_list += [sys.argv[i]]
        i = i+1
    main(file_list, output_file)
