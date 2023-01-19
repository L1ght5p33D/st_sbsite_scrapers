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
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.setdefaultencoding('ascii')


# python src/run_gen_diff_urls.py st_items_k2t2m1 /home/si/os_projects/SurfTrader/1_serve_surftrader/SCRAPE/Surftrade_Scrapers/auto_scrape_scripts/TheBoardSource/data /home/si/os_projects/SurfTrader/1_serve_surftrader/SCRAPE/Surftrade_Scrapers/auto_scrape_scripts/chromedriver

_1337ElasticInstance = Elasticsearch()

def generateUID():
    return binascii.b2a_hex(urandom(18)).decode("utf-8")

chrome_options = Options()
chrome_options.add_argument("--headless")
gsel = webdriver.Chrome(sys.argv[3], options=chrome_options)


def get_item_urls_from_special_endpoint():
    page=0
    getPages = 1

    #later load more with element click
    #clickable = driver.findElement(By.class("botiga-pagination-button"));
    #clickable.click()

    while page < getPages:
        gsel.get("https://theboardsource.com/product-category/surfboards-collection/")

                # https://theboardsource.com/wp-json/wc/v2/products?per_page=16&category=12&page=1&order=desc&min_price=0&max_price=200000&consumer_key=ck_f8a9d0f0a65c24b5f4363fd396c218e87b205a0f&consumer_secret=cs_997bd4619188cd08ad0ad38a8b0273854092ed8d

	
        pageSource = gsel.page_source
        # split_perma = pageSource.split('permalink":"')
        # split_prod = pageSource.split('product type-product')
        # for bns in split_prod:
        print("get page src ~ " + pageSource)
        split_woo_link = pageSource.split('woocommerce-LoopProduct-link')[1]
        print("split_woo link:::")
        print(split_woo_link)
        if "href" in split_woo_link:
            split_link = split_woo_link.split("href=\"")[1].split("\"")[0]
            print("got split link ~ " + split_link)
            with open( sys.argv[2] +  '/tbs_item_urls', 'a+') as tbs_url_file:
                tbs_url_file.write(split_link + "\n")
        page +=1




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

                with open("built_tbs_scrape_data", "a+") as file:
                    file.write(json.dumps(buildItemObj) + "\n")

def convert_scraped_objects_to_pre_elastic():
    parseDataObjFile = 'built_tbs_scrape_data'
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

        with open("built_tbs_preElastic_items_2.txt", "a+") as file:
            file.write(json.dumps(eItem) + "\n")


def index_preElastic_objects():
    parseDataObjFile = 'tbs_items.txt'
    parseDataObjList = []

    with open(parseDataObjFile) as urlF:
        parseDataObjList = urlF.readlines()
    urlF.close()

    itemIndex = 0
    for item in parseDataObjList:
        item = item.replace("\\n", "")

        _1337ElasticInstance.index(index="st_items_k2t1", doc_type="_doc",body=
                               json.loads(item), id = json.loads(item)["itemUUID"]
                               )
        print("indexed item")
    print("index done")


if __name__ == '__main__':

    get_item_urls_from_special_endpoint()

    buildParseItemData()
    
    #index_preElastic_objects()
    
    # print("main init TBS parse item")
    #
    # soFile = 'built_tbs_scrape_data.txt'
    # soList = []
    #
    # with open(soFile) as soF:
    #     urlList = soF.readlines()
    # soF.close()
    #
    # soIndex = 0
    # for scrapeobj in soIndex:
    #     soIndex += 1

    # convert_scraped_objects_to_pre_elastic()


#     gsel.close()












