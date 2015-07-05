"""
small collection of google search functions
"""

import urllib, urllib2
import json
import sys

def query_url(query):
	"""
	create a google query
	 """
	return "http://www.google.com/search?" + urllib.urlencode({"q": query})

def autocomplete(query):
	"""
	get autocompletions using google autocomplete
	"""
	
	# create query url
	url = "http://suggestqueries.google.com/complete/search?" + urllib.urlencode({"client": "firefox", "q": query})

	# get json from google
	response = urllib2.urlopen(url)
	result = response.read()
	query, completions =  json.loads(result)
	
	# just return the completions
	return completions

if __name__ == "__main__":

	# get query from the command line
	if len(sys.argv) == 1:
		query = "google is"
	else:
		query = " ".join(sys.argv[1:])


	# get autocompletions
	completions = autocomplete(query)
	separator = "=" * max((len(c) for c in completions))

	# print query	
	print(separator)
	print(query + "...")
	print(separator)
	
	# print all completions
	for completion in completions:
		print(completion)
