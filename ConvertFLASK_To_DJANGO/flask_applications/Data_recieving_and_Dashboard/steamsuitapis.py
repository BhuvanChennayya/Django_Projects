from Data_recieving_and_Dashboard.packages import *
steamsuit = Blueprint('steamsuit', __name__)


def verifysteamcamera_rtsp(url, image_namereplace):
    directory_path = os.getcwd() + '/' + 'steamcamera_image'
    handle_uploaded_file(directory_path)
    present_time = replace_spl_char(str(datetime.now()))
    cam = cv2.VideoCapture(url)
    full_path = None
    if cam.isOpened() == True:
        while cam.isOpened():
            ret, frame = cam.read()
            if ret:
                name = image_namereplace + '_' + present_time + '.jpg'
                full_path = directory_path + '/' + name
                cv2.imwrite(full_path, frame)
                image_resizing(full_path)
                verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                return verfy_rtsp_response
                break
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()
    else:
        return False    

def check_license_of_camera(CamCount):
    print(CamCount)
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_ofeee_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_ofee_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_licenseee_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        # print('res ===', res)
        # print('device_location', res['device_location'])
        lic = res['device_location']
        split_data=lic.split('_')[1].split("l")
        while '' in split_data:
            split_data.remove('')
        print(split_data[0])
        print(type(CamCount))
        print(type(split_data[0]))
        if CamCount < int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status

@steamsuit.route('/check_license', methods=['GET'])
def checkingCamlicense():
    if 1:
    # try:
        ret = {'message': 'something went wrong with get brand details api', 'success': False}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        sheet_camera_count = 0
        # print('sheet_data',sheet_data)
        if sheet_data is not None:
            sheet_data_count = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
             #mongo.db.panel_data.count_documents({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']})
            unique_iplist = []
            if len(sheet_data_count) !=0:
                for kl , eachElements in enumerate(sheet_data_count):
                    if len(eachElements['data']) !=0:
                        if eachElements['data']['ip_address'] not in unique_iplist:
                            unique_iplist.append(eachElements['data']['ip_address'])
                sheet_camera_count= len(unique_iplist) 
            
        CamCount = mongo.db.steamsuit_cameras.count_documents({})#find()#find_one()#mongo.db.steamsuit_cameras.find({}).count()
        # print("camera -count ",CamCount)
        # print("sheet_data count",sheet_camera_count)
        CamCount = CamCount + sheet_camera_count
        if check_license_of_camera(CamCount):
            ret['message']='you have license to add the camera'
            ret['success']=True
        else:
            ret['message']="you don't have license to add the camera"
    # except Exception as error:
    #     ret['message'] = str(error)
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_eeof_camera 4", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@steamsuit.route('/add_maincameraIP', methods=['POST'])
def add_Acamera():
    ret = {'success': False, 'message':'something went wrong with add camera api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['cameraip', 'camera_brand', 'username', 'password', 'area', 'cameraname', 'department']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:            
            ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            cameraip = data['cameraip']
            department= data['department']
            brand = data['camera_brand']
            username = data['username']
            password = data['password']
            port = data['port']
            area = data['area']
            cameraname = data['cameraname']
            regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
            find_data = mongo.db.steamsuit_cameras.find_one({ "$or": [ { "main_camera.camera_ip": cameraip },{ "sub_camera.camera_ip": cameraip } ] })#({'camera_ip': cameraip})
            if find_data is None:
                if regex_pwd.search(password) == None:
                    ping_response = final_ping(cameraip)
                    if ping_response:
                        channelNo = '1'
                        rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                        if rtsp_response:
                            image_namereplace = (replace_spl_char_panel_area_plant( '_' + area))
                            rtsp_response_image = verifysteamcamera_rtsp(rtsp_response,image_namereplace)
                            if rtsp_response_image:
                                Additional_data = {
                                    'camera_ip': cameraip,
                                    'username': username,
                                    'password': password,
                                    'camera_brand': brand,
                                    'rtsp_port': port,
                                    'cameraname': cameraname, 
                                    'imagename': rtsp_response_image['image_name'],
                                    'image_height': rtsp_response_image['height'],
                                    'image_width': rtsp_response_image['width'],
                                    'cameraid': None,
                                    'roi_data': [],
                                    'tc_data': [],
                                    'cr_data': [],
                                    'ppe_data': [],
                                    'camera_status': True, 
                                    'rtsp_url':rtsp_response, 
                                    'timestamp': now_time_with_time(),
                                    'ai_solution': [],
                                    'analytics_status':'false'}                                                               
                                
                                final_data = {'department':department,
                                                   'area': area,
                                                   "main_camera":Additional_data,
                                                   "alarm_details":{},
                                                   "sub_camera":{}
                                                   }
                                result = mongo.db.steamsuit_cameras.insert_one(final_data)
                                if result.acknowledged:
                                    ret = {'success': True, 'message':'camera added successfully.','data':final_data}
                                else:
                                    ret['message'] = 'data is not inserted properly, please try once again.'
                            else:
                                ret['message'] = 'rtsp stream is not working, please try once again.'
                        else:
                            ret['message'] = " ".join(["rtsp url is not able create or format it, please enter camera brand == ", str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'})]) 
                    else:
                        ret['message'] = 'cameraip is not able ping.'
                else:
                    ret['message'] = 'camera password should not have any special characters.'
            else:
                ret['message'] = 'entered ip is already exist, please give the different ip address.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)






@steamsuit.route('/add_subcameraip', methods=['POST'])
def add_substreamcameraip():
    ret = {'success': False, 'message': 'something went wrong with add camera api with rtsp'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['cameraip', 'camera_brand', 'username', 'password','cameraname','id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            
        else:
            cameraip = data['cameraip']
            brand = data['camera_brand']
            username = data['username']
            password = data['password']
            port = data['port']
            cameraname = data['cameraname']
            
            regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
            find_data =mongo.db.steamsuit_cameras.find_one({ "$or": [ { "main_camera.camera_ip": cameraip },{ "sub_camera.camera_ip": cameraip } ] })#({'main_camera.rtsp_url': rtsp_url})#{ $or: [ { "main_camera.rtsp_url": rtsp_url },{ "sub_camera.rtsp_url": rtsp_url } ] } 
            if find_data is None:
                if regex_pwd.search(password) == None:
                    ping_response = final_ping(cameraip)
                    if ping_response:
                        channelNo = '1'
                        rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                        if rtsp_response:
                            image_namereplace = (replace_spl_char_panel_area_plant('_'))
                            rtsp_response_image = verifysteamcamera_rtsp(rtsp_response,image_namereplace)
                            if rtsp_response_image:
                                Additional_data = {
                                    'camera_ip': cameraip,
                                    'username': username,
                                    'password': password,
                                    'camera_brand': brand,
                                    'rtsp_port': port,
                                    'cameraname': cameraname, 
                                    'imagename': rtsp_response_image['image_name'],
                                    'image_height': rtsp_response_image['height'],
                                    'image_width': rtsp_response_image['width'],
                                    'cameraid': None,
                                    'roi_data': [],
                                    'tc_data': [],
                                    'cr_data': [],
                                    'ppe_data': [],
                                    'camera_status': True, 
                                    'rtsp_url':rtsp_response, 
                                    'timestamp': now_time_with_time(),
                                    'ai_solution': [],
                                    'analytics_status':'false'} 
                                final_data = {
                                                "sub_camera":Additional_data
                                                }
                                result = mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(data['id'])}, {'$set': final_data})#insert_one( final_data)
                                if result.modified_count > 0 :
                                    print("final_data=====",final_data)
                                    ret = {'success': True, 'message':'sub camera added successfully.'}
                                else:
                                    ret['message'] = 'data is not inserted properly, please try once again.'
                            else:
                                ret['message'] = 'rtsp stream is not working, please try once again.'
                        else:
                            ret['message'] = " ".join(["rtsp url is not able create or format it, please enter camera brand == ", str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'})]) 
                    else:
                        ret['message'] = 'cameraip is not able ping.'
                else:
                    ret['message'] = 'camera password should not have any special characters.'
            else:
                ret['message'] = 'entered ip is already exist, please try with different ipaddress camera.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)


@steamsuit.route('/add_maincamera_rtsp', methods=['POST'])
def add_Acamera_rtsp():
    ret = {'success': False, 'message': 'something went wrong with add camera api with rtsp'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['camera_brand',  'area', 'cameraname', 'rtsp_url',  'department']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            
        else:
            rtsp_url = data['rtsp_url']
            department = data['department']
            brand = data['camera_brand']
            area = data['area']
            cameraname = data['cameraname']
            regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
            find_data = mongo.db.steamsuit_cameras.find_one({ "$or": [ { "main_camera.rtsp_url": rtsp_url },{ "sub_camera.rtsp_url": rtsp_url } ] })#({'main_camera.rtsp_url': rtsp_url})
            if find_data is None:
                rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                if rtsp_return_data:
                    password = rtsp_return_data['password']
                    cameraip = rtsp_return_data['ipaddress']
                    username = rtsp_return_data['username']
                    port = rtsp_return_data['port']
                    if 1:
                        if regex_pwd.search(password) == None:
                            ping_response = True
                            if ping_response:
                                image_namereplace = (replace_spl_char_panel_area_plant('_' + area))
                                rtsp_response_image = verifysteamcamera_rtsp(rtsp_url,image_namereplace)
                                if rtsp_response_image:
                                    Additional_data ={'camera_ip': cameraip,
                                                   'username': username,
                                                   'password':     password,
                                                   'camera_brand': brand,
                                                   'rtsp_port': port,
                                                   'cameraname':cameraname,
                                                  'imagename':rtsp_response_image['image_name'],
                                                  'image_height': rtsp_response_image['height'],
                                                  'image_width': rtsp_response_image['width'],
                                                  'cameraid': None, 
                                                  'roi_data': [],
                                                  'tc_data': [],
                                                  'cr_data': [],
                                                  'ppe_data': [], 
                                                  'camera_status':True,
                                                  'rtsp_url': rtsp_url,
                                                  'timestamp': now_time_with_time(),
                                                  'ai_solution': [],'analytics_status':'false'}
                                    final_data = {'department':department,
                                                   'area': area,
                                                   "main_camera":Additional_data,
                                                   "alarm_details":{},
                                                   "sub_camera":{}
                                                   }
                                    result = mongo.db.steamsuit_cameras.insert_one( final_data)
                                    if result.acknowledged:
                                        print("final_data=====",final_data)
                                        ret = {'success': True, 'message':'camera added successfully.',"data":final_data}
                                    else:
                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                else:
                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                            else:
                                ret['message'] = 'cameraip is not able ping.'
                        else:
                            ret['message'] = 'camera password should not have any special characters.'
                else:
                    ret['message'] = 'rtsp url error.'
            else:
                ret['message'] = 'entered ip is already exist, please try with different ipaddress camera.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)




@steamsuit.route('/add_subcamera_rtsp', methods=['POST'])
def add_substreamcamera_rtsp():
    ret = {'success': False, 'message': 'something went wrong with add camera api with rtsp'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['camera_brand',  'cameraname', 'rtsp_url','id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            
        else:
            rtsp_url = data['rtsp_url']
            brand = data['camera_brand']
            cameraname = data['cameraname']            
            regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
            find_data = mongo.db.steamsuit_cameras.find_one({ "$or": [ { "main_camera.rtsp_url": rtsp_url },{ "sub_camera.rtsp_url": rtsp_url } ] } )#({'main_camera.rtsp_url': rtsp_url})#{ $or: [ { "main_camera.rtsp_url": rtsp_url },{ "sub_camera.rtsp_url": rtsp_url } ] } 
            if find_data is None:
                rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                if rtsp_return_data:
                    password = rtsp_return_data['password']
                    cameraip = rtsp_return_data['ipaddress']
                    username = rtsp_return_data['username']
                    port = rtsp_return_data['port']
                    if 1:
                        if regex_pwd.search(password) == None:
                            ping_response = True
                            if ping_response:
                                image_namereplace = (replace_spl_char_panel_area_plant( '_' ))
                                rtsp_response_image = verifysteamcamera_rtsp(rtsp_url,image_namereplace)
                                if rtsp_response_image:
                                    Additional_data ={'camera_ip': cameraip,
                                                   'username': username,
                                                   'password':     password,
                                                   'camera_brand': brand,
                                                   'rtsp_port': port,
                                                   'cameraname':cameraname,
                                                  'imagename':rtsp_response_image['image_name'],
                                                  'image_height': rtsp_response_image['height'],
                                                  'image_width': rtsp_response_image['width'],
                                                  'cameraid': None, 
                                                  'roi_data': [],
                                                  'tc_data': [],
                                                  'cr_data': [],
                                                  'ppe_data': [], 
                                                  'camera_status':True,
                                                  'rtsp_url': rtsp_url,
                                                  'timestamp': now_time_with_time(),
                                                  'ai_solution': [],'analytics_status':'false'}
                                    final_data = {
                                                   "sub_camera":Additional_data
                                                   }
                                    result = mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(data['id'])}, {'$set': final_data})#insert_one( final_data)
                                    if result.modified_count > 0 :
                                        print("final_data=====",final_data)
                                        ret = {'success': True, 'message':'sub camera added successfully.'}
                                    else:
                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                else:
                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                            else:
                                ret['message'] = 'cameraip is not able ping.'
                        else:
                            ret['message'] = 'camera password should not have any special characters.'
                else:
                    ret['message'] = 'rtsp url error.'
            else:
                ret['message'] = 'entered ip is already exist, please try with different ipaddress camera.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)


@steamsuit.route("/edit_Steamsuitcamera",methods=['POST'])
def editCAM():
    ret={"success":False,"message":"something went wrong with edit api."}
    data = request.json
    if data is  None:
        data = {}
    if isEmpty(data):
        datakeys = list(data.keys())
        request_key_array = [ 'id', 'area', 'department']
        check =  all(item in request_key_array for item in datakeys)
        print("all ajdkfkadjkf==== ",check) 
        if check is True:
            print("The list {} contains all elements of the list {}".format(request_key_array, datakeys))
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                print("data====", data)
                finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(data['id'])})
                if finddata is not None: 
                    print("data ---", finddata)
                    result = mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(data['id'])}, {'$set': data})
                    if result.modified_count > 0:
                        ret = {'message': 'camera details edited successfully.','success': True}
                    else:
                        ret['message'] = 'camera details not edited, please try once again.'
                else:
                    ret['message']='camera details is not found for given id.'
        else:
            ret['message'] ='you have given wrong parameters edit camera details.'
        # else:
        #     ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    else:
        ret['message']='you have missed data parameter to send.'
    return ret


@steamsuit.route("/Steamsuitalarmdetails",methods=['POST'])
def editALARMDETAILS():
    ret={"success":False,"message":"something went wrong with edit api."}
    data = request.json
    if data is  None:
        data = {}
    if isEmpty(data):
        datakeys = list(data.keys())
        request_key_array = [ 'id','alarm_type', 'alarm_ip_address','alarm_enable','alarm_version']
        check =  all(item in request_key_array for item in datakeys)
        if check is True:
            print("The list {} contains all elements of the list {}".format(request_key_array, datakeys))
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                alarm_enable = data['alarm_enable']
                if alarm_type is not None :
                    if  alarm_ip_address is not None :
                        if alarm_enable:
                            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(data['id'])})
                            if finddata is not None: 
                                result = mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(data['id'])}, {'$set':{"alarm_details" :{"alarm_type":alarm_type,"alarm_ip_address":alarm_ip_address,"alarm_enable":alarm_enable}}})
                                if result.modified_count > 0:
                                    ret = {'message': 'alarm details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'alarm details not edited, please try once again.'
                            else:
                                ret['message']='alarm details is not found for given id.'
                        elif alarm_ip_address is not None and alarm_enable is not None :
                            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(data['id'])})
                            if finddata is not None: 
                                result = mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(data['id'])}, {'$set':{"alarm_details" :{"alarm_type":alarm_type,"alarm_ip_address":alarm_ip_address,"alarm_enable":alarm_enable}}})
                                if result.modified_count > 0:
                                    ret = {'message': 'alarm details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'alarm details not edited, please try once again.'
                            else:
                                ret['message']='alarm details is not found for given id.'
                        else:
                            ret['message']='alarm is enabled, alarm ipaddress should not be None.'
                    else:
                        ret['message']=' alarm ipaddress should not be None.'
                else:
                    ret['message']="alarm type is should not be None."
        else:
            ret['message'] ='you have given wrong parameters edit camera details.'
    else:
        ret['message']='you have missed data parameter to send.'
    return ret


@steamsuit.route('/get_steamroi_image/<image_file>', methods=['GET'])
def get_steamroi_image(image_file):
    try:
        base_path = os.path.join(os.getcwd(), 'steamcamera_image')
        response = send_from_directory(base_path, image_file)
        return response
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_steamroi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return str(error)
    


@steamsuit.route('/GetSteamCamdetails', methods=['GET'])
def GetSteamCamdetails():
    ret = {'success': False, 'message': 'something went wrong with add camera api with rtsp'}    
    find_data = list(mongo.db.steamsuit_cameras.find({ "$or": [ { "main_camera.rtsp_url":{"$ne" : None}   },{ "sub_camera.rtsp_url":{"$ne" : None}  } ] } ))#({'main_camera.rtsp_url': rtsp_url})#{ $or: [ { "main_camera.rtsp_url": rtsp_url },{ "sub_camera.rtsp_url": rtsp_url } ] } 
    if len(find_data) !=0:
        # print(find_data)
        ret = {"message":find_data,"success":True}
    else:
        ret['message']="data not found. please try to add the camera."
                
    return parse_json(ret)




@steamsuit.route('/GETstreamWisedata', methods=['POST'])
def GETstreamWisedata():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'steamtype']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            steamtype = data['steamtype']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if steamtype=='main':
                    ret = {"message":finddata['main_camera'],"success":True}
                elif steamtype=='sub':
                    ret = {"message":finddata['sub_camera'],"success":True}
                else:
                    ret['message']='please give proper steamtype.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)



