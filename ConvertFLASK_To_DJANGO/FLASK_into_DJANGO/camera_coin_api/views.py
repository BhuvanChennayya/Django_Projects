from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.final_ping import *

# Create your views here.

def NEWCAPTURPANELIMAGE(url):
    print("camera url getting ==",url)
    response = True    
    verfy_rtsp_response = None
    if response:
        directory_path =  os.path.join(os.getcwd() , 'rtsp_roi_image')
        if not os.path.exists(directory_path):
            handle_uploaded_file(directory_path)
        present_time = replace_spl_char(str(datetime.now()))
        print('verify_rtsp====',url)
        cam = cv2.VideoCapture(url)
        full_path = None
        count=0
        if cam.isOpened() == True:
            name = 'docketrun' + '_' + present_time + '.jpg'
            name1 = 'docketrun' + '_' + present_time + '1' + '.jpg'
            while cam.isOpened():
                ret, frame = cam.read()
                if ret:
                    if count == 10:
                        if frame.shape[-1] == 3:
                            if frame.shape[0] > 10 and frame.shape[1] > 10:
                                if frame.dtype == 'uint8':
                                    full_path = directory_path + '/' + name
                                    full_path1 = directory_path + '/' + name1
                                    cv2.imwrite(full_path, frame)
                                    cv2.imwrite(full_path1, frame)
                                    image_resizing(full_path)
                                    
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'imagename': name}
                                    break
                    elif count == 30:
                        if frame.shape[-1] == 3:
                            if frame.shape[0] > 10 and frame.shape[1] > 10:
                                if frame.dtype == 'uint8':
                                    full_path = directory_path + '/' + name
                                    full_path1 = directory_path + '/' + name1
                                    cv2.imwrite(full_path, frame)
                                    cv2.imwrite(full_path1, frame)
                                    image_resizing(full_path)
                                    
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'imagename': name}
                                    break
                    count += 1
                else:
                    break
            cam.release()
            #cv2.destroyAllWindows()
    return verfy_rtsp_response

def CHECKRTSPISWORKING( camera_brand, camera_username, camera_password,  camera_ip_address):
    print("---------------------------999999999999993333333333333333", camera_brand, camera_username, camera_password,  camera_ip_address)
    data = {}
    rtsp_url = ESIBRANDCAMERASRTSP(camera_ip_address,camera_brand,camera_username,camera_password)
    print('RTSP ------------------------------ ', rtsp_url)
    image_data = NEWCAPTURPANELIMAGE(rtsp_url)
    print("-----file -------------------RTSP ---------------",rtsp_url)
    print('image_data', image_data)
    if image_data is not None:
        if image_data['status'] == True:
            data['rtsp_status'] = image_data['status']
            data['imagename'] = image_data['imagename']
            data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
        return data
    else:
        return None
    
       
def Panel_NEWIMAGE(data):
    ifworked= 0
    if isEmpty(data):
        ImageData=CHECKRTSPISWORKING(data['camera_brand'],data['username'],data['password'], data['camera_ip'])
        if ImageData is not None:
            ifworked = 1
            data['imagename'] =  ImageData['imagename']
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PANELWISEDATAWITH3343IDANDIMAGESNAME 1", str(error), " ----time ---- ", now_time_with_time()]))
    if ifworked : 
        return parse_json(data)
    else:
        return None
    
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
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
        # print(type(CamCount))
        # print(type(split_data[0]))
        if CamCount < int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status

def CHECKMECHANICALCOLUMNS(file_path, column_names):
    try:
        try:
            df = pd.read_excel(file_path)
            existing_columns = df.columns.tolist()
            existing_columns_lower = [col.lower() for col in existing_columns]
            column_names_lower = [col.lower() for col in column_names]
            # print("-----------------------------------column_names_lower-----------------",existing_columns_lower)
            missing_columns = [col for col in column_names_lower if col not in existing_columns_lower]
            if not missing_columns:
                print("All specified columns are present in the Excel file.")
                return True
            else:
                missing_columns_original = [col for col in column_names if col.lower() in missing_columns]
                # print("Missing columns:", missing_columns_original)
            
            return missing_columns_original
        except Exception as  error:       
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                existing_columns = df.columns.tolist()
                existing_columns_lower = [col.lower() for col in existing_columns]
                column_names_lower = [col.lower() for col in column_names]
                missing_columns = [col for col in column_names_lower if col not in existing_columns_lower]
                if not missing_columns:
                    print("All specified columns are present in the Excel file.")
                    return True
                else:
                    missing_columns_original = [col for col in column_names if col.lower() in missing_columns]
                    # print("Missing columns:", missing_columns_original)
                return missing_columns_original
            except Exception as  error:
                print("")
                #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 2", str(error), " ----time ---- ", now_time_with_time()]))
        # df = pd.read_excel(file_path)
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
def Readnumbercolumn(file_path,column_names):
    try:
        try:
            df = pd.read_excel(file_path)
            df = df.dropna(how='all')
            existing_columns = df['IP Address'].tolist()
            print("columns ==read",existing_columns)
            existing_columns = [element if isinstance(element, ( str)) else None for element in existing_columns]
            # existing_columns = [int(float(element)) if isinstance(element, (float, int, str)) and element.replace('.', '').isdigit() else None for element in existing_columns]

            print("converted list llll-------",existing_columns)
            common_elements = set(existing_columns).intersection(column_names)
            return common_elements
        except Exception as  error:        
            # try:
            if 1:
                print("second try for reading excel ====")
                df = pd.read_excel(file_path, engine='openpyxl')
                df = df.dropna(how='all')
                existing_columns = df['IP Address'].tolist()
                
                print("columns ==read",existing_columns)
                existing_columns = [(element) if isinstance(element, ( str)) else None for element in existing_columns]
                # existing_columns = [int(float(element)) if isinstance(element, (float, int, str)) and element.replace('.', '').isdigit() else None for element in existing_columns]

                print("converted list llll-------",existing_columns)
                common_elements = set(existing_columns).intersection(column_names)
                print("comman ip list ---",common_elements)
                return common_elements
            # except Exception as  error:
            #     print("")
                #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 2", str(error), " ----time ---- ", now_time_with_time()]))
        # df = pd.read_excel(file_path)
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
def check_the_ip_status(csv_creating_file,df):
    table = open(csv_creating_file + '.csv', 'r')
    reader = csv.DictReader(table)
    header = df.head()
    ip_address_count= []
    for i____, each in enumerate(reader):
        new_each ={}        
        for fii, field in each.items():
            fii = fii.lower()
            if '.' in fii:
                fii = fii.replace('.', '')
            if ' ' in fii:
                fii = fii.replace(' ', '_')
            new_each[fii]=field
        if new_each['ip_address'] not in ip_address_count:
            ip_address_count.append(new_each['ip_address'])
    if check_license_of_camera(len(ip_address_count)):
        return True
    else:
        return False   

