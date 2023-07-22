# https://www.tutorialspoint.com/python3/python_dictionary.htm
# https://docs.kraken.com/rest/

import base64
import hashlib
import hmac
import requests
import json
import urllib.parse

from . import version
from .Prepper import Prepper


class KrakenAPI:
    def __init__(self) -> None:
        # public requests
        self.__uri = "https://api.kraken.com"
        self.__api_version = "0"
        self.__session = requests.Session()
        self.__session.headers.update({"User-Agent": version.__designation__ + "/" + version.__version__})
        
        # additions for private requests
        self.__keys_file = "TraderAPIs/Kraken/json/secrets/api_key.json"
        
        
        self.__prepper = Prepper()
        self.__prepper.get_pairs(self.query)
        self.__prepper.get_assets(self.query)
        
    @staticmethod
    def __set_nonce(nonce):
        nonce += 1
        return nonce
        
    def __get_keys(self):
        with open(self.__keys_file, "r") as f:
            keys = json.loads(f.read())
        keys["nonce"] = self.__set_nonce(keys["nonce"])
        with open(self.__keys_file, "w") as f:
            f.write(json.dumps(keys, indent=2))
        return keys
            
    def __get_signature(self, url_path, data):
        keys = self.__get_keys()
        data["nonce"] = keys["nonce"]
        
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(keys["private_key"]), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode(), keys["public_key"], data
        
    def __request(self, data):
        url_path = "/" + self.__api_version + "/" + data[0] + "/" + data[1]
       
        if data[0] == "private":
            signature = self.__get_signature(url_path, data=data[2])
            headers = {
                "API-Key": signature[1],
                "API-Sign": signature[0]
            }
            data = signature[2]
        else:
            headers = {}
            data = data[2]
        url = self.__uri + url_path
        response = self.__session.post(url, data=data, headers=headers)
            
        return response.json() if response.ok else response.raise_for_status()

    # Interface
    def query(self, endpoint="SystemStatus", data=None):
        prepared_data = self.__prepper.prepare_data(endpoint, data)
        return self.__request(prepared_data)
    
    def close(self):
        self.__session.close()
    
        
    
