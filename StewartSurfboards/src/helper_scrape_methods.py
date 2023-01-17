# filepath will come in from elastic doc to user, and when requesting delete back to this method
def delete_items_by_deleteFile(filepath):
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

    global _3TradeElasticInstance
    addObjList = []
    with open(filepath) as taf:
        addObjList = taf.readlines()


    for addobj in addObjList:
        decobj = json.loads(addobj.replace("\n",""))
        print("loaded add obj :::  ")
        print(decobj)
        if sys.argv[2] == "Index":
            _3TradeElasticInstance.index(index=sys.argv[0], doc_type="_doc",body=decobj)
       


###########################################################################################################################

###########################################################################################################################


def countTotalBracketsInJson(sdata):
    openBrackets = 0
    closeBrackets = 0

    for char in sdata:
        if char == "{":
            openBrackets+=1
        if char == "}":
            closeBrackets +=1
        if openBrackets == closeBrackets and openBrackets != 0:
            break

    total = openBrackets, closeBrackets
    return total


def parseJsonToCloseBracket(sdata):
    itemJson = ""
    openB, closeB = countTotalBracketsInJson(sdata)

    for char in sdata:
        itemJson +=char
        if char == "{":
            openB -=1
        if char == "}":
            closeB -=1
        if closeB == 0:
            break

    print("parsed json ::: ")
    print(itemJson)

    return itemJson

def removeCharsToOpenBracket(sd):
    trimString = sd
    for char in sd:
        if char != "{":
            trimString = trimString[1:]
        else:
            break
    return trimString