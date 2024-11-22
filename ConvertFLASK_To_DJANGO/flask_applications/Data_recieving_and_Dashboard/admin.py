from  Data_recieving_and_Dashboard.packages import *
from pymongo.errors import *
import json
from bson import json_util


admin = Blueprint("admin", __name__,template_folder='templates',url_prefix="/admin")

api = Api(admin)

# cors = CORS(admin)
#------------------media extensions--------------------------------------------------------------------
UPLOAD_FOLDER1 = 'static/uploads/admin'    #media storing folder

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}      #image extension
ALLOWED_EXTENSIONS1 = {'mp4', 'mkv', 'avi'}       #video extension

#  #-----------------database connection mongodb-----------------------------------------------------------
# mongo = pymongo.MongoClient(
#     host="localhost", 
#     port=27017,
#     serverSelectionTimeoutMS = 1000
#     )
# db = mongo.DOCKETRUNDB        # login = database name 

# mongo.server_info()

# mongo.db.admin.create_index([('adminid', 1), ('department', 1), ('company', 1), ('location', 1)], unique=True) # for admin
# mongo.db.user.create_index([('empid', 1), ('department', 1), ('company', 1), ('location', 1)], unique=True) # for user
# mongo.db.admin.create_index([('email', 1)], unique=True)



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
        return ""  # Return an empty string if any value cannot be converted to an integer

# Example usage:
# encoded_text = ''  # Assuming encoded_text is empty
# decoded_text = decode_encoded_text(encoded_text)
# print("Decoded text:", decoded_text)


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



def admin_send_reset_password_otp(email):
    # Generate OTP
    otp = random.randint(100000, 999999)
    # Save the OTP and its validity timestamp in the database or cache (e.g., Redis) with the user's email as the key
    otp_data = {
        'otp': otp,
        # 'valid_until': datetime.datetime.now() + datetime.timedelta(seconds=30)  # Set the validity for 10 minutes
        'valid_until' :datetime.now() + timedelta(seconds=10000000)
    }
    mongo.db.admin.update_one({'email': email}, {'$set': {'reset_password_otp': otp_data}})
    return otp



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
#------------------------home page-----------------------------------------------------------------------
@admin.route('/admin', methods=['GET'])
#@jwt_required()
def index1():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
    print("jwtoken=",jwtoken)
    #mongo.db.admin.find_one({'jwtoken':jwtoken})
    if not jwtoken:
        return jsonify({'message': 'missing authorization token'})   

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        #expire = datetime.fromtimestamp(decoded_token['exp'])
        print("decoded=",decoded_token)
        email = decoded_token['email']
        admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
        #email = admin['email']
        if not admin:
            return jsonify({'message': 'admin not found'})

        return jsonify({'message': 'you are already logged in','email':email})
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


