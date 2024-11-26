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

def checkwhichdictionarykeyvaluesChanged(requestdata, finddata):
    changed_values = {}  
    for key in finddata:
        if key in requestdata and finddata[key] != requestdata[key]:
            changed_values[key] =  requestdata[key]
    print("Changed values:")
    for key, value1 in changed_values.items():
        print(f"Key: {key},  New Value: {value1}")
    return changed_values

def checkdictionarfortruevaluesonly(dictionary,dataobject):
    print("dictionary===data==",dictionary)
    print("--------------dataobject---------",dataobject)
    updatestatus = False
    for aidatakey, aidatavalue in dictionary.items():
        print("aisolutionkeyvalues ==",aidatakey)
        if aidatavalue:
            # print('-----------aidatavalue----,kye---------',aidatavalue,aidatakey)
            if aidatakey=="PPE" :
                # print('-----------aidatavalue-------------',aidatavalue,aidatakey)
                print('---------------------')
                if len(dataobject['ppe_data']) != 0:
                    if dataobject['ppe_data'][0]['helmet'] != False or dataobject['ppe_data'][0]['vest'] != False or dataobject['ppe_data'][0]['crash_helmet'] != False:
                        updatestatus=True                        
            elif aidatakey=="RA" :
                if len(dataobject['roi_data']) != 0:
                    for x in dataobject['roi_data']:
                        if 'analyticstype' in x :
                            if x['analyticstype'] == 0:
                                updatestatus=True  
                                break 
                        elif len(x['bb_box']) !=0:
                            updatestatus=True
                            break
            elif aidatakey=="CR" :
                if len(dataobject['cr_data']) != 0:
                    updatestatus=True
            elif aidatakey=="TC" :
                if len(dataobject['tc_data']) != 0:
                    updatestatus=True
            elif aidatakey=="fire" :
                if isEmpty(dataobject['firesmoke_data']):
                    print('--------------firesmoke_data-----------',dataobject['firesmoke_data'])
                    if len(dataobject['firesmoke_data']['roi_parameters']) !=0:
                        updatestatus=True
                # if len(dataobject['firesmoke_data']) != 0:
                    # if dataobject['firesmoke_data'][0]['fire'] != False or dataobject['firesmoke_data'][0]['smoke'] != False:
                        # updatestatus=True                        
            elif aidatakey=="smoke" :
                if isEmpty(dataobject['firesmoke_data']):
                    if len(dataobject['firesmoke_data']['roi_parameters']) !=0:
                        updatestatus=True
                # if len(dataobject['firesmoke_data']) != 0:
                #     if dataobject['firesmoke_data'][0]['fire'] != False or dataobject['firesmoke_data'][0]['smoke'] != False:
                #         updatestatus=True
            elif aidatakey=="dust" :
                if isEmpty(dataobject['firesmoke_data']):
                    if len(dataobject['firesmoke_data']['roi_parameters']) !=0:
                        updatestatus=True
                # if len(dataobject['firesmoke_data']) != 0:
                #     if dataobject['firesmoke_data'][0]['dust'] != False :
                #         updatestatus=True
            elif aidatakey=="Parking" :
                if 'vpms_data' in dataobject.keys():
                    if len(dataobject['vpms_data']) != 0:
                        for x in dataobject['vpms_data']:
                            if x['parking_type'] == 'parking': 
                                updatestatus=True
                                break
                            
            elif aidatakey=="NO_Parking" :
                if 'vpms_data' in dataobject.keys():
                    if len(dataobject['vpms_data']) != 0:
                        for x in dataobject['vpms_data']:
                            if x['parking_type'] == 'no-parking': 
                                updatestatus=True
                                break
            elif aidatakey=="Traffic_Jam" :
                if len(dataobject['trafficjam_data']) != 0:
                    updatestatus=True
            elif aidatakey=="spillage" :
                if len(dataobject['spillage_roi_data']) != 0:
                    updatestatus=True
            elif aidatakey=="Protection_Zone":
                if len(dataobject['roi_data']) != 0:
                    for x in dataobject['roi_data']:
                        if 'analyticstype' in x :
                            if x['analyticstype'] == 2: 
                                updatestatus=True
                                break

            elif aidatakey=="POC":
                if 'poc' in dataobject:
                    print("dataobject['POC']:------------", dataobject['poc'])
                    poc_data_details = dataobject['poc']
                    if len(poc_data_details) != 0:
                        print("------------11")
                        if 'wheel_count' in poc_data_details:
                            print("------------222")
                            if len(poc_data_details['wheel_count']) != 0:
                                print("------------33")
                                updatestatus=True
    return updatestatus   

def remove_relayhooterDetailsinROi(inputdata, fetecheddata):
    # print("----------------------")
    # print("---------inputdata--------",inputdata)
    Newdataforupdate = []
    #'alarm_ip_address': {'hooter_ip': '10.11.1.162', 'relay_ip': '10.11.1.163'}, 'alarm_version': {'hooter': 'type2', 'relay': 'type1'
    if 'alarm_ip_address' in inputdata:
        if inputdata['alarm_ip_address'] is not None:
            if 'hooter_ip' in inputdata['alarm_ip_address'] and 'relay_ip' in inputdata['alarm_ip_address']:
                # print('------1-1--------',inputdata['alarm_ip_address']['hooter_ip'])
                if 'roi_data' in fetecheddata:                    
                    for newindex , newvalue in enumerate(fetecheddata['roi_data']):
                        SetnewValue = newvalue
                        # print("-----------------newvalue---",newvalue)
                        if 'alarm_type' in newvalue:
                            if newvalue['alarm_type'] is not None:
                                if 'hooter' in newvalue['alarm_type']:
                                    # print('-------newvalue------alarm_type-----',newvalue['alarm_type'])
                                    # print("inputdata['alarm_ip_address']['hooter_ip']---------",inputdata['alarm_ip_address']['hooter_ip'])
                                    if inputdata['alarm_ip_address']['hooter_ip'] == None:
                                        if newvalue['alarm_type']['hooter']:
                                            # print('------')
                                            SetnewValue['alarm_type']['hooter'] = False
                                            SetnewValue['alarm_ip_address']['hooter_ip']= None

                                    # print("SetnewValue=====hooter=========",SetnewValue)
                                    # print()
                                if 'relay' in newvalue['alarm_type']:
                                    # print('-------newvalue------alarm_type-----',newvalue['alarm_type'])
                                    # print("inputdata['alarm_ip_address']['hooter_ip']---------",inputdata['alarm_ip_address']['relay_ip'])
                                    
                                    if inputdata['alarm_ip_address']['relay_ip'] == None:
                                        if newvalue['alarm_type']['relay']:
                                            SetnewValue['alarm_type']['relay'] = False
                                            SetnewValue['alarm_ip_address']['relay_ip']= None

                                    # print("SetnewValue=====hooter=========",SetnewValue)
                                    # print()
                                Newdataforupdate.append(SetnewValue)
            elif 'hooter_ip' in inputdata['alarm_ip_address']:
                print('-------1-2------',inputdata['alarm_ip_address']['hooter_ip'])
                if 'roi_data' in fetecheddata:                    
                    for newindex , newvalue in enumerate(fetecheddata['roi_data']):
                        SetnewValue = newvalue
                        if 'alarm_type' in newvalue:
                            if newvalue['alarm_type'] is not None:
                                if 'hooter' in newvalue['alarm_type']:
                                    if inputdata['alarm_ip_address']['hooter_ip'] == None:
                                        if newvalue['alarm_type']['hooter']:
                                            SetnewValue['alarm_type']['hooter'] = False
                                            SetnewValue['alarm_ip_address']['hooter_ip']= None
                                if 'relay' in newvalue['alarm_type']:                                    
                                    if inputdata['alarm_ip_address']['relay_ip'] == None:
                                        if newvalue['alarm_type']['relay']:
                                            SetnewValue['alarm_type']['relay'] = False
                                            SetnewValue['alarm_ip_address']['relay_ip']= None
                                Newdataforupdate.append(SetnewValue)
            elif 'relay_ip' in inputdata['alarm_ip_address']:
                print('------1-3-------',inputdata['alarm_ip_address']['relay_ip'])  
                if 'roi_data' in fetecheddata:                    
                    for newindex , newvalue in enumerate(fetecheddata['roi_data']):
                        SetnewValue = newvalue
                        if 'alarm_type' in newvalue:
                            if newvalue['alarm_type'] is not None:
                                if 'hooter' in newvalue['alarm_type']:
                                    if inputdata['alarm_ip_address']['hooter_ip'] == None:
                                        if newvalue['alarm_type']['hooter']:
                                            SetnewValue['alarm_type']['hooter'] = False
                                            SetnewValue['alarm_ip_address']['hooter_ip']= None
                                if 'relay' in newvalue['alarm_type']:                                    
                                    if inputdata['alarm_ip_address']['relay_ip'] == None:
                                        if newvalue['alarm_type']['relay']:
                                            SetnewValue['alarm_type']['relay'] = False
                                            SetnewValue['alarm_ip_address']['relay_ip']= None
                                Newdataforupdate.append(SetnewValue)
    # print("------------Newdataforupdate-----------",Newdataforupdate)
    # print("------------Fetcheddata-----------",fetecheddata['roi_data'])
    # print("-------------------===Campare list status===================",compare_lists(fetecheddata['roi_data'], Newdataforupdate))   
    return Newdataforupdate  

def compare_lists(list1, list2):
    if len(list1) != len(list2):
        print(f"Different list lengths: {len(list1)} != {len(list2)}")
        return False

    identical = True
    for index, (dict1, dict2) in enumerate(zip(list1, list2)):
        differences = compare_dicts(dict1, dict2)
        if differences:
            identical = False
            print(f"Differences found in item {index}:")
            for key, value1, value2 in differences:
                print(f" - Key '{key}': '{value1}' != '{value2}'")

    return identical

def fetch_preset_value(listdata , coinid):
    # coin_details
    presetid = None
    returnvalues = [x for x in listdata if x['coin_id']== coinid]
    print("returnvalues", returnvalues)
    if len(returnvalues) !=0 and len(returnvalues)==1 :
        presetid= returnvalues[0]['preset_id']
    return presetid

def record_log_store_in(data):
    print("hello data ")
    print("log data === ", data)
    ret = {"message":"record queue is max limit for this camera","success":False}
    found_data_count = mongo.db.record_log.count_documents({'timestamp':{'$regex': '^' + str(date.today())},"camera_ip":data['camera_ip'],'cameraname':data['cameraname'],'camera_rtsp':data['camera_rtsp'],'record_status': 0})#.count()
    # data_count=found_data_count.count()
    print("count of found log data element===", found_data_count)
    if found_data_count < 3 :
        print("count of found log data element===", found_data_count)
        data_found_for_coin = mongo.db.record_log.find_one({'timestamp':{'$regex': '^' + str(date.today())},"camera_ip":data['camera_ip'],'cameraname':data['cameraname'],'camera_rtsp':data['camera_rtsp'],'duration':data['duration'],'coinid':data['coinid'],"cameraid":data['cameraid'],'record_status': 0})
        if data_found_for_coin is  None or  data_found_for_coin is not None :
            print("data not found for coin")
            result = mongo.db.record_log.insert_one(data)
            if result.acknowledged:
                ret= {'message':"violation data added to queue successfully",'success':True}
            else:
                ret['message'] = 'data is not inserted properly, please try once again.'
        else:
            ret['message']="for this coinid already recording is going on."
    else:
        ret['message']="record queue is max limit for this camera."
    return ret

