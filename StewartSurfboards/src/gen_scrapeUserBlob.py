import json
import uuid
from elasticsearch import Elasticsearch, exceptions, TransportError, RequestsHttpConnection
import os
import pprint
import time
from datetime import datetime
import sys




# positional params:
	# 1) index name
	# 2)  username


if __name__ == "__main__":

	print("init generate scrapeuser blob")

	esearch = Elasticsearch()
	useritem_search = esearch.search(index=sys.argv[1], body=
		{
		"query":{"match":{"userId":sys.argv[2]}}
		}, 
		size= 500
		)

	if useritem_search["hits"]["total"]["value"]> 0:
		print("hits found")

		all_user_items = []
		for hit in useritem_search["hits"]["hits"]:

			hit_source = hit["_source"]
			all_user_items.append(hit_source)


		file_time_slug = datetime.now().strftime("%m-%d-%Y--%H%M")
		with open("scrapeUserBlobGen_"+ file_time_slug, "a+") as blobf:
			for item in all_user_items:
				blobf.write(json.dumps(hit) + "\n")



	else:
		print("something went wrong, no items found for user")

	print("gen blob done")