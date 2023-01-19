import json
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helper_scrape_methods import countTotalBracketsInJson, parseJsonToCloseBracket, removeCharsToOpenBracket


chrome_options = Options()
chrome_options.add_argument("--headless")
gsel = webdriver.Chrome(sys.argv[2], options=chrome_options)


def objScrape(pageString, itemurl):
    jsonStart = ""
    try:
        jsonStart = removeCharsToOpenBracket(pageString.split("product-json")[1].split("</")[0])
    except Exception as rcerr:
        print("[Error objScrape] in remove chars")
        print(rcerr)
        return False

    json_parse_1 = parseJsonToCloseBracket(jsonStart)
    product_json_obj = json.loads(json_parse_1)
    product_json_obj["itemLink"] = itemurl
    return product_json_obj

def scrape_item_url(scrapeUrl, timeslug):
    print("Scrape new item url :: " + str(scrapeUrl))

    gsel.get(scrapeUrl)
    phtml = gsel.page_source

    objParse = objScrape(phtml, scrapeUrl)
    print("scrape new item result ::: ")
    print(objParse)

    if objParse == False:
        return

    with open(sys.argv[1] + '/scraped_items', "a+") as taf:
        taf.write(json.dumps(objParse) + "\n")


    return objParse

if __name__ == "__main__":
    print("init item scrape")

    file_time_slug = datetime.now().strftime("%m-%d-%Y--%H%M")

    addUrls = []
    with open( sys.argv[1] + "/toAdd_urls" ,"r") as addf:
        addUrls = addf.readlines()
        
        for aurl in addUrls:
            if len(aurl) >1:
                scrape_item_url(aurl, file_time_slug)
   
    
