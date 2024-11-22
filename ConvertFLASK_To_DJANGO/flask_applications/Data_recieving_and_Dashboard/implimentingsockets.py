####send  data,image and files###
# from flask import Blueprint
# from flask_socketio import SocketIO
# import os
# from Data_recieving_and_Dashboard.packages import *


# socketio_bp = Blueprint('socketio', __name__)

# socketio = SocketIO(async_mode='gevent',transports=['websocket', 'polling'],cors_allowed_origins='*')
# @socketio.on('request_file')
# def handle_request_file(request_file):
#     print('Requested file:', request_file)
#     file_path = os.path.join(os.getcwd(), request_file)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as f:
#             file_data = f.read()
#         # if b'some-pattern' in file_data:
            
#         #     pass
#         socketio.emit('request_file', {'file_name': request_file, 'file_data': file_data})
#     else:
#         print(f"File '{request_file}' not found")
#         socketio.emit('request_file', {'error': f"File '{request_file}' not found"})

from flask import Blueprint
from flask_socketio import SocketIO
import socketio
import time
from threading import Thread
# import gevent.monkey
# gevent.monkey.patch_all()
from Data_recieving_and_Dashboard.packages import *
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId


URL = "mongodb://localhost:27017/"
CLINET = MongoClient(URL)
DATABASE = CLINET['DOCKETRUNDB']
riro_data = DATABASE['riro_data']
job_sheet_details=DATABASE['job_sheet_details']
rtsp_flagcollection = DATABASE['rtsp_flag']
PPERAVIOLATIONCOLLECTION=DATABASE['data']
panel_data = DATABASE['panel_data']
mechesi = DATABASE['mechesi']
filterviolations = DATABASE['filterviolations']
flasherlogdata = DATABASE['flasherlogdata']
gpu_configurations = DATABASE['gpu_configurations']
linkagejobs = DATABASE['linkagejobs']
live_data_count = DATABASE['live_data_count']
mechjob_sheet = DATABASE['mechjob_sheet']
mockdrill = DATABASE['mockdrill']
ppera_cameras = DATABASE['ppera_cameras']
steamsuit_cameras= DATABASE['steamsuit_cameras']
trafficcountdata = DATABASE['trafficcountdata']
RAlive_data_count= DATABASE['RAlive_data_count']
PPElive_data_count= DATABASE['PPElive_data_count']
CRlive_data_count= DATABASE['CRlive_data_count']
live_data_countCollection = DATABASE['live_data_count']
riro_unplanned = DATABASE['riro_unplanned']
unplanedLivecount  = DATABASE['unplanedLivecount']
mechjob_sheet = DATABASE['mechjob_sheet']
mechesi = DATABASE['mechesi']
MEchHydracollection = DATABASE['hydra_data']


def riroInsertLIVE(RIROLIVEDATA):
    riro_data_inserted_status = False
    URL = "mongodb://localhost:27017/"
    DATABASE_NAME = "DOCKETRUNDB"
    RIRODataCollection = "riro_data"
    JOBSHEetdataCollection='job_sheet_details'
    CLINET = MongoClient(URL)
    DATABASE = CLINET[DATABASE_NAME]
    RIRO_COLLECTION = DATABASE[RIRODataCollection]
    JobSheetData=DATABASE[JOBSHEetdataCollection]
    sheet_data = JobSheetData.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
    # print("riro data === ", RIROLIVEDATA)
    riro_key_token = genarate_alphanumeric_key_for_riro_data()
    x = RIRO_COLLECTION.find_one({'date': RIROLIVEDATA['date'], 'id_no':  RIROLIVEDATA['id_no'], 'appruntime': RIROLIVEDATA['appruntime'], 'analytics_id': RIROLIVEDATA['analytics_id']})
    if sheet_data is not None:
        # print("88888888888888888888888888888888888886^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^--------------",RIROLIVEDATA)
        if x is None:
            print('riro data inserted')
            RIROLIVEDATA['job_sheet_name'] = sheet_data['job_sheet_name']
            RIROLIVEDATA['token'] = sheet_data['token']
            RIROLIVEDATA['riro_key_id'] = riro_key_token
            RIROLIVEDATA['other'] = None
            try :
                if RIROLIVEDATA['remark'] is not None and RIROLIVEDATA['remark'] != 'None':
                    RIROLIVEDATA['remarks'] = RIROLIVEDATA['remark']
                else:
                    RIROLIVEDATA['remarks'] = ''
            except :
                RIROLIVEDATA['remarks'] = ''
            RIROLIVEDATA['riro_edit_status'] = False
            RIROLIVEDATA['cropped_panel_image_path'] = None
            RIROLIVEDATA['lock_time'] = None
            RIROLIVEDATA['tag_time'] = None
            RIROLIVEDATA['within_15_min'] = None
            RIROLIVEDATA['flasher_status'] = 0
            
            # print("+++++++++++++++++++++++++++++++++++++++++%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%====",RIROLIVEDATA)
            result = RIRO_COLLECTION.insert_one(RIROLIVEDATA)
            if result.acknowledged > 0:
                riro_data_inserted_status = True
        else:
            new_change = {'rack_process': RIROLIVEDATA['rack_process'],   'rack_method': RIROLIVEDATA['rack_method'], 'person_in_time': RIROLIVEDATA['person_in_time'], 'person_out_time': RIROLIVEDATA['person_out_time'], 
                            'irrd_in_time': RIROLIVEDATA['irrd_in_time'], 'irrd_out_time': RIROLIVEDATA['irrd_out_time'], 'five_meter': RIROLIVEDATA['five_meter'], 'barricading':RIROLIVEDATA['barricading'], 'riro_image': RIROLIVEDATA['riro_image'],
                            'datauploadstatus': RIROLIVEDATA['datauploadstatus'], 'riro_merged_image': RIROLIVEDATA['riro_merged_image'],'riro_merged_image_size': RIROLIVEDATA['riro_merged_image_size']}
            # print('new change --------', new_change)
            result = RIRO_COLLECTION.update_one({'_id': ObjectId(x['_id'])}, {'$set': new_change})
            if result.modified_count > 0:
                print("---riro data updated---")
                riro_data_inserted_status = True
    else:
        print("riro_data-uploading- job sheet not yet uploaded ")
    CLINET.close()
    return riro_data_inserted_status


