#!/usr/bin/env python3

'''
Diet Visualizer (dietvisual)
Starting from a MyNetDiary data file, this program generates a plot of a certain measurement. 
'''

import datetime
import os
import sys
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
# import argparser

def main(file, measurement, start, end, g):
    df = pd.read_excel(file, sheet_name='Measurements')

    if(measurement == 'Weight'):
        df = df[df['Unit'] == 'kg']
    elif(measurement == 'BMI'):
        df = df[df['Measurement'] == 'Body Mass Index (BMI)']
    else:
        df = df[df['Measurement'] == measurement]
   
    if(start != -1):    
        df = df[df['Date'] >= start]
    if(end != -1):
        df = df[df['Date'] <= end]
    
    if g:
        df.to_excel('Data.xlsx', index=False)
    graphtitle= measurement + " in time"
    df.plot(x='Date', y='Value', kind="scatter", c="Value", colormap="viridis", colorbar=False, title=graphtitle, ylabel=measurement)
    plt.show()
    return 0


if len(sys.argv) < 3:
    if (len(sys.argv) > 1 and sys.argv[1] == 'help'):
        print("Mynetdiary visualizer")
        print("Usage:\n\t", sys.argv[0], "input_file measurement_name [-start GG/MM/YY] [-end GG/MM/YY] [-g]")
        print("Arguments:\n \tinput_file must be a .xlsx file, or a .xls file\n\t Files int the .xls format will be automatically converted.\n\tmeasurement_name must be the name of a measurement\n\t in the original file, or the expressions Weight or BMI\n\t-start indicates the start date\n\t-end indicates end date\n\t-g generate output file Data.xlsx\n\t (default false)")
        sys.exit(0)
    print("Usage:", sys.argv[0], "input_file measurement_name [-start GG/MM/YYYY] [-end GG/MM/YY] [-g]")
    print("Example: ", sys.argv[0], "Mynetdiary.xlsx Weight -start 02/05/22 -end 02/07/22");
    print("See", sys.argv[0], "help for more options")
else:
    f = sys.argv[1]
    if not os.path.exists(f):
        print("Couldn't find the file:", f)
    if not f.endswith('.xlsx'):
        if f.endswith('.xls'):
            print("The extension .xls is not supported. Generating a new copy of your file in xlsx format.")
            subprocess.check_call(['libreoffice', '--headless', '--convert-to', 'xlsx', f])
            print("The file ", f + 'x has been generated.')
            f = f + 'x'
        else:
            print("The input file must be an Excel .xlsx file.\nFiles in the .xls format will be automatically converted.")
            sys.exit(1)
    m = sys.argv[2]
    if m.endswith('.xlsx'):
        print("Please insert one input file only. You can merge .xls or .xlsx files with ./excel_merger.py file1 file2 [file3 ...]")
    lenght = len(sys.argv)
    i = 3
    s = -1
    e = -1
    generate = False
    while(i < lenght):
        if(sys.argv[i] == '-start'):
            s = sys.argv[i+1]
            s = datetime.datetime.strptime(s, '%d/%m/%y').date()
            s = datetime.datetime.combine(s, datetime.time())
            i=i+2
            continue
        if(sys.argv[i] == '-end'):
            e = sys.argv[i+1]
            e = datetime.datetime.strptime(e, '%d/%m/%y').date()
            e = datetime.datetime.combine(e, datetime.time())
            i=i+2
            continue
        if(sys.argv[i] == '-g'):
            generate = True
        i=i+1
    main(f, m, s, e, generate);
