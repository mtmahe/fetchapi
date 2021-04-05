import json

with open('/etc/fetchapi_config.json') as config_file:
    config = json.load(config_file)

class Config:
    IEX_KEY = config.get('iex_key')
    CM_KEY = config.get('cm_key')