def RTSPVERIFY(url):
    cam = cv2.VideoCapture(url)
    if cam.isOpened() == True:
        while cam.isOpened():
            ret, frame = cam.read()
            if ret:
                verfy_rtsp_response = True
                return verfy_rtsp_response
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()
    else:
        return False


def GETWORKINGANDNOTWORKINGcamCOUNT(find_data):
    workingcount = 0
    notworkingcount=0
    totalcountNew = 0
    totalcount = {'total_cameras':totalcountNew,'working_camcount':workingcount,'notworkingcamcount':notworkingcount}
    for ppera_data in find_data:
        totalcountNew += 1 
        if ppera_data['camera_ip'] == None:
            if ppera_data['rtsp_url'] != None:
                if RTSPVERIFY(ppera_data['rtsp_url']):
                    workingcount += 1
                else:
                    notworkingcount += 1
        else:
            testing_ip_working = final_ping(ppera_data['camera_ip'])
            if testing_ip_working is True:
                workingcount += 1
            else:
                notworkingcount += 1
    totalcount={'total_cameras':totalcountNew,'working_camcount':workingcount,'notworkingcamcount':notworkingcount}
    return totalcount



def NEWLICENSECOUNT():
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =0
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICE000NSECOUNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICEN-==00SECOUNT 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICEN009897SECOUNT 3", str(error), " ----time ---- ", now_time_with_time()]))
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        lic = res['device_location']
        split_data=lic.split('_')[1].split("l")
        while '' in split_data:
            split_data.remove('')
        # if CamCount < int((split_data[0])):
        license_status = int((split_data[0]))
        # else:
        #     license_status = False    
    return license_status



def live_data_pagination(live_data_count, all_data):
    try:
        data = live_data_countCollection.find_one()
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
            result = live_data_countCollection.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = live_data_countCollection.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_paginatio555n 1", str(error), " ----time ---- ", now_time_with_time()]))
        #ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30

# import ssl

# socketio_bp = Blueprint('socketio', __name__)
# socketio = SocketIO(logger=True, engineio_logger=True)

# # Configure logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# @socketio.on_error_default  
# def default_error_handler(e):
#     logger.error(f"SocketIO error: {str(e)}")

# @socketio_bp.route('/')
# def index():
#     return "SocketIO server is running."

# @socketio.on('connect')
# def handle_connect():
#     logger.info('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     logger.info('Client disconnected')


# @socketio_bp.route('/request_data')
# def handle_request_data():
#     # Handle request data logic here
#     pass

# @socketio_bp.route('/request_file')
# def handle_request_file():
#     # Handle request file logic here
#     pass

# def init_socketio(app):
#     socketio.init_app(app, async_mode='gevent',cors_allowed_origins='*')




# Initialize Socket.IO
socketio_bp = Blueprint('socketio', __name__)
socketio = SocketIO(cors_allowed_origins='*')

# Define your data emission function
def emit_data_continuously():
    while True:
        socketio.emit('continuous_data', {'message': 'Continuous data emission'})
        time.sleep(2)


@socketio.on('SOCKETcheck_process')
def process_checking_for():
    while 1:
        try:
            processName = ['docketrun-app', 'python3', 'node', 'dup', 'esi-monitor', 'smrec', 'hydra-app', 'phaseone-app', 'fire_smoke_app', 'spillage_app','tg_steamsuit']
            status = checkProcessRunning(processName)
            ret = status
        except Exception as e:
            ret = {'message': 'Error checking process', 'success': False}
        socketio.emit('SOCKETcheck_process', ret)
        time.sleep(2)



@socketio.on('SOCKETset_rtsp_flag')
def set_rtsp_flag_creating_config(data):
    print("---------------------flag----------------",data)
    ret = {'message': 'something went wrong with set_rtsp_flag_creating_config.', 'success': False}
    flag = data.get('flag')
    if flag is not None:
        ret= {'message': 'Flag not provided', 'success': False}   
        if flag != 'undefined':
            find_data = rtsp_flagcollection.find_one({}, sort=[('_id', pymongo.DESCENDING)])
            if find_data is not None:
                id = find_data['_id']
                againfinddata = rtsp_flagcollection.find_one({'_id': ObjectId(id)})
                print("-------------------------againfinddata------------------", againfinddata)
                result = rtsp_flagcollection.update_one({'_id': ObjectId(id)}, {'$set': {'rtsp_flag': flag}})
                if result.modified_count > 0:
                    ret = {'message': 'rtsp flag updated successfully.', 'success': True}
                elif find_data['rtsp_flag'] == '0':
                    ret = {'message': 'flag has been set for rtsp.', 'success': True}
                elif find_data['rtsp_flag'] == '1':
                    ret = {'message': 'flag has been set for rtspt.', 'success': True}
                elif find_data['rtsp_flag'] == 0:
                    ret = {'message': 'flag has been set for rtsp.', 'success': True}
                elif find_data['rtsp_flag'] == 1:
                    ret = {'message': 'flag has been set for rtspt.', 'success': True}
            else:
                result = rtsp_flagcollection.insert_one({'rtsp_flag': flag})
                if result.acknowledged > 0:
                    ret = {'message': 'rtsp flag inserted successfully.', 'success': True}
                else:
                    ret['message'] = 'rtsp flag is not inserted.'
        else:
            ret['message'] = 'rtsp flag should not be undefined'
    else:
        ret['message'] = 'rtsp flag should not be none value.'
    socketio.emit('SOCKETset_rtsp_flag', ret)


