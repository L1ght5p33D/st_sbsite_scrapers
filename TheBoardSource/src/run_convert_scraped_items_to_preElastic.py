import json
import time
import datetime
from os import urandom
import sys

def convert_scraped_objects_to_pre_elastic():
    parseDataObjFile = 'tbs_scrape_data'
    parseDataObjList = []

    with open(parseDataObjFile) as urlF:
        parseDataObjList = urlF.readlines()
    urlF.close()

    itemIndex = 0
    for item in parseDataObjList:
        item = item.replace("\\n", "")

        print("pre json load item ::: ")
        print(item)
        print("loading item")
        item = json.loads(item)

        print("LOADED ITEM")
        print(item)

        urllink = "theboardsource.com"
        if "urlLink" in item:
            urllink = item["urlLink"]

        desc = " "
        if "description" in item:
            desc = item["description"]

        imageUrl = None
        if "imageUrl" in item:
            imageUrl = item["imageUrl"]

        dimmap ={"lengthInches": 0,
             "lengthFeet": 0,
             "widthInches": 0,
             "widthFracNumer": 0,
             "widthFracDenom": 1,
             "widthFrac": " ",
             "thicknessInches": 0,
             "thicknessFracNumer": 0,
             "thicknessFracDenom": 1,
             "thicknessFrac": " ",
             "volumeLiters": 0
             }

        if 'lengthFeet' in item:
            print('found length dim')
            dimmap['lengthFeet'] = item['lengthFeet']
            dimmap['lengthInches'] = item['lengthInches']
            dimmap['widthInches'] = item['widthInches']
            dimmap['thicknessInches'] = item['thicknessInches']
        else:
            print("no dims")


        try:
            if item["widthFrac"] == 0:
                dimmap["widthFrac"] = " "
            else:
                if "/" in item["widthFrac"]:
                    dimmap['widthFracNumer'] = item['widthFrac'].split("/")[0]
                    dimmap['widthFracDenom'] = item['widthFrac'].split("/")[1]
                if "decimal" in item["widthFrac"] or "Decimal" in item["widthFrac"]:
                    nl = []
                    for char in item["widthFrac"]:
                        if char.isdigit():
                            nl.append(char)
                    fracstr = ""
                    for n in nl:
                        fracstr += str(n)
                    if fracstr == "44":
                        dimmap["widthFrac"] = "7/16"
                        dimmap["widthFracNumer"] = "7"
                        dimmap["widthFracDenom"] = "16"
                    if fracstr == "25":
                        dimmap["widthFrac"] = "1/4"
                        dimmap["widthFracNumer"] = "1"
                        dimmap["widthFracDenom"] = "4"
                    if fracstr == "3":
                        dimmap["widthFrac"] = "1/3"
                        dimmap["widthFracNumer"] = "1"
                        dimmap["widthFracDenom"] = "3"
                    if fracstr == "6":
                        dimmap["widthFrac"] = "2/3"
                        dimmap["widthFracNumer"] = "2"
                        dimmap["widthFracDenom"] = "3"
                    if fracstr == "72":
                        dimmap["widthFrac"] = "1/2"
                        dimmap["widthFracNumer"] = "1"
                        dimmap["widthFracDenom"] = "2"
                    if fracstr == "5":
                        dimmap["widthFrac"] = "1/2"
                        dimmap["widthFracNumer"] = "1"
                        dimmap["widthFracDenom"] = "2"
                    if fracstr == "75":
                        dimmap["widthFrac"] = "3/4"
                        dimmap["widthFracNumer"] = "3"
                        dimmap["widthFracDenom"] = "4"
                    if fracstr == "72":
                        dimmap["widthFrac"] = "11/16"
                        dimmap["widthFracNumer"] = "11"
                        dimmap["widthFracDenom"] = "16"
                    if fracstr == "70":
                        dimmap["widthFrac"] = "11/16"
                        dimmap["widthFracNumer"] = "11"
                        dimmap["widthFracDenom"] = "16"
                    if fracstr == "8":
                        dimmap["widthFrac"] = "13/16"
                        dimmap["widthFracNumer"] = "13"
                        dimmap["widthFracDenom"] = "16"
                    if fracstr == "87":
                        dimmap["widthFrac"] = "7/8"
                        dimmap["widthFracNumer"] = "7"
                        dimmap["widthFracDenom"] = "8"
        except Exception as e:
            print("width is int")
            dimmap["widthFrac"] = " "




        try:
            if item["thicknessFrac"] == 0:
                dimmap["thicknessFrac"] = " "
            else:

                if "/" in item["thicknessFrac"]:
                    dimmap['thicknessFracNumer'] = item['thicknessFrac'].split("/")[0]
                    dimmap['thicknessFracDenom'] = item['thicknessFrac'].split("/")[1]
                if "decimal" in item["thicknessFrac"] or "Decimal" in item["thicknessFrac"]:
                    nl = []
                    for char in item["thicknessFrac"]:
                        if char.isdigit():
                            nl.append(char)
                    fracstr = ""
                    for n in nl:
                        fracstr += str(n)
                    if fracstr == "44":
                        dimmap["thicknessFrac"] = "7/16"
                        dimmap["thicknessFracNumer"] = "7"
                        dimmap["thicknessFracDenom"] = "16"
                    if fracstr == "25":
                        dimmap["thicknessFrac"] = "1/4"
                        dimmap["thicknessFracNumer"] = "1"
                        dimmap["thicknessFracDenom"] = "4"
                    if fracstr == "3":
                        dimmap["thicknessFrac"] = "1/3"
                        dimmap["thicknessFracNumer"] = "1"
                        dimmap["thicknessFracDenom"] = "3"
                    if fracstr == "6":
                        dimmap["thicknessFrac"] = "2/3"
                        dimmap["thicknessFracNumer"] = "2"
                        dimmap["thicknessFracDenom"] = "3"
                    if fracstr == "72":
                        dimmap["thicknessFrac"] = "1/2"
                        dimmap["thicknessFracNumer"] = "1"
                        dimmap["thicknessFracDenom"] = "2"
                    if fracstr == "5":
                        dimmap["thicknessFrac"] = "1/2"
                        dimmap["thicknessFracNumer"] = "1"
                        dimmap["thicknessFracDenom"] = "2"
                    if fracstr == "75":
                        dimmap["thicknessFrac"] = "3/4"
                        dimmap["thicknessFracNumer"] = "3"
                        dimmap["thicknessFracDenom"] = "4"
                    if fracstr == "72":
                        dimmap["thicknessFrac"] = "11/16"
                        dimmap["thicknessFracNumer"] = "11"
                        dimmap["thicknessFracDenom"] = "16"
                    if fracstr == "70":
                        dimmap["thicknessFrac"] = "11/16"
                        dimmap["thicknessFracNumer"] = "11"
                        dimmap["thicknessFracDenom"] = "16"
                    if fracstr == "8":
                        dimmap["thicknessFrac"] = "13/16"
                        dimmap["thicknessFracNumer"] = "13"
                        dimmap["thicknessFracDenom"] = "16"
                    if fracstr == "87":
                        dimmap["thicknessFrac"] = "7/8"
                        dimmap["thicknessFracNumer"] = "7"
                        dimmap["thicknessFracDenom"] = "8"

        except Exception as e:
            print("width is int")
            dimmap["thicknessFrac"] = " "


        stdLength = 0
        stdThick = 0

        stdWidth = 0
        stdVol = 0

        stdPrice = float(item['price'])
        priceString = str(stdPrice)

        try:
            stdLength = (int(dimmap['lengthFeet']) * 12 )+ int(dimmap['lengthInches'])
        except Exception as e:
            print(e)
            print("error parsing std length")

        try:
            stdWidth = int(dimmap['widthInches']) + ( int(dimmap['widthFracNumer']) / int(dimmap['widthFracDenom']))
        except Exception as e:
            print(e)
            print("error parsing std width")

        try:
            stdThick = int(dimmap['thicknessInches']) + ( int(dimmap['thicknessFracNumer']) / int(dimmap['thicknessFracDenom']))
        except Exception as e:
            print(e)
            print("error parsing std thicknes")

        try:
            stdVol = float(dimmap["volumeLiters"])
        except Exception as e:
            print("error parsing vlum")
            print(e)



        eItem = {
            "stdLength": stdLength,
            "stdThick": stdThick,
            "stdPrice": stdPrice,
            "stdWidth": stdWidth,
            "stdVol": stdVol,
            "cdnImageList": [
                imageUrl
                # "//cdn.shopify.com/s/files/1/2146/1003/products/tip_p-114849.jpg?v=1570654183"
            ],
            "boardType": " ",
            "localImageUUIDList": [],
            "keywords": """["TheBoardSource"]""",
            "itemLink": urllink,
            "latitude": 33.1219673,
            "longitude": -117.355826,
            "description": desc,
            "title": item['title'],
            "finBrand": " ",
            "cityString": "Carlsbad",

            "price": priceString,
            "userUUID": "hv39t2wBJveYsvw3HjX",

            "itemUUID": generateUID(),
            "profilePic": False,
            "s3ImageTags": [
                imageUrl
                # "http://cdn.shopify.com/s/files/1/2146/1003/products/tip_p-114849.jpg?v=1570654183"
            ],
            "userId": "TheBoardSource",
            "sellerClass": "commercial",
            "finSetup": " ",
            "brandShaper": " ",
            "timeStamp": "2020-01-01 01:25:30.046",
            "condition": 120.0,
            "completePost": "complete",
            "dimensionMap": json.dumps(dimmap),

        }



        print("FINAL ::: ")
        print(eItem)

        if eItem["stdLength"] == 0:
            continue

        with open("built_tbs_preElastic_items", "a+") as file:
            file.write(json.dumps(eItem) + "\n")


if __name__ == '__main__':
    convert_scraped_objects_to_pre_elastic()