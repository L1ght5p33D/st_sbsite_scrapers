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
driver = webdriver.Chrome(executable_path= sys.argv[2], options= chrome_options)




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
                            
                with open( sys.argv[1]+ "/url_out", "a+") as of:
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
    page_txt = driver.page_source
    # print(page_txt)
    # with open(test_html_fname, "a+") as htmlf:
    # 	htmlf.write(page_txt)

    get_item_urls(page_txt)
    driver.quit()