#-------------------sign up-------------------------------------------------------------------------------
@admin.route("/admin_signup", methods=['POST'])
# @cross_origin()
def admin_signup():
    # required parameter
    required_params = ['fullname','department','email', 'password', 'contact','token']
    # ['first_name','last_name', 'adminid', 'company', 'location', 'department','email', 'password', 'contact']
    # required_params1 = ['profile_pic']
    # data = request.form
    data = request.json
    # data1 = request.files
    print('----data---',data)
    
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    fullname = data['fullname']
    department = data['department']
    # profile_pic = data1['profile_pic']
    email = data["email"]
    password = data["password"]
    password= decode_from_ascii(password)
    contact = data["contact"] 
    token = data['token']

    
    # validate first name
    if not firstname_regex.match(fullname):
        return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"success":False})   
    
           
    if token is not None:
        if len(token)< 6:
            return jsonify({"message":'token should be minimum 6 letters',"success":False})

    # validate department name
    if not company_regex.match(department):
        return jsonify({"message":'department should be 3 to 10 characters only alphabets',"success":False})        

    # Validate password
    # if not validate_password(password):
    #     return jsonify({"message":'Password must contain 8 to 16 characters,including at least alphanumeric,1 captial letter and special characters',"success":False})    

    # Validate email
    if not email_regex.match(email):
        return jsonify({"message": "invalid email","success":False})
    # Validate contact
    if not contact_regex.match(contact):
        return jsonify({"message": "contact number should contain 10 numbers only","success":False})
    # checking existing email
    if mongo.db.admin.find_one({"email": email}):
        return jsonify({"message": "email already registered as admin","success":False})

    if mongo.db.user.find_one({"email": email}):
        return jsonify({"message": "email already registered as user","success":False}) 

    # check adminid company department and location should be different
    if mongo.db.admin.find_one({'department':department,'email':email}):
        return {'message': 'email already registered',"success":False}  
    #----------------adding profile pic----------------
    # if profile_pic:
    #     if profile_pic.filename == '':
    #         return jsonify({'message': 'File not selected', 'success': False})

    #     if profile_pic and allowed_file(profile_pic.filename):
    #         filename = secure_filename(profile_pic.filename)
    #         upload_folder = app.config['UPLOAD_FOLDER1']
    #         os.makedirs(upload_folder, exist_ok=True)  # Create the upload folder if it doesn't exist
    #         profile_pic.save(os.path.join(upload_folder, filename))
    #     else:
    #         return jsonify({"message": "Selected file is not supported", 'success': False})
    # else:
    filename = None

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pwd_hash = generate_password_hash(password)
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    # verify email token generate
    # atoken = a.dumps(email, salt='email-confirmation-key')
    # save user information in the database
    Inputdetails = {                                   #-------users is collection of database
            "fullname": fullname,
            "department" : department,
            "profile_pic" : filename,
            "email": email,
            "password": hashed_password,
            "contact": contact,
            "super_adminid":False,
            "super_admin_email" : False,
            # "atoken": atoken,
            "created_at": created_at,
            "token":token
            # "_verify":False
        }
    print ("inputdetails === ",Inputdetails)
    try :
        mongo.db.admin.insert_one(Inputdetails)
        return jsonify({'message':'Admin registered successfully','success':True})
    except DuplicateKeyError as error :
        print("--------------error-----------1------registering-----",error)
        return jsonify ({"message":"foudn error while registring -{0}".format(error),"success":False})

#-------------------------------admin login-----------------------------------------------------------------
@admin.post("/admin_login")
def admin_login():
    required_params = ['email','password','token']
    jwtoken = request.headers.get('Authorization')
    print("Authorization=============================",jwtoken)
    data = request.json
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    email = data["email"]
    password = data["password"]
    password= decode_from_ascii(password)
    token = data['token']
    admin = mongo.db.admin.find_one({"email": email})

    if not admin:
        return jsonify({"message": "Sign up before login", "success": False})

    if not check_password(password, admin["password"]):
        return jsonify({"message": "given password is not matching.", "success": False})
    
    if token == None or token =='':
        return jsonify({"message": "invalid token please give proper token.", "success": False})
    if token != admin["token"]:
        return jsonify({"message": "invalid token please give proper token.", "success": False})
    
    CampareTime = now_time_with_time()
    if 'expire' in admin:
        if type(admin['expire']) == str :
            if admin['expire']<=CampareTime: 
                if check_password(password, admin["password"] ):
                    if admin:
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
                        mongo.db.adminloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                        mongo.db.admin.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                        return jsonify({'jwtoken': jwtoken, 'message': 'successful logged in', 'success': True})
                        
                    else:
                        return jsonify({'message' : 'wrong credentials',"success":False})

                else:        
                    return jsonify({'message' : 'password is incorrect',"success":False})
            else:
                #'email'
                FINDLOGDATA = mongo.db.adminloginlog.find_one({"email":email},sort=[("_id", pymongo.DESCENDING)])
                if FINDLOGDATA is not None:
                    print("====FINDLOGDATA===",FINDLOGDATA)
                    if 'browser' in FINDLOGDATA and 'systemid' in FINDLOGDATA:
                        return jsonify({'message' : 'already logged in browser {0} in system {1}'.format(FINDLOGDATA['browser'],FINDLOGDATA['systemid']),'jwtoken': admin['jwtoken'],"success":False})
                    else:
                        return jsonify({'message' : 'already logged in, please confirm do you want logout in other device.','jwtoken': admin['jwtoken'],"success":False})
                else:
                    return jsonify({'message' : 'already logged in, please confirm do you want logout in other device.','jwtoken': admin['jwtoken'],"success":False})
        elif  admin['expire'] == None:    
            if check_password(password, admin["password"] ):
                if admin:
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
                    mongo.db.adminloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                    mongo.db.admin.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                    return jsonify({'jwtoken': jwtoken, 'message': 'successful logged in', 'success': True})                    
                else:
                    return jsonify({'message' : 'wrong credentials',"success":False})

            else:        
                return jsonify({'message' : 'password is incorrect',"success":False})
        else:
            return jsonify({'message' : 'expire time format is not correct.',"success":False})

        
    else:
        if check_password(password, admin["password"] ):
            if admin:
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
                mongo.db.adminloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                mongo.db.admin.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                return jsonify({'jwtoken': jwtoken, 'message': 'successful logged in', 'success': True})
                
            else:
                return jsonify({'message' : 'wrong credentials',"success":False})

        else:        
            return jsonify({'message' : 'password is incorrect',"success":False})
        

