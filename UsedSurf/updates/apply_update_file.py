import sys
import json
from elasticsearch import Elasticsearch, exceptions, TransportError


_1337ElasticInstance = Elasticsearch()

# Arguments ::
    #  1) Index name
    #  2)  file1, file2,  ...  

if __name__ == '__main__':

    saveStrObjs = []
    removeStrObjs = []


    update_files = sys.argv[2:]

    if len(update_files) < 1:
        print("No file names arguments found exiting")
        sys.exit()

    for file_name in update_files:
        print("adding files from argfile ::: " + str(file_name))
        if "Add" in file_name:
            with open(file_name,) as objF:
                print("open obj file")
                enc_objs = objF.readlines()
                print("read obj file complete")
                dec_objs = []
                for enc in enc_objs:
                    try:
                        dec_item = enc.encode("utf-8")
                        dec_objs.append(dec_item)
                    except:
                        print("couldnt decode item")
                        dec_objs = enc_objs
                saveStrObjs.extend(dec_objs)
        if "Delete" in file_name:
            with open(file_name, "r+") as objF:
                removeStrObjs.extend(objF.readlines())

    objIndx = 0
    for sObj in saveStrObjs:
        objIndx+=1
        print("indexing item number ::: " + str(objIndx))
        # print(str(sObj))
        try:
            print("pre json load object")
            lObj = None
            try:
                # lObj = json.loads(sObj.replace("\n", ""))
                lObj = json.loads(sObj)
            except:
                print("could not json load sObj")
                lObj = sObj
            print("json loaded obj ::: ")
            print(lObj)

            try:
                print(lObj["userId"])
            except:
                print("could not access obj key")

            try:
                for k,v in lObj.items():
                    print("got keys :: ")
                    print(k)
                    if v == "":
                        print("found null string")
                        lObj[k] = " "
                    if isinstance(v,str) and "0/1" in v and len(v) < 10:
                        print("found malformated dim")
                        lObj[k] = " "
            except:
                print("couldnt parse object")

            _1337ElasticInstance.index(index=sys.argv[1], doc_type="_doc",
                                   body=lObj, id=lObj["itemUUID"])
        except Exception as e:
            print(e)
            print("couldnt index item ... passing")

    objIndx = 0
    for dObj in removeStrObjs:
        objIndx += 1
        print("deleting item number ::: " + str(objIndx))
        print(str(dObj))
        try:
            lObj = {}
            try:
                lObj = json.loads(dObj)
            except:
                print("could not load json object")
                lObj = dObj

            itemid = ""
            try:
                itemid = lObj["itemUUID"]
                _1337ElasticInstance.delete(index=sys.argv[1], id=lObj["itemUUID"])
            except Exception as e:
                print(e)
                print("could not delete item by uuid")


        except Exception as e:
            print(e)
            print("couldnt delete item ... passing")

