from Data_recieving_and_Dashboard.packages import *
# from flask import jsonify
import random

super_admin = Blueprint("super_admin", __name__,template_folder='templates',url_prefix="/super_admin")

api = Api(super_admin)
#------------------media extensions--------------------------------------------------------------------
UPLOAD_FOLDER_SUPER = 'static/uploads/super_admin'    #media storing folder

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}      #image extension
ALLOWED_EXTENSIONS1 = {'mp4', 'mkv', 'avi'}       #video extension



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



#-------------------------super admin signup-----------------------------------------------
@super_admin.route("/super_signup", methods=['POST'])
def super_signup():
    # required parameter
    required_params = ['first_name','last_name', 'super_adminid', 'company', 'location', 'department','email', 'password', 'contact']
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
    
    #data = request.form
    first_name = data['first_name']
    last_name = data['last_name']
    super_adminid = data['super_adminid']
    company = data['company']
    location = data['location']
    department = data['department']
    profile_pic = data1['profile_pic']
    email = data["email"]
    password = data["password"]
    contact = data["contact"] 

    
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
    elif not company_regex.match(location):
        return jsonify({"message":'location should be 3 to 10 characters only alphabets',"Success":False})          

    # validate adminid
    elif not diffid_regex.match(super_adminid):
        return jsonify({"message":'admin id should be 1 to 10 character only numeric ',"Success":False})          

    # Validate password
    # elif not validate_password(password):
    #     return jsonify({"message":'Password must contain 8 to 16 characters,including at least alphanumeric,1 captial letter and special characters',"Success":False})    

    # Validate email
    elif not email.endswith('@docketrun.com'):
        return jsonify({"message": "Invalid email domain","Success":False})
    # Validate contact
    elif not contact_regex.match(contact):
        return jsonify({"message": "contact number should contain 10 numbers only","Success":False})
    # checking existing email
    elif mongo.db.user.find_one({"email": email}):
        return jsonify({"message": "Email already exists","Success":False})

    elif mongo.db.admin.find_one({"email": email}):
        return jsonify({"message": "Email already exists"})

    elif mongo.db.super_admin.find_one({"email": email}):
        return jsonify({"message": "Email already exists"})     

    # check adminid company department and location should be different
    elif mongo.db.super_admin.find_one({'super_adminid': super_adminid, 'company': company, 'department':department,'location': location}):
        return {'message': 'super_adminid , company name,department and location already exists',"success":False}    
    #----------------adding profile pic----------------
    if profile_pic:
        if profile_pic.filename == '':
            return jsonify({'message': 'File not selected',"success":False})

        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            upload_folder = app.config['UPLOAD_FOLDER_SUPER']
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
    stoken = s.dumps(email, salt='email-confirmation-key')
    # save user information in the database
    mongo.db.super_admin.insert_one({                                   #-------users is collection of database
        "first_name": first_name,
        "last_name": last_name,
        "super_adminid": super_adminid,
        "company" : company,
        "location" :location,
        "department" : department,
        "profile_pic" : filename,
        "email": email,
        "password": hashed_password,
        "contact": contact,
        "stoken": stoken,
        "created_at": created_at,
        "_verify":False
    })
    return jsonify({"message": "Verification email sent","success":True})    

#-------------------------------super admin login-----------------------------------------------------------------
@super_admin.post("/super_login")
def super_login():
    required_params = ['email','password']
    data = request.form
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    email = data["email"]
    password = data["password"]
    sadmin = mongo.db.super_admin.find_one({"email": email})

    if not sadmin:
        return jsonify({"message": "Sign up before login", "success": False})

    if not check_password(password, sadmin["password"]):
        return jsonify({"message": "given password is not matching.", "success": False})

    if not sadmin["_verify"]:
        return jsonify({'message': 'Verify email before login', 'success': False})

    if check_password(password, sadmin["password"] ):
        if sadmin["_verify"]:
            expire = datetime.utcnow() + timedelta(minutes=240)
            payload = {
                'email': email,
                'exp': expire
                }

            jwtoken = jwt.encode(payload, "jwtsecretkey","HS256")
            mongo.db.super_admin.update_one({'email':email},{'$set':{'jwtoken':jwtoken, 'expire':expire}})
            return jsonify({'jwtoken': jwtoken, 'message': 'Successful logged in', 'success': True})
            
        else:
            return jsonify({'message' : 'verify email before login',"success":False})

    else:        
        return jsonify({'message' : 'password is incorrect',"success":False}) 

