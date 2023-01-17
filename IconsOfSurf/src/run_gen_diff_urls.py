import json
import uuid
from elasticsearch import Elasticsearch, exceptions, TransportError, RequestsHttpConnection
import os
import pprint
import time
from datetime import datetime
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from check_elast_status import checkElasticStatus




# from memory_profiler import profile
# fpmem=open('saveDelete_Memory_.log','w+')
# @profile(stream=fpmem)

g_all_boards_maps_list = []
g_allBoardsUrlList = []
#gsel = webdriver.PhantomJS()

chrome_options = Options()
chrome_options.add_argument("--headless")
gsel = webdriver.Chrome(sys.argv[3], options=chrome_options)

def getUrlListForPage(pagesource ):
    pageHtml = pagesource
#    print("full page html ~ " + pageHtml)
    productSplitList = pageHtml.split('class="product-list')[1].split("load-more")[0]
    print("product split text length ::: " + str(len(productSplitList)))

    pDivUrlSplit = productSplitList.split("href=\"")
    print("product split div length ::: " + str(len(pDivUrlSplit)))

    pageUrlList = []
    productLoopDivIndex = 1
    #for productLoopDiv in productSplitList:
    for productLoopDiv in pDivUrlSplit:

        try:
            # print("got board div")
            #bPageUrlSplit = productLoopDiv.split("href=\"")
            #bPageUrl = bPageUrlSplit[1].split("\">")[0]
            
            bPageUrl = productLoopDiv.split("\"")[0]
            print("got board url::: " + str(bPageUrl))

            if bPageUrl == "http://www.iconsofsurf.com/favicon.ico":
                print("favicon continuing")
                continue
            if bPageUrl in g_allBoardsUrlList:
                print("bpage in all urls conituning")
                continue
            else:
                # with open("../data/urls_list_" + filetimeslug , 'a+') as urlf:
                #     for url in urlf.readlines():
                #         if url == bPageUrl:
                #             print("found url already in file skipping")
                #             continue
                    
                #     urlf.write(bPageUrl + "\n")
                #     with open("../data/base_urls_list_" + filetimeslug, "a+") as burlf:
                #         burlf.write(baseurl + "\n")
                pageUrlList.append(bPageUrl)

        except Exception as e:
            print("error in load page loop")
            resDict = {'error': str(e)}
            print(resDict)
        productLoopDivIndex +=1
    return pageUrlList   

def scrape_item_urls():


    # List of map
    # [{"base":<baseurl>, "url":<pageurl>}, ...  ]
    
    scrapedUrl = "Init"
    # pages above max return last page results(very nice)
    # start at 1 or else 0 -> 1 gives same results
    productPageIndex = 1
    # save this and check if same for last page
    pageHTMLstring = "init"
    nextPage = True

    '''
    boardTypeBaseUrls = ["http://www.iconsofsurf.com/surfboards/longboards/?page=",
    "http://www.iconsofsurf.com/surfboards/shortboards/?page=", 
    "http://www.iconsofsurf.com/surfboards/mid-length-boards/?page=",
     "http://www.iconsofsurf.com/surfboards/simmons/?page=",
      "http://www.iconsofsurf.com/surfboards/fish/?page=" 
      ]
    '''
    boardTypeBaseUrls = [
            "https://www.iconsofsurf.com/collections/long-boards",
            "https://www.iconsofsurf.com/collections/shortboards",
            "https://www.iconsofsurf.com/collections/mid-length-boards"
            ]
    getUrlList = []
    lastUrlList = []
    for btUrl in boardTypeBaseUrls:
        nextPage = True
        productPageIndex = 1
        while nextPage == True:
            try:
                time.sleep(4)
                #gsel.get(btUrl + str(productPageIndex))
                gsel.get(btUrl)
                productPageIndex +=1
                print("scraping page with url::: " + btUrl)
                if gsel.page_source == pageHTMLstring:
                    nextPage = False
                    break

                pageHTMLstring = gsel.page_source
                getUrlList = getUrlListForPage(pageHTMLstring)
                
                if getUrlList == lastUrlList:
                    nextPage = False
                    break

                lastUrlList = getUrlList

                for nurl in getUrlList:
                    add_check = True
                    # print("::::::::::::::::::::::::::::::::::::::")
                    # print("newurl list item:: " + str(nurl))

                    for allurl in g_allBoardsUrlList:
                        # print("all list url compare :: " + str(allurl))
                        if nurl.strip().replace(" ", "").replace("\n", "") == allurl.strip().replace(" ", "").replace("\n", ""):
                            add_check = False
                            # print("found url already in list skipping")
                            continue
                    if add_check == True:
                        print("all urls list ::: "  )
                        print(str(g_allBoardsUrlList))
                        sanurl = nurl.replace("\n","").replace('\"',"").replace("\'","").replace('"',"").replace("'","")
                        # print("::::::::::::::::::::::::::::::::::::::")
                        g_allBoardsUrlList.append(sanurl)
                        g_all_boards_maps_list.append({"base":btUrl, "url":sanurl})


            except Exception as e:
                print("error in scrape 2 top level get")
                resDict = {'error': str(e)}
                print(resDict)




