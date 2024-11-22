from Data_recieving_and_Dashboard.packages import *
camera_details = Blueprint('camera_details', __name__)


def verify_rtsp(url, image_namereplace):
    directory_path = os.getcwd() + '/' + 'rtsp_roi_image'
    handle_uploaded_file(directory_path)
    present_time = replace_spl_char(str(datetime.datetime.now()))
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
    # print(CamCount)
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        ERRORLOGdata("\n [ERROR] camera_api  --  check_license_of_camera  1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata("\n [ERROR] camera_api  --check_license_of_camera 2 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata("\n [ERROR] camera_api  --check_license_of_camera 3 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        # print('res ===', res)
        # print('\n\n')
        # print('device_location', res['device_location'])
        lic = res['device_location']
        split_data=lic.split('_')[1].split("l")
        # print(lic.split('_')[1].split("l"))
        while '' in split_data:
            split_data.remove('')
        # print(split_data[0])
        # print(type(CamCount))
        # print(type(split_data[0]))
        if CamCount < int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status




@camera_details.route('/check_license', methods=['GET'])
def checkingCamlicense():
    # if 1:
    try:
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
                        for i in eachElements['data']:
                            # print(i)
                            if i['ip_address'] not in unique_iplist:
                                unique_iplist.append(i['ip_address'])
                sheet_camera_count= len(unique_iplist) 
            
        CamCount = mongo.db.ppera_cameras.count_documents({})#find()#find_one()#mongo.db.ppera_cameras.find({}).count()
        # print("camera -count ",CamCount)#.count('true'))
        # print("sheet_data count",sheet_camera_count)
        CamCount = CamCount + sheet_camera_count
        if check_license_of_camera(CamCount):
            ret['message']='you have license to add the camera'
            ret['success']=True
        else:
            ret['message']="you don't have license to add the camera"
    except Exception as error:
        ret['message'] = str(error)
        ERRORLOGdata("\n [ERROR] camera_api  --check_license_of_camera 4 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret



@camera_details.route('/get_camera_brand_details', methods=['GET'])
def get_camera_brand_details_all():
    try:
        ret = {'message': 'something went wrong with get brand details api', 'success': False}
        data = ['cp_plus', 'dahua', 'pelco', 'bosch', 'hikvision','samsung', 'uniview', 'univision', 'secur_eye',
                 'axis', 'honeywell','geovision','hixecure' ,'docketrun']
        if len(data) != 0:
            ret = {'success': True, 'message': data}
        else:
            ret['message'] = 'data not found'
    except Exception as error:
        ret['message'] = str(error)
        ERRORLOGdata("\n [ERROR] camera_api  --get_camera_brand_details 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret


@camera_details.route('/get_sample_rtsp', methods=['GET'])
def get_smaple_rtsp_all_brands():
    try:
        ret = {'message': 'something went wrong with get brand details api','success': False}
        data = ['cp_plus', 'dahua', 'pelco', 'bosch', 'hikvision','samsung', 'uniview', 'univision', 'secur_eye', 'axis', 'honeywell','geovision']
        dash_data = []
        cameraip = '192.168.1.1'
        channelNo = '1'
        username = 'admin'
        password = 'admin123'
        port = '544'
        for I___, i in enumerate(data):
            rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo,username, password, i, port)
            sample_data = {'rtsp': rtsp_url, 'username': username, 'password': password, 'ipaddress': cameraip, 'channelno': channelNo, 'port': port, 'brand': i}
            dash_data.append(sample_data)
        if len(dash_data) != 0:
            ret = {'success': True, 'message': dash_data}
        else:
            ret['message'] = 'data not found'
    except Exception as error:
        ret['message'] = str(error)
        ERRORLOGdata("\n [ERROR] camera_api  --get_sample_rtsp 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret


@camera_details.route('/add_camera', methods=['POST'])
def add_Acamera():
    ret = {'success': False, 'message':'something went wrong with add camera api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['cameraip', 'camera_brand', 'username', 'password','plant', 'area', 'cameraname', 'alarm_ip_address', 'alarm_type']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            if len(output)==2 and ('alarm_ip_address' in output  and "alarm_type" in output):
                cameraip = data['cameraip']
                brand = data['camera_brand']
                username = data['username']
                password = data['password']
                port = data['port']
                plant = data['plant']
                area = data['area']
                cameraname = data['cameraname']
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                find_data = mongo.db.ppera_cameras.find_one({'camera_ip': cameraip})
                if find_data is None:
                    if regex_pwd.search(password) == None:
                        ping_response = final_ping(cameraip)
                        if ping_response:
                            channelNo = '1'
                            rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                            if rtsp_response:
                                image_namereplace = (replace_spl_char_panel_area_plant(plant  + '-' + area))
                                rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                if rtsp_response_image:
                                    final_data = {'camera_ip': cameraip,'username': username, 'password': password,
                                    'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                    'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                    'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type,
                                    'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                    'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': [],'analytics_status':'false'}
                                    result = mongo.db.ppera_cameras.insert_one(final_data)
                                    if result.acknowledged:
                                        ret = {'success': True, 'message': 'camera added successfully.'}
                                    else:
                                        ret['message'] = ( 'data is not inserted properly, please try once again.'  )
                                else:
                                    ret['message'] = ( 'rtsp stream is not working, please try once again.' )
                            else:
                                ret['message'] = (  'rtsp url is not able create or format it, please enter camera brand ' + str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) + '.')
                        else:
                            ret['message'] = 'cameraip is not able ping.'
                    else:
                        ret['message'] = ('camera password should not have any special characters.')
                else:
                    ret['message'] = ('entered ip is already exist, please go with edit roi option.' )
            elif len(output)==1 and ('alarm_ip_address' in output  or "alarm_type" in output):
                cameraip = data['cameraip']
                brand = data['camera_brand']
                username = data['username']
                password = data['password']
                port = data['port']
                plant = data['plant']
                area = data['area']
                cameraname = data['cameraname']
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                find_data = mongo.db.ppera_cameras.find_one({'camera_ip': cameraip})
                if find_data is None:
                    if regex_pwd.search(password) == None:
                        ping_response = final_ping(cameraip)
                        if ping_response:
                            channelNo = '1'
                            rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                            if rtsp_response:
                                image_namereplace = (replace_spl_char_panel_area_plant(plant  + '-' + area))
                                rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                if rtsp_response_image:
                                    final_data = {'camera_ip': cameraip,'username': username, 'password': password,
                                    'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                    'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                    'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type,
                                    'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                    'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': [],'analytics_status':'false'}
                                    result = mongo.db.ppera_cameras.insert_one(final_data)
                                    if result.acknowledged:
                                        ret = {'success': True, 'message': 'camera added successfully.'}
                                    else:
                                        ret['message'] = ( 'data is not inserted properly, please try once again.'  )
                                else:
                                    ret['message'] = ( 'rtsp stream is not working, please try once again.' )
                            else:
                                ret['message'] = (  'rtsp url is not able create or format it, please enter camera brand ' + str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) + '.')
                        else:
                            ret['message'] = 'cameraip is not able ping.'
                    else:
                        ret['message'] = ('camera password should not have any special characters.')
                else:
                    ret['message'] = ('entered ip is already exist, please go with edit roi option.' )

            else:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            cameraip = data['cameraip']
            brand = data['camera_brand']
            username = data['username']
            password = data['password']
            port = data['port']
            plant = data['plant']
            area = data['area']
            cameraname = data['cameraname']
            alarm_type = data['alarm_type']
            alarm_ip_address = data['alarm_ip_address']
            regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
            find_data = mongo.db.ppera_cameras.find_one({'camera_ip': cameraip})
            if find_data is None:
                if regex_pwd.search(password) == None:
                    ping_response = final_ping(cameraip)
                    if ping_response:
                        channelNo = '1'
                        rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                        if rtsp_response:
                            image_namereplace = (replace_spl_char_panel_area_plant(plant  + '-' + area))
                            rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                            if rtsp_response_image:
                                final_data = {'camera_ip': cameraip,'username': username, 'password': password, 'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                 'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                 'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type,
                                 'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                 'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': [],'analytics_status':'false'}
                                result = mongo.db.ppera_cameras.insert_one(final_data)
                                if result.acknowledged:
                                    ret = {'success': True, 'message':'camera added successfully.'}
                                else:
                                    ret['message'] = ('data is not inserted properly, please try once again.')
                            else:
                                ret['message'] = ('rtsp stream is not working, please try once again.')
                        else:
                            ret['message'] = ('rtsp url is not able create or format it, please enter camera brand '+ str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) + '.')
                    else:
                        ret['message'] = 'cameraip is not able ping.'
                else:
                    ret['message'] = ( 'camera password should not have any special characters.')
            else:
                ret['message'] = ('entered ip is already exist, please go with edit roi option.')
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret



@camera_details.route('/add_camera_rtsp', methods=['POST'])
def add_Acamera_rtsp():
    ret = {'success': False, 'message': 'something went wrong with add camera api with rtsp'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['camera_brand', 'plant', 'area', 'cameraname', 'rtsp_url', 'alarm_type', 'alarm_ip_address']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            if len(output)==2 and ('alarm_ip_address' in output  and "alarm_type" in output) :
                rtsp_url = data['rtsp_url']
                brand = data['camera_brand']
                plant = data['plant']
                area = data['area']
                cameraname = data['cameraname']
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                find_data = mongo.db.ppera_cameras.find_one({'rtsp_url': rtsp_url})
                if find_data is None:
                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                    if rtsp_return_data:
                        password = rtsp_return_data['password']
                        cameraip = rtsp_return_data['ipaddress']
                        username = rtsp_return_data['username']
                        port = rtsp_return_data['port']
                        try:
                            if regex_pwd.search(password) == None:
                                ping_response = True
                                if ping_response:
                                    image_namereplace = (replace_spl_char_panel_area_plant(plant   +    '-' + area))
                                    rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                    if rtsp_response_image:
                                        final_data = {'camera_ip': cameraip,'username': username, 'password':     password, 'camera_brand': brand,'rtsp_port': port, 'cameraname':cameraname, 'plant': plant, 'area': area, 'imagename':rtsp_response_image['image_name'],'image_height': rtsp_response_image ['height'], 'image_width':rtsp_response_image['width'],'cameraid': None, 'alarm_type': alarm_type, 
                                            'alarm_ip_address':alarm_ip_address, 'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [], 'camera_status': True, 'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': [],'analytics_status':'false'}
                                        result = mongo.db.ppera_cameras.insert_one( final_data)
                                        if result.acknowledged:
                                            ret = {'success': True, 'message':'camera added successfully.'}
                                        else:
                                            ret['message'] = ( 'data is not inserted properly, please try once again.' )
                                    else:
                                        ret['message'] = ( 'rtsp stream is not working, please try once again.'  )
                                else:
                                    ret['message'] = 'cameraip is not able ping.'
                            else:
                                ret['message'] = ('camera password should not have any special characters.' )
                        except Exception as error:
                            print('ERROR -message in checking camera rtsp', str  (error))
                            ERRORLOGdata("\n [ERROR] camera_api  --add_camera_rtsp 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
                            image_namereplace = replace_spl_char_panel_area_plant(plant + '-' + area)
                            rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                            if rtsp_response_image:
                                final_data = {'camera_ip': cameraip, 'username': username, 'password': password,'camera_brand': brand, 'rtsp_port': port,'cameraname': cameraname,
                                              'plant': plant,'area': area, 'imagename': rtsp_response_image['image_name'],
                                              'image_height': rtsp_response_image[ 'height'], 'image_width':rtsp_response_image['width'], 
                                              'cameraid':None, 'alarm_type': alarm_type, 'alarm_ip_address': alarm_ip_address, 'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True, 
                                              'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': [],'analytics_status':'false'}
                                result = mongo.db.ppera_cameras.insert_one(final_data)
                                if result.acknowledged:
                                    ret = {'success': True, 'message': 'camera added successfully.'}
                                else:
                                    ret['message'] = ('data is not inserted properly, please try once again.' )
                            else:
                                ret['message'] = ( 'rtsp stream is not working, please try once again.')
                    else:
                        ret['message'] = 'rtsp url error.'
                else:
                    ret['message'] = ('entered ip is already exist, please go with edit roi option.' )      
            elif len(output)==1 and ('alarm_ip_address' in output  or "alarm_type" in output) :
                rtsp_url = data['rtsp_url']
                brand = data['camera_brand']
                plant = data['plant']
                area = data['area']
                cameraname = data['cameraname']
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                find_data = mongo.db.ppera_cameras.find_one({'rtsp_url': rtsp_url})
                if find_data is None:
                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                    if rtsp_return_data:
                        password = rtsp_return_data['password']
                        cameraip = rtsp_return_data['ipaddress']
                        username = rtsp_return_data['username']
                        port = rtsp_return_data['port']
                        try:
                            if regex_pwd.search(password) == None:
                                ping_response = True
                                if ping_response:
                                    image_namereplace = ( replace_spl_char_panel_area_plant(plant + '-' + area))
                                    rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                    if rtsp_response_image:
                                        final_data = {'camera_ip': cameraip,'username': username, 'password': password, 'camera_brand': brand,'rtsp_port': port, 'cameraname':     cameraname, 'plant': plant, 'area': area,
                                                    'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'], 
                                                    'image_width': rtsp_response_image['width'],'cameraid': None, 'alarm_type': alarm_type, 'alarm_ip_address': alarm_ip_address,
                                                    'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [], 'camera_status': True, 'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': [],'analytics_status':'false'}
                                        result = mongo.db.ppera_cameras.insert_one( final_data)
                                        if result.acknowledged:
                                            ret = {'success': True, 'message': 'camera added successfully.'}
                                        else:
                                            ret['message'] = ( 'data is not inserted properly, please try once again.' )
                                    else:
                                        ret['message'] = ( 'rtsp stream is not working, please try once again.'  )
                                else:
                                    ret['message'] = 'cameraip is not able ping.'
                            else:
                                ret['message'] = ('camera password should not have any special characters.')
                        except Exception as error:
                            print('ERROR -message in checking camera rtsp', str (error))
                            ERRORLOGdata("\n [ERROR] camera_api  --add_camera_rtsp 2 " + str(error)  +'  ----time ----   '+ now_time_with_time())
                            image_namereplace = replace_spl_char_panel_area_plant( plant + '-' + area)
                            rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                            if rtsp_response_image:
                                final_data = {'camera_ip': cameraip, 'username': username, 'password': password,'camera_brand': brand,'rtsp_port': port,'cameraname': cameraname, 'plant': plant,'area': area, 
                                              'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'],'image_width':rtsp_response_image['width'], 'cameraid': None, 'alarm_type': alarm_type,
                                              'alarm_ip_address': alarm_ip_address, 'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True,
                                              'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': [],'analytics_status':'false'}
                                result = mongo.db.ppera_cameras.insert_one(final_data)
                                if result.acknowledged:
                                    ret = {'success': True, 'message': 'camera added successfully.'}
                                else:
                                    ret['message'] = ('data is not inserted properly, please try once again.' )
                            else:
                                ret['message'] = ( 'rtsp stream is not working, please try once again.')
                    else:
                        ret['message'] = 'rtsp url error.'
                else:
                    ret['message'] = ('entered ip is already exist, please go with edit roi option.' )          
            else:
                ret['message'] = 'You have missed these parameters ' + str(output ) + ' to enter. please enter properly.'
        else:
            rtsp_url = data['rtsp_url']
            brand = data['camera_brand']
            plant = data['plant']
            area = data['area']
            cameraname = data['cameraname']
            alarm_type = data['alarm_type']
            alarm_ip_address = data['alarm_ip_address']
            regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
            find_data = mongo.db.ppera_cameras.find_one({'rtsp_url': rtsp_url})
            if find_data is None:
                rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                if rtsp_return_data:
                    password = rtsp_return_data['password']
                    cameraip = rtsp_return_data['ipaddress']
                    username = rtsp_return_data['username']
                    port = rtsp_return_data['port']
                    try:
                        if regex_pwd.search(password) == None:
                            ping_response = True
                            if ping_response:
                                image_namereplace = ( replace_spl_char_panel_area_plant(plant   +    '-' + area))
                                rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                if rtsp_response_image:
                                    final_data = {'camera_ip': cameraip,'username': username, 'password':     password, 'camera_brand': brand,'rtsp_port': port,'cameraname':cameraname, 'plant': plant, 'area': area,
                                                  'imagename':rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'],
                                                  'image_width': rtsp_response_image['width'],'cameraid': None, 'alarm_type':alarm_type, 'alarm_ip_address': alarm_ip_address, 
                                                  'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [], 'camera_status':True, 'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': [],'analytics_status':'false'}
                                    result = mongo.db.ppera_cameras.insert_one( final_data)
                                    if result.acknowledged:
                                        ret = {'success': True, 'message':'camera added successfully.'}
                                    else:
                                        ret['message'] = ( 'data is not inserted properly, please try once again.' )
                                else:
                                    ret['message'] = ( 'rtsp stream is not working, please try once again.' )
                            else:
                                ret['message'] = 'cameraip is not able ping.'
                        else:
                            ret['message'] = ( 'camera password should not have any special characters.' )
                    except Exception as error:
                        print('ERROR -message in checking camera rtsp', str(error))
                        ERRORLOGdata("\n [ERROR] camera_api  --add_camera_rtsp 3 " + str(error)  +'  ----time ----   '+ now_time_with_time())
                        image_namereplace = replace_spl_char_panel_area_plant(plant + '-' + area)
                        rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                        if rtsp_response_image:
                            final_data = {'camera_ip': cameraip, 'username':  username, 'password': password,'camera_brand': brand, 'rtsp_port': port,'cameraname': cameraname, 'plant': plant,'area': area,
                                          'imagename':rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'], 'image_width':rtsp_response_image['width'], 'cameraid':None, 
                                          'alarm_type': alarm_type, 'alarm_ip_address': alarm_ip_address, 'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True, 
                                          'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': [],'analytics_status':'false'}
                            result = mongo.db.ppera_cameras.insert_one(final_data)
                            if result.acknowledged:
                                ret = {'success': True, 'message':'camera added successfully.'}
                            else:
                                ret['message'] = ( 'data is not inserted properly, please try once again.')
                        else:
                            ret['message'] = ( 'rtsp stream is not working, please try once again.')
                else:
                    ret['message'] = 'rtsp url error.'
            else:
                ret['message'] = ('entered ip is already exist, please go with edit roi option.')
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key ) + ' to enter. please enter properly.'
    return ret


@camera_details.route('/add_roi122notused', methods=['POST'])
def camera_adding_roi123():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'roi_data', 'ai_solutions']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            roi_data = data['roi_data']
            ai_solutions = data['ai_solutions']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if roi_data is not None:
                    if type(roi_data) == list:
                        if len(roi_data) != 0:
                            if ai_solutions is not None:
                                if type(ai_solutions) == list:
                                    if len(ai_solutions) == 1:
                                        if finddata['ai_solution' ] is not None and finddata['roi_data'] is not None:
                                            if roi_data == finddata['roi_data'] and ai_solutions == finddata['ai_solution']:
                                                result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, { '$set': {'roi_data': roi_data,'ai_solution': ai_solutions}}))
                                                if result.modified_count > 0:
                                                    ret = {'message': 'roi added successfully.','success': True}
                                                else:
                                                    ret['message'] = 'roi not adeed.'
                                            elif roi_data == finddata['roi_data']:
                                                if ai_solutions == finddata['ai_solution']:
                                                    result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data,'ai_solution': ai_solutions}}))
                                                    if (result.modified_count > 0):
                                                        ret = {'message':'roi added successfully.','success': True}
                                                    else:
                                                        ret['message'] = 'roi not adeed.'
                                                else:
                                                    ai_solutions.append(finddata['ai_solution'] )
                                                    result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data, 'ai_solution': ai_solutions}}))
                                                    if (result.modified_count > 0):
                                                        ret = {'message': 'roi added successfully.','success': True}
                                                    else:
                                                        ret['message'] = 'roi not adeed.'
                                            elif ai_solutions == finddata['ai_solution']:
                                                if roi_data == finddata['roi_data']:
                                                    result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data, 'ai_solution': ai_solutions}}))
                                                    if (result.modified_count > 0):
                                                        ret = {'message':'roi added successfully.','success': True}
                                                    else:
                                                        ret['message'] = 'roi not adeed.'
                                                else:
                                                    roi_data.append(finddata['roi_data'])
                                                    result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data, 'ai_solution': ai_solutions}}))
                                                    if (result.modified_count > 0):
                                                        ret = {'message':'roi added successfully.','success': True}
                                                    else:
                                                        ret['message'] = 'roi not adeed.'
                                            else:
                                                roi_data.append(finddata['roi_data'])
                                                ai_solutions.append(finddata['ai_solution'])
                                                result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data,'ai_solution': ai_solutions}}))
                                                if result.modified_count > 0:
                                                    ret = {'message':'roi added successfully.', 'success': True}
                                                else:
                                                    ret['message'] = 'roi not adeed.'
                                        elif finddata['ai_solution'] is not None:
                                            print(finddata['ai_solution'])
                                        elif finddata['roi_data'] is not None:
                                            print(finddata['roi_data'])
                                        else:
                                            result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data,'ai_solution': ai_solutions}}))
                                            if result.modified_count > 0:
                                                ret = {'message':'roi added successfully.','success': True}
                                            else:
                                                ret['message'] = 'roi not adeed.'
                                    elif len(ai_solutions) > 1:
                                        print(ai_solutions)
                                        print(roi_data)
                                    else:
                                        ret['message'] = ( 'please give proper ai_solutions, al_solutions should not None type or empty.')
                                else:
                                    ret['message'] = ( 'please give proper ai_solutions, it should be list type.')
                            else:
                                ret['message'] = 'please give proper ai_solutions.'
                        else:
                            ret['message'] = 'please give proper roi data.'
                    else:
                        ret['message'] = ('please give proper roi data, it should be list type.')
                else:
                    ret['message'] = 'please give proper roi data, it should not none type.'
            else:
                ret['message'] = ('for this particular id, there is no such camera data exists.'     )
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret


