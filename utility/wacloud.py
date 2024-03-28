import json
import requests
from configs.configurations import WA_CLOUD_PHONE_NUMBER_ID,WA_CLOUD_WAAPITOKEN
from utility.logger import show
class WaCloudApi:
    def __init__(self):
        self.url = f"https://graph.facebook.com/v16.0/{WA_CLOUD_PHONE_NUMBER_ID}/messages"
    
    def send_template_with_params(self,template_id,params,to):
        show(f" ==== sending params template with params:{params} =====")
        params_texts = []
        for text in params:
            params_texts.append({
                    "type": "text",
                    "text": f"{text}"
                },)

        payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": f"{to}",
        "type": "template",
        "template": {
        "name": f"{template_id}",
            "language": {
            "code": "en"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": params_texts
                }
            ]
        }
        })
        headers = {
        'Authorization': f'Bearer {WA_CLOUD_WAAPITOKEN}',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        show(f"**********\n{response.text}\n****************")
        
        json_response = response.json()
        return json_response

    def send_template(self,template_id,to):
        show(f"=========== sending template with no params ===========")
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": f"{to}",
        "type": "template",
        "template": {
        "name": template_id,
            "language": {
            "code": "en"
            }
        }
        })
        headers = {
        'Authorization': f'Bearer {WA_CLOUD_WAAPITOKEN}',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        show(f"**********\n{response.text}\n****************")
        
        # json_response = response.json()
        # show(f"wa-cloud response===> {json_response}")
        # return json_response


    def send_message(self,to,text_msg):

        payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": text_msg
        }
        })
        headers = {
            'Authorization':f'Bearer {WA_CLOUD_WAAPITOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        # print("**********\n",response.text,"\n****************")
        
    def send_button_message(self,to,button_payload):
        
        button_list = button_payload['buttons']
        text_msg = button_payload['text'][0:1024]
        
        buttons = []
        for i,btn in enumerate(button_list):
            buttons.append({
                "type": "reply",
                "reply": {
                    "id": i,
                    "title": btn[0:20]
                }
            })
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": text_msg
            },
            "action":{
                "buttons":buttons
            }
        }
        })
        headers = {
            'Authorization':f'Bearer {WA_CLOUD_WAAPITOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        # print("**********\n",response.text,"\n****************")
        show(response.text)
        
    def send_list_message(self,to,button_payload):
        
        list_items = button_payload['buttons']
        text_msg = button_payload['text'][0:1024]
        list_button = button_payload.get('list_button',None)
        language_buttons = button_payload.get('language_buttons',None)
        
        language_options = []
        if(language_buttons):
            for b,lbtn in enumerate(language_buttons):
                language_options.append({
                    "id": b,
                    "title": lbtn[0:24],
                })
        list_options = []
        for i,btn in enumerate(list_items):
            list_options.append({
                "id": i,
                "title": btn[0:24],
                # "description": btn[0:72]
            })
        payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            # "header": {
            #     "type": "text",
            #     "text": "header"
            # },
            "body": {
                "text": text_msg
            },
            # "footer": {
            #     "text": "Lifeel"
            # },
            "action": {
            "button": list_button if list_button else "Select Option",
            "sections": [
                    {
                        "title": list_button,
                        "rows": list_options,
                    },
                    
                ]
            }
        }
        }
        
        if(language_options):
            payload['interactive']["action"]['sections'].append(
                {
                    "title":"Change language",
                    "rows":language_options,
                }
            )
            
        payload = json.dumps(payload)
        
        headers = {
            'Authorization':f'Bearer {WA_CLOUD_WAAPITOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        # print("**********\n",response.text,"\n****************")
        show(response.text)