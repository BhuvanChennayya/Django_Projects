from Data_recieving_and_Dashboard.packages import *
from bson import json_util

use = Blueprint("use", __name__,template_folder='templates',url_prefix="/user")

api = Api(use)


 #------------------media extensions--------------------------------------------------------------------
UPLOAD_FOLDER = 'static/uploads/profile_pics'    #media storing folder
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}      #image extension
ALLOWED_EXTENSIONS1 = {'mp4', 'mkv', 'avi'}       #video extension

 #-----------------database connection mongodb-----------------------------------------------------------
# mongo = pymongo.MongoClient(
#     host="localhost", 
#     port=27017,
#     serverSelectionTimeoutMS = 1000
#     )
# db = mongo.DOCKETRUNDB    # login = database name 
# mongo.server_info()

def encode_to_ascii(text):
    encoded_text = ','.join(str(ord(char)) for char in text)
    return encoded_text


def decode_from_ascii(encoded_text):
    if not encoded_text:
        return ""  # Return an empty string if encoded_text is empty
    try:
        decoded_text = ''.join(chr(int(code)) for code in encoded_text.split(',') if code.strip())
        return decoded_text
    except ValueError:
        return ""

# def decode_from_ascii(encoded_text):
#     decoded_text = ''.join(chr(int(code)) for code in encoded_text.split(','))
#     return decoded_text


def FUTURETIMEGIVENMINUTES(minutes=15):
    # print("datetime.today()====",datetime.today())
    future_time = datetime.today() + timedelta(minutes=minutes)
    # print("future_time===========",future_time)
    now = str(datetime.strptime(future_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    # print("now==================",now)
    return now


def now_time_with_time():
    now = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    return now

def parse_json(data):
    return json.loads(json_util.dumps(data))

# mongo.db.user.create_index([('empid', 1), ('department', 1), ('company', 1), ('location', 1)], unique=True) 


#----------------------file extension support----------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1
#--------------------------password encryption----------------------------------------------------------
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


#-------------------sign up-------------------------------------------------------------------------------
@use.route("/signup", methods=['POST'])
def signup():
    required_params = ['first_name','last_name', 'adminid', 'company', 'location', 'department',
    'email', 'password', 'contact','admin_email','empid']
    required_params1 = ['profile_pic']
    data = request.form
    data1 = request.files
    
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})

    missing_params1 = [param for param in required_params1 if param not in data1]
    if missing_params1:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params1)}', 'success': False})
    
    first_name = data['first_name']
    last_name = data['last_name']
    empid = data['empid']
    company = data['company']
    location = data['location']
    department = data['department']
    profile_pic = data1['profile_pic']
    email = data["email"]
    password = data["password"]
    password= decode_from_ascii(password)
    adminid = data["adminid"]
    contact = data["contact"]
    admin_email = data.get('admin_email')
    admin = db.admin.find_one({'email': admin_email, 'adminid': adminid})

    print("empid=",empid)
    # validate first name
    if not firstname_regex.match(first_name):
        return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"Success":False})   

    # validate last name
    elif not firstname_regex.match(last_name):
        return jsonify({"message":'last name should be 3 to 10 characters only alphabets',"Success":False})

    # validate company name
    elif not company_regex.match(company):
        return jsonify({"message":'company should be 3 to 10 characters only alphabets',"Success":False})  

    # validate department name
    elif not company_regex.match(department):
        return jsonify({"message":'department should be 3 to 10 characters only alphabets',"Success":False})

    # validate location
    elif not firstname_regex.match(location):
        return jsonify({"message":'location should be 3 to 10 characters only alphabets',"Success":False})          

    # validate adminid
    elif not diffid_regex.match(empid):
        return jsonify({"message":'employee id should be 1 to 10 numeric only',"Success":False})          
 
    # Validate password
    elif not validate_password(password):
        return jsonify({"message":'Password must contain 8 to 16 characters,including at least alphanumeric,1 captial letter and special characters',"Success":False})    

    # Validate email
    elif not email_regex.match(email):
        return jsonify({"message": "Invalid email","Success":False})
    # Validate contact
    elif not contact_regex.match(contact):
        return jsonify({"message": "contact number must contain 10 numbers only","Success":False})
    # checking existing email
    elif mongo.db.user.find_one({"email": email}):
        return jsonify({"message": "Email already exists","Success":False})

    elif not db.admin.find_one({"adminid": adminid}):
        return jsonify({"message": "admin id doess not exist","Success":False})    

    elif not db.admin.find_one({"email": admin_email}):
        return jsonify({"message": "admin email does not found","Success":False})

    elif not admin:
        return jsonify({"message":"Admin email and admin id do not match .","Success":False})
        
    # elif mongo.db.user.find_one({'empid': empid, 'company': company, 'department':department,'location': location}):
    #     return {'message': 'empid , company name,and location already exists',"success":False}, 409 
    
   # Check for duplicate records
    if mongo.db.user.find_one({'empid': empid, 'company': company, 'department': department, 'location': location}):
        return jsonify({'message': 'empid, company name, department, and location already exists', 'success': False})      
    #----------------adding profile pic----------------
    if profile_pic:
        if profile_pic.filename == '':
            return jsonify({'message': 'File not selected',"success":False})

        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)  # Create the upload folder if it doesn't exist
            profile_pic.save(os.path.join(upload_folder, filename))
            
        else:
            return jsonify({"message": "Selected file is not supported","success":False})   
    else: 
        filename = None    
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pwd_hash = generate_password_hash(password)
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    # verify email token generate
    # token = s.dumps(email, salt='email-confirmation-key')
    # save user information in the database
    mongo.db.user.insert_one({                                   #-------user is collection of database
        "first_name": first_name,
        "last_name": last_name,
        "empid": empid,
        "company" : company,
        "location" :location,
        "department" : department,
        "profile_pic" : filename,
        "email": email,
        "password": hashed_password,
        "contact": contact,
        "adminid" : adminid,
        "admin_email": admin_email,

        # "token": token,
        "created_at": created_at,
        # "_verify":False
    })
    return jsonify({'message':'user registered successfully','success':True})  

