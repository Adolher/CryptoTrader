import json
import time
import os

from .templates import templates


class Prepper:
    def __init__(self):
        self.pairs_file = "TraderAPIs/Kraken/json/pairs.json"
        self.assets_file = "TraderAPIs/Kraken/json/assets.json"
        self.templates = templates
        
    def get_pairs(self, query_pairs=None):
        try:
            with open(self.pairs_file, "r") as t:
                pairs = json.loads(t.read())
                if int(time.time()) - pairs["timestamp"] > 86400:
                    t.close()
                    os.remove(self.pairs_file)
                    self.get_pairs(query_pairs)
                else:
                    pairs = list(pairs["pair"])
        except FileNotFoundError:
            with open(self.pairs_file, "w") as t:
                pairs = query_pairs(endpoint="AssetPairs")
                pairs = list(pairs["result"].keys())
                t.write(json.dumps({"timestamp": int(time.time()) ,"pair":pairs}, indent=2))
                
        for template_keys in self.templates.keys():
            if "pair" in self.templates[template_keys].keys():
                self.templates[template_keys].update({"pair": pairs})
    
    def get_assets(self, query_assets=None):
        try:
            with open(self.assets_file, "r") as t:
                assets = json.loads(t.read())
                if int(time.time()) - assets["timestamp"] > 86400:
                    t.close()
                    os.remove(self.assets_file)
                    self.get_assets(query_assets)
                else:
                    assets = list(assets["asset"])
        except FileNotFoundError:
            with open(self.assets_file, "w") as t:
                assets = query_assets(endpoint="Assets")
                assets = list(assets["result"].keys())
                t.write(json.dumps({"timestamp": int(time.time()), "asset":assets}, indent=2))
                
        for template_keys in self.templates.keys():
            if "asset" in self.templates[template_keys].keys():
                self.templates[template_keys].update({"asset": assets})
    
    def prepare_data(self, endpoint, data):
        data = {} if data is None else data
        template = self.templates[endpoint].copy()
        
        # first check if all required parameters are in data
        for required_param in template["required"]:
            if required_param not in data.keys():
                raise Exception                                 # ToDo: handle this Exception
            
        del template["required"]
        scope = template.pop("scope")
        
        # then check if all query-parameters fits to the endpoint
        for param in data.keys():
            if param not in template.keys():
                raise Exception                                 # ToDo: handle this Exception
            else:
                # and check if parameter-values fits to the template-values
                if type(data[param]) is list:
                    for param_value in data[param]:
                        if param_value not in template[param]:
                            raise Exception                     # ToDo: handle this Exception
                    data[param] = ",".join(data[param]) # concatenate list to strings
                elif type(data[param]) is int:
                    if data[param] < template[param][0] or data[param] > template[param][-1]:
                        raise Exception                         # ToDo: handle this Exception
                else:
                    if data[param] not in template[param]:
                            raise Exception                     # ToDo: handle this Exception

        return scope,endpoint,data
