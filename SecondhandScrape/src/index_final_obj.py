import json
import time
import datetime
import os

from elasticsearch import Elasticsearch, exceptions, TransportError
_1337ElasticInstance = Elasticsearch()


if __name__ == '__main__':

    fp_items = []
    with open('final_parsed_items','r') as fpi:
        print("Index from to Add")
        fp_items = fpi.readlines()


    for item in fp_items:
        print("indexing item :::  ")
        print(item)
        
        item = json.loads(item)

        _1337ElasticInstance.index(index= sys.argv[1],
                                 body=item, id=item["itemUUID"]  )

        print("index complete")


    print("run delete routine")
    todelete_urls = []
    with open("toDelete_urls", "r") as tdf:
        todelete_urls = tdf.readlines()

    for td_url in todelete_urls:
        print("deleting url " + td_url)
        _1337ElasticInstance.delete_by_query(index=index_name,
                body={"query":{"match_phrase":{"itemLink":td_url}}})

    print("delete routine complete")
