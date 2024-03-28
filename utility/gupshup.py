# coding=utf-8
import json
import requests
import datetime
from utility.logger import show
from configs.configurations import API_URL,SENDER,SOURCE_NAME

class Gupshup():

    def __init__(self):
        self.base_url = API_URL
        self.sender = SENDER
        self.source = SOURCE_NAME


    def call_gupshup_api(self,payload:dict,route:str):
        _creds = {
            "channel" : "whatsapp",
            "source" : self.sender,
            "src.name" : self.source,
            "disablePreview":True
        }
        payload.update(_creds)
        url = f"{self.base_url}{route}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': 'i9jolayxqq25qikjtrfwqp7xk18ilij0'
        }
        answer = requests.post(url, data = payload, headers=headers)
        if answer.headers.get('content-type') is not None:
            return answer.json()

    def send_text_message(self,text,to):
        message_payload = json.dumps({
            "type": "text",
            "text": text[0:4096]
        })
        data = {"destination" : to,"message" : message_payload}
        status = self.call_gupshup_api(data,'/msg')
        return status

    def send_button_message(self,body_text,button_options,to):
        button_list = []

        # button_options :: array[]
        for button in button_options:
            button = button[0:20]
            button_list.append({
                    "type": "text",
                    "title": button,
                    "postbackText": button
            })
        json_data = {
            "type": "quick_reply",
            "content": {
                "type": "text",
                "text": body_text[0:1024]
            },
            "options": button_list
        }
        message_payload = json.dumps(json_data)
        data = {"destination" : to,"message" : message_payload}
        status = self.call_gupshup_api(data,'/msg')
        return status

    def send_list_message(self,list_data,to):
        list_options = []

        show(list_data)

        # list_data["list_sections"] => array_of_object[{}]
        for list_section in list_data["list_sections"]:
            section_data = {"title":list_section['title'][0:24],"options": []}

            # list_section['options'] => array[]
            for option in list_section['options']:
                section_data['options'].append(
                    {
                        "title": option[0:24]
                    }
                )
            list_options.append(section_data)
            section_data = {}

        json_data = {
            "type": "list",
            "title": list_data.get('header',"")[0:60],
            "body": list_data["body"][0:1024],
            "globalButtons": [
                {
                    "type": "text",
                    "title": list_data["button_text"][0:20],
                }
            ],
            "items": list_options
        }
        message_payload = json.dumps(json_data)
        data = {"destination" : to,"message" : message_payload}
        status = self.call_gupshup_api(data,'/msg')
        return status

    def extract_user_message(self,payload)->dict:
        user_data = {"from":0,"message":""}
        try:
            if(payload.get("type",None) == "message"):
                inner_payload = payload['payload']
                from_number = inner_payload['source']
                msg_type = inner_payload['type']
                msg_text = ""
                if(msg_type in ["button_reply","list_reply"]):
                    msg_text = inner_payload['payload']['title']
                else:
                    msg_text = inner_payload['payload'][msg_type]
                
                user_data = {"from":from_number,"message":msg_text}
        except:
            pass
        return user_data













    # Important !!
    ''' 
        send_list_message(list_data) :: 
        list_data = {
            "header":"",
            "body":"",
            "button_text":"",
            "list_sections":[
                {
                    "title" : "",
                    "options" : [1,2,3]
                }
            ]

        }
    '''