@steamsuit.route('/add_streamsuitroi', methods=['POST'])
def camera_adding_mainsteamsuitroi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'roi_data','steamtype']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            roi_data = data['roi_data']
            steamtype = data['steamtype']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if roi_data is not None:
                    if type(roi_data) == list:
                        if len(roi_data) != 0:   
                            if  steamtype == 'main': 
                                result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.roi_data': roi_data}}))
                                if result.modified_count > 0:
                                    ret = {'message': 'roi added to main successfully.','success': True}
                                else:
                                    ret['message'] = 'roi not adeed.'
                            elif  steamtype == 'sub':
                                result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.roi_data': roi_data}}))
                                if result.modified_count > 0:
                                    ret = {'message': 'roi added to substeam successfully.','success': True}
                                else:
                                    ret['message'] = 'roi not adeed.'
                        else:
                            ret['message'] = 'please give proper input data, try once again.'
                    else:
                        ret['message'] = 'please give proper roi data, it should be list type.'
                else:
                    ret['message'] = 'please give proper roi data, it should not none type.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)

@steamsuit.route('/add_streamsuitppe', methods=['POST'])
def camera_addingsteamsuitPPE():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ppe_data','steamtype']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            ppe_data = data['ppe_data']
            steamtype = data['steamtype']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if ppe_data is not None:
                    if type(ppe_data) == list:
                        if len(ppe_data) != 0:   
                            if  steamtype == 'main': 
                                result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.ppe_data': ppe_data}}))
                                if result.modified_count > 0:
                                    ret = {'message': 'ppe data added to main successfully.','success': True}
                                else:
                                    ret['message'] = 'ppe data not added.'
                            elif  steamtype == 'sub':
                                result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.ppe_data': ppe_data}}))
                                if result.modified_count > 0:
                                    ret = {'message': 'ppe data added to substeam successfully.','success': True}
                                else:
                                    ret['message'] = 'ppe data not added.'
                        else:
                            ret['message'] = 'please give proper input data, try once again.'
                    else:
                        ret['message'] = 'please give proper roi data, it should be list type.'
                else:
                    ret['message'] = 'please give proper roi data, it should not none type.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return parse_json(ret)