#-------------------------------user login--------------------------------------------
@use.post("/login")
def login():
    required_params = ['email','password','token']
    jwtoken = request.headers.get('Authorization')
    print("Authorization=============================",jwtoken)
    # data = request.form
    data = request.json
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    email = data["email"]
    password = data["password"]
    password= decode_from_ascii(password)
    token = data['token']
    userdata = mongo.db.user.find_one({"email": email})

    if not userdata:
        return jsonify({"message": "Sign up before login", "success": False})

    if not check_password(password, userdata["password"]):
        return jsonify({"message": "given password is not matching.", "success": False})
    
    if token == None or token =='':
        return jsonify({"message": "invalid token please give proper token.", "success": False})
    if token != userdata["token"]:
        return jsonify({"message": "invalid token please give proper token.", "success": False})
    
    CampareTime = now_time_with_time()
    if 'expire' in userdata:
        if type(userdata['expire']) == str :
            if userdata['expire']<=CampareTime: 
                if check_password(password, userdata["password"] ):
                    if userdata:
                        minutes = 180
                        stringfuturetime = FUTURETIMEGIVENMINUTES(minutes)
                        # print("now_time_with_time()======================",stringfuturetime)
                        expire = datetime.utcnow() + timedelta(minutes=minutes)
                        # print("===expire====",expire)
                        future_time = datetime.today() + timedelta(minutes=minutes)
                        # print('future_time==============',future_time)
                        payload = {
                            'email': email,
                            # 'exp':future_time
                            'exp': expire
                            }
                        selectedpages = None
                        if 'selectedpages' in userdata:
                            selectedpages = userdata['selectedpages']

                        jwtoken = jwt.encode(payload, "jwtsecretkey","HS256")
                        mongo.db.userloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                        mongo.db.user.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                        return jsonify({'jwtoken': jwtoken, 'message': 'successful logged in', 'success': True,'selectedpages':selectedpages})
                        
                    else:
                        return jsonify({'message' : 'wrong credentials',"success":False})

                else:        
                    return jsonify({'message' : 'password is incorrect',"success":False})
            else:
                #'email'
                selectedpages = None
                if 'selectedpages' in userdata:
                    selectedpages = userdata['selectedpages']
                FINDLOGDATA = mongo.db.userloginlog.find_one({"email":email},sort=[("_id", pymongo.DESCENDING)])
                if FINDLOGDATA is not None:
                    print("====FINDLOGDATA===",FINDLOGDATA)
                    if 'browser' in FINDLOGDATA and 'systemid' in FINDLOGDATA:
                        return jsonify({'message' : 'already logged in browser {0} in system {1}'.format(FINDLOGDATA['browser'],FINDLOGDATA['systemid']),'jwtoken': userdata['jwtoken'],"success":False,'selectedpages':selectedpages})
                    else:
                        return jsonify({'message' : 'already logged in, please confirm do you want logout in other device.','jwtoken': userdata['jwtoken'],"success":False,'selectedpages':selectedpages})
                else:
                    return jsonify({'message' : 'already logged in, please confirm do you want logout in other device.','jwtoken': userdata['jwtoken'],"success":False,'selectedpages':selectedpages})
        elif userdata['expire'] == None:
            if check_password(password, userdata["password"] ):
                if userdata:
                    minutes = 180
                    stringfuturetime = FUTURETIMEGIVENMINUTES(minutes)
                    # print("now_time_with_time()======================",stringfuturetime)
                    expire = datetime.utcnow() + timedelta(minutes=minutes)
                    # print("===expire====",expire)
                    future_time = datetime.today() + timedelta(minutes=minutes)
                    # print('future_time==============',future_time)
                    payload = {
                        'email': email,
                        # 'exp':future_time
                        'exp': expire
                        }      
                    selectedpages = None
                    if 'selectedpages' in userdata:
                        selectedpages = userdata['selectedpages']             
                    jwtoken = jwt.encode(payload, "jwtsecretkey","HS256")
                    mongo.db.userloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                    mongo.db.user.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                    return jsonify({'jwtoken': jwtoken, 'message': 'successful logged in', 'success': True,'selectedpages':selectedpages})
                    
                else:
                    return jsonify({'message' : 'wrong credentials',"success":False})
            else:        
                return jsonify({'message' : 'password is incorrect',"success":False})
        else:
            return jsonify({'message' : 'expire time format is not correct.',"success":False})

        
    else:
        if check_password(password, userdata["password"] ):
            if userdata:
                minutes = 180
                stringfuturetime = FUTURETIMEGIVENMINUTES(minutes)
                # print("now_time_with_time()======================",stringfuturetime)
                expire = datetime.utcnow() + timedelta(minutes=minutes)
                # print("===expire====",expire)
                future_time = datetime.today() + timedelta(minutes=minutes)
                # print('future_time==============',future_time)
                payload = {
                    'email': email,
                    # 'exp':future_time
                    'exp': expire
                    }
                selectedpages = None
                if 'selectedpages' in userdata:
                    selectedpages = userdata['selectedpages']    

                jwtoken = jwt.encode(payload, "jwtsecretkey","HS256")
                mongo.db.userloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                mongo.db.user.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                return jsonify({'jwtoken': jwtoken, 'message': 'successful logged in', 'success': True,'selectedpages':selectedpages})
            else:
                return jsonify({'message' : 'wrong credentials',"success":False})
        else:        
            return jsonify({'message' : 'password is incorrect',"success":False})