#-----------------super admin profile--------------------------------------------

@super_admin.route('/super_profile', methods=['GET'])
def super_profile():
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token', 'success': False})

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        sadmin = mongo.db.super_admin.find_one({'email': email, 'jwtoken': jwtoken})
        if not sadmin:
            return jsonify({'message': 'admin not found', 'success': False})

        return jsonify({
            'message': 'super admin profile',
            'email': sadmin["email"],
            "first_name": sadmin["first_name"],
            "last_name": sadmin["last_name"],
            "super_adminid": sadmin["super_adminid"],
            "company": sadmin["company"],
            "department": sadmin["department"],
            "contact": sadmin["contact"],
            "profile_pic": sadmin["profile_pic"],
            "location": sadmin["location"],
            "success": True
        })

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired', 'success': False})

    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token', 'success': False})


#-------------------------super admin view all users-------------------------------------------------
@super_admin.get('/super_view_users')
def super_view_users():
    jwtoken = request.headers.get('Authorization')

    if not jwtoken:
        return jsonify({'message': 'Missing authorization token', 'success': False})

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        sadmin = mongo.db.super_admin.find_one({'email': email, 'jwtoken': jwtoken})

        if not sadmin:
            return jsonify({'message': 'Admin not found', 'success': False})

        email = sadmin['email']
        sadmin = mongo.db.user.find()
        users = []
        for user in sadmin:
            if user:
                users.append({
                    'profile_pic': user['profile_pic'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'contact': user['contact'],
                    'empid': user['empid'],
                    'location': user['location'],
                    'department': user['department'],
                    'company': user['company'],
                    'email': user['email'],
                    'admin_email': user['admin_email']
                })

        if not users:
            return jsonify({"message": "Users not found", "success": False})

        return jsonify({'users': users})

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired', 'success': False})

    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token', 'success': False})


#-----------------------super admin view all admins--------------------------------------------
@super_admin.get('/super_view_admins')
def super_view_admins():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})      

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        sadmin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not sadmin:
            return jsonify({'message': 'admin not found',"success":False})      
        email = sadmin['email']
        sadmin = mongo.db.admin.find()
        admins = []
        for admin in sadmin:
            if admin:
                admins.append({
                'profile_pic' : admin ['profile_pic'],
                'first_name': admin['first_name'],
                'last_name' : admin['last_name'],
                'contact' : admin['contact'],
                'adminid' : admin['adminid'],
                'location' : admin['location'],
                'department' : admin ['department'],
                'company' : admin ['company'],
                'email': admin['email']
                })
        if not admins:
            return jsonify({"message": "users not found","success":False})
        return jsonify({'admins': admins}), 200
        #return jsonify({"message": "users not found","success":False})           
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})                          

#--------------------------view users by admin email----------------------------------- 
@super_admin.get('/super_view_users_admin')
def super_view():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token', 'success': False})
    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        sadmin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not sadmin:
            return jsonify({'message': 'Super Admin not found', 'success': False}) 
        data = request.form
        admin_email = data.get('admin_email')
        if not admin_email:
            return jsonify({"message": "Admin email is required", 'success': False})
        admin = mongo.db.admin.find_one({'email': admin_email})
        if not admin:
            return jsonify({"message": "Admin not found", 'success': False})
        users = mongo.db.user.find({'admin_email': admin_email})
        user_list = []
        for user in users:
            user_list.append({
                'empid': user['empid'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'company': user['company'],
                'department': user['department'],
                'location': user['location'],
                'contact': user['contact'],
                'admin_email': user['admin_email'],
                'profile_pic': user.get('profile_pic', '')
            })
            #return jsonify({'user_list': user_list}), 200
        if not user_list:
            return jsonify({"message": "No users found", 'success': True})
        return jsonify({"users": user_list, 'success': True})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired', 'success': False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token', 'success': False})  

