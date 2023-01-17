import json
from elasticsearch import Elasticsearch, exceptions, TransportError


_1337ElasticInstance = Elasticsearch()



if __name__ == '__main__':

    saveStrObjs = []

    with open("../updates/toAdd.txt", "r+") as objF:
        saveStrObjs = objF.readlines()

    objIndx = 0
    for sObj in saveStrObjs:
        objIndx+=1
        print("sobj ::: " + str(objIndx))
        print(str(sObj))

        lObj = json.loads(sObj)
        # print("load obj ::: " + str(lObj))

        lCopy = lObj
        for k,v in lObj.items():
            if v == "":
                lCopy[k] = " "
            if  "0/1" in v and len(v) < 10:
                lCopy[k] = " "


        _1337ElasticInstance.index(index="st_items_k2t1", doc_type="_doc",
                               body=lCopy, id=lObj["itemUUID"])