@use.post('/userloginlogdetails')
def USLOgDEtails():
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.userloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    # if 1:
    if Sessiontime is not None:
        jwtoken = request.headers.get('Authorization')
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})  

        try:
            jwtoken= jwtoken.split(" ")[1]
            TOKENQuery = {'jwtoken':  jwtoken}
            data = request.json
            print("=====data======",data)
            TOKENDEtails = mongo.db.userloginlog.find_one(TOKENQuery)
            if TOKENDEtails is not None:
                print("TOKENDEtails===",TOKENDEtails)
                TOKENDEtails = parse_json(TOKENDEtails)
                #( {'jwtoken':  jwtoken}, {'$set': data})   
                mongo.db.userloginlog.update_one( {'jwtoken':  jwtoken}, {'$set': data}) 
                return jsonify({"message":"log updated successfully","success":True})
            else:
                return jsonify({"message":'please login once again',"success":False})

              
        except jwt.ExpiredSignatureError as error:
            print("authorization token has expired. please log in again.")
            return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

        except jwt.ImmatureSignatureError as error:
            print("token is not yet valid")
            return jsonify({'message': 'token is not yet valid',"success":False})

        except jwt.InvalidIssuerError as error:
            print("Invalid issuer")
            return jsonify({'message': 'invalid issuer',"success":False})

        except jwt.InvalidAudienceError:
            print("Invalid audience")
            return jsonify({'message': 'invalid audience',"success":False})

        except jwt.InvalidAlgorithmError:
            print("Invalid algorithm")
            return jsonify({'message': 'invalid algorithm',"success":False})

        except jwt.MissingRequiredClaimError:
            print("Missing required claim")
            return jsonify({'message': 'missing required claim',"success":False})
        
        except (jwt.InvalidTokenError, KeyError):
            return jsonify({'message': 'Invalid authorization token',"success":False})

        except Exception as e:
            print("JWT error:", e)
            return jsonify({'message': str(e),"success":False})
    else:
        return jsonify({'message': "session expired, please login once again","success":False})
    

