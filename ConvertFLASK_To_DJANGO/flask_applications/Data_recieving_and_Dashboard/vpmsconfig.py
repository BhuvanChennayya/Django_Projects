from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_config_funcs import *

vehicle_parking = Blueprint('vehicle_parking', __name__)


def roi_data_cf(x, hooter_line, index, roi_enable_cam_ids, lines, traffic_count_cls_name_cls_id,NewcameraID):
    # print("-------------RA WITH -----------roi_data_cf---1----------",x)
    roi_label_names =[]
    label_name_for_hooter =[]
    hooter_list_type =[] 
    if len(x['roi_data']) != 0:  
        # print("kkkk00000000000000000000000000000000000000000000000000888888888888888888888888888888888===",x)      
        if x['alarm_type'] is not None and x['alarm_ip_address'] is not None  and x['alarm_ip_address'] != '':
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1') 
            hooteripstring = '['        
            testpinchrole = False
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                if 'pinch_role' in roi_value:
                    if roi_value['pinch_role']:
                        testpinchrole= True
                # print("x['alarm_ip_address']==== roi details ===",roi_value)
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi11_dataww_cf 1", str(error), " ----time ---- ", now_time_with_time()]))
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                if compare(label_name, roi_label_names) == False:
                    for lab_nam in label_name:
                        if lab_nam not in roi_label_names:
                            roi_label_names.append(lab_nam)
                if type(label_name) == list:
                    if len(label_name) != 0:
                        if len(label_name) == 1:
                            if label_name[0] not in label_name_for_hooter:
                                label_name_for_hooter.append(label_name[0])
                        elif len(label_name) > 1:
                            [label_name_for_hooter.append(i) for i in label_name if i not in label_name_for_hooter]
                    else:
                        print('No label name found in Restricate Area Roi')
                else:
                    print('the label name type is not the list -')
                if isEmpty(roi_value['alarm_type']):
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                    if roi_value['alarm_type']['hooter'] :
                        if  x['alarm_version']['hooter'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['hooter'] =='new':
                            hooter_list_type.append('1;')
                        elif   x['alarm_version']['hooter'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['hooter'] =='type2':
                            hooter_list_type.append('1;')
                        elif   x['alarm_version']['hooter'] =='type3':
                            hooter_list_type.append('1;')
                    if roi_value['alarm_type']['relay']:
                        if  x['alarm_version']['relay'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='new':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='type2':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type3':
                            hooter_list_type.append('2;')
                    if roi_value['alarm_type']['hooter']  == True and roi_value['alarm_type']['relay'] == True :
                        if  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='old' :
                            hooter_list_type.append('0;')
                        elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='new' :
                            hooter_list_type.append('3;')
                        elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type1' :
                            hooter_list_type.append('0;')
                        elif  x['alarm_version']['relay'] =='type2' and  x['alarm_version']['hooter'] =='type2' :
                            hooter_list_type.append('3;')
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_name) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_name)+',null]'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None :
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_name)+',null];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['relay_ip'] is not None :
                                hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_name)+',null];'
            hooter_empty_label_ls = []
            hooter_final_label = 'person;'
            # hooteripstring =hooteripstring+']' 
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
                
            # print("hooteripstringhooteripstringhooteripstringhooteripstring1",hooteripstring)
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            # print("hooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_type--1 ",hooter_list_type)
            if len(hooter_list_type) == 0:
                # print("hooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_type--2 ",hooter_list_type)
                hooter_line.append('hooter-type = {0}'.format('0;'))
            elif len(hooter_list_type) !=0:
                # print("hooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_typehooter_list_type--3 ",hooter_list_type)
                hooter_line.append('hooter-type = {0}'.format(format(''.join(hooter_list_type))))
            # print("hooter_line--------------------------------------------------------------------0000",hooter_line)
            if testpinchrole:
                hooter_line.append('analytics-type = 1')
            else:
                hooter_line.append('analytics-type = 0')
            if hooteripstring== '[' :
                hooteripstring='none'
                hooter_line.append('hooter-enable = 0')
            else:
                hooter_line.append('hooter-enable = 1')
            hooter_line.append('hooter-shoutdown-time = 10 ')
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3\n')              
            #[192.168.1.46:8000,track_1];[192.168.1.46:8000,track_2]      
        else:
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            testpinchrole = False
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                if 'pinch_role' in roi_value:
                    if roi_value['pinch_role']:
                        testpinchrole= True
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_dddata_cf 2", str(error), " ----time ---- ", now_time_with_time()]))
                    roi_bbox = (roi_value['bb_box'])
                if compare(label_name, roi_label_names) == False:
                    for lab_nam in label_name:
                        if lab_nam not in roi_label_names:
                            roi_label_names.append(lab_nam)

                if type(label_name) == list:
                    if len(label_name) != 0:
                        if len(label_name) == 1:
                            if label_name[0] not in label_name_for_hooter:
                                label_name_for_hooter.append(label_name[0])
                        elif len(label_name) > 1:
                            [label_name_for_hooter.append(i) for i in label_name if i not in label_name_for_hooter]
                    else:
                        print('No label name found in Restricted Area')
                else:
                    print('the label name type is not the list -')
                if isEmpty(roi_value['alarm_type']):
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                    # print("roi_value['alarm_type']====================",roi_value['alarm_type'])
                            
                    if roi_value['alarm_type']['hooter'] :
                        if  x['alarm_version']['hooter'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['hooter'] =='new':
                            hooter_list_type.append('1;')
                        elif   x['alarm_version']['hooter'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['hooter'] =='type2':
                            hooter_list_type.append('1;')
                        elif   x['alarm_version']['hooter'] =='type3':
                            hooter_list_type.append('1;')
                    if roi_value['alarm_type']['relay']:
                        if  x['alarm_version']['relay'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='new':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='type2':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type3':
                            hooter_list_type.append('2;')
                    if roi_value['alarm_type']['hooter']  == True and roi_value['alarm_type']['relay'] == True :
                        if  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='old' :
                            hooter_list_type.append('0;')
                        elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='new' :
                            hooter_list_type.append('3;')
                        elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type1' :
                            hooter_list_type.append('0;')
                        elif  x['alarm_version']['relay'] =='type2' and  x['alarm_version']['hooter'] =='type2' :
                            hooter_list_type.append('3;')
                    # print('hooter_list_type-----------------------',hooter_list_type)
                    # print("came into iiiiii===========222=========",roi_value['alarm_type'] )
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                # print('---------------1',x['alarm_ip_address']['hooter_ip'])
                                # print("--------------1 roi name ==", roi_name)
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_name) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_name)+',null]'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None :
                                # print('---------------2',x['alarm_ip_address']['hooter_ip'])
                                # print("--------------2 roi name ==", roi_name)
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_name)+',null];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['relay_ip'] is not None :
                                # print('--------------------3',x['alarm_ip_address']['relay_ip'])
                                # print("--------------3 roi name ==", roi_name)
                                hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_name)+'];'
            hooter_empty_label_ls = []
            hooter_final_label = 'person;'
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            if len(hooter_list_type) == 0:
                hooter_line.append('hooter-type = {0}'.format('0;'))
            elif len(hooter_list_type) !=0:
                hooter_line.append('hooter-type = {0}'.format(format(''.join(hooter_list_type))))

            if testpinchrole:
                hooter_line.append('analytics-type = 1')
            else:
                hooter_line.append('analytics-type = 0')
            if hooteripstring== '[' :
                hooteripstring='none'
                hooter_line.append('hooter-enable = 0')
            else:
                hooter_line.append('hooter-enable = 1')
            hooter_line.append('hooter-shoutdown-time = 10 ')
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3\n')      
        lines.append('[roi-filtering-stream-{0}]'.format(index))
        lines.append('enable=1')        
        for test_roi_ra, roi_value in enumerate(x['roi_data']):
            label_name = roi_value['label_name']
            roi_name = roi_value['roi_name']
            try:
                roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
            except Exception as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_deeata_cf 3", str(error), " ----time ---- ", now_time_with_time()]))
                roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
            if compare(label_name, roi_label_names) == False:
                for lab_nam in label_name:
                    if lab_nam not in roi_label_names:
                        roi_label_names.append(lab_nam)
            roi_bbox= checkNegativevaluesinBbox(roi_bbox)
            lines.append('roi-RA-{0} = {1}'.format(roi_name, roi_bbox))            
        fun_config_analytics_file = cr_fun_conf_anlytics(x, lines,  traffic_count_cls_name_cls_id)
        roi_enable_cam_ids.append(NewcameraID)
    return True

