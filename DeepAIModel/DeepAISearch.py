import requests
import json

def SearchData(searchText):
    r = requests.post("https://api.deepai.org/api/text2img",
                      data={ 'text':searchText },
                      headers={'api-key':'d36cd335-d0a9-4cc2-a82b-f6c59cffcc65'})
    r_Data = r.json()
    return r_Data