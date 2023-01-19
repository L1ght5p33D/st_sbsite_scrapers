import json
import time
import datetime
import os
from elasticsearch import Elasticsearch, exceptions, TransportError
import sys

_1337ElasticInstance = Elasticsearch()

def index_preElastic_objects():
    parseDataObjFile = "/built_tbs_preElastic_items"
    parseDataObjList = []

    with open(sys.argv[2] + parseDataObjFile) as urlF:
        parseDataObjList = urlF.readlines()
    urlF.close()

    itemIndex = 0
    for item in parseDataObjList:
        item = item.replace("\\n", "")

        _1337ElasticInstance.index(index= sys.argv[1], doc_type="_doc",body=
                               json.loads(item), id = json.loads(item)["itemUUID"]
                               )
        print("indexed item")
    print("indexing complete")


if __name__ == '__main__':
    index_preElastic_objects()