def check_coin_voilation_data(insertion_data):
    insertion_status = False 
    ret = {"message":"something went wrong with insertion of coinid voilation data","error_status":False,"success":False}
    try:
        conn = psycopg2.connect(user = "docketrun",password = "docketrun", host = "localhost",port = "5432",database = "docketrundb", sslmode="disable")
    except Exception as  error:
        print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - CONNECT", error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- smartrecordTABLECRATION CONNECT 2", str(error), " ----time ---- ", now_time_with_time()]))
        ret['error_status']=True
        ret['message']=str(error)
        conn = 0
    if conn:
        cursor = conn.cursor()
        SELECTQUERY = "SELECT * FROM smrec WHERE datauploadstatus = 0 or datauploadstatus = 1 " + "and  cameraid = '"+str(insertion_data['cameraid'])+ "' and  camera_name = '" + str(insertion_data['cameraname'] )+"'"
        print("SELECTQUERY=== ", SELECTQUERY)
        cursor.execute(SELECTQUERY)
        result =  cursor.fetchone()#fetchall()
        if result is None:
            postgres_insert_query = """insert into smrec (cameraid, camera_name, datauploadstatus, duration, coinid)   values (%s,%s,%s,%s,%s)"""
            #insert into smrec( cameraid, camera_name, datauploadstatus, duration, coinid ) VALUES ( '1', 'cam_1', 0, '200','coin1' );
            record_to_insert = ( str(insertion_data['cameraid']),str(insertion_data['cameraname']),str(insertion_data['datauploadstatus']),str(insertion_data['duration']) ,str(insertion_data['coinid']))
            # try:
            #     cursor.execute('UPDATE tsk_riro SET datauploadstatus=13 WHERE datauploadstatus=12 OR datauploadstatus=11;')
            #     # print("updated")
            # except Exception as  error:
            #     print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - UPDATE", error)
            # ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- smartrecordTABLECRATION update 2", str(error), " ----time ---- ", now_time_with_time()]))
            # print(postgres_insert_query, record_to_insert)
            # cursor.execute(postgres_insert_query, record_to_insert)
            # conn.commit()
            # creation_query = cursor.rowcount 
            # if creation_query > 0 :
            # print("creation_query ", creation_query)
            print("data inserted successfully .")
            ret['message'] = "voilation data not there please ."
            ret['success'] = True
            insertion_status = True
        else:
            print("already recording data exist for this coinid of camera")
            ret['message']= "already recording data exist for this coinid of camera."
        conn.close()
    return ret


def HIFOCUSPTZROTATEPRESET(cameraip,presetid):
    ret = {"message":"something went wrong with HIFOCUSPTZROTATEPRESET function===", "success":False}
    if cameraip is not None and presetid is not None:
        url = "http://"+str(cameraip)+"/LAPI/V1.0/Channel/0/PTZ/Presets/"+str(presetid)+"/Goto"
        print(url)
        try:
            r = requests.put(url,timeout=2)#('http://192.168.1.13/LAPI/V1.0/Channel/0/PTZ/Presets/3/Goto')
            if r is not None and r.status_code == 200:
                response_data = r.json()
                if response_data is not None:
                    print("RESPONSE ===", response_data)
                    response = response_data['Response']
                    print("response_data['ResponseString']",response['ResponseString'])
                    print("response_data['StatusString']",response['StatusString'])
                    print("response_data['StatusCode']",response['StatusCode'])
                    print("CreatedID ====", response['CreatedID'])
                    if response['StatusCode'] ==0 and response['StatusString'] =='Succeed' and response['ResponseString'] =='Succeed' and response['CreatedID']==-1 and response['ResponseCode']==0:
                        ret = {"message": "Camera is rotate for given coin id location", "success": True}
                    else:
                        ret = {"message": "camera was not able to rotate, to given coin id, please check is camera is working or not.", "success": False}
            else :
                ret = {"message": "camera url has given none response, please check is camera is working or not.", "success": False}
        except requests.exceptions.HTTPError as error :
            ret['message'] =" ".join(["request HTTPError ==  ", str(error)]) 
        except requests.exceptions.Timeout as error :
            ret['message'] = " ".join(["request timeout ==  ", str(error)])
        except requests.exceptions.ConnectionError as error:
            ret['message'] =" ".join(["request ConnectionError == ==  ", str(error)])
        except requests.exceptions.TooManyRedirects as error :
            ret['message'] =" ".join(["request TooManyRedirects == ", str(error)]) 
        except requests.exceptions.RequestException  as error : 
            ret['message'] =" ".join(["request RequestException == ", str(error)])  
    else:
        ret["message"] ="preset angle id is None or ip is None, please check and try" 
    return ret

def smartrecordTABLECRATION():
    tablecreationstatus = False 
    #CREATE TABLE IF NOT EXISTS smrec( id SERIAL PRIMARY KEY, date DATE NOT NULL DEFAULT CURRENT_DATE, cameraid text, camera_name text, duration text, video_name text, datauploadstatus integer );
    #"create table smrec( id SERIAL PRIMARY KEY, date DATE NOT NULL DEFAULT CURRENT_DATE, cameraid text, camera_name text, duration text, video_name text, datauploadstatus integer );"
    try:
        conn = psycopg2.connect(user = "docketrun",password = "docketrun", host = "localhost",port = "5432",database = "docketrundb", sslmode="disable")
    except Exception as  error:
        print("[ERR] smartrecordTABLECRATION - CONNECT", error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- smartrecordTABLECRATION CONNECT 3", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0

    if conn:
        cursor = conn.cursor()
        try:
            query = 'CREATE TABLE IF NOT EXISTS smrec( id SERIAL PRIMARY KEY, date DATE NOT NULL DEFAULT CURRENT_DATE, cameraid text, camera_name text, duration text, video_name text, coinID text, datauploadstatus integer );'
            cursor.execute(query) 
            conn.commit()
            # print("cursor === rowcount === ",cursor.rowcount)
            creation_query = cursor.rowcount 
            if creation_query == -1 :
                tablecreationstatus = True
                print("smrecord table successfully created.")
            else:
                print("smrecord table is not created.")
            # cursor.execute('UPDATE tsk_riro SET datauploadstatus=13 WHERE datauploadstatus=12 OR datauploadstatus=11;')
            # print("updated")
        except Exception as  error:
            print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - UPDATE", error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- smartrecordTABLECRATION UPDATE 1", str(error), " ----time ---- ", now_time_with_time()]))
        # conn.commit()
        conn.close()
    return tablecreationstatus


def insert_coin_voilation_data(insertion_data):
    insertion_status = False 
    ret = {"message":"something went wrong with insertion of coinid voilation data","error_status":False,"success":False}
    try:
        conn = psycopg2.connect(user = "docketrun",password = "docketrun", host = "localhost",port = "5432",database = "docketrundb", sslmode="disable")
    except Exception as  error:
        print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - CONNECT", error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- smartrecordTABLECRATION CONNECT 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['error_status']=True
        ret['message']=str(error)
        conn = 0
    if conn:
        cursor = conn.cursor()
        SELECTQUERY = "SELECT * FROM smrec WHERE datauploadstatus = 0 or datauploadstatus = 1 " + "and  cameraid = '"+str(insertion_data['cameraid'])+ "' and  camera_name = '" + str(insertion_data['cameraname'] )+"'"
        print("SELECTQUERY=== ", SELECTQUERY)
        cursor.execute(SELECTQUERY)
        result =  cursor.fetchone()#fetchall()
        if result is None:
            postgres_insert_query = """insert into smrec (cameraid, camera_name, datauploadstatus, duration, coinid)   values (%s,%s,%s,%s,%s)"""
            #insert into smrec( cameraid, camera_name, datauploadstatus, duration, coinid ) VALUES ( '1', 'cam_1', 0, '200','coin1' );
            record_to_insert = ( str(insertion_data['cameraid']),str(insertion_data['cameraname']),str(insertion_data['datauploadstatus']),str(insertion_data['duration']) ,str(insertion_data['coinid']))
            # try:
            #     cursor.execute('UPDATE tsk_riro SET datauploadstatus=13 WHERE datauploadstatus=12 OR datauploadstatus=11;')
            #     # print("updated")
            # except Exception as  error:
            #     print("[ERR] reset_tsk_riro_table_dataupload_12_to_13 - UPDATE", error)
            # ERRORLOGdata(" ".join(["\n", "[ERROR] camera_coin_apis -- smartrecordTABLECRATION 1", str(error), " ----time ---- ", now_time_with_time()]))
            print(postgres_insert_query, record_to_insert)
            cursor.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            creation_query = cursor.rowcount 
            if creation_query > 0 :
                print("creation_query ", creation_query)
                print("data inserted successfully .")
                ret['message'] = "voilation data inserted successfully."
                ret['success'] = True
                insertion_status = True
            else:
                print("data is not inserted.")
                ret['message'] = "data is not inserted."
        else:
            print("already recording data exist for this coinid of camera")
            ret['message']= "already recording data exist for this coinid of camera."
        conn.close()
    return ret


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


#26/11/2024

