from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.final_ping import *



def FETCHFIREANDSMOKEDATAFROMMONGO():
    data = []#pictures: { $exists: true, $type: 'array', $ne: [] }
    # fetch_require_data = list(mongo.db.ppera_cameras.find({'camera_status': True, "analytics_status": 'true', "$where":"firesmoke_data.length > 0"}))
    fetch_require_data = list(mongo.db.ppera_cameras.find({'camera_status': True, "analytics_status": 'true','firesmoke_data.roi_parameters':{'$exists':True,"$ne": []}}))
    if len(fetch_require_data) != 0:
        for i in fetch_require_data:
            J={}
            if ENABLED_SOLUTION_IS_EMPTY_DICT(i['firesmoke_data']):
                # print('----------------------i--------------------',i['firesmoke_data'])
                if 'roi_parameters' in i['firesmoke_data']:
                    # print("000000000000000000000000000000000-000000000000000",i['firesmoke_data']['roi_parameters'])
                    roi_parameters = i['firesmoke_data']['roi_parameters']
                    if len(roi_parameters) !=0:  
                        J['firesmoke_data']=i['firesmoke_data']                      
                        for indexnumber , Roivalues in enumerate(roi_parameters):
                            # print('-----------Roivalues-------------',Roivalues)
                            if 'camera_type' in Roivalues:
                                J['camera_type'] = Roivalues['camera_type']
                                break
                    if 'camera_type' not in J['camera_type'] :
                        J['camera_type']=''

                            
                    
                
            # if i['firesmoke_data'][0]['fire'] != False or i['firesmoke_data'][0]['smoke'] != False or i['firesmoke_data'][0]['dust']:
            #     J['firesmoke_data']=i['firesmoke_data']
            #     if 'camera_type' in i['firesmoke_data'][0]:
            #         J['camera_type'] = i['firesmoke_data'][0]['camera_type']
            #     else:
            #         J['camera_type'] = ''
            # elif  i['firesmoke_data'][0]['dust'] != False :
            #     J['firesmoke_data']=i['firesmoke_data']
            #     if 'camera_type' in i['firesmoke_data'][0]:
            #         J['camera_type'] = i['firesmoke_data'][0]['camera_type']
            #     else:
            #         J['camera_type'] = ''
            if ENABLED_SOLUTION_IS_EMPTY_DICT(J) :
                J['cameraname']=i['cameraname']
                J['alarm_type']=i['alarm_type']
                J['alarm_version']=i['alarm_version']
                J['alarm_ip_address']=i['alarm_ip_address']
                J['rtsp_url']=i['rtsp_url']
                data.append(J)
    return data


def FIRESMOKEdumpvoiceannaoumentdataintodatatable(getdata_response):
    # mongo.db.voice_announcement_status.delete_many({"violation_type":"VPMS"})
    if "voice_announcement_status" not in mongo.db.list_collection_names():
        print("Collection 'voice_announcement_status' does not exist-VPMS")
        # raise Exception("Collection 'voice_announcement_status' does not exist")
    else:
        mongo.db.voice_announcement_status.delete_many({"violation_type": { "$in": ["FSD"] }})
    for i , j in enumerate(getdata_response):

        if len(j['firesmoke_data']) !=0:
            FSDAreadata = j['firesmoke_data']['roi_parameters']
            insertvoice_dataFSD = []
            for roiindex , roivalues in enumerate(FSDAreadata):
                print('------roivalues-------------',roivalues)
                if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
                    if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
                            if roivalues['full_frame']==True:
                                insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'fullframe','violation_type':'FSD','violation_time':None,'valid_time':None,'roi_name':'fullframe'}
                                if insertvalue  not in insertvoice_dataFSD:
                                    insertvoice_dataFSD.append(insertvalue)
                            else:
                                if len(roivalues['label_name'])>1:
                                    labels_to_check=  ['fire','smoke','dust']
                                    labels_to_check1=  ['fire','smoke']
                                    labels_to_check2=  ['smoke','dust']
                                    labels_to_check3=  ['fire','dust']
                                    threecommon_labels = [label for label in roivalues['label_name'] if label in labels_to_check]
                                    threecommon_labels1 = [label for label in roivalues['label_name'] if label in labels_to_check1]
                                    threecommon_labels2 = [label for label in roivalues['label_name'] if label in labels_to_check2]
                                    threecommon_labels3 = [label for label in roivalues['label_name'] if label in labels_to_check3]
                                    if threecommon_labels:
                                        insertvalue1 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'fire','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        insertvalue2 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'smoke','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        insertvalue3 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'dust','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        if insertvalue1  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue1)
                                        if insertvalue2  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue2)
                                        if insertvalue3  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue3)
                                    elif threecommon_labels1:
                                        insertvalue1 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'fire','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        insertvalue2 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'smoke','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        if insertvalue1  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue1)
                                        if insertvalue2  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue2)                                   
                                    

                                    elif threecommon_labels2:
                                        insertvalue2 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'smoke','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        insertvalue3 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'dust','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        if insertvalue1  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue1)
                                        if insertvalue2  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue2)
                                        if insertvalue3  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue3)

                                    elif threecommon_labels3:
                                        insertvalue1 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'fire','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        insertvalue2 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'smoke','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        insertvalue3 = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'dust','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                        if insertvalue1  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue1)
                                        if insertvalue2  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue2)
                                        if insertvalue3  not in insertvoice_dataFSD:
                                            insertvoice_dataFSD.append(insertvalue3)

                                else:
                                    insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'FSD','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                    if insertvalue  not in insertvoice_dataFSD:
                                        insertvoice_dataFSD.append(insertvalue)

            if len(insertvoice_dataFSD) !=0:
                mongo.db.voice_announcement_status.insert_many(insertvoice_dataFSD)


