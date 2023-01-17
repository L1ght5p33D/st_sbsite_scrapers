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
from product_page_url_scrape import scrape_product_url



# from memory_profiler import profile
# fpmem=open('saveDelete_Memory_.log','w+')
# @profile(stream=fpmem)


if __name__ == "__main__":

    print("Checking elastic status ::: ")
    _3TradeElasticInstance = Elasticsearch()
    DELETE_FILE_NAME = sys.argv[2] + "/toDelete_urls"	
    UPDATE_FILE_NAME = sys.argv[2] + "/to_update_data"

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
            item_url_w_base = "https://www.iconsofsurf.com" + urldataitem["url"]
            scrape_product_url(item_url_w_base, urldataitem["base"], sys.argv[2], sys.argv[3])
        
        except Exception as e:
            print(e)
            print("error") 