@steamsuit.route('/edit_streamroi', methods=['POST'])
def camera_edit_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'roi_data','roi_id','steamtype']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            roi_id = data['roi_id']
            roi_data = data['roi_data']
            steamtype = data['steamtype']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(roi_data) == list:
                    if len(roi_data) != 0:
                        if steamtype =='main':
                            fetch_roi_data = finddata['main_camera']['roi_data']#main_camera#sub_camera
                            if len(fetch_roi_data) != 0:
                                if len(fetch_roi_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.roi_data': roi_data}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not updated.'
                                elif len(fetch_roi_data) > 1:
                                    update_data = []
                                    if len(roi_data) == 1:
                                        for __, i in enumerate(fetch_roi_data):
                                            if int(i['roi_id']) == int(roi_data[0][ 'roi_id']):
                                                i['bb_box'] = roi_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.roi_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not updated.'
                                    elif len(roi_data) > 1:
                                        update_data = []
                                        for __, i in enumerate(fetch_roi_data):
                                            for __, jjk in enumerate(fetch_roi_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    i['bb_box'] = jjk['bb_box']
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = (mongo.db.steamsuit_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.roi_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not updated.'
                                    else:
                                        ret['message'] = 'There is no roi region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                                
                        elif steamtype =='sub':
                            fetch_roi_data = finddata['sub_camera']['roi_data']
                            if len(fetch_roi_data) != 0:
                                if len(fetch_roi_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.roi_data': roi_data}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not updated.'
                                elif len(fetch_roi_data) > 1:
                                    update_data = []
                                    if len(roi_data) == 1:
                                        for __, i in enumerate(fetch_roi_data):
                                            if int(i['roi_id']) == int(roi_data[0][ 'roi_id']):
                                                i['bb_box'] = roi_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.roi_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not updated.'
                                    elif len(roi_data) > 1:
                                        update_data = []
                                        for __, i in enumerate(fetch_roi_data):
                                            for __, jjk in enumerate(fetch_roi_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    i['bb_box'] = jjk['bb_box']
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = (mongo.db.steamsuit_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.roi_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not updated.'
                                    else:
                                        ret['message'] = 'There is no roi region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        else:
                            ret['message'] ='please give proper steamtype.'
                    else:
                        ret['message'] = 'roi data should not be empty list.'
                else:
                    ret['message'] = 'roi data type should be list'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@steamsuit.route('/delete_steam_roi', methods=['POST'])
def camera_delete_roi():
    ret = {'success': False, 'message':'something went wrong with delete_roi roi api'}
    if 1:
    # try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_id','steamtype']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                steamtype = data['steamtype']
                print("i-----",data)
                finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if steamtype =='main': 
                            roi_data = finddata["main_camera"]['roi_data']
                            if len(roi_data) != 0:                            
                                update_data = []
                                if len(roi_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.roi_data': []}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                                elif len(roi_data) > 1:
                                    for __, i in enumerate(roi_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            roi_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.roi_data': update_data}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'roi data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                                else:
                                    ret['message'] = 'There is no roi region the camrea, please try to add.'
                        elif steamtype =='sub': 
                            update_data = []
                            roi_data = finddata["sub_camera"]['roi_data']
                            if len(roi_data) == 1:
                                result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.roi_data': []}})
                                if result.modified_count > 0:
                                    ret = {'message':'roi data delete successfully.','success': True}
                                else:
                                    ret['message'] = 'roi not deleted.'
                            elif len(roi_data) > 1:
                                for __, i in enumerate(roi_data):
                                    if int(i['roi_id']) == int(roi_id):
                                        roi_data.remove(i)
                                        pass
                                    else:
                                        update_data.append(i)
                                result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.roi_data': update_data}})
                                if result.modified_count > 0:
                                    ret = {'message': 'roi data delete successfully.','success': True}
                                else:
                                    ret['message'] = 'roi not deleted.'
                            else:
                                ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            ret['message']='give proper steamtype.'
                        
                    else:
                        ret['message'] = 'please give proper roi data, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] =" ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    # except Exception as error:
    #     ret['message'] =" ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_roi 1", str(error), " ----time ---- ", now_time_with_time()]))
    return ret




def UPDATECRDATATOEXISTINGONE(fINDCRDATA,GivenCRDATA):
    find_cr = fINDCRDATA
    initial_len = len(find_cr)
    find_cr.append(GivenCRDATA)
    if initial_len > len(find_cr) :
        print('finall cr data ===', len(find_cr))
    return find_cr


def CHECKTHEDATAKEYIDEXISTINCRDATA(find_data,roiid):
    print("find_data===", find_data)
    print("roi-id",roiid)
    id_status = True
    for i , j in enumerate(find_data):  
        print('lllll====lllll ',j)
        if j['roi_id']=='' or j['roi_id'] == None:
            pass
        elif j['roi_id']==roiid:
            id_status = False
    return id_status

@steamsuit.route('/add_steamcr_data', methods=['POST'])
def camera_add_cr_data():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'cr_data','steamtype']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            cr_data = data['cr_data']
            steamtype = data['steamtype']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if cr_data is not None:
                    if type(cr_data) == list:
                        if len(cr_data) != 0:
                            print("found_data=", finddata['main_camera']['cr_data'])
                            print("given_data=",cr_data)
                            if   steamtype =='main': 
                                if len(cr_data)==1:
                                    if cr_data[0]['full_frame']:
                                        if cr_data[0]['bb_box'] ==''and cr_data[0]['area_name']=='':
                                            #any([v==None for v in d.values()])
                                            if check_arraydictionaryishavinganynonevalue(cr_data[0]['data_object']):
                                                if check_dataobjects_of_cr_data(cr_data[0]['data_object']):
                                                    result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.cr_data':cr_data}}))
                                                    if result.modified_count > 0:
                                                        ret = {'message': 'cr data added successfully.','success': True}
                                                    else:
                                                        ret['message'] = 'cr data not adeed.'
                                                else:
                                                    ret['message']='in data object min count and max count should not be equal and min cout should be less than max count, please check and give proper data parameters.'          
                                            else:
                                                ret['message']='cr data data objects values should not be none.'
                                        else:
                                            ret['message']='bb_box or area_name should be empty string for full frame.'
                                    else:
                                        if cr_data[0]['bb_box'] is not None and cr_data[0]['bb_box'] !='':
                                            if len(cr_data[0]['data_object']) !=0:
                                                if check_arraydictionaryishavinganynonevalue(cr_data[0]['data_object']):
                                                    if check_dataobjects_of_cr_data(cr_data[0]['data_object']):
                                                        if cr_data[0]['area_name'] is not None and cr_data[0]['area_name'] !='':
                                                            if len(finddata['main_camera']['cr_data']) !=0:
                                                                print("cr_data--------------------",cr_data)
                                                                print("cr_data",cr_data[0]['roi_id'])
                                                                if CHECKTHEDATAKEYIDEXISTINCRDATA(finddata['main_camera']['cr_data'],cr_data[0]['roi_id']):
                                                                    final_cr_data = UPDATECRDATATOEXISTINGONE(finddata['main_camera']['cr_data'],cr_data[0])
                                                                    # final_cr_data = finddata['cr_data'].append(cr_data[0])
                                                                    if len(final_cr_data) != 0 :
                                                                        print("final_cr_data===",final_cr_data)
                                                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)},{'$set': {'main_camera.cr_data':final_cr_data}}))
                                                                        if result.modified_count > 0:
                                                                            ret = {'message': 'cr data added successfully.','success': True}
                                                                        else:
                                                                            ret['message'] = 'cr data not adeed.'
                                                                    else:
                                                                        ret['message'] = 'cr data is not added, deu to some internal issue'
                                                                else:
                                                                    ret['message']='roi key id already exists, please give proper one'
                                                            else:
                                                                final_cr_data = finddata['main_camera']['cr_data'].append(cr_data[0])
                                                                print("final_cr_data===",final_cr_data)
                                                                result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)},{'$set': {'main_camera.cr_data':cr_data}}))
                                                                if result.modified_count > 0:
                                                                    ret = {'message': 'cr data added successfully.','success': True}
                                                                else:
                                                                    ret['message'] = 'cr data not adeed.'

                                                        else:
                                                            ret['message']='in cr data area name should not be none or empty.'
                                                    else:
                                                        ret['message']='in data object min count and max count should not be equal and min cout should be less than max count, please check and give proper data parameters.'
                                                else:
                                                    ret['message']='in cr data data_object parameter none values in it, please check and correct it.'
                                            else:
                                                ret['message']='in cr data data_object parameter should not be empty.'
                                        else:
                                            ret['message']='bb_box cr data should not be none or empty.'
                                else:
                                    ret['message'] = 'length of cr data is more than one, it should be only one data element.'            
                                    
                            elif   steamtype =='sub': 
                                if len(cr_data)==1:
                                    if cr_data[0]['full_frame']:
                                        if cr_data[0]['bb_box'] ==''and cr_data[0]['area_name']=='':
                                            #any([v==None for v in d.values()])
                                            if check_arraydictionaryishavinganynonevalue(cr_data[0]['data_object']):
                                                if check_dataobjects_of_cr_data(cr_data[0]['data_object']):
                                                    result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.cr_data':cr_data}}))
                                                    if result.modified_count > 0:
                                                        ret = {'message': 'cr data added successfully.','success': True}
                                                    else:
                                                        ret['message'] = 'cr data not adeed.'
                                                else:
                                                    ret['message']='in data object min count and max count should not be equal and min cout should be less than max count, please check and give proper data parameters.'          
                                            else:
                                                ret['message']='cr data data objects values should not be none.'
                                        else:
                                            ret['message']='bb_box or area_name should be empty string for full frame.'
                                    else:
                                        if cr_data[0]['bb_box'] is not None and cr_data[0]['bb_box'] !='':
                                            if len(cr_data[0]['data_object']) !=0:
                                                if check_arraydictionaryishavinganynonevalue(cr_data[0]['data_object']):
                                                    if check_dataobjects_of_cr_data(cr_data[0]['data_object']):
                                                        if cr_data[0]['area_name'] is not None and cr_data[0]['area_name'] !='':
                                                            if len(finddata['sub_camera']['cr_data']) !=0:
                                                                print("cr_data--------------------",cr_data)
                                                                print("cr_data0",cr_data[0]['roi_id'])
                                                                if CHECKTHEDATAKEYIDEXISTINCRDATA(finddata['sub_camera']['cr_data'],cr_data[0]['roi_id']):
                                                                    final_cr_data = UPDATECRDATATOEXISTINGONE(finddata['sub_camera']['cr_data'],cr_data[0])
                                                                    if len(final_cr_data) != 0 :
                                                                        print("final_cr_data===",final_cr_data)
                                                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)},{'$set': {'sub_camera.cr_data':final_cr_data}}))
                                                                        if result.modified_count > 0:
                                                                            ret = {'message': 'cr data added successfully.','success': True}
                                                                        else:
                                                                            ret['message'] = 'cr data not adeed.'
                                                                    else:
                                                                        ret['message'] = 'cr data is not added, deu to some internal issue'
                                                                else:
                                                                    ret['message']='roi key id already exists, please give proper one'
                                                            else:
                                                                final_cr_data = finddata['sub_camera']['cr_data'].append(cr_data[0])
                                                                print("final_cr_data===",final_cr_data)
                                                                result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)},{'$set': {'sub_camera.cr_data':cr_data}}))
                                                                if result.modified_count > 0:
                                                                    ret = {'message': 'cr data added successfully.','success': True}
                                                                else:
                                                                    ret['message'] = 'cr data not adeed.'

                                                        else:
                                                            ret['message']='in cr data area name should not be none or empty.'
                                                    else:
                                                        ret['message']='in data object min count and max count should not be equal and min cout should be less than max count, please check and give proper data parameters.'
                                                else:
                                                    ret['message']='in cr data data_object parameter none values in it, please check and correct it.'
                                            else:
                                                ret['message']='in cr data data_object parameter should not be empty.'
                                        else:
                                            ret['message']='bb_box cr data should not be none or empty.'
                                else:
                                    ret['message'] = 'length of cr data is more than one, it should be only one data element.'  
                            else:
                                ret['message']='please give proper steamtype.'                           
                        else:
                            ret['message'] ='cr data is not given please give proper data.'         
                    else:
                        ret['message'] = 'please give proper cr data, it should be list type.'
                else:
                    ret['message'] = 'please give proper cr data, it should not none type.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@steamsuit.route('/edit_steamcrdata', methods=['POST'])
