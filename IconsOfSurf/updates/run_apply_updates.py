import json
import uuid
from elasticsearch import Elasticsearch, exceptions, TransportError, RequestsHttpConnection
import os
import pprint
import time
from datetime import datetime
import sys
from selenium import webdriver
import requests

sys.path.append("../src")

from product_page_url_scrape import scrape_product_url

# from memory_profiler import profile

# print("init")
# fpmem=open('saveDelete_Memory_.log','w+')
# @profile(stream=fpmem)

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

if __name__ == "__main__":

    print("Checking elastic status ::: ")
    checkElasticStatus()
    _3TradeElasticInstance = Elasticsearch()
    DELETE_FILE_NAME = "toDelete_urls_"	
    UPDATE_FILE_NAME = "to_update_data"

    diff_url_data = []

    df_urls = []
    with open(DELETE_FILE_NAME) as df:
        df_urls = df.readlines()


    for durl in df_urls:
        print("Deleting url:::" + str(durl))
        _3TradeElasticInstance.delete_by_query(index= sys.argv[1],body= \
            {"query":{"match_phrase": {"itemLink":durl}}})
        print("Done")

    ud_urls = []
    with open(UPDATE_FILE_NAME) as udf:
        ud_urls = udf.readlines()
    
    for urldataitem in ud_urls:
        try:
            urldataitem = json.loads(urldataitem)
            print("urldata item url")
            print(urldataitem["url"])

            scrape_product_url(urldataitem["url"], urldataitem["base"])
        
        except Exception as e:
            print(e)
            print("error") 


