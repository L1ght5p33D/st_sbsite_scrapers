from elasticsearch import Elasticsearch

es = Elasticsearch()

it_search = es.search(index="st_items_k2t2m1",doc_type="_doc",body={"query":{"match":{"userId":"IconsOfSurf"}}}, size=1000)

for it in it_search["hits"]["hits"]:
	print("updating item")
	it_up = es.update(index="st_items_k2t2m1", doc_type="_doc", id=it["_id"],  body= {"doc":{"stdPrice": float(it["_source"]["price"])}})

