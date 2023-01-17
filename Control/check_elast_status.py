import json
import requests

def checkElasticStatus():
    print("checking elastic status")
    port_9200_res = requests.get("http://localhost:9200")
    try:
        json.loads(port_9200_res.text)
        if "You Know, for Search" in port_9200_res.text:
            print("ELASTIC RUNNING")
            return True
    except:
        print("couldnt load json")
        return False
    return False

