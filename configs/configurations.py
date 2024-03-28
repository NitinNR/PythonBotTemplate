import os
from dotenv import load_dotenv
load_dotenv()

# General configs
BOT_ENV = os.environ.get("ENV", 'dev')
BOT_NAME = os.environ.get("BOT_NAME", 'NONE')
BOT_PORT = os.environ.get("BOT_PORT", 3000)
DEPLOY_IN = os.environ.get("DEPLOY_IN", 'true').lower() in ('true', '1')
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", 0)

# Database configs
ISDBREQUIRED = os.environ.get("isDbRequired", 0)
MYSQL_USER = os.environ.get("MUSER", 0)
MYSQL_DB = os.environ.get("DB", 0)
MYSQL_PASSWORD = os.environ.get("PASSWORD", 0)
MYSQL_HOST = os.environ.get("HOST", 0)
MYSQL_PORT = int(os.environ.get("PORT", 3306))

# DialogFlow configs
ISDIALOGFLOWREQUIRED = os.environ.get("isDialogflowRequired", False).lower() in ('true', '1')
CREDS_FILENAME = os.environ.get("JSON_FILENAME", 'DEAFULT')
CAT = os.environ.get("CLIENT_ACCESS_TOKEN", '0000')
PROJECT_ID = os.environ.get("PROJECT_ID", 0)
ROOTSHEETNAME = os.environ.get("rootSheetName",'NONE')

# Google Sheet configs
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# mtimezone = os.environ.get("TIMEZONE", 0)
BOT_TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")


# Twilio configs

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", 0)
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_ACCOUNT_SID", 0)



# def checkdb_isrequired():
#     status = True
#     if ISDBREQUIRED.casefold() == "yes":
#         status = False
#     return status


# def checkdf_isrequired():
#     status = True
#     if ISDIALOGFLOWREQUIRED.casefold() == "yes":
#         status = False
#     return status



#===================================
def setupgoogleAppllicationcreds():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/"+CREDS_FILENAME


# WHATSAPP Cloud

WA_CLOUD_PHONE_NUMBER_ID = os.environ.get("WA_CLOUD_PHONE_NUMBER_ID", 0)
WA_CLOUD_WAAPITOKEN = os.environ.get("WA_CLOUD_WAAPITOKEN", 0)
WA_WEBHOOK_VERIFY_TOKEN = os.environ.get("WA_WEBHOOK_VERIFY_TOKEN", 0)

# TEMPLATE
AFTER_CALL_TEMPLATE_NAME = os.environ.get("AFTER_CALL_TEMPLATE_NAME", 0)

#AIBT

AIBT_SERVER_URL = os.environ.get("AIBT_SERVER_URL", 0)


# Gupshup WaApi
API_URL = os.environ.get("GUPSHUP_API_URL", 0)
SENDER = os.environ.get("GUPSHUP_SENDER", 0)
SOURCE_NAME = os.environ.get("GUPSHUP_SOURCE_NAME", 0)