def FIRESMOKECONFIG(media,data_save_interval):
    ret = {'message': 'something went wrong with create config update_cam_id__.', 'success': False}
    getdata_response = FETCHFIREANDSMOKEDATAFROMMONGO()
    if len(getdata_response) != 0:
        FIRESMOKEdumpvoiceannaoumentdataintodatatable(getdata_response)
        function__response = WRITEFIRESMOKEMULTICONFIG(getdata_response,media,data_save_interval)
        # return_data_update_camera = UPdatemulticonfigCamid(function__response)
        return_data_update_camera ='200'
        if return_data_update_camera == '200':
            ret = { 'message': 'fire and smoke application is started successfully.', 'success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'please enable and add the ai analytics solutions.'
    return ret

def checkNegativevaluesinBbox(text):
    try:
        values = text.split(';')
        processed_values = [str(max(int(value) if value else 0, 0)) for value in values]
        
        if not processed_values or (processed_values[-1] == '0' and not values[-1]):
            # If the last value is either an empty string or '0', remove it
            processed_values.pop()
        
        result = ';'.join(processed_values)
    except:
        result = text
    return result


def FireANDSMOKeCAMERASTATUSUPDATE(parameter):
    print("hello====",parameter)
    if parameter['camera_type'] == 'ptz':
        mongo.db.firesmokecamerastatus.insert_one({"camera_status":0,"location":parameter['firesmoke_data'][0]['presets'][0]['presetlocation'],'camera_rtsp':parameter['rtsp_url']})
    elif parameter['camera_type'] == 'bullet':
        mongo.db.firesmokecamerastatus.insert_one({"camera_status":0,"location":parameter['cameraname'],'camera_rtsp':parameter['rtsp_url']})
    database_detail = {'firesmoketable':'camera_status', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =False
    conn = None
    # if 1:
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    tablecreatequery = '''
    CREATE TABLE IF NOT EXISTS camera_status ( id SERIAL PRIMARY KEY, camera_name text, camera_id integer, camera_rtsp text, location text, camera_status integer , camera_type text 
                                                ); 
                                                '''
    try:
        cursor.execute(tablecreatequery)
        conn.commit() 
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
        
    if 1:        
    # try:
        cursor.execute('SELECT * FROM ' + database_detail['firesmoketable'] + ' ORDER BY id desc')
        camerastausdetails = list(cursor.fetchall())
        cols_name = list(map(lambda x: x[0], cursor.description))
        print("columns names==",cols_name)
        if len(camerastausdetails) !=0 :
            print("")
            print("got the data coming inside===",camerastausdetails)
            for i, eachdata in enumerate(camerastausdetails):
                resere = dict(zip(cols_name,eachdata))
                print('newerrerwewre==',resere)
                res = dict(zip(cols_name, eachdata))
                print('EACHDATA===',eachdata)
                if res['camera_rtsp'] == parameter['rtsp_url']:
                    update_data_query =''#''' UPDATE camera_status SET camera_status = %d camera_id =%d location=%s WHERE id = %s;  '''
                    new_status= ''
                    if parameter['camera_type'] == 'ptz':
                        update_data_query = '''UPDATE camera_status SET camera_status = %s, camera_id = %s, location = %s ,camera_type = %s WHERE id = %s;'''
                        new_status = (0, parameter['cameraid'], parameter['firesmoke_data'][0]['presets'][0]['presetlocation'],parameter['camera_type'])
                    else:
                        update_data_query = '''UPDATE camera_status SET camera_status = %s, camera_id = %s ,camera_type = %s WHERE id = %s;'''
                        new_status = (0, parameter['cameraid'],str(parameter['camera_type']))
                    cursor.execute(update_data_query, new_status + (res['id'],))
                    conn.commit() 
                    license_status = True  
                else:
                    print("camerastausdetails==",camerastausdetails)
                    if any(parameter['rtsp_url'] == tpl[3] for tpl in camerastausdetails):#any(parameter['rtsp_url'] == tpl for tpl in camerastausdetails):
                    # if any(parameter['rtsp_url'] in tpl for tpl in camerastausdetails):
                        print("-------------------------------",camerastausdetails)
                        print("===========",parameter['firesmoke_data'][0]['presets'][0]['presetlocation'])
                        if parameter['camera_type'] == 'ptz':
                            insert_data_query = '''INSERT INTO camera_status ( camera_name, camera_id, camera_rtsp, location, camera_status,camera_type ) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;'''
                            data_to_insert = (parameter['cameraname'], parameter['cameraid'],parameter['rtsp_url'],parameter['firesmoke_data'][0]['presets'][0]['presetlocation'],0,parameter['camera_type'])
                            cursor.execute(insert_data_query, data_to_insert)
                            conn.commit()
                            inserted_id = cursor.fetchone()[0]
                            if inserted_id is not  None:
                                license_status = True
                            print(f'Data inserted with ID: {inserted_id}')
                        elif  parameter['camera_type'] == 'bullet':
                            insert_data_query = '''INSERT INTO camera_status ( camera_name, camera_id, camera_rtsp, location, camera_status,camera_type ) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;'''
                            data_to_insert = (parameter['cameraname'], parameter['cameraid'],parameter['rtsp_url'],parameter['cameraname'],0,parameter['camera_type'])
                            cursor.execute(insert_data_query, data_to_insert)
                            conn.commit()
                            inserted_id = cursor.fetchone()[0]
                            if inserted_id is not  None:
                                license_status = True
                            print(f'Data inserted with ID: {inserted_id}')
                    else:
                        # cursor.execute('SELECT * FROM ' + database_detail['firesmoketable'] + ' WHERE camera_rtsp = %s ;', str(parameter['rtsp_url'])) #WHERE camera_rtsp = %s;'''
                        cursor.execute('SELECT * FROM ' + database_detail['firesmoketable'] + ' WHERE camera_rtsp = %s;', (parameter['rtsp_url'],))
                        AGIANFIND = cursor.fetchone()
                        if AGIANFIND is None  :
                            if  parameter['camera_type'] == 'ptz': 
                                insert_data_query = '''INSERT INTO camera_status ( camera_name, camera_id, camera_rtsp, location, camera_status,camera_type ) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;'''
                                data_to_insert = (parameter['cameraname'], parameter['cameraid'],parameter['rtsp_url'],parameter['firesmoke_data'][0]['presets'][0]['presetlocation'],0,parameter['camera_type'])
                                cursor.execute(insert_data_query, data_to_insert)
                                conn.commit()
                                inserted_id = cursor.fetchone()[0]
                                if inserted_id is not  None:
                                    license_status = True
                            elif  parameter['camera_type'] == 'bullet':
                                insert_data_query = '''INSERT INTO camera_status ( camera_name, camera_id, camera_rtsp, location, camera_status,camera_type ) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;'''
                                data_to_insert = (parameter['cameraname'], parameter['cameraid'],parameter['rtsp_url'],parameter['cameraname'],0,parameter['camera_type'])
                                cursor.execute(insert_data_query, data_to_insert)
                                conn.commit()
                                inserted_id = cursor.fetchone()[0]
                                if inserted_id is not  None:
                                    license_status = True
                                
                        print("camera already add-----")
        else:
            if  parameter['camera_type'] == 'ptz':  
                print("there is not data found..====",parameter)
                insert_data_query = '''INSERT INTO camera_status ( camera_name, camera_id, camera_rtsp, location, camera_status ,camera_type) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;'''
                data_to_insert = (parameter['cameraname'], parameter['cameraid'],parameter['rtsp_url'],parameter['firesmoke_data'][0]['presets'][0]['presetlocation'],0,parameter['camera_type'])
                cursor.execute(insert_data_query, data_to_insert)
                conn.commit()
                inserted_id = cursor.fetchone()[0]
                if inserted_id is not  None:
                    license_status = True
                print(f'Data inserted with ID: {inserted_id}')  
            elif  parameter['camera_type'] == 'bullet': 
                insert_data_query = '''INSERT INTO camera_status ( camera_name, camera_id, camera_rtsp, location, camera_status ,camera_type) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;'''
                data_to_insert = (parameter['cameraname'], parameter['cameraid'],parameter['rtsp_url'],parameter['cameraname'],0,parameter['camera_type'])
                cursor.execute(insert_data_query, data_to_insert)
                conn.commit()
                inserted_id = cursor.fetchone()[0]
                if inserted_id is not  None:
                    license_status = True
                print(f'Data inserted with ID: {inserted_id}')
    # except psycopg2.errors.UndefinedTable as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    # except psycopg2.errors.InFailedSqlTransaction as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
    cursor.close()
    conn.close()
    return license_status
    
    
def Truncatefiresmokecamera():
    database_detail = {'firesmoketable':'camera_status', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =False
    conn = None
    # if 1:
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    TruncateQuery = '''TRUNCATE TABLE camera_status ; '''
    try:
        cursor.execute(TruncateQuery)
        conn.commit() 
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
    cursor.close()
    conn.close()
    


def WRITEFIRESMOKEMULTICONFIG(response,media,data_save_interval):
    # print("------------------------response---------------------",response)
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
    batch_pushouttime = 40000
    drop_frame_interval=1
    ticket_reset_time =10
    gridview_true = True
    numberofsources_= 4
    rtsp_reconnect_interval = 3
    displayfontsize = 12
    display_tracker =True

    firesmokemodeltype = 'int8'
    modelthreshold = getthreshholdmodelconfig_details()
    firesmokedust_threshold = '0.3'
    if modelthreshold is not None:
        if len(modelthreshold['threshold']) !=0:
            for new,classname in enumerate(modelthreshold['threshold']):
                if classname['class']=='fire_smoke_dust':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            firesmokedust_threshold = int(classname['value'])/100
                            if firesmokedust_threshold==1:
                                firesmokedust_threshold ='0.9'
                        else:
                            firesmokedust_threshold = '0.2'           
                


    if ('drop_frame_interval' in Genral_configurations and Genral_configurations['drop_frame_interval'] is not None) and ('camera_fps' in Genral_configurations and  Genral_configurations['camera_fps'] is not None) :
        camera_fps = Genral_configurations['camera_fps']
        drop_frame_interval = Genral_configurations['drop_frame_interval']
        Newpushouttime = math.ceil(int(camera_fps)/int(drop_frame_interval))
        batch_pushouttime= math.ceil(1000000/Newpushouttime)
    
    if ('rtsp_reconnect_interval' in Genral_configurations and Genral_configurations['rtsp_reconnect_interval'] is not None):
        rtsp_reconnect_interval = Genral_configurations['rtsp_reconnect_interval'] 
    

    if ('grid_view' in Genral_configurations and Genral_configurations['grid_view'] is not None):
        gridview_true = Genral_configurations['grid_view'] 
    if ('grid_size' in Genral_configurations and Genral_configurations['grid_size'] is not None):
        numberofsources_ = int(Genral_configurations['grid_size'])


    if ('ticket_reset_time' in Genral_configurations and Genral_configurations['ticket_reset_time'] is not None):
        ticket_reset_time = int(Genral_configurations['ticket_reset_time'])
    if 'display_font_size' in Genral_configurations :
        displayfontsize = Genral_configurations['display_font_size']

    if 'display_tracker' in Genral_configurations :
        display_tracker = Genral_configurations['display_tracker']


    if "modelconfigurations" not in mongo.db.list_collection_names():
        print("Collection 'modelconfigurations' does not exist")

    else:
        print("modelconfigurations------------------exist----------")
        modelconfiguration = mongo.db.modelconfigurations.find_one()
        if modelconfiguration is not None:
            print('------------------modelconfiguration-------------------',modelconfiguration)
            if 'fire_smoke_dust_modal_type' in modelconfiguration:
                firesmokemodeltype= modelconfiguration['fire_smoke_dust_modal_type']



    



    allWrittenSourceCAmIds =[]
    numberofsources_= 4
    new_response = split_list(response,numberofsources_)
    camera_id =1 
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'firesmokesampleconfig.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/fire_and_smoke'+'/configs'
    yolo_config_path = get_current_dir_and_goto_parent_dir() + '/models/fsd'
    traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models/fsd/engine'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)
    if not os.path.exists(yolo_config_path):
        os.makedirs(yolo_config_path)
    if not os.path.exists(traffic_config_path):
        os.makedirs(traffic_config_path)         
    remove_text_files(deepstream_config_path)   
    # print("------------------------new_response-----------",new_response)  
    for config_index, writingresponse in enumerate(new_response):  
        config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
        configanalytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
        fsd_configfile = os.path.join(deepstream_config_path, 'fsd_custom_{0}.txt'.format(config_index+1))
        lines = [ '']
        normal_config_file = 0
        fsdline =[]
        analyticsdetailsline = []
        print("length == === 1", len(writingresponse))
        with open(sample_config_file) as file:
            for write_config, line in enumerate(file):
                if line.strip() == '[application]':
                    lines.append('[application]')
                    lines.append('enable-perf-measurement=1')
                    lines.append('perf-measurement-interval-sec=5\n')
                elif line.strip() == '[tiled-display]':
                    finaL_RA_PPE = writingresponse
                    total_stream_for_stremux_union = finaL_RA_PPE
                    rows,columns = get_layout(total_stream_for_stremux_union)
                    lines.append('[tiled-display]')
                    lines.append('enable=1')
                    lines.append('rows={0}'.format(str(rows)))
                    lines.append('columns={0}'.format(str(columns)))
                    lines.append('width=1280')
                    lines.append('height=720')
                    lines.append('gpu-id=0')
                    lines.append('nvbuf-memory-type=0\n')
                elif line.strip() == '[sources]': 
                    print("newlength===2", len(writingresponse))
                    analyticsdetailsline.append('[property]')
                    analyticsdetailsline.append('enable=1')
                    analyticsdetailsline.append('config-width=960')
                    analyticsdetailsline.append('config-height=544')
                    analyticsdetailsline.append('osd-mode=2')
                    analyticsdetailsline.append(f'display-font-size={displayfontsize}\n')
                    for n, x in enumerate(writingresponse):
                        print("-----------------------x-------------------firesmokeconfig-1",x)
                        cam_id = '{0}'.format(int(n))
                        firesmokehooterconfiguration = {"enable":1, "metadata":[{"enable":1, "ip":None, "details":[], "hooter-stop-buffer-time":3, "hooter-shoutdown-time":8 }] }
                        hooteripstring = '['
                        hootermetadata = '['
                        hooterip = None
                        relayip = None
                        find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                        if find_data is not None:
                            if find_data['rtsp_flag'] == '1':
                                if 'rtsp' in x['rtsp_url']:
                                    x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                        if ENABLED_SOLUTION_IS_EMPTY_DICT(x['firesmoke_data']):
                            Camerawiselabels =[]
                            if 'roi_parameters' in x['firesmoke_data']:
                                roi_parameters = x['firesmoke_data']['roi_parameters']
                                # print('=----------------roi_parameters------',x)
                                hooter_list_type =[]                                 
                                FSdstring = '['  
                                analyticsdetailsline.append('[roi-filtering-stream-{0}]'.format(normal_config_file))                                   
                                for labelindex , labelvalue in enumerate(roi_parameters):
                                    # print('=================labelvalue==========',labelvalue)
                                    print("============================labelvalue['alarm_type']============",labelvalue['alarm_type'])
                                    #{"enable":1, "metadata":[{"enable":1, "ip":"192.168.1.240", "details":[{"hooter-type":1, "Roi_name":"Area2", "channel":"null"}], "hooter-stop-buffer-time":3, "hooter-shoutdown-time":8 }] }
                                    if isEmpty(labelvalue['alarm_type']):                                        
                                        if hooteripstring != '[' :
                                            if labelvalue['alarm_type']['hooter'] or  labelvalue['alarm_type']['relay']  : 
                                                hooteripstring= hooteripstring+'['
                                        if labelvalue['alarm_type']['hooter']  == True and labelvalue['alarm_type']['relay'] == True :
                                            print("fire smoke both relay and hooter-------------")
                                            print("both relay and hooter-------------")
                                            if     x['alarm_version']['hooter'] =='old' and x['alarm_version']['relay'] =='old' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(0)                                     
                                                    else:
                                                        hooter_list_type.append(0) 
                                            elif  x['alarm_version']['hooter'] =='new'  and x['alarm_version']['relay'] =='new'   :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(3)                                     
                                                    else:
                                                        hooter_list_type.append(2) 
                                            elif   x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type1'   :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(0)                                     
                                                    else:
                                                        hooter_list_type.append(0)                              
                                            elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type2' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(3)  
                                                    if  x['alarm_ip_address']['hooter_ip'] is not None :
                                                        hooter_list_type.append(1) 
                                                    if  x['alarm_ip_address']['relay_ip'] is not None :
                                                        hooter_list_type.append(2) 

                                            elif  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='new' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(0) 

                                            elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='old' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(1) 

                                            elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type2' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(0)  

                                            elif x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type2':
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(0)  

                                            elif   x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type2' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(4)  
                                            elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type3'  :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(1)  

                                            elif x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type1' :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(4)  
                                            elif  x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type3'    :
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                                    if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                                        hooter_list_type.append(0)                     
                                        elif labelvalue['alarm_type']['hooter'] :
                                            print(" hooter-------------")
                                            if  x['alarm_version']['hooter'] =='old':
                                                hooter_list_type.append(0)
                                            elif   x['alarm_version']['hooter'] =='new':
                                                hooter_list_type.append(1)
                                            elif   x['alarm_version']['hooter'] =='type1':
                                                hooter_list_type.append(0)
                                            elif   x['alarm_version']['hooter'] =='type2':
                                                hooter_list_type.append(1)
                                            elif   x['alarm_version']['hooter'] =='type3':
                                                hooter_list_type.append(1)
                                        elif labelvalue['alarm_type']['relay']:
                                            print(" relay-------------")
                                            if  x['alarm_version']['relay'] =='old':
                                                hooter_list_type.append(0)
                                            elif   x['alarm_version']['relay'] =='new':
                                                hooter_list_type.append(2)
                                            elif   x['alarm_version']['relay'] =='type1':
                                                hooter_list_type.append(0)
                                            elif   x['alarm_version']['relay'] =='type2':
                                                hooter_list_type.append(2)
                                            elif   x['alarm_version']['relay'] =='type3':
                                                hooter_list_type.append(4)
                                        if labelvalue['alarm_type']['hooter']==True and labelvalue['alarm_type']['relay']==True:
                                            if isEmpty(x['alarm_ip_address']):
                                                if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:                                                    
                                                    if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                                        if x['alarm_version']['relay'] =='type3':
                                                            if 'channel' in labelvalue['alarm_type']:
                                                                channel = 'OUT'+str(labelvalue['alarm_type']['channel'])
                                                                hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "{channel}"}'
                                                            elif  x['alarm_version']['relay'] =='type3':
                                                                channel = 'OUT'+str(1)
                                                                hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "{channel}"}'
                                                            else:
                                                                hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}'
                                                        else:
                                                            hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}'
                                                    else:
                                                        if x['alarm_version']['relay'] =='type3':
                                                            if 'channel' in labelvalue['alarm_type']:
                                                                channel = 'OUT'+str(labelvalue['alarm_type']['channel'])
                                                                hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "{channel}"}'
                                                            elif x['alarm_version']['relay'] =='type3':
                                                                channel = 'OUT'+str(1)
                                                                hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "{channel}"}'
                                                            else:
                                                                hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}'
                                                        else:
                                                            hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}'
                            
                                        elif labelvalue['alarm_type']['hooter']==True :
                                            if isEmpty(x['alarm_ip_address']):
                                                if x['alarm_ip_address']['hooter_ip'] is not None :
                                                    hooterip = x['alarm_ip_address']['hooter_ip']
                                                    print('---------------2',x['alarm_ip_address']['hooter_ip'])
                                                    print("--------------2 roi hooter_list_type ==", hooter_list_type)
                                                    hooter_type_combined = int("".join(map(str, hooter_list_type)))
                                                    hooteripstring += f'{{"hooter-type": {hooter_type_combined}, "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}}'

                                                    # hooteripstring += f'{{"hooter-type": {hooter_list_type}, "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}}'

                                                    # hooteripstring += f'{{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}}'   
                                                    
                                        elif labelvalue['alarm_type']['relay']==True :
                                            if isEmpty(x['alarm_ip_address']):
                                                if x['alarm_ip_address']['relay_ip'] is not None :
                                                    relayip = x['alarm_ip_address']['hooter_ip']
                                                    if x['alarm_version']['relay'] =='type3':
                                                        if 'channel' in labelvalue['alarm_type']:
                                                            channel = 'OUT'+str(labelvalue['alarm_type']['channel'])
                                                            hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "{channel}"}'
                                                        elif x['alarm_version']['relay'] =='type3':
                                                            channel = 'OUT'+str(1)
                                                            hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "{channel}"}'
                                                        else:
                                                            hooteripstring += f'{"hooter-type": "{ "".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}' 
                                                    else:
                                                        hooteripstring += f'{"hooter-type": "{"".join(hooter_list_type)}", "Roi_name": "{labelvalue["roi_name"] if labelvalue["roi_name"] else "null"}", "channel": "null"}'  
                                    if hooteripstring != '[':
                                        hooteripstring+=']'
                                    print('--------------------------hooteripstring------1..1.1.1--------------------------------------------------------',hooteripstring)
                                    
                                    
                                    
                                    roi_bbox= checkNegativevaluesinBbox(labelvalue['bb_box'])                                                                      
                                    print('{"ROI": "%s", "label": "%s;"}' % (labelvalue['roi_name'],';'.join(labelvalue['label_name'])))
                                    for label in labelvalue['label_name']:
                                        # if label in ['dust','smoke']:
                                        #     label ='smoke/dust'
                                        if label not in Camerawiselabels:
                                            Camerawiselabels.append(label)
                                    if FSdstring != '[' :
                                        label_names = ['smoke/dust' if label in ['dust', 'smoke'] else label for label in labelvalue['label_name']]
                                        FSdstring= FSdstring+',{"ROI": "%s", "label": "%s"}' % (labelvalue['roi_name'],';'.join(labelvalue['label_name']) + ';')
                                        analyticsdetailsline.append('roi-fsd-{0} = {1}'.format(labelvalue['roi_name'], roi_bbox))  
                                    elif FSdstring == '[' :
                                        if 'full_frame' in labelvalue:
                                            if labelvalue['full_frame']== False:
                                                if labelvalue['roi_name']!='':
                                                    analyticsdetailsline.append('enable=1')
                                                    analyticsdetailsline.append('roi-fsd-{0} = {1}'.format(labelvalue['roi_name'], roi_bbox))  
                                                    label_names = ['smoke/dust' if label in ['dust', 'smoke'] else label for label in labelvalue['label_name']]
                                                    FSdstring= FSdstring+'{"ROI": "%s", "label": "%s"}' % (labelvalue['roi_name'],';'.join(labelvalue['label_name']) + ';')
                                                else:
                                                    analyticsdetailsline.append('enable=0')
                                                    label_names = ['smoke/dust' if label in ['dust', 'smoke'] else label for label in labelvalue['label_name']]
                                                    FSdstring= FSdstring+'{"ROI": "%s", "label": "%s"}' % ("NULL",';'.join(labelvalue['label_name']) + ';')
                                                    analyticsdetailsline.append('roi-fsd-{0} = {1}'.format('abc', '1;2;3;4')) 
                                                    break 
                                            else:
                                                analyticsdetailsline.append('enable=0')
                                                label_names = ['smoke/dust' if label in ['dust', 'smoke'] else label for label in labelvalue['label_name']]
                                                FSdstring= FSdstring+'{"ROI": "%s", "label": "%s"}' % ("NULL",';'.join(labelvalue['label_name']) + ';')
                                                analyticsdetailsline.append('roi-fsd-{0} = {1}'.format('abc', '1;2;3;4')) 
                                                break 
                                        else:
                                            if labelvalue['roi_name']!='':
                                                analyticsdetailsline.append('enable=1')
                                                analyticsdetailsline.append('roi-fsd-{0} = {1}'.format(labelvalue['roi_name'], roi_bbox))  
                                                label_names = ['smoke/dust' if label in ['dust', 'smoke'] else label for label in labelvalue['label_name']]
                                                FSdstring= FSdstring+'{"ROI": "%s", "label": "%s"}' % (labelvalue['roi_name'],';'.join(labelvalue['label_name']) + ';')
                                            else:
                                                analyticsdetailsline.append('enable=0')
                                                label_names = ['smoke/dust' if label in ['dust', 'smoke'] else label for label in labelvalue['label_name']]
                                                # joined_labels = ';'.join(labelvalue['label_name']).rstrip(';')
                                                FSdstring= FSdstring+'{"ROI": "%s", "label": "%s"}' % ("NULL",';'.join(labelvalue['label_name']) + ';')
                                                analyticsdetailsline.append('roi-fsd-{0} = {1}'.format('abc', '1;2;3;4')) 
                                                break 
                                    


                                
                                            
                                if FSdstring != '[':
                                    FSdstring=FSdstring+']'
                                analyticsdetailsline.append('inverse-roi=0')
                                analyticsdetailsline.append('class-id=0;1;2;3;7\n')
                            uri = x['rtsp_url']
                            lines.append('[source{0}]'.format(normal_config_file))
                            lines.append('enable=1')
                            lines.append('type=4')
                            lines.append('uri = {0}'.format(uri))
                            lines.append('num-sources=1')
                            lines.append('gpu-id=0')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('camera-id={0}'.format(camera_id))
                            camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                            allWrittenSourceCAmIds.append(camera_required_data)
                            lines.append('camera-name={0}'.format(x['cameraname']))
                            lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                            lines.append('drop-frame-interval = {0}'.format(drop_frame_interval))
                            bbox_entries = ','.join(['{"label": "%s", "min_bbox_w": 36, "min_bbox_h": 5, "max_bbox_w": 300, "max_bbox_h": 300}' % label for label in Camerawiselabels])
                            lines.append('#pre-process-bbox = [%s]' % bbox_entries)
                            lines.append('operate-on-class = {};\n'.format(';'.join(Camerawiselabels)))
                            fsdline.append('[fsd{0}]'.format(str(normal_config_file)))
                            if 'static_parameters' in x['firesmoke_data']:
                                staticparameters = x['firesmoke_data']['static_parameters']
                                fsdline.append('enable = 1')
                                if 'process_mode' in staticparameters:  
                                    fsdline.append('process-mode = {0}'.format(staticparameters['process_mode']))
                                else:
                                    fsdline.append('process-mode = {0}'.format('image'))

                                if 'frame-verification' in staticparameters:  
                                    fsdline.append('frame-verification = {0}'.format(staticparameters['frame-verification']))
                                else:
                                    fsdline.append('frame-verification = {0}'.format('10'))

                                if 'image_save_interval' in staticparameters:  
                                    fsdline.append('image-save-interval = {0}'.format(staticparameters['image_save_interval']))
                                else:
                                    fsdline.append('image-save-interval = {0}'.format('10'))

                                if 'analytics_event_stop_interval' in staticparameters:
                                    fsdline.append('Analytics_event_stop_interval = {0}'.format(staticparameters['analytics_event_stop_interval']))
                                else:
                                    fsdline.append('Analytics_event_stop_interval = {0}'.format('10'))
                                fsdline.append('store-image-data=1')                                
                                # fsdline.append('frame-verification= {0}'.format(10))
                                # fsdline.append('image-save-interval = {0}'.format(data_save_interval)) 
                                # fsdline.append('Analytics_event_stop_interval = {0}'.format(data_save_interval)) #                            
                            if Camerawiselabels != '' and Camerawiselabels is not None:
                                #'[{"ROI":"NULL", "label":"fire;smoke;dust;"}]'
                                fsdline.append('operate-on = %s' % FSdstring)
                                #fsdline.append('operate-on={0}'.format(labelnames)) 
                            else:
                                fsdline.append('operate-on=fire;') 



                            #{"enable":1, "metadata":[{"enable":1, "ip":"192.168.1.240", "details":[{"hooter-type":1, "Roi_name":"Area2", "channel":"null"}], "hooter-stop-buffer-time":3, "hooter-shoutdown-time":8 }] }
                            if hooteripstring != '[':
                                print('===============metadata=====',hooteripstring)
                                # if relayip is not None and hooterip is not None:
                                #     new = {"enable":1, "metadata":[{"enable":1, "ip":hooterip, "details":hooteripstring, "hooter-stop-buffer-time":3, "hooter-shoutdown-time":8 }] }
                            
                                #     fsdline.append(f'hooter-details={new}\n') 
                                # elif hooterip is not None:
                                #     new = {"enable":1, "metadata":[{"enable":1, "ip":hooterip, "details":hooteripstring, "hooter-stop-buffer-time":3, "hooter-shoutdown-time":8 }] }
                            
                                #     fsdline.append(f'hooter-details={new}\n') 
                                # elif relayip is not None:
                                #     new = {"enable":1, "metadata":[{"enable":1, "ip":hooterip, "details":hooteripstring, "hooter-stop-buffer-time":3, "hooter-shoutdown-time":8 }] }
                            
                                #     fsdline.append(f'hooter-details={new}\n')
                                print('-------------------hooteripstring----------',hooteripstring)
                                if relayip is not None and hooterip is not None:
                                    new = {
                                        "enable": 1,
                                        "metadata": [{
                                            "enable": 1,
                                            "ip": hooterip,
                                            "details":  json.loads(hooteripstring),  # Proper list structure
                                            "hooter-stop-buffer-time": 3,
                                            "hooter-shoutdown-time": 8
                                        }]
                                    }

                                    print('------------bothe fsd------------',new)
                                    json_string = json.dumps(new)
                                    print('------------bothe fsd------------',json_string)
                                    fsdline.append(f"hooter-details={json_string}\n")

                                elif hooterip is not None:
                                    new = {
                                        "enable": 1,
                                        "metadata": [{
                                            "enable": 1,
                                            "ip": hooterip,
                                            "details": json.loads(hooteripstring),  # Proper list structure
                                            "hooter-stop-buffer-time": 3,
                                            "hooter-shoutdown-time": 8
                                        }]
                                    }
                                    
                                    
                                    print('------------bothe fsd------------',new)
                                    json_string = json.dumps(new)
                                    print('------------bothe fsd------------',json_string)
                                    fsdline.append(f"hooter-details={json_string}\n")

                                elif relayip is not None:
                                    new = {
                                        "enable": 1,
                                        "metadata": [{
                                            "enable": 1,
                                            "ip": hooterip,
                                            "details": json.loads(hooteripstring),  # Proper list structure
                                            "hooter-stop-buffer-time": 3,
                                            "hooter-shoutdown-time": 8
                                        }]
                                    }

                                    print('------------bothe fsd------------',new)
                                    json_string = json.dumps(new)
                                    print('------------bothe fsd------------',json_string)
                                    fsdline.append(f"hooter-details={json_string}\n")
                                
                            
                             
                            
                            x['cameraid']=camera_id
                            FireANDSMOKeCAMERASTATUSUPDATE(x)
                            normal_config_file += 1
                            camera_id += 1
                elif line.strip() == '[sink0]':
                    lines.append('[sink0]')
                    lines.append('enable=1')
                    
                    if gridview_true is True:
                        lines.append('type=2')
                    else:
                        lines.append('type=1')
                    lines.append('sync=0')
                    lines.append('source-id=0')
                    lines.append('gpu-id=0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[osd]':
                    lines.append('[osd]')
                    lines.append('enable=1')
                    lines.append('gpu-id=0')
                    lines.append('border-width=1')
                    lines.append('text-size=15')
                    lines.append('text-color=1;1;1;1;')
                    lines.append('text-bg-color=0.3;0.3;0.3;1;')
                    lines.append('font=Arial')
                    lines.append('show-clock=0')
                    lines.append('clock-x-offset=800')
                    lines.append('clock-y-offset=820')
                    lines.append('clock-text-size=12')
                    lines.append('clock-color=1;0;0;0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[streammux]':
                    lines.append('[streammux]')
                    lines.append('gpu-id=0')
                    lines.append('live-source=0')
                    lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('batched-push-timeout=40000')
                    lines.append('width=1920')
                    lines.append('height=1080')
                    lines.append('enable-padding=0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[primary-gie]':
                    lines.append('[primary-gie]')
                    lines.append('enable=1')
                    lines.append('gpu-id=0')
                    lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('bbox-border-color0=1;0;0;1')
                    lines.append('bbox-border-color1=0;1;1;1')
                    lines.append('bbox-border-color2=0;1;1;1')
                    lines.append('bbox-border-color3=0;1;0;1')
                    lines.append('nvbuf-memory-type=0')
                    lines.append('interval=0')
                    lines.append('gie-unique-id=1')
                    # '{0}/models/fsd/engine/'.format(get_current_dir_and_goto_parent_dir())
                    lines.append('model-engine-file={0}/models/fsd/engine/model_b{1}_gpu0_{2}.engine'.format(get_current_dir_and_goto_parent_dir(),len(list(total_stream_for_stremux_union)),firesmokemodeltype))
                    modelconfigfile = 'config_infer_fsd_yoloV8_small'
                    lines.append('config-file=../../models/fsd/{0}_{1}.txt'.format(modelconfigfile,config_index+1) )                    
                    FIRESMOKEDUSTMODEL =[]
                    FIRESMOKEDUSTMODEL.append('[property]')
                    FIRESMOKEDUSTMODEL.append('gpu-id={0}'.format(0))
                    FIRESMOKEDUSTMODEL.append('batch-size=1')
                    FIRESMOKEDUSTMODEL.append('net-scale-factor=0.0039215697906911373')
                    FIRESMOKEDUSTMODEL.append('model-color-format=0')
                    FIRESMOKEDUSTMODEL.append('custom-network-config={0}/models/fsd/yolov8_bests.cfg'.format(get_current_dir_and_goto_parent_dir()))
                    enginFilePath = '{2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype)
                    if os.path.exists(enginFilePath):
                        # print("yolov3 EngineFIle exists.")
                        FIRESMOKEDUSTMODEL.append('#model-file={0}/models/fsd/yolov8_bests.wts'.format(get_current_dir_and_goto_parent_dir()))
                        FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype))
                    else:
                        # print("yolov3 EngineFIle does not exist.")
                        anotherenginFilePath = '{2}/fire_and_smoke/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype)
                        secondenginFilePath = '{2}/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype)
                        if os.path.exists(anotherenginFilePath):
                            print('----------------------')
                            destination= '{0}/models/fsd/engine/'.format(get_current_dir_and_goto_parent_dir())
                            
                            shutil.copy(anotherenginFilePath, destination)
                            if os.path.exists(enginFilePath):
                                print('----------------') 
                                FIRESMOKEDUSTMODEL.append('#model-file={0}/models/fsd/yolov8_bests.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype))
                            else:
                                FIRESMOKEDUSTMODEL.append('model-file={0}/models/fsd/yolov8_bests.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype))
                        elif os.path.exists(secondenginFilePath):
                            print('----------------------')
                            destination= '{0}/models/fsd/engine/'.format(get_current_dir_and_goto_parent_dir())
                            shutil.copy(secondenginFilePath, destination)
                            if os.path.exists(enginFilePath):
                                FIRESMOKEDUSTMODEL.append('#model-file={0}/models/fsd/yolov8_bests.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype))
                            else:
                                FIRESMOKEDUSTMODEL.append('model-file={0}/models/fsd/yolov8_bests.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype))
                        else:
                            FIRESMOKEDUSTMODEL.append('model-file={0}/models/fsd/yolov8_bests.wts'.format(get_current_dir_and_goto_parent_dir()))
                            FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/fsd/engine/model_b{0}_gpu{1}_{3}.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir(),firesmokemodeltype))
                        
                    FIRESMOKEDUSTMODEL.append('labelfile-path={0}/models/fsd/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                    FIRESMOKEDUSTMODEL.append('int8-calib-file={0}/models/fsd/calib.table'.format(get_current_dir_and_goto_parent_dir()))
                    FIRESMOKEDUSTMODEL.append('network-mode=1')
                    FIRESMOKEDUSTMODEL.append('num-detected-classes=3')
                    FIRESMOKEDUSTMODEL.append('interval=0')
                    FIRESMOKEDUSTMODEL.append('gie-unique-id=1')
                    FIRESMOKEDUSTMODEL.append('network-type=0')
                    FIRESMOKEDUSTMODEL.append('cluster-mode=2')
                    FIRESMOKEDUSTMODEL.append('maintain-aspect-ratio=1')
                    FIRESMOKEDUSTMODEL.append('symmetric-padding=1')
                    FIRESMOKEDUSTMODEL.append('parse-bbox-func-name=NvDsInferParseYolo')
                    FIRESMOKEDUSTMODEL.append('custom-lib-path=utils/libnvdsinfer_custom_impl_Yolo.so')
                    FIRESMOKEDUSTMODEL.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                    FIRESMOKEDUSTMODEL.append('[class-attrs-all]')
                    FIRESMOKEDUSTMODEL.append('nms-iou-threshold=0.1')
                    FIRESMOKEDUSTMODEL.append(f'pre-cluster-threshold={firesmokedust_threshold}')
                    FIRESMOKEDUSTMODEL.append('topk=300')
                    with open(get_current_dir_and_goto_parent_dir()+'/models/fsd/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                        for O_O_O, modelline in enumerate(FIRESMOKEDUSTMODEL):
                            f.write('%s\n' % modelline)

                elif line.strip() == '[tracker]':
                    lines.append('[tracker]')
                    lines.append('enable=1')
                    lines.append('tracker-width=960')
                    lines.append('tracker-height=544')
                    if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                        lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                    else:
                        shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                        lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                    if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                        lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                    else:
                        shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                        lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                    lines.append('gpu-id={0}'.format(0))
                    lines.append('#enable-batch-process=0')
                    if display_tracker :
                        lines.append('display-tracking-id=1')
                    else:
                        lines.append('display-tracking-id=0')
                    lines.append('user-meta-pool-size=64')

                elif line.strip() == '[nvds-analytics]':
                    lines.append('[nvds-analytics]')
                    lines.append('enable = 1')
                    lines.append('config-file = ./config_analytics_{0}.txt'.format(config_index+1))

                elif line.strip() == '[tests]':
                    lines.append('[tests]')

                elif line.strip() == '[application-config]':
                    lines.append('[application-config]')
                    lines.append('app-title = SafetyEye')
                    lines.append('image-save-path = images/frame\n')

                elif line.strip() == '[fsd]':
                    lines.append('[fsd]')
                    lines.append('enable=1')
                    lines.append('fsd-config-file=./fsd_custom_{0}.txt'.format(config_index+1))
                else:
                    lines.append(line.strip())  
        with open(config_file, 'w') as f:
            for O_O_O, item in enumerate(lines):
                f.write('%s\n' % item)

        with open(configanalytics_file, 'w') as analyticsFILE:
            for _1111, Newvlaues  in enumerate(analyticsdetailsline):
                analyticsFILE.write('%s\n' % Newvlaues)

        with open(fsd_configfile, 'w') as fsdfile:
            for jim in fsdline:
                fsdfile.write('%s\n' % jim)
    return allWrittenSourceCAmIds


def calculate_text_size(text, font):
    font_size = font
    text_width = font_size * len(text) // 2  # Adjust as needed for accurate width estimation
    text_height = font_size 
    return text_width, text_height    



def live_data_pagination(live_data_count, all_data):
    try:
        data = mongo.db.live_data_count.find_one()
        live_data_30 = []
        if data is not None:
            if int(data['live_data_count']) < int(live_data_count):
                live_data_30 = pagination_block(data['page_num'], data['page_limit'], all_data)
                live_data_30['previous_live_count'] = data['live_data_count']
                live_data_30['now_live_count'] = live_data_count
            else:
                live_data_30 = pagination_block(data['page_num'], data['page_limit'], all_data)
                live_data_30['previous_live_count'] = data['live_data_count']
                live_data_30['now_live_count'] = live_data_count
            data['live_data_count'] = live_data_count
            data['page_limit'] = data['page_limit']
            data['page_num'] = data['page_num']
            result = mongo.db.live_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.live_data_count.insert_one(dictionary)
            if result.acknowledged > 0:
                pass
            else:
                pass
            live_data_30 = pagination_block(dictionary['page_num'], dictionary['page_limit'], all_data)
            live_data_30['previous_live_count'] = 0
            live_data_30['now_live_count'] = live_data_count
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_paginqqqation 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30

def FireSmokecreate_chart(workbook, from_date, to_date, violation_types, list1):
    try:
        start_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date format! Please enter the date in 'YYYY-MM-DD HH:MM:SS' format.")
        return

    # Define header formats
    header_font = workbook.add_format({'bold': True, 'color': 'FFFFFF', 'bg_color': '4F81BD', 'size': '12'})
    border_style = workbook.add_format({'border': 1})

    # Initialize the structure to hold violation counts
    violations_by_date = defaultdict(lambda: defaultdict(int))  # For date-wise counting
    violations_by_date_hour = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # For timestamp-wise counting

    date_range_exceeds_three_days = (end_date - start_date).days > 3
    print("Date range exceeds three days:", date_range_exceeds_three_days)

    for v_type in violation_types:
        data = [
            record for record in list1 
            if ', '.join({obj["class_name"] for detail in record["analytics_details"]["details"]
                         for obj in detail["obj_details"]}) == v_type
        ]
        
        sheet_name = f"{v_type} Violation"

        # Check if the sheet already exists
        existing_sheets = [sheet.get_name() for sheet in workbook.worksheets_objs]
        if sheet_name in existing_sheets:
            continue  # Skip if the sheet already exists

        sheet = workbook.add_worksheet(sheet_name)

        # Create headers
        headers = ['Date' if date_range_exceeds_three_days else 'Timestamp'] + list(violation_types)
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, header_font)

        # Process the data
        for record in data:
            for detail in record['analytics_details']['details']:
                timestamp = detail.get('timestamp')
                if timestamp:
                    timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    if date_range_exceeds_three_days:
                        violation_date = timestamp_obj.date()
                        violations_by_date[violation_date][v_type] += 1
                    else:
                        violation_date = timestamp_obj.date()
                        violation_hour = timestamp_obj.hour
                        violations_by_date_hour[violation_date][violation_hour][v_type] += 1

        # Write the data to the sheet
        row_index = 1
        if date_range_exceeds_three_days:
            # Date-wise logic
            current_date = start_date.date()
            while current_date <= end_date.date():
                row = [str(current_date)]
                for violationType in violation_types:
                    count = violations_by_date[current_date].get(violationType, 0)
                    row.append(count)
                sheet.write_row(row_index, 0, row)
                row_index += 1
                current_date += timedelta(days=1)
        else:
            # Timestamp-wise logic
            current_time = start_date
            while current_time <= end_date:
                timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                row = [timestamp]
                for violationType in violation_types:
                    count = violations_by_date_hour[current_time.date()][current_time.hour].get(violationType, 0)
                    row.append(count)
                sheet.write_row(row_index, 0, row)
                row_index += 1
                current_time += timedelta(hours=1)

        # Calculate total violations for chart title
        if date_range_exceeds_three_days:
            total_violations = sum(
                sum(date_data.values()) for date_data in list(violations_by_date.values())
            )
        else:
            total_violations = sum(
                sum(hour.get(v_type, 0) for hour in date_data.values())
                for date_data in list(violations_by_date_hour.values())
            )

        # Create a bar chart
        chart = workbook.add_chart({'type': 'column'})
        chart.set_title({'name': f"{sheet_name} Total Counts: {total_violations}"})
        chart.set_x_axis({'name': 'Date' if date_range_exceeds_three_days else 'Violation Time'})
        chart.set_y_axis({'name': 'Detected Count'})
        chart.set_size({'width': 1100, 'height': 700})

        # Set ranges for the chart
        data_range = f"'{sheet_name}'!B2:B{row_index}"
        categories_range = f"'{sheet_name}'!A2:A{row_index}"

        # Add data to the chart
        chart.add_series({
            'name': f"{v_type} Violations",
            'categories': categories_range,
            'values': data_range,
            'data_labels': {'value': True}
        })

        # Insert the chart into the worksheet
        sheet.insert_chart(f"C2", chart)
        sheet.set_column(0, 0, 20)



def FSDcreatecamera_wisechart(workbook, list1, from_date, to_date, title="Camera-wise Violation Chart"):
    violations_by_camera = defaultdict(int)

    # Count violations by camera
    for record in list1:
        camera_name = record.get("camera_name", "Unknown Camera")
        violations_by_camera[camera_name] += 1

    # Create a worksheet and add chart data
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        # Headers
        sheet.write(0, 0, "Camera", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        # Populate data
        row_index = 1
        for camera, count in violations_by_camera.items():
            sheet.write(row_index, 0, camera)
            sheet.write(row_index, 1, count)
            row_index += 1

        # Add the column chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': "Violation Counts",
            'categories': f"'{sheet_name}'!A2:A{row_index}",
            'values': f"'{sheet_name}'!B2:B{row_index}",
            'data_labels': {'value': True}
        })
        chart.set_title({
            'name': f'Camera-wise Violation Counts\n({from_date} to {to_date})'
        })
        chart.set_x_axis({'name': 'Camera'})
        chart.set_y_axis({'name': 'Violation Count'})
        chart.set_size({'width': 1200, 'height': 600})  # Adjusted size

       
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)

def FSDcreatedepartment_wisechart(workbook, list1, from_date, to_date, title="Department-wise Violation Chart"):
    violations_by_department = defaultdict(int)

    # Count violations by department
    for record in list1:
        department = (
            record.get("department") or
            (record.get("camera_info", {}).get("department")) or
            "Unknown Department"
        )
        violations_by_department[department] += 1

    # Create a worksheet and add chart data
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        # Headers
        sheet.write(0, 0, "Department", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        # Populate data
        row_index = 1
        for department, count in violations_by_department.items():
            sheet.write(row_index, 0, department)
            sheet.write(row_index, 1, count)
            row_index += 1

        # Add the column chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': "Violation Counts",
            'categories': f"'{sheet_name}'!A2:A{row_index}",
            'values': f"'{sheet_name}'!B2:B{row_index}",
            'data_labels': {'value': True}
        })
        chart.set_title({
            'name': f'Department-wise Violation Counts\n({from_date} to {to_date})'
        })
        chart.set_x_axis({'name': 'Department'})
        chart.set_y_axis({'name': 'Violation Count'})
        chart.set_size({'width': 1200, 'height': 600})  # Adjusted size

        # Insert the chart in the sheet
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)




