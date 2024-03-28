from sqlitedict import SqliteDict
import gc
from utility.logger import logging
from traceback import format_exc
from utility.logger import show


class Unicorn:

    def __init__(self):
        gc.collect()

    def udbconn(self,tablename):
        userdb = SqliteDict('./sqlitedatabase/userDb.sqlite',tablename, autocommit=True)
        return userdb

    def __gdbconn(self,tablename):
        gdb = SqliteDict('./sqlitedatabase/gdb.sqlite',tablename, autocommit=True)
        return gdb

    def check_key(self,tablename,number, key):
        status = False
        keyValue = False
        userdb = self.udbconn(tablename)
        try:
            status = True if key in userdb[number] else False
            if status:
                keyValue = userdb[number][key]
        except Exception as e:
            status = False
        finally:
            self.closeudb(userdb)
        return {"status": status, "value": keyValue}

    def check_key_lvl2(self,tablename,number,key1,key2):
        status = False
        userdb = self.udbconn(tablename)
        try:
            if key1 in userdb[number]:
                if key2 in userdb[number][key1]:
                    status = True
        except:
            status = False
        finally:
            self.closeudb(userdb)

        return status

    def checkr(self,tablename, number):
        status = False
        userdb = self.udbconn(tablename)
        try:
            status = True if number in userdb else False
        except Exception as e:
            status = False
        finally:
            self.closeudb(userdb)

        return status

    def createFirstkv(self,tablename, number, key, value):
        userdb = self.udbconn(tablename)
        try:
            userdb[number] = {key: value}
        except Exception as e:
            logging.error(e)
        finally:
            self.closeudb(userdb)

    def doUp(self,tablename, number, key, value):
        userdb = self.udbconn(tablename)
        if value != "" and value != None:
            try:
                old_data = userdb[number]
                # print(f"&&&&&&&&&&&&&&&&&\noldData:{old_data}")
                new_pair = {key: value}
                old_data.update(new_pair)
                new_data = dict(old_data)
                userdb[number] = new_data
                print("**********************************")
                print(f"New data:>{new_data}")

            except Exception as e:
                logging.error(e)
            finally:
                self.closeudb(userdb)

    def doUpList(self,tablename, number, key, value,allowduplicatedata=False):
        userdb = self.udbconn(tablename)
        if value != "" and value is not None:
            try:
                old_data = userdb.get(number,None)
                if(old_data):
                    if value not in old_data.get(key) or allowduplicatedata:
                        old_data.get(key).append(value)
                        new_data = old_data
                        userdb[number] = new_data
                else:
                    userdb[number] = {key:[value]}
            except Exception as e:
                logging.error(e)
            finally:
                self.closeudb(userdb)
        else:
            pass

    def doMassUp(self,tablename, number, dict_data):
        userdb = self.udbconn(tablename)
        try:
            old_data = userdb.get(number)
            old_data.update(dict_data)
            new_data = dict(old_data)
            userdb[number] = new_data
            print("**********************************")
            print(f"New data:>{new_data}")
        except Exception as e:
            logging.error(e)
        finally:
            self.closeudb(userdb)

    def gv(self,tablename, number):
        userdb = self.udbconn(tablename)
        try:
            return userdb.get(number)
        except Exception as e:
            logging.error(e)
            return 0
        finally:
            self.closeudb(userdb)

    def mass_gv(self, tablename,number, keys: list):
        userdb = self.udbconn(tablename)
        try:
            return {k: userdb.get(number).get(k) for k in keys}
        except:
            return "not found"
        finally:
            self.closeudb(userdb)

    def getRecord(self,tablename, number):
        userdb = self.udbconn(tablename)
        try:
            return dict(userdb[number])
        except:
            return False
        finally:
            self.closeudb(userdb)

    def dv(self,tablename, number):
        userdb = self.udbconn(tablename)
        try:
            del userdb[number]
        except Exception as e:
            logging.error(e)
        finally:
            self.closeudb(userdb)

    def deletMultiplkeys(self,tablename, number, keys:list):
        userdb = self.udbconn()
        try:
            old_data = userdb[number]
            for key in keys:
                del old_data[key]
            userdb[number] = old_data
        except Exception as e:
            logging.error(e)
        finally:
            self.closeudb(userdb)

    def deleteRoot(self,tablename,number):
        userdb = self.udbconn()
        try:
            userdb[number] = {}
            userdb.__delitem__(number)
        except Exception as e:
            logging.error(e)
        finally:
            self.closeudb(userdb)

    def createG(self,tablename, key, value):
        show(tablename)
        show(key)
        gdb = self.__gdbconn(tablename)
        status = True
        try:
            gdb[key] = value
            logging.info("Data Added !")

        except Exception as e:
            status = False
            logging.error(e)
        finally:
            self.closegdb(gdb)
            return status

    def updateG(self, key, value):
        gdb = self.__gdbconn()
        if value != "" and value is not None:
            try:
                gdb.update({key: value})
            except Exception as e:
                logging.error(e)
            finally:
                self.closegdb(gdb)

    def getg(self,tablename, key):
        show(tablename)
        show(key)
        gdb = self.__gdbconn(tablename)
        glb = None
        try:
            # print("KEYS:",list(gdb))
            glb = gdb[key.lower()]
        except Exception as e:
            logging.error(e)
        finally:
            self.closegdb(gdb)
            return glb

    def getGColvalues(self, key):
        gdb = self.udbconn()
        rangeOfStart = 2
        try:
            glb = gdb[key]
            items_dict = {}
            for i in range(rangeOfStart, len(glb)):
                place = glb[i][1].strip(" ").strip("\n")
                ct = glb[i][2]
                if place:
                    items_dict[i - 1] = f"{place}@{ct}"
        except Exception as e:
            logging.error(e)
        finally:
            self.closegdb()
        return items_dict

    def lvl2_manipulate(self, number, key, key1, value1):
        userdb = self.udbconn()
        try:
            old_data = userdb[number]
            new_pair = {key1: value1}
            if key not in old_data.keys():
                old_data[key] = {}

            old_data[key].update(new_pair)

            new_data = dict(old_data)
            userdb[number] = new_data
        except Exception as e:
            print("lvl2_manipulate ERROR =>", e)
        finally:
            self.closeudb(userdb)

    def mass_lvl2_manipulate(self, number, key, data: dict):
        userdb = self.udbconn()
        try:
            old_data = userdb[number]
            if key not in old_data.keys():
                old_data[key] = {}

            for k, v in data.items():
                new_pair = {k: v}
                old_data[key].update(new_pair)
            new_data = dict(old_data)
            userdb[number] = new_data
        except Exception as e:
            logging.error(f">>>>>>> {format_exc()}")

        finally:
            self.closeudb(userdb)

    def closeudb(self,userdb):
        userdb.close()

    def closegdb(self,gdb):
        gdb.close()


