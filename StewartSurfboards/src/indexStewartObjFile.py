
import json
from elasticsearch import Elasticsearch, exceptions, TransportError
from pprint import pprint
import math
import sys


_1337ElasticInstance = Elasticsearch()

print("main obj parse")
objFile = '../data/preElasticObjects.txt'

objs = []

with open(objFile) as objF:
    objs = objF.readlines()
objF.close()

# idx = 0
for scrapeObjString in objs:
    # if idx == 0:
    print("str data:::")
    pprint("pprint str ::: ")
    pprint(scrapeObjString)
    scrapeObjString.strip()
    pprint("pprint obj strip ::: ")
    pprint(scrapeObjString)
    scrapeObj = json.loads(scrapeObjString)



    print("json loaded scrape obj ")
    pprint("pprint obj ::: ")
    pprint(scrapeObjString)
    print(scrapeObj["title"])
    print(scrapeObj["itemUUID"])

    sanDesc = scrapeObj["description"]
    sanDesc = sanDesc.replace("\\n", "")
    sanDesc = sanDesc.replace("\n", "")
    sanDesc = sanDesc.replace("\u2019", "'")
    sanDesc = sanDesc.replace("\\u2019", "'")
    sanDesc = sanDesc.replace("\u201d", '"')
    sanDesc = sanDesc.replace("\\u201d", '"')
    scrapeObj["description"] = sanDesc
    print(scrapeObj["description"])
    # print(scrapeObj[])


    _1337ElasticInstance.index(
        index= sys.argv[1],
        # index="st_items_k2t1",
        doc_type="_doc",
        body=scrapeObj,
        id=scrapeObj["itemUUID"]
                                   )

    # print(scrapeObj["description"])
    # print(scrapeObj["price"])
    # print(scrapeObj["tags"])
    # print(scrapeObj["images"])
    # # print(scrapeObj["featuredImage"])
    #
    # for tag in scrapeObj["tags"]:
    #     print("tagn")
    #     print(tag)
    # for im in scrapeObj["images"]:
    #     print("imn")
    #     print(im)
    # idx += 1

    # {
    #     "stdLength": 5.8333,
    #     "boardType": "Shortboard",
    #     "localImageUUIDList": """["8394a794-911f-457b-9797-412fdd120d7f"]""",
    #     "keywords": """["Firewire"]""",
    #     "latitude": 33.401167318256014,
    #     "description": "The Mini Driver started with the original Driver. The initial adjustments incorporated a fast, low nose rocker with a forward placed outline, both of which added drive. After adding a rounded tail for control, but with additional width at 12\" up from the tail, the Mini Driver emerged. The clean and elliptical outline moved freely on the face and inside the tube. The MD can be surfed in a variety of wave sizes, it excels in waist to head high + range.",
    #     "title": " 5'10 FIREWIRE MINI DRIVER SURFBOARD",
    #     "finBrand": "Future",
    #     "cityString": "San Clemente",
    #     "stdThick": 2.38,
    #     "price": " 549.00",
    #     "userUUID": "k3PremkBzMAFBItzdH0s",
    #     "stdPrice": 549.0,
    #     "longitude": -117.59550930943115,
    #     "itemUUID": "6a621c48-bee3-4ccb-96e3-a6b208e6c641",
    #     "profilePic": true,
    #     "s3ImageTags": [
    #         "https://storage.googleapis.com/surftrade_user_images/8394a794-911f-457b-9797-412fdd120d7f.jpg"
    #     ],
    #     "userId": "initUserDefault",
    #     "finSetup": "Five",
    #     "brandShaper": "Firewire",
    #     "timeStamp": "2019-04-05 22:51:23.858990",
    #     "condition": 100.0,
    #     "completePost": "complete",
    #     "dimensionMap": """{"lengthFeet":" 5","lengthInches":" 10","widthInches":" 19","widthFracNumer":"1","widthFracDenom":"4","widthFrac":"1/4\"","thicknessInches":" 2","thicknessFracNumer":"3","thicknessFracDenom":"8","thicknessFrac":"3/8\"","volumeLiters":" 27.8"}""",
    #     "stdWidth": 19.25,
    #     "stdVol": 27.8
    # }