# @camera_coin.route("/edit_camera",methods=['POST'])
@csrf_exempt
def editCAM(request):
    ret={"success":False,"message":"something went wrong with edit api."}
    if request.method == "POST":
        data = json.loads(request.body)
        if data is  None:
            data = {}
        if isEmpty(data):
            print("-----------------data-------Requestdata------Edit camera------",data)
            datakeys = list(data.keys())
            request_key_array1 = [ 'id','plant', 'area', 'cameraname', 'alarm_type', 'alarm_ip_address','coin_details','department','alarm_enable','ai_solution','alarm_version','genetic_id']
            check1 =  all(item in request_key_array1 for item in datakeys)
            Request_key_array2 = ['ai_solution', 'alarm_enable', 'alarm_ip_address', 'alarm_type', 'alarm_version', 'area', 'cameraname', 'department', 'genetic_id', 'plant', 'trafficjam_data', 'vpms_data', 'id']
            Check2 = all(item in Request_key_array2 for item in datakeys)        
            if check1:
                output = [k for k, v in data.items() if v == '']
                if output:
                    if len(output) ==1 and 'genetic_id' in output:
                        finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                        if finddata is not None: 
                            id = data['id']
                            print("data =keys ",list(data.keys()))
                            # print('----------------------data----------------------edit camera----------',data)
                            if 'ai_solution' in data:
                                print("====ai_solutions",data['ai_solution'])
                                print("found_ai solutions",finddata['ai_solution'])
                                if 'roi_data' in data:
                                    del data['roi_data']
                                if 'tc_data' in data:
                                    del data['tc_data']
                                if 'cr_data' in data:
                                    del data['cr_data']
                                if 'ppe_data' in data:
                                    del data['ppe_data']
                                if 'vpms_data' in data:
                                    del data['vpms_data']
                                if 'trafficjam_data' in data:
                                    del data['trafficjam_data']
                                if (finddata['ai_solution']==data['ai_solution']) != True:
                                    print("finddata['ai_solution']=====checking both dictionaries are equal===",finddata['ai_solution']==data['ai_solution'])
                                    returnvalue=checkwhichdictionarykeyvaluesChanged(data['ai_solution'],finddata['ai_solution'])
                                    print("returnvalue===",returnvalue)
                                    has_true_value = any(value for value in returnvalue.values())
                                    if has_true_value:    
                                        print("updatestatus==5=",checkdictionarfortruevaluesonly(returnvalue,finddata)   ) 
                                        if checkdictionarfortruevaluesonly(returnvalue,finddata)  : 
                                            if '_id' in data:
                                                del data['id']
                                            contains_false = all(value is False for value in data['ai_solution'].values())
                                            if contains_false:
                                                data['analytics_status']='false'
                                            print("-----------------------hooterrelay test1.0--")
                                            NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                            ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                            # print("--------------------------ReturnValueOFHooterrelay--------------",ReturnValueOFHooterrelay)
                                            data['roi_data'] =NEwROIDATA
                                            result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                            if result.modified_count > 0:
                                                ret = {'message': 'camera details edited successfully.','success': True}
                                            else:
                                                ret['message'] = 'camera details not edited, please try once again.'
                                        else:
                                            ret['message'] = 'there is no data found ai solution enabled, please add data in camera setting page then try again.'
                                    else:
                                        if '_id' in data:
                                            del data['id']
                                        contains_false = all(value is False for value in data['ai_solution'].values())
                                        if contains_false:
                                            data['analytics_status']='false'
                                        print("-----------------------hooterrelay test1.1--")
                                        NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                        ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                        # print("--------------------------ReturnValueOFHooterrelay--------------",ReturnValueOFHooterrelay)
                                        data['roi_data'] =NEwROIDATA
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                        if result.modified_count > 0:
                                            ret = {'message': 'camera details edited successfully.','success': True}
                                        else:
                                            ret['message'] = 'camera details not edited, please try once again.'                                
                                else:
                                    if '_id' in data:
                                        del data['id']
                                    contains_false = all(value is False for value in data['ai_solution'].values())
                                    if contains_false:
                                        data['analytics_status']='false'
                                    print("-----------------------hooterrelay test1.2--")
                                    NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                    ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                    data['roi_data'] =NEwROIDATA
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                    if result.modified_count > 0:
                                        ret = {'message': 'camera details edited successfully.','success': True}
                                    else:
                                        ret['message'] = 'camera details not edited, please try once again.'
                            else:
                                if '_id' in data:
                                    del data['id']
                                if 'roi_data' in data:
                                    del data['roi_data']
                                if 'tc_data' in data:
                                    del data['tc_data']
                                if 'cr_data' in data:
                                    del data['cr_data']
                                if 'ppe_data' in data:
                                    del data['ppe_data']
                                if 'vpms_data' in data:
                                    del data['vpms_data']
                                if 'trafficjam_data' in data:
                                    del data['trafficjam_data']
                                # contains_false = all(value is False for value in data['ai_solution'].values())
                                # if contains_false:
                                #     data['analytics_status']='false'
                                print("-----------------------hooterrelay test1.3--")
                                NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                data['roi_data'] =NEwROIDATA
                                result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                if result.modified_count > 0:
                                    ret = {'message': 'camera details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'camera details not edited, please try once again.'
                        else:
                            ret['message']='camera details is not found for given id.'
                    else:
                        ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                    if finddata is not None: 
                        id = data['id']
                        print("data =keys ",list(data.keys()))
                        if 'roi_data' in data:
                            del data['roi_data']
                        if 'tc_data' in data:
                            del data['tc_data']
                        if 'cr_data' in data:
                            del data['cr_data']
                        if 'ppe_data' in data:
                            del data['ppe_data']
                        if 'vpms_data' in data:
                            del data['vpms_data']
                        if 'trafficjam_data' in data:
                            del data['trafficjam_data']
                        # print('----------------------data----------------------edit camera----------',data)
                        if 'ai_solution' in data:
                            print("====ai_solutions",data['ai_solution'])
                            print("found_ai solutions",finddata['ai_solution'])
                            if (finddata['ai_solution']==data['ai_solution']) != True:
                                print("finddata['ai_solution']=====checking both dictionaries are equal===",finddata['ai_solution']==data['ai_solution'])
                                returnvalue=checkwhichdictionarykeyvaluesChanged(data['ai_solution'],finddata['ai_solution'])
                                print("returnvalue===",returnvalue)
                                has_true_value = any(value for value in returnvalue.values())
                                if has_true_value:    
                                    print("updatestatus==1=",checkdictionarfortruevaluesonly(returnvalue,finddata)   ) 
                                    if checkdictionarfortruevaluesonly(returnvalue,finddata)  : 
                                        if '_id' in data:
                                            del data['id']
                                        contains_false = all(value is False for value in data['ai_solution'].values())
                                        if contains_false:
                                            data['analytics_status']='false'
                                        print("-----------------------hooterrelay test1.4--")
                                        NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                        ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                        data['roi_data'] =NEwROIDATA
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                        if result.modified_count > 0:
                                            ret = {'message': 'camera details edited successfully.','success': True}
                                        else:
                                            ret['message'] = 'camera details not edited, please try once again.'
                                    else:
                                        ret['message'] = 'there is no data found ai solution enabled, please add data in camera setting page then try again.'
                                else:
                                    if '_id' in data:
                                        del data['id']
                                    contains_false = all(value is False for value in data['ai_solution'].values())
                                    if contains_false:
                                        data['analytics_status']='false'
                                    print("-----------------------hooterrelay test1.5--")
                                    NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                    ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                    data['roi_data'] =NEwROIDATA
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                    if result.modified_count > 0:
                                        ret = {'message': 'camera details edited successfully.','success': True}
                                    else:
                                        ret['message'] = 'camera details not edited, please try once again.'                                
                            else:
                                if '_id' in data:
                                    del data['id']
                                contains_false = all(value is False for value in data['ai_solution'].values())
                                if contains_false:
                                    data['analytics_status']='false'

                                print("-----------------------hooterrelay test1.6--")
                                NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                data['roi_data'] =NEwROIDATA
                                result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                if result.modified_count > 0:
                                    ret = {'message': 'camera details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'camera details not edited, please try once again.'
                        else:
                            if '_id' in data:
                                del data['id']
                            # contains_false = all(value is False for value in data['ai_solution'].values())
                            # if contains_false:
                            #     data['analytics_status']='false'
                            print("-----------------------hooterrelay test1.7--")
                            NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                            ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                            data['roi_data'] =NEwROIDATA
                            result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                            if result.modified_count > 0:
                                ret = {'message': 'camera details edited successfully.','success': True}
                            else:
                                ret['message'] = 'camera details not edited, please try once again.' 
                    else:
                        ret['message']='camera details is not found for given id.'

            elif Check2:
                output = [k for k, v in data.items() if v == '']
                if output:
                    if 'roi_data' in data:
                        del data['roi_data']
                    if 'tc_data' in data:
                        del data['tc_data']
                    if 'cr_data' in data:
                        del data['cr_data']
                    if 'ppe_data' in data:
                        del data['ppe_data']
                    if 'vpms_data' in data:
                        del data['vpms_data']
                    if 'trafficjam_data' in data:
                        del data['trafficjam_data']
                    if len(output) ==1 and 'genetic_id' in output:
                        finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                        if finddata is not None: 
                            id = data['id']
                            print("data =keys ",list(data.keys()))
                            # print('----------------------data----------------------edit camera----------',data)
                            if 'ai_solution' in data:
                                print("====ai_solutions",data['ai_solution'])
                                print("found_ai solutions",finddata['ai_solution'])
                                if (finddata['ai_solution']==data['ai_solution']) != True:
                                    print("finddata['ai_solution']=====checking both dictionaries are equal===",finddata['ai_solution']==data['ai_solution'])
                                    returnvalue=checkwhichdictionarykeyvaluesChanged(data['ai_solution'],finddata['ai_solution'])
                                    print("returnvalue===",returnvalue)
                                    has_true_value = any(value for value in returnvalue.values())
                                    if has_true_value:    
                                        print("updatestatus==2=",checkdictionarfortruevaluesonly(returnvalue,finddata)   ) 
                                        if checkdictionarfortruevaluesonly(returnvalue,finddata)  : 
                                            if '_id' in data:
                                                del data['id']
                                            contains_false = all(value is False for value in data['ai_solution'].values())
                                            if contains_false:
                                                data['analytics_status']='false'
                                            print("-----------------------hooterrelay test1.8--")
                                            NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                            ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                            data['roi_data'] =NEwROIDATA
                                            result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                            if result.modified_count > 0:
                                                ret = {'message': 'camera details edited successfully.','success': True}
                                            else:
                                                ret['message'] = 'camera details not edited, please try once again.'
                                        else:
                                            ret['message'] = 'there is no data found ai solution enabled, please add data in camera setting page then try again.'
                                    else:
                                        if '_id' in data:
                                            del data['id']
                                        contains_false = all(value is False for value in data['ai_solution'].values())
                                        if contains_false:
                                            data['analytics_status']='false'
                                        print("-----------------------hooterrelay test1.9--")
                                        NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                        ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                        data['roi_data'] =NEwROIDATA
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                        if result.modified_count > 0:
                                            ret = {'message': 'camera details edited successfully.','success': True}
                                        else:
                                            ret['message'] = 'camera details not edited, please try once again.'                                
                                else:
                                    if '_id' in data:
                                        del data['id']
                                    contains_false = all(value is False for value in data['ai_solution'].values())
                                    if contains_false:
                                        data['analytics_status']='false'
                                    print("-----------------------hooterrelay test1.10--")
                                    NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                    ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                    data['roi_data'] =NEwROIDATA
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                    if result.modified_count > 0:
                                        ret = {'message': 'camera details edited successfully.','success': True}
                                    else:
                                        ret['message'] = 'camera details not edited, please try once again.'
                            else:
                                if '_id' in data:
                                    del data['id']
                                # contains_false = all(value is False for value in data['ai_solution'].values())
                                # if contains_false:
                                #     data['analytics_status']='false'
                                print("-----------------------hooterrelay test1.11--")
                                NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                data['roi_data'] =NEwROIDATA
                                result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                if result.modified_count > 0:
                                    ret = {'message': 'camera details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'camera details not edited, please try once again.'
                        else:
                            ret['message']='camera details is not found for given id.'
                    else:
                        ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                    if finddata is not None: 
                        id = data['id']
                        if 'roi_data' in data:
                            del data['roi_data']
                        if 'tc_data' in data:
                            del data['tc_data']
                        if 'cr_data' in data:
                            del data['cr_data']
                        if 'ppe_data' in data:
                            del data['ppe_data']
                        if 'vpms_data' in data:
                            del data['vpms_data']
                        if 'trafficjam_data' in data:
                            del data['trafficjam_data']
                        print("data =keys ",list(data.keys()))
                        # print('----------------------data----------------------edit camera----------',data)
                        if 'ai_solution' in data:
                            print("====ai_solutions",data['ai_solution'])
                            print("found_ai solutions",finddata['ai_solution'])
                            if (finddata['ai_solution']==data['ai_solution']) != True:
                                print("finddata['ai_solution']=====checking both dictionaries are equal===",finddata['ai_solution']==data['ai_solution'])
                                returnvalue=checkwhichdictionarykeyvaluesChanged(data['ai_solution'],finddata['ai_solution'])
                                print("returnvalue===",returnvalue)
                                has_true_value = any(value for value in returnvalue.values())
                                if has_true_value:    
                                    print("updatestatus==3=",checkdictionarfortruevaluesonly(returnvalue,finddata)   ) 
                                    if checkdictionarfortruevaluesonly(returnvalue,finddata)  : 
                                        if '_id' in data:
                                            del data['id']
                                        contains_false = all(value is False for value in data['ai_solution'].values())
                                        if contains_false:
                                            data['analytics_status']='false'
                                        print("-----------------------hooterrelay test1.12--")
                                        NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                        ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                        data['roi_data'] =NEwROIDATA
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                        if result.modified_count > 0:
                                            ret = {'message': 'camera details edited successfully.','success': True}
                                        else:
                                            ret['message'] = 'camera details not edited, please try once again.'
                                    else:
                                        ret['message'] = 'there is no data found ai solution enabled, please add data in camera setting page then try again.'
                                else:
                                    if '_id' in data:
                                        del data['id']
                                    contains_false = all(value is False for value in data['ai_solution'].values())
                                    if contains_false:
                                        data['analytics_status']='false'
                                    print("-----------------------hooterrelay test1.13--")
                                    NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                    ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                    data['roi_data'] =NEwROIDATA
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                    if result.modified_count > 0:
                                        ret = {'message': 'camera details edited successfully.','success': True}
                                    else:
                                        ret['message'] = 'camera details not edited, please try once again.'                                
                            else:
                                if '_id' in data:
                                    del data['id']
                                contains_false = all(value is False for value in data['ai_solution'].values())
                                if contains_false:
                                    data['analytics_status']='false'
                                print("-----------------------hooterrelay test1.14--")
                                NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                data['roi_data'] =NEwROIDATA
                                result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                if result.modified_count > 0:
                                    ret = {'message': 'camera details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'camera details not edited, please try once again.'
                        else:
                            if '_id' in data:
                                del data['id']
                            # contains_false = all(value is False for value in data['ai_solution'].values())
                            # if contains_false:
                            #     data['analytics_status']='false'
                            print("-----------------------hooterrelay test1.15--")
                            NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                            ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                            data['roi_data'] =NEwROIDATA
                            result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                            if result.modified_count > 0:
                                ret = {'message': 'camera details edited successfully.','success': True}
                            else:
                                ret['message'] = 'camera details not edited, please try once again.'
                    else:
                        ret['message']='camera details is not found for given id.'
            else:
                request_key_array = [ 'id','plant', 'area', 'cameraname', 'alarm_type', 'alarm_ip_address','coin_details','department','alarm_enable','ai_solution','alarm_version','poc','genetic_id']
                print("-------------request_key_array--1---",request_key_array)
                print("-------------datakeys--------1------",datakeys)
                check =  all(item in request_key_array for item in datakeys)
                print("all ajdkfkadjkf===1= ",check) 
                if 'roi_data' in data:
                    del data['roi_data']
                if 'tc_data' in data:
                    del data['tc_data']
                if 'cr_data' in data:
                    del data['cr_data']
                if 'ppe_data' in data:
                    del data['ppe_data']
                if 'vpms_data' in data:
                    del data['vpms_data']
                if 'trafficjam_data' in data:
                    del data['trafficjam_data']
                if check is True:
                    print("The list {} contains all elements of the list {}".format(request_key_array, datakeys))
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        if 'genetic_id' in output and len(output) ==1:
                        
                            finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                            if finddata is not None: 
                                id = data['id']
                                print("data =keys ",list(data.keys()))
                                # print('----------------------data----------------------edit camera----------',data)
                                if 'ai_solution' in data:
                                    print("====ai_solutions",data['ai_solution'])
                                    print("found_ai solutions",finddata['ai_solution'])
                                    if (finddata['ai_solution']==data['ai_solution']) != True:
                                        print("finddata['ai_solution']=====checking both dictionaries are equal===",finddata['ai_solution']==data['ai_solution'])
                                        returnvalue=checkwhichdictionarykeyvaluesChanged(data['ai_solution'],finddata['ai_solution'])
                                        print("returnvalue===",returnvalue)
                                        has_true_value = any(value for value in returnvalue.values())
                                        if has_true_value:    
                                            print("updatestatus==4=",checkdictionarfortruevaluesonly(returnvalue,finddata)   ) 
                                            if checkdictionarfortruevaluesonly(returnvalue,finddata)  : 
                                                if '_id' in data:
                                                    del data['id']
                                                contains_false = all(value is False for value in data['ai_solution'].values())
                                                if contains_false:
                                                    data['analytics_status']='false'
                                                print("-----------------------hooterrelay test1.16--")
                                                NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                                ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                                data['roi_data'] =NEwROIDATA
                                                result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                                if result.modified_count > 0:
                                                    ret = {'message': 'camera details edited successfully.','success': True}
                                                else:
                                                    ret['message'] = 'camera details not edited, please try once again.'
                                            else:
                                                ret['message'] = 'there is no data found ai solution enabled, please add data in camera setting page then try again.'
                                        else:
                                            if '_id' in data:
                                                del data['id']
                                            contains_false = all(value is False for value in data['ai_solution'].values())
                                            if contains_false:
                                                data['analytics_status']='false'
                                            print("-----------------------hooterrelay test1.17--")
                                            NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                            ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                            data['roi_data'] =NEwROIDATA
                                            result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                            if result.modified_count > 0:
                                                ret = {'message': 'camera details edited successfully.','success': True}
                                            else:
                                                ret['message'] = 'camera details not edited, please try once again.'                                
                                    else:
                                        if '_id' in data:
                                            del data['id']
                                        contains_false = all(value is False for value in data['ai_solution'].values())
                                        if contains_false:
                                            data['analytics_status']='false'
                                        print("-----------------------hooterrelay test1.18--")
                                        NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                        ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                        data['roi_data'] =NEwROIDATA
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                        if result.modified_count > 0:
                                            ret = {'message': 'camera details edited successfully.','success': True}
                                        else:
                                            ret['message'] = 'camera details not edited, please try once again.'
                                else:
                                    if '_id' in data:
                                        del data['id']
                                    # contains_false = all(value is False for value in data['ai_solution'].values())
                                    # if contains_false:
                                    #     data['analytics_status']='false'
                                    print("-----------------------hooterrelay test1.19--")
                                    NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                    ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                    data['roi_data'] =NEwROIDATA
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                    if result.modified_count > 0:
                                        ret = {'message': 'camera details edited successfully.','success': True}
                                    else:
                                        ret['message'] = 'camera details not edited, please try once again.'
                            else:
                                ret['message']='camera details is not found for given id.'
                        else:
                            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                    else:
                        finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                        if finddata is not None: 
                            id = data['id']
                            print("data =keys ",list(data.keys()))
                            # print('----------------------data----------------------edit camera----------',data)
                            if 'ai_solution' in data:
                                print("====ai_solutions",data['ai_solution'])
                                print("found_ai solutions",finddata['ai_solution'])
                                if (finddata['ai_solution']==data['ai_solution']) != True:
                                    print("finddata['ai_solution']=====checking both dictionaries are equal===",finddata['ai_solution']==data['ai_solution'])
                                    returnvalue=checkwhichdictionarykeyvaluesChanged(data['ai_solution'],finddata['ai_solution'])
                                    print("returnvalue===",returnvalue)
                                    has_true_value = any(value for value in returnvalue.values())
                                    if has_true_value:    
                                        print("updatestatus==4=",checkdictionarfortruevaluesonly(returnvalue,finddata)   ) 
                                        if checkdictionarfortruevaluesonly(returnvalue,finddata)  : 
                                            if '_id' in data:
                                                del data['id']
                                            contains_false = all(value is False for value in data['ai_solution'].values())
                                            if contains_false:
                                                data['analytics_status']='false'
                                            print("-----------------------hooterrelay test1.16--")
                                            NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                            ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                            data['roi_data'] =NEwROIDATA
                                            result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                            if result.modified_count > 0:
                                                ret = {'message': 'camera details edited successfully.','success': True}
                                            else:
                                                ret['message'] = 'camera details not edited, please try once again.'
                                        else:
                                            ret['message'] = 'there is no data found ai solution enabled, please add data in camera setting page then try again.'
                                    else:
                                        if '_id' in data:
                                            del data['id']
                                        contains_false = all(value is False for value in data['ai_solution'].values())
                                        if contains_false:
                                            data['analytics_status']='false'
                                        print("-----------------------hooterrelay test1.17--")
                                        NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                        ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                        data['roi_data'] =NEwROIDATA
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                        if result.modified_count > 0:
                                            ret = {'message': 'camera details edited successfully.','success': True}
                                        else:
                                            ret['message'] = 'camera details not edited, please try once again.'                                
                                else:
                                    if '_id' in data:
                                        del data['id']
                                    contains_false = all(value is False for value in data['ai_solution'].values())
                                    if contains_false:
                                        data['analytics_status']='false'
                                    print("-----------------------hooterrelay test1.18--")
                                    NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                    ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                    data['roi_data'] =NEwROIDATA
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                    if result.modified_count > 0:
                                        ret = {'message': 'camera details edited successfully.','success': True}
                                    else:
                                        ret['message'] = 'camera details not edited, please try once again.'
                            else:
                                if '_id' in data:
                                    del data['id']
                                # contains_false = all(value is False for value in data['ai_solution'].values())
                                # if contains_false:
                                #     data['analytics_status']='false'
                                print("-----------------------hooterrelay test1.19--")
                                NEwROIDATA = remove_relayhooterDetailsinROi(data, finddata)
                                ReturnValueOFHooterrelay = compare_lists(finddata['roi_data'], NEwROIDATA)
                                data['roi_data'] =NEwROIDATA
                                result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': data})
                                if result.modified_count > 0:
                                    ret = {'message': 'camera details edited successfully.','success': True}
                                else:
                                    ret['message'] = 'camera details not edited, please try once again.'
                        else:
                            ret['message']='camera details is not found for given id.'
                else:
                    ret['message'] ='you have given wrong parameters edit camera details.'
        else:
            ret['message']='you have missed data parameter to send.'
    return JsonResponse(ret)


# @camera_coin.route("/edit_alarmdetails",methods=['POST'])
@csrf_exempt
def editALARMDETAILS(request):
    ret={"success":False,"message":"something went wrong with edit api."}
    if request.method == "POST":
        data = json.loads(request.body)
        if data is  None:
            data = {}
        if isEmpty(data):
            datakeys = list(data.keys())
            request_key_array = [ 'id','alarm_type', 'alarm_ip_address','coin_details','alarm_enable']
            check =  all(item in request_key_array for item in datakeys)
            if check is True:
                print("The list {} contains all elements of the list {}".format(request_key_array, datakeys))
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    if data['alarm_type'] =='sensegiz':
                        data['alarm_ip_address'] = None
                    elif data['alarm_type']=='hooter' or data['alarm_type']=='relay':
                        data['coin_details'] = None
                    finddata = ppera_cameras.find_one({'_id': ObjectId(data['id'])})
                    if finddata is not None: 
                        result = ppera_cameras.update_one({'_id': ObjectId(data['id'])}, {'$set': data})
                        if result.modified_count > 0:
                            ret = {'message': 'alarm details edited successfully.','success': True}
                        else:
                            ret['message'] = 'alarm details not edited, please try once again.'
                    else:
                        ret['message']='alarm details is not found for given id.'
            else:
                ret['message'] ='you have given wrong parameters edit camera details.'
        else:
            ret['message']='you have missed data parameter to send.'
    return JsonResponse(ret)

# @camera_coin.route('/add_roi', methods=['POST'])
@csrf_exempt
def camera_adding_roi(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'roi_data', 'ai_solutions', 'ppe_data']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_data = data['roi_data']
                ai_solutions = data['ai_solutions']
                ppe_data = data['ppe_data']
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
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
                                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': ai_solutions,'ppe_data': ppe_data}}))
                                                    if result.modified_count > 0:
                                                        ret = {'message':'ppe added successfully.', 'success': True}
                                                    else:
                                                        ret['message'] = 'ppe not adeed.'
                                                else:
                                                    ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                            elif type(ai_solutions) == dict:
                                                if isEmpty(ai_solutions) :
                                                    finddata['ai_solution'].update(ai_solutions)
                                                    print("ai_solutions")
                                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': finddata['ai_solution'],'ppe_data': ppe_data}}))
                                                    if result.modified_count > 0:
                                                        ret = {'message':'ppe added successfully.', 'success': True}
                                                    else:
                                                        ret['message'] = 'ppe not adeed.'
                                                else:
                                                    ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, it should be list type.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions.'
                                    else:
                                        ret['message'] = 'please give proper ppe data.'
                                else:
                                    if ai_solutions is not None:
                                        if type(ai_solutions) == list:
                                            if len(ai_solutions) != 0:
                                                ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data,'ai_solution': ai_solutions,'ppe_data': ppe_data}}))
                                                if result.modified_count > 0:
                                                    ret = {'message': 'roi added successfully.','success': True}
                                                else:
                                                    ret['message'] = 'roi not adeed.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                        elif type(ai_solutions) == dict:
                                            if isEmpty(ai_solutions) :
                                                finddata['ai_solution'].update(ai_solutions)
                                                result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data,'ai_solution': finddata['ai_solution'],'ppe_data': ppe_data}}))
                                                if result.modified_count > 0:
                                                    ret = {'message': 'roi added successfully.','success': True}
                                                else:
                                                    ret['message'] = 'roi not adeed.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions, it should be list type.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions.'
                            elif ppe_data is not None:
                                if type(ppe_data) == list:
                                    if len(ppe_data) != 0:
                                        if ai_solutions is not None:
                                            if type(ai_solutions) == list:
                                                if len(ai_solutions) != 0:
                                                    ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': ai_solutions,'ppe_data': ppe_data}}))
                                                    if result.modified_count > 0:
                                                        ret = {'message':'ppe added successfully.', 'success': True}
                                                    else:
                                                        ret['message'] = 'ppe not adeed.'
                                                else:
                                                    ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                            elif type(ai_solutions) == dict:
                                                if isEmpty(ai_solutions) :
                                                    finddata['ai_solution'].update(ai_solutions)
                                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': finddata['ai_solution'],'ppe_data': ppe_data}}))
                                                    if result.modified_count > 0:
                                                        ret = {'message':'ppe added successfully.', 'success': True}
                                                    else:
                                                        ret['message'] = 'ppe not adeed.'
                                                else:
                                                    ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, it should be list type.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions.'
                                    else:
                                        ret['message'] = 'please give proper ppe data.'
                                else:
                                    ret['message'] = 'please give proper ppe data, it should be list type.'
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
    return JsonResponse(ret)


