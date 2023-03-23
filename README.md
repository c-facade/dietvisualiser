# dietvisualiser

This repository was born out of a very specific necessity: being able to visualise my diet information that I logged in the MyNetDiary app without paying.
In fact, I could download my data in the .xls format, but I couldn't use the graph function of the android app to visualise it.
I used pandas to import the data into a dataframe and generate charts.
I used argparse to deal with command line arguments.
The excel_merge is an utility to merge the files and convert them into xlsx. It uses libreoffice to do this conversion.