#-------------------------super admin logout--------------------------
@super_admin.route('/super_logout', methods=['GET'])
def super_logout():
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})    

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email})
        if not admin:
            return jsonify({'message': 'Admin not found',"success":False}),  

        mongo.db.super_admin.update_one({'email':email},{"$set": {'jwtoken':0}})
        return jsonify({'message': 'Logged out successfully',"success":True})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})   
   
@super_admin.route('/super_admin_profile_picture/<filename>', methods=['GET'])
# def super_profile_pic(filename):
def super_profile_pic(*args, **kwargs):
    filename = kwargs.get("filename")
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})  

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'admin not found',"success":False})     

        file_path = os.path.join(os.getcwd(), "static/uploads/super_admin", filename)

        if not os.path.isfile(file_path):
            return jsonify({'message': 'Invalid file', "success": False})

        if admin['profile_pic']:
            return send_file(file_path)
        else:
            return jsonify({"message":"error","success":False})  

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})

#---------------------change password---------------------------------------------------------------------
@super_admin.route('/super_changepassword', methods=['PUT'])
def super_change():
    jwtoken = request.headers.get('Authorization')
    tokens = db.super_super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        sadmin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not sadmin:
            return jsonify({'message': 'super admin not found',"success":False})       
        if sadmin:
            required_params = ['current_password','new_password','confirm_password']
            data = request.form
            # Check if all required parameters are present
            missing_params = [param for param in required_params if param not in data]
            if missing_params:
                return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
            current_password = data['current_password']
            new_password = data['new_password']
            confirm_password = data['confirm_password']
        
            if not bcrypt.checkpw(current_password.encode('utf-8'), sadmin['password'].encode('utf-8')):
                return jsonify({"message":'Current password is incorrect',"success":False}),  

            # if not validate_password(new_password):
            #     return jsonify({"message":'Password must contain 8 to 16 characters at least 1, including alphanumeric, 1 capital letter and special characters',"Success":False})
    
            if new_password != confirm_password:
                return jsonify({'message': 'New password and confirm password do not match',"Success":False})      
        
            hashed_password = hash_password(new_password)
            #print('new_password=',new_password)
            mongo.db.super_admin.update_one({'email': email},{'$set':{'password':hashed_password}})
            
            return jsonify({"message": "updated successfully","success":True})        
            response = jsonify({'message': 'admin' + id + 'updated'})  # DETAILS IS collection name
            return response
        else : 
            return jsonify({"message": "enter all required fileds","success":False})    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})        

#----------------forgot password---------------------------------------------------------------------------
@super_admin.route('/super_forgot_password', methods=['POST'])
def super_forgot_password():
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
        user = mongo.db.super_admin.find_one({'email': email})
        if not user:
            return jsonify({"error": 'Email not found', "success": False})
        # Send the OTP to the user's email
        super_send_reset_password_otp(email)
        return jsonify({"message": "OTP sent to email", "success": True})

# Use a separate route or function for verifying the OTP and sending the reset password link
@super_admin.route('/super_admin_verify_reset_password_otp', methods=['POST'])
def super_verify_reset_password_otp():
    required_params = ['email']
    otp_data = request.form
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in otp_data]
    if missing_params:
        return jsonify({'message': f'Missing parameters: {", ".join(missing_params)}', 'success': False})
    
    
    # Get the email and OTP from the request
    email = otp_data['email']
    otp = otp_data['otp']
    # Retrieve the OTP and its validity timestamp from the database or cache based on the user's email
    user = mongo.db.super_admin.find_one({'email': email})
    if not user:
        return jsonify({"error": 'Email not found', "success": False})
    otp_data = user.get('reset_password_otp')
    if not otp_data:
        return jsonify({"error": 'OTP not found', "success": False})
    # Check if the OTP has expired
    valid_until = otp_data.get('valid_until')
    if not valid_until or datetime.now() > valid_until:
        return jsonify({"error": 'OTP has expired', "success": False})

  
    
    # Compare the provided OTP with the stored OTP
    if int(otp) != otp_data['otp']:
        return jsonify({"error": 'Invalid OTP', "success": False})
   
    return jsonify({"message": "Reset password link sent to email", "success": True})
     

       