#-------------view user profile-------------------------------------------------------------
@use.route('/profile', methods=['GET','POST'])
def admin_profile():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.userloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    # if 1:
    if  request.method == 'POST':
        print()
        required_params = ['activity']
        data= request.json
        # Check if all required parameters are present
        missing_params = [param for param in required_params if param not in data]
        if missing_params:
            return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})

        activity = data['activity']
        # print("--------activity======",activity)
        # print("--------activity======",str(activity))
        if activity == 'true':
            if Sessiontime is not None:
                if not jwtoken:
                    return jsonify({'message': 'missing authorization token',"success":False})  

                try:
                    # print('JSEKKK',jwtoken)
                    # if admindata is not None:
                    jwtoken = jwtoken.split(" ")[1]
                    decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
                    # print("decoded_token====",decoded_token)
                    email = decoded_token['email']
                    admin = mongo.db.user.find_one({'email': email})
                    if not admin:
                        return jsonify({'message': 'admin details not found',"success":False})  
                    if admin['jwtoken'] == 0:
                        return jsonify({'message': 'admin already logged out',"success":False})  


                    minutes = 180
                    stringfuturetime = FUTURETIMEGIVENMINUTES(minutes)
                    # print("now_time_with_time()======================",stringfuturetime)
                    expire = datetime.utcnow() + timedelta(minutes=minutes)
                    # print("===expire====",expire)
                    future_time = datetime.today() + timedelta(minutes=minutes)
                    # print('future_time==============',future_time)
                    payload = {
                        'email': email,
                        # 'exp':future_time
                        'exp': expire
                        }
                    jwtoken = jwt.encode(payload, "jwtsecretkey","HS256")
                    mongo.db.userloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                    mongo.db.user.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                    
                    return jsonify({'message':parse_json(admin) ,"success":True })

                except jwt.ExpiredSignatureError as error:
                    print("authorization token has expired. please log in again.")
                    return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

                except jwt.ImmatureSignatureError as error:
                    print("token is not yet valid")
                    return jsonify({'message': 'token is not yet valid',"success":False})

                except jwt.InvalidIssuerError as error:
                    print("Invalid issuer")
                    return jsonify({'message': 'invalid issuer',"success":False})

                except jwt.InvalidAudienceError:
                    print("Invalid audience")
                    return jsonify({'message': 'invalid audience',"success":False})

                except jwt.InvalidAlgorithmError:
                    print("Invalid algorithm")
                    return jsonify({'message': 'invalid algorithm',"success":False})

                except jwt.MissingRequiredClaimError:
                    print("Missing required claim")
                    return jsonify({'message': 'missing required claim',"success":False})
                
                except (jwt.InvalidTokenError, KeyError):
                    return jsonify({'message': 'Invalid authorization token',"success":False})

                except Exception as e:
                    print("JWT error:", e)
                    return jsonify({'message': str(e),"success":False})
            else:
                return jsonify({'message': "session expired, please login once again","success":False})
        elif activity =='false':
            if Sessiontime is not None:
                if not jwtoken:
                    return jsonify({'message': 'missing authorization token',"success":False})  

                try:
                    # print('JSEKKK',jwtoken)
                    # if admindata is not None:
                    jwtoken = jwtoken.split(" ")[1]
                    decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
                    # print("decoded_token====",decoded_token)
                    email = decoded_token['email']
                    admin = mongo.db.user.find_one({'email': email})
                    if not admin:
                        return jsonify({'message': 'admin details not found',"success":False})  
                    if admin['jwtoken'] == 0:
                        return jsonify({'message': 'admin already logged out',"success":False})  
                    
                    return jsonify({'message':parse_json(admin) ,"success":True })

                except jwt.ExpiredSignatureError as error:
                    print("authorization token has expired. please log in again.")
                    return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

                except jwt.ImmatureSignatureError as error:
                    print("token is not yet valid")
                    return jsonify({'message': 'token is not yet valid',"success":False})

                except jwt.InvalidIssuerError as error:
                    print("Invalid issuer")
                    return jsonify({'message': 'invalid issuer',"success":False})

                except jwt.InvalidAudienceError:
                    print("Invalid audience")
                    return jsonify({'message': 'invalid audience',"success":False})

                except jwt.InvalidAlgorithmError:
                    print("Invalid algorithm")
                    return jsonify({'message': 'invalid algorithm',"success":False})

                except jwt.MissingRequiredClaimError:
                    print("Missing required claim")
                    return jsonify({'message': 'missing required claim',"success":False})
                
                except (jwt.InvalidTokenError, KeyError):
                    return jsonify({'message': 'Invalid authorization token',"success":False})

                except Exception as e:
                    print("JWT error:", e)
                    return jsonify({'message': str(e),"success":False})
            else:
                return jsonify({'message': "session expired, please login once again","success":False})
        else:
            return jsonify({'message': "session expired, please login once again","success":False})
    elif  request.method == 'GET':
        if Sessiontime is not None:
            if not jwtoken:
                return jsonify({'message': 'missing authorization token',"success":False})  

            try:
                # print('JSEKKK',jwtoken)
                # if admindata is not None:
                jwtoken = jwtoken.split(" ")[1]
                decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
                # print("decoded_token====",decoded_token)
                email = decoded_token['email']
                admin = mongo.db.user.find_one({'email': email})
                if not admin:
                    return jsonify({'message': 'admin details not found',"success":False})  
                if admin['jwtoken'] == 0:
                    return jsonify({'message': 'admin already logged out',"success":False})  
                
                return jsonify({'message':parse_json(admin) ,"success":True })

            except jwt.ExpiredSignatureError as error:
                print("authorization token has expired. please log in again.")
                return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

            except jwt.ImmatureSignatureError as error:
                print("token is not yet valid")
                return jsonify({'message': 'token is not yet valid',"success":False})

            except jwt.InvalidIssuerError as error:
                print("Invalid issuer")
                return jsonify({'message': 'invalid issuer',"success":False})

            except jwt.InvalidAudienceError:
                print("Invalid audience")
                return jsonify({'message': 'invalid audience',"success":False})

            except jwt.InvalidAlgorithmError:
                print("Invalid algorithm")
                return jsonify({'message': 'invalid algorithm',"success":False})

            except jwt.MissingRequiredClaimError:
                print("Missing required claim")
                return jsonify({'message': 'missing required claim',"success":False})
            
            except (jwt.InvalidTokenError, KeyError):
                return jsonify({'message': 'Invalid authorization token',"success":False})

            except Exception as e:
                print("JWT error:", e)
                return jsonify({'message': str(e),"success":False})
        else:
            return jsonify({'message': "session expired, please login once again","success":False})
    else:
        return jsonify({'message': "session expired, please login once again","success":False})


