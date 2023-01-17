import json
import sys
import requests

if __name__ == "__main__":
    print("checking elastic status")
    port_9200_res = requests.get("http://localhost:9200")
    # print("prot res :: ")
    # print(str(port_9200_res.text))
    try:
        json.loads(port_9200_res.text)
        if "You Know, for Search" in port_9200_res.text:
            print("ELASTIC RUNNING")
    except:
        print("couldnt load json")
    print("done")
