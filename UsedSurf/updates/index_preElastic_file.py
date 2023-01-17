import json
from elasticsearch import Elasticsearch, exceptions, TransportError

import sys

_1337ElasticInstance = Elasticsearch()


'''
 Positional Arguments ::: 
 1) index name 
2) File name / relative path
'''
if __name__ == '__main__':

    saveStrObjs = []

    file_name = sys.argv[2]

    with open(file_name, "r+") as objF:
        saveStrObjs = objF.readlines()

    objIndx = 0
    for sObj in saveStrObjs:
        objIndx+=1
        print("sobj ::: " + str(objIndx))
        print(str(sObj))

        lObj = json.loads(sObj.replace("\n",""))
        print("load obj ::: " + str(lObj))

        lCopy = lObj
        for k,v in lObj.items():
            if v == "":
                lCopy[k] = " "
            
            if k == "price":
                lCopy[k] = str(v)


        _1337ElasticInstance.index(index=sys.argv[1], doc_type="_doc",
                               body=lCopy, id=lObj["itemUUID"])