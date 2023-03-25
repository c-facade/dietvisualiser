#!/usr/bin/env python3

'''
Diet Visualizer (dietvisual)
Starting from a MyNetDiary data file, this program generates a plot of a certain measurement. 
'''

import datetime
import os
import sys
import subprocess
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main(file, measurement, start, end, g):
    df = pd.read_excel(file, sheet_name='Measurements')

    if(measurement == 'Weight'):
        df = df[df['Unit'] == 'kg']
    elif(measurement == 'BMI'):
        df = df[df['Measurement'] == 'Body Mass Index (BMI)']
    else:
        df = df[df['Measurement'] == measurement]
   
    if(start != ""): 
        df = df[df['Date'] >= start]
    if(end != ""):
        df = df[df['Date'] <= end]
    
    if g:
        print("Generating file Data.xlsx")
        df.to_excel('Data.xlsx', index=False) 
    
    graphtitle= measurement + " in time"
    df.plot(x='Date', y='Value', kind="scatter", c="Value", colormap="viridis", colorbar=False, title=graphtitle, ylabel=measurement)
    plt.show()
    return 0


parser = argparse.ArgumentParser(prog="dietvisual.py", description="Draws charts of data about weight, BMI, and other diet related measurements", usage='%(prog)s\n\tinput_file measurement_name\n\t[-start GG/MM/YY] [-end GG/MM/YY] [-g] [--help]')

parser.add_argument("input_file", help="The file that contains measurements data.\nMust be .xlsx or .xls file.\nFiles in the .xls format will be automatically converted.")
parser.add_argument("measurement_name", help="The name of the measurement you wish to visualise. Example: Weight, BMI, Daily Steps.")
parser.add_argument("-start", help="Start date in [DD/MM/YY] (day, month, year) format.", default="")
parser.add_argument("-end", help="End date in [DD/MM/YY] (day, month, year) format", default="")
parser.add_argument("-g", action="store_true", help="Generate output file data.xlsx (default false)")

args = parser.parse_args()

if not os.path.exists(args.input_file):
    print("Couldn't find the file:", args.input_file)
if not args.input_file.endswith('.xlsx'):
    if args.input_file.endswith('.xls'):
        print("The extension .xls is not supported. Generating a new copy of your file in xlsx format.")
        subprocess.check_call(['libreoffice', '--headless', '--convert-to', 'xlsx', args.input_file])
        print("The file ", args.input_file + 'x has been generated.')
        args.input_file = args.input_file + 'x'
    else:
        print("The input file must be an Excel .xlsx file.\nFiles in the .xls format will be automatically converted.")
        sys.exit(1)
if args.measurement_name.endswith('.xlsx') or args.measurement_name.endswith('.xls'):
    print("Please insert one input file only. You can merge .xls or .xlsx files with ./excel_merger.py file1 file2 [file3 ...]")
if(args.start != ""):
    args.start = datetime.datetime.strptime(args.start, '%d/%m/%y').date()
    args.start = datetime.datetime.combine(args.start, datetime.time())
if(args.end != ""):
    args.end = datetime.datetime.strptime(args.end, '%d/%m/%y').date()
    args.end = datetime.datetime.combine(args.end, datetime.time())
main(args.input_file, args.measurement_name, args.start, args.end, args.g);
