import json
import time
import datetime
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from elasticsearch import Elasticsearch, exceptions, TransportError
import binascii
from os import urandom
import requests
import urllib3
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.setdefaultencoding('ascii')


# python src/run_gen_diff_urls.py st_items_k2t2m1 /home/si/os_projects/SurfTrader/1_serve_surftrader/SCRAPE/Surftrade_Scrapers/auto_scrape_scripts/TheBoardSource/data /home/si/os_projects/SurfTrader/1_serve_surftrader/SCRAPE/Surftrade_Scrapers/auto_scrape_scripts/chromedriver

_1337ElasticInstance = Elasticsearch()

def generateUID():
    return binascii.b2a_hex(urandom(18)).decode("utf-8")

chrome_options = Options()
chrome_options.add_argument("--headless")
gsel = webdriver.Chrome(sys.argv[3], options=chrome_options)


def get_item_urls_from_special_endpoint():
    page=0
    getPages = 1

    #later load more with element click
    #clickable = driver.findElement(By.class("botiga-pagination-button"));
    #clickable.click()

    while page < getPages:
        gsel.get("https://theboardsource.com/product-category/surfboards-collection/")

                # https://theboardsource.com/wp-json/wc/v2/products?per_page=16&category=12&page=1&order=desc&min_price=0&max_price=200000&consumer_key=ck_f8a9d0f0a65c24b5f4363fd396c218e87b205a0f&consumer_secret=cs_997bd4619188cd08ad0ad38a8b0273854092ed8d

	
        # split_perma = pageSource.split('permalink":"')
        # split_prod = pageSource.split('product type-product')
        # for bns in split_prod:
        pageSource = gsel.page_source
        # print("get page src ~ " + pageSource)
        split_woo_link = pageSource.split('woocommerce-LoopProduct-link')[1]
        print("split_woo link:::")
        print(split_woo_link)
        if "href" in split_woo_link:
            split_link = split_woo_link.split("href=\"")[1].split("\"")[0]
            print("got split link ~ " + split_link)
            with open( sys.argv[2] +  '/tbs_item_urls', 'a+') as tbs_url_file:
                tbs_url_file.write(split_link + "\n")
        page +=1









if __name__ == '__main__':

    get_item_urls_from_special_endpoint()

    