@socketio.on('SOCKETget_cam_status_enable_cam_count')
# @camera_status.route('/get_cam_status_enable_cam_count', methods=['GET'])
def get_cam_status_enable_cam_count():
    ret = {'success': False, 'message': 'something went wrong with get all solutions count api'}
    if 1:
    # try:
        find_data_cam_status = list(ppera_cameras.find({'camera_status': True}))        
        if len(find_data_cam_status) !=0:
            disable_data_count = 0
            enable_data_count = 0
            for find_data in find_data_cam_status:
                if len(find_data['roi_data']) == 0 and len(find_data['tc_data'] ) == 0 and len(find_data['cr_data']) == 0 and len(find_data['ppe_data']) == 0 :
                    disable_data_count += 1            
                else:
                    if len(find_data['roi_data']) != 0 or len(find_data['tc_data'] ) != 0 or len(find_data['cr_data']) != 0 or (len(find_data['ppe_data']) and any(value is True for value in find_data['ppe_data'][0].values())) != 0:
                        if find_data["analytics_status"] == 'true':
                            enable_data_count += 1  
                        else:
                            disable_data_count += 1           
                    else:
                        disable_data_count += 1
            """Calling function to get the working camera list and not woorking camera list"""
            wcam_list_and_nwcam_list = GETWORKINGANDNOTWORKINGcamCOUNT(find_data_cam_status)
            REQUIRED = [{'total_cam_count': wcam_list_and_nwcam_list['total_cameras'], 'working_cam_count': wcam_list_and_nwcam_list['working_camcount'], 'not_working_cam_count': wcam_list_and_nwcam_list['notworkingcamcount'], 'disable_data_count': disable_data_count, 'enable_data_count': enable_data_count}]
            ret = {'message': REQUIRED, 'success': True}
        else:
            ret['message']='there are no cameras added for analytics.'
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_cam_status_enable_cam_count 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] =" ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")
    # except Exception as error:
    #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_cam_status_enable_cam_count 2", str(error), " ----time ---- ", now_time_with_time()]))
    # return ret
    socketio.emit('SOCKETget_cam_status_enable_cam_count', ret)


