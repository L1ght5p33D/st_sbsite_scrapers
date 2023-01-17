#!/bin/bash


cleanup() {
    rv=$?
    rm -rf "$tmpdir"
    exit $rv
}

tmpdir="$(mktemp)"
trap "cleanup" INT TERM EXIT


# cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/Auto_Scrape_Env/bin
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/new_scrape_ENV_3/scrap3/bin
source ./activate
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/IconsOfSurf/updates


#ONLY 1 ARGUMENT

echo ' ~ Icons of Surf Scrape ~'
# The script name
echo '$0' = $0
echo 'Args'
# Index name
echo 'Index name ::: '
echo '$1 = ' $1

date_string=$(date '+%Y-%m-%d')
time_string=$(date '+%Y%m%d-%H%M')

mv ./cur_urls ./archive/cur_url_${time_string}
mv ./to_update_data ./archive/update_data_${time_string}
mv ./scraped_items_ ./archive/scraped_items_${time_string}
mv ./preElastic_items ./archive/pre_elastic_${time_string}
mv ./diff_urls ./archive/diff_urls_${time_string}

cp ./toAdd* ./archive/to_add_${time_string}
cp ./toDelete* ./archive/to_delete_${time_string}
rm ./toAdd*
rm ./toDelete*

touch toDelete_urls_
touch to_update_data
touch cur_urls
touch diff_urls


	python run_gen_diff_urls.py $1

    echo "Pre elastic exist::: Run run_apply_updats.py ............"
# run_apply_updates.py is not named right, it only creates the scraped_items_ and toDelete_urls_ files that get used
    python run_apply_updates.py $1

    echo "Apply update complete continue run convert"
    # creates preElastic_items
    python run_convert_scraped_items_to_preElastic.py

    echo ' Run convert complete finish run index'
    python run_index_preElastic.py $1

