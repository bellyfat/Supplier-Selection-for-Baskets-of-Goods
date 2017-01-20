# file name:  bom_quote.py

# Code outline
# Section 1: Import bill of materials in csv format
# Section 2: Query octopart's REST api
# Section 3: Analyze results


def import_bom(csvFileName = "arduino_bom.csv", toTest = False):
	"""
	Convert csv file into line items and queries
	
	Inputs:
	
	csvFileName = csv formatted file. This code assumes a file format similar to the one on the	Arduino BOM, file name arduino_bom.csv.  
	
	toTest = True truncates the output queries, to allow test of a subset of data.
	
	Outputs:
	
	line_items = list of lines in csv file that have both part bumbers and manufactures
	
	queries = list of dictionaries corresponding to each line_item
	"""
	
	import csv

	csv_file = open(csvFileName, "r")
	csv_reader = csv.DictReader(csv_file)
	line_items = []
	queries = []
	for line_item in csv_reader:

		# Skip line items without part numbers and manufacturers
		if not line_item['Part Number'] or not line_item['Manufacturer']:
			continue
		line_items.append(line_item)
		# if toTest:
			# print "toTest == True, line item is:", line_item, "\n"
		queries.append({'mpn': line_item['Part Number'],
						'brand': line_item['Manufacturer'],
						'reference': len(line_items) - 1})
		
	if toTest:
		print ("\n\ntoTest = True in import_bom")
		# return only a subset 
		line_items = line_items[:1]
		queries = queries[:1]
		print ("\tline_items:", line_items)
		print ("\tqueries:", queries)
		#assert False

	return line_items, queries	

#line_items, queries = \
#	import_bom(csvFileName = "arduino_bom.csv", toTest = True)

def send_queries(queries, toTest=False):
	"""
	Send queries to REST API for part matching.
	
	Inputs:
	
	queries = list of dictionaries formatted per octopart api
	
	Outputs:
	
	results = list of results
	
	"""
	
	import json
	import urllib

	results = []
	for i in range(0, len(queries), 20):
		# Batch queries in groups of 20, query limit of
		# parts match endpoint
		batched_queries = queries[i: i + 20]

		url = 'http://octopart.com/api/v3/parts/match?queries=%s' \
			% urllib.quote(json.dumps(batched_queries))
		#url += '&apikey=REPLACE_ME'
		url += '&apikey=ce6096b2'
		data = urllib.urlopen(url).read()
		response = json.loads(data)
		# print ("response:", response)

		# Record results for analysis
		results.extend(response['results'])

	if toTest:
		print "\n\ntoTest == True in send_queries"
		print "\tqueries sent = ", queries, "\n"
		# print "\tresults:\n:"
		# print results
		from pprint import pprint
		pprint (results)
	assert False	
	return results

#results = send_queries(queries)

def analyze(results, line_items, toTest=False):
	"""
	Analyze results sent back by Octopart API

	Inputs:
	
	results = list of results from API 
	
	line_items = list of line items from the Bill of Materials

	Outputs:
	
	itemsCount = int, number of items in Bill of Materials
	itemsNotFound = list, line_items having no results
	
	
	"""

	from decimal import Decimal

	print "Found %s line items in BOM." % len(line_items)
	itemsCount = len(line_items)
	# Price BOM
	hits = 0
	total_avg_price = 0
	
	itemsNotFound = []
	for result in results:
		line_item = line_items[result['reference']]
		if len(result['items']) == 0:
			print "Did not find match on line item %s" % line_item
			itemsNotFound = itemsNotFound.append(line_item)
			continue

		# Get pricing from the first item for desired quantity
		quantity = Decimal(line_items[result['reference']]['Qty'])
		prices = []
		for offer in result['items'][0]['offers']:
			if 'USD' not in offer['prices'].keys():
				continue
			price = None
			for price_tuple in offer['prices']['USD']:
				# Find correct price break
				if price_tuple[0] > quantity:
					break
				# Cast pricing string to Decimal for precision
				# calculations
				price = Decimal(price_tuple[1])
			if price is not None:
				prices.append(price)

		if len(prices) == 0:
			print "Did not find pricing on line item %s" % line_item
			continue
		avg_price = quantity * sum(prices) / len(prices)
		total_avg_price += avg_price
		hits += 1

	print "Matched on %.2f of BOM, total average price is USD %.2f" % ( \
		hits / float(len(line_items)), total_avg_price)
		
	return itemsNotFound, itemsCount
	
if __name__ == '__main__':
	line_items, queries = \
		import_bom(csvFileName = "arduino_bom.csv", toTest = True)
	results = \
		send_queries(queries, toTest = True)
	
	
	# itemsNotFound, itemsCount = \
		# analyze(results, line_items)
	# print "results[0][0]", results[0][0]
	# print "itemsNotFound:", itemsNotFound
	# print "itemsCount:", itemsCount

	
	