#!/bin/bash


cleanup() {
    rv=$?
    rm -rf "$tmpdir"
    exit $rv
}

tmpdir="$(mktemp)"
trap "cleanup" INT TERM EXIT


# cd /Users/drix/SurfTrade_Content_Root/httpScrapers/scrapeEnv/bin
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/new_scrape_ENV_3/scrap3/bin

source ./activate
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/StewartSurfboards/src

echo '~~~ Stewart Scrape ~~~'
echo ' ::: '
# The script name
# echo '$0' = $0
# echo 'Args'
# Full or Diff 
# echo 'Full scrape or Diff scrape'
# echo '$1 = ' $1
# Index or not index
# echo 'Index or not index ::: '
# echo '$2 = ' $2
# Index or not index
# echo 'Index name ::: '
# echo '$3 = ' $3

date_string=$(date '+%Y-%m-%d')
time_string=$(date '+%Y%m%d-%H%M')

if [[ "$1" == 0 ]] ; then
    echo 'Specify Parameters'
    exit 1
fi

if [[ "$1" == "Full" ]] ; then
    echo 'Full Scrape'

    saveScrapeObjPath="../data/old_scrape_objects/oldOBJS_"
    saveUrlsPath="../data/old_scrape_objects/oldURLS_"
    savePreElasticObjectsPath="../data/old_scrape_objects/oldPREELASTIC_"

    extenForFile="_.txt"

    mv ../data/full_scrape_data.txt ${saveScrapeObjPath}${date_string}${extenForFile}
    mv ../data/stewartItemUrls.txt ${saveUrlsPath}${date_string}${extenForFile}
    mv ../data/preElasticObjects.txt ${savePreElasticObjectsPath}${date_string}${extenForFile}

    scrapy runspider ssProductPageScrapeUrls.py
	echo 'Crawl Done'

	python ssItemPageScrape.py
	python ss_object_parse_and_save.py

	if [[ "$2" == "Index" ]] ; then
    echo 'Indexing'
    python indexStewartObjFile.py $3
    exit 1

	fi
fi


if [[ "$1" ==  "Diff" ]] ; then
    echo 'Diff Scrape'
    touch ../data/cur_urls.txt
    touch ../data/diff_urls.txt
    # Calls parse_toAdd_for_preElastic which creates /data/diff_preElastic_objects.txt"
    python diff_url_scrape.py $3 $2
    echo 'Diff Scrape complete '    
    #the urls from current items in elastic for user

    
        

    mv ../data/cur_urls.txt ../data/old_scrape_objects/user_cur_items/cur_urls_${time_string}
    cp ../data/diff_urls.txt ../updates/diff_urls
    mv ../data/diff_urls.txt ../data/old_scrape_objects/diff_urls_${time_string}

    echo 'Files moved start parse elastic'
    # creates diff_preElastic_objects.txt

    python parse_toAdd_for_preElastic.py
    
    if [[ "$2" == "Index" ]] ; then
    echo 'Indexing'


    python index_preElastic_objects.py $3 "../data/diff_preElastic_objects.txt"

    echo 'Indexing complete'
    fi

    echo 'init Steawart cleanup'
    cp ../data/diff_preElastic_objects.txt ../updates/_diff_gen_formatted_items_
    mv ../data/diff_preElastic_objects.txt ../data/preElasticBackup/archive/diff_items_${time_string}.txt
    touch ../data/diff_preElastic_objects.txt

    cp ../data/toAdd* ../updates/
    cp ../data/toDelete* ../updates/


    echo 'Cleanup complete'
fi
