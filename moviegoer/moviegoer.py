#!/usr/bin/env python
"""

MovieGoer.py

Lookup for cinemas from local malls. Gets schedules , ratings, details etc.
I plan to run this on termux. So double quotes are not needed when using commandline parameters 

Pagination is not supported (yet).

TODO: 
- caching 
- movie info, ratings
- tabulate results

"""
import re
import urllib.parse
import argparse
import requests
from bs4 import BeautifulSoup

class MovieGoer:
    def __init__(self):
        self.base_url = "https://m.clickthecity.com"
        self.headers = {"user-agent" : "Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}  
        # yeah let's pretend we're a mobile phone. 
        self.mall_name = None
        self.session = requests.Session()
    

    def search_mall(self, mall_name):
        self.mall_name = mall_name

        url = f"{self.base_url}/search/?q={urllib.parse.quote(mall_name)}"
        response = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser") 
        search_results = soup.select("div.searchItem")
        return search_results

    def scrape_cinema_page(self, url: str):

        
        r = self.session.get(url,headers=self.headers)
        
        # get featured movie 

        soup = BeautifulSoup(r.text, 'html.parser') # TODO use lxml
        cinemas = soup.select("div#cinemas div[itemprop='itemListElement']")
        print(len(cinemas), "Movies found: ")
        for cinema in cinemas: 
            print(cinema.select("a > span[itemprop='name']")[0].get_text() ) 
            # wip
            # TODO get time, rating, etc.
        

    def run(self): # we'll put every execution eventually on a function
        pass

def main():
    """ Main """
    parser = argparse.ArgumentParser(description='Search details ')
    parser.add_argument('mall_name', metavar='Mall Name', nargs="*", type=str,
                        help='an integer for the accumulator')

    args = parser.parse_args()
    if args.mall_name:
        mall_name = " ".join(args.mall_name)
    else:
        mall_name = input("Enter Mall Name: ")

    moviegoer = MovieGoer()
    search_results = moviegoer.search_mall(mall_name)


    if search_results:
        # TODO put in class method
        # TODO add optional parameter for instant redirect on first item
    
        matches = list(filter(lambda item: item.find("div", attrs={"class": "mall-links"}), search_results))
        match_count = len(matches)
        
        if match_count == 1:
            a = matches[0].find("a", attrs={"title": re.compile("^Cinemas")})
            url = a['href']
            moviegoer.scrape_cinema_page(url)
            
        elif match_count > 1:

            for index, search_item in enumerate(matches, start=1):

                print(index, search_item.find("a").get_text())
            
        else:
            print("No Mall Results found")

            # TODO if has .mall-links then print 


    else:
        print("No Results found")


    # TODO: 
    # get link of first item ask to proceed if found (maybe(?))
    # go to link ex: https://m.clickthecity.com/movies/theaters/sm-city-bicutan
    # scrape contents 




# import requests

if __name__ == "__main__":
    main()