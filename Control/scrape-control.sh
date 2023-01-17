#!/bin/bash


cleanup() {
    rv=$?
    exit $rv
}


trap "cleanup" INT TERM EXIT


# Script name
echo '$0' = $0
echo 'Args'
# Index name
echo 'Index name ::: '
echo 'Arg $1 Elastic Index Name = ' $1

date_string=$(date '+%Y-%m-%d')
time_string=$(date '+%Y%m%d-%H%M')

stItemIndex=$1
scrapeclients=("StewartSurfboards" "UsedSurfSC" "IconsOfSurf" "TheBoardSource")

source ./scrape_config.sh

for client in "${scrapeclients[@]}"; do


    if [[ $client == "StewartSurfboards" ]] ; then
        echo '~ Stewart Surfboards ~'
        
        cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/StewartSurfboards

        ./StewartSurfboardsScrape.sh Diff Index $stItemIndex
    fi



    if [[ $client == "UsedSurfSC" ]] ; then
        echo '~ UsedSurfSC ~'

        cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/UsedSurf
        # to add files generated
        ./UsedSurfSC_Scrape.sh Diff Index $stItemIndex
        cd /Users/drix/projects/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts/UsedSurf/updates

        
        # python ./apply_updates_file.py toAdd_ 
	   # python ./apply_updates_file.py toDelete_
        echo '~ UsedSurfSC scrape complete'

    fi


    if [[ $client == "IconsOfSurf" ]] ; then
        echo '~ Icons Scrape ~'
    
	cd $scrape_dir/IconsOfSurf/src
	./IconsScrape.sh Index $stItemIndex    
    fi

    

done


mv scrapeUserBlobGen* ./old_blobs/
cd /Users/drix/SurfTrade_Content_Root/httpScrapers/auto_scrape_scripts
python3 gen_scrapeUserBlob.py $stItemIndex StewartSurfboards
python3 gen_scrapeUserBlob.py $stItemIndex UsedSurfSC
python3 gen_scrapeUserBlob.py $stItemIndex IconsOfSurf

echo 'Scrape Blob Generation complete'

