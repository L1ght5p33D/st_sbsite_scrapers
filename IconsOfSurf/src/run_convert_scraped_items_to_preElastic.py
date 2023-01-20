import sys
import json


# Only 1arg) data dir
if __name__ == "__main__":
    all_items = []
    print("Run CONVERT SCRAPED ITEM CALLED")
    with open(sys.argv[1] + "/scraped_items","r") as sif:
        all_items = sif.readlines()

    parsed_obj = {}
    for item in all_items:
        if item == "\n":
            continue
        print("parse item ~ " + str(item))

        parsed_obj = json.loads(item.replace("\n", ""))


        if "brand new" in parsed_obj["title"].lower():
            parsed_obj["condition"] = 100.0
        if "almost new" in parsed_obj["title"].lower():
            parsed_obj["condition"] = 80.0


        parsed_obj["description"] = parsed_obj["description"].replace("&nbsp;", "").replace("&nbsp", "")
        dm_map = json.loads(parsed_obj["dimensionMap"])

        length_std = 0.0
        try:
            length_std = float(dm_map["lengthFeet"]) + (float(dm_map["lengthInches"]) / (12.0))
        except:
            print("couldnt parse length to float")

        width_std = 0.0
        try:
            width_std = float(dm_map["widthInches"]) + (
                        float(dm_map["widthFracNumer"]) / float(dm_map["widthFracDenom"]))
        except:
            print("couldnt parse width to float")

        thick_std = 0.0
        try:
            thick_std = float(dm_map["thickInches"]) + (
                        float(dm_map["thicknessFracNumer"]) / float(dm_map["thicknessFracDenom"]))
        except:
            print("couldnt parse thickn to float")

        print("std  dims ~ ")

        print(str(length_std))
        print(str(width_std))
        print(str(thick_std))

        # dont exist yet
        parsed_obj["stdLength"] = length_std
        parsed_obj["stdWidth"] = width_std
        parsed_obj["stdThick"] = thick_std

        # must be double, int throws error
        parsed_obj["condition"] = 100.0
        parsed_obj["latitude"] = float(parsed_obj["latitude"])
        parsed_obj["longitude"] = float(parsed_obj["longitude"])
        
        san_images = []
        for cdn_url in parsed_obj["cdnImageList"]:
            print("parsing cdn url ~" + cdn_url[0:2])
            if cdn_url[0:2] == "//":
                san_images.append("https:" + cdn_url)
            else:
                san_images.append(cdn_url)

        print("adding s3 tags " + str( san_images ))
        parsed_obj["s3ImageTags"] = san_images

        buildDims = {"lengthFeet": "0", "lengthInches": "0",
                     "widthInches": "0", "widthFracNumer": "0",
                     "widthFracDenom": "1", "widthFrac": " ",
                     "thicknessInches": "0", "thicknessFracNumer": "0", "thicknessFracDenom": "1",
                     "thicknessFrac": " ", "volumeLiters": " "}

        try:
            buildDims["lengthFeet"] = str(int(dm_map["lengthFeet"]))
        except:
            print("couldnt convert length")

        try:
            buildDims["lengthInches"] = str(int(dm_map["lengthInches"]))
        except:
            print("couldnt convert length inches")

        try:
            buildDims["widthInches"] = str(int(dm_map["widthInches"]))
        except:
            print("couldnt convert length")

        try:
            buildDims["widthFracNumer"] = int(dm_map["widthFracNumer"])
        except:
            print("couldnt convert width numner")

        try:
            buildDims["widthFracDenom"] = int(dm_map["widthFracDenom"])
        except:
            print("couldnt convert width denom")

        try:
            buildDims["thicknessInches"] = str(int(dm_map["thicknessInches"]))
        except:
            print("couldnt convert thick in")

        try:
            buildDims["thicknessFracNumer"] = int(dm_map["thicknessFracNumer"])
        except:
            print("couldnt convert thick fn")

        try:
            buildDims["thicknessFracDenom"] = int(dm_map["thicknessFracDenom"])
        except:
            print("couldnt convert width numner")

        try:
            buildDims["volumeLiters"] = str(float(dm_map["volumeLiters"]))
        except:
            print("couldnt convert width numner")

        
        try:
            parsed_obj["stdPrice"] = float(parsed_obj["price"])
        except:
            print("couldnt convert price to float")
            parsed_obj["stdPrice"] = 0

        parsed_obj["dimensionMap"] = json.dumps(buildDims)

        print("final item ~ " + str( parsed_obj ))
        
        with open(sys.argv[1] + "/preElastic_items", "a+") as fef:
            fef.write(json.dumps(parsed_obj) + "\n")
