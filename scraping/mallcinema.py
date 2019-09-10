#!/usr/bin/python
"""

Mall Cinema

Lookup for cinemas from local malls. Gets schedules , ratings, details etc.
I plan to run this on termux. So double quotes are not needed when using commandline parameters 

"""
import urllib.parse
import argparse
import requests
from bs4 import BeautifulSoup

def main():
	parser = argparse.ArgumentParser(description='Search details ')
	parser.add_argument('mall_name', metavar='Mall Name', nargs="*", type=str,
                    help='an integer for the accumulator')
	
	args = parser.parse_args()
	if args.mall_name:
		mall_name = " ".join(args.mall_name)
	else:
		mall_name = input("Enter Mall Name: ")

	url = "https://m.clickthecity.com/search/?q={}".format(urllib.parse.quote(mall_name))
	headers = {"user-agent" : "Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
	
	s = requests.Session()
	s.get(url,headers=headers)
	
	# test for now 
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, "html.parser") 
	search_results = soup.select("div.searchItem")
	if search_results: 
		print("results found: ")
		# TODO add optional parameter for instant redirect on first item

		for index, search_item in enumerate(search_results, start=1):

			print(index, search_item.find("a").get_text())

			# TODO if has .mall-links then print 

		target = input("Select item: ")

	else:
		print("No Results found")


	# TODO: 
	# get link of first item ask to proceed if found (maybe(?))
	# go to link ex: https://m.clickthecity.com/movies/theaters/sm-city-bicutan
	# scrape contents 




# import requests

if __name__ == "__main__":
	main()