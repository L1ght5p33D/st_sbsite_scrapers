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



def add_items_by_addFile():
    print("add file item")
    global _3TradeElasticInstance
    addObjList = []
    with open( "../data/preElastic_objects" ) as taf:
        addObjList = taf.readlines()


    for addobj in addObjList:
        decobj = json.loads(addobj.replace("\n",""))
        print("loaded add obj :::  ")
        print(decobj)
        _3TradeElasticInstance.index(index=sys.argv[1], doc_type="_doc",body=decobj, id=decobj["itemUUID"])



def delete_item_by_url():
    print("start delete items by delfile")

    with open( "../data/toDelete_urls", "r" ) as delurlf:
        for durl in delurlf.readlines():
            di_search = _3TradeElasticInstance.search( index = sys.argv[1],
              body={"query":{"match_phrase":{"itemLink":durl}}})

            if di_search["hits"]["total"]["value"] > 0:

                print("found delete hits")
                docId = di_search["hits"]["hits"][0]["_id"]
                try:
                    print("Deleting url item")
                    _3TradeElasticInstance.delete(index=sys.argv[1],id=docId)
                except Exception as err:
                    print("Could not delete item. possibly not found in index")


    print("delete item done")


if __name__ == "__main__":
    print("Indexing pre elastic objects ... ")
    _3TradeElasticInstance = Elasticsearch()

    add_items_by_addFile()

    delete_items_by_url()
