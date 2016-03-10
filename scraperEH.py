from requests import get
import csv
import re
from datetime import datetime
from time import sleep

#list for both nasdaq and nyse stocks gotten on Aug. 17, 2015

#THIS IS FOR EXTENDED HOURS

if __name__ == "__main__":
	with open('tempstocklist.csv', 'rb') as read_file:
		csvreader = csv.reader(read_file)
		stock_list = csvreader.next()

	stock_list = ['AAME']

	for stock in stock_list:
		sleep(1)
		print 'Updating ' + stock + '...'

		resp = get('http://www.google.com/finance/getprices?i=60&p=15d&sessions=ext_hours&f=d,c,v,o,h,l&df=cpct&q=' + stock)

		html =  resp.content

		lines = html.split('\n')
		if len(lines) <= 8:
			continue
		lines = lines[8:-1]

		with open('output/extended/' + stock + '.Last.txt', 'wb') as stock_file:
			csvwriter = csv.writer(stock_file, delimiter=';')
			new_day = 0
			for line in lines:
				try:
					if re.search('a(\d+)', line):
						new_day = int(float(re.search('a(\d+)', line).group(1)))
						close, high, low, openn, volume = line.split(',')[1:]
						csvwriter.writerow([
							datetime.fromtimestamp(new_day).strftime('%Y%m%d %H%M%S'),
							openn, high, low, close, volume
						])
					else:
						minut, close, high, low, openn, volume = line.split(',')
						csvwriter.writerow([
							datetime.fromtimestamp(new_day + int(float(minut))*60).strftime('%Y%m%d %H%M%S'),
							openn, high, low, close, volume
						])
				except ValueError:
					continue
