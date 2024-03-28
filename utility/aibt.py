import requests
import json
from configs.configurations import AIBT_SERVER_URL
class AIBT:
    def __init__(self):
        self.url = AIBT_SERVER_URL
    
    def query_db(self,query,user_sheet):
        
        cols = {"PranaEnglish":"pra-qna"}
        url = self.url+"/query"
        payload = json.dumps({
        "query": query,
        "collection": cols.get(user_sheet,"pra-qna-hindi")
        })
        headers = {
        'access_token': 'myfreewilliswhaticare',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer myfreewilliswhaticare'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text