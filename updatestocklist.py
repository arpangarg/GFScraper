from os import listdir
from os.path import isfile, join
import csv

toslistpath = '../shareHost/toslists/'
list_files = [ f for f in listdir(toslistpath) if isfile(join(toslistpath,f)) ]

main_list = []
previous_list = []

for one_file in list_files:
	with open(toslistpath + one_file, 'rb') as read_file:
		csvreader = csv.reader(read_file)
		start = False
		for row in csvreader:
			if start:
				main_list.append(row[0])
			if len(row) > 0:
				if ((not start) and (row[0] == "Symbol" or row[0] == "Contract")):
					start = True

main_list = list(set(main_list))


with open('allstocks_current.csv', 'rb') as read_file:
	csvreader = csv.reader(read_file)
	previous_list = csvreader.next()

with open('allstocks_current_backup.csv', 'wb') as write_file:
	csvwriter = csv.writer(write_file)
	csvwriter.writerow(previous_list)

updated_list = sorted(list(set(previous_list + main_list)))

#check new tickers added
#print list(set(updated_list) - set(previous_list))

with open('allstocks_current.csv', 'wb') as write_file:
	csvwriter = csv.writer(write_file)
	csvwriter.writerow(updated_list)
