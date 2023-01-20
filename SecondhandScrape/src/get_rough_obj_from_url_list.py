import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from opencage.geocoder import OpenCageGeocode
import json
from datetime import datetime
import requests
import sys
import os
from pprint import pprint
import uuid


req_keys = [
    "boardType",
    "brandShaper",
    "cdnImageList",
    "cityString",
    "completePost",
    "condition",
    "description",
    "dimensionMap",
    "finBrand",
    "finSetup",
    "itemLink",
    "itemUUID",
    "keywords",
    "latitude",
    "localImageUUIDList",
    "longitude",
    "price",
    "profilePic",
    "pwAccountType",
    "s3ImageTags",
    "sellerClass",
    "stdLength",
    "stdPrice",
    "stdThick",
    "stdVol",
    "stdWidth",
    "timeStamp",
    "title",
    "uploadTime",
    "userId",
    "userUUID",
]

bt_cap_list = [
    'Shortboard',
    'Hybrid',
    'Fish',
    'Step-up',
    'Gun',
    'Longboard',
    'Prone Paddle',
    'SUP'
]


# map of cityName string to geolocator API resp
g_loc_map = {}


def scrape_url_ret_obj(url, driver):

    print("Init page scrape")

    driver.get(url)
    time.sleep(5)
    t = driver.page_source

    itemLink = url

    bod = {}
    dimmap = {}
    buildDesc = ""
    bod["userId"] = "SecondhandBoards"
    bod["userUUID"] = "gG45uh5c3KJDFr6NCg"
    bod["cityString"] = ""
    bod["keywords"] = []
    bod["stdWidth"] = 0
    bod["stdThick"] = 0
    bod["timeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000")
    utime = datetime.strptime(bod["timeStamp"], "%Y-%m-%d %H:%M:%S.%f")
    tm = int(utime.timestamp() * 1000)
    bod["uploadTime"] = tm
    bod["localImageUUIDList"] = []
    bod["finBrand"] = ""
    bod["finSetup"] = ""
    UID = uuid.uuid4()
    UIDstring = str(UID)
    print("gen uuid ")
    bod["itemUUID"] = UIDstring

    bod["itemLink"] = itemLink

    bod["sellerClass"] = "commercial"
    bod["pwAccountType"] = "Enterprise"

    bod["completePost"] = "complete"

    bod["description"] = ""
    bod["profilePic"] = False
    bod["condition"] = 120
    bod["title"] = ""
    bod["stdVol"] = 0

    if "<title>" in t:
        s1 = t.split("<title>")[1].split("</title>")[0]
        print("Get title")
        print(s1)

        if "   " in s1:
            s1 = s1.replace("   ", "")

        bod["title"] = s1

    if "Type: <strong>" in t:
        s1 = t.split("Type: <strong>")[1]

        type_split = s1.split("</strong>")[0]

        print("type split :::  " + type_split)
        bod["p_type"] = type_split
        if len(type_split) < 60:
            ts_san = type_split.replace(" ", "").lower()
            print("Match type split :: " + ts_san)
            for bt_cap in bt_cap_list:
                if bt_cap.lower().replace(" ", "") == ts_san:
                    bod["boardType"] = bt_cap

    if "sellertype:<strong>" in t.replace(" ", "").lower():
        s1 = t.replace(" ", "").lower().split(
            "sellertype:<strong>")[1].split("</strong>")[0]
        print("seller type get :: " + str(s1))

        bod["p_seller"] = s1

    if "model:<strong>" in t.replace(" ", "").lower():
        s1 = t.replace(" ", "").lower().split(
            "model:<strong>")[1].split("</strong>")[0]
        print("model field get :: " + str(s1))

        bod["p_model"] = s1

    if "shipping:<strong>" in t.replace(" ", "").lower():
        s1 = t.replace(" ", "").lower().split(
            "shipping:<strong>")[1].split("</strong>")[0]
        print("shipping type get :: " + str(s1))

        bod["p_shipping"] = s1

    if "posted:<strong>" in t.replace(" ", "").lower():
        s1 = t.replace(" ", "").lower().split(
            "posted:<strong>")[1].split("</strong>")[0]
        print("posted type get :: " + str(s1))

        bod["p_posted"] = s1
