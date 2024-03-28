import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
class sendMail:
    def send_mail(self,fromaddr,toaddr,filename,path_of_file,subject,body):
        msg = MIMEMultipart() 
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(path_of_file, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "qwupdxeflwrkldmw")
        text = msg.as_string()
        print(s.sendmail(fromaddr, toaddr, text) )
        s.quit()
        
    def send_email_on_trigger(self,user_message,bot_reply,user_number):
            # cur=conn.cursor()
        my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
        #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        date = my_date.strftime("%d/%m/%Y")
        time = my_date.strftime("%H:%M")
        fromaddr = "ravi.salvi935@gmail.com"
        toaddr_testing1 = "ketan.salvi21@gmail.com"
        # subject = "Daily Report of "+str(date)
        body = "Adverse Effect Message Triggered"+"\n\n\nUser Message: "+str(user_message)+"User Number: "+str(user_number)+"\n\nBot Reply: "+str(bot_reply)+"\n\nDate: "+str(date)+" Time: "+str(time)
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        # s.login("ravi.salvi935@gmail.com", "qwupdxeflwrkldmw") 
        s.login(fromaddr, "qwupdxeflwrkldmw")
        message = body
        # s.sendmail(fromaddr, toaddr_testing, message)
        s.sendmail(fromaddr, toaddr_testing1, message)
        s.quit() 