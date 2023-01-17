import json
import uuid
from elasticsearch import Elasticsearch, exceptions, TransportError, RequestsHttpConnection
import os
import pprint
import time
from datetime import datetime
import sys
from selenium import webdriver
from parse_toAdd_for_preElastic import parse_toAdd_for_preElastic
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
# Look for False in scrape_and_index_itm_url 
def objScrape(pageString, itemurl):
    jsonStart = ""
    try:
        jsonStart = removeCharsToOpenBracket(pageString.split("product-json")[1].split("</")[0])
    except Exception as rcerr:
        print("[Error objScrape] in remove chars")
        print(rcerr) 
        return False

    json_parse_1 = parseJsonToCloseBracket(jsonStart)
    product_json_obj = json.loads(json_parse_1)
    product_json_obj["itemLink"] = itemurl 
    return product_json_obj

# @profile
def scrape_and_index_item_url(scrapeUrl, timeslug):
    print("Scrape new item url :: " + str(scrapeUrl))

    gsel.get(scrapeUrl)
    phtml = gsel.page_source

    objParse = objScrape(phtml, scrapeUrl)
    print("scrape new item result ::: ")
    print(objParse)

    if objParse == False:
        return

    # with open('../data/toAdd'+timeslug+'.txt', "a+") as taf:
    with open('../data/toAdd', "a+") as taf:
        taf.write(json.dumps(objParse) + "\n")



    index_to_add(timeslug)
    return objParse


def index_to_add(timeslug):

    
    parsedObjList = []
    with open('../data/toAdd') as taf:
        parsedObjList = taf.readlines()

    objLengthMax = 0
    objLengthMin = 0

    objLengthAvg = 0
    for obj in parsedObjList:
        objLengthAvg += len(json.dumps(obj))

    objLengthAvg = objLengthAvg / len(parsedObjList)

    index_add_doc = {

    # "add_items" : json.dumps(parsedObjList),
                        "add_file_name" : 'toAdd',
                        "items_length": len(parsedObjList),
                        "average_item_length": objLengthAvg,
                        "timestamp": int(round(time.time() * 1000)), 
                        "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }

    _3TradeElasticInstance.index(index="scrape_update", doc_type="_doc",body=index_add_doc)


def index_to_delete(timeslug):
    print("indexing delete update elastic doc")


    parsedObjList = []
    with open('../data/toDelete') as tdf:
        parsedObjList = tdf.readlines()

    index_delete_doc = {
                        "delete_file_name": 'toDelete',
                        "items_length": len(parsedObjList),
                        "timestamp": int(round(time.time() * 1000)), 
                        "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }

    _3TradeElasticInstance.index(index="scrape_update", doc_type="_doc",body=index_delete_doc)


def delete_item_by_url(url, timeslug):
    print("delete old item url ::: " + str(url))

    di_search = _3TradeElasticInstance.search(
index = sys.argv[1],
      body={"query":{"match_phrase":{"itemLink":url}}})

    if di_search["hits"]["total"]["value"] > 0:
        
        with open('../data/toDelete', "a+") as tdf:
            tdf.write( json.dumps({di_search["hits"]["hits"][0]["_id"]: di_search["hits"]["hits"][0]["_source"]})+ "\n")

        index_to_delete(timeslug)

        if sys.argv[2] == "Index":
            print("found delete hits")
            docId = di_search["hits"]["hits"][0]["_id"]
            try:
                print("Deleting url item")
                _3TradeElasticInstance.delete(index=sys.argv[1],id=docId)
            except Exception as err:
                print("Could not delete item. possibly not found in index")
                

    print("delete item done")




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


    with open("../data/diff_urls.txt", "a+") as file:
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
        # 'http://quotes.toscrape.com/page/1/',
        # 'http://quotes.toscrape.com/page/2/',
    ]
    urlnum = 0
    for url in urls:
        urlnum +=1
        print("url request #" + str(urlnum))
        gsel.get(url)
        page = gsel.page_source
        get_item_urls(page)


Full_Run = False
if __name__ == "__main__":
    print("init diff url scrape")
    print("FULL RUN ENABLED ::: " + str(Full_Run))
    
    if checkElasticStatus() == False:
        print('ElasticSearch is not running ... ')
        sys.exit()



    ci_search = _3TradeElasticInstance.search(index="st_items_k2t1",body={
        "query":{"match":{"userId":"StewartSurfboards"}}
        }, size = 300)

    old_url_file = "../data/cur_urls.txt"    
    new_url_file = "../data/diff_urls.txt"

    if Full_Run == True:

        with open(old_url_file, "a+") as cf:
            for hit in ci_search["hits"]["hits"]:
                print("appending cur url :: " + str(hit["_source"]["itemLink"]))
                cf.write(hit["_source"]["itemLink"].replace("'","").replace('"', "").replace("\n", "") + "\n")

        gsel = webdriver.PhantomJS()
        # Populate diff_urls.txt   with scraped urls from website. Takes a minute
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
    if Full_Run == True:
        
        for line in linesNew:
            print("comparing new line")
            if line not in linesOld:
                print("new line not in old ::: " + str(line))
                scrape_and_index_item_url(line, file_time_slug)

    remLines = []
    for line in linesOld:
        print("comparing old line")
        if line not in linesNew:
            remLines.append(line)
            print("old url not in new ::: " + str(line))
            delete_item_by_url(line, file_time_slug)

    
    if len(remLines) > 0:
        print("found len remlines gt zero")
        action_filename = "removed_items_"
        if sys.argv[2] != "Index":
            action_filename = "toDelete_items_"

        with open('../updates/'+ action_filename , 'a+') as remf:
            remf.write(json.dumps(remLines))


    if (os.path.exists("../data/toAdd")):
        parse_toAdd_for_preElastic("../data/toAdd")
    print("url scrape compare complete")







