# coding=utf-8
from flask import Flask, request,jsonify
from routes.route_bot import bot
from utility.logger import logging
from traceback import format_exc
from configs.configurations import setupgoogleAppllicationcreds,BOT_PORT

from mains.flow import flow

# start
setupgoogleAppllicationcreds()

app = Flask(__name__)

# routes

app.register_blueprint(bot, url_prefix='/bot/v1')

app.config.from_object(__name__)
logging.debug("Bot Bootting...")

@app.route('/status',methods = ['GET','POST'])
def getstatus():
      return "Bot droid Working"

@app.route('/test',methods = ['GET','POST'])
def test():
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
      


def run():
  if __name__ == "__main__":
      app.run(host='0.0.0.0',port=BOT_PORT,debug=True)

run() 
