from google.cloud import dialogflow_v2 as df
from configs.configurations import PROJECT_ID
from mains.dbmodel import Dbmodel
from utility.sheet import BeautSheet
from utility.logger import logging
from traceback import format_exc
from utility.unicorn import Prana
from datetime import datetime
import pytz
from utility.logger import show
# from utility.wacloud import WaCloudApi
from utility.gupshup import Gupshup
from utility.payload_formatter import PayloadFormatter
import re
from utility.aibt import AIBT
import json

class flow(Prana):
    def __init__(self,session_id) -> None:
        super().__init__()
        self.df_session_client = df.SessionsClient()
        self.PROJECT_ID = PROJECT_ID
        self.rw_lst = []
        
        # dialogflow variables
        self.dfrrp = None
        self.dfintent = None
        self.dfreply = None
        self.custom_reply = None
        
        # custom bot variables define here...
        
    def fetch_reply(self, query, session_id):
        show("=========New Flow Start========")
        self.user_original_query = query
        bot_reply = None
        try:
            self.store_message_logs(session_id,self.user_original_query,bot_reply)
        except Exception as e:
            show(e)
        finally:
            show("=========Flow End========")
            
        return self.dialogflow_operation_new(query, session_id)
        
    
    
    def dialogflow_operation_new(self, query, session_id):
        
        self.number = session_id
        logging.debug(f"Intent:{self.dfintent}")
        try:
            # bot_reply = self.check_intent(self.dfintent,session_id,query,self.dfrrp)
            bot_reply = self.call_intent({"number":session_id,"query":query})
        except Exception as e:
            logging.error(format_exc())
        finally:
            return bot_reply
    
    def check_intent(self,intent,number,query,parameters):
        self.dfintent = intent.lower()
        show(f"Intent:{self.dfintent}")
        bot_reply = None
        if self.dfintent == "welcome":
            user_terms_status = True # check for whether user is new or existing !
            show(f"user terms status :{user_terms_status}")
            if(user_terms_status):
                # OLD USER
                self.main_menu_option = "main menu option" # get actual menu option from unicorn db
                bot_reply = getattr(self, self.dfintent)(number, query, parameters)
                show(f"bot_reply:{bot_reply}")
            else:
                # NEW USER
                bot_reply = self.call_intent({"number":number,"query":"new_user_intent_trigger_query"})
                
        else:
            if(self.dfintent):
                self.main_menu_option = "main menu option" # get actual menu option from unicorn db
                bot_reply = getattr(self, self.dfintent)(number, query, parameters)
            else:
                bot_reply = None
            
            
        try:
            self.custom_reply = bot_reply
            self.store_message_logs(number,self.user_original_query,bot_reply) # store messages into mysql remote db
            if(not self.interactiveReplies(self.dfintent)):
                return bot_reply
            else:
                return None
        except Exception as e:
            show(f"{format_exc()}")
            return None
    
    def welcome(self,number,query,params={}):
        show(f"Welcome query:{query}")
        # self.delete_next_options(number)
        botreply = None
        botreply = "reply message from unicorn db" # get actual reply message from unicorn db
        return botreply
        
    def diseasestypes(self,number,query,parameters:dict={}):
        parameters = dict(parameters)
        show(f"parameters:{parameters}")
        main_menu_option = parameters['main_menu_option']
        self.store_options_of_diseasestypes(self.user_sheet,main_menu_option,number) # to verify option later
        if(main_menu_option):
            self.upsert("sheettracks",number,main_menu_option)
            return self.get_sub_menu(self.user_sheet,main_menu_option)
        else:
            show(f"diseasestypes query:{query}")
            # main_menu_option = self.gv("sheettracks",number)
            main_menu_option = self.main_menu_option
            return self.get_sub_menu(self.user_sheet,main_menu_option)
        
        
    def diseasesinfoways(self,number,query,parameters:dict={}):
        parameters = dict(parameters)
        disease_type_option = parameters['sub_menu_option']
        # main_menu_option = self.gv("sheettracks",number)
        main_menu_option = self.main_menu_option
        self.store_options_of_diseasesinfoways(self.user_sheet,main_menu_option,disease_type_option,number) # to verify option later
        self.upsert("disease_type_option",number,disease_type_option)
        return self.get_disease_ways(self.user_sheet,main_menu_option,disease_type_option)
    
    def waysinfo(self,number,query,parameters:dict={}):
        # reset next_option value to []
        self.upsert("next_options",number,[])
        way_option = int(self.dfrrp['way_option'])
        main_menu_option = self.main_menu_option
        disease_type = int(self.gv("disease_type_option",number))
        return self.get_way_info(self.user_sheet,main_menu_option,disease_type,way_option)
        

    # Back Intents define here
    def back_to_disease_types(self,number,query,parameters:dict={}):
        show(f"self.main_menu_option:{self.main_menu_option}")
        # main_menu_option = self.gv("sheettracks",number)
        return self.call_intent({"message":self.main_menu_option,"number":number})
    
    def back_to_disease_ways(self,number,query,parameters:dict={}):
        main_menu_option = self.main_menu_option
        disease_type_option = int(self.gv('disease_type_option',number))
        return self.call_intent({"message":disease_type_option,"number":number})
    
    def updatelanguage(self,number,query,parameters:dict={}):
        query = str(query).lower()
        show(f"self.user_sheet:{self.user_sheet}")
        language = "hindi"
        self.user_sheet = "PranaHindi"
        if(query == "english"):
            language = "english"
            self.user_sheet = "PranaEnglish"

        self.upsert("language",number,language)
        
        return self.call_intent({"number":number,"query":"menu"})

    def default_fallback_intent(self,number,query,params={}):
        bot_reply  = "default_fallback_intent message reply from unicorn db" # get the actual reply from the unicorn db
        return bot_reply
    
    # Non-Intent Function:
    
    def call_intent(self, myobj):
        session_id = myobj['number']
        query = myobj['query'] if "query" in myobj else myobj['message']
        language_code = "en-USA"
        session_client = df.SessionsClient()
        session = session_client.session_path(self.PROJECT_ID, session_id)
        text_input = df.TextInput(text=str(query), language_code=language_code)
        query_input = df.QueryInput(text=text_input)
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        self.dfrrp = dict(response.query_result.parameters)
        self.dfintent = response.query_result.intent.display_name
        self.dfreply = response.query_result.fulfillment_text
        self.custom_reply = self.dfreply
        
        show(f"This Intent got Hit===>{self.dfintent}")
        # self.intent_management(session_id,self.dfintent)
        return self.check_intent(self.dfintent,session_id,query,self.dfrrp)
        
    def idGenerator(self):
        cdate = datetime.now(pytz.timezone(self.MYTIMEZONE))
        id = str(int(cdate.timestamp() * 1000))
        return id,cdate

    def getDateTimeNow(self):
        cdate = datetime.now(pytz.timezone(self.MYTIMEZONE))
        return cdate
    
    def intent_management(self, number, intent):
        avoidIntents = ["Default_Fallback_Intent","Default Fallback Intent"]
        preintent = ""
        if intent not in avoidIntents:
            obj = self.check_key(number, "curintent")
            if obj['status']:
                curintent = obj['value']
                if curintent != intent:
                    preintent = curintent
            else:
                self.createFirstkv(number, "curintent", intent)
            self.doMassUp(number,{"preintent":preintent,"curintent": intent})       
    
    def checkUserExist(self,number):
        status = self.check_key(number,'userExist')
        if status['status']:
            return status['value']
        return False

    def togoback(self,number,query):
        print("@@@@@@@ gotoback intent")
        return self.justgoBack(number)

    def store_message_logs(self,number,user_msg,bot_reply):

        show("STORE MESSAGE LOGS")
        dbm = Dbmodel()
        dbm.store_message(number,user_msg,bot_reply)

         