# @camera_coin.route('/edit_roi', methods=['POST'])
@csrf_exempt
def camera_edit_roi(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'ai_solutions', 'roi_data','roi_id']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                roi_data = data['roi_data']
                print("-----------id-----",id)
                print("ai_solutions====",ai_solutions)
                print("==roi_data==",roi_data)
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if type(roi_data) == list:
                        if len(roi_data) != 0:
                            if isEmpty(ai_solutions):
                                fetch_roi_data = finddata['roi_data']
                                if len(fetch_roi_data) != 0:
                                    if len(fetch_roi_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': roi_data, 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'roi data updated successfully.','success': True}
                                        else:
                                            print("------roi not updated-------------0000001.6.")
                                            ret['message'] = 'roi not updated.'
                                    elif len(fetch_roi_data) > 1:
                                        update_data = []
                                        if len(roi_data) == 1:
                                            finddata['ai_solution'].update(ai_solutions)
                                            for __, i in enumerate(fetch_roi_data):
                                                if int(i['roi_id']) == int(roi_data[0][ 'roi_id']):
                                                    # i['bb_box'] = roi_data[0]['bb_box']
                                                    # # i = roi_data[0]['bb_box']
                                                    # if 'pinch_role' in roi_data[0] :
                                                    #     i['pinch_role']= roi_data[0]['pinch_role']
                                                    i = roi_data[0]
                                                    #'pinch_role': {'bb_box': '', 'roi_name': '', 'status': True}
                                                    update_data.append(i)
                                                else:
                                                    update_data.append(i)
                                            
                                            print("---------------------fetch_roi_data--------------",fetch_roi_data)
                                            print("------------------update_data-------------------",update_data)
                                            result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                print("------roi updated-------------0000001.5.")
                                                ret = {'message': 'roi data updated successfully.','success': True}
                                            else:
                                                print("------roi not updated-------------0000001.5.")
                                                ret['message'] = 'roi not updated.'
                                        elif len(roi_data) > 1:
                                            update_data = []
                                            finddata['ai_solution'].update(ai_solutions)
                                            for __, i in enumerate(fetch_roi_data):
                                                for __, jjk in enumerate(roi_data):
                                                    if int(i['roi_id']) == int(jjk['roi_id']):
                                                        # i['bb_box'] = jjk['bb_box']
                                                        # if 'pinch_role' in jjk :
                                                        #     i['pinch_role']= jjk['pinch_role']
                                                        i = jjk
                                                        if i not in update_data:
                                                            update_data.append(i)
                                                    else:
                                                        if i not in update_data:
                                                            update_data.append(i)
                                                        if jjk not in update_data:
                                                            update_data.append(jjk)
                                            result = (ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'roi data updated successfully.','success': True}
                                            else:
                                                print("------roi not updated-------------0000001.1.")
                                                ret['message'] = 'roi not updated.'
                                        else:
                                            ret['message'] = 'There is no roi region the camrea, please try to add.'
                                else:
                                    ret['message'] = 'There is no camrea details exist , please try to add.'
                            elif len(fetch_roi_data) != 0:
                                update_data = []
                                if len(fetch_roi_data) == 1:
                                    final_ai = (set(ai_solutions).union(set (finddata['ai_solution'])))
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'roi_data': roi_data, 'ai_solution': final_ai}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'roi data updated successfully.','success': True}
                                    else:
                                        print("------roi not updated-------------0000001.2.")
                                        ret['message'] = 'roi not updated.'
                                elif len(fetch_roi_data) > 1:
                                    if len(roi_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(fetch_roi_data):
                                            if int(i['roi_id']) == int(roi_data[0]['roi_id']):
                                                # i['bb_box'] = roi_data[0]['bb_box']
                                                i = roi_data[0]
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'roi data updated successfully.','success': True}
                                        else:
                                            print("------roi not updated-------------0000001.3.")
                                            ret['message'] = 'roi not updated.'
                                    elif len(roi_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(fetch_roi_data):
                                            for __, jjk in enumerate(fetch_roi_data):
                                                if int(i['roi_id']) == int(jjk['roi_id']):
                                                    # i['bb_box'] = jjk['bb_box']
                                                    i = jjk
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                                else:
                                                    if i not in update_data:
                                                        update_data.append(i)
                                                    if jjk not in update_data:
                                                        update_data.append(jjk)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message': 'roi data updated successfully.','success': True}
                                        else:
                                            print("------roi not updated-------------0000001.4.")
                                            ret['message'] = 'roi not updated.'
                                    else:
                                        ret['message'] = 'There is no roi region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        else:
                            ret['message'] = 'roi data should not be empty list.'
                    else:
                        ret['message'] = 'roi data type should be list'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)


