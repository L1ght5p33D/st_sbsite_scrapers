#!/bin/bash


cleanup() {
    rv=$?
    exit $rv
}

set -e

trap "cleanup" INT TERM EXIT

source ../Control/scrape_config.sh


cd $scrape_dir/env_scrape/bin
source ./activate
cd $scrape_dir/IconsOfSurf


data_dir=/home/si/os_projects/SurfTrader/1_serve_surftrader/SCRAPE/Surftrade_Scrapers/auto_scrape_scripts/TheBoardSource/data

echo ' ~ The Board Source Scrape ~'
echo 'Args ::: '
echo '$0' = $0
echo 'Index name ::: '
echo '$1 = ' $1

date_string=$(date '+%Y-%m-%d')
time_string=$(date '+%Y%m%d-%H%M')

if [ -f "data/cur_urls" ]; then
        mv data/cur_urls data/archive/cur_url_${time_string}
fi

# list of base url and product url for board type data
if [ -f "data/to_update_data" ]; then
        mv data/to_update_data data/archive/update_data_${time_string}
fi
if [ -f "data/scraped_items" ]; then
        mv data/scraped_items data/archive/scraped_items_${time_string}
fi
if [ -f "data/preElastic_items" ]; then
        mv data/preElastic_items data/archive/pre_elastic_${time_string}
fi
if [ -f "data/diff_urls" ]; then
        mv data/diff_urls data/archive/diff_urls_${time_string}
fi

# Current Urls are generated from elasticsearch, makes it simpler

if ls data/toAdd* > /dev/null 2>&1; then
        mv $(ls data/toAdd*) data/archive/to_add_${time_string}
fi
if ls data/toDelete* > /dev/null 2>&1; then
        mv $(ls data/toDelete*) data/archive/to_delete_${time_string}
fi


# Gets board info page urls from list pages
    python src/run_gen_diff_urls.py $1 $data_dir $webdriver_path

    echo " Call run_get_updates.py ............"
    # run_get_updates.py calls product_page_url_scrape.py and creates scraped_items file
    python src/run_scrape_items.py $1 $data_dir $webdriver_path

    echo "Apply update complete continue run convert"
    # creates preElastic_items
    python src/run_convert_scraped_items_to_preElastic.py $data_dir

    echo ' Run convert complete finish run index'
    if [[ $1 == "Index" ]]; then
      python src/run_index_preElastic.py $1 $data_dir
    fi

