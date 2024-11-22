from Data_recieving_and_Dashboard.packages import *
alertemails = Blueprint('alertemails', __name__)






def get_new_slns_name(analytics_types):
    # print("ANALYTICS LIST:-------------", analytics_types)
    # Check if the specific values exist and replace them
    if 'ra' in analytics_types:
        if 'RA' not in analytics_types:
            analytics_types[analytics_types.index('ra')] = 'RA'

    if 'cr' in analytics_types:
        if 'CRDCNT' not in analytics_types:
            analytics_types[analytics_types.index('cr')] = 'CRDCNT'

    if 'ppe' in analytics_types:
        if 'PPE_TYPE1' not in analytics_types:
            analytics_types[analytics_types.index('ppe')] = 'PPE_TYPE1'

    if 'ppe_type1' in analytics_types:
        if 'PPE_TYPE1' not in analytics_types:
            analytics_types[analytics_types.index('ppe_type1')] = 'PPE_TYPE1'

        else:
            analytics_types.remove('ppe_type1')
    return analytics_types

def is_connected():
    try:
        # Attempt to connect to a public DNS server (e.g., Google's 8.8.8.8)
        socket.create_connection(("8.8.8.8", 53), timeout=0.5)
        return True
    except OSError:
        return False
    
def is_valid_smtp_port(server, port):
    if not is_connected():
        print("ERROR: No network connection.")
        return False
    
    try:
        with smtplib.SMTP(server, port) as smtp:
            # Successfully connected
            return True
        
    except gaierror as e:
        print("ERROR: Failed to resolve hostname:", e)
        res = e #"ERROR: Failed to resolve hostname:", e
        return res
    
    except ConnectionRefusedError as e:
        print("ERROR: Connection refused by the server:", e)
        res = e #"ERROR: Connection refused by the server:", e
        return res
    
    except Exception as e:
        print("ERROR: An unexpected error occurred:", e)
        res = e #"ERROR: An unexpected error occurred:", e
        return res
    
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


def is_valid_email(email):
    # Regular expression pattern to match a valid email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_boolean(value):
    return isinstance(value, bool)

def validate_email_recipients(email_recipients_dict):
    # Check if the "to" field is a list
    if isinstance(email_recipients_dict.get('to'), list):
        # Loop through each email in the "to" list
        for to_eml in email_recipients_dict['to']:
            if not is_valid_email(to_eml):
                return {'message': f"The to-email '{to_eml}' is not a valid email address.", "success": False} #"invalid_email": to_eml, 

        # If "cc" exists, check if it's a list
        if 'cc' in email_recipients_dict:
            if isinstance(email_recipients_dict['cc'], list):
                # Loop through each email in the "cc" list
                for cc_eml in email_recipients_dict['cc']:
                    if not is_valid_email(cc_eml):
                        return {'message': f"The cc-email '{cc_eml}' is not a valid email address.", "success": False} #"invalid_email": cc_eml,
            else:
                return {'message': "The cc-email is not in the correct format.", "success": False}

        # If "bcc" exists, check if it's a list
        if 'bcc' in email_recipients_dict:
            if isinstance(email_recipients_dict['bcc'], list):
                # Loop through each email in the "bcc" list
                for bcc_eml in email_recipients_dict['bcc']:
                    if not is_valid_email(bcc_eml):
                        return {'message': f"The bcc-email '{bcc_eml}' is not a valid email address.", "success": False} #, "invalid_email": bcc_eml
            else:
                return {'message': "The bcc-email is not in the correct format.", "success": False}

        # If everything is valid, return success
        return {'message': {'to':email_recipients_dict['to'], 'cc': email_recipients_dict['cc'], 'bcc': email_recipients_dict['bcc']}, "success": True}
        # return {'message': "All email addresses are valid.", "success": True}
    
    else:
        return {'message': "The to-email is not in the correct format.", "success": False}
    