#----------------------super admin update profile-----------------------------------------------
@super_admin.route('/update_superadmin_profile',methods=['PUT','PATCH'])
def super_admin_update_profile():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})   

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found',"success":False})          
        data = request.form
        data1 = request.files
        
        update_fields = {}
        if data:
         # Validate contact
            if 'first_name' in data:
                if not re.match(r"^[a-zA-Z]{3,10}$", data['first_name']):
                    return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"Success":False})   
                update_fields['first_name'] = data['first_name']

            if 'last_name' in data: 
                if not re.match(r"^[a-zA-Z]{3,10}$", data['last_name']):
                    return jsonify({"message":'last name should be 3 to 10 characters only alphabets',"Success":False}) 
                update_fields['last_name'] = data['last_name']  

            if 'contact' in data:
                if not re.match(r"^[0-9]{10}$", data['contact']):
                    return jsonify({"message": "Invalid contact number","Success":False}) 
                update_fields['contact'] = data['contact']   

            mongo.db.super_admin.update_one({"email":email}, {"$set": update_fields})
            return jsonify({"message": "updated successfully ","updated":update_fields,"success":True}) 
            
        if 'profile_pic' in data1:
            profile_pic = data1['profile_pic']
            if profile_pic.filename == '':
                return jsonify({'message': 'file not selected',"success":False})
            if profile_pic and allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER_SUPER'], filename))
                update_fields['profile_pic'] = filename
                mongo.db.super_admin.update_one({"email":email}, {"$set": update_fields})
                return jsonify({"message": "updated successfully ","updated":update_fields,"success":True}) 

        return jsonify({"message":"nothing updated","success":False})

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})   

#-----------------------------super admin update profile image-----------------------
@super_admin.route('/super_admin_update_profile_picture', methods=['PATCH'])
def super_admin_update_profile_picture():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})    

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found',"success":False})      
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
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER_SUPER'], filename))
            mongo.db.super_admin.update_one({'email': admin['email']}, {'$set': {'profile_pic': filename}})
    
            return jsonify({'message': 'Profile picture updated successfully',"success":True})

        else:
            return jsonify({'message': 'Check login before updating',"success":False})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})   

#---------------------super admin delete account---------------------------------
@super_admin.delete("/super_delete")
def super_delete():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token'})     

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found'})

        mongo.db.super_admin.delete_one({'email':email})
        return jsonify({'message': 'Account deleted successfully',"success":True})


    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})  
    

#------------------------------------delete admins-----------------------------------
@super_admin.delete("/super_admin_delete")
def delete():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token'})     

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found'}) 
        
        data = request.form
        email = data['email']
        deleted_admin = mongo.db.admin.find_one_and_delete({'email':email})
        if not deleted_admin:
            return jsonify({'message': 'Admin not found'})
        mongo.db.user.delete_many({'admin_email':email})
        return jsonify({'message': 'Accounts of admin and users deleted successfully',"success":True})

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})
#------------------------------------admin delete and transfer-------------------------------------        
@super_admin.delete("/admin_delete")
def admin_delete():
    # Get the JWT token from the request header
    jwtoken = request.headers.get('Authorization')

    # Check if the JWT token is missing
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token'}) 

    try:
        # Extract the token from the "Bearer" string
        jwtoken = jwtoken.split(" ")[1]

        # Verify the JWT token using the secret key
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']

        # Check if the super admin exists
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'Super admin not found'})    

        # Get the admin email and new admin email from the request data
        data = request.form
        email = data['email']
        new_admin_id = data.get('new_admin_id')
        new_admin_email = data.get('new_admin_email')

        

        # If there are users registered under the deleted admin email
        transferred_users = mongo.db.user.find({'admin_email': email})
        transferred_users_list = list(transferred_users)
        if len(transferred_users_list) > 0:

            # Check if a new admin email is provided
            if not new_admin_email:
                return jsonify({'message': 'New admin email is missing'})

            # Check if the new admin exists
            new_admin = mongo.db.admin.find_one({'email': new_admin_email,'adminid':new_admin_id}) 
            if not mongo.db.admin.find_one({"email": new_admin_email}):
                return jsonify({"message":"Admin email not found.","success":False})

            if not mongo.db.admin.find_one({"adminid": new_admin_id}):
                return jsonify({"message": "admin id  does not exist","Success":False})

            if not new_admin:
                return jsonify({'message': 'Admin email and admin ID do not match.',"success":False})      

            # Transfer the users to the new admin
            mongo.db.user.update_many({'admin_email': email}, {'$set': {'admin_email': new_admin_email,'adminid':new_admin_id}})
        # Delete the admin account
        deleted_admin = mongo.db.admin.find_one_and_delete({'email':email})
        if not deleted_admin:
            return jsonify({'message': 'Admin not found'}),  
        # Return success message
        return jsonify({'message': 'Account and users deleted/Transferred successfully',"success":True})
    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})  