# Seen so far
# 	shb_ft_list = [
# "Thruster",
# "Quad",
# "2+1",
# "3+2",
# "Single",
# "Twin"
# 	]

    tstrp = t.lower().replace(" ", "")
    if "finset-up:<strong>" in tstrp:
        s1 = tstrp.split("finset-up:<strong>")[1]

        fs_split = s1.split("</strong>")[0]

        print("fs split :::  " + fs_split)

        if fs_split == "thruster":
            bod["finSetup"] = "Thruster"
        if fs_split == "3+2":
            bod["finSetup"] = "Five"
        if fs_split == "2+1":
            bod["finSetup"] = "2+1"
        if fs_split == "quad":
            bod["finSetup"] = "Quad"
        if fs_split == "single":
            bod["finSetup"] = "Single"
        if fs_split == "twin":
            bod["finSetup"] = "Twin"

    if "Brand: <strong>" in t:
        s1 = t.split("Brand: <strong>")[1]

        brand_split = s1.split("</strong>")[0]
        print("brand split " + brand_split)
        if len(brand_split) < 60:
            bod["brandShaper"] = brand_split

    lengthFeet = 0
    lengthInches = 0
    if "Length: <strong>" in t:
        s1 = t.split("Length: <strong>")[1]

        l_split = s1.split("</strong>")[0]
        print("lenght split " + l_split)

        lengthData = l_split[0:30]
        lengthDigits = []

        for char in lengthData:
            if char.isdigit():
                lengthDigits += char

        if len(lengthDigits) == 4 and int(lengthDigits[0]) == 1:
            sdf = str(lengthDigits[0]) + str(lengthDigits[1])
            lengthFeet = sdf
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

        print("Length Get :: ")
        print(str(lengthFeet) + " Feet")
        print(str(lengthInches) + "  inches")

        if len(str(lengthFeet)) < 3:
            dimmap["lengthFeet"] = lengthFeet
        if len(str(lengthInches)) < 3:
            dimmap["lengthInches"] = lengthInches

    widthInches = 0
    widthFrac = 0

    trs = t.replace(" ", "")
    widthDigits = []
    if "Width:<strong>" in trs:
        s1 = trs.split("Width:<strong>")[1]

        l_split = s1.split("</strong>")[0]
        print("width split " + l_split)

        widthData = l_split[0:18]

        print("width digits ::: ")
        for char in widthData:
            if char.isdigit():
                widthDigits += char
                print(str(char))

    nwidthdigits = len(widthDigits)
    orderedDigits = widthDigits

    boardWidthInches = 0
    boardWidthFrac = 0

    if nwidthdigits == 2:
        boardWidthInches = str(orderedDigits[0]) + str(orderedDigits[1])
    if nwidthdigits == 4:
        boardWidthInches = str(orderedDigits[0]) + str(orderedDigits[1])
        widthSplitFracNum = str(orderedDigits[2])
        widthSplitFracDenom = str(orderedDigits[3])
        boardWidthFrac = widthSplitFracNum + "/" + widthSplitFracDenom

    if nwidthdigits == 5:
        boardWidthInches = str(orderedDigits[0]) + str(orderedDigits[1])
        widthSplitFracNum = str(orderedDigits[2])
        widthSplitFracDenom = str(orderedDigits[3]) + str(orderedDigits[4])
        boardWidthFrac = widthSplitFracNum + "/" + widthSplitFracDenom

    if nwidthdigits == 6:
        boardWidthInches = str(orderedDigits[0]) + str(orderedDigits[1])
        widthSplitFracNum = str(orderedDigits[2]) + str(orderedDigits[3])
        widthSplitFracDenom = str(orderedDigits[4]) + str(orderedDigits[5])
        boardWidthFrac = widthSplitFracNum + "/" + widthSplitFracDenom
    print("width digits ::: ")
    print(boardWidthInches)
    print(boardWidthFrac)

    dimmap["widthInches"] = str(boardWidthInches)
    dimmap["widthFracNumer"] = boardWidthFrac
    if "/" in str(boardWidthFrac):
        dimmap["widthFracNumer"] = boardWidthFrac.split("/")[0]
        dimmap["widthFracDenom"] = boardWidthFrac.split("/")[1]

    try:
        stw = dimmap['widthInches']
        stf = 0
        try:
            stf = float(dimmap['widthFracNumer']
                        ) // float(dimmap["widthFracDenom"])
        except Exception as e:
            print("no width inches")

        bod["stdWidth"] = float(stw) + float(stf)

    except Exception:
        print("width std no parse")

    thickInches = 0
    thickFrac = 0
    thickDigits = []
    trs = t.replace(" ", "")
    if "Thickness:<strong>" in trs:
        s1 = trs.split("Thickness:<strong>")[1]

        l_split = s1.split("</strong>")[0]
        print("thick split " + l_split)

        thickData = l_split[0:18]

        print("thickness digits ::: ")
        for char in thickData:
            if char.isdigit():
                thickDigits += char
                print(str(char))

    nthickdigits = len(thickDigits)
    orderedDigits = thickDigits

    if nthickdigits == 1:
        thickInches = str(thickDigits[0])

    if nthickdigits == 3:

        thickInches = str(orderedDigits[0])
        thickSplitFracNum = str(orderedDigits[1])
        thickSplitFracDenom = str(orderedDigits[2])
        thickFrac = thickSplitFracNum + "/" + thickSplitFracDenom

    if nthickdigits == 4:

        thickInches = str(orderedDigits[0])
        thickSplitFracNum = str(orderedDigits[1])
        thickSplitFracDenom = str(orderedDigits[2]) + str(orderedDigits[3])
        thickFrac = thickSplitFracNum + "/" + thickSplitFracDenom

    if nthickdigits == 5:

        thickInches = str(orderedDigits[0])
        thickSplitFracNum = str(orderedDigits[1]) + str(orderedDigits[2])
        thickSplitFracDenom = str(orderedDigits[3]) + str(orderedDigits[4])
        thickFrac = thickSplitFracNum + "/" + thickSplitFracDenom

    print("thicknessInches :: " + str(thickInches))
    print("thicknessFrac :: " + str(thickFrac))

    dimmap["thicknessInches"] = str(thickInches)
    dimmap["thicknessFracNumer"] = thickFrac
    if "/" in str(thickFrac):
        dimmap["thicknessFracNumer"] = thickFrac.split("/")[0]
        dimmap["thicknessFracDenom"] = thickFrac.split("/")[1]

    try:
        stw = dimmap['thicknessInches']
        stf = 0
        try:
            stf = float(dimmap['thicknessFracNumer']
                        ) // float(dimmap["thicknessFracDenom"])
        except Exception as e:
            print("no width inches")

        bod["stdThick"] = float(stw) + float(stf)

    except Exception:
        print("width std no parse")

    vol_num = 0

    trs = t.replace(" ", "")
    volDigits = []
    if "Volume:<strong>" in trs:
        print("found vol div")
        s1 = trs.split("Volume:<strong>")[1]

        l_split = s1.split("</strong>")[0]
        print("Volume split " + l_split)

        volData = l_split[0:18]

        print("volume digits ::: ")
        for char in volData:
            if char.isdigit():
                volDigits += char
                print(str(char))
    vol_build = "0"
    if len(volDigits) < 3:
        for vchar in volDigits:
            vol_build += str(vchar)
    dimmap["volumeLiters"] = vol_build
    bod["stdVol"] = float(vol_build)

    if "Model:<strong>" in t.replace(" ", ""):
        s1 = t.split("Model: <strong>")[1]

        m_split = s1.split("</strong>")[0]
        print("model split " + m_split)
        if len(m_split) < 60:
            buildDesc += m_split