@alertemails.route("/insert_email_details", methods=["POST"])
def insert_email_details():
    if True:
        ret = {"success": False, "message":"An unexpected error has occurred, please try again later"}
        jsonobject = request.json
        if jsonobject == None:  
            jsonobject = {}
        request_key_array=['email_receivers','violation_report','analytics_types','timestamp', 'smtp_server', 'smtp_port', 'sender_email', 'sender_pwd', 'department','require_smtp', 'report_template']
        jsonobjectarray= list(set(jsonobject))
        missing_key = verfify_keys_miss_or_not(request_key_array, jsonobjectarray)
        if not missing_key:
            output = verify_parameter_val(jsonobject)
            if output:
                ret = {'message': 'You have missed these parameters '+str(output)+' to enter. please enter properly.', 'success': False}
            else:
                if jsonobject['email_receivers'] == {}:
                    ret = {"message": 'You have missed recipients to enter in the emails. please enter properly.', 'success': False}
                else:
                    list_analytics_solns = ['WHEEL_COUNT','RA', 'ra', 'PPE', 'ppe', 'PPE_TYPE1', 'PPE_TYPE2', 'TC', 'tc', 'CR', 'CRDCNT', 'cr', 'Fire', 'Water', 'fire', 'water','smoke','Smoke', 'dust', 'Dust', 'Parking', 'PA', 'NO_Parking', 'NPA', 'parking','no_parking','Traffic_Jam','traffic_jam', 'Protection_Zone','protection_zone']
                    email_recipients = ['to', 'cc', 'bcc']
                    to_recipient = ['to']
                    all_email_receipients_keys = jsonobject['email_receivers'].keys()
                    # Convert the keys to a list if needed
                    to_recipient_shld_be = verfify_keys_miss_or_not(to_recipient, list(all_email_receipients_keys))
                    if not to_recipient_shld_be:
                        given_all_analytics_slns_list = jsonobject['analytics_types']
                        print("GIVEN ANALYTICS LIST:--------------------", given_all_analytics_slns_list)
                        if len(given_all_analytics_slns_list) != 0:
                            all_given_analytics_slns_exist = all(item in list_analytics_solns for item in given_all_analytics_slns_list)

                            all_given_email_recipients_keys_exist = all(item in email_recipients for item in list(all_email_receipients_keys))
                            print("********************************************** 1 ")
                            if all_given_analytics_slns_exist == True:
                                if all_given_email_recipients_keys_exist == True:
                                    ("********************************************** 2 ")
                                    email_recipients_values = verify_parameter_val(jsonobject['email_receivers'])
                                    if email_recipients_values:
                                        print("********************************************** 3 ")
                                        ret = {'message': 'Please enter values for '+str(email_recipients_values)+' these keys.', 'success': False}
                                    else:
                                        email_recipients_dict = jsonobject['email_receivers']
                                        if len(email_recipients_dict['to']) == 0:
                                            print("********************************************** 4 ")
                                            ret = {'message': 'Please enter value for "to" key, it should not be empty.', 'success': False}                                           
                                        else:
                                            print("********************************************** 5 ")
                                            if type(jsonobject['timestamp']) == list:
                                                given_sender_email = jsonobject['sender_email']
                                                if 'require_smtp' in jsonobject:
                                                    require_email = jsonobject['require_smtp']
                                                    if given_sender_email == None:
                                                        if require_email == True:
                                                            sender_mail = "safetyvoilation.dolvi@jsw.in" #"alertdocketrun@gmail.com" 
                                                            sender_password = "jcmgktdlczwsvzbd" #"pegu msgu pudd hqnt "
                                                            smtp_server_input = "smtp.office365.com" #"smtp.gmail.com"
                                                            smtp_port_input = 587
                                                        else:
                                                            sender_mail = "docketrun.alert.mail@gmail.com" #"alertdocketrun@gmail.com" 
                                                            sender_password = "ebmt ekfg ralb gnfk " #"pegu msgu pudd hqnt "
                                                            smtp_server_input = "smtp.gmail.com"
                                                            smtp_port_input = 587

                                                        jsonobject['sender_email'] = sender_mail
                                                        jsonobject['sender_pwd'] = sender_password
                                                        if is_valid_email(sender_mail):
                                                            # smtp_server_input = "smtp.gmail.com"
                                                            jsonobject['smtp_server'] = smtp_server_input
                                                            # smtp_port_input = 25 #587
                                                            jsonobject['smtp_port'] = smtp_port_input
                                                            # print("-----------email_recipients----------",email_recipients)
                                                            # print("type--------------",type(email_recipients))
                                                            # print("-------jsonobject['timestamp']------------",jsonobject['timestamp'])
                                                            jsonobject['scheduled_time']=jsonobject['timestamp']
                                                            # email_recipients['scheduled_time']=jsonobject['timestamp']
                                                            # if is_valid_smtp_port(smtp_server_input, smtp_port_input):
                                                            # fun_response = is_valid_smtp_port(smtp_server_input, smtp_port_input)
                                                            # if fun_response == True:
                                                            existed_data = mongo.db.email_details.find_one(jsonobject)
                                                            if existed_data:
                                                                ret = {'message':'this entered data already exist.', 'success': False}                                                            
                                                            else:
                                                                email_recipients_dict = jsonobject['email_receivers']
                                                                eml_validating_result = validate_email_recipients(email_recipients_dict)
                                                                if eml_validating_result["success"] == False:
                                                                    ret = eml_validating_result                                                                 
                                                                elif type(jsonobject['department']) == list:
                                                                    response = mongo.db.email_details.insert_one(jsonobject)
                                                                    if mongo.db.dummytest.find_one({'sender_mail':sender_mail}):
                                                                        pass
                                                                    else:
                                                                        mongo.db.dummytest.insert_one({'sender_mail':sender_mail,'sender_pwd':sender_password,"smtp_server_input": smtp_server_input, "smtp_port_input" : smtp_port_input})

                                                                    if response.acknowledged > 0:
                                                                        ret = {'message':'data inserted successfully.', 'success': True}
                                                                    else:
                                                                        ret = {"status":False, "message":"data not inserted."}
                                                                else:
                                                                    ret = {"status":False, "message":"given department is not valid format."}
                                                            # else:
                                                            #     ret = {"message":f"the SMTP port {smtp_port_input} for '{smtp_server_input}' is '{fun_response}'.", "success": False}    #{"message":f"the SMTP port {smtp_port_input} for '{smtp_server_input}' is invalid or cannot be reached.", "success": False}                                                    
                                                        else:
                                                            ret = {'message':f"the sender-email '{sender_mail}' is not a valid email address.", "success":False}                                                        
                                                    else:
                                                        ret = {'message':f"the sender-email '{given_sender_email}' is not a 'NULL'.", "success":False}
                                                else:
                                                    sender_mail = "docketrun.alert.mail@gmail.com" #"alertdocketrun@gmail.com" 
                                                    sender_password = "ebmt ekfg ralb gnfk " #"pegu msgu pudd hqnt "
                                                    smtp_server_input = "smtp.gmail.com"
                                                    smtp_port_input = 587
                                                    if given_sender_email == None:                                                        
                                                        jsonobject['sender_email'] = sender_mail
                                                        jsonobject['sender_pwd'] = sender_password
                                                        if is_valid_email(sender_mail):
                                                            # smtp_server_input = "smtp.gmail.com"
                                                            jsonobject['smtp_server'] = smtp_server_input
                                                            # smtp_port_input = 25 #587
                                                            jsonobject['smtp_port'] = smtp_port_input
                                                            # print("-----------email_recipients----------",email_recipients)
                                                            # print("type--------------",type(email_recipients))
                                                            # print("-------jsonobject['timestamp']------------",jsonobject['timestamp'])
                                                            jsonobject['scheduled_time']=jsonobject['timestamp']
                                                            # email_recipients['scheduled_time']=jsonobject['timestamp']
                                                            # if is_valid_smtp_port(smtp_server_input, smtp_port_input):
                                                            existed_data = mongo.db.email_details.find_one(jsonobject)
                                                            if existed_data:
                                                                ret = {'message':'this entered data already exist.', 'success': False}                                                            
                                                            else:
                                                                email_recipients_dict = jsonobject['email_receivers']
                                                                eml_validating_result = validate_email_recipients(email_recipients_dict)
                                                                if eml_validating_result["success"] == False:
                                                                    ret = eml_validating_result                                                                 
                                                                elif type(jsonobject['department']) == list:
                                                                    response = mongo.db.email_details.insert_one(jsonobject)
                                                                    if mongo.db.dummytest.find_one({'sender_mail':sender_mail}):
                                                                        pass
                                                                    else:
                                                                        mongo.db.dummytest.insert_one({'sender_mail':sender_mail,'sender_pwd':sender_password,"smtp_server_input": smtp_server_input, "smtp_port_input" : smtp_port_input})
                                                                    if response.acknowledged > 0:
                                                                        ret = {'message':'data inserted successfully.', 'success': True}
                                                                    else:
                                                                        ret = {"status":False, "message":"data not inserted."}
                                                                else:
                                                                    ret = {"status":False, "message":"given department is not valid format."}
                                                            # else:
                                                            #     ret = {"message":f"the SMTP port {smtp_port_input} for '{smtp_server_input}' is invalid or cannot be reached.", "success": False}                                                    
                                                        else:
                                                            ret = {'message':f"the sender-email '{sender_mail}' is not a valid email address.", "success":False}                                                        
                                                    else:
                                                        ret = {'message':f"the sender-email '{given_sender_email}' is not a 'NULL'.", "success":False}                                                
                                            else:
                                                ret = {"message":"timestamp is not the format", "success": False}                                            
                                else:
                                    ret = {'message':'given eamil receivers are not valid.', 'success': False}
                            else:
                                ret = {'message':'given all analytics solutions are not valid, please check it.', 'success': False}                        
                        else:
                            ret = {'message':'you had missed to give "analytics solutions", please check it.', 'success': False}
                    else:
                        ret = {'message': 'you have missed '+ str(to_recipient_shld_be) + 'to enter. Please enter properly.', 'success': False}
        else:
            ret={'success':False,'message':'you have missed these keys '+str(missing_key)+' to enter. please enter properly.'}

        return ret



