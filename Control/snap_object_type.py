import json
import sys






def type_check_surftrade_item():
	item_type_map= {
	"cdnImageList":"List"
	}


	sobjs = []
	with open(sys.argv[1]) as sotf:
		sobjs = sotf.readlines()


		print("test file objects length")
		print(len(sobjs))

		for item in sobjs:
			print("json decode item obj length")
			print(len(json.loads(item.replace("\n", ""))))

			conv_item = json.loads(item)

			for k ,v in json.loads(item).items():
				print("item k " + str(k))
				print("item v") 
				print(v)

				if k == "cdnImageList" and isinstance(v, list):
					print("got list cdn")
					continue
				elif k == "cdnImageList" and isinstance(v, list) == False:
					print("got str cdn image list")
					try:
						imenc = json.loads(v)
						conv_item["cdnImageList"] = imenc
						continue
					except:
						print("Error converting cdn to list")
						conv_item["cdnImageList"] = []
						return
				

				if k == "userId" and isinstance(v, str):
					print("got str id")
					continue
				elif k == "userId" and isinstance(v, str) == False:
					print("userid type ::: ")
					print(str(type(v)))
					print("malformed field  userid conversion incomplete")
					return

				if k == "cityString" and isinstance(v, str):
					print("got str city string")
					continue
				elif k == "cityString" and isinstance(v, str) == False:
					print("malformed field citystring conversion incomplete")
					return

				if k == "keywords" and isinstance(v, str):
					print("got str keywords")
					continue
				elif k == "keywords" and isinstance(v, str) == False:
					print("got list keywords")
					try:
						lenc = json.dumps(v)
						conv_item["keywords"] = lenc
						continue
					except:
						print("error converting keywords to string")
						conv_item["keywords"] = "[]"
						return
				
				if k == "boardType" and isinstance(v, str):
					print("got str boardtype")
					continue
				
				if k == "title" and isinstance(v, str):
					print("got str title")
					continue
			
				if k == "timeStamp" and isinstance(v, str):
					print("got str timeStamp")
					continue
				
				if k == "localImageUUIDList":
					if isinstance(v, str):
						print("got str localImageUUIDList")
						continue
					elif isinstance(v,str) == False:
						try:
							enclist = json.dumps(v)
							conv_item["localImageUUIDList"] = enclist
						except:
							print("could not convert uuid to string")
							return
				
				if k == "finBrand":
					if isinstance(v, str):
						print("got str finBrand")
						continue
					else:
						print("field malformed")
						return
				
				if k == "itemUUID":
					if isinstance(v, str):
						print("got str itemuuid")
						continue
					else:
						print("field malformed")
						return
				
				if k == "latitude":
					if isinstance(v, str):
						print("got str latitude")
						try:
							print("float latitude")
							floatlat = float(v)
							print(str(floatlat))
							conv_item["latitude"] = str(floatlat)
						except Exception as e:
							print(e)
							print("Error parsing latitude for float")
							return

					if isinstance(v, str) == False:
						try:
							strlat = str(float(v))
							conv_item["latitude"] = strlat
						except:
							print("Error parsing latitude")
							return
				

				if k == "longitude":
					if isinstance(v, str):
						print("got str longitude")
						try:
							floatlong = float(v)
							conv_item["longitude"] = str(floatlong)
						except:
							print("Error parsing longitude for float")
							return
					if isinstance(v, str) == False:
						try:
							strlat = str(float(v))
							conv_item["longitude"] = strlat
						except:
							print("Error parsing longitude")
							return
				
				if k == "price":
					if isinstance(v, str):
						print("got str price")
						try:
							floatprice = float(v)
							conv_item["price"] = str(floatprice)
						except:
							print("Error parsing price for float")
							return
					if isinstance(v, str) == False:
						print("got not str price")
						try:
							strprice = str(float(v))
							conv_item["price"] = str(floatprice)
						except:
							print("Error parsing not str price for float")
							return
				

				if k == "dimensionMap":
					if isinstance(v, str):
						print("got str dim map")
					elif k == "dimensionMap" and isinstance(v, str) == False:
						print("got not str dimmap")
						try:
							getfield = v["lengthInches"]
							conv_item["dimensionMap"] = json.dumps(v) 
						except:
							print("Error malformed dim map")
							return
					

				if k == "brandShaper":
					if isinstance(v, str):
						print("got str brandshaper")
					else:
						print(" Error malformed brandshaper")
						return

				

				if k == "profilePic" and isinstance(v, bool):
					print("got bool profilePic")
				

				if k == "condition":
					if isinstance(v, int):
						print("got int condition")
					elif k == "condition" and isinstance(v, int) == False:
						try:
							convcondition = int(v)
							conv_item["condition"] = convcondition 
						except:
							print("Error malformed condition")
							return
				
				if k == "finSetup" and isinstance(v, str):
					print("got str finSetup")
				
				if k == "stdPrice":
					if isinstance(v, float):
						print("float price found")
						continue
					elif isinstance(v,float) == False:
						try:
							fp = float(v)
							conv_item["stdPrice"] = fp
						except:
							print("could not get float stdPrice")
							return

				if k == "stdLength":
					if isinstance(v, float):
						print("float length found")
						continue
					elif isinstance(v,float) == False:
						try:
							flength = float(v)
							conv_item["stdLength"] = flength
						except:
							print("could not get float stdLength")
							return

				if k == "stdWidth":
					if isinstance(v, float):
						print("float width found")
						continue
					elif isinstance(v,float) == False:
						try:
							fvol = float(v)
							conv_item["stdWidth"] = fvol
						except:
							print("could not get float stdWidth")
							return
				if k == "stdThick":
					if isinstance(v, float):
						print("float thick found")
						continue
					elif isinstance(v,float) == False:
						try:
							fthick = float(v)
							conv_item["stdThick"] = fthick
						except:
							print("could not get float stdThick")
							return

				if k == "stdVol":
					if isinstance(v, float):
						print("float vol found")
						continue
					elif isinstance(v,float) == False:
						try:
							fvol = float(v)
							conv_item["stdVol"] = fvol
						except:
							print("could not get float stdVol")
							return

				if k == "userUUID" and isinstance(v, str):
					print("got str user uuid")
				

				if k == "dimensionMap":
					try:
						dims = json.loads(v)

						print("loaded dims obj")

						print(str(dims["thicknessInches"]))

					except:
						print("could not parse dimension map")
						return





if __name__ == "__main__":
	print("Init type check")
	type_check_surftrade_item()
	print("type check done")


	




				# print("item v type " + str(type(v)))