def FETCH_VEHICLE_PARKING_DATAFROMMONGO():
    data = []#pictures: { $exists: true, $type: 'array', $ne: [] }
    # fetch_require_data = list(mongo.db.ppera_cameras.find({'camera_status': True, "analytics_status": 'true', "$where":"firesmoke_data.length > 0"}))
    fetch_require_data = list(mongo.db.ppera_cameras.find({'camera_status': True, "analytics_status": 'true','vehicle_parking_data':{'$exists':True,"$ne": []}}))
    if len(fetch_require_data) != 0:
        for i in fetch_require_data:
            J={}
            if i['vehicle_parking_data'][0]['fire'] != False or i['firesmoke_data'][0]['smoke'] != False:
                J['firesmoke_data']=i['firesmoke_data']
                if 'camera_type' in i['firesmoke_data'][0]:
                    J['camera_type'] = i['firesmoke_data'][0]['camera_type']
                else:
                    J['camera_type'] = ''
            elif  i['firesmoke_data'][0]['dust'] != False :
                J['firesmoke_data']=i['firesmoke_data']
                if 'camera_type' in i['firesmoke_data'][0]:
                    J['camera_type'] = i['firesmoke_data'][0]['camera_type']
                else:
                    J['camera_type'] = ''
            if ENABLED_SOLUTION_IS_EMPTY_DICT(J) :
                J['cameraname']=i['cameraname']
                J['alarm_type']=i['alarm_type']
                J['alarm_ip_address']=i['alarm_ip_address']
                J['rtsp_url']=i['rtsp_url']
                data.append(J)
    return data



def VPMSCONFIG(media,data_save_interval):
    ret = {'message': 'something went wrong with create config update_cam_id__.', 'success': False}
    getdata_response = FETCH_VEHICLE_PARKING_DATAFROMMONGO()
    if len(getdata_response) != 0:
        function__response = WRITEVPMSMULTICONFIG(getdata_response,media,data_save_interval)
        # return_data_update_camera = UPdatemulticonfigCamid(function__response)
        return_data_update_camera ='200'
        if return_data_update_camera == '200':
            ret = { 'message': 'fire and smoke application is started successfully.', 'success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'please enable and add the ai analytics solutions.'
    return ret




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
    


@vehicle_parking.route('/add_Parking_roi', methods=['POST'])
def add_Parking_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'vpms_data', 'ai_solutions', ]
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            vpms_data = data['vpms_data']
            ai_solutions = data['ai_solutions']
            # print('---------------------------------------while adding---------------vpms_data',vpms_data)
            # print('---------------------------------------while adding---------------ai_solutions',ai_solutions)
            # print('---------------------------------------while adding---------------id',id)
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if vpms_data is not None:
                    if len(vpms_data) != 0:
                        if type(vpms_data) ==list:
                            if ai_solutions is not None:
                                if type(ai_solutions) == list:
                                    if len(ai_solutions) != 0:
                                        ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'vpms_data': vpms_data,'ai_solution': ai_solutions}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'vehicle parking configuration details added successfully.','success': True}
                                        else:
                                            ret['message'] = 'vehicle parking configuration details not adeed.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                elif type(ai_solutions) == dict:
                                    if isEmpty(ai_solutions) :
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'vpms_data': vpms_data,'ai_solution': finddata['ai_solution']}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'vehicle parking configuration details added successfully.','success': True}
                                        else:
                                            ret['message'] = 'vehicle parking configuration details not adeed.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                else:
                                    ret['message'] = 'please give proper ai_solutions, it should be list type.'
                            else:
                                ret['message'] = 'please give proper ai_solutions.'
                        else:
                            ret['message']='please give proper input vpms_data type should be list.'   
                    else:
                        ret['message']='please give proper input parameters.'               
                else:
                    ret['message'] = 'please give proper Restricted Area data, it should not none type.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@vehicle_parking.route('/edit_Parking_roi', methods=['POST'])
