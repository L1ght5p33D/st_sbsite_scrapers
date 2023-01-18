import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from datetime import datetime
import requests
import sys
import os


test_html_fname = "card_page_get_html_4noscroll.txt"

card_page = "https://www.secondhandboards.com/us-surfboards"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path= sys.argv[3], options= chrome_options)


g_allBoardsUrlList = []

def get_item_urls(url_page_text):
    t = url_page_text
    
    s1 = t.split('class="resultscontainer')

    sref = s1[1].split("href=")


    got_urls = []
    for hrs in sref:
        if "#" in hrs[0:10]:
            continue

        durl = hrs.split("=")[0]

        surl = durl.replace("data-original-title", "").replace("title","")

        print("got san url ::: ")
        print(surl)

        if "https://www.secondhandboards.com" in surl:
            # Getting doubles for some reason
            if surl not in got_urls:
                got_urls.append(surl)
                g_allBoardsUrlList.append(surl)

                with open( sys.argv[2]+ "/url_out", "a+") as of:
                    of.write(surl + "\n") 


if __name__ == "__main__":
    print("Second hand scrape init")

    driver.get(card_page)
    time.sleep(5)
    print("card page get done")
    # just have to scroll once to load all boards
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(5)
    print("execute script complete")
    all_boards_page_txt = driver.page_source
    # print(page_txt)
    # with open(test_html_fname, "a+") as htmlf:
    # 	htmlf.write(page_txt)

    # Get current urls from db
    ci_search = _3TradeElasticInstance.search(index=sys.argv[1],body={
        "query":{"match":{"userId":"SecondhandBoards"}}
        }, size = 300)

    cur_url_file = sys.argv[2] + "/cur_urls"
    new_url_file = sys.argv[2] + "/url_out"

    with open(cur_url_file, "a+") as cf:
        for hit in ci_search["hits"]["hits"]:
            # print("appending cur url :: " + str(hit["_source"]["itemLink"]))
            cf.write(hit["_source"]["itemLink"].replace("'","").replace('"', "").replace("\n", "") + "\n")
 
    
    get_item_urls(all_boards_page_txt)
    
    linesNew = []
    linesOld = []
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

    
    driver.quit()

