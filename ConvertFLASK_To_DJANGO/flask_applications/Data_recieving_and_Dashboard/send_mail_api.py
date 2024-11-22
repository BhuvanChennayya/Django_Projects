# from send_email_apis_report.send_mail_api import *
# from send_email_apis_report.database import mongo
from fileinput import filename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from datetime import datetime
from datetime import date
from flask import Flask, Blueprint
from flask import Flask, request
from flask_pymongo import PyMongo
from datetime import timedelta
import requests, json, os, glob
from flask_cors import CORS
from flask_debug import Debug
import re
import smtplib
from socket import gaierror
from bson.objectid import ObjectId
from bson import json_util
from bson import ObjectId
import time

# from send_email_apis_report.packages import *
send_email = Blueprint('send_email_api', __name__)

app = Flask(__name__)
cors = CORS(app, resources={'*': {'origins': '*'}}, supports_credentials=True)
Debug(app)
mongo = PyMongo()
app.register_blueprint(send_email)
app.config['FLASK_DEBUG_DISABLE_STRICT'] = True
app.config['SECRET_KEY'] = '123nagashanti123@'                                            
app.config['MONGO_DBNAME'] = 'alert_email_details'                                           #Configuring the MongoDB Database Name 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/alert_email_details'                    #and URL of MongoDB
mongo.init_app(app)

def parse_json(data):
    return json.loads(json_util.dumps(data))


def is_valid_smtp_port(server, port):
    try:
        # Try to connect to the SMTP server with the given port
        with smtplib.SMTP(server, port) as smtp:
            # Successfully connected
            return True
    except gaierror as e:
        print("ERROR: Failed to resolve hostname:", e)
        return False
    except ConnectionRefusedError as e:
        print("ERROR: Connection refused by the server:", e)
        return False
    except Exception as e:
        print("ERROR: An unexpected error occurred:", e)
        return False

    
def is_valid_time_format(input_time):
    # Regular expression pattern to match "HH:MM" format
    pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    return re.match(pattern, input_time) is not None


def verfify_keys_miss_or_not(require_keys, given_keys):
    missing_key=set(require_keys).difference(given_keys)

    return missing_key

def verify_parameter_val(obj):
    output=[k for k, v in obj.items() if v =='']

    return output

def is_valid_password(password):
    # Check if the password contains at least one character and one digit
    has_character = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_character and has_digit

# def is_valid_email(email):
#     # Regular expression pattern for a basic email validation
#     pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
#     return re.match(pattern, email)

def is_valid_email(email):
    # Regular expression pattern to match a valid email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_boolean(value):
    return isinstance(value, bool)
    