# @camera_coin.route('/delete_roi', methods=['POST'])
@csrf_exempt
def camera_delete_roi(request):
    ret = {'success': False, 'message':'something went wrong with delete_roi roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        try:
        
            if data == None:
                data = {}
            request_key_array = ['id', 'roi_id', 'ai_solutions']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    id = data['id']
                    roi_id = data['roi_id']
                    ai_solutions = data['ai_solutions']
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if finddata is not None:
                        if roi_id is not None:
                            if isEmpty(ai_solutions) :
                                roi_data = finddata['roi_data']
                                if len(roi_data) != 0:
                                    update_data = []
                                    if len(roi_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        print("finddata['ai_solution']",finddata['ai_solution'])
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.0')
                                            ret = {'message':'roi data delete successfully.','success': True}
                                        else:
                                            print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.1')
                                            ret['message'] = 'roi not deleted.'
                                    elif len(roi_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(roi_data):
                                            if int(i['roi_id']) == int(roi_id):
                                                print()
                                                # roi_data.remove(i)
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.2')
                                            ret = {'message': 'roi data delete successfully.','success': True}
                                        else:
                                            print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.3')
                                            ret['message'] = 'roi not deleted.'
                                else:
                                    ret['message'] = 'There is no roi region the camrea, please try to add.'
                            else:
                                roi_data = finddata['roi_data']
                                if len(roi_data) != 0:
                                    if len(roi_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'roi data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not deleted.'
                                    elif len(roi_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(roi_data):
                                            if int(i['roi_id']) == int(roi_id):
                                                print()
                                                # roi_data.remove(i)
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'roi data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'roi not deleted.'
                                else:
                                    ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            ret['message'] = 'please give proper roi data, it should not none type.'
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] =" ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
        except Exception as error:
            ret['message'] =" ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_roi 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @camera_coin.route('/add_cr_data', methods=['POST'])
@csrf_exempt
def camera_add_cr_data(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'cr_data','ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                cr_data = data['cr_data']
                ai_solutions = data['ai_solutions']
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if cr_data is not None:
                        if type(cr_data) == list:
                            if len(cr_data) != 0:
                                if ai_solutions is not None:
                                    if isEmpty(ai_solutions) :
                                        print("found_data=", finddata['cr_data'])
                                        print("given_data=",cr_data)
                                        if len(cr_data)==1:
                                            if cr_data[0]['full_frame']:
                                                if cr_data[0]['bb_box'] ==''and cr_data[0]['area_name']=='':
                                                    #any([v==None for v in d.values()])
                                                    if check_arraydictionaryishavinganynonevalue(cr_data[0]['data_object']):
                                                        if check_dataobjects_of_cr_data(cr_data[0]['data_object']):
                                                            finddata['ai_solution'].update(ai_solutions)
                                                            result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'cr_data':cr_data,'ai_solution': finddata['ai_solution']}}))
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
                                                                                finddata['ai_solution'].update(ai_solutions)
                                                                                result = (ppera_cameras.update_one({'_id': ObjectId(id)},{'$set': {'cr_data':final_cr_data,'ai_solution': finddata['ai_solution']}}))
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
                                                                        finddata['ai_solution'].update(ai_solutions)
                                                                        result = (ppera_cameras.update_one({'_id': ObjectId(id)},{'$set': {'cr_data':cr_data,'ai_solution': finddata['ai_solution']}}))
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
                                        ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                else:
                                    ret['message'] = 'please give proper ai_solutions.' 
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
    return JsonResponse(ret)

# @camera_coin.route('/edit_crdata', methods=['POST'])
@csrf_exempt
def camera_editCRroi(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'ai_solutions', 'cr_data','roi_id']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                cr_data = data['cr_data']
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if type(cr_data) == list:
                        if len(cr_data) != 0:
                            if isEmpty(ai_solutions):
                                fetch_cr_data = finddata['cr_data']
                                if len(fetch_cr_data) != 0:
                                    if len(fetch_cr_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': cr_data, 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    elif len(fetch_cr_data) > 1:
                                        update_data = []
                                        if len(cr_data) == 1:
                                            finddata['ai_solution'].update(ai_solutions)
                                            for __, i in enumerate(fetch_cr_data):
                                                if int(i['roi_id']) == int(cr_data[0][ 'roi_id']):
                                                    i['bb_box'] = cr_data[0]['bb_box']
                                                    update_data.append(i)
                                                else:
                                                    update_data.append(i)
                                            result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'cr_data data updated successfully.','success': True}
                                            else:
                                                ret['message'] = 'cr_data not updated.'
                                        elif len(cr_data) > 1:
                                            update_data = []
                                            finddata['ai_solution'].update(ai_solutions)
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
                                            result = (ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'cr_data data updated successfully.','success': True}
                                            else:
                                                ret['message'] = 'cr_data not updated.'
                                        else:
                                            ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                                else:
                                    ret['message'] = 'There is no camrea details exist , please try to add.'
                            elif len(fetch_cr_data) != 0:
                                update_data = []
                                if len(fetch_cr_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'cr_data': cr_data, 'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'cr_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not updated.'
                                elif len(fetch_cr_data) > 1:
                                    if len(cr_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(fetch_cr_data):
                                            if int(i['roi_id']) == int(cr_data[0]['roi_id']):
                                                i['bb_box'] = cr_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    elif len(cr_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
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
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not updated.'
                                    else:
                                        ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        else:
                            ret['message'] = 'cr_data data should not be empty list.'
                    else:
                        ret['message'] = 'cr_data data type should be list'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)


# @camera_coin.route('/delete_cr_data', methods=['POST'])
@csrf_exempt
def camera_delete_cr_data(request):
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            if data == None:
                data = {}
            request_key_array = ['id', 'roi_id', 'ai_solutions']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    id = data['id']
                    roi_id = data['roi_id']
                    ai_solutions = data['ai_solutions']
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if finddata is not None:
                        if roi_id is not None:
                            if isEmpty(ai_solutions):
                                cr_data = finddata['cr_data']
                                if len(cr_data) != 0:
                                    update_data = []
                                    if len(cr_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'cr_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not deleted.'
                                    elif len(cr_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(cr_data):
                                            if int(i['roi_id']) == int(roi_id):
                                                print()
                                                # cr_data.remove(i)
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message': 'cr_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not deleted.'
                                else:
                                    ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                            else:
                                cr_data = finddata['cr_data']
                                if len(cr_data) != 0:
                                    if len(cr_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'cr_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not deleted.'
                                    elif len(cr_data) > 1:
                                        update_data=[]
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(cr_data):
                                            if int(i['roi_id']) == int(roi_id):
                                                # cr_data.remove(i)
                                                print()
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'cr_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'cr_data not deleted.'
                                else:
                                    ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                        else:
                            ret['message'] = 'please give proper cr_data data, it should not none type.'
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
        except Exception as error:
            ret['message'] = " ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ])
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_cr_data 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @camera_coin.route('/delete_crfullframe_data', methods=['POST'])
@csrf_exempt
def delete_crfullframe_data(request):
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            if data == None:
                data = {}
            request_key_array = ['id', 'ai_solutions']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    id = data['id']
                    ai_solutions = data['ai_solutions']
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if finddata is not None:
                        if isEmpty(ai_solutions):
                            cr_data = finddata['cr_data']
                            if len(cr_data) != 0:
                                update_data = []
                                if len(cr_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                                elif len(cr_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(cr_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            cr_data.remove(i)
                                        else:
                                            update_data.append(i)
                                    result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                            else:
                                ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                        else:
                            cr_data = finddata['cr_data']
                            if len(cr_data) != 0:
                                if len(cr_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                                elif len(cr_data) > 1:
                                    update_data=[]
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(cr_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            cr_data.remove(i)
                                        else:
                                            update_data.append(i)
                                    result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'cr_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'cr_data data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'cr_data not deleted.'
                            else:
                                ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
        except Exception as error:
            ret['message'] = " ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ])
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_cr_data 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @camera_coin.route('/add_tc_data', methods=['POST'])
@csrf_exempt
def camera_add_tc_data(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        # print("hi--------------------")
        # print(data)
        if data == None:
            data = {}
        request_key_array = ['id', 'tc_data','ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                # print(id,"------------------")
                tc_data = data['tc_data']
                # print(tc_data,"------------------")
                ai_solutions = data['ai_solutions']
                # print(ai_solutions,"------------------")
                if id is not None:
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    # print(finddata,"-------------")
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
                                                            if isEmpty(ai_solutions):
                                                                finddata['ai_solution'].update(ai_solutions)
                                                                result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'ai_solution': finddata['ai_solution'],'tc_data': returntcdata}}))
                                                                if result.modified_count > 0:
                                                                    ret = {'message': 'traffic count data added successfully.', 'success': True}
                                                                else:
                                                                    ret['message'] = 'traffic count data not adeed.'
                                                            else:
                                                                ret['message'] = 'please give proper ai_solutions, it should be object type.'
                                                        else:
                                                            ret['message' ] = 'please give proper ai_solutions.' 
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
                                    ret['message']=' tc data  should not be empty list.'
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
    return JsonResponse(ret)

# @camera_coin.route('/edit_tcdata', methods=['POST'])
@csrf_exempt
def camera_edittcroi(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'ai_solutions', 'tc_data','roi_id']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                tc_data = data['tc_data']
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if type(tc_data) == list:
                        if len(tc_data) != 0:
                            if isEmpty(ai_solutions):
                                fetch_tc_data = finddata['tc_data']
                                if len(fetch_tc_data) != 0:
                                    if len(fetch_tc_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': tc_data, 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    elif len(fetch_tc_data) > 1:
                                        update_data = []
                                        if len(tc_data) == 1:
                                            finddata['ai_solution'].update(ai_solutions)
                                            for __, i in enumerate(fetch_tc_data):
                                                if int(i['roi_id']) == int(tc_data[0][ 'roi_id']):
                                                    i['bb_box'] = tc_data[0]['bb_box']
                                                    update_data.append(i)
                                                else:
                                                    update_data.append(i)
                                            result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'tc_data data updated successfully.','success': True}
                                            else:
                                                ret['message'] = 'tc_data not updated.'
                                        elif len(tc_data) > 1:
                                            update_data = []
                                            finddata['ai_solution'].update(ai_solutions)
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
                                            result = (ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'tc_data data updated successfully.','success': True}
                                            else:
                                                ret['message'] = 'tc_data not updated.'
                                        else:
                                            ret['message'] = 'There is no cr_data region the camrea, please try to add.'
                                else:
                                    ret['message'] = 'There is no camrea details exist , please try to add.'
                            elif len(fetch_tc_data) != 0:
                                update_data = []
                                if len(fetch_tc_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'tc_data': tc_data, 'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'tc_data data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'tc_data not updated.'
                                elif len(fetch_tc_data) > 1:
                                    if len(tc_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(fetch_tc_data):
                                            if int(i['roi_id']) == int(tc_data[0]['roi_id']):
                                                i['bb_box'] = tc_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    elif len(tc_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
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
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not updated.'
                                    else:
                                        ret['message'] = 'There is no tc_data in the camrea, please try to add.'
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
    return JsonResponse(ret)


# @camera_coin.route('/delete_tc_data', methods=['POST'])
@csrf_exempt
def camera_delete_tc_data(request):
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if 1:
        # try:
            if data == None:
                data = {}
            request_key_array = ['id', 'roi_id', 'ai_solutions']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    id = data['id']
                    roi_id = data['roi_id']
                    ai_solutions = data['ai_solutions']
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if finddata is not None:
                        if roi_id is not None:
                            if isEmpty(ai_solutions):
                                tc_data = finddata['tc_data']
                                if len(tc_data) != 0:
                                    update_data = []
                                    if len(tc_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'tc_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not deleted.'
                                    elif len(tc_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(tc_data):
                                            if int(i['roi_id']) == int(roi_id):
                                                # tc_data.remove(i)
                                                print()
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message': 'tc_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not deleted.'
                                else:
                                    ret['message'] = 'There is no tc_data region the camrea, please try to add.'
                            else:
                                print("delete tc data === ,",ai_solutions)
                                tc_data = finddata['tc_data']
                                if len(tc_data) != 0:
                                    update_data=[]
                                    if len(tc_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'tc_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not deleted.'
                                    elif len(tc_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        print("tc_datatc_datatc_data==",tc_data)
                                        for __, i in enumerate(tc_data):
                                            print("---i",i)
                                            if int(i['roi_id']) == int(roi_id):
                                                # tc_data.remove(i)
                                                print()
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'tc_data': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'tc_data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'tc_data not deleted.'
                                else:
                                    ret['message'] = 'There is no tc_data in the camrea, please try to add.'
                        else:
                            ret['message'] = 'please give proper tc_data data, it should not none type.'
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
        # except Exception as error:
        #     ret['message'] = " ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
        #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_tc_data 2", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)

# @camera_coin.route('/get_ra_camera_details/<id>', methods=['GET'])
# @camera_coin.route('/get_ra_camera_details', methods=['GET'])
@csrf_exempt
def ra_camera_details(request,id=None):
    ret = {'success': False, 'message':'something went wrong with ra camera details api'}
    if request.method == "GET":
        try:
            final_data = []
            if id is not None:
                data = ppera_cameras.find_one({'_id': ObjectId(id)})
                if data is not None:
                    data = parse_json(data)
                    data = delete_keys_from_dict(data, ['cameraid', 'username', 'password', 'camera_brand', 'rtsp_port','camera_status',  'timestamp'])
                    final_data.append(data)
                    if len(final_data) != 0:
                        ret = {'message': final_data, 'success': True}
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                data = ppera_cameras.find()
                if data is not None:
                    for jj, i in enumerate(data):
                        i = delete_keys_from_dict(i, ['cameraid', 'username', 'password', 'image_height','image_width', 'rtsp_port', 'camera_status','timestamp'])
                        final_data.append(i)
                    final_data = parse_json(final_data)
                    if len(final_data) != 0:
                        ret = {'message': final_data, 'success': True}
                    else:
                        ret['message'] = 'cameras are not found for RA, PPE, please add cameras.'
                else:
                    ret['message'] = 'cameras are not found for RA, PPE, please add cameras.'
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- get_ra_camera_details 2", str(error), " ----time ---- ", now_time_with_time()]))
        # ret.headers['X-Frame-Options'] = 'DENY' 
    return JsonResponse(ret)


# @camera_coin.route('/delete_ra_camera/<id>', methods=['GET'])
@csrf_exempt
def delete_ra_cameras(request,id):
    ret = {'success': False, 'message':'something went wrong with delete ra camera api'}
    if request.method == "GET":
        try:
            if id is not None:
                find_data = ppera_cameras.find_one({'_id': ObjectId(id)})
                if find_data is not None:
                    delete_data = ppera_cameras.delete_one({'_id':ObjectId(id)})
                    if delete_data.deleted_count > 0:
                        #delete_hooter_data(find_data)
                        ret = {'message': 'camera is deleted successfully.','success': True}
                    else:ret['message' ] = 'data is not deleted, please try once again.'
                else:
                    ret['message'] = 'for the given id there no data found, please change the id or try once again.'
            else:
                ret['message'] = 'please give mongoid for deletion of camera details.'
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_ra_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @camera_coin.route('/delete_multiple_camera', methods=['POST'])
# @camera_coin.route('/delete_all_camera', methods=['GET'])
@csrf_exempt
def delete_multiple_camera(request):
    ret = {'success': False, 'message':'something went wrong with delete ra camera api'}
    if request.method == 'GET':
        ret = {'success': False, 'message':'something went wrong with delete ra camera api'}
        try:
            find_data = ppera_cameras.find_one({})
            if find_data is not None:
                delete_data = ppera_cameras.delete_many({})
                if delete_data.deleted_count > 0:
                    #delete_hooter_data(find_data)
                    ret = {'message': 'camera is deleted successfully.','success': True}
                else:ret['message' ] = 'data is not deleted, please try once again.'
            else:
                ret['message'] = 'for the given id there no data found, please change the id or try once again.'
            
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_ra_camera 1", str(error), " ----time ---- ", now_time_with_time()]))

    elif request.method == 'POST':
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['camera_id']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '' or  v == ' ']
            if len(output) !=0 :
                cameraids = data['camera_id']
                if len(cameraids) !=0 :
                    deletestatus = False
                    for i, id in enumerate(cameraids):
                        find_data = ppera_cameras.find_one({'_id': ObjectId(id)})
                        if find_data is not None:
                            delete_data = ppera_cameras.delete_one({'_id':ObjectId(id)})
                            if delete_data.deleted_count > 0:
                                deletestatus= True 
                    if deletestatus:
                        ret = {'message': 'camera is deleted successfully.','success': True}
                    else:
                        ret['message'] = 'for the given id there no data found, please change the id or try once again.'
                else:
                    ret['message'] ='please give proper camera details for deleting cameras.'
            else:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)


# @camera_coin.route('/analytics_status/<id>/<status>', methods=['GET'])
@csrf_exempt
def analyt(request,id = None, status=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if request.method == 'GET':
        if 1:
        # try:
            if id is not None and status is not None:
                    data = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if data is not None:
                        if status !='false':
                            # print("data['ai_solution']==========",data['ai_solution'])
                            # print("data==========",data)
                            print("--------------checkdictionarfortruevaluesonly(data['ai_solution'],data)",checkdictionarfortruevaluesonly(data['ai_solution'],data))
                            if checkdictionarfortruevaluesonly(data['ai_solution'],data):
                                filters ={'_id': ObjectId(id)} #{'analytics_status': status}
                                newvalues = {'$set':{'analytics_status': status}}
                                result = ppera_cameras.update_one(filters, newvalues)
                                if result.modified_count > 0:
                                    ret = {'message':'updated analytics status successfully.','success': True}
                                else:
                                    ret['message'] = 'analytics status is not updated.'
                            else:
                                ret['message']='there is not data for AI analytics, please add any solution in settting page.'
                        else:
                            filters ={'_id': ObjectId(id)} #{'analytics_status': status}
                            newvalues = {'$set':{'analytics_status': status}}
                            result = ppera_cameras.update_one(filters, newvalues)
                            if result.modified_count > 0:
                                ret = {'message':'updated analytics status successfully.','success': True}
                            else:
                                ret['message'] = 'analytics status is not updated.'
                    else:
                        ret['message']='camera details are not found for this id.'
            else:
                ret['message'] = 'mongoid and status should not be None.'
        # except Exception as error:
        #     ret['message'] = " ".join([ "error occerred ", str(error)])
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- analytics_status 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @camera_coin.route('/coin_id_start_record', methods=['POST'])
@csrf_exempt
def coin_id_start_record(request):
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if request.method == 'POST':
        data = json.loads(request.body)
        if 1:
        # try:
            if data == None:
                data = {}
            request_key_array = ['coin_id', 'recording_time']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    coin_id = data['coin_id']
                    recording_time = data['recording_time']
                    # finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    finddata = ppera_cameras.find_one({"coin_details":{"$elemMatch":{"coin_id": coin_id}}})
                    if finddata is not None:
                        camera_ip = finddata['camera_ip']
                        cameraname = finddata['cameraname']
                        camera_rtsp = finddata['rtsp_url']
                        cameraid = finddata['cameraid']
                        camera_brand = finddata['camera_brand']
                        coinid_data = coin_id_violation_data.find_one({'timestamp':{'$regex': '^' + str(date.today())},"camera_ip":camera_ip,'cameraname':cameraname,'camera_rtsp':camera_rtsp,'duration':data['recording_time'],'coinid':data['coin_id'],"cameraid":cameraid,'datauploadstatus':{"＄ne": 1}})
                        if coinid_data is None :
                            print("coindata == ", finddata)
                            coindata= finddata['coin_details']
                            # fetch_preset_value(coinid_data)
                            if camera_brand=='hifocus':
                                presetid = fetch_preset_value(coindata , coin_id)
                                # presetid = ''
                                if presetid is not None:
                                    insertion_data = {"camera_ip":camera_ip,'cameraname':cameraname,'camera_rtsp':camera_rtsp,'coinid':coin_id,"cameraid":cameraid,'datauploadstatus':0,'timestamp':str(date.today()),'duration':recording_time,"request_start_time":now_time_with_time(),"request_end_time":None,"video_name":None,'status':None,"smartrecordkeyid":None}
                                    insertion_data_log = {"camera_ip":camera_ip,'camerabrand':camera_brand,'cameraname':cameraname,'camera_rtsp':camera_rtsp,'coinid':coin_id,"cameraid":cameraid,'datauploadstatus':0,'timestamp':str(date.today()),'duration':recording_time,"request_start_time":now_time_with_time(),"request_end_time":None,"video_name":None,'status':None,"smartrecordkeyid":None,'presetid':presetid,'record_status':0}
                                    record_log_response = record_log_store_in(insertion_data_log)
                                    if record_log_response['success']:
                                        check_camera_record_status  = check_coin_voilation_data(insertion_data)
                                        if check_camera_record_status['error_status'] == False:
                                            if check_camera_record_status['success']:
                                                rotation_return = HIFOCUSPTZROTATEPRESET(camera_ip,presetid)
                                                if rotation_return['success'] :
                                                    time.sleep(5)
                                                    insertion_data = {"camera_ip":camera_ip,'cameraname':cameraname,'camera_rtsp':camera_rtsp,'coinid':coin_id,"cameraid":cameraid,'datauploadstatus':0,'timestamp':str(date.today()),'duration':recording_time,"request_start_time":now_time_with_time(),"request_end_time":None,"video_name":None,'status':None,"smartrecordkeyid":None}
                                                    print("only_date() ", only_date())
                                                    print("tr(date.today()",str(date.today()))
                                                    print("insertion data ====", insertion_data)
                                                    smartrecordTABLECRATION()
                                                    insertion_response = insert_coin_voilation_data(insertion_data)
                                                    if insertion_response['error_status'] == False:
                                                        if insertion_response['success']:
                                                            result = coin_id_violation_data.insert_one(insertion_data)
                                                            if result.acknowledged:
                                                                ret = {'success': True, 'message': 'violation data added successfully.'}                                                            
                                                            else:
                                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                                        else:
                                                            ret['message'] = insertion_response['message']
                                                    elif insertion_response['error_status'] == True:
                                                        ret['message'] = insertion_response['message']
                                                else:
                                                    ret=rotation_return
                                            else:
                                                # ret['message']=check_camera_record_status['message']
                                                ret = record_log_response
                                        elif check_camera_record_status['error_status'] == True:
                                            ret['message'] = check_camera_record_status['message']
                                    else:
                                        ret =record_log_response
                                else:
                                    ret['message']='preset id not valid, please check it.'
                            else:
                                # print('coin_id details not found ')
                                insertion_data = {"camera_ip":camera_ip,'cameraname':cameraname,'camera_rtsp':camera_rtsp,'coinid':coin_id,"cameraid":cameraid,'datauploadstatus':0,'timestamp':str(date.today()),'duration':recording_time,"request_start_time":now_time_with_time(),"request_end_time":None,"video_name":None,'status':None,"smartrecordkeyid":None}
                                insertion_data_log = {"camera_ip":camera_ip,'camerabrand':camera_brand,'cameraname':cameraname,'camera_rtsp':camera_rtsp,'coinid':coin_id,"cameraid":cameraid,'datauploadstatus':0,'timestamp':str(date.today()),'duration':recording_time,"request_start_time":now_time_with_time(),"request_end_time":None,"video_name":None,'status':None,"smartrecordkeyid":None,'presetid':None,'record_status':0}
                                record_log_response = record_log_store_in(insertion_data_log)
                                if record_log_response['success']:
                                    print("only_date() ", only_date())
                                    print("tr(date.today()",str(date.today()))
                                    print("insertion data ====", insertion_data)
                                    smartrecordTABLECRATION()
                                    insertion_response = insert_coin_voilation_data(insertion_data)
                                    if insertion_response['error_status'] == False:
                                        if insertion_response['success']:
                                            result = coin_id_violation_data.insert_one(insertion_data)
                                            if result.acknowledged:
                                                ret = {'success': True, 'message': 'violation data added successfully.'}
                                            else:
                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                        else:
                                            # ret['message'] = insertion_response['message']
                                            ret = record_log_response
                                    elif insertion_response['error_status'] == True:
                                        ret['message'] = insertion_response['message']
                                else:
                                    ret =record_log_response
                        else:
                            ret['message']= 'for this coin id data already exists.'                    
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
        # except Exception as error:
        #     ret['message'] = " ".join(["something error occurred in delete roi ",str(error), ' to enter. please enter properly.','  ----time ----   ',now_time_with_time() ]) 
        #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- coin_id_start_record 1", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @camera_coin.route("/get_coin_violationData",methods=['GET','POST'])
@csrf_exempt
def CoinIDViolationData(request):
    ret= {"message":"something went wrong with get_coin_violationDATA","success":False}
    if request.method == 'GET':
        { "status": { "$in": [None,1 ] }}
        # { "smartrecordkeyid": { "$in": [None, ] }}
        match_data = {'timestamp':{'$regex': '^' + str(date.today())},"status": { "$in": [None,1 ] }}
        find_data = list(coin_id_violation_data.find(match_data))
        if len(find_data) != 0:
            count1 = 1 
            dashdata =[]
            for j , i in enumerate(find_data):
                i['SNo'] = count1
                dashdata.append(i)
                count1 = count1 +1 
            if len(dashdata) != 0 :
                ret={"message":json.loads(find_data),"success":True}
            else:
                ret['message']= "data not found."
        else:
            ret['message'] = "coin_id violation not found for today."
    elif request.method =="POST":
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['coin_id','date',"camera_name"]
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '' or  v == ' ']
            if len(output) !=0 :
                coin_id = data['coin_id']
                date_only = data['date']
                camera_name = data['camera_name']
                # print("data === ", data)
                # print("output ====", output)
                # print("output len ===", len(output))
                if len(output)==3 :
                    match_data = {'timestamp':{'$regex': '^' + str(date.today())},"status": { "$in": [None,1 ] }}
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 8")
                        ret['message'] = "coin_id violation not found for today."
                elif len(output)==2 and "coin_id" in output and "date" in output   :
                    match_data = {"cameraname":camera_name,"status": { "$in": [None,1 ] }}
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 7")
                        ret['message'] = "for the given parameters there is no violation data."
                elif len(output)==2 and "coin_id" in output and "camera_name" in output :
                    match_data = {'timestamp':{'$regex': '^' + date_only},"status": { "$in": [None,1 ] }}
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 6")
                        ret['message'] = "for the given parameters there is no violation data."
                elif len(output)==2 and "date" in output and "camera_name" in output :
                    match_data = {"coinid":coin_id,"status": { "$in": [None,1 ] }}
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 5")
                        ret['message'] = "for the given parameters there is no violation data."
                elif len(output) ==1 and "date" in output :
                    match_data = {"coinid":coin_id ,"cameraname":camera_name,"status": { "$in": [None,1 ] } }
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 4")
                        ret['message'] = "for the given parameters there is no violation data."
                elif len(output) ==1 and "camera_name" in output :
                    match_data = {"coinid":coin_id ,'timestamp':{'$regex': '^' + date_only},"status": { "$in": [None,1 ] } }
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 3")
                        ret['message'] = "for the given parameters there is no violation data."
                elif len(output) ==1 and "coin_id" in output :
                    match_data = {"cameraname":camera_name,'timestamp':{'$regex': '^' + date_only} ,"status": { "$in": [None,1 ] }}
                    find_data = list(coin_id_violation_data.find(match_data))
                    if len(find_data) != 0:
                        count1 = 1 
                        dashdata =[]
                        for j , i in enumerate(find_data):
                            i['SNo'] = count1
                            dashdata.append(i)
                            count1 = count1 +1 
                        if len(dashdata) != 0 :
                            ret={"message":parse_json(find_data),"success":True}
                        else:
                            ret['message']= "data not found."
                        # ret={"message":parse_json(find_data),"success":True}
                    else:
                        print("555 2")
                        ret['message'] = "for the given parameters there is no violation data."
                else:
                    ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                coin_id = data['coin_id']
                date_only = data['date']
                camera_name = data['camera_name']
                match_data = {'timestamp':{'$regex': '^' + date_only},"coinid":coin_id,"cameraname":camera_name,"status": { "$in": [None,1 ] }}
                find_data = list(coin_id_violation_data.find(match_data))
                if len(find_data) != 0:
                    count1 = 1 
                    dashdata =[]
                    for j , i in enumerate(find_data):
                        i['SNo'] = count1
                        dashdata.append(i)
                        count1 = count1 +1 
                    if len(dashdata) != 0 :
                        ret={"message":parse_json(find_data),"success":True}
                    else:
                        ret['message']= "data not found."
                    # ret={"message":parse_json(find_data),"success":True}
                else:
                    print("555 1")
                    ret['message'] = "for the given parameters there is no violation data."
        else:
            ret['message'] =" ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)

# @camera_coin.route('/getviolationvideo/<video_name>', methods=['GET'])
@csrf_exempt
def CoinviolationVideo(request,video_name = None):
    ret = {"message":"something went wrong with GETCOINVIOLATIONVIDEO api ","success":False}
    if request.method == "GET":
        if video_name is not None:
            match_data = {"video_name":video_name}
            video_data  = coin_id_violation_data.find_one(match_data)
            if video_data is not None:
                print("hello coming video")
                try:
                    #base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'RIRO_merged_imgs')
                # return send_from_directory(base_path, image_file)
                    base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'sm_rec')#os.path.join(os.getcwd(), 'smaple_files')#os.path.basename('add_camera_sample.xlsx')#
                    file_path = os.path.basename(video_name)
                    response = send_from_directory(base_path, file_path, as_attachment=True)
                    return response
                except Exception as  error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] camera_coin_apis -- GETCOINVIOLATIONVIDEO 1", str(error), " ----time ---- ", now_time_with_time()]))
                    ret['message'] =str(error)   
                    return ret
                    
            else:
                ret['message'] = "video data is not found."
                #{"message":"video data is not found.","success":False}
        else:
            ret['message'] = "video file name is not, please give proper one."
    return JsonResponse(ret)


# @camera_coin.route('/getcoinidlist', methods=['GET'])
@csrf_exempt
def COinidlist(request):
    ret = {"message":"something went wrong with getcoinidlist api ","success":False}
    if request.method == "GET":
        match_data = {"alarm_type":"sensegiz","camera_status":True,"coin_details": { "$exists": True, "$not": {"$size": 0} } }
        data = list(ppera_cameras.aggregate([{'$match': match_data},{'$group':{'_id':{'coindata': '$coin_details.coin_id'}, 'all_data':{'$first': '$$ROOT'}}},{'$limit': 4000000}]))
        dash_data = []
        if len(data) != 0:
            for count, i in enumerate(data):
                if len(i['all_data']['coin_details']) !=0:
                    for kk, coinid in enumerate(i['all_data']['coin_details']):
                        if coinid['coin_id']  not in dash_data:
                            dash_data.append(coinid['coin_id'])
            if len(dash_data) != 0:
                ret = {'success': True, 'message': dash_data}
            else:
                ret['message'] = 'data not found'
        else:
            ret['message'] = 'data not found'
    return JsonResponse(ret)


# @camera_coin.route('/getcoinidcameralist', methods=['GET'])
@csrf_exempt
def getcoinidcameralist(request):
    ret = {"message":"something went wrong with getcoinidlist api ","success":False}
    if request.method == "GET":
        match_data = {"alarm_type":"sensegiz","camera_status":True,"coin_details": { "$exists": True, "$not": {"$size": 0} } }
        data = list(ppera_cameras.aggregate([{'$match': match_data},{'$group':{'_id':{'cameraname': '$cameraname'}, 'all_data':{'$first': '$$ROOT'}}},{'$limit': 4000000}]))
        dash_data = []
        if len(data) != 0:
            for count, i in enumerate(data):
                if len(i['all_data']) !=0:
                    if i['all_data']['cameraname']  not in dash_data:
                        dash_data.append(i['all_data']['cameraname'])
            if len(dash_data) != 0:
                ret = {'success': True, 'message': dash_data}
            else:
                ret['message'] = 'data not found'
        else:
            ret['message'] = 'data not found'
    return JsonResponse(ret)

    

# @camera_coin.route('/get_samplefileFORCHECKCAMERA', methods=['GET'])
@csrf_exempt
def get_obj_img(request):
    ret = {"message":"something went wrong with get_obj_img api ","success":False}
    if request.method == "GET":
        try:
            base_path = os.path.join(os.getcwd(), 'smaple_files')
            file_path = os.path.basename('add_camera_sample.xlsx')
            ret = send_from_directory(base_path, file_path, as_attachment=True)
            # return response
        except Exception as  error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] camera_coin_apis -- get_samplefileFORCHECKCAMERA 1", str(error), " ----time ---- ", now_time_with_time()]))      
            ret=str(error)
    return JsonResponse(ret)
    

# @camera_coin.route('/add_firesmoke', methods=['POST'])
@csrf_exempt
def add_firesmoke(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'firesmoke_data', 'ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                firesmoke_data = data['firesmoke_data']
                ai_solutions = data['ai_solutions']
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if firesmoke_data is not None:
                        if type(firesmoke_data) == list:
                            if len(firesmoke_data) != 0:
                                if "firesmoke_data" in finddata:
                                    if firesmoke_data == finddata['firesmoke_data']:
                                        ret['message'] = 'fire and smoke data same as previous data.'
                                    else:
                                        if ai_solutions is not None:
                                            if isEmpty(ai_solutions) :
                                                finddata['ai_solution'].update(ai_solutions)
                                                result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'firesmoke_data': firesmoke_data,'ai_solution': finddata['ai_solution']}}))
                                                if result.modified_count > 0:
                                                    ret = {'message': 'firesmoke_data added successfully.','success': True}
                                                else:
                                                    ret['message'] = 'firesmoke_data not adeed.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions.'
                                else:
                                    if ai_solutions is not None:
                                        if isEmpty(ai_solutions) :
                                            finddata['ai_solution'].update(ai_solutions)
                                            result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'firesmoke_data': firesmoke_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'firesmoke_data added successfully.','success': True}
                                            else:
                                                ret['message'] = 'firesmoke_data not adeed.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions.'                                
                            else:
                                ret['message'] = 'please give proper input data, try once again.'
                        else:
                            ret['message'] = 'please give proper fire and smoke data, it should be list type.'
                    else:
                        ret['message'] = 'please give proper fire and smoke data, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)

