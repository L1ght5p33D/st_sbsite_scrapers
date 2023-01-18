#!/bin/bash


cleanup() {
    rv=$?
    exit $rv
}

trap "cleanup" INT TERM EXIT

set -e


source ../Control/scrape_config.sh

cd ../env_scrape/bin
source ./activate
cd ../../StewartSurfboards

data_dir=$scrape_dir/StewartSurfboards/data

echo '~~~ Stewart Scrape ~~~'
echo ' ::: '
# Script name
# echo '$0' = $0
# echo 'Args'
# Index or not index
# echo '$1 = ' $1
# echo 'Index name ::: '
# echo '$2 = ' $2

date_string=$(date '+%Y-%m-%d')
time_string=$(date '+%Y%m%d-%H%M')

if [[ "$1" == 0 ]] ; then
    echo 'Specify Parameters for Stewart sh'
    exit 1
fi

if [ -f "data/cur_urls" ]; then
    mv data/cur_urls data/scrape_archive/cur_urls_${time_string}
fi

if [ -f "data/diff_urls" ]; then
    mv data/diff_urls data/scrape_archive/diff_urls_${time_string}
fi

if [ -f "data/scraped_items" ]; then
    mv data/scraped_items data/scrape_archive/scraped_items_${time_string}
fi

if [ -f "data/preElastic_objects" ]; then
    mv data/preElastic_objects data/scrape_archive/preElasticObjects_${time_string}
fi

if ls data/toAdd* > /dev/null 2>&1; then
    mv data/toAdd* data/scrape_archive/toAdd_${time_string}
fi

if ls data/toDelete* > /dev/null 2>&1; then    
    mv data/toDelete* data/scrape_archive/toDelete_${time_string}
fi


    touch data/cur_urls
    touch data/diff_urls
    touch data/preElastic_objects

    # Calls parse_toAdd_for_preElastic which creates /data/preElastic_objects"
    python src/ss_url_scrape.py $2 $data_dir $webdriver_path
    echo ' stewart scrape url scrape complete '

    python src/ss_item_scrape.py $webdriver_path
    echo 'Stewart Surf Url Scrape complete '    
   
    python  parse_scraped_for_preElastic.py  
    echo ' parse scraped for pre elastic complete '
    
    if [[ "$2" == "Index" ]] ; then

    python src/index_preElastic_objects.py $2

    echo 'Indexing complete'
   fi
