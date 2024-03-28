# routes.py
from flask import Blueprint,request,jsonify
from utility.logger import logging,show
import json
from utility.unicorn import Unicorn
from traceback import format_exc
from configs.configurations import WA_WEBHOOK_VERIFY_TOKEN,AFTER_CALL_TEMPLATE_NAME
from utility.wacloudDataextr import WaCloudDataExtr
from utility.wacloud import WaCloudApi
from utility.gupshup import Gupshup
from mains.dbmodel import Dbmodel
from mains.flow import flow

# Create a new blueprint
bot = Blueprint('bot_api', __name__)

@bot.route('/status',methods=['GET'])
def index():
    return "HELLO bot !"
  
@bot.route('/test',methods=['GET'])
def testbot():
  try:
    bot = flow()
    message = request.form.get('message')
    number = request.form.get('number')
    data = {
          "number": number,
          "message": message,
          "reply":"Nothing"
      }
    reply = bot.fetch_reply(message, number)
    data['reply'] = reply
  except:
    logging.error(format_exc())
  finally:
    del bot
    return jsonify(data),200
    
@bot.route('/savesheet',methods=['POST'])
def savesheet():
      response= {"status":False,"message":"Sheet not saved ! Please try after some time"}
      try:
        uc = Unicorn()
        tablename = request.json['table_name']
        sheetname = request.json['sheet_name']
        sheetdata = request.json['data']
        show(sheetname)
        status = uc.createG(tablename,sheetname,sheetdata)
        response['status'] = status
        response['message'] = "Saved" if status else "Not Saved"
        show(f"create g status :{status}")
      except:
          logging.error(format_exc())
      finally:
        del uc
        return response
 
 
# whatsapp cloud api webhook 
@bot.route('/wa-cloud-api-webhook',methods=['GET','POST'])
def wa_cloud_api():
      response = None
      if(request.method == "GET"):
        try:
          response = verify_token(request)
        except:
          response = "Ok"
            
      elif(request.method == "POST"):
          response = "Ok"
          try:
              data_extr = WaCloudDataExtr()
              bot = flow()
              waapi = None # to make possible to delete in finally clause
              logging.debug(request.json)
              number_and_message = data_extr.getMessage(request.json)
              number = number_and_message.get('number')
              message = number_and_message.get('message')
              show(f"{number,message}")
              if(number and message):
                  logging.debug(number_and_message)
                  message = number_and_message['message'][0:250]
                  waapi = WaCloudApi()
                  reply = bot.fetch_reply(message,number)
                  waapi.send_message(number,reply)
              
          except:
              logging.debug(number_and_message)
              logging.error(format_exc())
          finally:
            del bot
            del waapi
            
            
      return response
    

@bot.route('/message-logs')
def get_message_logs():
  db = Dbmodel()
  last_id = request.args['last_id']
  show(last_id)
  return db.get_messages(last_id)
  

@bot.route('/official',methods=['GET','POST'])
def get_bot_reply():
  try:
    data = request.json
    # print("Response:",data)
    reply = "*Try again later !*"
    if data['type']=='message':
      message = (data['payload']['payload']['text'])
      number = data['payload']['source']
      name = data['payload']['sender']['name']
      # print("\nMEssage:",message," | Number:",number,"\n")
      reply = dg.fetch_reply(message, number,username=name)
      # print("Reply:\n",reply)
      return reply if reply else ''
    elif('type' in data['payload'] and data['payload']['type'] == "failed"):
        # print("Response:",data)
        destination = data['payload']['destination']
        code = data['payload']['payload']['code']
        reason = data['payload']['payload']['reason']
        if code == 1006 and "not opted in for template message" in reason:
            send.set_user_opt_in(destination)
        elif "not opted" in reason:
            send.set_user_opt_in(destination)
        elif code == 1008:
            send.set_user_opt_in(destination)
        else:
          pass
        return '',200
    return reply,200
  except Exception as e:
    logging.error(f"official /endpoint error :{format_exc()}")
    return ''
  

@bot.route('/gupshup',methods=['GET','POST'])
def gupshup_webhook():
  response = None
  if(request.method == "GET"):
    show("GET REQUEST of gupshup")
    try:
      response = verify_token(request)
      show("response")
      show(response)

    except:
      show("GET REQUEST of gupshup ERROR")
      response = "Ok"
        
  elif(request.method == "POST"):
    try:
      show("request.json")
      show(request.json)
      gs = Gupshup()

      response = ""

      number_and_message = gs.extract_user_message(request.json)
      number = number_and_message.get('from')
      message = number_and_message.get('message')
      show(f"{number,message}")
      if(number and message):
          bot = flow(number)
          logging.debug(number_and_message)
          message = number_and_message['message'][0:250]
          reply = bot.fetch_reply(message,number)
          if(reply):
            gs.send_text_message(reply,number)

    except:
      logging.debug(number_and_message)
      logging.error(format_exc())
    finally:
      return response

def verify_token(req):
      response = None
      verify_token = req.args.to_dict()['hub.verify_token']
      if(verify_token == WA_WEBHOOK_VERIFY_TOKEN):
            response = req.args.to_dict()['hub.challenge']
      return response
  