#-----------------------------logout------------------------------------------------------------
@use.route('/logout', methods=['GET'])
def logout():
    jwtoken = request.headers.get('Authorization')
    print("------jwtoken---",jwtoken)
    if not jwtoken:
        return jsonify({'message': 'missing authorization token',"success":False})   
    # if 1:
    try:
        jwtoken = jwtoken.split(" ")[1]
        print("-------------jwtoken=========",jwtoken)
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        user = mongo.db.user.find_one({'email': email})
        if not user:
            return jsonify({'message': 'user not found',"success":False})

        mongo.db.user.update_one({'email':email},{"$set": {'jwtoken':0,'expire':None}})
        return jsonify({'message': 'logged out successfully',"success":True})
    except jwt.ExpiredSignatureError as error:
        try:
            admin = mongo.db.user.find_one({'jwtoken': jwtoken})
            if not admin:
                return jsonify({'message': 'Admin not found',"success":False})
            mongo.db.user.update_one({'jwtoken': jwtoken},{"$set": {'jwtoken':0,'expire':None}})
            return jsonify({'message': 'Logged out successfully',"success":True})
        except Exception as error :

            print("authorization token has expired. please log in again.")
            return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

        # print("authorization token has expired. please log in again.")
        # return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

    except jwt.ImmatureSignatureError as error:
        print("token is not yet valid")
        return jsonify({'message': 'token is not yet valid',"success":False})

    except jwt.InvalidIssuerError as error:
        print("Invalid issuer")
        return jsonify({'message': 'invalid issuer',"success":False})

    except jwt.InvalidAudienceError:
        print("Invalid audience")
        return jsonify({'message': 'invalid audience',"success":False})

    except jwt.InvalidAlgorithmError:
        print("Invalid algorithm")
        return jsonify({'message': 'invalid algorithm',"success":False})

    except jwt.MissingRequiredClaimError:
        print("Missing required claim")
        return jsonify({'message': 'missing required claim',"success":False})
    
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'invalid authorization token',"success":False})   

