class WaCloudDataExtr:
    def __init__(self):
        pass
    
    def getMessage(self,jsonpayload):
        number = 0
        message = None
        changes_obj = jsonpayload['entry'][0]['changes'][0]
        if(changes_obj['field'] == "messages"):
            message_obj = changes_obj['value'].get('messages',None)
            if(message_obj):
                message_obj = message_obj[0]
                number = message_obj['from']
                if(message_obj['type'] == "text"):
                    message = self.getTextMessage(message_obj)
                else:
                    msg_type = message_obj['type']
                    interactive_type = message_obj[msg_type]['type']
                    message = message_obj[msg_type][interactive_type]['title']
            else:
                return {'number':number,'message':message}
                
        return {'number':number,'message':message}
            
            
    def getTextMessage(self,message_payload):
        return message_payload['text']['body']
        