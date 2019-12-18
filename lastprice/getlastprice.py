#!usr/bin/env python
# encoding: utf-8

from lxml import html
import requests

import xml.etree.ElementTree as ET

stock_sell_lst = [
	
	# {"code": "ali", "lot" : 500,  "buy_price": 25.4, "percent_change_to_sell": 0.58}, 
	{"code": "nikl", "lot" : 1000,  "buy_price": 4.39, "percent_change_to_sell": 0.50}, 
	{"code": "fni", "lot" : 7000,  "buy_price": 1.49, "percent_change_to_sell": 0.50},
	{"code": "mpi", "lot" : 1000,  "buy_price": 3.15, "percent_change_to_sell": 0.06},

] 

stock_buy_lst = [
	{"code": "nikl", "lot" : 1000,  "buy_price": 2.5},
	{"code": "sm", "lot" : 5,  "buy_price": 880},
	{"code": "jgs", "lot" : 100,  "buy_price": 50},
	{"code": "mpi", "lot" : 1000,  "buy_price": 3.15},
] 
	


def getlastvalue(stockcode):
	code = stockcode.lower()
	url = 'https://www.marketwatch.com/investing/stock/{0}?countrycode=ph' .format(code)
	page = requests.get(url)
	tree = html.fromstring(page.content)

	last_price = float(tree.xpath('//span[@class="last-value"]/text()')[0].replace(",",''))

	# print ("Last price for {0} : {1}" .format(code, last_price))
	return last_price

def notifysell(stockcode, last_price, buy_price, percent_change_to_sell=None, lot=None):
	# SELL 
	percent_earning = round((last_price - buy_price)/buy_price * 100, 2)

	trade_amount = (last_price - buy_price)*lot
	commission = trade_amount*0.0025
	vat = commission * 0.12
	pse_fee = trade_amount*0.00005
	sccp_fee = trade_amount*0.0001
	sales_tax = lot*last_price*0.006
	total_fee = commission + vat + pse_fee + sccp_fee + sales_tax 

	net_gain = round(trade_amount - total_fee, 2)

	if last_price >= ((buy_price * percent_change_to_sell) + buy_price) :
		print ("SELL {0} {1} shares at {2}, earn {3} at {4}% ..." .format(  stockcode, lot,last_price, net_gain, percent_earning  ) )
	else: #HOLD
		print ("HOLD {0} {1} shares at {2}, {3}%..." .format(  stockcode, lot,last_price, percent_earning)       )
	
	return

def notifybuy(stockcode, last_price, buy_price, lot=None):
	if last_price <= buy_price:
		print ("BUY {0} {1} shares at {2} ..." .format(  stockcode, lot,last_price ) )
	return





if __name__ == '__main__':
    for dct in stock_sell_lst:
    	last_price = getlastvalue(dct['code'])
    	notifysell(dct['code'],last_price, dct['buy_price'], dct['percent_change_to_sell'], dct['lot'])
    for dct in stock_buy_lst:
    	last_price = getlastvalue(dct['code'])
    	notifybuy(dct['code'],last_price, dct['buy_price'], dct['lot'])