#---------------------change password---------------------------------------------------------------------
@use.route('/changepassword', methods=['POST'])
def change():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.userloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    # if 1:
    if Sessiontime is not None:
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})   
        try:
            jwtoken = jwtoken.split(" ")[1]
            decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
            email = decoded_token['email']
            admin = mongo.db.user.find_one({'email': email,'jwtoken':jwtoken})
            if not admin:
                return jsonify({'message': 'user details not found',"success":False})    
            
            if admin['jwtoken'] == 0:
                return jsonify({'message': 'user already logged out',"success":False})  
            if admin:
                required_params = ['current_password','new_password','confirm_password']
                data = request.json
                # Check if all required parameters are present
                missing_params = [param for param in required_params if param not in data]
                if missing_params:
                    return jsonify({'message': f'missing parameters: {", ".join(missing_params)}', 'success': False})
                current_password = data['current_password']
                current_password= decode_from_ascii(current_password)
                new_password = data['new_password']
                new_password= decode_from_ascii(new_password)
                confirm_password = data['confirm_password']
                confirm_password= decode_from_ascii(confirm_password)
            
                if not bcrypt.checkpw(current_password.encode('utf-8'), admin['password'].encode('utf-8')):
                    return jsonify({"message":'current password is incorrect',"success":False})

                if not validate_password(new_password):
                    return jsonify({"message":'password must contain 8 to 16 characters at least 1, including alphanumeric, 1 capital letter and special characters',"success":False})
        
                if new_password != confirm_password:
                    return jsonify({'message': 'new password and confirm password do not match',"success":False})       
            
                hashed_password = hash_password(new_password)
                mongo.db.user.update_one({'email': email},{'$set':{'password':hashed_password}})
                
                return jsonify({"message": "password updated successfully","success":True})   
            else : 
                return jsonify({"message": "enter all required fileds","success":False})    
        except jwt.ExpiredSignatureError as error:
            print("authorization token has expired. please log in again.")
            return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

        except jwt.ImmatureSignatureError as error:
            print("token is not yet valid")
            return jsonify({'message': 'token is not yet valid',"success":False})

        except jwt.InvalidIssuerError as error:
            print("Invalid issuer")
            return jsonify({'message': 'invalid issuer',"success":False})

        except jwt.InvalidAudienceError:
            print("Invalid audience")
            return jsonify({'message': 'invalid audience',"success":False})

        except jwt.InvalidAlgorithmError:
            print("Invalid algorithm")
            return jsonify({'message': 'invalid algorithm',"success":False})

        except jwt.MissingRequiredClaimError:
            print("Missing required claim")
            return jsonify({'message': 'missing required claim',"success":False})
        
        except (jwt.InvalidTokenError, KeyError):
            return jsonify({'message': 'invalid authorization token',"success":False})

        except Exception as e:
            print("JWT error:", e)
            return jsonify({'message': str(e),"success":False})
    else:
        return jsonify({'message': "session expired, please login once again","success":False})
    