def FSDCREATE(list1,from_date, to_date):
    #print("list1 ===",list1)
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'firesmoke_violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:E', 30)
        worksheet.set_column('F:F', 43)
        worksheet.set_row(0, 100)
        worksheet.set_row(1,  20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(40)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        # worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        # worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/JSW_Group_Logo.jpg'), {'x_scale': 0.4, 'y_scale':0.2})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:F1', 'Violation Details', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(18)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        
        
        cell_format_7 = workbook.add_format()
        cell_format_7.set_bold()
        cell_format_7.set_font_color('white')
        cell_format_7.set_font_name('Calibri')
        cell_format_7.set_font_size(18)
        cell_format_7.set_align('center_across')
        cell_format_7.set_bg_color('#800080')        
        row = 1
        col = 0
        worksheet.write(row, col ,"Department Name" , cell_format_1)
        worksheet.write(row, col + 1, 'Camera Name', cell_format_1)
        worksheet.write(row, col + 2, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 4, 'Ended Time', cell_format_1)
        worksheet.write(row, col + 5, 'Violation', cell_format_1)
        cell_format_2 = workbook.add_format()
        cell_format_2.set_font_name('Calibri')
        cell_format_2.set_align('center_across')
        rows = 2
        cols = 0
        cols1 = 1
        cols2 = 2
        cols3 = 3
        cols4 = 4
        cols5 = 5
        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0
        
        df = pd.DataFrame(list1)
        # df = pd.DataFrame(list1)

        df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%d-%m-%Y')
        result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        result_dict = {
            'date': result_df['date'].tolist(),
            'cameraname': result_df['camera_name'].tolist(),
            'No of times': result_df['No of times'].tolist()
        }
        df = pd.DataFrame(result_dict)

        # df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
        # result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        # result_dict = {
        #     'date': result_df['date'].tolist(),
        #     'cameraname': result_df['camera_name'].tolist(),
        #     'No of times': result_df['No of times'].tolist()
        # }
        excel_file =filename# 'grouped_column.xlsx'
        sheet_name = 'sheet 2'

        df.to_excel(excel_file, sheet_name=sheet_name, index=False)
        for i in list1:
            # try:
                if cols == 0:
                    worksheet.write(rows, cols, i['department'], cell_format_2)
                if cols1 == 1:
                    worksheet.write(rows, cols1, i['camera_name'], cell_format_2)
                    
                    # worksheet.write(rows, cols1, i['analytics_details'], cell_format_2)                
                if cols2 == 2:
                    class_names = {obj["class_name"] for detail in i["analytics_details"]["details"] for obj in detail["obj_details"]}
                    class_names_str = ', '.join(class_names)
                    worksheet.write(rows, cols2, class_names_str, cell_format_2)     
                    # worksheet.write(rows, cols2, i['camera_name'], cell_format_2)
                if cols3 == 3:
                    date_time = datetime.strptime(str(i['analytics_status']['Analytics_started_time']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols3, date_time,  date_format)
                if cols4 == 4:
                    if i['analytics_status']['Analytics_stopped_time'] is not None and i['analytics_status']['Analytics_stopped_time'] != 'None':
                        date_time = datetime.strptime(str(i['analytics_status']['Analytics_stopped_time']), '%Y-%m-%d %H:%M:%S')
                        date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                        worksheet.write_datetime(rows, cols4, date_time,  date_format)
                    else:
                        worksheet.write(rows, cols4, "-----", cell_format_2)
                if cols5 ==5 :
                    if i['analytics_details'] is not None:
                        if 'details' in i['analytics_details'] :
                            Details = i['analytics_details']['details']
                            if len(Details)!= 0:
                                for indexddddi , IMagedetails  in enumerate(Details):
                                    verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' +IMagedetails['image_name'] )
                                    verify_img.verify()
                                    worksheet.set_row(rows, 180)
                                    if len(IMagedetails['obj_details']) !=0:
                                        draw_bbox_and_insert_image(worksheet, IMagedetails['image_name'],IMagedetails['obj_details'],rows,cols5)
                                    else:
                                        print("else_condition-----")
                                        worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + str(IMagedetails['image_name']), {'x_scale': 0.16, 'y_scale': 0.212})
                                    break
                            else :
                                worksheet.write(rows, cols5, "-----", cell_format_2)
                        else :
                            worksheet.write(rows, cols5, "-----", cell_format_2)
                    else :
                        worksheet.write(rows, cols5, "-----", cell_format_2)
                rows += 1
        class_names = {obj["class_name"] for detail in i["analytics_details"]["details"] for obj in detail["obj_details"]} 
        violation_types = class_names

        FireSmokecreate_chart(workbook, from_date, to_date, violation_types, list1)
        FSDcreatecamera_wisechart(workbook, list1,from_date,to_date)
        FSDcreatedepartment_wisechart(workbook, list1,from_date,to_date)
        workbook.close()
            
        print('UnidentifiedImageError_count111111111111111111111 == ',UnidentifiedImageError_count)
        print('FileNotFoundError_count 11111111111111111111== ', FileNotFoundError_count)
        ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
       
    return ret

def FireSmokecreate_chart(workbook, from_date, to_date, violation_types, list1):
    try:
        start_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date format! Please enter the date in 'YYYY-MM-DD HH:MM:SS' format.")
        return

    # Define header formats
    header_font = workbook.add_format({'bold': True, 'color': 'FFFFFF', 'bg_color': '4F81BD', 'size': '12'})
    border_style = workbook.add_format({'border': 1})

    # Initialize the structure to hold violation counts
    violations_by_date = defaultdict(lambda: defaultdict(int))  # For date-wise counting
    violations_by_date_hour = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # For timestamp-wise counting

    date_range_exceeds_three_days = (end_date - start_date).days > 3
    print("Date range exceeds three days:", date_range_exceeds_three_days)

    for v_type in violation_types:
        data = [
            record for record in list1 
            if ', '.join({obj["class_name"] for detail in record["analytics_details"]["details"]
                         for obj in detail["obj_details"]}) == v_type
        ]
        
        sheet_name = f"{v_type} Violation"

        # Check if the sheet already exists
        existing_sheets = [sheet.get_name() for sheet in workbook.worksheets_objs]
        if sheet_name in existing_sheets:
            continue  # Skip if the sheet already exists

        sheet = workbook.add_worksheet(sheet_name)

        # Create headers
        headers = ['Date' if date_range_exceeds_three_days else 'Timestamp'] + list(violation_types)
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, header_font)

        # Process the data
        for record in data:
            for detail in record['analytics_details']['details']:
                timestamp = detail.get('timestamp')
                if timestamp:
                    timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    if date_range_exceeds_three_days:
                        violation_date = timestamp_obj.date()
                        violations_by_date[violation_date][v_type] += 1
                    else:
                        violation_date = timestamp_obj.date()
                        violation_hour = timestamp_obj.hour
                        violations_by_date_hour[violation_date][violation_hour][v_type] += 1

        # Write the data to the sheet
        row_index = 1
        if date_range_exceeds_three_days:
            # Date-wise logic
            current_date = start_date.date()
            while current_date <= end_date.date():
                row = [str(current_date)]
                for violationType in violation_types:
                    count = violations_by_date[current_date].get(violationType, 0)
                    row.append(count)
                sheet.write_row(row_index, 0, row)
                row_index += 1
                current_date += timedelta(days=1)
        else:
            # Timestamp-wise logic
            current_time = start_date
            while current_time <= end_date:
                timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                row = [timestamp]
                for violationType in violation_types:
                    count = violations_by_date_hour[current_time.date()][current_time.hour].get(violationType, 0)
                    row.append(count)
                sheet.write_row(row_index, 0, row)
                row_index += 1
                current_time += timedelta(hours=1)

        # Calculate total violations for chart title
        if date_range_exceeds_three_days:
            total_violations = sum(
                sum(date_data.values()) for date_data in list(violations_by_date.values())
            )
        else:
            total_violations = sum(
                sum(hour.get(v_type, 0) for hour in date_data.values())
                for date_data in list(violations_by_date_hour.values())
            )

        # Create a bar chart
        chart = workbook.add_chart({'type': 'column'})
        chart.set_title({'name': f"{sheet_name} Total Counts: {total_violations}"})
        chart.set_x_axis({'name': 'Date' if date_range_exceeds_three_days else 'Violation Time'})
        chart.set_y_axis({'name': 'Detected Count'})
        chart.set_size({'width': 1100, 'height': 700})

        # Set ranges for the chart
        data_range = f"'{sheet_name}'!B2:B{row_index}"
        categories_range = f"'{sheet_name}'!A2:A{row_index}"

        # Add data to the chart
        chart.add_series({
            'name': f"{v_type} Violations",
            'categories': categories_range,
            'values': data_range,
            'data_labels': {'value': True}
        })

        # Insert the chart into the worksheet
        sheet.insert_chart(f"C2", chart)
        sheet.set_column(0, 0, 20)



