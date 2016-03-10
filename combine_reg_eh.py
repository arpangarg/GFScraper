import csv
from datetime import datetime, time

#script for combining data scraped for RTH and ETH

def time_overlaps_regular(check_time):
	if (time(9, 30, 0) < check_time <= time(16, 0, 0)):
		return True
	return False


reg_data = []
extended_data = []

with open('output/reg/AAPL.Last.txt', 'rb') as read_file:
	csvreader = csv.reader(read_file, delimiter=';')
	for row in csvreader:
		reg_data.append(row)

with open('output/extended/AAPL.Last.txt', 'rb') as read_file:
	csvreader = csv.reader(read_file, delimiter=';')
	for row in csvreader:
		if time_overlaps_regular(datetime.strptime(row[0], '%Y%m%d %H%M%S').time()):
			continue
		extended_data.append(row)

data_sorted = sorted(reg_data + extended_data, key=lambda x: datetime.strptime(x[0], '%Y%m%d %H%M%S'))

with open('output/AAPLcombined.txt', 'wb') as write_file:
	csvwriter = csv.writer(write_file, delimiter=';')
	for row in data_sorted:
		csvwriter.writerow(row)
