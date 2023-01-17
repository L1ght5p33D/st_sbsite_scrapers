
import json
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from random import randint



# nl ::::  list of numbers for use to build fraction

gsel = webdriver.PhantomJS()

def build_thickness_frac(nl):

    thick_map = {
    # "thicknessInches": "0",
    "thicknessFracNumer":"0",
    "thicknessFracDenom":"1",
    "thicknessFrac": " "
    }
    if len(nl) >= 2 and  len(nl) <=3 :
        print("Found length two thick frac decimal")
        # if float(str(nl[0]) + str(nl[1])) / float(str(nl[2]) + str(nl[3])) > 0 and
        # float(str(nl[0]) + str(nl[1])) / float(str(nl[2]) + str(nl[3]))<  .07:
        if float(str(nl[0]) + str(nl[1])) >= 0 and float(str(nl[0]) + str(nl[1])) < 7:
            thick_map["thicknessFrac"] = "1/16"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 7 and float(str(nl[0]) + str(nl[1])) < 13:
            thick_map["thicknessFrac"] = "1/8"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "8"
        if float(str(nl[0]) + str(nl[1])) >= 13 and float(str(nl[0]) + str(nl[1])) < 19:
            thick_map["thicknessFrac"] = "3/16"
            thick_map["thicknessFracNumer"] = "3"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 19 and float(str(nl[0]) + str(nl[1])) <= 25:
            thick_map["thicknessFrac"] = "1/4"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "4"
        if float(str(nl[0]) + str(nl[1])) > 25 and float(str(nl[0]) + str(nl[1])) < 31:
            thick_map["thicknessFrac"] = "5/16"
            thick_map["thicknessFracNumer"] = "5"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 31 and float(str(nl[0]) + str(nl[1])) < 37:
            thick_map["thicknessFrac"] = "3/8"
            thick_map["thicknessFracNumer"] = "3"
            thick_map["thicknessFracDenom"] = "8"
        if float(str(nl[0]) + str(nl[1])) >= 37 and float(str(nl[0]) + str(nl[1])) < 43:
            thick_map["thicknessFrac"] = "3/8"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "2"
        if float(str(nl[0]) + str(nl[1])) >= 43 and float(str(nl[0]) + str(nl[1])) < 51:
            thick_map["thicknessFrac"] = "1/2"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "2"
        if float(str(nl[0]) + str(nl[1])) >= 51 and float(str(nl[0]) + str(nl[1])) < 55:
            thick_map["thicknessFrac"] = "1/2"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "2"
        if float(str(nl[0]) + str(nl[1])) >= 55 and float(str(nl[0]) + str(nl[1])) < 61:
            thick_map["thicknessFrac"] = "9/16"
            thick_map["thicknessFracNumer"] = "9"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 61 and float(str(nl[0]) + str(nl[1])) < 67:
            thick_map["thicknessFrac"] = "10/16"
            thick_map["thicknessFracNumer"] = "10"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 67 and float(str(nl[0]) + str(nl[1])) < 73:
            thick_map["thicknessFrac"] = "11/16"
            thick_map["thicknessFracNumer"] = "11"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 73 and float(str(nl[0]) + str(nl[1])) < 79:
            thick_map["thicknessFrac"] = "3/4"
            thick_map["thicknessFracNumer"] = "3"
            thick_map["thicknessFracDenom"] = "4"
        if float(str(nl[0]) + str(nl[1])) >= 79 and float(str(nl[0]) + str(nl[1])) < 85:
            thick_map["thicknessFrac"] = "13/16"
            thick_map["thicknessFracNumer"] = "13"
            thick_map["thicknessFracDenom"] = "16"
        if float(str(nl[0]) + str(nl[1])) >= 85 and float(str(nl[0]) + str(nl[1])) < 91:
            thick_map["thicknessFrac"] = "7/8"
            thick_map["thicknessFracNumer"] = "7"
            thick_map["thicknessFracDenom"] = "8"
        if float(str(nl[0]) + str(nl[1])) >= 91 and float(str(nl[0]) + str(nl[1])) < 100:
            thick_map["thicknessFrac"] = "15/16"
            thick_map["thicknessFracNumer"] = "15"
            thick_map["thicknessFracDenom"] = "16"

    if len(nl) == 1 :
        print("found length one thick frac decimal")
        if int(nl[0]) == 1:
            thick_map["thicknessFrac"] = "1/8"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "8"
        if int(nl[0]) == 2:
            thick_map["thicknessFrac"] = "3/16"
            thick_map["thicknessFracNumer"] = "3"
            thick_map["thicknessFracDenom"] = "16"
        if int(nl[0]) == 3:
            thick_map["thicknessFrac"] = "5/16"
            thick_map["thicknessFracNumer"] = "5"
            thick_map["thicknessFracDenom"] = "16"

        if int(nl[0]) == 4:
            thick_map["thicknessFrac"] = "3/8"
            thick_map["thicknessFracNumer"] = "3"
            thick_map["thicknessFracDenom"] = "8"

        if int(nl[0]) == 5:
            thick_map["thicknessFrac"] = "1/2"
            thick_map["thicknessFracNumer"] = "1"
            thick_map["thicknessFracDenom"] = "2"

        if int(nl[0]) == 6:
            thick_map["thicknessFrac"] = "9/16"
            thick_map["thicknessFracNumer"] = "9"
            thick_map["thicknessFracDenom"] = "16"

        if int(nl[0]) == 7:
            thick_map["thicknessFrac"] = "11/16"
            thick_map["thicknessFracNumer"] = "11"
            thick_map["thicknessFracDenom"] = "16"


        if int(nl[0]) == 8:
            thick_map["thicknessFrac"] = "13/16"
            thick_map["thicknessFracNumer"] = "13"
            thick_map["thicknessFracDenom"] = "16"

        if int(nl[0]) == 9:
            thick_map["thicknessFrac"] = "15/16"
            thick_map["thicknessFracNumer"] = "15"
            thick_map["thicknessFracDenom"] = "16"
    return thick_map