def edit_Parking_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ai_solutions', 'vpms_data','roi_id']
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
            vpms_data = data['vpms_data']
            print("-----------id-----",id)
            print("ai_solutions====",ai_solutions)
            # print("==vpms_data==",vpms_data)
            print("--------------------inputdataof  edit ============------",data )
            print("\n\n\n")
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            print("----------------------fetched_data -------",finddata)
            if finddata is not None:
                print("------------------------------11-11")
                if type(vpms_data) == list:
                    print("------------------------------11-11")
                    if len(vpms_data) != 0:
                        if isEmpty(ai_solutions):
                            MONDATAFetchedData = finddata['vpms_data']
                            if len(MONDATAFetchedData) != 0:
                                if len(MONDATAFetchedData) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': vpms_data, 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'vehicle parking configuration details updated successfully.','success': True}
                                    else:
                                        print("------vehicle parking configuration details not updated-------------0000001.6.")
                                        ret['message'] = 'vehicle parking configuration details not updated.'
                                elif len(MONDATAFetchedData) > 1:
                                    update_data = []
                                    if len(vpms_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(MONDATAFetchedData):
                                            if int(i['roi_id']) == int(roi_id):
                                                i['bb_box'] = vpms_data[0]['bb_box']
                                                if 'pinch_role' in vpms_data[0] :
                                                    i['pinch_role']= vpms_data[0]['pinch_role']
                                                update_data.append(vpms_data[0])
                                            else:
                                                update_data.append(i)
                                        # print("---------------------MONDATAFetchedData--------------",MONDATAFetchedData)
                                        # print("------------------update_data-------------------",update_data)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'vpms_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                        if result.modified_count > 0:
                                            print("------vehicle parking configuration details updated-------------0000001.5.")
                                            ret = {'message': 'vehicle parking updated successfully.','success': True}
                                        else:
                                            print("------vehicle parking configuration details not updated-------------0000001.5.")
                                            ret['message'] = 'vehicle parking configuration details not updated.'                                    
                                    else:
                                        ret['message'] = 'There is no roi region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        elif len(MONDATAFetchedData) != 0:
                            update_data = []
                            if len(MONDATAFetchedData) == 1:
                                final_ai = (set(ai_solutions).union(set (finddata['ai_solution'])))
                                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'vpms_data': vpms_data, 'ai_solution': final_ai}})
                                if result.modified_count > 0:
                                    ret = {'message': 'vehicle parking configuration details data updated successfully.','success': True}
                                else:
                                    print("------roi not updated-------------0000001.2.")
                                    ret['message'] = 'vehicle parking configuration details not updated.'
                            elif len(MONDATAFetchedData) > 1:
                                if len(vpms_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(MONDATAFetchedData):
                                        if int(i['roi_id']) == int(roi_id):
                                            i['bb_box'] = vpms_data[0]['bb_box']
                                            update_data.append(vpms_data[0])
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'vehicle parking configuration details data updated successfully.','success': True}
                                    else:
                                        print("------roi not updated-------------0000001.3.")
                                        ret['message'] = 'vehicle parking configuration details not updated.'
                                elif len(vpms_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(MONDATAFetchedData):
                                        for __, jjk in enumerate(MONDATAFetchedData):
                                            if int(i['roi_id']) == int(roi_id):
                                                i['bb_box'] = jjk['bb_box']
                                                if jjk not in update_data:
                                                    update_data.append(jjk)
                                            else:
                                                if i not in update_data:
                                                    update_data.append(i)
                                                if jjk not in update_data:
                                                    update_data.append(jjk)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'vehicle parking configuration details data updated successfully.','success': True}
                                    else:
                                        print("------roi not updated-------------0000001.4.")
                                        ret['message'] = 'vehicle parking configuration details not updated.'
                                else:
                                    ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            ret['message'] = 'There is no camrea details exist , please try to add.'
                    else:
                        ret['message'] = 'vehicle parking details should not be empty list.'
                else:
                    ret['message'] = 'vehicle parking details type should be list'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@vehicle_parking.route('/delete_parkingRoi', methods=['POST'])
