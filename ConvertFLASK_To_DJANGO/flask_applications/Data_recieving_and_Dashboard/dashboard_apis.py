from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_hydra_config_file import * 


dashboard = Blueprint('dashboard', __name__)



def NEWLICENSECOUNT():
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =0
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICE000NSECOUNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICEN-==00SECOUNT 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICEN009897SECOUNT 3", str(error), " ----time ---- ", now_time_with_time()]))
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
        print(type(split_data[0]))
        # if CamCount < int((split_data[0])):
        license_status = int((split_data[0]))
        # else:
        #     license_status = False    
    return license_status



@dashboard.route('/licenseNewcount', methods=['GET'])
def license_count():
    Return = {'total_license':0,'added_cameras_count':0,'remaining_license':0}
    if 1:
    # try:
        ret = {'message': 'something went wrong with get license_count', 'success': False}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        sheet_camera_count = 0
        # print('sheet_data',sheet_data)
        if sheet_data is not None:
            sheet_data_count = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
             #mongo.db.panel_data.count_documents({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']})
            unique_iplist = []
            if len(sheet_data_count) !=0:
                for kl , eachElements in enumerate(sheet_data_count):
                    # if isEmpty(eachElements['data']) :
                    #     print("00098865234567888888",eachElements)
                    if eachElements['ip_address'] not in unique_iplist:
                        unique_iplist.append(eachElements['ip_address'])
                sheet_camera_count= len(unique_iplist) 
            
        CamCount = mongo.db.ppera_cameras.count_documents({})#find()#find_one()#mongo.db.ppera_cameras.find({}).count()
        # print("camera -count ",CamCount)
        # print("sheet_data count",sheet_camera_count)
        # CamCount = CamCount #+ sheet_camera_count
        Total_license = NEWLICENSECOUNT() 
        print("type -------------sheet_camera_count",sheet_camera_count)
        print("count --------------type ==",type(sheet_camera_count))
        Return = {'total_license':Total_license,'added_cameras_count':CamCount+sheet_camera_count,'remaining_license':Total_license-(CamCount+sheet_camera_count)}
        ret['message']=Return
        ret['success']=True
    # except Exception as error:
    #     ret['message'] = str(error)
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_licedsdnse_of_camera 4", str(error), " ----time ---- ", now_time_with_time()]))
    return ret

#done for object
@dashboard.route('/delete_job_sheet/<id>', methods=['GET'])
def delete_job_sheet(id=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    try: 
        if id is not None:
            find_result= mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)})
            if find_result is not None:
                result = mongo.db.job_sheet_details.delete_one({'_id': ObjectId(find_result['_id'])})
                if result.deleted_count > 0:
                    ret = {'message': 'job sheet  deleted successfully.','success': True}
                else:
                    ret['message'] ='job sheet is not deleted.'
            else:
                ret['message'] = 'job sheet is not found for this mongoid.'
        else:
            ret['message']= 'mongoid should not be none.'  
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 1", str(error), " ----time ---- ", now_time_with_time()]))   
        ret['message'] =" ".join(["something error has occered in api", str(error)])      
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")               
    except Exception as  error:
        ret = {'success': False, 'message': str(error)}
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return ret


#time_stamp_data= [item if i['irrd_in_time'] is not None else mongo_id_data.append(i) for item, i in enumerate(list_of_dict)]
############################ NOt used functions ###################
def remove_same_panel_from_db():
    try:
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
            if data is not None:
                if len(data) != 0:
                    for ios, check_empty_panel_data in enumerate(data):
                        final_data = []
                        if check_empty_panel_data['type'] =='HT' or check_empty_panel_data['type'] =='ht':
                            if isEmpty(check_empty_panel_data['data']) :
                                for jkk, is_empty_bbox in enumerate(check_empty_panel_data['data']):
                                    final_data_data = is_empty_bbox
                                    if len(is_empty_bbox['panel_data']) != 0:
                                        final_panel_data_for_updating = []
                                        for jkkee, panel_is_empty_bbox in enumerate(is_empty_bbox['panel_data']):
                                            if isEmpty(panel_is_empty_bbox):
                                                all_panel_id = []
                                                if panel_is_empty_bbox['panel_id'] != 'NA':
                                                    if panel_is_empty_bbox['panel_id'] not in all_panel_id:
                                                        all_panel_id.append(panel_is_empty_bbox['panel_id'])
                                                        if isEmpty(panel_is_empty_bbox['roi_data']):
                                                            if panel_is_empty_bbox['roi_data']['bbox'] != '':
                                                                final_panel_data_for_updating.append(panel_is_empty_bbox)
                                        if len(final_panel_data_for_updating) != 0:
                                            final_data_data['panel_data'] = final_panel_data_for_updating
                                            final_data.append(final_data_data)
                                        else:
                                            is_empty_bbox['panel_data'] = []
                                            final_data_data['panel_data'] = []
                                            final_data.append(final_data_data)
                                id = check_empty_panel_data['_id']
                                result = mongo.db.panel_data.update_one({'_id':ObjectId(id)}, {'$set':{'data': final_data}})
                                if result.matched_count > 0:
                                    pass
    except ( 
        pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        pymongo.errors.WTimeoutError,      pymongo.errors.WriteConcernError,        pymongo.errors.WriteError) as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- remove_same_panelddd_from_db 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")    
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- remove_same_panel_fddrom_db 2", str(error), " ----time ---- ", now_time_with_time()]))




def panel_detection_function_for_image(detector,panel_image_file):
    handle_uploaded_file(os.path.join(str(os.getcwd()),'cropped_images_for_panel'))
    result = detector.detect(panel_image_file)
    if type(result) == list:
        if len(result) != 0:
            result = COORIDINATES_FROM_DETECTED_PANEL(result)
    return parse_json(result)


def arrange_x_in_ascending_order(x, y):
    for i in range(0, len(x)):
        if x[i] < 0:
            x[i] = 0
    for i in range(0, len(y)):
        if y[i] < 0:
            y[i] = 0
    return x, y


def extend_roi_points(width=960, height=544, data=None, buffer=40):
    try:
        x_point = []
        y_point = []
        split_data = data.split(';')
        for point in enumerate(split_data):
            if (point[0] + 1) % 2 == 0:
                if point[1] != '':
                    y_point.append(int(point[1]))
            elif point[1] != '':
                x_point.append(int(point[1]))
        if len(x_point) == len(y_point):
            x_point, y_point = arrange_x_in_ascending_order(x_point, y_point)
            y_point_min = min(y_point)
            y_point_max = max(y_point)
            x_point_min = min(x_point)
            x_point_max = max(x_point)
            roi_height = y_point_max - y_point_min
            roi_width = x_point_max - x_point_min
            extend_height = int(roi_height / 3)
            for i in range(0, len(x_point)):
                if y_point[i] >= y_point_max - buffer and y_point[i] <= y_point_max:
                    y_point[i] = y_point[i] + extend_height
                    if y_point[i] > height:
                        y_point[i] = height
            return_data = None
            for i in range(0, len(x_point)):
                if return_data == None:
                    return_data = str(x_point[i]) + ';'
                    return_data += str(y_point[i]) + ';'
                else:
                    return_data += str(x_point[i]) + ';'
                    return_data += str(y_point[i]) + ';'
            return return_data
        else:
            return data
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- extend_roi_points 1", str(error), " ----time ---- ", now_time_with_time()]))
        return data


def frence_roi_points(data=None):
    try:
        x_point = []
        y_point = []
        split_data = data.split(';')
        while '' in split_data:
            split_data.remove('')
        for point in enumerate(split_data):
            if (point[0] + 1) % 2 == 0:
                y_point.append(int(point[1]))
            else:
                x_point.append(int(point[1]))
        if len(x_point) == len(y_point):
            w = x_point[1] - x_point[0]
            h = y_point[1] - y_point[0]
            return_data = None
            if return_data == None:
                return_data = str(x_point[0]) + ';'
                return_data += str(y_point[0]) + ';'
                return_data += str(w) + ';'
                return_data += str(h) + ';'
            return return_data
        else:
            return data
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- frence_ro33i_points 1", str(error), " ----time ---- ", now_time_with_time()]))
        return data

def FUNTOMERGESAMEIPANDRTSPPANELDATA(ALL_PANELDATA,REPEATEDIPDATA):
    for indexcount , Element in enumerate(ALL_PANELDATA):
        if REPEATEDIPDATA['ip_address'] ==Element['ip_address']:
            get_panel_key_id12 = [ioo['panel_id'] for __p, ioo in enumerate(Element['panel_data']) if ioo['panel_id'] is not None]
            panelnumberLISTDATA = [ioo['panel_id'] for __p, ioo in enumerate(REPEATEDIPDATA['panel_data']) if ioo['panel_id']is not None]
            if len(REPEATEDIPDATA['panel_data'])==1:
                if REPEATEDIPDATA['panel_data'][0]['panel_id'] !=Element['panel_data'][0]['panel_id']:
                    Element['panel_data'].append(REPEATEDIPDATA['panel_data'][0])
            elif len(REPEATEDIPDATA['panel_data'])> 1:
                for ll, multipanel in enumerate(REPEATEDIPDATA['panel_data']):                    
                    Element['panel_data'].append(multipanel)
    return ALL_PANELDATA


def REPEATEDPANELNOFORDIFFERENTJOB(allPANELDATA):
    if len(allPANELDATA)!=0:
        for indexno , eachsource in enumerate(allPANELDATA):
            get_panel_key_id12 =[]
            check_panel_id =[]
            if len(eachsource['panel_data']) !=0:
                for i, ioo in enumerate(eachsource['panel_data']):
                    if ioo['panel_id']  not in check_panel_id:
                        check_panel_id.append(ioo['panel_id'])
                        get_panel_key_id12.append(ioo)
                eachsource['panel_data'] =get_panel_key_id12
    return allPANELDATA

def CHECKMULIPINESI(main_list):
    final_list = []
    check_the_ipaddress=[]
    make_final = []
    if len(main_list) != 0:
        for ___12, panel_val in enumerate(main_list):
            if len(panel_val['panel_data']) != 0:
                require_panel_data = {'ip_address': panel_val['ip_adrs' ], 'camera_name': panel_val['camera_name'],'rtsp_url': panel_val['rtsp_url'],
                                        'panel_data':panel_val['panel_data'], 'ai_solution': panel_val['ai_solution'], 'roi_ra': panel_val['roi_ra'],'hooter_ip':panel_val['hooter_ip']}
                if require_panel_data not in final_list:
                    if require_panel_data['ip_address'] in check_the_ipaddress :
                        make_final.append(require_panel_data['ip_address'])
                        final_list = FUNTOMERGESAMEIPANDRTSPPANELDATA(final_list,require_panel_data)
                    elif require_panel_data['ip_address'] not in check_the_ipaddress:
                        final_list.append(require_panel_data)
                        check_the_ipaddress.append(require_panel_data['ip_address'] )
    if len(final_list) != 0 :
        final_list = REPEATEDPANELNOFORDIFFERENTJOB(final_list)
    return final_list

def check_panel_data_is_empty_(all_data_to_check_panel):
    return_data_ = []
    panel_empty_status = False
    if isEmpty(all_data_to_check_panel) :
        if len(all_data_to_check_panel['panel_data']) != 0:
            panel_empty_status = True
            return_data_.append(all_data_to_check_panel)
    else:
        return_data_ = return_data_
    return return_data_


def relocate_data_points(data):
    data_xy = []
    co_ord = data
    co_ord_split = co_ord.split(';')
    min_x = None
    min_y = None
    try:
        for i in range(0, len(co_ord_split) - 1):
            if i % 2 == 0:
                data_xy.append((int(co_ord_split[i]), int(co_ord_split[i + 1])))
        for p in data_xy:
            if min_x == None:
                min_x = p[0]
            elif p[0] <= min_x:
                min_x = p[0]
        temp = []
        for p in data_xy:
            if p[0] <= min_x + 20 and p[0] >= min_x - 20:
                temp.append(p)
        if len(temp) > 1:
            for p in temp:
                if min_y == None:
                    min_y = p[1]
                    min_x = p[0]
                elif p[1] <= min_y:
                    min_y = p[1]
                    min_x = p[0]
        else:
            min_y = temp[0][1]
        while not (data_xy[0][0] == min_x and data_xy[0][1] == min_y):
            data1 = data_xy[0]
            for i in range(0, len(data_xy) - 1):
                data_xy[i] = data_xy[i + 1]
            data_xy[len(data_xy) - 1] = data1
        data_send = ''
        for x in data_xy:
            data_send = data_send + str(x[0]) + ';'
            data_send = data_send + str(x[1]) + ';'
        return data_send
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- reloc33ate_data_points 1", str(error), " ----time ---- ", now_time_with_time()]))
        return data


def update_cam_id(ESICAMUPDATE):
    data_values = ESICAMUPDATE['data']
    require_data_list = []
    for R__R__R, i in enumerate(data_values):
        require_data_list.append(i)
    require_data = {'roi_cam_ids': require_data_list[0], 'ppe_cam_ids': require_data_list[1], 'rtsp_cam_name': require_data_list[2]}
    camera_ids = []
    for RRR, total_data in enumerate(require_data['rtsp_cam_name']):
        total_data_camera_name = total_data['camera_name']
        total_rtsp_url = total_data['rtsp_url']
        total_camera_id = total_data['camera_id']
        camera_ids.append(total_camera_id)
        result_data = mongo.db.panel_data.find_one({'data.rtsp_url': total_rtsp_url, 'data.camera_name': total_data_camera_name})
        if result_data is not None:
            result_data['_id'] = str(result_data['_id'])
            id = result_data['_id']
            data_field = result_data['data']
            if result_data['data']['rtsp_url'] == total_rtsp_url:
                result_data['data']['camera_id'] = total_camera_id
            result = mongo.db.panel_data.update_one({'_id': ObjectId(id),'data.rtsp_url': total_rtsp_url}, {'$set':{'data':result_data['data']}})
            if result.matched_count > 0:
                pass    
    return '200'




def NewCameraid_Update(ESICAMUPDATE):
    for RRR, total_data in enumerate(ESICAMUPDATE):
        # print("update details cameraid---", total_data)
        Cameraaddress = total_data['ip_address']
        result_data = list(mongo.db.panel_data.find({'data.ip_address': Cameraaddress}))
        if len(result_data) !=0:
            for Indexid , EachcameraUpdata in enumerate(result_data):
                id = EachcameraUpdata['_id']
                result = mongo.db.panel_data.update_one({'_id': ObjectId(id)}, {'$set':{'data.camera_id':total_data['camera_id']}})
                if result.matched_count > 0:
                    pass    
    return '200'
#gpu_configurations



def ESINEWCAMERAIDupdatenew():
    ret = {'message':'something went wrong with create config .','success': False}
    remove_empty_space_panels_from_db()
    getdata_response = createNEWESIconfig()
    if len(getdata_response) != 0:
        response = getdata_response['data']
        function__response = MULTI1CONFIG(response)
        if len(function__response) !=0 :
        # require_cam_ids_data = {'data': list(function__response)}
            return_data_update_camera = NewCameraid_Update(function__response)
            if return_data_update_camera == '200':
                ret = {'message': 'config files are created successfully.','success': True}
            else:
                ret = {'message': 'camera id not updated .', 'success': False}
        else:
            ret['message']='properly data has not give for starting safty eye application.'
    else:
        ret['message'] = 'there is no data found for create config file '
    return ret

def CheckPANELEMPTYBBOXANDRWBBOX(panel_data):
    newpaneldata = []
    for index, eachpanel in enumerate(panel_data):
        # print("---------------------------------------------eachpanel  1-------",eachpanel)
        if eachpanel['roi_data']['bbox'] != '' :
            # and len(eachpanel['roi_data']['RW']) != 0  and eachpanel['roi_data']['panel_no'] is not None:
            if type(eachpanel['roi_data']['RW']) == str :
                if eachpanel['panel_id'] is not None:
                    # print("bbox --not empty==-",eachpanel)
                    newpaneldata.append(eachpanel)
            elif type(eachpanel['roi_data']['RW']) == list:
                if eachpanel['panel_id'] is not None and eachpanel['roi_data']['bbox'] !='':
                    if eachpanel['roi_data']['unallocated_job_status']:
                        print("ANOTHER CONDITION ----------",)
                        newpaneldata.append(eachpanel)
        elif  eachpanel['roi_data']['bbox'] == '' :
            print("-------------eachpanel-2---",eachpanel)

    return newpaneldata
            

def createNEWESIconfig():
    response = []
    main_list = []
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if sheet_data is not None:
        fetch_panel_data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],'type':"HT"}))
        if len(fetch_panel_data) != 0:
            for ol__io, i in enumerate(fetch_panel_data):
                return_data = check_panel_data_is_empty_(i['data'])
                if len(return_data) != 0:
                    # print("-----------------------------i-----------",i)
                    video_names = None
                    if 'video_names' in i:
                        video_names = i['video_names']
                    ip_address = i['data']['ip_address']
                    cam_name = i['data']['camera_name']
                    rtsp = i['data']['rtsp_url']
                    panel_data = i['data']['panel_data']
                    if len(panel_data) != 0:
                        # panel_data = CheckPANELEMPTYBBOXANDRWBBOX(panel_data)    
                        panel_data = CheckPANELEMPTYBBOXANDRWBBOX(panel_data)
                        # print("newpaneldata===",panel_data)              
                        if len(panel_data) != 0:
                            if rtsp is not None:
                                if 'hooter_ip' in i:
                                    if i['hooter_ip'] is not None and i['hooter_ip'] !='':
                                        require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'video_names':video_names,'panel_data':panel_data, 'ai_solution': ['PPE'],'roi_ra': [],'hooter_ip':i['hooter_ip']}
                                    else:
                                        require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'video_names':video_names,'panel_data':panel_data, 'ai_solution': ['PPE'],'roi_ra': [],'hooter_ip':None}
                                else:
                                    require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'video_names':video_names,'panel_data':panel_data, 'ai_solution': ['PPE'],'roi_ra': [],'hooter_ip':None}
                                main_list.append(require_panel_data)
    response = CHECKMULIPINESI(main_list)
    if len(response) != 0:
        response = {'data': response}
    return response

def split_list(input_list, sublist_length):
    return [input_list[i:i+sublist_length] for i in range(0, len(input_list), sublist_length)]

def drop_ppe_type1_metadata_table():
    try:
        conn = psycopg2.connect(user ="docketrun",  password = "docketrun",  host = "localhost", port = "5432",   database = "docketrundb",  sslmode="disable")
    except:
        conn = 0
        
    if conn:
        cursor = conn.cursor()
        print ("[INFO] DB connected successfully drop ppe metadata")
        try:
            cursor.execute('DROP TABLE ppe_type_1_metadata_tsk;')
        except psycopg2.errors.UndefinedTable as e:
            print("ERR drop ppe metadata UndefinedTable")
        except psycopg2.errors.InFailedSqlTransaction as e:
            print("ERR drop ppe metadata InFailedSqlTransaction")
        cursor.close()
        conn.close()
        
def copy_file(src, dst):
    try:
        with open(src, 'rb') as source_file:
            with open(dst, 'wb') as destination_file:
                destination_file.write(source_file.read())
        print(f"File copied from {src} to {dst}")
    except IOError as e:
        print(f"Unable to copy file. Error: {e}")
#gpu_configurations
def MULTI1CONFIG(response):
    CAMIDUPDATEDETAILS= []
    print("CHEKC -----------------------------------CHECK ------------------ paneldata -----------",)
    
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
    print("Genral_configurations===",Genral_configurations)
    batch_pushouttime = 40000
    drop_frame_interval=1
    if ('drop_frame_interval' in Genral_configurations and Genral_configurations['drop_frame_interval'] is not None) and ('camera_fps' in Genral_configurations and  Genral_configurations['camera_fps'] is not None) :
        camera_fps = Genral_configurations['camera_fps']
        drop_frame_interval = Genral_configurations['drop_frame_interval']
        Newpushouttime = math.ceil(int(camera_fps)/int(drop_frame_interval))
        batch_pushouttime= math.ceil(1000000/Newpushouttime)
    rtsp_reconnect_interval = 3

    if ('rtsp_reconnect_interval' in Genral_configurations and Genral_configurations['rtsp_reconnect_interval'] is not None):
         rtsp_reconnect_interval = Genral_configurations['rtsp_reconnect_interval'] 
    

    numberofsources_= 4
    if ('grid_size' in Genral_configurations and Genral_configurations['grid_size'] is not None):
         numberofsources_ = int(Genral_configurations['grid_size'])



    # for new,idatacheck in enumerate(response):
    #     print("oookkk-------------",idatacheck)
    Total_source_count = len(response)
    GPU_data = mongo.db.gpu_configurations.find_one({})


    
    require_data = []
    roi_enable_cam_ids = []
    
    if GPU_data is not None:
        GPUCOUNT = 1
        Totalcamera_pereachGpu = 2
        print("-------------------Total_source_count--------------------------------",Total_source_count)
        print("-------------------GPU_data--------------------------------",GPU_data)
        # drop_ppe_type1_metadata_table()
        os.system( "rm -r "+ os.path.join(get_current_dir_and_goto_parent_dir(),'docketrun_eis_monitor/configs') + "/*.txt" )    
        
        camera_id =1 
        new_response = split_list(response,numberofsources_) 
        GPUSINDEX = 0    
        NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus'])# (Total_source_count /    GPU_data['system_gpus'])   
        print("=====NEwcount====",NEwcount)

        if 'system_gpus' in GPU_data:
            GPUCOUNT = GPU_data['system_gpus']
        if len(GPU_data['gpu_details']) !=0 :
            for jindex, iooojjn in enumerate(GPU_data['gpu_details']):
                Totalcamera_pereachGpu = iooojjn['camera_limit']
                break
        for config_index, writingresponse in enumerate(new_response):
                
            # if GPU_data['system_gpus']==1 :
            #     GPUSINDEX = GPUSINDEX
            # elif config_index ==0  :
            #     GPUSINDEX = config_index
            # elif camera_id >= NEwcount:
            #     GPUSINDEX= GPUSINDEX+1 
            # else:
            #     GPUSINDEX= GPUSINDEX
            if Totalcamera_pereachGpu >= camera_id:
                GPUSINDEX= 0
            elif (Totalcamera_pereachGpu +Totalcamera_pereachGpu) >= camera_id:
                if GPUCOUNT > 1:
                    GPUSINDEX= 1
            elif (Totalcamera_pereachGpu +Totalcamera_pereachGpu+Totalcamera_pereachGpu) >= camera_id:
                if GPUCOUNT > 2:
                    GPUSINDEX= 2
            elif (Totalcamera_pereachGpu +Totalcamera_pereachGpu+Totalcamera_pereachGpu+Totalcamera_pereachGpu) >= camera_id:
                if GPUCOUNT > 3:
                    GPUSINDEX= 3
            elif (Totalcamera_pereachGpu +Totalcamera_pereachGpu+Totalcamera_pereachGpu+Totalcamera_pereachGpu+Totalcamera_pereachGpu) >= camera_id:
                if GPUCOUNT > 4:
                    GPUSINDEX= 4
            else:
                GPUSINDEX= 0
            # for GPUSINDEX, Gpudetails in enumerate(GPU_data['gpu_details']):    
            print("---------------GPUSINDEX---------------GPUSINDEX------------",GPUSINDEX)
            sample_config_file = os.path.join(os.getcwd(),  'smaple_files', 'esi_sample_config.txt')
            sample_config_esi_engine = os.path.join(os.getcwd(), 'smaple_files', 'esi_engine_file_create.txt')
            create_engine_file_config_file = os.path.join(get_current_dir_and_goto_parent_dir(), 'models/config_infer_primary_tsk_v_0_2.txt')
            deepstream_config_path =  os.path.join(get_current_dir_and_goto_parent_dir(),'docketrun_eis_monitor/configs')
            handle_uploaded_file(deepstream_config_path)
            config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
            config_analytics_file = os.path.join(deepstream_config_path,'config_analytics_{0}.txt'.format(config_index+1))
            config_fences_file = os.path.join(deepstream_config_path,'config_fences_{0}.txt'.format(config_index+1))
            lines = ['[property]', 'enable=1', 'config-width=960','config-height=544', 'osd-mode=2', 'display-font-size=12', '']
            test_data = []
            index = 0
            ppe_enable_cam_ids = []
            
            for Cherry, x in enumerate(writingresponse):
                x['camera_id'] = int(index) + 1
                require_data.append(x)
                analytics_config = x['panel_data']
                test_data.append(analytics_config)
                roi_exist_or_not = '[roi-filtering-stream-{0}]'.format(index)
                if len(x['roi_ra']) != 0:
                    roi_enable_cam_ids.append(index + 1)
                elif len(x['panel_data']) != 0:
                    ppe_enable_cam_ids.append(index + 1)
                if len(x['roi_ra']) != 0 or len(x['panel_data']) != 0:
                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                    lines.append('enable=1')
                    for power_star, roi_value in enumerate(x['roi_ra']):
                        panel_name = roi_value['roi_name']
                        try:
                            roi_value['bb_box'] = extend_roi_points(data=roi_value['bb_box'])
                            roi_value['bb_box'] = relocate_data_points(roi_value['bb_box'])
                            roi_bbox = roi_value['bb_box']
                        except Exception as  error:
                            roi_bbox = roi_value['bb_box']
                            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- write_cddonnfig 1", str(error), " ----time ---- ", now_time_with_time()]))
                        bbox_values = []
                        lines.append('roi-RA-{0} = {1}'.format(panel_name, roi_bbox))
                    for ___p, vlaue in enumerate(x['panel_data']):
                        somename_data = vlaue['roi_data']
                        roi_bbox = somename_data['bbox']
                        if somename_data['unallocated_job_status']:
                            somename_data['bbox'] = extend_roi_points(data=somename_data['bbox'])
                            somename_data['bbox'] = relocate_data_points(somename_data['bbox'])
                            roi_bbox = somename_data['bbox']
                            if str(vlaue['panel_id']) == 'NA':
                                panel_num = str(vlaue['panel_id']) + str(___p)
                            else:
                                panel_num = str(vlaue['panel_id'])
                            lines.append('roi-UNPLANNED-{0} = {1}'.format(panel_num, roi_bbox))

                        else:

                            somename_data['bbox'] = extend_roi_points(data=somename_data['bbox'])
                            somename_data['bbox'] = relocate_data_points(somename_data['bbox'])
                            roi_bbox = somename_data['bbox']
                            if str(vlaue['panel_id']) == 'NA':
                                panel_num = str(vlaue['panel_id']) + str(___p)
                            else:
                                panel_num = str(vlaue['panel_id'])
                            lines.append('roi-PNL-{0} = {1}'.format(panel_num, roi_bbox))
                    lines.append('inverse-roi=0')
                    lines.append('class-id=0;1;2;\n')
                index += 1
            with open(config_analytics_file, 'w') as f:
                for item in lines:
                    f.write('%s\n' % item)
            lines = []
            with open(sample_config_file) as file:
                camera_id_start = camera_id
                Cameraids_for_ppe=[]
                for young_TIGER, line in enumerate(file):
                    if line.strip() == '[application]':
                        lines.append('[application]')
                        lines.append('enable-perf-measurement=1')
                        lines.append('perf-measurement-interval-sec=5')
                    elif line.strip() == '[tiled-display]':
                        columns = int(math.sqrt(len(writingresponse)))
                        rows = int(math.ceil(len(writingresponse) / columns))
                        lines.append('[tiled-display]')
                        lines.append('enable=1')
                        if rows == 1 and columns == 1:
                            lines.append('rows=1')
                            lines.append('columns=2')
                        else:
                            if rows >2 :
                                lines.append('rows={0}'.format(str(2)))
                                lines.append('columns={0}'.format(str(2)))
                            else:
                                lines.append('rows={0}'.format(str(2)))
                                lines.append('columns={0}'.format(str(2)))

                        lines.append('width=960')
                        lines.append('height=544')
                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                        lines.append('nvbuf-memory-type=0')
                    elif line.strip() == '[sources]':

                        for n, x in enumerate(writingresponse):
                            cam_id = '{0}'.format(int(n) + 1)
                            roi_enable_cam_ids_exist = roi_enable_cam_ids.count(int(cam_id))
                            ppe_enable_cam_ids_exist = ppe_enable_cam_ids.count(int(cam_id))
                            if (roi_enable_cam_ids_exist > 0 or ppe_enable_cam_ids_exist > 0):
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace('rtsp', 'rtspt')
                                if 'video_names' in x :
                                    if x['video_names'] is not None:
                                        print("=========================================================111====x =================",x['video_names'])
                                        if 'file:' in x['video_names'] :
                                            uri = x['video_names']
                                            lines.append('[source{0}]'.format(n))
                                            lines.append('enable=1')
                                            lines.append('type=3')
                                            lines.append('uri = {0}'.format(uri))
                                            lines.append('num-sources=1')
                                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                                            lines.append('nvbuf-memory-type=0')
                                            lines.append('latency=500')
                                            lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                            lines.append('camera-id={0}'.format(camera_id))
                                            Camdetails = {'ip_address':x['ip_address'],'camera_name':x['camera_name'],'camera_id':camera_id,'url':uri}
                                            CAMIDUPDATEDETAILS.append(Camdetails)
                                            Cameraids_for_ppe.append(camera_id)
                                            lines.append('camera-name = {0}'.format(x['camera_name']))
                                            if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                                lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                            else:
                                                lines.append('drop-frame-interval = 1\n')
                                            camera_id +=1
                                        elif 'rtsp' in x['video_names'] :
                                            uri = x['video_names']
                                            lines.append('[source{0}]'.format(n))
                                            lines.append('enable=1')
                                            lines.append('type=4')
                                            lines.append('uri = {0}'.format(uri))
                                            lines.append('num-sources=1')
                                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                                            lines.append('nvbuf-memory-type=0')
                                            lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                            lines.append('latency=500')
                                            lines.append('camera-id={0}'.format(camera_id))
                                            lines.append('camera-name = {0}'.format(x['camera_name']))
                                            Camdetails = {'ip_address':x['ip_address'],'camera_name':x['camera_name'],'camera_id':camera_id,'url':uri}
                                            CAMIDUPDATEDETAILS.append(Camdetails)
                                            Cameraids_for_ppe.append(camera_id)
                                            if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                                lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                            else:
                                                lines.append('drop-frame-interval = 0\n')
                                            camera_id +=1
                                        elif '.mp4' in x['video_names'] or '.avi' in  x['video_names']:
                                            uri = x['video_names']
                                            lines.append('[source{0}]'.format(n))
                                            lines.append('enable=1')
                                            lines.append('type=3')
                                            lines.append('uri = file://../../test_videos/{0}'.format(uri))
                                            # lines.append('uri = {0}'.format(uri))
                                            lines.append('num-sources=1')
                                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                                            lines.append('nvbuf-memory-type=0')
                                            lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                            lines.append('latency=500')
                                            lines.append('camera-id={0}'.format(int(n) + 1))
                                            Camdetails = {'ip_address':x['ip_address'],'camera_name':x['camera_name'],'camera_id':int(n) + 1,'url':uri}
                                            CAMIDUPDATEDETAILS.append(Camdetails)
                                            Cameraids_for_ppe.append(camera_id)
                                            lines.append('camera-name = {0}'.format(x['camera_name']))
                                            if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                                lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                            else:
                                                lines.append('drop-frame-interval = 1\n')
                                        else:
                                            uri = x['video_names']
                                            lines.append('[source{0}]'.format(n))
                                            lines.append('enable=1')
                                            lines.append('type=3')
                                            lines.append('uri = file://../../test_videos/{0}'.format(uri))
                                            lines.append('num-sources=1')
                                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                                            lines.append('nvbuf-memory-type=0')
                                            lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                            lines.append('latency=500')
                                            lines.append('camera-id={0}'.format(camera_id))
                                            lines.append('camera-name = {0}'.format(x['camera_name']))
                                            Camdetails = {'ip_address':x['ip_address'],'camera_name':x['camera_name'],'camera_id':camera_id,'url':uri}
                                            CAMIDUPDATEDETAILS.append(Camdetails)
                                            Cameraids_for_ppe.append(camera_id)
                                            if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                                lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                            else:
                                                lines.append('drop-frame-interval = 1\n')
                                            camera_id +=1
                                elif x['rtsp_url'] is not None:
                                    if '.mp4' in x['rtsp_url']:
                                        uri = x['rtsp_url']
                                        lines.append('[source{0}]'.format(n))
                                        lines.append('enable=1')
                                        lines.append('type=3')
                                        lines.append('uri = {0}'.format(uri))
                                        lines.append('num-sources=1')
                                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                                        lines.append('nvbuf-memory-type=0')
                                        lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                        lines.append('latency=500')
                                        lines.append('camera-id={0}'.format(int(n) + 1))
                                        lines.append('camera-name = {0}'.format(x['camera_name']))
                                        Camdetails = {'ip_address':x['ip_address'],'camera_name':x['camera_name'],'camera_id':camera_id,'url':uri}
                                        CAMIDUPDATEDETAILS.append(Camdetails)
                                        Cameraids_for_ppe.append(camera_id)
                                        if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                            lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                        else:
                                            lines.append('drop-frame-interval = 1\n')
                                        camera_id +=1
                                    else:
                                        uri = x['rtsp_url']
                                        lines.append('[source{0}]'.format(n))
                                        lines.append('enable=1')
                                        lines.append('type=4')
                                        lines.append('uri = {0}'.format(uri))
                                        lines.append('num-sources=1')
                                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                                        lines.append('nvbuf-memory-type=0')
                                        lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                        lines.append('latency=500')
                                        lines.append('camera-id={0}'.format(camera_id))
                                        lines.append('camera-name = {0}'.format(x['camera_name']))
                                        Camdetails = {'ip_address':x['ip_address'],'camera_name':x['camera_name'],'camera_id':camera_id,'url':uri}
                                        CAMIDUPDATEDETAILS.append(Camdetails)
                                        Cameraids_for_ppe.append(camera_id)
                                        if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                            lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                        else:
                                            lines.append('drop-frame-interval = 1\n')
                                        camera_id +=1
                    elif line.strip() == '[sink0]':
                        lines.append('[sink0]')
                        lines.append('enable=1')
                        lines.append('type=2')
                        lines.append('sync=0')
                        lines.append('source-id=0')
                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                        lines.append('nvbuf-memory-type=0')
                    elif line.strip() == '[osd]':
                        lines.append('[osd]')
                        lines.append('enable=1')
                        lines.append('gpu-id={0}'.format(GPUSINDEX))
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
                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                        lines.append('live-source=1')
                        lines.append('batch-size={0}'.format(len(writingresponse)))
                        if batch_pushouttime == 40000:
                            lines.append('batched-push-timeout=40000')
                        else:
                            lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            
                        lines.append('width=960')
                        lines.append('height=544')
                        lines.append('enable-padding=0')
                        lines.append('nvbuf-memory-type=0')
                    elif line.strip() == '[primary-gie]':
                        lines.append('[primary-gie]')
                        lines.append('enable=1')
                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                        lines.append('batch-size={0}'.format(len(writingresponse)))
                        lines.append('bbox-border-color0=0;1;0;0.7')
                        lines.append('bbox-border-color1=0;1;1;0.7')
                        lines.append('bbox-border-color2=0;1;0;0.7')
                        lines.append('bbox-border-color3=0;1;0;0.7')
                        lines.append('nvbuf-memory-type=0')
                        lines.append('interval=0')
                        lines.append('gie-unique-id=1')
                        lines.append('config-file = ../../models/config_infer_primary_tsk_v_0_2.txt')
                    elif line.strip() =='[secondary-gie0]':
                        lines.append('[secondary-gie0]')
                        lines.append('enable = 0')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                        lines.append('gie-unique-id = 5')
                        lines.append('operate-on-gie-id = 1')
                        lines.append('operate-on-class-ids = 0;')
                        lines.append('batch-size = 1')
                        lines.append('config-file = ../../models/classification_vest.txt')
                    elif line.strip() =='[secondary-gie1]':
                        lines.append('[secondary-gie1]')
                        lines.append('enable = 0')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                        lines.append('gie-unique-id = 4')
                        lines.append('operate-on-gie-id = 1')
                        lines.append('operate-on-class-ids = 0;')
                        lines.append('batch-size = 1')
                        lines.append('config-file = ../../models/classification_helmet.txt')
                    elif line.strip() =='[secondary-gie2]':
                        lines.append('[secondary-gie2]')
                        lines.append('enable = 1')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                        lines.append('gie-unique-id = 6')
                        lines.append('operate-on-gie-id = 1')
                        lines.append('operate-on-class-ids = 0;')
                        lines.append('batch-size = 1')
                        lines.append('bbox-border-color0 = 0;0;0;0.7')
                        lines.append('bbox-border-color1 = 1;0;0;0.7')
                        lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                    elif line.strip() =='[secondary-gie3]':
                        lines.append('[secondary-gie3]')
                        lines.append('enable = 1')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                        lines.append('gie-unique-id = 7')
                        lines.append('operate-on-gie-id = 1')
                        lines.append('operate-on-class-ids = 0;')
                        lines.append('batch-size = 1')
                        lines.append('bbox-border-color0 = 1;0;1;0.7')
                        lines.append('bbox-border-color1 = 1;0;0;0.7')
                        lines.append('config-file = ../../models/config_infer_secandary_arc_jacket_v5.txt')

                    elif line.strip() =='[secondary-gie4]':
                        lines.append('[secondary-gie4]')
                        lines.append('enable = 1')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                        lines.append('gie-unique-id = 8')
                        lines.append('operate-on-gie-id = 1')
                        lines.append('operate-on-class-ids = 1;')
                        lines.append('batch-size = 1')
                        lines.append('bbox-border-color0 = 1;0;1;0.7')
                        lines.append('bbox-border-color1 = 1;0;0;0.7')
                        lines.append('config-file = ../../models/config_infer_secandary_irrd_v2.txt')
                    elif line.strip() == '[tracker]':
                        lines.append('[tracker]')
                        lines.append('enable=1')
                        lines.append('tracker-width=960')
                        lines.append('tracker-height=544')
                        lines.append('ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                        lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.3/lib/libnvds_nvmultiobjecttracker.so')
                        lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.0/lib/libnvds_nvmultiobjecttracker.so')
                        lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                        lines.append('#ll-config-file=./tracker_config.yml')
                        lines.append('ll-config-file=/opt/nvidia/deepstream/deepstream-6.4/samples/configs/deepstream-app/config_tracker_NvDCF_perf.yml')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                        lines.append('display-tracking-id=1')
                        lines.append('#enable-batch-process=0')

                    elif line.strip() == '[nvds-analytics]':
                        lines.append('[nvds-analytics]')
                        lines.append('enable = 1')
                        lines.append('config-file = ./config_analytics_{0}.txt'.format(config_index+1))

                    elif line.strip() == '[application-config]':
                        lines.append('[application-config]')
                        lines.append('image-save-path = images/frame')
                        lines.append('app-title = SafetyEye {0} to {1}'.format(camera_id_start, camera_id-1 ))
                    elif line.strip() == '[tests]':
                        lines.append('[tests]')
                    elif line.strip() == '[docketrun-device]':
                        lines.append('[docketrun-device]')
                        lines.append('gui-title = DOCKETRUN APP {0} to {1}'.format(camera_id_start, camera_id-1 ))
                    elif line.strip() == '[docketrun-image]':
                        lines.append('[docketrun-image]')
                    elif line.strip() == '[restricted-access]':
                        lines.append('[restricted-access]')
                    elif line.strip() == '[ppe-type-1]':
                        lines.append('[ppe-type-1]')
                        empty_ppe_ls = []
                        # for OPI_, n in enumerate(ppe_enable_cam_ids):
                        for OPI_, n in enumerate(Cameraids_for_ppe):
                            text = str(n) + ';'
                            empty_ppe_ls.append(text)
                        string2 = ''
                        if len(empty_ppe_ls) == 0:
                            string2 = '-1;'
                            lines.append('camera-ids = {0}'.format(string2))
                        if len(empty_ppe_ls) != 0:
                            string2 = ''
                            lines.append('camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                    elif line.strip() == '[TSK_RIRO]':
                        lines.append('[TSK_RIRO]')
                        lines.append('enable = 1')
                        lines.append('config-file = ./config_fences_{0}.txt'.format(config_index+1))
                        if 'frame_analytics_time' in Genral_configurations and Genral_configurations['frame_analytics_time'] is not None:
                            lines.append('stop-riro-frame-buffer-time = {0}'.format(Genral_configurations['frame_analytics_time'] ))
                        else:
                            lines.append('stop-riro-frame-buffer-time = 300')

                        if 'panel_analytics_time' in Genral_configurations and Genral_configurations['panel_analytics_time'] is not None:
                            lines.append('stop-riro-pnl-buffer-time = {0}'.format(Genral_configurations['panel_analytics_time'] ))
                        else:
                            lines.append('stop-riro-pnl-buffer-time = 60')
                        lines.append('rw-change-percentage = 0.3')
                        lines.append('irrd-light-process-interval = 4')
                        lines.append('rw-process-on-gpu = 0')
                        lines.append('gpu-id = {0}'.format(GPUSINDEX))
                    else:
                        lines.append(line.strip())
            with open(config_file, 'w') as f:
                for O_O_O, item in enumerate(lines):
                    f.write('%s\n' % item)
            esi_lines = []
            with open(sample_config_esi_engine) as file:
                for write_config, line in enumerate(file):
                    if line.strip():
                        if 'etlt_b4' in line.strip():
                            line = line.replace('etlt_b4', 'etlt_b' + str(len(writingresponse)))
                        esi_lines.append(line.strip())
            with open(create_engine_file_config_file, 'w') as f:
                for item in esi_lines:
                    f.write('%s\n' % item)
            test_data = []
            index = 0
            lines = []
            flag_count = None
            fence_count_ = 0
            for ___, x in enumerate(writingresponse):
                if ___ + 1:
                    flag_count = True
                fence_name = 'fence{0}'.format(___)
                require_roi_keys = ['RW', 'TG', 'LK0', 'LK1']
                require_roi_keys1 = ['RW', 'TG', 'LK0', 'LK1']
                count = 0
                for ______P, panel_data_ in enumerate(x['panel_data']):
                    row_data_keys = [str(i) for i in panel_data_['roi_data'].keys()]
                    key_status = set(require_roi_keys) & set(row_data_keys)
                    if key_status:
                        if fence_name not in lines:
                            somename_data = panel_data_['roi_data']
                            panel_num = str(panel_data_['panel_id'])
                    count = 0
                    for key, value in somename_data.items():
                        if key in require_roi_keys1:
                            if value is not None:
                                print("---value--",value)
                                if type(value) != list and value!='' :
                                    if flag_count:
                                        lines.append('\n[fence{0}]'.format(___))
                                        lines.append('enable = 1')
                                        if 'hooter_ip' in x :
                                            if x['hooter_ip'] is not None:
                                                hooteripstring = 'hooter-relay-details =[{'+'"enable":1,"ip":'
                                                hooteripstring= hooteripstring + '"{0}"'.format(x['hooter_ip'])
                                                hooteripstring = hooteripstring + ',"type":1,"shutdown_time":60,"buffer_stop_time":2}]'
                                                # hooteripstring = 'hooter-relay-details =[{'+'"cameraid":1,"ip":'+'{0},"type":1,"shutdown_time":60,"buffer_stop_time":2}]\n'.format(response[0]['hooter_ip'])
                                                print('----------hooteripstring--------',hooteripstring)
                                                lines.append(hooteripstring)
                                                # lines.append('hooter-relay-details = [{"enable":1,"ip":"192.168.1.74","type":1,"shutdown_time":60,"buffer_stop_time":2}]')
                                            else:
                                                lines.append('hooter-relay-details = Null')
                                        else:
                                            lines.append('hooter-relay-details = Null')

                                        flag_count = False
                                    value = frence_roi_points(data=value)
                                    if str(panel_num) == 'NA':
                                        lines.append('{0}-{1} = {2}'.format(str(panel_num) + str(______P), str(key), value))
                                    else:
                                        lines.append('{0}-{1} = {2}'.format(str(panel_num), str(key), value))
                                        
                                    count += 1
                                # elif ('[fence{0}]'.format(___)) not in lines:
                                #     lines.append('\n[fence{0}]'.format(___))
                                #     lines.append('enable = 0')
                if ('\n[fence{0}]'.format(___)) not in lines:
                    lines.append('\n[fence{0}]'.format(___))
                    lines.append('enable = 0')
                    lines.append('hooter-relay-details = Null')
                fence_count_ += 1
                index += 1
            with open(config_fences_file, 'w') as f:
                for fence_, item in enumerate(lines):
                    f.write('%s\n' % item)
    return  CAMIDUPDATEDETAILS

@dashboard.route('/create_esi_multiconfig', methods=['GET'])
def ESICREAeeTECONFIG1121():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        esi_app_set_ESI_monitoring_started(True)
        return_data = ESINEWCAMERAIDupdatenew()
        # HYDRACREATECONFIG()
        if return_data:
            # stop_application_for_esi_creating_config()
            if return_data['success'] == True:
                esi_app_set_ESI_monitoring_started(False)
                ret = {'message':'esi config files are created successfully.', 'success': True}
            else:
                ret['message' ] = 'something went wrong  creating config files.'
        else:
            ret['message'] = ' feeder data not found to create config files.'
    else:
        ret = ret
    return ret


def UpdateHooterAcknowldgementstatus():
    database_detail = {'sql_panel_table':'dockappanalyticstable', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE ' + database_detail['sql_panel_table'] + " set analytics_data = jsonb_set(analytics_data, \'{status}\', \'\"OFF\"\'), datauploadstatus =0 where date='20240606' and analytics_data->>'status'='ON' ;")
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
    
    cursor.close()
    conn.commit()
    conn.close()  
    return license_status

@dashboard.route('/stop_app_common', methods=['GET'])
def stop_application_1_app_common():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        app_set_common_monitoring_started(True)
        createHOOTERMETAJSONSTOP()
        UpdateHooterAcknowldgementstatus()

        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret



# @dashboard.route('/stop_phaseoneapp', methods=['GET'])
# def stop_application_1_phaseoneapp():
#     ret = {'message': 'something went wrong with create config.', 'success': False}
#     if 1:
#         app_set_phaseoneapp_monitoring_started(True)
#         ret = {'message': 'application stopped.', 'success': True}
#     else:
#         ret = ret
#     return ret


@dashboard.route('/stop_app_esi', methods=['GET'])
def stop_application_1_app_esi():
    ret = {'message': 'something went wrong with create config.', 'success':  False}
    if 1:
        esi_app_set_ESI_monitoring_started(True)
        reset_tsk_riro_table_dataupload_12_to_13()
        reset_mag_flash_table_dataupload_to_25()
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret


def verify_rtsp(detector,type, video_name, camera_ip_address, url):
    print("camera url getting ==",url)
    response = True
    if video_name is not None and video_name !='':
        if 'rtsp' in video_name :
            url = video_name
        else:
            url =  os.path.join(get_current_dir_and_goto_parent_dir() , 'test_videos',video_name)
    verfy_rtsp_response = None
    if response:
        directory_path =  os.path.join(os.getcwd() , 'rtsp_roi_image')
        if not os.path.exists(directory_path):
            handle_uploaded_file(directory_path)
        present_time = replace_spl_char(str(datetime.now()))
        print('verify___rtsp====',url)
        cam = cv2.VideoCapture(url)
        full_path = None
        count=0
        newpanelpoints = []
        RackwindowMODEL = os.path.join(os.getcwd() , 'Data_recieving_and_Dashboard','Rw_detection_yolo_v8_19_02_2024.onnx')
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
                                    if type == 'ht' or type == 'HT':
                                        panel_detection_data = (panel_detection_function_for_image(detector,full_path1))
                                        if len(panel_detection_data) != 0:
                                            for PANLINDEX , DETECTEDPANELPOINTS in enumerate(panel_detection_data):
                                                print("-----DETECTEDPANELPOINTS----",DETECTEDPANELPOINTS)
                                                NEWRACKWINDOW = extract_rw_bbox_details_cv2( DETECTEDPANELPOINTS['bbox'], full_path, RackwindowMODEL )
                                                # NEWRACKWINDOW = extract_rw_bbox_details( DETECTEDPANELPOINTS['bbox'], frame )
                                                print("------------------------NEW RACKWINDOW --",NEWRACKWINDOW)
                                                if NEWRACKWINDOW is not None :
                                                    DETECTEDPANELPOINTS['RW']=NEWRACKWINDOW
                                                    newpanelpoints.append(DETECTEDPANELPOINTS)
                                                else:
                                                    newpanelpoints.append(DETECTEDPANELPOINTS)


                                        print('----------------------------------------------0000----------',panel_detection_data)
                                    else:
                                        panel_detection_data = None
                                        newpanelpoints = None
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name, 'panel_detection': panel_detection_data}
                                    # verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name, 'panel_detection': newpanelpoints}
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
                                    if type == 'ht' or type == 'HT':
                                        panel_detection_data = (panel_detection_function_for_image(detector,full_path1))
                                        if len(panel_detection_data) != 0:
                                            for PANLINDEX , DETECTEDPANELPOINTS in enumerate(panel_detection_data):
                                                print("-----DETECTEDPANELPOINTS----",DETECTEDPANELPOINTS)
                                                
                                                NEWRACKWINDOW = extract_rw_bbox_details_cv2( DETECTEDPANELPOINTS['bbox'], full_path, RackwindowMODEL )

                                                # NEWRACKWINDOW = extract_rw_bbox_details( DETECTEDPANELPOINTS['bbox'], frame )
                                                print("------------------------NEW RACKWINDOW --",NEWRACKWINDOW)
                                                if NEWRACKWINDOW is not None :
                                                    DETECTEDPANELPOINTS['RW']=NEWRACKWINDOW
                                                    newpanelpoints.append(DETECTEDPANELPOINTS)
                                                else:
                                                    newpanelpoints.append(DETECTEDPANELPOINTS)

                                        print('----------------------------------------------111111----------',panel_detection_data)
                                    else:
                                        panel_detection_data = None
                                        newpanelpoints = None
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name, 'panel_detection': panel_detection_data}
                                    # verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name, 'panel_detection': newpanelpoints}
                                    break
                    count += 1
                else:
                    break
            cam.release()
            #cv2.destroyAllWindows()
    return verfy_rtsp_response

def VERIFYRTSPFOREXTRAPANELS( jobtype, url):
    response = True
    verfy_rtsp_response = None
    if response:
        directory_path = os.path.join(os.getcwd() ,'rtsp_roi_image')
        if not os.path.exists(directory_path):
            handle_uploaded_file(directory_path)
        present_time = replace_spl_char(str(datetime.now()))
        cam = cv2.VideoCapture(url)
        full_path = None
        if cam.isOpened() == True:
            name = 'docketrun' + '_' + present_time + '.jpg'
            name1 = 'docketrun' + '_' + present_time + '1' + '.jpg'
            while cam.isOpened():
                ret, frame = cam.read()
                if ret:
                    full_path = directory_path + '/' + name
                    full_path1 = directory_path + '/' + name1
                    cv2.imwrite(full_path, frame)
                    cv2.imwrite(full_path1, frame)
                    image_resizing(full_path)
                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name}
                    break
                else:
                    break
            cam.release()
            #cv2.destroyAllWindows()
    return verfy_rtsp_response



def for_all_panel_id(detector,type, video_name, panel_list, ipaddress,camera_brand, camera_username,camera_password):
    data_append = []
    data = {}
    if camera_username == '':
        camera_username = 'admin'
    if camera_password == '':
        camera_password = 'TATA_tsk123'
    rtsp_url = ESIBRANDCAMERASRTSP(ipaddress,camera_brand,camera_username,camera_password)#create_rtsp(ipaddress)
    print('RTSP ------------------------------ ', rtsp_url)
    image_data = verify_rtsp(detector,type, video_name, ipaddress, rtsp_url)
    if video_name is not None and video_name !='':
        if 'rtsp' in video_name:
            rtsp_url = video_name
        else:
            rtsp_url ='file:///'+get_current_dir_and_goto_parent_dir()+ '/docketrun_eis_monitor/configs/../../test_videos/'+ video_name

    print("-----file -------------------RTSP ---------------",rtsp_url)
    print('image_data', image_data)
    if type =='HT' or type =='ht': 
        if image_data is not None:
            data['ip_address'] = ipaddress
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if ipaddress is not None and ipaddress !='':
                camera_name= remove_all_specail_char_with_hifhen(ipaddress)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            for i, j in enumerate(panel_list):
                panel_id_list_refer = 0
                if image_data['status'] == True:
                    data['rtsp_status'] = image_data['status']
                    data['image_name'] = image_data['image_name']
                    data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
                    for ___k, in__kk in enumerate(image_data['panel_detection']):
                        if j == in__kk['panel_no']:
                            panel_id_list_refer = 1
                            panel_key_id_list.append(in__kk['panel_key_id'])
                            data_append.append({'panel_id': str(j), 'roi_data': in__kk, 'panel_status': None,'isolation_status':None,'flasher_status':None})
                if panel_id_list_refer != 1:
                    print(' --------------------- PANEL NUMBER IS NOT CAMPARED  ---------------------- ')
            for ___k, in__kk in enumerate(image_data['panel_detection']):
                if in__kk['panel_key_id'] not in panel_key_id_list:
                    data_append.append({'panel_id': 'NA', 'roi_data': in__kk,'panel_status': None,'isolation_status':None,'flasher_status':None})
            data['panel_data'] = data_append
            return data
        else:
            return None

    elif type =='Hydraulic' or type =='hydraulic' :
        if image_data is not None:
            data['ip_address'] = ipaddress
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if ipaddress is not None and ipaddress !='':
                camera_name= remove_all_specail_char_with_hifhen(ipaddress)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            # for i, j in enumerate(panel_list):
            #     panel_id_list_refer = 0
            if image_data['status'] == True:
                data['rtsp_status'] = image_data['status']
                data['image_name'] = image_data['image_name']
                data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            data['hydraulic_data'] =[]
            return data

    elif type =='pneumatic' or type =='Pneumatic' :
        if image_data is not None:
            data['ip_address'] = ipaddress
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if ipaddress is not None and ipaddress !='':
                camera_name= remove_all_specail_char_with_hifhen(ipaddress)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            # for i, j in enumerate(panel_list):
            #     panel_id_list_refer = 0
            if image_data['status'] == True:
                data['rtsp_status'] = image_data['status']
                data['image_name'] = image_data['image_name']
                data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            data['hydraulic_data'] =[]
            return data

    else:
        if image_data is not None:
            data['ip_address'] = ipaddress
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if ipaddress is not None and ipaddress !='':
                camera_name= remove_all_specail_char_with_hifhen(ipaddress)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            for i, j in enumerate(panel_list):
                panel_id_list_refer = 0
                if image_data['status'] == True:
                    data['rtsp_status'] = image_data['status']
                    data['image_name'] = image_data['image_name']
                    data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            data['panel_data'] =[]
            return data



def JOBrawdata(detector,row):
    if row is not None:
        if row['ip_address'] is not None:
            if row['panel'] is not None:
                return_data = for_all_panel_id(detector,row['type'], row[ 'video_names'], row['panel'], row['ip_address'],row['camera_brand'],row['camera_username'],row['camera_password'])
                if return_data is not None:
                    if isEmpty(return_data):
                        row['data'] =return_data
                    else:
                        row['data'] ={}   
                else  :
                    row['data'] =None 
    return row



def GETJOBSHEETDETAILS(job_sheet_name,token_key):
    try:
        if job_sheet_name is not None:
            row = {}
            row['job_sheet_name'] = job_sheet_name
            row['shutdownname'] = job_sheet_name
            row['timestamp'] = now_time_with_time()
            row['status'] = 1
            row['token'] =token_key
            row['reset_time'] = None
            result = mongo.db.job_sheet_details.insert_one(row)
            if result.acknowledged > 0:
                pass
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- GETJOBSHEET222DETAILS 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- GETJOBSHEET22DETAILS 2", str(error), " ----time ---- ", now_time_with_time()]))
    return row['token']

def check_license_of_camera(CamCount):
    print(CamCount)
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        print('device_location', res['device_location'])
        lic = res['device_location']
        split_data=lic.split('_')[1].split("l")
        while '' in split_data:
            split_data.remove('')
        if CamCount < int((split_data[0])):
            license_status = True
        elif CamCount == int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status


def convert_to_int(value):
    try:
        result = int(value)
        return result
    except ValueError:
        return value

def read_the_excel_file_data_insert_to_db_new_concept(detector,csv_creating_file,jobsheetfile, df, token):
    print(df)
    table = open(csv_creating_file + '.csv', 'r')
    reader = csv.DictReader(table)
    header = df.head()
    count = 0
    ip_address_count= []
    ALL_DATA = []
    for i____, each in enumerate(reader):
        row = {}
        row['token'] = token
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
                    eachrow['job_sheet_name'] = jobsheetfile
                    eachrow['sheet_status'] = True
                    eachrow['job_sheet_time'] = str(now_time_with_time())
                    if final_ping(eachrow['ip_address']): 
                        eachrow['ip_status'] = {'ip': eachrow['ip_address'],'status': True}
                    else:
                        eachrow['ip_status'] = {'ip': eachrow['ip_address'],'status': False}
                else:
                    eachrow['job_sheet_name'] = jobsheetfile
                    eachrow['sheet_status'] = False
                    eachrow['ip_status'] = {'ip': None, 'status': False}
                    eachrow['job_sheet_time'] = str(now_time_with_time())

                print("---eachrow---ip_status",eachrow)
                    
                if eachrow['ip_status']['status'] :                        
                    if dictionary_key_exists(eachrow,'video_names'):
                        pass
                    else:
                        eachrow['video_names']=None   
                        
                    if dictionary_key_exists(eachrow,'feeder_number'):
                        eachrow['panel'] = eachrow['feeder_number']
                        try:
                            del eachrow['feeder_number']
                        except :
                            pass
                        
                    if dictionary_key_exists(eachrow,'switch_board_name'):
                        eachrow['board'] = eachrow['switch_board_name']
                        try:
                            del eachrow['switch_board_name']
                        except :
                            pass
                        
                    if dictionary_key_exists(eachrow,'job_type'):
                        eachrow['type'] = eachrow['job_type']
                        try:
                            del eachrow['job_type']
                        except :
                            pass
                        
                    if dictionary_key_exists(eachrow,'tag_name'):
                        eachrow['tagname'] = eachrow['tag_name']
                        try:
                            del eachrow['tag_name']
                        except :
                            pass   

                    eachrow['job_no'] = convert_to_int(eachrow['job_no'])               
                    try:
                        if type(eachrow['job_no']) == str:
                            eachrow['job_no'] = int(eachrow['job_no'])
                        elif type(eachrow['job_no']) == float:
                            eachrow['job_no'] = int(eachrow['job_no'])
                        elif type(eachrow['job_no']) == int:
                            eachrow['job_no'] = int(eachrow['job_no'])
                    except Exception as  error:
                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- read_the_excel_file_data_ins44ert_to_db_new_concept 2", str(error), " ----time ---- ", now_time_with_time()]))
                        try:
                            eachrow['job_no'] = int(eachrow['job_no'])
                        except Exception as  error:
                            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- read_the_excel_file_data44_insert_to_db_new_concept 3", str(error), " ----time ---- ", now_time_with_time()]))
                            eachrow['job_no'] = eachrow['job_no']
                    if eachrow['ip_status']['status'] == True:
                        find_data = None#mongo.db.panel_data.find_one({ 'job_sheet_time':{'$regex': '^' + str(date.today())}, 'job_sheet_name': eachrow['job_sheet_name'],'token': token})#'job_no': eachrow['job_no'],
                        if find_data is None:
                            eachrow = JOBrawdata(detector,eachrow)
                            if eachrow['data'] is not None:
                                if isEmpty(eachrow['data']) :
                                    print('raw data --- data is not empty in  inserting 1')
                                    if type(eachrow['data']) == list :
                                        eachrow['data'] = eachrow['data'][0]
                                    print("jobnumber========111",eachrow['job_no'],type(eachrow['job_no']))
                                    eachrow['job_no'] = convert_to_int(eachrow['job_no']) 
                                    print("jobnumber========1.===2",eachrow['job_no'],type(eachrow['job_no']))
                                    if type(eachrow['job_no']) == str:
                                        if '.' in eachrow['job_no']:
                                            eachrow['job_no']=int(eachrow['job_no'].split('.')[0])
                                    eachrow['remark']  = None
                                    eachrow['job_type']= 'main_job'
                                    result = mongo.db.panel_data.insert_one(eachrow)
                                    if result.acknowledged > 0:
                                        pass
                                    if mongo.db.job_sheet_details.find_one({'job_sheet_name': eachrow['job_sheet_name'],'token': token}) is None:
                                        GETJOBSHEETDETAILS(jobsheetfile,token)
                                else:
                                    print('raw data --- data is empty in  inserting 1')
                                    if type(row['data']) == list :
                                        row['data'] = row['data'][0]
                                    print("jobnumber========222",eachrow['job_no'],type(eachrow['job_no']))
                                    eachrow['job_no'] = convert_to_int(eachrow['job_no']) 
                                    print("jobnumber========22...===2",eachrow['job_no'],type(eachrow['job_no']))
                                    if type(eachrow['job_no']) == str:
                                        if '.' in eachrow['job_no']:
                                            eachrow['job_no']=int(eachrow['job_no'].split('.')[0])
                                    eachrow['remark']  = None
                                    eachrow['job_type']= 'main_job'
                                    result = mongo.db.panel_data.insert_one(eachrow)
                                    if mongo.db.job_sheet_details.find_one({'job_sheet_name': eachrow['job_sheet_name'],'token': token}) is None:
                                        GETJOBSHEETDETAILS(jobsheetfile,token)
                                    if result.acknowledged > 0:
                                        pass
                    else:
                        print('--------- ip is not working -------------- ')
                        print("jobnumber========3333",eachrow['job_no'],type(eachrow['job_no']))
                        eachrow['job_no'] = convert_to_int(eachrow['job_no']) 
                        print("jobnumber========3333====3333",eachrow['job_no'],type(eachrow['job_no']))
                        if type(eachrow['job_no']) == str:
                            if '.' in eachrow['job_no']:
                                eachrow['job_no']=int(eachrow['job_no'].split('.')[0])
                        eachrow['remark']  = None
                        eachrow['type']= eachrow['job_type']
                        eachrow['job_type']= 'main_job'
                        if 'panel' in eachrow :
                            eachrow['panel']= eachrow['panel']
                        if 'feeder_number' in eachrow :
                            eachrow['panel']= eachrow['feeder_number']
                        result = mongo.db.panel_data.insert_one(eachrow)
                        find_data = mongo.db.panel_data.find_one({ 'job_sheet_time':{'$regex': '^' + str(date.today())}, 'job_no': eachrow['job_no'],'job_sheet_name': eachrow['job_sheet_name'],'token': token})
                        if find_data is None:
                            eachrow['data'] = {}    
                        if mongo.db.job_sheet_details.find_one({'job_sheet_name': eachrow['job_sheet_name'],'token': token}) is None:
                            GETJOBSHEETDETAILS(jobsheetfile,token)   
                else:
                    print('--------- ip is not working -------------- ')
                    print("jobnumber========3333",eachrow['job_no'],type(eachrow['job_no']))
                    eachrow['job_no'] = convert_to_int(eachrow['job_no']) 
                    print("jobnumber========3333====3333",eachrow['job_no'],type(eachrow['job_no']))
                    if type(eachrow['job_no']) == str:
                        if '.' in eachrow['job_no']:
                            eachrow['job_no']=int(eachrow['job_no'].split('.')[0])
                    eachrow['remark']  = None
                    eachrow['type']= eachrow['job_type']
                    if 'panel' in eachrow :
                        eachrow['panel']= eachrow['panel']
                    if 'feeder_number' in eachrow :
                        eachrow['panel']= eachrow['feeder_number']
                    eachrow['job_type']= 'main_job'                    
                    eachrow['data']={}
                    result = mongo.db.panel_data.insert_one(eachrow)
                    find_data = mongo.db.panel_data.find_one({ 'job_sheet_time':{'$regex': '^' + str(date.today())}, 'job_no': eachrow['job_no'],'job_sheet_name': eachrow['job_sheet_name'],'token': token})
                    if find_data is None:
                        eachrow['data'] = {}    
                    if mongo.db.job_sheet_details.find_one({'job_sheet_name': eachrow['job_sheet_name'],'token': token}) is None:
                        GETJOBSHEETDETAILS(jobsheetfile,token)             
        else:
            return {'error':False,'message':'limit exceeded','success':False}


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


def check_excel_columns(file_path, column_names):
    try:
        try:
            df = pd.read_excel(file_path)
            existing_columns = df.columns.tolist()
            existing_columns_lower = [col.lower() for col in existing_columns]
            column_names_lower = [col.lower() for col in column_names]
            missing_columns = [col for col in column_names_lower if col not in existing_columns_lower]
            if not missing_columns:
                print("All specified columns are present in the Excel file.")
                return True
            else:
                missing_columns_original = [col for col in column_names if col.lower() in missing_columns]
                print("Missing columns:", missing_columns_original)
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
                    print("Missing columns:", missing_columns_original)
                return missing_columns_original
            except Exception as  error:
                print("")
                #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 2", str(error), " ----time ---- ", now_time_with_time()]))
        # df = pd.read_excel(file_path)
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file):
    TOtallicense = GETCAMERALICENSE()
    LISTIPaddress = GETLISTOFIPSEXISTS()
    print("TOtallicense-----------------",TOtallicense)
    # print("LISTIPaddress",LISTIPaddress)
    Remaininglicense = TOtallicense['message']['remaining_license'] 
    totalcamerasinexcel =Getipaddresslist(get_excel_file,LISTIPaddress)
    if type(totalcamerasinexcel)==list:
        print("Remaininglicense<=len(LISTIPaddress)",Remaininglicense,len(totalcamerasinexcel))
        print("listed================licenser ===",len(totalcamerasinexcel) <=Remaininglicense)
        if Remaininglicense !=0 and len(totalcamerasinexcel) <=Remaininglicense:
            return True
        else:
            return False
    else:
        return None


@dashboard.route('/upload_file', methods=['POST'])
def file_upload():
    from Data_recieving_and_Dashboard.app import DetectPanel
    detector = DetectPanel()
    ret = {'message': 'Something error has occured in your code', 'success': False}
    file_key = ['file']
    missed_file_key = []
    excelfile = request.files
    convert_list = dict(excelfile.lists())
    converting_set = set(convert_list)
    f_key = set(file_key)
    missing_key = list(sorted(f_key - converting_set))
    get_excel_file = request.files.get('file')
    columns_to_lowercase = ['Camera Brand']
    if len(missing_key) != 0:
        ret = {'message':'You have missed these parameters {0} to enter. please enter properly.'.format(missing_key), 'success': False}
    elif len(get_excel_file.filename) != 0:
        app_run_response = esi_app_set_ESI_monitoring_started(True)
        excelfilepath = 'panel_data_excels'
        now = datetime.now()
        csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
        filename_db = os.path.join(os.getcwd(), excelfilepath,"ESI_MONITORING_"+now.strftime('%m-%d-%Y-%H-%M-%S.')+str(extention_of_excel))
        handle_uploaded_file(os.path.join(os.getcwd(),excelfilepath))
        get_excel_file.seek(0)
        get_excel_file.save(os.path.join(os.getcwd(),excelfilepath,filename_db))#os.path.join(os.getcwd(),excelfilepath,filename_db)
        columns_to_check = ['Job No', 'Job Type', 'Department', 'Sub Area', 'Job Description', 'No. of Isolating Points', 'Isolating Location', 
        'Switch Board Name', 'Feeder Number', 'IP Address', 'TagName','Camera Brand', 'camera_username','camera_password']
        missingcolumns = check_excel_columns(get_excel_file, columns_to_check)
        if missingcolumns is not None:
            if type(missingcolumns) ==list:
                if len(missingcolumns) !=0 and len(missingcolumns) ==1 :
                    if 'video names' in missingcolumns:
                        token_key =genarate_alphanumeric_key()
                        Extension_excel = ['.XLS', '.XLSX', '.xls', '.xlsx']
                        csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
                        excel_sheet_name = 'ESI_MONITORING_' + now.strftime('%m-%d-%Y-%H-%M-%S')
                        csv_creating_file = os.path.join(os.getcwd() ,excelfilepath , excel_sheet_name)
                        if get_excel_file.filename.endswith(tuple(Extension_excel)):
                            print("----------------------CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file)",CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file))
                            if CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file)== True or CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file)== None :
                                # try:
                                #     read_file = pd.read_excel(filename_db, skiprows=lambda x: x > 0 and all(pd.isna(y) for y in x))
                                #     read_file.to_csv(csv_creating_file + '.csv', index=None, header=True)
                                #     print('Excel file successfully read and converted to CSV:', csv_creating_file + '.csv')
                                # except Exception as error1:
                                #     ERRORLOGdata(f"\n[ERROR] dashboard_apis -- upload_file 1: {str(error1)} ----time ---- {now_time_with_time()}")
                                #     try:
                                #         read_file = pd.read_excel(filename_db, engine='openpyxl', skiprows=lambda x: x > 0 and all(pd.isna(y) for y in x))
                                #         read_file.to_csv(csv_creating_file + '.csv', index=None, header=True)
                                #         print('Excel file successfully read and converted to CSV (using openpyxl):', csv_creating_file + '.csv')
                                #     except Exception as error2:
                                #         ERRORLOGdata(f"\n[ERROR] dashboard_apis -- upload_file 2: {str(error2)} ----time ---- {now_time_with_time()}")

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
                                df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)          
                                if check_the_ip_status(csv_creating_file,df):
                                    check_status_variable =  read_the_excel_file_data_insert_to_db_new_concept(detector,csv_creating_file , get_excel_file.filename, df, token_key)
                                    print('uploading-completed----------')
                                    if check_status_variable is None: 
                                        ret = {'message': 'successfully added', 'success': True}
                                                                            
                                    else:
                                        print("check statu variable ===", check_status_variable)
                                        if check_status_variable['error']:
                                            ret= {'message': check_status_variable['message'], 'success': False}
                                        else:
                                            sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
                                            if len(sheet_data) != 0:
                                                think = 0
                                                app_run_response = esi_app_set_ESI_monitoring_started(True)
                                                for im, simin in enumerate(sheet_data):
                                                    filters = {'_id': ObjectId(simin['_id'])}
                                                    newvalues = {'$set':{'status': 0}}
                                                    result = mongo.db.job_sheet_details.update_one(filters, newvalues)
                                                    if result.modified_count > 0:
                                                        think += 1
                                else:
                                    ret={'message': 'maximum camera limit has reached.', 'success': False}
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
                token_key = genarate_alphanumeric_key()
                Extension_excel = ['.XLS', '.XLSX', '.xls', '.xlsx']
                csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
                excel_sheet_name = 'ESI_MONITORING_' + now.strftime('%m-%d-%Y-%H-%M-%S')
                csv_creating_file = os.path.join(os.getcwd() ,excelfilepath , excel_sheet_name)
                if get_excel_file.filename.endswith(tuple(Extension_excel)):
                    print("----------------------CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file)",CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file))
                    if CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file)== True or CHECKCAMERASANDLICENSEFOrJObsheet(get_excel_file)== None :
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
                        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)          
                        if check_the_ip_status(csv_creating_file,df):
                            check_status_variable =  read_the_excel_file_data_insert_to_db_new_concept(detector,csv_creating_file , get_excel_file.filename, df, token_key)
                            
                            print('uploading-completed----------')
                            if check_status_variable is None: 
                                ret = {'message': 'successfully added', 'success': True}
                            else:
                                print("check statu variable ===", check_status_variable)
                                if check_status_variable['error']:
                                    ret= {'message': check_status_variable['message'], 'success': False}
                                    
                                else:
                                    sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
                                    if len(sheet_data) != 0:
                                        think = 0
                                        app_run_response = esi_app_set_ESI_monitoring_started(True)
                                        for im, simin in enumerate(sheet_data):
                                            filters = {'_id': ObjectId(simin['_id'])}
                                            newvalues = {'$set':{'status': 0}}
                                            result = mongo.db.job_sheet_details.update_one(filters, newvalues)
                                            if result.modified_count > 0:
                                                think += 1
                        else:
                            ret={'message': 'maximum camera limit has reached.', 'success': False}
                    else:
                        ret={'message': 'maximum camera limit has reached.', 'success': False}
                else:
                    ret['message'] = 'Please upload correct format excel sheet.'
            else:
                    ret = {'message': 'missing column names - {0}'.format(missingcolumns),'success': False}
        else:
            ret = {'message': 'missing column names - {0}'.format(missingcolumns),'success': False}
    else:
        ret = {'message': 'missing file {0}'.format(converting_set),'success': False}
    return ret



def getjobnumberslist(job_sheet_name,token):
    print()#'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']
    getdatajobnumberdata = list(mongo.db.panel_data.find({'job_sheet_name':job_sheet_name, 'token':token}))
    jobnumberlist = []
    if len(getdatajobnumberdata) !=0 :
        for i, eachjobnumber in enumerate(getdatajobnumberdata):
            if eachjobnumber['job_no'] not in jobnumberlist :
                jobnumberlist.append(eachjobnumber['job_no'])
    return jobnumberlist



def Readnumbercolumn(file_path,column_names):
    try:
        try:
            df = pd.read_excel(file_path)
            df = df.dropna(how='all')
            existing_columns = df['Job No'].tolist()
            print("columns ==read",existing_columns)
            existing_columns = [int(float(element)) if isinstance(element, (float, int, str)) else None for element in existing_columns]
            print("converted list llll-------",existing_columns)
            common_elements = set(existing_columns).intersection(column_names)
            return common_elements
        except Exception as  error:        
            try:
                print("second try for reading excel ====")
                df = pd.read_excel(file_path, engine='openpyxl')
                df = df.dropna(how='all')
                existing_columns = df['Job No'].tolist()
                
                print("columns ==read",existing_columns)
                existing_columns = [int(float(element)) if isinstance(element, (float, int, str)) else None for element in existing_columns]
                print("converted list llll-------",existing_columns)
                common_elements = set(existing_columns).intersection(column_names)
                return common_elements
            except Exception as  error:
                print("")
                #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- upload_file 2", str(error), " ----time ---- ", now_time_with_time()]))
        # df = pd.read_excel(file_path)
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None



@dashboard.route('/AddJobsViasheet', methods=['POST'])
def Addjobviasheet():
    from Data_recieving_and_Dashboard.app import DetectPanel
    detector = DetectPanel()
    ret = {'message': 'Something error has occured in your code', 'success': False}
    file_key = ['file']
    excelfile = request.files
    convert_list = dict(excelfile.lists())
    converting_set = set(convert_list)
    f_key = set(file_key)
    missing_key = list(sorted(f_key - converting_set))
    get_excel_file = request.files.get('file')
    print("get_excel_file===",get_excel_file)
    columns_to_lowercase = ['Camera Brand']
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if sheet_data is not None:
        #['job_sheet_name']
        token_key =sheet_data['token']
        sheetname = sheet_data['job_sheet_name']
        if len(missing_key) != 0:
            ret = {'message':'You have missed these parameters {0} to enter. please enter properly.'.format(missing_key), 'success': False}
        elif len(get_excel_file.filename) != 0:
            excelfilepath = 'panel_data_excels'
            now = datetime.now()
            csv_creating_file, extention_of_excel = os.path.splitext(get_excel_file.filename)
            filename_db = os.path.join(os.getcwd(), excelfilepath,"ESI_MONITORING_"+now.strftime('%m-%d-%Y-%H-%M-%S.')+str(extention_of_excel))
            handle_uploaded_file(os.path.join(os.getcwd(),excelfilepath))
            get_excel_file.seek(0)
            get_excel_file.save(os.path.join(os.getcwd(),excelfilepath,filename_db))#os.path.join(os.getcwd(),excelfilepath,filename_db)
            columns_to_check = ['Job No', 'Job Type', 'Department', 'Sub Area', 'Job Description', 'No. of Isolating Points', 'Isolating Location', 
            'Switch Board Name', 'Feeder Number', 'IP Address', 'TagName', 'Camera Brand','camera_username','camera_password']
            missingcolumns = check_excel_columns(get_excel_file, columns_to_check)
            print("check job numbers ===", )
            listofjobnumbers = getjobnumberslist(sheetname,token_key)
            print("listed job numbers ====",listofjobnumbers)
            results_jobnumber = Readnumbercolumn(get_excel_file,listofjobnumbers)
            print("results_jobnumber====",results_jobnumber)
            if missingcolumns is not None:
                if results_jobnumber is  None or len(results_jobnumber) ==0:                    
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
                                        check_status_variable =  read_the_excel_file_data_insert_to_db_new_concept(detector,csv_creating_file , sheetname, df, token_key)
                                        print('uploading-completed----------')
                                        if check_status_variable is None: 
                                            ret = {'message': 'successfully added', 'success': True}
                                                                                
                                        else:
                                            print("check statu variable ===", check_status_variable)
                                            if check_status_variable['error']:
                                                ret= {'message': check_status_variable['message'], 'success': False}
                                            else:
                                                sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
                                                if len(sheet_data) != 0:
                                                    think = 0
                                                    print("sheet_data----",sheet_data)
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
                                check_status_variable =  read_the_excel_file_data_insert_to_db_new_concept(detector,csv_creating_file , sheetname, df, token_key)
                                
                                print('uploading-completed----------')
                                if check_status_variable is None: 
                                    ret = {'message': 'successfully added', 'success': True}
                                else:
                                    print("check statu variable ===", check_status_variable)
                                    if check_status_variable['error']:
                                        ret= {'message': check_status_variable['message'], 'success': False}
                                        
                                    else:
                                        sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
                                        if len(sheet_data) != 0:
                                            think = 0
                            else:
                                ret={'message': 'maximum camera limit has reached.', 'success': False}
                        else:
                            ret['message'] = 'Please upload correct format excel sheet.'
                    else:
                        ret = {'message': 'missing column names - {0}'.format(missingcolumns),'success': False}
                else:
                    ret['message']='in uploaded jobsheet {0} job numbers are already exist, please remove already exist job number and then try to upload.'.format(results_jobnumber)
            else:
                ret = {'message': 'missing column names - {0}'.format(missingcolumns),'success': False}
        else:
            ret = {'message': 'missing file {0}'.format(converting_set),'success': False}
    else:
        ret['message']='job sheet is not yet uploaded, please upload job sheet.'
    return ret

def PANELWISERIRODATAFUNCTION(data):
    all_data = []
    data = parse_json(data)
    if 1:
    # try:
        if type(data) == list:
            for __, i in enumerate(data):
                if i['type']=='HT' or i['type']=='ht':
                    if isEmpty(i['data']) :
                        all_panel_data = i['data']
                        if len(all_panel_data['panel_data']) == 1:
                            yxz = i['data']
                            yxz['panel_data'] = yxz['panel_data'][0]
                            i['data'] = yxz
                            zz =i 
                            return_1 = REPATATIVERIRODATA(zz, all_data)
                            if return_1:
                                all_data.append(return_1)
                        elif len(all_panel_data['panel_data']) > 1:
                            panel_data1 = all_panel_data
                            for __, iii in enumerate(all_panel_data['panel_data']):
                                panel_data1['panel_data'] = iii
                                i['data'] = panel_data1
                                return_1 = REPATATIVERIRODATA(i, all_data)
                                if return_1:
                                    all_data.append(return_1)                                    
        elif isEmpty(data['data']) :
            all_panel_data = data['data']
            if len(all_panel_data['panel_data']) == 1:
                yxz = data['data']
                yxz['panel_data'] = yxz['panel_data'][0]
                data['data'] = yxz
                zz = data
                return_1 = REPATATIVERIRODATA(zz, all_data)
                if return_1:
                    all_data.append(return_1)
            elif len(all_panel_data['panel_data']) > 1:
                panel_data1 = all_panel_data
                for __, iii in enumerate(all_panel_data['panel_data']):
                    panel_data1['panel_data'] = iii
                    data['data'] = panel_data1
                    return_1 = REPATATIVERIRODATA(data, all_data)
                    if return_1:
                        all_data.append(return_1)
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  1", str(error), " ----time ---- ", now_time_with_time()]))
    return all_data






def MUPANRRILATION_multi_isolation(data):
    all_data = []
    data = parse_json(data)
    if 1:
    # try:
        if type(data) == list:
            for __, i in enumerate(data):
                if i['type'] is not None and i['type'] =='HT' or i['type'] =='ht':
                    # if i['type'] =='HT' or i['type'] =='ht': 
                    if isEmpty(i['data']):
                        if len(i['data']['panel_data']) !=0:
                            if len(i['data']['panel_data']) == 1:
                                yxz = i['data']
                                yxz['panel_data'] = yxz['panel_data'][0]
                                if yxz['panel_data']['roi_data']['unallocated_job_status'] == False:
                                    i['data'] = yxz
                                    zz = i
                                    return_1 = REPATATIVERIRODATA(zz, all_data)
                                    if return_1:
                                        all_data.append(return_1)
                            elif len(i['data']['panel_data']) > 1:
                                panel_data1 = i['data']
                                for __, iii in enumerate(i['data']['panel_data']):
                                    if iii['roi_data']['unallocated_job_status'] == False:
                                        panel_data1['panel_data'] = iii
                                        i['data'] = panel_data1
                                        return_1 = REPATATIVERIRODATA(i, all_data)
                                        if return_1:
                                            all_data.append(return_1)
                        else:
                            all_data.append(i)
                    else:
                        all_data.append(i)
                else:
                    if len(i['data']):
                        return_2 = MUlRIRODATACMECH(i, all_data)
                        if return_2:
                            all_data.append(return_2) 
                    else:
                        all_data.append(i)  
        elif  data is not None:
            # print('---------data---new ----',data)   
            all_data.append(data)                
            
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- MUPANRRILATION222_multi_isolation 1", str(error), " ----time ---- ", now_time_with_time()]))
    return all_data

def FUNCHECKrepeativeJobSheetstatus(data):
    all_data = []
    data = parse_json(data)
    if 1:
    # try:
        for __, i in enumerate(data):
            if isEmpty(i['data']):
                if i['type']== 'HT' or i['type']== 'ht':
                    if isEmpty(i['data']):
                        all_panel_data = i['data']
                        if len(all_panel_data['panel_data']) == 1:
                            yxz = i['data']
                            yxz['panel_data'] = yxz['panel_data'][0]
                            if yxz['panel_data']['roi_data']['unallocated_job_status'] == False:
                                if yxz['panel_data']['panel_id'] != 'NA':
                                    i['data'] = yxz
                                    zz =i 
                                    return_1 = REPATATIVERIRODATA(zz, all_data)
                                    if return_1:
                                        all_data.append(return_1)
                        elif len(all_panel_data['panel_data']) > 1:
                            panel_data1 = all_panel_data
                            for __, iii in enumerate(all_panel_data['panel_data']):
                                if iii['roi_data']['unallocated_job_status'] == False:
                                    panel_data1['panel_data'] = iii
                                    if panel_data1['panel_data']['panel_id'] != 'NA':
                                        i['data'] = panel_data1
                                        return_1 = REPATATIVERIRODATA(i, all_data)
                                        if return_1:
                                            all_data.append(return_1)                
                else:
                    return_2 = MUlRIRODATACMECH(i, all_data)
                    if return_2:
                        all_data.append(return_2) 
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- FUNCHECKrepeat33iveJobSheetstatus 1", str(error), " ----time ---- ", now_time_with_time()]))
    return all_data


def rw_data_remove_extra_point(rack_WINDOW):
    if rack_WINDOW is not None:
        if type(rack_WINDOW) == str:
            bbox_rw = rack_WINDOW
            try:
                split_data = bbox_rw.split(';')
                while '' in split_data:
                    split_data.remove('')
                if len(split_data) == 8:
                    x1 = split_data[0]
                    y1 = split_data[1]
                    x2 = split_data[2]
                    y2 = split_data[1]
                    x3 = split_data[4]
                    y3 = split_data[5]
                    x4 = split_data[0]
                    y4 = split_data[3]
                    final_string = str(x1) + ';' + str(y1) + ';' + str(x3) + ';' + str(y3) + ';'
                    rack_WINDOW = final_string
                else:
                    rack_WINDOW = rack_WINDOW
            except Exception as  error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- rw_data_remoddve_extra_point 1", str(error), " ----time ---- ", now_time_with_time()]))
    return rack_WINDOW

def rack_window_split(RACK_window_bboX):
    if RACK_window_bboX is not None:
        bbox_rw = RACK_window_bboX
        try:
            x_point = []
            y_point = []
            split_data = bbox_rw.split(';')
            while '' in split_data:
                split_data.remove('')
            x1 = split_data[0]
            y1 = split_data[1]
            x2 = split_data[2]
            y2 = split_data[1]
            x3 = split_data[2]
            y3 = split_data[3]
            x4 = split_data[0]
            y4 = split_data[3]
            final_string = str(x1) + ';' + str(y1) + ';' + str(x2) + ';' + str(y2) + ';' + str(x3) + ';' + str(y3) + ';' + str(x4) + ';' + str(y4) + ';'
            RACK_window_bboX = final_string
        except Exception as  error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- rack_wddindow_split 1", str(error), " ----time ---- ", now_time_with_time()]))
    return RACK_window_bboX


def rack_window_extrack_points_one_panel(rack_window_data):
    if len(rack_window_data) != 0:
        rack_image_ = []
        for ___, kkl in enumerate(rack_window_data):
            if isEmpty(kkl['roi_data']):
                if kkl['roi_data']['RW']:
                    RACK_window_bboX = kkl['roi_data']['RW']
                    kkl['roi_data']['RW'] = rack_window_split(RACK_window_bboX)
                    rack_image_.append(kkl)
                else:
                    print("rack_window_data['data']['panel_data']['roi_data']['RW']   EMPTY ")
                    rack_image_.append(kkl)
            else:
                print("rack_window_data['data']['panel_data']['roi_data']   EMPTY ")
                rack_image_.append(kkl)
        rack_window_data = rack_image_
    return rack_window_data


def rack_window_extrack_points(rack_window_data):
    try:
        if rack_window_data is not None:
            if rack_window_data['data'] is not None:
                if isEmpty(rack_window_data['data']):
                    if isEmpty(rack_window_data['data']['panel_data']):
                        if isEmpty(rack_window_data['data']['panel_data']['roi_data']):
                            if rack_window_data['data']['panel_data']['roi_data']['RW']:
                                RACK_window_bboX = rack_window_data['data']['panel_data']['roi_data']['RW']
                                rack_window_data['data']['panel_data']['roi_data']['RW'] = rack_window_split(RACK_window_bboX)
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- rack_window_extrack_poiddnts 1", str(error), " ----time ---- ", now_time_with_time()]))
    return rack_window_data


def get_panel_data1_check_bbox_in_empty_string(rack_window_data):
    if rack_window_data:
        final_list = []
        for j, k in enumerate(rack_window_data):
            if k['roi_data']:
                if k['roi_data']['bbox'] != '':
                    final_list.append(k)
            else:
                final_list.append(k)
        rack_window_data = final_list
    return rack_window_data


def check_bbox_in_empty_string(rack_window_data):
    final_list = []
    all_final_list = []
    for i in rack_window_data:
        if i['data']['panel_data']:
            if i['data']['panel_data']['roi_data']:
                if i['data']['panel_data']['roi_data']['bbox'] == '':
                    i['data']['panel_data'] = []
                    final_list.append(i)
                else:
                    final_list.append(i)
            else:
                final_list.append(i)
    for j in final_list:
        if type(j['data']['panel_data']) == list:
            if len(j['data']['panel_data']) != 0:
                all_final_list.append(j)
        else:
            all_final_list.append(j)
    return all_final_list

def image_roi_draw_data(image_data):
    if image_data is not None:
        if image_data['analyticstype'] == 'PPE_TYPE1':
            image_data['analyticstype'] = 'PPE'
            object_data = image_data['object_data']
            if len(object_data) != 0:
                final_object_data = []
                if len(object_data) == 1:
                    if object_data[0]['class_name'] == 'person':
                        if object_data[0]['Helmet'] == False:
                            del object_data[0]['tracking_id']
                            object_data[0]['violation_count']  = 'person ' + str(1)
                            final_object_data.append(object_data[0])
                        elif object_data[0]['Vest'] == 'no_ppe':
                            del object_data[0]['tracking_id']
                            object_data[0]['violation_count']  = 'person ' + str(1)
                            final_object_data.append(object_data[0])
                elif len(object_data) > 1:
                    person_count = 0
                    for ___, jjj in enumerate(object_data):
                        if jjj['class_name'] == 'person':
                            if jjj['Helmet'] == False:
                                del jjj['tracking_id']
                                jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                final_object_data.append(jjj)
                                person_count += 1
                            elif jjj['Vest'] == 'no_ppe':
                                del jjj['tracking_id']
                                jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                final_object_data.append(jjj)
                                person_count += 1
                if len(final_object_data) != 0:
                    image_data['object_data'] = final_object_data
                else:
                    image_data = final_object_data
        elif image_data['analyticstype'] == 'RA':
            object_data = image_data['object_data']
            if len(object_data) != 0:
                final_object_data = []
                if len(object_data) == 1:
                    if object_data[0]['violation'] == True:
                        if object_data[0]['class_name'] == 'person':
                            del object_data[0]['tracking_id']
                            object_data[0]['violation_count']  = 'person ' + str(1)
                            final_object_data.append(object_data[0])
                elif len(object_data) > 1:
                    person_count = 0
                    for ___, jjj in enumerate(object_data):
                        person_count = ___
                        if jjj['violation'] == True:
                            if jjj['class_name'] == 'person':
                                del jjj['tracking_id']
                                jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                final_object_data.append(jjj)
                image_data['object_data'] = final_object_data
    return image_data


@dashboard.route('/reset_jobsheet', methods=['GET'])
def RESETJOB_SHEET():
    ret = {'success': False, 'message':'something went wrong with reset_jobsheet api'}
    try:
        sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
        if len(sheet_data) != 0:
            think = 0
            app_run_response = esi_app_set_ESI_monitoring_started(True)
            for im, simin in enumerate(sheet_data):
                filters = {'_id': ObjectId(simin['_id'])}
                newvalues = {'$set':{'status': 0,'reset_time':now_time_with_time()}}
                result = mongo.db.job_sheet_details.update_one(filters, newvalues)
                if result.modified_count > 0:
                    think += 1
            if think > 0:
                ret = {'message':'job sheet status reset successfully , please try to upload new job sheet.', 'success': True}
            else:
                ret['message'] = 'job sheet status not reset, please try again.'
        else:
            ret['message'] = 'job sheet status not reset, please try again.'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- reset_jobsheet 1", str(error), " ----time ---- ", now_time_with_time()]))
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- reset_jobsheet 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret




# done for object
@dashboard.route('/sheet_ipaddress', methods=['GET'])
@dashboard.route('/sheet_ipaddress', methods=['POST'])
def sheet_ipaddress():
    ret = {'success': False, 'message':'something went wrong with get  details api'}
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if request.method == 'GET':
        if sheet_data is not None:
            match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
            data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
                                                        {'$group':{'_id':{'ipdata': '$data.ip_address'}, 'all_data':{'$first': '$$ROOT'}}},
                                                        {'$limit': 4000000}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    if isEmpty(i['all_data']['data']) :
                        # print("----------------------",i['all_data']['type'])
                        if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
                            if len(i['all_data']['data']['panel_data']) !=0  :
                                if i['all_data']['data']['ip_address']  not in dash_data:
                                    dash_data.append(i['all_data']['data']['ip_address'])

                        

                        elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
                            if 'hydraulic_data' in i['all_data']['data']:
                                if len(i['all_data']['data']['hydraulic_data']) !=0 :
                                    if i['all_data']['data']['ip_address']  not in dash_data:
                                        dash_data.append(i['all_data']['data']['ip_address'])

                        elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
                            if len(i['all_data']['data']['useal_data']) !=0 :
                                if i['all_data']['data']['ip_address']  not in dash_data:
                                    dash_data.append(i['all_data']['data']['ip_address'])
                if len(dash_data) != 0:
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
            else:
                ret['message'] = 'data not found'
        else:
            ret['message'] = 'job sheet is not uploaded yet'
    elif request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['department','job_no','type']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = keys_with_none_values(jsonobject) #[k for k, v in data.items() if v in ['', ' ', 'None'] ]
            if output:
                print(" something missing ",output)                
                query = {}                               
                if jsonobject['type'] is not None:
                    if jsonobject['type'] != ' ' and jsonobject['type'] != '':
                        query['type'] = jsonobject['type'] 
                if jsonobject['department'] is not None:
                    if jsonobject['department'] != ' ' and jsonobject['department'] != '':
                        query['department'] = jsonobject['department']
                        
                if jsonobject['job_no'] is not None:
                    if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
                        query['job_no']= jsonobject['job_no']
                print("query ====",query)
                ret = SORTIPADDRESS(query)
            else:
                department = jsonobject['department']
                query = {}  
                if jsonobject['type'] is not None:
                    if jsonobject['type'] != ' ' and jsonobject['type'] != '':
                        query['type'] = jsonobject['type'] 
                if jsonobject['department'] is not None:
                    if jsonobject['department'] != ' ' and jsonobject['department'] != '':
                        query['department'] = jsonobject['department']
                        
                if jsonobject['job_no'] is not None:
                    if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
                        query['job_no']= jsonobject['job_no']
                print("query ====",query)
                ret = SORTIPADDRESS(query)
                
        else:
            ret = {'success': False, 'message':  " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    else:
        ret['message'] = 'request type wrong, please try once again.'
    return jsonify(ret)





## done for object
@dashboard.route('/sheetDepartmentlist', methods=['GET'])
@dashboard.route('/sheetDepartmentlist', methods=['POST'])
def sheetDepar33dstmentlist():
    try:
        ret = {'success': False, 'message':'something went wrong with get  details api'}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
        if request.method == 'GET':
            
            if sheet_data is not None:
                match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
                data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
                                                           {'$group':{'_id': '$department', 'all_data':{'$first': '$$ROOT'}}},
                                                           {'$limit': 4000000}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if isEmpty(i['all_data']['data']):
                            if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
                                if len(i['all_data']['data']['panel_data']) !=0  :
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                else:
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])

                            elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
                                if 'hydraulic_data' in i['all_data']['data']:
                                    if len(i['all_data']['data']['hydraulic_data']) !=0 :
                                        if i['_id'] not in dash_data:
                                            dash_data.append(i['_id'])
                                    else:
                                        if i['_id']  not in dash_data:
                                            dash_data.append(i['_id'])

                            elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
                                if len(i['all_data']['data']['useal_data']) !=0 :
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                        
                                else:
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                
                    if len(dash_data) != 0:
                        ret = {'success': True, 'message': dash_data}
                    else:
                        ret['message'] = 'data not found'
                else:
                    ret['message'] = 'data not found'
            else:
                ret['message'] = 'job sheet is not uploaded yet'
        elif request.method == 'POST':
            jsonobject = request.json
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['job_no','type']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output =  keys_with_none_values(jsonobject)
                if output:
                    print(" something missing ",output)                
                    query = {}                
                    panel_data = {'panel_data':{"$elemMatch":[]}}                
                    if jsonobject['type'] is not None:
                        if jsonobject['type'] != ' ' and jsonobject['type'] != '':
                            query['type'] = jsonobject['type']                
                            
                    if jsonobject['job_no'] is not None:
                        if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
                            query['job_no']= jsonobject['job_no']
                    print("query ====",query)                  
                    
                    
                    ret = SORTDEPARTMENT(query)
                else:
                    job_no = jsonobject['job_no']                    
                    if sheet_data is not None:
                        # query = {}                              
                        # if jsonobject['type'] is not None:
                        #     if jsonobject['type'] != ' ' and jsonobject['type'] != '':
                        #         query['type'] = jsonobject['type']                
                                
                        # if jsonobject['job_no'] is not None:
                        #     if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
                        #         query['job_no']= jsonobject['job_no']
                        # ret = SORTDEPARTMENT(query)
                        if job_no is not None:
                            match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token'],'job_no':job_no}
                            data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
                                                                        {'$group':{'_id':{'ipdata': '$data.ip_address'}, 'all_data':{'$first': '$$ROOT'}}},
                                                                        {'$limit': 4000000}]))
                            dash_data = []
                            if len(data) != 0:
                                for count, i in enumerate(data):
                                    if isEmpty(i['all_data']['data']):
                                        if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
                                            if len(i['all_data']['data']['panel_data']) !=0  :
                                                if i['all_data']['department']  not in dash_data:
                                                    dash_data.append(i['all_data']['department'])
                                            else:
                                                if i['all_data']['department']  not in dash_data:
                                                    dash_data.append(i['all_data']['department'])

                                        elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
                                            if 'hydraulic_data' in i['all_data']['data']:
                                                if len(i['all_data']['data']['hydraulic_data']) !=0 :
                                                    if i['all_data']['department'] not in dash_data:
                                                        dash_data.append(i['all_data']['department'])
                                                else:
                                                    if i['all_data']['department']  not in dash_data:
                                                        dash_data.append(i['all_data']['department'])

                                        elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
                                            if len(i['all_data']['data']['useal_data']) !=0 :
                                                if i['all_data']['department']  not in dash_data:
                                                    dash_data.append(i['all_data']['department'])
                                                    
                                            else:
                                                if i['all_data']['department'] not in dash_data:
                                                    dash_data.append(i['all_data']['department'])
                                            
                                if len(dash_data) != 0:
                                    ret = {'success': True, 'message': dash_data}
                                else:
                                    ret['message'] = 'data not found'
                            else:
                                ret['message'] = 'data not found'
                        else:
                            ret['message'] = 'given job_no is none.'                            
                    else:
                        ret['message'] = 'job sheet is not uploaded yet'
            else:
                ret = {'success': False, 'message':  " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
                
        else:
            ret['message'] = 'request type wrong, please try once again.'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- sheetDepartmeeerntlist 1", str(error), " ----time ---- ", now_time_with_time()])) 
        ret['message' ] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")    
    except Exception as  error:
        ret = {'success': False, 'message': str(error)}
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- sheetDepeerartmentlist 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)


## done for object 
@dashboard.route('/listofjobtypes', methods=['GET'])
def JOBTYPESORTING():
    ret = {'success': False, 'message':'something went wrong with get  details api'}
    if request.method == 'GET':
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
            data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
                                                        {'$group':{'_id': '$type', 'all_data':{'$first': '$$ROOT'}}},
                                                        {'$limit': 4000000}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    # print("000000000000000000000000000000000000000000000000000&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&------",i)
                    if isEmpty(i['all_data']['data']) :
                        if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
                            if len(i['all_data']['data']['panel_data']) !=0  :
                                if i['_id']  not in dash_data:
                                    dash_data.append(i['_id'])
                            else:
                                if i['_id']  not in dash_data:
                                    dash_data.append(i['_id'])

                        elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
                            if 'hydraulic_data' in i['all_data']['data']:
                                if len(i['all_data']['data']['hydraulic_data']) !=0 :
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                else:
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])

                        elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
                            if len(i['all_data']['data']['useal_data']) !=0 :
                                if i['_id']  not in dash_data:
                                    dash_data.append(i['_id'])
                            else:
                                if i['_id']  not in dash_data:
                                    dash_data.append(i['_id'])
                    else:
                        if i['_id']  not in dash_data:
                            dash_data.append(i['_id'])

                if len(dash_data) != 0:
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
            else:
                ret['message'] = 'data not found'
        else:
            ret['message'] = 'job sheet is not uploaded yet'
    else:
        ret['message'] = 'request type wrong, please try once again.'
    return jsonify(ret)





#done for object 
@dashboard.route('/update_panel_roi_id', methods=['POST'])
def update_panel_roi_id__():
    ret = {'success': False, 'message':'something went wrong with get  api'}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['data']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            list_data = jsonobject['data']
            if isEmpty(list_data) :
                sheet_data = mongo.db.job_sheet_details.find_one({ 'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    id = list_data['id'] 
                    roi_data = list_data['roi_data']
                    image_name = list_data['image_name']
                    panel_key_id = list_data['panel_key_id']
                    panel_id = list_data['panel_id']
                    if id is not None:
                        if image_name is not None:
                            if panel_id is not None:
                                panel_find_data = (mongo.db.panel_data.find_one({'_id': ObjectId(id), 'data.image_name': image_name, 'data.panel_data.roi_data.panel_key_id': panel_key_id, 'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}))
                                if panel_find_data is not None:
                                    if isEmpty( panel_find_data[ 'data']) :
                                        data___ = []
                                        if panel_find_data[ 'data']['image_name'] == image_name:
                                            for __p, ioo in enumerate(panel_find_data[ 'data']['panel_data']):
                                                if ioo['panel_id'] != 'NA':
                                                    if ioo['roi_data']:
                                                        if (ioo['roi_data']['bbox'] != ''):
                                                            if ioo['roi_data']['unallocated_job_status'] == False:
                                                                #  if ioo['roi_data']['unallocated_job_status'] == False:
                                                                #         data___.append(ioo)
                                                                #     elif ioo['roi_data']['unallocated_job_status'] == True:
                                                                #         ioo['roi_data']['RW']=''
                                                                #         data___.append(ioo)
                                                                if (ioo['roi_data']['panel_key_id'] == panel_key_id):
                                                                    if roi_data['unallocated_job_status'] == False:
                                                                        (ioo['panel_id']) = (panel_id)
                                                                        if (roi_data['RW'] is not None):
                                                                            print(' --- type of rack window -- 1',type(roi_data['RW']))
                                                                            (roi_data['RW']) = (rw_data_remove_extra_point(roi_data['RW']))
                                                                        (ioo['roi_data']) = (roi_data)
                                                                    elif  roi_data['unallocated_job_status'] == True:
                                                                        roi_data['RW']=''
                                                                        (ioo['roi_data']) = (roi_data)
                                                                    data___.append(ioo)
                                                                else:
                                                                    data___.append(ioo)
                                                            elif ioo['roi_data']['unallocated_job_status'] == True:
                                                                ioo['roi_data']['RW']=''
                                                                data___.append(ioo)
                                                            
                                                elif ioo['panel_id'] == 'NA':
                                                    if ioo['roi_data']:
                                                        if (ioo['roi_data']['bbox'] != ''):
                                                            if ioo['roi_data']['unallocated_job_status'] == False:
                                                                if (ioo['roi_data']['panel_key_id'] ==panel_key_id):
                                                                    if roi_data['unallocated_job_status'] == False:
                                                                        (ioo['panel_id']) = (panel_id)
                                                                        if (roi_data['RW'] is not None):
                                                                            print(' --- type of rack window -- 2 ',type(roi_data['RW']))
                                                                            (roi_data['RW']) = (rw_data_remove_extra_point(roi_data['RW']))
                                                                        (ioo['roi_data']) = (roi_data)
                                                                    elif  roi_data['unallocated_job_status'] == True:
                                                                        roi_data['RW']=''
                                                                        (ioo['roi_data']) = (roi_data)
                                                                    data___.append(ioo)
                                                                else:
                                                                    data___.append(ioo)
                                                            elif ioo['roi_data']['unallocated_job_status'] == True:
                                                                ioo['roi_data']['RW']=''
                                                                data___.append(ioo)
                                            panel_find_data[ 'data']['panel_data']= data___
                                        filters = {'_id': ObjectId(id)}
                                        newvalues = {'$set':{'data': panel_find_data[ 'data']}}
                                        result = (mongo.db.panel_data.update_one(filters, newvalues))
                                        if (result.modified_count > 0):
                                            ret = {'message': 'panel roi is updated successfully.',  'success': True}
                                        else:
                                            (ret['message']) ='panel roi is not updated.'                                                    
                                    else:
                                        ret['message'] ='feeder data is not found.'
                                else:
                                    ret['message'] ='feeder data is not found.'
                            else:
                                ret['message'] ='panel id  should not be none.'
                        else:
                            ret['message'] ='image_name should not be none.'
                    else:
                        ret['message'] = 'id should not be none'   
                else:
                    ret['message'] = 'job sheet is not uploaded yet'
            else:
                ret['message'] = 'data should not be none'
    else:
        ret = {'success': False, 'message':  " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    return jsonify(ret)

## done for object 
@dashboard.route('/add_panel_roi_id', methods=['POST'])
def add_panel2232_roi_id__():
    ret = {'success': False, 'message':'something went wrong with get   api'}
    if 1:
    # try:
        # if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['data']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                list_data = jsonobject['data']
                if isEmpty(list_data) :
                    sheet_data = mongo.db.job_sheet_details.find_one({ 'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if sheet_data is not None:
                        RackwindowMODEL = os.path.join(os.getcwd() , 'Data_recieving_and_Dashboard','Rw_detection_yolo_v8_19_02_2024.onnx')
                        id = list_data['id']
                        roi_data = list_data['roi_data']
                        image_name = list_data['image_name']
                        panel_key_id = list_data['panel_key_id']
                        panel_id = list_data['panel_id']
                        final_data = []
                        if id is not None:
                            if image_name is not None:
                                if panel_id is not None:
                                    if panel_key_id is not None:
                                        panel_find_data = mongo.db.panel_data.find_one({'_id': ObjectId(id), 'data.image_name': image_name, 'job_sheet_name': sheet_data[ 'job_sheet_name'], 'token': sheet_data['token']})
                                        if panel_find_data is not None:
                                            panel_find_data_roi = panel_find_data[ 'data']
                                            check_key_id_status = False
                                            repeated_panelSTATUS = False
                                            if isEmpty(panel_find_data_roi):
                                                get_panel_key_id12=[]
                                                panelnumberLISTDATA= []
                                                get_panel_key_id12 = [ioo['roi_data']['panel_key_id'] for __p, ioo in enumerate(panel_find_data_roi['panel_data']) if ioo['roi_data']['panel_key_id']is not None]
                                                panelnumberLISTDATA = [ioo['panel_id'] for __p, ioo in enumerate(panel_find_data_roi['panel_data']) if ioo['panel_id']is not None]
                                                if panel_key_id not in get_panel_key_id12:
                                                    check_key_id_status = True
                                                if len(panel_find_data_roi['panel_data'])==0 :
                                                    check_key_id_status = True
                                                    repeated_panelSTATUS = True 
                                                if panel_id not in panelnumberLISTDATA:
                                                    repeated_panelSTATUS = True 
                                                print('panel keys ids ---- ', get_panel_key_id12)
                                                print("panel numbers ---", panelnumberLISTDATA)
                                            if check_key_id_status :
                                                if repeated_panelSTATUS:                                                   
                                                    data___ = []
                                                    # for ___, jjjk in enumerate(panel_find_data_roi):
                                                    panel_find_data_roi
                                                    if panel_find_data_roi['image_name'] == image_name:
                                                        get_panel_key_id = [ioo['roi_data']['panel_key_id'] for __p, ioo in enumerate(panel_find_data_roi['panel_data']) if ioo['panel_id'] != 'NA' or ioo['panel_id'] == 'NA']
                                                        if (panel_key_id is not get_panel_key_id):
                                                            if type(roi_data['RW']) == list:
                                                                #########################need-add-camera
                                                                if roi_data['unallocated_job_status'] == False:
                                                                    img_path = os.path.join(os.getcwd() , 'rtsp_roi_image',image_name) 
                                                                    GetNewrackwindow = extract_rw_bbox_details_cv2( roi_data['bbox'], img_path, RackwindowMODEL )
                                                                    if GetNewrackwindow is not None:
                                                                        roi_data['RW']=GetNewrackwindow
                                                                data___.append({'panel_id': panel_id,  'roi_data': roi_data,'panel_status': None,'isolation_status':None,"flasher_status":None})
                                                            else:
                                                                if roi_data['unallocated_job_status'] == False:

                                                                    (roi_data['RW']) = (rw_data_remove_extra_point(roi_data ['RW']))
                                                                data___.append({'panel_id': panel_id,     'roi_data': roi_data,   'panel_status': None,'isolation_status':None,"flasher_status":None})
                                                            for __PO, ioo in enumerate(panel_find_data_roi['panel_data']):
                                                                if ioo['roi_data']['unallocated_job_status'] == False:
                                                                    data___.append(ioo)
                                                                elif ioo['roi_data']['unallocated_job_status'] == True:
                                                                    ioo['roi_data']['RW']=''
                                                                    data___.append(ioo)
                                                                # data___.append(ioo)
                                                        else:
                                                            for __PO, ioo in enumerate(panel_find_data_roi[ 'panel_data']):
                                                                if ioo['roi_data']['unallocated_job_status'] == False:
                                                                    data___.append(ioo)
                                                                elif ioo['roi_data']['unallocated_job_status'] == True:
                                                                    ioo['roi_data']['RW']=''
                                                                    data___.append(ioo)
                                                                # data___.append(ioo)
                                                        panel_find_data_roi['panel_data'] = data___
                                                    filters = {'_id': ObjectId(id)}
                                                    newvalues = {'$set':{'data': panel_find_data_roi}}
                                                    result = (mongo.db.panel_data.update_one(filters, newvalues))
                                                    if (result.modified_count > 0):
                                                        ret = {'message':  'panel roi is updated successfully.',  'success': True}
                                                    else:
                                                        ret['message'] ='panel roi is not updated.'
                                                else:
                                                    ret['message']='entered panel number is already exist for same camera, please check.'
                                            else:
                                                ret['message'] = 'panel key id is already exists.'
                                        else:
                                            ret['message'] = 'feeder data is not found.'
                                    else:
                                        ret['message'] = 'panel key id should not be None'
                                else:
                                    ret['message'] = 'panel id  should not be none.'
                            else:
                                ret['message'] = 'image_name should not be none.'
                        else:
                            ret['message'] = 'id should not be none'
                    else:
                        ret['message'] = 'job sheet is not uploaded yet'
                else:
                    ret['message'] = 'data should not be none'
        else:
            ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])}
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panel_erroroi_id 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret = {'success': False, 'message': str(error)}
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panel_erroroi_id 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)

@dashboard.route('/excel_download', methods=['GET'])
def excel_result():
    try:
        list_of_files = glob.glob(os.path.join(os.getcwd(), "ESI_MONITORING_SHEETS/*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        path, filename = os.path.split(latest_file)
        if filename:
            main_path = os.path.abspath(path)
            response = make_response(send_from_directory(main_path, filename, as_attachment=True, download_name=filename))
            response.headers['Excel_filename'] = filename
            return response
        else:
            return {'success': False, 'message': 'File is not found.'}
    except (NameError, RuntimeError, FileNotFoundError, AssertionError,
        AttributeError, EOFError, FloatingPointError, TypeError,
        GeneratorExit, IndexError, KeyError, KeyboardInterrupt, MemoryError,
        NotImplementedError, OSError, OverflowError, ReferenceError,
        StopIteration, SyntaxError, IndentationError, TabError, SystemError,
        SystemExit, TypeError, UnboundLocalError, UnicodeError,
        UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError,
        ValueError, ZeroDivisionError, ConnectionError, KeyboardInterrupt,
        BaseException, ValueError) as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- excel_download 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return {'success': False, 'message': str(error)}
        
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- excel_download 2", str(error), " ----time ---- ", now_time_with_time()])) 
        return {'success': False, 'message': str(error)}
    


@dashboard.route('/violation_excel_download', methods=['GET'])
def violation_excel_result():
    list_of_files = glob.glob(os.path.join(os.getcwd(), "violation_excel_sheets/*"))
    latest_file = max(list_of_files, key=os.path.getctime)
    path, filename = os.path.split(latest_file)
    if filename:
        main_path = os.path.abspath(path)
        response = make_response(send_from_directory(main_path, filename, as_attachment=True, download_name=filename))
        response.headers['Excel_filename'] = filename
        return response
        # return send_from_directory(main_path, filename,headers=headers)
    else:
        return {'success': False, 'message': 'File is not found.'}


def remove_empty_space_panels_from_db():
    if 1:
    # try:
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
            if len(data) != 0:
                for ios, check_empty_panel_data in enumerate(data):
                    final_data = []
                    final_data_data = check_empty_panel_data
                    final_panel_data_for_updating = []
                    if check_empty_panel_data['type']=='HT' or check_empty_panel_data['type']=='ht':
                        if isEmpty(check_empty_panel_data['data']):
                            # print("is_empty_bbox---",check_empty_panel_data)                            
                            if len(check_empty_panel_data['data']['panel_data']) != 0:                                
                                for jkkee, panel_is_empty_bbox in enumerate(check_empty_panel_data['data']['panel_data']):
                                    if isEmpty(panel_is_empty_bbox):
                                        if panel_is_empty_bbox['panel_id'] != 'NA':
                                            if isEmpty(panel_is_empty_bbox['roi_data']):
                                                if panel_is_empty_bbox['roi_data']['bbox'] != '':
                                                    final_panel_data_for_updating.append(panel_is_empty_bbox)
                                # if len(final_panel_data_for_updating) != 0:
                                #     final_data_data['data']['panel_data'] = final_panel_data_for_updating
                                # else:
                                #     final_data_data['data']['panel_data'] = []
                            id = check_empty_panel_data['_id']
                            result = mongo.db.panel_data.update_one({'_id':ObjectId(id)}, {'$set':{'data.panel_data': final_panel_data_for_updating}})
                            if result.matched_count > 0:
                                pass

    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- remove_empty22_space_panels_from_db 2", str(error), " ----time ---- ", now_time_with_time()]))         
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- remove_empt22y_space_panels_from_db 2", str(error), " ----time ---- ", now_time_with_time()])) 

def remove_delete_panels_from_db(data, image_name, panel_no,panel_key_id):
    panel_delete_return_value = False
    #try:
    if 1:
        if data is not None:
            if data['type'] =='HT' or data['type'] =='ht':
                final_data = []
                if isEmpty(data['data']) :
                    if len(data['data']['panel_data']) != 0:
                        if data['data']['image_name'] == image_name:
                            final_panel_data_for_updating =[]
                            for jkkee, panel_is_empty_bbox in enumerate(data['data']['panel_data']):
                                if isEmpty(panel_is_empty_bbox):
                                    if panel_is_empty_bbox['panel_id'] != panel_no  and panel_is_empty_bbox['roi_data']['panel_key_id'] !=panel_key_id:
                                        if isEmpty(panel_is_empty_bbox['roi_data']):
                                            if panel_is_empty_bbox['roi_data']['bbox' ] != '':
                                                final_panel_data_for_updating.append(panel_is_empty_bbox)
                                    else:
                                        if panel_is_empty_bbox['panel_id'] == panel_no  and panel_is_empty_bbox['roi_data']['panel_key_id']==panel_key_id:
                                            print("outside condition ******************* db_panel_no",panel_is_empty_bbox['panel_id'])
                                            print('db panel key id ===',panel_is_empty_bbox['roi_data']['panel_key_id'])
                                            print("given panel key id ====", panel_key_id)
                                            pass
                                        else:
                                            if isEmpty(panel_is_empty_bbox['roi_data']):
                                                if panel_is_empty_bbox['roi_data']['bbox' ] != '':
                                                    final_panel_data_for_updating.append(panel_is_empty_bbox)
                            if len(final_panel_data_for_updating) != 0:
                                data['data']['panel_data']  = final_panel_data_for_updating
                            else:
                                data['data']['panel_data']  = []
                    id = data['_id']
                    result = mongo.db.panel_data.update_one({'_id': ObjectId(id)},{'$set':{'data': data['data']}})
                    if result.matched_count > 0:                        
                        panel_delete_return_value = True
                        # print("data====delete data===",data['data']['panel_data'])
                        # if len(data['data']['panel_data'])==0:
                        #     newresult = mongo.db.panel_data.delete_one({'_id': ObjectId(id)})                            
                        #     if newresult.deleted_count > 0:
                        #         print("panel_data is empty is detelting data.")                
                    else:
                        panel_delete_return_value = False
                else:
                    print("data is empty =====")
            else:
                print("other than ht data")
        else:
            print('feeder data not found  removing the empty panels 2---')
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- remove_delete_panels33_from_db 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- remove_delete_pan33els_from_db 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return panel_delete_return_value

def check_the_serial_number_and_rtsp_exist_in_database(data):
    print("serial number===function entered ")
    job_no = 0
    serial_number = []
    if len(data) != 0:        
        for __, inser in enumerate(data):
            if type(inser['job_no']) ==int :
                inser['job_no'] =str(inser['job_no'] )
            serial_number.append(inser['job_no'])
        serial_number.sort(key = float)
        # serial_number.sort()
        print('serial_number ==',serial_number)  
        if len(serial_number) !=0:
            job_no = int(float(serial_number[-1]))
    print("serial_number=====",serial_number)
    return job_no


def check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(data, rtsp_url):
    ret = []
    diction = {}
    rtsp_status = True
    if len(data) != 0:
        for __, inser in enumerate(data):
            if isEmpty(inser['data']) :
                if inser['data']['rtsp_url'] is not None:
                    if inser['data']['rtsp_url'] == rtsp_url:
                        rtsp_status = False
                        diction['_id'] = inser['_id']
                        diction['image_name'] = inser['data']['image_name']
                        diction['rtsp_url'] = inser['data']['rtsp_url']
                        diction['new_job'] = False
                        ret = inser
                    else:
                        print('RTSP IS not equal -  checking the existing rtsp')
                else:
                    print('RTSP IS None -  checking the existing rtsp')
            else:
                print('data parameter is empty   --- checking the existing rtsp ')
    else:
        print('fe data is empty -- data not found  checking the existing rtsp')
    if rtsp_status:
        ret = []
    else:
        ret = [diction]
    return ret


def final_data_value_to_return(rtsp_exist):
    ret = []
    diction = {}
    rtsp_status = True
    if len(rtsp_exist) != 0:
        if type(rtsp_exist) == dict:
            if isEmpty(rtsp_exist['data']) :
                # founddata= mongo.db.panel_data.find_one({"token":rtsp_exist['token'],"data.rtsp_url":rtsp_exist['data']['rtsp_url']})
                # if founddata is not None :
                if rtsp_exist['data']['rtsp_url'] is not None:
                    rtsp_status = False
                    diction['_id'] = rtsp_exist['_id']
                    diction['image_name'] = rtsp_exist['data']['image_name']
                    diction['rtsp_url'] = rtsp_exist['data']['rtsp_url']
                    diction['new_job'] = True
                else:
                    print('RTSP IS None -  checking the existing rtsp')
            else:
                print('data parameter is empty array  --- checking the existing rtsp ')
        elif type(rtsp_exist) == list:
            for __, inser in enumerate(rtsp_exist):
                if isEmpty(inser['data']) :
                    # founddata= mongo.db.panel_data.find_one({"token":inser['token'],"data.rtsp_url":inser['data']['rtsp_url']})
                    # if founddata is not None:
                    if inser['data']['rtsp_url'] is not None:
                        rtsp_status = False
                        diction['_id'] = inser['_id']
                        diction['image_name'] = inser['data']['image_name']
                        diction['rtsp_url'] = inser['data']['rtsp_url']
                        diction['new_job'] = True
                    else:
                        print('RTSP IS None -  checking the existing rtsp')                    
                else:
                    print('data parameter is empty array  --- checking the existing rtsp ')
    else:
        print('panel data is empty -- data not found  checking the existing rtsp')
    if rtsp_status:
        ret = []
    else:
        ret = [diction]
    return ret


def ADDINGJOBUSINGIPFOREXISTINGONE(rtsp_exist):
    print("enter checking for data ===",rtsp_exist)
    ret = []
    diction = {}
    rtsp_status = True
    if len(rtsp_exist) != 0:
        #rtsp_exist['data']['rtsp_url']
        # founddata= mongo.db.panel_data.find_one({"token":rtsp_exist['token'],"data.rtsp_url":rtsp_exist['data']['rtsp_url']})
        # if founddata is not None:
        if isEmpty(rtsp_exist['data']) :
            if rtsp_exist['data']['rtsp_url'] is not None:                    
                rtsp_status = False
                diction['_id'] = rtsp_exist['_id']
                diction['image_name'] = rtsp_exist['data']['image_name']
                diction['rtsp_url'] = rtsp_exist['data']['rtsp_url']
                diction['new_job'] = True
            else:
                print('RTSP IS None -  checking the existing rtsp')            
        else:
            print('data parameter is empty array  --- checking the existing rtsp ')
    else:
        print('panel data is empty -- data not found  checking the existing rtsp')
    if rtsp_status:
        ret = []
    else:
        if 'new_job' in diction.keys():
            pass
        else:
            diction['new_job']=False
        ret = [diction]
    return ret





def NEWCOOLLNNECXT__RTSPADDED(rtsp_exist):
    ret = []
    diction = {}
    rtsp_status = True
    if len(rtsp_exist) != 0:
        if type(rtsp_exist) == dict:
            if isEmpty(rtsp_exist['data']) :
                founddata= mongo.db.panel_data.find_one({"token":rtsp_exist['token'],"data.rtsp_url":rtsp_exist['data']['rtsp_url']},sort=[('_id', pymongo.DESCENDING)])
                if founddata is not None :
                    if founddata['data']['rtsp_url'] is not None:
                        rtsp_status = False
                        diction['_id'] = founddata['_id']
                        diction['image_name'] = founddata['data']['image_name']
                        diction['rtsp_url'] = founddata['data']['rtsp_url']
                        diction['new_job'] = True
                    else:
                        print('RTSP IS None -  checking the existing rtsp')
            else:
                print('data parameter is empty array  --- checking the existing rtsp ')
        elif type(rtsp_exist) == list:
            for __, inser in enumerate(rtsp_exist):
                if isEmpty(inser['data']) :
                    founddata= mongo.db.panel_data.find_one({"token":inser['token'],"data.rtsp_url":inser['data']['rtsp_url']},sort=[('_id', pymongo.DESCENDING)])
                    if founddata is not None:
                        if founddata['data']['rtsp_url'] is not None:
                            rtsp_status = False
                            diction['_id'] = founddata['_id']
                            diction['image_name'] = founddata['data']['image_name']
                            diction['rtsp_url'] = founddata['data']['rtsp_url']
                            diction['new_job'] = True
                        else:
                            print('RTSP IS None -  checking the existing rtsp')                    
                else:
                    print('data parameter is empty array  --- checking the existing rtsp ')
    else:
        print('panel data is empty -- data not found  checking the existing rtsp')
    if rtsp_status:
        ret = []
    else:
        ret = [diction]
    return ret


def NEWADDEDJOBWITHIP(rtsp_exist):
    print("_-------------------------------------new job ip -----------------************************")
    print("NEWJOB ENTEED _DATA IP ===",rtsp_exist)
    ret = []
    diction = {}
    rtsp_status = True
    if len(rtsp_exist) != 0:
        rtsp_exist['data']['rtsp_url']
        founddata= mongo.db.panel_data.find_one({"token":rtsp_exist['token'],"data.rtsp_url":rtsp_exist['data']['rtsp_url']},sort=[('_id', pymongo.DESCENDING)])
        if founddata is not None:
            if isEmpty(founddata['data']) :
                if founddata['data']['rtsp_url'] is not None:                    
                    rtsp_status = False
                    diction['_id'] = founddata['_id']
                    diction['image_name'] = founddata['data']['image_name']
                    diction['rtsp_url'] = founddata['data']['rtsp_url']
                    diction['new_job'] = True
                else:
                    print('RTSP IS None -  checking the existing rtsp')            
            else:
                print('data parameter is empty array  --- checking the existing rtsp ')
        else:
            print('data parameter is empty array  --- checking the existing rtsp ')
    else:
        print('panel data is empty -- data not found  checking the existing rtsp')
    if rtsp_status:
        ret = []
    else:
        if 'new_job' in diction.keys():
            pass
        else:
            diction['new_job']=False
        ret = [diction]
        
        
    print("final ---return value ============================",ret)
    return ret


@dashboard.route('/add_panel_rtsp', methods=['POST'])
def add_new_panel():
    ret = {'success': False, 'message':'something went wrong with add camera api with rtsp'}
    if 1:
    # try:
        job_no = 0
        
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['camera_brand',   'area','common_no', 'rtsp_url', 'job_description', 'no_of_isolating_points','type' , 'job_type','isolating_location']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                print("entered into =====missing rtsp ===1 ",output)
                if 'tagname' in output and 'board' in output:
                    print("entered into =====missing rtsp ===1.1 ",output)
                    jtype = data['type']
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        print("entered into =====missing rtsp ===1.1.0 ",output)
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                print("entered into =====missing rtsp ===1.1.1.0 ",output)
                                job_no = check_the_serial_number_and_rtsp_exist_in_database (panel_status_data)
                                rtsp_exist = check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url)
                                if len(rtsp_exist) != 0:
                                    ret = {'success': True, 'message': rtsp_exist}
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data['token'], 'common_no':common_no,'job_no': int(job_no)+1,   'sub_area': sub_area,
                                                                    'job_description': job_description, 'panel': "", 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                      'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                    'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                    'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                                                                                 
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message' ] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                print("entered into =====missing rtsp ===1.1.1.2 ",output)
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data['token'],'common_no':common_no, 'job_no': int(job_no)+1,  'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location, 'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data['timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board': board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                                                                               
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                elif 'tagname' in output :
                    print("entered into =====missing rtsp ===1.2.0 ",output)
                    jtype = data['type']
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                print("entered into =====missing rtsp ===1.2.1.0 ",output)
                                job_no = check_the_serial_number_and_rtsp_exist_in_database (panel_status_data)
                                rtsp_exist = check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url)
                                if len(rtsp_exist) != 0:
                                    ret = {'success': True, 'message': rtsp_exist}
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1,  'sub_area': sub_area,
                                                                    'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                     'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                    'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                    'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] = 'rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message' ] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] = 'camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] = 'rtsp video stream is not working please check with camera.'
                            else:
                                print("entered into =====missing rtsp ===1.2.1.1 ",output)
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no': int(job_no)+1, 'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location,'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board':board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] = 'rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                elif 'board' in output :
                    print("entered into =====missing rtsp ===1.3.0 ",output)
                    jtype = data['type']
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                print("entered into =====missing rtsp ===1.3.1.0 ",output)
                                job_no = (check_the_serial_number_and_rtsp_exist_in_database (panel_status_data))
                                rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                if len(rtsp_exist) != 0:
                                    ret = {'success': True, 'message': rtsp_exist}
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1, 'sub_area': sub_area,
                                                                    'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'ip_address': cameraip, 'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                    'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                    'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] = 'rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message' ] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] = 'camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                print("entered into =====missing rtsp ===1.3.2.0 ",output)
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no': int(job_no)+1,  'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location, 'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data['timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board':board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                else:          
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("entered into =====missing rtsp ===1.4.0 ",data)
                jtype = data['type']
                if  jtype !='HT' or jtype !='ht':
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']                
                    department = data['department']
                    job_type = data['job_type']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    tagname = None
                    board = None
                    if "tagname" in data:
                        if data['tagname'] is not None :
                            tagname = data['tagname']
                                                    
                    if "board" in data :
                        if data['board'] is not None:
                            board = data['board']
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                print("entered into =====missing rtsp ===1.4.1.0 ",data)
                                job_no = (check_the_serial_number_and_rtsp_exist_in_database (panel_status_data))
                                rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                if len(rtsp_exist) != 0:
                                    ret = {'success': True, 'message': rtsp_exist}
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            
                                            
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url':rtsp_url, #'rtsp_url': 'file://../../test_videos/hydra001.mp4',#rtsp_url,
                                                                       'rtsp_status': True,
                                                                    'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1,   'sub_area': sub_area,'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                     'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                    'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                    'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]    
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message' ] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                print("entered into =====missing rtsp ===1.4.1.1 ",data)
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1, 'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location,'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board': board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                else:
                    print("entered into =====missing rtsp ===1.4.4.0 ",data)
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    jtype = data['type']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                print("entered into =====missing rtsp ===1.4.4.1 ",data)
                                job_no = (check_the_serial_number_and_rtsp_exist_in_database (panel_status_data))
                                rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                if len(rtsp_exist) != 0:
                                    ret = {'success': True, 'message': rtsp_exist}
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {
                                                                    'ip_address': cameraip, 'camera_brand': brand, 'camera_id':None,
                                                                    'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True, 
                                                                    'image_name':rtsp_response_image['image_name'], 'image_size':{'height':rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []
                                                                    }
                                                        main_data = {
                                                                    'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1, 'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                    'no_of_isolating_points':no_of_isolating_points, 'isolating_location':isolating_location,  'video_names': None,'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department': department, 'board': board, 'tagname': tagname,'job_type':job_type,'remark':None
                                                                    }
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message' ] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                print("entered into =====missing rtsp ===1.4.4.1 ",data)
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 
                                                                'camera_name': cameraname,'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name':rtsp_response_image['image_name'],'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1, 'sub_area': sub_area,'job_description': job_description,'panel': '','no_of_isolating_points': no_of_isolating_points,'isolating_location': isolating_location, 'video_names': None,
                                                                 'ip_status': '','ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'job_sheet_name':sheet_data['job_sheet_name'],'sheet_status': True,'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data,'type': jtype, 'department': department, 'board': board,'tagname': tagname, 'job_type': job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]                                                          
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(final_data_value_to_return(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] = 'rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panel_rtsp 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panel_rtsp 2", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message']=" ".join(["something error has occered in api", str(error)])
    return parse_json(ret)





@dashboard.route('/add_panel_New_rtsp', methods=['POST'])
def add_PANEL_new_panel():
    ret = {'success': False, 'message':'something went wrong with add camera api with rtsp'}
    if 1:
    # try:
        job_no = 0
        
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['camera_brand',   'area','common_no', 'rtsp_url', 'job_description', 'no_of_isolating_points','type' , 'job_type','isolating_location']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                if 'tagname' in output and 'board' in output:
                    jtype = data['type']
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                job_no = check_the_serial_number_and_rtsp_exist_in_database (panel_status_data)
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data['token'], 'common_no':common_no,'job_no': int(job_no)+1,   'sub_area': sub_area,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'job_description': job_description, 'panel': "", 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                'ip_address': cameraip, 'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                    
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                                                                                
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data['token'],'common_no':common_no, 'job_no': int(job_no)+1,  'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location,
                                                                  'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data['timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board': board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                                                                               
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                elif 'tagname' in output :
                    jtype = data['type']
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                job_no = check_the_serial_number_and_rtsp_exist_in_database (panel_status_data)                                
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1,  'sub_area': sub_area,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                'ip_address': cameraip, 'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] = 'rtsp video stream is not working please check with camera.'
                            else:
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no': int(job_no)+1, 'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location, 'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board':board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] = 'rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                elif 'board' in output :
                    jtype = data['type']
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                job_no = (check_the_serial_number_and_rtsp_exist_in_database (panel_status_data))
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1, 'sub_area': sub_area,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                'ip_address': cameraip, 'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no': int(job_no)+1,  'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location, 'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data['timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board':board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                else:          
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                jtype = data['type']
                if  jtype !='HT' or jtype !='ht':
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']                
                    department = data['department']
                    job_type = data['job_type']
                    common_no = data['common_no']
                    tagname = None
                    board = None
                    if "tagname" in data:
                        if data['tagname'] is not None :
                            tagname = data['tagname']
                                                    
                    if "board" in data :
                        if data['board'] is not None:
                            board = data['board']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                job_no = (check_the_serial_number_and_rtsp_exist_in_database (panel_status_data))
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url':rtsp_url, #'rtsp_url': 'file://../../test_videos/hydra001.mp4',#rtsp_url,
                                                                    'rtsp_status': True,
                                                                'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1,   'sub_area': sub_area,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                'ip_address': cameraip, 'video_names': None, 'ip_status': {}, 'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype,'department': department, 
                                                                'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]    
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                'rtsp_url': rtsp_url, 'rtsp_status':True, 'image_name':rtsp_response_image['image_name'],
                                                                'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1, 'sub_area': sub_area,'job_description': job_description,'panel': '',
                                                                'no_of_isolating_points': no_of_isolating_points,'isolating_location':isolating_location,'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'video_names': None,'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'],
                                                                'sheet_status': True,'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data,'type': jtype, 
                                                                'department':department, 'board': board,'tagname': tagname, 'job_type':job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
                else:
                    rtsp_url = data['rtsp_url']
                    brand = data['camera_brand']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    jtype = data['type']
                    department = data['department']
                    job_type = data['job_type']
                    board = data['board']
                    tagname = data['tagname']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if rtsp_url is not None:
                        if sheet_data is not None:
                            panel_status_data = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(panel_status_data) != 0:
                                job_no = (check_the_serial_number_and_rtsp_exist_in_database (panel_status_data))
                                
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand,rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                if rtsp_response_image:
                                                    final_data = {
                                                                'ip_address': cameraip, 'camera_brand': brand, 'camera_id':None,
                                                                'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True, 
                                                                'image_name':rtsp_response_image['image_name'], 'image_size':{'height':rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []
                                                                }
                                                    main_data = {
                                                                'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1, 'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                'no_of_isolating_points':no_of_isolating_points, 'isolating_location':isolating_location, 'ip_address': cameraip, 'video_names': None,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                'data': final_data, 'type': jtype, 'department': department, 'board': board, 'tagname': tagname,'job_type':job_type,'remark':None
                                                                }
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] ='rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] ='camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                check_rtsp = check_rtsp_is_working(rtsp_url)
                                if check_rtsp:
                                    rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                    if rtsp_return_data:
                                        password = rtsp_return_data['password']
                                        cameraip = rtsp_return_data['ipaddress']
                                        username = rtsp_return_data['username']
                                        port = rtsp_return_data['port']
                                        cameraname = 'docketrun_'+ brand
                                        if cameraip is not None:
                                            cameraname = replace_spl_char_panel_area_plant(cameraip)
                                        if regex_pwd.search(password) == None:
                                            ping_response = True
                                            if ping_response:
                                                rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                if rtsp_response_image:
                                                    final_data = {'ip_address': cameraip,'camera_brand': brand, 'camera_id':None, 
                                                                'camera_name': cameraname,'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name':rtsp_response_image['image_name'],'image_size':{'height':rtsp_response_image['height'],'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                    main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1, 'sub_area': sub_area,'job_description': job_description,'panel': '','no_of_isolating_points': no_of_isolating_points,'isolating_location': isolating_location,  'video_names': None,'ip_status': '',
                                                                 'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                'job_sheet_name':sheet_data['job_sheet_name'],'sheet_status': True,'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data,'type': jtype, 'department': department, 'board': board,'tagname': tagname, 'job_type': job_type,'remark':None}
                                                    if type(main_data['data']) == list :
                                                        main_data['data'] = main_data['data'][0]                                                          
                                                    result = mongo.db.panel_data.insert_one(main_data)
                                                    if result.acknowledged:
                                                        ret = {'success': True, 'message':parse_json(NEWCOOLLNNECXT__RTSPADDED(main_data))}
                                                    else:
                                                        ret['message'] = 'data is not inserted properly, please try once again.'
                                                else:
                                                    ret['message'] = 'rtsp stream is not working, please try once again.'
                                            else:
                                                ret['message' ] = 'cameraip is not able ping.'
                                        else:
                                            ret['message'] = 'camera password should not have any special characters.'
                                    else:
                                        ret['message'] = 'rtsp url error.'
                                else:
                                    ret['message'] = 'rtsp video stream is not working please check with camera.'
                        else:
                            ret['message'] = 'job sheet is not yet uploaded'
                    else:
                        ret['message'] = 'rtsp url should not be none.'
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panel_rtsp 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panel_rtsp 2", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message']=" ".join(["something error has occered in api", str(error)])
    return parse_json(ret)



@dashboard.route('/add_panel_ip', methods=['POST'])
def add_new_panel_using_ip():
    job_no = 0
    ret = {'success': False, 'message':'something went wrong with add camera api with rtsp'}
    if 1:
    # try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['cameraip', 'username', 'type', "common_no",'department', 'job_type', 'password', 'port', 'camera_brand',  'area',  'job_description','no_of_isolating_points', 'isolating_location']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                print("missed parameters =while adding ip ---===",output)
                jtype = data['type']
                cameraip = data['cameraip']
                brand = data['camera_brand']
                username = data['username']
                password = data['password']
                port = data['port']
                sub_area = data['area']
                job_description = data['job_description']
                no_of_isolating_points = data['no_of_isolating_points']
                isolating_location = data['isolating_location']
                department = data['department']
                job_type = data['job_type']
                common_no = data['common_no']
                board = data['board']
                tagname = data['tagname']
                if 'tagname' in output and 'board' in output :
                    print("first condition is adding ip ===",output)
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------111",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                    if len(rtsp_exist) != 0:
                                        ret = {'success': True, 'message': rtsp_exist}
                                    else:
                                        check_rtsp = check_rtsp_is_working(rtsp_url)
                                        if check_rtsp:
                                            rtsp_return_data = split_rtsp_url(brand,
                                                rtsp_url)
                                            if rtsp_return_data:
                                                password = rtsp_return_data['password']
                                                cameraip = rtsp_return_data['ipaddress']
                                                cameraname = 'docketrun_'+ brand
                                                if cameraip is not None:
                                                    cameraname = replace_spl_char_panel_area_plant(cameraip)
                                                username = rtsp_return_data['username']
                                                port = rtsp_return_data['port']
                                                if regex_pwd.search(password) == None:
                                                    ping_response = True
                                                    if ping_response:
                                                        rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                        if rtsp_response_image:
                                                            final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                        'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                            main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                        'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,  'video_names': None, 'ip_status': {}, 
                                                                        'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                        'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 
                                                                        'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                            if type(main_data['data']) == list :
                                                                main_data['data'] = main_data['data'][0]                                                     
                                                            result = mongo.db.panel_data.insert_one(main_data)
                                                            if result.acknowledged:
                                                                ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                            else:
                                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                                        else:
                                                            ret['message'] ='rtsp stream is not working, please try once again.'
                                                    else:
                                                        ret['message'] ='cameraip is not able ping.'
                                                else:
                                                    ret['message'] ='camera password should not have any special characters.'
                                            else:
                                                ret['message'] = 'rtsp url error.'
                                        else:
                                            ret['message'] ='rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id':  None, 'camera_name': cameraname, 'rtsp_url': rtsp_url,
                                                                    'rtsp_status':True, 'image_name': rtsp_response_image['image_name'],
                                                                        'image_size':{'height':rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1,     'sub_area': sub_area, 'job_description': job_description,
                                                                    'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location':isolating_location,  'video_names': None, 'ip_status': {}, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                             
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'      
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                elif 'tagname' in output  :
                    print("second condition is adding ip ===",output)
                    board = data['board']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------222",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                    if len(rtsp_exist) != 0:
                                        ret = {'success': True, 'message':parse_json(rtsp_exist)}
                                    else:
                                        check_rtsp = check_rtsp_is_working(rtsp_url)
                                        if check_rtsp:
                                            rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                            if rtsp_return_data:
                                                password = rtsp_return_data['password']
                                                cameraip = rtsp_return_data['ipaddress']
                                                username = rtsp_return_data['username']
                                                port = rtsp_return_data['port']
                                                cameraname = 'docketrun_'+ brand
                                                if cameraip is not None:
                                                    cameraname = replace_spl_char_panel_area_plant(cameraip)
                                                if regex_pwd.search(password) == None:
                                                    ping_response = True
                                                    if ping_response:
                                                        rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                        if rtsp_response_image:
                                                            final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                        'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                            main_data = {'token': sheet_data['token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                        'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,  'video_names': None, 'ip_status': {}, 
                                                                        'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                        'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 
                                                                        'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                            if type(main_data['data']) == list :
                                                                main_data['data'] = main_data['data'][0]                                                           
                                                            result = mongo.db.panel_data.insert_one(main_data)
                                                            if result.acknowledged:
                                                                ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                            else:
                                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                                        else:
                                                            ret['message'] ='rtsp stream is not working, please try once again.'
                                                    else:
                                                        ret['message'] ='cameraip is not able ping.'
                                                else:
                                                    ret['message'] ='camera password should not have any special characters.'
                                            else:
                                                ret['message'] = 'rtsp url error.'
                                        else:
                                            ret['message'] ='rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                    'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name': rtsp_response_image['image_name'], 
                                                                    'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1,   'sub_area': sub_area, 'job_description': job_description,
                                                                    'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location':isolating_location, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'video_names': None, 'ip_status': {}, 'job_sheet_name':
                                                                    sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                           
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                elif  'board' in output  :
                    print("third condition is adding ip ===",output)
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------333",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                    if len(rtsp_exist) != 0:
                                        ret = {'success': True, 'message': rtsp_exist}
                                    else:
                                        check_rtsp = check_rtsp_is_working(rtsp_url)
                                        if check_rtsp:
                                            rtsp_return_data = split_rtsp_url(brand,
                                                rtsp_url)
                                            if rtsp_return_data:
                                                password = rtsp_return_data['password']
                                                cameraip = rtsp_return_data['ipaddress']
                                                username = rtsp_return_data['username']
                                                port = rtsp_return_data['port']
                                                cameraname = 'docketrun_'+ brand
                                                if cameraip is not None:
                                                    cameraname = replace_spl_char_panel_area_plant(cameraip)
                                                if regex_pwd.search(password) == None:
                                                    ping_response = True
                                                    if ping_response:
                                                        rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                        if rtsp_response_image:
                                                            final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                        'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                            main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no':  int(job_no)+1, 'sub_area': sub_area, 'job_description': job_description, 'panel':'',
                                                                        'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,  
                                                                        'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                        'video_names': None, 'ip_status': {}, 
                                                                        'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 
                                                                        'department':department, 'board': None, 'board': tagname, 'job_type':job_type,'remark':None}
                                                            if type(main_data['data']) == list :
                                                                main_data['data'] = main_data['data'][0]                                                           
                                                            result = mongo.db.panel_data.insert_one(main_data)
                                                            if result.acknowledged:
                                                                ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                            else:
                                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                                        else:
                                                            ret['message'] ='rtsp stream is not working, please try once again.'
                                                    else:
                                                        ret['message'] ='cameraip is not able ping.'
                                                else:
                                                    ret['message'] = 'camera password should not have any special characters.'
                                            else:
                                                ret['message'] = 'rtsp url error.'
                                        else:
                                            ret['message'] = 'rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,
                                            rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url ))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 
                                                                    'rtsp_status': True, 'image_name': rtsp_response_image['image_name'], 
                                                                    'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1,   'sub_area': sub_area, 'job_description': job_description,
                                                                    'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location':isolating_location, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                      'video_names': None, 'ip_status': {}, 'job_sheet_name':
                                                                    sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                                                                                 
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                else:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("normal condition is adding ip ===",data)
                jtype = data['type']
                if jtype !='HT' or jtype !='ht':
                    cameraip = data['cameraip']
                    brand = data['camera_brand']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    common_no = data['common_no']
                    tagname = None
                    board = None
                    if "tagname" in data:
                        if data['tagname'] is not None :
                            tagname = data['tagname']
                                                    
                    if "board" in data :
                        if data['board'] is not None:
                            board = data['board']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------444",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    rtsp_exist = (check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url))
                                    if len(rtsp_exist) != 0:
                                        ret = {'success': True, 'message': rtsp_exist}
                                    else:
                                        check_rtsp = check_rtsp_is_working(rtsp_url)
                                        if check_rtsp:
                                            rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                            if rtsp_return_data:
                                                password = rtsp_return_data['password']
                                                cameraip = rtsp_return_data['ipaddress']
                                                username = rtsp_return_data['username']
                                                port = rtsp_return_data['port']
                                                cameraname = 'docketrun_'+ brand
                                                if cameraip is not None:
                                                    cameraname = replace_spl_char_panel_area_plant(cameraip)
                                                if regex_pwd.search(password) == None:
                                                    ping_response = True
                                                    if ping_response:
                                                        rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                        if rtsp_response_image:
                                                            final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url':rtsp_url,
                                                                        'rtsp_status': True, 'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                            main_data = {'token': sheet_data['token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                         'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                          'no_of_isolating_points': no_of_isolating_points,
                                                                        'isolating_location':isolating_location,  'video_names': None, 'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                        'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                            if type(main_data['data']) == list :
                                                                main_data['data'] = main_data['data'][0]
                                                                                                                       
                                                            result = mongo.db.panel_data.insert_one(main_data)
                                                            if result.acknowledged:
                                                                ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                            else:
                                                                ret['message'] = 'data is not inserted properly, please try once again.'
                                                        else:
                                                            ret['message'] ='rtsp stream is not working, please try once again.'
                                                    else:
                                                        ret['message'] ='cameraip is not able ping.'
                                                else:
                                                    ret['message'] ='camera password should not have any special characters.'
                                            else:
                                                ret['message'] = 'rtsp url error.'
                                        else:
                                            ret['message'] ='rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 
                                                                    'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name':rtsp_response_image['image_name'],
                                                                    'image_size':{'height':rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 
                                                                    'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 
                                                                    'panel': '', 'no_of_isolating_points':no_of_isolating_points, 'isolating_location':isolating_location,
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                      'video_names': None, 'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'], 
                                                                    'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 'department':department,
                                                                    'board': data['board'], 'tagname': data['tagname'], 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                                                                                 
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                else:
                    print("normal condition is adding ip ===",data)
                    cameraip = data['cameraip']
                    brand = data['camera_brand']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    board = data['board']
                    tagname = data['tagname']
                    job_type = data['job_type']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("------555",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = check_the_serial_number_and_rtsp_exist_in_database(panel_status_data)
                                    rtsp_exist = check_the_serial_number_and_rtsp_exist_in_database_only_to_check_rtsp(panel_status_data, rtsp_url)
                                    if len(rtsp_exist) != 0:
                                        ret = {'success': True, 'message': rtsp_exist}
                                    else:
                                        check_rtsp = check_rtsp_is_working(rtsp_url)
                                        if check_rtsp:
                                            rtsp_return_data = split_rtsp_url(brand,
                                                rtsp_url)
                                            if rtsp_return_data:
                                                password = rtsp_return_data['password']
                                                cameraip = rtsp_return_data['ipaddress']
                                                username = rtsp_return_data['username']
                                                port = rtsp_return_data['port']
                                                cameraname = 'docketrun_'+ brand
                                                if cameraip is not None:
                                                    cameraname = replace_spl_char_panel_area_plant(cameraip)
                                                if regex_pwd.search(password) == None:
                                                    ping_response = True
                                                    if ping_response:
                                                        rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                        if rtsp_response_image:
                                                            final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                        'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                            main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': [],
                                                                        'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location, 
                                                                        'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                          'video_names': None, 'ip_status': {}, 
                                                                        'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype, 
                                                                        'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                            if type(main_data['data']) == list :
                                                                main_data['data'] = main_data['data'][0]
                                                               
                                                            print("newjob while adding ipaddress ----",)                                                        
                                                            result = mongo.db.panel_data.insert_one(main_data)
                                                            if result.acknowledged:
                                                                ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
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
                                            ret['message'] = 'rtsp video stream is not working please check with camera.'
                                else:
                                    print("comming in else condition for adding ip job")
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no': int(job_no)+1, 
                                                                     'sub_area': sub_area, 'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location, 
                                                                     'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                     'video_names': None, 'ip_status': {}, 
                                                                    'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                    'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,
                                                                    'department':department, 'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]      
                                                                                                                   
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(ADDINGJOBUSINGIPFOREXISTINGONE(main_data))}
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
                                        ret['message'] = 'rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_peeanel_ip 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #     ret['message']=" ".join(["something error has occered in api", str(error)])
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panssel_ip 2", str(error), " ----time ---- ", now_time_with_time()]))     
    return parse_json(ret)






@dashboard.route('/add_panelNew_ip', methods=['POST'])
def add_new_panel_Newusing_ip():
    job_no = 0
    ret = {'success': False, 'message':'something went wrong with add camera api with rtsp'}
    if 1:
    # try:
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['cameraip', 'username', 'type', "common_no",'department', 'job_type', 'password', 'port', 'camera_brand',  'area',  'job_description','no_of_isolating_points', 'isolating_location']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                print("missed parameters =while adding ip ---===",output)
                jtype = data['type']
                cameraip = data['cameraip']
                brand = data['camera_brand']
                username = data['username']
                password = data['password']
                port = data['port']
                sub_area = data['area']
                job_description = data['job_description']
                no_of_isolating_points = data['no_of_isolating_points']
                isolating_location = data['isolating_location']
                department = data['department']
                job_type = data['job_type']
                common_no = data['common_no']
                board =  data['board']
                tagname =  data['tagname']
                if 'tagname' in output and 'board' in output :
                    print("first condition is adding ip ===",output)
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------111",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,
                                            rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                    'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'video_names': None, 'ip_status': {}, 
                                                                    'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 
                                                                    'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                     
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] ='cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id':  None, 'camera_name': cameraname, 'rtsp_url': rtsp_url,
                                                                    'rtsp_status':True, 'image_name': rtsp_response_image['image_name'],
                                                                        'image_size':{'height':rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1,     'sub_area': sub_area, 'job_description': job_description,
                                                                    'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location':isolating_location, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'video_names': None, 'ip_status': {}, 'job_sheet_name':
                                                                    sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                             
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'      
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                elif 'tagname' in output  :
                    print("second condition is adding ip ===",output)
                    board = data['board']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------222",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data['token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': '',
                                                                    'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location, 
                                                                     'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand, 'video_names': None, 'ip_status': {}, 
                                                                    'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 
                                                                    'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                           
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] ='cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id':None, 'camera_name': cameraname,
                                                                    'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name': rtsp_response_image['image_name'], 
                                                                    'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1,   'sub_area': sub_area, 'job_description': job_description,
                                                                    'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location':isolating_location, 
                                                                     'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand, 'video_names': None, 'ip_status': {}, 'job_sheet_name':
                                                                    sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                           
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                elif  'board' in output  :
                    print("third condition is adding ip ===",output)
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------333",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,
                                            rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no':  int(job_no)+1, 'sub_area': sub_area, 'job_description': job_description, 'panel':'',
                                                                    'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,  
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,'video_names': None, 'ip_status': {}, 
                                                                    'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 
                                                                    'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]                                                           
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] ='cameraip is not able ping.'
                                            else:
                                                ret['message'] = 'camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] = 'rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,
                                            rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url ))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 
                                                                    'rtsp_status': True, 'image_name': rtsp_response_image['image_name'], 
                                                                    'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no':  int(job_no)+1,   'sub_area': sub_area, 'job_description': job_description,
                                                                    'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location':isolating_location,  
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'video_names': None, 'ip_status': {}, 'job_sheet_name':
                                                                    sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                                                                                 
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                else:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("normal condition is adding ip ===",data)
                jtype = data['type']
                if jtype !='HT' or jtype !='ht':
                    cameraip = data['cameraip']
                    brand = data['camera_brand']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    job_type = data['job_type']
                    common_no = data['common_no']
                    tagname = None
                    board = None
                    if "tagname" in data:
                        if data['tagname'] is not None :
                            tagname = data['tagname']
                                                    
                    if "board" in data :
                        if data['board'] is not None:
                            board = data['board']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("-------44new---4",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = (check_the_serial_number_and_rtsp_exist_in_database(panel_status_data))
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url':rtsp_url,
                                                                    'rtsp_status': True, 'image_name':rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data['token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points,
                                                                    'isolating_location':isolating_location, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                      'video_names': None, 'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'],
                                                                    'data': final_data, 'type': jtype, 'department':department, 'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                                                                                    
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                            print("================================while adding new job =================1111.0",ret)
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] ='cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                                else:
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = (VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url))
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 
                                                                    'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name':rtsp_response_image['image_name'],
                                                                    'image_size':{'height':rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 
                                                                    'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no':  int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 
                                                                    'panel': '', 'no_of_isolating_points':no_of_isolating_points, 'isolating_location':isolating_location, 
                                                                    'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                    'video_names': None, 'ip_status': {}, 'job_sheet_name':sheet_data['job_sheet_name'], 
                                                                    'sheet_status': True, 'job_sheet_time': sheet_data[ 'timestamp'], 'data': final_data, 'type': jtype, 'department':department,
                                                                    'board': data['board'], 'tagname': data['tagname'], 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                                                                                 
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
                                                        else:
                                                            ret['message'] = 'data is not inserted properly, please try once again.'
                                                    else:
                                                        ret['message'] ='rtsp stream is not working, please try once again.'
                                                else:
                                                    ret['message'] = 'cameraip is not able ping.'
                                            else:
                                                ret['message'] ='camera password should not have any special characters.'
                                        else:
                                            ret['message'] = 'rtsp url error.'
                                    else:
                                        ret['message'] ='rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
                else:
                    print("normal condition is adding ip ===",data)
                    cameraip = data['cameraip']
                    brand = data['camera_brand']
                    username = data['username']
                    password = data['password']
                    port = data['port']
                    sub_area = data['area']
                    job_description = data['job_description']
                    no_of_isolating_points = data['no_of_isolating_points']
                    isolating_location = data['isolating_location']
                    department = data['department']
                    board = data['board']
                    tagname = data['tagname']
                    job_type = data['job_type']
                    common_no = data['common_no']
                    regex_pwd = re.compile('[@!#$%^&*()<>?/\\|}{~:]')
                    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    channelNo = '1'
                    if regex_pwd.search(password) == None:
                        rtsp_url = create_rtsp_for_all_brand(cameraip, channelNo, username, password, brand, port)
                        print("------555",rtsp_url)
                        if rtsp_url is not None:
                            if sheet_data is not None:
                                panel_status_data = list(mongo.db.panel_data.find({ 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(panel_status_data) != 0:
                                    job_no = check_the_serial_number_and_rtsp_exist_in_database(panel_status_data)
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand,
                                            rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            cameraname = 'docketrun_'+ brand
                                            if cameraip is not None:
                                                cameraname = replace_spl_char_panel_area_plant(cameraip)
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True,
                                                                    'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'], 'common_no':common_no,'job_no': int(job_no)+1,  'sub_area': sub_area, 'job_description': job_description, 'panel': [],
                                                                    'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location,
                                                                      'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand, 
                                                                      'video_names': None, 'ip_status': {}, 
                                                                    'job_sheet_name': sheet_data['job_sheet_name'], 'sheet_status': True, 'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype, 
                                                                    'department':department, 'board': board, 'tagname': tagname, 'job_type':job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]
                                                            
                                                        print("newjob while adding ipaddress ----",)                                                        
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
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
                                        ret['message'] = 'rtsp video stream is not working please check with camera.'
                                else:
                                    print("comming in else condition for adding ip job")
                                    check_rtsp = check_rtsp_is_working(rtsp_url)
                                    if check_rtsp:
                                        rtsp_return_data = split_rtsp_url(brand, rtsp_url)
                                        if rtsp_return_data:
                                            password = rtsp_return_data['password']
                                            cameraip = rtsp_return_data['ipaddress']
                                            username = rtsp_return_data['username']
                                            port = rtsp_return_data['port']
                                            if regex_pwd.search(password) == None:
                                                ping_response = True
                                                if ping_response:
                                                    rtsp_response_image = VERIFYRTSPFOREXTRAPANELS(jtype,rtsp_url)
                                                    if rtsp_response_image:
                                                        final_data = {'ip_address': cameraip, 'camera_brand': brand, 'camera_id': None, 'camera_name': cameraname, 'rtsp_url': rtsp_url, 'rtsp_status': True, 'image_name': rtsp_response_image['image_name'], 'image_size':{'height': rtsp_response_image['height'], 'width': rtsp_response_image[ 'width']}, 'panel_data': []}
                                                        main_data = {'token': sheet_data[ 'token'],'common_no':common_no, 'job_no': int(job_no)+1, 
                                                                     'sub_area': sub_area, 'job_description': job_description, 'panel': '', 'no_of_isolating_points': no_of_isolating_points, 'isolating_location': isolating_location, 
                                                                      'ip_address': cameraip,'camera_username':username,'camera_password':password,'camera_brand':brand,
                                                                     'video_names': None, 'ip_status': {}, 
                                                                    'job_sheet_name':  sheet_data['job_sheet_name'], 'sheet_status': True,
                                                                    'job_sheet_time': sheet_data['timestamp'], 'data': final_data, 'type': jtype,
                                                                    'department':department, 'board': board, 'tagname': tagname, 'job_type': job_type,'remark':None}
                                                        if type(main_data['data']) == list :
                                                            main_data['data'] = main_data['data'][0]      
                                                                                                                   
                                                        result = mongo.db.panel_data.insert_one(main_data)
                                                        if result.acknowledged:
                                                            ret = {'success': True, 'message':parse_json(NEWADDEDJOBWITHIP(main_data))}
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
                                        ret['message'] = 'rtsp video stream is not working please check with camera.'
                            else:
                                ret['message'] = 'job sheet is not yet uploaded'
                        else:
                            ret['message'] = 'rtsp url should not be none.'
                    else:
                        ret['message' ] = ' camera password should not have any special characters.'
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_peeanel_ip 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #     ret['message']=" ".join(["something error has occered in api", str(error)])
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- add_panssel_ip 2", str(error), " ----time ---- ", now_time_with_time()]))     
    return parse_json(ret)

#done for the object
@dashboard.route('/delete_riro_data/<key_id>', methods=['GET'])
def delete_riro_data_key_id_wise(key_id=None):
    ret = {'message': 'something error occured in delte_riro_data.','success': False}
    try:
        if key_id is not None:
            find_delete_data = mongo.db.riro_data.find_one({'riro_key_id': key_id})
            if find_delete_data is not None:
                result = mongo.db.riro_data.delete_one({'_id': ObjectId(find_delete_data['_id'])})
                if result.deleted_count > 0:
                    ret = {'message': 'riro_data deleted successfully.','success': True}
                else:
                    ret['message'] ='riro_data is not deleted ,due to something went wrong with database.'
            else:
                ret['message' ] = '  riro_data is not found for this id, please try once again.'
        else:
            ret['message' ] = '  riro key id is None type please give proper riro key id.'
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



@dashboard.route('/deleteRemark/<key_id>', methods=['GET'])
def deleteRemark(key_id=None):
    ret = {'message': 'something error occured in delte_riro_data.','success': False}
    try:
        if key_id is not None:
            find_delete_data = mongo.db.riro_data.find_one({'riro_key_id': key_id})
            if find_delete_data is not None:
                result = mongo.db.riro_data.update_one({'_id': ObjectId(find_delete_data['_id'])},  {'$set': {"remarks":''}})
                if result.matched_count > 0:
                    ret = {'message': 'riro_data deleted successfully.','success': True}
                else:
                    ret['message'] ='riro_data is not deleted ,due to something went wrong with database.'
            else:
                ret['message' ] = '  riro_data is not found for this id, please try once again.'
        else:
            ret['message' ] = '  riro key id is None type please give proper riro key id.'
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

@dashboard.route('/edit_riro_data', methods=['POST'])
def edit_riro_data():
    ret = {'message': 'something error occured in edit_riro_data.','success': False}
    try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['data']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                data_122 = jsonobject['data']
                print('got data ------------------------ ', data_122)
                if isEmpty(data_122):
                    key_in_riro_data = ['riro_key_id', 'rack_process','rack_method', 'irrd_in_time', 'tag', 'lock', 'remarks','five_meter', 'barricading', 'magnetic_flasher']
                    if data_122['riro_key_id'] is not None:
                        if check_the_data_keys(key_in_riro_data, data_122.keys()):
                            print('all_input keys are there--- ')
                            print('the all items()', data_122.items())
                            checking_the_empty = [k for k, v in data_122.items() if v == '']
                            check_the_none_values = [k for k, v in data_122.
                                items() if v is None]
                            if len(checking_the_empty) == 0 and len(check_the_none_values) == 0:
                                find_edit_data = mongo.db.riro_data.find_one({ 'riro_key_id': data_122['riro_key_id']})
                                if find_edit_data is not None:
                                    # print('find_edit data ===', find_edit_data)
                                    try:
                                        if 'five_meter' in data_122.keys():
                                            data_122['five_meter'] = {'violation':data_122['five_meter']}
                                    except Exception as  error:
                                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- edit_riro_data 1", str(error), " ----time ---- ", now_time_with_time()]))
                                    print('final data updating -- data_122', type(data_122))
                                    data_122['riro_edit_status'] = True
                                    if dictionary_key_exists(data_122,'rack_process') and (dictionary_key_exists(data_122,'tag') or dictionary_key_exists(data_122,'lock') ):
                                        if data_122['rack_process']=='rack_out' and ((data_122['tag']=='untag') or (data_122['lock']=='unlock')):
                                            data_122['datauploadstatus']=0
                                    daata = data_122
                                    print('final data ==== ', daata)
                                    result = mongo.db.riro_data.update_one({ '_id': ObjectId(find_edit_data['_id'])},  {'$set': daata})
                                    print(result.matched_count)
                                    if result.matched_count > 0:
                                        ret = {'message': 'riro data updated successfully.','success': True}
                                    else:
                                        ret['message'] ='something went wrong updating the riro data.'
                                else:
                                    ret['message'] ='riro data is not found this riro key id, please try different key id.'
                            elif len(checking_the_empty) != 0 and len(check_the_none_values) != 0:
                                ret['message'] =('parameters are empty  {0} , and some parameters are none {1}'.format(checking_the_empty, check_the_none_values))
                            elif len(checking_the_empty) != 0:
                                ret['message']  = 'parameters are empty  {0}'.format(checking_the_empty)
                            elif len(check_the_none_values) != 0:
                                ret['message'] = 'parameters are none  {0}'.format(check_the_none_values)
                            else:
                                ret['message'] = 'parameters not matches.'
                        else:
                            print('----- all input keys are not there ')
                            ret['message'] =' all input keys are not there and should not be none, please give proper riro data.'
                    else:
                        ret['message'] ='riro key id should not be none, please give proper riro key id.'
                else:
                    ret['message' ] = '  riro edit data is empty, please give proper data.'
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- edit_riro_data 3", str(error), " ----time ---- ", now_time_with_time()]))        
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- edit_riro_data 3", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@dashboard.route('/delete_panel', methods=['POST'])
def delete_panel_while():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['panel_no', 'id', 'imagename','panel_key_id']
        print(jsonobject)
        print(type(jsonobject))
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                panel_no = jsonobject['panel_no']
                imagename = jsonobject['imagename']
                id = jsonobject['id']
                panel_key_id = jsonobject['panel_key_id']
                all_data = []
                if panel_no is not None:
                    if id is not None:
                        data = mongo.db.panel_data.find_one({'_id':ObjectId(id)})
                        if data is not None:
                            final_panel_data = None
                            return_value_for_delete_panel = remove_delete_panels_from_db(data, imagename, panel_no,panel_key_id)
                            if return_value_for_delete_panel:
                                ret = {'success': True, 'message':'panel deleted successfully'}
                            else:
                                ret['message'] = 'panel is not deleted.'
                        else:
                            ret['message'] = 'data not found'
                    else:
                        ret['message'] ='mongo id  should not be none, please enter the proper mongo id.'
                else:
                    ret['message'] ='panel number should not be none, please enter the proper panel data.'
        else:
            ret = {'message': 'parameters missing file {0}'.format(missing_key), 'success': False}
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     print("print(,)", str(error))
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_panel 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")     
    # except Exception as  error:
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_panel 2", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    return ret

############## most_repeate_functions
def check_ppe_violation_at_riro_moment(rtsp_url, panel_id, person_in_time,person_out_time):
    violation_test = False
    find_violation_data = list(mongo.db.data.find({'camera_rtsp': rtsp_url,'timestamp':{'$gte': person_in_time, '$lte': person_out_time},'violation_status': True}).sort('timestamp', -1))
    if len(find_violation_data) != 0:
        for olki, kl in enumerate(find_violation_data):
            for LILA, SHIVA in enumerate(kl['object_data']):
                if 'pannel_details' in SHIVA.keys():
                    if panel_id is not None and SHIVA['pannel_details'
                        ] is not None:
                        if panel_id in SHIVA['pannel_details']:
                            violation_test = True
                            break
    return violation_test


def check_the_riro_data(rtsp_url, panel_id, check_data):
    match_data = []
    violation_test = False
    panel_status = False
    panel_count = 0
    rack_process_list = []
    lock_list = []
    tag_list = []
    for zz, kiku in enumerate(check_data):
        if panel_id == kiku['panel_no']:
            panel_count += 1
            if kiku['rack_process'] is not None:
                if kiku['rack_process'] not in rack_process_list:
                    rack_process_list.append(kiku['rack_process'])
                if kiku['rack_process'] == 'rack_out':
                    if kiku['tag'] is not None and kiku['lock'] is not None:
                        if kiku['lock'] not in lock_list:
                            lock_list.append(kiku['lock'])
                        if kiku['tag'] not in tag_list:
                            tag_list.append(kiku['tag'])
            if kiku['rack_method'] == 'automatic':
                if kiku['irrd_in_time'] is not None and kiku['irrd_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                elif kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                riro_data_test_1 = {'sort_id': kiku['sort_id'], 'panel_no':kiku['panel_no'], 'rack_method': kiku['rack_method'],
                                    'rack_process': kiku['rack_process'], 'irrd_in_time':kiku['irrd_in_time'], 'irrd_out_time': kiku['irrd_out_time'],
                                    'tag': kiku['tag'], 'lock': kiku['lock'], 'tag_time': kiku['tag_time'], 'lock_time': kiku['lock_time'],
                                    'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher': kiku['magnetic_flasher'], 
                                    'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image': kiku['riro_merged_image'], 
                                    'riro_merged_image_size':kiku['riro_merged_image_size'], 'riro_edit_status': kiku['riro_edit_status'], 
                                    'lock_tag_image': kiku['cropped_panel_image_path'], 'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
            elif kiku['rack_method'] == 'manual':
                if kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                riro_data_test_1 = {'sort_id': kiku['sort_id'], 'panel_no': kiku['panel_no'], 'rack_method': kiku['rack_method'],
                                    'rack_process': kiku['rack_process'], 'irrd_in_time':kiku['person_in_time'], 'irrd_out_time': kiku['person_out_time'],
                                    'tag': kiku['tag'], 'lock': kiku['lock'], 'tag_time': kiku['tag_time'], 'lock_time':kiku['lock_time'], 
                                    'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher':kiku['magnetic_flasher'],
                                    'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image': kiku['riro_merged_image'], 
                                    'riro_merged_image_size':kiku['riro_merged_image_size'], 'riro_edit_status': kiku['riro_edit_status'], 
                                    'lock_tag_image': kiku['cropped_panel_image_path'], 'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
    if len(rack_process_list) != 0:
        rack_process_for_job = ['rack_out', 'rack_in']
        if rack_process_for_job == rack_process_list:
            panel_status = True
        elif 'rack_in' in rack_process_list:
            panel_status = True
    return match_data, panel_status


def with_campare_time_and_get_latest_data_of_riro(to_find_latest_data):
    temp = '0000-00-00 00:00:00'
    set_value = None
    for ooo, ter in enumerate(to_find_latest_data):
        if temp < ter['irrd_in_time']:
            temp = ter['irrd_in_time']
            set_value = ter
    return set_value



def riro_for_sorting(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    joinedlist = None
    try:
        for mix, i in enumerate(list_of_dict):
            if i['irrd_in_time'] is not None:
                time_stamp_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_(time_stamp_data)
            mongo_id_data = sort_job_sheet_time_sort_key_(mongo_id_data)
            joinedlist = time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            joinedlist = sort_irrd_time_(time_stamp_data)
        elif len(mongo_id_data) != 0:
            joinedlist = sort_job_sheet_time_sort_key_(mongo_id_data)
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_for_sorting 1", str(error), " ----time ---- ", now_time_with_time()]))
    return joinedlist


def check_the_riro_data_with_sorting(rtsp_url, panel_id, check_data):
    match_data = []
    violation_test = False
    panel_status = False
    panel_count = 0
    rack_process_list = []
    lock_list = []
    tag_list = []
    within_15_min = None
    for zz, kiku in enumerate(check_data):
        if panel_id == kiku['panel_no']:
            panel_count += 1
            if kiku['rack_process'] is not None:
                if kiku['rack_process'] not in rack_process_list:
                    rack_process_list.append(kiku['rack_process'])
                if kiku['rack_process'] == 'rack_out':
                    if kiku['tag'] is not None and kiku['lock'] is not None:
                        if kiku['lock'] not in lock_list:
                            lock_list.append(kiku['lock'])
                        if kiku['tag'] not in tag_list:
                            tag_list.append(kiku['tag'])
            if dictionary_key_exists(kiku,'within_15_min'):
                within_15_min = kiku['within_15_min']
            if kiku['rack_method'] == 'automatic':
                if kiku['irrd_in_time'] is not None and kiku['irrd_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['irrd_in_time'], kiku['irrd_out_time'])
                elif kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                riro_data_test_1 = {'panel_no': kiku['panel_no'],'rack_method': kiku['rack_method'], 'rack_process':
                    kiku['rack_process'], 'irrd_in_time': kiku['irrd_in_time'], 'irrd_out_time': kiku['irrd_out_time'],'tag': kiku['tag'], 'lock': kiku['lock'], 'tag_time':
                    kiku['tag_time'], 'lock_time': kiku['lock_time'],'five_meter': kiku['five_meter'], 'barricading': kiku['barricading'], 'magnetic_flasher': kiku['magnetic_flasher'], 'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image':
                    kiku['riro_merged_image'], 'riro_merged_image_size':
                    kiku['riro_merged_image_size'], 'riro_edit_status':
                    kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'within_15_min':within_15_min,'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
            elif kiku['rack_method'] == 'manual':
                if kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                riro_data_test_1 = {'panel_no': kiku['panel_no'],'rack_method': kiku['rack_method'], 'rack_process':
                    kiku['rack_process'], 'irrd_in_time': kiku['person_in_time'], 'irrd_out_time': kiku['person_out_time'], 'tag': kiku['tag'], 'lock': kiku['lock'], 'lock_time': kiku['lock_time'], 'tag_time':
                    kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher':
                    kiku['magnetic_flasher'], 'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image':
                    kiku['riro_merged_image'], 'riro_merged_image_size':
                    kiku['riro_merged_image_size'], 'riro_edit_status':
                    kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'within_15_min':within_15_min,'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
    if len(rack_process_list) != 0:
        print('rack process list --- ', rack_process_list)
        print('violation_test --- ', violation_test)
        print('tag_list', tag_list)
        print('lock_list', lock_list)
        rack_process_for_job = ['rack_out', 'rack_in']
        if rack_process_for_job == rack_process_list:
            panel_status = True
        elif 'rack_in' in rack_process_list:
            panel_status = True
    return riro_for_sorting(match_data), panel_status

def checking_panel_number_there_in_jobsheet_or_not_there(jobsheet_panels, panel_id):
    sheet_panel_status = True
    if len(jobsheet_panels) != 0:
        if len(jobsheet_panels) == 1:
            if panel_id in jobsheet_panels[0]:
                sheet_panel_status = False
        elif len(jobsheet_panels) > 1:
            for jum, jum1 in enumerate(jobsheet_panels):
                if panel_id in jum1:
                    sheet_panel_status = False
    else:
        sheet_panel_status = False
    return sheet_panel_status



@dashboard.route('/riro_all_jobs_data_by_panel_id', methods=['POST'])
def riro_all_jobs_data_by_panel_id():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['panel_no', 'id', 'imagename']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                panel_no = jsonobject['panel_no']
                imagename = jsonobject['imagename']
                id = jsonobject['id']
                all_data = []
                if panel_no is not None:
                    if id is not None:
                        data = mongo.db.panel_data.find_one({'_id': ObjectId(id)})
                        if data is not None:
                            final_panel_data = None
                            data = PANELWISERIRODATAFUNCTION(data)                            
                            for ___INNN, emmmi in enumerate(data):
                                if emmmi['data']['panel_data']['panel_id' ] is not None and emmmi['data']['panel_data']['panel_id'] == panel_no: 
                                    final_panel_data = emmmi
                            if final_panel_data is not None:
                                riro_return_data = []
                                find_riro_data = list(mongo.db.riro_data.find({ 'token': final_panel_data['token'],'camera_name': final_panel_data['data']['camera_name'],'camera_rtsp': final_panel_data['data']['rtsp_url'], 'panel_no': panel_no},sort=[('_id', pymongo.DESCENDING)]))
                                if len(find_riro_data) != 0:
                                    check_data, panel_status = (check_the_riro_data_with_sorting(final_panel_data['data']['rtsp_url'], final_panel_data['data']['panel_data']['panel_id'], find_riro_data))
                                    if panel_status or len(check_data) != 0:
                                        final_panel_data['data']['panel_data'][ 'panel_status'] = panel_status
                                        final_panel_data['riro_data'] = check_data
                                    else:
                                        check_data = [{'panel_no':final_panel_data['data'][ 'panel_data']['panel_id'],'rack_method': None, 
                                                       'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,'lock': None, 
                                                       'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,
                                                       'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                       'riro_merged_image_size':{'height':None, 'width': None},
                                                       'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
                                        final_panel_data['riro_data'] = check_data
                                    ret = {'message': final_panel_data,'success': True}
                                else:
                                    ret['message'] ='rackin rackout data is not for this panel, Please try again.'
                            else:
                                ret = {'message': 'panel data not found.','success': False}
                        else:
                            ret['message'] = 'data not found'
                    else:
                        ret['message'] ='mongo id  should not be none, please enter the proper mongo id.'
                else:
                    ret['message'] ='panel number should not be none, please enter the proper panel data.'
        else:
            ret = {'message': 'parameters missing file {0}'.format(missing_key), 'success': False}
    # except ( 
    #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #     pymongo.errors.WriteError) as error:
    #     print("print(,)", str(error))
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_all_jobs_data_by_ffpanel_id 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_all_jobs_ddddata_by_panel_id 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return ret


def riro_history_riro_for_sorting(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    joinedlist = []
    try:
        for mix, i in enumerate(list_of_dict):
            if i['irrd_in_time'] is not None:
                time_stamp_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_(time_stamp_data)
            mongo_id_data = sort_job_sheet_time_sort_key_(mongo_id_data)
            joinedlist = time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            joinedlist = sort_irrd_time_(time_stamp_data)
        elif len(mongo_id_data) != 0:
            joinedlist = sort_job_sheet_time_sort_key_(mongo_id_data)
    except Exception as  error:
        print('error --- ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_history_riro_for_sorting 1", str(error), " ----time ---- ", now_time_with_time()])) 
    return joinedlist


#not_recognised
def TWOELEMENTSOFRIRO(joinedlist):
    final_join_list = []
    if len(joinedlist) != 0:
        if len(joinedlist) == 1:
            final_join_list = joinedlist
        elif len(joinedlist) > 1:
            if joinedlist[1]['rack_process'] == joinedlist[0]['rack_process']:
                final_join_list.append(joinedlist[0])
            elif joinedlist[0]['rack_process']=='rack_in' and joinedlist[1]['rack_process'] =='rack_in':
                final_join_list.append(joinedlist[0])
            elif joinedlist[0]['rack_process']=='rack_out' and joinedlist[1]['rack_process'] =='rack_out':
                final_join_list.append(joinedlist[0])
            # elif joinedlist[0]['rack_process']=='rack_out' and joinedlist[1]['rack_process'] =='rack_out':
            #     final_join_list.append(joinedlist[0])
            elif joinedlist[0]['rack_process'] == 'rack_in':
                if joinedlist[1]['rack_process'] == 'rack_out':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                    # final_join_list.append(joinedlist[-1])
                elif joinedlist[1]['rack_process'] == 'maintenance':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'not_recognised':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
            elif joinedlist[0]['rack_process'] == 'not_recognised':
                if joinedlist[1]['rack_process'] == 'rack_out':
                    final_join_list.append(joinedlist[1])
                    final_join_list.append(joinedlist[0])
                    # final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'rack_in':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                    # final_join_list.append(joinedlist[-1])
                elif joinedlist[1]['rack_process'] == 'maintenance':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                    
                elif joinedlist[1]['rack_process'] == 'not_recognised':
                    final_join_list.append(joinedlist[0])
            elif joinedlist[0]['rack_process'] == 'rack_out':
                if joinedlist[1]['rack_process'] == 'not_recognised':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'rack_in':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                else:
                    final_join_list.append(joinedlist[0])
                    
                
            elif joinedlist[0]['rack_process'] == 'maintenance':
                if joinedlist[1]['rack_process'] == 'rack_out':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'rack_in':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'not_recognised':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
    if len(final_join_list)==2:
        if final_join_list[0]['rack_process'] == final_join_list[1]['rack_process']:
            final_join_list=[final_join_list[0]]
    return final_join_list

def riro_history_riro_for_sorting_only_two(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    joinedlist = []
    if 1:
    # try:
        for mix, i in enumerate(list_of_dict):
            if i['irrd_in_time'] is not None:
                time_stamp_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_(time_stamp_data)
            mongo_id_data = sort_job_sheet_time_sort_key_(mongo_id_data)
            joinedlist = time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            joinedlist = sort_irrd_time_(time_stamp_data)
        elif len(mongo_id_data) != 0:
            joinedlist = sort_job_sheet_time_sort_key_(mongo_id_data)
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_history_riro_for_sorting_55only_two 1", str(error), " ----time ---- ", now_time_with_time()])) 
    if len(joinedlist) != 0:
        joinedlist = TWOELEMENTSOFRIRO(joinedlist)
    return joinedlist


def check_the_rackout_process_(rack_process_list):
    panel_status = False
    if len(rack_process_list) != 0:
        if len(rack_process_list) == 1:
            if rack_process_list[0]['rack_process'] is not None:
                if rack_process_list[0]['rack_process'] == 'rack_out':
                    panel_status = False
                elif rack_process_list[0]['rack_process'] == 'rack_in':
                    panel_status = True
                elif rack_process_list[0]['rack_process'] == 'maintenance':
                    panel_status = False
        elif len(rack_process_list) > 1:
            if rack_process_list[0]['rack_process'] is not None:
                if rack_process_list[1]['rack_process'] is not None:
                    if rack_process_list[1]['rack_process'] == 'rack_in' and rack_process_list[0]['rack_process']=='rack_in':
                        panel_status = True
                    elif rack_process_list[1]['rack_process'] == rack_process_list[0]['rack_process']:
                        panel_status = False                    
                    elif rack_process_list[0]['rack_process'] == 'rack_out':
                        panel_status = False
                    elif rack_process_list[0]['rack_process'] == 'rack_in':
                        panel_status = True
                    elif rack_process_list[0]['rack_process'] == 'maintenance':
                        panel_status = False
    return panel_status


def riro_history_check_the_riro_data_with_sorting_(rtsp_url, panel_id, check_data):
    match_data = []
    within_15_min = None
    violation_test = False
    panel_status = False
    panel_count = 0
    rack_process_list = []
    lock_list = []
    tag_list = []
    for zz, kiku in enumerate(check_data):
        if panel_id == kiku['panel_no']:
            panel_count += 1
            if kiku['rack_process'] is not None:
                if kiku['rack_process'] not in rack_process_list:
                    rack_process_list.append(kiku['rack_process'])
                if kiku['rack_process'] == 'rack_out':
                    if kiku['tag'] is not None and kiku['lock'] is not None:
                        if kiku['lock'] not in lock_list:
                            lock_list.append(kiku['lock'])
                        if kiku['tag'] not in tag_list:
                            tag_list.append(kiku['tag'])
            if kiku['rack_method'] == 'automatic':
                if kiku['irrd_in_time'] is not None and kiku['irrd_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['irrd_in_time'], kiku['irrd_out_time'])
                elif kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                if dictionary_key_exists(kiku,'within_15_min'):
                    within_15_min = kiku['within_15_min']
                riro_data_test_1 = {'sort_id': kiku['_id'], 'panel_no': kiku['panel_no'], 'rack_method': kiku['rack_method'],'rack_process': kiku['rack_process'], 'irrd_in_time': kiku['irrd_in_time'], 'irrd_out_time': kiku['irrd_out_time'], 
                                    'tag': kiku['tag'], 'lock': kiku['lock'], 'lock_time': kiku['lock_time'], 'tag_time':kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'],
                                    'magnetic_flasher':kiku['magnetic_flasher'],'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image':kiku['riro_merged_image'], 'riro_merged_image_size': kiku['riro_merged_image_size'],
                                    'riro_edit_status':kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'within_15_min':within_15_min,'job_sheet_name':kiku['job_sheet_name'],
                                    'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
            elif kiku['rack_method'] == 'manual':
                if kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                if dictionary_key_exists(kiku,'within_15_min'):
                    within_15_min = kiku['within_15_min']
                riro_data_test_1 = {'sort_id': kiku['_id'], 'panel_no':kiku['panel_no'], 'rack_method': kiku['rack_method'],'rack_process': kiku['rack_process'], 
                                    'irrd_in_time':kiku['person_in_time'], 'irrd_out_time': kiku['person_out_time'], 'tag': kiku['tag'], 'lock': kiku['lock'],
                                    'lock_time': kiku['lock_time'], 'tag_time':kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'],
                                    'magnetic_flasher':kiku['magnetic_flasher'], 'violation': violation_test,'riro_key_id': kiku['riro_key_id'],
                                    'riro_merged_image': kiku['riro_merged_image'], 'riro_merged_image_size':kiku['riro_merged_image_size'], 'riro_edit_status':kiku['riro_edit_status'],
                                    'lock_tag_image': kiku['cropped_panel_image_path'],'within_15_min':within_15_min, 'job_sheet_name':kiku['job_sheet_name'],'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
    # if len(rack_process_list) != 0:
    #     rack_process_for_job = ['rack_out', 'rack_in']
    #     if rack_process_for_job == rack_process_list:
    #         panel_status = check_the_rackout_process_(match_data)
    #     elif 'rack_in' in rack_process_list:
    #         panel_status = True
    check_panel_status = riro_history_riro_for_sorting_only_two(match_data)
    return riro_history_riro_for_sorting_only_two(match_data), check_the_rackout_process_(check_panel_status), check_riro_edit_status(match_data)


def riro_live_data(live_riro_data):
    for index_no, live_form in enumerate(live_riro_data):
        check_data = [{'sort_id': live_form['_id'], 'panel_no': live_form['panel_no'], 'rack_method': None, 'rack_process': None,'irrd_in_time': None, 'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None, 'tag_time': None, 'five_meter': None, 'barricading': None, 'magnetic_flasher': live_form['magnetic_flasher'], 'violation': False, 'riro_key_id': None,'riro_merged_image': None, 'riro_merged_image_size':{'height':None, 'width': None}, 'riro_edit_status': False,'lock_tag_image': None, 'remarks': live_form['remarks']}]
    return check_data


def time_sort_key_for_history(d):
    return d['riro_data'][0]['irrd_in_time']


def sort_irrd_time_for_history(time_stamp_data):
    final_time_sort = sorted(time_stamp_data, key=time_sort_key_for_history,reverse=True)
    return final_time_sort


def riro_for_history(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    live_data = []
    joinedlist = None
    if 1:
    # try:
        for mix, i in enumerate(list_of_dict):
            if i['type'] == 'HT' or i['type'] == 'ht':
                if isEmpty((i['data'])) :
                    if len(i['data']['panel_data']) !=0:
                        if i['live_status']:
                            live_data.append(i)
                        elif i['riro_data'][0]['irrd_in_time'] is not None:
                            time_stamp_data.append(i)
                        else:
                            mongo_id_data.append(i)
                    else:
                        mongo_id_data.append(i)
                else:
                    mongo_id_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_for_history(time_stamp_data)
            joinedlist = live_data + time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            time_stamp_data = sort_irrd_time_for_history(time_stamp_data)
            joinedlist = live_data + time_stamp_data
        elif len(mongo_id_data) != 0:
            joinedlist = live_data + mongo_id_data
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_for_history 1", str(error), " ----time ---- ", now_time_with_time()])) 
    return joinedlist


def all_riro_final_sortin(final_test_sort):
    # new_final_test_riro = riro_for_history(final_test_sort)
    return riro_for_history(final_test_sort)


def isolation_camaparision_function(tagname):
    database_detail = {'sql_panel_table':'testopc', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrunopc', 'sslmode':'disable'}
    isolation_status =None
    conn = None
    if 1:
    # try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    # except Exception as  error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- isolation_camaparision_function 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY local_time desc')
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- isolation_camaparision_function 2", str(error), " ----time ---- ", now_time_with_time()])) 
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- isolation_camaparision_function 3", str(error), " ----time ---- ", now_time_with_time()])) 
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        for x_values, y_values in res.items():
            if type(y_values) == str:
                if x_values == tagname:
                    if y_values == '1':
                        isolation_status = 'isolated'
                    elif y_values == '2':
                        isolation_status = 'live'
                    elif y_values == '0':
                        isolation_status = 'unknown'
                    else:
                        isolation_status = 'unknown'
                    break
            elif type(y_values) == int:
                if x_values == tagname:
                    if y_values == 1:
                        isolation_status = 'isolated'
                    elif y_values == 2:
                        isolation_status = 'live'
                    elif y_values == 0:
                        isolation_status = 'unknown'
                    else:
                        isolation_status = 'unknown'
                    break
            elif type(y_values) == float:
                if x_values == tagname:
                    if int(y_values) == 1:
                        isolation_status = 'isolated'
                    elif int(y_values) == 2:
                        isolation_status = 'live'
                    elif int(y_values) == 0:
                        isolation_status = 'unknown'
                    else:
                        isolation_status = 'unknown'
                    break    
    return isolation_status

def check_magnetic_flasher_status(listOFdata):
    # print('------------------------listOFdata---',listOFdata)
    # print('000000000type----',type(listOFdata))
    all_data = []
    # print("length of the data====new sorted==",len(listOFdata))
    if listOFdata is not None:
        for index_number , data_element in enumerate(listOFdata):
            if isEmpty (data_element['data']):
                if data_element['type'] =='HT'  or   data_element['type'] =='ht' :
                    data_element['sticker_status_isolation'] = False
                    if len(data_element['data']['panel_data']) !=0:
                        if data_element['tagname'] is not None and data_element['tagname'] !='' :
                            if 1:
                            # try:
                                if data_element['isolation_status']=='live' and data_element['data']['panel_data']['isolation_status']=='live':
                                    data_element['exception_status']=True     
                                elif  data_element['isolation_status']=='live' and data_element['data']['panel_data']['isolation_status']=='isolated':
                                    data_element['exception_status']=True  
                                elif  data_element['isolation_status']=='isolated' and data_element['data']['panel_data']['isolation_status']=='isolated':
                                    data_element['exception_status']=False  
                                    data_element['sticker_status_isolation'] = True
                                elif  data_element['isolation_status']=='isolated' and data_element['data']['panel_data']['isolation_status']=='live':
                                    data_element['exception_status']=False  
                                    data_element['sticker_status_isolation'] = True
                                
                                elif  data_element['isolation_status']=='isolated' and data_element['data']['panel_data']['isolation_status']=='isolated':
                                    data_element['exception_status']=False  
                            # except Exception as  error :
                            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_magnetic33_flasher_status 1", str(error), " ----time ---- ", now_time_with_time()])) 
                            all_data.append(data_element)
                        else:
                            if 1:
                            # try :
                                if data_element['data']['panel_data']['flasher_status'] is not None:
                                    if data_element['data']['panel_data']['flasher_status']['status']=='no':
                                        data_element['isolation_status'] = 'live'
                                        if data_element['riro_data'][0]['magnetic_flasher'] is not None:
                                            data_element['riro_data'][0]['magnetic_flasher']=data_element['data']['panel_data']['flasher_status']
                                            data_element['exception_status']=True 
                                        else:
                                            data_element['riro_data'][0]['magnetic_flasher']=data_element['data']['panel_data']['flasher_status']
                                            data_element['exception_status']=True 
                                    elif data_element['data']['panel_data']['flasher_status']['status']=='yes':
                                        data_element['isolation_status'] = 'isolated'
                                        data_element['sticker_status_isolation'] = True
                                        data_element['riro_data'][0]['magnetic_flasher']= data_element['data']['panel_data']['flasher_status']

                                elif data_element['data']['panel_data']['flasher_status'] is None:
                                    if data_element['riro_data'][0]['magnetic_flasher']:
                                        if data_element['riro_data'][0]['magnetic_flasher']['status']=='no':
                                            data_element['isolation_status'] = 'live'
                                        elif data_element['riro_data'][0]['magnetic_flasher']['status']=='yes':
                                            data_element['isolation_status'] = 'isolated'
                            # except Exception as  error :
                            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_magnetic_33flasher_status 2", str(error), " ----time ---- ", now_time_with_time()]))
                            all_data.append(data_element)
                    else:
                        all_data.append(data_element)
                else:
                    all_data.append(data_element)
            else:
                all_data.append(data_element)
    return all_data






def check_the_hydralic_process_(rack_process_list):
    panel_status = False
    if len(rack_process_list) != 0:
        if len(rack_process_list) == 1:
            if rack_process_list[0]['lock_on_details'] is not None and rack_process_list[0]['lock_off_details'] is not None :
                panel_status = True
        elif len(rack_process_list) > 1:
            if rack_process_list[0]['lock_on_details'] is not None and rack_process_list[0]['lock_off_details'] is not None :
                panel_status = True
    return panel_status

def hydralockdataFetch(hydra_data):
    hydralic_status= False
    only_two_data =[]
    if hydra_data['type']=='hydraulic' or hydra_data['type']=='pneumatic' or hydra_data['type']=='Hydraulic' or hydra_data['type']=='Pneumatic':
        FINDHYDRADATA= list(mongo.db.hydra_data.find({'camera_rtsp':hydra_data['data']['rtsp_url'],"camera_name":hydra_data['data']['camera_name']}, sort=[('_id',   pymongo.DESCENDING)]))#.sort({"_id":1}).limit(1))#.sort({"_id":1}).limit(1)
        if len(FINDHYDRADATA) != 0 :
            newlist = sorted(FINDHYDRADATA, key=lambda d: d['_id']) 
            for u,i in enumerate(newlist):
                if u > 0:
                    break
                only_two_data.append(i)    
            hydralic_status = check_the_hydralic_process_(only_two_data)
    return only_two_data , hydralic_status       
          
        

@dashboard.route('/multiisolation', methods=['GET'])
@dashboard.route('/multiisolation/<id>', methods = ['GET'])
def multii44solation_convayor_pnumertic_hydralic23323(id = None):
    if 1:
    # try:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        sheet_data=None
        if id is not None:
            sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
        else:            
            sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])     
        if sheet_data is not None:
            data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0:# is not None:
                final_panel_data = []   
                data = MUPANRRILATION_multi_isolation(data)
                riro_final = []
                for ___INNN, emmmi in enumerate(data):
                    if (emmmi['type']=='HT' or emmmi['type']=='ht' ) :
                        if isEmpty(emmmi['data']) :
                            if (type(emmmi['data']['panel_data']) != list) :
                                if emmmi['data']['panel_data']['panel_id'] is not None:
                                    #list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url'], 'flasher_status':1, 'panel_no': emmmi['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                    show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url'], 'panel_no': emmmi['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                    
                                    if len(show_live_riro) != 0:
                                        show_live_riro = riro_live_data(show_live_riro)
                                        emmmi['riro_data'] = show_live_riro
                                        emmmi['riro_edit_status'] = False
                                        emmmi['live_status'] = True
                                        emmmi['sort_id'] = show_live_riro[0]['sort_id'] 
                                        if emmmi['tagname']  is not None and emmmi['tagname']  !='':
                                            emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
                                        else:
                                            emmmi['isolation_status'] = None
                                        emmmi['exception_status'] = False
                                        riro_final.append(emmmi)
                                    elif emmmi['data']['rtsp_url']:
                                        find_riro_data = list(mongo.db.riro_data.find({'token': emmmi['token'], 'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                                        if len(find_riro_data) != 0:
                                            (check_data, panel_status, riro_edit_status) = riro_history_check_the_riro_data_with_sorting_(emmmi['data']['rtsp_url'], emmmi['data']['panel_data']['panel_id'], find_riro_data)
                                            check_data = list(check_data)
                                            if panel_status or len(check_data) != 0:
                                                emmmi['data']['panel_data']['panel_status'] = panel_status
                                                emmmi['riro_data'] = check_data
                                                emmmi['riro_edit_status'] = riro_edit_status
                                                emmmi['live_status'] = False
                                                emmmi['sort_id'] = check_data[0]['sort_id']
                                                if emmmi['tagname']  is not None and emmmi['tagname']  !='':
                                                    emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
                                                else:
                                                    emmmi['isolation_status'] = None
                                                emmmi['exception_status'] = False
                                                riro_final.append(emmmi)
                                            else:
                                                check_data = [{'sort_id': None,'panel_no': emmmi['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
                                                                'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                                'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
                                                emmmi['riro_data'] = check_data
                                                emmmi['riro_edit_status'] = False
                                                emmmi['live_status'] = False
                                                emmmi['sort_id'] = None
                                                if emmmi['tagname']  is not None and emmmi['tagname']  !='':
                                                    emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
                                                else:
                                                    emmmi['isolation_status'] = None
                                                emmmi['exception_status'] = False
                                                riro_final.append(emmmi)
                                        else:
                                            check_data = [{'sort_id': None, 'panel_no':emmmi['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
                                                    'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
                                            emmmi['riro_data'] = check_data
                                            emmmi['riro_edit_status'] = False
                                            emmmi['live_status'] = False
                                            emmmi['sort_id'] = None
                                            if emmmi['tagname']  is not None and emmmi['tagname']  !='':
                                                emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
                                            else:
                                                emmmi['isolation_status'] = None
                                            emmmi['exception_status'] = False
                                            riro_final.append(emmmi)
                            else:
                                emmmi['riro_data'] = []
                                emmmi['riro_edit_status'] = False
                                emmmi['live_status'] = False
                                emmmi['sort_id'] = None
                                emmmi['isolation_status'] = None
                                emmmi['exception_status'] = False
                                riro_final.append(emmmi)
                        else:
                            emmmi['riro_data'] = []
                            emmmi['riro_edit_status'] = False
                            emmmi['live_status'] = False
                            emmmi['sort_id'] = None
                            emmmi['isolation_status'] = None
                            emmmi['exception_status'] = False
                            riro_final.append(emmmi)
                    elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                        hydata , panel_status = hydralockdataFetch(emmmi)
                        check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
                        emmmi['riro_data'] = check_data
                        emmmi['riro_edit_status'] = False
                        emmmi['live_status'] = False
                        emmmi['sort_id'] = None
                        emmmi['isolation_status'] = None
                        emmmi['exception_status'] = False
                        riro_final.append(emmmi)
                    else:
                        emmmi['riro_data'] = []
                        emmmi['riro_edit_status'] = False
                        emmmi['live_status'] = False
                        emmmi['sort_id'] = None
                        emmmi['isolation_status'] = None
                        emmmi['exception_status'] = False
                        riro_final.append(emmmi)
                        
                if len(riro_final) !=0:             
                    ret = {'message': check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final)) ),'success': True}
                    ret['job_sheet_status'] = True
                else:
                    ret = {'message': 'panel data not found.', 'success': False}
                    ret['job_sheet_status'] = True
            else:
                ret['message'] = 'panel data not found'
                ret['job_sheet_status'] = True
        else:
            ret['message'] ="jobsheet is not yet uploaded, please upload the jobsheet"

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
    # ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    # ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret



@dashboard.route('/SORTINGIPWISE/<ip_address>', methods=['GET'])
def SORTINGJOBSIPWISE(ip_address = None ):
    if 1:
    # try:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        sheet_data = None
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            if ip_address is not None:
                data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],"data.ip_address": ip_address}, sort=[('_id',   pymongo.DESCENDING)]))
                # print("data=====",len(data))
                if len(data) !=0 :
                    final_panel_data = []   
                    data = MUPANRRILATION_multi_isolation(data)
                    for ___INNN, emmmi in enumerate(data):
                        if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and emmmi['data']['panel_data']['panel_id'] is not None:
                            final_panel_data.append(emmmi)
                        elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                            final_panel_data.append(emmmi)
                    print("find panel data ====",len(final_panel_data) )
                    if len(final_panel_data) != 0:
                        riro_final = []
                        for i, each_panel in enumerate(final_panel_data):
                            if each_panel['type'] =='HT' or each_panel['type']=='ht':
                                show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status':1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(show_live_riro) != 0:
                                    show_live_riro = riro_live_data(show_live_riro)
                                    each_panel['riro_data'] = show_live_riro
                                    each_panel['riro_edit_status'] = False
                                    each_panel['live_status'] = True
                                    each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    each_panel['exception_status'] = False
                                    riro_final.append(each_panel)
                                elif each_panel['data']['rtsp_url']:
                                    find_riro_data = list(mongo.db.riro_data.find({'token': each_panel['token'], 'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                                    if len(find_riro_data) != 0:
                                        (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                        check_data = list(check_data)
                                        if panel_status or len(check_data) != 0:
                                            each_panel['data']['panel_data']['panel_status'] = panel_status
                                            each_panel['riro_data'] = check_data
                                            each_panel['riro_edit_status'] = riro_edit_status
                                            each_panel['live_status'] = False
                                            each_panel['sort_id'] = check_data[0]['sort_id']
                                            if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                            else:
                                                each_panel['isolation_status'] = None
                                            each_panel['exception_status'] = False
                                            riro_final.append(each_panel)
                                        else:
                                            check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
                                                        'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                        'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
                                            each_panel['riro_data'] = check_data
                                            each_panel['riro_edit_status'] = False
                                            each_panel['live_status'] = False
                                            each_panel['sort_id'] = None
                                            if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                            else:
                                                each_panel['isolation_status'] = None
                                            each_panel['exception_status'] = False
                                            riro_final.append(each_panel)
                                    else:
                                        check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
                                            'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
                                        each_panel['riro_data'] = check_data
                                        each_panel['riro_edit_status'] = False
                                        each_panel['live_status'] = False
                                        each_panel['sort_id'] = None
                                        if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                            each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                        else:
                                            each_panel['isolation_status'] = None
                                        each_panel['exception_status'] = False
                                        riro_final.append(each_panel)
                            else:
                                hydata , panel_status = hydralockdataFetch(each_panel)
                                check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
                                each_panel['riro_data'] = check_data
                                each_panel['riro_edit_status'] = False
                                each_panel['live_status'] = False
                                each_panel['sort_id'] = None
                                each_panel['isolation_status'] = None
                                each_panel['exception_status'] = False
                                riro_final.append(each_panel)

                        else:                        
                            ret = {'message': check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final))  ),'success': True}
                            ret['job_sheet_status'] = True
                    else:
                        ret = {'message': 'panel data not found.', 'success': False}
                        ret['job_sheet_status'] = True                
                else:
                    ret['message'] = 'panel data not found'
                    ret['job_sheet_status'] = True
            else:
                ret['message'] = 'ip address given none value, please try to send correct one.'
                ret['job_sheet_status'] = True
        else:
            ret['message'] = 'job sheet is not uploaded, please upload the jobsheet.'
            ret['job_sheet_status'] = False

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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGIPWISE 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGIPWISE 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret



def SRONPARAMETERSDEPARTMENTIPPANELNO(department=None, ip_address=None,panel_no=None):
    print("(parameterdata)", department,ip_address,panel_no)
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        sheet_data = None
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            if department is not None and ip_address is not None and panel_no is not None:
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],'department':department,"data.ip_address": ip_address,"data.panel_data":{"$elemMatch":{"panel_id": panel_no}}}, sort=[('_id',   pymongo.DESCENDING)])
            elif department is not None and ip_address is not None :
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],'department':department,"data.ip_address": ip_address}, sort=[('_id',   pymongo.DESCENDING)])
            elif department is not None  and panel_no is not None:
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],'department':department,"data.panel_data":{"$elemMatch":{"panel_id": panel_no}}}, sort=[('_id',   pymongo.DESCENDING)])
            elif ip_address is not None and panel_no is not None:
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],"data.ip_address": ip_address,"data.panel_data":{"$elemMatch":{"panel_id": panel_no}}}, sort=[('_id',   pymongo.DESCENDING)])
            elif department is not None :
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],'department':department}, sort=[('_id',   pymongo.DESCENDING)])
            elif  ip_address is not None :
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],"data.ip_address": ip_address}, sort=[('_id',   pymongo.DESCENDING)])
            elif  panel_no is not None :
                data = mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],"data.panel_data":{"$elemMatch":{"panel_id": panel_no}}}, sort=[('_id',   pymongo.DESCENDING)])
            else:
                ret['job_sheet_status']=True
                ret['message']='you have missed the input parameters.'
            data = list(data)
            if len(data) !=0 :
                final_panel_data = []   
                data = MUPANRRILATION_multi_isolation(data)
                for ___INNN, emmmi in enumerate(data):
                    if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and emmmi['data']['panel_data']['panel_id'] is not None:
                        final_panel_data.append(emmmi)
                    elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                        final_panel_data.append(emmmi)
                if len(final_panel_data) != 0:
                    riro_final = []
                    for i, each_panel in enumerate(final_panel_data):
                        if each_panel['type'] =='HT' or each_panel['type']=='ht':
                            show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status':1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(show_live_riro) != 0:
                                show_live_riro = riro_live_data(show_live_riro)
                                each_panel['riro_data'] = show_live_riro
                                each_panel['riro_edit_status'] = False
                                each_panel['live_status'] = True
                                each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                else:
                                    each_panel['isolation_status'] = None
                                each_panel['exception_status'] = False
                                riro_final.append(each_panel)
                            elif each_panel['data']['rtsp_url']:
                                find_riro_data = list(mongo.db.riro_data.find({'token': each_panel['token'], 'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                                if len(find_riro_data) != 0:
                                    (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                    check_data = list(check_data)
                                    if panel_status or len(check_data) != 0:
                                        each_panel['data']['panel_data']['panel_status'] = panel_status
                                        each_panel['riro_data'] = check_data
                                        each_panel['riro_edit_status'] = riro_edit_status
                                        each_panel['live_status'] = False
                                        each_panel['sort_id'] = check_data[0]['sort_id']
                                        if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                            each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                        else:
                                            each_panel['isolation_status'] = None
                                        each_panel['exception_status'] = False
                                        riro_final.append(each_panel)
                                    else:
                                        check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
                                                       'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                       'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
                                        each_panel['riro_data'] = check_data
                                        each_panel['riro_edit_status'] = False
                                        each_panel['live_status'] = False
                                        each_panel['sort_id'] = None
                                        if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                            each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                        else:
                                            each_panel['isolation_status'] = None
                                        each_panel['exception_status'] = False
                                        riro_final.append(each_panel)
                                else:
                                    check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
                                          'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
                                    each_panel['riro_data'] = check_data
                                    each_panel['riro_edit_status'] = False
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = None
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    each_panel['exception_status'] = False
                                    riro_final.append(each_panel)
                        else:
                            hydata , panel_status = hydralockdataFetch(each_panel)
                            check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
                            each_panel['riro_data'] = check_data
                            each_panel['riro_edit_status'] = False
                            each_panel['live_status'] = False
                            each_panel['sort_id'] = None
                            each_panel['isolation_status'] = None
                            each_panel['exception_status'] = False
                            riro_final.append(each_panel)
                    else:                      
                        ret = {'message': check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final))   ),'success': True}
                        ret['job_sheet_status'] = True
                else:
                    ret = {'message': 'panel data not found.', 'success': False}
                    ret['job_sheet_status'] = True
            else:
                ret['message'] = 'panel data not found'
                ret['job_sheet_status'] = True
        else:
            ret['job_sheet_status']=False
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'

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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SRONPARAMET11ERSDEPARTMENTIPPANELNO 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SRONPARAMETERSDEP111ARTMENTIPPANELNO 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


###done object
@dashboard.route('/SORTINGJOBSHEETDATA', methods=['POST'])
def JOSOIPDEPARTMPAL():
    ret = {'success': False, 'message':'something went wrong with SORTINGJOBSHEETDATA api'}
    data = request.json
    if data == None:
        data = {}
    if isEmpty(data):
        request_key_array = ['panel_no','ip_address','department']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '' or v == ' ' ]
            if output:
                print("camera_ip something missing ",output)
                if len(output)==2 and ('ip_address' in output  and "department" in output):
                    panel_no = data['panel_no']
                    department = None
                    ip_address= None
                    ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no) 
                elif len(output)==2 and ('panel_no' in output  and "department" in output):
                    panel_no = None
                    department = None
                    ip_address= data['ip_address']
                    ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no) 
                elif len(output)==2 and ('panel_no' in output  and "ip_address" in output):
                    panel_no = None
                    department = data['department']
                    ip_address= None
                    ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no) 
                elif len(output)==1 and ('panel_no' in output ):
                    panel_no = None
                    department = data['department']
                    ip_address= data['ip_address']
                    ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no) 
                elif len(output)==1 and ("ip_address" in output):
                    panel_no =data['panel_no']
                    department = data['department']
                    ip_address= None
                    ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no) 
                elif len(output)==1 and ( "department" in output):
                    panel_no = data['panel_no']
                    department = None
                    ip_address= data['ip_address']
                    ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no) 
                else:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])  
            else:
                panel_no = data['panel_no']
                ip_address = data['ip_address']
                department =data['department']
                ret = SRONPARAMETERSDEPARTMENTIPPANELNO(department,ip_address,panel_no)   
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    else:
        ret['message']="you have not given any parameters."  

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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGJOBSHEETDATA 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGJOBSHEETDATA 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


def SORTJOBS(Query):
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        data = []
        sheet_data = None
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            Query['job_sheet_name'] = sheet_data['job_sheet_name']
            Query['token'] = sheet_data['token']
            panel_no = None
            # print("sorkkkkkjob final query ---------",Query)
            if "panel_no" in Query:
                panel_no = Query['panel_no']
            elif 'data.panel_data.panel_id' in Query:
                panel_no = Query['data.panel_data.panel_id']
                print('--------------query_data',panel_no)
                # panel_no = Query['data.panel_data.panel_id']

            print('-------------------panel_no--------------',panel_no)
            data = list(mongo.db.panel_data.find(Query))
            # data = list(data)
            # print("data--length-----",len(data))

            if len(data) !=0 :
                final_panel_data = []   
                data = MUPANRRILATION_multi_isolation(data)
                if  panel_no is not None :
                    for ___INNN, emmmi in enumerate(data):
                        if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and  emmmi['data']['panel_data']['panel_id'] is not None:
                            if panel_no is not None :
                                if emmmi['data']['panel_data']['panel_id'] == panel_no : 
                                    final_panel_data.append(emmmi)
                        #     else:
                        #         final_panel_data.append(emmmi)
                        # elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                        #     final_panel_data.append(emmmi)
                else:
                    for ___INNN, emmmi in enumerate(data):
                        if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and  emmmi['data']['panel_data']['panel_id'] is not None:
                            if panel_no is not None :
                                if emmmi['data']['panel_data']['panel_id'] == panel_no : 
                                    final_panel_data.append(emmmi)
                            else:
                                final_panel_data.append(emmmi)
                        elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                            final_panel_data.append(emmmi)

                print('--------------final_panel_data------------------',len(final_panel_data))
                if len(final_panel_data) != 0:
                    riro_final = []
                    for i, each_panel in enumerate(final_panel_data):
                        if each_panel['type'] =='HT' or each_panel['type']=='ht':
                            if isEmpty(each_panel['data']) :
                                if len(each_panel['data']['panel_data']) !=0:
                                    show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status':1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                    if len(show_live_riro) != 0:
                                        show_live_riro = riro_live_data(show_live_riro)
                                        each_panel['riro_data'] = show_live_riro
                                        each_panel['riro_edit_status'] = False
                                        each_panel['live_status'] = True
                                        each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
                                        if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                            each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                        else:
                                            each_panel['isolation_status'] = None
                                        each_panel['exception_status'] = False
                                        riro_final.append(each_panel)
                                    elif each_panel['data']['rtsp_url']:
                                        find_riro_data = list(mongo.db.riro_data.find({'token': each_panel['token'], 'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                                        if len(find_riro_data) != 0:
                                            (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                            check_data = list(check_data)
                                            if panel_status or len(check_data) != 0:
                                                each_panel['data']['panel_data']['panel_status'] = panel_status
                                                each_panel['riro_data'] = check_data
                                                each_panel['riro_edit_status'] = riro_edit_status
                                                each_panel['live_status'] = False
                                                each_panel['sort_id'] = check_data[0]['sort_id']
                                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                                else:
                                                    each_panel['isolation_status'] = None
                                                each_panel['exception_status'] = False
                                                riro_final.append(each_panel)
                                            else:
                                                check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
                                                            'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                            'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
                                                each_panel['riro_data'] = check_data
                                                each_panel['riro_edit_status'] = False
                                                each_panel['live_status'] = False
                                                each_panel['sort_id'] = None
                                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                                else:
                                                    each_panel['isolation_status'] = None
                                                each_panel['exception_status'] = False
                                                riro_final.append(each_panel)
                                        else:
                                            check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
                                                'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
                                            each_panel['riro_data'] = check_data
                                            each_panel['riro_edit_status'] = False
                                            each_panel['live_status'] = False
                                            each_panel['sort_id'] = None
                                            if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                            else:
                                                each_panel['isolation_status'] = None
                                            each_panel['exception_status'] = False
                                            riro_final.append(each_panel)
                                else:
                                    each_panel['riro_data'] = []
                                    each_panel['riro_edit_status'] = False
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = None
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    each_panel['exception_status'] = False
                                    riro_final.append(each_panel)
                                
                        else:
                            hydata , panel_status = hydralockdataFetch(each_panel)
                            check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
                            each_panel['riro_data'] = check_data
                            each_panel['riro_edit_status'] = False
                            each_panel['live_status'] = False
                            each_panel['sort_id'] = None
                            each_panel['isolation_status'] = None
                            each_panel['exception_status'] = False
                            riro_final.append(each_panel)
                    else:                      
                        ret = {'message': check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final))   ),'success': True}
                        ret['job_sheet_status'] = True
                else:
                    ret = {'message': 'panel data not found.', 'success': False}
                    ret['job_sheet_status'] = True
            else:
                ret['message'] = 'panel data not found'
                ret['job_sheet_status'] = True
        else:
            ret['job_sheet_status']=False
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'

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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SRONPARAMETERS222222222333222222222222222222DEPARTMENTIPPANELNO 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SRONPARAMETERS22233222222222222222222222222DEPARTMENTIPPANELNO 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret





def SORTDEPARTMENT(Query):
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            Query['job_sheet_name'] = sheet_data['job_sheet_name']
            Query['token'] = sheet_data['token']
            panel_no = None
            if "panel_no" in Query:
                panel_no = Query['panel_no']
            print("final_query_of-SORTDEPARTMENT",Query)
            data = list(mongo.db.panel_data.find(Query))
            final_panel_data = [] 
            print("data---length ====",len(data))
            if len(data) !=0 :
                for i, departmentname in enumerate(data):
                    if departmentname['department'] not in final_panel_data:
                        final_panel_data.append(departmentname['department'])
                if len(final_panel_data) !=0:
                    ret['message']=final_panel_data
                    ret['success']=True      
            else:
                ret['message'] = 'panel data not found'
        else:
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'
    return ret
            


def SORTIPADDRESS(Query):
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        data = []
        sheet_data = None
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            Query['job_sheet_name'] = sheet_data['job_sheet_name']
            Query['token'] = sheet_data['token']
            panel_no = None
            if "panel_no" in Query:
                panel_no = Query['panel_no']
            data = list(mongo.db.panel_data.find(Query))
            final_panel_data = [] 
            if len(data) !=0 :
                for i, IPaddress in enumerate(data):
                    if IPaddress['data']['ip_address']  not in final_panel_data:
                            final_panel_data.append(IPaddress['data']['ip_address'])
                    # if departmentname['department'] not in final_panel_data:
                    #     final_panel_data.append(departmentname['department'])
                if len(final_panel_data) !=0:
                    ret['message']=final_panel_data
                    ret['success']=True      
            else:
                ret['message'] = 'ipaddress list is not found for given details.'
        else:
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'
    return ret

   


# def keys_with_empty_values(dictionary):
#     return [key for key, value in dictionary.items() if value in ('', None,'None', ' ',False)]
def keys_with_none_values(dictionary):
    return [key for key, value in dictionary.items() if value is None]

@dashboard.route('/SORTINGBYJOBTYPE', methods=['POST'])
def JOSOIPJOBTYPEDEPARTMPAL1():
    ret = {'success': False, 'message':'something went wrong with SORTINGJOBSHEETDATA api'}
    data = request.json
    print("-----data",data)
    if data == None:
        data = {}
    if isEmpty(data):
        print("entered =====",data )
        request_key_array = ['panel_no','ip_address','department','type','job_no']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            print("adfaksdddddddddkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk111--------------------------------")
            output = keys_with_none_values(data) #[k for k, v in data.items() if v in ['', ' ', 'None'] ]
            if output:
                print(" something missing ",output)                
                query = {}                
                panel_data = {'panel_data':{"$elemMatch":[]}}                
                if data['type'] is not None:
                    if data['type'] != ' ' and data['type'] != '':
                        query['type'] = data['type']                
                if data['ip_address'] is not None:
                    if data['ip_address'] != ' ' and data['ip_address'] != '' :
                        query['data.ip_address'] = data['ip_address']
                if data['department'] is not None:
                    if data['department'] != ' ' and data['department'] != '':
                        query['department'] = data['department']
                if data['panel_no'] is not None:
                    if data['panel_no'] != '' and  data['panel_no'] != ' ':
                        # panel_data['panel_data']["$elemMatch"]= data['panel_no']
                        # query['data.panel_data.$elemMatch']= data['panel_no']
                        # if data['panel_no'] != '' and  data['panel_no'] != ' ':
                        # query['data']['panel_data']["$elemMatch"]= data['panel_no']
                        # query['data.panel_data'] = {"$elemMatch":{     '$eq': data['panel_no']    } }
                        # {  'data.panel_data.panel_id': '5'}
                        query['data.panel_data.panel_id']=data['panel_no']
                        
                if data['job_no'] is not None:
                    if data['job_no'] != '' and  data['job_no'] != ' ':
                        query['job_no']= data['job_no']
                print("query ==JOSOIPJOBTYPEDEPA4444----RTMPAL1 ==",query)
                ret = SORTJOBS(query)
            else:
                panel_no = data['panel_no']
                ip_address = data['ip_address']
                department =data['department']
                jobtype = data['type']
                job_no = data['job_no']
                print('all parameters had given===',data)
                query = {}                
                panel_data = {'panel_data':{"$elemMatch":[]}}                
                if data['type'] is not None:
                    if data['type'] != ' ' and data['type'] != '':
                        query['type'] = data['type']                
                if data['ip_address'] is not None:
                    if data['ip_address'] != ' ' and data['ip_address'] != '' :
                        query['data.ip_address'] = data['ip_address']
                if data['department'] is not None:
                    if data['department'] != ' ' and data['department'] != '':
                        query['department'] = data['department']
                if data['panel_no'] is not None:
                    if data['panel_no'] != '' and  data['panel_no'] != ' ':
                        # query['data']['panel_data']["$elemMatch"]= data['panel_no']
                        # query['data'] = {"panel_data":{"$elemMatch":{     '$eq': data['panel_no']    } }}
                        #query['data.panel_data'] = {"$elemMatch":{     '$eq': data['panel_no']    } }
                        query['data.panel_data.panel_id']=data['panel_no']
                        
                if data['job_no'] is not None:
                    if data['job_no'] != '' and  data['job_no'] != ' ':
                        query['job_no']= data['job_no']
                print("query ==JOSOIP226677890JOBTYPEDEPARTMPAL1 ==",query)
                ret = SORTJOBS(query)
                
        else:
            print("asdkfjaksdfaksdk--------------------------------hellow ------------------",data)
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])
    else:
        ret['message']="you have not given any parameters."  

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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGJOBSHEETDATA 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGJOBSHEETDATA 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret



def SORTPANELSGROUPPANELS(Query):
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            Query['job_sheet_name'] = sheet_data['job_sheet_name']
            Query['token'] = sheet_data['token']
            panel_no = None
            if "panel_no" in Query:
                panel_no = Query['panel_no']
            if 'type' in Query :
                Query['type']="HT"
            # print("final_query_of-SORTPANELSGROUPPANELS ",Query)
            data = list(mongo.db.panel_data.find(Query))
            final_panel_data = [] 
            if len(data) !=0 :
                for i, paneldatacheck in enumerate(data):
                    if isEmpty(paneldatacheck['data']) :
                        if len(paneldatacheck['data']['panel_data']) !=0:
                            for i , panelid in enumerate(paneldatacheck['data']['panel_data']):
                                if panelid['panel_id'] not in final_panel_data:
                                    final_panel_data.append(panelid['panel_id'])
                    # else:
                    #     final_panel_data.append(paneldatacheck)

                if len(final_panel_data) !=0:
                    ret['message']=final_panel_data
                    ret['success']=True      
            else:
                ret['message'] = 'panel data not found'
        else:
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'
    return ret

@dashboard.route('/GROUPBYPANEL', methods=['POST'])
def GROUPBYPANEL():
    ret = {'success': False, 'message':'something went wrong with SORTINGJOBSHEETDATA api'}
    data = request.json
    if data == None:
        data = {}
    if isEmpty(data):
        request_key_array = ['ip_address','department','job_no']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                print("camera_ip something missing ",output)
                
                query = {}                
                panel_data = {'panel_data':{"$elemMatch":[]}}                 
                if data['ip_address'] is not None:
                    if data['ip_address'] != ' ' and data['ip_address'] != '' :
                        query['data.ip_address'] = data['ip_address']
                if data['department'] is not None:
                    if data['department'] != ' ' and data['department'] != '':
                        query['department'] = data['department']              
                if data['type'] is not None:
                    if data['type'] != ' ' and data['type'] != '':
                        query['type'] = data['type']                
                        
                if data['job_no'] is not None:
                    if data['job_no'] != '' and  data['job_no'] != ' ':
                        query['job_no']= data['job_no']
                print("query ==GROUPBYPANEL-1==",query) 
                ret = SORTPANELSGROUPPANELS(query)
                        
                        
                
            else:
                ip_address = data['ip_address']
                department =data['department']
                
                query = {}                
                panel_data = {'panel_data':{"$elemMatch":[]}}                 
                if data['ip_address'] is not None:
                    if data['ip_address'] != ' ' and data['ip_address'] != '' :
                        query['data.ip_address'] = data['ip_address']
                if data['department'] is not None:
                    if data['department'] != ' ' and data['department'] != '':
                        query['department'] = data['department']              
                        
                if data['job_no'] is not None:
                    if data['job_no'] != '' and  data['job_no'] != ' ':
                        query['job_no']= data['job_no']
                print("query ==GROUPBYPANEL===2==",query) 
                ret = SORTPANELSGROUPPANELS(query)   
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])
    else:
        ret['message']="you have not given any parameters."
    return ret

def merge_multi_isolation_jobs(final_test_sort):
    # l = final_test_sort
    res = [{'job_no': i, 'merged_data': [k for oo, k in enumerate(final_test_sort) if k['job_no'] == i]} for i in set([p['job_no'] for ooo, p in enumerate(final_test_sort)])   ]
    return res


def TSKSHEET123(list1):
    if 1:
    # try:
        check_data =list1
        print("SHEET123===",len(list1))
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = "_".join(["ESI_MONITORING_", now.strftime('%m-%d-%Y-%H-%M-%S'), '.xlsx'])#os.path.join("ESI_MONITORING_", now.strftime('%m-%d-%Y-%H-%M-%S'),'.xlsx')#"_".join(["ESI_MONITORING_", now.strftime('%m-%d-%Y-%H-%M-%S'), '.xlsx'])
        create_multiple_dir(os.path.join(os.getcwd(), "ESI_MONITORING_SHEETS"))
        filename =os.path.join(os.getcwd(), "ESI_MONITORING_SHEETS", excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('ESI MONITORING DATA')
        worksheet.set_column('A:D', 20)
        # worksheet.set_column('A:D', 20)
        worksheet.set_column(4, 4, 40)
        worksheet.set_column(5, 5, 30)
        worksheet.set_column('G:J', 30)
        worksheet.set_column('K:K', 40)
        worksheet.set_column(11, 11, 30)        
        worksheet.set_column(12, 12, 40)
        worksheet.set_column(16, 16, 40)
        worksheet.set_column(20, 20, 30)
        worksheet.set_column(21, 21, 30)
        worksheet.set_column(19, 19, 30)
        worksheet.set_column(17, 17, 25)
        worksheet.set_column('N:N', 30)
        worksheet.set_column('O:P', 20)
        worksheet.set_column('S:U', 20)
        worksheet.set_column('V:V', 45)
        worksheet.set_column('R:R', 45)
        worksheet.set_column('W:Y', 20)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(35)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd(), "smaple_files",'Docketrun_logo.png'), {'x_scale': 0.49, 'y_scale': 0.46})
        worksheet.write('B1', 'ESI MONITORING DATA', cell_format)
        worksheet.merge_range('B1:R1', 'ESI MONITORING DATA', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'JOB NO', cell_format_1)
        worksheet.write(row, col + 1, 'Job Type', cell_format_1)
        worksheet.write(row, col + 2, 'Department', cell_format_1)
        worksheet.write(row, col + 3, 'Sub Area', cell_format_1)
        worksheet.write(row, col + 4, 'Job Description', cell_format_1)
        worksheet.write(row, col + 5, 'No. of Isolating Points', cell_format_1)
        worksheet.write(row, col + 6, 'Isolating Location', cell_format_1)
        worksheet.write(row, col + 7, 'Switch Board Name', cell_format_1)#Feeder Number#Switch Board Name
        worksheet.write(row, col + 8, 'Feeder Number', cell_format_1)
        worksheet.write(row, col + 9, 'IP Address', cell_format_1)
        worksheet.write(row, col + 10, 'Tag Name', cell_format_1)
        worksheet.write(row, col + 11, 'Job Status', cell_format_1)
        worksheet.write(row, col + 12, 'Power Status', cell_format_1)
        worksheet.write(row, col + 13, 'Magnetic Sticker', cell_format_1)
        worksheet.write(row, col + 14, 'RIRO IMAGE', cell_format_1)
        worksheet.write(row, col + 15, 'RACK IN/OUT', cell_format_1)
        worksheet.write(row, col + 16, 'Method of Rack in/out', cell_format_1)
        worksheet.write(row, col + 17, 'DATE-TIME ', cell_format_1)
        worksheet.write(row, col + 18, 'PPE Violations', cell_format_1)
        worksheet.write(row, col + 19, 'Tag/Untag', cell_format_1)
        worksheet.write(row, col + 20, 'Lock/Unlock', cell_format_1)
        worksheet.write(row, col + 21, 'No of Person within 5 Mtr',            cell_format_1)
        worksheet.write(row, col + 22, 'Barricading', cell_format_1)
        # worksheet.write(row, col + 23, 'Job Sheet panel', cell_format_1)
        worksheet.write(row, col + 23, 'Remarks', cell_format_1)
        cell_format_2 = workbook.add_format()
        cell_format_2.set_font_name('Calibri')
        cell_format_2.set_align('center_across')
        format2 = workbook.add_format({'bg_color': '#C6EFCE', 'font_color':'#006100'})
        cell_format_3 = workbook.add_format()
        cell_format_3.set_font_name('Calibri')
        cell_format_3.set_align('center_across')
        cell_format_3.set_bg_color('red')
        cell_format_4 = workbook.add_format()
        cell_format_4.set_font_name('Calibri')
        cell_format_4.set_align('center_across')
        cell_format_4.set_bg_color('#FFFF00')
        cell_format_5 = workbook.add_format()
        cell_format_5.set_font_name('Calibri')
        cell_format_5.set_align('center_across')
        cell_format_5.set_bg_color('green')
        text_wrap = workbook.add_format({'valign': 'center_across'})
        rows = 2
        cols = 0
        cols1 = 1
        cols2 = 2
        cols3 = 3
        cols4 = 4
        cols5 = 5
        cols6 = 6
        cols7 = 7
        cols8 = 8
        cols9 = 9
        cols10 = 10
        cols11 = 11
        cols12 = 12
        cols13 = 13
        cols14 = 14
        cols15 = 15
        cols16 = 16
        cols17 = 17
        cols18 = 18
        cols19 = 19
        cols20 = 20
        cols21 = 21
        cols22 = 22
        cols23 = 23
        cols24 = 24

        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0
        for hello, ikim in enumerate(check_data):
            if len(ikim['merged_data']) !=0:
                if 1:
                # try:
                    for hello, i in enumerate(ikim['merged_data']):
                        print("====job_no and panelnumber====",i['job_no'],i['data']['panel_data']['panel_id'])
                        if type(i['riro_data']) == list:
                            if len(i['riro_data']) != 0:
                                if len(i['riro_data']) == 1:
                                    if cols == 0:
                                        worksheet.write(rows, cols, i['job_no'], cell_format_2)
                                    if cols1 == 1:
                                        worksheet.write(rows, cols1, i['type'], cell_format_2)
                                    if cols2 == 2:
                                         worksheet.write(rows, cols2, i['department'], cell_format_2)
                                    if cols3 == 3:
                                        try:                    
                                            worksheet.write(rows, cols3, i['sub_area'], cell_format_2)
                                        except KeyError as error:
                                            worksheet.write(rows, cols3, i['area'], cell_format_2)

                                    if cols4 == 4:
                                        worksheet.write(rows, cols4, i['job_description'],cell_format_2)
                                    if cols5 == 5:
                                        worksheet.write(rows, cols5, i['no_of_isolating_points'],cell_format_2)
                                    if cols6 == 6:
                                        try:
                                            worksheet.write(rows, cols6, i['isolating_location'],cell_format_2)
                                        except KeyError as error :
                                            worksheet.write(rows, cols6, i['isolating_locations'],cell_format_2)
                                    if cols7 == 7:
                                        worksheet.write(rows, cols7, i['board'],cell_format_2)
                                    if cols8 == 8:
                                        worksheet.write(rows, cols8, i['data']['panel_data']['panel_id'],cell_format_2)
                                    if cols9 ==9 :
                                        worksheet.write(rows, cols9, i['data']['ip_address'],cell_format_2)
                                    if cols10 ==10:
                                        if i['tagname']:
                                            worksheet.write(rows, cols10, i['tagname'], cell_format_2)
                                        else:
                                            worksheet.write(rows, cols10, '-----', cell_format_2)
                                    if cols11 == 11:
                                        if i['data']['panel_data']['panel_status']:
                                            worksheet.write(rows, cols11,'completed', cell_format_2)
                                        else:
                                            worksheet.write(rows, cols11, '-----', cell_format_2)
                                    if cols12 == 12:
                                        if i['riro_data'][0]['magnetic_flasher']:
                                            if i['riro_data'][0]['magnetic_flasher']['status']=='yes':
                                                worksheet.write(rows, cols12, 'isolated', cell_format_2)
                                            else:
                                                worksheet.write(rows, cols12, 'live', cell_format_2)
                                        else:
                                            worksheet.write(rows, cols12, '-----',cell_format_2) 
                                    if cols13 == 13:
                                        if i['riro_data'][0]['magnetic_flasher']:
                                            worksheet.write(rows, cols13, i['riro_data'][0]['magnetic_flasher']['status'], cell_format_2)
                                        else:
                                            worksheet.write(rows, cols13, '-----',cell_format_2)        
                                    
                                    if cols14 == 14:
                                        if i['riro_data'][0]['riro_merged_image']:
                                            try:
                                                verify_img = Image.open(get_current_dir_and_goto_parent_dir() + '/images/RIRO_merged_imgs' +'/' + i['riro_data'][0]['riro_merged_image'])
                                                verify_img.verify()
                                                worksheet.set_column(5, 5,40)
                                                worksheet.set_row(rows, 180)
                                                worksheet.insert_image(rows, cols14, get_current_dir_and_goto_parent_dir() + '/images/RIRO_merged_imgs' + '/' + str(i['riro_data'][0]['riro_merged_image']), {'x_scale': 0.29, 'y_scale': 0.36})
                                            except FileNotFoundError as error :
                                                worksheet.set_column(5, 5,40)
                                                worksheet.set_row(rows, 180)
                                                worksheet.insert_image(rows, cols14, os.path.join(os.getcwd() , 'smaple_files','NOT_FOUND_IMAGE.png'), {'x_scale': 0.159, 'y_scale': 0.37})

                                        else:
                                            worksheet.write(rows, cols14, '-----',cell_format_2)
                                    if cols15 == 15:
                                        if i['riro_data'][0]['rack_process'] is not None:
                                            worksheet.write(rows, cols15, i['riro_data'][0]['rack_process'], cell_format_2)
                                        else:
                                            worksheet.write(rows, cols15, '-----',cell_format_2)
                                    if cols16 == 16:
                                        if i['riro_data'][0]['rack_method'] is not None:
                                            if i['riro_data'][0]['rack_method'] == 'automatic':
                                                worksheet.write(rows, cols16, i[ 'riro_data'][0]['rack_method'],cell_format_2)
                                            else:
                                                worksheet.write(rows, cols16, i[ 'riro_data'][0]['rack_method'],cell_format_3)
                                        else:
                                            worksheet.write(rows, cols16, '-----', cell_format_2)
                                    if cols17 == 17:
                                        if i['riro_data'][0]['irrd_in_time'] or i['riro_data'][0]['irrd_out_time']:
                                            worksheet.write(rows, cols17, str(i['riro_data'][0]['irrd_in_time']) +  '    ' + str(i['riro_data'][0]['irrd_out_time']), cell_format_2)
                                        else:
                                            worksheet.write(rows, cols17, '-----', cell_format_2)
                                    if cols18 == 18:
                                        if i['riro_data'][0]['violation']:
                                            worksheet.write(rows, cols18, 'TRUE',cell_format_2)
                                        else:
                                            worksheet.write(rows, cols18, 'FALSE',cell_format_2)
                                    if cols19 == 19:
                                        if i['riro_data'][0]['tag']:
                                            worksheet.write(rows, cols19, i['riro_data'][0]['tag'], cell_format_2)
                                        else:
                                            worksheet.write(rows, cols19, '-----',cell_format_2)
                                    if cols20 == 20:
                                        if i['riro_data'][0]['lock']:
                                            worksheet.write(rows, cols20, i['riro_data'][0]['lock'], cell_format_2)
                                        else:
                                            worksheet.write(rows, cols20, '-----',cell_format_2)
                                    if cols21 == 21:
                                        if i['riro_data'][0]['five_meter']:
                                            try:
                                                if type(i['riro_data'][0]['five_meter']) == bool:
                                                    if i['riro_data'][0]['five_meter']:
                                                        worksheet.write(rows, cols21, 'yes',cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols21, 'no',cell_format_2)
                                                elif type(i['riro_data'][0]['five_meter']) == str:
                                                    if i['riro_data'][0]['five_meter'] == 'yes':
                                                        worksheet.write(rows, cols21, 'yes',cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols21, 'no', cell_format_2)
                                                elif type(i['riro_data'][0]['five_meter']) == dict:
                                                    if i['riro_data'][0]['five_meter'][ 'violation']:
                                                        worksheet.write(rows, cols21, 'yes', cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols21, 'no', cell_format_2)
                                                elif i['riro_data'][0]['five_meter'][ 'violation']:
                                                    worksheet.write(rows, cols21, 'yes', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols21, 'no',cell_format_2)
                                            except Exception as  error:
                                                print('FIVE VIOLATION ERROR WHILE WRITING EXCEL --', error)
                                                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEereT123 1", str(error), " ----time ---- ", now_time_with_time()]))
                                                worksheet.write(rows, cols21, '-----', cell_format_2)
                                        else:
                                            worksheet.write(rows, cols16, '-----',cell_format_2)
                                    if cols22 == 22:
                                        if i['riro_data'][0]['barricading']:
                                            worksheet.write(rows, cols22, i['riro_data'][0]['barricading'],cell_format_2)
                                        else:
                                            worksheet.write(rows, cols22, '-----', cell_format_2)
                                    if cols23 == 23:
                                        if i['riro_data'][0]['remarks']:
                                            worksheet.write(rows, cols23, i['riro_data'][0]['remarks'], cell_format_2)
                                        else:
                                            worksheet.write(rows, cols23, ' ',  cell_format_2)
                                elif len(i['riro_data']) > 1:
                                    for kmk, jumila in enumerate(i['riro_data']):
                                        # rows += 1
                                        if kmk==0:                                            
                                            if cols == 0:
                                                worksheet.write(rows, cols, i['job_no'], cell_format_2)
                                            if cols1 == 1:
                                                worksheet.write(rows, cols1, i['type'], cell_format_2)
                                            if cols2 == 2:
                                                worksheet.write(rows, cols2, i['department'], cell_format_2)
                                            if cols3 == 3:
                                                try :
                                                    worksheet.write(rows, cols3, i['sub_area'], cell_format_2)
                                                except KeyError as error :
                                                    worksheet.write(rows, cols3, i['area'], cell_format_2)
                                            if cols4 == 4:
                                                worksheet.write(rows, cols4, i['job_description'],cell_format_2)
                                            if cols5 == 5:
                                                worksheet.write(rows, cols5, i['no_of_isolating_points'],cell_format_2)
                                            if cols6 == 6:
                                                try :
                                                    worksheet.write(rows, cols6, i['isolating_location'],cell_format_2)
                                                except KeyError as error :
                                                    worksheet.write(rows, cols6, i['isolating_locations'],cell_format_2)
                                            if cols7 == 7:
                                                worksheet.write(rows, cols7, i['board'],cell_format_2)
                                                #i['data']['panel_data']['panel_id']
                                            if cols8 == 8:
                                                worksheet.write(rows, cols8, i['data']['panel_data']['panel_id'],cell_format_2)
                                            if cols9 ==9 :
                                                worksheet.write(rows, cols9, i['data']['ip_address'],cell_format_2)
                                            if cols10 ==10:
                                                if i['tagname']:
                                                    worksheet.write(rows, cols10, i['tagname'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols10, '-----', cell_format_2)
                                            if cols11 == 11:
                                                if i['data']['panel_data']['panel_status']:
                                                    worksheet.write(rows, cols11,'completed', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols11, '-----', cell_format_2)
                                            if cols12 == 12:
                                                if jumila['magnetic_flasher']:
                                                    if jumila['magnetic_flasher']['status']=='yes':
                                                        worksheet.write(rows, cols12, 'isolated', cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols12, 'live', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols12, '-----',cell_format_2) 
                                                    
                                            
                                            if cols13 == 13:
                                                if jumila['magnetic_flasher']:
                                                    worksheet.write(rows, cols13, jumila['magnetic_flasher']['status'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols13, '-----',cell_format_2)        
                                            
                                            if cols14 == 14:
                                                if jumila['riro_merged_image']:
                                                    try:
                                                        verify_img = Image.open(get_current_dir_and_goto_parent_dir() + '/images/RIRO_merged_imgs' +'/' + jumila['riro_merged_image'])
                                                        verify_img.verify()
                                                        worksheet.set_column(5, 5,40)
                                                        worksheet.set_row(rows, 180)
                                                        worksheet.insert_image(rows, cols14, get_current_dir_and_goto_parent_dir() + '/images/RIRO_merged_imgs' + '/' + str(jumila['riro_merged_image']), {'x_scale': 0.29, 'y_scale': 0.36})
                                                    except FileNotFoundError as error :
                                                        worksheet.set_column(5, 5,40)
                                                        worksheet.set_row(rows, 180)    
                                                        worksheet.insert_image(rows, cols14, os.path.join(os.getcwd() , 'smaple_files','NOT_FOUND_IMAGE.png'), {'x_scale': 0.159, 'y_scale': 0.37})
                                                else:
                                                    worksheet.write(rows, cols14, '-----',cell_format_2)
                                            if cols15 == 15:
                                                if jumila['rack_process'] is not None:
                                                    worksheet.write(rows, cols15, jumila['rack_process'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols15, '-----',cell_format_2)
                                            if cols16 == 16:
                                                if jumila['rack_method'] is not None:
                                                    if jumila['rack_method'] == 'automatic':
                                                        worksheet.write(rows, cols16, jumila['rack_method'],cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols16,jumila['rack_method'],cell_format_3)
                                                else:
                                                    worksheet.write(rows, cols16, '-----', cell_format_2)
                                            if cols17 == 17:
                                                if jumila['irrd_in_time'] or jumila['irrd_out_time']:
                                                    worksheet.write(rows, cols17, str(jumila['irrd_in_time']) +  '    ' + str(jumila['irrd_out_time']), cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols17, '-----', cell_format_2)
                                            if cols18 == 18:
                                                if jumila['violation']:
                                                    worksheet.write(rows, cols18, 'TRUE',cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols18, 'FALSE',cell_format_2)
                                            if cols19 == 19:
                                                if jumila['tag']:
                                                    worksheet.write(rows, cols19, jumila['tag'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols19, '-----',cell_format_2)
                                            if cols20 == 20:
                                                if jumila['lock']:
                                                    worksheet.write(rows, cols20, jumila['lock'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols20, '-----',cell_format_2)
                                            if cols21 == 21:
                                                if i['riro_data'][0]['five_meter']:
                                                    try:
                                                        if type(jumila['five_meter']) == bool:
                                                            if jumila['five_meter']:
                                                                worksheet.write(rows, cols21, 'yes',cell_format_2)
                                                            else:
                                                                worksheet.write(rows, cols21, 'no',cell_format_2)
                                                        elif type(jumila['five_meter']) == str:
                                                            if jumila['five_meter'] == 'yes':
                                                                worksheet.write(rows, cols21, 'yes',cell_format_2)
                                                            else:
                                                                worksheet.write(rows, cols21, 'no', cell_format_2)
                                                        elif type(jumila['five_meter']) == dict:
                                                            if jumila['five_meter'][ 'violation']:
                                                                worksheet.write(rows, cols21, 'yes', cell_format_2)
                                                            else:
                                                                worksheet.write(rows, cols21, 'no', cell_format_2)
                                                        elif jumila['five_meter'][ 'violation']:
                                                            worksheet.write(rows, cols21, 'yes', cell_format_2)
                                                        else:
                                                            worksheet.write(rows, cols21, 'no',cell_format_2)
                                                    except Exception as  error:
                                                        print('FIVE VIOLATION ERROR WHILE WRITING EXCEL --', error)
                                                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEereT123 1", str(error), " ----time ---- ", now_time_with_time()]))
                                                        worksheet.write(rows, cols21, '-----', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols16, '-----',cell_format_2)
                                            if cols22 == 22:
                                                if jumila['barricading']:
                                                    worksheet.write(rows, cols22, jumila['barricading'],cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols22, '-----', cell_format_2)
                                            if cols23 == 23:
                                                if jumila['remarks']:
                                                    worksheet.write(rows, cols23, jumila['remarks'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols23, ' ',  cell_format_2)
                                        else:
                                            if cols11 == 11:
                                                if i['data']['panel_data']['panel_status']:
                                                    worksheet.write(rows, cols11,'completed', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols11, '-----', cell_format_2)
                                            if cols12 == 12:
                                                if jumila['magnetic_flasher']:
                                                    if jumila['magnetic_flasher']['status']=='yes':
                                                        worksheet.write(rows, cols12, 'isolated', cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols12, 'live', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols12, '-----',cell_format_2) 
                                                    
                                            
                                            if cols13 == 13:
                                                if jumila['magnetic_flasher']:
                                                    worksheet.write(rows, cols13, jumila['magnetic_flasher']['status'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols13, '-----',cell_format_2)        
                                            
                                            if cols14 == 14:
                                                if jumila['riro_merged_image']:
                                                    try :
                                                        verify_img = Image.open(get_current_dir_and_goto_parent_dir() + '/images/RIRO_merged_imgs' +'/' + jumila['riro_merged_image'])
                                                        verify_img.verify()
                                                        worksheet.set_column(14, 14, 25)
                                                        worksheet.set_row(rows, 180)
                                                        worksheet.insert_image(rows, cols14, get_current_dir_and_goto_parent_dir() + '/images/RIRO_merged_imgs' + '/' + str(jumila['riro_merged_image']), {'x_scale': 0.29, 'y_scale': 0.36})
                                                    except FileNotFoundError as error :
                                                        worksheet.set_column(5, 5,40)
                                                        worksheet.set_row(rows, 180)    
                                                        worksheet.insert_image(rows, cols14, os.path.join(os.getcwd() , 'smaple_files','NOT_FOUND_IMAGE.png'), {'x_scale': 0.159, 'y_scale': 0.37})
                                                else:
                                                    worksheet.write(rows, cols14, '-----',cell_format_2)
                                            if cols15 == 15:
                                                if jumila['rack_process'] is not None:
                                                    worksheet.write(rows, cols15, jumila['rack_process'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols15, '-----',cell_format_2)
                                            if cols16 == 16:
                                                if jumila['rack_method'] is not None:
                                                    if jumila['rack_method'] == 'automatic':
                                                        worksheet.write(rows, cols16, jumila['rack_method'],cell_format_2)
                                                    else:
                                                        worksheet.write(rows, cols16, jumila['rack_method'],cell_format_3)
                                                else:
                                                    worksheet.write(rows, cols16, '-----', cell_format_2)
                                            if cols17 == 17:
                                                if jumila['irrd_in_time'] or jumila['irrd_out_time']:
                                                    worksheet.write(rows, cols17, str(jumila['irrd_in_time']) +  '    ' + str(jumila['irrd_out_time']), cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols17, '-----', cell_format_2)
                                            if cols18 == 18:
                                                if jumila['violation']:
                                                    worksheet.write(rows, cols18, 'TRUE',cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols18, 'FALSE',cell_format_2)
                                            if cols19 == 19:
                                                if jumila['tag']:
                                                    worksheet.write(rows, cols19, jumila['tag'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols19, '-----',cell_format_2)
                                            if cols20 == 20:
                                                if jumila['lock']:
                                                    worksheet.write(rows, cols20, jumila['lock'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols20, '-----',cell_format_2)
                                            if cols21 == 21:
                                                if jumila['five_meter']:
                                                    try:
                                                        if type(jumila['five_meter']) == bool:
                                                            if jumila['five_meter']:
                                                                worksheet.write(rows, cols21, 'yes',cell_format_2)
                                                            else:
                                                                worksheet.write(rows, cols21, 'no',cell_format_2)
                                                        elif type(jumila['five_meter']) == str:
                                                            if jumila['five_meter'] == 'yes':
                                                                worksheet.write(rows, cols21, 'yes',cell_format_2)
                                                            else:
                                                                worksheet.write(rows, cols21, 'no', cell_format_2)
                                                        elif type(jumila['five_meter']) == dict:
                                                            if jumila['five_meter'][ 'violation']:
                                                                worksheet.write(rows, cols21, 'yes', cell_format_2)
                                                            else:
                                                                worksheet.write(rows, cols21, 'no', cell_format_2)
                                                        elif jumila['five_meter'][ 'violation']:
                                                            worksheet.write(rows, cols21, 'yes', cell_format_2)
                                                        else:
                                                            worksheet.write(rows, cols21, 'no',cell_format_2)
                                                    except Exception as  error:
                                                        print('FIVE VIOLATION ERROR WHILE WRITING EXCEL --', error)
                                                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEereT123 1", str(error), " ----time ---- ", now_time_with_time()]))
                                                        worksheet.write(rows, cols21, '-----', cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols16, '-----',cell_format_2)
                                            if cols22 == 22:
                                                if jumila['barricading']:
                                                    worksheet.write(rows, cols22, jumila['barricading'],cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols22, '-----', cell_format_2)
                                            if cols23 == 23:
                                                if jumila['remarks']:
                                                    worksheet.write(rows, cols23, jumila['remarks'], cell_format_2)
                                                else:
                                                    worksheet.write(rows, cols23, ' ',  cell_format_2)
                                        if kmk !=len(i['riro_data'])-1:
                                            rows += 1
                                
                        rows += 1
                # except UnidentifiedImageError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEETerreq123 4", str(error), " ----time ---- ", now_time_with_time()]))
                #     UnidentifiedImageError_count += 1
                # except FileNotFoundError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEqerqweT123 5", str(error), " ----time ---- ", now_time_with_time()]))
                #     FileNotFoundError_count += 1
                # except UserWarning as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEETqerqwe123 6", str(error), " ----time ---- ", now_time_with_time()]))
                # except ImportError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEET1qerq23 7", str(error), " ----time ---- ", now_time_with_time()]))
                # except xlsxwriter.exceptions.FileCreateError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEeqrwerqT123 08", str(error), " ----time ---- ", now_time_with_time()]))
                # except PermissionError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHqerqweEET123 09", str(error), " ----time ---- ", now_time_with_time()]))
                # except xlsxwriter.exceptions.XlsxWriterException as  error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEqeqreET123 10", str(error), " ----time ---- ", now_time_with_time()]))
        if 1:
        # try:
            workbook.close()
            print('UnidentifiedImageError_count == ',
                UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        # except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter.
        #     exceptions.EmptyChartSeries, xlsxwriter.exceptions.
        #     DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,
        #     xlsxwriter.exceptions.DuplicateWorksheetName, xlsxwriter.
        #     exceptions.XlsxWriterException, xlsxwriter.exceptions.
        #     XlsxFileError, xlsxwriter.exceptions.FileCreateError,
        #     xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions
        #     .FileSizeError) as error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKS33HEET123 11", str(error), " ----time ---- ", now_time_with_time()]))
        # except PermissionError as error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKS33HEET123 12", str(error), " ----time ---- ", now_time_with_time()]))
        # except AttributeError as error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHE33ET123 13", str(error), " ----time ---- ", now_time_with_time()]))
    # except Exception as  error:
    #     ret = {'success': False, 'message': str(error)}
    return ret



def COMPLETESTATUSRITS(rack_process_list):
    panel_status = False
    if len(rack_process_list) != 0:
        if len(rack_process_list) == 1:
            if rack_process_list[0]['rack_process'] is not None:
                if rack_process_list[0]['rack_process'] == 'rack_out':
                    panel_status = False
                elif rack_process_list[0]['rack_process'] == 'rack_in':
                    panel_status = True
                elif rack_process_list[0]['rack_process'] == 'maintenance':
                    panel_status = False
        elif len(rack_process_list) > 1:
            if rack_process_list[0]['rack_process'] is not None:
                if rack_process_list[1]['rack_process'] is not None:
                    if rack_process_list[1]['rack_process'
                        ] == rack_process_list[0]['rack_process']:
                        panel_status = False
                    elif rack_process_list[0]['rack_process'] == 'rack_out':
                        panel_status = False
                    elif rack_process_list[0]['rack_process'] == 'rack_in':
                        panel_status = True
                    elif rack_process_list[0]['rack_process'] == 'maintenance':
                        panel_status = False
    return panel_status

def EDitstatus(final_data_riro_data):
    riro_edit_status = False
    if len(final_data_riro_data) != 0:
        for i in final_data_riro_data:
            if i['riro_edit_status']:
                riro_edit_status = True
                break
    return riro_edit_status

def PPEVIOlationinESI(rtsp_url, panel_id, person_in_time,person_out_time):
    violation_test = False
    try:
        find_violation_data = list(mongo.db.data.find({'camera_rtsp': rtsp_url,'timestamp':{'$gte': person_in_time, '$lte': person_out_time},'violation_status': True}).sort('timestamp', -1))
        if len(find_violation_data) != 0:
            for olki, kl in enumerate(find_violation_data):
                for LILA, SHIVA in enumerate(kl['object_data']):
                    if 'pannel_details' in SHIVA.keys():
                        if panel_id is not None and SHIVA['pannel_details'] is not None:
                            if panel_id in SHIVA['pannel_details']:
                                violation_test = True
                                break
    
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PPEVIOlationinESI 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PPEVIOlationinESI 2", str(error), " ----time ---- ", now_time_with_time()]))
    return violation_test

def SORTINGFORLATESTTWODATAEXCEl(joinedlist):
    final_join_list = []
    if len(joinedlist) != 0:
        if len(joinedlist) == 1:
            final_join_list = joinedlist
        elif len(joinedlist) > 1:
            if joinedlist[1]['rack_process'] == joinedlist[0]['rack_process']:
                final_join_list.append(joinedlist[0])
            elif joinedlist[0]['rack_process'] == 'rack_in':
                if joinedlist[1]['rack_process'] == 'rack_out':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'maintenance':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
            elif joinedlist[0]['rack_process'] == 'rack_out':
                final_join_list.append(joinedlist[0])
            elif joinedlist[0]['rack_process'] == 'maintenance':
                if joinedlist[1]['rack_process'] == 'rack_out':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
                elif joinedlist[1]['rack_process'] == 'rack_in':
                    final_join_list.append(joinedlist[0])
                    final_join_list.append(joinedlist[1])
    return final_join_list

def SORTRIRODATAFOREXCEL(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    joinedlist = []
    try:
        for mix, i in enumerate(list_of_dict):
            if i['irrd_in_time'] is not None:
                time_stamp_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_(time_stamp_data)
            mongo_id_data = sort_job_sheet_time_sort_key_(mongo_id_data)
            joinedlist = time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            joinedlist = sort_irrd_time_(time_stamp_data)
        elif len(mongo_id_data) != 0:
            joinedlist = sort_job_sheet_time_sort_key_(mongo_id_data)
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTRIRODATAFOREXCEL 1", str(error), " ----time ---- ", now_time_with_time()]))
    if len(joinedlist) != 0:
        joinedlist = SORTINGFORLATESTTWODATAEXCEl(joinedlist)
    return joinedlist

def GENERATIONEXCELRIRODATA(rtsp_url, panel_id, check_data):
    match_data = []
    violation_test = False
    panel_status = False
    panel_count = 0
    rack_process_list = []
    lock_list = []
    tag_list = []
    for zz, kiku in enumerate(check_data):
        if panel_id == kiku['panel_no']:
            panel_count += 1
            if kiku['rack_process'] is not None:
                if kiku['rack_process'] not in rack_process_list:
                    rack_process_list.append(kiku['rack_process'])
                if kiku['rack_process'] == 'rack_out':
                    if kiku['tag'] is not None and kiku['lock'] is not None:
                        if kiku['lock'] not in lock_list:
                            lock_list.append(kiku['lock'])
                        if kiku['tag'] not in tag_list:
                            tag_list.append(kiku['tag'])
            if kiku['rack_method'] == 'automatic':
                if kiku['irrd_in_time'] is not None and kiku['irrd_out_time'] is not None:
                    violation_test = PPEVIOlationinESI(rtsp_url, panel_id, kiku['irrd_in_time'], kiku['irrd_out_time'])
                elif kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = PPEVIOlationinESI(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                riro_data_test_1 = {'sort_id': kiku['_id'], 'panel_no': kiku['panel_no'], 'rack_method': kiku['rack_method'],'rack_process': kiku['rack_process'], 'irrd_in_time': kiku['irrd_in_time'], 'irrd_out_time': kiku['irrd_out_time'], 'tag': kiku['tag'], 'lock': kiku['lock'], 'lock_time': kiku['lock_time'], 'tag_time':kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher':kiku['magnetic_flasher'],'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image':kiku['riro_merged_image'], 'riro_merged_image_size': kiku['riro_merged_image_size'], 'riro_edit_status':kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
            elif kiku['rack_method'] == 'manual':
                if kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = PPEVIOlationinESI(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                riro_data_test_1 = {'sort_id': kiku['_id'], 'panel_no':kiku['panel_no'], 'rack_method': kiku['rack_method'],'rack_process': kiku['rack_process'], 'irrd_in_time':kiku['person_in_time'], 'irrd_out_time': kiku['person_out_time'], 'tag': kiku['tag'], 'lock': kiku['lock'], 'lock_time': kiku['lock_time'], 'tag_time':kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher':kiku['magnetic_flasher'], 'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image': kiku['riro_merged_image'], 'riro_merged_image_size':kiku['riro_merged_image_size'], 'riro_edit_status':kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
    if len(rack_process_list) != 0:
        rack_process_for_job = ['rack_out', 'rack_in']
        if rack_process_for_job == rack_process_list:
            panel_status = COMPLETESTATUSRITS(match_data)
        elif 'rack_in' in rack_process_list:
            panel_status = True
    return match_data,COMPLETESTATUSRITS(match_data), EDitstatus(match_data)#SORTRIRODATAFOREXCEL(match_data), COMPLETESTATUSRITS(match_data), EDitstatus(match_data)


@dashboard.route('/create_excel', methods=['GET'])
@dashboard.route('/create_excel/<id>', methods=['GET'])
def TSKEXCELGENERATION(id = None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        sheet_data=None
        if id is not None:
            sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
        else:            
            sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
            if len(data) !=0 :
                final_panel_data = []
                data = PANELWISERIRODATAFUNCTION(data)
                for ___INNN, emmmi in enumerate(data):
                    if emmmi['data']['panel_data']['panel_id'] is not None:
                        final_panel_data.append(emmmi)
                if len(final_panel_data) != 0:
                    riro_final = []
                    for i, each_panel in enumerate(final_panel_data):
                        show_live_riro =list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status': 1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                        if len(show_live_riro) != 0:
                            show_live_riro = riro_live_data(show_live_riro)
                            each_panel['riro_data'] = show_live_riro
                            each_panel['riro_edit_status'] = False
                            each_panel['live_status'] = True
                            each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
                            if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                            else:
                                each_panel['isolation_status'] = None
                            #each_panel = parse_json(each_panel)
                            riro_final.append(each_panel)
                        elif each_panel['data']['rtsp_url']:
                            find_riro_data =list(mongo.db.riro_data.find({ 'token': each_panel['token'], 'camera_name':  each_panel['data']['camera_name'],'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(find_riro_data) != 0:
                                (check_data, panel_status, riro_edit_status) = GENERATIONEXCELRIRODATA(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data)#(riro_history_check_the_riro_data_with_sorting_(camera_rtsp, each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                
                                if panel_status or len(check_data) != 0:
                                    each_panel['data']['panel_data']['panel_status'] = panel_status
                                    each_panel['riro_data'] = check_data
                                    each_panel['riro_edit_status'] = riro_edit_status
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = check_data[0]['sort_id']
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    riro_final.append(each_panel)
                                else:
                                    check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':
                                        None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':
                                        None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':
                                        None, 'riro_merged_image': None,'riro_merged_image_size':{'height':
                                        None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}  ]
                                    each_panel['riro_data'] = check_data
                                    each_panel['riro_edit_status'] = False
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = None
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    riro_final.append(each_panel)
                            else:
                                check_data = [{'sort_id': None, 'panel_no':
                                    each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':
                                    None, 'irrd_out_time': None, 'tag':
                                    None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None, 'magnetic_flasher':
                                    None, 'violation': False, 'riro_key_id':
                                    None, 'riro_merged_image': None,'riro_merged_image_size':{'height':
                                    None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}]
                                each_panel['riro_data'] = check_data
                                each_panel['riro_edit_status'] = False
                                each_panel['live_status'] = False
                                each_panel['sort_id'] = None
                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                else:
                                    each_panel['isolation_status'] = None
                                riro_final.append(each_panel) 
                    newdata = merge_multi_isolation_jobs(parse_json(riro_final))      
                    ret =TSKSHEET123(newdata)
                else:
                    ret = {'message': 'panel data not found.', 'success': False}
            else:
                ret['message'] = 'panel data not found'
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create22_excel 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ret['success'] = False
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_33excel 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret

@dashboard.route('/all_riro_data_history_new_concept', methods=['GET'])
def all_riro_data_history_new_concept():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    ret['job_sheet_status'] = False
    try:
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
            if len(data) !=0:
                final_panel_data = []
                data = PANELWISERIRODATAFUNCTION(data)
                # final_panel_data = [emmmi for ___INNN, emmmi  in enumerate(data) if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and  emmmi['data']['panel_data']['panel_id'] is not None]
                for ___INNN, emmmi in enumerate(data):
                    if emmmi['data']['panel_data']['panel_id'] is not None:
                        final_panel_data.append(emmmi)
                if len(final_panel_data) != 0:
                    riro_final = []
                    for i, each_panel in enumerate(final_panel_data):
                        show_live_riro =list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status': 1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                        if len(show_live_riro) != 0:
                            show_live_riro = riro_live_data(show_live_riro)
                            each_panel['riro_data'],each_panel['riro_edit_status'],each_panel['live_status'],each_panel['sort_id']  = show_live_riro,False,True,show_live_riro[0]['sort_id'] 
                            if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                            else:
                                each_panel['isolation_status'] = None
                            # each_panel = parse_json(each_panel)
                            riro_final.append(each_panel)
                        elif each_panel['data']['rtsp_url']:
                            find_riro_data =list(mongo.db.riro_data.find({ 'token': each_panel['token'], 'camera_name':  each_panel['data']['camera_name'],'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                            if len(find_riro_data) != 0:
                                (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                if panel_status or len(check_data) != 0:
                                    each_panel['data']['panel_data']['panel_status'] = panel_status
                                    each_panel['riro_data'] = check_data
                                    each_panel['riro_edit_status'] = riro_edit_status
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = check_data[0]['sort_id']
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    riro_final.append(each_panel)
                                else:
                                    check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 
                                                   'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None,
                                                   'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 
                                                   'riro_key_id': None, 'riro_merged_image': None,
                                                   'riro_merged_image_size':{'height': None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '} ]
                                    each_panel['riro_data'] = check_data
                                    each_panel['riro_edit_status'] = False
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = None
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None                                    
                                    riro_final.append(each_panel)
                            else:
                                check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 
                                               'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 
                                               'five_meter': None,'barricading': None, 'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 
                                               'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}]
                                each_panel['riro_data'] = check_data
                                each_panel['riro_edit_status'] = False
                                each_panel['live_status'] = False
                                each_panel['sort_id'] = None
                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                else:
                                    each_panel['isolation_status'] = None
                                riro_final.append(each_panel)
                    else:
                        ret = {'message': merge_multi_isolation_jobs(parse_json(all_riro_final_sortin(parse_json(riro_final)))), 'success': True}
                        ret['job_sheet_status'] = True
                else:
                    ret = {'message': 'panel data not found.', 'success': False }
                    ret['job_sheet_status'] = True
            else:
                ret['message'] = 'panel data not found'
                ret['job_sheet_status'] = True
        else:
            ret['message'] = 'job sheet data is not found.'
            ret['job_sheet_status'] = False
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- all_riro_data_history_new_concept 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message'] = " ".join(["something error has occered in api", str(error)])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ret['message'] = str(error)
        ret['success'] = False
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- all_riro_data_history_new_concept 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@dashboard.route('/riro_violation_data', methods=['POST'])
def riro_violation_data():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    try:
        
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['panel_no', 'id', 'imagename']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                panel_no = jsonobject['panel_no']
                imagename = jsonobject['imagename']
                id = jsonobject['id']
                all_data = []
                Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
                if Foundfileterdata  is None:
                    Foundfileterdata = {"helmet":30,"vest":30} 
                if panel_no is not None:
                    if id is not None:
                        data = mongo.db.panel_data.find_one({'_id':ObjectId(id)})
                        if data is not None:
                            final_panel_data = None
                            data = PANELWISERIRODATAFUNCTION(data)                            
                            for ___INNN, emmmi in enumerate(data):
                                if emmmi['data']['panel_data']['panel_id'] is not None and emmmi['data']['panel_data']['panel_id' ] == panel_no:
                                    final_panel_data = emmmi
                            if final_panel_data is not None:
                                riro_return_data = []
                                find_riro_data = mongo.db.riro_data.find_one({ 'token': final_panel_data['token'],'camera_name': final_panel_data['data']['camera_name'], 'camera_rtsp':final_panel_data['data']['rtsp_url'], 'panel_no': panel_no}, sort=[('_id', pymongo.DESCENDING)])
                                if find_riro_data is not None:
                                    find_violation_data = list(mongo.db.data.find({ 'camera_rtsp': final_panel_data['data']['rtsp_url'],'timestamp':{'$gte':  find_riro_data['person_in_time'],'$lte': find_riro_data['person_out_time']}}).sort('timestamp',-1).limit(30))
                                    if len(find_violation_data) != 0:
                                        for olki, kl in enumerate(find_violation_data):
                                            wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                                            if type(wapas_data) == list:
                                                pass
                                            else:
                                                riro_return_data.append(wapas_data)
                                        if len(riro_return_data) != 0:
                                            ret = {'success': True, 'message': parse_json(riro_return_data) }
                                        else:
                                            ret = {'success': False, 'message':  'PPE data not found.'}
                                    else:
                                        ret = {'success': False, 'message':  'violation data not found.'}
                                else:
                                    ret = {'success': False, 'message': 'riro data not found.'}
                            else:
                                ret = {'message': 'panel data not found.','success': False}
                        else:
                            ret['message'] = 'data not found'
                    else:
                        ret['message'] ='mongo id  should not be none, please enter the proper mongo id.'
                else:
                    ret['message'] ='panel number should not be none, please enter the proper panel data.'
        else:
            ret = {'message': 'parameters missing file {0}'.format(missing_key), 'success': False}

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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_violation_data 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message'] = " ".join(["something error has occered in api", str(error)])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ret['message'] = str(error)
        ret['success'] = False
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_violation_data 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret



def SORTBYPANELKEYID(d):
    key_id = str(d['roi_data']['panel_key_id'])
    return key_id


def SORTPANELDATA(panel_data):
    panel_data['panel_data'] = sorted(panel_data['panel_data'], key=SORTBYPANELKEYID)
    return panel_data


#done for object
@dashboard.route('/get_panel_data1/<id>', methods=['GET'])
@dashboard.route('/get_panel_data1/<id>/<imagename>', methods=['GET'])
def get_panel_data1(id=None, imagename=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1 :
    # try:
        all_data = []
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            newlapp =[] 
            if id is not None and imagename is not None:
                data = mongo.db.panel_data.find_one({'_id': ObjectId(id),'data.image_name': imagename, 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)])
                
                if data is not None:  
                    if 'panel' in data:
                        newlapp.append(data['panel'])
                    elif 'feeder_number' in data:
                        newlapp.append(data['feeder_number'])
                    data['all_panels']=newlapp   
                     
                    if data['type']=='HT' or data['type']=='ht':
                        # NewDataOFall = list(mongo.db.panel_data.find({'ip_address':data['ip_address'] ,'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
                        # if list(NewDataOFall) !=0:
                        #     for i , jjin in enumerate(NewDataOFall):
                        #         newlapp.append(jjin['panel'])

                        if data['data']:
                            if len(data['data']['panel_data'])!=0:
                                one_panel_data = SORTPANELDATA(data['data'])
                                rack_RW_points = rack_window_extrack_points_one_panel(one_panel_data['panel_data'])
                                ret = {'message': rack_RW_points, 'success': True}
                                if len(rack_RW_points) != 0:
                                    final_return = get_panel_data1_check_bbox_in_empty_string(rack_RW_points)
                                    data['data']['panel_data']=final_return
                                    ret = {'message': data, 'success': True}
                            else:
                                ret = {'message': data, 'success': True}
                        else:
                            ret['message'] = 'data not found.'
                    elif data['type']== 'pneumatic' or data['type']=='hydraulic' or data['type']=='Hydraulic' or data['type']== 'Pneumatic':
                        if data['data']['image_name'] == imagename:
                            ret={'message':data,'success':True}
                    elif data['type'] == 'conveyor':
                        if data['data']['image_name'] == imagename:
                            ret={'message':data,'success':True}
                else:
                    ret['message'] = 'data not found'

            elif id is not None :
                data = mongo.db.panel_data.find_one({'_id': ObjectId(id), 'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)])
                if data is not None:      
                    if 'panel' in data:
                        newlapp.append(data['panel'])
                    elif 'feeder_number' in data:
                        newlapp.append(data['feeder_number'])
                    data['all_panels']=newlapp
                    if data['type']=='HT' or data['type']=='ht':
                        # NewDataOFall = list(mongo.db.panel_data.find({'ip_address':data['ip_address'] ,'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
                        # if list(NewDataOFall) !=0:
                        #     for i , jjin in enumerate(NewDataOFall):
                        #         newlapp.append(jjin['panel'])
                        if data['data']:
                            if len(data['data']['panel_data'])!=0:
                                one_panel_data = SORTPANELDATA(data['data'])
                                rack_RW_points = rack_window_extrack_points_one_panel(one_panel_data['panel_data'])
                                ret = {'message': rack_RW_points, 'success': True}
                                if len(rack_RW_points) != 0:
                                    final_return = get_panel_data1_check_bbox_in_empty_string(rack_RW_points)
                                    data['data']['panel_data']=final_return
                                    ret = {'message': data, 'success': True}
                            else:
                                ret = {'message': data, 'success': True}
                        else:
                            ret['message'] = 'data not found.'
                    elif data['type']== 'pneumatic' or data['type']=='hydraulic' or data['type']=='Hydraulic' or data['type']== 'Pneumatic':
                        ret={'message':data,'success':True}
                    elif data['type'] == 'conveyor':
                        ret={'message':data,'success':True}
                else:
                    ret['message'] = 'data not found'
            else:
                ret['message']='mongid and image name are missing parameters.'
            
        else:
            ret['message'] = 'job sheet is not uploaded yet'
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_panel_1data1 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_panel_2data1 2", str(error), " ----time ---- ", now_time_with_time()]))
    return parse_json(ret)


def rack_window_extrack_points_one_panel_add_new_panel(rack_window_data):
    RACK_WINDOW_FINAL = rack_window_data
    try:
        if rack_window_data is not None:
            if rack_window_data is not None:
                if isEmpty(rack_window_data):
                    if len(rack_window_data['panel_data']) != 0:
                        rack_image_ = []
                        panel_data = rack_window_data['panel_data']
                        for ___, kkl in enumerate(rack_window_data['panel_data']):
                            if isEmpty(kkl['roi_data']):
                                if kkl['roi_data']['RW']:
                                    RACK_window_bboX = kkl['roi_data']['RW']
                                    kkl['roi_data']['RW'] = rack_window_split(RACK_window_bboX)
                                    rack_image_.append(kkl)
                                else:
                                    print("rack_window_data['data']['panel_data']['roi_data']['RW']   EMPTY ")
                                    rack_image_.append(kkl)
                            else:
                                print("rack_window_data['data']['panel_data']['roi_data']   EMPTY ")
                                rack_image_.append(kkl)
                        rack_window_data['panel_data'] = rack_image_
                        RACK_WINDOW_FINAL.append(rack_window_data)
                    else:
                        print("rack_window_data['data']['panel_data']   EMPTY ")
                else:
                    print("rack_window_data['data']   EMPTY ")
            else:
                print("rack_window_data['data']  NONE ")
        else:
            print('rack_window_data   EMPTY ')
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- _add_new_panel 1", str(error), " ----time ---- ", now_time_with_time()]))
    return RACK_WINDOW_FINAL


def racK_WINDOW_EXTRACT(rack_window_data):
    RACK_WINDOW_FINAL = []
    try:
        if rack_window_data is not None:
            if len(rack_window_data) != 0:
                rack_image_ = []
                panel_data = rack_window_data
                if len(rack_window_data) == 1:
                    print("CAME1")
                    if type(rack_window_data[0]['roi_data']['RW'])== list:
                        rack_image_.append(rack_window_data[0])
                    elif type(rack_window_data[0]['roi_data']['RW'])== str and (rack_window_data[0]['roi_data']['RW'])!= '':
                        print('length one rack window --- ',rack_window_data[0]['roi_data']['RW'])
                        print(rack_window_data[0]['roi_data']['RW'])
                        RACK_window_bboX = rack_window_data[0]['roi_data']['RW']
                        rack_window_data[0]['roi_data']['RW']  = rack_window_split(RACK_window_bboX)
                        rack_image_.append(rack_window_data[0])
                    else:
                        rack_image_.append(rack_window_data[0])
                elif len(rack_window_data) > 1:
                    for ___, kkl in enumerate(rack_window_data):
                        print("kkl------------------------", kkl )
                        if isEmpty(kkl['roi_data']):
                            if type(kkl['roi_data']['RW'])== list:
                                rack_image_.append(kkl)
                            elif type(kkl['roi_data']['RW']) == str and kkl['roi_data']['RW'] !='' :
                                RACK_window_bboX = kkl['roi_data']['RW']
                                kkl['roi_data']['RW'] = rack_window_split(RACK_window_bboX)
                                rack_image_.append(kkl)
                            else:
                                rack_image_.append(kkl)
                        else:
                            rack_image_.append(kkl)
                rack_window_data = rack_image_
                RACK_WINDOW_FINAL = rack_window_data
            else:
                print("rack_window_data['data']['panel_data']   EMPTY ")
        else:
            print("rack_window_data['data']  NONE ")
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- racK_WINDOW_E1XTRACT 1", str(error), " ----time ---- ", now_time_with_time()]))
    return RACK_WINDOW_FINAL




def PANELWISEDATAWITHIDANDIMAGESNAME(data, imagename):
    if 1:
    # try:
        if isEmpty(data['data']):
            if len(data['data']['panel_data']) != 0:
                data['data']['panel_data'] = racK_WINDOW_EXTRACT(data['data']['panel_data'])                
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PANELWISEDATAWITH3343IDANDIMAGESNAME 1", str(error), " ----time ---- ", now_time_with_time()]))
    return parse_json(data)

## done for object
@dashboard.route('/get_panel_data3/<id>/<imagename>', methods=['GET'])
def get_panel_data3(id=None, imagename=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            if id is not None and imagename is not None:
                data = mongo.db.panel_data.find_one({'_id': ObjectId(id),'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)])
                if data is not None:
                    return_data = PANELWISEDATAWITHIDANDIMAGESNAME(data, imagename)
                    print("999999999999999999999999999999999999999999999999")
                    ret = {'message': return_data, 'success': True}
                else:
                    ret['message'] = 'data not found.'   
            elif id is not None :
                data = mongo.db.panel_data.find_one({'_id': ObjectId(id),'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)])
                if data is not None:
                    return_data = PANELWISEDATAWITHIDANDIMAGESNAME(data, imagename)
                    print("999999999999999999999999999999999999999999999999")
                    ret = {'message': return_data, 'success': True}
                else:
                    ret['message'] = 'data not found.'  
            else:
                ret['message']='please give proper input data id and imagename.'         
        else:
            ret['message'] = 'job sheet is not uploaded yet.'
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
    return ret
def NEWCAPTURPANELIMAGE( url):
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
                                    if type == 'ht' or type == 'HT':
                                        panel_detection_data = None#(panel_detection_function_for_image(detector,full_path1))
                                    else:
                                        panel_detection_data = None
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name, 'panel_detection': panel_detection_data}
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
                                    if type == 'ht' or type == 'HT':
                                        panel_detection_data = None#(panel_detection_function_for_image(detector,full_path1))
                                    else:
                                        panel_detection_data = None
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'image_name': name, 'panel_detection': panel_detection_data}
                                    break
                    count += 1
                else:
                    break
            cam.release()
            #cv2.destroyAllWindows()
    return verfy_rtsp_response




def CHECKRTSPISWORKING(Jobtype, camera_brand, camera_username, camera_password,  camera_ip_address):
    print("---------------------------999999999999993333333333333333",Jobtype, camera_brand, camera_username, camera_password,  camera_ip_address)
    data_append = []
    data = {}
    if camera_username == '':
        camera_username = 'admin'
    if camera_password == '':
        camera_password = 'TATA_tsk123'
    rtsp_url = ESIBRANDCAMERASRTSP(camera_ip_address,camera_brand,camera_username,camera_password)#create_rtsp(ipaddress)
    print('RTSP ------------------------------ ', rtsp_url)
    image_data = NEWCAPTURPANELIMAGE(rtsp_url)#verify_rtsp(detector,type, video_name, ipaddress, rtsp_url)

    print("-----file -------------------RTSP ---------------",rtsp_url)
    print('image_data', image_data)
    if type =='HT' or type =='ht': 
        if image_data is not None:
            data['ip_address'] = camera_ip_address
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if camera_ip_address is not None and camera_ip_address !='':
                camera_name= remove_all_specail_char_with_hifhen(camera_ip_address)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            panel_id_list_refer = 0
            if image_data['status'] == True:
                data['rtsp_status'] = image_data['status']
                data['image_name'] = image_data['image_name']
                data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            
            data['panel_data'] = data_append
            return data
        else:
            return None

    elif type =='Hydraulic' or type =='hydraulic' :
        if image_data is not None:
            data['ip_address'] = camera_ip_address
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if camera_ip_address is not None and camera_ip_address !='':
                camera_name= remove_all_specail_char_with_hifhen(camera_ip_address)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            if image_data['status'] == True:
                data['rtsp_status'] = image_data['status']
                data['image_name'] = image_data['image_name']
                data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            data['hydraulic_data'] =[]
            return data

    elif type =='pneumatic' or type =='Pneumatic' :
        if image_data is not None:
            data['ip_address'] = camera_ip_address
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if camera_ip_address is not None and camera_ip_address !='':
                camera_name= remove_all_specail_char_with_hifhen(camera_ip_address)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            if image_data['status'] == True:
                data['rtsp_status'] = image_data['status']
                data['image_name'] = image_data['image_name']
                data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            data['hydraulic_data'] =[]
            return data

    else:
        if image_data is not None:
            data['ip_address'] = camera_ip_address
            data['camera_brand'] = 'cp_plus'
            data['camera_id'] = None
            camera_name = 'docketrun'+'cp_plus'
            if camera_ip_address is not None and camera_ip_address !='':
                camera_name= remove_all_specail_char_with_hifhen(camera_ip_address)
            data['camera_name'] =camera_name
            data['rtsp_url'] = rtsp_url
            panel_key_id_list = []
            
            if image_data['status'] == True:
                data['rtsp_status'] = image_data['status']
                data['image_name'] = image_data['image_name']
                data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
            data['panel_data'] =[]
            return data


def Panel_NEWIMAGE(data):
    ifworked= 0
    newlapp =[]
    if 1:
    # try:
        NewDataOFall = list(mongo.db.panel_data.find({'ip_address':data['ip_address'] ,'job_sheet_name': data['job_sheet_name'], 'token': data['token']}, sort=[('_id',pymongo.DESCENDING)]))
        # if list(NewDataOFall) !=0:
            # for i , jjin in enumerate(NewDataOFall):
            #     newlapp.append(jjin['panel'])
        
        # data['all_panels']=data['feeder_number']
        if 'panel' in data:
            newlapp.append(data['panel'])
        elif 'feeder_number' in data:
            newlapp.append(data['feeder_number'])
        data['all_panels']=newlapp
        # if data['type']=='HT' or data['type']=='ht':
            #hydraulic_data

        if isEmpty(data['data']):
            if 'panel_data' in (data['data']) :
                if len(data['data']['panel_data']) != 0:
                    try :
                        ImageData=CHECKRTSPISWORKING(data['type'],data['camera_brand'],data['camera_username'],data['camera_password'], data['ip_address'])
                        if ImageData is not None:
                            
                            ifworked = 1
                            data['data']['image_name'] =  ImageData['image_name']
                            
                    except  KeyError as error :
                        print("KEYERROR---------11--",error)
                else:
                    try :
                        ImageData=CHECKRTSPISWORKING(data['type'],data['camera_brand'],data['camera_username'],data['camera_password'], data['ip_address'])
                        if ImageData is not None:
                            ifworked = 1
                            data['data']['image_name'] =  ImageData['image_name'] 
                    except  KeyError as error :
                        print("KEYERROR------222-----",error)
            elif 'hydraulic_data' in data['data']:
                if len(data['data']['hydraulic_data']) != 0:
                    try :
                        ImageData=CHECKRTSPISWORKING(data['type'],data['camera_brand'],data['camera_username'],data['camera_password'], data['ip_address'])
                        if ImageData is not None:
                            
                            ifworked = 1
                            data['data']['image_name'] =  ImageData['image_name']
                            
                    except  KeyError as error :
                        print("KEYERROR---------11--",error)
                else:
                    try :
                        ImageData=CHECKRTSPISWORKING(data['type'],data['camera_brand'],data['camera_username'],data['camera_password'], data['ip_address'])
                        if ImageData is not None:
                            ifworked = 1
                            data['data']['image_name'] =  ImageData['image_name'] 
                    except  KeyError as error :
                        print("KEYERROR------222-----",error)

            else:
                try :
                    ImageData=CHECKRTSPISWORKING(data['type'],data['camera_brand'],data['camera_username'],data['camera_password'], data['ip_address'])
                    if ImageData is not None:
                        ifworked = 1
                        data['data']['image_name'] =  ImageData['image_name'] 
                        data['data']['panel_data']=[]
                except  KeyError as error :
                    print("KEYERROR------222-----",error)
        else:
            print("data---------------data",data)    
            try :
                ImageData = CHECKRTSPISWORKING(data['type'],data['camera_brand'],data['camera_username'],data['camera_password'], data['ip_address'])  
                if ImageData is not None: 
                    ifworked = 1
                    data['data']=ImageData     
            except  KeyError as error :
                print("KEYERROR------333-----",error)    
        
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PANELWISEDATAWITH3343IDANDIMAGESNAME 1", str(error), " ----time ---- ", now_time_with_time()]))
    if ifworked : 
        return parse_json(data)
    else:
        return None

@dashboard.route('/recaptureImageJob/<id>', methods=['GET'])
def recaptureImageJob(id=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        sheet_data = mongo.db.job_sheet_details.find_one({},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            if id is not None :
                data = mongo.db.panel_data.find_one({'_id': ObjectId(id)}, sort=[('_id', pymongo.DESCENDING)])
                if data is not None:
                    return_data = Panel_NEWIMAGE(data)
                    if return_data is not None:
                        print("999999999999999988888888888888888888899999999999999999999999999999999")
                        result = mongo.db.panel_data.update_one({ '_id': ObjectId(id)},  {'$set': {"data":return_data['data']}})
                        print(result.matched_count)
                        # NewReturn= {'data':{'image_name':return_data['data']['image_name']}}
                        # print("-------NewReturn--",NewReturn)
                        if result.matched_count > 0:
                            #ret = {'message': 'image recaptured successfully.','success': True}
                            ret = {'message': return_data, 'success': True}
                        else:
                            ret['message'] ='something went wrong updating image.'
                    else:
                        ret['message'] ='rtsp is not working or something wrong with rtsp.'
                else:
                    ret['message'] = 'panel data not found.'   
            else:
                ret['message']='please give proper input data id and imagename.'         
        else:
            ret['message'] = 'job sheet is not uploaded yet.'
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
    return ret


@dashboard.route('/get_roi_image/<image_file>', methods=['GET'])
def get_roi_image_(image_file):
    try:
        base_path = os.path.join(os.getcwd(), 'rtsp_roi_image')
        response = send_from_directory(base_path, image_file)
        return response
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        # return str(error)
        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        main_path = os.path.abspath(path)
        return send_from_directory(main_path, filename)


@dashboard.route('/get_job_sheet_status', methods=['GET'])
@dashboard.route('/get_job_sheet_status/<id>', methods=['GET'])
def get_job_she333et_status_of_current(id = None):
    ret = {'message': 'Something went wrong with job sheet status api','success': False}
    if 1:
    # try:
        all_data = []
        sheet_data=None
        if id is not None:
            sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
        else:            
            sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            riro_return_data = []
            data1 = list(mongo.db.panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
            if len(data1) != 0:
                all_data =FUNCHECKrepeativeJobSheetstatus(data1)
                for ___12, iisddf in enumerate(all_data):
                    if iisddf['type']=="HT" or iisddf['type']=='ht':
                        find_riro_data = list(mongo.db.riro_data.find({'token': sheet_data['token'], 'camera_name': iisddf['data']['camera_name'], 'camera_rtsp': iisddf['data']['rtsp_url']}, sort=[ ('_id', pymongo.DESCENDING)]))
                        if len(find_riro_data) != 0:
                            check_data, panel_status, hello = riro_history_check_the_riro_data_with_sorting_(iisddf['data']['rtsp_url'], iisddf['data']['panel_data']['panel_id'], find_riro_data)
                            if panel_status or len(check_data) != 0:
                                if len(check_data) == 1:
                                    iisddf['sort_id'] = check_data[0]['sort_id']
                                    iisddf['data']['panel_data']['panel_status'] = panel_status
                                    iisddf['rack_method'] = check_data[0]['rack_method']
                                    iisddf['rack_process'] = check_data[0]['rack_process']
                                    iisddf['irrd_in_time'] = check_data[0]['irrd_in_time']
                                    iisddf['irrd_out_time'] = check_data[0]['irrd_out_time']
                                    iisddf['violation'] = check_data[0]['violation' ]
                                    iisddf['tag'] = check_data[0]['tag']
                                    iisddf['lock'] = check_data[0]['lock']
                                    iisddf['lock_time'] = check_data[0]['lock_time']
                                    iisddf['tag_time'] = check_data[0]['tag_time']
                                    iisddf['five_meter'] = check_data[0]['five_meter']
                                    iisddf['barricading'] = check_data[0]['barricading']
                                    iisddf['magnetic_flasher'] = check_data[0]['magnetic_flasher']
                                    iisddf['riro_key_id'] = check_data[0]['riro_key_id']
                                    iisddf['riro_merged_image'] = check_data[0]['riro_merged_image']
                                    iisddf['riro_merged_image_size'] = check_data[0]['riro_merged_image_size']
                                    iisddf['riro_edit_status'] = check_data[0]['riro_edit_status']
                                    iisddf['lock_tag_image'] = check_data[0]['lock_tag_image']
                                    iisddf['within_15_min']=check_data[0]['within_15_min']
                                    iisddf['remarks'] = check_data[0]['remarks']
                                if len(check_data) > 1:
                                    latest_riro_ = with_campare_time_and_get_latest_data_of_riro(check_data)
                                    if latest_riro_ is not None:
                                        iisddf['sort_id'] = latest_riro_['sort_id']
                                        iisddf['data']['panel_data']['panel_status' ] = panel_status
                                        iisddf['rack_method'] = latest_riro_['rack_method']
                                        iisddf['rack_process'] = latest_riro_['rack_process']
                                        iisddf['irrd_in_time'] = latest_riro_['irrd_in_time']
                                        iisddf['irrd_out_time'] = latest_riro_['irrd_out_time']
                                        iisddf['violation'] = latest_riro_['violation']
                                        iisddf['tag'] = latest_riro_['tag']
                                        iisddf['lock'] = latest_riro_['lock']
                                        iisddf['lock_time'] = check_data[0]['lock_time']
                                        iisddf['tag_time'] = check_data[0]['tag_time']
                                        iisddf['five_meter'] = latest_riro_['five_meter']
                                        iisddf['barricading'] = latest_riro_['barricading']
                                        iisddf['magnetic_flasher'] = latest_riro_['magnetic_flasher']
                                        iisddf['riro_key_id'] = latest_riro_['riro_key_id']
                                        iisddf['riro_merged_image'] = latest_riro_['riro_merged_image']
                                        iisddf['riro_merged_image_size' ] = latest_riro_['riro_merged_image_size']
                                        iisddf['riro_edit_status'] = latest_riro_['riro_edit_status']
                                        iisddf['lock_tag_image'] = latest_riro_['lock_tag_image']
                                        iisddf['within_15_min']=latest_riro_['within_15_min']
                                        iisddf['remarks'] = latest_riro_['remarks']
                            else:
                                iisddf['sort_id'] = None
                                iisddf['rack_method'] = None
                                iisddf['rack_process'] = None
                                iisddf['irrd_in_time'] = None
                                iisddf['irrd_out_time'] = None
                                iisddf['violation'] = False
                                iisddf['tag'] = None
                                iisddf['lock'] = None
                                iisddf['lock_time'] = None
                                iisddf['tag_time'] = None
                                iisddf['five_meter'] = None
                                iisddf['barricading'] = None
                                iisddf['magnetic_flasher'] = None
                                iisddf['riro_key_id'] = None
                                iisddf['riro_merged_image'] = None
                                iisddf['riro_merged_image_size'] = {'height': None, 'width': None}
                                iisddf['riro_edit_status'] = False
                                iisddf['lock_tag_image'] = None
                                iisddf['within_15_min']= None
                                iisddf['remarks'] = ''
                        else:
                            iisddf['sort_id'] = None
                            iisddf['rack_method'] = None
                            iisddf['rack_process'] = None
                            iisddf['irrd_in_time'] = None
                            iisddf['irrd_out_time'] = None
                            iisddf['violation'] = False
                            iisddf['tag'] = None
                            iisddf['lock'] = None
                            iisddf['lock_time'] = None
                            iisddf['tag_time'] = None
                            iisddf['five_meter'] = None
                            iisddf['barricading'] = None
                            iisddf['magnetic_flasher'] = None
                            iisddf['riro_key_id'] = None
                            iisddf['riro_merged_image'] = None
                            iisddf['riro_merged_image_size'] = {'height': None,'width': None}
                            iisddf['riro_edit_status'] = False
                            iisddf['lock_tag_image'] = None
                            iisddf['within_15_min']= None
                            iisddf['remarks'] = ''
                    else:
                        iisddf['sort_id'] = None
                        iisddf['rack_method'] = None
                        iisddf['rack_process'] = None
                        iisddf['irrd_in_time'] = None
                        iisddf['irrd_out_time'] = None
                        iisddf['violation'] = False
                        iisddf['tag'] = None
                        iisddf['lock'] = None
                        iisddf['lock_time'] = None
                        iisddf['tag_time'] = None
                        iisddf['five_meter'] = None
                        iisddf['barricading'] = None
                        iisddf['magnetic_flasher'] = None
                        iisddf['riro_key_id'] = None
                        iisddf['riro_merged_image'] = None
                        iisddf['riro_merged_image_size'] = {'height': None,'width': None}
                        iisddf['riro_edit_status'] = False
                        iisddf['lock_tag_image'] = None
                        iisddf['within_15_min']=None
                        iisddf['remarks'] = ''
                    if 'ip_address' in iisddf.keys():
                        del iisddf['ip_address']
                    riro_return_data.append(iisddf)
                all_data = riro_return_data
                rack_method_done_count = 0
                rack_method_not_done_count = 0
                total_panel_count = 0
                pending_rack_ou_count = 0
                if len(riro_return_data) != 0:
                    for singsing, xml_to in enumerate(riro_return_data):
                        total_panel_count += 1
                        if xml_to['type']=="HT" or xml_to['type']=='ht':
                            if xml_to['data']['panel_data']['panel_status']:
                                rack_method_done_count += 1
                            else:
                                rack_method_not_done_count += 1
                                if xml_to['rack_process'] is not None :
                                    if xml_to['rack_process'] =='rack_out':
                                        pending_rack_ou_count +=1
                        else:
                            rack_method_not_done_count += 1
                    final_data = {'total_panel_count': total_panel_count,'processed_count': rack_method_done_count,'not_processed': rack_method_not_done_count,'rack_out_count':pending_rack_ou_count}
                    ret = {'message': final_data, 'success': True}
                else:
                    ret['message'] = 'data not found.'
            else:
                ret['message'] = 'panel_data is not found.'
        else:
            ret['message'] = 'job sheet is not uploaded yet'

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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_job_she333et_status 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message'] =" ".join(["something error has occered in api", str(error)])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_job_she333et_status 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return ret



@dashboard.route('/get_samplefile', methods=['GET'])
def get_obj_img():
    try:
        base_path = os.path.join(os.getcwd(), 'smaple_files')
        file_path = os.path.basename('sample_file.xlsx')
        response = send_from_directory(base_path, file_path, as_attachment=True)
        return response
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_samplefile 1", str(error), " ----time ---- ", now_time_with_time()]))         
        return str(error)
    
@dashboard.route('/riro_image/<image_file>', methods=['GET'])
def get_img_bbox_riro(image_file):
    try:
        image_data = mongo.db.riro_data.find_one({'riro_merged_image':image_file})
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'RIRO_merged_imgs')
            return send_from_directory(base_path, image_file)
        else:
            return 'image is not found'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_image 1", str(error), " ----time ---- ", now_time_with_time()]))
        
        
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_image 2", str(error), " ----time ---- ", now_time_with_time()]))         
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])


@dashboard.route('/taglock_image/<image_file>', methods=['GET'])
def taglock_image(image_file):
    # if 1:
    try:
        image_data = mongo.db.riro_data.find_one({'cropped_panel_image_path': image_file})
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'lock_tag_images')
            return send_from_directory(base_path, image_file)
        else:
            return 'image is not found'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- taglock_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        
        
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- taglock_image 2", str(error), " ----time ---- ", now_time_with_time()]))         
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])



@dashboard.route('/fivemeter_image/<image_file>', methods=['GET'])
def fivemeter_image(image_file):
    try:
        base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
        return send_from_directory(base_path, image_file)
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- fivemeter_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])


@dashboard.route('/magneticflasher_image/<image_file>', methods=['GET'])
def magneticflasher_image(image_file):
    try:
        base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'flasher_croped_images')
        return send_from_directory(base_path, image_file)
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- magneticflasher_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])




def MECHANICALRTSP( id,url):
    response = True
    verfy_rtsp_response = None
    if response:
        directory_path = os.path.join(os.getcwd(), "Mechanicalrtsp_roi_image")
        if not os.path.exists(directory_path):
            handle_uploaded_file(directory_path)
        present_time = replace_spl_char(str(datetime.now()))
        cam = cv2.VideoCapture(url)
        full_path = None
        if cam.isOpened() == True:
            name = id + '_' + present_time + '.jpg'
            while cam.isOpened():
                ret, frame = cam.read()
                if ret:
                    full_path = directory_path + '/' + name
                    cv2.imwrite(full_path, frame)
                    verfy_rtsp_response = {'image_name':name}               
                    break
                else:
                    break
            cam.release()
            #cv2.destroyAllWindows()
        else:
            print('stream is not able to fetch--- ')
    else:
        verfy_rtsp_response = None
    return verfy_rtsp_response

## done for object
@dashboard.route('/check_mechanical_job', methods=['POST'])
def mechanical_job_():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['id',  'rtsp_url']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                id = jsonobject['id']
                rtsp_url = jsonobject['rtsp_url']
                if id is not None:
                    if rtsp_url is not None:
                        function_response = MECHANICALRTSP( id,rtsp_url)
                        if function_response is not None:
                            image_name = function_response['image_name']
                            ret['message']= {'image_name':image_name,'timestamp':now_time_with_time()}
                            result= mongo.db.mechanical_jobs.insert_one({'image_name':image_name,'timestamp':now_time_with_time(),'reference_id':id,'rtsp_url':rtsp_url})
                            if result.acknowledged:
                                ret = {'success': True, 'message':{'image_name':image_name,'timestamp':now_time_with_time(),'id':id}}
                            else:
                                ret['message']='not able insert the data into database'
                        else:
                            ret['message']='rtsp is not working.'
                    
                    else:
                        ret['message']= 'rtsp url should not be none.'
                else:
                    ret['message']= 'mongoid should not be none.'  
        else:
            ret['message']='you have missed keys '+str(missing_key) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_mech222anical_job 1", str(error), " ----time ---- ", now_time_with_time()]))
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_mech222anical_job 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret

## done for object
@dashboard.route('/mech_jobimage/<image_file>', methods=['GET'])
def mech_jobimage(image_file):
    try:
        base_path = os.path.join(os.getcwd(), 'Mechanicalrtsp_roi_image')
        response = send_from_directory(base_path, image_file)
        return response
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- mech_jobimage 1", str(error), " ----time ---- ", now_time_with_time()]))       
        return str(error)

#done for object
@dashboard.route('/delete_mechanical_job/<id>', methods=['GET'])
def mechanical_job_delete(id=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    try: 
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            if id is not None:
                find_result= mongo.db.panel_data.find_one({'_id': ObjectId(id),'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']})
                if find_result is not None:
                    result = mongo.db.panel_data.delete_one({'_id': ObjectId(find_result['_id'])})
                    if result.deleted_count > 0:
                        ret = {'message': 'job deleted successfully.','success': True}
                    else:
                        ret['message'] ='job is not deleted ,due to something went wrong with database.'
                else:
                    ret['message'] = 'job is not found for this mongoid.'
            else:
                ret['message']= 'mongoid should not be none.'  
        else:
            ret['message']='job sheet is not yet uploaded.'   
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 1", str(error), " ----time ---- ", now_time_with_time()]))   
        ret['message'] =" ".join(["something error has occered in api", str(error)])      
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")               
    except Exception as  error:
        ret = {'success': False, 'message': str(error)}
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return ret

def hydralockdataHISTORYFetch(hydra_data):
    only_two_data =[]
    if hydra_data['type']=='hydraulic' or hydra_data['type']=='pneumatic' or hydra_data['type']=='Hydraulic' or hydra_data['type']=='Pneumatic':
        FINDHYDRADATA= list(mongo.db.hydra_data.find({'camera_rtsp':hydra_data['data']['rtsp_url'],"camera_name":hydra_data['data']['camera_name']}, sort=[('_id',   pymongo.DESCENDING)]))
        if len(FINDHYDRADATA) != 0 :
            newlist = sorted(FINDHYDRADATA, key=lambda d: d['_id']) 
            for u,i in enumerate(newlist):
                only_two_data.append(i)    
    return only_two_data  



@dashboard.route('/hydra_history', methods=['POST'])
def hydra_pneumatic_histroy():
    ret = {'success': False, 'message':'Something went wrong in hydra_history, please try again later'}
    # if 1:
    try:        
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = [ 'id', 'imagename']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                imagename = jsonobject['imagename']
                id = jsonobject['id']
                all_data = []
                if id is not None:
                    data = mongo.db.mechesi.find_one({'_id': ObjectId(id)})
                    if data is not None:
                        if isEmpty(data['data'])  :
                            hydrahistory=hydralockdataHISTORYFetch(data)
                            if len(hydrahistory) != 0 :
                                ret['message'] = parse_json(hydrahistory)
                                ret['success'] = True
                            else:
                                ret['message'] ='lock history is not found for this hydraulic data.'
                        else:
                            ret['message']='hydraulic data is not found.'
                    else:
                        ret['message']='hydraulic data is not found.'
                else:
                    ret['message'] ='mongo id  should not be none, please enter the proper mongo id.'
        else:
            ret = {'message': 'parameters missing file {0}'.format(missing_key), 'success': False}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- hydra_history 1", str(error), " ----time ---- ", now_time_with_time()]))   
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ret['message'] = str(error)
        ret['success'] = False
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- hydra_history 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return ret


@dashboard.route('/hydralockimage/<image_file>', methods=['GET'])
def HYRAIMAGElocktageimage(image_file):
    try:
        if image_file is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'hydra')
            return send_from_directory(base_path, image_file)
        else:
            return 'image is not found'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- hydralockimage 1", str(error), " ----time ---- ", now_time_with_time()])) 
        
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")
                " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- hydralockimage 2", str(error), " ----time ---- ", now_time_with_time()]))        
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])


@dashboard.route('/delete_hydradata/<key_id>', methods=['GET'])
def delete_HYDRAdata_key_id_wise(key_id=None):
    ret = {'message': 'something error occured in delte_riro_data.','success': False}
    try:
        if key_id is not None:
            find_delete_data = mongo.db.hydra_data.find_one({'modify_key': key_id})
            if find_delete_data is not None:
                print('hydra data delete --- object id ', find_delete_data['_id'])
                result = mongo.db.hydra_data.delete_one({'_id': ObjectId(find_delete_data['_id'])})
                if result.deleted_count > 0:
                    ret = {'message': 'hydra data deleted successfully.','success': True}
                else:
                    ret['message'] ='hydra data is not deleted ,due to something went wrong with database.'
            else:
                ret['message' ] = 'hydra data is not found for this id, please try once again.'
        else:
            ret['message' ] = '  hydra data key id is None type please give proper riro key id.'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_hydradata 1", str(error), " ----time ---- ", now_time_with_time()]))        
        ret['message' ] =" ".join(["something error has occered in api", str(error) , '  ----time ----   ',now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ret['message' ] =" ".join(["something error has occered in api", str(error)])
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_hydradata 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@dashboard.route('/fetchdataflasher', methods=['GET'])
@dashboard.route("/fetchdataflasher/<ipaddress>/<panelnumber>",methods =['GET'])
@dashboard.route('/fetchdataflasher/<panelnumber>', methods=['GET'])
def Fetch_flasherdata(ipaddress=None,panelnumber=None):
    ret = {'message': 'something error occured in fetchdataflasher.','success': False}
    try:
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            print("panelnumber ====",panelnumber)
            print("ipaddress ====",ipaddress)
            if panelnumber is not None and ipaddress is not None: 
                find_delete_data =list( mongo.db.flasherlogdata.find({'token': sheet_data['token'],"ip_address":ipaddress,'panel_number': panelnumber},sort=[('_id', pymongo.DESCENDING)]).limit(30))        
                if len(find_delete_data) !=0 :
                    ret= {"message":parse_json(find_delete_data),"success":True}
                else:
                    ret['message' ] = 'there is no flasher data found for this panel_number.'
            elif ipaddress is not None: 
                find_delete_data = list(mongo.db.flasherlogdata.find({'token': sheet_data['token'],"ip_address":ipaddress},sort=[('_id', pymongo.DESCENDING)]).limit(30))         
                if len(find_delete_data) !=0 :
                    ret= {"message":parse_json(find_delete_data),"success":True}
                else:
                    ret['message' ] = 'there is no flasher data found for this panel_number.'  
            else:
                find_delete_data = list(mongo.db.flasherlogdata.find({'token': sheet_data['token']},sort=[('_id', pymongo.DESCENDING)]).limit(30))
                if len(find_delete_data) !=0 :
                    ret = { "message":parse_json(find_delete_data),"success":True}
                else:
                    ret['message']='magnetic sticker data not found.'
        else:
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'

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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- fetchdataflasher 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = " ".join([ "something error has occered in   2", str(error)])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ret['message']=" ".join(["something error has occered in api", str(error)])  
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- fetchdataflasher 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


#done for object
@dashboard.route('/delete_ht_job/<id>', methods=['GET'])
def HTjob_delete(id=None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    try: 
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            if id is not None:
                find_result= mongo.db.panel_data.find_one({'_id': ObjectId(id),'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']})
                if find_result is not None:
                    result = mongo.db.panel_data.delete_one({'_id': ObjectId(find_result['_id'])})
                    if result.deleted_count > 0:
                        ret = {'message': 'job deleted successfully.','success': True}
                    else:
                        ret['message'] ='job is not deleted ,due to something went wrong with database.'
                else:
                    ret['message'] = 'job is not found for this mongoid.'
            else:
                ret['message']= 'mongoid should not be none.'  
        else:
            ret['message']='job sheet is not yet uploaded.'   
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 1", str(error), " ----time ---- ", now_time_with_time()]))   
        ret['message'] =" ".join(["something error has occered in api", str(error)])      
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")               
    except Exception as  error:
        ret = {'success': False, 'message': str(error)}
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return ret



@dashboard.route('/unplanned_data', methods=['GET'])
@dashboard.route('/unplanned_data/<id>', methods=['GET'])
def UnplannedRIRODATA(id= None):
    if 1:
    # try:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        sheet_data  = None
        if id is not None:
            sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])    
        else:
            sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            data = list(mongo.db.riro_unplanned.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, {'cameraid':0,'analytics_id':0,'cropped_panel_image_path':0,'five_meter':0,
                                                                                                                                    'flasher_status':0,'appruntime':0,'appruntime':0,'id':0,'barricading':0,'date':0,'riro_merged_image':0,'riro_merged_image_size':0,
                                                                                                                                    'lock':0,'lock_time':0,'magnetic_flasher':0,'person_in_time':0,'person_out_time':0,'within_15_min':0,'tag':0,'tag_time':0},sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0: 
                ret['message']=data
                ret['success']=True
                ret['job_sheet_status']=True
            else:
                ret['message'] = 'there is no data found for unplanned jobs'
                ret['job_sheet_status'] = True
        else:
            ret['message'] ="jobsheet is not yet uploaded, please upload the jobsheet"
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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 2", str(error), " ----time ---- ", now_time_with_time()]))
    return parse_json(ret)


def PROPERFORMATE(input_data,jobsheettagnames):
    print("length ---tagnames ==",len(jobsheettagnames))
    finaloutputformat={'i_time':input_data['i_time'],'l1data':[]}
    output_data=[]
    lasttime =input_data['i_time']
    for key, value in input_data.items():
        if key not in ["i_time", "index", "local_time"]:    
            tagname = key
            for JobSheetTag in jobsheettagnames:
                if tagname == JobSheetTag:
                    if value == 2:
                        isolation_status = "live"
                    elif value == 1:
                        isolation_status = "isolated"
                    else :
                        isolation_status ="unknown"
                    entry = {"tagname": tagname, "isolation_status": isolation_status, "value": value}
                    if entry  not in  output_data:
                        output_data.append(entry)
                # else:
                #     if JobSheetTag not in list(input_data.keys()):
                #         entry = {"tagname": JobSheetTag, "isolation_status": "unknown", "value": value}
                #         if entry  not in  output_data:
                #             output_data.append(entry)


    finaloutputformat['l1data']=output_data
    return finaloutputformat

def GetthejobshettTagnames():
    Tagnamelist =[]
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])     
    if sheet_data is not None:
        #field: { $type: [ <BSON type1> , <BSON type2>, ... ] } 
        data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],'type':{"$in":['ht','HT']}}, sort=[('_id',   pymongo.DESCENDING)]))
        if len(data) !=0:
            for i , tagnamedata in enumerate(data):
                if 'tagname' in tagnamedata and tagnamedata['tagname'] is not None and tagnamedata['tagname'] !='':
                    Tagnamelist.append(tagnamedata['tagname'])
        else:
            print("data ===", data)
    else:
        print("while geting l1 data === ,",sheet_data)
    return Tagnamelist
@dashboard.route('/GetL1dataofHT', methods=['GET'])
def FETCHL1dataofHT():
    ret={'message':"something wrong with Getl1dataofHT ",'success':False} 
    database_detail = {'sql_panel_table':'testopc', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrunopc', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as  error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- GetL1dat33333aofHT 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
        ret['message']=str(error)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY i_time desc')
    except psycopg2.errors.UndefinedTable as error:
        ret['mesPROPERFORMATEsage']=str(error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- GetL1da3333taofHT 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ret['message']=str(error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- GetL1dat3343aofHT 3", str(error), " ----time ---- ", now_time_with_time()]))
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    res = None
    if l1data_row is not None: 
        res = dict(zip(cols_name, list(l1data_row)))
        print('L1 == data ', res)
        # print("l1 ", l1data_row)
        if res is not None:
            # print(PROPERFORMATE(res))
            TAGNAMES = GetthejobshettTagnames()
            # print('GetthejobLISTshettTagnames',GetthejobshettTagnames())
            ret={'message':PROPERFORMATE(res,TAGNAMES),'success':True}
        else:
            ret['message']='l1 of HT is not found in table, please verify.'
    else:
        ret['message']='l1 of HT is not found in table, please verify.'        
    return parse_json(ret)





def UnplannedRIROLivecount(live_data_count, all_data):
    try:
        data = mongo.db.unplanedLivecount.find_one()
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
            result = mongo.db.unplanedLivecount.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.unplanedLivecount.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- UnplannedL(((ivecount 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30




@dashboard.route('/GetUnplannedLivecount', methods=['GET'])
def GetUnplannedFORRIROLivecount():
    if 1:
    # try:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            data = list(mongo.db.riro_unplanned.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, {'cameraid':0,'analytics_id':0,'panel_no':0,'cropped_panel_image_path':0,'five_meter':0,
                                                                                                                                    'flasher_status':0,'appruntime':0,'appruntime':0,'id':0,'barricading':0,'date':0,'riro_merged_image':0,'riro_merged_image_size':0,
                                                                                                                                    'lock':0,'lock_time':0,'magnetic_flasher':0,'person_in_time':0,'person_out_time':0,'within_15_min':0,'tag':0,'tag_time':0},sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0:                 
                ret=UnplannedRIROLivecount(len(data), data)
            else:
                ret['message'] = 'there is no data found for unplanned jobs'
        else:
            ret['message'] ="jobsheet is not yet uploaded, please upload the jobsheet"
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
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as  error:
    #     ret['message'] = str(error)
    #     ret['success'] = False
    #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 2", str(error), " ----time ---- ", now_time_with_time()]))
    return parse_json(ret)





@dashboard.route('/delete_unplannedRiro/<key_id>', methods=['GET'])
def DELETEUNPLANNEDRIRODATA(key_id=None):
    ret = {'message': 'something error occured in delte_riro_data.','success': False}
    try:
        if key_id is not None:
            find_delete_data = mongo.db.riro_unplanned.find_one({'riro_key_id': key_id})
            if find_delete_data is not None:
                result = mongo.db.riro_unplanned.delete_one({'_id': ObjectId(find_delete_data['_id'])})
                if result.deleted_count > 0:
                    ret = {'message': 'riro_data deleted successfully.','success': True}
                else:
                    ret['message'] ='riro_data is not deleted ,due to something went wrong with database.'
            else:
                ret['message' ] = '  riro_data is not found for this id, please try once again.'
        else:
            ret['message' ] = '  riro key id is None type please give proper riro key id.'
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



@dashboard.route('/edit_UnplannedRIROData', methods=['POST'])
def edit_UnplannedRIROData():
    ret = {'message': 'something error occured in edit_riro_data.','success': False}
    try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['data']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                data_122 = jsonobject['data']
                if isEmpty(data_122):
                    key_in_riro_data = ['riro_key_id', 'rack_process','remarks','panel_no']#,'rack_method', 'irrd_in_time', 'tag', 'lock', 'remarks','five_meter', 'barricading', 'magnetic_flasher']
                    if data_122['riro_key_id'] is not None:
                        if check_the_data_keys(key_in_riro_data, data_122.keys()):
                            print('all_input keys are there--- ')
                            print('the all items()', data_122.items())
                            checking_the_empty = [k for k, v in data_122.items() if v == '']
                            check_the_none_values = [k for k, v in data_122.items() if v is None]
                            if len(checking_the_empty) == 0 and len(check_the_none_values) == 0:
                                find_edit_data = mongo.db.riro_unplanned.find_one({ 'riro_key_id': data_122['riro_key_id']})
                                if find_edit_data is not None:
                                    # print('find_edit data ===', find_edit_data)
                                    # try:
                                    #     if 'five_meter' in data_122.keys():
                                    #         data_122['five_meter'] = {'violation':data_122['five_meter']}
                                    # except Exception as  error:
                                    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- edit_riro_data 1", str(error), " ----time ---- ", now_time_with_time()]))
                                    # print('final data updating -- data_122', type(data_122))
                                    # data_122['riro_edit_status'] = True
                                    # if dictionary_key_exists(data_122,'rack_process') and (dictionary_key_exists(data_122,'tag') or dictionary_key_exists(data_122,'lock') ):
                                    #     if data_122['rack_process']=='rack_out' and ((data_122['tag']=='untag') or (data_122['lock']=='unlock')):
                                    #         data_122['datauploadstatus']=0
                                    daata = data_122
                                    print('final data ==== ', daata)
                                    result = mongo.db.riro_unplanned.update_one({ '_id': ObjectId(find_edit_data['_id'])},  {'$set': daata})
                                    print(result.matched_count)
                                    if result.matched_count > 0:
                                        ret = {'message': 'riro data updated successfully.','success': True}
                                    else:
                                        ret['message'] ='something went wrong updating the riro data.'
                                else:
                                    ret['message'] ='riro data is not found this riro key id, please try different key id.'
                            elif len(checking_the_empty) != 0 and len(check_the_none_values) != 0:
                                ret['message'] =('parameters are empty  {0} , and some parameters are none {1}'.format(checking_the_empty,check_the_none_values))
                            elif len(checking_the_empty) != 0:
                                ret['message']  = 'parameters are empty  {0}'.format(checking_the_empty)
                            elif len(check_the_none_values) != 0:
                                ret['message'] = 'parameters are none  {0}'.format(check_the_none_values)
                            else:
                                ret['message'] = 'parameters not matches.'
                        else:
                            print('----- all input keys are not there ')
                            ret['message'] =' all input keys are not there and should not be none, please give proper riro data.'
                    else:
                        ret['message'] ='riro key id should not be none, please give proper riro key id.'
                else:
                    ret['message' ] = '  riro edit data is empty, please give proper data.'
        else:
            ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- edit_riro_data 3", str(error), " ----time ---- ", now_time_with_time()]))        
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- edit_riro_data 3", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@dashboard.route('/DeleteFeedernumber', methods = ['POST'])
def DeleteFeedernumber():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['riro_key_id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['riro_key_id']
            if id is not None:
                find_edit_data = mongo.db.riro_unplanned.find_one({ 'riro_key_id': jsonobject['riro_key_id']})
                if find_edit_data is not None: 
                #sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                # if sheet_data is not None:
                    result = mongo.db.riro_unplanned.update_one({ '_id': ObjectId(find_edit_data['_id'])},  {'$set': {"panel_no":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'feeder number is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong with deleting feeder number.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                          
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)


@dashboard.route('/Unplannedriroimage/<image_file>', methods=['GET'])
def Unplannedriroimage(image_file):
    try:
        if image_file is not None:
            try :
                base_path =os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'RIRO')
                return send_from_directory(base_path, image_file)
            except:
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)
        else:
            return 'image name should not be None'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_image 1", str(error), " ----time ---- ", now_time_with_time()]))
        # ret['message'] =" ".join(["something error has occered in api", str(error)])
        
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- riro_image 2", str(error), " ----time ---- ", now_time_with_time()]))         
        return " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    
    
@dashboard.route('/GetShutdownname', methods = ['GET'])
def GetShutdownname(id=None):
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    sheet_data = None
    if id is not None: 
        sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
    else:            
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
    if sheet_data is not None:
        ret = {"message":sheet_data, "success":True}
    else:
        ret['message']='job sheet not uploaded please upload it.'
    return parse_json(ret)
    
@dashboard.route('/UpdateShutdownname', methods = ['POST'])
def UpdateShutdownname():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['shutdownname','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            shutdownname = jsonobject['shutdownname']
            id = jsonobject['id']
            sheet_data =None
            if id is not None: 
                sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            else:
                sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
            if sheet_data is not None:
                result = mongo.db.job_sheet_details.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"shutdownname":shutdownname}})
                print(result.matched_count)
                if result.matched_count > 0:
                    ret = {'message': 'shutdown name is pdated successfully.','success': True}
                else:
                    ret['message'] ='something went wrong updating shutdown name.'
            else:
                ret['message']='job sheet not uploaded please upload it.'
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



@dashboard.route('/RiroUnplannedviolation_verification/<id>/<flag>', methods=['GET'])
def verification_of_violation(id=None, flag=0):
    ret = {'message': 'something went wrong with violation status .','success': False}
    try:
        if id is not None:
            if flag is not None:
                if flag != 'undefined':
                    find_data = mongo.db.riro_unplanned.find_one({'_id': ObjectId(id)})
                    if find_data is not None:
                        if flag == 'false':
                            print("flag====111",flag)
                            result = mongo.db.riro_unplanned.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False, 'violation_verificaton_status': True}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.','success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        elif flag == 'true':
                            print("flag====112",flag)
                            result = mongo.db.riro_unplanned.update_one({'_id':ObjectId(id)}, {'$set':{ 'violation_status': True,'violation_verificaton_status': True}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status already updated successfully.' , 'success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        else:
                            print("flag====132",flag)
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





@dashboard.route('/UnplannedJobscreate_excel', methods=['GET'])
@dashboard.route('/UnplannedJobscreate_excel/<id>', methods=['GET'])
def UNplanned_excelSheetGeneration(id = None):
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        sheet_data=None
        if id is not None:
            sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
        else:            
            sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            #'violation_status':True
            data = list(mongo.db.riro_unplanned.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, {'cameraid':0,'analytics_id':0,'cropped_panel_image_path':0,'five_meter':0,
                                                                                                                                    'flasher_status':0,'appruntime':0,'appruntime':0,'id':0,'barricading':0,'date':0,'riro_merged_image':0,'riro_merged_image_size':0,
                                                                                                                                    'lock':0,'lock_time':0,'magnetic_flasher':0,'person_in_time':0,'person_out_time':0,'within_15_min':0,'tag':0,'tag_time':0},sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0 : 
                print("LENGTH OF UNPLANNED JOBS ===",len(data)) 
                response = TSKNEWUNPLANNED(data)  
                print("TSKNEWUNPLANNED(data)========",response)  
                ret =response#TSKNEWUNPLANNED(data)
            else:
                ret['message'] = 'panel data not found'
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create22_excel 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ret['success'] = False
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_33excel 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret





@dashboard.route('/Unplannedexcel_download', methods=['GET'])
def UNPLANNED_JOBS_SHEET():
    try:
        list_of_files = glob.glob(os.path.join(os.getcwd(), "UNPLANNED_JOBS_SHEET/*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        path, filename = os.path.split(latest_file)
        if filename:
            main_path = os.path.abspath(path)
            response = make_response(send_from_directory(main_path, filename, as_attachment=True, download_name=filename))
            response.headers['Excel_filename'] = filename
            return response
        else:
            return {'success': False, 'message': 'File is not found.'}
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- excel_download", str(error), " ----time ---- ", now_time_with_time()]))
        return {'success': False, 'message': str(error)}


def TSKNEWUNPLANNED(list1):
    if 1:
    # try:
        print("SHEET123===",len(list1))
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = "_".join(["UNPLANNED_JOBSHEET", now.strftime('%m-%d-%Y-%H-%M-%S'), '.xlsx'])#os.path.join("ESI_MONITORING_", now.strftime('%m-%d-%Y-%H-%M-%S'),'.xlsx')#"_".join(["ESI_MONITORING_", now.strftime('%m-%d-%Y-%H-%M-%S'), '.xlsx'])
        create_multiple_dir(os.path.join(os.getcwd(), "UNPLANNED_JOBS_SHEET"))
        filename =os.path.join(os.getcwd(), "UNPLANNED_JOBS_SHEET", excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('UNPLANNED JOBS DATA')
        worksheet.set_column('A:E', 20)
        worksheet.set_column(3,3, 35)       
        worksheet.set_column(7, 7, 30)
        worksheet.set_column(8, 8, 30)
        worksheet.set_column(9, 9, 30)
        worksheet.set_column(10, 10, 30)
        worksheet.set_column(11, 11, 30)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(35)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd(), "smaple_files",'Docketrun_logo.png'), {'x_scale': 0.49, 'y_scale': 0.46})
        worksheet.write('B1', 'UNPlANNED JOBS DATA', cell_format)
        worksheet.merge_range('B1:L1', 'UNPlANNED JOBS DATA', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'Job Type', cell_format_1)
        worksheet.write(row, col + 1, 'Department', cell_format_1)
        worksheet.write(row, col + 2, 'Sub Area', cell_format_1)
        worksheet.write(row, col + 3, 'Feeder Number', cell_format_1)
        worksheet.write(row, col + 4, 'IP Address', cell_format_1)
        worksheet.write(row, col + 5, 'BEFORE IMAGE ', cell_format_1)
        worksheet.write(row, col + 6, 'AFTER IMAGE', cell_format_1)
        worksheet.write(row, col + 7, 'Method of Rack in/out', cell_format_1)
        worksheet.write(row, col + 8, 'IRRD IN TIME ', cell_format_1)
        worksheet.write(row, col + 9, 'IRRD OUT TIME ', cell_format_1)
        worksheet.write(row, col + 10, 'RACK PROCESS', cell_format_1)
        worksheet.write(row, col + 11, 'Remarks', cell_format_1)
        cell_format_2 = workbook.add_format()
        cell_format_2.set_font_name('Calibri')
        cell_format_2.set_align('center_across')
        format2 = workbook.add_format({'bg_color': '#C6EFCE', 'font_color':'#006100'})
        cell_format_3 = workbook.add_format()
        cell_format_3.set_font_name('Calibri')
        cell_format_3.set_align('center_across')
        cell_format_3.set_bg_color('red')
        cell_format_4 = workbook.add_format()
        cell_format_4.set_font_name('Calibri')
        cell_format_4.set_align('center_across')
        cell_format_4.set_bg_color('#FFFF00')
        cell_format_5 = workbook.add_format()
        cell_format_5.set_font_name('Calibri')
        cell_format_5.set_align('center_across')
        cell_format_5.set_bg_color('green')
        text_wrap = workbook.add_format({'valign': 'center_across'})
        rows = 2
        cols = 0
        cols1 = 1
        cols2 = 2
        cols3 = 3
        cols4 = 4
        cols5 = 5
        cols6 = 6
        cols7 = 7
        cols8 = 8
        cols9 = 9
        cols10 = 10
        cols11 = 11
        cols12 = 12
        cols13 = 13
        cols14 = 14
        cols15 = 15
        cols16 = 16
        cols17 = 17
        cols18 = 18
        cols19 = 19
        cols20 = 20
        cols21 = 21
        cols22 = 22
        cols23 = 23
        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0
        for hello, ikim in enumerate(list1):
            if cols == 0:
                worksheet.write(rows, cols, ikim['type'], cell_format_2)
            if cols1 == 1:
                worksheet.write(rows, cols1, ikim['department'], cell_format_2)
            if cols2 == 2:
                try :
                    worksheet.write(rows, cols2, ikim['sub_area'], cell_format_2)
                except :
                    worksheet.write(rows, cols2, ikim['area'], cell_format_2)
            if cols3 == 3:
                try:                    
                    worksheet.write(rows, cols3, ikim['panel_no'], cell_format_2)
                except :
                    worksheet.write(rows, cols3, '-----', cell_format_2)
            if cols4 ==4 :
                worksheet.write(rows, cols4, ikim['ip_address'],cell_format_2)  
            if cols5 ==5 :
                if ikim['riro_image'] is not None: 
                    if 'Before' in    ikim['riro_image']:                
                        if ikim['riro_image']['Before'] is not None:
                            try:
                                verify_img = Image.open(get_current_dir_and_goto_parent_dir() + '/images/RIRO' +'/' + ikim['riro_image']['Before'])
                                verify_img.verify()
                                worksheet.set_column(5, 5,40)
                                worksheet.set_row(rows, 180)
                                # worksheet.insert_image(rows, cols5, get_current_dir_and_goto_parent_dir() + '/images/RIRO' + '/' + str(ikim['riro_image']['Before']), {
                                #                         'x_scale': 0.3,
                                #                         'y_scale': 0.4,
                                #                         'x_offset': (worksheet.default_col_width / 2) - ((0.3 * 96) / 2), 
                                #                         'y_offset': (worksheet.default_row_height / 2) - ((0.4 * 96) / 2),
                                #                     })
                                worksheet.insert_image(rows, cols5, get_current_dir_and_goto_parent_dir() + '/images/RIRO' + '/' + str(ikim['riro_image']['Before']),{'x_scale': 0.29, 'y_scale': 0.37})#{'x_scale': width_scale, 'y_scale': height_scale})# {'x_scale': 0.424, 'y_scale': 0.4})#{'x_scale': 0.4, 'y_scale': 0.4})
                            except FileNotFoundError as error :
                                worksheet.write(rows, cols5, 'image file not found',cell_format_2)
                        else:
                            worksheet.write(rows, cols5, '-----',cell_format_2)
            if cols6 ==6 :
                if 'After' in ikim['riro_image']:
                    if ikim['riro_image']['After'] is not None:
                        try:
                            verify_img = Image.open(get_current_dir_and_goto_parent_dir() + '/images/RIRO' +'/' + ikim['riro_image']['After'])
                            verify_img.verify()
                            worksheet.set_column(6, 6, 40)
                            worksheet.set_row(rows, 180)
                            worksheet.insert_image(rows, cols6, get_current_dir_and_goto_parent_dir() + '/images/RIRO' + '/' + str(ikim['riro_image']['After']),{'x_scale': 0.29, 'y_scale': 0.37})#{'x_scale': width_scale, 'y_scale': height_scale})#{'x_scale': 0.424, 'y_scale': 0.38})# {'x_scale': 0.38, 'y_scale': 0.38})
                        except FileNotFoundError as error :
                            worksheet.write(rows, cols5, 'image file not found',cell_format_2)
                    else:
                        worksheet.write(rows, cols6, '-----',cell_format_2)
            if cols7 ==7 :
                if ikim['rack_method'] is not None:
                    if ikim['rack_method'] == 'automatic':
                        worksheet.write(rows, cols7, ikim['rack_method'],cell_format_2)
                    else:
                        worksheet.write(rows, cols7, ikim['rack_method'],cell_format_3)
                else:
                    worksheet.write(rows, cols7, '-----', cell_format_2)
                    
            if cols8 == 8:
                if ikim['irrd_in_time'] is not None:
                    worksheet.write(rows, cols8, str(ikim['irrd_in_time']) , cell_format_2)
                else:
                    worksheet.write(rows, cols8, '-----', cell_format_2)
            if cols9 == 9:
                if ikim['irrd_out_time'] is not None:
                    worksheet.write(rows, cols9, str(ikim['irrd_out_time']) , cell_format_2)
                else:
                    worksheet.write(rows, cols9, '-----', cell_format_2)                    
                    
            if cols10 == 10:
                if ikim['rack_process'] is not None:
                    worksheet.write(rows, cols10, ikim['rack_process'], cell_format_2)
                else:
                    worksheet.write(rows, cols10, '-----',cell_format_2)
            if cols11 == 11:
                if ikim['remarks']:
                    worksheet.write(rows, cols11, ikim['remarks'], cell_format_2)
                else:
                    worksheet.write(rows, cols11, '------ ',  cell_format_2)
                   
            rows += 1
                # except UnidentifiedImageError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEETerreq123 4", str(error), " ----time ---- ", now_time_with_time()]))
                #     UnidentifiedImageError_count += 1
                # except FileNotFoundError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEqerqweT123 5", str(error), " ----time ---- ", now_time_with_time()]))
                #     FileNotFoundError_count += 1
                # except UserWarning as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEETqerqwe123 6", str(error), " ----time ---- ", now_time_with_time()]))
                # except ImportError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEET1qerq23 7", str(error), " ----time ---- ", now_time_with_time()]))
                # except xlsxwriter.exceptions.FileCreateError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEEeqrwerqT123 08", str(error), " ----time ---- ", now_time_with_time()]))
                # except PermissionError as error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHqerqweEET123 09", str(error), " ----time ---- ", now_time_with_time()]))
                # except xlsxwriter.exceptions.XlsxWriterException as  error:
                #     ret = {'success': False, 'message': str(error)}
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHEqeqreET123 10", str(error), " ----time ---- ", now_time_with_time()]))
        if 1:
        # try:
            workbook.close()
            print('UnidentifiedImageError_count == ',
                UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        # except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter.
        #     exceptions.EmptyChartSeries, xlsxwriter.exceptions.
        #     DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,
        #     xlsxwriter.exceptions.DuplicateWorksheetName, xlsxwriter.
        #     exceptions.XlsxWriterException, xlsxwriter.exceptions.
        #     XlsxFileError, xlsxwriter.exceptions.FileCreateError,
        #     xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions
        #     .FileSizeError) as error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKS33HEET123 11", str(error), " ----time ---- ", now_time_with_time()]))
        # except PermissionError as error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKS33HEET123 12", str(error), " ----time ---- ", now_time_with_time()]))
        # except AttributeError as error:
        #     ret = {'success': False, 'message': str(error)}
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- TSKSHE33ET123 13", str(error), " ----time ---- ", now_time_with_time()]))
    # except Exception as  error:
    #     ret = {'success': False, 'message': str(error)}
    return ret




@dashboard.route('/UpdateTagName', methods = ['POST'])
def UpdateTagName():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['tagname','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            tagname = jsonobject['tagname']
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"tagname":tagname}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'tag name is updated successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating tag name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



@dashboard.route('/DeleteTagName', methods = ['POST'])
def DeleteTagName():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"tagname":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'tag name is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating tag name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)




@dashboard.route('/UpdateAreaName', methods = ['POST'])
def UpdateAreaname():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['sub_area','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            sub_area = jsonobject['sub_area']
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"sub_area":sub_area}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'sub_area name is updated successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating sub_area name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)


@dashboard.route('/DeleteAreaName', methods = ['POST'])
def DeleteAreaName():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"sub_area":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'area name is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating area name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



@dashboard.route('/UpdateDepartmentname', methods = ['POST'])
def UpdateDepartmentname():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['department','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            department = jsonobject['department']
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"department":department}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'department name is updated successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating department name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)


@dashboard.route('/DeleteDepartmentname', methods = ['POST'])
def DeleteDepartmentname():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"department":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'department name is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating department name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                          
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)


@dashboard.route('/UpdateJobDescription', methods = ['POST'])
def UpdateJobDescription():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['job_description','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            job_description = jsonobject['job_description']
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"job_description":job_description}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'job_description is updated successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating job_description.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)

@dashboard.route('/DeleteJobDescription', methods = ['POST'])
def DeleteJobDescription():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"job_description":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'job_description  is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating job_description.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                          
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



#SwitchBoardName
@dashboard.route('/UpdateSwitchBoardName', methods = ['POST'])
def UpdateSwitchBoardName():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['board','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            boardname = jsonobject['board']
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"board":boardname}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'switch board is updated successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating switch board.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)

@dashboard.route('/DeleteSwitchBoardName', methods = ['POST'])
def DeleteSwitchBoardName():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"board":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'board  is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating board.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                          
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



@dashboard.route('/GetJOBNUMBER', methods=['GET'])
@dashboard.route('/GetJOBNUMBER', methods=['POST'])
def GetJOBNUMBER():
    try:
        ret = {'success': False, 'message':'something went wrong with get  details api'}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
        if request.method == 'GET':
            if sheet_data is not None:
                match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
                data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
                                                           {'$group':{'_id': '$job_no', 'all_data':{'$first': '$$ROOT'}}},
                                                           {'$limit': 4000000}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if isEmpty(i['all_data']['data']):
                            if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
                                if len(i['all_data']['data']['panel_data']) !=0  :
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                else:
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])

                            elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
                                if 'hydraulic_data' in i['all_data']['data']:
                                    if len(i['all_data']['data']['hydraulic_data']) !=0 :
                                        if i['_id'] not in dash_data:
                                            dash_data.append(i['_id'])
                                    else:
                                        if i['_id']  not in dash_data:
                                            dash_data.append(i['_id'])

                            elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
                                if len(i['all_data']['data']['useal_data']) !=0 :
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                        
                                else:
                                    if i['_id']  not in dash_data:
                                        dash_data.append(i['_id'])
                                
                    if len(dash_data) != 0:
                        ret = {'success': True, 'message': dash_data}
                    else:
                        ret['message'] = 'data not found'
                else:
                    ret['message'] = 'data not found'
            else:
                ret['message'] = 'job sheet is not uploaded yet'
                
        elif request.method == 'POST':
            jsonobject = request.json
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['type']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    jobtype = jsonobject['type']
                    if sheet_data is not None:
                        if jobtype is not None:
                            
                            match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token'],'type':jobtype}
                            data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
                                                                    {'$group':{'_id': '$job_no', 'all_data':{'$first': '$$ROOT'}}},
                                                                    {'$limit': 4000000}]))
                            dash_data = []
                            if len(data) != 0:
                                for count, i in enumerate(data):
                                    if isEmpty(i['all_data']['data']):
                                        if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
                                            if len(i['all_data']['data']['panel_data']) !=0  :
                                                if i['_id']  not in dash_data:
                                                    dash_data.append(i['_id'])
                                            else:
                                                if i['_id']  not in dash_data:
                                                    dash_data.append(i['_id'])

                                        elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
                                            if 'hydraulic_data' in i['all_data']['data']:
                                                if len(i['all_data']['data']['hydraulic_data']) !=0 :
                                                    if i['_id'] not in dash_data:
                                                        dash_data.append(i['_id'])
                                                else:
                                                    if i['_id']  not in dash_data:
                                                        dash_data.append(i['_id'])

                                        elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
                                            if len(i['all_data']['data']['useal_data']) !=0 :
                                                if i['_id']  not in dash_data:
                                                    dash_data.append(i['_id'])
                                                    
                                            else:
                                                if i['_id']  not in dash_data:
                                                    dash_data.append(i['_id'])
                                            
                                if len(dash_data) != 0:
                                    ret = {'success': True, 'message': dash_data}
                                else:
                                    ret['message'] = 'data not found'
                            else:
                                ret['message'] = 'data not found'
                        else:
                            ret['message'] = 'given job type is none.'
                    else:
                        ret['message'] = 'job sheet is not uploaded yet'
        else:
            ret['message'] = 'request type wrong, please try once again.'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- sheetDepartmeeerntlist 1", str(error), " ----time ---- ", now_time_with_time()])) 
        ret['message' ] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")    
    except Exception as  error:
        ret = {'success': False, 'message': str(error)}
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- sheetDepeerartmentlist 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)

@dashboard.route('/AddRemarksForHoleJob', methods = ['POST'])
def AddRemarksForHoleJob():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['remark','id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            remark = jsonobject['remark']
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"remark":remark}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'remark is updated successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating sub_area name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



@dashboard.route('/RemoveRemarksForHoleJob', methods = ['POST'])
def RemoveRemarksForHoleJob():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['id']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            id = jsonobject['id']
            if id is not None: 
                sheet_data = mongo.db.panel_data.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            # else:
            #     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
                if sheet_data is not None:
                    result = mongo.db.panel_data.update_one({ '_id': ObjectId(sheet_data['_id'])},  {'$set': {"remark":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'remark is deleted successfully.','success': True}
                    else:
                        ret['message'] ='something went wrong updating sub_area name.'
                else:
                    ret['message']='job sheet not uploaded please upload it.'
            else:
                ret['message']='id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)



@dashboard.route('/RemoveRemarksForUnplannedJob', methods = ['POST'])
def DeleteRemarkUnplanned():
    ret = {"message":"somthing wrong with job sheet ", 'success':False}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['riro_key_id']#riro_key_id
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        if output:
            ret['message'] =" ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        else:
            riro_key_id = jsonobject['riro_key_id']
            print("jsonobject ===jsonobject",riro_key_id)
            if riro_key_id is not None: 
                query = {'riro_key_id':riro_key_id}
                print("query ====************************** ",query)
                print("jsonobject=====",jsonobject)
                sheet_data = mongo.db.riro_unplanned.find_one(jsonobject)
                print("unplanned data ====",sheet_data)
                if sheet_data is not None:
                    result = mongo.db.riro_unplanned.update_one({'riro_key_id':riro_key_id}, {'$set': {"remarks":None}})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'remark is deleted successfully.','success': True}
                    else:
                        ret['message'] = 'something went wrong updating sub_area name.'
                else:
                    ret['message']='unplanned job is not found.'
            else:
                ret['message']='riro_key_id should not be None.'                
    else:
        ret['message'] = " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly."])
    return parse_json(ret)




def FORELECTRICALLINK(Query):
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        data = []
        sheet_data = None
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            Query['job_sheet_name'] = sheet_data['job_sheet_name']
            Query['token'] = sheet_data['token']
            panel_no = None
            # print("sorkkkkkjob final query ---------",Query)
            if "panel_no" in Query:
                panel_no = Query['panel_no']
            data = list(mongo.db.panel_data.find(Query))
            # data = list(data)
            # print("data--length-----",len(data))
            if len(data) !=0 :
                final_panel_data = []   
                data = MUPANRRILATION_multi_isolation(data)
                for ___INNN, emmmi in enumerate(data):
                    if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and  emmmi['data']['panel_data']['panel_id'] is not None:
                        if panel_no is not None :
                            if emmmi['data']['panel_data']['panel_id'] == panel_no : 
                                final_panel_data.append(emmmi)
                        else:
                            final_panel_data.append(emmmi)
                    elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                        final_panel_data.append(emmmi)
                if len(final_panel_data) != 0:
                    riro_final = []
                    for i, each_panel in enumerate(final_panel_data):
                        if each_panel['type'] =='HT' or each_panel['type']=='ht':
                            if isEmpty(each_panel['data']) :
                                if len(each_panel['data']['panel_data']) !=0:
                                    show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status':1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                    if len(show_live_riro) != 0:
                                        show_live_riro = riro_live_data(show_live_riro)
                                        each_panel['riro_data'] = show_live_riro
                                        each_panel['riro_edit_status'] = False
                                        each_panel['live_status'] = True
                                        each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
                                        if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                            each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                        else:
                                            each_panel['isolation_status'] = None
                                        each_panel['exception_status'] = False
                                        riro_final.append(each_panel)
                                    elif each_panel['data']['rtsp_url']:
                                        find_riro_data = list(mongo.db.riro_data.find({'token': each_panel['token'], 'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
                                        if len(find_riro_data) != 0:
                                            (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                            check_data = list(check_data)
                                            if panel_status or len(check_data) != 0:
                                                each_panel['data']['panel_data']['panel_status'] = panel_status
                                                each_panel['riro_data'] = check_data
                                                each_panel['riro_edit_status'] = riro_edit_status
                                                each_panel['live_status'] = False
                                                each_panel['sort_id'] = check_data[0]['sort_id']
                                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                                else:
                                                    each_panel['isolation_status'] = None
                                                each_panel['exception_status'] = False
                                                riro_final.append(each_panel)
                                            else:
                                                check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
                                                            'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                            'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
                                                each_panel['riro_data'] = check_data
                                                each_panel['riro_edit_status'] = False
                                                each_panel['live_status'] = False
                                                each_panel['sort_id'] = None
                                                if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                    each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                                else:
                                                    each_panel['isolation_status'] = None
                                                each_panel['exception_status'] = False
                                                riro_final.append(each_panel)
                                        else:
                                            check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
                                                'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
                                            each_panel['riro_data'] = check_data
                                            each_panel['riro_edit_status'] = False
                                            each_panel['live_status'] = False
                                            each_panel['sort_id'] = None
                                            if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                                each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                            else:
                                                each_panel['isolation_status'] = None
                                            each_panel['exception_status'] = False
                                            riro_final.append(each_panel)
                                else:
                                    each_panel['riro_data'] = []
                                    each_panel['riro_edit_status'] = False
                                    each_panel['live_status'] = False
                                    each_panel['sort_id'] = None
                                    if each_panel['tagname']  is not None and each_panel['tagname']  !='':
                                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                                    else:
                                        each_panel['isolation_status'] = None
                                    each_panel['exception_status'] = False
                                    riro_final.append(each_panel)
                                
                        else:
                            hydata , panel_status = hydralockdataFetch(each_panel)
                            check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
                            each_panel['riro_data'] = check_data
                            each_panel['riro_edit_status'] = False
                            each_panel['live_status'] = False
                            each_panel['sort_id'] = None
                            each_panel['isolation_status'] = None
                            each_panel['exception_status'] = False
                            riro_final.append(each_panel)
                    else:             
                        checkdata = all_riro_final_sortin(riro_final)    
                        # print('----------------------------checkdata------',checkdata)  
                        newdata = check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final))   )   
                        # print('-------------------------------newdata ------------------',newdata)
                        ret = {'message': newdata,'success': True}
                        ret['job_sheet_status'] = True
                else:
                    ret = {'message': 'panel data not found.', 'success': False}
                    ret['job_sheet_status'] = True
            else:
                ret['message'] = 'panel data not found'
                ret['job_sheet_status'] = True
        else:
            ret['job_sheet_status']=False
            ret['message']='job sheet is not yet uploaded, please upload job sheet.'

    return ret


def ELECTICALSTATUS(jobnumber):
    process = None
    if jobnumber != 'NA':
        Query = {'job_no':int(jobnumber)}
        ResultofElectrical = FORELECTRICALLINK(Query)
        if ResultofElectrical is not None:
            if ResultofElectrical['message'] is not None:
                Electridata = ResultofElectrical['message']
                # print("========Electridata================1==",Electridata)
                newvariable = False 
                if type(Electridata ) != str:
                
                # print('Electridata-------111----------------------',Electridata[0]['riro_data'])
                    if Electridata[0]['riro_data'] is not None:
                        if len(Electridata[0]['riro_data']) !=0 :
                            # print("---------Electridata['riro_data']---------------------",Electridata[0]['riro_data'])
                            if Electridata[0]['riro_data'][0]['rack_process'] is not None:
                                newvariable = Electridata[0]['riro_data'][0]['rack_process']
                    process = {'isolation_status':Electridata[0]['isolation_status'],'panel_status': newvariable}
                else:
                    process = {'isolation_status':None,'panel_status': newvariable}
    return process

def FieldjobviolationDetails(camera_name):
    violation_details = {"ra_violation": False,'ppe_violation':False, 'crowd_count_violation':False}
    match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name}
    data = list(mongo.db.data.aggregate([{'$match': match_data},{'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'analyticstype': '$analyticstype'}}}]))#, 'data':{'$first':'$$ROOT'}
    if len(data) !=0 :
        # print('===============violationdata============len=========',len(data))
        for i, j in enumerate(data):
            if j['_id']['analyticstype']=='RA':
                violation_details['ra_violation'] = True
            if j['_id']['analyticstype']=='CRDCNT':
                violation_details['crowd_count_violation'] = True
            if j['_id']['analyticstype']=='PPE_TYPE1':
                violation_details['ppe_violation'] = True
    return violation_details



def Linkmechisolationdatadetails(rack_process_list):
    panel_status = None
    if len(rack_process_list) != 0:
        if len(rack_process_list) == 1:
            if rack_process_list[0]['lock_on_details'] is not None and rack_process_list[0]['lock_off_details'] is not None :
                panel_status = True
            elif rack_process_list[0]['lock_on_details'] is not None:
                panel_status = False
            elif rack_process_list[0]['lock_off_details'] is not None:
                panel_status = True
        elif len(rack_process_list) > 1:
            if rack_process_list[0]['lock_on_details'] is not None and rack_process_list[0]['lock_off_details'] is not None :
                panel_status = True
            elif rack_process_list[0]['lock_on_details'] is not None:
                panel_status = False
            elif rack_process_list[0]['lock_off_details'] is not None:
                panel_status = True
    return panel_status

def CheckforMechisolation(job_no):
    hydralic_status= None
    only_two_data =[]
    sheet_data = mongo.db.mechjob_sheet.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])     
    if sheet_data is not None:
        data = mongo.db.mechesi.find_one({'job_no':job_no,'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',   pymongo.DESCENDING)])
        # print('-----data----jobnumber ------------',data)
        if data :
            final_panel_data = []   
            data = MUPANRRILATION_multi_isolation(data)
            # print('--------------------------datamew after modification ---',data)
            for ___INNN, emmmi in enumerate(data):
                # print('-----data-----emmmi--------------',emmmi)
                if emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                    FINDHYDRADATA= list(mongo.db.hydra_data.find({'camera_rtsp':emmmi['data']['rtsp_url'],"camera_name":emmmi['data']['camera_name']}, sort=[('_id',   pymongo.DESCENDING)]))#.sort({"_id":1}).limit(1))#.sort({"_id":1}).limit(1)
                    # print('---------------------------FINDHYDRADATA',FINDHYDRADATA)
                    if len(FINDHYDRADATA) != 0 :
                        newlist = sorted(FINDHYDRADATA, key=lambda d: d['_id']) 
                        for u,i in enumerate(newlist):
                            if u > 0:
                                break
                            only_two_data.append(i)    
                        hydralic_status = Linkmechisolationdatadetails(only_two_data)
        # else:
            # print('-------------------------------job number not found------')
    Valuestatus = {'valve_status':hydralic_status}
    return Valuestatus#only_two_data , hydralic_status     



@dashboard.route('/linkget_ra_camera_details/<id>', methods=['GET'])
@dashboard.route('/linkget_ra_camera_details', methods=['GET'])
def ra_camera_details(id=None):
    ret = {'success': False, 'message':'something went wrong with ra camera details api'}
    if 1:
    # try:
        final_data = []
        if id is not None:
            data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if data is not None:
                data = parse_json(data)
                linkeddata = mongo.db.linkagejobs.find_one({'fieldjobreferencid': str(id)})
                if linkeddata is not None:
                    electrical_jobnumber = linkeddata['electrical_jobnumber']
                    mechanical_jobnumber = linkeddata['mechanical_jobnumber']
                    data['electrical_jobnumber'] = linkeddata['electrical_jobnumber']
                    data['electrical_jobstatus'] = ELECTICALSTATUS(linkeddata['electrical_jobnumber'])
                    data['mechanical_jobnumber'] = linkeddata['mechanical_jobnumber']
                    
                    data['mechanical_jobstatus'] =CheckforMechisolation(linkeddata['mechanical_jobnumber'])
                    data['violation'] = FieldjobviolationDetails(data['cameraname'])
                    data['joblinkedid'] = linkeddata['_id']
                else:
                    data['electrical_jobnumber'] = None
                    data['mechanical_jobnumber'] = None
                    data['electrical_jobstatus'] = None
                    data['mechanical_jobstatus'] = None
                    data['violation'] = None
                    data['joblinkedid'] = None
                data = delete_keys_from_dict(data, ['cameraid', 'username', 'password', 'camera_brand', 'rtsp_port','camera_status',  'timestamp'])
                final_data.append(data)
                if len(final_data) != 0:
                    ret = {'message': final_data, 'success': True}
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            data = mongo.db.ppera_cameras.find()
            if data is not None:
                for jj, i in enumerate(data):
                    linkeddata = mongo.db.linkagejobs.find_one({'fieldjobreferencid': str(i['_id'])})
                    if linkeddata is not None:
                        electrical_jobnumber = linkeddata['electrical_jobnumber']
                        mechanical_jobnumber = linkeddata['mechanical_jobnumber']
                        i['electrical_jobnumber'] = linkeddata['electrical_jobnumber']
                        i['electrical_jobstatus'] = ELECTICALSTATUS(linkeddata['electrical_jobnumber'])
                        i['mechanical_jobnumber'] = linkeddata['mechanical_jobnumber']
                        i['mechanical_jobstatus'] = CheckforMechisolation(linkeddata['mechanical_jobnumber'])
                        i['violation'] =  FieldjobviolationDetails(i['cameraname'])
                        i['joblinkedid'] = linkeddata['_id']
                    else:
                        i['electrical_jobnumber'] = None
                        i['mechanical_jobnumber'] = None
                        i['electrical_jobstatus'] = None
                        i['mechanical_jobstatus'] = None
                        i['violation'] = None
                        i['joblinkedid'] = None
                    i = delete_keys_from_dict(i, ['cameraid', 'username', 'password', 'image_height','image_width', 'rtsp_port', 'camera_status','timestamp'])
                    final_data.append(i)
                final_data = parse_json(final_data)
                if len(final_data) != 0:
                    ret = {'message': final_data, 'success': True}
                else:
                    ret['message'] = 'cameras are not found for RA, PPE, please add cameras.'
            else:
                ret['message'] = 'cameras are not found for RA, PPE, please add cameras.'
    # except Exception as error:
    #     ret['message'] = str(error)
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- get_ra_cameiiira_details 2", str(error), " ----time ---- ", now_time_with_time()]))
    # ret.headers['X-Frame-Options'] = 'DENY' 
    return ret