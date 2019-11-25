#!/usr/bin/env python
"""

MovieGoer.py

Lookup for cinemas from local malls. Gets schedules , ratings, details etc.
I plan to run this on termux. So double quotes are not needed when using commandline parameters 

Pagination is not supported (yet).

TODO: 

- caching 
- movie info, ratings
- tabulate results (ok)
- Add date option (+1...3day)
"""
import re
import urllib.parse
import argparse
import requests
from tabulate import tabulate
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
        output_table = []  
        for cinema in cinemas: 
              
            movie_title = cinema.select("a > span[itemprop='name']")
            cinema_name = cinema.select("div.panel-heading")[0].get_text() # TODO might ask for optional parameter to include cinema name to save screen space for mobile. also I don't need cinema name for my case but will still add option just in case
            if movie_title: # also determine if has content. Vacant cinemas will return None
                # cinema name, 
                # schedule
                showtimes_list = cinema.find("div", attrs={"class": "showtimes"}).find_all("span")
                showtimes = " ".join(x.get_text() for x in showtimes_list)

                output_table.append([movie_title[0].get_text(), showtimes])
                


            # print(cinema.select("a > span[itemprop='name']")[0].get_text() ) 
            # wip
            # TODO get time, rating, etc.
        else:
            print("")
            print(tabulate(output_table, headers=["Movie Title", "Showtimes"] ))
            print("")
    

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
            # automatically redirect if only 1 match found
            a = matches[0].find("a", attrs={"title": re.compile("^Cinemas")})
            url = a['href']
            
        elif match_count > 1:
            menu = []
            for index, search_item in enumerate(matches, start=1):
                mall_result_name = search_item.find("a").get_text();
                menu.append([index, mall_result_name])

                # print(index, search_item.find("a").get_text())
            print(tabulate(menu, headers=["Number", "Mall Name"]))
                
            # Prompt for user to enter mall/theater name
            choice = 0
            is_invalid = True
            while is_invalid:
                choice = int(input("Enter result number: "))
                if choice > 0 and choice <= match_count :
                    a = matches[choice-1].find("a", attrs={"title": re.compile("^Cinemas")})
                    url = a['href']
                    is_invalid = False
                else:
                    print("You have entered an invalid number. Please re-enter")
                    print(tabulate(menu, headers=["Number", "Mall Name"]))
        else:
            print("No matches")
        moviegoer.scrape_cinema_page(url)

    else:
        print("No Results found")


    # TODO: 
    # get link of first item ask to proceed if found (maybe(?))
    # go to link ex: https://m.clickthecity.com/movies/theaters/sm-city-bicutan
    # scrape contents 




# import requests

if __name__ == "__main__":
    main()