def FSDcreatecamera_wisechart(workbook, list1, from_date, to_date, title="Camera-wise Violation Chart"):
    violations_by_camera = defaultdict(int)

    # Count violations by camera
    for record in list1:
        camera_name = record.get("camera_name", "Unknown Camera")
        violations_by_camera[camera_name] += 1

    # Create a worksheet and add chart data
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        # Headers
        sheet.write(0, 0, "Camera", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        # Populate data
        row_index = 1
        for camera, count in violations_by_camera.items():
            sheet.write(row_index, 0, camera)
            sheet.write(row_index, 1, count)
            row_index += 1

        # Add the column chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': "Violation Counts",
            'categories': f"'{sheet_name}'!A2:A{row_index}",
            'values': f"'{sheet_name}'!B2:B{row_index}",
            'data_labels': {'value': True}
        })
        chart.set_title({
            'name': f'Camera-wise Violation Counts\n({from_date} to {to_date})'
        })
        chart.set_x_axis({'name': 'Camera'})
        chart.set_y_axis({'name': 'Violation Count'})
        chart.set_size({'width': 1200, 'height': 600})  # Adjusted size

       
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)

def FSDcreatedepartment_wisechart(workbook, list1, from_date, to_date, title="Department-wise Violation Chart"):
    violations_by_department = defaultdict(int)

    # Count violations by department
    for record in list1:
        department = (
            record.get("department") or
            (record.get("camera_info", {}).get("department")) or
            "Unknown Department"
        )
        violations_by_department[department] += 1

    # Create a worksheet and add chart data
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        # Headers
        sheet.write(0, 0, "Department", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        # Populate data
        row_index = 1
        for department, count in violations_by_department.items():
            sheet.write(row_index, 0, department)
            sheet.write(row_index, 1, count)
            row_index += 1

        # Add the column chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': "Violation Counts",
            'categories': f"'{sheet_name}'!A2:A{row_index}",
            'values': f"'{sheet_name}'!B2:B{row_index}",
            'data_labels': {'value': True}
        })
        chart.set_title({
            'name': f'Department-wise Violation Counts\n({from_date} to {to_date})'
        })
        chart.set_x_axis({'name': 'Department'})
        chart.set_y_axis({'name': 'Violation Count'})
        chart.set_size({'width': 1200, 'height': 600})  # Adjusted size

        # Insert the chart in the sheet
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)