#######################################
#######################################

class Prana(Unicorn):
    
    
    def __init__(self):
        gc.collect()
        
    def get_language_selection_message(self):
        msg = self.getg("PranaEnglish","userlanguage")
        msg = msg[0][0] if msg else self.getg("PranaHindi","userlanguage")[0][0]
        return msg
    
    def get_user_language(self,number):
        user_language = self.gv("language",number)
        user_language = "hindi" if user_language == 0 else user_language
        return user_language
        
    def get_terms_status(self,number):
        userdb = self.udbconn("terms")
        status = False
        try:
            status = userdb[number]
        except Exception as e:
            logging.error(e)
        finally:
            self.closeudb(userdb)
            return status
    
    def store_terms_status(self,number,status):
        userdb = self.udbconn("terms")
        ack = True
        try:
            userdb[number] = status
        except Exception as e:
            logging.error(e)
            ack = False
        finally:
            self.closeudb(userdb)
            return ack

    def upsert(self,tablename, number, value):
        userdb = self.udbconn(tablename)
        if value != "" and value != None:
            try:
                userdb[number] = value
            except Exception as e:
                logging.error(e)
            finally:
                self.closeudb(userdb)

    
    
    def get_main_menu(self, tablename, subsheet_name):
        sheet_data = self.getg(tablename,subsheet_name)
        main_menu = sheet_data[1][1]
        return main_menu
    
    def get_sub_menu(self, tablename, subsheet_name):
        sheet_data = self.getg(tablename,subsheet_name)
        sub_menu = sheet_data[3][1]
        return sub_menu
    
    #
    def get_disease_ways(self,tablename,subsheet_name,user_disese_option):
        sheet_data = self.getg(tablename,subsheet_name)
        ways = None
        next_disese_option = 6
        for i in range(4,len(sheet_data),next_disese_option):
            disease_type = sheet_data[i][1]
            if(user_disese_option == disease_type):
                ways = sheet_data[i+1][1]
                break
        return ways
    
    def get_way_info(self,user_sheet,main_menu_option,disease_type,way_option):
        show(f"{user_sheet,main_menu_option,disease_type,way_option}")
        sheet_data = self.getg(user_sheet,main_menu_option)
        way_options_row = 0
        next_disese_option = 6
        # first find row
        for i in range(4,len(sheet_data),next_disese_option):
            if(sheet_data[i][1] == disease_type ):
                way_options_row = i+2
                break
            
        way_option_column = 0
        
        # second find column
        if(way_options_row != 0):
            way_options = sheet_data[way_options_row][1:]
            
            # removing blank entries here
            way_options = [x for x in way_options if x]
            show(f"way_options:{way_options}")
            
            for i,option in enumerate(way_options):
                if(option == way_option):
                    way_option_column = i+1
                    show(f"i:{i}")
                    break
                
        show(f"way_options_row:{way_options_row},way_option_column:{way_option_column}")
        return sheet_data[way_options_row+1][way_option_column]
                
    def get_disease_type_option(self,number):
        disease_type_option = self.udbconn("disease_type_option")[number]
        return disease_type_option
    
    def get_disclaimer(self,tablename):
        show(f"sheet:{tablename}")
        disclaimer = self.getg(tablename,"terms")[0][0]
        return disclaimer

    def get_default_reply(self,tablename):
        default_reply = self.getg(tablename,"default_reply")[0][0]
        return default_reply

    
    def store_options_of_diseasestypes(self,tablename,subsheet_name,number):
        diseasesinfoways = self.getg(tablename,subsheet_name)
        options = []
        for i in range(4,len(diseasesinfoways),6):
            disease_type = diseasesinfoways[i][1]
            options.append(disease_type)
        show(f"next options {options}")
        self.upsert("next_options", number, options)
        return True

    def store_options_of_diseasesinfoways(self,user_sheet,main_menu_option,disease_type,number):
        sheet_data = self.getg(user_sheet,main_menu_option)
        way_options_row = 0
        
        for i in range(4,len(sheet_data)):
            if(sheet_data[i][1] == disease_type ):
                way_options_row = i+2
                break

        if(way_options_row != 0):
            way_options = sheet_data[way_options_row][1:]
            # removing blank entries here
            way_options = [x for x in way_options if x]
            show(f"new options:{way_options}")
            self.upsert("next_options", number, way_options)
            return True


    def get_next_options(self,number):
        next_options = self.gv("next_options",number)
        return next_options

    def delete_next_options(self,number):
        next_options = self.dv("next_options",number)
        return next_options

    def get_invalid_option_message(self,tablename):
        invalid_option_message = self.getg(tablename,"invalid_option_message")
        show(F"invalid :{invalid_option_message}")
        invalid_option_message = invalid_option_message[0][0]
        return invalid_option_message

    def get_translations(self,tablename):
        return self.getg(tablename,"translated text")
        
        