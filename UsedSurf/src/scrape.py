
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
    time.sleep(2)
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
          "title" : "",
          "price" : " ",
          "brandShaper" : "",
          "description" : "",
                "itemLink": itemUrl,
          "latitude" : 33.4344735,
          "longitude" : -117.6241256,
          "dimensionMap" : """{"lengthFeet":" ","lengthInches":" ","widthInches":" ","widthFracNumer":" ","widthFracDenom":" ","widthFrac":" ","thicknessInches":" ","thicknessFracNumer":" ","thicknessFracDenom":" ","thicknessFrac":" ","volumeLiters":" "}""",
          "finBrand" : "",
          "finSetup" : "",
          "boardType" : "",
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

            # if "Model:" in pd2[1]:
            #     pdb = pd2[1].split("Model:")
            #     modelData = pdb[1].split("<")[0]
            #     boardDataObj["title"] = modelData
            #     print("brand data " + modelData)
            #     sModelD = modelData.replace(" ", "")
            #     if sModelD == "N/A":



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
                        lengthFeet = ldf
                        lengthInches = lengthData.split("'")[1].split(" ")[0].replace("\"", "")



                if lengthFeet != "0":
                    buildDims["lengthFeet"] = lengthFeet.replace(":","").replace(" ", "")
                else:
                    buildDims["lengthFeet"] = "0"
                if lengthInches !="0":
                    buildDims["lengthInches"] = lengthInches.replace(" ","")
                else:
                    buildDims["lengthInches"] = "0"


            if "Width:" in pd2[1]:
                pdb = pd2[1].split("Width")
                widthData = pdb[1].split("<")[0]


                widthNumList = []
                for char in widthData:
                    if char.isdigit():
                        widthNumList.append(char)

                if "." in widthData:
                    widthFracNumer = "0"
                    widthFracDenom = "1"
                    widthInches = "0"

                elif len(widthNumList) >=4 and len(widthNumList)<=6:
                    widthInches = str(widthNumList[0]) + str(widthNumList[1])

                    buildDims["widthInches"] = widthInches
                elif len(widthNumList) == 4:
                    widthFracNumer = str(widthNumList[2])
                    widthFracDenom = str(widthNumList[3])

                elif len(widthNumList) == 5:
                    widthFracNumer = str(widthNumList[2])
                    widthFracDenom = str(widthNumList[3]) + str(widthNumList[4])

                elif len(widthNumList) == 6:
                    widthFracNumer = str(widthNumList[2]) + str(widthNumList[3])
                    widthFracDenom = str(widthNumList[4]) + str(widthNumList[5])
                buildDims["widthFracNumer"] = widthFracNumer
                buildDims["widthFracDenom"] = widthFracDenom
                buildDims["widthFrac"] = str(widthFracNumer) + "/" + str(widthFracDenom)


            if "Thickness:" in pd2[1]:
                pdb = pd2[1].split("Thickness")
                ThicknessData = pdb[1].split("<")[0]

                print("thick data " + str(ThicknessData))


                ThicknessNumList = []
                for char in ThicknessData:
                    if char.isdigit():
                        ThicknessNumList.append(char)

                if "." in ThicknessData:
                    thicknessInches = "0"
                    thicknessFracNumer = "0"
                    thicknessFracDenom = "1"

                elif len(ThicknessNumList) >=3 and len(ThicknessNumList)<=5:
                    thicknessInches = str(ThicknessNumList[0])

                    buildDims["thicknessInches"] = thicknessInches

                elif len(ThicknessNumList) == 3:
                    thicknessFracNumer = str(ThicknessNumList[1])
                    thicknessFracDenom = str(ThicknessNumList[2])


                elif len(ThicknessNumList) == 4:
                    thicknessFracNumer = str(ThicknessNumList[1])
                    thicknessFracDenom = str(ThicknessNumList[2]) + str(ThicknessNumList[3])

                elif len(ThicknessNumList) == 5:
                    thicknessFracNumer = str(ThicknessNumList[1]) + str(ThicknessNumList[2])
                    thicknessFracDenom = str(ThicknessNumList[3]) + str(ThicknessNumList[4])
                    buildDims["thicknessFrac"] = str(thicknessFracNumer) + "/" + str(thicknessFracDenom)


                buildDims["thicknessFracNumer"] = thicknessFracNumer
                buildDims["thicknessFracDenom"] = thicknessFracDenom

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
                        volume = str(VolNumList[0]) + str(VolNumList[1])
                    if len(VolNumList) == 3:
                        volume = str(VolNumList[0]) + str(VolNumList[1]) + "." +str(VolNumList[2])
                    if len(VolNumList) == 4:
                        volume = str(VolNumList[0]) + str(VolNumList[1]) + "." +str(VolNumList[2]) + str(VolNumList[3])

                buildDims["volumeLiters"] = volume

                print("Volume data " + VolumeData)

            # if "Contruction:" in pd2[1]:
            #     pdb = pd2[1].split("Contruction:")
            #     ContructionData = pdb[1].split("<")[0]
            #     print("length data " + lengthData)

            if "Fins:" in pd2[1]:
                pdb = pd2[1].split("Fins:")
                finsData = pdb[1].split("<")[0]
                print("fins data " + finsData)

                finType = ""
                finSetup = ""

                if "fcs" in finsData.lower():
                    finType = "FCS"

                if "future" in finsData.lower():
                    finType = "Future"

                finStringRegionGet = finsData.lower()
                #
                # if "Future" in finStringRegionGet:
                #     finType = "Future"
                # if "FCS" in finStringRegionGet:
                #     finType = "FCS"
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


            # if "Description:" in pd2[1]:
            #     descSplit = pd2[1].split("Description:")[1]
            #
            #     obs = descSplit.split(">")
            #
            #     for seg in obs:
            #         print("seg:::" + seg)
            #         if seg[1] == "<":
            #             continue
            #         else:
            #
            #             descData = seg.split("<")[0]
            #             print("Desc data ::: " +descData)
            #             if "&nbsp" in descData:
            #                 continue
            #             else:
            #                 print("found desc data::" +descData)
            #                 boardDataObj["description"] = descData
            #                 break


                # pdb = pd2[1].split("Description:")
                # pd1 = pdb[1].split("strong")
                # if "</" in pd1[2]:
                #     pd2 = pd1[2].split("</")[0]
                #     print("desc data " + pd2)
                #     boardDataObj["description"] = pd2

            if "price--withoutTax" in html_source:
                pdp = html_source.split("price--withoutTax")
                pd1 = pdp[1].split(">")
                if "</" in pd1[1]:
                    pd2 = pd1[1].split("</")[0]
                    print("price data " + pd2)
                    pdSan = pd2.replace("$","")
                    boardDataObj["price"] = pdSan


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


            boardDataObj["dimensionMap"] = json.dumps(buildDims)

            print("ldf" + str(lengthFeet))
            print("ldi" + str(lengthInches))
            print("wi:" + str(widthInches))
            print("wfn:" + str(widthFracNumer))
            print("wfd:" + str(widthFracDenom))
            print("ti:" + str(thicknessInches))
            print("tfn:" + str(thicknessFracNumer))
            print("tfd:" + str(thicknessFracDenom))
            print("vd:" + str(volume))
            print("desc:" + boardDataObj["description"])


            '''
            Convert dims to STD values for searching
            '''


            stdLength = 0

            lengthNumFeet=0
            lengthNumInches=0

            try :
                lnf = lengthFeet.replace(":", "")
                lengthNumFeet = int(lnf.replace(" ", ""))
                lengthNumInches = int(lengthInches.replace(" ", ""))

            except:
                print("std length not able to pe parsed")



            stdLength = lengthNumFeet + (lengthNumInches / 12)

            stdWidth = int(json.loads(boardDataObj["dimensionMap"])["widthInches"]) + int(json.loads(boardDataObj["dimensionMap"])["widthFracNumer"]) / int(json.loads(boardDataObj["dimensionMap"])["widthFracDenom"])


            stdThick = int(json.loads(boardDataObj["dimensionMap"])["thicknessInches"]) + int(json.loads(boardDataObj["dimensionMap"])["thicknessFracNumer"]) / int(json.loads(boardDataObj["dimensionMap"])["thicknessFracDenom"])

            if "new" in itemLinkUrl:
                boardDataObj["condition"] = 100.0
            elif "used" in itemLinkUrl:
                boardDataObj["condition"] = 80.0
            else:
                boardDataObj["condition"] = 120.0



            boardDataObj["stdLength"] = stdLength
            boardDataObj["stdWidth"] = stdWidth
            boardDataObj["stdThick"] = stdThick
            boardDataObj["stdVol"] = float(json.loads(boardDataObj["dimensionMap"])["volumeLiters"])
            boardDataObj["stdPrice"] = float(boardDataObj["price"])


            print("board obj:")
            print(str(boardDataObj) + "\n")

            with open("../data/used_surf_parsed_objects.txt", 'a+') as objF:
                objF.write(json.dumps(boardDataObj) + "\n")
                # json.dump(boardDataObj, objF)
                # objF.write("\n")
                # objF.close()



if __name__ == '__main__':

    


    print("Init main used surf scrape")
    gsel = webdriver.PhantomJS()
    buildUrlListsAndOutputItemUrls()


# for testing
    # newUrls = [
    #     "https://usedsurf.com/new-surfboards/?sort=featured&page=1",
    #     "https://usedsurf.com/new-surfboards/?sort=featured&page=2",
    #     "https://usedsurf.com/new-surfboards/?sort=featured&page=3"
    #
    # ]


    urls = []

    with open("../data/scraped_Item_Urls.txt") as urlF:
        urls = urlF.readlines()

    startidx = 107
    urlidx = 0
    for itemUrl in urls:
        if urlidx < startidx:
            urlidx+=1
            continue
        elif urlidx < len(urls):
            sanUrl = urls[urlidx].replace("\"", "")
            gsel.get(sanUrl)
            psrc = gsel.page_source

            itemLinkUrl = sanUrl.replace("\n", "")
            scrapeItemDataPage(psrc, itemLinkUrl)
            # with open("item_html_src_example.txt", 'a+') as htmlsrc:
            #     htmlsrc.write(psrc)
        urlidx +=1



    gsel.close()