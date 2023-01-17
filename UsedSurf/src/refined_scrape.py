
import json
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from random import randint




def findItemUrl(psrc):
    print("init find url")


    cardNum = 1
    while cardNum <= 9:

        try:
            print("found iterated card figure ")
            s1 = psrc.split("<figure class=\"card-figure\">")[cardNum]
        except:
            print("probably out of cards")
            return

        s2 = ""
        if "href" in s1:
            s2 = s1.split("href")[1]


        if "http" in s2[:10]:

            s3 = s2.split("=")[1]

            s4 = s3.split(">")[0]
            print("found url ::: ")
            print(s4)
        else:
            cardNum += 1
            continue
        cardNum += 1

        with open("../data/scraped_Item_Urls.txt", 'a+') as f:
            f.write(s4 + "\n")

        f.close()

def scrapeProductsPage(scrapeUrl):

    global gsel
    time.sleep(1)
    gsel.get(scrapeUrl)
    phtml = gsel.page_source
    findItemUrl(phtml)
    

def contains_digit(s):
    return any(i.isdigit() for i in s)

def count_digits(s):
    dcount = 0
    for i in s:
        if i.isdigit():
            dcount +=1
    return dcount

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def buildUrlListsAndOutputItemUrls():
    print("bulaoiu called")
    newUrls = []
    usedUrls = []

    pi1 = 1
    while pi1 < 9:
        newUrls.append("https://usedsurf.com/new-surfboards/?sort=featured&page="+str(pi1))
        pi1+=1
    pi2 = 1
    while pi2 < 53:
        usedUrls.append("https://usedsurf.com/used-surfboards/?sort=featured&page="+str(pi2))
        pi2+=1

    for nUrl in newUrls:
        scrapeProductsPage(nUrl)
    for uUrl in usedUrls:
        scrapeProductsPage(uUrl)