def delete_parkingRoi():
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
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if isEmpty(ai_solutions) :
                            vpms_data = finddata['vpms_data']
                            if len(vpms_data) != 0:
                                update_data = []
                                if len(vpms_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    print("finddata['ai_solution']",finddata['ai_solution'])
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.0')
                                        ret = {'message':'vehicle parking details delete successfully.','success': True}
                                    else:
                                        print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.1')
                                        ret['message'] = 'vehicle parking details not deleted.'
                                elif len(vpms_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(vpms_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            # vpms_data.remove(i)
                                            print('---------------------remov--------',roi_id)
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.2')
                                        ret = {'message': 'vehicle parking details delete successfully.','success': True}
                                    else:
                                        print('-----------------------------kkkkadskskkkk--------delete-roi---1.0.3')
                                        ret['message'] = 'vehicle parking details not deleted.'
                            else:
                                ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            vpms_data = finddata['vpms_data']
                            if len(vpms_data) != 0:
                                if len(vpms_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'vehicle parking details delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'vehicle parking details not deleted.'
                                elif len(vpms_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(vpms_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            print('---------------------remov--------',roi_id)
                                            # vpms_data.remove(i)
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'vpms_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'vehicle parking details delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'vehicle parking details not deleted.'
                            else:
                                ret['message'] = 'There is no roi region the camrea, please try to add.'
                    else:
                        ret['message'] = 'please give proper vehicle parking details, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] =" ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    except Exception as error:
        ret['message'] =" ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_roi 1", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@vehicle_parking.route('/add_TrafficJam_roi', methods=['POST'])
def add_TrafficJam_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'trafficjam_data', 'ai_solutions', ]
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            trafficjam_data = data['trafficjam_data']
            ai_solutions = data['ai_solutions']
            print('---------------------------------------while adding---------------vpms_data',trafficjam_data)
            print('---------------------------------------while adding---------------ai_solutions',ai_solutions)
            print('---------------------------------------while adding---------------id',id)
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if trafficjam_data is not None:
                    if len(trafficjam_data) != 0:
                        if type(trafficjam_data) ==list:
                            if ai_solutions is not None:
                                if type(ai_solutions) == list:
                                    if len(ai_solutions) != 0:
                                        ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'trafficjam_data': trafficjam_data,'ai_solution': ai_solutions}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'trafficjam configuration details added successfully.','success': True}
                                        else:
                                            ret['message'] = 'trafficjam configuration details not adeed.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                elif type(ai_solutions) == dict:
                                    if isEmpty(ai_solutions) :
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'trafficjam_data': trafficjam_data,'ai_solution': finddata['ai_solution']}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'trafficjam configuration details added successfully.','success': True}
                                        else:
                                            ret['message'] = 'trafficjam parking configuration details not adeed.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                else:
                                    ret['message'] = 'please give proper ai_solutions, it should be list type.'
                            else:
                                ret['message'] = 'please give proper ai_solutions.'
                        else:
                            ret['message']='please give proper input vpms_data type should be list.'   
                    else:
                        ret['message']='please give proper input parameters.'               
                else:
                    ret['message'] = 'please give proper trafficjam configuration details, it should not none type.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@vehicle_parking.route('/edit_TrafficJam_roi', methods=['POST'])
def edit_TrafficJam_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ai_solutions', 'trafficjam_data','roi_id']
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
            trafficjam_data = data['trafficjam_data']
            print("-----------id-----",id)
            print("ai_solutions====",ai_solutions)
            print("==vpms_data==",trafficjam_data)
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(trafficjam_data) == list:
                    if len(trafficjam_data) != 0:
                        if isEmpty(ai_solutions):
                            MONDATAFetchedData = finddata['trafficjam_data']
                            if len(MONDATAFetchedData) != 0:
                                if len(MONDATAFetchedData) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': trafficjam_data, 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'trafficjam configuration details updated successfully.','success': True}
                                    else:
                                        print("------vehicle parking configuration details not updated-------------0000001.6.")
                                        ret['message'] = 'trafficjam configuration details not updated.'
                                elif len(MONDATAFetchedData) > 1:
                                    update_data = []
                                    if len(trafficjam_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(MONDATAFetchedData):
                                            if int(i['roi_id']) == int(roi_id):
                                                i['bb_box'] = trafficjam_data[0]['bb_box']
                                                if 'pinch_role' in trafficjam_data[0] :
                                                    i['pinch_role']= trafficjam_data[0]['pinch_role']
                                                update_data.append(trafficjam_data[0])
                                            else:
                                                update_data.append(i)
                                        print("---------------------MONDATAFetchedData--------------",MONDATAFetchedData)
                                        print("------------------update_data-------------------",update_data)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'trafficjam_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                        if result.modified_count > 0:
                                            print("------vehicle parking configuration details updated-------------0000001.5.")
                                            ret = {'message': 'trafficjam configuration details updated successfully.','success': True}
                                        else:
                                            print("------vehicle parking configuration details not updated-------------0000001.5.")
                                            ret['message'] = 'trafficjam configuration details not updated.'                                    
                                    else:
                                        ret['message'] = 'There is no roi region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        elif len(MONDATAFetchedData) != 0:
                            update_data = []
                            if len(MONDATAFetchedData) == 1:
                                final_ai = (set(ai_solutions).union(set (finddata['ai_solution'])))
                                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'trafficjam_data': trafficjam_data, 'ai_solution': final_ai}})
                                if result.modified_count > 0:
                                    ret = {'message': 'trafficjam configuration details data updated successfully.','success': True}
                                else:
                                    print("------roi not updated-------------0000001.2.")
                                    ret['message'] = 'trafficjam configuration details not updated.'
                            elif len(MONDATAFetchedData) > 1:
                                if len(trafficjam_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(MONDATAFetchedData):
                                        if int(i['roi_id']) == int(roi_id):
                                            i['bb_box'] = trafficjam_data[0]['bb_box']
                                            update_data.append(trafficjam_data[0])
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'trafficjam configuration details data updated successfully.','success': True}
                                    else:
                                        print("------roi not updated-------------0000001.3.")
                                        ret['message'] = 'trafficjam configuration details not updated.'
                                elif len(trafficjam_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(MONDATAFetchedData):
                                        for __, jjk in enumerate(MONDATAFetchedData):
                                            if int(i['roi_id']) == int(roi_id):
                                                i['bb_box'] = jjk['bb_box']
                                                if jjk not in update_data:
                                                    update_data.append(jjk)
                                            else:
                                                if i not in update_data:
                                                    update_data.append(i)
                                                if jjk not in update_data:
                                                    update_data.append(jjk)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'trafficjam configuration details data updated successfully.','success': True}
                                    else:
                                        print("------roi not updated-------------0000001.4.")
                                        ret['message'] = 'trafficjam configuration details not updated.'
                                else:
                                    ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            ret['message'] = 'There is no camrea details exist , please try to add.'
                    else:
                        ret['message'] = 'trafficjam configuration details should not be empty list.'
                else:
                    ret['message'] = 'trafficjam configuration details type should be list'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret


@vehicle_parking.route('/delete_TrafficJamRoi', methods=['POST'])
def delete_TrafficJamRoi():
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
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if isEmpty(ai_solutions) :
                            trafficjam_data = finddata['trafficjam_data']
                            if len(trafficjam_data) != 0:
                                update_data = []
                                if len(trafficjam_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    print("finddata['ai_solution']",finddata['ai_solution'])
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        print('-----------------------------Trafficjam--------delete-roi---1.0.0')
                                        ret = {'message':'trafficjam configuration details delete successfully.','success': True}
                                    else:
                                        print('-----------------------------Trafficjam--------delete-roi---1.0.1')
                                        ret['message'] = 'trafficjam configuration details not deleted.'
                                elif len(trafficjam_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(trafficjam_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            # trafficjam_data.remove(i)
                                            print()
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        print('-----------------------------Trafficjam--------delete-roi---1.0.2')
                                        ret = {'message': 'trafficjam configuration details delete successfully.','success': True}
                                    else:
                                        print('-----------------------------Trafficjam--------delete-roi---1.0.3')
                                        ret['message'] = 'trafficjam configuration details not deleted.'
                            else:
                                ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            trafficjam_data = finddata['trafficjam_data']
                            if len(trafficjam_data) != 0:
                                if len(trafficjam_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'trafficjam configuration details delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'roi not deleted.'
                                elif len(trafficjam_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(trafficjam_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            # trafficjam_data.remove(i)
                                            print()
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'trafficjam_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'trafficjam configuration details delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'trafficjam configuration details not deleted.'
                            else:
                                ret['message'] = 'There is no roi region the camrea, please try to add.'
                    else:
                        ret['message'] = 'please give proper trafficjam configuration details, it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] =" ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    except Exception as error:
        ret['message'] =" ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_roi 1", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@vehicle_parking.route('/start_VPMSAPP', methods=['GET'])
@vehicle_parking.route('/start_VPMSAPP', methods=['POST'])
def start_VPMSAPP():
    ret = {'message': 'something went wrong with create config.', 'success': False}


    if request.method=='POST':
        jsonobject = request.json
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
                    Truncatefiresmokecamera()
                    common_return_data = VPMSCONFIG(media_type,data_interval)
                    if common_return_data:
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
        ret = ret
    return ret


@vehicle_parking.route('/stop_VPMSAPP', methods=['GET'])
def stop_VPMSAPP():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        firesmoke_app_monitoring_started(True)
        mongo.db.firesmokecamerastatus.delete_many({})
        Truncatefiresmokecamera()
        ret = {'message': 'fire smoke application stopped.', 'success': True}
    else:
        ret = ret
    return ret

def WRITEVPMSMULTICONFIG(response,media,data_save_interval):
    print("------------------------response-----OF--FIRE----AND----SMOKE----------------",response)
    allWrittenSourceCAmIds =[]
    numberofsources_= 4
    new_response = split_list(response,numberofsources_)
    camera_id =1 
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'firesmokesampleconfig.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/fire_and_smoke'+'/configs'
    yolo_config_path = get_current_dir_and_goto_parent_dir() + '/models/firemodel'
    traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)
    if not os.path.exists(yolo_config_path):
        os.makedirs(yolo_config_path)
    if not os.path.exists(traffic_config_path):
        os.makedirs(traffic_config_path)         
    remove_text_files(deepstream_config_path)   
    print("------------------------new_response----OF--FIRE----AND----SMOKE-------",new_response)  
    for config_index, writingresponse in enumerate(new_response): 
        print("-------------------------writingresponse----OF---FIRE-AND----SMOKE--------", writingresponse) 
        config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
        config_analytics_configfile = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
        lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', 'display-font-size=12', '']
        normal_config_file = 0
        analyticsline =[]
        print("length == === 1", len(writingresponse))
        with open(sample_config_file) as file:
            for write_config, line in enumerate(file):
                if line.strip() == '[application]':
                    lines.append('[application]')
                    lines.append('enable-perf-measurement=1')
                    lines.append('perf-measurement-interval-sec=1')
                
                elif line.strip() == '[tiled-display]':
                    finaL_RA_PPE = writingresponse
                    total_stream_for_stremux_union = finaL_RA_PPE
                    num = math.sqrt(int(len(finaL_RA_PPE)))
                    print("num----",num )
                    print("num----",num )
                    if 1 < num < 1.4:
                        rows = 1
                        columns = 2
                    elif num == 1:
                        rows = 1
                        columns = 2
                    else:
                        if 1 > num >= 1.4:
                            if len(finaL_RA_PPE)>3:
                                rows = 2
                                columns = 2
                            else:
                                rows = 1
                                columns = 2
                                
                        else:
                            rows = int(round(num))
                            columns = 2
                        print("row====s ",rows)
                        print("columns====s ",columns)

                    lines.append('[tiled-display]')
                    lines.append('enable=1')
                    lines.append('rows={0}'.format(str(rows)))
                    lines.append('columns={0}'.format(str(columns)))
                    lines.append('width=960')
                    lines.append('height=544')
                    lines.append('gpu-id=0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[sources]':  
                    print("newlength===2", len(writingresponse))
                    for n, x in enumerate(writingresponse):
                        print("-----------------------x-------------------firesmokeconfig-1",x)
                        cam_id = '{0}'.format(int(n))
                        find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                        if find_data is not None:
                            if find_data['rtsp_flag'] == '1':
                                if 'rtsp' in x['rtsp_url']:
                                    x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                        if len(x['firesmoke_data'])>0 and ( x['firesmoke_data'][0]['fire'] != False or x['firesmoke_data'][0]['smoke'] != False) or  x['firesmoke_data'][0]['dust'] != False:
                            print('[source{0}]'.format(normal_config_file))
                            print("x['firesmoke_data']===",x['firesmoke_data'])
                            labelnames = ''
                            if 'dust' in x['firesmoke_data'][0] and 'fire' in x['firesmoke_data'][0] :
                                if x['firesmoke_data'][0]['dust']:
                                    labelnames='dust;'
                                if  x['firesmoke_data'][0]['fire']:
                                    if labelnames != '' and labelnames is not None:
                                        labelnames+='fire;'
                                if   x['firesmoke_data'][0]['smoke']:
                                    if labelnames != '' and labelnames is not None:
                                        labelnames+='smoke;'
                            uri = x['rtsp_url']
                            lines.append('[source{0}]'.format(normal_config_file))
                            lines.append('enable=1')
                            lines.append('type=4')
                            lines.append('uri = {0}'.format(uri))
                            lines.append('num-sources=1')
                            lines.append('gpu-id=0')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('latency=100')
                            lines.append('camera-id={0}'.format(camera_id))
                            camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                            allWrittenSourceCAmIds.append(camera_required_data)
                            lines.append('camera-name={0}'.format(x['cameraname']))
                            lines.append("rtsp-reconnect-interval-sec=2")
                            lines.append('drop-frame-interval = 1\n')
                            analyticsline.append('[fsd{0}]'.format(str(normal_config_file)))
                            # [fsd0]
                            # enable=1
                            # process-mode=0
                            # image-save-interval=10
                            # operate-on=fire;smoke;dust
                            analyticsline.append('enable = 1')  
                            analyticsline.append('process-mode = {0}'.format(media))
                            analyticsline.append('image-save-interval = {0}'.format(data_save_interval)) #
                            if labelnames != '' and labelnames is not None:
                                analyticsline.append('operate-on={0}'.format(labelnames)) 
                            else:
                                analyticsline.append('operate-on=fire;') 
                            x['cameraid']=camera_id
                            FireANDSMOKeCAMERASTATUSUPDATE(x)
                            normal_config_file += 1
                            camera_id += 1

                elif line.strip() == '[sink0]':
                    lines.append('[sink0]')

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
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[streammux]':
                    lines.append('[streammux]')
                    lines.append('gpu-id=0')
                    lines.append('live-source=1')
                    lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('batched-push-timeout=40000')
                    lines.append('width=1920')
                    lines.append('height=1080')
                    lines.append('enable-padding=0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[primary-gie]':
                    lines.append('[primary-gie]')
                    lines.append('enable=1')
                    lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('bbox-border-color0=1;0;0;1')
                    lines.append('bbox-border-color1=0;1;1;1')
                    lines.append('bbox-border-color2=0;0;1;1')
                    lines.append('bbox-border-color3=0;1;0;1')
                    lines.append('nvbuf-memory-type=0')
                    lines.append('interval=0')
                    lines.append('gie-unique-id=1')
                    lines.append('config-file=../../models/FSD.txt')  
                # elif line.strip() == '[secondary-gie0]':
                #     lines.append('[secondary-gie0]')
                #     lines.append('enable = 1')
                #     lines.append('gpu-id = 0')
                #     lines.append('gie-unique-id = 5')
                #     lines.append('operate-on-gie-id = 1')
                #     lines.append('operate-on-class-ids = 0;')
                #     lines.append('batch-size = 1')
                #     lines.append('bbox-border-color0 = 1;0;1;0.7')
                #     lines.append('frame-verification=10bbox-border-color1 = 1;0;0;0.7')
                #     lines.append('config-file = ../../models/smoke_Nov_23.txt')

                elif line.strip() == '[tracker]':
                    lines.append('[tracker]')

                elif line.strip() == '[tests]':
                    lines.append('[tests]')

                elif line.strip() == '[docketrun-analytics]':
                    lines.append('[docketrun-analytics]')
                    # lines.append('smart-record-stop-buffer = 2\n')

                elif line.strip() == '[docketrun-image]':
                    lines.append('[docketrun-image]')
                elif line.strip() == '[fsd]':
                    lines.append('[fsd]')
                    lines.append('enable=1')
                    lines.append('frame-verification=10')
                    lines.append('fsd-config-file=./fsd_custom_{0}.txt'.format(config_index+1))
                else:
                    lines.append(line.strip())  

        with open(config_file, 'w') as f:
            for O_O_O, item in enumerate(lines):
                f.write('%s\n' % item)

        with open(config_analytics_configfile, 'w') as config_analyticsfile:
            for jim in analyticsline:
                config_analyticsfile.write('%s\n' % jim)
    return allWrittenSourceCAmIds


     
# @firesmoke.route('/getFireVideo/<vidoename>', methods=['GET'])
# def firevidoe(vidoename):
#     try:
#         base_path = get_current_dir_and_goto_parent_dir()+'/images/sm_rec'
#         response = send_from_directory(base_path, vidoename)
#         return response
#     except Exception as  error:
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
#         return str(error)
    
    

@vehicle_parking.route('/getVPMSAPPVideo/<vidoename>', methods=['GET'])
def getVPMSAPPVideo(vidoename):
    try:
        base_path = get_current_dir_and_goto_parent_dir()+'/images/sm_rec'
        video_path = os.path.join(base_path, vidoename)

        # Check if the request explicitly wants an mp4 file
        if request.headers.get('Accept') == 'video/mp4':
            return send_file(video_path, as_attachment=True, mimetype='video/mp4')
        
        # Otherwise, use the default behavior
        response = send_from_directory(base_path, vidoename)
        return response
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return str(error)
    
    
@vehicle_parking.route('/GETVPMSAPPIMAGE/<imagename>', methods=['GET'])
def GETVPMSAPPIMAGE(imagename):
    try:
        base_path = get_current_dir_and_goto_parent_dir()+'/images/fsd'
        video_path = os.path.join(base_path, imagename)
        image_data = mongo.db.firesmokeviolationdata.find_one({'video_file_name': imagename})
        if image_data is not None:
            if len(image_data['object_details']) == 1:
                height = image_data['object_details'][0]['bbox']['H']
                width = image_data['object_details'][0]['bbox']['W']
                x_value = image_data['object_details'][0]['bbox']['X']
                y_value = image_data['object_details'][0]['bbox']['Y']
                file_path = os.path.join(base_path, imagename)
                w, h = width, height
                shape = [(x_value, y_value),(x_value+width, y_value+height)]#[(x_value, y_value),(width, height)]#[(x_value, y_value), (w - 10, h - 10)](X + W, Y + H)
                # print("for single shape==",shape)
                source_img = Image.open(file_path)
                draw = ImageDraw.Draw(source_img)
                draw.rectangle(shape, outline='red', width=3)
                draw.text((x_value + 6, y_value + 2), 'dust', 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 28,encoding='unic'))
                imgByteArr = io.BytesIO()
                source_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=imagename)
            elif len(image_data['object_details']) > 1:
                    file_path = os.path.join(base_path, imagename)
                    source_img = Image.open(file_path)
                    for ___, thiru in enumerate(image_data['object_details']):
                        height = thiru['bbox']['H']
                        width = thiru['bbox']['W']
                        x_value = thiru['bbox']['X']
                        y_value = thiru['bbox']['Y']
                        w, h = width, height
                        shape = [(x_value, y_value),(x_value+width, y_value+height)]
                        draw = ImageDraw.Draw(source_img)
                        draw.rectangle(shape, outline='red', width=3)
                        draw.text((x_value + 6, y_value + 2),  'dust', 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        28, encoding='unic'))
                    imgByteArr = io.BytesIO()
                    source_img.save(imgByteArr, format='JPEG')
                    imgByteArr.seek(0)
                    return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=imagename)
            else:
                response = send_from_directory(base_path, imagename)
        return response
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return str(error)
    

    

@vehicle_parking.route('/DeleteVPMSAPPViolation/<id>', methods=['GET'])
def DeleteVPMSAPPViolation(id=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    try:
        if id is not None:
            find_data = mongo.db.firesmokeviolationdata.find_one({'_id': ObjectId(id)})
            if find_data is not None:
                result = mongo.db.firesmokeviolationdata.delete_one({'_id':ObjectId(id)})
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
    return ret



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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_pagination 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30


@vehicle_parking.route('/VPMSAPPverification/<id>/<flag>', methods=['GET'])
def VPMSAPPverification(id=None, flag=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    try:
        if id is not None:
            if flag is not None:
                if flag != 'undefined':
                    find_data = mongo.db.firesmokeviolationdata.find_one({'_id': ObjectId(id)})
                    if find_data is not None:
                        print("flag ===",flag)
                        if flag == 'false':
                            result = mongo.db.firesmokeviolationdata.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False, 'violation_verificaton_status': True}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.','success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        elif flag == 'true':
                            result = mongo.db.firesmokeviolationdata.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': True,  'violation_verificaton_status': True}})
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
    return ret


@vehicle_parking.route('/VPMSAPPLiveviolationdata', methods=['GET'])
@vehicle_parking.route('/VPMSAPPLiveviolationdata/<camera_name>', methods=['GET'])
def FiresmokeLiveviolationdata( camera_name=None):
    ret = {'success': False,'message':"something went wrong in live_data1 apis"}
    if 1:    
        dash_data = []
        if camera_name is not None :
            match_data = {'start_time':{'$regex': '^' + str(date.today())},'camera_name': camera_name,'violation_status': True}# {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}
            data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}},
                                                 {'$limit': 4000000}, {'$sort':{'_id': -1}},{'$project': {"_id":0,'data':1,}},
                                                 {'$project': {'data.camera_rtsp': 0,'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,'data.violation_status':0,'data.ticketno':0}}]))
            if len(data) != 0:
                for count, i in enumerate(data):
                    i['SNo'] = count
                    dash_data.append(i)
                ret = live_data_pagination(len(dash_data), parse_json(dash_data))
            else:
                ret['message'] = 'data not found'
        else:
            match_data = {'start_time':{'$regex': '^' + str(date.today())},'violation_status': True}
            data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data},  {'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}},                                                  
                                                 {'$limit': 4000000}, {'$sort':{'_id': -1}},
                                                #  {'$project': {"_id":0,'data':1,}},
                                                #  {'$project': {'data.camera_rtsp': 0,'data.appruntime':0,
                                                #                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                #                'data.cameraid':0,'data.id_no':0,'data.violation_status':0,'data.ticketno':0}}
                                                 ]))
            if len(data) != 0:
                for count, i in enumerate(data):
                    i['SNo'] = count
                    dash_data.append(i)
                ret =live_data_pagination(len(dash_data), parse_json(dash_data)) 
            else:
                ret['message'] = 'data not found'  
    return jsonify(ret)


@vehicle_parking.route('/datewiseVPMSAPP', methods=['POST'])
@vehicle_parking.route('/datewiseVPMSAPP/<cameraname>', methods=['POST'])
@vehicle_parking.route('/datewiseVPMSAPP/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@vehicle_parking.route('/datewiseVPMSAPP/<pagenumber>/<page_limit>', methods=['POST'])
def datewiseVPMSAPP(cameraname=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
    # try:
        jsonobject = request.json
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
                    match_data = {'start_time':{'$gte': from_date, '$lte': to_date}, 'camera_name':  cameraname, 'violation_status': True}
                    data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}}   ]))
                                                # , {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                                                #  {'$project': {'data.camera_rtsp': 0,'data.appruntime':0,
                                                #                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                #                'data.cameraid':0,'data.id_no':0,'data.violation_status':0,'data.ticketno':0}}]))
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
                    match_data = {'start_time':{'$gte': from_date, '$lte': to_date}, 'violation_status': True}
                    data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}}, ]))
                                                #  {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                                                #  {'$project': {'data.camera_rtsp': 0,'data.appruntime':0,
                                                #                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                #                'data.cameraid':0,'data.id_no':0,'data.violation_status':0,'data.ticketno':0}}]))
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
    return jsonify(ret)



