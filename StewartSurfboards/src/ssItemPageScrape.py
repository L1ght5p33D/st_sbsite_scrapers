import json
import time
import datetime
import os
from selenium import webdriver



def countTotalBracketsInJson(sdata):
	openBrackets = 0
	closeBrackets = 0

	for char in sdata:
		if char == "{":
			openBrackets+=1
		if char == "}":
			closeBrackets +=1
		if openBrackets == closeBrackets and openBrackets != 0:
			break

	total = openBrackets, closeBrackets
	return total

def parseJsonToCloseBracket(sdata):
	itemJson = ""
	openB, closeB = countTotalBracketsInJson(sdata)

	for char in sdata:
		itemJson +=char
		if char == "{":
			openB -=1
		if char == "}":
			closeB -=1
		if closeB == 0:
			break

	print("parsed json ::: ")
	print(itemJson)

	return itemJson

def removeCharsToOpenBracket(sd):
	trimString = sd
	for char in sd:
		if char != "{":
			trimString = trimString[1:]
		else:
			break
	return trimString


def objScrape(pageString):
	jsonStart = ""
	try:
		jsonStart = removeCharsToOpenBracket(pageString.split("product-json")[1].split("</")[0])
	except Exception as rcerr:
		print("[Error objScrape] in remove chars")
		print(rcerr)
		#look for 
		return False

	json_parse_1 = parseJsonToCloseBracket(jsonStart)
	json_obj = json.loads(json_parse_1)
	return json_obj


def scrapePageForItemJson(scrapeUrl):

	global gsel

	gsel.get(scrapeUrl)
	phtml = gsel.page_source

	objParse = objScrape(phtml)
	return objParse



if __name__ == '__main__':


	print("init selenium phantom")
	gsel = webdriver.PhantomJS()
	print("init scrape")

	ssUrlFile = '../data/stewartItemUrls.txt'
	urlBase = "https://stewart-surfboards.myshopify.com"

	urls = []
	with open(ssUrlFile) as urlF:
		urls = urlF.readlines()
	urlF.close()


	su_index = 0
	with open("../data/full_scrape_data.txt", 'w+') as f:
		for url_slug in urls:
			su_index +=1
			print("scraping url number ~ "+str(su_index)+" ::: " + urlBase + url_slug)
			time.sleep(2)
			pageGetObj = scrapePageForItemJson(urlBase + url_slug)
			
			if pageGetObj != False:
				f.write(json.dumps(pageGetObj)+"\n")

		gsel.close()



