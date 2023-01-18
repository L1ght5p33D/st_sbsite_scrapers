import json
import uuid
from elasticsearch import Elasticsearch, exceptions, TransportError, RequestsHttpConnection
import os
import pprint
import time
from datetime import datetime
import sys
from selenium import webdriver
from parse_scraped_for_preElastic import parse_scraped_for_preElastic
import requests
from helper_scrape_methods import countTotalBracketsInJson, parseJsonToCloseBracket, removeCharsToOpenBracket

# from memory_profiler import profile

# print("init")
# fpmem=open('saveDelete_Memory_.log','w+')
# @profile(stream=fpmem)

gsel = webdriver.PhantomJS()
_3TradeElasticInstance = Elasticsearch()

def checkElasticStatus():
    print("checking elastic status")
    port_9200_res = requests.get("http://localhost:9200")
    try:
        json.loads(port_9200_res.text)
        if "You Know, for Search" in port_9200_res.text:
            print("ELASTIC RUNNING")
            return True
    except:
        print("couldnt load json")
        return False
    return False
    print("done")





def get_item_urls(pageData):
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
                allItemUrls.append("https://stewart-surfboards.myshopify.com" + piData.replace("\"","").replace('"',""))


    with open("../data/diff_urls", "a+") as file:
        for urlLine in allItemUrls:
            print("adding diff url in scrape ::: ")
            print(urlLine)
            file.write(urlLine)


def scrape_new_urls():
    print("scrape new url init")
    
    print("req started")
    urls = [
    "https://stewart-surfboards.myshopify.com/collections/surfboards?page=1",
    "https://stewart-surfboards.myshopify.com/collections/surfboards?page=2",
    "https://stewart-surfboards.myshopify.com/collections/surfboards?page=3",
    "https://stewart-surfboards.myshopify.com/collections/surfboards?page=4",
    "https://stewart-surfboards.myshopify.com/collections/surfboards?page=5",
    "https://stewart-surfboards.myshopify.com/collections/surfboards?page=6"
    ]
    urlnum = 0
    for url in urls:
        urlnum +=1
        print("url request #" + str(urlnum))
        gsel.get(url)
        page = gsel.page_source
        get_item_urls(page)


if __name__ == "__main__":
    print("init url scrape")
    
    if checkElasticStatus() == False:
        print('ElasticSearch is not running ... ')
        sys.exit()


    ci_search = _3TradeElasticInstance.search(index="st_items_k2t1",body={
        "query":{"match":{"userId":"StewartSurfboards"}}
        }, size = 300)

    old_url_file = "../data/cur_urls.txt"    
    new_url_file = "../data/diff_urls.txt"

    with open(old_url_file, "a+") as cf:
        for hit in ci_search["hits"]["hits"]:
            print("appending cur url :: " + str(hit["_source"]["itemLink"]))
            cf.write(hit["_source"]["itemLink"].replace("'","").replace('"', "").replace("\n", "") + "\n")

    # Populate diff_urls with scraped urls from website
    scrape_new_urls()

    linesNew = []
    linesOld = []
    lineIdx = 0
    print("Reading old and new url files for diff comparison")
    with open(old_url_file) as ofile:
        linesOld = ofile.readlines()

    with open(new_url_file) as nfile:
        linesNew = nfile.readlines()
    
    
    file_time_slug = datetime.now().strftime("%m-%d-%Y--%H%M")    
    for newurl in linesNew:
        print("comparing new line")
        if newurl not in linesOld:
            print("new line not in old ::: " + str(newurl))
            #scrape_item_url(newurl, file_time_slug)

    remLines = []
    for line in linesOld:
        print("comparing old line")
        if line not in linesNew:
            remLines.append(line)
            print("old url not in new ::: " + str(line))
            #delete_item_by_url(line, file_time_slug)
            

    with open( "../data/toDelete_urls" , "a+") as remf:
        for line in remLines:
            remf.write(line + "\n" )

    with open( "../data/toAdd_urls", "a+" ) as addf:
        for line in addLines:
            addf.write(line + "\n")


    if (os.path.exists("../data/scraped_items")):
        parse_scraped_for_preElastic(sitem)
    
    print("url scrape complete")