def REadExcelFIleGetcameradetails(csv_creating_file, df):
    print(df)
    table = open(csv_creating_file + '.csv', 'r')
    reader = csv.DictReader(table)
    header = df.head()
    count = 0
    ip_address_count= []
    ALL_DATA = []
    for i____, each in enumerate(reader):
        row = {}
        for fii, field in enumerate(header):
            field1 = field.lower()
            if '.' in field1:
                field1 = field1.replace('.', '')
            if ' ' in field1:
                field1 = field1.replace(' ', '_')
            each[field] = clean(each[field])
            each[field] = clear_asci(each[field])
            row[field1] = each[field]
            
        ALL_DATA.append(row)
    if len(ALL_DATA) !=0 :
        for k ,i in enumerate(ALL_DATA):
            if i['ip_address']  not in ip_address_count:
                ip_address_count.append(i['ip_address'])
                
        print("length of all data ===",len(ALL_DATA))
        if  check_license_of_camera(len(ip_address_count)):
            for index, eachrow in enumerate(ALL_DATA):
                print("eachrow======",eachrow)
                if eachrow['ip_address'] is not None:   
                    eachrow['timestamp'] = str(now_time_with_time())
                    if final_ping(eachrow['ip_address']): 
                        eachrow['ip_status'] = {'ip': eachrow['ip_address'],'status': True}
                    else:
                        eachrow['ip_status'] = {'ip': eachrow['ip_address'],'status': False}
                else:
                    eachrow['ip_status'] = {'ip': None, 'status': False}
                    eachrow['timestamp'] = str(now_time_with_time())

                print("---eachrow---ip_status",eachrow)
                    
                if eachrow['ip_status']['status'] :                        
                    if dictionary_key_exists(eachrow,'video_names'):
                        pass
                    else:
                        eachrow['video_names']=None   
                         

                    eachrow["analytics_status"]="false"
                    eachrow["ai_solution"]={
                                            "CR": False,
                                            "PPE": False,
                                            "RA": False,
                                            "TC": False,
                                            "Parking":False,
                                            "NO_Parking":False,
                                            "Traffic_Jam":False,
                                            "spillage":False,
                                            "fire":False,
                                            "dust":False
                                        }
                    eachrow["ppe_data"]= [
                                        {
                                        "helmet": False,
                                        "vest": False
                                        }
                                    ]
                    eachrow["cr_data"]=[]
                    eachrow["tc_data"]=[]
                    eachrow["roi_data"]=[]
                    eachrow["alarm_enable"]=False
                    eachrow['coin_details']=None
                    eachrow["alarm_type"]= {
                            "hooter": None,
                            "relay": None
                        },
                    eachrow["alarm_ip_address"]= {
                            "hooter": None,
                            "relay": None
                        }
                    eachrow['alarm_version']={'hooter':None,'relay':None}
                    if eachrow['ip_status']['status'] == True:
                        find_data = None#ppera_cameras.find_one({ 'timestamp':{'$regex': '^' + str(date.today())}})#'no': eachrow['no'],
                        if find_data is None:
                            eachrow = CHECKCAMERADATA(eachrow)
                            if eachrow['data'] is not None:
                                print("RTSP _working -------------------------Eachrow===",eachrow)
                                if isEmpty(eachrow['data']) :
                                    eachrow['camera_ip']=eachrow['data']['camera_ip']
                                    eachrow['camera_id']=eachrow['data']['camera_id']
                                    eachrow['cameraname']=eachrow['data']['cameraname']
                                    eachrow['rtsp_url']=eachrow['data']['rtsp_url']
                                    eachrow['camera_status']=eachrow['data']['rtsp_status']
                                    eachrow['imagename']=eachrow['data']['imagename']
                                    eachrow['image_height']=eachrow['data']['image_height']
                                    eachrow['image_width']=eachrow['data']['image_width']
                                    del eachrow['data']
                                    if 'ip_address'in eachrow:
                                        del eachrow['ip_address']
                                    if 'no' in eachrow:
                                        del eachrow['no']
                                    if 'video_names' in eachrow:
                                        del eachrow['video_names']
                                    if 'ip_status' in eachrow:
                                        del eachrow['ip_status']
                                    if 'camera_username' in eachrow:
                                        eachrow['username']= eachrow['camera_username']
                                        del eachrow['camera_username']
                                    if 'camera_password' in eachrow:
                                        eachrow['password']= eachrow['camera_password']
                                        del eachrow['camera_password']
                                    if 'ip_address'in eachrow:
                                        del eachrow['ip_address']
                                    result = ppera_cameras.insert_one(eachrow)
                                    if result.acknowledged > 0:
                                        pass
                                else:
                                    
                                    if 'no' in eachrow:
                                        del eachrow['no']
                                    if 'video_names' in eachrow:
                                        del eachrow['video_names']
                                    if 'ip_status' in eachrow:
                                        del eachrow['ip_status']
                                    if 'camera_username' in eachrow:
                                        eachrow['username']= eachrow['camera_username']
                                        del eachrow['camera_username']
                                    if 'camera_password' in eachrow:
                                        eachrow['password']= eachrow['camera_password']
                                        del eachrow['camera_password']
                                    
                                    if 'ip_address'in eachrow:
                                        eachrow['camera_ip']=eachrow['ip_address']
                                        if eachrow['ip_address'] is not None and eachrow['ip_address'] !='':
                                            eachrow['cameraname']= remove_all_specail_char_with_hifhen(eachrow['ip_address'])
                                        del eachrow['ip_address']
                                    if eachrow['ip_address'] is not None and eachrow['ip_address'] !='':
                                        camera_name= remove_all_specail_char_with_hifhen(eachrow['ip_address'])
                                    eachrow['camera_id']=None
                                    result = ppera_cameras.insert_one(eachrow)
                                    if result.acknowledged > 0:
                                        pass
                    else:
                        if 'no' in eachrow:
                            del eachrow['no']
                        if 'video_names' in eachrow:
                            del eachrow['video_names']
                        if 'ip_status' in eachrow:
                            del eachrow['ip_status']
                        if 'camera_username' in eachrow:
                            eachrow['username']= eachrow['camera_username']
                            del eachrow['camera_username']
                        if 'camera_password' in eachrow:
                            eachrow['password']= eachrow['camera_password']
                            del eachrow['camera_password']
                        if 'ip_address'in eachrow:
                            eachrow['camera_ip']=eachrow['ip_address']
                            if eachrow['ip_address'] is not None and eachrow['ip_address'] !='':
                                eachrow['cameraname']= remove_all_specail_char_with_hifhen(eachrow['ip_address'])
                            del eachrow['ip_address']
                        eachrow['camera_id']=None
                        result = ppera_cameras.insert_one(eachrow)     
                else:
                    if 'no' in eachrow:
                        del eachrow['no']
                    if 'video_names' in eachrow:
                        del eachrow['video_names']
                    if 'ip_status' in eachrow:
                        del eachrow['ip_status']
                    if 'camera_username' in eachrow:
                        eachrow['username']= eachrow['camera_username']
                        del eachrow['camera_username']
                    if 'camera_password' in eachrow:
                        eachrow['password']= eachrow['camera_password']
                        del eachrow['camera_password']
                    if 'ip_address'in eachrow:
                        if eachrow['ip_address'] is not None and eachrow['ip_address'] !='':
                            eachrow['cameraname']= remove_all_specail_char_with_hifhen(eachrow['ip_address'])
                        eachrow['camera_ip']=eachrow['ip_address']
                        del eachrow['ip_address']
                    eachrow['camera_id']=None
                    result = ppera_cameras.insert_one(eachrow)
                           
        else:
            return {'error':False,'message':'limit exceeded','success':False}