#----------------forgot password---------------------------------------------------------------------------
@use.route('/forgot_password', methods=['POST'])
def forgot_password():
    required_params = ['email']
    forgot = request.form
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in forgot]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    
    if request.method == 'POST':
        # Get the user's email from the request
        email = forgot['email']
        # Check if the email exists in the database
        user = mongo.db.user.find_one({'email': email})
        if not user:
            return jsonify({"error": 'Email not found', "success": False})
        # Send the OTP to the user's email
        # user_send_reset_password_otp(email)
        return jsonify({"message": "OTP sent to email", "success": True})
        

   

#--------------------reset password--------------------------------------------------------------------------
@use.route('/reset_password', methods=['GET', 'POST'])
# def reset_password(rtoken):
def reset_password():
    if request.method == 'POST':
        # Get the new password from the request
        data = request.form
        password = data['password']
        password= decode_from_ascii(password)
        confirm_password = data['confirm_password']
        email = data.get('email')

        if password != confirm_password:
            return jsonify({"message": 'Passwords do not match', "Success": False})

        if not validate_password(password):
            return jsonify({"message": 'Password must contain 8 to 16 characters, at least 1 alphanumeric, 1 capital letter, and 1 special character', "Success": False})    

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Retrieve the user based on the email saved in the OTP verification step
        user = mongo.db.user.find_one({'email': email})
        if not user:
            return jsonify({"error": 'User not found', "success": False})

        # Update the user's password in the database
        mongo.db.user.update_one({'email': email}, {'$set': {'password': hashed_password}})

        # Optionally, you can also remove the reset_token from the user's document
        # mongo.db.user.update_one({'_id': user['_id']}, {'$unset': {'reset_token': ''}})

        return jsonify({"message": "Password updated", "success": True})
       

#------------------------update user profile------------------------------------------------------------------
@use.route('/update_user_profile',methods=['PUT','PATCH','POST'])
def update_user():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.userloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    if Sessiontime is not None:
        tokens = mongo.db.user.find_one({"jwtoken":jwtoken})
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})    

        try:
            jwtoken = jwtoken.split(" ")[1]
            decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
            email = decoded_token['email']
            admin = mongo.db.user.find_one({'email': email,'jwtoken':jwtoken})
            if not admin:
                return jsonify({'message': 'admin not found',"success":False})   
            data = request.json    
            # data = request.form
            # data1 = request.files
            print("data-----update data ===",data)
            
            update_fields = {}
            if data:
                if 'fullname' in data:
                    if not re.match(r"^[a-zA-Z]{3,10}$", data['fullname']):
                        return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"success":False})   
                    update_fields['fullname'] = data['fullname']   
                if 'contact' in data:
                    if not re.match(r"^[0-9]{10}$", data['contact']):
                        return jsonify({"message": "Invalid contact number","success":False})
                    update_fields['contact'] = data['contact']   
                if 'department' in data:
                    if data['department'] is None:
                        return jsonify({"message": "department name is not given or given as empty string.","success":False})
                    update_fields['department'] = data['department']  

                print('=====update_fields===',update_fields)

                mongo.db.user.update_one({"email":email}, {"$set": update_fields})
                return jsonify({"message": "updated successfully ","updated":update_fields,"success":True}) 
            else:
                return jsonify({'message': 'please enter input fields properly.',"success":False})   


        except jwt.ExpiredSignatureError as error:
            print("authorization token has expired. please log in again.")
            return jsonify({'message': 'jwt authorization token has expired. please log in again.',"success":False})       

        except jwt.ImmatureSignatureError as error:
            print("token is not yet valid")
            return jsonify({'message': 'token is not yet valid',"success":False})

        except jwt.InvalidIssuerError as error:
            print("Invalid issuer")
            return jsonify({'message': 'invalid issuer',"success":False})

        except jwt.InvalidAudienceError:
            print("Invalid audience")
            return jsonify({'message': 'invalid audience',"success":False})

        except jwt.InvalidAlgorithmError:
            print("Invalid algorithm")
            return jsonify({'message': 'invalid algorithm',"success":False})

        except jwt.MissingRequiredClaimError:
            print("Missing required claim")
            return jsonify({'message': 'missing required claim',"success":False})
        
        except (jwt.InvalidTokenError, KeyError):
            return jsonify({'message': 'Invalid authorization token',"success":False})

        except Exception as e:
            print("JWT error:", e)
            return jsonify({'message': str(e),"success":False}) 
    else:
        return jsonify({'message': "session expired, please login once again","success":False})
    # jwtoken = request.headers.get('Authorization')
    # if not jwtoken:
    #     return jsonify({'message': 'Missing authorization token',"success":False})   

    # try:
    #     jwtoken = jwtoken.split(" ")[1]
    #     decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
    #     email = decoded_token['email']
    #     user = mongo.db.user.find_one({'email': email,'jwtoken':jwtoken})
    #     if not user:
    #         return jsonify({'message': 'user not found',"success":False})     
    #     data = request.form
    #     data1 = request.files 
    #     update_fields = {}
    #     if data:
    #         # Validate contact
    #         if 'first_name' in data:
    #             if not re.match(r"^[a-zA-Z]{3,10}$", data['first_name']):
    #                 return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"Success":False})   
    #             update_fields['first_name'] = data['first_name']

    #         if 'last_name' in data: 
    #             if not re.match(r"^[a-zA-Z]{3,10}$", data['last_name']):
    #                 return jsonify({"message":'last name should be 3 to 10 characters only alphabets',"Success":False}) 
    #             update_fields['last_name'] = data['last_name']  

    #         if 'contact' in data:
    #             if not re.match(r"^[0-9]{10}$", data['contact']):
    #                 return jsonify({"message": "Invalid contact number","Success":False})
    #             update_fields['contact'] = data['contact']  

    #         mongo.db.user.update_one({"email":email}, {"$set": update_fields})
    #         return jsonify({"message": "updated successfully ","updated":update_fields,"success":True}) 
        
    #     if 'profile_pic' in data1:
    #         profile_pic = data1['profile_pic']
    #         if profile_pic.filename == '':
    #             return jsonify({'message': 'file not selected',"success":False})
    #         if profile_pic and allowed_file(profile_pic.filename):
    #             filename = secure_filename(profile_pic.filename)
    #             profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #             update_fields['profile_pic'] = filename
    #             db.admin.update_one({"email":email}, {"$set": update_fields})
    #             return jsonify({"message": "updated successfully ","updated":update_fields,"success":True}) 

    #     return jsonify({"message":"nothing updated","success":False})   
    # except jwt.ExpiredSignatureError:
    #     return jsonify({'message': 'Token has expired',"success":False})
    # except (jwt.InvalidTokenError, KeyError):
    #     return jsonify({'message': 'Invalid authorization token',"success":False}) 