def fun_edit_parameters(editing_details):
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$-----------", editing_details)
    ret = {'message': 'something went wrong in fun_edit_parameters.', 'success': True}
    if "timestamp" in editing_details.keys(): 
        timestamp_arr = editing_details['timestamp']

        if type(timestamp_arr) == list:
            if len(timestamp_arr) != 0:
                pass   
            else:
                return {"message":"Please enter the value for 'Timestamp', it should not be empty.", "success": False}
        else:
            return  {"message":"Timestamp is not the format", "success": False}
        
    if "email_receivers" in editing_details.keys():
        email_recipients_dict = editing_details['email_receivers']                            
        email_recipients_values = verify_parameter_val(email_recipients_dict)
        if email_recipients_values:
            return {'message': 'You have missed these parameters '+str(email_recipients_values)+' to enter. please enter properly.', 'success': False}
        
        else:
            email_receivers_val = validate_email_recipients(email_recipients_dict)
            if email_receivers_val["success"] != False:
                pass
        
            else:
                return email_receivers_val         

    if "analytics_types" in editing_details.keys():
        if type(editing_details["analytics_types"]) is list:
            given_all_analytics_slns_list = editing_details["analytics_types"]
            list_analytics_solns = ['RA', 'WHEEL_COUNT', 'ra', 'PPE', 'ppe','ppe_type1', 'PPE_TYPE1', 'PPE_TYPE2', 'TC', 'tc', 'CR', 'CRDCNT', 'cr', 'Fire', 'Water', 'fire', 'water','smoke','Smoke', 'dust', 'Dust', 'Parking', 'PA', 'NO_Parking', 'NPA', 'parking','no_parking','Traffic_Jam','traffic_jam', 'Protection_Zone','protection_zone']
            # ['RA', 'ra', 'PPE', 'ppe', 'TC', 'tc', 'CR', 'cr', 'Fire', 'Water', 'fire', 'water', 'dust', 'Dust', 'Parking', 'NO_Parking', 'parking','no_parking','Traffic_Jam','traffic_jam', 'Protection_Zone','protection_zone']
            all_given_analytics_slns_exist = all(item in list_analytics_solns for item in given_all_analytics_slns_list)
            if all_given_analytics_slns_exist == True:
                pass

            else:
                return {'message':'Given analytics-solutions are not valid.', 'success': False}
        else:
            return {"message":" 'analytics_types' is not the format.", "success": False}


    if "violation_report" in editing_details.keys():
        if is_boolean(editing_details['violation_report']):
            pass            
        else:
            ret = {'message':f"The given violation_report is not a boolean.", "success":False}  
            return ret

    if "department" in editing_details.keys():
        if type(editing_details['department']) == list:
            pass
        else:
            return  {'message':f"The given department type should be list.", "success":False}  
        
    return ret