def verify_rtsp(url, image_namereplace):
    directory_path = os.getcwd() + '/' + 'rtsp_roi_image'
    handle_uploaded_file(directory_path)
    present_time = replace_spl_char(str(datetime.now()))
    cam = cv2.VideoCapture(url)
    full_path = None
    count=0
    if cam.isOpened() == True:
        while cam.isOpened():            
            ret, frame = cam.read()
            if ret:
                if count == 10:
                    if frame.shape[-1] == 3:
                        if frame.shape[0] > 10 and frame.shape[1] > 10:
                            if frame.dtype == 'uint8':
                                name = image_namereplace + '_' + present_time + '.jpg'
                                full_path = directory_path + '/' + name
                                cv2.imwrite(full_path, frame)
                                image_resizing(full_path)
                                verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                                return verfy_rtsp_response
                            else:
                                name = image_namereplace + '_' + present_time + '.jpg'
                                full_path = directory_path + '/' + name
                                cv2.imwrite(full_path, frame)
                                image_resizing(full_path)
                                verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                                return verfy_rtsp_response
                        else:
                            name = image_namereplace + '_' + present_time + '.jpg'
                            full_path = directory_path + '/' + name
                            cv2.imwrite(full_path, frame)
                            image_resizing(full_path)
                            verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                            return verfy_rtsp_response
                    else:
                        name = image_namereplace + '_' + present_time + '.jpg'
                        full_path = directory_path + '/' + name
                        cv2.imwrite(full_path, frame)
                        image_resizing(full_path)
                        verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                        return verfy_rtsp_response
                        
                elif count == 30:
                    if frame.shape[-1] == 3:
                        if frame.shape[0] > 10 and frame.shape[1] > 10:
                            if frame.dtype == 'uint8':
                                name = image_namereplace + '_' + present_time + '.jpg'
                                full_path = directory_path + '/' + name
                                cv2.imwrite(full_path, frame)
                                image_resizing(full_path)
                                verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                                return verfy_rtsp_response
                            else:
                                name = image_namereplace + '_' + present_time + '.jpg'
                                full_path = directory_path + '/' + name
                                cv2.imwrite(full_path, frame)
                                image_resizing(full_path)
                                verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                                return verfy_rtsp_response
                        else:
                            name = image_namereplace + '_' + present_time + '.jpg'
                            full_path = directory_path + '/' + name
                            cv2.imwrite(full_path, frame)
                            image_resizing(full_path)
                            verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                            return verfy_rtsp_response
                    else:
                        name = image_namereplace + '_' + present_time + '.jpg'
                        full_path = directory_path + '/' + name
                        cv2.imwrite(full_path, frame)
                        image_resizing(full_path)
                        verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                        return verfy_rtsp_response
                else:
                    count += 30
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()
    else:
        return False


# @camera_coin.route('/CameraIMAGE/<id>', methods=['GET'])
@csrf_exempt
def CameraIMAGE(request,id=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if request.method == "GET":
        if 1:
        # try:
            if id is not None :
                data = ppera_cameras.find_one({'_id': ObjectId(id)})
                if data is not None:
                    return_data = Panel_NEWIMAGE(data)
                    if return_data is not None:
                        print("999999999999999988888------------camera_setting--------8888888---88888888899999999999999999999999999999999")
                        result = ppera_cameras.update_one({ '_id': ObjectId(id)},  {'$set': {"imagename":return_data['imagename']}})
                        print(result.matched_count)
                        if result.matched_count > 0:
                            ret = {'message': return_data, 'success': True}
                        else:
                            ret['message'] ='something went wrong updating image.'
                    else:
                        ret['message'] ='rtsp is not working or something wrong with rtsp.'
                else:
                    ret['message'] = 'panel data not found.'   
            else:
                ret['message']='please give proper input data id and imagename.'     
        # except ( 
        #          pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #          pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #          pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #          pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #          pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #          pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #          pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #          pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #          pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_panel_data3 1", str(error), " ----time ---- ", now_time_with_time()]))
        #     ret['message'] = " ".join(["something error has occered in api", str(error)])
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.") 
        # except Exception as  error:
        #     ret['message'] = str(error)
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_panel_data3 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return JsonResponse(ret)

# @camera_coin.route('/check_license', methods=['GET'])
@csrf_exempt
def checkingCamlicense(request):
    ret = {'message': 'something went wrong with get brand details api', 'success': False}
    if request.method == "GET":
    # if 1:
        try:
            sheet_data = job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
            sheet_camera_count = 0
            # print('sheet_data',sheet_data)
            if sheet_data is not None:
                sheet_data_count = list(panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                #mongo.db.panel_data.count_documents({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']})
                unique_iplist = []
                if len(sheet_data_count) !=0:
                    for kl , eachElements in enumerate(sheet_data_count):
                        if len(eachElements['data']) !=0:
                            if eachElements['ip_address'] not in unique_iplist:
                                unique_iplist.append(eachElements['ip_address'])
                        else:
                            if eachElements['ip_address'] not in unique_iplist:
                                unique_iplist.append(eachElements['ip_address'])
                    sheet_camera_count= len(unique_iplist) 
                
            CamCount = ppera_cameras.count_documents({})#find()#find_one()#ppera_cameras.find({}).count()
            # print("camera -count ",CamCount)
            # print("sheet_data count",sheet_camera_count)
            CamCount = CamCount + sheet_camera_count
            if check_license_of_camera(CamCount):
                ret['message']='you have license to add the camera'
                ret['success']=True
            else:
                ret['message']="you don't have license to add the camera."
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license_of_camera 4", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)

# @camera_coin.route('/get_camera_brand_details', methods=['GET'])
@csrf_exempt
def get_camera_brand_details_all(request):
    ret = {'message': 'something went wrong with get brand details api', 'success': False}
    if request.method == "GET":
        try:
            data = ['cp_plus', 'dahua', 'pelco', 'bosch', 'hikvision','samsung', 'uniview', 'univision', 'secur_eye',
                    'axis', 'honeywell','geovision','hixecure' ,'hifocus','sparsh','ganz','aviron','docketrun']
            if len(data) != 0:
                ret = {'success': True, 'message': data}
            else:
                ret['message'] = 'data not found'
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- get_camera_brand_details 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)

# @camera_coin.route('/get_sample_rtsp', methods=['GET'])
@csrf_exempt
def get_smaple_rtsp_all_brands(request):
    ret = {'message': 'something went wrong with get brand details api','success': False}
    if request.method == "GET":
        try:
            data = ['cp_plus', 'dahua', 'pelco', 'bosch', 'hikvision','samsung', 'uniview', 'univision', 'secur_eye',
                    'axis', 'honeywell','geovision','hixecure' ,'hifocus','sparsh','ganz','aviron','docketrun']
            dash_data = []
            cameraip = '192.168.1.1'
            channelNo = '1'
            username = 'admin'
            password = 'admin123'
            port = '544'
            for I___, i in enumerate(data):
                rtsp_url = Samplerurl_for_all_brand(cameraip, channelNo,username, password, i, port)#create_rtsp_for_all_brand(cameraip, channelNo,username, password, i, port)
                sample_data = {'rtsp': rtsp_url, 'username': username, 'password': password, 'ipaddress': cameraip, 'channelno': channelNo, 'port': port, 'brand': i}
                dash_data.append(sample_data)
            if len(dash_data) != 0:
                ret = {'success': True, 'message': dash_data}
            else:
                ret['message'] = 'data not found'
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- get_sample_rtsp 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)