@app.route("/insert_email_details", methods=["POST"])
def insert_email_details():
    if True:
        ret = {"success": False, "message":"An unexpected error has occurred, please try again later"}

        jsonobject = request.json
        if jsonobject == None:  
            jsonobject = {}
        request_key_array=['email_receivers','violation_report','analytics_types','timestamp', 'smtp_server', 'smtp_port', 'sender_email', 'sender_pwd']
        jsonobjectarray= list(set(jsonobject))
        # missing_key=set(request_key_array).difference(jsonobjectarray)
        missing_key = verfify_keys_miss_or_not(request_key_array, jsonobjectarray)
        if not missing_key:
            # output=[k for k, v in jsonobject.items() if v =='']
            output = verify_parameter_val(jsonobject)
            if output:
                # ret['message']='You have missed these parameters '+str(output)+' to enter. please enter properly.'
                ret = {'message': 'You have missed these parameters '+str(output)+' to enter. please enter properly.', 'success': False}

            else:
                if jsonobject['email_receivers'] == {}:
                    ret = {"message": 'You have missed recipients to enter in the emails. please enter properly.', 'success': False}

                else:
                    list_analytics_solns = ['RA', 'ra', 'PPE', 'ppe', 'TC', 'tc', 'CR', 'cr', 'Fire', 'Water', 'fire', 'water']
                    email_recipients = ['to', 'cc', 'bcc']
                    to_recipient = ['to']

                    all_email_receipients_keys = jsonobject['email_receivers'].keys()
                    # Convert the keys to a list if needed
                    all_email_receipients_keys_list = list(all_email_receipients_keys)
                    to_recipient_shld_be = verfify_keys_miss_or_not(to_recipient, all_email_receipients_keys_list)
                    # print("Missing reciever emails:", to_recipient_shld_be)

                    if not to_recipient_shld_be:
                        given_all_analytics_slns_list = jsonobject['analytics_types']
                        if len(given_all_analytics_slns_list) != 0:
                            # Check if all items in 'GIVE_ANALYTICS_SLNS' are present in 'LIST_ANALYTICS_SLNS' using list comprehension and all()
                            all_given_analytics_slns_exist = all(item in list_analytics_solns for item in given_all_analytics_slns_list)

                            # Check if all items in 'GIVE_EMAIL_RECIPIENTS_KEYS' are present in 'EMAIL_RECIPIENTS' using list comprehension and all()
                            all_given_email_recipients_keys_exist = all(item in email_recipients for item in all_email_receipients_keys_list)

                            if all_given_analytics_slns_exist == True:
                                if all_given_email_recipients_keys_exist == True:

                                    # email_recipients_values=[k for k, v in jsonobject['email_receivers'].items() if v =='']
                                    email_recipients_values = verify_parameter_val(jsonobject['email_receivers'])
                                    if email_recipients_values:
                                        # ret['message']='You have missed these parameters '+str(output)+' to enter. please enter properly.'
                                        ret = {'message': 'Please enter values for '+str(email_recipients_values)+' these keys.', 'success': False}

                                    else:
                                        # contains_empty_list = any(isinstance(item, list) and not item for item in my_list)
                                        email_recipients_value_arr_empty = [k for k, v in jsonobject['email_receivers'].items() if len(v) ==0]
                                        email_recipients_dict = jsonobject['email_receivers']
                                        # if len(email_recipients_value_arr_empty) != 0:
                                        if len(email_recipients_dict['to']) == 0:
                                            ret = {'message': 'Please enter value for "to" key, it should not be empty.', 'success': False}
                                            # ret = {'message': 'You have missed these parameters '+ str(email_recipients_value_arr_empty) +' to enter. please enter properly.', 'success': False}

                                        else:
                                            #VERIFY TIMESTAMP DATA TYPE & FORMAT
                                            timestamp_arr = jsonobject['timestamp']
                                            print("Timestamp ARR:", timestamp_arr)
                                            time_format_res_ls = []
                                            if type(timestamp_arr) == list:
                                                for t in timestamp_arr:
                                                    input_time = t
                                                    verify_time_format = is_valid_time_format(input_time)
                                                    time_format_res_ls.append(verify_time_format)

                                                if False in time_format_res_ls:
                                                    ret = {"message":"Given time format is not valid, please check it once and enter proper value. ", "success": False}
                                                
                                                else:
                                                    given_sender_email = jsonobject['sender_email']
                                                    print("given_sender_emailgiven_sender_email:--------111111111111------", given_sender_email)
                                                    email_valid_not = is_valid_email(given_sender_email)
                                                    if is_valid_email(given_sender_email):
                                                        # Example usage: Verify an SMTP server and port from a given string
                                                        smtp_server_input = jsonobject['smtp_server']
                                                        smtp_port_input = jsonobject['smtp_port']

                                                        if is_valid_smtp_port(smtp_server_input, smtp_port_input):
                                                            email_recipients_dict = jsonobject['email_receivers']
                                                            if type(email_recipients_dict['to']) == list:
                                                                for to_eml in email_recipients_dict['to']:
                                                                    email_valid_not = is_valid_email(to_eml)
                                                                    if is_valid_email(to_eml):
                                                                        if 'cc' in email_recipients_dict.keys():
                                                                            if type(email_recipients_dict['cc']) == list:
                                                                                for cc_eml in email_recipients_dict['cc']:
                                                                                    email_valid_not = is_valid_email(cc_eml)
                                                                                    if is_valid_email(cc_eml):
                                                                                        pass
                                                                                    
                                                                                    else:
                                                                                        print(f"The email '{cc_eml}' is not a valid email address.")
                                                                                        ret = {'message':f"The cc-email '{cc_eml}' is not a valid email address.", "success":False}

                                                                            else:
                                                                                ret = {'message':f"The bcc-email is not in the format.", "success":False}

                                                                                
                                                                        if 'bcc' in email_recipients_dict.keys():
                                                                            if type(email_recipients_dict['bcc']) == list:
                                                                                for bcc_eml in email_recipients_dict['bcc']:
                                                                                    email_valid_not = is_valid_email(bcc_eml)
                                                                                    if is_valid_email(bcc_eml):
                                                                                        pass
                                                                                    
                                                                                    else:
                                                                                        print(f"The email '{bcc_eml}' is not a valid email address.")
                                                                                        ret = {'message':f"The bcc-email '{bcc_eml}' is not a valid email address.", "success":False}
                                                                            else:
                                                                                ret = {'message':f"The bcc-email is not in the format.", "success":False}
                                                                        existed_data = mongo.db.email_details.find_one(jsonobject)
                                                                        if existed_data:
                                                                            ret = {'message':'Data existed in the collection.', 'success': True}

                                                                        else:
                                                                            response = mongo.db.email_details.insert_one(jsonobject)
                                                                            # result = mongo.db.email_details.countDocuments({'_id': response.inserted_id})#ObjectId(response.inserted_id) })
                                                                            ret = mongo.db.email_details.find_one({"_id": response.inserted_id})

                                                                            if ret :
                                                                                ret = {'message':'Data inserted successfully.', 'success': True}

                                                                            else:
                                                                                ret

                                                                    else:
                                                                        print(f"The email '{to_eml}' is not a valid email address.")
                                                                        ret = {'message':f"The to-email '{to_eml}' is not a valid email address.", "success":False}
                                                            else:
                                                                print(f"The to-email parameter is not a valid format.")
                                                                ret = {'message':f"The given to-email is not a valid format.", "success":False}

                                                        else:
                                                            print(f"The SMTP port {smtp_port_input} for '{smtp_server_input}' is invalid or cannot be reached.")
                                                            ret = {"message":f"The SMTP port {smtp_port_input} for '{smtp_server_input}' is invalid or cannot be reached.", "success": False}
                                                    
                                                    else:
                                                        print(f"The email '{given_sender_email}' is not a valid email address.")
                                                        ret = {'message':f"The cc-email '{given_sender_email}' is not a valid email address.", "success":False}

                                            else:
                                                ret = {"message":"Timestamp is not the format", "success": False}
                                            
                                else:
                                    ret = {'message':'Given eamil receivers are not valid.', 'success': False}

                            else:
                                ret = {'message':'Given all analytics solutions are not valid, please check it.', 'success': False}
                        
                        else:
                            ret = {'message':'You had missed to give "analytics solutions", please check it.', 'success': False}

                    else:
                        ret = {'message': 'You have missed '+ str(to_recipient_shld_be) + 'to enter. Please enter properly.', 'success': False}

        else:
            ret={'success':False,'message':'You have missed these keys '+str(missing_key)+' to enter. please enter properly.'}

        return ret


