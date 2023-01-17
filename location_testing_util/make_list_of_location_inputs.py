import json
dob = []
with open("scrape_run_data_dump","r") as df:

	dob = df.readlines()


loc_list = []
for it in dob:
	loc_list.append(json.loads(it)["cityString"])


with open("location_data_list","a+") as ofile:
	for ln in loc_list:
		ofile.write(ln + "\n")