@admin.post('/adminloginlogdetails')
#mongo.db.admin.update_one({'email': admin['email']}, {'$set': {'profile_pic': filename}})   
def ADLOgDEtails():
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
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
            TOKENDEtails = mongo.db.adminloginlog.find_one(TOKENQuery)
            if TOKENDEtails is not None:
                print("TOKENDEtails===",TOKENDEtails)
                TOKENDEtails = parse_json(TOKENDEtails)
                #( {'jwtoken':  jwtoken}, {'$set': data})   
                mongo.db.adminloginlog.update_one( {'jwtoken':  jwtoken}, {'$set': data}) 
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


#------------------------admin add users------------------------------------------------------------------
@admin.post("/admin_add_users")
def admin_addusers():
    CampareTime = now_time_with_time()
    print("CampareTime===",CampareTime)
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    # if Sessiontime['expire'] > CampareTime:
    #     print("Sessiontime============",Sessiontime)

    # if 1:
    if Sessiontime is not None:
        jwtoken = request.headers.get('Authorization')
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})  

        try:
            jwtoken= jwtoken.split(" ")[1]
            TOKENQuery = {'jwtoken':  jwtoken}
            # data = request.json
            # print("=====data======",data)
            TOKENDEtails = mongo.db.adminloginlog.find_one(TOKENQuery)
            if TOKENDEtails is not None:
                print("TOKENDEtails===",TOKENDEtails)
                admin_email= TOKENDEtails['email']
                # jwtoken = request.headers.get('Authorization')
                # if not jwtoken:
                #     return jsonify({'message': 'missing authorization token',"success":False})  

                # try:
                    # jwtoken = jwtoken.split(" ")[1]
                decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
                email = decoded_token['email']
                admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
                if not admin:
                    return jsonify({'message': 'admin not found',"success":False}) 
                if admin:
                    required_params = ['fullname','department', 'department','email', 
                    'password', 'contact','token']
                    # required_params1 = ['profile_pic']
                    # data = request.form
                    # data1 = request.files
                    data= request.json
                    # Check if all required parameters are present
                    missing_params = [param for param in required_params if param not in data]
                    if missing_params:
                        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})

                    # missing_params1 = [param for param in required_params1 if param not in data1]
                    # if missing_params1:
                    #     return jsonify({'message': f'Missing parameters: {", ".join(missing_params1)}', 'success': False})

                    first_name = data['fullname']
                    department = data['department']
                    email = data["email"]
                    password = data["password"]
                    password= decode_from_ascii(password)
                    contact = data["contact"] 
                    pin = data['token']
                    selectedpages = None
                    if 'selectedpages' in data:
                        selectedpages = data['selectedpages']



                    print('-------------------------data --------------userdetails --------',data)
                    
                    # validate first name
                    if not firstname_regex.match(first_name):
                        return jsonify({"message":'full name should be 3 to 10 characters only alphabets',"success":False})   

                    # validate last name
                    
                    # validate department name
                    if not company_regex.match(department):
                        return jsonify({"message":'department should be 3 to 10 characters only alphabets',"success":False})

                    
                    # Validate password
                    # if not validate_password(password):
                    #     return jsonify({"message":'password must contain 8 to 16 characters,including at least alphanumeric,1 captial letter and special characters',"success":False})    

                    # Validate email
                    if not email_regex.match(email):
                        return jsonify({"message": "invalid email","success":False})
                    # Validate contact
                    if not contact_regex.match(contact):
                        return jsonify({"message": "invalid contact number","success":False})
                    # checking existing email
                    if mongo.db.user.find_one({"email": email}):
                        return jsonify({"message": "email already registered as user, please login as user","success":False})

                    if mongo.db.admin.find_one({"email": email}):
                        return jsonify({"message": "email already registered as admin, please login as admin.","success":False})

                    # admin = mongo.db.admin.find_one({"email": admin_email, 'adminid': adminid})
                    # if not mongo.db.admin.find_one({"email": admin_email}):
                    #     return jsonify({"message":"Admin email not found.","success":False})

                    # if not mongo.db.admin.find_one({"email": adminid}):
                    #     return jsonify({"message": "admin id  does not exist","success":False})  
                    # if not admin:
                    #     return jsonify({'message': 'Admin email and admin ID do not match.',"success":False})     
            

                    
                    
                    filename = None    
                    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    pwd_hash = generate_password_hash(password)
                # Hash password
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                # verify email token generate
                    # token = s.dumps(email, salt='email-confirmation-key')
                # save user information in the database
                    mongo.db.user.insert_one({                                   #-------users is collection of database
                    "fullname": first_name,
                    "department" : department,
                    "profile_pic" : filename,
                    "email": email,
                    "password": hashed_password,
                    "contact": contact,
                    "admin_email" : admin_email,
                    "super_adminid":False,
                    "super_admin_email" : False,
                    "token":pin,
                    # "token": token,
                    'selectedpages':selectedpages,
                    "created_at": created_at,
                    # "_verify":False
                    })
                    return jsonify({'message':'user registered successfully','success':True})
            else:
                return jsonify({'message':'admin login details is not found for register user, please once again login','success':False})  
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

    
#-------------view user profile-------------------------------------------------------------------------------
@admin.route('/admin_profile', methods=['GET','POST'])
def admin11_profile():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
    if  request.method == 'POST':
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
                    jwtoken = jwtoken.split(" ")[1]
                    decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
                    email = decoded_token['email']
                    admin = mongo.db.admin.find_one({'email': email})
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
                    mongo.db.adminloginlog.insert_one({'email':email,'jwtoken':jwtoken, 'expire':stringfuturetime})
                    result = mongo.db.admin.update_one({'email':admin['email']},{'$set':{'jwtoken':jwtoken, 'expire':stringfuturetime}})
                    if (result.modified_count > 0):
                        return jsonify({'message':parse_json(admin) ,"success":True })
                    else:
                        return jsonify({'message':'profile is not updated successfully.' ,"success":False })

                    # return jsonify({'message':parse_json(admin) ,"success":True })

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
                    jwtoken = jwtoken.split(" ")[1]
                    decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
                    email = decoded_token['email']
                    admin = mongo.db.admin.find_one({'email': email})
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



    elif request.method == 'GET':
        # print("Sessiontime============",Sessiontime)
        # if 1:
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
                admin = mongo.db.admin.find_one({'email': email})
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

        
    
        
#-------------------------admin view added users-------------------------------------------------
@admin.get('/admin_view_users')
def admin_view_users():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    # if 1:
    if Sessiontime is not None:

        tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})   

        try:
            jwtoken = jwtoken.split(" ")[1]
            
            # print('-------------------------------jwtoken 1.0-------------------adminusers---',jwtoken)
            decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
            email = decoded_token['email']
            # print('-----------------------------admin 1.1--------view users',email)
            # print('--------------------------admin query --1.1------------',{'email': email})
            admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
            if not admin:
                # print('-----------------------------admin 1--------view users',admin)
                return jsonify({'message': 'admin not found',"success":False})    
            email = admin['email']
            admin = list(mongo.db.user.find({'admin_email':email}))
            if len(admin) !=0 :

                return jsonify({'message': parse_json(admin),'success':True})
            else:
                return jsonify({'message': "no user are added from {0}".format(email),'success':False})

            # users = []
            # for user in admin:
            #     if user:
                    # users.append({
                    # 'profile_pic' : user ['profile_pic'],
                    # 'first_name': user['first_name'],
                    # 'last_name' : user['last_name'],
                    # 'contact' : user['contact'],
                    # 'empid' : user['empid'],
                    # 'location' : user['location'],
                    # 'department' : user ['department'],
                    # 'company' : user ['company'],
                    # 'email': user['email']
                    # })
            
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