@socketio.on('SOCKETlicenseNewcount')
# @dashboard.route('/licenseNewcount', methods=['GET'])
def license_count():
    Return = {'total_license':0,'added_cameras_count':0,'remaining_license':0}
    if 1:
    # try:
        ret = {'message': 'something went wrong with get license_count', 'success': False}
        sheet_data = job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        sheet_camera_count = 0
        if sheet_data is not None:
            sheet_data_count = list(panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
            unique_iplist = []
            if len(sheet_data_count) !=0:
                for kl , eachElements in enumerate(sheet_data_count):
                    if eachElements['ip_address'] not in unique_iplist:
                        unique_iplist.append(eachElements['ip_address'])
                sheet_camera_count= len(unique_iplist) 
            
        CamCount = ppera_cameras.count_documents({})
        Total_license = NEWLICENSECOUNT() 
        Return = {'total_license':Total_license,'added_cameras_count':CamCount+sheet_camera_count,'remaining_license':Total_license-(CamCount+sheet_camera_count)}
        ret['message']=Return
        ret['success']=True
    # except Exception as error:
    #     ret['message'] = str(error)
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_licedsdnse_of_camera 4", str(error), " ----time ---- ", now_time_with_time()]))
    # return ret
    socketio.emit('SOCKETlicenseNewcount', ret)

# Start emitting data in a separate thread
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Start the continuous data emission in a separate thread
    # socketio.start_background_task(target=emit_data_continuously)
    socketio.start_background_task(target=process_checking_for)
    socketio.start_background_task(target=admin_live_data_with_pagination)
    socketio.start_background_task(target=multii44solation_convayor_pnumertic_hydralic23323)
    #
    socketio.start_background_task(target=get_job_she333et_status_of_current)
    # socketio.start_background_task(target=set_rtsp_flag_creating_config)
    # print('Client connected')
    # emit_thread = Thread(target=emit_data_continuously)
    # process_check_thread = Thread(target=process_checking_for)
    # set_rtsp_flag_thread = Thread(target=set_rtsp_flag_creating_config)
    
    # emit_thread.start()
    # process_check_thread.start()
    # set_rtsp_flag_thread.start()



# Define your continuous data emission function
# def emit_continuous_data():
#     while True:
#         data = {'message': 'Continuous data'}
#         socketio.emit('continuous_data', data)
#         time.sleep(2)  # Adjust the sleep time as needed

# # Start the continuous data emission in a separate thread
# continuous_thread = Thread(target=emit_continuous_data)
# continuous_thread.start()

# Define your data request event
@socketio.on('request_data')
def handle_data_request():
    # Simulate fetching data from somewhere
    data = {'message': 'Requested data'}
    socketio.emit('requested_data', data)




@socketio.on('SOCKETlive_data1')
def admin_live_data_with_pagination():
    while 1:
        ret = {'success': False,'message':"something went wrong in live_data1 apis"}
        violation_type=None
        camera_name=None
        # try:
        if 1:        
            dash_data = []
            Foundfileterdata = filterviolations.find_one({},{'_id':0})
            if Foundfileterdata  is None:
                Foundfileterdata = {"helmet":70,"vest":70} 
            if camera_name is not None and violation_type is not None:
                if violation_type == 'PPE':
                    violation_type = 'PPE_TYPE1'
                match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type}
                data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                    {'$project': {   'appruntime':0,
                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                                'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1
                            wapas_data['SNo'] = count1
                            dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                    all_data = live_data_pagination(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
            elif camera_name is not None:
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'camera_name': camera_name}
                data =list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                    {'$project': {   'appruntime':0,
                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                                'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1
                            wapas_data['SNo'] = count1
                            dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                    all_data = live_data_pagination(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
            elif violation_type is not None:
                if violation_type == 'PPE':
                    violation_type = 'PPE_TYPE1'
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
                data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                    {'$project': {   'appruntime':0,
                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                                'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1
                            wapas_data['SNo'] = count1
                            dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                    all_data = live_data_pagination(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
            else:
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
                data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                    {'$project': {   'appruntime':0,
                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                                'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1
                            wapas_data['SNo'] = count1
                            dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                    all_data = live_data_pagination(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
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
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data1 1", str(error), " ----time ---- ", now_time_with_time()]))   
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
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data1 2", str(error), " ----time ---- ", now_time_with_time()]))   
        # return jsonify(ret)
        socketio.emit('SOCKETlive_data1', ret)
        time.sleep(2)



def RALIVECOUNT(live_data_count, all_data):
    try:
        data = RAlive_data_count.find_one()
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
            result = RAlive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = RAlive_data_count.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- RALIVECOUeeeNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        #ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30





def VIolationcountforRA(live_data):
    # print("---------------------------------------------live_data ----------------------------------- ",live_data)
    ret = False
    if live_data is not None:
        if 1:
        # try:
            if len(live_data['data']) !=0:
                if len(live_data['data']) ==1:
                    if live_data['data'][0]['analyticstype'] == 'RA':
                        department_name = None
                        finddepartment = ppera_cameras.find_one({'rtsp_url': live_data['data'][0]['camera_rtsp'],"cameraname":live_data['data'][0]['camera_name']})
                        if finddepartment is not None :
                            department_name = finddepartment['department']
                        else:
                            finddepartment = ppera_cameras.find_one({'rtsp_url': live_data['data'][0]['camera_rtsp']})
                            if finddepartment is not None :
                                department_name = finddepartment['department']
                            else:
                                finddepartment = ppera_cameras.find_one({"cameraname":live_data['data'][0]['camera_name']})
                                if finddepartment is not None:
                                    department_name = finddepartment['department']
                                else:
                                    department_name= live_data['data'][0]['camera_name']
                                    
                        live_data['data'][0]['department'] = department_name                         
                        object_data = live_data['data'][0]['object_data']                        
                        if len(object_data) != 0:
                            if 1:
                            # try:
                                final_object_data = []
                                if len(object_data) == 1:
                                    if object_data[0]['violation'] == False:
                                        pass
                                    elif object_data[0]['violation'] == True:
                                        if object_data[0]['class_name'] == 'person':
                                            del object_data[0]['bbox']
                                            del object_data[0]['tracking_id']
                                            object_data[0]['violation_count'
                                                ] = 'person ' + str(1)
                                            final_object_data.append(object_data[0])
                                elif len(object_data) > 1:
                                    for ___, jjj in enumerate(object_data):
                                        if jjj['violation'] == False:
                                            pass
                                        elif jjj['violation'] == True:
                                            if jjj['class_name'] == 'person':
                                                del jjj['bbox']
                                                del jjj['tracking_id']
                                                jjj['violation_count'] = 'person ' + str(int(___) + int(1))
                                                final_object_data.append(jjj)
                                live_data['data'][0]['object_data'] = final_object_data
                            # except Exception as  error:
                            #     print('(live_data)    line --- 2347 ',  error)
                elif len(live_data['data']) > 1:
                    newlivedata = []                    
                    for indexlivedata, eachobjectlivedata in enumerate(live_data['data']):
                        if eachobjectlivedata['analyticstype'] == 'RA':
                            department_name = None
                            finddepartment = ppera_cameras.find_one({'rtsp_url':eachobjectlivedata['camera_rtsp'],"cameraname":eachobjectlivedata['camera_name']})
                            if finddepartment is not None :
                                department_name = finddepartment['department']
                            else:
                                finddepartment = ppera_cameras.find_one({'rtsp_url': eachobjectlivedata['camera_rtsp']})
                                if finddepartment is not None :
                                    department_name = finddepartment['department']
                                else:
                                    finddepartment = ppera_cameras.find_one({"cameraname":eachobjectlivedata['camera_name']})
                                    if finddepartment is not None:
                                        department_name = finddepartment['department']
                                    else:
                                        department_name= eachobjectlivedata['camera_name']
                                        
                            eachobjectlivedata['department'] = department_name
                            object_data = eachobjectlivedata['object_data']
                            if len(object_data) != 0:
                                if 1:
                                # try:
                                    final_object_data = []
                                    if len(object_data) == 1:
                                        if object_data[0]['violation'] == False:
                                            pass
                                        elif object_data[0]['violation'] == True:
                                            if object_data[0]['class_name'] == 'person':
                                                del object_data[0]['bbox']
                                                del object_data[0]['tracking_id']
                                                object_data[0]['violation_count'
                                                    ] = 'person ' + str(1)
                                                final_object_data.append(object_data[0])
                                    elif len(object_data) > 1:
                                        for ___, jjj in enumerate(object_data):
                                            if jjj['violation'] == False:
                                                pass
                                            elif jjj['violation'] == True:
                                                if jjj['class_name'] == 'person':
                                                    del jjj['bbox']
                                                    del jjj['tracking_id']
                                                    jjj['violation_count'] = 'person ' + str(int(___) + int(1))
                                                    final_object_data.append(jjj)
                                    eachobjectlivedata['object_data'] =  final_object_data
                                    newlivedata.append(eachobjectlivedata)
                                # except Exception as  error:
                                #     print('(live_data)    line --- 2347 ',  error)   
                                    
                    live_data['data']=newlivedata       
                
            ret = live_data
        # except Exception as  error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  2", str(error), " ----time ---- ", now_time_with_time()]))
    else:
        ret = ret
    return ret

@socketio.on('SOCKETlive_data1RA')
# @violationanalysis_data.route('/live_data1RA', methods=['GET'])
# @violationanalysis_data.route('/live_data1RA/cameraname/<camera_name>', methods=['GET'])
# @violationanalysis_data.route('/live_data1RA/department/<department_name>', methods=['GET'])
# @violationanalysis_data.route('/live_data1RA', methods=['POST'])
def LIVEVIOLATIONOFRA(data):
    camera_name=None
    department_name =None
    if 'camera_name' in data:
        if data['camera_name'] is not None:
            camera_name = data['camera_name']
    if 'department_name' in data:
        if data['department_name'] is not None:
            department_name = data['department_name']
    violation_type='RA'
    
    ret = {'success': False,'message':"something went wrong in live_data1RA apis"}
    if data is not None:
        jsonobject= data
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['camera_name', 'department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                camera_name = jsonobject['camera_name']
                department_name = jsonobject['department_name']
                dash_data = []
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and    department_name !='') :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {'$project': {'_id': 0, 'data': 1}},
                                {'$lookup': {'from': 'ppera_cameras', 'localField': 'data.camera_name', 'foreignField': 'cameraname', 'as': 'camera_data'}},
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                    'data.department': {
                                        '$cond': {
                                            'if': {'$eq': ['$camera_data.department', department_name]},
                                            'then': '$camera_data.department',
                                            'else': '$$REMOVE'
                                        }
                                    }
                                }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'data.timestamp': -1}},
                                {'$match': {'data.department': {'$exists': True}}}
                            ]                    
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {'$project': {'_id': 0, 'data': 1}},
                                {'$lookup': {'from': 'ppera_cameras', 'localField': 'data.camera_name', 'foreignField': 'cameraname', 'as': 'camera_data'}},
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                    'data.department': {
                                        '$cond': {
                                            'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                            'then': '$camera_data.department',
                                            'else': '$$REMOVE'
                                        }
                                    }
                                }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'data.timestamp': -1}},
                                {'$match': {'data.department': {'$exists': True}}}
                            ]                    
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    pipeline = [
                                {'$match': match_data},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {'$project': {'_id': 0, 'data': 1}},
                                {'$lookup': {'from': 'ppera_cameras', 'localField': 'data.camera_name', 'foreignField': 'cameraname', 'as': 'camera_data'}},
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                    'data.department': {
                                        '$cond': {
                                            'if': {'$eq': ['$camera_data.department', department_name]},
                                            'then': '$camera_data.department',
                                            'else': '$$REMOVE'
                                        }
                                    }
                                }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'data.timestamp': -1}},
                                {'$match': {'data.department': {'$exists': True}}}
                            ]                    
                else:
                    pipeline = [
                                {'$match': match_data},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {'$project': {'_id': 0, 'data': 1}},
                                {'$lookup': {'from': 'ppera_cameras', 'localField': 'data.camera_name', 'foreignField': 'cameraname', 'as': 'camera_data'}},
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                    'data.department': {
                                        '$cond': {
                                            'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                            'then': '$camera_data.department',
                                            'else': '$$REMOVE'
                                        }
                                    }
                                }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'data.timestamp': -1}},
                                {'$match': {'data.department': {'$exists': True}}}
                            ]
                data=list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = VIolationcountforRA(i)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1         
                            wapas_data['SNo'] = count1
                            dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                    all_data = RALIVECOUNT(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    else:
        dash_data = []
        if camera_name is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type}
            pipeline = [
                        {'$match': match_data},
                        {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$project': {'_id': 0, 'data': 1}},
                        {'$lookup': {'from': 'ppera_cameras', 'localField': 'data.camera_name', 'foreignField': 'cameraname', 'as': 'camera_data'}},
                        {'$unwind': '$camera_data'},
                        {'$addFields': {
                            'data.department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},  
                        {'$sort': {'data.timestamp': -1}},
                        {'$match': {'data.department': {'$exists': True}}}
                    ]
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
            # print("================match_data==============",match_data)
            pipeline = [
                        {'$match': match_data},
                        {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$project': {'_id': 0, 'data': 1}},
                        {'$lookup': {'from': 'ppera_cameras', 'localField': 'data.camera_name', 'foreignField': 'cameraname', 'as': 'camera_data'}},
                        {'$unwind': '$camera_data'},
                        {'$addFields': {
                            'data.department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},  
                        {'$sort': {'data.timestamp': -1}},
                        {'$match': {'data.department': {'$exists': True}}}
                    ]
            
        data=list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
        if len(data) != 0:
            count1 = 0 
            for count, i in enumerate(data):
                wapas_data = VIolationcountforRA(i)
                if type(wapas_data) == list:
                    pass
                elif wapas_data:
                    count1 +=1         
                    wapas_data['SNo'] = count1
                    dash_data.append(wapas_data)
                else:
                    count1 +=1
                    i['SNo'] = count1
                    dash_data.append(i)
            all_data = RALIVECOUNT(len(dash_data), parse_json(dash_data))
            ret = all_data
        else:
            ret['message'] = 'data not found'  
    # return jsonify(ret)
    socketio.emit('SOCKETlive_data1RA', ret)



def PPELIVECOUNT(live_data_count, all_data):
    try:
        data = PPElive_data_count.find_one()
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
            result = PPElive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = PPElive_data_count.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PPELIVECOUNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        #ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30


@socketio.on('SOCKETlive_data1PPE')
def LIVEVIOLATIONOFPPE(PPEINPUTdata):
    ret = {'success': False,'message':"something went wrong in live_data1PPE apis"}
    # print("-----LIVEVIOLATIONOFPPE------",PPEINPUTdata)
    camera_name=None
    department_name =None
    if 'camera_name' in PPEINPUTdata:
        if PPEINPUTdata['camera_name'] is not None:
            camera_name = PPEINPUTdata['camera_name']
    if 'department_name' in PPEINPUTdata:
        if PPEINPUTdata['department_name'] is not None:
            department_name = PPEINPUTdata['department_name']
    violation_type='PPE_TYPE1'
    dash_data = []
    pipeline = []
    Foundfileterdata = filterviolations.find_one({},{'_id':0})
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
    pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}},
                {'$lookup': {
                    'from': 'ppera_cameras',
                    'localField': 'camera_name',
                    'foreignField': 'cameraname',
                    'as': 'camera_data'
                }},
                {'$addFields': {
                    'department': {
                        '$cond': {
                            'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                            'then': '$camera_data.department',
                            'else': '$$REMOVE'
                        }
                    }
                }},
                {'$unset': 'camera_data'},
                {'$sort': {'timestamp': -1}},
                {'$lookup': {
                    'from': 'panel_data',
                    'localField': 'camera_name',
                    'foreignField': 'data.camera_name',
                    'as': 'Newcameradetailspaneld'
                }},
                {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                {'$addFields': {
                    'department': {
                        '$cond': {
                            'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                            'then': '$department',
                            'else': '$Newcameradetailspaneld.department'
                        }
                    }
                }},
                {'$unset': 'Newcameradetailspaneld'},
                {'$sort': {'timestamp': -1}},
                {'$match': {'department': {'$exists': True}}}
                    ]
    if Foundfileterdata  is None:
        Foundfileterdata = {"helmet":70,"vest":70} 
    if PPEINPUTdata is not None:
        jsonobject =PPEINPUTdata
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['camera_name', 'department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                camera_name = jsonobject['camera_name']
                department_name = jsonobject['department_name']

                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and    department_name !='') :
                    match_data['camera_name']= camera_name
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': 'camera_name',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', department_name]},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'panel_data',
                            'localField': 'camera_name',
                            'foreignField': 'data.camera_name',
                            'as': 'Newcameradetailspaneld'
                        }},
                        {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                                    'then': '$department',
                                    'else': '$Newcameradetailspaneld.department'
                                }
                            }
                        }},
                        {'$unset': 'Newcameradetailspaneld'},
                        {'$sort': {'timestamp': -1}},
                        {'$match': {'department': {'$exists': True}}}
                    ]
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': 'camera_name',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'panel_data',
                            'localField': 'camera_name',
                            'foreignField': 'data.camera_name',
                            'as': 'Newcameradetailspaneld'
                        }},
                        {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                                    'then': '$department',
                                    'else': '$Newcameradetailspaneld.department'
                                }
                            }
                        }},
                        {'$unset': 'Newcameradetailspaneld'},
                        {'$sort': {'timestamp': -1}},
                        {'$match': {'department': {'$exists': True}}}
                    ]
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': 'camera_name',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', department_name]},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'panel_data',
                            'localField': 'camera_name',
                            'foreignField': 'data.camera_name',
                            'as': 'Newcameradetailspaneld'
                        }},
                        {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                                    'then': '$department',
                                    'else': '$Newcameradetailspaneld.department'
                                }
                            }
                        }},
                        {'$unset': 'Newcameradetailspaneld'},
                        {'$sort': {'timestamp': -1}},
                        {'$match': {'department': {'$exists': True}}}
                    ]

                # print('--------------------------------pipeline=====1==11=1=1---------------',pipeline)
                data = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = VIolationcountforPPE(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1
                            wapas_data['SNo'] = count1
                            dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                    all_data = PPELIVECOUNT(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found' 

        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    else:
        if camera_name is not None :
            match_data['camera_name']=camera_name
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': 'camera_name',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'panel_data',
                            'localField': 'camera_name',
                            'foreignField': 'data.camera_name',
                            'as': 'Newcameradetailspaneld'
                        }},
                        {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                                    'then': '$department',
                                    'else': '$Newcameradetailspaneld.department'
                                }
                            }
                        }},
                        {'$unset': 'Newcameradetailspaneld'},
                        {'$sort': {'timestamp': -1}},
                        {'$match': {'department': {'$exists': True}}}
                    ]

        if (department_name is not None and department_name != 'none'):
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': 'camera_name',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', department_name]},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'panel_data',
                            'localField': 'camera_name',
                            'foreignField': 'data.camera_name',
                            'as': 'Newcameradetailspaneld'
                        }},
                        {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                                    'then': '$department',
                                    'else': '$Newcameradetailspaneld.department'
                                }
                            }
                        }},
                        {'$unset': 'Newcameradetailspaneld'},
                        {'$sort': {'timestamp': -1}},
                        {'$match': {'department': {'$exists': True}}}
                    ]
        else:
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': 'camera_name',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                        {'$unset': 'camera_data'},
                        {'$sort': {'timestamp': -1}},
                        #{'$match': {'$or': [{'department': {'$exists': True}}, {'data.panel_data.panel_number': {'$exists': True}}]}},
                        {'$lookup': {
                            'from': 'panel_data',
                            'localField': 'camera_name',
                            'foreignField': 'data.camera_name',
                            'as': 'Newcameradetailspaneld'
                        }},
                        {'$unwind': {'path': '$Newcameradetailspaneld', 'preserveNullAndEmptyArrays': True}},
                        {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': [{'$type': '$Newcameradetailspaneld.department'}, 'missing']},
                                    'then': '$department',
                                    'else': '$Newcameradetailspaneld.department'
                                }
                            }
                        }},
                        {'$unset': 'Newcameradetailspaneld'},
                        {'$sort': {'timestamp': -1}},
                        {'$match': {'department': {'$exists': True}}}
                    ]

        # print('==================================pipeline==================',pipeline)
        data = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
        if len(data) != 0:
            count1 = 0 
            for count, i in enumerate(data):
                wapas_data = VIolationcountforPPE(i,Foundfileterdata)
                if type(wapas_data) == list:
                    pass
                elif wapas_data:
                    count1 +=1
                    wapas_data['SNo'] = count1
                    dash_data.append(wapas_data)
                else:
                    count1 +=1
                    i['SNo'] = count1
                    dash_data.append(i)
            all_data = PPELIVECOUNT(len(dash_data), parse_json(dash_data))
            ret = all_data
        else:
            ret['message'] = 'data not found' 
    # return jsonify(ret)
    socketio.emit('SOCKETlive_data1PPE', ret)