def fun_edit_parameters(keys_not_existed, editing_details, given_keys, email_sender_data, id):
    update_data ={}
    # ret = {'message': 'something went wrong.', 'success': False}
    if keys_not_existed != False:
        to_val = []
        cc_val = []
        bcc_val = []
        analytics_types_val = []
        if "email_receivers" in editing_details:
            email_recipients_dict = editing_details['email_receivers']
            print("EMAIL RECEIVERS DATA:-**********--", email_recipients_dict)
            if email_recipients_dict != {}:
                if 'to' in email_recipients_dict.keys():
                    if len(email_recipients_dict['to']) == 0:
                        ret = {'message': 'You have missed these parameters "to" to enter. please enter properly.', 'success': False}

                    else:
                        if "timestamp" in given_keys: 
                            #VERIFY TIMESTAMP DATA TYPE & FORMAT
                            timestamp_arr = editing_details['timestamp']
                            time_format_res_ls = []
                            if type(timestamp_arr) == list:
                                if len(timestamp_arr) != 0: 
                                    for t in timestamp_arr:
                                        input_time = t
                                        verify_time_format = is_valid_time_format(input_time)
                                        print("Verify time format", type(verify_time_format))
                                        time_format_res_ls.append(verify_time_format)

                                    if False in time_format_res_ls:
                                        ret = {"message":"Given time format is not valid, please check it once and confirm. ", "success": False}

                                    else:
                                        timestamp_val = editing_details['timestamp']
                                        update_data['timestamp']=timestamp_val

                                else:
                                    ret = {"message":"Please enter the value for 'Timestamp', it should not be empty.", "success": False}

                            else:
                                ret = {"message":"Timestamp is not the format", "success": False}

                        if "smtp_server" in given_keys and "smtp_port" in given_keys:
                            # Example usage: Verify an SMTP server and port from a given string
                            smtp_server_input = editing_details['smtp_server']
                            smtp_port_input = editing_details['smtp_port']

                            if is_valid_smtp_port(smtp_server_input, smtp_port_input):
                                smtp_server_val = smtp_server_input
                                smtp_port_val = smtp_port_input
                                
                            else:
                                ret = {"message":f"The SMTP port {smtp_port_input} for '{smtp_server_input}' is invalid or cannot be reached.", "success": False}

                        
                        if "email_receivers" in given_keys:
                            email_recipients_dict = editing_details['email_receivers']
                            
                            email_recipients_values = verify_parameter_val(editing_details['email_receivers'])
                            if email_recipients_values:
                                ret = {'message': 'You have missed these parameters '+str(email_recipients_values)+' to enter. please enter properly.', 'success': False}

                            else:
                                email_receivers_val = {}
                                if 'to' in email_recipients_dict.keys():
                                    if type(email_recipients_dict['to']) == list:
                                        if len(email_recipients_dict['to']) != 0:
                                            to_emails = []
                                            for to_eml in email_recipients_dict['to']:
                                                email_valid_not = is_valid_email(to_eml)
                                                if is_valid_email(to_eml):
                                                    print(f"The email '{to_eml}' is valid.")
                                                    to_emails.append(to_eml)
                                                    to_val = to_emails

                                                else:
                                                    print(f"The email '{to_eml}' is not a valid email address.")
                                                    ret = {'message':f"The to-email '{to_eml}' is not a valid email address.", "success":False}

                                        else:
                                            print("YES I AM COMING HERE")
                                            ret = {'message':'The to-email should not be empty.', 'success': False}

                                    else:
                                        ret = {'message':f"The to-email format is not a valid, please enter it proporly.", "success":False}
                                

                                if 'cc' in email_recipients_dict.keys():
                                    print("YES CC GIVEN:")  
                                    if type(email_recipients_dict['cc']) == list:
                                        if len(email_recipients_dict['cc']) != 0:
                                            cc_emails = []
                                            for cc_eml in email_recipients_dict['cc']:
                                                email_valid_not = is_valid_email(cc_eml)
                                                if is_valid_email(cc_eml):
                                                    cc_emails.append(cc_eml)
                                                    cc_val = cc_emails
                                                
                                                else:
                                                    print(f"The email '{cc_eml}' is not a valid email address.")
                                                    ret = {'message':f"The cc-email '{cc_eml}' is not a valid email address.", "success":False}

                                        else:
                                            cc_val = email_recipients_dict['cc']

                                    else:
                                        ret = {"message":"Given cc-email format is not valid, please enter it proporly.", "success": False}
                                        print("RESULT:***************************", ret)


                                if 'bcc' in email_recipients_dict.keys():
                                    print("YES CC GIVEN:")  
                                    if type(email_recipients_dict['bcc']) == list:
                                        if len(email_recipients_dict['bcc']) != 0:
                                            bcc_emails = []
                                            for bcc_eml in email_recipients_dict['bcc']:
                                                email_valid_not = is_valid_email(bcc_eml)
                                                if is_valid_email(bcc_eml):
                                                    bcc_emails.append(bcc_eml)
                                                    bcc_val = bcc_emails
                                                    email_receivers_val['bcc'] = bcc_val
                                                
                                                else:
                                                    print(f"The email '{bcc_eml}' is not a valid email address.")
                                                    ret = {"message":f"The bcc-email '{bcc_eml}' is not a valid email address.", "success":False}
                                        else:
                                            bcc_val = email_recipients_dict['bcc']  

                                    else:
                                        ret = {"success":False, "message": "Given bcc-email format is not valid, please enter it proporly."}

                                    
                                email_receivers_val = {"to": to_val, "cc": cc_val, "bcc": bcc_val}
                                update_data['email_receivers']=email_receivers_val   
                            
                        if "analytics_types" in given_keys:
                            if type(editing_details["analytics_types"]) is list:
                                given_all_analytics_slns_list = editing_details["analytics_types"]
                                print("GIVEN ANALYTICS SLNS:", given_all_analytics_slns_list)
                                list_analytics_solns = ['RA', 'ra', 'PPE', 'ppe', 'TC', 'tc', 'CR', 'cr', 'Fire', 'Water', 'fire', 'water']
                                all_given_analytics_slns_exist = all(item in list_analytics_solns for item in given_all_analytics_slns_list)
                                if all_given_analytics_slns_exist == True:
                                    analytics_types_val = editing_details["analytics_types"]
                                    update_data['analytics_types']=analytics_types_val

                                else:
                                    ret = {'message':'Given analytics-solutions are not valid.', 'success': False}

                            else:
                                ret = {"message":" 'analytics_types' is not the format.", "success": False}

                        if "sender_email" in given_keys:
                            given_sender_email = editing_details['sender_email']
                            email_valid_not = is_valid_email(given_sender_email)
                            if is_valid_email(given_sender_email):
                                sender_email_val = given_sender_email
                                update_data['sender_email']=sender_email_val

                            else:
                                print(f"The email '{given_sender_email}' is not a valid email address.")
                                ret = {'message':f"The email '{given_sender_email}' is not a valid email address.", "success":False}

                            
                        if "sender_pwd" in given_keys:
                            password = editing_details['sender_pwd']
                            is_valid_password(password)
                            if is_valid_password(password):
                                print("The password is valid.")
                                sender_pwd_val = editing_details['sender_pwd']
                                update_data['sender_pwd']=sender_pwd_val

                            else:
                                print("The password is not valid.")
                                ret = {'message':f"The given password is not valid.", "success":False}


                        if "violation_report" in given_keys:
                            violation_report_val = editing_details['violation_report']
                            # Example usage: Verify if a value is a boolean
                            if is_boolean(violation_report_val):
                                print("The value is a boolean.")
                                violation_report_val = editing_details['violation_report']
                                update_data['violation_report']=violation_report_val

                            else:
                                print("The value is not a boolean.")
                                ret = {'message':f"The given violation_report is not a boolean.", "success":False}
                        
                        else:
                            if "violation_report" not in given_keys:
                                violation_report_val = email_sender_data['violation_report']
                                update_data['violation_report']=violation_report_val

                            if "analytics_types" not in given_keys:
                                analytics_types_val = email_sender_data['analytics_types']
                                update_data['analytics_types']=analytics_types_val

                            if "sender_email" not in given_keys:
                                sender_email_val = email_sender_data['sender_email']
                                update_data['sender_email']=sender_email_val

                            if "sender_pwd" not in given_keys:
                                sender_pwd_val = email_sender_data['sender_pwd']
                                update_data['sender_pwd']=sender_pwd_val

                            if "smtp_server" not in given_keys:
                                smtp_server_val = email_sender_data['smtp_server']
                                update_data['smtp_server']=smtp_server_val

                            if "smtp_port" not in given_keys:
                                smtp_port_val = email_sender_data['smtp_port']
                                update_data['smtp_port']=smtp_port_val

                            if "timestamp" not in given_keys:
                                timestamp_val = email_sender_data['timestamp']
                                update_data['timestamp']=timestamp_val

                            if "email_receivers" not in given_keys:
                                email_receivers_val = email_sender_data['email_receivers']
                                update_data['email_receivers']=email_receivers_val


                        result = mongo.db.email_details.update_one({'_id':ObjectId(id)},{"$set":update_data})  
                        # print("Response:", result.status())
                        if result.modified_count > 0:
                            ret = {'message': 'Data updated successfully.', 'success': True}
                            print("--------------", result.modified_count > 0)

                        else:
                            existed_data = mongo.db.email_details.find_one(update_data)
                            if existed_data:
                                ret = {'message':'No changes were made during the update.', 'success':False}

                            else:
                                ret
                
            else:
                ret = {'message':'You had missed the "email_receivers value", please enter it proporly.', 'success': False}
            
        
    else:
        ret = {'message':'Given all parameters are not valid, please check it.', 'success': False}

    return ret
    # return ret


