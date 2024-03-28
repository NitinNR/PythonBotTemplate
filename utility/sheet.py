import gspread
from oauth2client.service_account import ServiceAccountCredentials
from configs import configurations as config
from datetime import datetime
import pytz

class Sheet:
    def __init__(self) -> None:
        scope = config.SCOPE
        creds = ServiceAccountCredentials.from_json_keyfile_name("keys/apikey.json", scope)
        self.client = gspread.authorize(creds)
        self.SheetName = config.ROOTSHEETNAME
        self.MYTIMEZONE = config.BOT_TIMEZONE
        self.sheet = self.client.open("Beautex WhatsApp Bot")
    
    def storeSheetRecord(self,data:list,worksheet)->None:
        # here data is the list
        # sheet = self.client.open(self.SheetName)
        ws = self.sheet.worksheet(worksheet)
        dateTime = self.getDateTimeNow().strftime("%d/%m/%Y, %I:%M %p")
        data.append(dateTime)
        ws.append_row(data)

    def getDateTimeNow(self):
      cdate = datetime.now(pytz.timezone(self.MYTIMEZONE))
      return cdate
  
    def getValue(self,worksheet_name,row,col):
        wrk = self.sheet.worksheet(worksheet_name)
        val = wrk.cell(row,col).value
        return val
    
    def updateCell(self,worksheet_name,row,col,newvalue):
        wrk = self.sheet.worksheet(worksheet_name)
        wrk.update_cell(row,col,newvalue)
        
    def findAll(self,worksheet_name,valuetofound):
        wrk = self.sheet.worksheet(worksheet_name)
        return wrk.findall(valuetofound)
    
    def getColvalues(self,worksheet_name,col):
        wrk = self.sheet.worksheet(worksheet_name)
        colvaues = wrk.col_values(col)
        return colvaues
    
    def addRow(self,worksheet_name,roww):
        wrk = self.sheet.worksheet(worksheet_name)
        wrk.append_row(roww)


class BeautSheet(Sheet):
    
    
    def main_menu(self):        
        val = self.getColvalues("main-menu",2)
        val = val[1:]
        reply= "*Main-menu* 〽️\n\n"
        for  value in val:
            reply = reply + value
            reply = reply + "\n"
        
        val = self.getValue("Main Menu logic",6,3)        
        try:
            if len(val):
                offers = "\n-------------\n   offers\n-------------\n"+str(val)+"\n"
            else:
                offers = " "
        except:
            offers = ""
        header = self.getValue("Main Menu logic",6,1)
        footer = "\n\n"+self.getValue("Main Menu logic",6,2)+"\n"  
        main_menu = header+reply+offers+footer
        return str(main_menu)
    
    
    def register_followup_1(self):        
        val = self.getValue("Main Menu logic",21,1)
        return str(val)
    
    def register_followup_2(self):
        val = self.getValue("Main Menu logic",21,2)
        return str(val)
        
    def register_followup_3(self):
        val = self.getValue("Main Menu logic",21,2)
        return str(val)
        
    def comm_pro_search(self,row,col):
        val = self.getValue('Main Menu logic',row,col)
        return str(val)
    
    def prod_comm(self,number,qns_ans,col):
        number_cel = self.findAll('Product Lead',number)
        number_cel = number_cel[-1]
        if len(str(number_cel)):
            user_row = number_cel.row
            self.updateCell('Product Lead',user_row,col,qns_ans)
            
    def fetch_brochures(self,option_number):
        col = self.getColvalues("brochure",1)
        col = col[1:]
        for valuee in col:
            print("fetching brochure")
            row = int(col.index(str(option_number)))+2
            reply = self.getValue("brochure",row,3)
            return reply
        
    def warranty_info(self,number,name,email,info):
        self.addRow("Warranty & Bill",[str(number),name,email,info])
        val = self.getValue("Main Menu logic",9,9)
        return str(val)
    
    def dealership_info(self,number,name,email,info):        
        self.addRow("Dealership & Enquiry",[str(number),name,email,info])
        val = self.getValue("Main Menu logic",10,9)
        return str(val)
    
    
    def complaints_info(self,number,name,email,info):
        my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
        date_time = my_date.strftime("%m/%d/%Y, %H:%M:%S")        
        self.addRow("Complaints",[str(number),name,email,info,str(date_time)])
        val = self.getValue("Main Menu logic",9,9)
        return str(val)
    
    def others_info(self,number,name,email,info):
        my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
        date_time = my_date.strftime("%m/%d/%Y, %H:%M:%S")
        self.addRow("Others",[str(number),name,email,info,str(date_time)])
        val = self.getValue("Main Menu logic",10,9)
        return str(val)