"""
Simple scraper using html, beautifulsoup, urllib2, and currency_converter to find the cheapest place to get airpods around the world.
"""


import urllib2,re
from currency_converter import CurrencyConverter as cc
from bs4 import BeautifulSoup

# Dictionary of all different countries, currencies, and full names
countries = {"us":("USD", "US"), "ca":("CAD", "Canada"), "cn":("CNY", "China"), "my":("MYR", "Malaysia"), 'uk':("GBP", "the UK"), 'jp': ("JPY", "Japan"), 'kr':("KRW", "Korea"), 'sg':("SGD", "Singapore")}

# currency_converter
c = cc()

product = "airpods"

prices = {}

print("Loading... \n")

for country in countries:
    # Product URL
    url = "https://www.apple.com/{}/shop/product/MMEF2C/A/{}".format(country, product)

    # return html 
    page = urllib2.urlopen(url)

    # parse html using beautiful soup
    soup = BeautifulSoup(page, 'html.parser')

    # find the name and the price of the airpods
    name_box = soup.find('h1', attrs={'class': 'materializer'})
    price_box = soup.find('span', attrs={'class':'current_price'})

    # strip away so only the name and price are left
    name = name_box.text.strip()
    price = price_box.text.strip()

    # change prices to numerics only for countries that have their own currency markers
    s = re.findall("\d+\,*\.*\d+", price)
    price1 = s[0].replace(',', '')

    # convert prices to canadian dollars
    CAD_price = c.convert(price1, countries[country][0], 'CAD')

    prices[CAD_price]= countries[country], price1


sorted_dict = sorted(prices.items())

location = sorted_dict[0][1][0][1]
local_price = str(sorted_dict[0][1][1])
local_currency = sorted_dict[0][1][0][0]
cad_equiv = str(sorted_dict[0][0])

print("The cheapest place to buy " + product + " is in " + location + ", for " + local_price + local_currency + ", which is " + cad_equiv + " CAD.")
