from datetime import datetime
from diff_scrape_item_url_helper import diff_scrape_item_url
import json
import uuid
from elasticsearch import Elasticsearch, exceptions, TransportError, RequestsHttpConnection
import os
import pprint
import time
from datetime import datetime
import sys
from selenium import webdriver

def parse_and_save_diff_urls(psrc):
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
            with open("../data/diff_urls.txt", 'a+') as f:
                f.write(s4.replace('"',"").replace("'","") + "\n")

        cardNum += 1



def scrapeProductsPageForItemUrls(scrapeUrl):

    global gsel
    # time.sleep(1)
    gsel.get(scrapeUrl)
    phtml = gsel.page_source
    parse_and_save_diff_urls(phtml)

def buildUrlListsAndOutputItemUrls():
    print("buuild url lists called")
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

    allUrls = []

    for nUrl in newUrls:
        scrapeProductsPageForItemUrls(nUrl)
    for uUrl in usedUrls:
        scrapeProductsPageForItemUrls(uUrl)


if __name__ == "__main__":
    print("~~~ Used Surf Scrape ~~~")
    _3TradeElasticInstance = Elasticsearch()
    old_url_file = "../data/last_urls.txt"
    new_url_file = "../data/diff_urls.txt"

    file_time_slug = datetime.now().strftime("%m-%d-%Y--%H%M")

    gsel = webdriver.PhantomJS()
    linesOld = []
    linesNew = []

    USE_TEST_URLS = False
    
    if USE_TEST_URLS == True:
        with open("../data/test_urls.txt") as turls:
            linesNew = turls.readlines()
    elif USE_TEST_URLS == False:
        buildUrlListsAndOutputItemUrls()
        with open(new_url_file) as nfile:
            linesNew = nfile.readlines()

    # linesOldSan = []
    linesNewSan = []
    # for line in linesOld:
    #     linesOldSan.appned(line.replace('"',"").replace("'",""))
    for line in linesNew:
        linesNewSan.append(line.replace('"',"").replace("'","").replace("\n",""))

    # linesOld = linesOldSan
    linesNew = linesNewSan

    linesOld = []
    
    print("read line NEW ELASTIC OLD URL METHOD")
    # with open(old_url_file) as ofile:
    #     linesOld = ofile.readlines()

    us_search = _3TradeElasticInstance.search(index=sys.argv[1],body={
        "query":{"match":{"userId":"UsedSurfSC"}}
    }, size= 500
                                )
    print("used surf found items ::: " + str(us_search["hits"]["total"]["value"]))

    for hit in us_search["hits"]["hits"]:
        linesOld.append(hit["_source"]["itemLink"].replace('"',"").replace("'","").replace("\n",""))

    print("New lines old ::: ")


    for line in linesNew:

        sanLine = line.replace('"',"").replace("'","").replace("\n","")
        print("comparing new line ::: " + sanLine)
        if sanLine not in linesOld:
            if len(linesOld) > 0:
                print("compare to lines old :::" + linesOld[0])
                print("new line not in old ::: " + str(sanLine))

            try:
                print("diff scrape new url")
                diffNewItemObj_Response = diff_scrape_item_url(line)
                if diffNewItemObj_Response != False:

                    print("scrape res::: " )
                    print(diffNewItemObj_Response)
                    # with open("../updates/toAdd-" + file_time_slug, "a+") as taf:
                    with open("../updates/toAdd_", "a+") as taf:

                        taf.write(json.dumps(diffNewItemObj_Response) + "\n")

            except Exception as e:
                print(e)
                print("ERROR diff_scrape_item_url could not be saved as toAdd file")

    for line in linesOld:
        print("comparing old line ::: " + line)
        sanLine = line.replace('"', "").replace("'", "").replace("\n", "")
        if sanLine not in linesNew:
            print("ITEM SOLD OR DELETED")
            print("compare to new line ::: " + linesNew[0])
            print("old url not in new ::: " + str(sanLine))

            di_search = _3TradeElasticInstance.search(index=sys.argv[1], body={
                "query": {"match_phrase": {"itemLink": sanLine}}
            })

            if di_search["hits"]["total"]["value"] > 0:
                print("Delete item search match")
                di_doc = di_search["hits"]["hits"][0]
                # with open("../updates/toDelete-" + file_time_slug, "a+") as taf:
                with open("../updates/toDelete_", "a+") as taf:
                    taf.write(json.dumps(di_doc["_source"]) + "\n")


            elif di_search["hits"]["total"]["value"] <= 1:
                print("item not found")

        elif sanLine in linesNew:
            print("found item do nothing")

    print("url scrape compare complete")




