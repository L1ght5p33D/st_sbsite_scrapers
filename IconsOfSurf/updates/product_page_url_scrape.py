import time
from selenium import webdriver
import json
from datetime import datetime

def contains_digit(s):
    return any(i.isdigit() for i in s)

def count_digits(s):
    dcount = 0
    for i in s:
        if i.isdigit():
            dcount +=1
    return dcount


def scrape_product_url(productUrl, baseurl):
	gsel = webdriver.PhantomJS()
	print("starting scrape method")
	time.sleep(1)
	gsel.get(productUrl)
	bPageSrc = gsel.page_source
	boardUrl = productUrl
	checkImageArr = []
	imgMainGet = None
	secondaryImagesSplitSrc1 = None
	secondaryImagesSplitSrc2 = None


	boardDesc = " "
	boardTitle = " "
	boardPriceNum = " "

	boardLengthFeet = " "
	boardLengthInches = " "
	boardWidthInches = " "
	boardWidthFrac = " "
	boardThickInches = " "
	boardThickFrac = " "

	boardFinSetup = " "
	boardFinBrand = " "

	boardType = " "

	UUIDwithBoardSKU = "IconsOfSurfBoardId-"

	print("board url ::: " + boardUrl)
	print("base url :::" + baseurl)

	if "longboard" in baseurl:
	    boardType = "Longboard"
	elif "shortboard" in baseurl:
	    boardType = "Shortboard"
	elif "fish" in baseurl:
	    boardType = "Fish"
	elif "mid-length" in baseurl:
	    boardType = "Funboard"

	try:
	    imgMainSplit = bPageSrc.split('<div class="image-box"')
	    imgMainSplitHref = imgMainSplit[1].split("href=\"")
	    imgMainGet= imgMainSplitHref[1].split("\"")[0]

	    print("image main get ::: " + imgMainGet)
	    checkImageArr.append(imgMainGet)

	    imgSecondarySplit = bPageSrc.split('<div class="dpimages-icons-box"')
	    imgSecondarySplitDivs = imgSecondarySplit[1].split("<a href=\"")

	    secondaryImagesSplitSrc1 = imgSecondarySplitDivs[1].split("\"")[0]
	    secondaryImagesSplitSrc2 = imgSecondarySplitDivs[2].split("\"")[0]

	    print("second img split 1" + secondaryImagesSplitSrc1)
	    print("second img split 2"+ secondaryImagesSplitSrc2)
	    checkImageArr.append(secondaryImagesSplitSrc1)
	    checkImageArr.append(secondaryImagesSplitSrc2)
	except Exception:
	    print("exception in secondary image get")

	gotImageArr = []
	for imgUrl in checkImageArr:
	    if imgUrl != None:
	        gotImageArr.append(imgUrl)

	boardBrandShaper = bPageSrc.split('<div class="brand-name">')[1].split(">")[1].split("</")[0]
	print("board brand shaper::" + boardBrandShaper)

	boardTitleSplit = bPageSrc.split("<h1>")
	boardTitle = boardTitleSplit[1].split("</h1>")[0]
	print("board title::" + boardTitle)

	boardPriceSplit = bPageSrc.split('product_price">')[1].split("<")[0]
	boardPriceNum = round(float(boardPriceSplit), 2)
	print("board price ::::" + str(boardPriceNum))

	descSplit = bPageSrc.split('</h1>')[1]
	descGet = descSplit.split("<table")[0]

	descParse = descGet.lower()

	print("parsing desc parse ::: ")
	print(descParse)
	if "tail:" in descParse:
	    print("got lower tail in desc parse")
	    tailTypeGet = descParse.split("tail:")[1].split("<br>")[0]
	    tailTypeGet.replace(" ", "")
	    print("found tail type ::" + tailTypeGet)
	    if tailTypeGet == "fish":
	        boardType = "Fish"

	if "fin:" in descParse:
	    print("got lower fin in desc parse")
	    finTypeGet = descParse.split("fin:")[1].split("/table")[0]
	    print("fin div get :: " + finTypeGet)
	    if len(finTypeGet) > 20:
	        finTypeGet = finTypeGet[0:15]
	    print("fin div trunc :: " + finTypeGet)
	    if "future" in finTypeGet:
	        boardFinBrand = "Future"
	    elif "fcs" in finTypeGet:
	        boardFinBrand = "FCS"
	    if "single" in finTypeGet:
	        boardFinSetup = "Single"
	    if "5" in finTypeGet or "five" in finTypeGet:
	        boardFinSetup = "Five"
	    if "quad" in finTypeGet:
	        boardFinSetup = "Quad"
	    if "twin" in finTypeGet:
	        boardFinSetup = "Twin"
	    if "thruster" in finTypeGet:
	        boardFinSetup = "Thruster"
	    if "trailer" in finTypeGet:
	        boardFinSetup = "2+1"
	    if "2+1" in finTypeGet or "2 + 1" in finTypeGet:
	        boardFinSetup = "2+1"

	if "style=" in descGet:
	    descStyleSplit = descGet.split("style=")
	    descStyleSplitTagSplit = descStyleSplit[0].split(">")
	    descGet = descStyleSplit[0] + descStyleSplitTagSplit[1]


	descSanitize = descGet.replace("<p>", " ")
	descSanitize = descSanitize.replace("</p>", " ")
	descSanitize = descSanitize.replace("<div>", " ")
	descSanitize = descSanitize.replace("</div>", " ")
	descSanitize = descSanitize.replace("<br>", " ")
	descSanitize = descSanitize.replace("<em>", " ")
	descSanitize = descSanitize.replace("</em>", " ")
	descSanitize = descSanitize.replace("<td>", " ")
	descSanitize = descSanitize.replace("</td>", " ")
	descSanitize = descSanitize.replace("<tr>", " ")
	descSanitize = descSanitize.replace("</tr>", " ")
	descSanitize = descSanitize.replace("<tbody>", " ")
	descSanitize = descSanitize.replace("</tbody>", " ")
	descSanitize = descSanitize.replace("<table>", " ")
	descSanitize = descSanitize.replace("</table>", " ")
	descSanitize = descSanitize.replace("&nbsp;", " ")
	descSanitize = descSanitize.replace("&nbsp", " ")
	descSanitize = descSanitize.replace("\n", " ")
	descSanitize = descSanitize.replace('<p class="p1">'," ")
	descSanitize = descSanitize.replace("<strong>", " ")
	descSanitize = descSanitize.replace("</strong>", " ")
	descSanitize = descSanitize.replace("<span>", " ")
	descSanitize = descSanitize.replace("</span>", " ")
	descSanitize = descSanitize.replace('<p class="p2">', " ")
	descSanitize = descSanitize.replace("u201c", " ")
	descSanitize = descSanitize.replace("&amp;", "")
	descSanitize = descSanitize.replace("&amp", "")

	boardDesc = descSanitize
	print("boardDesc" + boardDesc)

	lengthSplit = bPageSrc.split("<th>Length</th")[1].split("<td>")[1].split("<")[0]

	print("ln split orig")
	print(str(lengthSplit))
	lengthSplitFeet = lengthSplit.split("'")[0]
	print("ln splt zer")
	print(lengthSplitFeet)
	lengthSplitInches = lengthSplit.split("'")[1]
	print("leng spit inches 1")
	print(lengthSplitInches)

	nlengthdigitsfeet = count_digits(lengthSplitFeet)
	orderedDigits = []
	for i in lengthSplitFeet:
	    if i.isdigit():
	        orderedDigits.append(i)
	print("using ordererd digins")
	print(str(orderedDigits))
	if nlengthdigitsfeet == 1:
	    boardLengthFeet = str(orderedDigits[0])
	if nlengthdigitsfeet == 2:
	    boardLengthFeet = str(orderedDigits[0]) + str(orderedDigits[1])

	print("past feet method")
	nlengthdigitsinches = count_digits(lengthSplitInches)
	orderedDigits = []
	for i in lengthSplitInches:
	    if i.isdigit():
	        orderedDigits.append(i)
	if nlengthdigitsinches == 1:
	    boardLengthInches = str(orderedDigits[0])
	if nlengthdigitsinches == 2:
	    boardLengthInches = str(orderedDigits[0]) + str(orderedDigits[1])

	print("length feet :: " + boardLengthFeet)
	print("length inches :: " + boardLengthInches)

	widthSplit = bPageSrc.split("<th>Width</th")[1].split("<td>")[1].split("<")[0]
	nwidthdigits = count_digits(widthSplit)
	orderedDigits = []
	for i in widthSplit:
	    if i.isdigit():
	        orderedDigits.append(i)
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

	# widthParseInches = widthSplit.split(" ")
	# boardWidthInches = widthParseInches[0]
	# if "/" in widthSplit:
	#     boardWidthFrac = widthParseInches[1]
	print("widthInches :: " + boardWidthInches)
	print("widthFrac :: " + boardWidthFrac)

	thickSplit = bPageSrc.split("<th>Thickness</th")[1].split("<td>")[1].split("<")[0]

	nthickdigits = count_digits(thickSplit)
	orderedDigits = []
	for i in thickSplit:
	    if i.isdigit():
	        orderedDigits.append(i)
	if nthickdigits == 1:
	    for i in thickSplit:
	        if i.isdigit():
	            boardThickInches = str(i)
	if nthickdigits == 3:

	    boardThickInches = str(orderedDigits[0])
	    thickSplitFracNum = str(orderedDigits[1])
	    thickSplitFracDenom = str(orderedDigits[2])
	    boardThickFrac = thickSplitFracNum + "/" + thickSplitFracDenom

	if nthickdigits == 4:

	    boardThickInches = str(orderedDigits[0])
	    thickSplitFracNum = str(orderedDigits[1])
	    thickSplitFracDenom = str(orderedDigits[2]) + str(orderedDigits[3])
	    boardThickFrac = thickSplitFracNum + "/" + thickSplitFracDenom

	if nthickdigits == 5:

	    boardThickInches = str(orderedDigits[0])
	    thickSplitFracNum = str(orderedDigits[1]) + str(orderedDigits[2])
	    thickSplitFracDenom = str(orderedDigits[3]) + str(orderedDigits[4])
	    boardThickFrac = thickSplitFracNum + "/" + thickSplitFracDenom

	print("thickInches :: " + boardThickInches)
	print("thickFrac :: " + boardThickFrac)




	boardSKUSplit = bPageSrc.split('<td class="property-name">SKU:</td>')[1].split('colspan="2">')[1].split("<")[0]

	UUIDwithBoardSKU += boardSKUSplit
	print("board uuid with sku ::: " + UUIDwithBoardSKU)

	boardDataObj = {}
	dimensionMap = {}

	dimensionMap["volumeLiters"] = " "
	dimensionMap["lengthInches"] = boardLengthInches
	dimensionMap["lengthFeet"] = boardLengthFeet

	dimensionMap["widthInches"] = boardWidthInches
	if "/" in boardWidthFrac:
	    dimensionMap["widthFrac"] = boardWidthFrac
	    dimensionMap["widthFracNumer"] = boardWidthFrac.split("/")[0]
	    dimensionMap["widthFracDenom"] = boardWidthFrac.split("/")[1]
	else:
	    dimensionMap["thicknessFrac"] = " "
	    dimensionMap["thicknessFracNumer"] = " "
	    dimensionMap["thicknessFracDenom"] = " "

	dimensionMap["thicknessInches"] = boardThickInches
	if "/" in boardThickFrac:
	    dimensionMap["thicknessFrac"] = boardThickFrac
	    dimensionMap["thicknessFracNumer"] = boardThickFrac.split("/")[0]
	    dimensionMap["thicknessFracDenom"] = boardThickFrac.split("/")[1]
	else:
	    dimensionMap["thicknessFrac"] = " "
	    dimensionMap["thicknessFracNumer"] = " "
	    dimensionMap["thicknessFracDenom"] = " "

	print("dim map")
	print(str(dimensionMap))


	keyWordsAll = ["icons"]

	brandShaperKeyWords = boardBrandShaper.split(" ")

	for kw in brandShaperKeyWords:
	    kwl = kw.lower()
	    keyWordsAll.append(kwl)

	boardDataObj["title"] = boardTitle
	boardDataObj["description"] = boardDesc + "  For more information visit iconsofsurf.com, call us at 949-429-7133 or come visit our store at 710 N. El Camino Real San Clemente, CA 92672"
	boardDataObj["price"] = str(boardPriceNum)
	boardDataObj["cdnImageList"] = gotImageArr
	boardDataObj["itemLink"] = boardUrl
	boardDataObj["profilePic"] = False
	boardDataObj["boardType"] = boardType
	boardDataObj["finBrand"] = boardFinBrand
	boardDataObj["finSetup"] = boardFinSetup
	boardDataObj["localImageUUIDList"] = json.dumps([])
	boardDataObj["condition"] = 100
	boardDataObj["latitude"] = "33.4301191"
	boardDataObj["longitude"] = "-117.6182791"
	boardDataObj["cityString"] = "San Clemente"
	boardDataObj["completePost"] = "complete"
	boardDataObj["brandShaper"] = boardBrandShaper
	boardDataObj["dimensionMap"] = json.dumps(dimensionMap)
	boardDataObj["userId"] = "IconsOfSurf"
	boardDataObj["keywords"] = json.dumps(keyWordsAll)
	boardDataObj["timeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000")
	boardDataObj["itemUUID"] = UUIDwithBoardSKU
	boardDataObj["userUUID"] = "Eej2PG0B5UJ_N8i6L8NK"

	print("final board obj")
	itemObjStr = json.dumps(boardDataObj)
	print(itemObjStr)


	with open("scraped_items_", "a+") as fSave:
		fSave.write(itemObjStr + '\n')
		fSave.close()

