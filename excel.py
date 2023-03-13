'''
Playing with pandas
'''

import datetime
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def main(file, measurement, start, end):
    command = "libreoffice --headless --convert-to xlsx" + file
    os.system(command)
    
    # stupid hack
    df = pd.read_excel(file + 'x', sheet_name='Measurements')

    if(measurement == 'Weight'):
        df = df[df['Unit'] == 'kg']
    elif(measurement == 'BMI'):
        df = df[df['Measurement'] == 'Body Mass Index (BMI)']

    else:
        df = df[df['Measurement'] == measurement]
    
    # TODO: check how to convert dates
    if(start != -1):
        df = df[df['Date'] >= start]
    if(end != -1):
        df = df[df['Date'] <= end]

    df.to_excel('Dati.xlsx', index=False)
    df.plot(x='Date', y='Value')
    plt.show()
    return 0


if len(sys.argv) < 3:
    print("Usage:", sys.argv[0], "input_file measurement_name [-start GG/MM/YYYY] [-end GG/MM/YYYY]")
    print("Example: ", sys.argv[0], "Mynetdiary.xls Weight -start 02/05/22 -end 02/07/22");
else:
    f = sys.argv[1]
    m = sys.argv[2]
    lenght = len(sys.argv)
    i = 3
    s = -1
    e = -1
    while(i < lenght):
        if(sys.argv[i] == '-start'):
            s = datetime.datetime.strptime(sys.argv[i+1], '%d/%m/%y').date()
            i=i+2
            continue
        if(sys.argv[i] == '-end'):
            e = datetime.datetime.strptime(sys.argv[i+1], '%d/%m/%y').date()
            i=i+2
            continue
        i=i+1
main(f, m, s, e);
