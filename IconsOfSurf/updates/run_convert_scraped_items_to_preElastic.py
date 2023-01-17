import sys
import json



if __name__ == "__main__":
    all_items = []
    print("Run CONVERT SCRAPED ITEM CALLED")
    with open("scraped_items_") as peof:
        all_items = peof.readlines()

    parsed_obj = {}
    for item in all_items:
        print("parsing hit")

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

        print("st   d ")

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

        parsed_obj["s3ImageTags"] = parsed_obj["cdnImageList"]

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

        with open("preElastic_items", "a+") as fef:
            fef.write(json.dumps(parsed_obj) + "\n")