#-----------------------------logout------------------------------------------------------------
@admin.route('/admin_logout', methods=['GET'])
def admin_logout():
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'missing authorization token',"success":False})    

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.admin.find_one({'email': email})
        if not admin:
            return jsonify({'message': 'Admin not found',"success":False})

        mongo.db.admin.update_one({'email':email},{"$set": {'jwtoken':0,'expire':None}})
        return jsonify({'message': 'Logged out successfully',"success":True})
    except jwt.ExpiredSignatureError as error:
        try:
            admin = mongo.db.admin.find_one({'jwtoken': jwtoken})
            if not admin:
                return jsonify({'message': 'Admin not found',"success":False})
            mongo.db.admin.update_one({'jwtoken': jwtoken},{"$set": {'jwtoken':0,'expire':None}})
            return jsonify({'message': 'Logged out successfully',"success":True})
        except Exception as error :

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


#----------------------------view admin profile pic---------------------------------------------------
@admin.route('/admin_profile_picture/<filename>', methods=['GET'])
def admin_11profile_pic(*args, **kwargs):
    filename = kwargs.get("filename")
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.admin.find_one({"jwtoken": jwtoken})
    if not jwtoken:
        return jsonify({'message': 'missing authorization token', "success": False})

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.admin.find_one({'email': email, 'jwtoken': jwtoken})
        if not admin:
            return jsonify({'message': 'admin not found', "success": False})

        if filename:
            file_path = os.path.join(os.getcwd(), "static/uploads/admin", filename)

            if not os.path.exists(file_path):
                return jsonify({'message': 'File not found', "success": False})

            if admin.get('profile_pic'):
                return send_file(file_path)
            else:
                return jsonify({'message': 'No profile picture to view', "success": False})
        else:
            return jsonify({'message': 'No profile picture to view', "success": False})

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




        
    
#---------------------change password---------------------------------------------------------------------
@admin.route('/admin_changepassword', methods=['POST'])
def admin_change():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    # if 1:
    if Sessiontime is not None:
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})    

        try:
            jwtoken = jwtoken.split(" ")[1]
            decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
            email = decoded_token['email']
            admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
            if not admin:
                return jsonify({'message': 'admin details not found',"success":False})    
            
            if admin['jwtoken'] == 0:
                return jsonify({'message': 'admin already logged out',"success":False})  
            if admin:
                required_params = ['current_password','new_password','confirm_password']
                # data = request.form
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
                #print('new_password=',new_password)
                mongo.db.admin.update_one({'email': email},{'$set':{'password':hashed_password}})
                
                return jsonify({"message": "password updated successfully","success":True})        
                # response = jsonify({'message': 'admin' + id + 'updated'})  # DETAILS IS collection name
                # return response
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
@admin.route('/admin_forgot_password', methods=['POST'])

def admin_forgot_password():
    required_params = ['email']
    # forgot = request.form
    forgot = request.json
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in forgot]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    
    if request.method == 'POST':
        # Get the user's email from the request
        email = forgot['email']
        # Check if the email exists in the database
        user = mongo.db.admin.find_one({'email': email})
        if not user:
            return jsonify({"message": 'given email is not registered please register.', "success": False})
        # Send the OTP to the user's email
        otp = admin_send_reset_password_otp(email)
        return jsonify({"message": "otp is generated, ",'otp':otp, "success": True})


     

#--------------------reset password--------------------------------------------------------------------------
@admin.route('/admin_reset_password', methods=['GET', 'POST'])
# def admin_reset_password(rtoken):
# @admin.route('/admin_reset_password', methods=['POST'])
def admin_reset_password():
    if request.method == 'POST':
        data = request.json     
        otp = data['otp']   
        password = data['password']
        password= decode_from_ascii(password)
        confirm_password = data['confirm_password']
        confirm_password= decode_from_ascii(confirm_password)
        email = data.get('email')

        if email is None or email =='':
            return jsonify({"message": 'email should be valid or not None', "success": False})


        # if not validate_password(password):
        #     return jsonify({"message": 'password must contain 8 to 16 characters, at least 1 alphanumeric, 1 capital letter, and 1 special character', "success": False})    


        if password != confirm_password:
            return jsonify({"message": 'passwords do not match', "success": False})

        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Retrieve the user based on the email saved in the OTP verification step
        user = mongo.db.admin.find_one({'email': email})
        if user is not None :
            valid_until =user['reset_password_otp']['valid_until']# user.reset_password_otp('valid_until')
            print("=======valid_until===",valid_until)
            if not valid_until or datetime.now() > valid_until:
                return jsonify({"message": 'otp has expired', "success": False})
            if not user:
                return jsonify({"message": 'user not found', "success": False})
            mongo.db.admin.update_one({'email': email}, {'$set': {'password': hashed_password}})
            # Optionally, you can also remove the reset_token from the user's document
            # mongo.db.admin.update_one({'_id': user['_id']}, {'$unset': {'reset_token': ''}})

            return jsonify({"message": "password updated", "success": True})
        else:
            return jsonify({"message": "user data not found", "success": False})

    else:
        return jsonify({"message": "incorrect method.", "success": False})






       
#----------------------admin update profile-----------------------------------------------
@admin.route('/update_admin_profile',methods=['PUT','PATCH','POST'])
def admin_update_profile():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    if Sessiontime is not None:
        tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
        if not jwtoken:
            return jsonify({'message': 'missing authorization token',"success":False})    

        try:
            jwtoken = jwtoken.split(" ")[1]
            decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
            email = decoded_token['email']
            admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
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

                mongo.db.admin.update_one({"email":email}, {"$set": update_fields})
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
    




#-----------------------------user update profile image-----------------------
@admin.route('/update_profile_picture', methods=['PATCH'])
def admin_update_profile_picture():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'missing authorization token',"success":False})    

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
        if not admin:
            return jsonify({'message': 'admin not found',"success":False})     
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
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
            mongo.db.admin.update_one({'email': admin['email']}, {'$set': {'profile_pic': filename}})    
            return jsonify({'message': 'Profile picture updated successfully',"success":True})

        else:
            return jsonify({'message': 'Check login before updating',"success":False})
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

@admin.delete("/delete")
def delete():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'missing authorization token'})   

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
        if not admin:
            return jsonify({'message': 'admin not found'})

        mongo.db.admin.delete_one({'email':email})
        return jsonify({'message': 'Account deleted successfully',"success":True})


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

# @admin.delete("/userdelete")
# def user_delete():
#     jwtoken = request.headers.get('Authorization')
#     CampareTime = now_time_with_time()
#     query = {'expire': {'$gte': CampareTime}}
#     Sessiontime = mongo.db.adminloginlog.find_one(query)
#     print("Sessiontime============",Sessiontime)
#     if Sessiontime is not None:
#         # jwtoken = request.headers.get('Authorization')
#         tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
#         if not jwtoken:
#             return jsonify({'message': 'missing authorization token'})    

#         try:
#             jwtoken = jwtoken.split(" ")[1]
#             decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
#             email = decoded_token['email']
#             admin = mongo.db.admin.find_one({'email': email,'jwtoken':jwtoken})
#             if not admin:
#                 return jsonify({'message': 'admin not found'})
#             data = request.form
#             email = data['email']
#             users = mongo.db.user.find_one({'email':email})   
#             if users:
#                 if users['admin_email'] != admin['email']:  # check if the admin who created the user is the same as the admin making the delete request
#                     return jsonify({"message":"You are not authorized to delete this user"})

#                 mongo.db.user.delete_one({'email':email})
#                 return jsonify({'message': 'User Account deleted successfully',"success":True})
#             else:
#                 return jsonify({"message":"user email not found"})    

#         except jwt.ExpiredSignatureError as error:
#             print("authorization token has expired. please log in again.")
#             return jsonify({'message': 'authorization token has expired. please log in again.',"success":False})       

#         except jwt.ImmatureSignatureError as error:
#             print("token is not yet valid")
#             return jsonify({'message': 'token is not yet valid',"success":False})

#         except jwt.InvalidIssuerError as error:
#             print("Invalid issuer")
#             return jsonify({'message': 'invalid issuer',"success":False})

#         except jwt.InvalidAudienceError:
#             print("Invalid audience")
#             return jsonify({'message': 'invalid audience',"success":False})

#         except jwt.InvalidAlgorithmError:
#             print("Invalid algorithm")
#             return jsonify({'message': 'invalid algorithm',"success":False})

#         except jwt.MissingRequiredClaimError:
#             print("Missing required claim")
#             return jsonify({'message': 'missing required claim',"success":False})
        
#         except (jwt.InvalidTokenError, KeyError):
#             return jsonify({'message': 'Invalid authorization token',"success":False})

#         except Exception as e:
#             print("JWT error:", e)
#             return jsonify({'message': str(e),"success":False})
#     else:
#         return jsonify({'message': "session expired, please login once again","success":False})



@admin.post("/userdelete")
def user_delete():
    jwtoken = request.headers.get('Authorization')
    CampareTime = now_time_with_time()
    query = {'expire': {'$gte': CampareTime}}
    Sessiontime = mongo.db.adminloginlog.find_one(query)
    # print("Sessiontime============",Sessiontime)
    if Sessiontime is not None:
        # jwtoken = request.headers.get('Authorization')
        tokens = mongo.db.admin.find_one({"jwtoken":jwtoken})
        if not jwtoken:
            return jsonify({'message': 'missing authorization token'})    

        try:
            jwtoken = jwtoken.split(" ")[1]
            decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
            email = decoded_token['email']
            admin = mongo.db.admin.find_one({'email': email})#{'email': email,'jwtoken':jwtoken}
            if not admin:
                return jsonify({'message': 'admin not found'})
            data = request.json
            email = data['email']
            users = mongo.db.user.find_one({'email':email})   
            if users:
                if users['admin_email'] != admin['email']:  # check if the admin who created the user is the same as the admin making the delete request
                    return jsonify({"message":"you are not authorized to delete this user"})

                mongo.db.user.delete_one({'email':email})
                return jsonify({'message': 'user Account deleted successfully',"success":True})
            else:
                return jsonify({"message":"user email not found"})    

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




# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=4000,debug=True)  