# Good on everything
    if "Condition:<strong>" in t.replace(" ", ""):
        s1 = t.replace(" ", "").split("Condition:<strong>")[1]
        c_split = s1.split("</strong>")[0]
        print("condition ::: " + str(c_split))

        bod["conditionText"] = c_split

    if "Price:<strong>" in t.replace(" ", ""):
        s1 = t.replace(" ", "").split("Price:<strong>")[1]
        c_split = s1.split("</strong>")[0]
        print("price::: " + str(c_split))

        pget = ""
        for char in c_split[0:8]:
            if char.isdigit():
                pget += str(char)

        print("get price :::   " + str(pget))

        bod["price"] = str(pget)

    
    get_cdn_imgs = []
    board_slugs_get = []
    img_split = t.split('https://www.secondhandboards.com/boardimages/')

    for imreg in img_split:
        print("found im split im reg")
        imreg_check = imreg[:888]
        print(imreg_check)

        if "/boardimages/" in imreg_check.replace(" ", ""):
            print("found im region")

            if "/boardimages/" in imreg_check and "class" in imreg_check:

                for bis in imreg_check.split("/boardimages/"):
                    imslug = bis.split("class")[0]
                    imget = "/boardimages/" + imslug
                    print("im get done ::: ")
                    print(imget)
                    if imget not in board_slugs_get:
                        board_slugs_get.append(imget)

    for bs in board_slugs_get:
        bss = bs.replace("\"", "").replace("\\", "").replace("'", "")
        get_cdn_imgs.append(
            "https://www.secondhandboards.com/boardimages" + bss)


    bod["s3ImageTags"] = get_cdn_imgs

    if len(get_cdn_imgs) >0:
        print("image scraping successful, continue with geocoding request")
        if "Location: <strong>" in t:
            s1 = t.split("Location: <strong>")[1]
            c_split = s1.split("</strong>")[0]
            print("GOT LOCATION ::: " + c_split)

            bod["cityString"] = c_split
            s2 = s1.split("<p>")[1].split("</p>")[0].replace("�", " ")

            print("p desc attempt ::: ")
            print(s2)
            bod["p_description"] = s2

            bod["latitude"] = 0.0
            bod["longitude"] = 0.0
            if c_split not in g_loc_map.keys():
                geocoder = OpenCageGeocode(
                    os.environ['OPENCAGE_API_KEY_STSCRAPE_GEOCODE']
                    )
                query = c_split
                results = geocoder.geocode(query)
                if len(results) > 0:
                    try:
                        g_loc_map[c_split] = (
                            results[0]["geometry"]["lat"], results[0]["geometry"]["lng"])
                        print("geocode results")
                        pprint(results)
                        print("SET GEOCODE COORDS ::: " + str(
                            results[0]["geometry"]["lat"]) + " __ " + str(results[0]["geometry"]["lng"]))
                        bod["latitude"] = results[0]["geometry"]["lat"]
                        bod["longitude"] = results[0]["geometry"]["lng"]

                    except Exception:
                        print("Geocoding error")
            else:
                print("Using cached g loc map location COORDS" +
                str(g_loc_map[c_split][0]) + " __ " + str(g_loc_map[c_split][1]))
                bod["latitude"] = g_loc_map[c_split][0]
                bod["longitude"] = g_loc_map[c_split][1]

                # Get the description with same split
                print("p desc get ::: ")
                print(s2)
                bod["p_description"] = s2


    build_dims = {"thicknessInches": " ", "thicknessFracNumer": " ", "lengthFeet": " ", "widthFrac": " ", "widthFracNumer": " ",
                  "thicknessFrac": " ", "thicknessFracDenom": " ", "volumeLiters": " ", "widthFracDenom": " ", "lengthInches": " ", "widthInches": " "}

    std_length_build = " "

    # if lengthFeet != 0 and len(str(lengthFeet)) < 3:
    # 	build_dims["lengthFeet"] = lengthFeet
    for k, v in build_dims.items():
        if k in dimmap.keys():
            build_dims[k] = dimmap[k]
    bod["dimensionMap"] = build_dims

    std_length_build = 0
    try:
        std_length_build += int(lengthFeet)
        std_length_build += int(lengthInches)/12
        print("built complete std length ::: " + str(std_length_build))
    except Exception as e:
        print("could not conv length to int")
        print(e)

    bod["stdLength"] = std_length_build

    price_int = 0
    try:
        price_int = int(bod["price"])

    except:
        print("no int price")
    bod["stdPrice"] = price_int

    js_obj = bod

    for rk in req_keys:
        if rk not in js_obj.keys():
            print("NEED FIELD ADDED ::: " + rk)

    print("final board obj ::: ")
    print(json.dumps(bod))

    return bod


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path=sys.argv[2], options=chrome_options)

    urls_to_scrape = []
    with open(sys.argv[1] + "/toAdd_urls", "r") as urlf:
        urls_to_scrape = urlf.readlines()

    for url in urls_to_scrape:
        print("found url ::: " + str(url))
        sanurl = url.replace('"', "")
        sobj = scrape_url_ret_obj(sanurl, driver)

        with open(sys.argv[1] + '/scrape_run_data_dump', 'a+') as srd:
            srd.write(json.dumps(sobj) + "\n")
