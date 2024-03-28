from datetime import datetime,timedelta,date
import pytz
import pymysql as db
# import xlwt
import pandas.io.sql as sql
import pandas as pd
# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2 import service_account
######

#E-Mail
from utility.sendmail import sendMail
from configs.configurations import MYSQL_HOST,MYSQL_DB,MYSQL_PASSWORD,MYSQL_USER,MYSQL_PORT
from utility.logger import show

my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
date_time = my_date.strftime("%m/%d/%Y T %H:%M:%S")

class Dbmodel:
    def __init__(self) -> None:
        self.conn = db.Connection(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,passwd=MYSQL_PASSWORD, db=MYSQL_DB,cursorclass=db.cursors.DictCursor)
        

    def check_number_exist_in_db(self,number):
        cur=self.conn.cursor()
        sql="SELECT * FROM `users` WHERE `whatsapp_number` = %s"
        cur.execute(sql,(str(number)))
        users=cur.fetchone()
        self.conn.close()
        if users is None:
            return False
        if users is not None:
            return True
        
    def create_user(self,name,email,number):
        try:
            cur = self.conn.cursor()
            my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
            date_time = my_date.strftime("%m/%d/%YT%H:%M:%S")
            sql = "INSERT INTO users(whatsapp_number,email,name,DateTime) VALUES (%s,%s,%s,%s)"
            cur.execute(sql,(number,email,name,date_time))
            self.conn.commit()
            self.conn.close()
            status = True
        except:
            status = False
        finally:
            return status


    def store_message(self,number,user_msg,bot_reply):
        try:
            cur = self.conn.cursor()
            sql = "INSERT INTO message_logs(user_phone,user_message,bot_reply) VALUES (%s,%s,%s)"
            cur.execute(sql,(number,user_msg,bot_reply))
            self.conn.commit()
            self.conn.close()
            status = True
        except Exception as e:
            show(e)
            status = False
        finally:
            return status

    def get_messages(self,last_id):
        messages_status = {"status":False,"message":[]}
        try:
            cur = self.conn.cursor()
            sql = "select id,user_phone,user_message,bot_reply,created_at ,DATE_FORMAT(created_at, %s) AS formatted_datetime from message_logs where id > %s"
            cur.execute("SET time_zone = 'Asia/Kolkata';")
            datetime_format = '%W, %M %e, %Y, %h:%i %p'  # Format for date and time            
            cur.execute(sql,(datetime_format,last_id))
            messages = cur.fetchall()
            messages_status = {"status":True,"message":messages}
            self.conn.close()
        except Exception as e:
            show(e)
        finally:
            return messages_status


    # def store_message(self,number,message)
        
    def getUserDetails(self,number):
        cur=self.conn.cursor()
        sql="SELECT name,email FROM `users` WHERE `whatsapp_number` = %s"
        cur.execute(sql,(str(number)))
        users=cur.fetchone()
        self.conn.close()
        print(users,"uuuu")
        return users

#------------------------------------------------------

# here
    def send_mail(self,fromaddr,toaddr,filename,path_of_file,subject,body):
        sendMail().send_mail(fromaddr,toaddr,filename,path_of_file,subject,body)

#------------------------- Exporting -----------------------------


    def export_to_excel(self):
        conn = db.Connection(host=HOST, port=PORT, user=USER,       passwd=PASSWORD, db=DB)
        # cur=conn.cursor()
        my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
        #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        date = my_date.strftime("%d/%m/%Y")
        time = my_date.strftime("%H:%M")
        print("date",date," and time:",time)
        # sqll = "SELECT * FROM `healthcare` WHERE `Date`=%s"
        # cur.execute(sqll,(str(date)))
        # users = cur.fetchall()
        # df=sql.read_sql(users,conn)
        
        df=sql.read_sql("SELECT  `From Number`, `To Number`, `Text`, `Date`, `Time` FROM `healthcare` WHERE `Date`='"+str(date)+"'",conn)
        print(df)
        # export the data into the excel sheet
        df.to_excel('daily_report.xls')
        # self.rename_file('daily_report.xls')
        
        fromaddr = "ravi.salvi935@gmail.com"
        toaddr_testing1 = "ketan.salvi21@gmail.com"
        filename = 'daily_report.xls'
        # filename = "messages-"+str(date)+".xls"
        path_of_file = filename
        subject = "Message Dump for the day "+str(date)
        body = "Report Dated : "+str(date)
        self.send_mail(fromaddr,toaddr_testing1,filename,path_of_file,subject,body)
        conn.close()