def FSDCREATE(list1,from_date, to_date):
    #print("list1 ===",list1)
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'firesmoke_violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:E', 30)
        worksheet.set_column('F:F', 43)
        worksheet.set_row(0, 100)
        worksheet.set_row(1,  20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(40)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        # worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        # worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/JSW_Group_Logo.jpg'), {'x_scale': 0.4, 'y_scale':0.2})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:F1', 'Violation Details', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(18)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        
        
        cell_format_7 = workbook.add_format()
        cell_format_7.set_bold()
        cell_format_7.set_font_color('white')
        cell_format_7.set_font_name('Calibri')
        cell_format_7.set_font_size(18)
        cell_format_7.set_align('center_across')
        cell_format_7.set_bg_color('#800080')        
        row = 1
        col = 0
        worksheet.write(row, col ,"Department Name" , cell_format_1)
        worksheet.write(row, col + 1, 'Camera Name', cell_format_1)
        worksheet.write(row, col + 2, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 4, 'Ended Time', cell_format_1)
        worksheet.write(row, col + 5, 'Violation', cell_format_1)
        cell_format_2 = workbook.add_format()
        cell_format_2.set_font_name('Calibri')
        cell_format_2.set_align('center_across')
        rows = 2
        cols = 0
        cols1 = 1
        cols2 = 2
        cols3 = 3
        cols4 = 4
        cols5 = 5
        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0
        
        df = pd.DataFrame(list1)
        # df = pd.DataFrame(list1)

        df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%d-%m-%Y')
        result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        result_dict = {
            'date': result_df['date'].tolist(),
            'cameraname': result_df['camera_name'].tolist(),
            'No of times': result_df['No of times'].tolist()
        }
        df = pd.DataFrame(result_dict)

        # df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
        # result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        # result_dict = {
        #     'date': result_df['date'].tolist(),
        #     'cameraname': result_df['camera_name'].tolist(),
        #     'No of times': result_df['No of times'].tolist()
        # }
        excel_file =filename# 'grouped_column.xlsx'
        sheet_name = 'sheet 2'

        df.to_excel(excel_file, sheet_name=sheet_name, index=False)
        for i in list1:
            # try:
                if cols == 0:
                    worksheet.write(rows, cols, i['department'], cell_format_2)
                if cols1 == 1:
                    worksheet.write(rows, cols1, i['camera_name'], cell_format_2)
                    
                    # worksheet.write(rows, cols1, i['analytics_details'], cell_format_2)                
                if cols2 == 2:
                    class_names = {obj["class_name"] for detail in i["analytics_details"]["details"] for obj in detail["obj_details"]}
                    class_names_str = ', '.join(class_names)
                    worksheet.write(rows, cols2, class_names_str, cell_format_2)     
                    # worksheet.write(rows, cols2, i['camera_name'], cell_format_2)
                if cols3 == 3:
                    date_time = datetime.strptime(str(i['analytics_status']['Analytics_started_time']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols3, date_time,  date_format)
                if cols4 == 4:
                    if i['analytics_status']['Analytics_stopped_time'] is not None and i['analytics_status']['Analytics_stopped_time'] != 'None':
                        date_time = datetime.strptime(str(i['analytics_status']['Analytics_stopped_time']), '%Y-%m-%d %H:%M:%S')
                        date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                        worksheet.write_datetime(rows, cols4, date_time,  date_format)
                    else:
                        worksheet.write(rows, cols4, "-----", cell_format_2)
                if cols5 ==5 :
                    if i['analytics_details'] is not None:
                        if 'details' in i['analytics_details'] :
                            Details = i['analytics_details']['details']
                            if len(Details)!= 0:
                                for indexddddi , IMagedetails  in enumerate(Details):
                                    verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' +IMagedetails['image_name'] )
                                    verify_img.verify()
                                    worksheet.set_row(rows, 180)
                                    if len(IMagedetails['obj_details']) !=0:
                                        draw_bbox_and_insert_image(worksheet, IMagedetails['image_name'],IMagedetails['obj_details'],rows,cols5)
                                    else:
                                        print("else_condition-----")
                                        worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + str(IMagedetails['image_name']), {'x_scale': 0.16, 'y_scale': 0.212})
                                    break
                            else :
                                worksheet.write(rows, cols5, "-----", cell_format_2)
                        else :
                            worksheet.write(rows, cols5, "-----", cell_format_2)
                    else :
                        worksheet.write(rows, cols5, "-----", cell_format_2)
                rows += 1
        class_names = {obj["class_name"] for detail in i["analytics_details"]["details"] for obj in detail["obj_details"]} 
        violation_types = class_names

        FireSmokecreate_chart(workbook, from_date, to_date, violation_types, list1)
        FSDcreatecamera_wisechart(workbook, list1,from_date,to_date)
        FSDcreatedepartment_wisechart(workbook, list1,from_date,to_date)
        workbook.close()
            
        print('UnidentifiedImageError_count111111111111111111111 == ',UnidentifiedImageError_count)
        print('FileNotFoundError_count 11111111111111111111== ', FileNotFoundError_count)
        ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
       
    return ret

def draw_bbox_and_insert_image(worksheet, image_path, image_data, row, column):
    boundingboxdetails =  {
     "object_thickness": 5,
    "roi_thickness": 5,
    "object_font_size": 12,
    "roi_font_size": 50,
    "roi": "#fa0707",
    "person": "#ff0015",
    "helmet": "#ff0000",
    "vest": "#FFFF00",
    "fsd": "#5ce65c",
    "bicycle": "#ff4de6",
    "motorcycle": "#ffa800",
    "car": "#8b00ff",
    "bus": "#808000",
    "truck": "#f08080",
    "biker": "#ff0000"
  }
    if "rtsp_flag" in mongo.db.list_collection_names():
        finddataboxdata = mongo.db.rtsp_flag.find_one()
        if finddataboxdata is not None:
            if 'bb_box_settings' in finddataboxdata:
                if finddataboxdata['bb_box_settings'] is not None:
                    boundingboxdetails = finddataboxdata['bb_box_settings']

    else:
        print("Collection 'rtsp_flag' does not exist")
    helmetboxcolor= boundingboxdetails['helmet']    
    vestboxcolor= boundingboxdetails['vest']
    personboxcolor= boundingboxdetails['person']
    fsdboxcolor= boundingboxdetails['fsd']
    bicycleboxcolor= boundingboxdetails['bicycle']
    motorcycleboxcolor= boundingboxdetails['motorcycle']
    carboxcolor= boundingboxdetails['car']
    busboxcolor= boundingboxdetails['bus']
    truckboxcolor= boundingboxdetails['truck']
    bikerboxcolor= boundingboxdetails['biker']
    objectfont_size= boundingboxdetails['object_font_size']
    Objectbbox_thickness= boundingboxdetails['object_thickness']
    ROIbboxthickness= boundingboxdetails['roi_thickness']
    roiboxcolor= boundingboxdetails['roi']
    roifont_size = boundingboxdetails['roi_font_size']
    img = Image.open(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', image_path))
    draw = ImageDraw.Draw(img)    
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', objectfont_size, encoding='unic')
    if len(image_data) > 0:
        for obj_detail in image_data:
            height = obj_detail['bbox']['H']
            width = obj_detail['bbox']['W']
            x = obj_detail['bbox']['X']
            y = obj_detail['bbox']['Y']
            class_name = obj_detail.get('class_name', 'Unknown').upper()
            start_col = x
            start_row = y
            end_col = x + width
            end_row = y + height
            draw.rectangle([start_col, start_row, end_col, end_row], outline=fsdboxcolor, width=Objectbbox_thickness)
            text_width, text_height = calculate_text_size(class_name, objectfont_size)
            text_x = start_col + 6
            text_y = end_row + 10 
            text_bg_position = (text_x, text_y, text_x + text_width + 10, text_y + text_height)
            draw.rectangle(text_bg_position, fill=(0, 0, 0, 128))
            draw.text((text_x, text_y), class_name, fill=fsdboxcolor, font=font)
    image_io = BytesIO()
    img.save(image_io, format='JPEG')
    image_io.seek(0) 
    worksheet.insert_image(row, column, 'image.jpg', {'image_data': image_io, 'x_scale': 0.16, 'y_scale': 0.212})




def FIREANDSMOKEEXCELWITHOUTVIDOE(list1):
    # print("list1 ===",list1)
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'firesmoke_violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:E', 30)
        worksheet.set_column('F:F', 43)
        worksheet.set_row(0, 100)
        worksheet.set_row(1,  20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(40)
        cell_format.set_align('center_across')
        #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/JSW_Group_Logo.jpg'), {'x_scale': 0.4, 'y_scale':0.2})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:F1', 'Violation Details', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(18)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')    
        cell_format_7 = workbook.add_format()
        cell_format_7.set_bold()
        cell_format_7.set_font_color('white')
        cell_format_7.set_font_name('Calibri')
        cell_format_7.set_font_size(18)
        cell_format_7.set_align('center_across')
        cell_format_7.set_bg_color('#800080')        
        row = 1
        col = 0
        worksheet.write(row, col ,"Camera Name" , cell_format_1)
        worksheet.write(row, col + 1, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 2, 'Location', cell_format_1)
        worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 4, 'Ended Time', cell_format_1)
        worksheet.write(row, col + 5, 'Violation', cell_format_1)
        cell_format_2 = workbook.add_format()
        cell_format_2.set_font_name('Calibri')
        cell_format_2.set_align('center_across')
        rows = 2
        cols = 0
        cols1 = 1
        cols2 = 2
        cols3 = 3
        cols4 = 4
        cols5 = 5
        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0        
        df = pd.DataFrame(list1)
        # df = pd.DataFrame(list1)
        df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
        result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        result_dict = {
            'date': result_df['date'].tolist(),
            'cameraname': result_df['camera_name'].tolist(),
            'No of times': result_df['No of times'].tolist()
        }
        df = pd.DataFrame(result_dict)

        # df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
        # result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        # result_dict = {
        #     'date': result_df['date'].tolist(),
        #     'cameraname': result_df['camera_name'].tolist(),
        #     'No of times': result_df['No of times'].tolist()
        # }
        excel_file =filename# 'grouped_column.xlsx'
        sheet_name = 'sheet 2'

        df.to_excel(excel_file, sheet_name=sheet_name, index=False)

        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column("A:D", 20)
            worksheet.merge_range('A1:D1', 'MIS-Fugitive Emission Report', workbook.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'size': 14
            }))
            cell_format_title = workbook.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'size': 18,
                'font_color': 'white',
                'font_name': 'Calibri',
                'bg_color': '#333300',
                'center_across': True
            })

            cell_format_column = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Calibri',
                'center_across': True
            })

            worksheet.set_row(0, 40)
            worksheet.set_row(1, 20)

            column_names = df.columns
            for col_num, value in enumerate(column_names):
                worksheet.write(1, col_num, value, cell_format_title)

            logo_path = 'Untitled.jpeg'
            worksheet.insert_image('D1', logo_path, {'x_scale': 0.27, 'y_scale': 0.15, 'x_offset': 1, 'y_offset': 10, 'width': 640, 'height': 640})

            for i, row in enumerate(df.itertuples(), 2):
                for col_num, value in enumerate(row[1:]): 
                    worksheet.write(i, col_num, value, cell_format_column)

            chart = workbook.add_chart({'type': 'column'})
            for i, row in enumerate(df.itertuples(), 1):
                color = 'blue'
                category_label = f'{row.date} - {row.cameraname}'
                chart.add_series({
                    'name': category_label,
                    'categories': ['Sheet1', 1, 0, len(df), 0],
                    'values': ['Sheet1', 1, i, len(df), i],
                    'fill': {'color': color},
                    'gap': 300,
                    'overlap': -50,
                })

            chart.set_x_axis({'name': 'Date '})
            chart.set_y_axis({'name': 'Number of Times', 'major_gridlines': {'visible': False}})
            chart.set_title({'name': 'Number of Times by Location and Date'})
            chart.set_size({'width': 960, 'height': 720})
            worksheet.insert_chart('G2', chart)
        # worksheet1 = workbook.add_worksheet('Summary Data')
        # worksheet1.set_column('A:E', 30)
        # df = pd.DataFrame(list1)

        # df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
        # result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
        # result_dict = {
        #     'date': result_df['date'].tolist(),
        #     'cameraname': result_df['camera_name'].tolist(),
        #     'No of times': result_df['No of times'].tolist()
        # }
        
        # # df.to_excel(writer, sheet_name=sheet_name, index=False)
        # # workbook = writer.book
        # # worksheet1 = writer.sheets[sheet_name]
        # worksheet1.set_column("A:D", 20)
        # worksheet1.merge_range('A1:D1', 'MIS-Fugitive Emission Report', workbook.add_format({
        #     'bold': True,
        #     'align': 'center',
        #     'valign': 'vcenter',
        #     'size': 14
        # }))
        # cell_format_title = workbook.add_format({
        #     'bold': True,
        #     'align': 'center',
        #     'valign': 'vcenter',
        #     'size': 18,
        #     'font_color': 'white',
        #     'font_name': 'Calibri',
        #     'bg_color': '#333300',
        #     'center_across': True
        # })

        # cell_format_column = workbook.add_format({
        #     'align': 'center',
        #     'valign': 'vcenter',
        #     'font_name': 'Calibri',
        #     'center_across': True
        # })

        # worksheet1.set_row(0, 40)
        # worksheet1.set_row(1, 20)

        # column_names = df.columns
        # for col_num, value in enumerate(column_names):
        #     worksheet1.write(1, col_num, value, cell_format_title)

        # logo_path = 'Untitled.jpeg'
        # worksheet1.insert_image('D1', logo_path, {'x_scale': 0.27, 'y_scale': 0.15, 'x_offset': 1, 'y_offset': 10, 'width': 640, 'height': 640})

        # for i, row in enumerate(df.itertuples(), 2):
        #     for col_num, value in enumerate(row[1:]): 
        #         worksheet1.write(i, col_num, value, cell_format_column)

        # chart = workbook.add_chart({'type': 'column'})
        # for i, row in enumerate(df.itertuples(), 1):
        #     color = 'blue'
        #     category_label = f'{row.date} - {row.cameraname}'
        #     chart.add_series({
        #         'name': category_label,
        #         'categories': ['Sheet1', 1, 0, len(df), 0],
        #         'values': ['Sheet1', 1, i, len(df), i],
        #         'fill': {'color': color},
        #         'gap': 300,
        #         'overlap': -50,
        #     })

        # chart.set_x_axis({'name': 'Date '})
        # chart.set_y_axis({'name': 'Number of Times', 'major_gridlines': {'visible': False}})
        # chart.set_title({'name': 'Number of Times by Location and Date'})
        # chart.set_size({'width': 960, 'height': 720})
        # worksheet1.insert_chart('G2', chart)
        # worksheet1.set_row(0, 30)
        # worksheet1.set_row(1, 20)
        # violation_counts = Counter()
        # locations = []
        # x_axis_labels = []

        # for row_data in list1:
        #     location = row_data.get('location', 'Unknown')
        #     violation = row_data.get('analytics_details', 'Unknown').strip(',')
        #     start_time = row_data.get('start_time', 'Unknown')
        #     start_time = start_time.split(' ')[0]
        #     key = f"{location}--{violation}--{start_time}"
        #     violation_counts[key] += 1

        # summary_data = [{'location': key.split('--')[0], 'analytics_details': key.split('--')[1], 'start_time': key.split('--')[2], 'violation_count': count} for key, count in violation_counts.items()]

        # worksheet1.write('A2', 'DATE', cell_format_7)
        # worksheet1.write('B2', 'Location Details', cell_format_7)
        # worksheet1.write('C2', 'Violation Type', cell_format_7)
        # worksheet1.write('D2', 'Number of times', cell_format_7)

        # for row_num, row_data in enumerate(summary_data, start=2):
        #     worksheet1.write(row_num, 0, row_data['start_time'], cell_format_2)
        #     worksheet1.write(row_num, 1, row_data['location'], cell_format_2)
        #     worksheet1.write(row_num, 2, row_data['analytics_details'], cell_format_2)
        #     worksheet1.write(row_num, 3, row_data['violation_count'], cell_format_2)
        #     x_axis_labels.append(f"{row_data['location']} - {row_data['start_time']}")
        #     if row_data['location'] not in locations:
        #         locations.append(row_data['location'])
                
        # chart = workbook.add_chart({'type': 'column'})
        # chart.add_series({
        #     'categories': f'=Summary Data!$A$2:$A${len(x_axis_labels) + 1}',
        #     'values': f'=Summary Data!$D$2:$D${len(x_axis_labels) + 1}',
        # })

        # chart.set_x_axis({'name': 'Date and Location', 'text_axis': True, 'categories': x_axis_labels})
        # chart.set_title({'name': 'Violation Counts by Location'})
        # chart.set_size({'width': 720, 'height': 576})
        # worksheet1.insert_chart('G2', chart)
        
        for i in list1:
            try:
                if cols == 0:
                    worksheet.write(rows, cols, i['camera_name'], cell_format_2)
                if cols1 == 1:
                    worksheet.write(rows, cols1, i['analytics_details'], cell_format_2)                    
                if cols2 == 2:
                    worksheet.write(rows, cols2, i['location'], cell_format_2)
                if cols3 == 3:
                    date_time = datetime.strptime(str(i['start_time']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols3, date_time,  date_format)
                if cols4 == 4:
                    if i['stop_time'] is not None and i['stop_time'] != 'None':
                        date_time = datetime.strptime(str(i['stop_time']), '%Y-%m-%d %H:%M:%S')
                        date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                        worksheet.write_datetime(rows, cols4, date_time,  date_format)
                    else:
                        worksheet.write(rows, cols4, "-----", cell_format_2)
                if cols5 ==5 :
                    if i['video_file_name'] is not None:
                        if  'jpg' in i['video_file_name'] :
                            verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/fsd' + '/' +i['video_file_name'] )
                            verify_img.verify()
                            worksheet.set_row(rows, 180)
                            if len(i['object_details']) !=0:
                                draw_bbox_and_insert_image(worksheet, i['video_file_name'],i['object_details'],rows,cols5)                               
                                # worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/fsd' + '/Temparary.jpg' , {'x_scale': 0.16, 'y_scale': 0.212})
                            else:
                                print("else_condition-----")
                                worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/fsd' + '/' + str(i['video_file_name']), {'x_scale': 0.16, 'y_scale': 0.212})
                                
                        
                        else:
                            
                            video_file_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'sm_rec', i['video_file_name'])

                            worksheet.write_url(0, 0, 'external:' + video_file_path, string='Click to play video')
                            # worksheet.write_url(rows,cols5,  get_current_dir_and_goto_parent_dir() +  '/images/sm_rec' + '/' + str(i['video_file_name']), string='Click to play video')

                    else :
                        worksheet.write(rows, cols5, "-----", cell_format_2)
                rows += 1
            except UnidentifiedImageError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 1", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
                UnidentifiedImageError_count += 1
            except FileNotFoundError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 2", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
                FileNotFoundError_count += 1
            except UserWarning as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 3", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except ImportError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 4", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except xlsxwriter.exceptions.FileCreateError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 5", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except PermissionError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 6", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except xlsxwriter.exceptions.XlsxWriterException as  error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 7", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FIREANDSMOKEENOXCELWITHOUTVIDOE 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret


# Create your views here.


# @firesmoke.route('/start_firesmoke', methods=['GET'])
# @firesmoke.route('/start_firesmoke', methods=['POST'])
@csrf_exempt
def start_firesmoke(request):
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if request.method == "POST":
        jsonobject = json.loads(request.body)
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['media_type', 'data_interval']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                media_type = jsonobject['media_type']
                data_interval = jsonobject['data_interval']
                if media_type == 'video':
                    media_type = 0
                elif media_type == 'image' :
                    media_type = 1 
                else : 
                    media_type = 1 
                    
                print("media_typemedia_type",media_type)
                print("data_interval",data_interval)
                if 1:
                    firesmokecamerastatus.delete_many({})
                    Truncatefiresmokecamera()
                    common_return_data = FIRESMOKECONFIG(media_type,data_interval)
                    if common_return_data:
                        createHOOTERMETAJSONSTART()
                        firesmoke_app_monitoring_started(True)
                        stop_application_for_firesmokeapp_creating_config()
                        if common_return_data['success'] == True:
                            firesmoke_app_monitoring_started(False)
                            ret = common_return_data
                        else:
                            ret['message'] = common_return_data['message']
                    else:
                        ret['message'] = 'data not found to create config files.'
        else:
            ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    return JsonResponse(ret)