def CCLIVECOUNT(live_data_count, all_data):
    try:
        data = CRlive_data_count.find_one()
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
            result =CRlive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = CRlive_data_count.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- CCLIVECOUNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        #ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30


@socketio.on('SOCKETlive_data1CC')
def LIVEVIOLATIONOFCC(CrowdcountINputdata):
    camera_name=None
    violation_type= 'CRDCNT'
    department_name =None
    if 'camera_name' in CrowdcountINputdata:
        if CrowdcountINputdata['camera_name'] is not None:
            camera_name = CrowdcountINputdata['camera_name']
    if 'department_name' in CrowdcountINputdata:
        if CrowdcountINputdata['department_name'] is not None:
            department_name = CrowdcountINputdata['department_name']
    ret = {'success': False,'message':"something went wrong in live_data1 apis"}
    pipeline=[]
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
    if CrowdcountINputdata is not None:
        jsonobject = CrowdcountINputdata
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['camera_name', 'department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                camera_name = jsonobject['camera_name']
                department_name = jsonobject['department_name']
                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and    department_name !='') :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {
                                    '$lookup': {
                                        'from': 'ppera_cameras',
                                        'localField': 'camera_name',
                                        'foreignField': 'cameraname',
                                        'as': 'camera_data'
                                    }
                                },
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                            'department': {
                                                '$cond': {
                                                    'if': {'$eq': ['$camera_data.department', department_name]},
                                                    'then': '$camera_data.department',
                                                    'else': '$$REMOVE'
                                                }
                                            }
                                        }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'timestamp': -1}},
                                {'$match': {'department': {'$exists': True}}}
                            ]
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {
                                    '$lookup': {
                                        'from': 'ppera_cameras',
                                        'localField': 'camera_name',
                                        'foreignField': 'cameraname',
                                        'as': 'camera_data'
                                    }
                                },
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                            'department': {
                                                '$cond': {
                                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                                    'then': '$camera_data.department',
                                                    'else': '$$REMOVE'
                                                }
                                            }
                                        }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'timestamp': -1}},
                                {'$match': {'department': {'$exists': True}}}
                            ]
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    pipeline = [
                            {'$match': match_data},
                            {'$limit': 4000000},
                            {'$sort': {'timestamp': -1}},
                            {
                                '$lookup': {
                                    'from': 'ppera_cameras',
                                    'localField': 'camera_name',
                                    'foreignField': 'cameraname',
                                    'as': 'camera_data'
                                }
                            },
                            {'$unwind': '$camera_data'},
                            {'$addFields': {
                                        'department': {
                                            '$cond': {
                                                'if': {'$eq': ['$camera_data.department', department_name]},
                                                'then': '$camera_data.department',
                                                'else': '$$REMOVE'
                                            }
                                        }
                                    }},
                            {'$unset': 'camera_data'},  
                            {'$sort': {'timestamp': -1}},
                            {'$match': {'department': {'$exists': True}}}
                                                ]
                else:
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                {
                                    '$lookup': {
                                        'from': 'ppera_cameras',
                                        'localField': 'camera_name',
                                        'foreignField': 'cameraname',
                                        'as': 'camera_data'
                                    }
                                },
                                {'$unwind': '$camera_data'},
                                {'$addFields': {
                                            'department': {
                                                '$cond': {
                                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                                    'then': '$camera_data.department',
                                                    'else': '$$REMOVE'
                                                }
                                            }
                                        }},
                                {'$unset': 'camera_data'},  
                                {'$sort': {'timestamp': -1}},
                                {'$match': {'department': {'$exists': True}}}]
                data = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
                if len(data) != 0:
                    all_data = CCLIVECOUNT(len(data), parse_json(data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'   
        
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    else:    
        dash_data = []    
        if camera_name is not None :
            match_data['camera_name']=camera_name
            pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}},
                {
                    '$lookup': {
                        'from': 'ppera_cameras',
                        'localField': 'camera_name',
                        'foreignField': 'cameraname',
                        'as': 'camera_data'
                    }
                },
                {'$unwind': '$camera_data'},
                {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                {'$unset': 'camera_data'},  
                {'$sort': {'timestamp': -1}},
                {'$match': {'department': {'$exists': True}}}
            ]

        if (department_name is not None and department_name != 'none'):
            pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}},
                {
                    '$lookup': {
                        'from': 'ppera_cameras',
                        'localField': 'camera_name',
                        'foreignField': 'cameraname',
                        'as': 'camera_data'
                    }
                },
                {'$unwind': '$camera_data'},
                {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', department_name]},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                {'$unset': 'camera_data'},  
                {'$sort': {'timestamp': -1}},
                {'$match': {'department': {'$exists': True}}}
            ]
        else:
            pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}},
                {
                    '$lookup': {
                        'from': 'ppera_cameras',
                        'localField': 'camera_name',
                        'foreignField': 'cameraname',
                        'as': 'camera_data'
                    }
                },
                {'$unwind': '$camera_data'},
                {'$addFields': {
                            'department': {
                                '$cond': {
                                    'if': {'$eq': ['$camera_data.department', '$camera_data.department']},
                                    'then': '$camera_data.department',
                                    'else': '$$REMOVE'
                                }
                            }
                        }},
                {'$unset': 'camera_data'},  
                {'$sort': {'timestamp': -1}},
                {'$match': {'department': {'$exists': True}}}
            ]


        print('-----------------------pipeline------------else-',pipeline)
        data = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))   
        if len(data) != 0:
            all_data = CCLIVECOUNT(len(data), parse_json(data))
            ret = all_data
        else:
            ret['message'] = 'data not found' 
    # return jsonify(ret)
    socketio.emit('SOCKETlive_data1CC',ret)


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
            
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- MUPANRRILATION222_multi_isolation 1", str(error), " ----time ---- ", now_time_with_time()]))
    return all_data