#----------------------------view user profile pic---------------------------------------------------
@use.route('/profile_picture/<filename>', methods=['GET'])
# def profile_pic(filename):
def profile_pic(*args, **kwargs):
    filename = kwargs.get("filename")
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})    

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        user = mongo.db.user.find_one({'email': email,'jwtoken':jwtoken})
        if not user:
            return jsonify({'message': 'user not found',"success":False})     
        file_path = os.path.join(os.getcwd(), "static/uploads/profile_pics", filename)

        if not os.path.isfile(file_path):
            return jsonify({'message': 'Invalid file', "success": False})

        if user['profile_pic']:
            return send_file(file_path)
        else:
            return jsonify({"message":"error","success":False}) 
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})

#-----------------------------user update profile image-----------------------

@use.route('/update_profile_picture', methods=['PATCH'])
def update_profile_picture():
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})    

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        user = mongo.db.user.find_one({'email': email,'jwtoken':jwtoken})
        if not user:
            return jsonify({'message': 'user not found',"success":False})  

        required_params = ['profile_pic']
        data = request.files
            # Check if all required parameters are present
        missing_params = [param for param in required_params if param not in data]
        if missing_params:
            return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})      
        profile_pic = data['profile_pic']
        if profile_pic.filename == '':
            return jsonify({'message': 'file not selected',"success":False})
        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mongo.db.user.update_one({'email': user['email']}, {'$set': {'profile_pic': filename}})
    
            return jsonify({'message': 'Profile picture updated successfully',"success":True})

        else:
            return jsonify({'message': 'Check login before updating',"success":False})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})
   

#----------------------------error handler------------------------------------------------------------------
@use.errorhandler(404)
def not_found(error=None):
    message = {
    'status': 404,
    'message' : 'Not Found' + request.url
    }
    response = jsonify(message)
    response.status_code = 404

    return response

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=4000,debug=True)   