def compare_data(editing_details, email_sender_data):
    differences = {}
    for key, value in editing_details.items():
        # print("email_sender_data[key]", email_sender_data[key])
        if key in email_sender_data and email_sender_data[key] != value:
            differences[key] = value
    del differences["_id"] 
    return differences


@alertemails.route('/edit_email_details', methods=['POST'])
def edit_email_details():
    ret = {'success': False, 'message':'something went wrong with edit_email_details api'}
    editing_details = request.json
    # print("EDITING DETAILS:", editing_details)
    if (editing_details != {}):
        given_keys = list(set(editing_details))
        # print("GIVEN KEYS:-----", given_keys)
        require_keys = ['_id']
        missing_key = verfify_keys_miss_or_not(require_keys, given_keys)        
        if not missing_key:
            id =  editing_details['_id']
            if ObjectId.is_valid(id) == True:
                email_sender_data = mongo.db.email_details.find_one({'_id':ObjectId(id)})
                #print("email_sender_data:",email_sender_data)
                # print("editing_details--------------------------", editing_details)
                compare_values_func = compare_data(editing_details, email_sender_data)
                # print("compare_values_func--------------------------", compare_values_func)
                if compare_values_func != {}:
                    ret = fun_edit_parameters(compare_values_func)
                    if ret['success'] != False:
                        if "timestamp" in compare_values_func.keys():
                            compare_values_func['scheduled_time'] = compare_values_func['timestamp']
                        result = mongo.db.email_details.update_one({'_id':ObjectId(id)},{"$set":compare_values_func})
                        # print("Response:", result.status())
                        if result.modified_count > 0:
                            ret = {'message': 'Data updated successfully.', 'success': True}
                            # print("--------------", result.modified_count > 0)
                        else:
                            existed_data = mongo.db.email_details.find_one(compare_values_func)
                            if existed_data:
                                ret = {'message':'no changes were made during the update.', 'success':False}
                            
            else:
                ret={'success':False,'message':'Given mongo-id is not valid, please enter properly.'}            
        else:
            ret={'success':False,'message':'You have missed these keys '+str(missing_key)+' to enter. please enter properly.'}
    else:
        ret={'success':False,'message':'Give proper parameters to edit the email-details.'}        
    return ret