def check_magnetic_flasher_status(listOFdata):
    all_data = []
    # print("length of the data====new sorted==",len(listOFdata))
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- 333 1", str(error), " ----time ---- ", now_time_with_time()])) 
    return joinedlist

def riro_live_data(live_riro_data):
    for index_no, live_form in enumerate(live_riro_data):
        check_data = [{'sort_id': live_form['_id'], 'panel_no': live_form['panel_no'], 'rack_method': None, 'rack_process': None,'irrd_in_time': None, 'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None, 'tag_time': None, 'five_meter': None, 'barricading': None, 'magnetic_flasher': live_form['magnetic_flasher'], 'violation': False, 'riro_key_id': None,'riro_merged_image': None, 'riro_merged_image_size':{'height':None, 'width': None}, 'riro_edit_status': False,'lock_tag_image': None, 'remarks': live_form['remarks']}]
    return check_data

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

def all_riro_final_sortin(final_test_sort):
    return riro_for_history(final_test_sort)

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

def hydralockdataFetch(FINDHYDRADATA):
    hydralic_status= False
    only_two_data =[]
    if FINDHYDRADATA['type']=='hydraulic' or FINDHYDRADATA['type']=='pneumatic' or FINDHYDRADATA['type']=='Hydraulic' or FINDHYDRADATA['type']=='Pneumatic':
        if isEmpty(FINDHYDRADATA['data']) :
            FINDHYDRADATA= list(MEchHydracollection.find({'camera_rtsp':FINDHYDRADATA['data']['rtsp_url'],"camera_name":FINDHYDRADATA['data']['camera_name']}, sort=[('_id',   pymongo.DESCENDING)]))#.sort({"_id":1}).limit(1))#.sort({"_id":1}).limit(1)
            if len(FINDHYDRADATA) != 0 :
                newlist = sorted(FINDHYDRADATA, key=lambda d: d['_id']) 
                for u,i in enumerate(newlist):
                    if u > 0:
                        break
                    only_two_data.append(i)    
                hydralic_status = check_the_hydralic_process_(only_two_data)
    return only_two_data , hydralic_status       
          

@socketio.on('SOCKETmultiisolation')
def multii44solation_convayor_pnumertic_hydralic23323(id = None):
    while 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        sheet_data=None
        if id is not None:
            sheet_data = job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
        else:            
            sheet_data =job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])     
        if sheet_data is not None:
            data = list(panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0:
                final_panel_data = []   
                data = MUPANRRILATION_multi_isolation(data)
                riro_final = []
                for ___INNN, emmmi in enumerate(data):
                    if (emmmi['type']=='HT' or emmmi['type']=='ht' ) :
                        if isEmpty(emmmi['data']) :
                            if (type(emmmi['data']['panel_data']) != list) :
                                if emmmi['data']['panel_data']['panel_id'] is not None:
                                    show_live_riro = list(riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url'], 'panel_no': emmmi['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                    
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
                                        find_riro_data = list(riro_data.find({'token': emmmi['token'], 'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
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
        socketio.emit('SOCKETmultiisolation',ret)
        time.sleep(1)

def with_campare_time_and_get_latest_data_of_riro(to_find_latest_data):
    temp = '0000-00-00 00:00:00'
    set_value = None
    for ooo, ter in enumerate(to_find_latest_data):
        if temp < ter['irrd_in_time']:
            temp = ter['irrd_in_time']
            set_value = ter
    return set_value


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


def check_ppe_violation_at_riro_moment(rtsp_url, panel_id, person_in_time,person_out_time):
    violation_test = False
    find_violation_data = list(PPERAVIOLATIONCOLLECTION.find({'camera_rtsp': rtsp_url,'timestamp':{'$gte': person_in_time, '$lte': person_out_time},'violation_status': True}).sort('timestamp', -1))
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
    check_panel_status = riro_history_riro_for_sorting_only_two(match_data)
    return riro_history_riro_for_sorting_only_two(match_data), check_the_rackout_process_(check_panel_status), check_riro_edit_status(match_data)

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


def sort_irrd_time_for_history(time_stamp_data):
    final_time_sort = sorted(time_stamp_data, key=time_sort_key_for_history,reverse=True)
    return final_time_sort



def time_sort_key_for_history(d):
    return d['riro_data'][0]['irrd_in_time']

@socketio.on('SOCKETget_job_sheet_status')
def get_job_she333et_status_of_current(id=None):
    while 1:
        ret = {'message': 'Something went wrong with job sheet status api','success': False}
        if 1:
        # try:
            all_data = []
            sheet_data=None
            if id is not None:
                sheet_data = job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
            else:            
                sheet_data = job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
            if sheet_data is not None:
                riro_return_data = []
                data1 = list(panel_data.find({'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                if len(data1) != 0:
                    all_data =FUNCHECKrepeativeJobSheetstatus(data1)
                    for ___12, iisddf in enumerate(all_data):
                        if iisddf['type']=="HT" or iisddf['type']=='ht':
                            find_riro_data = list(riro_data.find({'token': sheet_data['token'], 'camera_name': iisddf['data']['camera_name'], 'camera_rtsp': iisddf['data']['rtsp_url']}, sort=[ ('_id', pymongo.DESCENDING)]))
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
                        final_data = {'total_panel_count': total_panel_count,'processed_count': rack_method_done_count,'not_processed': rack_method_not_done_count,'rack_out_count':pending_rack_ou_count,'ppe_violation':0, 'five_meter_violation':0}
                        ret = {'message': final_data, 'success': True}
                    else:
                        ret['message'] = 'data not found.'
                else:
                    ret['message'] = 'panel_data is not found.'
            else:
                ret['message'] = 'job sheet is not uploaded yet'
        socketio.emit('SOCKETget_job_sheet_status',ret)
        time.sleep(7)






def UnplannedRIROLivecount(live_data_count, all_data):
    try:
        data = unplanedLivecount.find_one()
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
            result = unplanedLivecount.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = unplanedLivecount.insert_one(dictionary)
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


@socketio.on('SOCKETGetUnplannedLivecount')
def GetUnplannedFORRIROLivecount():
    if 1:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        sheet_data = job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
        if sheet_data is not None:
            data = list(riro_unplanned.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, {'cameraid':0,'analytics_id':0,'panel_no':0,'cropped_panel_image_path':0,'five_meter':0,
                                                                                                                                    'flasher_status':0,'appruntime':0,'appruntime':0,'id':0,'barricading':0,'date':0,'riro_merged_image':0,'riro_merged_image_size':0,
                                                                                                                                    'lock':0,'lock_time':0,'magnetic_flasher':0,'person_in_time':0,'person_out_time':0,'within_15_min':0,'tag':0,'tag_time':0},sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0:                 
                ret=UnplannedRIROLivecount(len(data), data)
            else:
                ret['message'] = 'there is no data found for unplanned jobs'
        else:
            ret['message'] ="jobsheet is not yet uploaded, please upload the jobsheet"
    
    socketio.emit('SOCKETGetUnplannedLivecount',parse_json(ret))

    # return parse_json(ret)



@socketio.on('SOCKETMechmultiisolation')
def multii44solation_convayor_errpnumertic_hydralic23323(id = None):
    if 1:
    # try:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        ret['job_sheet_status'] = False
        sheet_data=None
        if id is not None:
            sheet_data =mechjob_sheet.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
        else:            
            sheet_data = mechjob_sheet.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])     
        if sheet_data is not None:
            data = list(mechesi.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',   pymongo.DESCENDING)]))
            if len(data) !=0:# is not None:
                final_panel_data = []   
                data = MUPANRRILATION_multi_isolation(data)
                riro_final = []
                for ___INNN, emmmi in enumerate(data):
                    if (emmmi['type']=='HT' or emmmi['type']=='ht' ) :
                        if isEmpty(emmmi['data']) :
                            if (type(emmmi['data']['panel_data']) != list) :
                                if emmmi['data']['panel_data']['panel_id'] is not None:
                                    show_live_riro = list(riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url'], 'panel_no': emmmi['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                    
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
                                        find_riro_data = list(riro_data.find({'token': emmmi['token'], 'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
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
    socketio.emit('SOCKETGetUnplannedLivecount',parse_json(ret))
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
    # return ret




# @socketio.on('SOCKETcheck_process')
# Start the Socket.IO server
def init_socketio(app):
    socketio.init_app(app)



