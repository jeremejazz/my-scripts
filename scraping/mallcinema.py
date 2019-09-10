#!/usr/bin/python
"""

Mall Cinema

Lookup for cinemas from local malls. Gets schedules , ratings, details etc.

"""
import urllib.parse
import argparse
import requests
from bs4 import BeautifulSoup

def main():
	parser = argparse.ArgumentParser(description='Search details ')
	parser.add_argument('mall_name', metavar='Mall Name', type=str,
                    help='an integer for the accumulator')
	
	args = parser.parse_args()

	url = "https://m.clickthecity.com/search/?q={}".format(urllib.parse.quote(args.mall_name))
	headers = {"user-agent" : "Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
	
	s = requests.Session()
	s.get(url,headers=headers)
	
	# test for now 
	r = requests.get(url, headers=headers)
	print(r.text)
	
	# TODO: 
	# get link of first item ask to proceed if found (maybe(?))
	# go to link ex: https://m.clickthecity.com/movies/theaters/sm-city-bicutan
	# scrape contents 




# import requests

if __name__ == "__main__":
	main()