# @firesmoke.route('/stop_firesmokeapp', methods=['GET'])
@csrf_exempt
def stop_application_1_phaseoneapp(request):
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if request.method == "GET":
        if 1:
            firesmoke_app_monitoring_started(True)
            createHOOTERMETAJSONSTOP()
            # mongo.db.voice_announcement_status.delete_many({"violation_type":"VPMS"})
            if "voice_announcement_status" not in DATABASE.list_collection_names():
                print("Collection 'voice_announcement_status' does not exist-VPMS")
                # raise Exception("Collection 'voice_announcement_status' does not exist")
            else:
                voice_announcement_status.delete_many({"violation_type": { "$in": ["FSD"] }})
            firesmokecamerastatus.delete_many({})
            Truncatefiresmokecamera()
            ret = {'message': 'fire smoke application stopped.', 'success': True}
        else:
            ret = ret
    return JsonResponse(ret)


# @firesmoke.route('/getFireVideo/<vidoename>', methods=['GET'])
@csrf_exempt
def firevidoe(request,vidoename):
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if request.method == "GET":
        
        try:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'sm_rec')
            video_path = os.path.join(base_path, vidoename)

            # Check if the video file exists
            if not os.path.exists(video_path):
                return JsonResponse({"message":"File not found.", "success":False})

            # Check if the request explicitly wants an mp4 file
            if request.headers.get('Accept') == 'video/mp4':
                try:
                    # Serve the video as an attachment with the correct MIME type
                    response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
                    response['Content-Disposition'] = f'attachment; filename="{vidoename}"'
                    return response
                except Exception as e:
                    return JsonResponse(f"Error while processing the video: {str(e)}", status=500)
            else:
                try:
                    # Default behavior: Serve the video file
                    response = FileResponse(open(video_path, 'rb'))
                    return response
                except Exception as e:
                    return JsonResponse(f"Error while processing the video: {str(e)}", status=500)
            # return response
        except Exception as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
            ret = str(error)
    return JsonResponse(ret)
    

# @firesmoke.route('/GETFIRESMOKEIMAGE/<imagename>', methods=['GET'])
@csrf_exempt
def FIREANDSMOKEDUSTIMAGE(request,imagename):
    if request.method == "GET":
        #Fsd = (127, 255, 0)
        boundingboxdetails =  {
        "object_thickness": 5,
        "roi_thickness": 5,
        "object_font_size": 12,
        "roi_font_size": 50,
        "roi": "#fa0707",
        "person": "#ff0015",
        "helmet": "#ff0000",
        "vest": "#FFFF00",
        "fsd": "#5ce65c",
        "bicycle": "#ff4de6",
        "motorcycle": "#ffa800",
        "car": "#8b00ff",
        "bus": "#808000",
        "truck": "#f08080",
        "biker": "#ff0000"
    }
        if "rtsp_flag" in DATABASE.list_collection_names():
            finddataboxdata =rtsp_flag.find_one()
            if finddataboxdata is not None:
                if 'bb_box_settings' in finddataboxdata:
                    if finddataboxdata['bb_box_settings'] is not None:
                        boundingboxdetails = finddataboxdata['bb_box_settings']
            else:
                ret={"message":"data not found"}
                return JsonResponse(ret)

        else:
            print("Collection 'rtsp_flag' does not exist")
        helmetboxcolor= boundingboxdetails['helmet']    
        vestboxcolor= boundingboxdetails['vest']
        personboxcolor= boundingboxdetails['person']
        fsdboxcolor= boundingboxdetails['fsd']
        bicycleboxcolor= boundingboxdetails['bicycle']
        motorcycleboxcolor= boundingboxdetails['motorcycle']
        carboxcolor= boundingboxdetails['car']
        busboxcolor= boundingboxdetails['bus']
        truckboxcolor= boundingboxdetails['truck']
        bikerboxcolor= boundingboxdetails['biker']
        objectfont_size= boundingboxdetails['object_font_size']
        Objectbbox_thickness= boundingboxdetails['object_thickness']
        ROIbboxthickness= boundingboxdetails['roi_thickness']
        roiboxcolor= boundingboxdetails['roi']
        roifont_size = boundingboxdetails['roi_font_size'] 
        if 1:
        # try:
            base_path = get_current_dir_and_goto_parent_dir()+'/images/frame'
            file_path = os.path.join(base_path, imagename)
            image_data = firesmokeviolationdata.find_one({'analytics_details.details.image_name':imagename})#({'video_file_name': imagename})
            if image_data is not None:
                if isEmpty(image_data['analytics_details']) :
                    imagedetaildata = image_data['analytics_details']
                    ALlimagedeta = imagedetaildata['details']
                    if len(ALlimagedeta) !=0:
                        for imageindex , imaged in enumerate(ALlimagedeta):
                            if imaged['image_name']==imagename:
                                source_img = Image.open(file_path)
                                draw = ImageDraw.Draw(source_img)
                                if len(imaged['obj_details']) !=0:
                                    for j,lkkkbbox in enumerate(imaged['obj_details']):
                                        Vestheight = lkkkbbox['bbox']['H']
                                        Vestwidth = lkkkbbox['bbox']['W']
                                        Vestx_value = lkkkbbox['bbox']['X']
                                        Vesty_value = lkkkbbox['bbox']['Y']     
                                        # Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                                        Vestshape = [(Vestx_value, Vesty_value),(Vestwidth, Vestheight)]
                                        text_width,text_height = calculate_text_size(lkkkbbox['class_name'].upper(),objectfont_size)                                    
                                        text_x = Vestx_value + 6
                                        text_y = Vesty_value +     Vestheight                  
                                        text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(lkkkbbox['class_name'].upper())), text_y + text_height )
                                        # draw.rectangle(text_bg_position, fill='black')
                                        draw.rectangle(text_bg_position, fill=(0, 0, 0, 128)) 
                                        draw.rectangle(Vestshape, outline=fsdboxcolor, width=Objectbbox_thickness)#127, 255, 0#(34, 139, 34)
                                        draw.text((text_x, text_y), lkkkbbox['class_name'].upper(), fsdboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic')) 
                                    imgByteArr = io.BytesIO()
                                    source_img.save(imgByteArr, format='JPEG')
                                    imgByteArr.seek(0)
                                response = FileResponse(imgByteArr, content_type='image/jpeg')
                                # Set the Content-Disposition header to indicate that the file should be downloaded
                                response['Content-Disposition'] = f'attachment; filename="{imagename}"'
                                return (response)
                
                else:
                    ret={"message":FileResponse(base_path, imagename)}
                    return JsonResponse(ret)
                    # return response
            ret= {"message":'given image data found.'}
            return JsonResponse(ret)
        # except Exception as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     return str(error)
    else:
        ret={'message': 'something went wrong with create config.', 'success': False}

    return JsonResponse(ret)


# @firesmoke.route('/DeleteFireViolation/<id>', methods=['GET'])
@csrf_exempt
def DeleteFIREviolation(request,id=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    if request.method == "GET":
        try:
            if id is not None:
                find_data = firesmokeviolationdata.find_one({'_id': ObjectId(id)})
                if find_data is not None:
                    result = firesmokeviolationdata.delete_one({'_id':ObjectId(id)})
                    if result.deleted_count > 0:
                        ret = {'message':'violation deleted successfully.','success': True}
                    else:
                        ret = {'message':'violation not deleted.','success': False}                        
                else:
                    ret['message'] = 'violation data is not found.'
            else:
                ret['message'] = 'mongodb should not be none.'
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
            print("print(,)", str(error))
            ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_verification 1", str(error), " ----time ---- ", now_time_with_time()]))
            if restart_mongodb_r_service():
                print("mongodb restarted")
            else:
                if forcerestart_mongodb_r_service():
                    print("mongodb service force restarted-")
                else:
                    print("mongodb service is not yet started.") 
        except Exception as  error:
            ret['message'] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()]) 
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_verification 2", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)



