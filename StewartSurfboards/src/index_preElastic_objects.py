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



def add_items_by_addFile(filepath):
    print("add file item")
    global _3TradeElasticInstance
    addObjList = []
    with open(filepath) as taf:
        addObjList = taf.readlines()


    for addobj in addObjList:
        decobj = json.loads(addobj.replace("\n",""))
        print("loaded add obj :::  ")
        print(decobj)
        _3TradeElasticInstance.index(index=sys.argv[1], doc_type="_doc",body=decobj, id=decobj["itemUUID"])


if __name__ == "__main__":
    print("Indexing pre elastic objects ... ")
    _3TradeElasticInstance = Elasticsearch()

    addFilePath = "../data/" + sys.argv[2]

    add_items_by_addFile(addFilePath)