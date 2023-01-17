from opencage.geocoder import OpenCageGeocode
from pprint import pprint
import mt_obj

key = os.environ['GOOGLE_API_KEY_STSCRAPE_GEOCODE']
# geocoder = OpenCageGeocode(key)

# results = geocoder.reverse_geocode(44.8303087, -0.5761911)
# pprint(results)

# query = u'Deerfield Beach, Florida'
# results = geocoder.geocode(query)

# pprint(results)

print("mtob len")
print(str(len(mt_obj.mt_obj)))

mo = mt_obj.mt_obj

for m in mo:
	print("found mo")
	print(m)

	if 'annotations' in m:
		print("got ann")
	if "geometry" in m:
		print("gem")
		print(m['geometry'])
		# if 'DMS' in m['annotations']:
		# 	print("dms")
		# 	if 'lat' in m['annotations']['DMS']:
				

				