@app.route('/edit_email_details', methods=['POST'])
def edit_email_details():
    print("--------------YES I AM COMING:-------------")
    ret = {'success': False, 'message':'something went wrong with edit_email_details api'}
    editing_details = request.json

    #VERIFY REQUIRE HAS GIVEN OR NOT
    given_keys = list(set(editing_details))
    require_keys = ['_id']
    missing_key = verfify_keys_miss_or_not(require_keys, given_keys)
    id =  editing_details['_id']
    # print("Verify mongoid:---------------------------", ObjectId.is_valid(id))

    if ObjectId.is_valid(id) == True:
        email_sender_data = mongo.db.email_details.find_one({'_id':ObjectId(id)})
        print("email_sender_data:",email_sender_data)
        if email_sender_data != None:
            email_receivers_val = {}
            if not missing_key:
                output = verify_parameter_val(editing_details)
                if output:
                    # ret['message']='You have missed these parameters '+str(output)+' to enter. please enter properly.'
                    ret = {'message': 'You have missed these parameters '+str(output)+' to enter. please enter properly.', 'success': False}
                    
                else:

                    # existed_data = mongo.db.email_details.find_one(editing_details)
                    # if existed_data:
                    #     ret = {'message':'No changes were made during the update.', 'success':False}

                    # else:
                    if "sender_email" in given_keys:
                        given_keys = list(set(editing_details))
                        require_keys = ['sender_pwd']
                        missing_sender_pwd = verfify_keys_miss_or_not(require_keys, given_keys)
                        if missing_sender_pwd:
                            ret = {'message':f"The email '{missing_sender_pwd}' is not a valid email address.", "success":False}
                        
                        else:
                            #VERIFY GIVEN KEY IS VALID OR NOT
                            all_keys_list = ['_id', 'email_receivers','violation_report','analytics_types','timestamp', 'smtp_server', 'smtp_port', 'sender_email', 'sender_pwd']
                            # Check if all items in 'GIVE_ANALYTICS_SLNS' are present in 'LIST_ANALYTICS_SLNS' using list comprehension and all()
                            keys_not_existed = all(item in all_keys_list for item in given_keys)
                            ret = fun_edit_parameters(keys_not_existed, editing_details, given_keys, email_sender_data, id)
                            
                    else:
                        #VERIFY GIVEN KEY IS VALID OR NOT
                        all_keys_list = ['_id', 'email_receivers','violation_report','analytics_types','timestamp', 'smtp_server', 'smtp_port', 'sender_email', 'sender_pwd']
                        # Check if all items in 'GIVE_ANALYTICS_SLNS' are present in 'LIST_ANALYTICS_SLNS' using list comprehension and all()
                        keys_not_existed = all(item in all_keys_list for item in given_keys)
                        ret = fun_edit_parameters(keys_not_existed, editing_details, given_keys, email_sender_data, id)
                    

            else:
                ret={'success':False,'message':'You have missed these keys '+str(missing_key)+' to enter. please enter properly.'}

        else:
            ret = {'success':False, 'message':'Given mongo-id does not existed, please check it and enter.'}

    else:
        ret={'success':False,'message':'Given mongo-id is not valid, please enter properly.'}
    return ret