# @camera_coin.route('/license_count', methods=['GET'])
def license_count(request):
    ret = {'message': 'something went wrong with get license_count', 'success': False}
    if request.method == "GET":
        Return = {'total_license':0,'added_cameras_count':0,'remaining_license':0}
        # if 1:
        try:
            sheet_data =job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
            sheet_camera_count = 0
            # print('sheet_data',sheet_data)
            if sheet_data is not None:
                sheet_data_count = list(panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                #mongo.db.panel_data.count_documents({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']})
                unique_iplist = []
                if len(sheet_data_count) !=0:
                    for kl , eachElements in enumerate(sheet_data_count):
                        if len(eachElements['data']) !=0:
                            if eachElements['ip_address'] not in unique_iplist:
                                unique_iplist.append(eachElements['ip_address'])
                        else:
                            if eachElements['ip_address'] not in unique_iplist:
                                unique_iplist.append(eachElements['ip_address'])
                    sheet_camera_count= len(unique_iplist) 
                
            CamCount = ppera_cameras.count_documents({})#find()#find_one()#ppera_cameras.find({}).count()
            # print("camera -count ",CamCount)
            # print("sheet_data count",sheet_camera_count)
            CamCount = CamCount + sheet_camera_count
            Total_license = NEWLICENSECOUNT() 
            Return = {'total_license':Total_license,'added_cameras_count':CamCount,'remaining_license':Total_license-CamCount}
            ret['message']=Return
            ret['success']=True
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_licedsdnse_of_camera 4", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)

# @camera_coin.route('/addcamerausingexcel', methods=['POST'])
@csrf_exempt
def ADDCAMERASUSINGEXCEL(request):
    ret = {'message': 'Something error has occured in your code', 'success': False}
    # if request.method=="POST":
    #     file_key = ['file']
    #     excelfile = request.FILES
    #     convert_list = dict(excelfile.lists())
    #     converting_set = set(convert_list)
    #     f_key = set(file_key)
    #     missing_key = list(sorted(f_key - converting_set))
    #     get_excel_file = request.FILES.get('file')
    #     print("get_excel_file===",get_excel_file)
    #     columns_to_lowercase = ['Camera Brand']

    if request.method == "POST":
        # Required key
        file_key = ['file']
        # Get uploaded files from  request
        excelfile = request.FILES
        # Create a dictionary of uploaded files with their corresponding lists 
        convert_list = {key: excelfile.getlist(key) for key in excelfile.keys()}
        # Convert to sets for comparison
        converting_set = set(convert_list.keys())
        print(converting_set)
        f_key = set(file_key)
        # Identify missing keys
        missing_key = list(sorted(f_key - converting_set))
        # Get the uploaded Excel file
        get_excel_file = request.FILES.get('file')
        print("get_excel_file ===", get_excel_file)
        columns_to_lowercase = ['Camera Brand']
        # Placeholder for further processing
           
    #     # sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
        # if sheet_data is not None:
        if 1:
            if len(missing_key) != 0:
                ret = {'message':'You have missed these parameters {0} to enter. please enter properly.'.format(missing_key), 'success': False}
            elif len(get_excel_file.filename) != 0:
                excelfilepath = 'mechanical_camera_excel'
                now = datetime.now()
                csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
                filename_db = os.path.join(os.getcwd(), excelfilepath,"Mechanical"+now.strftime('%m-%d-%Y-%H-%M-%S.')+str(extention_of_excel))
                handle_uploaded_file(os.path.join(os.getcwd(),excelfilepath))
                get_excel_file.seek(0)
                get_excel_file.save(os.path.join(os.getcwd(),excelfilepath,filename_db))
                columns_to_check = ['No', 'Department', 'Area', 'Plant',  'IP Address',  'Camera Brand','camera_username','camera_password']
                missingcolumns = CHECKMECHANICALCOLUMNS(get_excel_file, columns_to_check)
                print("check job numbers ===", )
                LISTIPaddress = GETLISTOFIPSEXISTS()
                TOtallicense = GETCAMERALICENSE()
                print("TOtallicense-----------------",TOtallicense)
                print("LISTIPaddress",LISTIPaddress)
                Remaininglicense = TOtallicense['message']['remaining_license'] 
                totalcamerasinexcel =Getipaddresslist(get_excel_file,LISTIPaddress)
                if type(totalcamerasinexcel)==list:
                    print("Remaininglicense<=len(LISTIPaddress)",Remaininglicense,len(totalcamerasinexcel))
                    print("listed================licenser ===",len(totalcamerasinexcel) <=Remaininglicense)
                    if Remaininglicense !=0 and len(totalcamerasinexcel) <=Remaininglicense:
                        print("listed ipaddress ====",LISTIPaddress)
                        resultsIPaddress = Readnumbercolumn(get_excel_file,LISTIPaddress)
                        print("resultsIPaddress====",resultsIPaddress)
                        if missingcolumns is not None:
                            if resultsIPaddress is  None or len(resultsIPaddress) ==0:                    
                                if type(missingcolumns) ==list:
                                    if len(missingcolumns) !=0 and len(missingcolumns) ==1 :
                                        if 'video names' in missingcolumns:                             
                                            Extension_excel = ['.XLS', '.XLSX', '.xls', '.xlsx']
                                            csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
                                            excel_sheet_name = 'ESI_MONITORING_' + now.strftime('%m-%d-%Y-%H-%M-%S')
                                            csv_creating_file = os.path.join(os.getcwd() ,excelfilepath , excel_sheet_name)
                                            if get_excel_file.filename.endswith(tuple(Extension_excel)):

                                                try:
                                                    read_file = pd.read_excel(filename_db)
                                                    read_file = read_file.dropna(how='all')
                                                    read_file = read_file.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                                    for column in columns_to_lowercase:
                                                        if column in read_file.columns:
                                                            read_file[column] = read_file[column].str.lower()
                                                    print('excel reading ', read_file)
                                                    read_file.to_csv(csv_creating_file + '.csv', index=None, header=True)
                                                except Exception as  error:
                                                    ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 1", str(error), " ----time ---- ", now_time_with_time()]))
                                                    try:
                                                        read_file = pd.read_excel(filename_db, engine='openpyxl')
                                                        read_file = read_file.dropna(how='all')
                                                        read_file = read_file.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                                        for column in columns_to_lowercase:
                                                            if column in read_file.columns:
                                                                read_file[column] = read_file[column].str.lower()
                                                        read_file.to_csv(csv_creating_file + '.csv', index=None,header=True)
                                                    except Exception as  error:
                                                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 2", str(error), " ----time ---- ", now_time_with_time()]))
                                                df = pd.DataFrame(pd.read_csv(csv_creating_file + '.csv'))  
                                                # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                                # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                                df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)          
                                                if check_the_ip_status(csv_creating_file,df):
                                                    check_status_variable =  REadExcelFIleGetcameradetails(csv_creating_file ,  df)
                                                    print('uploading-completed----------')
                                                    if check_status_variable is None: 
                                                        ret = {'message': 'successfully added', 'success': True}
                                                                                            
                                                    else:
                                                        print("check statu variable ===", check_status_variable)
                                                        if check_status_variable['error']:
                                                            ret= {'message': check_status_variable['message'], 'success': False}
                                                        # else:
                                                        #     sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
                                                        #     if len(sheet_data) != 0:
                                                        #         think = 0
                                                        #         print("sheet_data----",sheet_data)
                                                else:
                                                    ret={'message': 'maximum camera limit has reached.', 'success': False}
                                            else:
                                                ret['message'] = 'Please upload correct format excel sheet.'
                                        else:
                                            ret['message']='missing column names in  {0}'.format(missingcolumns)

                                        print("columns===",missingcolumns)
                                    elif len(missingcolumns) !=0 and len(missingcolumns) > 1:
                                        ret['message']='missing column names in  {0}'.format(missingcolumns)
                                    else:
                                        ret['message']='job sheet some iternal error please check and upload error ==={0}'.format(missingcolumns)

                                    print("hello_ missing coumns found==",missingcolumns)
                                elif type(missingcolumns) ==bool :
                                    Extension_excel = ['.XLS', '.XLSX', '.xls', '.xlsx']
                                    csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
                                    excel_sheet_name = 'ESI_MONITORING_' + now.strftime('%m-%d-%Y-%H-%M-%S')
                                    csv_creating_file = os.path.join(os.getcwd() ,excelfilepath , excel_sheet_name)
                                    if get_excel_file.filename.endswith(tuple(Extension_excel)):
                                        try:
                                            read_file = pd.read_excel(filename_db)
                                            print('excel reading ', read_file)
                                            read_file = read_file.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                            for column in columns_to_lowercase:
                                                if column in read_file.columns:
                                                    read_file[column] = read_file[column].str.lower()
                                            read_file.to_csv(csv_creating_file + '.csv', index=None, header=True)
                                        except Exception as  error:
                                            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 1", str(error), " ----time ---- ", now_time_with_time()]))
                                            try:
                                                read_file = pd.read_excel(filename_db, engine='openpyxl')
                                                read_file = read_file.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                                for column in columns_to_lowercase:
                                                    if column in read_file.columns:
                                                        read_file[column] = read_file[column].str.lower()
                                                read_file.to_csv(csv_creating_file + '.csv', index=None,header=True)
                                            except Exception as  error:
                                                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 2", str(error), " ----time ---- ", now_time_with_time()]))
                                        df = pd.DataFrame(pd.read_csv(csv_creating_file + '.csv'))  
                                        # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                                        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)          
                                        if check_the_ip_status(csv_creating_file,df):
                                            check_status_variable =  REadExcelFIleGetcameradetails(csv_creating_file ,  df)
                                            
                                            print('uploading-completed----------')
                                            if check_status_variable is None: 
                                                ret = {'message': 'successfully added', 'success': True}
                                            else:
                                                print("check statu variable ===", check_status_variable)
                                                if check_status_variable['error']:
                                                    ret= {'message': check_status_variable['message'], 'success': False}
                                                    
                                                # else:
                                                    # sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
                                                    # if len(sheet_data) != 0:
                                                    #     think = 0
                                        else:
                                            ret={'message': 'maximum camera limit has reached.', 'success': False}
                                    else:
                                        ret['message'] = 'Please upload correct format excel sheet.'
                                else:
                                    ret = {'message': 'missing column names - {0}'.format(missingcolumns),'success': False}
                            else:
                                ret['message']='in uploaded jobsheet {0} ipaddress are already exist, please remove already exist ipaddress and then try to upload.'.format(resultsIPaddress)
                        else:
                            ret = {'message': 'missing column names - {0}'.format(missingcolumns),'success': False}
                    else:
                        ret={'message': 'reached maximum license count','success': False}
                else:
                    ret={'message': 'please upload correct format excel','success': False}
            else:
                ret = {'message': 'missing file {0}'.format(converting_set),'success': False}
        else:
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'
    return JsonResponse(ret)


# @camera_coin.route('/add_camera', methods=['POST'])
@csrf_exempt
def add_Acamera(request):
    ret = {'success': False, 'message':'something went wrong with add camera api'}
    if request.method == "POST":
        data = json.loads(request.body)
        print("------------data------------",data)
        if data == None:
            data = {}
        request_key_array = ['cameraip', 'camera_brand', 'username', 'password','plant', 'area', 'cameraname', 'alarm_ip_address', 'alarm_type','coin_details','department','alarm_enable']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                print("camera_ip something missing ",output)
                print("data====", data)
                if len(output)==2 and ('alarm_ip_address' in output  and "alarm_type" in output):
                    cameraip = data['cameraip']
                    brand = data['camera_brand']
                    department = data['department']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']
                    alarm_ip_address = data['alarm_ip_address']
                    alarm_enable = data['alarm_enable']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data =ppera_cameras.find_one({'camera_ip': cameraip})
                    if find_data is None:
                        if regex_pwd.search(password) == None:
                            ping_response = final_ping(cameraip)
                            if ping_response:
                                channelNo = '1'
                                rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                                if rtsp_response:
                                    image_namereplace = (replace_spl_char_panel_area_plant(plant  + '_' + area))
                                    rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                    if rtsp_response_image:
                                        final_data = {"department":department,
                                            'camera_ip': cameraip,'username': username, 'password': password,
                                        'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                        'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                        'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type, 'coin_details':None,'alarm_enable':alarm_enable,
                                        'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                        'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution':ai_solution ,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                        result = ppera_cameras.insert_one(final_data)
                                        if result.acknowledged:
                                            ret = {'success': True, 'message': 'camera added successfully.'}
                                        else:
                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                    else:
                                        ret['message'] = 'rtsp stream is not working, please try once again.'
                                else:
                                    ret['message'] = " ".join(["rtsp url is not able create or format it, please enter camera brand ", str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) ])
                            else:
                                ret['message'] = 'cameraip is not able ping.'
                        else:
                            ret['message'] = 'camera password should not have any special characters.'
                    else:
                        ret['message'] = 'entered ip is already exist, please go with edit roi option.'
                elif len(output)==2 and ('coin_details' in output  and "alarm_type" in output):
                    cameraip = data['cameraip']
                    department= data['department']
                    brand = data['camera_brand']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']
                    alarm_ip_address = data['alarm_ip_address']
                    alarm_enable = data['alarm_enable']
                    coin_details = data['coin_details']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data = ppera_cameras.find_one({'camera_ip': cameraip})
                    if alarm_type =='sensegiz':
                        if find_data is None:
                            if regex_pwd.search(password) == None:
                                ping_response = final_ping(cameraip)
                                if ping_response:
                                    channelNo = '1'
                                    rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                                    if rtsp_response:
                                        image_namereplace = (replace_spl_char_panel_area_plant(plant  + '_' + area))
                                        rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                        if rtsp_response_image:
                                            final_data = {"department":department, 'camera_ip': cameraip,'username': username, 'password': password,
                                            'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                            'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                            'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type, 'coin_details':coin_details,'alarm_enable':alarm_enable,
                                            'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                            'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                            result = ppera_cameras.insert_one(final_data)
                                            if result.acknowledged:
                                                ret = {'success': True, 'message': 'camera added successfully.'}
                                            else:
                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                        else:
                                            ret['message'] = 'rtsp stream is not working, please try once again.'
                                    else:
                                        ret['message'] = " ".join(["rtsp url is not able create or format it, please enter camera brand ", str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) ])
                                else:
                                    ret['message'] = 'cameraip is not able ping.'
                            else:
                                ret['message'] = 'camera password should not have any special characters.'
                        else:
                            ret['message'] = 'entered ip is already exist, please go with edit roi option.'
                    else:
                        ret['message'] = " ".join(["You have missed these parameters ", str(output) ,' to enter. please enter properly.' ])        
                elif len(output)==2 and ('coin_details' in output  and "alarm_ip_address" in output):
                    cameraip = data['cameraip']
                    department= data['department']
                    brand = data['camera_brand']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']
                    alarm_ip_address = data['alarm_ip_address']
                    alarm_enable = data['alarm_enable']
                    coin_details = data['coin_details']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data = ppera_cameras.find_one({'camera_ip': cameraip})
                    if alarm_type =='sensegiz':
                        if find_data is None:
                            if coin_details is not None and coin_details !='':
                                if regex_pwd.search(password) == None:
                                    ping_response = final_ping(cameraip)
                                    if ping_response:
                                        channelNo = '1'
                                        rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                                        if rtsp_response:
                                            image_namereplace = (replace_spl_char_panel_area_plant(plant  + '_' + area))
                                            rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                            if rtsp_response_image:
                                                final_data = {"department":department,
                                                    'camera_ip': cameraip,'username': username, 'password': password,
                                                'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                                'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                                'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type, 'coin_details':coin_details,'alarm_enable':data['alarm_enable'],
                                                'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                                'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                                result = ppera_cameras.insert_one(final_data)
                                                if result.acknowledged:
                                                    ret = {'success': True, 'message': 'camera added successfully.'}
                                                else:
                                                    ret['message'] = 'data is not inserted properly, please try once again.'
                                            else:
                                                ret['message'] = 'rtsp stream is not working, please try once again.'
                                        else:
                                            ret['message'] = " ".join(["rtsp url is not able create or format it, please enter camera brand ", str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) ])  
                                    else:
                                        ret['message'] = 'cameraip is not able ping.'
                                else:
                                    ret['message'] = 'camera password should not have any special characters.'
                            else:
                                ret['message']='coin details are empty please give proper input.'
                        else:
                            ret['message'] = 'entered ip is already exist, please go with edit roi option.'
                    else:
                        ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ])      
                elif len(output)==1 and ('alarm_ip_address' in output  or "alarm_type" in output):                
                    cameraip = data['cameraip']
                    brand = data['camera_brand']
                    department= data['department']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']
                    alarm_ip_address = data['alarm_ip_address']
                    alarm_enable= data['alarm_enable']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data = ppera_cameras.find_one({'camera_ip': cameraip})
                    if alarm_type != 'sensegiz':
                        if alarm_type in ['hooter','relay']:
                            if find_data is None:
                                if regex_pwd.search(password) == None:
                                    ping_response = final_ping(cameraip)
                                    if ping_response:
                                        channelNo = '1'
                                        rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                                        if rtsp_response:
                                            image_namereplace = (replace_spl_char_panel_area_plant(plant  + '_' + area))
                                            rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                            if rtsp_response_image:
                                                final_data = {"department":department,
                                                    'camera_ip': cameraip,'username': username, 'password': password,
                                                    'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                                    'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                                    'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type, 'coin_details':None,'alarm_enable':alarm_enable,
                                                    'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                                    'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                                result = ppera_cameras.insert_one(final_data)
                                                if result.acknowledged:
                                                    ret = {'success': True, 'message': 'camera added successfully.'}
                                                else:
                                                    ret['message'] = 'data is not inserted properly, please try once again.'
                                            else:
                                                ret['message'] = 'rtsp stream is not working, please try once again.'
                                        else:
                                            ret['message'] = 'rtsp url is not able create or format it, please enter camera brand ' + str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'}) + '.'
                                    else:
                                        ret['message'] = 'cameraip is not able ping.'
                                else:
                                    ret['message'] = 'camera password should not have any special characters.'
                            else:
                                ret['message'] = 'entered ip is already exist, please go with edit roi option.'
                        else:
                            ret['message'] ="please check spelling of alarm type, try once again."
                    elif alarm_type =='sensegiz':
                        ai_solution = data['ai_solution']
                        coin_details =  data['coin_details']
                        if find_data is None:
                            if regex_pwd.search(password) == None:
                                ping_response = final_ping(cameraip)
                                if ping_response:
                                    channelNo = '1'
                                    rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                                    if rtsp_response:
                                        image_namereplace = (replace_spl_char_panel_area_plant(plant  + '_' + area))
                                        rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                        if rtsp_response_image:
                                            final_data = {"department":department,
                                                'camera_ip': cameraip,'username': username, 'password': password,
                                            'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                            'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                            'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type, 'coin_details':coin_details,
                                            'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 'alarm_enable':alarm_enable,
                                            'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                            result = ppera_cameras.insert_one(final_data)
                                            if result.acknowledged:
                                                ret = {'success': True, 'message': 'camera added successfully.'}
                                            else:
                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                        else:
                                            ret['message'] = 'rtsp stream is not working, please try once again.'
                                    else:
                                        ret['message'] =" ".join(["rtsp url is not able create or format it, please enter camera brand == ", str({'dahua', 'hikvision', 'samsung','cp_plus', 'bosch'})])   
                                else:
                                    ret['message'] = 'cameraip is not able ping.'
                            else:
                                ret['message'] = 'camera password should not have any special characters.'
                        else:
                            ret['message'] = 'entered ip is already exist, please go with edit roi option.'
                    else:
                        ret['message']="entered wrong alarm_type, please try once again"
                else:
                    ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                cameraip = data['cameraip']
                department= data['department']
                brand = data['camera_brand']
                username = data['username']
                password = data['password']
                port = data['port']
                plant = data['plant']
                area = data['area']
                cameraname = data['cameraname']
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                alarm_enable = data['alarm_enable']
                ai_solution = data['ai_solution']
                genetic_id = None
                if 'genetic_id' in data :
                    genetic_id = data['genetic_id']
                regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                find_data = ppera_cameras.find_one({'camera_ip': cameraip})
                if find_data is None:
                    if regex_pwd.search(password) == None:
                        ping_response = final_ping(cameraip)
                        if ping_response:
                            channelNo = '1'
                            rtsp_response = create_rtsp_for_all_brand(cameraip,channelNo, username, password, brand, port)
                            if rtsp_response:
                                image_namereplace = (replace_spl_char_panel_area_plant(plant  + '_' + area))
                                rtsp_response_image = verify_rtsp(rtsp_response,image_namereplace)
                                if rtsp_response_image:
                                    final_data = {"department":department,
                                        'camera_ip': cameraip,'username': username, 'password': password, 'camera_brand': brand,'rtsp_port': port, 'cameraname': cameraname, 'plant': plant, 
                                    'area':area, 'imagename': rtsp_response_image['image_name'], 'image_height': rtsp_response_image['height'],
                                    'image_width': rtsp_response_image['width'], 'cameraid': None,'alarm_type': alarm_type, 'coin_details':None,'alarm_enable':alarm_enable,
                                    'alarm_ip_address': alarm_ip_address,'roi_data': [], 'tc_data': [],'cr_data': [], 'ppe_data': [],'camera_status': True, 
                                    'rtsp_url':rtsp_response, 'timestamp': now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}                                
                                    # print("CAME HERE ---dude $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ---- ")
                                    result = ppera_cameras.insert_one(final_data)
                                    if result.acknowledged:
                                        ret = {'success': True, 'message':'camera added successfully.'}
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
                    ret['message'] = 'entered ip is already exist, please go with edit roi option.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)

# @camera_coin.route('/add_camera_rtsp', methods=['POST'])
@csrf_exempt
def add_Acamera_rtsp(request):
    ret = {'success': False, 'message': 'something went wrong with add camera api with rtsp'}
    if request.method == "POST":
        data = json.loads(request.body)
        print("------------data------------",data)
        if data == None:
            data = {}
        request_key_array = ['camera_brand', 'plant', 'area', 'cameraname', 'rtsp_url', 'alarm_type', 'alarm_ip_address','coin_details','department','alarm_enable']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                # print("come 1")
                # print("output ===", output)
                # print("print(output ====), ",data)
                if len(output)==2 and ('alarm_ip_address' in output  and "alarm_type" in output) :
                    print("Hello sar ==== camera here for the functionally ----------------------" )
                    rtsp_url = data['rtsp_url']
                    department = data['department']
                    brand = data['camera_brand']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']
                    alarm_ip_address = data['alarm_ip_address']
                    alarm_enable= data['alarm_enable']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data = ppera_cameras.find_one({'rtsp_url': rtsp_url})
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
                                        image_namereplace = (replace_spl_char_panel_area_plant(plant   + '_' + area))
                                        rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                        if rtsp_response_image:
                                            final_data = {'department':department,
                                                'camera_ip': cameraip,'username': username, 'password': password, 'camera_brand': brand,'rtsp_port': port, 
                                                'cameraname':cameraname, 'plant': plant, 'area': area, 'imagename':rtsp_response_image['image_name'],
                                                'image_height': rtsp_response_image ['height'], 'image_width':rtsp_response_image['width'],'cameraid': None,
                                                'coin_details':None,'alarm_enable':alarm_enable,
                                                'alarm_type': alarm_type,'alarm_ip_address':alarm_ip_address, 'roi_data': [],'tc_data': [], 'cr_data': [],
                                                'ppe_data': [], 'camera_status': True, 'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': ai_solution,
                                                'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}   
                                            result = ppera_cameras.insert_one( final_data)
                                            if result.acknowledged:
                                                ret = {'success': True, 'message':'camera added successfully.'}
                                            else:
                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                        else:
                                            ret['message'] = 'rtsp stream is not working, please try once again.'
                                    else:
                                        ret['message'] = 'cameraip is not able ping.'
                                else:
                                    ret['message'] = 'camera password should not have any special characters.'
                            except Exception as error:
                                print('ERROR -message in checking camera rtsp', str  (error))
                                ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- add_camera_rtsp 1", str(error), " ----time ---- ", now_time_with_time()]))
                                image_namereplace = replace_spl_char_panel_area_plant(plant + '_' + area)
                                rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                if rtsp_response_image:
                                    final_data = {
                                        "department":department,
                                        'camera_ip': cameraip, 'username': username, 'password': password,'camera_brand': brand, 'rtsp_port': port,'cameraname': cameraname,
                                        'plant': plant,'area': area, 'imagename': rtsp_response_image['image_name'],
                                        'image_height': rtsp_response_image[ 'height'], 'image_width':rtsp_response_image['width'], 
                                        'coin_details':None,'alarm_enable':alarm_enable,
                                        'cameraid':None, 'alarm_type': alarm_type, 'alarm_ip_address': alarm_ip_address, 'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True, 
                                        'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id
                                        }
                                    result = ppera_cameras.insert_one(final_data)
                                    if result.acknowledged:
                                        ret = {'success': True, 'message': 'camera added successfully.'}
                                    else:
                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                else:
                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                        else:
                            ret['message'] = 'rtsp url error.'
                    else:
                        ret['message'] = 'entered ip is already exist, please go with edit roi option.'    
                elif len(output)==2 and ('coin_details' in output  and "alarm_type" in output):
                    rtsp_url = data['rtsp_url']
                    department = data['department']
                    brand = data['camera_brand']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']
                    alarm_ip_address = data['alarm_ip_address']
                    coin_details = data['coin_details']
                    alarm_enable= data['alarm_enable']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data = ppera_cameras.find_one({'rtsp_url': rtsp_url})
                    if alarm_type =='sensegiz':
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
                                            image_namereplace = (replace_spl_char_panel_area_plant(plant   + '_' + area))
                                            rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                            if rtsp_response_image:
                                                final_data = {'department':department,
                                                    'camera_ip': cameraip,'username': username, 'password': password,
                                                            'camera_brand': brand,'rtsp_port': port, 'cameraname':cameraname, 'plant': plant, 'area': area,
                                                            'imagename':rtsp_response_image['image_name'],'image_height': rtsp_response_image ['height'], 
                                                            'image_width':rtsp_response_image['width'],'cameraid': None, 'alarm_type': alarm_type, 'alarm_enable':alarm_enable,
                                                            'coin_details':coin_details,
                                                                'alarm_ip_address':None, 'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [],
                                                                'camera_status': True, 'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                                result = ppera_cameras.insert_one( final_data)
                                                if result.acknowledged:
                                                    ret = {'success': True, 'message':'camera added successfully.'}
                                                else:
                                                    ret['message'] = 'data is not inserted properly, please try once again.'
                                            else:
                                                ret['message'] = 'rtsp stream is not working, please try once again.'
                                        else:
                                            ret['message'] = 'cameraip is not able ping.'
                                    else:
                                        ret['message'] = 'camera password should not have any special characters.'
                                except Exception as error:
                                    print('ERROR -message in checking camera rtsp', str  (error))
                                    ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- add_camera_rtsp 2", str(error), " ----time ---- ", now_time_with_time()]))
                                    image_namereplace = replace_spl_char_panel_area_plant(plant + '_' + area)
                                    rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                    if rtsp_response_image:
                                        final_data = {"department":department,
                                            'camera_ip': cameraip, 'username': username, 'password': password,'camera_brand': brand, 'rtsp_port': port,'cameraname': cameraname,
                                                    'plant': plant,'area': area, 'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image[ 'height'], 
                                                    'image_width':rtsp_response_image['width'], 'cameraid':None, 'alarm_type': alarm_type, 'alarm_ip_address': None,'alarm_enable':alarm_enable,
                                                    'coin_details':coin_details,
                                                    'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True,  'rtsp_url': rtsp_url,
                                                    'timestamp':now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                        result = ppera_cameras.insert_one(final_data)
                                        if result.acknowledged:
                                            ret = {'success': True, 'message': 'camera added successfully.'}
                                        else:
                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                    else:
                                        ret['message'] = 'rtsp stream is not working, please try once again.'
                            else:
                                ret['message'] = 'rtsp url error.'
                        else:
                            ret['message'] = 'entered ip is already exist, please go with edit roi option.' 
                    else:
                        ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ])       
                elif len(output)==1 and ('alarm_ip_address' in output  or "alarm_type" in output) :
                    rtsp_url = data['rtsp_url']
                    department = data['department']
                    brand = data['camera_brand']
                    plant = data['plant']
                    area = data['area']
                    cameraname = data['cameraname']
                    alarm_type = data['alarm_type']                
                    alarm_enable =data['alarm_enable']
                    ai_solution = data['ai_solution']
                    genetic_id = None
                    if 'genetic_id' in data :
                        genetic_id = data['genetic_id']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    find_data = ppera_cameras.find_one({'rtsp_url': rtsp_url})
                    if alarm_type != 'sensegiz':
                        alarm_ip_address = data['alarm_ip_address']
                        if alarm_type in ['hooter','relay']:
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
                                                image_namereplace = ( replace_spl_char_panel_area_plant(plant + '_' + area))
                                                rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                                if rtsp_response_image:
                                                    final_data = {'department':department,
                                                        'camera_ip': cameraip,'username': username, 'password': password, 'camera_brand': brand,'rtsp_port': port, 
                                                                'cameraname':     cameraname, 'plant': plant, 'area': area,
                                                                'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'], 
                                                                'image_width': rtsp_response_image['width'],'cameraid': None,
                                                                'alarm_type': alarm_type, 'alarm_ip_address': alarm_ip_address,'alarm_enable':alarm_enable,
                                                                'coin_details':None,
                                                                'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [], 'camera_status': True,
                                                                'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                                    result = ppera_cameras.insert_one( final_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message': 'camera added successfully.'}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message'] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    except Exception as error:
                                        print('ERROR -message in checking camera rtsp', str (error))
                                        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- add_camera_rtsp 3", str(error), " ----time ---- ", now_time_with_time()]))
                                        image_namereplace = replace_spl_char_panel_area_plant( plant + '_' + area)
                                        rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                        if rtsp_response_image:
                                            final_data = {"department":department,
                                                'camera_ip': cameraip, 'username': username, 'password': password,'camera_brand': brand,'rtsp_port': port,'cameraname': cameraname, 'plant': plant,'area': area, 
                                                        'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'],'image_width':rtsp_response_image['width'], 'cameraid': None, 'alarm_type': alarm_type,
                                                        'alarm_enable':alarm_enable,'alarm_ip_address': alarm_ip_address, 'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True,
                                                        'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                            result = ppera_cameras.insert_one(final_data)
                                            if result.acknowledged:
                                                ret = {'success': True, 'message': 'camera added successfully.'}
                                            else:
                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                        else:
                                            ret['message'] = 'rtsp stream is not working, please try once again.'
                                else:
                                    ret['message'] = 'rtsp url error.'
                            else:
                                ret['message'] = 'entered ip is already exist, please go with edit roi option.'  
                        else:
                            ret['message']="please check spelling of alarm type, try once again."
                    elif alarm_type == 'sensegiz'   :
                        ai_solution = data['ai_solution']
                        coin_details = data['coin_details']
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
                                            image_namereplace = ( replace_spl_char_panel_area_plant(plant + '_' + area))
                                            rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                            if rtsp_response_image:
                                                final_data = {"department":department,
                                                    'camera_ip': cameraip,'username': username, 'password': password, 'camera_brand': brand,'rtsp_port': port, 'cameraname':     cameraname, 'plant': plant, 'area': area,
                                                            'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'], 
                                                            'image_width': rtsp_response_image['width'],'cameraid': None, 'alarm_type': alarm_type, 'alarm_ip_address': None,'alarm_enable':alarm_enable,
                                                            'coin_details':coin_details,
                                                            'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [], 'camera_status': True, 
                                                            'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                                result = ppera_cameras.insert_one( final_data)
                                                if result.acknowledged:
                                                    ret = {'success': True, 'message': 'camera added successfully.'}
                                                else:
                                                    ret['message'] = 'data is not inserted properly, please try once again.'
                                            else:
                                                ret['message'] = 'rtsp stream is not working, please try once again.'
                                        else:
                                            ret['message'] = 'cameraip is not able ping.'
                                    else:
                                        ret['message'] = 'camera password should not have any special characters.'
                                except Exception as error:
                                    print('ERROR -message in checking camera rtsp', str (error))
                                    ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- add_camera_rtsp 4", str(error), " ----time ---- ", now_time_with_time()]))
                                    image_namereplace = replace_spl_char_panel_area_plant( plant + '_' + area)
                                    rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                    if rtsp_response_image:
                                        final_data = {"department":department,
                                            'camera_ip': cameraip, 'username': username, 'password': password,'camera_brand': brand,'rtsp_port': port,'cameraname': cameraname, 'plant': plant,'area': area, 
                                                    'imagename': rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'],'image_width':rtsp_response_image['width'], 'cameraid': None, 'alarm_type': alarm_type,
                                                    'alarm_enable':alarm_enable,
                                                    'coin_details':coin_details,'alarm_ip_address': None, 'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True,
                                                    'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                        result = ppera_cameras.insert_one(final_data)
                                        if result.acknowledged:
                                            ret = {'success': True, 'message': 'camera added successfully.'}
                                        else:
                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                    else:
                                        ret['message'] = 'rtsp stream is not working, please try once again.'
                            else:
                                ret['message'] = 'rtsp url error.'
                        else:
                            ret['message'] = 'entered ip is already exist, please go with edit roi option.'
                else:
                    ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                rtsp_url = data['rtsp_url']
                department = data['department']
                brand = data['camera_brand']
                plant = data['plant']
                area = data['area']
                cameraname = data['cameraname']
                alarm_type = data['alarm_type']
                alarm_ip_address = data['alarm_ip_address']
                alarm_enable = data['alarm_enable']
                ai_solution = data['ai_solution']
                genetic_id = None
                if 'genetic_id' in data :
                    genetic_id = data['genetic_id']
                regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                find_data = ppera_cameras.find_one({'rtsp_url': rtsp_url})
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
                                    image_namereplace = (replace_spl_char_panel_area_plant(plant+ '_' + area))
                                    rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                                    if rtsp_response_image:
                                        final_data = {'department':department,
                                            'camera_ip': cameraip,'username': username, 'password':     password, 'camera_brand': brand,'rtsp_port': port,'cameraname':cameraname, 'plant': plant, 'area': area,
                                                    'imagename':rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'],
                                                    'image_width': rtsp_response_image['width'],'cameraid': None, 'alarm_type':alarm_type, 'alarm_ip_address': alarm_ip_address, 'coin_details':None,'alarm_enable':alarm_enable,
                                                    'roi_data': [],'tc_data': [], 'cr_data': [],'ppe_data': [], 'camera_status':True, 'rtsp_url': rtsp_url,'timestamp': now_time_with_time(),
                                                    'ai_solution':ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                        result = ppera_cameras.insert_one(final_data)
                                        if result.acknowledged:
                                            ret = {'success': True, 'message':'camera added successfully.'}
                                        else:
                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                    else:
                                        ret['message'] = 'rtsp stream is not working, please try once again.'
                                else:
                                    ret['message'] = 'cameraip is not able ping.'
                            else:
                                ret['message'] = 'camera password should not have any special characters.'
                        except Exception as error:
                            print('ERROR -message in checking camera rtsp', str(error))
                            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- add_camera_rtsp 5", str(error), " ----time ---- ", now_time_with_time()]))
                            image_namereplace = replace_spl_char_panel_area_plant(plant + '_' + area)
                            rtsp_response_image = verify_rtsp(rtsp_url,image_namereplace)
                            if rtsp_response_image:
                                final_data = {"department":department,
                                    'camera_ip': cameraip, 'username':  username, 'password': password,'camera_brand': brand, 'rtsp_port': port,'cameraname': cameraname, 'plant': plant,'area': area,
                                            'imagename':rtsp_response_image['image_name'],'image_height': rtsp_response_image['height'], 'image_width':rtsp_response_image['width'], 'cameraid':None, 
                                            'alarm_type': alarm_type, 'alarm_ip_address': alarm_ip_address,'coin_details':None,'alarm_enable':alarm_enable,
                                            'roi_data': [], 'tc_data': [], 'cr_data': [], 'ppe_data': [], 'camera_status': True, 
                                            'rtsp_url': rtsp_url, 'timestamp':now_time_with_time(), 'ai_solution': ai_solution,'analytics_status':'false','alarm_version':{'hooter':None,'relay':None},'genetic_id':genetic_id}
                                result = ppera_cameras.insert_one(final_data)
                                if result.acknowledged:
                                    ret = {'success': True, 'message':'camera added successfully.'}
                                else:
                                    ret['message'] = 'data is not inserted properly, please try once again.'
                            else:
                                ret['message'] = 'rtsp stream is not working, please try once again.'
                    else:
                        ret['message'] = 'rtsp url error.'
                else:
                    ret['message'] = 'entered ip is already exist, please go with edit roi option.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)

