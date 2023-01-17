import scrapy
import json
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from random import randint



def delete_items_by_deleteFile(filepath):

	print("delete file item")
    global _3TradeElasticInstance
    deleteObjList = []
    with open(filepath) as tdf:
        deleteObjList = tdf.readlines()


    for dobj in deleteObjList:
        decobj = json.loads(dobj)
        for k,v in decobj.items():
            print("found k v for delete")
            delete_doc_id = k
            # _3TradeElasticInstance.delete(index=sys.argv[0], id = delete_doc_id)

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
        if sys.argv[0] == "Index":
            _3TradeElasticInstance.index(index=sys.argv[1], doc_type="_doc",body=decobj)



if __name__ == "__main__":
    print("init diff index by add and delete file")
    _3TradeElasticInstance = Elasticsearch()

    deleteFilePath = "../data/toDelete.txt"
    addFilePath = "../data/toAdd.txt"

    delete_items_by_deleteFile(deleteFilePath)
    add_items_by_addFile(addFilePath)