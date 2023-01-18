import json
import datetime
import sys


bt_cap_list = [
'Shortboard',
'Hybrid',
'Fish',
'Step-up',
'Gun',
'Longboard',
'Prone Paddle',
'SUP'
]


rough_items = []
with open(sys.argv[1] + '/scrape_run_data_dump','r') as sf:
	rough_items = sf.readlines()


for item in rough_items:
	print("got rough item :: ")
	# print(item)

	item = json.loads(item)
	if item["s3ImageTags"] == None or len(item["s3ImageTags"]) == 0:
		print("no images skipping")
		continue


	descGet = item["p_description"]

	descSanitize = descGet.replace("<p>", " ")
	descSanitize = descSanitize.replace("</p>", " ")
	descSanitize = descSanitize.replace("<div>", " ")
	descSanitize = descSanitize.replace("</div>", " ")
	descSanitize = descSanitize.replace("<br>", " ")
	descSanitize = descSanitize.replace("<em>", " ")
	descSanitize = descSanitize.replace("</em>", " ")
	descSanitize = descSanitize.replace("<td>", " ")
	descSanitize = descSanitize.replace("</td>", " ")
	descSanitize = descSanitize.replace("<tr>", " ")
	descSanitize = descSanitize.replace("</tr>", " ")
	descSanitize = descSanitize.replace("<tbody>", " ")
	descSanitize = descSanitize.replace("</tbody>", " ")
	descSanitize = descSanitize.replace("<table>", " ")
	descSanitize = descSanitize.replace("</table>", " ")
	descSanitize = descSanitize.replace("&nbsp;", " ")
	descSanitize = descSanitize.replace("&nbsp", " ")
	descSanitize = descSanitize.replace("\n", " ")
	descSanitize = descSanitize.replace('<p class="p1">'," ")
	descSanitize = descSanitize.replace("<strong>", " ")
	descSanitize = descSanitize.replace("</strong>", " ")
	descSanitize = descSanitize.replace("<span>", " ")
	descSanitize = descSanitize.replace("</span>", " ")
	descSanitize = descSanitize.replace('<p class="p2">', " ")
	descSanitize = descSanitize.replace("u201c", " ")
	descSanitize = descSanitize.replace("&amp;", "")
	descSanitize = descSanitize.replace("&amp", "")

	print("new desc :::")
	print(descSanitize)

	item["description"] = descSanitize

	item["itemLink"] = item["itemLink"].replace("\n","").replace('"',"").replace("\\","").replace("'","").replace(" ","")

	if item["conditionText"] == "VeryGood":
		item["condition"] = 100
	if item["conditionText"] == "Good":
		item["condition"] = 80
	if item["conditionText"] == "Fair":
		item["condition"] = 60


	stdvol = 0
	if item["dimensionMap"]["volumeLiters"][0] == "0":
		item["dimensionMap"]["volumeLiters"] = item["dimensionMap"]["volumeLiters"][1:]

	build_dims = {"thicknessInches": " ", "thicknessFracNumer": " ", "lengthFeet": " ", "widthFrac": " ", "widthFracNumer": " ", "thicknessFrac": " ", "thicknessFracDenom": " ", "volumeLiters": " ", "widthFracDenom": " ", "lengthInches": " ", "widthInches": " "}

	dimmap = item["dimensionMap"]

	for k,v in build_dims.items():
		print("check key :: " + str(k))
		if k in dimmap.keys():
			if dimmap[k] != "":
				print("found not null dmmap " + str(dimmap[k]))
				build_dims[k] = dimmap[k]	
			else:
				print("found null str dimmap")
				build_dims[k] = " "
		if v == "":
			build_dims[k] = " "

	item["dimensionMap"] = build_dims
	print("mid ite dim")
	print(build_dims)		

	try:
		print("conv vol")
		print(item["dimensionMap"]["volumeLiters"])
		stdvol = float(item["dimensionMap"]["volumeLiters"])
	except Exception as e:
		print("couldnt float vol")

	item["stdVol"] = stdvol


	item["keywords"] = str(item["keywords"])

	san_tags = []
	for link in item["s3ImageTags"]:
		san_tags.append("https://www.secondhandboards.com/slir/q100/" + link.replace(" ","").replace("\ ", "").replace("\\","").replace("\\ ", "").replace("/boardimages/boardimages/", "/boardimages/"))


	item["s3ImageTags"] = san_tags



	bt_lower_list=[]
	for cap_item in bt_cap_list:
		bt_lower_list.append(cap_item.lower())

	item["boardType"] = " "
	if "boardType" in item:
		if item["boardType"].lower().replace(" ","") in bt_lower_list:
			bt_list_idx = bt_lower_list.index(item["boardType"].lower())
			item["boardType"] = bt_cap_list[bt_list_idx]
		else:
			item["boardType"] = " "

	# "timeStamp" : "2020-05-27 18:38:12",
	# "uploadTime" : 1590629892000
	mns = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
	dstr = item['p_posted']
	day_nums = []

	print("time ")
	print(dstr)

	if dstr[0].isdigit():
		day_nums.append(dstr[0])
	if dstr[1].isdigit():
		day_nums.append(dstr[1])	

	get_date = ""

	if len(day_nums) == 2:
		get_date = str(day_nums[0] ) + str(day_nums[1])
		dstr = dstr[2:]
	else:
		get_date = day_nums[0]
		dstr = dstr[1:]
	print("GET DATE ::: " + get_date)

	mn_str = dstr[0:3]
	get_mn = 0
	get_mn = mns.index(mn_str.lower()) + 1
	print("GET MONTH::: " + str(get_mn))
	get_yr = dstr[-4:]

	ctime  = datetime.datetime(int(get_yr), get_mn , int(get_date))
	print("got c time")
	print( ctime.timestamp() * 1000)
	item["uploadTime"] = ctime.timestamp() * 1000

	item["timeStamp"] = str(ctime)
	
	if item['p_seller'] == 'shop':
		item['sellerClass'] = "commercial"
	else:
		item['sellerClass'] = "private"

	for k,v in item["dimensionMap"].items():
		if v == 0 or v == "0":
			item["dimensionMap"][k] = " "

	item["dimensionMap"] = json.dumps(item["dimensionMap"])

	for k,v in item.items():
		if v == "":
			item[k] = " "

	item["localImageUUIDList"] = json.dumps(item["localImageUUIDList"])
	item["stdVol"] = float(item['stdVol'])
	item["stdLength"] = float(item['stdLength'])
	item["stdWidth"] = float(item['stdWidth'])
	item["stdThick"] = float(item['stdThick'])
	item["condition"] = float(item['condition']) 

	item["description"] = item["p_description"].replace("<br>", "").replace("\\n", "").replace("\\ufffd","")

	with open(sys.argv[1] + "/final_parsed_items","a+") as wf:
		wf.write(json.dumps(item) + "\n")



