from utility.logger import show 
class PayloadFormatter:

    def convert_cloudapi_payload_to_gupshupone(self,payload_type,cloudapi_payload):
        show("cloudapi_payload_converter")
        converted_payload = {
            "body":cloudapi_payload['text'],
            "button_text":cloudapi_payload['list_button'],
            "list_sections":[
                {
                    "title" : cloudapi_payload['list_button'],
                    "options" : cloudapi_payload['buttons']
                }
            ]

        }
        if(cloudapi_payload['language_buttons']):
            converted_payload["list_sections"].append({
                "title":"Change Language",
                "options" : cloudapi_payload['language_buttons']
        })

        return converted_payload