def scrapeItemDataPage(item_source, itemUrl):
    # with open("item_html_src_example.txt", 'r') as html_source_file:
    #     html_source = html_source_file.read()
    html_source = item_source
    if "product-description" in html_source:

        if "product-description--top" in html_source:
            print("product description in source")
            pd2 = html_source.split("product-description--top")
            # pd2 = pd2[1].split("</section>")[0]


            boardDataObj = {
          "localImageUUIDList" : "[]",
          "userId" : "UsedSurfSC",
          "userUUID" : "YpuI4G0BU8g6NLDjRmxR",
          "title" : " ",
          "price" : " ",
          "brandShaper" : " ",
          "description" : " ",
                "itemLink": itemUrl,
          "latitude" : 33.4344735,
          "longitude" : -117.6241256,
          "dimensionMap" : """{"lengthFeet":" ","lengthInches":" ","widthInches":" ","widthFracNumer":" ","widthFracDenom":" ","widthFrac":" ","thicknessInches":" ","thicknessFracNumer":" ","thicknessFracDenom":" ","thicknessFrac":" ","volumeLiters":" "}""",
          "finBrand" : " ",
          "finSetup" : " ",
          "boardType" : " ",
          "condition" : 100.0,
          "keywords" : json.dumps(["UsedSurf", "Used", "Surf", "San Clemente"]),
          "timeStamp" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000"),
          "completePost" : "complete",
          "cityString" : "San Clemente",
          "itemUUID" : "",
          "profilePic" : False,
          "s3ImageTags" : [

          ],
          "stdLength" : 0,
          "stdWidth" : 0,
          "stdThick" : 0,
          "stdVol" : 0,
          "stdPrice" : 0
        }

            buildDims = {"lengthFeet":"0","lengthInches":"0","widthInches":"0","widthFracNumer":"0","widthFracDenom":"1","widthFrac":" 0","thicknessInches":"0","thicknessFracNumer":"0","thicknessFracDenom":"1","thicknessFrac":"0","volumeLiters":"1"}


            if "productView-title" in html_source:
                print("found productview title")
                pdb = html_source.split("productView-title")[1].split("name")[1].split(">")
                titleData = pdb[1].split("<")[0]
                boardDataObj["title"] = titleData
                print("title data " + titleData)

                boarduid = "usedsurf_" + str(random_with_N_digits(10))
                if "#" in titleData:
                    boardNum = titleData.split("#")[1].split("<")[0]
                    print("board num ::: " + str(boardNum))

                    if len(boardNum) > 4 and len(boardNum) < 10:
                        boarduid = "usedsurf_" + boardNum

                boardDataObj["itemUUID"] = boarduid



            if "Brand:" in pd2[1]:
                pdb = pd2[1].split("Brand:")
                brandData = pdb[1].split("<")[0]
                boardDataObj["brandShaper"] = brandData
                print("brand data " + brandData)

            # if "Model:" in pd2[1]:
            #     pdb = pd2[1].split("Model:")
            #     modelData = pdb[1].split("<")[0]
            #     boardDataObj["title"] = modelData
            #     print("brand data " + modelData)
            #     sModelD = modelData.replace(" ", "")
            #     if sModelD == "N/A":


            lengthFeet_get = "0"
            lengthInches_get = "0"


            if "Length:" in pd2[1]:
                print("length block")
                pdb = pd2[1].split("Length")
                lengthData = pdb[1].split("<")[0]


                lengthDigits = []
                for char in lengthData:
                    if char.isdigit():
                        lengthDigits.append(char)
                for d in lengthDigits:
                    print("length digit:" +str(d))

                if "." in lengthData:
                    buildDims["lengthFeet"] = str(0)
                    buildDims["lengthInches"] = str(0)

                elif len(lengthDigits) > 4:

                    buildDims["lengthFeet"] = str(0)
                    buildDims["lengthInches"] = str(0)

                elif "'" in lengthData:
                    if "/" in lengthData:
                        ldi = str(0)
                    else:
                        print("length digits <=3 and single quote")
                        ldf = lengthData.split("'")[0]
                        lengthFeet_get = ldf
                        lengthInches_get = lengthData.split("'")[1].split(" ")[0].replace("\"", "")



                if lengthFeet_get != "0":
                    buildDims["lengthFeet"] = lengthFeet_get.replace(":","").replace(" ", "")
                else:
                    buildDims["lengthFeet"] = "0"
                if lengthInches_get !="0":
                    buildDims["lengthInches"] = lengthInches_get.replace(" ","")
                else:
                    buildDims["lengthInches"] = "0"


            if "Width:" in pd2[1]:
                pdb = pd2[1].split("Width")
                widthData = pdb[1].split("<")[0]
                if "thick" in widthData.lower():
                    widthData = widthData.lower().split("thick")[0]


                ###########################################################################
                ###########################################################################
                # New width test
                parsedWidthInches = 0
                parsedWidthFracNumer = 0
                parsedWidthFracDenom = 0

            
                # widthSplit = scrapeObj["description"].split("Width")[1]
                # ws1 = widthSplit.split("<")[0]

                print("INIT NEW WIDTH CALC")
                ws1 = widthData
                widthDigitsCount = count_digits(ws1)



                wdDigits = []
                wInchesEndIndexCount = 0
                wInchesEndIndexFinal = 0

                wInchesCount = 0
                for char in ws1:
                    wInchesEndIndexCount +=1
                    if char.isdigit():
                        wInchesCount +=1
                        if wInchesCount ==2:
                            wInchesEndIndexFinal = wInchesEndIndexCount
                            wInchesCount +=1
                        wdDigits.append(char)

   

                if len(wdDigits) >=2:
                    parsedWidthInches = " "
                    parsedWidthFracNumer = " "
                    parsedWidthFracDenom = " "

                    parsedWidthInches = str(wdDigits[0]) + str(wdDigits[1])
                    

                    dimmap = {"widthInches": parsedWidthInches,
                    }


                    print("WIDTH DATA OUT")
                    print(widthData)

                    print("inches end final :: " + str(wInchesEndIndexFinal))


                    print("width data no inches :: ")

                    widthFracData = widthData[wInchesEndIndexFinal:]
                    print(widthFracData)

                    if "/" in widthFracData:
                        dimmap['widthFracNumer'] = widthFracData.split("/")[0]
                        dimmap['widthFracDenom'] = widthFracData.split("/")[1]
                    if "." in widthData:
                        print("found decimal width data")
                        nl_noInches = []
                        for char in widthFracData:
                            if char.isdigit():
                                nl_noInches.append(char)
                        
                        fracstr = ""
                        for n in nl_noInches:
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

                    print("SECOND NEW WIDTH CALC ::: ")
                    print(str(dimmap))


                    buildDims["widthInches"] = dimmap["widthInches"]
                    if "widthFracNumer" in dimmap:
                        buildDims["widthFracNumer"] = dimmap["widthFracNumer"].replace('"',"").replace("'","")
                    if "widthFracDenom" in dimmap:
                        buildDims["widthFracDenom"] = dimmap["widthFracDenom"].replace('"',"").replace("'","")




            if "Thickness:" in pd2[1]:
                pdb = pd2[1].split("Thickness")
                ThicknessData = pdb[1][1:12]

                print("thick data " + str(ThicknessData))

                ThicknessNumList = []
                for char in ThicknessData:
                    if char.isdigit():
                        ThicknessNumList.append(char)

                print("thickness num list :: ")
                print(str(ThicknessNumList))

                dimmap = {}

                if len(ThicknessNumList) >= 1:

                    print("INITIAL THICKNESS INCHES :: ")
                    print(ThicknessNumList[0])
        

                    buildDims["thicknessInches"] = str(ThicknessNumList[0])
                    dimmap = {"thicknessInches" : str(ThicknessNumList[0])}

                    dimmap["thicknessFrac"] = " "
                    
                    thick_str_data = ""

                    tsd_idx = 0
                    for tsd in ThicknessData.split(str(ThicknessNumList[0])):
                        if tsd_idx == 0:
                            continue
                        else:
                            thick_str_data = thick_str_data + tsd


                

                    if "/" in thick_str_data:
                        dimmap['thicknessFracNumer'] = thick_str_data.split("/")[0]
                        dimmap['thicknessFracDenom'] = thick_str_data.split("/")[1]
                    if "." in thick_str_data:
                        nl = []
                        for char in thick_str_data:
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
                        else:
                            print("calculating frac")

                            
                            if len(nl) >= 2 and  len(nl) <=3 :
                                print("Found length two thick frac decimal")
                                if float(str(nl[0]) + str(nl[1])) > 0 and float(str(nl[0]) + str(nl[1])) < 7:
                                    dimmap["thicknessFrac"] = "1/16"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 7 and float(str(nl[0]) + str(nl[1])) < 13:
                                    dimmap["thicknessFrac"] = "1/8"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "8"
                                if float(str(nl[0]) + str(nl[1])) >= 13 and float(str(nl[0]) + str(nl[1])) < 19:
                                    dimmap["thicknessFrac"] = "3/16"
                                    dimmap["thicknessFracNumer"] = "3"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 19 and float(str(nl[0]) + str(nl[1])) < 25:
                                    dimmap["thicknessFrac"] = "1/4"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "4"
                                if float(str(nl[0]) + str(nl[1])) >= 25 and float(str(nl[0]) + str(nl[1])) < 31:
                                    dimmap["thicknessFrac"] = "5/16"
                                    dimmap["thicknessFracNumer"] = "5"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 31 and float(str(nl[0]) + str(nl[1])) < 37:
                                    dimmap["thicknessFrac"] = "3/8"
                                    dimmap["thicknessFracNumer"] = "3"
                                    dimmap["thicknessFracDenom"] = "8"
                                if float(str(nl[0]) + str(nl[1])) >= 37 and float(str(nl[0]) + str(nl[1])) < 43:
                                    dimmap["thicknessFrac"] = "3/8"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "2"
                                if float(str(nl[0]) + str(nl[1])) >= 43 and float(str(nl[0]) + str(nl[1])) < 49:
                                    dimmap["thicknessFrac"] = "1/2"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "2"
                                if float(str(nl[0]) + str(nl[1])) >= 49 and float(str(nl[0]) + str(nl[1])) < 55:
                                    dimmap["thicknessFrac"] = "1/2"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "2"
                                if float(str(nl[0]) + str(nl[1])) >= 55 and float(str(nl[0]) + str(nl[1])) < 61:
                                    dimmap["thicknessFrac"] = "9/16"
                                    dimmap["thicknessFracNumer"] = "9"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 61 and float(str(nl[0]) + str(nl[1])) < 67:
                                    dimmap["thicknessFrac"] = "10/16"
                                    dimmap["thicknessFracNumer"] = "10"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 67 and float(str(nl[0]) + str(nl[1])) < 73:
                                    dimmap["thicknessFrac"] = "11/16"
                                    dimmap["thicknessFracNumer"] = "11"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 73 and float(str(nl[0]) + str(nl[1])) < 79:
                                    dimmap["thicknessFrac"] = "3/4"
                                    dimmap["thicknessFracNumer"] = "3"
                                    dimmap["thicknessFracDenom"] = "4"
                                if float(str(nl[0]) + str(nl[1])) >= 79 and float(str(nl[0]) + str(nl[1])) < 85:
                                    dimmap["thicknessFrac"] = "13/16"
                                    dimmap["thicknessFracNumer"] = "13"
                                    dimmap["thicknessFracDenom"] = "16"
                                if float(str(nl[0]) + str(nl[1])) >= 85 and float(str(nl[0]) + str(nl[1])) < 91:
                                    dimmap["thicknessFrac"] = "7/8"
                                    dimmap["thicknessFracNumer"] = "7"
                                    dimmap["thicknessFracDenom"] = "8"
                                if float(str(nl[0]) + str(nl[1])) >= 91 and float(str(nl[0]) + str(nl[1])) < 100:
                                    dimmap["thicknessFrac"] = "15/16"
                                    dimmap["thicknessFracNumer"] = "15"
                                    dimmap["thicknessFracDenom"] = "16"
                            if len(nl) == 1 :
                                print("found length one thick frac decimal")
                                if int(nl[0]) == 1:
                                    dimmap["thicknessFrac"] = "1/8"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "8"
                                if int(nl[0]) == 2:
                                    dimmap["thicknessFrac"] = "3/16"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "4"
                                if int(nl[0]) == 3:
                                    dimmap["thicknessFrac"] = "5/16"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "4"

                                if int(nl[0]) == 4:
                                    dimmap["thicknessFrac"] = "3/8"
                                    dimmap["thicknessFracNumer"] = "3"
                                    dimmap["thicknessFracDenom"] = "8"

                                if int(nl[0]) == 5:
                                    dimmap["thicknessFrac"] = "1/2"
                                    dimmap["thicknessFracNumer"] = "1"
                                    dimmap["thicknessFracDenom"] = "2"

                                if int(nl[0]) == 6:
                                    dimmap["thicknessFrac"] = "9/16"
                                    dimmap["thicknessFracNumer"] = "9"
                                    dimmap["thicknessFracDenom"] = "16"

                                if int(nl[0]) == 7:
                                    dimmap["thicknessFrac"] = "11/16"
                                    dimmap["thicknessFracNumer"] = "7"
                                    dimmap["thicknessFracDenom"] = "8"


                                if int(nl[0]) == 8:
                                    dimmap["thicknessFrac"] = "13/16"
                                    dimmap["thicknessFracNumer"] = "11"
                                    dimmap["thicknessFracDenom"] = "16"

                                if int(nl[0]) == 9:
                                    dimmap["thicknessFrac"] = "15/16"
                                    dimmap["thicknessFracNumer"] = "7"
                                    dimmap["thicknessFracDenom"] = "8"



                    print("NEW THICKNESS DATA OUT")
                    print(str(dimmap))

                    
                    
                    if "thicknessFracDenom" in dimmap:
                        dimmap["thicknessFracDenom"] = dimmap["thicknessFracDenom"].replace('"',"").replace("'","")
                        try:
                            fnumtest = float(dimmap["thicknessFracDenom"])
                            buildDims["thicknessFracDenom"] = dimmap["thicknessFracDenom"]
                        except:
                            print("couldnt parse thickness denominator")
                            buildDims["thicknessFracDenom"] = 1
                    
                    if "thicknessFracNumer" in dimmap:
                        dimmap["thicknessFracNumer"] = dimmap["thicknessFracNumer"].replace('"',"").replace("'","")
                        try:
                            fnumtest = float(dimmap["thicknessFracNumer"])
                            buildDims["thicknessFracNumer"] = dimmap["thicknessFracNumer"]
                        except:
                            print("couldnt parse thickness numerator")
                            buildDims["thicknessFracNumer"] = 0
                            buildDims["thicknessFracDenom"] = 1
                        
                        

            volume_get = 0
            if "Volume:" in pd2[1]:
                print("found volume sub")
                pdb = pd2[1].split("Volume:")
                VolumeData = pdb[1].split("<")[0]
                print("volume data :: " + str(VolumeData))

                VolNumList = []
                for char in VolumeData:
                    if char.isdigit():
                        VolNumList.append(char)
                print("vol list")
                print(VolNumList)
                if len(VolNumList) >= 2 and len(VolNumList) <=4:
                    if len(VolNumList) == 2:
                        volume_get = str(VolNumList[0]) + str(VolNumList[1])
                    if len(VolNumList) == 3:
                        volume_get = str(VolNumList[0]) + str(VolNumList[1]) + "." +str(VolNumList[2])
                    if len(VolNumList) == 4:
                        volume_get = str(VolNumList[0]) + str(VolNumList[1]) + "." +str(VolNumList[2]) + str(VolNumList[3])

                buildDims["volumeLiters"] = volume_get

                print("Volume data " + VolumeData)


            if "Fins:" in pd2[1]:
                pdb = pd2[1].split("Fins:")
                finsData = pdb[1].split("<")[0]
                print("fins data " + finsData)

                finType = " "
                finSetup = " "

                if "fcs" in finsData.lower():
                    finType = "FCS"

                if "future" in finsData.lower():
                    finType = "Future"

                finStringRegionGet = finsData.lower()

                if "fcs2" in finStringRegionGet:
                    finType = "FCS2"
                if "glass" in finStringRegionGet:
                    finType = "Glass"
                if "quad" in finStringRegionGet:
                    finSetup = "Quad"
                if "five" in finStringRegionGet or "5" in finStringRegionGet:
                    finSetup = "Five"
                if "tri" in finStringRegionGet or "thruster" in finStringRegionGet:
                    finSetup = "Thruster"
                if "single" in finStringRegionGet:
                    finSetup = "Single"
                if "center" in finStringRegionGet and "side" in finStringRegionGet:
                    finSetup = "2+1"

                print("fins type" + finType)
                print("fins setup:" + finSetup)

                boardDataObj["finBrand"] = finType
                boardDataObj["finSetup"] = finSetup



            if "price--withoutTax" in html_source:
                pdp = html_source.split("price--withoutTax")
                pd1 = pdp[1].split(">")
                if "</" in pd1[1]:
                    pd2 = pd1[1].split("</")[0]
                    print("price data " + pd2)
                    pdSan = pd2.replace("$","").replace(".","")
                    print("pd san ::: " + str(pdSan))

                    try:
                        float(pdSan)
                        if float(pdSan) > 10000:
                            boardDataObj["price"] = str(float(pdSan) / 100)
                        else:
                            boardDataObj["price"] = str(float(pdSan))
                    except:
                        print("no parse price")
                        boardDataObj["price"] = "0"




            if "fish" in boardDataObj["description"].lower() or "fish" in boardDataObj["title"].lower():
                boardDataObj["boardType"] = "Fish"

            if "presentation" in html_source:
                print("found pres in html src")
                psplit = html_source.split("presentation")
                pPossible = []
                for presArea in psplit:
                    if "src" in presArea[0:10]:
                        print("found src in presArea")
                        pPossible.append(presArea)
                if len(pPossible) == 1:
                    pSrc = pPossible[0].split("src")[1]
                    pData = pSrc.split("\"")
                    pImg = pData[1]
                    print("found img::" + pImg)
                    boardDataObj["s3ImageTags"] = [pImg]
                else:
                    for pos in pPossible:
                        if "src" in pos:
                            print("second if pos found")



            buildDims["widthFrac"] = str(buildDims["widthFracNumer"]) + "/" + str(buildDims["widthFracDenom"])
            buildDims["thicknessFrac"] = str(buildDims["thicknessFracNumer"]) + "/" + str(buildDims["thicknessFracDenom"])


            

     
            '''
                Final cleanup
            '''

            if "0/1" in buildDims["thicknessFrac"]:
                print("found malformed zero thickness dim")
                buildDims["thicknessFrac"] = " "



            boardDataObj["dimensionMap"] = json.dumps(buildDims)

            '''
            Convert dims to STD values for searching
            '''


            stdLength = 0.0

            lengthNumFeet=0
            lengthNumInches=0


            try :
                lnf = lengthFeet_get.replace(":", "")
                lengthNumFeet = int(lnf.replace(" ", ""))
                lengthNumInches = int(lengthInches_get.replace(" ", ""))

            except:
                print("std length not able to pe parsed")



            try:
                stdWidth = int(json.loads(boardDataObj["dimensionMap"])["widthInches"]) + int(json.loads(boardDataObj["dimensionMap"])["widthFracNumer"]) / int(json.loads(boardDataObj["dimensionMap"])["widthFracDenom"])
            except:
                stdWidth = 0
            try:
                stdThick = int(json.loads(boardDataObj["dimensionMap"])["thicknessInches"]) + int(json.loads(boardDataObj["dimensionMap"])["thicknessFracNumer"]) / int(json.loads(boardDataObj["dimensionMap"])["thicknessFracDenom"])
            except:
                stdThick = 0

            if "new" in itemLinkUrl:
                boardDataObj["condition"] = 100.0
            elif "used" in itemLinkUrl:
                boardDataObj["condition"] = 80.0
            else:
                boardDataObj["condition"] = 120.0

            if json.loads(boardDataObj["dimensionMap"])["lengthFeet"] != " ":
                try:
                    print("loading length map fields")
                    length_feet_num = int(json.loads(boardDataObj["dimensionMap"])["lengthFeet"])
                    print("lenght feet num " + str(length_feet_num))
                    length_inches_num = int(json.loads(boardDataObj["dimensionMap"])["lengthInches"])
                    print("length inches num " + str(length_inches_num))
                    if length_feet_num <20:
                        print("less 20 feet")
                        print("length_feet_num" + str(length_feet_num))
                        print("length_inches_num" + str(length_inches_num))
                        linot = int(length_inches_num)/12
                        print("lnot ::: "  )
                        print(str(linot))

                        stdLength = float(length_feet_num + (float(float(length_inches_num)/12)))
                        print("std length calc ::: ")
                        print(str(stdLength))
                    else:
                        stdLength = 0

                except:
                    print("could not parse numerical lengths")
                    stdLengh = 0

            boardDataObj["stdLength"] = stdLength
            boardDataObj["stdWidth"] = stdWidth
            boardDataObj["stdThick"] = stdThick
            boardDataObj["stdVol"] = float(json.loads(boardDataObj["dimensionMap"])["volumeLiters"])
            boardDataObj["stdPrice"] = float(boardDataObj["price"])

            for f,v in boardDataObj.items():
                if v == "":
                    boardDataObj[f] = " "


            print("board obj:")
            print(str(boardDataObj) + "\n")

            with open("../data/used_surf_parsed_objects.txt", 'a+') as objF:
                objF.write(json.dumps(boardDataObj) + "\n")



if __name__ == '__main__':
    print("Init main used surf scrape")
    gsel = webdriver.PhantomJS()

    # Dont run when testing already have url file
    # buildUrlListsAndOutputItemUrls()

    urls = []

    with open("../data/scraped_Item_Urls.txt") as urlF:
        urls = urlF.readlines()

    urlidx = 0
    for itemUrl in urls:
        if urlidx < len(urls):
            print("scrape url number ~ " + str(urlidx) + " ::: " + urls[urlidx])
            sanUrl = urls[urlidx].replace("\"", "")
            gsel.get(sanUrl)
            psrc = gsel.page_source

            itemLinkUrl = sanUrl.replace("\n", "")
            scrapeItemDataPage(psrc, itemLinkUrl)
            # with open("item_html_src_example.txt", 'a+') as htmlsrc:
            #     htmlsrc.write(psrc)
        urlidx +=1



    gsel.close()