@alertemails.route('/get_alert_emaildata', methods=['GET'])
@alertemails.route('/get_alert_emaildata/<id>', methods=['GET'])
def test_email(id=None):
    result = {'msg':'something went wrong with get_email_details api'}
    try:
        if id is not None:
            test_email_data = mongo.db.email_details.find_one({"_id":ObjectId(id)}, {"_id":1, "analytics_types":1, "department":1, "email_receivers":1, "timestamp":1,"violation_report":1})
            test_email_data["analytics_types"] = get_new_slns_name(test_email_data["analytics_types"])
            print("TEST EMAIL DATA:-------------", test_email_data)
            if test_email_data:
                result = {'success':True, 'message':parse_json(test_email_data)}
            else:
                result = {'success':False, 'message':'email sender details not there.'}
        else:
            test_email_data = mongo.db.email_details.find({},{"_id":1, "analytics_types":1, "department":1, "email_receivers":1, "timestamp":1,"violation_report":1})
            all_email_details_data = []
            for x_data in test_email_data:
                x_data["analytics_types"] = get_new_slns_name(x_data["analytics_types"])
                all_email_details_data.append(x_data)
            # print("test_email_data:----------------------------", all_email_details_data) #test_email_data)
            if test_email_data:
                result = {'success':True, 'message':parse_json(all_email_details_data)} #test_email_data)}
            else:
                result = {'success':False, 'message':'email sender details not there.'}

    except ( 
                pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
                pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
                pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
                pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
                pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
                pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
                pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
                pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
                pymongo.errors.WriteError) as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_panel_data3 1", str(error), " ----time ---- ", now_time_with_time()]))
        result['message'] = " ".join(["something error has occered in api", str(error)])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        result['message'] = str(error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_panel_data3 2", str(error), " ----time ---- ", now_time_with_time()]))
    return result


@alertemails.route('/departments_list', methods=['GET'])
def departments_list():
    ret = {'success': False, 'message': 'Something went wrong with the get departments_list API.'}    
    try:
        department_aggregation = mongo.db.ppera_cameras.aggregate([
            {'$match': {'camera_status': True}},  
            {'$group': {'_id': '$department'}}   
        ])
        department_list = [dep['_id'] for dep in department_aggregation]
        if department_list:
            ret = {'success': True, 'message': department_list}
        else:
            ret['message'] = 'No departments found.'    
    except Exception as e:
        ret['message'] = str(e) 
    return parse_json(ret)

@alertemails.route('/delete_email_detail', methods=['POST'])
@alertemails.route('/delete_email_detail/<id>', methods=['GET'])
def delete_email_detail(id=None):
    ret = {'success': False, 'message':'something went wrong with delete_email_detail api'}
    if request.method == 'GET':
        if ObjectId.is_valid(id) == True:
            email_sender_data = mongo.db.email_details.find_one({'_id':ObjectId(id)})
            if email_sender_data != None:
                result = mongo.db.email_details.delete_one({'_id':ObjectId(id)})
                if result.deleted_count > 0:
                    ret = {'message': 'Data successfully deleted.', 'success': True}
                else:
                    return ret
            else:
                ret = {'success': False, 'message':'given mongo-id has not existed, please give valid mongo-id.'}
        else:
            ret = {'success': False, 'message': 'given mongo-id is not valid, please enter proporly.'}
    elif request.method == 'POST':
        mongo_id = request.json
        if mongo_id == None:  
            mongo_id = {}
        given_keys = list(set(mongo_id))
        require_keys = ['_id']
        missing_key = verfify_keys_miss_or_not(require_keys, given_keys)
        if not missing_key:
            id =  mongo_id['_id']
            if ObjectId.is_valid(id) == True:
                email_sender_data = mongo.db.email_details.find_one({'_id':ObjectId(id)})
                if email_sender_data != None:
                    result = mongo.db.email_details.delete_one({'_id':ObjectId(id)})
                    if result.deleted_count > 0:
                        ret = {'message': 'Data successfully deleted.', 'success': True}
                    else:
                        return ret
                else:
                    ret = {'success': False, 'message':'given mongo-id has not existed, please give valid mongo-id.'}
            else:
                ret = {'success': False, 'message': 'given mongo-id is not valid, please enter proporly.'}            
        else:
            ret={'success':False,'message':'You have missed these keys '+str(missing_key)+' to enter. please enter properly.'}        
    return ret