# @firesmoke.route('/FIRESMOKEverification/<id>/<flag>', methods=['GET'])
@csrf_exempt
def FIRESMOKEVERIFICATIONviolation(request,id=None, flag=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    if request.method == "GET":
        try:
            if id is not None:
                if flag is not None:
                    if flag != 'undefined':
                        find_data = firesmokeviolationdata.find_one({'_id': ObjectId(id)})
                        if find_data is not None:
                            print("flag ===",flag)
                            if flag == 'false':
                                result = firesmokeviolationdata.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False, 'violation_verificaton_status': True}})
                                if result.modified_count > 0:
                                    ret = {'message':'violation status updated successfully.','success': True}
                                else:
                                    ret = {'message':'violation status not updated .','success': False}
                            elif flag == 'true':
                                result = firesmokeviolationdata.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': True,  'violation_verificaton_status': True}})
                                if result.modified_count > 0:
                                    ret = {'message':'violation status updated successfully.' , 'success': True}
                                else:
                                    ret = {'message':'violation status already updated.','success': False}
                            else:
                                ret = {'message':'violation status not updated .', 'success': False}
                        else:
                            ret['message'] = 'violation data is not found.'
                    else:
                        ret['message'] = 'violation statusshould not be undefined'
                else:
                    ret['message'] = 'violation status should not be none value.'
            else:
                ret['message'] = 'mongodb should not be none.'
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
            print("print(,)", str(error))
            ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_verification 1", str(error), " ----time ---- ", now_time_with_time()]))
            if restart_mongodb_r_service():
                print("mongodb restarted")
            else:
                if forcerestart_mongodb_r_service():
                    print("mongodb service force restarted-")
                else:
                    print("mongodb service is not yet started.") 
        except Exception as  error:
            ret['message'] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()]) 
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_verification 2", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)


# @firesmoke.route('/FSDLiveviolationdata', methods=['GET'])
# @firesmoke.route('/FSDLiveviolationdata/<camera_name>', methods=['GET'])
@csrf_exempt
def FSDLiveviolationdata( request,camera_name=None):
    ret = {'success': False,'message':"something went wrong in live_data1 apis"}
    if request.method == "GET":
        if 1:    
            dash_data = []
            if camera_name is not None :
                match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name}# {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}
                data = list(firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket_no':'$ticket_no'}, 'data':{'$push':'$$ROOT'}}},{'$limit': 4000000}, {'$sort':{'data._id': -1}} ]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        i['SNo'] = count+1
                        dash_data.append(i)
                    ret = live_data_pagination(len(dash_data), parse_json(dash_data))
                else:
                    ret['message'] = 'data not found'
            else:
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
                data = list(firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket_no':'$ticket_no'}, 'data':{'$push':'$$ROOT'}}},                                                  
                                                    {'$limit': 4000000}    ,  {'$sort':{'data._id': -1}}                     
                                                    ]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        i['SNo'] = count+1
                        dash_data.append(i)
                    ret =live_data_pagination(len(dash_data), parse_json(dash_data)) 
                else:
                    ret['message'] = 'data not found'  
    return JsonResponse(ret)


# @firesmoke.route('/datewiseFiresmoke', methods=['POST'])
# @firesmoke.route('/datewiseFiresmoke/<cameraname>', methods=['POST'])
# @firesmoke.route('/datewiseFiresmoke/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
# @firesmoke.route('/datewiseFiresmoke/<pagenumber>/<page_limit>', methods=['POST'])
@csrf_exempt
def datewiseFiresmoke(request,cameraname=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if request.method == "POST":
        if 1:
        # try:
            jsonobject = json.loads(request.body)
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['from_date', 'to_date']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    from_date = jsonobject['from_date']
                    to_date = jsonobject['to_date']
                    if cameraname is not None:
                        match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'camera_name':  cameraname}
                        data = list(firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket_no':'$ticket_no'}, 'data':{'$push':'$$ROOT'}}} , {'$limit': 4000000}    ,  {'$sort':{'data._id': -1}}   ]))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    else:
                        match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}}
                        data = list(firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket_no':'$ticket_no'}, 'data':{'$push':'$$ROOT'}}},  {'$limit': 4000000}    ,  {'$sort':{'data._id': -1}}   ]))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
            else:
                ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
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
        #     print("print(,)", str(error))
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise 1", str(error), " ----time ---- ", now_time_with_time()]))
        #     ret['message'] = " ".join(["something error has occered in api", str(error)])
            
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as  error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(ret)



# @firesmoke.route('/Firecameradetails', methods=['GET'])
# @firesmoke.route('/Firecameradetails', methods=['POST'])
@csrf_exempt
def Firecameradetails(request):
    ret = {'success': False, 'message':'something went wrong with camera_details details'}
    if request.method == 'POST':
        jsonobject = json.loads(request.body)
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}}
                data = list(firesmokeviolationdata.aggregate([{'$sort': {'timestamp': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                                                    {'$project': {'data': 0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['camera_name'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
        else:
            ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
            
    elif request.method == 'GET':
        
        try:
            match_data =  {'timestamp':{'$regex': '^' + str(date.today())}}
            data = list(firesmokeviolationdata.aggregate([{'$sort': {'timestamp': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                                                    {'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['camera_name'])
                ret = {'success': True, 'message': parse_json(dash_data)}
            else:
                ret['message'] = 'data not found'
                 
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
            print("print(,)", str(error))
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
            ret['message'] = " ".join(["something error has occered in api", str(error)])
            if restart_mongodb_r_service():
                print("mongodb restarted")
            else:
                if forcerestart_mongodb_r_service():
                    print("mongodb service force restarted-")
                else:
                    print("mongodb service is not yet started.") 
        except Exception as  error:
            ret = {'success': False, 'message': str(error)}
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_details 2", str(error), " ----time ---- ", now_time_with_time()]))     
    return JsonResponse(ret)

# @firesmoke.route('/Firedepartmentdetails', methods=['GET'])
# @firesmoke.route('/Firedepartmentdetails', methods=['POST'])
def Firedepartmentdetails(request):
    ret = {'success': False, 'message':'something went wrong with camera_details details'}
    if request.method == 'POST':
        jsonobject =json.loads(request.body)
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data=[]
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}}
                pipeline = [
                {'$sort': {'_id': -1}},
                {'$match': match_data}
                         ]            
                data = list(firesmokeviolationdata.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
        else:
            ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}            
    elif request.method == 'GET':
        dash_data  =[]
        try:
            match_data =  {'timestamp':{'$regex': '^' + str(date.today())}}
            pipeline = [
                {'$sort': {'_id': -1}},
                {'$match': match_data} ]            
            data = list(firesmokeviolationdata.aggregate(pipeline))
            if len(data) != 0:
                for count, i in enumerate(data):
                    if i['department'] not in dash_data:
                        dash_data.append(i['department'])
                ret = {'success': True, 'message': parse_json(dash_data)}
            else:
                ret['message'] = 'data not found'                  
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
            print("print(,)", str(error))
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
            ret['message'] = " ".join(["something error has occered in api", str(error)])
            if restart_mongodb_r_service():
                print("mongodb restarted")
            else:
                if forcerestart_mongodb_r_service():
                    print("mongodb service force restarted-")
                else:
                    print("mongodb service is not yet started.") 
        except Exception as  error:
            ret = {'success': False, 'message': str(error)}
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
           
    return JsonResponse(ret)



# @firesmoke.route('/create_violation_excelFSD', methods=['POST'])
@csrf_exempt
def create_violation_excelFSD(request):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if request.method == 'POST':
        jsonobject =json.loads(request.body)
        if 1:
        # try:
            if not os.path.exists('firesmoke_violation_excel_sheets'):
                handle_uploaded_file(os.path.join(os.getcwd(), "firesmoke_violation_excel_sheets"))
            # jsonobject = request.json
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['from_date', 'to_date', 'cameraname']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    from_date = jsonobject['from_date']
                    to_date = jsonobject['to_date']
                    cameraname = jsonobject['cameraname']
                    virtual_cameraname = cameraname
                    if type(virtual_cameraname) == str:
                        virtual_cameraname.lower()
                    list1 = []
                    all_data = []
                    if (virtual_cameraname !='none'):
                        if cameraname is not None :
                            if (cameraname == 'all_cameras' ):
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
                                mongo_data = list(firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}},  {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
                                                                        ]))
                                if len(mongo_data) !=0:
                                    excel_create = FSDCREATE(mongo_data,from_date,to_date)
                                    if excel_create['success'] == True:
                                        ret = excel_create#{'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}                                
                            elif cameraname is not None :
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True}
                                mongo_data = list(firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000}
                                                                        ]))
                                if len(mongo_data) !=0:
                                    excel_create = FSDCREATE(mongo_data,from_date,to_date)
                                    if excel_create['success'] == True:
                                        ret = excel_create#{'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                    else:
                        match_data = {'timestamp':{'$gte': from_date,'$lte': to_date},'violation_status': True}
                        mongo_data = list(firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000} ]))
                        if len(mongo_data) !=0:
                            print("length===========",len(mongo_data))
                            excel_create = FSDCREATE(mongo_data,from_date,to_date)
                            if excel_create['success'] == True:
                                ret =excel_create #{'success': True, 'message': 'Excel sheet is created sucessfully'}
                            else:
                                ret = excel_create
                        else:
                            ret = {'success': False, 'message':'data not found.'}   
            else:
                ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    return JsonResponse(ret)    



# @firesmoke.route('/create_violation_excelFireSmoke', methods=['POST'])
@csrf_exempt
def create_violation_excelFireSmoke(request):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if request.method == 'POST':
        jsonobject =json.loads(request.body)
        if 1:
        # try:
            if not os.path.exists('firesmoke_violation_excel_sheets'):
                handle_uploaded_file(os.path.join(os.getcwd(), "firesmoke_violation_excel_sheets"))
            # jsonobject = request.json
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['from_date', 'to_date', 'cameraname']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    from_date = jsonobject['from_date']
                    to_date = jsonobject['to_date']
                    cameraname = jsonobject['cameraname']
                    virtual_cameraname = cameraname
                    if type(virtual_cameraname) == str:
                        virtual_cameraname.lower()
                    list1 = []
                    all_data = []
                    if (virtual_cameraname !='none'):
                        if cameraname is not None :
                            if (cameraname == 'all_cameras' ):
                                match_data = {'start_time':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
                                mongo_data = list(firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}},  {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
                                                                        ]))
                                if len(mongo_data) !=0:
                                    excel_create = (FIREANDSMOKEEXCELWITHOUTVIDOE(mongo_data))
                                    if excel_create['success'] == True:
                                        ret = excel_create#{'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}                                
                            elif cameraname is not None :
                                match_data = {'start_time':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True}
                                mongo_data = list(firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000}
                                                                        ]))
                                if len(mongo_data) !=0:
                                    excel_create = (FIREANDSMOKEEXCELWITHOUTVIDOE(mongo_data))
                                    if excel_create['success'] == True:
                                        ret = excel_create#{'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                    else:
                        match_data = {'start_time':{'$gte': from_date,'$lte': to_date},'violation_status': True}
                        mongo_data = list(firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000} ]))
                        if len(mongo_data) !=0:
                            print("length===========",len(mongo_data))
                            excel_create = (FIREANDSMOKEEXCELWITHOUTVIDOE(mongo_data))
                            if excel_create['success'] == True:
                                ret =excel_create #{'success': True, 'message': 'Excel sheet is created sucessfully'}
                            else:
                                ret = excel_create
                        else:
                            ret = {'success': False, 'message':'data not found.'}  
            else:
                ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}               
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
        #     print("print(,)", str(error))
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message'] =" ".join(["something error has occered in api", str(error)])
            
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as  error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret) 


# @firesmoke.route('/firesmokeviolation_excel_download', methods=['GET'])
@csrf_exempt
def firesmokeviolation_excel_download(request):
    if request.method == 'GET':
        if 1:
        # try:
            list_of_files = glob.glob(os.path.join(os.getcwd(), "firesmoke_violation_excel_sheets/*"))
            latest_file = max(list_of_files, key=os.path.getctime)
            path, filename = os.path.split(latest_file)
            if filename:
                main_path = os.path.abspath(path)
                with open(latest_file, 'rb') as f:
                    return FileResponse(f, as_attachment=True, filename=filename)
            
            else:
                ret = {'success': False, 'message': 'File is not found.'}
    else:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
    return JsonResponse(ret) 