def find_diff_urls(psrc):
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

        with open("../data/diff_urls.txt", 'a+') as f:
            f.write(s4 + "\n")
        f.close()


def scrape_for_diff_urls(scrapeUrl):
    time.sleep(1)
    gsel.get(scrapeUrl)
    phtml = gsel.page_source
    find_diff_urls(phtml)
    
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
    print("buildUrlLists called")
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
        scrape_for_diff_urls(nUrl)
    for uUrl in usedUrls:
        scrape_for_diff_urls(uUrl)


def scrapeItemDataPage(item_source, itemUrl):
    html_source = item_source
    if "product-description" in html_source:

        if "product-description--top" in html_source:
            print("product description in source")
            pd2 = html_source.split("product-description--top")

            dtn =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            utime = datetime.datetime.strptime(dtn,"%Y-%m-%d %H:%M:%S")
            tm = int(utime.timestamp() * 1000)
            

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

          "timeStamp" : dtn,
          "uploadTime" : tm,

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

            lengthFeet = "0"
            lengthInches = "0"
            widthInches = "0"
            widthFracNumer = "0"
            widthFracDenom = "1"
            thicknessInches = "0"
            thicknessFracNumer = "0"
            thicknessFracDenom = "1"

            volume = "0"

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

            if "Length:" in pd2[1]:
                print("length block")
                pdb = pd2[1].split("Length")
                lengthData = pdb[1].split("<")[0]

                print("length data ::: ")
                print(str(lengthData))

                lengthDigits = []
                for char in lengthData:
                    if char.isdigit():
                        lengthDigits.append(char)

                for d in lengthDigits:
                    print("length digit:" +str(d))

                if "." in lengthData:
                    print("length data decimal")
                    buildDims["lengthFeet"] = str(0)
                    buildDims["lengthInches"] = str(0)

                elif len(lengthDigits) > 4:

                    buildDims["lengthFeet"] = str(0)
                    buildDims["lengthInches"] = str(0)

                if "'" in lengthData:
                    if "/" in lengthData:
                        print("single quiote and slash in length")
                        ldi = str(0)
                    else:
                        print("length digits <=3 and single quote")
                        if len(lengthDigits) == 4 and int(lengthDigits[0]) == 1:
                            ldf = str(lengthDigits[0]) + str(lengthDigits[1])
                            lengthFeet = ldf
                            lengthInches = str(lengthDigits[2]) + str(lengthDigits[3])
                        
                        if len(lengthDigits) == 3 and int(lengthDigits[0]) == 1:
                            ldf = str(lengthDigits[0]) + str(lengthDigits[1])
                            lengthFeet = ldf
                            lengthInches = str(lengthDigits[2]) 

                        if len(lengthDigits) == 3 and int(lengthDigits[0]) != 1:
                            ldf = str(lengthDigits[0]) 
                            lengthFeet = ldf
                            lengthInches = str(lengthDigits[1]) + str(lengthDigits[2])

                        if len(lengthDigits) == 2 and int(lengthDigits[0]) == 1:
                            ldf = str(lengthDigits[0]) + str(lengthDigits[1])
                            lengthFeet = ldf
                            lengthInches = 0
                        
                        if len(lengthDigits) == 2 and int(lengthDigits[0]) != 1:
                            ldf = str(lengthDigits[0])
                            lengthFeet = ldf
                            lengthInches = str(lengthDigits[1]) 

                        if len(lengthDigits) == 1 and int(lengthDigits[0]) != 1:
                            ldf = str(lengthDigits[0])
                            lengthFeet = ldf
                            lengthInches = 0



                if int(lengthFeet) != 0:
                    buildDims["lengthFeet"] = lengthFeet.replace(" ", "")
                else:
                    buildDims["lengthFeet"] = "0"
               
                if int(lengthInches) != 0:
                    buildDims["lengthInches"] = lengthInches.replace(" ","")
                else:
                    buildDims["lengthInches"] = "0"


            if "Width:" in pd2[1]:
                pdb = pd2[1].split("Width")
                widthData = pdb[1].split("<")[0]
                if "thick" in widthData.lower():
                    widthData = widthData.lower().split("thick")[0]

                parsedWidthInches = 0
                parsedWidthFracNumer = 0
                parsedWidthFracDenom = 0
            
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

                    widthFracData = widthData[wInchesEndIndexFinal:]
           
                    if "/" in widthFracData:
                        # dimmap['widthFracNumer'] = widthFracData.split("/")[0]
                        # dimmap['widthFracDenom'] = widthFracData.split("/")[1]
                        print("frac width data ::: ")
                        print(widthFracData)
                        try:
                            wss_split1 = widthFracData.split("/")[0]
                            print("wss split 1")
                            print(wss_split1)
                            dimmap['widthFracNumer'] = int(wss_split1[(len(wss_split1) - 2):])
                            print("dm wfn")
                            print(dimmap['widthFracNumer'])
                            print("dm wfd")

                            width_denom_num_list = []
                            width_denom_num_count = 0
                            for char in widthFracData.split("/")[1][0:2]:
                                if width_denom_num_count < 2:
                                    if char.isdigit():
                                        width_denom_num_list.append(char)
                                        width_denom_num_count += 1

                            if len(width_denom_num_list) == 1:
                                dimmap['widthFracDenom'] = int(str(width_denom_num_list[0]))
                            if len(width_denom_num_list) == 2:
                                dimmap['widthFracDenom'] = int(str(width_denom_num_list[0]) + str(width_denom_num_list[1]))
                            print(dimmap['widthFracDenom'])
                        except Exception as e:
                            print(e)
                            print("error parseing width to int")
                            dimmap["widthFracNumer"] = 0
                            dimmap["widthFracDenom"] = 1

                        buildDims["widthFracDenom"] = dimmap["widthFracDenom"]
                        buildDims["widthFracNumer"] = dimmap["widthFracNumer"]
                        buildDims["widthFrac"] = str(buildDims["widthFracNumer"]) + "/" + str(buildDims["widthFracDenom"])
                    if "." in widthData:
                        print("Decimal widht data")
                        nl_noInches = []
                        for char in widthFracData:
                            if char.isdigit():
                                nl_noInches.append(char)
                        frac_map = build_thickness_frac(nl_noInches)
                        buildDims["widthFracNumer"] = frac_map["thicknessFracNumer"]
                        buildDims["widthFracDenom"] = frac_map["thicknessFracDenom"]
                        buildDims["widthFrac"] = frac_map["thicknessFrac"]
                        # fracstr = ""
                        # for n in nl_noInches:
                        #     fracstr += str(n)
                        # if fracstr == "44":
                        #     dimmap["widthFrac"] = "7/16"
                        #     dimmap["widthFracNumer"] = "7"
                        #     dimmap["widthFracDenom"] = "16"
                        # if fracstr == "25":
                        #     dimmap["widthFrac"] = "1/4"
                        #     dimmap["widthFracNumer"] = "1"
                        #     dimmap["widthFracDenom"] = "4"
                        # if fracstr == "3":
                        #     dimmap["widthFrac"] = "1/3"
                        #     dimmap["widthFracNumer"] = "1"
                        #     dimmap["widthFracDenom"] = "3"
                        # if fracstr == "6":
                        #     dimmap["widthFrac"] = "2/3"
                        #     dimmap["widthFracNumer"] = "2"
                        #     dimmap["widthFracDenom"] = "3"
                        # if fracstr == "72":
                        #     dimmap["widthFrac"] = "1/2"
                        #     dimmap["widthFracNumer"] = "1"
                        #     dimmap["widthFracDenom"] = "2"
                        # if fracstr == "5":
                        #     dimmap["widthFrac"] = "1/2"
                        #     dimmap["widthFracNumer"] = "1"
                        #     dimmap["widthFracDenom"] = "2"
                        # if fracstr == "75":
                        #     dimmap["widthFrac"] = "3/4"
                        #     dimmap["widthFracNumer"] = "3"
                        #     dimmap["widthFracDenom"] = "4"
                        # if fracstr == "72":
                        #     dimmap["widthFrac"] = "11/16"
                        #     dimmap["widthFracNumer"] = "11"
                        #     dimmap["widthFracDenom"] = "16"
                        # if fracstr == "70":
                        #     dimmap["widthFrac"] = "11/16"
                        #     dimmap["widthFracNumer"] = "11"
                        #     dimmap["widthFracDenom"] = "16"
                        # if fracstr == "8":
                        #     dimmap["widthFrac"] = "13/16"
                        #     dimmap["widthFracNumer"] = "13"
                        #     dimmap["widthFracDenom"] = "16"
                        # if fracstr == "87":
                        #     dimmap["widthFrac"] = "7/8"
                        #     dimmap["widthFracNumer"] = "7"
                        #     dimmap["widthFracDenom"] = "8"

                    # print("SECOND NEW WIDTH CALC ::: ")
                    # print(str(dimmap))

                    buildDims["widthInches"] = dimmap["widthInches"]
                    if "widthFracNumer" in dimmap:
                        buildDims["widthFracNumer"] = dimmap["widthFracNumer"]
                    if "widthFracDenom" in dimmap:
                        buildDims["widthFracDenom"] = dimmap["widthFracDenom"]


            if "Thickness:" in pd2[1]:
                print("found thickness keyword")
                pdb = pd2[1].split("Thickness")
                ThicknessData = pdb[1].split("<")[0]

                print("thick data " + str(ThicknessData))


                ThicknessNumList = []
                for char in ThicknessData:
                    if char.isdigit():
                        ThicknessNumList.append(char)
                dimmap = {}

                if len(ThicknessNumList) >= 1:

                    print("INITIAL THICKNESS INCHES :: ")
                    print(ThicknessNumList[0])

                    tInchesEndIndexFinal = 0

                    tInchesSplit = ThicknessData.split(str(ThicknessNumList[0]))
                    tInchesSplit = [e+ThicknessNumList[0] for e in ThicknessData.split(ThicknessNumList[0]) if e]
                    tFracSegs = tInchesSplit[1:]

                    fracsegstr = ""
                    for seg in tFracSegs:
                        fracsegstr+=seg
                    print("found thickness split seg :: ")
                    print(fracsegstr)

                    dimmap = {}
                    dimmap = {"thicknessInches" : str(ThicknessNumList[0])}

                    if "/" in fracsegstr:
                        print("frac thickness")
                        try:
                            fss_split1 = fracsegstr.split("/")[0]
                            print("ffs split 1")
                            print(fss_split1)
                            dimmap['thicknessFracNumer'] = int(fss_split1[(len(fss_split1)-2):])
                            print("dm tfn")
                            print(dimmap['thicknessFracNumer'])
                            print("dm tfd")
                            dimmap['thicknessFracDenom'] = int(fracsegstr.split("/")[1][0:2].replace('"',"").replace("'","").replace(" ",""))
                            print(dimmap['thicknessFracDenom'])
                        except Exception as e:
                            print(e)
                            print("error parseing thickness to int")
                            dimmap["thicknessFracNumer"] = 0
                            dimmap["thicknessFracDenom"] = 1
                        buildDims["thicknessFracDenom"] = dimmap["thicknessFracDenom"]
                        buildDims["thicknessFracNumer"] = dimmap["thicknessFracNumer"]
                        buildDims["thicknessFrac"] = str(buildDims["thicknessFracNumer"]) + "/" + str(buildDims["thicknessFracDenom"])

                    if "." in fracsegstr:
                        print("decimal thickness")
                        nl = []
                        for char in fracsegstr:
                            if char.isdigit():
                                nl.append(char)
                        thick_frac_dims = build_thickness_frac(nl)
                        buildDims["thicknessFracNumer"] = thick_frac_dims["thicknessFracNumer"]
                        buildDims["thicknessFracDenom"] = thick_frac_dims["thicknessFracDenom"]
                        buildDims["thicknessFrac"] = str(buildDims["thicknessFracNumer"]) + "/" + str(buildDims["thicknessFracDenom"])
                        # fracstr = ""
                        # for n in nl:
                        #     fracstr += str(n)
                        # if fracstr == "44":
                        #     dimmap["thicknessFrac"] = "7/16"
                        #     dimmap["thicknessFracNumer"] = "7"
                        #     dimmap["thicknessFracDenom"] = "16"
                        # if fracstr == "25":
                        #     dimmap["thicknessFrac"] = "1/4"
                        #     dimmap["thicknessFracNumer"] = "1"
                        #     dimmap["thicknessFracDenom"] = "4"
                        # if fracstr == "3":
                        #     dimmap["thicknessFrac"] = "1/3"
                        #     dimmap["thicknessFracNumer"] = "1"
                        #     dimmap["thicknessFracDenom"] = "3"
                        # if fracstr == "6":
                        #     dimmap["thicknessFrac"] = "2/3"
                        #     dimmap["thicknessFracNumer"] = "2"
                        #     dimmap["thicknessFracDenom"] = "3"
                        # if fracstr == "72":
                        #     dimmap["thicknessFrac"] = "1/2"
                        #     dimmap["thicknessFracNumer"] = "1"
                        #     dimmap["thicknessFracDenom"] = "2"
                        # if fracstr == "5":
                        #     dimmap["thicknessFrac"] = "1/2"
                        #     dimmap["thicknessFracNumer"] = "1"
                        #     dimmap["thicknessFracDenom"] = "2"
                        # if fracstr == "75":
                        #     dimmap["thicknessFrac"] = "3/4"
                        #     dimmap["thicknessFracNumer"] = "3"
                        #     dimmap["thicknessFracDenom"] = "4"
                        # if fracstr == "72":
                        #     dimmap["thicknessFrac"] = "11/16"
                        #     dimmap["thicknessFracNumer"] = "11"
                        #     dimmap["thicknessFracDenom"] = "16"
                        # if fracstr == "70":
                        #     dimmap["thicknessFrac"] = "11/16"
                        #     dimmap["thicknessFracNumer"] = "11"
                        #     dimmap["thicknessFracDenom"] = "16"
                        # if fracstr == "8":
                        #     dimmap["thicknessFrac"] = "13/16"
                        #     dimmap["thicknessFracNumer"] = "13"
                        #     dimmap["thicknessFracDenom"] = "16"
                        # if fracstr == "87":
                        #     dimmap["thicknessFrac"] = "7/8"
                        #     dimmap["thicknessFracNumer"] = "7"
                        #     dimmap["thicknessFracDenom"] = "8"

                    # print("NEW THICKNESS DATA OUT")
                    # print(str(dimmap))



                    buildDims["thicknessInches"] = dimmap["thicknessInches"]
                    # if "thicknessFracDenom" in dimmap:
                    #     dimmap["thicknessFracDenom"] = dimmap["thicknessFracDenom"].replace('"',"").replace("'","")
                    #     try:
                    #         fnumtest = float(dimmap["thicknessFracDenom"])
                    #         buildDims["thicknessFracDenom"] = dimmap["thicknessFracDenom"]
                    #     except:
                    #         print("couldnt parse thickness denominator")
                    #         buildDims["thicknessFracDenom"] = 1
                    #
                    # if "thicknessFracNumer" in dimmap:
                    #     dimmap["thicknessFracNumer"] = dimmap["thicknessFracNumer"].replace('"',"").replace("'","")
                    #     try:
                    #         fnumtest = float(dimmap["thicknessFracNumer"])
                    #         buildDims["thicknessFracNumer"] = dimmap["thicknessFracNumer"]
                    #     except:
                    #         print("couldnt parse thickness numerator")
                    #         buildDims["thicknessFracNumer"] = 0
                    #         buildDims["thicknessFracDenom"] = 1
                        
            if "Volume:" in pd2[1]:
                # print("found volume sub")
                pdb = pd2[1].split("Volume:")
                VolumeData = pdb[1].split("<")[0]
                # print("volume data :: " + str(VolumeData))
                VolNumList = []
                for char in VolumeData:
                    if char.isdigit():
                        VolNumList.append(char)
                print("vol list")
                print(VolNumList)
                if len(VolNumList) >= 2 and len(VolNumList) <=4:
                    if len(VolNumList) == 2:
                        volume = str(VolNumList[0]) + str(VolNumList[1])
                    if len(VolNumList) == 3:
                        volume = str(VolNumList[0]) + str(VolNumList[1]) + "." +str(VolNumList[2])
                    if len(VolNumList) == 4:
                        volume = str(VolNumList[0]) + str(VolNumList[1]) + "." +str(VolNumList[2]) + str(VolNumList[3])
                buildDims["volumeLiters"] = volume
                # print("Volume data " + VolumeData)

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


                boardDataObj["finBrand"] = finType
                boardDataObj["finSetup"] = finSetup

            if "price--withoutTax" in html_source:
                pdp = html_source.split("price--withoutTax")
                pd1 = pdp[1].split(">")
                if "</" in pd1[1]:
                    pd2 = pd1[1].split("</")[0]
                    print("price data " + pd2)
                    
                    try:
                        pdSan = pd2.replace("$","").split(".")[0].replace(".","")
                        print("pd san ::: " + str(pdSan))
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
                    if "src" in presArea[0:100]:
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

            boardDataObj["dimensionMap"] = json.dumps(buildDims)

     
            stdLength = 0

            lengthNumFeet=0
            lengthNumInches=0

            try :
                lengthNumFeet = float(lengthFeet.replace(":", "").replace(" ", ""))
                lengthNumInches = float(lengthInches.replace(" ", ""))

            except:
                print("std length not able to pe parsed")
                try:
                    lengthNumFeet = float(buildDims["lengthFeet"])
                    lengthNumInches = float(buildDims["lengthInches"])
                except:
                    print("couldnt parse build feet to float either")


            stdLength = lengthNumFeet + (lengthNumInches / 12)

            try:
                stdWidth = int(json.loads(boardDataObj["dimensionMap"])["widthInches"]) + int(json.loads(boardDataObj["dimensionMap"])["widthFracNumer"]) / int(json.loads(boardDataObj["dimensionMap"])["widthFracDenom"])
            except:
                stdWidth = 0
            try:
                stdThick = int(json.loads(boardDataObj["dimensionMap"])["thicknessInches"]) + int(json.loads(boardDataObj["dimensionMap"])["thicknessFracNumer"]) / int(json.loads(boardDataObj["dimensionMap"])["thicknessFracDenom"])
            except:
                stdThick = 0

            if "new" in itemUrl:
                boardDataObj["condition"] = 100.0
            elif "used" in itemUrl:
                boardDataObj["condition"] = 80.0
            else:
                boardDataObj["condition"] = 120.0

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
            return boardDataObj


def diff_scrape_item_url(url):
    print("Diff scrape url ::: " + str(url))

    sanUrl = url.replace('"',"").replace("'","").replace("\n","")
    gsel.get(sanUrl)
    psrc = gsel.page_source

    itemLinkUrl = url.replace("\n", "")
    try:
        return scrapeItemDataPage(psrc, itemLinkUrl)
    except Exception as e:
        print(e)
        print("Error scraping Used Surf in diff_scrape_item_url_helper.scrapeItemDataPage")
        return False
    gsel.close()