@app.route('/get_email_details', methods=['GET'])
@app.route('/get_email_details/<id>', methods=['GET'])
def get_email_details(id = None):
    ret = {'success': False, 'message':'something went wrong with get_email_details api'}
    editing_details = request.json

    email_sender_data = mongo.db.email_details.find()
    if email_sender_data:
        data = parse_json(email_sender_data)
        ret = {'success': True, 'message': data}

    else:
        ret = {'success': False, 'message': "Email sender details not there."}

    
    return ret


@app.route('/delete_email_detail', methods=['POST'])
def delete_email_detail():
    ret = {'success': False, 'message':'something went wrong with get_email_details api'}
    mongo_id = request.json
    print("MONGO ID:", mongo_id)

    #VERIFY REQUIRE HAS GIVEN OR NOT
    given_keys = list(set(mongo_id))
    require_keys = ['_id']
    missing_key = verfify_keys_miss_or_not(require_keys, given_keys)
    id =  mongo_id['_id']
    # print("Verify mongoid:---------------------------", ObjectId.is_valid(id))

    if ObjectId.is_valid(id) == True:
        email_sender_data = mongo.db.email_details.find_one({'_id':ObjectId(id)})
        print("email_sender_data:",email_sender_data)
        if email_sender_data != None:
            result = mongo.db.email_details.delete_one({'_id':ObjectId(id)})
            print("Given ID data:", email_sender_data)
            if result.deleted_count > 0:
                ret = {'message': 'Data successfully deleted.', 'success': True}

            else:
                return ret

        else:
            ret = {'success': False, 'message':'Given mongo-id has not existed, please give valid mongo-id.'}

    else:
        ret = {'success': False, 'message': 'Given mongo-id is not valid, please enter proporly.'}

    return ret


# # Get today's date
# today = date.today()

# # Get 1 day earlier
# yesterday = today - timedelta(days = 10)
# print("Yesterday:", yesterday)

# all_data = mongo.db.email_details.find({})
# require_data_ls = []
# for x_data in all_data:
#     # print("X_DATA:", x_data)
#     for given_time in x_data["timestamp"]:
#         # require_data = {"email_receivers":x_data["email_receivers"], "analytics":x_data["analytics_types"], "times":given_time, "email_sent_status":False}
#         require_data = {"email_receivers":x_data["email_receivers"], "analytics":x_data["analytics_types"], "times":given_time, "sender_email":x_data['sender_email'], "sender_pwd":x_data['sender_pwd'], "smtp_server":x_data["smtp_server"], "smtp_port":x_data["smtp_port"]}
#         require_data_ls.append(require_data)
#     # print("TRAIL RESULT:", require_data_ls)

# sorted_ls_data(require_data_ls, yesterday, today)
# send_email_attachment(require_data_ls)


if __name__ == '__main__':
    app.run(  host='0.0.0.0',port=5000,debug=True, threaded=True)