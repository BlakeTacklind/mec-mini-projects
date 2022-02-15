import requests
import json
import re
import math
import statistics

#since dataset is no longer free to use, using provided set given by another student
JSON_URL = "https://www.quandl.com/api/v3/datasets/FSE/AFX_X/data.json"
#
YEAR_TO_FIND = 2017

def main():
	json_data = json.loads(requests.get(JSON_URL).text)

	#get subset of dates we care about and convert it into a format 
	setOfYear = list(filter(lambda x: x.year == YEAR_TO_FIND, map(TradeData, json_data['dataset_data']['data'])))
	#sort to gets dates in order, used in largest day to day close value diff
	setOfYear.sort(key = lambda x: x.date)

	#get a dictionary of the initial dataset
	results = initialData()

	#filter through items
	lastDay = None
	for val in setOfYear:
		#get low value
		if val.low < results['min']['value']:
			results['min']['value'] = val.low
			results['min']['date'] = val.date

		#get high value
		if val.high > results['max']['value']:
			results['max']['value'] = val.high
			results['max']['date'] = val.date

		#get daily high-low delta value
		if abs(val.high - val.low) > results['change']['value']:
			results['change']['value'] = abs(val.high - val.low)
			results['change']['date'] = val.date

		#get largest diff data to dat
		if lastDay is not None:
			if abs(val.close - lastDay.close) > abs(results['closeChange']['value']):
				results['closeChange']['value'] = val.close - lastDay.close
				results['closeChange']['dateStart'] = lastDay.date
				results['closeChange']['dateEnd'] = val.date

		lastDay = val

		results['averageTrade']['sum'] += val.volume
		results['averageTrade']['count'] += 1

	#print results
	print(f"Lowest Value: {results['min']['value']} on {results['min']['date']}")
	print(f"Highest Value: {results['max']['value']} on {results['max']['date']}")
	print(f"One Day Change: {results['change']['value']:.2f} on {results['change']['date']}")
	print(f"Largest Day to Day Close: {results['closeChange']['value']:.2f} from {results['closeChange']['dateStart']} to {results['closeChange']['dateEnd']}")
	print(f"Mean Trade Volume: {results['averageTrade']['sum'] / results['averageTrade']['count']:.1f}")
	print(f"Median Trade Volume: {statistics.median(map(lambda x: x.volume, setOfYear))}")

def initialData():
	return {
		'min':{
			'value': math.inf,
			'date': ''
		},
		'max':{
			'value': -math.inf,
			'date': ''
		},
		'change':{
			'value': 0,
			'date': ''
		},
		'closeChange':{
			'value': 0,
			'dateStart': '',
			'dateEnd': ''
		},
		'averageTrade':{
			'sum': 0,
			'count': 0
		}
	}

COLUMN_FOR_DATE = 0
COLUMN_FOR_HIGH = 2
COLUMN_FOR_LOW = 3
COLUMN_FOR_CLOSE = 4
COLUMN_FOR_TRADE_VOL = 6

p = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})')
class TradeData(object):
	def __init__(self, datum):
		self._datum = datum

	@property
	def year(self):
		m = p.match(self._datum[COLUMN_FOR_DATE])

		if m is None:
			print(self._datum)
			raise Exception("No match on the date")

		year = None
		try:
			return int(m.group('year'))
		except ValueError:
			print(self._datum)
			raise Exception("got a value error in year")

	@property
	def date(self):
		return self._datum[COLUMN_FOR_DATE]

	@property
	def high(self):
		return float(self._datum[COLUMN_FOR_HIGH])

	@property
	def low(self):
		return float(self._datum[COLUMN_FOR_LOW])

	@property
	def close(self):
		return float(self._datum[COLUMN_FOR_CLOSE])

	@property
	def volume(self):
		return float(self._datum[COLUMN_FOR_TRADE_VOL])

	
if __name__ == '__main__':
	main()
