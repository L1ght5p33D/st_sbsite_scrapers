import json
import time
import datetime
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from elasticsearch import Elasticsearch, exceptions, TransportError
import binascii
from os import urandom
import requests
import urllib3

import sys


def buildParseItemData():
    urlFile = 'tbs_item_urls'
    urlList = []

    with open(urlFile) as urlF:
        urlList = urlF.readlines()
    urlF.close()

    urlIndex = 0
    for produrl in urlList:
        urlIndex += 1

        sanurl = None
        try:
            sanurl = produrl.replace("\\", "")
            gsel.get(sanurl)
        except:
            print("url invalid")
            continue

        time.sleep(3)

        print("produrl resp")

        tbs = gsel.page_source

        buildItemObj = {}



        prodimgsplit = ""
        if "woocommerce-product-gallery__image" in tbs:
            prodimgsplit = tbs.split("woocommerce-product-gallery__image")[1].split("href=\"")[1].split("\"")[0]
            print("got prod image ~ " + prodimgsplit)

        buildItemObj["imageUrl"] = prodimgsplit

        if "<h1 class=\"product_title entry-title\">" in tbs:
            ts1 = tbs.split("<h1 class=\"product_title entry-title\">")[1].split("</h1>")[0]
            print("title split")
            print(ts1)
            buildItemObj['title'] = ts1

            xcount = 0
            numcount = 0
            for char in ts1:
                if char == "x" or char == "X":
                    xcount += 1
                if char.isdigit() == True:
                    numcount += 1

            print(xcount)
            print(numcount)

            if xcount >= 2 and numcount >= 5:
                print("found dimension candidate")
                xs1 = ts1.lower().split("x")

                sliceSrcMap = {}
                sliceNumListMap = {}

                numsInSliceList = []

                # look for / or . to determine fraction or decimal
                specCharMap = {}

                slicecount = 0
                for xslice in xs1:

                    sliceSrcMap[slicecount] = xslice
                    sliceNumListMap[slicecount] = []
                    specCharMap[slicecount] = []

                    xsnumcount = 0
                    xscutoffcount = 0
                    for char in xslice:
                        if xscutoffcount > 14 and slicecount != 0:
                            # print("distance cuttoff reached")
                            break
                        xscutoffcount += 1
                        if char.isdigit():
                            xsnumcount += 1
                            sliceNumListMap[slicecount].append(char)
                        if char == "/":
                            print("found slash")
                            specCharMap[slicecount].append("/")
                        if char == ".":
                            print("found dot")
                            specCharMap[slicecount].append(".")

                    slicecount += 1

                    numsInSliceList.append(xsnumcount)

                print("slicenumlistmap")
                print(sliceNumListMap)
                print("numsInSliceList")
                print(numsInSliceList)
                print("spec chars map lists")
                print(specCharMap)
                print("slice source map xslice ::: ")
                print(sliceSrcMap)

                if len(numsInSliceList) > 3:
                    print("dont know which slice has dims still")
                elif len(numsInSliceList) == 3 and len(sliceNumListMap) == 3:
                    print("got dims pretty sure")

                    lengthFeet = None
                    lengthInches = None
                    widthInches = None
                    widthFrac = None
                    thickInches = None
                    thickFrac = None

                    volume = None

                    groupnum = 0
                    for sliceIndex, numList in sliceNumListMap.items():
                        groupnum += 1

                        if groupnum == 1:
                            print("groupnum 1 length")
                            print(len(numList))
                            if len(numList) == 4:
                                lengthFeet = str(numList[0]) + str(numList[1])
                                lengthInches = str(numList[2]) + str(numList[4])

                            if len(numList) == 3:
                                print("len 3 length")
                                if "'" in sliceSrcMap[sliceIndex]:
                                    print("got foot indicator")
                                    split_feet = sliceSrcMap[sliceIndex].split("'")
                                    feetnumlist = []
                                    inchesnumlist = []
                                    for char in split_feet[0]:
                                        if char.isdigit():
                                            feetnumlist.append(char)
                                    for char in split_feet[1]:
                                        if char.isdigit():
                                            inchesnumlist.append(char)
                                    print("analyze ln lists")
                                    if len(feetnumlist) == 2:
                                        lengthFeet = str(feetnumlist[0]) + str(feetnumlist[1])
                                        lengthInches = inchesnumlist[0]
                                    elif len(feetnumlist) == 1:
                                        lengthFeet = feetnumlist[0]
                                        lengthInches = str(inchesnumlist[0]) + str(inchesnumlist[1])

                                else:
                                    lengthFeet = None

                            if len(numList) == 2:
                                if "'" in sliceSrcMap[sliceIndex]:
                                    split_feet = sliceSrcMap[sliceIndex].split("'")
                                    feetnumlist = []
                                    inchesnumlist = []
                                    for char in split_feet[0]:
                                        if char.isdigit():
                                            feetnumlist.append(char)
                                    for char in split_feet[1]:
                                        if char.isdigit():
                                            inchesnumlist.append(char)
                                    if len(feetnumlist) == 1:
                                        lengthFeet = feetnumlist[0]
                                        lengthInches = inchesnumlist[0]
                                    elif len(feetnumlist) == 2:
                                        lengthFeet = str(feetnumlist[0]) + str(feetnumlist[1])
                                        lengthInches = 0

                                else:
                                    lengthFeet = None
                            if len(numList) == 1:
                                lengthFeet = numList[0]
                                lengthInches = 0

                            print("got length feet/inches vals")
                            # print(lengthFeet)
                            # print(lengthInches)

                        if groupnum == 2:
                            print("group2 width")
                            print(len(numList))

                            widthInches = str(numList[0]) + str(numList[1])
                            if len(numList) == 6:

                                if "." in specCharMap[sliceIndex]:
                                    print("found decimal width")
                                if "/" in specCharMap[sliceIndex]:
                                    print("found frac width")

                                    # preSlashNumsList = []
                                    # postSlashNumsList = []

                                    # widthFracNumsSlashSplit = sliceSrcMap[sliceIndex].split("/")

                                    # for char in widthFracNumsSlashSplit[0]:
                                    #     if char.isdigit():
                                    #         preSlashNumsList.append(char)

                                    # for char in widthFracNumsSlashSplit[1]:
                                    #     if char.isdigit():
                                    #         postSlashNumsList.append(char)

                                    widthFrac = str(numList[2]) + str(numList[3]) + "/" + str(numList[4]) + str(
                                        numList[5])

                            if len(numList) == 5:
                                if "." in specCharMap[sliceIndex]:
                                    print("found decimal width")

                                if "/" in specCharMap[sliceIndex]:
                                    print("found frac width")

                                    widthFrac = str(numList[2]) + "/" + str(numList[3]) + str(numList[4])

                            if len(numList) == 4:
                                if "." in specCharMap[sliceIndex]:
                                    print("found decimal width")
                                    widthFrac = "decimal :::: " + str(numList[2]) + str(numList[3])

                                if "/" in specCharMap[sliceIndex]:
                                    print("found frac width")

                                    widthFrac = str(numList[2]) + "/" + str(numList[3])

                            if len(numList) == 3:
                                if "." in specCharMap[sliceIndex]:
                                    # print("found decimal width")
                                    # split_dec = sliceSrcMap[sliceIndex].split(".")[1]
                                    # print("parsing split dec ::: ")
                                    # print(split_dec)

                                    # fracNumList = []
                                    # limit = 0
                                    # for char in split_dec:
                                    #     if limit > 5:
                                    #         break
                                    #     if char.isdigit():
                                    #         fracNumList.append(char)
                                    #     limit+=1
                                    # widthFrac = "decimal ::: " + str(fracNumList[0]) + str(fracNumList[1]
                                    widthFrac = "decimal ::: " + str(numList[2])

                            if len(numList) == 2:
                                widthFrac = 0
                                # if "." in specCharMap[sliceIndex]:
                                # print("found decimal width")
                                # split_dec = sliceSrcMap[sliceIndex].split(".")[1]
                                # fracNumList = []
                                # limit = 0
                                # for char in split_dec:
                                #     if limit > 5:
                                #         break
                                #     if char.isdigit():
                                #         fracNumList.append(char)
                                #     limit+=1
                                # widthFrac = "decimal ::: " + str(fracNumList[0]) + str(fracNumList[1])
                                # else:
                                #     widthFrac = str(numList[0]) + str(numList[1])

                        if groupnum == 3:
                            print("group 3 thickness")
                            thickInches = numList[0]

                            preSlashNumsList = []
                            postSlashNumsList = []

                            if "L" in sliceSrcMap[sliceIndex] or "l" in sliceSrcMap[sliceIndex]:
                                print("got liter slice")
                                if "(" in sliceSrcMap[sliceIndex]:
                                    split_parenth = sliceSrcMap[sliceIndex].split("(")[1].split(")")[0]
                                    volNumList = []
                                    for char in split_parenth:
                                        if char.isdigit():
                                            volNumList.append(char)
                                    if len(volNumList) == 3:
                                        volume = str(volNumList[0]) + str(volNumList[1]) + "." + str(volNumList[2])
                                    if len(volNumList) == 4:
                                        volume = str(volNumList[0]) + str(volNumList[1]) + "." + str(
                                            volNumList[2]) + str(volNumList[3])
                                elif "(" not in sliceSrcMap[sliceIndex]:
                                    if "/" in sliceSrcMap[sliceIndex]:
                                        print("split thick slash")
                                        split_slash = sliceSrcMap[sliceIndex].split("/")

                                        preSlashNums = []
                                        for char in split_slash[0]:
                                            if char.isdigit():
                                                preSlashNums.append(char)
                                        if len(preSlashNums) == 3:
                                            thickFrac = str(numList[1]) + str(numList[2]) + "/" + str(numList[3]) + str(
                                                numList[4])
                                        if len(preSlashNums) == 2:
                                            if " " in split_slash[1]:
                                                split_postSlash = split_slash[1].split(" ")[0]
                                                psNumList = []
                                                for char in split_postSlash:
                                                    if char.isdigit():
                                                        psNumList.append(char)
                                                if len(psNumList) == 1:
                                                    thickFrac = numList[1] + "/" + numList[2]
                                                if len(psNumList) == 2:
                                                    thickFrac = numList[1] + "/" + str(numList[2]) + str(numList[3])

                            if "/" in specCharMap[sliceIndex]:
                                print("slash thickness")
                                thickFracNumsSlashSplit = sliceSrcMap[sliceIndex].split("/")

                                preSlashNumsList = []
                                postSlashNumsList = []

                                for char in thickFracNumsSlashSplit[0]:
                                    if char.isdigit():
                                        preSlashNumsList.append(char)

                                for char in thickFracNumsSlashSplit[1].split(" ")[0]:
                                    if char.isdigit():
                                        postSlashNumsList.append(char)
                                if len(preSlashNumsList) == 2:
                                    if len(postSlashNumsList) == 2:
                                        thickFrac = preSlashNumsList[1] + "/" + str(postSlashNumsList[0]) + str(
                                            postSlashNumsList[1])
                                    if len(postSlashNumsList) == 1:
                                        thickFrac = preSlashNumsList[1] + "/" + str(postSlashNumsList[0])
                                if len(preSlashNumsList) == 3:
                                    if len(postSlashNumsList) == 2:
                                        thickFrac = str(preSlashNumsList[1]) + \
                                                    str(preSlashNumsList[1]) + \
                                                    "/" + str(postSlashNumsList[0]) + str(postSlashNumsList[1])

                                # if len(numList) == 5:
                                #     thickFrac = str(numList[1]) + str(numList[2]) + "/" + str(numList[3]) + str(numList[4])
                                # if len(numList) == 4:
                                #     thickFrac = str(numList[1]) + "/" + str(numList[2]) + str(numList[3])
                                # if len(numList) == 3:
                                #     thickFrac = str(numList[1]) + "/" + str(numList[2])

                            if "." in specCharMap[sliceIndex]:

                                print("thickness decimal")
                                split_dec = sliceSrcMap[sliceIndex].split(".")
                                split_postDec = split_dec[1].split(" ")[0]
                                preDecNumList = []
                                postDecNumList = []
                                for char in split_dec[0]:
                                    if char.isdigit():
                                        preDecNumList.append(char)
                                for char in split_postDec:
                                    if char.isdigit():
                                        postDecNumList.append(char)

                                if len(preDecNumList) < 2:
                                    thickInches = preDecNumList[0]
                                    if len(postDecNumList) == 1:
                                        thickFrac = "Decimal ::: " + str(postDecNumList[0])
                                    if len(postDecNumList) == 2:
                                        thickFrac = "Decimal ::: " + str(postDecNumList[0]) + str(postDecNumList[1])
                                if len(split_dec) > 2:
                                    print("possible volume decimal")

                                    split_postDec = split_dec[2].split(" ")[0]
                                    preDecNumList = []
                                    postDecNumList = []
                                    for char in split_dec[1]:
                                        if char.isdigit():
                                            preDecNumList.append(char)
                                    for char in split_postDec:
                                        if char.isdigit():
                                            postDecNumList.append(char)

                                    if len(preDecNumList) == 2:
                                        if len(postDecNumList) == 1:
                                            volume = str(preDecNumList[0]) + str(preDecNumList[1]) + "." + str(
                                                postDecNumList[0])
                                        if len(postDecNumList) == 2:
                                            volume = str(preDecNumList[0]) + str(preDecNumList[1]) + "." + str(
                                                postDecNumList[0]) + str(postDecNumList[1])

                            # if len(numList) == 3:
                            #     thickFrac = "Decimal ::: " + str(numList[1]) + str(numList[2])
                            #
                            # if len(numList) == 2:
                            #     thickFrac = "Decimal ::: " + str(numList[1])


                    buildItemObj["widthInches"] = widthInches
                    buildItemObj["widthFrac"] = widthFrac
                    buildItemObj["lengthFeet"] = lengthFeet
                    buildItemObj["lengthInches"] = lengthInches
                    buildItemObj["thicknessInches"] = thickInches
                    buildItemObj["thicknessFrac"] = thickFrac
                    buildItemObj["volume"] = volume

                    print("BUILD OBJ :::::::: ")
                    print(buildItemObj)

                with open("tbs_scrape_data", "a+") as file:
                    file.write(json.dumps(buildItemObj) + "\n")




if __name__ == '__main__':
    buildParseItemData()