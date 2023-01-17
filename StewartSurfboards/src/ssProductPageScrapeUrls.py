import scrapy

import json
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from random import randint

def getItemUrls(pageData):
        alphaData = pageData.split("data-alpha")
        allItemUrls = []

        for ad in alphaData:
            if "product-info" in ad:
                piSplit = ad.split("product-info")
                pi1 = piSplit[1].split("=")
                pi2 = pi1[1].split(">")
                piData = pi2[0] + "\n"
                print(piData)
                if len(piData) < 123 and len(piData) > 17:
                    allItemUrls.append(piData.replace("\"","").replace('"',""))

        
        with open("../data/stewartItemUrls.txt", "a+") as file:
            for urlLine in allItemUrls:
                file.write(urlLine)

class StewartSpider(scrapy.Spider):
    name = "prodscrape"


    def start_requests(self):
        self.log("req started")
        urls = [
        "https://stewart-surfboards.myshopify.com/collections/surfboards?page=1",
        "https://stewart-surfboards.myshopify.com/collections/surfboards?page=2",
        "https://stewart-surfboards.myshopify.com/collections/surfboards?page=3",
        "https://stewart-surfboards.myshopify.com/collections/surfboards?page=4",
        "https://stewart-surfboards.myshopify.com/collections/surfboards?page=5",
        # "https://stewart-surfboards.myshopify.com/collections/surfboards?page=6"
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        urlnum = 0
        for url in urls:
            urlnum +=1
            self.log("url request #" + str(urlnum))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("resurl")
        print(response.url)
        page = response.url[-1]

        filename = 'stewart_data-%s.html' % page
        self.log("save to filename")
        self.log(filename)

        pageBytes = response.body
        pageText = response.text

        getItemUrls(pageText)

        with open('../data/url_html_pages/' + filename, 'wb') as f:
            f.write(pageBytes)
        self.log('Saved file %s' % filename)








