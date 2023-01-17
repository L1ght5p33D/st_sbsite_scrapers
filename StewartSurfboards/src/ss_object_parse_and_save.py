import json
import time
import datetime


import os

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import sys
sys.path.append("..")

from elasticsearch import Elasticsearch, exceptions, TransportError
_1337ElasticInstance = Elasticsearch()

def contains_digit(s):
    return any(i.isdigit() for i in s)

def count_digits(s):
    dcount = 0
    for i in s:
        if i.isdigit():
            dcount +=1
    return dcount


if __name__ == '__main__':
    print("main obj parse")
    objFile = '../data/finalStewartJsonData.txt'

    objs = []

    sObj = {}

    with open(objFile) as objF:
        objs = objF.readlines()
    objF.close()


    parsedLengthFeet = 0
    parsedLengthInches = 0

    itemLinkList = []
    with open("../data/stewartItemUrls.txt") as urlF:
        itemLinkList = urlF.readlines()


    itemIndex = 0
    for scrapeObjString in objs:
        if itemIndex<=999:
            try:
                scrapeObj = json.loads(scrapeObjString)
            except Exception as e:
                print("couldnt load json")
                continue

            tDimsMap = {}
            parsedLengthFeet = 0
            parsedLengthInches = 0

            lengthfeetlist = []
            lengthInchesList = []

            if "Length" in scrapeObj["description"]:
                print("found len in desc")

                lsb = scrapeObj["description"].split("Length")[1].split("<")[0]
                print("found lsb")
                print(lsb)
                lsp = ""

                lsf = 0
                if "'" in lsb:
                    print("found quote in lsb")
                    lsf = lsb.split("'")[0]
                    print("lsb zer")
                    print(lsf)

                    for char in lsf:
                        if char.isdigit():
                            print("digit")
                            lengthfeetlist.append(char)

                lfc = count_digits(lsf)

                if lfc == 2:
                    print("found twho lfc")
                    parsedLengthFeet = str(lengthfeetlist[0]) + str(lengthfeetlist[1])
                elif lfc == 1:
                    print("found one lfc")
                    print(lengthfeetlist)
                    parsedLengthFeet = str(lengthfeetlist[0])
                    print("lfl zero")
                    print(str(lengthfeetlist[0]))
                else:
                    print("NO LENGTH FEET")
                    parsedLengthFeet = "0"

                lsi = lsb.split("'")[1]

                for char in lsi:
                    if char.isdigit():
                        lengthInchesList.append(char)

                if len(lengthInchesList) ==2:
                    parsedLengthInches = str(lengthInchesList[0] ) + str(lengthInchesList[1])
                elif len(lengthInchesList) == 1:
                    parsedLengthInches = str(lengthInchesList[0])
                else:
                    parsedLengthInches = " "

                print("parsed length fields")
                print(parsedLengthFeet)
                print(parsedLengthInches)
                tDimsMap["lengthInches"] = parsedLengthInches
                tDimsMap["lengthFeet"] = parsedLengthFeet



            if "Width" in scrapeObj["description"]:

                widthSplit = scrapeObj["description"].split("Width")[1]
                ws1 = widthSplit.split("<")[0]
                widthDigitsCount = count_digits(ws1)

            wdDigits = []
            for char in ws1:
                if char.isdigit():
                    wdDigits.append(char)

            parsedWidthInches = " "
            parsedWidthFracNumer = " "
            parsedWidthFracDenom = " "

            parsedWidthInches = str(wdDigits[0])
            parsedWidthInches += str(wdDigits[1])

            if widthDigitsCount == 4:
                parsedWidthFracNumer = str(wdDigits[2])
                parsedWidthFracDenom = str(wdDigits[3])
            if widthDigitsCount == 5:
                parsedWidthFracNumer = str(wdDigits[2])
                parsedWidthFracDenom = str(wdDigits[3]) + str(wdDigits[4])
            if widthDigitsCount == 6:
                parsedWidthFracNumer = str(wdDigits[2])+str(wdDigits[3])
                parsedWidthFracDenom = str(wdDigits[4]) + str(wdDigits[5])
            else:
                parsedWidthFracNumer= 0
                parsedWidthFracDenom=1

            parsedThickInches = 0
            parsedThickFracNumer = 0
            parsedThickFracDenom = 0

            if "Thickness" in scrapeObj["description"]:

                thickSplit = scrapeObj["description"].split("Thickness")[1]
                ts1 = thickSplit.split("<")[0]
                thickDigitsCount = count_digits(ts1)

            tdDigits = []
            for char in ts1:
                if char.isdigit():
                    tdDigits.append(char)

            parsedThickInches = str(tdDigits[0])

            if thickDigitsCount == 3:
                parsedThickFracNumer = str(tdDigits[1])
                parsedThickFracDenom = str(tdDigits[2])
            if thickDigitsCount == 4:
                parsedThickFracNumer = str(tdDigits[1])
                parsedThickFracDenom = str(tdDigits[2]) + str(tdDigits[3])
            if thickDigitsCount == 5:
                parsedThickFracNumer = str(tdDigits[1])+str(tdDigits[2])
                parsedThickFracDenom = str(tdDigits[3]) + str(tdDigits[4])
            else:
                parsedThickFracNumer = 0
                parsedThickFracDenom = 1



            tDimsMap["lengthFeet"] = parsedLengthFeet
            tDimsMap["lengthInches"] = parsedLengthInches

            tDimsMap["widthInches"] = parsedWidthInches
            tDimsMap["widthFracNumer"] = parsedWidthFracNumer
            tDimsMap["widthFracDenom"] = parsedWidthFracDenom

            tDimsMap["widthFrac"] = str(parsedWidthFracNumer) + "/" + str(parsedWidthFracDenom)
            if parsedWidthFracNumer == 0:
                tDimsMap["widthFrac"] = " "



            tDimsMap["thicknessInches"] = parsedThickInches
            tDimsMap["thicknessFracNumer"] = parsedThickFracNumer
            tDimsMap["thicknessFracDenom"] = parsedThickFracDenom
            tDimsMap["thicknessFrac"] = str(parsedThickFracNumer) + "/" + str(parsedThickFracDenom)
            if parsedThickFracNumer == 0:
                tDimsMap["thicknessFrac"] = " "

            sObj["dimMap"] = tDimsMap


            price = "0"

            if "price" in scrapeObj:
                price = int(scrapeObj["price"])


            price = int(price/100)

            sObj["price"] = price

            imagesList = []

            if "featured_image" in scrapeObj:
                imagesList.append(scrapeObj["featured_image"])

            sObj["ims"] = imagesList

            finalObj = {}

            cLengthF = float(tDimsMap["lengthFeet"])
            cLengthI = float(tDimsMap["lengthInches"])

            sLength = cLengthF + (cLengthI/12)

            cWidth = float(tDimsMap["widthInches"])
            cWidthNumer = float(tDimsMap["widthFracNumer"])
            cWidthDenom = float(tDimsMap["widthFracDenom"])
            sWidth = cWidth + (cWidthNumer/cWidthDenom)

            cThick = float(tDimsMap["thicknessInches"])
            cThickNumer = float(tDimsMap["thicknessFracNumer"])
            cThickDenom = float(tDimsMap["thicknessFracDenom"])

            sThick = " "
            if (cThickNumer == 0.0):
                sThick = cThick
            else:
                sThick = cThick + (cThickNumer/cThickDenom)

            tDimsMap["volumeLiters"] = " "

            sanDesc = scrapeObj["description"].split("<")[0]

            # sanDesc = sanDesc.replace("\\n", " ")
            # sanDesc = sanDesc.replace("\n", " ")
            # sanDesc = sanDesc.replace("\u2019", "'")
            # sanDesc = sanDesc.replace("\\u2019", "'")
            # sanDesc = sanDesc.replace("\u201d", '"')
            # sanDesc = sanDesc.replace("\\u201d", '"')


            finalObj["description"] =  sanDesc

            urlSan = itemLinkList[itemIndex]
            if "?" in itemLinkList[itemIndex]:
                urlSan = urlSan.split("?")[0]

            urlSan = urlSan.replace("\"", "")
            urlSan = urlSan.replace("\\", "")
            urlSan = urlSan.replace("\n", "")
            finalObj["itemLink"] = "https://stewart-surfboards.myshopify.com" + urlSan

            finalObj["boardType"] = " "
            if "longboard" in sanDesc.lower():
                finalObj["boardType"] = "Longboard"


            finalObj["itemUUID"] = str(scrapeObj["id"])
            finalObj["dimensionMap"] = json.dumps(tDimsMap)


            stripImageUrl = imagesList[0]


            finalObj["localImageUUIDList"] = []
            finalObj["cdnImageList"] = [stripImageUrl]
            finalObj["s3ImageTags"] = ["http:" + stripImageUrl]
            finalObj["keywords"] = json.dumps(["Stewart"])
            finalObj["latitude"] =  33.415505
            finalObj["longitude"] = -117.603018
            finalObj["profilePic"] = False
            finalObj["condition"] = 100.0
            finalObj["completePost"] = "complete"
            finalObj["stdLength"] = sLength
            finalObj["stdWidth"] = sWidth
            finalObj["stdThick"] = sThick
            # finalObj["description"] = scrapeObj["description"].split("<")[0]
            finalObj["title"] = scrapeObj["title"]
            finalObj["finBrand"] =" "
            finalObj["finSetup"] = " "
            finalObj["brandShaper"] = "Stewart"
            finalObj["cityString"] = "San Clemente"
            finalObj["price"] = str(price)
            finalObj["stdPrice"] = float(price)
            finalObj["userUUID"] = "aI7km2wBJGeEsvw7DZMA"
            finalObj["userId"] = "StewartSurfboards"
            finalObj["stdVol"] =0
            finalObj["timeStamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000")


            finalObjEncoded = json.dumps(finalObj)
            

            print(finalObj)
            with open("../data/preElasticObjects.txt", "a+") as file:
                file.write(json.dumps(finalObj) + "\n")

            # _1337ElasticInstance.index(index="ttitems", doc_type="useritem",
            #                      body=finalObj, id=finalObj["itemUUID"]  )

            itemIndex +=1
