#!/bin/bash


cleanup() {
    rv=$?
    exit $rv
}

trap "cleanup" INT TERM EXIT

set -e

source ../Control/scrape_config.sh

data_dir=$scrape_dir/SecondhandScrape/data

cd $scrape_dir/env_scrape/bin
source ./activate

cd $scrape_dir/SecondhandScrape



echo ' ~ Second Hand Surf Scrape init  ~'
# The script name
echo '$0' = $0
echo 'Args'
# Index name
echo 'Index name ::: '
echo '$1 = ' $1

date_string=$(date '+%Y-%m-%d')
time_string=$(date '+%Y%m%d-%H%M')


#TODO Add diff  >> need toDelete urls

if [ -f "data/url_out" ];then
	mv data/url_out scrape_archive/url_out${date_string}${time_string}
else
	echo "no url out file"
fi

if [ -f "data/cur_urls" ];then
	mv data/cur_urls scrape_archive/cur_urls_${time_string}
else
	echo "no cur urls file"
fi

if [ -f "data/toAdd_urls" ];then
	mv data/toAdd_urls scrape_archive/toaddurls_${time_string}
else
	echo "no to add urls file"
fi

if [ -f "data/toDelete_urls" ];then
	mv data/toDelete_urls scrape_archive/todeleteurls_${time_string}
else
	echo "no delete urls file"
fi

if [ -f "data/scrape_run_data_dump" ];then
	mv data/scrape_run_data_dump scrape_archive/scrun_datadump_${time_string}
else
	echo "no scrape run data dump file"
fi

if [ -f "data/final_parsed_items" ];then
	mv data/final_parsed_items scrape_archive/fpitems_${time_string}
else
	echo "no final parsed items file"
fi

#python3 src/get_item_urls.py $items_index $data_dir $webdriver_path

#python3 src/get_rough_obj_from_url_list.py $data_dir $webdriver_path

#python3 src/get_san_obj_from_rough.py $data_dir

#python3 src/index_final_obj.py $items_index



