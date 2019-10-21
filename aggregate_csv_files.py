
import os
import glob
import pandas as pd
os.chdir('C:/python/projects/giraffe/viasat_data')
cwd = os.getcwd()
cwd

# match pattern of .csv files
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
type(all_filenames)

# Combine all files in the list and export as unique CSV
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
