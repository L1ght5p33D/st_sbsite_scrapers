import json
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from elasticsearch import Elasticsearch, exceptions, TransportError
import sys




def delete_items_by_delFile():
    DELETE_FILE_NAME = "/toDelete_urls"

    diff_url_data = []

    df_urls = []
    with open(sys.argv[2] + DELETE_FILE_NAME) as df:
        df_urls = df.readlines()


    for durl in df_urls:
        print("Deleting url:::" + str(durl))
        _3TradeElasticInstance.delete_by_query(index= sys.argv[1],body= \
            {"query":{"match_phrase": {"itemLink":durl}}})
        print("Done")



def add_items_by_addFile():
    print("add file item")
    global _3TradeElasticInstance
    addObjList = []
    
    with open(sys.argv[2] + "/preElastic_items") as taf:
        addObjList = taf.readlines()


    for addobj in addObjList:
        decobj = json.loads(addobj.replace("\n",""))
        print("loaded add obj :::  ")
        print(decobj)

        utime = datetime.datetime.strptime(decobj["timeStamp"],"%Y-%m-%d %H:%M:%S.%f")
        tm = int(utime.timestamp() * 1000)
        decobj["uploadTime"] = tm

        _3TradeElasticInstance.index(index=sys.argv[1], doc_type="_doc",body=decobj, id=decobj["itemUUID"])


if __name__ == "__main__":
    print("Indexing pre elastic objects ... ")
    _3TradeElasticInstance = Elasticsearch()

    
    delete_items_by_delFile()
    add_items_by_addFile()
