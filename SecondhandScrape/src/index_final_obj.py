import json
import time
import datetime
import os

from elasticsearch import Elasticsearch, exceptions, TransportError
_1337ElasticInstance = Elasticsearch()


index_name = "st_items_k2t2m1"
if __name__ == '__main__':

    fp_items = []
    with open('final_parsed_items.txt','r') as fpi:
        print("Index from to Add")
        fp_items = fpi.readlines()


    

    for item in fp_items:
        print("indexing item :::  ")
        print(item)
        
        item = json.loads(item)

        # _1337ElasticInstance.delete_by_query(index=index_name,
        #     body={"query":{"match":{"userId":"SecondhandBoards"}}})
        
        print("all items deleted")

        _1337ElasticInstance.index(index=index_name,
                                 body=item, id=item["itemUUID"]  )

        print("index complete")