def camera_editCRroi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'steamtype', 'cr_data','roi_id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            roi_id = data['roi_id']
            steamtype = data['steamtype']
            cr_data = data['cr_data']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(cr_data) == list:
                    if len(cr_data) != 0:
                        if steamtype=='main':
                            fetch_cr_data = finddata['main_camera']['cr_data']
                            if len(fetch_cr_data) != 0:
                                if len(fetch_cr_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.cr_data': cr_data}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not updated.'
                                elif len(fetch_cr_data) > 1:
                                    update_data = []
                                    if len(cr_data) == 1:
                                        for __, i in enumerate(fetch_cr_data):
                                            if int(i['roi_id']) == int(cr_data[0][ 'roi_id']):
                                                i['bb_box'] = cr_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.cr_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    elif len(cr_data) > 1:
                                        update_data = []
                                        for __, i in enumerate(fetch_cr_data):
                                            for __, jjk in enumerate(fetch_cr_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    i['bb_box'] = jjk['bb_box']
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = (mongo.db.steamsuit_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.cr_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    else:
                                        ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        elif  steamtype=='sub':
                            fetch_cr_data = finddata['sub_camera']['cr_data']
                            if len(fetch_cr_data) != 0:
                                if len(fetch_cr_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.cr_data': cr_data}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not updated.'
                                elif len(fetch_cr_data) > 1:
                                    update_data = []
                                    if len(cr_data) == 1:
                                        for __, i in enumerate(fetch_cr_data):
                                            if int(i['roi_id']) == int(cr_data[0][ 'roi_id']):
                                                i['bb_box'] = cr_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.cr_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    elif len(cr_data) > 1:
                                        update_data = []
                                        for __, i in enumerate(fetch_cr_data):
                                            for __, jjk in enumerate(fetch_cr_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    i['bb_box'] = jjk['bb_box']
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = (mongo.db.steamsuit_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.cr_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    else:
                                        ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        else:
                            ret['message']='please give the proper steamtype.'
                    else:
                        ret['message'] = 'cr_data data should not be empty list.'
                else:
                    ret['message'] = 'cr_data data type should be list'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@steamsuit.route('/delete_steam_cr_data', methods=['POST'])
def camera_delete_cr_data():
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if 1:
    # try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_id', 'steamtype']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                steamtype = data['steamtype']
                finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if steamtype == 'main':
                            cr_data = finddata['main_camera']['cr_data']
                            if len(cr_data) != 0:
                                update_data = []
                                if len(cr_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.cr_data': []}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                                elif len(cr_data) > 1:
                                    for __, i in enumerate(cr_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            cr_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.cr_data': update_data}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                            else:
                                ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                        elif steamtype == 'sub':
                            cr_data = finddata['sub_camera']['cr_data']
                            if len(cr_data) != 0:
                                update_data = []
                                if len(cr_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.cr_data': []}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                                elif len(cr_data) > 1:
                                    for __, i in enumerate(cr_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            cr_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.cr_data': update_data}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                            else:
                                ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                        else:
                            ret['message']='please give proper steamtype.'
                    else:
                        ret['message'] = 'please give proper cr_data data, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    # except Exception as error:
    #     ret['message'] = " ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ])
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_cr_data 1", str(error), " ----time ---- ", now_time_with_time()]))
    return ret




def CHECKDICTIONARY_HAVING_ANY_NONE_VALUE(dictionary):
    dictionary_status = True
    for element in dictionary:
        if element is None or element ==' ':
            dictionary_status= True
    return dictionary_status

def CHECKTCDATAKEYIDISEXIST(find_data,roiid):
    id_status = True
    for i , j in enumerate(find_data):  
        if j['roi_id']==roiid:
            id_status = False
    return id_status

def TCDATAMODIFICATION_STEAM(dbtcdata,requestdata):
    if dbtcdata is not None and requestdata is not None :
        if len(dbtcdata) !=0:
            if len(requestdata)==1:
                if requestdata[0] is not None:
                    dbtcdata.append(requestdata[0])
        else:
            dbtcdata = requestdata
    return dbtcdata

@steamsuit.route('/add_steamtc_data', methods=['POST'])
def camera_add_tc_data():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'tc_data','steamtype']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            tc_data = data['tc_data']
            steamtype = data['steamtype']
            if id is not None:
                finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if tc_data is not None:
                        if type(tc_data) == list:
                            if len(tc_data) != 0:
                                if steamtype =='main':
                                    if len(tc_data) ==1:
                                        print("tc -data ", tc_data[0])
                                        fetched_tc_data =  tc_data[0]
                                        print("fetched_tc_data---", fetched_tc_data)
                                        if len(fetched_tc_data['class_name']) !=0:
                                            if isEmpty(fetched_tc_data['line_bbox']):
                                                if CHECKDICTIONARY_HAVING_ANY_NONE_VALUE(fetched_tc_data['line_bbox']):
                                                    if CHECKTCDATAKEYIDISEXIST(finddata['main_camera']['tc_data'],fetched_tc_data['roi_id']):
                                                        returntcdata = TCDATAMODIFICATION_STEAM(finddata['main_camera']['tc_data'],tc_data)
                                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.tc_data': returntcdata}}))
                                                        if result.modified_count > 0:
                                                            ret = {'message': 'traffic count data added successfully.', 'success': True}
                                                        else:
                                                            ret['message'] = 'traffic count data not adeed.'                                                            
                                                    else:
                                                        ret['message']='roi key id already exists, please give different one while adding the tc data.'
                                                else:
                                                    ret['message']='line bbox should not be have any none or empty values in dictionary.'
                                            else:
                                                ret['message']='line bbox should not be empty dictionary.'
                                        else:
                                            ret['message']='in tc data class name should not be empty list.'
                                    else:
                                        ret['message'] ='tc data is containing multiple data objects.'
                                elif steamtype =='sub':
                                    if len(tc_data) ==1:
                                        print("tc -data ", tc_data[0])
                                        fetched_tc_data =  tc_data[0]
                                        print("fetched_tc_data---", fetched_tc_data)
                                        if len(fetched_tc_data['class_name']) !=0:
                                            if isEmpty(fetched_tc_data['line_bbox']):
                                                if CHECKDICTIONARY_HAVING_ANY_NONE_VALUE(fetched_tc_data['line_bbox']):
                                                    if CHECKTCDATAKEYIDISEXIST(finddata['sub_camera']['tc_data'],fetched_tc_data['roi_id']):
                                                        returntcdata = TCDATAMODIFICATION_STEAM(finddata['sub_camera']['tc_data'],tc_data)
                                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.tc_data': returntcdata}}))
                                                        if result.modified_count > 0:
                                                            ret = {'message': 'traffic count data added successfully.', 'success': True}
                                                        else:
                                                            ret['message'] = 'traffic count data not adeed.'                                                            
                                                    else:
                                                        ret['message']='roi key id already exists, please give different one while adding the tc data.'
                                                else:
                                                    ret['message']='line bbox should not be have any none or empty values in dictionary.'
                                            else:
                                                ret['message']='line bbox should not be empty dictionary.'
                                        else:
                                            ret['message']='in tc data class name should not be empty list.'
                                    else:
                                        ret['message'] ='tc data is containing multiple data objects.'
                                else:
                                    ret['message']='please give proper steamtype.'
                        else:
                            ret['message'] = 'please give proper traffic data, it should be list type.'
                    else:
                        ret['message'] = 'please give proper traffic data, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] =  'give the proper mongodb id, id should not be none type.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@steamsuit.route('/edit_steam_tcdata', methods=['POST'])
def camera_edittcroi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'steamtype', 'tc_data','roi_id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            roi_id = data['roi_id']
            steamtype = data['steamtype']
            tc_data = data['tc_data']
            finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(tc_data) == list:
                    if len(tc_data) != 0:
                        if steamtype =='main':
                            fetch_tc_data = finddata['main_camera']['tc_data']
                            if len(fetch_tc_data) != 0:
                                if len(fetch_tc_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.tc_data': tc_data}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not updated.'
                                elif len(fetch_tc_data) > 1:
                                    update_data = []
                                    if len(tc_data) == 1:
                                        for __, i in enumerate(fetch_tc_data):
                                            if int(i['roi_id']) == int(tc_data[0][ 'roi_id']):
                                                i['bb_box'] = tc_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.tc_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    elif len(tc_data) > 1:
                                        update_data = []
                                        for __, i in enumerate(fetch_tc_data):
                                            for __, jjk in enumerate(fetch_tc_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    i['bb_box'] = jjk['bb_box']
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'main_camera.tc_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    else:
                                        ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                                
                        elif steamtype =='sub':
                            fetch_tc_data = finddata['sub_camera']['tc_data']
                            if len(fetch_tc_data) != 0:
                                if len(fetch_tc_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.tc_data': tc_data}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not updated.'
                                elif len(fetch_tc_data) > 1:
                                    update_data = []
                                    if len(tc_data) == 1:
                                        for __, i in enumerate(fetch_tc_data):
                                            if int(i['roi_id']) == int(tc_data[0][ 'roi_id']):
                                                i['bb_box'] = tc_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.tc_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    elif len(tc_data) > 1:
                                        update_data = []
                                        for __, i in enumerate(fetch_tc_data):
                                            for __, jjk in enumerate(fetch_tc_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    i['bb_box'] = jjk['bb_box']
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = (mongo.db.steamsuit_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'sub_camera.tc_data': update_data}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    else:
                                        ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                    else:
                        ret['message'] = 'tc_data data should not be empty list.'
                else:
                    ret['message'] = 'tc_data data type should be list'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@steamsuit.route('/delete_steam_tc_data', methods=['POST'])
def camera_delete_tc_data():
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if 1:
    # try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_id', 'steamtype']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                steamtype = data['steamtype']
                finddata = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if steamtype == 'main':
                            tc_data = finddata['main_camera']['tc_data']
                            if len(tc_data) != 0:
                                update_data = []
                                if len(tc_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.tc_data': []}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                                elif len(tc_data) > 1:
                                    for __, i in enumerate(tc_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            tc_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'main_camera.tc_data': update_data}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                            else:
                                ret['message'] = 'There is no tc_data region the camrea, please try to add.'
                        if steamtype == 'sub':
                            tc_data = finddata['sub_camera']['tc_data']
                            if len(tc_data) != 0:
                                update_data = []
                                if len(tc_data) == 1:
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.tc_data': []}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                                elif len(tc_data) > 1:
                                    for __, i in enumerate(tc_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            tc_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.steamsuit_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'sub_camera.tc_data': update_data}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                            else:
                                ret['message'] = 'There is no tc_data region the camrea, please try to add.'
                        
                    else:
                        ret['message'] = 'please give proper tc_data data, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    # except Exception as error:
    #     ret['message'] = " ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
    #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_tc_data 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret



def update_set_data_to_table(inputdata):
    try :
        print("**************************************input data -----------",inputdata)
        # L1datatablecreation()
        databasedetails = { 
            "sql_objecttable_name" :"tsk_ss_l1" ,
            "user": "docketrun",
            "password" :"docketrun",
            "host": "localhost",
            "port": "5432",
            "database" :"docketrundb",
            "sslmode":"disable"}
        if 1:
        # try:
            conn = psycopg2.connect(user = databasedetails['user'],  password =databasedetails['password'],  host = databasedetails['host'], port = databasedetails['port'],   database = databasedetails['database'],  sslmode=databasedetails['sslmode'])
        else:
        # except:
            conn = 0
            
        if conn:
            print("************************************************************************************update values ******************")
            cursor = conn.cursor()
            print("dsksdfjsdakfksadj------------------------------cursor connection-----")
            # try:
            #     print("CREATING TABLE ---tsk_ss44444444_l1tsk_ss_4l1tsk_ss_444l14444tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1--")
            #     query = '''CREATE TABLE IF NOT EXISTS tsk_ss_l1(id SERIAL PRIMARY KEY,
            # set1 integer,
            # set2 integer,
            # set3 integer,
            # set4 integer,
            # person_count_manual integer,
            # person_count_auto integer,
            # analytics_stop_time integer );'''
            #     cursor.execute(query) 
            #     conn.commit()
            #     # print("cursor === rowcount === ",cursor.rowcount)
            #     creation_query = cursor.rowcount 
            #     if creation_query == -1 :
            #         tablecreationstatus = True
            #         print("streamsuitl1data table successfully created.")
            #     else:
            #         print("streamsuitl1data table is not created.")
                    
            # except Exception as  error:
            #     print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - UPDATE", error)
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- L1datatablecreation UPDATE 1", str(error), " ----time ---- ", now_time_with_time()]))
            print ("[INFO] DB connected successfully for l1data inserting send  testopc")
            # while 1:
            try :
                print('-------------------------------------l1data 1.0')
            
                data  =[]
                try:
                    print('-------------------------------------l1data 1.1')
                    cursor.execute('SELECT * FROM '+databasedetails['sql_objecttable_name']+' ORDER BY id desc')
                    print('-------------------------------------l1data 1.2')
                except psycopg2.errors.UndefinedTable as e:
                    print("[ERR] from send data encountered error at stage 1 as ",e)
                except psycopg2.errors.InFailedSqlTransaction as e:
                    print("[ERR] from send data encountered error at stage 1 as ",e)
                row = cursor.fetchone()   
                print('-------------------------------------l1data 1.3')         
                cols_name = list(map(lambda x: x[0], cursor.description))
                if row is not None:   
                    print('-------------------------------------l1data 1.4')
                    res = dict(zip(cols_name, list(row)))
                    print('-------------------------------------l1data 1.5')
                    data =res
                    update_data = {
                                    "id": 1, 
                                    "set1": int(inputdata['set1']),
                                    "set2": int(inputdata['set2']), 
                                    "set3": int(inputdata['set3']), 
                                    "set4": int(inputdata['set4'])  ,
                                    "person_count_manual":int(inputdata['person_count_manual']),
                                    "person_count_auto": int(inputdata['person_count_auto']),
                                    "analytics_stop_time":int(inputdata['analytics_stop_time'])
                                }
                    update_data_sql = """
                        UPDATE tsk_ss_l1
                        SET set1 = %(set1)s, set2 = %(set2)s, set3 = %(set3)s, set4 = %(set4)s, person_count_manual = %(person_count_manual)s,
                        person_count_auto = %(person_count_auto)s, analytics_stop_time = %(analytics_stop_time)s
                        WHERE id = %(id)s;
                    """    
                    print('-------------------------------------l1data 1.6')                
                    print("data===",update_data)  
                    print(update_data_sql,update_data) 
                    cursor.execute(update_data_sql, update_data)
                    conn.commit()
                    print('-------------------------------------l1data 1.7')   
                else:
                    # update_data = {
                    #                 "id": 1, 
                    #                 "set1": int(inputdata['set1']),
                    #                 "set2": int(inputdata['set2']), 
                    #                 "set3": int(inputdata['set3']), 
                    #                 "set4": int(inputdata['set4'])  ,
                    #                 "person_count_manual":int(inputdata['person_count_manual']),
                    #                 "person_count_auto": int(inputdata['person_count_auto']),
                    #                 "analytics_stop_time":int(inputdata['analytics_stop_time'])
                    #             }
                    # update_data_sql = """
                    #     UPDATE tsk_ss_l1
                    #     SET set1 = %(set1)s, set2 = %(set2)s, set3 = %(set3)s, set4 = %(set4)s, person_count_manual = %(person_count_manual)s,
                    #     person_count_auto = %(person_count_auto)s, analytics_stop_time = %(analytics_stop_time)s
                    #     WHERE id = %(id)s;
                    # """    
                    # print('-------------------------------------l1data 1.6')                
                    # print("data===",update_data)  
                    # print(update_data_sql,update_data) 
                    # cursor.execute(update_data_sql, update_data)
                    # conn.commit()

                    insert_data = {
                                        "set1": int(inputdata['set1']),
                                        "set2": int(inputdata['set2']),
                                        "set3": int(inputdata['set3']),
                                        "set4": int(inputdata['set4']),
                                        "person_count_manual": int(inputdata['person_count_manual']),
                                        "person_count_auto": int(inputdata['person_count_auto']),
                                        "analytics_stop_time": int(inputdata['analytics_stop_time'])
                                    }

                    insert_data_sql = """
                        INSERT INTO tsk_ss_l1 
                        (set1, set2, set3, set4, person_count_manual, person_count_auto, analytics_stop_time)
                        VALUES (%(set1)s, %(set2)s, %(set3)s, %(set4)s, %(person_count_manual)s, %(person_count_auto)s, %(analytics_stop_time)s);
                    """

                    print('-------------------------------------l1data 1.6')                
                    print("data===", insert_data)  
                    print(insert_data_sql, insert_data) 
                    cursor.execute(insert_data_sql, insert_data)
                    conn.commit()
                    print('-------------------  ------------------l1data 1.7')   

            except psycopg2.OperationalError as e:
                print('-------------------------------------l1data 1.8')
                try:
                    print("CREATING TABLE ---tsk_ss44444444_l1tsk_ss_4l1tsk_ss_444l14444tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1--")
                    query = '''CREATE TABLE IF NOT EXISTS tsk_ss_l1(id SERIAL PRIMARY KEY,
                                set1 integer,
                                set2 integer,
                                set3 integer,
                                set4 integer,
                                person_count_manual integer,
                                person_count_auto integer,
                                analytics_stop_time integer );'''
                    print('-------------------------------------l1data 1.9')
                    cursor.execute(query) 
                    conn.commit()
                    print('-------------------------------------l1data 1.1.0')
                    # print("cursor === rowcount === ",cursor.rowcount)
                    creation_query = cursor.rowcount 
                    if creation_query == -1 :
                        print('-------------------------------------l1data 1.1.1')
                        tablecreationstatus = True
                        print("streamsuitl1data table successfully created.")
                    else:
                        print("streamsuitl1data table is not created.")
                        print('-------------------------------------l1data 1.1.2')
                        
                except Exception as  error:
                    print('-------------------------------------l1data 1.1.3')
                    print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - UPDATE", error)
                    ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- L1datatablecreation UPDATE 1", str(error), " ----time ---- ", now_time_with_time()]))  
                    
            except psycopg2.ProgrammingError as e:
                print('-------------------------------------l1data 1.1.4')
                try:
                    print("CREATING TABLE ---tsk_ss44444444_l1tsk_ss_4l1tsk_ss_444l14444tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1tsk_ss_l1--")
                    query = '''CREATE TABLE IF NOT EXISTS tsk_ss_l1(id SERIAL PRIMARY KEY,
                set1 integer,
                set2 integer,
                set3 integer,
                set4 integer,
                person_count_manual integer,
                person_count_auto integer,
                analytics_stop_time integer );'''
                    cursor.execute(query) 
                    conn.commit()
                    # print("cursor === rowcount === ",cursor.rowcount)
                    creation_query = cursor.rowcount 
                    print('-------------------------------------l1data 1.1.5')
                    if creation_query == -1 :
                        tablecreationstatus = True
                        print('-------------------------------------l1data 1.1.6')
                        print("streamsuitl1data table successfully created.")
                    else:
                        print("streamsuitl1data table is not created.")
                        print('-------------------------------------l1data 1.1.7')
                        
                except Exception as  error:
                    print('-------------------------------------l1data 1.1.8')
                    print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - UPDATE", error)
                    ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- L1datatablecreation UPDATE 1", str(error), " ----time ---- ", now_time_with_time()]))        
                    
            cursor.close()
            conn.close()
        else:
            print ("[ERR] PostgreSQL DB CONNECTION FAILED - data upload")
            
    except Exception as error :
        print("-------------------------------------error ",error)

    return 1


@steamsuit.route('/set_value_configuration', methods=['POST'])
def configuresetvalue():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = [ 'data']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            Steamsuitel1data = data['data']
            if Steamsuitel1data is not None:
                if isEmpty(Steamsuitel1data):
                    if CHECKDICTIONARY_HAVING_ANY_NONE_VALUE(Steamsuitel1data):
                        finddata =mongo.db.steamsuitl1.find_one({})
                        if finddata is None:
                            update_set_data_to_table(Steamsuitel1data)
                            result = (mongo.db.steamsuitl1.insert_one(Steamsuitel1data))
                            if result.acknowledged:
                                ret = {'message': 'l1 data added successfully.', 'success': True}
                            else:
                                ret['message'] =  'same data is already exists.'   
                        else:
                            update_set_data_to_table(Steamsuitel1data)
                            result = (mongo.db.steamsuitl1.update_one({'_id': ObjectId(finddata['_id'])}, {'$set': Steamsuitel1data}))
                            if result.modified_count > 0:
                                ret = {'message': 'l1 data added successfully.', 'success': True}
                            else:
                                ret['message'] = 'l1 data not added.'  
                    else:
                        ret['message']='please give proper input data. any value of data should not None.'
                else:
                    ret['message']='please give proper input data. it should not be empty.'    
            else:
                ret['message'] =  'give the proper input data, data should not be none type.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret


def GETL1details():
    retrurnvalue = None
    databasedetails = { 
        "sql_objecttable_name" :"tsk_ss_l1" ,
        "user": "docketrun",
        "password" :"docketrun",
        "host": "localhost",
        "port": "5432",
        "database" :"docketrundb",
        "sslmode":"disable"}
    try:
        conn = psycopg2.connect(user = databasedetails['user'],  password =databasedetails['password'],  host = databasedetails['host'], port = databasedetails['port'],   database = databasedetails['database'],  sslmode=databasedetails['sslmode'])
    except:
        conn = 0
        
    if conn:
        cursor = conn.cursor()
        print ("[INFO] DB connected successfully  send  testopc")
        data  =[]        
        try:
            cursor.execute('SELECT * FROM '+databasedetails['sql_objecttable_name']+' ORDER BY id desc')
        except psycopg2.errors.UndefinedTable as e:
            print("[ERR] from send data encountered error at stage 1 as ",e)
        except psycopg2.errors.InFailedSqlTransaction as e:
            print("[ERR] from send data encountered error at stage 1 as ",e)
        row = cursor.fetchone()            
        cols_name = list(map(lambda x: x[0], cursor.description))
        if row is not None:   
            res = dict(zip(cols_name, list(row)))
            data =res
            if data is not None:
                retrurnvalue= data    
        cursor.close()
        conn.close()
    else:
        print ("[ERR] PostgreSQL DB CONNECTION FAILED - data upload")
    return retrurnvalue

@steamsuit.route('/GetL1datadetails', methods=['GET'])
def GetL1datadetails():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}   
    L1data= GETL1details()
    if L1data is not None:
        ret={'message':L1data,"success":True}
    else:
        ret['message']='data not found.'
    return ret


@steamsuit.route('/GetLsteamsuit', methods=['GET'])
def Steamsuitviolationdatadetails():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}   
    L1data= list(mongo.db.steamsuitviolationdata.find( sort=[('_id', pymongo.DESCENDING)]))
    if len(L1data) !=0 :
        for indexnu , dataelement in enumerate(L1data):
            # print("=================================== sadkfjaksdfjkasdfkjaksdfkjaksdfkj---------------------------------------------------")
            # print("data========= ",len(dataelement['analytics_details']))
            # print("data========= ",dataelement['analytics_details'])
            # for i ,j in enumerate(dataelement['analytics_details']):
            #     print('====one data ==',j)
            #     print("image_name",j['image_name'])
            #     j['image_name'] = os.path.basename(j['image_name'])
            #     break                
            print("\n\n\n\n")
        ret={'message':L1data,"success":True}
    else:
        ret['message']='data not found.'
    return parse_json(ret)



@steamsuit.route('/GetLlateststeamsuitviolation', methods=['GET'])
def Steamsuitlatestviolationdatadetails():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}   
    L1data= mongo.db.steamsuitviolationdata.find_one( sort=[('_id', pymongo.DESCENDING)])
    if L1data is not None :
        # print("=================================== sadkfjaksdfjkasdfkjaksdfkjaksdfkj---------------------------------------------------")
        # print("===sss===data========= ",L1data) 
        # print("====== ss len ===", len(L1data['analytics_details']) )
        livecountdata = mongo.db.steamsuitlivecount.find_one( sort=[('_id', pymongo.DESCENDING)])
        returndata= {'ticket_no':L1data['ticket_no'],'previous_count':0,"now_count":len(L1data['analytics_details']),'analytics_details':L1data}
        if livecountdata is not None :
            # print(livecountdata)
            returndata= {'ticket_no':L1data['ticket_no'],'previous_count':livecountdata['now_count'],"now_count":len(L1data['analytics_details']),'analytics_details':L1data}
            mongo.db.steamsuitlivecount.update_one({ '_id':ObjectId(livecountdata['_id'])}, {'$set': returndata}) 
        
        else:
            returndata=  {'ticket_no':L1data['ticket_no'],'previous_count':0,"now_count":len(L1data['analytics_details']),'analytics_details':L1data}
            mongo.db.steamsuitlivecount.insert_one(returndata)    
        # print("\n\n\n\n")
        ret={'message':returndata,"success":True}
    else:
        ret['message']='data not found.'

    # print("====== ss ret =====", ret )
    return parse_json(ret)


def image_roi_draw_data(image_data,imagename):
    onlyobject_data = []
    if image_data is not None:
        for i, j in enumerate(image_data['analytics_details']):
            if j['image_name']==imagename:
                print(j['obj_details'])
                object_data = j['obj_details']
                if len(object_data) != 0:
                    final_object_data = []
                    if len(object_data) == 1:
                        if object_data[0]['class_name'] == 'person':
                            object_data[0]['violation_count']  = 'person ' + str(1)
                            final_object_data.append(object_data[0])
                    elif len(object_data) > 1:
                        person_count = 0
                        for ___, jjj in enumerate(object_data):
                            person_count = ___
                            if jjj['class_name'] == 'person':
                                jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                final_object_data.append(jjj)
                onlyobject_data = final_object_data
    return onlyobject_data




@steamsuit.route('/STEAMVIOLATIONIMAGE/<image_file>', methods=['GET'])
def steamsuitimage(image_file):
    try:
        image_data = mongo.db.steamsuitviolationdata.find_one({'analytics_details.image_name': {'$in': [image_file]}})
        if image_data is not None:
            onlyobject_data = image_data.get('analytics_details', [])
            if onlyobject_data:
                base_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame')
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path)
                draw = ImageDraw.Draw(source_img)
                IMage_widthscal = source_img.width
                IMage_heigthscal = source_img.height                
                for thiru in onlyobject_data:
                    
                    if thiru['image_name']==image_file:
                        obj_details = thiru.get('obj_details', [])
                        for obj_detail in obj_details:
                            bbox = obj_detail.get('bbox', {})
                            x_value = int(bbox.get('X', 0))
                            y_value = int(bbox.get('Y', 0))
                            width = int(bbox.get('W', 0))
                            height = int(bbox.get('H', 0))
                            shape = [(x_value, y_value), (x_value + width, y_value + height)]
                            #bbox_values = scale_polygon(shape, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                            draw.rectangle(shape, outline='red', width=3)
                
                imgByteArr = io.BytesIO()
                source_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
            else:
                path, filename = (os.path.join(os.getcwd(), "smaple_files"), 'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)
        else:
            return {'message': 'Given image is not found', 'success': False}
    except Exception as error:
        print("Error:", error)
        return {'message': str(error), 'success': False}




# @steamsuit.route('/steamsuitimage/<image_file>', methods=['GET'])
# def steamsuitimage(image_file):
#     print("Imagesteamsuitdata---image_file-",image_file)
#     if 1:
#     # try:
#         image_data = mongo.db.steamsuitviolationdata.find_one({'analytics_details.image_name':{'$in': [ image_file]}})
#         # print("Imagesteamsuitdata----",image_data)
#         if image_data is not None:
#             onlyobject_data = image_roi_draw_data(image_data,image_file)
#             print("imagereturn=== ",onlyobject_data)
#             base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
            
#             file_path = os.path.join(base_path, image_file)
#             source_img = Image.open(file_path)
#             draw = ImageDraw.Draw(source_img)
#             IMage_widthscal = source_img.width
#             IMage_heigthscal = source_img.height
            
#             if len(onlyobject_data) != 0:
#                 if 1:
#                 # try : 
#                     for ___, thiru in enumerate(onlyobject_data):
#                         Vestheight , Vestwidth,Vestx_value,Vesty_value=0,0,0,0
#                         Helmetheight , Helmetwidth,Helmetx_value,Helmety_value=0,0,0,0
#                         # if thiru['Vest']=='no_ppe':
#                         #     Vestheight = thiru['vest_bbox']['H']
#                         #     Vestwidth = thiru['vest_bbox']['W']
#                         #     Vestx_value = thiru['vest_bbox']['X']
#                         #     Vesty_value = thiru['vest_bbox']['Y']
#                         #     # Vestshape = [(Vestx_value, Vesty_value), (Vestwidth - 10, Vestheight - 10)]#(X + W, Y + H)       
#                         #     Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]#(X + W, Y + H)                              
#                         #     # draw.rectangle(Vestshape, outline='orange', width=5)
#                         #     #darkgray
#                         #     draw.rectangle(Vestshape, outline='yellow', width=3)
#                         # if thiru['Helmet']== False:
#                         #     Helmetheight = thiru['helmet_bbox']['H']
#                         #     Helmetwidth = thiru['helmet_bbox']['W']
#                         #     Helmetx_value = thiru['helmet_bbox']['X']
#                         #     Helmety_value = thiru['helmet_bbox']['Y']
#                         #     # Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth - 10, Helmetheight - 10)]#(X + W, Y + H)
#                         #     Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth , Helmetheight )]#(X + W, Y + H)
#                         #     draw.rectangle(Helmetshape, outline='red', width=3)
#                         height = int(thiru['bbox']['H'])
#                         width = int(thiru['bbox']['W'])
#                         x_value = int(thiru['bbox']['X'])
#                         y_value = int(thiru['bbox']['Y'])
#                         w, h = width, height
#                         shape = [(x_value, y_value), (w , h )]
#                         bbox_values = scale_polygon(shape, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
#                         # shape = [(x_value, y_value), (w - 10, h - 10)]#(X + W, Y + H)
#                         #(X + W, Y + H)
#                         print('---------------------------shape--------------',shape)
#                         if Helmetheight==0 and Helmetwidth==0  and Helmetx_value==0 and Helmety_value==0 and Vestheight ==0 and Vestwidth ==0 and Vestx_value ==0 and Vesty_value ==0:
#                             draw.rectangle(bbox_values, outline='red', width=3)
#                         # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        28, encoding='unic'))
#                     imgByteArr = io.BytesIO()
#                     source_img.save(imgByteArr, format='JPEG')
#                     imgByteArr.seek(0)
#                     return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
#                 # except Exception as error :
#                 #     imgByteArr = io.BytesIO()
#                 #     source_img.save(imgByteArr, format='JPEG')
#                 #     imgByteArr.seek(0)
#                 #     return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
#             else:
#                 path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
#                 main_path = os.path.abspath(path)
#                 return send_from_directory(main_path, filename)
#             # if len(onlyobject_data) == 1:
#             #     height = onlyobject_data[0]['bbox']['H']
#             #     width = onlyobject_data[0]['bbox']['W']
#             #     x_value = onlyobject_data[0]['bbox']['X']
#             #     y_value = onlyobject_data[0]['bbox']['Y']
#             #     file_path = os.path.join(base_path, image_file)
#             #     w, h = width, height
#             #     shape = [(x_value, y_value), (w , h )]#[(x_value, y_value), (w - 10, h - 10)]
#             #     source_img = Image.open(file_path)
#             #     draw = ImageDraw.Draw(source_img)
#             #     draw.rectangle(shape, outline='red', width=3)
#             #     draw.text((x_value + 6, y_value + 2), str(onlyobject_data[0]['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 28,encoding='unic'))
#             #     imgByteArr = io.BytesIO()
#             #     source_img.save(imgByteArr, format='JPEG')
#             #     imgByteArr.seek(0)
#             #     return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
#             # elif len(onlyobject_data) > 1:
#             #     file_path = os.path.join(base_path, image_file)
#             #     source_img = Image.open(file_path)
#             #     for ___, thiru in enumerate(onlyobject_data):
#             #         print('=============bbox======',thiru)
#             #         height = thiru['bbox']['H']
#             #         width = thiru['bbox']['W']
#             #         x_value = thiru['bbox']['X']
#             #         y_value = thiru['bbox']['Y']
#             #         w, h = width, height
#             #         shape = [(x_value, y_value), (w , h )]#[(x_value, y_value), (w - 10, h - 10)]
#             #         draw = ImageDraw.Draw(source_img)
#             #         draw.rectangle(shape, outline='red', width=3)
#             #         draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        28, encoding='unic'))
#             #     imgByteArr = io.BytesIO()
#             #     source_img.save(imgByteArr, format='JPEG')
#             #     imgByteArr.seek(0)
#             #     return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
#         else:
#             return {'message': 'given image is not found', 'success': False}
#     # except ( 
#     #          pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#     #          pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#     #          pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#     #          pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#     #          pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#     #          pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#     #          pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#     #          pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#     #          pymongo.errors.WriteError) as error:
#     #     print("print(,)", str(error))
#     #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 1", str(error), " ----time ---- ", now_time_with_time()]))
#     #     ret['message'] =" ".join(["something error has occered in api", str(error)])     
#     #     if restart_mongodb_r_service():
#     #         print("mongodb restarted")
#     #     else:
#     #         if forcerestart_mongodb_r_service():
#     #             print("mongodb service force restarted-")
#     #         else:
#     #             print("mongodb service is not yet started.") 
#     #     return {'message': str(error), 'success': False}
#     # except Exception as  error :
#     #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 2", str(error), " ----time ---- ", now_time_with_time()]))     
#     #     return {'message': str(error), 'success': False}



    # ret = {'success': False, 'message': 'something went wrong with add roi api'}
    # data = request.json
    # if data == None:
    #     data = {}
    # request_key_array = [ 'data']
    # jsonobjectarray = list(set(data))
    # missing_key = set(request_key_array).difference(jsonobjectarray)
    # if not missing_key:
    #     output = [k for k, v in data.items() if v == '']
    #     if output:
    #         ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
    #     else:
    #         Steamsuitel1data = data['data']


#######################original image####################
# @steamsuit.route('/STEAMVIOLATIONIMAGE/<image_file>', methods=['GET'])
# def STEAMVIOLATIONIMAGE(image_file):    
#     try:
#         base_path = os.path.join(get_current_dir_and_goto_parent_dir() , 'images','frame')
#         response = send_from_directory(base_path, image_file)
#         return response
#     except Exception as  error:
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
#         return str(error)



#done for the object
@steamsuit.route('/delete_main/<key_id>', methods=['GET'])
def deletemain(key_id=None):
    ret = {'message': 'something error occured in delte_riro_data.','success': False}
    try:
        if key_id is not None:
            find_delete_data = mongo.db.steamsuit_cameras.find_one({'_id': ObjectId(key_id)})
            if find_delete_data is not None:
                result = mongo.db.steamsuit_cameras.delete_one({'_id': ObjectId(key_id)})
                if result.deleted_count > 0:
                    ret = {'message': 'camera deleted successfully.','success': True}
                else:
                    ret['message'] = ('camera is not deleted ,due to something went wrong with database.')
            else:
                ret['message' ] = '  camera is not found for this id, please try once again.'
        else:
            ret['message' ] = '   id is None type please give proper  key id.'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_riro_data 1", str(error), " ----time ---- ", now_time_with_time()])) 
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ret['message']=" ".join(["something error has occered in api", str(error)])
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_riro_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return ret





"""Write Config File Code"""
def STEAMSUITWRITECONFIG(response):
    print("----------------------------response-----------------",response)
    sample_config_file = os.path.join(os.getcwd(),  'smaple_files', 'steamsuit.txt')
    sample_config_esi_engine = os.path.join(os.getcwd(), 'smaple_files', 'esi_engine_file_create.txt')
    create_engine_file_config_file = os.path.join(get_current_dir_and_goto_parent_dir(), 'models/config_infer_primary_tsk_v_0_2.txt')
    deepstream_config_path =  os.path.join(get_current_dir_and_goto_parent_dir(),'docketrun_app_ss/configs')
    handle_uploaded_file(deepstream_config_path)
    config_file = os.path.join(deepstream_config_path, 'config.txt')
    config_analytics_file = os.path.join(deepstream_config_path,'config_analytics.txt')
    lines = ['[property]', 'enable=1', 'config-width=960','config-height=544', 'osd-mode=2', 'display-font-size=12', '']
    test_data = []
    index = 0
    require_data = []
    roi_enable_cam_ids = []
    ppe_enable_cam_ids = []
    
    with open(config_analytics_file, 'w') as f:
        for item in lines:
            f.write('%s\n' % item)
    lines = []
    with open(sample_config_file) as file:
        for young_TIGER, line in enumerate(file):
            if line.strip() == '[application]':
                lines.append('[application]')
                lines.append('enable-perf-measurement=1')
                lines.append('perf-measurement-interval-sec=5')
            elif line.strip() == '[tiled-display]':
                columns = int(math.sqrt(len(response)))
                rows = int(math.ceil(len(response) / columns))
                if columns == 1:
                    columns =2
                lines.append('[tiled-display]')
                lines.append('enable=1')
                lines.append('rows={0}'.format(str(rows)))
                lines.append('columns={0}'.format(str(columns)))
                lines.append('width=960')
                lines.append('height=544')
                lines.append('gpu-id=0')
                lines.append('nvbuf-memory-type=0\n')
            elif line.strip() == '[sources]':
                print("data")
                for n, x in enumerate(response):
                    cam_id = '{0}'.format(int(n) + 1)                            
                    if x['rtsp_url'] is not None:
                        uri = x['rtsp_url']
                        lines.append('[source{0}]'.format(n))
                        lines.append('enable=1')
                        lines.append('type=4')
                        lines.append('uri = {0}'.format(uri))
                        lines.append('num-sources=1')
                        lines.append('gpu-id=0')
                        lines.append('nvbuf-memory-type=0')
                        lines.append('latency=500')
                        lines.append('camera-id={0}'.format(int(n) + 1))
                        lines.append('camera-name = {0}'.format(x['camera_name']))
                        lines.append('drop-frame-interval = 1\n')                    
            elif line.strip() == '[sink0]':
                lines.append('[sink0]')
                lines.append('enable=1')
                lines.append('type=2')
                lines.append('sync=0')
                lines.append('source-id=0')
                lines.append('gpu-id=0')
                lines.append('nvbuf-memory-type=0\n')
            elif line.strip() == '[osd]':
                lines.append('[osd]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('border-width=2')
                lines.append('text-size=15')
                lines.append('text-color=1;1;1;1;')
                lines.append('text-bg-color=0.3;0.3;0.3;1;')
                lines.append('font=Arial')
                lines.append('show-clock=0')
                lines.append('clock-x-offset=800')
                lines.append('clock-y-offset=820')
                lines.append('clock-text-size=12')
                lines.append('clock-color=1;0;0;0')
                lines.append('nvbuf-memory-type=0\n')
            elif line.strip() == '[streammux]':
                lines.append('[streammux]')
                lines.append('gpu-id=0')
                lines.append('live-source=1')
                lines.append('batch-size={0}'.format(len(response)))
                lines.append('batched-push-timeout=40000')
                lines.append('width=1920')
                lines.append('height=1080')
                lines.append('enable-padding=0')
                lines.append('nvbuf-memory-type=0\n')
            elif line.strip() == '[primary-gie]':
                lines.append('[primary-gie]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('batch-size={0}'.format(len(response)))
                lines.append('bbox-border-color0=0;1;0;0.7')
                lines.append('bbox-border-color1=0;1;1;0.7')
                lines.append('bbox-border-color2=0;1;0;0.7')
                lines.append('bbox-border-color3=0;1;0;0.7')
                lines.append('nvbuf-memory-type=0')
                lines.append('interval=0')
                lines.append('gie-unique-id=1')
                lines.append('config-file = ../../models/config_infer_primary_tsk_ss.txt\n')
            elif line.strip() == '[secondary-gie0]':
                lines.append('[secondary-gie0]')
                lines.append('enable = 1')
                lines.append('gpu-id={0}'.format(str(0)))
                lines.append('gie-unique-id = 6')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('bbox-border-color0 = 0;0;0;0.7')
                lines.append('bbox-border-color1 = 1;0;0;0.7')
                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt\n')
            elif line.strip() == '[secondary-gie1]':
                lines.append('[secondary-gie1]')
                lines.append('enable = 1')
                lines.append('gpu-id={0}'.format(str(0)))
                lines.append('gie-unique-id = 7')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('bbox-border-color0 = 0;0;0;0.7')
                lines.append('bbox-border-color1 = 1;0;0;0.7')
                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt\n')
            elif line.strip() == '[tracker]':
                lines.append('[tracker]')
                lines.append("enable=1")
                lines.append("tracker-width=960")
                lines.append("tracker-height=544")
                lines.append("ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so")
                lines.append("ll-config-file=../../models/config_tracker_NvDCF_perf.yml")
                lines.append("gpu-id=0")
                lines.append("display-tracking-id=1\n")
            elif line.strip() == '[nvds-analytics]':
                lines.append('[nvds-analytics]')
                lines.append('enable = 0')
                lines.append('config-file = ./config_analytics.txt\n')
            elif line.strip() == '[tests]':
                lines.append('[tests]')
                lines.append('file-loop=1\n')
            elif line.strip() == '[docketrun-analytics]':
                lines.append('[docketrun-analytics]\n') 

            elif line.strip() == '[application-config]':
                lines.append('[application-config]')
                lines.append('app-title = SafetyEye')
                lines.append('image-save-path = images/frame\n')

            elif line.strip()=='[restricted-access]'    :
                lines.append('[restricted-access]')  
                lines.append('enable = 0')  
                lines.append('config-file = restricted_access_1.txt')
                lines.append('roi-overlay-enable = 1\n')

            
            elif line.strip()=='[ppe-type-1]':
                lines.append('[ppe-type-1]')  
                lines.append('camera-ids = 1;')  
                lines.append('data-save-interval = 1\n')

            elif line.strip()=='[steam-suit]'    :
                lines.append('[steam-suit]')  
                lines.append('camera-ids = 1;') 
                lines.append('data-save-interval = 1')
                if  response[0]['hooter_ip'] is not None :
                    if response[0]['hooter_ip'] !='':
                        hooteripstring = 'hooter-relay-details =[{'+'"cameraid":1,"ip":'
                        hooteripstring= hooteripstring + '{0}'.format(response[0]['hooter_ip'])
                        hooteripstring = hooteripstring + ',"type":1,"shutdown_time":60,"buffer_stop_time":2}]'
                        # hooteripstring = 'hooter-relay-details =[{'+'"cameraid":1,"ip":'+'{0},"type":1,"shutdown_time":60,"buffer_stop_time":2}]\n'.format(response[0]['hooter_ip'])
                        print('----------hooteripstring--------',hooteripstring)
                        # lines.append('hooter-relay-details =[{"cameraid":1,"ip":{0}},"type":1,"shutdown_time":60,"buffer_stop_time":2}]\n'.format(response[0]['hooter_ip']))
                        lines.append(hooteripstring)
                    else:
                        lines.append('hooter-relay-details =null\n')
                else:
                    lines.append('hooter-relay-details =null\n')
            elif line.strip('[crowd-counting]'):
                if '[crowd-counting]' not in lines:
                    lines.append('[crowd-counting]')
                    lines.append('enable = 0')
                    lines.append('config-file = crowd.txt')
                    lines.append('roi-overlay-enable=1\n')
                
            else:
                lines.append(line.strip())
    with open(config_file, 'w') as f:
        for O_O_O, item in enumerate(lines):
            f.write('%s\n' % item)
    return roi_enable_cam_ids, ppe_enable_cam_ids, require_data




def createSTEAMSUITconfig():
    response = []
    main_list = []
    fetch_panel_data = mongo.db.steamsuit_cameras.find_one({})
    if fetch_panel_data is not None:
        if (fetch_panel_data['main_camera']) is not None :
            ip_address =fetch_panel_data['main_camera']['camera_ip']
            cam_name = fetch_panel_data['main_camera']['cameraname']
            rtsp = fetch_panel_data['main_camera']['rtsp_url']
            if rtsp is not None:
                if 'alarm_details' in fetch_panel_data:
                    if isEmpty(fetch_panel_data):
                        print("==================fetch_panel_data===========",fetch_panel_data['alarm_details'])
                        if 'alarm_ip_address' in fetch_panel_data['alarm_details']:
                            if  (fetch_panel_data['alarm_details']['alarm_ip_address']):
                                if 'hooter_ip' in fetch_panel_data['alarm_details']['alarm_ip_address']:
                                    if fetch_panel_data['alarm_details']['alarm_ip_address']['hooter_ip']:
                                        require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':fetch_panel_data['alarm_details']['alarm_ip_address']['hooter_ip']}
                                    else:
                                        require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':''}
                                else:
                                    require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':''}
                            else:
                                require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':''}
                        else:
                            require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':''}
                    else:
                        require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':''}
                else:
                    require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'hooter_ip':''}
                main_list.append(require_panel_data)    
    if len(main_list) != 0:
        response = {'data': main_list}    
    return response

def STEAMSUITCAMERAIDupdate():
    ret = {'message':'something went wrong with create config .','success': False}
    getdata_response = createSTEAMSUITconfig()
    if len(getdata_response) != 0:
        response = getdata_response['data']
        function__response = STEAMSUITWRITECONFIG(response)
        require_cam_ids_data = {'data': list(function__response)}
        if '200':
            ret = {'message': 'config files are created successfully.','success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'there is no data found for create config file '
    return ret



@steamsuit.route('/startsteamsuit', methods=['GET'])
def ESICREATECONFIG():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        esi_app_set_STEAMSUIT_monitoring_started(True)
        return_data = STEAMSUITCAMERAIDupdate()
        # HYDRACREATECONFIG()
        if return_data:
            # stop_application_for_esi_creating_config()
            if return_data['success'] == True:
                esi_app_set_STEAMSUIT_monitoring_started(False)
                ret = {'message':'steamsuit file are created successfully.', 'success': True}
            else:
                ret['message' ] = 'something went wrong  creating config files.'
        else:
            ret['message'] = 'data not found to create config files.'
    else:
        ret = ret
    return ret


@steamsuit.route('/stopsteamsuitapp', methods=['GET'])
def stop_steamsuit():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        esi_app_set_STEAMSUIT_monitoring_started(True)
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret




