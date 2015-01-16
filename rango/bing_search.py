import json
import urllib, urllib2

BING_API_KEY = '33my+jO2tvvODcCjv1ft0rtgI7z3NkE5YZ+lEDegTo8'

def run_query(search_terms):
	# Specify the base
	root_url = "https://api.datamarket.azure.com/Bing/Search/"
	source = 'Web'

	# Specify number of results per page and the starting offset
	# for example, 10 per page and an offset of 11 would start on
	# page 2
	results_per_page = 10
	offset = 0

	# Wrap quotes around query as required by Bing API
	query = "'{0}'".format(search_terms)
	query = urllib.quote(query)

	# Construct the latter part of our request's url.
	# Sets the format of the response to JSON as well as other properties
	search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
		root_url,
		source,
		results_per_page,
		offset,
		query)

	# Setup authentication with the Bing servers
	# Username must be a black string
	username = ''

	# Create a password manager that handles authentication for us
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, BING_API_KEY)

	# Create results list to be populated later
	results = []

	try:
		# Prepare to connect to Bing servers
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

		# Connect to the server and read the response generated
		response = urllib2.urlopen(search_url).read()

		# Convert string response to Python dict
		json_response = json.loads(response)

		# Loop through results and populate out response list
		for result in json_response['d']['results']:
			results.append({
				'title': result['Title'],
				'url': result['Url'],
				'summary': result['Description']})

	except urllib2.URLError, e:
		print "Error when querying Bing Search API: ", e

	# Return the list of results to the calling function
	return results


def main():
	search_terms = raw_input("Enter your search terms: ")
	output = run_query(search_terms)

	for line in output:
		print "{0}\n-------------\n{1}\n------------\n{2}\n\n".format(
			line['title'].encode('utf-8'),
			line['url'].encode('utf-8'),
			line['summary'].encode('utf-8'))


if __name__ == '__main__':
	main()