@vehicle_parking.route('/VPMSAPPcameradetails', methods=['GET'])
@vehicle_parking.route('/VPMSAPPcameradetails', methods=['POST'])
def VPMSAPPcameradetails():
    ret = {'success': False, 'message':'something went wrong with camera_details details'}
    if request.method == 'POST':
        jsonobject = request.json
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
                match_data = {'start_time':{'$gte':from_date, '$lte': to_date}}
                data = list(mongo.db.firesmokeviolationdata.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                                                    {'$project': {'data': 0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['camera_name'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            
    elif request.method == 'GET':
        
        try:
            match_data =  {'start_time':{'$regex': '^' + str(date.today())}}
            data = list(mongo.db.firesmokeviolationdata.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
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
    # try:
    #     data = list(mongo.db.firesmokeviolationdata.aggregate([{'$sort': {'start_time': -1}}, {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
    #                                          {'$project': {'data': 0}}]))
    #     dash_data = []
    #     if len(data) != 0:
    #         for count, i in enumerate(data):
    #             dash_data.append(i['_id']['camera_name'])
    #         ret = {'success': True, 'message': parse_json(dash_data)}
    #     else:
    #         ret['message'] = 'data not found'
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_details 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return jsonify(ret)



@vehicle_parking.route('/VPMSAPPdepartmentdetails', methods=['GET'])
@vehicle_parking.route('/VPMSAPPdepartmentdetails', methods=['POST'])
def VPMSAPPdepartmentdetails():
    ret = {'success': False, 'message':'something went wrong with camera_details details'}
    if request.method == 'POST':
        jsonobject = request.json
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
                match_data = {'start_time':{'$gte':from_date, '$lte': to_date}}
                pipeline = [
                {'$sort': {'_id': -1}},
                {'$match': match_data},
                {
                    '$lookup': {
                        'from': 'ppera_cameras',
                        'localField': 'camera_name',
                        'foreignField': 'cameraname',
                        'as': 'camera_data'
                    }
                },
                {'$unwind': '$camera_data'},
                {
                    '$project': {
                        '_id': 0,
                        'cameraname': '$camera_name',
                        'department': '$camera_data.department'
                    }
                }
                         ]
            
                data = list(mongo.db.firesmokeviolationdata.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
                # data = list(mongo.db.firesmokeviolationdata.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                #                                     {'$project': {'data': 0}}]))
                # dash_data = []
                # if len(data) != 0:
                #     for count, i in enumerate(data):
                #         finddata = mongo.db.ppera_cameras.find_one({'cameraname': i['_id']['camera_name']})
                #         if finddata is not None :
                #             dash_data.append(finddata['department'])
                #         # dash_data.append(i['_id']['camera_name'])
                #     ret = {'success': True, 'message': parse_json(dash_data)}
                # else:
                #     ret['message'] = 'data not found'
            
    elif request.method == 'GET':
        dash_data  =[]
        try:
            match_data =  {'start_time':{'$regex': '^' + str(date.today())}}
            pipeline = [
                {'$sort': {'_id': -1}},
                {'$match': match_data},
                {
                    '$lookup': {
                        'from': 'ppera_cameras',
                        'localField': 'camera_name',
                        'foreignField': 'cameraname',
                        'as': 'camera_data'
                    }
                },
                {'$unwind': '$camera_data'},
                {
                    '$project': {
                        '_id': 0,
                        'cameraname': '$camera_name',
                        'department': '$camera_data.department'
                    }
                }
                         ]
            
            data = list(mongo.db.firesmokeviolationdata.aggregate(pipeline))
            if len(data) != 0:
                for count, i in enumerate(data):
                    if i['department'] not in dash_data:
                        dash_data.append(i['department'])
                ret = {'success': True, 'message': parse_json(dash_data)}
            else:
                ret['message'] = 'data not found' 
            # data = list(mongo.db.firesmokeviolationdata.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
            #                                         {'$project': {'data': 0}}]))
            # dash_data = []
            # if len(data) != 0:
            #     for count, i in enumerate(data):
            #         finddata = mongo.db.ppera_cameras.find_one({'cameraname': i['_id']['camera_name']})
            #         if finddata is not None :
            #             dash_data.append(finddata['department'])
            #         # dash_data.append(i['_id']['camera_name'])
            #     ret = {'success': True, 'message': parse_json(dash_data)}
            # else:
            #     ret['message'] = 'data not found'
                 
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
           
    return jsonify(ret)


@vehicle_parking.route('/create_violation_excelVPMSAPP', methods=['POST'])
def create_violation_excelVPMSAPP():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        if not os.path.exists('firesmoke_violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "firesmoke_violation_excel_sheets"))
        jsonobject = request.json
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
                            mongo_data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}},  {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
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
                            mongo_data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000}
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
                    mongo_data = list(mongo.db.firesmokeviolationdata.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000} ]))
                    if len(mongo_data) !=0:
                        print("length===========",len(mongo_data))
                        excel_create = (FIREANDSMOKEEXCELWITHOUTVIDOE(mongo_data))
                        if excel_create['success'] == True:
                            ret =excel_create #{'success': True, 'message': 'Excel sheet is created sucessfully'}
                        else:
                            ret = excel_create
                    else:
                        ret = {'success': False, 'message':'data not found.'}                 
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
    return ret


def draw_bbox_and_insert_image(worksheet, image_path, image_data, row, column):
    img = Image.open(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'fsd', image_path))
    draw = ImageDraw.Draw(img)
    if len(image_data) > 0 :
        for obj_detail in image_data:
            height = obj_detail['bbox']['H']
            width = obj_detail['bbox']['W']
            x = obj_detail['bbox']['X']
            y = obj_detail['bbox']['Y']
            start_col = x
            start_row = y
            end_col = x + width
            end_row = y + height

            draw.rectangle([start_col, start_row, end_col, end_row], outline=(255, 0, 0), width=7)
        imagename = os.path.splitext(image_path)[0]
        img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'fsd', imagename+'_1.jpg'))
        worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'fsd', imagename+'_1.jpg'), {'x_scale': 0.16, 'y_scale': 0.212})
        
        # try:
        #     os.remove(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'fsd', imagename+'_1.jpg'))
        # except Exception as error:
        #     print(f"Error removing temporary image: {error}")



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


@vehicle_parking.route('/VPMSAPPviolation_excel_download', methods=['GET'])
def VPMSAPPviolation_excel_download():
    if 1:
    # try:
        list_of_files = glob.glob(os.path.join(os.getcwd(), "firesmoke_violation_excel_sheets/*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        path, filename = os.path.split(latest_file)
        if filename:
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
        else:
            return {'success': False, 'message': 'File is not found.'}