#------------------------transfer users to another admin---------------------------
@super_admin.put("/super_transfer")
def super_transfer():
    # Get the JWT token from the request header
    jwtoken = request.headers.get('Authorization')

    # Check if the JWT token is missing
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token'})  

    try:
        # Extract the token from the "Bearer" string
        jwtoken = jwtoken.split(" ")[1]

        # Verify the JWT token using the secret key
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']

        # Check if the super admin exists
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'Super admin not found'})     

        # Get the admin email and new admin email from the request data
        data = request.form
        old_admin_email = data.get('old_admin_email')
        new_admin_id = data.get('new_admin_id')
        new_admin_email = data.get('new_admin_email')
        
        #old = mongo.db.user.find({'admin_email': old_admin_email})
        if not old_admin_email:
                return jsonify({'message': 'old admin email is missing'})

        # Check if a new admin email is provided
        if not new_admin_email:
            return jsonify({'message': 'New admin email is missing'})

        if not new_admin_id:
            return jsonify({'message': 'New admin id is missing'})              

        old_admin = mongo.db.admin.find_one({'email': old_admin_email})
        if not old_admin:
            return jsonify({'message': 'old admin not found'})  
        # If there are users registered under the old admin email
        transferred_users = mongo.db.user.find({'admin_email': old_admin_email})
        
        transferred_users_list = list(transferred_users)
        if len(transferred_users_list) > 0:


            # Check if the new admin exists
            new_admin = mongo.db.admin.find_one({'email': new_admin_email,'adminid':new_admin_id})

            if not mongo.db.admin.find_one({"email": new_admin_email}):
                return jsonify({"message":"New Admin email not found.","success":False})

            if not mongo.db.admin.find_one({"adminid": new_admin_id}):
                return jsonify({"message": "admin id  does not exist","Success":False}) 

            if not new_admin:
                return jsonify({'message': 'Admin email and admin ID do not match.',"success":False})     

            # Transfer the users to the new admin
            mongo.db.user.update_many({'admin_email': old_admin_email}, {'$set': {'admin_email': new_admin_email,'adminid':new_admin_id}})

        # Return success message
        return jsonify({'message': 'Users are transferred to another admin successfully',"success":True})
    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False}) 


#---------------------------transfer particular users to another admin----------------------------------
@super_admin.put("/super_usertransfer")
def super_usertransfer():
    # Get the JWT token from the request header
    jwtoken = request.headers.get('Authorization')

    # Check if the JWT token is missing
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token'})  

    try:
        # Extract the token from the "Bearer" string
        jwtoken = jwtoken.split(" ")[1]

        # Verify the JWT token using the secret key
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']

        # Check if the super admin exists
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'Super admin not found'})     

        # Get the admin email and new admin email from the request data
        data = request.form
        user_email = data.get('user_email')
        new_admin_email = data.get('new_admin_email')

        if not user_email:
                return jsonify({'message': 'old admin email is missing'}) 

        user = mongo.db.user.find_one({'email': user_email})
        if not user:
            return jsonify({'message': 'user not found'}) 

        # If there are users registered under the old admin email
        transferred_users = mongo.db.user.find({'email': user_email})
        transferred_users_list = list(transferred_users)
        if len(transferred_users_list) > 0:

            if not user_email:
                return jsonify({'message': 'user email is missing'}) 
            # Check if a new admin email is provided
            if not new_admin_email:
                return jsonify({'message': 'New admin email is missing'}) 

            # Check if the new admin exists
            new_admin = mongo.db.admin.find_one({'email': new_admin_email})
            if not new_admin:
                return jsonify({'message': 'New admin not found'}) 

            # Transfer the users to the new admin
            mongo.db.user.update_many({'email': user_email}, {'$set': {'admin_email': new_admin_email}})

        # Return success message
        return jsonify({'message': 'Users are transferred to another admin successfully',"success":True})
    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})

