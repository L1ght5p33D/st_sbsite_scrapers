#!/bin/bash


cleanup() {
    rv=$?
    rm -rf "$tmpdir"
    exit $rv
}

tmpdir="$(mktemp)"
trap "cleanup" INT TERM EXIT
# Do things...
echo 'error exiting'

#cd /Users/drix/projects/surftradeETC/httpScrapers/scrapeEnv/bin
# cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/Auto_Scrape_Env/bin
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/new_scrape_ENV_3/scrap3/bin
source ./activate

#cd /Users/drix/projects/surftradeETC/httpScrapers/auto_scrape_scripts/UsedSurf/src
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/UsedSurf/src

echo '~~~ Used Surf Scrape ~~~'
echo ' ::: '
echo '$0' = $0
echo 'Args'
# Full or Diff 
echo 'Full scrape or Diff scrape'
echo '$1 = ' $1
# Index or <not Index>
echo 'Index or NOIndex ::: '
echo '$2 = ' $2
# Index name for surftrade items
echo 'Index name ::: '
echo '$3 = ' $3

# exit 1
date_string=$(date '+%Y-%m-%d')

if [[ "$1" == 0 ]] ; then
    echo 'Specify Parameters'
    exit 1
fi

if [[ "$1" == "Full" ]] ; then
    echo 'Full Scrape'
fi

if [[ "$1" ==  "Diff" ]] ; then
    echo 'Diff Scrape'

    mv ../updates/toAdd_ ../updates/oldAddAndDeletes/
    mv ../updates/toDelete_ ../updates/oldAddAndDeletes/
    touch ../updates/toAdd_
    touch ../updates/toDelete_
    python diff_scrape.py $3


    mv ../data/last_urls.txt ../data/ALL_scraped_urls_backup/last_urls_archive$(date +'%m-%d-%H%M').txt
    mv ../data/diff_urls.txt ../data/last_urls.txt
    touch ../data/diff_urls.txt

fi

if [[ "$2" ==  "Index" ]] ; then
    echo 'Indexing'
    cd ../updates
    python apply_update_file.py $3 toAdd_
    python apply_update_file.py $3 toDelete_
    echo 'Index complete'
fi