if __name__ == "__main__":

    print("init diff url scrape")

    if checkElasticStatus() == False:
        print('ElasticSearch is not running ... ')
        sys.exit(1)


    _3TradeElasticInstance = Elasticsearch()
    file_time_slug = datetime.now().strftime("%m-%d-%Y--%H%M")

    # search for current items instead of holding old url files
    ci_search = _3TradeElasticInstance.search(index=sys.argv[1],body={
        "query":{"match":{"userId":"IconsOfSurf"}}
        }, size = 300)

    cur_url_file = sys.argv[2] + "/cur_urls"
    new_url_file = sys.argv[2] + "/diff_urls"
    new_url_map_update = sys.argv[2] + "/to_update_data"

    with open(cur_url_file, "a+") as cf:
        for hit in ci_search["hits"]["hits"]:
            # print("appending cur url :: " + str(hit["_source"]["itemLink"]))
            cf.write(hit["_source"]["itemLink"].replace("'","").replace('"', "").replace("\n", "") + "\n")

    scrape_item_urls()

    print("scrape item urls complete")

    with open(new_url_map_update, "a+") as nurlf:
        for abi in g_all_boards_maps_list:
            nurlf.write(json.dumps(abi) + "\n")

    # need to check if already added
    #with open("toAdd_urls", "a+") as af:
    #    for aurl in g_allBoardsUrlList:
    #        af.write(aurl.replace("'","").replace('"', "").replace("\n", "") + "\n")

    linesNew = []
    linesOld = []
    lineIdx = 0
    print("Reading old and new url files for diff comparison")
    with open(cur_url_file) as ofile:
        linesOld = ofile.readlines()

    with open(new_url_file) as nfile:
        linesNew = nfile.readlines()

    san_new = []
    for line in linesNew:
        sanline = line.replace("'","").replace('"', "").replace("\n", "")
        if sanline not in san_new:
            san_new.append(sanline)

    linesNew = san_new

    san_old = []
    for urlold in linesOld:
    	san_old.append(urlold.replace("'","").replace('"', "").replace("\n", ""))
    
    linesOld = san_old

    addLines = []
    for line in linesNew:
        print("comparing new line")
        san_line = line.replace("'","").replace('"', "").replace("\n", "")
        if san_line not in linesOld:
            print("new line not in old ::: " + str(line))
            addLines.append(san_line)
            # scrape_and_index_item_url(line, file_time_slug)

    remLines = []
    for line in linesOld:
        print("comparing old line")
        san_line = line.replace("'","").replace('"', "").replace("\n", "")
        if san_line not in linesNew:
            remLines.append(san_line)
            print("old url not in new ::: " + str(line))
            # delete_item_by_url(line, file_time_slug)

    if len(remLines) > 0:
        print("found lines to remove creating to delete file len ~ ")
        print(len(remLines))
        with open( sys.argv[2] + "/toDelete_urls"  , 'a+') as remf:
            for line in remLines:
                remf.write(line + "\n")


            

    if len(addLines) > 0:
        print("found lines to add creating add file len ~ ")
        print(len(addLines))
        with open( sys.argv[2] + "/toAdd_urls" , 'a+') as addf:
            for line in addLines:
                addf.write(line + "\n")


    print("url scrape compare complete")




