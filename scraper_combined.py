from requests import get
import csv
import re
from datetime import datetime, time
from time import sleep

#both ETH and RTH

def time_overlaps_regular(check_time):
	if (time(9, 30, 0) < check_time <= time(16, 0, 0)):
		return True
	return False


if __name__ == "__main__":
	with open('allstocks_current.csv', 'rb') as read_file:
		csvreader = csv.reader(read_file)
		stock_list = csvreader.next()

	#stock_list = ['FPO^A']

	for stock in stock_list:
		sleep(1)
		print 'Updating ' + stock + '...'

		reg_data = []
		extended_data = []

		resp = get('http://www.google.com/finance/getprices?i=60&p=15d&f=d,o,h,l,c,v&df=cpct&q=' + stock)

		html =  resp.content

		lines = html.split('\n')
		if len(lines) <= 7:
			continue
		lines = lines[7:-1]

		new_day = 0
		for line in lines:
			try:
				if re.search('a(\d+)', line):
					new_day = int(float(re.search('a(\d+)', line).group(1)))
				else:
					minut, close, high, low, openn, volume = line.split(',')
					reg_data.append([
						datetime.fromtimestamp(new_day + int(float(minut))*60).strftime('%Y%m%d %H%M%S'),
						openn, high, low, close, volume
					])
			except ValueError:
				continue

		resp = get('http://www.google.com/finance/getprices?i=60&p=15d&sessions=ext_hours&f=d,c,v,o,h,l&df=cpct&q=' + stock)

		html =  resp.content

		lines = html.split('\n')

		if len(lines) <= 8:
			with open('output/combined/' + stock + '.Last.txt', 'wb') as write_file:
				csvwriter = csv.writer(write_file, delimiter=';')
				for row in reg_data:
					csvwriter.writerow(row)
			continue

		lines = lines[8:-1]

		new_day = 0
		for line in lines:
			try:
				if re.search('a(\d+)', line):
					new_day = int(float(re.search('a(\d+)', line).group(1)))
					close, high, low, openn, volume = line.split(',')[1:]
					if time_overlaps_regular(datetime.fromtimestamp(new_day).time()):
						continue
					extended_data.append([
						datetime.fromtimestamp(new_day).strftime('%Y%m%d %H%M%S'),
						openn, high, low, close, volume
					])
				else:
					minut, close, high, low, openn, volume = line.split(',')
					if time_overlaps_regular(datetime.fromtimestamp(new_day + int(float(minut))*60).time()):
						continue
					extended_data.append([
						datetime.fromtimestamp(new_day + int(float(minut))*60).strftime('%Y%m%d %H%M%S'),
						openn, high, low, close, volume
					])
			except ValueError:
				continue

		data_sorted = sorted(reg_data + extended_data, key=lambda x: datetime.strptime(x[0], '%Y%m%d %H%M%S'))

		with open('output/combined/' + stock + '.Last.txt', 'wb') as write_file:
			csvwriter = csv.writer(write_file, delimiter=';')
			for row in data_sorted:
				csvwriter.writerow(row)