#-----------------------------super admin create users--------------------------------------------------
@super_admin.post("/super_add_users")
def super_admin_addusers():
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})     

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found',"success":False})  
        if admin:
            required_params = ['first_name','last_name', 'super_adminid', 'company', 'location', 'department','email', 
            'password', 'contact','super_admin_email']
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
            contact = data["contact"] 
            super_adminid = data.get('super_adminid')
            super_admin_email = data.get('super_admin_email')
            
            # validate first name
            if not firstname_regex.match(first_name):
                return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"Success":False})   

            # validate last name
            if not firstname_regex.match(last_name):
                return jsonify({"message":'last name should be 3 to 10 characters only alphabets',"Success":False})

            # validate company name
            if not company_regex.match(company):
                return jsonify({"message":'company should be 3 to 10 characters only alphabets',"Success":False})  

            # validate department name
            if not company_regex.match(department):
                return jsonify({"message":'department should be 3 to 10 characters only alphabets',"Success":False})

            # validate location
            if not firstname_regex.match(location):
                return jsonify({"message":'location should be 3 to 10 characters only alphabets',"Success":False})          

            # validate adminid
            if not diffid_regex.match(empid):
                return jsonify({"message":'admin id should be 1 to 10 numeric only',"Success":False})          


            # Validate password
            # if not validate_password(password):
            #     return jsonify({"message":'Password must contain 8 to 16 characters,including at least alphanumeric,1 captial letter and special characters',"Success":False})    

            # Validate email
            if not email_regex.match(email):
                return jsonify({"message": "Invalid email","Success":False})  
            # Validate contact
            if not contact_regex.match(contact):
                return jsonify({"message": "Invalid contact number","Success":False})  
            # checking existing email
            if mongo.db.user.find_one({"email": email}):
                return jsonify({"message": "Email already exists","Success":False}) 

            if mongo.db.admin.find_one({"email": email}):
                return jsonify({"message": "email already exist","Success":False})   

            admin = mongo.db.super_admin.find_one({"email": super_admin_email, 'super_adminid': super_adminid})
            if not mongo.db.super_admin.find_one({"email": super_admin_email}):
                return jsonify({"message":"super Admin email not found.","success":False})

            if not mongo.db.super_admin.find_one({"super_adminid": super_adminid}):
                return jsonify({"message": "super admin id  does not exist","Success":False})    
            if not admin:
                return jsonify({'message': 'super Admin email and super admin ID do not match.',"success":False})      
       

            if mongo.db.user.find_one({'empid': empid, 'company': company, 'department':department,'location': location}):
                return {'message': 'empid , company name,and location already exists',"success":False}     
        #----------------adding profile pic----------------

            if profile_pic:
                if profile_pic.filename == '':
                    return jsonify({'message': 'profile picture file not selected',"success":False})
                if profile_pic and allowed_file(profile_pic.filename):
                    filename = secure_filename(profile_pic.filename)
                    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else: 
                filename = None        
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pwd_hash = generate_password_hash(password)
        # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # verify email token generate
            # token = s.dumps(email, salt='email-confirmation-key')
        # save user information in the database
            mongo.db.user.insert_one({                                   #-------users is collection of database
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
            "super_adminid":super_adminid,
            "super_admin_email" : super_admin_email,
            "adminid":False,
            "admin_email" : False,
            # "token": token,
            "created_at": created_at,
            # "_verify":False
            })
            return jsonify({'message':'user registered successfully','success':True})   
        else:
            return jsonify({"message": "required all fields","success":False})    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False}) 