@camera_details.route('/add_roi', methods=['POST'])
def camera_adding_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'roi_data', 'ai_solutions', 'ppe_data']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            roi_data = data['roi_data']
            ai_solutions = data['ai_solutions']
            ppe_data = data['ppe_data']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if roi_data is not None:
                    if type(roi_data) == list:
                        if len(roi_data) != 0:
                            if roi_data == finddata['roi_data']:
                                if len(ppe_data) != 0:
                                    if ai_solutions is not None:
                                        if type(ai_solutions) == list:
                                            if len(ai_solutions) != 0:
                                                ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': ai_solutions,'ppe_data': ppe_data}}))
                                                if result.modified_count > 0:
                                                    ret = {'message':'ppe added successfully.', 'success': True}
                                                else:
                                                    ret['message'] = 'ppe not adeed.'
                                            else:
                                                ret['message'] = ( 'please give proper ai_solutions, al_solutions should not None type or empty.')
                                        else:
                                            ret['message'] = ('please give proper ai_solutions, it should be list type.')
                                    else:
                                        ret['message'] = 'please give proper ai_solutions.'
                                else:
                                    ret['message'] = 'please give proper ppe data.'
                            else:
                                if ai_solutions is not None:
                                    if type(ai_solutions) == list:
                                        if len(ai_solutions) != 0:
                                            ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                            result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data,'ai_solution': ai_solutions,'ppe_data': ppe_data}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'roi added successfully.','success': True}
                                            else:
                                                ret['message'] = 'roi not adeed.'
                                        else:
                                            ret['message'] = ('please give proper ai_solutions, al_solutions should not None type or empty.')
                                    else:
                                        ret['message'] = ('please give proper ai_solutions, it should be list type.' )
                                else:
                                    ret['message'] = 'please give proper ai_solutions.'
                        elif ppe_data is not None:
                            if type(ppe_data) == list:
                                if len(ppe_data) != 0:
                                    if ai_solutions is not None:
                                        if type(ai_solutions) == list:
                                            if len(ai_solutions) != 0:
                                                ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': ai_solutions,'ppe_data': ppe_data}}))
                                                if result.modified_count > 0:
                                                    ret = {'message':'ppe added successfully.', 'success': True}
                                                else:
                                                    ret['message'] = 'ppe not adeed.'
                                            else:
                                                ret['message'] = ( 'please give proper ai_solutions, al_solutions should not None type or empty.')
                                        else:
                                            ret['message'] = ('please give proper ai_solutions, it should be list type.')
                                    else:
                                        ret['message'] = 'please give proper ai_solutions.'
                                else:
                                    ret['message'] = 'please give proper ppe data.'
                            else:
                                ret['message'] = ('please give proper ppe data, it should be list type.')
                        else:
                            ret['message'] = ('please give proper input data, try once again.' )
                    else:
                        ret['message'] = ( 'please give proper roi data, it should be list type.' )
                else:
                    ret['message'] = 'please give proper roi data, it should not none type.'
            else:
                ret['message'] = ( 'for this particular id, there is no such camera data exists.' )
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret


@camera_details.route('/edit_roi', methods=['POST'])
def camera_edit_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ai_solutions', 'roi_data','roi_id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            roi_id = data['roi_id']
            ai_solutions = data['ai_solutions']
            roi_data = data['roi_data']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(roi_data) == list:
                    if len(roi_data) != 0:
                        if len(ai_solutions) != 0:
                            fetch_roi_data = finddata['roi_data']
                            if len(fetch_roi_data) != 0:
                                if len(fetch_roi_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data, 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not updated.'
                                elif len(fetch_roi_data) > 1:
                                    update_data = []
                                    if len(roi_data) == 1:
                                        final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                        for __, i in enumerate(fetch_roi_data):
                                            if int(i['roi_id']) == int(roi_data[0][ 'roi_id']):
                                                i['bb_box'] = roi_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': final_ai}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not updated.'
                                    elif len(roi_data) > 1:
                                        update_data = []
                                        final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
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
                                        result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': final_ai}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not updated.'
                                    else:
                                        ret['message'] = ( 'There is no roi region the camrea, please try to add.')
                            else:
                                ret['message'] = ('There is no camrea details exist , please try to add.')
                        elif len(fetch_roi_data) != 0:
                            update_data = []
                            if len(fetch_roi_data) == 1:
                                final_ai = list(set(ai_solutions).union(set (finddata['ai_solution'])))
                                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'roi_data': roi_data, 'ai_solution': final_ai}})
                                if result.modified_count > 0:
                                    ret = {'message': 'roi data updated successfully.','success': True}
                                else:
                                    ret['message'] = 'roi not updated.'
                            elif len(fetch_roi_data) > 1:
                                if len(roi_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(fetch_roi_data):
                                        if int(i['roi_id']) == int(roi_data[0]['roi_id']):
                                            i['bb_box'] = roi_data[0]['bb_box']
                                            update_data.append(i)
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not updated.'
                                elif len(roi_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
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
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'roi data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not updated.'
                                else:
                                    ret['message'] = ('There is no roi region the camrea, please try to add.')
                        else:
                            ret['message'] = ( 'There is no camrea details exist , please try to add.')
                    else:
                        ret['message'] = 'roi data should not be empty list.'
                else:
                    ret['message'] = 'roi data type should be list'
            else:
                ret['message'] = ( 'for this particular id, there is no such camera data exists.' )
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret






@camera_details.route('/delete_roi', methods=['POST'])
def camera_delete_roi():
    ret = {'success': False, 'message':'something went wrong with delete_roi roi api'}
    try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_id', 'ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if len(ai_solutions) != 0:
                            roi_data = finddata['roi_data']
                            if len(roi_data) != 0:
                                update_data = []
                                if len(roi_data) == 1:
                                    final_ai = list(set(ai_solutions).union  (set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': [], 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                                elif len(roi_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(roi_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            roi_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'roi data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                            else:
                                ret['message'] = ( 'There is no roi region the camrea, please try to add.')
                        else:
                            roi_data = finddata['roi_data']
                            if len(roi_data) != 0:
                                if len(roi_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': [], 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                                elif len(roi_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(roi_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            roi_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'roi data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                            else:
                                ret['message'] = ('There is no roi region the camrea, please try to add.')
                    else:
                        ret['message'] = ( 'please give proper roi data, it should not none type.')
                else:
                    ret['message'] = ('for this particular id, there is no such camera data exists.')
        else:
            ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    except Exception as error:
        ret['message'] = 'something error occurred in delete roi ' + str(error)  +'  ----time ----   '+ now_time_with_time()
        ERRORLOGdata("\n [ERROR] camera_api  --delete_roi 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret


def check_dataobjects_of_cr_data(dataobjects):
    datacrobjectsstatus = True
    print('data objects ',dataobjects)
    for i,j in enumerate(dataobjects):
        print(j)
        if j['min_count'] < j['max_count']:
            datacrobjectsstatus = True
        elif j['min_count'] != j['max_count']:
            datacrobjectsstatus = True
        else:
            datacrobjectsstatus=False  
            break 
    return datacrobjectsstatus


def check_the_tc_data_is_key_idisexistCRdata(find_data,roiid):
    print("find_data===", find_data)
    print("roi-id",roiid)
    id_status = True
    for i , j in enumerate(find_data['cr_data']):  
        print('lllll====lllll ',j)
        if j['roi_id']=='' or j['roi_id'] == None:
            pass
        elif j['roi_id']==roiid:
            id_status = False
    return id_status


def update_cr_data_to_existing_one(fINDCRDATA,GivenCRDATA):
    find_cr = fINDCRDATA['cr_data']
    initial_len = len(find_cr)
    find_cr.append(GivenCRDATA)
    if initial_len > len(find_cr) :
        print('finall cr data ===', len(find_cr))
    return find_cr


@camera_details.route('/add_cr_data', methods=['POST'])
def camera_add_cr_data():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'cr_data','ai_solutions']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            cr_data = data['cr_data']
            ai_solutions = data['ai_solutions']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if cr_data is not None:
                    if type(cr_data) == list:
                        if len(cr_data) != 0:
                            if ai_solutions is not None:
                                if type(ai_solutions) == list:
                                    if len(ai_solutions) != 0:
                                        print("found_data=", finddata['cr_data'])
                                        print("given_data=",cr_data)
                                        if len(cr_data)==1:
                                            if cr_data[0]['full_frame']:
                                                if cr_data[0]['bb_box'] ==''and cr_data[0]['area_name']=='':
                                                    #any([v==None for v in d.values()])
                                                    if check_arraydictionaryishavinganynonevalue(cr_data[0]['data_object']):
                                                        if check_dataobjects_of_cr_data(cr_data[0]['data_object']):
                                                            ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                            result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'cr_data':cr_data,'ai_solution': ai_solutions}}))
                                                            # print()
                                                            # if check_the_tc_data_is_key_idisexist(finddata,cr_data[0]['roi_id'])
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
                                                                    if len(finddata['cr_data']) !=0:
                                                                        print("cr_data--------------------",cr_data)
                                                                        print("cr_data0",cr_data[0]['roi_id'])
                                                                        if check_the_tc_data_is_key_idisexistCRdata(finddata,cr_data[0]['roi_id']):
                                                                            final_cr_data = update_cr_data_to_existing_one(finddata,cr_data[0])
                                                                            # final_cr_data = finddata['cr_data'].append(cr_data[0])
                                                                            if len(final_cr_data) != 0 :
                                                                                print("final_cr_data===",final_cr_data)
                                                                                ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                                                result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)},{'$set': {'cr_data':final_cr_data,'ai_solution': ai_solutions}}))
                                                                                if result.modified_count > 0:
                                                                                    ret = {'message': 'cr data added successfully.','success': True}
                                                                                else:
                                                                                    ret['message'] = 'cr data not adeed.'
                                                                            else:
                                                                                ret['message'] = 'cr data is not added, deu to some internal issue'
                                                                        else:
                                                                            ret['message']='roi key id already exists, please give proper one'
                                                                    else:
                                                                        final_cr_data = finddata['cr_data'].append(cr_data[0])
                                                                        print("final_cr_data===",final_cr_data)
                                                                        ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)},{'$set': {'cr_data':cr_data,'ai_solution': ai_solutions}}))
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
                                        ret['message'] = ('please give proper ai_solutions, al_solutions should not None type or empty.')
                                else:
                                    ret['message'] = ('please give proper ai_solutions, it should be list type.' )
                            else:
                                ret['message'] = 'please give proper ai_solutions.' 
                        else:
                            ret['message'] ='cr data is not given please give proper data.'         
                    else:
                        ret['message'] = ( 'please give proper cr data, it should be list type.' )
                else:
                    ret['message'] = 'please give proper cr data, it should not none type.'
            else:
                ret['message'] = ( 'for this particular id, there is no such camera data exists.' )
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret


@camera_details.route('/edit_crdata', methods=['POST'])
def camera_editCRroi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ai_solutions', 'cr_data','roi_id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            roi_id = data['roi_id']
            ai_solutions = data['ai_solutions']
            cr_data = data['cr_data']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(cr_data) == list:
                    if len(cr_data) != 0:
                        if len(ai_solutions) != 0:
                            fetch_cr_data = finddata['cr_data']
                            if len(fetch_cr_data) != 0:
                                if len(fetch_cr_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': cr_data, 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not updated.'
                                elif len(fetch_cr_data) > 1:
                                    update_data = []
                                    if len(cr_data) == 1:
                                        final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                        for __, i in enumerate(fetch_cr_data):
                                            if int(i['roi_id']) == int(cr_data[0][ 'roi_id']):
                                                i['bb_box'] = cr_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': final_ai}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    elif len(cr_data) > 1:
                                        update_data = []
                                        final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
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
                                        result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': final_ai}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    else:
                                        ret['message'] = ( 'There is no cr_data region the camrea, please try to add.')
                            else:
                                ret['message'] = ('There is no camrea details exist , please try to add.')
                        elif len(fetch_cr_data) != 0:
                            update_data = []
                            if len(fetch_cr_data) == 1:
                                final_ai = list(set(ai_solutions).union(set (finddata['ai_solution'])))
                                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'cr_data': cr_data, 'ai_solution': final_ai}})
                                if result.modified_count > 0:
                                    ret = {'message': 'cr_data data updated successfully.','success': True}
                                else:
                                    ret['message'] = 'cr_data not updated.'
                            elif len(fetch_cr_data) > 1:
                                if len(cr_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(fetch_cr_data):
                                        if int(i['roi_id']) == int(cr_data[0]['roi_id']):
                                            i['bb_box'] = cr_data[0]['bb_box']
                                            update_data.append(i)
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not updated.'
                                elif len(cr_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
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
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'cr_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not updated.'
                                else:
                                    ret['message'] = ('There is no cr_data region the camrea, please try to add.')
                        else:
                            ret['message'] = ( 'There is no camrea details exist , please try to add.')
                    else:
                        ret['message'] = 'cr_data data should not be empty list.'
                else:
                    ret['message'] = 'cr_data data type should be list'
            else:
                ret['message'] = ( 'for this particular id, there is no such camera data exists.' )
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret

@camera_details.route('/delete_cr_data', methods=['POST'])
def camera_delete_cr_data():
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_id', 'ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if len(ai_solutions) != 0:
                            cr_data = finddata['cr_data']
                            if len(cr_data) != 0:
                                update_data = []
                                if len(cr_data) == 1:
                                    final_ai = list(set(ai_solutions).union  (set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': [], 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                                elif len(cr_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(cr_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            cr_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                            else:
                                ret['message'] = ( 'There is no cr_data region the camrea, please try to add.')
                        else:
                            cr_data = finddata['cr_data']
                            if len(cr_data) != 0:
                                if len(cr_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': [], 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                                elif len(cr_data) > 1:
                                    update_data=[]
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(cr_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            cr_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                            else:
                                ret['message'] = ('There is no cr_data region the camrea, please try to add.')
                    else:
                        ret['message'] = ( 'please give proper cr_data data, it should not none type.')
                else:
                    ret['message'] = ('for this particular id, there is no such camera data exists.')
        else:
            ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    except Exception as error:
        ret['message'] = 'something error occurred in delete roi ' + str(error)  +'  ----time ----   '+ now_time_with_time()
        ERRORLOGdata("\n [ERROR] camera_api  --delete_cr_data 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret

def tc_data_modification(dbtcdata,requestdata):
    if dbtcdata is not None and requestdata is not None :
        if len(dbtcdata) !=0:
            if len(requestdata)==1:
                if requestdata[0] is not None:
                    dbtcdata.append(requestdata[0])
        else:
            dbtcdata = requestdata
    return dbtcdata


def check_the_tc_data_is_key_idisexist(find_data,roiid):
    id_status = True
    for i , j in enumerate(find_data):  
        if j['roi_id']==roiid:
            id_status = False
    return id_status

@camera_details.route('/add_tc_data', methods=['POST'])
def camera_add_tc_data():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'tc_data','ai_solutions']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            tc_data = data['tc_data']
            ai_solutions = data['ai_solutions']
            if id is not None:
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if tc_data is not None:
                        if type(tc_data) == list:
                            if len(tc_data) != 0:
                                if len(tc_data) ==1:
                                    print("tc -data ", tc_data[0])
                                    fetched_tc_data =  tc_data[0]
                                    print("fetched_tc_data---", fetched_tc_data)
                                    if len(fetched_tc_data['class_name']) !=0:
                                        if isEmpty(fetched_tc_data['line_bbox']):
                                            if check_dictionaryishavinganynonevalue(fetched_tc_data['line_bbox']):
                                                if check_the_tc_data_is_key_idisexist(finddata['tc_data'],fetched_tc_data['roi_id']):
                                                    returntcdata = tc_data_modification(finddata['tc_data'],tc_data)
                                                    if ai_solutions is not None:
                                                        if type(ai_solutions) == list:
                                                            if len(ai_solutions) != 0:
                                                                ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                                result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': ai_solutions,'tc_data': returntcdata}}))
                                                                if result.modified_count > 0:
                                                                    ret = {'message': 'traffic count data added successfully.', 'success': True}
                                                                else:
                                                                    ret['message'] = ('traffic count data not adeed.')
                                                            else:
                                                                ret['message'] = ('please give proper ai_solutions, al_solutions should not None type or empty.')
                                                        else:
                                                            ret['message'] = ( 'please give proper ai_solutions, it should be list type.')
                                                    else:
                                                        ret['message' ] = 'please give proper ai_solutions.' 
                                                else:
                                                    ret['message']='roi key id already exists, please give different one adding the tc data.'
                                            else:
                                                ret['message']='line bbox should not be have any none or empty values in dictionary.'
                                        else:
                                            ret['message']='line bbox should not be empty dictionary.'
                                    else:
                                        ret['message']='in tc data class name should not be empty list.'
                                else:
                                    ret['message'] ='tc data is containing multiple data objects.'
                        else:
                            ret['message'] = ( 'please give proper traffic data, it should be list type.' )
                    else:
                        ret['message'] = 'please give proper traffic data, it should not none type.'
                else:
                    ret['message'] = ( 'for this particular id, there is no such camera data exists.' )
            else:
                ret['message'] =  'give the proper mongodb id, id should not be none type.'
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret


@camera_details.route('/edit_tcdata', methods=['POST'])
def camera_edittcroi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ai_solutions', 'tc_data','roi_id']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            id = data['id']
            roi_id = data['roi_id']
            ai_solutions = data['ai_solutions']
            tc_data = data['tc_data']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(tc_data) == list:
                    if len(tc_data) != 0:
                        if len(ai_solutions) != 0:
                            fetch_tc_data = finddata['tc_data']
                            if len(fetch_tc_data) != 0:
                                if len(fetch_tc_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': tc_data, 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not updated.'
                                elif len(fetch_tc_data) > 1:
                                    update_data = []
                                    if len(tc_data) == 1:
                                        final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                        for __, i in enumerate(fetch_tc_data):
                                            if int(i['roi_id']) == int(tc_data[0][ 'roi_id']):
                                                i['bb_box'] = tc_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': final_ai}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    elif len(tc_data) > 1:
                                        update_data = []
                                        final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
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
                                        result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': final_ai}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    else:
                                        ret['message'] = ( 'There is no cr_data region the camrea, please try to add.')
                            else:
                                ret['message'] = ('There is no camrea details exist , please try to add.')
                        elif len(fetch_tc_data) != 0:
                            update_data = []
                            if len(fetch_tc_data) == 1:
                                final_ai = list(set(ai_solutions).union(set (finddata['ai_solution'])))
                                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'tc_data': tc_data, 'ai_solution': final_ai}})
                                if result.modified_count > 0:
                                    ret = {'message': 'tc_data data updated successfully.','success': True}
                                else:
                                    ret['message'] = 'tc_data not updated.'
                            elif len(fetch_tc_data) > 1:
                                if len(tc_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(fetch_tc_data):
                                        if int(i['roi_id']) == int(tc_data[0]['roi_id']):
                                            i['bb_box'] = tc_data[0]['bb_box']
                                            update_data.append(i)
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not updated.'
                                elif len(tc_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
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
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'tc_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not updated.'
                                else:
                                    ret['message'] = ('There is no tc_data in the camrea, please try to add.')
                        else:
                            ret['message'] = ( 'There is no camrea details exist , please try to add.')
                    else:
                        ret['message'] = 'tc_data data should not be empty list.'
                else:
                    ret['message'] = 'tc_data data type should be list'
            else:
                ret['message'] = ( 'for this particular id, there is no such camera data exists.' )
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret

@camera_details.route('/delete_tc_data', methods=['POST'])
def camera_delete_tc_data():
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if 1:
    # try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_id', 'ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if len(ai_solutions) != 0:
                            tc_data = finddata['tc_data']
                            if len(tc_data) != 0:
                                update_data = []
                                if len(tc_data) == 1:
                                    final_ai = list(set(ai_solutions).union  (set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': [], 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                                elif len(tc_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(tc_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            tc_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                            else:
                                ret['message'] = ( 'There is no tc_data region the camrea, please try to add.')
                        else:
                            tc_data = finddata['tc_data']
                            if len(tc_data) != 0:
                                update_data=[]
                                if len(tc_data) == 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': [], 'ai_solution':final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                                elif len(tc_data) > 1:
                                    final_ai = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                    for __, i in enumerate(tc_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            tc_data.remove(i)
                                            pass
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message':'tc_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not deleted.'
                            else:
                                ret['message'] = ('There is no tc_data in the camrea, please try to add.')
                    else:
                        ret['message'] = ( 'please give proper tc_data data, it should not none type.')
                else:
                    ret['message'] = ('for this particular id, there is no such camera data exists.')
        else:
            ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    # except Exception as error:
    #     ret['message'] = 'something error occurred in delete roi ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #ERRORLOGdata("\n [ERROR] camera_api  --delete_tc_data 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret


@camera_details.route('/get_ra_camera_details/<id>', methods=['GET'])
@camera_details.route('/get_ra_camera_details', methods=['GET'])
def ra_camera_details(id=None):
    ret = {'success': False, 'message':'something went wrong with ra camera details api'}
    try:
        final_data = []
        if id is not None:
            data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if data is not None:
                data = parse_json(data)
                data = delete_keys_from_dict(data, ['cameraid', 'username', 'password', 'camera_brand', 'rtsp_port','camera_status',  'timestamp'])
                final_data.append(data)
                if len(final_data) != 0:
                    ret = {'message': final_data, 'success': True}
                else:
                    ret['message'] = ('for this particular id, there is no such camera data exists.')
            else:
                ret['message'] = ( 'for this particular id, there is no such camera data exists.')
        else:
            data = mongo.db.ppera_cameras.find()
            if data is not None:
                for jj, i in enumerate(data):
                    i = delete_keys_from_dict(i, ['cameraid', 'username', 'password', 'image_height','image_width', 'rtsp_port', 'camera_status','timestamp'])
                    final_data.append(i)
                final_data = parse_json(final_data)
                if len(final_data) != 0:
                    ret = {'message': final_data, 'success': True}
                else:
                    ret['message'] = ( 'cameras are not found for RA, PPE, please add cameras.' )
            else:
                ret['message'] = 'cameras are not found for RA, PPE, please add cameras.'
    except Exception as error:
        ret['message'] = str(error)
        ERRORLOGdata("\n [ERROR] camera_api  --get_ra_camera_details 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret


def delete_hooter_data(find_data):
    try:
        hooter_find_data = mongo.db.hooter_on_table.find_one({'rtsp_url':find_data['camera_rtsp'], 'cameraname': find_data['camera_name']})
        if hooter_find_data is not None:
            delete_data = mongo.db.hooter_on_table.delete_one({'rtsp_url':hooter_find_data['camera_rtsp'], 'cameraname': hooter_find_data['camera_name']})
            if delete_data.deleted_count > 0:
                ret = {'message': 'hooter is deleted successfully.','success': True}
            else:
                ret['message'] = 'data is not deleted, please try once again.'
        else:
            ret['message'] = ( 'for the given id there no data found, please change the id or try once again.' )
    except Exception as error:
        ERRORLOGdata("\n [ERROR] camera_api  --delete_hooter_data 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
        print(error)


@camera_details.route('/delete_ra_camera/<id>', methods=['GET'])
def delete_ra_cameras(id):
    ret = {'success': False, 'message':'something went wrong with delete ra camera api'}
    try:
        if id is not None:
            find_data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if find_data is not None:
                delete_data = mongo.db.ppera_cameras.delete_one({'_id':ObjectId(id)})
                if delete_data.deleted_count > 0:
                    #delete_hooter_data(find_data)
                    ret = {'message': 'camera is deleted successfully.','success': True}
                else:ret['message' ] = 'data is not deleted, please try once again.'
            else:
                ret['message'] = ('for the given id there no data found, please change the id or try once again.')
        else:
            ret['message'] = 'please give mongoid for deletion of camera details.'
    except Exception as error:
        ret['message'] = str(error)
        ERRORLOGdata("\n [ERROR] camera_api  --delete_ra_camera 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return ret



@camera_details.route('/analytics_status/<id>/<status>', methods=['GET'])
def analyt(id = None, status=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    try:
        if id is not None and status is not None:
                data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if data is not None:
                    filters ={'_id': ObjectId(id)} #{'analytics_status': status}
                    newvalues = {'$set':{'analytics_status': status}}
                    result = mongo.db.ppera_cameras.update_one(filters, newvalues)
                    if result.modified_count > 0:
                        ret = {'message':'updated analytics status successfully.','success': True}
                    else:
                        ret['message'] = 'analytics status is not updated.'
                else:
                    ret['message']='camera details are not found for this id.'
        else:
            ret['message'] = 'mongoid and status should not be None.'
    except Exception as error:
        ret['message'] = "error occerred -"+str(error)
        ERRORLOGdata("\n [ERROR] camera_api  --analytics_status 1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    return jsonify(ret)