# ----------super admin adding admins----------------------
@super_admin.post("/super_add_admins")
def super_admin_addadmins():
    jwtoken = request.headers.get('Authorization')
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token',"success":False})     

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found',"success":False})  
        if admin:
            required_params = ['first_name','last_name', 'super_adminid', 'company', 'location', 'department','email', 
            'password', 'contact','super_admin_email']
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
            contact = data["contact"] 
            super_adminid = data.get('super_adminid')
            super_admin_email = data.get('super_admin_email')
            
            # validate first name
            if not firstname_regex.match(first_name):
                return jsonify({"message":'first name should be 3 to 10 characters only alphabets',"Success":False})   

            # validate last name
            if not firstname_regex.match(last_name):
                return jsonify({"message":'last name should be 3 to 10 characters only alphabets',"Success":False})

            # validate company name
            if not company_regex.match(company):
                return jsonify({"message":'company should be 3 to 10 characters only alphabets',"Success":False})  

            # validate department name
            if not company_regex.match(department):
                return jsonify({"message":'department should be 3 to 10 characters only alphabets',"Success":False})

            # validate location
            if not firstname_regex.match(location):
                return jsonify({"message":'location should be 3 to 10 characters only alphabets',"Success":False})          

            # validate adminid
            if not diffid_regex.match(empid):
                return jsonify({"message":'admin id should be 1 to 10 numeric only',"Success":False})          


            # Validate password
            # if not validate_password(password):
            #     return jsonify({"message":'Password must contain 8 to 16 characters,including at least alphanumeric,1 captial letter and special characters',"Success":False})    

            # Validate email
            if not email_regex.match(email):
                return jsonify({"message": "Invalid email","Success":False})  
            # Validate contact
            if not contact_regex.match(contact):
                return jsonify({"message": "Invalid contact number","Success":False})  
            # checking existing email
            if mongo.db.user.find_one({"email": email}):
                return jsonify({"message": "Email already exists","Success":False}) 

            if mongo.db.admin.find_one({"email": email}):
                return jsonify({"message": "email already exist","Success":False})   

            admin = mongo.db.super_admin.find_one({"email": super_admin_email, 'super_adminid': super_adminid})
            if not mongo.db.super_admin.find_one({"email": super_admin_email}):
                return jsonify({"message":"super Admin email not found.","success":False})

            if not mongo.db.super_admin.find_one({"super_adminid": super_adminid}):
                return jsonify({"message": "super admin id  does not exist","Success":False})    
            if not admin:
                return jsonify({'message': 'super Admin email and super admin ID do not match.',"success":False})      
       

            if mongo.db.admin.find_one({'empid': empid, 'company': company, 'department':department,'location': location}):
                return {'message': 'empid , company name,and location already exists',"success":False}     
        #----------------adding profile pic----------------

            if profile_pic:
                if profile_pic.filename == '':
                    return jsonify({'message': 'profile picture file not selected',"success":False})
                if profile_pic and allowed_file(profile_pic.filename):
                    filename = secure_filename(profile_pic.filename)
                    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
            else: 
                filename= None        
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pwd_hash = generate_password_hash(password)
        # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # verify email token generate
            # token = s.dumps(email, salt='email-confirmation-key')
        # save user information in the database
            mongo.db.user.insert_one({                                   #-------users is collection of database
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
            "super_adminid":super_adminid,
            "super_admin_email" : super_admin_email,
            # "token": token,
            "created_at": created_at,
            # "_verify":False
            })
            return jsonify({'message':'admin registered successfully','success':True})   
        else:
            return jsonify({"message": "required all fields","success":False})    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False}) 
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False}) 
#------------------------super admin delete users----------------------------------------------------
@super_admin.delete("/super_userdelete")
def super_user_delete():
    jwtoken = request.headers.get('Authorization')
    tokens = mongo.db.super_admin.find_one({"jwtoken":jwtoken})
    if not jwtoken:
        return jsonify({'message': 'Missing authorization token'})     

    try:
        jwtoken = jwtoken.split(" ")[1]
        decoded_token = jwt.decode(jwtoken, "jwtsecretkey", algorithms=["HS256"])
        email = decoded_token['email']
        admin = mongo.db.super_admin.find_one({'email': email,'jwtoken':jwtoken})
        if not admin:
            return jsonify({'message': 'super admin not found'}),  
        data = request.form
        email = data['email']
        users = mongo.db.user.find_one({'email':email})   
        if users:
            # if users['admin_email'] != admin['email']:  # check if the admin who created the user is the same as the admin making the delete request
            #     return jsonify({"message":"You are not authorized to delete this user"}),  

            mongo.db.user.delete_one({'email':email})
            return jsonify({'message': 'User Account deleted successfully',"success":True})
        else:
            return jsonify({"message":"user email not found"})    

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired',"success":False})
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({'message': 'Invalid authorization token',"success":False})  
