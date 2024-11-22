from Data_recieving_and_Dashboard.packages import *
violationanalysis_data = Blueprint('violationanalysis_data', __name__)


@violationanalysis_data.route('/systemdetails', methods=['GET'])
def get_system_utilization():
    # Get system memory information
    memory_info = psutil.virtual_memory()
    memory_dict = {
        "total_ram": round(memory_info.total / (1024 ** 3), 2),
        "available_ram": round(memory_info.available / (1024 ** 3), 2),
        "used_ram": round(memory_info.used / (1024 ** 3), 2),
        "ram_utilization": memory_info.percent
    }

    # Get GPU information
    gpus = GPUtil.getGPUs()
    gpu_list = []
    for gpu in gpus:
        gpu_list.append({
            "gpu_id": gpu.id,
            "gpu_name": gpu.name,
            "total_gpu_memory": round(gpu.memoryTotal / 1024, 2),
            "available_gpu_memory": round(gpu.memoryFree / 1024, 2),
            "used_gpu_memory": round(gpu.memoryUsed / 1024, 2),
            "gpu_memory_utilization": round(gpu.memoryUtil * 100, 1),
            "gpu_utilization": round(gpu.load * 100, 1),
            "gpu_temperature": gpu.temperature
        })

    # Get storage information
    if platform.system() == "Windows":
        root_directory = "C:\\"
    else:
        root_directory = "/"
    
    storage_usage = psutil.disk_usage(root_directory)
    storage_dict = {
        "storage_device": root_directory,
        "total_storage": round(storage_usage.total / (1024 ** 3), 2),
        "free_storage": round(storage_usage.free / (1024 ** 3), 2),
        "used_storage": round(storage_usage.used / (1024 ** 3), 2),
        "storage_utilization": storage_usage.percent
    }

    # Combine everything into a final result dictionary
    system_utilization = {
        "memory_utilization": memory_dict,
        "gpu_utilization": gpu_list,
        "storage_utilization": storage_dict
    }

    return system_utilization

@violationanalysis_data.route('/get_video/<video_name>', methods=['GET'])
def get_video(video_name):
    try:
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500)


@violationanalysis_data.route('/get_Conveyor_belt_video', methods=['GET'])
def get_Conveyor_belt_video():
    try:
        video_name = "Conveyor_belt.mp4"
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)      
        # file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500)


@violationanalysis_data.route('/get_Conveyor_pipe_video', methods=['GET'])
def get_Conveyor_pipe_video():
    try:
        video_name = "Conveyor_pipe.mp4"
        # custom_video_path = "/home/docketrun/Videos/Custom_SOP's_Videos"
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)        
        # file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500)




@violationanalysis_data.route('/get_Crane_guard_video', methods=['GET'])
def get_Crane_guard_video():
    try:
        video_name = "Crane_guard.mp4"
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)              
        # file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500)



@violationanalysis_data.route('/get_Crop_Shear_HSM2_video', methods=['GET'])
def get_Crop_Shear_HSM2_video():
    try:
        video_name = 'Crop_Shear.mp4'
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)              
        # file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500)
    
   
@violationanalysis_data.route('/get_OCR_Coke_video', methods=['GET'])
def get_OCR_Coke_video():
    try:
        video_name = 'OCR_Coke.mp4'
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)              
        # file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500) 
    

   
@violationanalysis_data.route('/get_OCR_WRM_video', methods=['GET'])
def get_OCR_WRM_video():
    try:
        video_name = 'OCR_WRM.mp4'
        base_path = os.path.join(os.getcwd() ,'smaple_files', "dashboardvideo")
        file_path = os.path.join(base_path, video_name)            
        # file_path = os.path.join(base_path, video_name)        
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise FileNotFoundError(f"The file {video_name} does not exist.")        
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_video 1", str(error), " ----time ---- ", now_time_with_time()]))
        return Response(f"An error occurred: {str(error)}", status=500) 

@violationanalysis_data.route('/SoftWare_info', methods=['GET'])
def SoftWare_info():
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
        if request.method == 'POST':
            jsonobject = request.json
            print('-----------------jsonobject---------',jsonobject)
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['ppepercentage']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    all_data = []
                    ppepercentage = jsonobject['ppepercentage'] 
                    if 'crash_helmet'  in ppepercentage and ppepercentage is not None:   
                        Foundfileterdata = mongo.db.filterviolations.find_one({})
                        if Foundfileterdata is not None:
                            id = Foundfileterdata['_id']
                            FILterviolationUPdateresult = mongo.db.filterviolations.update_one({'_id':ObjectId(id)}, {'$set':ppepercentage})
                            if FILterviolationUPdateresult.modified_count > 0:
                                ret = {'message':'filter percentage is set successfully.','success': True}
                            else:
                                ret = {'message':'filter percentage is set already.','success': True}
                        else :
                            filterviolationsinsertionresult =  mongo.db.filterviolations.insert_one(ppepercentage)  
                            if filterviolationsinsertionresult.acknowledged > 0  :
                                ret ={'message':'filter percentage is set successfully.','success':True}   
                            else:
                                ret['message']='something wrong with the insertion of filter percentage.'  
                    elif ppepercentage is not None:
                        Foundfileterdata = mongo.db.filterviolations.find_one({})
                        if Foundfileterdata is not None:
                            id = Foundfileterdata['_id']
                            FILterviolationUPdateresult = mongo.db.filterviolations.update_one({'_id':ObjectId(id)}, {'$set':{"helmet":ppepercentage['helmet'],"vest":ppepercentage['vest']}})
                            if FILterviolationUPdateresult.modified_count > 0:
                                ret = {'message':'filter percentage is set successfully.','success': True}
                            else:
                                ret = {'message':'filter percentage is set already.','success': True}
                        else :
                            filterviolationsinsertionresult =  mongo.db.filterviolations.insert_one(ppepercentage)  
                            if filterviolationsinsertionresult.acknowledged > 0  :
                                ret ={'message':'filter percentage is set successfully.','success':True}   
                            else:
                                ret['message']='something wrong with the insertion of filter percentage.'                
                        
            else:
                ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
        elif request.method == 'GET':
            Foundfileterdata = mongo.db.Software_info.find_one({},{'_id':0})
            if Foundfileterdata is not None:
                ret = {'message':Foundfileterdata,'success': True}
            else :
                ppepercentage = {
                    "name": "DocketEye",
                    "tag_name": "v-0.2.1-2",
                    "body": "I am a Perimeter Security Specialist, helping safeguard your premises by monitoring and making decisions to halt machinery or raise alerts when necessary.\r\n\r\nI am a Safety Inspector, assisting in ensuring your safety by monitoring adherence to safety regulations and standards.\r\n\r\nI am a Crowd Manager, responsible for ensuring safety, preventing overcrowding, and maintaining order.\r\n\r\nI am a Traffic enforcement officer, responsible for observing and managing traffic flow.\r\n\r\nI am a parking enforcement officer, responsible for overseeing parking areas, ensuring that vehicles are parked correctly, and enforcing parking regulations.\r\n\r\nI am DocketEye.\r\n\r\nWhats new ?\r\n\r\n1. patch update for TJM is provided.",
                    "published_at": "",
                    "target_commitish": ""
                }
                filterviolationsinsertionresult =  mongo.db.Software_info.insert_one(ppepercentage)  
                if filterviolationsinsertionresult.acknowledged > 0  :
                    ret ={'message':ppepercentage,'success':True}   
                else:
                    ret['message']='something wrong with the of filter percentage.'   
    return jsonify(ret)

@violationanalysis_data.route('/set_rtsp_flag/<flag>', methods=['GET'])
def set_rtsp_flag_creating_config(flag=0):
    ret = {'message':'something went wrong with set_rtsp_flag_creating_config.','success': False}
    try:
        if flag is not None:
            if flag != 'undefined':
                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
                if find_data is not None:
                    id = find_data['_id']
                    result = mongo.db.rtsp_flag.update_one({'_id': ObjectId (id)}, {'$set':{'rtsp_flag': flag}})
                    if result.modified_count > 0:
                        ret = {'message': 'rtsp flag updated successfully.','success': True}
                    elif find_data['rtsp_flag'] == '0':
                        ret = {'message': 'flag has been set for rtsp.','success': True}
                    elif find_data['rtsp_flag'] == '1':
                        ret = {'message': 'flag has been set for rtspt.','success': True}
                else:
                    result = mongo.db.rtsp_flag.insert_one({'rtsp_flag': flag})
                    if result.acknowledged > 0:
                        ret = {'message':'rtsp flag inserted successfully.', 'success': True}
                    else:
                        ret['message'] = 'rtsp flag is not inserted.'
            else:
                ret['message'] = 'rtsp flag should not be undefined'
        else:
            ret['message'] = 'rtsp flag should not be none value.'
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 2", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    return ret


@violationanalysis_data.route('/CONFIGConfiguration', methods=['POST'])
@violationanalysis_data.route('/CONFIGConfiguration', methods=['GET'])
def CONFIGConfigaration():    
    ret = {'message':'something went wrong with CONFIGarations .','success': False}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['configuration_data']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                configuration_data = jsonobject['configuration_data']   
                if configuration_data is not None:
                    print("configuration_data",configuration_data)
                    find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
                    if find_data is not None:
                        id = find_data['_id']
                        result = mongo.db.rtsp_flag.update_one({'_id': ObjectId (id)}, {'$set':configuration_data})
                        if result.modified_count > 0:
                            ret = {'message': 'configurations updated successfully.','success': True}
                        else:
                            ret['message']='already configuration is set.'
                    else:
                        configuration_data['rtsp_flag'] ='0'
                        result = mongo.db.rtsp_flag.insert_one(configuration_data)
                        if result.acknowledged > 0:
                            ret = {'message':'configurations inserted successfully.', 'success': True}
                        else:
                            ret['message'] = ' configuration is not inserted.'                           
                    #{"configuration_data": {"camera_fps":20,"drop_frame_interval":1,"data_save_interval":1,"rtsp_reconnect_interval":1}}
                else:
                    ret['message']='please give proper configuration data'
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}  
    elif request.method == 'GET':
        Foundfileterdata = mongo.db.rtsp_flag.find_one({},{'_id':0})
        if Foundfileterdata is not None:
            ret = {'message':Foundfileterdata,'success': True}
        else :
            ret['message']='configuration data is not found.' 
    # try:
    #     
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 2", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    return ret



def createmockdrillTable(parameter):
    database_detail = {'sql_panel_table':'mockdrill', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
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
    CREATE TABLE IF NOT EXISTS mockdrill (
        id SERIAL PRIMARY KEY,
        type VARCHAR,
        status VARCHAR
        );  
        '''
    try:
        cursor.execute(tablecreatequery)
        conn.commit() 
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
        
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY id desc')
        l1data_row = cursor.fetchone()
        cols_name = list(map(lambda x: x[0], cursor.description))
        if l1data_row is not None:
            res = dict(zip(cols_name, list(l1data_row)))
            update_data_query =''' UPDATE mockdrill SET status = %s WHERE id = %s;  '''
            if parameter==1 or  parameter=='1':
                new_status = 'on'
            else:
                new_status ='off'
            # new_status = 'Inactive'
            update_id = res['id']
            cursor.execute(update_data_query, (new_status, update_id))
            conn.commit()
            license_status = True
        else:
            insert_data_query = '''INSERT INTO mockdrill ( type,status) VALUES (%s, %s) RETURNING id;'''
            data_to_insert = ('mockdrill', 'off')
            if parameter==1 or  parameter=='1':
                data_to_insert = ('mockdrill', 'on')
            else:
                data_to_insert = ('mockdrill', 'off')
            cursor.execute(insert_data_query, data_to_insert)
            conn.commit()
            inserted_id = cursor.fetchone()[0]
            if inserted_id is not  None:
                license_status = True
            print(f'Data inserted with ID: {inserted_id}')
        
    except psycopg2.errors.UndefinedTable as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- check_license_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
    cursor.close()
    conn.close()
    return license_status
    


@violationanalysis_data.route('/Deleteviolation/<id>', methods=['GET'])
def Deleteviolation(id=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    try:
        if id is not None:
            find_data = mongo.db.data.find_one({'_id': ObjectId(id)})
            if find_data is not None:
                result = mongo.db.data.delete_one({'_id':ObjectId(id)})
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

@violationanalysis_data.route('/set_mockdrill/<flag>', methods=['GET'])
@violationanalysis_data.route('/set_mockdrill', methods=['GET'])
def set_mockdrill(flag=None):
    ret = {'message':'something went wrong with set_mockdrill.','success': False}
    # if 1:
    try:
        if flag is not None:
            if flag != 'undefined':
                find_data = mongo.db.mockdrill.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
                if find_data is not None:
                    id = find_data['_id']
                    if createmockdrillTable(flag):
                        try:
                            connection = psycopg2.connect(
                                user="docketrun",
                                password="docketrun",
                                host="localhost",
                                port="5432",
                                database="docketrundb"
                            )
                            # create_table_pintchrole(connection)
                            # for new, camera in enumerate(pintch_role_cameras):
                            postgres_insert_query =""" update  pinch_role_status set process=0"""
                            if flag==1 or flag =='1' :
                                postgres_insert_query = """ update  pinch_role_status set process=1"""


                            if True:
                                cursor = connection.cursor()
                            # try :
                                cursor.execute(postgres_insert_query)
                                connection.commit()
                                print("success")

                        except psycopg2.Error as e:
                            print(f"Unable to connect to the database. Error: {e}")
                        finally:
                            if connection:
                                connection.close()
                        
                        result = mongo.db.mockdrill.update_one({'_id': ObjectId (id)}, {'$set':{'mockdrill_flag': flag}})
                        if result.modified_count > 0:
                            ret = {'message': 'mock drill flag updated successfully.','success': True}
                        else:
                            ret['message'] = 'mock drill flag is already set.'
                    else:
                        ret['message'] = 'mock drill flag is not set.'
                else:
                    if createmockdrillTable(flag):
                        try:
                            connection = psycopg2.connect(
                                user="docketrun",
                                password="docketrun",
                                host="localhost",
                                port="5432",
                                database="docketrundb"
                            )
                            # create_table_pintchrole(connection)
                            # for new, camera in enumerate(pintch_role_cameras):
                            postgres_insert_query =""" update  pinch_role_status set process=0"""
                            if flag==1 or flag =='1' :
                                postgres_insert_query = """ update  pinch_role_status set process=1"""


                            if True:
                                cursor = connection.cursor()
                            # try :
                                cursor.execute(postgres_insert_query)
                                connection.commit()
                                print("success")

                        except psycopg2.Error as e:
                            print(f"Unable to connect to the database. Error: {e}")
                        finally:
                            if connection:
                                connection.close()
                        result = mongo.db.mockdrill.insert_one({'rtsp_flag': flag})
                        if result.acknowledged > 0:
                            ret = {'message':'mock drill flag inserted successfully.', 'success': True}
                        else:
                            ret['message'] = 'mock drill flag is already set.'
                    else:
                        ret['message'] = 'mock drill flag is not inserted.'
            else:
                ret['message'] = 'mock drill flag should not be undefined'
        else:
            find_data = mongo.db.mockdrill.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
            if find_data is not None:
                if find_data['mockdrill_flag']==1 or find_data['mockdrill_flag']=='1':
                    ret = {'message': 'mock drill is on.','success': True}
                else:
                    ret = {'message': 'mock drill is off.','success': False}
            else:
                ret['message'] = 'mock drill flag data not found.'    
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 2", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
    return ret


# def set_mockdrill(flag=None):
#     ret = {'message':'something went wrong with set_rtsp_flag_creating_config.','success': False}
#     # if 1:
#     try:
#         if flag is not None:
#             if flag != 'undefined':
#                 find_data = mongo.db.mockdrill.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
#                 if find_data is not None:
#                     id = find_data['_id']
#                     if createmockdrillTable(flag):
#                         result = mongo.db.mockdrill.update_one({'_id': ObjectId (id)}, {'$set':{'mockdrill_flag': flag}})
#                         if result.modified_count > 0:
#                             ret = {'message': 'mock drill flag updated successfully.','success': True}
#                         else:
#                             ret['message'] = 'mock drill flag is already set.'
#                     else:
#                         ret['message'] = 'mock drill flag is not set.'
#                 else:
#                     if createmockdrillTable(flag):
#                         result = mongo.db.mockdrill.insert_one({'rtsp_flag': flag})
#                         if result.acknowledged > 0:
#                             ret = {'message':'mock drill flag inserted successfully.', 'success': True}
#                         else:
#                             ret['message'] = 'mock drill flag is already set.'
#                     else:
#                         ret['message'] = 'mock drill flag is not inserted.'
#             else:
#                 ret['message'] = 'mock drill flag should not be undefined'
#         else:
#             find_data = mongo.db.mockdrill.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
#             if find_data is not None:
#                 if find_data['mockdrill_flag']==1 or find_data['mockdrill_flag']=='1':
#                     ret = {'message': 'mock drill is on.','success': True}
#                 else:
#                     ret = {'message': 'mock drill is off.','success': False}
#             else:
#                 ret['message'] = 'mock drill flag data not found.'    
#     except ( 
#         pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#         pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#         pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#         pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#         pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#         pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#         pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#         pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#         pymongo.errors.WriteError) as error:
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 1", str(error), " ----time ---- ", now_time_with_time()]))
#         ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
#         if restart_mongodb_r_service():
#             print("mongodb restarted")
#         else:
#             if forcerestart_mongodb_r_service():
#                 print("mongodb service force restarted-")
#             else:
#                 print("mongodb service is not yet started.") 
#     except Exception as  error:
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- set_rtsp_flag 2", str(error), " ----time ---- ", now_time_with_time()]))
#         ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
#     return ret




def update_hooter_details(ip_address, skip_value, connection_details):
    # Establish a connection to the database
    conn = psycopg2.connect(**connection_details)
    cursor = conn.cursor()

    # Define the query components
    existing_data_query = sql.SQL("""
        WITH existing_data AS (
            SELECT id
            FROM hooter_details_ga
            WHERE {skip_value} = ANY(skip) AND ip = {ip_address}
        )
        UPDATE hooter_details_ga
        SET status = 'OFF', processed = 0, skip = array_append(skip, {skip_value})
        WHERE ip = {ip_address} AND NOT EXISTS (SELECT 1 FROM existing_data);
    """).format(
        skip_value=sql.Literal(skip_value),
        ip_address=sql.Literal(ip_address)
    )

    try:
        # Execute the query
        cursor.execute(existing_data_query)
        conn.commit()

        # Check if any row was updated
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()

# Example usage


@violationanalysis_data.route('/violation_verification/<id>/<flag>', methods=['GET'])
@violationanalysis_data.route('/violation_verification', methods=['POST'])
def verification_of_violation(id=None, flag=0):
    ret = {'message': 'something went wrong with violation status .','success': False}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['camera_name','camera_rtsp','ticketno','id','verificationstatus','hooteraknowledgement','hooter_ip']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                camera_name = jsonobject['camera_name']      
                camera_rtsp = jsonobject['camera_rtsp'] 
                ticketno = jsonobject['ticketno'] 
                id = jsonobject['id'] 
                verificationstatus = jsonobject['verificationstatus'] 
                hooteraknowledgement = jsonobject['hooteraknowledgement']
                hooter_ip = jsonobject['hooter_ip']
                print("--------------------jsonobject---------------",jsonobject)           
                if  hooteraknowledgement ==False:
                    find_data = mongo.db.data.find_one({'_id': ObjectId(id)})
                    if find_data is not None:
                        if verificationstatus == 'false' or verificationstatus == False:
                            result = mongo.db.data.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.','success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        elif verificationstatus == 'true' or verificationstatus == True :
                            result = mongo.db.data.update_one({'_id':ObjectId(id)}, {'$set':{ 'violation_verificaton_status': True}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.' , 'success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        else:
                            ret = {'message':'violation status not updated .', 'success': False}
                    else:
                        ret['message'] = 'violation data is not found.'  
                elif hooteraknowledgement == True :
                    if hooter_ip is not None and hooter_ip !='':
                        connection_details = {
                                            'dbname': 'docketrundb',
                                            'user': 'docketrun',
                                            'password': 'docketrun',
                                            'host': 'localhost',
                                            'port': '5432'
                                        }

                        ip_address = hooter_ip
                        skip_value = ticketno
                        if update_hooter_details(ip_address, skip_value, connection_details):
                            print("Update successful")
                        else:
                            print("Update failed or no rows affected")
                    find_data = mongo.db.data.find_one({'_id': ObjectId(id)})
                    if find_data is not None:
                        if verificationstatus == 'false' or verificationstatus == False:
                            result = mongo.db.data.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False,'hooteraknowledgement':hooteraknowledgement}})
                            mongo.db.data.update_many({'ticketno': ticketno}, {'$set':{ 'hooteraknowledgement':hooteraknowledgement}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.','success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        elif verificationstatus == 'true' or verificationstatus == True :
                            result = mongo.db.data.update_one({'_id':ObjectId(id)}, {'$set':{ 'violation_verificaton_status': True,'hooteraknowledgement':hooteraknowledgement}})
                            mongo.db.data.update_many({'ticketno': ticketno}, {'$set':{ 'hooteraknowledgement':hooteraknowledgement}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.' , 'success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        else:
                            ret = {'message':'violation status not updated .', 'success': False}
                    else:
                        ret['message'] = 'violation data is not found.' 

                    
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    elif request.method == 'GET':
        try:
            if id is not None:
                if flag is not None:
                    if flag != 'undefined':
                        find_data = mongo.db.data.find_one({'_id': ObjectId(id)})
                        if find_data is not None:
                            if flag == 'false':
                                result = mongo.db.data.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False}})
                                if result.modified_count > 0:
                                    ret = {'message':'violation status updated successfully.','success': True}
                                else:
                                    ret = {'message':'violation status not updated .','success': False}
                            elif flag == 'true':
                                result = mongo.db.data.update_one({'_id':ObjectId(id)}, {'$set':{ 'violation_verificaton_status': True}})
                                if result.modified_count > 0:
                                    ret = {'message':'violation status updated successfully.' , 'success': True}
                                else:
                                    ret = {'message':'violation status not updated .','success': False}
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

@violationanalysis_data.route('/stop_phaseoneapp', methods=['GET'])
def stop_application_1_phaseoneapp():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        app_set_phaseoneapp_monitoring_started(True)

        app_set_common_monitoring_started(True)
        createHOOTERMETAJSONSTOP()
        if "voice_announcement_status" not in mongo.db.list_collection_names():
            print("Collection 'voice_announcement_status' does not exist")
        else:
            mongo.db.voice_announcement_status.delete_many({"violation_type": { "$in": ["RA", "PPE_TYPE1", "PPE_TYPE2","CRDCNT",'TJM'] }})
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret



def creation_of_222excel_functionWITHOUTIMAGE(list1):
    try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:F', 30)
        worksheet.set_row(0, 100)
        worksheet.set_row(1,  20)
        #worksheet.set_row(1, None, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(40)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:C1', 'Violation Data', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(18)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col , 'Violation Type', cell_format_1)
        worksheet.write(row, col + 1, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 2, 'Camera Name', cell_format_1)
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
        for i in list1:
            try:
                if cols == 0:
                    if i['analyticstype'] == 'RA':
                        worksheet.write(rows, cols, 'Restricted Area', cell_format_2)
                    elif i['analyticstype'] == 'ONB':
                        worksheet.write(rows, cols, 'Object Near By Truck',cell_format_2)
                    elif i['analyticstype'] == 'PPE_TYPE1':
                        worksheet.write(rows, cols, 'PPE', cell_format_2)
                if cols1 == 1:
                    date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols1, date_time,  date_format)
                if cols2 == 2:
                    worksheet.write(rows, cols2, i['camera_name'], cell_format_2)
                rows += 1
            except UnidentifiedImageError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 1", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
                UnidentifiedImageError_count += 1
            except FileNotFoundError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 2", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
                FileNotFoundError_count += 1
            except UserWarning as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 3", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except ImportError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 4", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except xlsxwriter.exceptions.FileCreateError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 5", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except PermissionError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 6", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except xlsxwriter.exceptions.XlsxWriterException as  error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 7", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.'}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ewitoutimagexcel_function 11", str(error), " ----time ---- ", now_time_with_time()]))
        ret = {'success': False, 'message': str(error)}
    return ret



def draw_bbox_and_insert_image(worksheet, image_path, alldata ,image_data, row, column):
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

    Newalldata = alldata
    source_img = Image.open(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', image_path))
    draw = ImageDraw.Draw(source_img)
    IMage_widthscal = source_img.width
    IMage_heigthscal = source_img.height
    alldata = image_roi_draw_data(alldata)
    imagename = os.path.splitext(image_path)[0]
    imgByteArr = None
    if type(alldata) != list:
        if alldata['analyticstype']=="PPE":
            if len(alldata['object_data']) != 0:
                try:
                    for ___, thiru in enumerate(alldata['object_data']):
                        Vestheight , Vestwidth,Vestx_value,Vesty_value=0,0,0,0
                        Helmetheight , Helmetwidth,Helmetx_value,Helmety_value=0,0,0,0
                        if thiru['Vest']=='no_ppe':
                            Vestheight = thiru['vest_bbox']['H']
                            Vestwidth = thiru['vest_bbox']['W']
                            Vestx_value = thiru['vest_bbox']['X']
                            Vesty_value = thiru['vest_bbox']['Y']     
                            Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                            text_width,text_height = calculate_text_size('NO-VEST',objectfont_size)                                    
                            text_x = Vestx_value + 6
                            text_y = Vesty_value +(Vestheight- Vesty_value)                           
                            text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-VEST')), text_y + text_height )
                            draw.rectangle(text_bg_position, fill='black')
                            draw.rectangle(Vestshape, outline='yellow', width=3)
                            draw.text((text_x, text_y), 'NO-VEST', 'yellow', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        if thiru['Helmet']== False:
                            Helmetheight = thiru['helmet_bbox']['H']
                            Helmetwidth = thiru['helmet_bbox']['W']
                            Helmetx_value = thiru['helmet_bbox']['X']
                            Helmety_value = thiru['helmet_bbox']['Y']
                            Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth , Helmetheight )]#(X + W, Y + H)
                            text_width,text_height = calculate_text_size("NO-HELMET",objectfont_size)
                            text_x = Helmetx_value + 6
                            text_y = Helmety_value +(Helmetheight- Helmety_value)    
                            # text_bg_position = (text_x - 5, text_y - 5, text_x + text_width + 10, text_y + text_height )
                            # draw.rectangle(text_bg_position, fill='black')   
                            draw.rectangle(Helmetshape, outline='red', width=3)
                            draw.text((text_x, text_y), "NO-HELMET", 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))                        
                        if Helmetheight==0 and Helmetwidth==0  and Helmetx_value==0 and Helmety_value==0 and Vestheight ==0 and Vestwidth ==0 and Vestx_value ==0 and Vesty_value ==0:
                            height = thiru['bbox']['H']
                            width = thiru['bbox']['W']
                            x_value = thiru['bbox']['X']
                            y_value = thiru['bbox']['Y']
                            w, h = width, height
                            shape = [(x_value, y_value), (w , h )]#(X + W, Y + H)
                            text_width,text_height = calculate_text_size('NO-PPE',objectfont_size)
                            text_x = x_value + 6
                            text_y = y_value +(height- y_value)                            
                            draw.rectangle(shape, outline='red', width=5)
                            text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-PPE')), text_y + text_height )
                            draw.rectangle(text_bg_position, fill='black')
                            draw.text((text_x, text_y), 'NO-PPE', 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    # imgByteArr = io.BytesIO()
                    # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                    imgByteArr = BytesIO()
                    source_img.save(imgByteArr, format='JPEG')
                    imgByteArr.seek(0)
                except Exception as error :
                    imgByteArr = BytesIO()
                    source_img.save(imgByteArr, format='JPEG')
                    imgByteArr.seek(0)
                    # imgByteArr = io.BytesIO()
                    # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                    # imgByteArr.seek(0)     

        elif alldata['analyticstype']=="PPE_TYPE2":
            if len(alldata['object_data']) != 0:
                try:
                    for ___, thiru in enumerate(alldata['object_data']):                        
                        height = thiru['bbox']['H']
                        width = thiru['bbox']['W']
                        x_value = thiru['bbox']['X']
                        y_value = thiru['bbox']['Y']
                        w, h = width, height
                        shape = [(x_value, y_value), (w , h )]#(X + W, Y + H)
                        text_width,text_height = calculate_text_size('BIKER',objectfont_size)
                        text_x = x_value + 6
                        text_y = y_value +(height- y_value)                            
                        draw.rectangle(shape, outline='red', width=5)
                        text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('BIKER')), text_y + text_height )
                        draw.rectangle(text_bg_position, fill='black')
                        draw.text((text_x, text_y), 'BIKER', 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    imgByteArr = BytesIO()
                    source_img.save(imgByteArr, format='JPEG')
                    imgByteArr.seek(0)
                    # imgByteArr = io.BytesIO()
                    # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                    # imgByteArr.seek(0)
                except Exception as error :
                    imgByteArr = BytesIO()
                    source_img.save(imgByteArr, format='JPEG')
                    imgByteArr.seek(0)
                    # imgByteArr = io.BytesIO()
                    # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                    # imgByteArr.seek(0)   
                       
        elif alldata['analyticstype']=="RA":
            if len(alldata['object_data']) != 0:
                ROISHAPE = alldata['analytics_data']
                if 'ROI_details' in ROISHAPE:
                    if type(ROISHAPE['ROI_details']) != list :
                        for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                            if BoundingBoxValueFORROI is not None:
                                BBOXVALUE = list(BoundingBoxValueFORROI.values())[0]
                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)                                                                 
                                text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                padding = 5
                                text_bg_position = (
                                    text_position[0] - padding,
                                    text_position[1] - padding,
                                    text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                    text_position[1] + text_height + padding
                                )
                                draw.rectangle(text_bg_position, fill='black')
                                if str(BoundingBoxValueFORROI['roi_name']) is None and str(BoundingBoxValueFORROI['roi_name'])=='':
                                    BoundingBoxValueFORROI['roi_name']='Region of interest'
                                draw.text(text_position, str(BoundingBoxValueFORROI['roi_name']), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                    else:
                        if len(ROISHAPE['ROI_details']) !=0 :
                            for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                if BoundingBoxValueFORROI is not None:
                                    BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                    if BBOXVALUE is not None:
                                        polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                        bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                        flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                        draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                        text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                        
                                        text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                        padding = 5
                                        text_bg_position = (
                                            text_position[0] - padding,
                                            text_position[1] - padding,
                                            text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                            text_position[1] + text_height + padding
                                        )                                           
                                        draw.rectangle(text_bg_position, fill='black')
                                        keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                        if keys_list is None and keys_list=='':
                                            keys_list='Region of interest'
                                        draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                        #draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))                            
                for ___, thiru in enumerate(alldata['object_data']):
                    height = thiru['bbox']['H']
                    width = thiru['bbox']['W']
                    x_value = thiru['bbox']['X']
                    y_value = thiru['bbox']['Y']
                    w, h = width, height
                    shape = [(x_value, y_value), (w - 10, h - 10)]
                    text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                    text_x = x_value + 6
                    text_y = y_value +(height- y_value)
                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                    draw.rectangle(text_bg_position, fill='black')
                    if thiru['class_name']=='truck':
                        draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                        #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                        draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='car':
                        draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                        draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='motorcycle'or thiru['class_name']=='motorbike':
                        draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                        draw.text((text_x, text_y), str(thiru['class_name']), '#ffa800', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bus':
                        draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                        draw.text((text_x, text_y), str(thiru['class_name']),busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bicycle':
                        draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                        draw.text((text_x, text_y), str(thiru['class_name']),bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='person':
                        draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                        draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                
                imgByteArr = BytesIO()
                source_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                
                # imgByteArr = io.BytesIO()
                # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                # imgByteArr.seek(0)

        elif alldata['analyticstype']=="RA":
            if len(alldata['object_data']) != 0:
                ROISHAPE = alldata['analytics_data']
                if 'ROI_details' in ROISHAPE:
                    if type(ROISHAPE['ROI_details']) != list :
                        for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                            if BoundingBoxValueFORROI is not None:
                                BBOXVALUE = list(BoundingBoxValueFORROI.values())[0]
                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)                                                                 
                                text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                padding = 5
                                text_bg_position = (
                                    text_position[0] - padding,
                                    text_position[1] - padding,
                                    text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                    text_position[1] + text_height + padding
                                )
                                draw.rectangle(text_bg_position, fill='black')
                                if str(BoundingBoxValueFORROI['roi_name']) is None and str(BoundingBoxValueFORROI['roi_name'])=='':
                                    BoundingBoxValueFORROI['roi_name']='Region of interest'
                                draw.text(text_position, str(BoundingBoxValueFORROI['roi_name']), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                    else:
                        if len(ROISHAPE['ROI_details']) !=0 :
                            for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                if BoundingBoxValueFORROI is not None:
                                    BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                    if BBOXVALUE is not None:
                                        polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                        bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                        flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                        draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                        text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                        
                                        text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                        padding = 5
                                        text_bg_position = (
                                            text_position[0] - padding,
                                            text_position[1] - padding,
                                            text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                            text_position[1] + text_height + padding
                                        )                                           
                                        draw.rectangle(text_bg_position, fill='black')
                                        keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                        if keys_list is None and keys_list=='':
                                            keys_list='Region of interest'
                                        draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")                           
                for ___, thiru in enumerate(alldata['object_data']):
                    height = thiru['bbox']['H']
                    width = thiru['bbox']['W']
                    x_value = thiru['bbox']['X']
                    y_value = thiru['bbox']['Y']
                    w, h = width, height
                    shape = [(x_value, y_value), (w - 10, h - 10)]
                    text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                    text_x = x_value + 6
                    text_y = y_value +(height- y_value)
                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                    draw.rectangle(text_bg_position, fill='black')
                    if thiru['class_name']=='truck':
                        draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                        #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                        draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='car':
                        draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                        draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='motorcycle'or thiru['class_name']=='motorbike':
                        draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                        draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bus':
                        draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                        draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bicycle':
                        draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                        draw.text((text_x, text_y), str(thiru['class_name']),bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='person':
                        draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                        draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                imgByteArr = BytesIO()
                source_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                
                
                # imgByteArr = io.BytesIO()
                # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                # imgByteArr.seek(0)
        elif alldata['analyticstype']=="CRDCNT":
            # print('-----------------------image_data-----------0.1',alldata)
            if isEmpty(alldata['analytics_data']) :
                CRDCNTDATA = alldata['analytics_data']
                if CRDCNTDATA['process_on_full_frame']==0:
                    for EachREgionIndex , EachRoiVALUES in enumerate(CRDCNTDATA['data']):
                        if isEmpty(EachRoiVALUES):
                            if EachRoiVALUES is not None:
                                BBOXVALUE = EachRoiVALUES['ROI_bbox']
                                if BBOXVALUE is not None:
                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                    flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                    draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                    text_position = get_text_position_within_polygon(EachRoiVALUES['ROI'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                        
                                    text_width, text_height = calculate_text_size(EachRoiVALUES['ROI'], roifont_size)
                                    padding = 5
                                    text_bg_position = (
                                        text_position[0] - padding,
                                        text_position[1] - padding,
                                        text_position[0] + text_width + padding + (len(EachRoiVALUES['ROI']) * 5),
                                        text_position[1] + text_height + padding
                                    )
                                    draw.rectangle(text_bg_position, fill='black')
                                    keys_list = EachRoiVALUES['ROI']
                                    if keys_list is None and keys_list=='':
                                        keys_list='Crowd Count Detection'
                                    draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
            elif 'crowdcountdetails' in image_data:
                if isEmpty(alldata['crowdcountdetails']):
                    CRROIDETAILS = alldata['crowdcountdetails']
                    if CRROIDETAILS:
                        if CRROIDETAILS['full_frame']==False:
                            BBOXVALUE = CRROIDETAILS['bb_box']
                            if BBOXVALUE is not None:
                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                text_position = get_text_position_within_polygon(CRROIDETAILS['area_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                text_width, text_height = calculate_text_size(CRROIDETAILS['area_name'], roifont_size)
                                padding = 5
                                text_bg_position = (
                                    text_position[0] - padding,
                                    text_position[1] - padding,
                                    text_position[0] + text_width + padding + (len(CRROIDETAILS['area_name']) * 5),
                                    text_position[1] + text_height + padding
                                )
                                draw.rectangle(text_bg_position, fill='black')
                                keys_list = CRROIDETAILS['area_name']
                                if keys_list is None and keys_list=='':
                                    keys_list='Crowd count area'
                                draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
            if len(alldata['object_data']) != 0:
                for ___, thiru in enumerate(alldata['object_data']):
                    if thiru['violation']:
                        height = thiru['bbox']['H']
                        width = thiru['bbox']['W']
                        x_value = thiru['bbox']['X']
                        y_value = thiru['bbox']['Y']
                        shape = [(x_value, y_value), ( width, height)]
                        text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                        text_position = (x_value + 6, y_value + 2)
                        text_x = x_value + 6
                        text_y = y_value + (height-y_value)
                        text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                        draw.rectangle(text_bg_position, fill='black')
                        if thiru['class_name']=='truck':
                            draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                            #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                            draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='car':
                            draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                            draw.text((text_x, text_y), str(thiru['class_name']), '#8b00ff', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                            draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                            draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='bus':
                            draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                            draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='bicycle':
                            draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                            draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='person':
                            draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                            draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
            # imgByteArr = io.BytesIO()
            # source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
            # imgByteArr.seek(0)   
            imgByteArr = BytesIO()
            source_img.save(imgByteArr, format='JPEG')
            imgByteArr.seek(0)     

        worksheet.insert_image(row, column, 'image.jpg', {'image_data': imgByteArr,'x_scale': 0.08900000, 'y_scale': 0.080})
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.08900000, 'y_scale': 0.080})
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.10, 'y_scale': 0.10})
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.12, 'y_scale': 0.12})
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': x_scale, 'y_scale': y_scale})
    else:
        # print('-----------------------image_data',Newalldata)
        if Newalldata['analyticstype']=="PPE":
            if len(Newalldata['object_data']) != 0:
                try:
                    for ___, thiru in enumerate(Newalldata['object_data']):
                        Vestheight , Vestwidth,Vestx_value,Vesty_value=0,0,0,0
                        Helmetheight , Helmetwidth,Helmetx_value,Helmety_value=0,0,0,0
                        if thiru['Vest']=='no_ppe':
                            Vestheight = thiru['vest_bbox']['H']
                            Vestwidth = thiru['vest_bbox']['W']
                            Vestx_value = thiru['vest_bbox']['X']
                            Vesty_value = thiru['vest_bbox']['Y']     
                            Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                            text_width,text_height = calculate_text_size('NO-VEST',objectfont_size)                                    
                            text_x = Vestx_value + 6
                            text_y = Vesty_value +(Vestheight- Vesty_value)                           
                            text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-VEST')), text_y + text_height )
                            draw.rectangle(text_bg_position, fill='black')
                            draw.rectangle(Vestshape, outline='yellow', width=3)
                            draw.text((text_x, text_y), 'NO-VEST', 'yellow', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        if thiru['Helmet']== False:
                            Helmetheight = thiru['helmet_bbox']['H']
                            Helmetwidth = thiru['helmet_bbox']['W']
                            Helmetx_value = thiru['helmet_bbox']['X']
                            Helmety_value = thiru['helmet_bbox']['Y']
                            Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth , Helmetheight )]#(X + W, Y + H)
                            text_width,text_height = calculate_text_size("NO-HELMET",objectfont_size)
                            text_x = Helmetx_value + 6
                            text_y = Helmety_value +(Helmetheight- Helmety_value)    
                            # text_bg_position = (text_x - 5, text_y - 5, text_x + text_width + 10, text_y + text_height )
                            # draw.rectangle(text_bg_position, fill='black')   
                            draw.rectangle(Helmetshape, outline='red', width=3)
                            draw.text((text_x, text_y), "NO-HELMET", 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))                        
                        if Helmetheight==0 and Helmetwidth==0  and Helmetx_value==0 and Helmety_value==0 and Vestheight ==0 and Vestwidth ==0 and Vestx_value ==0 and Vesty_value ==0:
                            height = thiru['bbox']['H']
                            width = thiru['bbox']['W']
                            x_value = thiru['bbox']['X']
                            y_value = thiru['bbox']['Y']
                            shape = [(x_value, y_value), (width , height )]#(X + W, Y + H)
                            text_width,text_height = calculate_text_size('NO-PPE',objectfont_size)
                            text_x = x_value + 6
                            text_y = y_value +(height- y_value)                            
                            draw.rectangle(shape, outline='red', width=5)
                            text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-PPE')), text_y + text_height )
                            draw.rectangle(text_bg_position, fill='black')
                            draw.text((text_x, text_y), 'NO-PPE', 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    imgByteArr = io.BytesIO()
                    source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                    imgByteArr.seek(0)
                except Exception as error :
                    imgByteArr = io.BytesIO()
                    source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                    imgByteArr.seek(0)                    
        elif Newalldata['analyticstype']=="RA":
            if len(Newalldata['object_data']) != 0:
                ROISHAPE = Newalldata['analytics_data']
                if 'ROI_details' in ROISHAPE:
                    if type(ROISHAPE['ROI_details']) != list :
                        for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                            if BoundingBoxValueFORROI is not None:
                                BBOXVALUE = list(BoundingBoxValueFORROI.values())[0]
                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)                                                                 
                                text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                padding = 5
                                text_bg_position = (
                                    text_position[0] - padding,
                                    text_position[1] - padding,
                                    text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                    text_position[1] + text_height + padding
                                )
                                draw.rectangle(text_bg_position, fill='black')
                                if str(BoundingBoxValueFORROI['roi_name']) is None and str(BoundingBoxValueFORROI['roi_name'])=='':
                                    BoundingBoxValueFORROI['roi_name']='Region of interest'
                                draw.text(text_position, str(BoundingBoxValueFORROI['roi_name']), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                    else:
                        if len(ROISHAPE['ROI_details']) !=0 :
                            for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                if BoundingBoxValueFORROI is not None:
                                    BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                    if BBOXVALUE is not None:
                                        polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                        bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                        flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                        draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                        text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                        
                                        text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                        padding = 5
                                        text_bg_position = (
                                            text_position[0] - padding,
                                            text_position[1] - padding,
                                            text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                            text_position[1] + text_height + padding
                                        )                                                
                                        # Draw the background rectangle for the text
                                        draw.rectangle(text_bg_position, fill='black')
                                        keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                        if keys_list is None and keys_list=='':
                                            keys_list='Region of interest'
                                        draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")                          
                for ___, thiru in enumerate(Newalldata['object_data']):
                    height = thiru['bbox']['H']
                    width = thiru['bbox']['W']
                    x_value = thiru['bbox']['X']
                    y_value = thiru['bbox']['Y']
                    w, h = width, height
                    shape = [(x_value, y_value), (w - 10, h - 10)]
                    text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                    text_x = x_value + 6
                    text_y = y_value +(height- y_value)
                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                    draw.rectangle(text_bg_position, fill='black')
                    if thiru['class_name']=='truck':
                        draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                        #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                        draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='car':
                        draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                        draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                        draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                        draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bus':
                        draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                        draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bicycle':
                        draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                        draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='person':
                        draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                        draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                imgByteArr = io.BytesIO()
                source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                imgByteArr.seek(0)
        elif Newalldata['analyticstype']=="CRDCNT":
            if isEmpty(Newalldata['analytics_data']) :
                CRDCNTDATA = Newalldata['analytics_data']
                if CRDCNTDATA['process_on_full_frame']==0:
                    for EachREgionIndex , EachRoiVALUES in enumerate(CRDCNTDATA['data']):
                        if isEmpty(EachRoiVALUES):
                            if EachRoiVALUES is not None:
                                BBOXVALUE = EachRoiVALUES['ROI_bbox']
                                if BBOXVALUE is not None:
                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                    flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                    draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                    text_position = get_text_position_within_polygon(EachRoiVALUES['ROI'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', objectfont_size, encoding='unic'))
                                        
                                    text_width, text_height = calculate_text_size(EachRoiVALUES['ROI'], roifont_size)
                                    padding = 5
                                    text_bg_position = (
                                        text_position[0] - padding,
                                        text_position[1] - padding,
                                        text_position[0] + text_width + padding + (len(EachRoiVALUES['ROI']) * 5),
                                        text_position[1] + text_height + padding
                                    )
                                    draw.rectangle(text_bg_position, fill='black')
                                    if keys_list is None and keys_list=='':
                                        keys_list='Crowd Count Detection'
                                    draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
            elif 'crowdcountdetails' in image_data:
                if isEmpty(Newalldata['crowdcountdetails']):
                    CRROIDETAILS = Newalldata['crowdcountdetails']
                    if CRROIDETAILS:
                        if CRROIDETAILS['full_frame']==False:
                            BBOXVALUE = CRROIDETAILS['bb_box']
                            if BBOXVALUE is not None:
                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                text_position = get_text_position_within_polygon(CRROIDETAILS['area_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                text_width, text_height = calculate_text_size(CRROIDETAILS['area_name'], roifont_size)
                                padding = 5
                                text_bg_position = (
                                    text_position[0] - padding,
                                    text_position[1] - padding,
                                    text_position[0] + text_width + padding + (len(CRROIDETAILS['area_name']) * 5),
                                    text_position[1] + text_height + padding
                                )
                                draw.rectangle(text_bg_position, fill='black')
                                keys_list = CRROIDETAILS['area_name']
                                if keys_list is None and keys_list=='':
                                    keys_list='Crowd count area'
                                draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
            if len(Newalldata['object_data']) != 0:
                for ___, thiru in enumerate(Newalldata['object_data']):
                    if thiru['violation']:
                        height = thiru['bbox']['H']
                        width = thiru['bbox']['W']
                        x_value = thiru['bbox']['X']
                        y_value = thiru['bbox']['Y']
                        shape = [(x_value, y_value), ( width, height)]
                        text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                        text_position = (x_value + 6, y_value + 2)
                        text_x = x_value + 6
                        text_y = y_value + (height-y_value)
                        text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                        draw.rectangle(text_bg_position, fill='black')
                        if thiru['class_name']=='truck':
                            draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                            #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                            draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='car':
                            draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                            draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                            draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                            draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='bus':
                            draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                            draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='bicycle':
                            draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                            draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                        elif thiru['class_name']=='person':
                            draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                            draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
            imgByteArr = io.BytesIO()
            source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
            imgByteArr.seek(0)  
        worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.08900000, 'y_scale': 0.080})      
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.08900000, 'y_scale': 0.080})  
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.12, 'y_scale': 0.12})
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),{'x_scale':x_scale, 'y_scale': y_scale})# {'x_scale': x_scale, 'y_scale': y_scale})
        #worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),{'x_scale':x_scale, 'y_scale': y_scale})# {'x_scale': x_scale, 'y_scale': y_scale})


def OnlyForTRA(worksheet, image_path, alldata ,image_data, row, column):
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

    Newalldata = alldata
    source_img = Image.open(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', image_path))
    draw = ImageDraw.Draw(source_img)
    IMage_widthscal = source_img.width
    IMage_heigthscal = source_img.height
    alldata = image_roi_draw_data(alldata)
    imagename = os.path.splitext(image_path)[0]
    if type(alldata) != list:
        if alldata['analyticstype']=="RA":
            if len(alldata['object_data']) != 0:
                ROISHAPE = alldata['analytics_data']
                if 'ROI_details' in ROISHAPE:
                    if type(ROISHAPE['ROI_details']) != list :
                        for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                            if BoundingBoxValueFORROI is not None:
                                BBOXVALUE = list(BoundingBoxValueFORROI.values())[0]
                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)                                                                 
                                text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                padding = 5
                                text_bg_position = (
                                    text_position[0] - padding,
                                    text_position[1] - padding,
                                    text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                    text_position[1] + text_height + padding
                                )
                                draw.rectangle(text_bg_position, fill='black')
                                if str(BoundingBoxValueFORROI['roi_name']) is None and str(BoundingBoxValueFORROI['roi_name'])=='':
                                    BoundingBoxValueFORROI['roi_name']='Region of interest'
                                draw.text(text_position, str(BoundingBoxValueFORROI['roi_name']), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                    else:
                        if len(ROISHAPE['ROI_details']) !=0 :
                            for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                if BoundingBoxValueFORROI is not None:
                                    BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                    if BBOXVALUE is not None:
                                        if 'direction_line' in BoundingBoxValueFORROI.keys():
                                            # print('---------------BoundingBoxValueFORROI--------second--------',BoundingBoxValueFORROI)
                                            direction_line = BoundingBoxValueFORROI['direction_line']
                                            if direction_line is not None and direction_line!='null':
                                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                                keys_list = list(BoundingBoxValueFORROI.keys())
                                                coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]
                                                #line################################                                                        
                                                LINEBBOX = [int(coord) for coord in direction_line.split(';') if coord.strip().isdigit()]
                                                FinAlIneBBox = scale_polygon(LINEBBOX, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                # Flatten the list of coordinates
                                                GivenFlatten = [coord for point in FinAlIneBBox for coord in point]
                                                # Ensure GivenFlatten has enough coordinates to draw lines and arrows
                                                if len(GivenFlatten) >= 4:  
                                                    draw.line(GivenFlatten, fill='blue', width=5)
                                                    draw_arrow(draw, GivenFlatten, arrow_size=50, color='blue')
                                                else:
                                                    print("Error: Not enough coordinates in GivenFlatten to draw the line or arrow.")
                                            

                                                text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                                
                                                text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                                padding = 5
                                                text_bg_position = (
                                                    text_position[0] - padding,
                                                    text_position[1] - padding,
                                                    text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                                    text_position[1] + text_height + padding
                                                )
                                                draw.rectangle(text_bg_position, fill='black')
                                                keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                if keys_list is None and keys_list=='':
                                                    keys_list='Region of interest'
                                                draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                        
                for ___, thiru in enumerate(alldata['object_data']):
                    height = thiru['bbox']['H']
                    width = thiru['bbox']['W']
                    x_value = thiru['bbox']['X']
                    y_value = thiru['bbox']['Y']
                    w, h = width, height
                    shape = [(x_value, y_value), (w - 10, h - 10)]
                    text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                    text_x = x_value + 6
                    text_y = y_value +(height- y_value)
                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                    draw.rectangle(text_bg_position, fill='black')
                    if thiru['class_name']=='truck':
                        draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                        #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                        draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='car':
                        draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                        draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='motorcycle'or thiru['class_name']=='motorbike':
                        draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                        draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bus':
                        draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                        draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='bicycle':
                        draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                        draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                    elif thiru['class_name']=='person':
                        draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                        draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                imgByteArr = io.BytesIO()
                source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
                imgByteArr.seek(0)
    else:
        if len(Newalldata['object_data']) != 0:
            ROISHAPE = Newalldata['analytics_data']
            if 'ROI_details' in ROISHAPE:
                if type(ROISHAPE['ROI_details']) != list :
                    for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                        if BoundingBoxValueFORROI is not None:
                            BBOXVALUE = list(BoundingBoxValueFORROI.values())[0]
                            polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                            bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                            flattened_bbox_values = [coord for point in bbox_values for coord in point]
                            draw.polygon(flattened_bbox_values,outline=roiboxcolor, width=ROIbboxthickness)                                                                 
                            text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                            text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                            padding = 5
                            text_bg_position = (
                                text_position[0] - padding,
                                text_position[1] - padding,
                                text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                text_position[1] + text_height + padding
                            )
                            draw.rectangle(text_bg_position, fill='black')
                            if str(BoundingBoxValueFORROI['roi_name']) is None and str(BoundingBoxValueFORROI['roi_name'])=='':
                                BoundingBoxValueFORROI['roi_name']='Region of interest'
                            draw.text(text_position, str(BoundingBoxValueFORROI['roi_name']), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                else:
                    if len(ROISHAPE['ROI_details']) !=0 :
                        for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                            if BoundingBoxValueFORROI is not None:
                                BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                if BBOXVALUE is not None:
                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                    flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                    draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                    text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                        
                                    text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                    padding = 5
                                    text_bg_position = (
                                        text_position[0] - padding,
                                        text_position[1] - padding,
                                        text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                        text_position[1] + text_height + padding
                                    )                                                
                                    # Draw the background rectangle for the text
                                    draw.rectangle(text_bg_position, fill='black')
                                    keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                    if keys_list is None and keys_list=='':
                                        keys_list='Region of interest'
                                    draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                    #draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))                            
            for ___, thiru in enumerate(Newalldata['object_data']):
                height = thiru['bbox']['H']
                width = thiru['bbox']['W']
                x_value = thiru['bbox']['X']
                y_value = thiru['bbox']['Y']
                w, h = width, height
                shape = [(x_value, y_value), (w - 10, h - 10)]
                text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                text_x = x_value + 6
                text_y = y_value +(height- y_value)
                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                draw.rectangle(text_bg_position, fill='black')
                if thiru['class_name']=='truck':
                    draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                    #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                    draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                elif thiru['class_name']=='car':
                    draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                    draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                    draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                    draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                elif thiru['class_name']=='bus':
                    draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                    draw.text((text_x, text_y), str(thiru['class_name']),busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                elif thiru['class_name']=='bicycle':
                    draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                    draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                elif thiru['class_name']=='person':
                    draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                    draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
            imgByteArr = io.BytesIO()
            source_img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),format='JPEG', quality=20)
            imgByteArr.seek(0)               
        
    worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.08900000, 'y_scale': 0.080})      
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.08900000, 'y_scale': 0.080})  
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'), {'x_scale': 0.12, 'y_scale': 0.12})
        # worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),{'x_scale':x_scale, 'y_scale': y_scale})# {'x_scale': x_scale, 'y_scale': y_scale})
        #worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg'),{'x_scale':x_scale, 'y_scale': y_scale})# {'x_scale': x_scale, 'y_scale': y_scale})


def filter_object_data(data):
    keys_to_ignore = {'algorithm_details', 'bbox', 'helmet_bbox','vest_bbox','roi_details','tracking_id'}
    return {k: v for k, v in data.items() if k not in keys_to_ignore}



def process_violation_data(data):
    class_names = [entry['class_name'] for entry in data]
    roi_names = [entry['roi_name'] for entry in data]
    violation_count = sum(entry['violation'] for entry in data)
    return class_names, roi_names, violation_count


def count_and_generate_sentences(data):
    roi_violations = defaultdict(lambda: defaultdict(int))    
    for item in data:
        violation = item.get('violation')
        roi_name = item.get('roi_name')
        class_name = item.get('class_name')
        
        if violation and roi_name not in [None, 'null', 'None']:            
            roi_violations[roi_name][class_name] += 1

        roi_details = item.get('roi_details')
        if roi_details:
            for roi_detail in roi_details:
                if roi_detail.get('violation'):
                    nested_roi_name = roi_detail.get('roi_name')
                    nested_class_name = roi_detail.get('class_name', class_name)  # Use outer class_name if not provided
                    if nested_roi_name not in [None, 'null', 'None']:
                        roi_violations[nested_roi_name][nested_class_name] += 1

    # Generate sentences while filtering out invalid roi_names
    sentences = []
    for roi_name, classes in roi_violations.items():
        for class_name, count in classes.items():
            if count > 0:  # Ensure that there's at least one count
                sentence = f"A violation was detected in region '{roi_name}' involving {count} {class_name}(s)."
                sentences.append(sentence)
                    
    return sentences


def process_and_filter_object_data(data, analytics_data):
    if not isinstance(data, list):
        raise ValueError("Expected a list of dictionaries for data")

    keys_to_ignore = {'algorithm_details', 'bbox', 'helmet_bbox', 'vest_bbox', 'roi_details', 'tracking_id'}
    filtered_data = []
    roi_info = defaultdict(lambda: defaultdict(lambda: {
        "class_name": None,
        "violation_count": 0,
        "set_count": 0,
        "violation_type": None
    }))

    process_on_full_frame = analytics_data.get('process_on_full_frame', 0)

    # Filter and process data entries
    for entry in data:
        if not isinstance(entry, dict):
            raise ValueError("Each entry in data should be a dictionary")

        filtered_entry = {k: v for k, v in entry.items() if k not in keys_to_ignore}
        filtered_data.append(filtered_entry)

        if entry.get('violation'):
            roi_names = entry.get('roi_name')
            roi_names = "FullFrame" if roi_names in [None, 'null'] else re.sub(r'[\[\]]', '', roi_names)
            for roi_name in roi_names.split(','):
                class_name = entry.get('class_name')
                if class_name:
                    info = roi_info[roi_name][class_name]
                    info["class_name"] = class_name
                    info["violation_count"] += 1

    # Update set_count and violation_type from analytics_data
    for JValue in analytics_data['data']:
        roi_name = JValue['ROI']
        class_name = JValue['class_name']
        if roi_name in roi_info and class_name in roi_info[roi_name]:
            roi_info[roi_name][class_name]['set_count'] = JValue['set_count']
            roi_info[roi_name][class_name]['violation_type'] = JValue['violation_type']

    roi_summary = [
        {
            "roi_name": roi_name,
            "violationobject": class_name,
            "violationCount": details["violation_count"],
            'set_count': details["set_count"],
            'violation_type': details["violation_type"]
        }
        for roi_name, class_dict in roi_info.items()
        for class_name, details in class_dict.items()
    ]

    # sentences = [
    #     f"Maximum {details['set_count']} people can be there, but {details['violationCount']} people detected in the {roi_name} ROI."
    #     if details['violation_type'] == 'MAX' else
    #     f"Minimum {details['set_count']} people should be there, but only {details['violationCount']} people detected in the {roi_name} ROI."
    #     if details['violation_type'] == 'MIN' else
    #     print()
    #     for details in roi_summary
    # ]

    sentences = [
    f"Maximum {details['set_count']} people can be there, but {details['violationCount']} people detected in the {roi_name} ROI."
    if details['violation_type'] == 'MAX' else
    f"Minimum {details['set_count']} people should be there, but only {details['violationCount']} people detected in the {roi_name} ROI."
    for details in roi_summary if details['violation_type'] in ['MAX', 'MIN']
]
    return filtered_data, roi_summary, sentences


def PPEfilter_object_data(data):
    keys_to_ignore = {'algorithm_details', 'bbox', 'helmet_bbox', 'vest_bbox', 'roi_details', 'violation_count', 'class_name'}
    processed_data = {}
    no_helmet_count = 0
    no_vest_count = 0
    for k, v in data.items():
        if k not in keys_to_ignore:
            if k == 'Helmet' and not v:
                processed_data[k] = 'No-Helmet'
                no_helmet_count += 1
            elif k == 'Vest' and v == 'no_ppe':
                processed_data[k] = 'No-Vest'
                no_vest_count += 1
            else:
                processed_data[k] = v

    return processed_data, no_helmet_count, no_vest_count


def CrashHelmetfilter_object_data(data):
    keys_to_ignore = {'algorithm_details', 'bbox', 'helmet_bbox', 'vest_bbox', 'roi_details', 'violation_count', 'class_name'}
    processed_data = {}
    no_helmet_count = 0
    no_vest_count = 0
    for k, v in data.items():
        if k not in keys_to_ignore:
            if k == 'Bike_Helmet' and not v:
                processed_data[k] = 'NO_Bike_Helmet'
                no_helmet_count += 1
            

    return processed_data, no_helmet_count, no_vest_count




# def creation_of_excel_function(list1):
#     if 1:
#     # try:
#         ret = {'success': False, 'message': 'Something went Worng'}
#         now = datetime.now()
#         date_formats = 'dd/mm/yyyy hh:mm:ss'
#         excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
#         filename = os.path.join(os.getcwd() , 'violation_excel_sheets' ,excel_sheet_name)
#         workbook = xlsxwriter.Workbook(filename)
#         worksheet = workbook.add_worksheet('Violation Data')
#         worksheet.set_column('A:F', 31)
#         worksheet.set_row(0, 60)
#         worksheet.set_row(1, 20)
#         cell_format = workbook.add_format()
#         cell_format.set_bold()
#         cell_format.set_font_color('navy')
#         cell_format.set_font_name('Calibri')
#         cell_format.set_font_size(18)
#         cell_format.set_align('center_across')
#         worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
#         #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.png'), {'x_scale': 1.2, 'y_scale':1.1})
#         worksheet.write('B1', 'Violation Data', cell_format)
#         worksheet.merge_range('B1:D1', 'Violation Data', cell_format)
#         cell_format_1 = workbook.add_format()
#         cell_format_1.set_bold()
#         cell_format_1.set_font_color('white')
#         cell_format_1.set_font_name('Calibri')
#         cell_format_1.set_font_size(15)
#         cell_format_1.set_align('center_across')
#         cell_format_1.set_bg_color('#333300')
#         row = 1
#         col = 0
#         worksheet.write(row, col, 'Image', cell_format_1)
#         worksheet.write(row, col + 1, 'Violation Details', cell_format_1)
#         worksheet.write(row, col + 2, 'Violation Type', cell_format_1)
#         worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
#         worksheet.write(row, col + 4, 'Department Name', cell_format_1)
#         worksheet.write(row, col + 5, 'Camera Name', cell_format_1)        
#         cell_format_2 = workbook.add_format()
#         cell_format_2.set_font_name('Calibri')
#         cell_format_2.set_align('center_across')
#         rows = 2
#         cols = 0
#         cols1 = 1
#         cols2 = 2
#         cols3 = 3
#         cols4 = 4
#         cols5 = 5
#         UnidentifiedImageError_count = 0
#         FileNotFoundError_count = 0
#         for i in list1:
#             # try:
#                 if cols == 0:
#                     for zzz in i['imagename']:
#                         verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + zzz)
#                         verify_img.verify()
#                         worksheet.set_row(rows, 90)
#                         if len(i['object_data']) !=0:
#                             imagename = os.path.splitext(zzz)[0]
#                             if os.path.exists(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg')):
#                                 draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols)  
#                                 #worksheet.insert_image(rows, cols,  get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + imagename+'_1.jpg', {'x_scale': 0.12, 'y_scale': 0.12})
#                             else:
#                                 draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols)  
#                 if cols1 == 1:
#                     cell_format_2.set_text_wrap()
#                     # object_data_str = '\n'.join(i['object_data']) if len(i['object_data']) != 0 else ''
#                     # object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                    
#                     if i['analyticstype'] == 'RA':
#                         filtered_object_data = count_and_generate_sentences(i['object_data'])
#                         object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
#                         if len(i['object_data']) !=0:                            
#                             worksheet.write(rows, cols1, object_data_str, cell_format_2)
#                     elif i['analyticstype'] == 'ONB':
#                         filtered_object_data = count_and_generate_sentences(i['object_data'])#[filter_object_data(obj) for obj in i['object_data']]
#                         object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
#                         if len(i['object_data']) !=0:
#                             worksheet.write(rows, cols1, object_data_str,cell_format_2)
#                     elif i['analyticstype'] == 'PPE_TYPE1':
#                         filtered_object_data_list = []
#                         no_helmet_count = 0
#                         no_vest_count = 0
#                         for obj in i['object_data']:
#                             filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
#                             no_helmet_count += helmet_count
#                             no_vest_count += vest_count
#                             if filtered_obj:
#                                 filtered_object_data_list.append(filtered_obj)
#                         object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
#                         if len(i['object_data']) !=0:
#                             if no_helmet_count > 0 and  no_vest_count > 0:
#                                 worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
#                             elif no_helmet_count > 0 :
#                                 worksheet.write(rows, cols1, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
#                             elif no_vest_count > 0 :
#                                 worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
#                     elif i['analyticstype'] == 'PPE_TYPE2':
#                         filtered_object_data_list = []
#                         no_helmet_count = 0
#                         no_vest_count = 0
#                         for obj in i['object_data']:
#                             filtered_obj, helmet_count, vest_count = CrashHelmetfilter_object_data(obj)
#                             no_helmet_count += helmet_count
#                             no_vest_count += vest_count
#                             if filtered_obj:
#                                 filtered_object_data_list.append(filtered_obj)
#                         object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
#                         if len(i['object_data']) !=0:
#                             if no_helmet_count > 0 and  no_vest_count > 0:
#                                 worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
#                             elif no_helmet_count > 0 :
#                                 worksheet.write(rows, cols1, "No-Bike-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
#                             elif no_vest_count > 0 :
#                                 worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
#                     elif i['analyticstype'] == 'PPE':
#                         filtered_object_data_list = []
#                         no_helmet_count = 0
#                         no_vest_count = 0
#                         for obj in i['object_data']:
#                             filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
#                             no_helmet_count += helmet_count
#                             no_vest_count += vest_count
#                             if filtered_obj:
#                                 filtered_object_data_list.append(filtered_obj)

#                         object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
#                         if len(i['object_data']) !=0:
#                             if no_helmet_count > 0 and  no_vest_count > 0:
#                                 worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
#                             elif no_helmet_count > 0 :
#                                 worksheet.write(rows, cols1, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
#                             elif no_vest_count > 0 :
#                                 worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
#                     elif i['analyticstype'] == 'CRDCNT':                        
#                         filtered_object_data,roi_info ,sentecnes=process_and_filter_object_data(i['object_data'],i['analytics_data'])
#                         object_data_str = '\n'.join([json.dumps(obj) for obj in sentecnes]) if len(sentecnes) != 0 else ''
#                         if len(i['object_data']) !=0:
#                             worksheet.write(rows, cols1, object_data_str, cell_format_2)
                
#                 if cols2 == 2:
#                     if i['analyticstype'] == 'RA':
#                         worksheet.write(rows, cols2, 'Restricted Area', cell_format_2)
#                     elif i['analyticstype'] == 'ONB':
#                         worksheet.write(rows, cols2, 'Object Near By Truck',cell_format_2)
#                     elif i['analyticstype'] == 'PPE_TYPE1':
                        
#                         worksheet.write(rows, cols2, 'Personal-Protective-Equipment', cell_format_2)
#                     elif i['analyticstype'] == 'PPE':
#                         worksheet.write(rows, cols2, 'Personal-Protective-Equipment', cell_format_2)
#                     elif i['analyticstype'] == 'PPE_TYPE2':
#                         worksheet.write(rows, cols2, 'Crash-Helmet', cell_format_2)
#                     elif i['analyticstype'] == 'CRDCNT':
#                         worksheet.write(rows, cols2, 'Crowd Count Violation', cell_format_2)
#                 if cols3 == 3:
#                     date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
#                     date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
#                     worksheet.write_datetime(rows, cols3, date_time,  date_format)
                
#                 if cols4 == 4:

#                     try:
#                         if 'department' in i:
#                             worksheet.write(rows, cols4, i['department'], cell_format_2)
#                         elif 'camera_info' in i:
#                             worksheet.write(rows, cols4, i['camera_info']['department'], cell_format_2)
#                         else:
#                             worksheet.write(rows, cols4, i['camera_name'], cell_format_2)
#                     except Exception as error :
#                         worksheet.write(rows, cols4, i['camera_name'], cell_format_2)
#                 if cols5 == 5:
#                     worksheet.write(rows, cols5, i['camera_name'], cell_format_2)
#                 rows += 1
#             # except UnidentifiedImageError as error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 1", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#             #     UnidentifiedImageError_count += 1
#             # except FileNotFoundError as error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_o444f_excel_function 2", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#             #     FileNotFoundError_count += 1
#             # except UserWarning as error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 3", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#             # except ImportError as error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ex444cel_function 4", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#             # except xlsxwriter.exceptions.FileCreateError as error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_e444xcel_function 5", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#             # except PermissionError as error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc444el_function 6", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#             # except xlsxwriter.exceptions.XlsxWriterException as  error:
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- 444 7", str(error), " ----time ---- ", now_time_with_time()]))
#             #     ret = {'success': False, 'message': str(error)}
#         try:
#             workbook.close()
#             print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
#             print('FileNotFoundError_count == ', FileNotFoundError_count)
#             ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
#         except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
#             DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
#             xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
#             xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc454454el_function 8", str(error), " ----time ---- ", now_time_with_time()]))
#             ret = {'success': False, 'message': str(error)}
#         except PermissionError as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel45455_function 9", str(error), " ----time ---- ", now_time_with_time()]))
#             ret = {'success': False, 'message': str(error)}
#         except AttributeError as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exce44555l_function 10", str(error), " ----time ---- ", now_time_with_time()]))
#             ret = {'success': False, 'message': str(error)}
#     # except Exception as  error:
#     #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel_45454function 11", str(error), " ----time ---- ", now_time_with_time()]))
#     #     ret = {'success': False, 'message': str(error)}
#     return ret



def create_chart(workbook, from_date, to_date, violation_types, list1, title=None):
    #print("list1--------------------------------",list1)
    try:
        start_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date format! Please enter the date in 'YYYY-MM-DD HH:MM:SS' format.")
        return

    header_font = workbook.add_format({'bold': True, 'color': 'FFFFFF', 'bg_color': '4F81BD', 'size': '12'})
    border_style = workbook.add_format({'border': 1})

    date_range_exceeds_three_days = (end_date - start_date).days > 3
    print("date_range_exceeds_three_days------------------",date_range_exceeds_three_days)

   
    violations_by_date = defaultdict(lambda: defaultdict(int))  # For date-wise counting
    violations_by_date_hour = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # For timestamp-wise counting

    for v_type in violation_types:
        data = [record for record in list1 if record.get("analyticstype") == v_type]
        sheet_name = title or f"{v_type} Violation Chart"
        
        existing_sheets = [sheet.get_name() for sheet in workbook.worksheets_objs]
        if sheet_name not in existing_sheets:
            sheet = workbook.add_worksheet(sheet_name)
        else:
            return

      
        headers = ['Date' if date_range_exceeds_three_days else 'Timestamp'] + list(violation_types)
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, header_font)

       
        for record in data:
            timestamp = record.get("timestamp")
            violationType = record.get("analyticstype")
            if timestamp and violationType:
                timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if date_range_exceeds_three_days:
                 
                    violation_date = timestamp_obj.date()
                    violations_by_date[violation_date][violationType] += 1
                else:
                   
                    violation_date = timestamp_obj.date()
                    violation_hour = timestamp_obj.hour
                    violations_by_date_hour[violation_date][violation_hour][violationType] += 1

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

        if date_range_exceeds_three_days:
          
            total_violations = sum(
                sum(date_data.values()) for date_data in list(violations_by_date.values())
            )
        else:
           
            total_violations = sum(
                sum(hour.get(v_type, 0) for hour in date_data.values())
                for date_data in list(violations_by_date_hour.values())
            )

      
        chart = workbook.add_chart({'type': 'column'})
        chart.set_title({'name': f"{sheet_name} Total Counts: {total_violations}"})
        chart.set_x_axis({'name': 'Date' if date_range_exceeds_three_days else 'Violation Time'})
        chart.set_y_axis({'name': 'Detected Count'})
        chart.set_size({'width': 1100, 'height': 700})

        
        data_range = f"'{sheet_name}'!B2:B{row_index}"
        categories_range = f"'{sheet_name}'!A2:A{row_index}"

        
        chart.add_series({
            'name': f"{v_type} Violations",
            'categories': categories_range,
            'values': data_range,
            'data_labels': {'value': True}
        })

        
        sheet.insert_chart(f"C2", chart)
        sheet.set_column(0, 0, 20)


def create_camera_wise_chart(workbook, list1, from_date, to_date, title="Camera-wise Violation Chart"):
    violations_by_camera = defaultdict(int)

    
    for record in list1:
        camera_name = record.get("camera_name", "Unknown Camera")
        violations_by_camera[camera_name] += 1

   
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        
        sheet.write(0, 0, "Camera", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        
        row_index = 1
        for camera, count in violations_by_camera.items():
            sheet.write(row_index, 0, camera)
            sheet.write(row_index, 1, count)
            row_index += 1

       
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
##add
def create_department_wise_chart(workbook, list1, from_date, to_date, title="Department-wise Violation Chart"):
    violations_by_department = defaultdict(int)

    for record in list1:
        department = (
            record.get("department") or
            (record.get("camera_info", {}).get("department")) or
            "Unknown Department"
        )
        violations_by_department[department] += 1

   
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        
        sheet.write(0, 0, "Department", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        row_index = 1
        for department, count in violations_by_department.items():
            sheet.write(row_index, 0, department)
            sheet.write(row_index, 1, count)
            row_index += 1

       
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

       
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)

######################################################################################################


def creation_of_excel_function(list1,from_date, to_date):
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:F', 31)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(18)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.png'), {'x_scale': 1.2, 'y_scale':1.1})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:D1', 'Violation Data', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'Image', cell_format_1)
        worksheet.write(row, col + 1, 'Violation Details', cell_format_1)
        worksheet.write(row, col + 2, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 4, 'Department Name', cell_format_1)
        worksheet.write(row, col + 5, 'Camera Name', cell_format_1)        
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
        for i in list1:
            # try:
                if cols == 0:
                    for zzz in i['imagename']:
                        verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + zzz)
                        verify_img.verify()
                        worksheet.set_row(rows, 90)
                        if len(i['object_data']) !=0:
                            imagename = os.path.splitext(zzz)[0]
                            if os.path.exists(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg')):
                                draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols)  
                                #worksheet.insert_image(rows, cols,  get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + imagename+'_1.jpg', {'x_scale': 0.12, 'y_scale': 0.12})
                            else:
                                draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols)  
                if cols1 == 1:
                    cell_format_2.set_text_wrap()
                    # object_data_str = '\n'.join(i['object_data']) if len(i['object_data']) != 0 else ''
                    # object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                    
                    if i['analyticstype'] == 'RA':
                        filtered_object_data = count_and_generate_sentences(i['object_data'])
                        object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                        if len(i['object_data']) !=0:                            
                            worksheet.write(rows, cols1, object_data_str, cell_format_2)
                    elif i['analyticstype'] == 'ONB':
                        filtered_object_data = count_and_generate_sentences(i['object_data'])#[filter_object_data(obj) for obj in i['object_data']]
                        object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                        if len(i['object_data']) !=0:
                            worksheet.write(rows, cols1, object_data_str,cell_format_2)
                    elif i['analyticstype'] == 'PPE_TYPE1':
                        filtered_object_data_list = []
                        no_helmet_count = 0
                        no_vest_count = 0
                        for obj in i['object_data']:
                            filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
                            no_helmet_count += helmet_count
                            no_vest_count += vest_count
                            if filtered_obj:
                                filtered_object_data_list.append(filtered_obj)
                        object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                        if len(i['object_data']) !=0:
                            if no_helmet_count > 0 and  no_vest_count > 0:
                                worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                            elif no_helmet_count > 0 :
                                worksheet.write(rows, cols1, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                            elif no_vest_count > 0 :
                                worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
                    elif i['analyticstype'] == 'PPE_TYPE2':
                        filtered_object_data_list = []
                        no_helmet_count = 0
                        no_vest_count = 0
                        for obj in i['object_data']:
                            filtered_obj, helmet_count, vest_count = CrashHelmetfilter_object_data(obj)
                            no_helmet_count += helmet_count
                            no_vest_count += vest_count
                            if filtered_obj:
                                filtered_object_data_list.append(filtered_obj)
                        object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                        if len(i['object_data']) !=0:
                            if no_helmet_count > 0 and  no_vest_count > 0:
                                worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                            elif no_helmet_count > 0 :
                                worksheet.write(rows, cols1, "No-Bike-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                            elif no_vest_count > 0 :
                                worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
                    elif i['analyticstype'] == 'PPE':
                        filtered_object_data_list = []
                        no_helmet_count = 0
                        no_vest_count = 0
                        for obj in i['object_data']:
                            filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
                            no_helmet_count += helmet_count
                            no_vest_count += vest_count
                            if filtered_obj:
                                filtered_object_data_list.append(filtered_obj)

                        object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                        if len(i['object_data']) !=0:
                            if no_helmet_count > 0 and  no_vest_count > 0:
                                worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                            elif no_helmet_count > 0 :
                                worksheet.write(rows, cols1, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                            elif no_vest_count > 0 :
                                worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
                    elif i['analyticstype'] == 'CRDCNT':                        
                        filtered_object_data,roi_info ,sentecnes=process_and_filter_object_data(i['object_data'],i['analytics_data'])
                        object_data_str = '\n'.join([json.dumps(obj) for obj in sentecnes]) if len(sentecnes) != 0 else ''
                        if len(i['object_data']) !=0:
                            worksheet.write(rows, cols1, object_data_str, cell_format_2)
                
                if cols2 == 2:
                    if i['analyticstype'] == 'RA':
                        worksheet.write(rows, cols2, 'Restricted Area', cell_format_2)
                    elif i['analyticstype'] == 'ONB':
                        worksheet.write(rows, cols2, 'Object Near By Truck',cell_format_2)
                    elif i['analyticstype'] == 'PPE_TYPE1':
                        
                        worksheet.write(rows, cols2, 'Personal-Protective-Equipment', cell_format_2)
                    elif i['analyticstype'] == 'PPE':
                        worksheet.write(rows, cols2, 'Personal-Protective-Equipment', cell_format_2)
                    elif i['analyticstype'] == 'PPE_TYPE2':
                        worksheet.write(rows, cols2, 'Crash-Helmet', cell_format_2)
                    elif i['analyticstype'] == 'CRDCNT':
                        worksheet.write(rows, cols2, 'Crowd Count Violation', cell_format_2)
                if cols3 == 3:
                    date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols3, date_time,  date_format)
                
                if cols4 == 4:

                    try:
                        if 'department' in i:
                            worksheet.write(rows, cols4, i['department'], cell_format_2)
                        elif 'camera_info' in i:
                            worksheet.write(rows, cols4, i['camera_info']['department'], cell_format_2)
                        else:
                            worksheet.write(rows, cols4, i['camera_name'], cell_format_2)

                    except Exception as error :
                        worksheet.write(rows, cols4, i['camera_name'], cell_format_2)
                if cols5 == 5:
                    worksheet.write(rows, cols5, i['camera_name'], cell_format_2)
                    # print(" i['camera_name']=====================", i['camera_name'])
                    # print("cols5----------------",cols5)
                rows += 1
        violation_types = set(item['analyticstype'] for item in list1)
        if "RA" in violation_types:
            create_chart(workbook, from_date, to_date, violation_types, list1, title="Danger Zone Violation")
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
        else:
            create_chart(workbook, from_date, to_date, violation_types, list1)
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
            
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc454454el_function 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel45455_function 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exce44555l_function 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel_45454function 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret


def creation_DOLVI_excel_function(list1,from_date,to_date):
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:F', 31)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(18)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.png'), {'x_scale': 1.2, 'y_scale':1.1})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:D1', 'Violation Data', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'Image', cell_format_1)
        worksheet.write(row, col + 1, 'Violation Details', cell_format_1)
        worksheet.write(row, col + 2, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 4, 'Department Name', cell_format_1)
        worksheet.write(row, col + 5, 'Camera Name', cell_format_1)        
        worksheet.write(row, col + 6, 'Area', cell_format_1)        
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
        cols6 = 6
        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0
        for i in list1:
            # try:
            if cols == 0:
                for zzz in i['imagename']:
                    verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + zzz)
                    verify_img.verify()
                    worksheet.set_row(rows, 90)
                    if len(i['object_data']) !=0:
                        imagename = os.path.splitext(zzz)[0]
                        if os.path.exists(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg')):
                            draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols)  
                            #worksheet.insert_image(rows, cols,  get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + imagename+'_1.jpg', {'x_scale': 0.12, 'y_scale': 0.12})
                        else:
                            draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols)  
            if cols1 == 1:
                cell_format_2.set_text_wrap()
                # object_data_str = '\n'.join(i['object_data']) if len(i['object_data']) != 0 else ''
                # object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                
                if i['analyticstype'] == 'RA':
                    filtered_object_data = count_and_generate_sentences(i['object_data'])
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                    if len(i['object_data']) !=0:                            
                        worksheet.write(rows, cols1, object_data_str, cell_format_2)
                elif i['analyticstype'] == 'ONB':
                    filtered_object_data = count_and_generate_sentences(i['object_data'])#[filter_object_data(obj) for obj in i['object_data']]
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                    if len(i['object_data']) !=0:
                        worksheet.write(rows, cols1, object_data_str,cell_format_2)
                elif i['analyticstype'] == 'PPE_TYPE1':
                    filtered_object_data_list = []
                    no_helmet_count = 0
                    no_vest_count = 0
                    for obj in i['object_data']:
                        filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
                        no_helmet_count += helmet_count
                        no_vest_count += vest_count
                        if filtered_obj:
                            filtered_object_data_list.append(filtered_obj)
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                    if len(i['object_data']) !=0:
                        if no_helmet_count > 0 and  no_vest_count > 0:
                            worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                        elif no_helmet_count > 0 :
                            worksheet.write(rows, cols1, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                        elif no_vest_count > 0 :
                            worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
                            
                elif i['analyticstype'] == 'PPE_TYPE2':
                    filtered_object_data_list = []
                    no_helmet_count = 0
                    no_vest_count = 0
                    for obj in i['object_data']:
                        filtered_obj, helmet_count, vest_count = CrashHelmetfilter_object_data(obj)
                        no_helmet_count += helmet_count
                        no_vest_count += vest_count
                        if filtered_obj:
                            filtered_object_data_list.append(filtered_obj)
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                    if len(i['object_data']) !=0:
                        if no_helmet_count > 0 and  no_vest_count > 0:
                            worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                        elif no_helmet_count > 0 :
                            worksheet.write(rows, cols1, "No-Bike-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                        elif no_vest_count > 0 :
                            worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
                elif i['analyticstype'] == 'PPE':
                    filtered_object_data_list = []
                    no_helmet_count = 0
                    no_vest_count = 0
                    for obj in i['object_data']:
                        filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
                        no_helmet_count += helmet_count
                        no_vest_count += vest_count
                        if filtered_obj:
                            filtered_object_data_list.append(filtered_obj)

                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                    if len(i['object_data']) !=0:
                        if no_helmet_count > 0 and  no_vest_count > 0:
                            worksheet.write(rows, cols1, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                        elif no_helmet_count > 0 :
                            worksheet.write(rows, cols1, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                        elif no_vest_count > 0 :
                            worksheet.write(rows, cols1, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)
                elif i['analyticstype'] == 'CRDCNT':                 
                    filtered_object_data,roi_info ,sentecnes=process_and_filter_object_data(i['object_data'],i['analytics_data'])
                    object_data_str = '\n'.join([json.dumps(obj) for obj in sentecnes]) if len(sentecnes) != 0 else ''
                    if len(i['object_data']) !=0:
                        worksheet.write(rows, cols1, object_data_str, cell_format_2)
            
            if cols2 == 2:
                if i['analyticstype'] == 'RA':
                    worksheet.write(rows, cols2, 'Restricted Area', cell_format_2)
                elif i['analyticstype'] == 'ONB':
                    worksheet.write(rows, cols2, 'Object Near By Truck',cell_format_2)
                elif i['analyticstype'] == 'PPE_TYPE1':
                    
                    worksheet.write(rows, cols2, 'Personal-Protective-Equipment', cell_format_2)
                elif i['analyticstype'] == 'PPE':
                    worksheet.write(rows, cols2, 'Personal-Protective-Equipment', cell_format_2)
                elif i['analyticstype'] == 'PPE_TYPE2':
                    worksheet.write(rows, cols2, 'Crash-Helmet', cell_format_2)
                elif i['analyticstype'] == 'CRDCNT':
                    worksheet.write(rows, cols2, 'Crowd Count Violation', cell_format_2)
            if cols3 == 3:
                date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                worksheet.write_datetime(rows, cols3, date_time,  date_format)
            
            if cols4 == 4:
                try:
                    if 'department' in i:
                        worksheet.write(rows, cols4, i['department'], cell_format_2)
                    elif 'camera_info' in i:
                        worksheet.write(rows, cols4, i['camera_info']['department'], cell_format_2)
                    else:
                        worksheet.write(rows, cols4, i['camera_name'], cell_format_2)
                except Exception as error :
                    worksheet.write(rows, cols4, i['camera_name'], cell_format_2)

            if cols5 == 5:
                worksheet.write(rows, cols5, i['camera_name'], cell_format_2)

            if cols6 == 6:
                #print("TEST-----5555555555555:", serail_number+1)
                try:
                    worksheet.write(rows, cols6, i['area'],  cell_format_2) 
                    # worksheet.write(rows, cols4, i['camera_name'],  cell_format_2) 

                except Exception as error :
                    # worksheet.write(rows, cols4, i['area'], cell_format_2)
                    worksheet.write(rows, cols6, i['camera_name'], cell_format_2)
                
            rows += 1
        violation_types = set(item['analyticstype'] for item in list1)
        if "RA" in violation_types:
            create_chart(workbook, from_date, to_date, violation_types, list1, title="Danger Zone Violation")
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
        else:
            create_chart(workbook, from_date, to_date, violation_types, list1)
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
            # except UnidentifiedImageError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 1", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            #     UnidentifiedImageError_count += 1
            # except FileNotFoundError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_o444f_excel_function 2", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            #     FileNotFoundError_count += 1
            # except UserWarning as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 3", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except ImportError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ex444cel_function 4", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except xlsxwriter.exceptions.FileCreateError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_e444xcel_function 5", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except PermissionError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc444el_function 6", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except xlsxwriter.exceptions.XlsxWriterException as  error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- 444 7", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            print('Violation_report_10-08-2024-20-42-00.xlsx', excel_sheet_name)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc454454el_function 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel45455_function 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exce44555l_function 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel_45454function 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret


def creation_CRM2_excel_function(list1, area_incharger,from_date,to_date):
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'violation_excel_sheets', excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:K', 31)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(18)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.png'), {'x_scale': 1.2, 'y_scale':1.1})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:K1', 'Violation Data', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'Sr.No', cell_format_1)
        worksheet.write(row, col + 1, 'Department', cell_format_1)
        worksheet.write(row, col + 2, 'Section/Line', cell_format_1)
        worksheet.write(row, col + 3, 'Image', cell_format_1)
        worksheet.write(row, col + 4, 'Area Identification', cell_format_1)
        worksheet.write(row, col + 5, 'Date', cell_format_1)
        worksheet.write(row, col + 6, 'Time', cell_format_1)
        worksheet.write(row, col + 7, 'Name of Area In-Charge', cell_format_1)
        worksheet.write(row, col + 8, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 9, 'Violation Details', cell_format_1)
        worksheet.write(row, col + 10, 'Camera Name', cell_format_1) 
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
        cols6 = 6
        cols7 = 7
        cols8 = 8
        cols9 = 9
        cols10 = 10
        UnidentifiedImageError_count = 0
        FileNotFoundError_count = 0
        serail_number = 0
        #print(":LIST1 VALUE:-------------------", len(list1))
        for i in list1:
            print("SERIAL NUMBER:", serail_number+1)
            serail_number+=1
            # try:
            if cols == 0:
                #print("TEST111111111111111111111:", serail_number+1)
                worksheet.write(rows, cols, serail_number, cell_format_2)

            if cols1 == 1:
                #print("TEST-----2222222222222222:", serail_number+1)
                try:
                    if 'department' in i:
                        worksheet.write(rows, cols1, i['department'], cell_format_2)
                        
                    elif 'camera_info' in i:
                        worksheet.write(rows, cols1, i['camera_info']['department'], cell_format_2)

                    else:
                        worksheet.write(rows, cols1, i['camera_name'], cell_format_2)
                        
                except Exception as error :
                    worksheet.write(rows, cols1, i['camera_name'], cell_format_2)

            if cols2 == 2:
                #print("TEST-----33333333333333333:", serail_number+1)
                worksheet.write(rows, cols2, "CAL_1", cell_format_2)

            if cols3 == 3:
                #print("TEST-----44444444444444444:", serail_number+1)
                for zzz in i['imagename']:
                    verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + zzz)
                    verify_img.verify()
                    worksheet.set_row(rows, 90)
                    if len(i['object_data']) !=0:
                        imagename = os.path.splitext(zzz)[0]
                        if os.path.exists(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg')):
                            draw_bbox_and_insert_image(worksheet, zzz, i, i['object_data'], rows, cols3)  
                            #worksheet.insert_image(rows, cols,  get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + imagename+'_1.jpg', {'x_scale': 0.12, 'y_scale': 0.12})
                        else:
                            draw_bbox_and_insert_image(worksheet, zzz,i,i['object_data'],rows,cols3)

            if cols4 == 4:
                #print("TEST-----5555555555555:", serail_number+1)
                try:
                    worksheet.write(rows, cols4, i['area'],  cell_format_2) 
                    # worksheet.write(rows, cols4, i['camera_name'],  cell_format_2) 

                except Exception as error :
                    # worksheet.write(rows, cols4, i['area'], cell_format_2)
                    worksheet.write(rows, cols4, i['camera_name'], cell_format_2)
                    
                

            if cols5 == 5:
               # print("TEST-----66666666666666666666:", serail_number+1)
                date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                # print("DATETIME:--", i['timestamp'].split( ))
                datetime_seperate_val = i['timestamp'].split( )
                print("DATETIME:-SEPERAted -", datetime_seperate_val[0])
                date_obj = datetime_seperate_val[0] #date_time.date()
                # time_obj = date_time.time()

                # date_str = date_obj.strftime('%Y-%m-%d')
                # print("DATE TIME:----------date_str", date_str)
                # date_format = workbook.add_format({'num_format': date_obj, 'align': 'center'})
                worksheet.write(rows, cols5, date_obj,  cell_format_2)

            if cols6 == 6:
                #print("TEST-----7777777777777777777:", serail_number+1)
                date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                # time_str = time_obj.strftime('%H:%M:%S')
                datetime_seperate_val = i['timestamp'].split( )
                time_obj = datetime_seperate_val[1]#date_time.time()
                # date_format = workbook.add_format({'num_format': time_str, 'align': 'center'})
                worksheet.write(rows, cols6, time_obj,  cell_format_2)

                
            if cols7 == 7:
               # print("TEST-----8888888888888888:", serail_number+1)
                worksheet.write(rows, cols7, area_incharger, cell_format_2)

            
            if cols8 == 8:
                #print("TEST-----999999999999999999999:", serail_number+1)
                if i['analyticstype'] == 'RA':
                    worksheet.write(rows, cols8, 'Restricted Area', cell_format_2)
                elif i['analyticstype'] == 'ONB':
                    worksheet.write(rows, cols8, 'Object Near By Truck',cell_format_2)
                elif i['analyticstype'] == 'PPE_TYPE1':
                    
                    worksheet.write(rows, cols8, 'Personal-Protective-Equipment', cell_format_2)
                elif i['analyticstype'] == 'PPE':
                    worksheet.write(rows, cols8, 'Personal-Protective-Equipment', cell_format_2)
                elif i['analyticstype'] == 'PPE_TYPE2':
                    worksheet.write(rows, cols8, 'Crash-Helmet', cell_format_2)
                elif i['analyticstype'] == 'CRDCNT':
                    worksheet.write(rows, cols8, 'Crowd Count Violation', cell_format_2)
                
            if cols9 == 9:
                #print("TEST-----101010101010:", serail_number+1)
                cell_format_2.set_text_wrap()
                # object_data_str = '\n'.join(i['object_data']) if len(i['object_data']) != 0 else ''
                # object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                if i['analyticstype'] == 'RA':
                    filtered_object_data = count_and_generate_sentences(i['object_data'])
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                    if len(i['object_data']) !=0:                            
                        worksheet.write(rows, cols9, object_data_str, cell_format_2)
                elif i['analyticstype'] == 'ONB':
                    filtered_object_data = count_and_generate_sentences(i['object_data'])#[filter_object_data(obj) for obj in i['object_data']]
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data]) if len(filtered_object_data) != 0 else ''
                    if len(i['object_data']) !=0:
                        worksheet.write(rows, cols9, object_data_str,cell_format_2)
                elif i['analyticstype'] == 'PPE_TYPE1':
                    filtered_object_data_list = []
                    no_helmet_count = 0
                    no_vest_count = 0
                    for obj in i['object_data']:
                        filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
                        no_helmet_count += helmet_count
                        no_vest_count += vest_count
                        if filtered_obj:
                            filtered_object_data_list.append(filtered_obj)
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                    if len(i['object_data']) !=0:
                        if no_helmet_count > 0 and  no_vest_count > 0:
                            worksheet.write(rows, cols9, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                        elif no_helmet_count > 0 :
                            worksheet.write(rows, cols9, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                        elif no_vest_count > 0 :
                            worksheet.write(rows, cols9, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)

                elif i['analyticstype'] == 'PPE_TYPE2':
                    filtered_object_data_list = []
                    no_helmet_count = 0
                    no_vest_count = 0
                    for obj in i['object_data']:
                        filtered_obj, helmet_count, vest_count = CrashHelmetfilter_object_data(obj)
                        no_helmet_count += helmet_count
                        no_vest_count += vest_count
                        if filtered_obj:
                            filtered_object_data_list.append(filtered_obj)
                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                    if len(i['object_data']) !=0:
                        if no_helmet_count > 0 and  no_vest_count > 0:
                            worksheet.write(rows, cols9, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                        elif no_helmet_count > 0 :
                            worksheet.write(rows, cols9, "No-Bike-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                        elif no_vest_count > 0 :
                            worksheet.write(rows, cols9, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)

                elif i['analyticstype'] == 'PPE':
                    filtered_object_data_list = []
                    no_helmet_count = 0
                    no_vest_count = 0
                    for obj in i['object_data']:
                        filtered_obj, helmet_count, vest_count = PPEfilter_object_data(obj)
                        no_helmet_count += helmet_count
                        no_vest_count += vest_count
                        if filtered_obj:
                            filtered_object_data_list.append(filtered_obj)

                    object_data_str = '\n'.join([json.dumps(obj) for obj in filtered_object_data_list]) if filtered_object_data_list else ''
                    if len(i['object_data']) !=0:
                        if no_helmet_count > 0 and  no_vest_count > 0:
                            worksheet.write(rows, cols9, "No-Helmet-Count={0}\nNo-Vest-Count={1}".format(no_helmet_count,no_vest_count), cell_format_2)
                        elif no_helmet_count > 0 :
                            worksheet.write(rows, cols9, "No-Helmet-Count={0}\n".format(no_helmet_count), cell_format_2)
                        elif no_vest_count > 0 :
                            worksheet.write(rows, cols9, "No-Vest-Count={0}\n".format(no_vest_count), cell_format_2)

                elif i['analyticstype'] == 'CRDCNT':                        
                    filtered_object_data,roi_info ,sentecnes=process_and_filter_object_data(i['object_data'],i['analytics_data'])
                    object_data_str = '\n'.join([json.dumps(obj) for obj in sentecnes]) if len(sentecnes) != 0 else ''
                    if len(i['object_data']) !=0:
                        worksheet.write(rows, cols9, object_data_str, cell_format_2)

            if cols10 == 10:
                #print("TEST-----111101010111111111111111:", serail_number+1)
                worksheet.write(rows, cols10, i['camera_name'], cell_format_2)

            rows += 1
        violation_types = set(item['analyticstype'] for item in list1)
        if "RA" in violation_types:
            create_chart(workbook, from_date, to_date, violation_types, list1, title="Danger Zone Violation")
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
        else:
            create_chart(workbook, from_date, to_date, violation_types, list1)
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
            # except UnidentifiedImageError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 1", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            #     UnidentifiedImageError_count += 1
            # except FileNotFoundError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_o444f_excel_function 2", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            #     FileNotFoundError_count += 1
            # except UserWarning as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 3", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except ImportError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ex444cel_function 4", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except xlsxwriter.exceptions.FileCreateError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_e444xcel_function 5", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except PermissionError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc444el_function 6", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except xlsxwriter.exceptions.XlsxWriterException as  error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- 444 7", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc454454el_function 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel45455_function 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exce44555l_function 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel_45454function 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret


def TRAExcelCreation(list1, from_date, to_date):
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Violation Data')
        worksheet.set_column('A:F', 31)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(18)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.png'), {'x_scale': 1.2, 'y_scale':1.1})
        worksheet.write('B1', 'Violation Data', cell_format)
        worksheet.merge_range('B1:D1', 'Violation Data', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'Image', cell_format_1)
        worksheet.write(row, col + 1, 'Violation Type', cell_format_1)
        worksheet.write(row, col + 2, 'Detected Time', cell_format_1)
        worksheet.write(row, col + 3, 'Department Name', cell_format_1)
        worksheet.write(row, col + 4, 'Camera Name', cell_format_1)
        
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
        for i in list1:
            # print("iiiii===",i)
            if 1:
            # try:
                if cols == 0:
                    for zzz in i['imagename']:
                        verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + zzz)
                        verify_img.verify()
                        worksheet.set_row(rows, 90)
                        if len(i['object_data']) !=0:
                            imagename = os.path.splitext(zzz)[0]
                            if os.path.exists(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'frame', imagename+'_1.jpg')):
                                OnlyForTRA(worksheet, zzz,i,i['object_data'],rows,cols)  
                                #worksheet.insert_image(rows, cols,  get_current_dir_and_goto_parent_dir() +  '/images/frame' + '/' + imagename+'_1.jpg', {'x_scale': 0.12, 'y_scale': 0.12})
                            else:
                                OnlyForTRA(worksheet, zzz,i,i['object_data'],rows,cols)  
                if cols1 == 1:
                    if i['analyticstype'] == 'RA':
                        worksheet.write(rows, cols1, 'Protection-Zone', cell_format_2)
                    elif i['analyticstype'] == 'ONB':
                        worksheet.write(rows, cols1, 'Object Near By Truck',cell_format_2)
                    elif i['analyticstype'] == 'PPE_TYPE1':
                        worksheet.write(rows, cols1, 'Personal-Protective-Equipment', cell_format_2)
                    elif i['analyticstype'] == 'PPE':
                        worksheet.write(rows, cols1, 'Personal-Protective-Equipment', cell_format_2)
                    elif i['analyticstype'] == 'CRDCNT':
                        worksheet.write(rows, cols1, 'Crowd Count Violation', cell_format_2)
                if cols2 == 2:
                    date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols2, date_time,  date_format)
                
                if cols3 == 3:

                    try:
                        if 'department' in i:
                            worksheet.write(rows, cols3, i['department'], cell_format_2)
                        elif 'camera_info' in i:
                            worksheet.write(rows, cols3, i['camera_info']['department'], cell_format_2)
                        else:
                            worksheet.write(rows, cols3, i['camera_name'], cell_format_2)
                    except Exception as error :
                        worksheet.write(rows, cols3, i['camera_name'], cell_format_2)
                if cols4 == 4:
                    worksheet.write(rows, cols4, i['camera_name'], cell_format_2)
                rows += 1
        violation_types = set(item['analyticstype'] for item in list1)

        if "RA" in violation_types:
            create_chart(workbook, from_date, to_date, violation_types, list1, title="Protection Zone Violation")
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)
        else:
            create_chart(workbook, from_date, to_date, violation_types, list1) 
            create_camera_wise_chart(workbook, list1,from_date,to_date)
            create_department_wise_chart(workbook, list1,from_date,to_date)   
            # except UnidentifiedImageError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 1", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            #     UnidentifiedImageError_count += 1
            # except FileNotFoundError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_o444f_excel_function 2", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            #     FileNotFoundError_count += 1
            # except UserWarning as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_444excel_function 3", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except ImportError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_ex444cel_function 4", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except xlsxwriter.exceptions.FileCreateError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_e444xcel_function 5", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except PermissionError as error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc444el_function 6", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
            # except xlsxwriter.exceptions.XlsxWriterException as  error:
            #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- 444 7", str(error), " ----time ---- ", now_time_with_time()]))
            #     ret = {'success': False, 'message': str(error)}
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc454454el_function 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel45455_function 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exce44555l_function 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel_45454function 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret

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
        # print('res ===', res)
        # print('\n\n')
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
        elif CamCount == int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status




#UPDATED NORMAL RA DATA
def VIolationcountforRA(live_data):
    ret = False
    if live_data is not None:
        if 1:
        # try:
            if len(live_data['data']) !=0:
                # if len(live_data['data']) ==1:
                #     if live_data['data'][0]['analyticstype'] == 'RA':
                #         department_name = None                       
                #         object_data = live_data['data'][0]['object_data']              
                #         if len(object_data) != 0:
                #             if 1:
                #             # try:
                #                 # final_object_RA_data = []
                #                 # final_object_SRA_data = []
                #                 final_object_data = []
                #                 # final_object_TRA_data = []
                #                 if len(object_data) == 1:
                #                     if object_data[0]['violation'] == True:
                #                         # print("VIOLATION object_data:------------------", len(object_datsa[0]["roi_details"]))
                #                         if object_data[0]['class_name'] == 'person':
                #                             del object_data[0]['bbox']
                #                             del object_data[0]['tracking_id']
                #                             object_data[0]['violation_count'] = 'person ' + str(1)
                                            
                #                             # for inx in object_data[0]["roi_details"]:
                #                             # print("object_data[0][roi_details])______________________________", object_data[0]["roi_details"])
                #                             if "roi_details" in object_data[0].keys():
                #                                 testtttttttttt = []
                #                                 for index, inx in enumerate(object_data[0]["roi_details"]):
                #                                     if inx["analytics_type"] == "0" and inx["violation"] == True:
                #                                         testtttttttttt.append(object_data[0]["roi_details"][index])
                #                                 object_data[0]["roi_details"] = testtttttttttt

                #                             # else:
                #                             #     # final_object_data.append(jjj)
                #                             #     final_object_data.append(object_data[0])

                #                             final_object_data.append(object_data[0]) # object_data[0])
                                    
                #                 elif len(object_data) > 1:
                #                     # print("object_data:---------------ELSE ANALYTICS---", object_data[0]["roi_details"][0]["analytics_type"])
                #                     for ___, jjj in enumerate(object_data):
                #                         if jjj['violation'] == True:
                #                             if jjj['class_name'] == 'person':
                #                                 del jjj['bbox']
                #                                 del jjj['tracking_id']
                #                                 jjj['violation_count'] = 'person ' + str(int(___) + int(1))

                #                                 if "roi_details" in jjj.keys():
                #                                     testttt4 = []
                #                                     for index, inx in enumerate(jjj["roi_details"]):
                #                                         if inx["analytics_type"] == "0" and inx["violation"] == True:
                #                                             # jjj["roi_details"] = jjj["roi_details"][index] #inx[index]
                #                                             testttt4.append(jjj["roi_details"][index])

                #                                     jjj["roi_details"] = testttt4

                #                                 final_object_data.append(jjj) #inx[index]) # jjj)
                                            

                #                 live_data['data'][0]['object_data'] = final_object_data
                #             # except Exception as  error:
                #             #     print('(live_data)    line --- 2347 ',  error)
                # elif len(live_data['data']) > 1:
                newlivedata = []                    
                for indexlivedata, eachobjectlivedata in enumerate(live_data['data']):
                    if eachobjectlivedata['analyticstype'] == 'RA':
                        object_data = eachobjectlivedata['object_data']
                        if len(object_data) != 0:
                            if 1:
                            # try:
                                final_object_data = []
                                # if len(object_data) == 1:
                                #     if object_data[0]['violation'] == True:
                                #         if object_data[0]['class_name'] == 'person':
                                #             del object_data[0]['bbox']
                                #             del object_data[0]['tracking_id']
                                #             object_data[0]['violation_count'
                                #                 ] = 'person ' + str(1)
                                            
                                #             if "roi_details" in object_data[0].keys():
                                #                 # for inx in object_data[0]["roi_details"]:
                                #                 testttt2 = []
                                #                 for index, inx in enumerate(object_data[0]["roi_details"]): #inx[index]
                                #                     if inx["analytics_type"] == "0" and inx["violation"] == True:
                                #                         testttt2.append(object_data[0]["roi_details"][index])

                                #                 object_data[0]["roi_details"] = testttt2

                                #             final_object_data.append(object_data[0]) #inx[index]) # object_data[0])
                                # elif len(object_data) > 1:
                                for ___, jjj in enumerate(object_data):
                                    if jjj['violation'] == True:
                                        if jjj['class_name'] == 'person':
                                            del jjj['bbox']
                                            del jjj['tracking_id']
                                            jjj['violation_count'] = 'person ' + str(int(___) + int(1))
                                            if "roi_details" in jjj.keys():
                                                testttt3 = []
                                                for index, inx in enumerate(jjj["roi_details"]):
                                                    if inx["analytics_type"] == "0" and inx["violation"] == True:
                                                        testttt3.append(jjj["roi_details"][index])
                                                jjj["roi_details"] = testttt3
                                            final_object_data.append(jjj) #inx[index]) # jjj)
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

def VIolationcountforASRALATEST(live_data):
    ret = False
    if live_data is not None:
        if 1:
        # try:
            if len(live_data['data']) !=0:
                if len(live_data['data']) ==1:
                    if live_data['data'][0]['analyticstype'] == 'RA':
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
                if len(live_data['data']) > 1:
                    newlivedata = []   
                    print("data====latestdata ===",live_data['data'])                 
                    # for indexlivedata, eachobjectlivedata in enumerate(live_data['data']):
                    if live_data['data']['analyticstype'] == 'RA':
                        object_data = live_data['data']['object_data']
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
                                live_data['data']['object_data'] =  final_object_data
                               # newlivedata.append(live_data['data'])
                            # except Exception as  error:
                            #     print('(live_data)    line --- 2347 ',  error)   
                                    
                    #live_data['data']=newlivedata       
                
            ret = live_data
        # except Exception as  error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  2", str(error), " ----time ---- ", now_time_with_time()]))
    else:
        ret = ret
    return ret


# def get_ppe_helmet_violation(details,percent=30):
#     helmet_percentage = (details['helmet'] / details['frame_count']) * 100
#     no_helmet_percentage = (details['no_helmet'] /details['frame_count']) * 100
#     if helmet_percentage >= int(percent) or no_helmet_percentage >= int(percent):
#         if helmet_percentage > no_helmet_percentage:
#             return "true"
#         elif helmet_percentage < no_helmet_percentage:
#             return "false"
#         else:
#             return "null"
#     return "null"


# def get_ppe_vest_violation(details,percent=30):
#     vest_percentage = (details['vest'] / details['frame_count']) * 100
#     arc_jacket_percentage = (details['arc_jacket'] / details['frame_count']) * 100
#     no_vest_jacket_percentage = (details['no_ppe'] / details['frame_count']) * 100
#     if vest_percentage >= int(percent) or arc_jacket_percentage >= int(percent) or no_vest_jacket_percentage >= int(percent):
#         if vest_percentage > arc_jacket_percentage and vest_percentage > no_vest_jacket_percentage:
#             return "vest"
#         elif arc_jacket_percentage > vest_percentage and arc_jacket_percentage > no_vest_jacket_percentage:
#             return "arc_jacket"
#         elif no_vest_jacket_percentage > vest_percentage and no_vest_jacket_percentage > arc_jacket_percentage:
#             return "no_ppe"
#         else:
#             return "null"
#     return "null"





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


def RALIVECOUNT(live_data_count, all_data):
    try:
        data = mongo.db.RAlive_data_count.find_one()
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
            result = mongo.db.RAlive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.RAlive_data_count.insert_one(dictionary)
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


def RALIVECOUNTCamera(live_data_count, all_data):
    try:
        data = mongo.db.RAlive_data_count.find_one()
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
            # result = mongo.db.RAlive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            # if result.matched_count > 0:
            #     pass
            # else:
            #     pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.RAlive_data_count.insert_one(dictionary)
            # if result.acknowledged > 0:
            #     pass
            # else:
            #     pass
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


def PPELIVECOUNT(live_data_count, all_data):
    try:
        data = mongo.db.PPElive_data_count.find_one()
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
            result = mongo.db.PPElive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.PPElive_data_count.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PPELIVEC444OUNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        #ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30




def CrushHelmetLIveCount(live_data_count, all_data):
    try:
        data = mongo.db.CrushHelmetLiveCount.find_one()
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
            result = mongo.db.CrushHelmetLiveCount.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.CrushHelmetLiveCount.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- CrushHelmetLIveCount 1", str(error), " ----time ---- ", now_time_with_time()]))
        #ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30


def CCLIVECOUNT(live_data_count, all_data):
    try:
        data = mongo.db.CRlive_data_count.find_one()
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
            result = mongo.db.CRlive_data_count.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = mongo.db.CRlive_data_count.insert_one(dictionary)
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

def image_roi_draw_data(image_data):
    if image_data is not None:
        if image_data['analyticstype'] == 'PPE_TYPE1':
            image_data['analyticstype'] = 'PPE'
            object_data = image_data['object_data']
            if len(object_data) != 0:
                final_object_data = []
                if len(object_data) == 1:
                    if object_data[0]['Helmet'] == 'None' or object_data[0]['Helmet'] == None or object_data[0]['Vest'] == None or object_data[0]['Vest'] == 'None' or object_data[0]['Vest'] == 'arc_jacket' and object_data[0]['Helmet'] == True:
                        pass
                    elif object_data[0]['class_name'] == 'person':
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
                        if jjj['class_name'] == 'irrd':
                            pass
                        elif jjj['class_name'] == 'cool_coat':
                            pass
                        elif jjj['Helmet'] == 'None' or jjj['Helmet'] == None or jjj['Vest'] == None or jjj['Vest'] == 'None' or jjj['Vest'] == 'arc_jacket' and jjj['Helmet'] == True:
                            pass
                        elif jjj['class_name'] == 'person':
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
        elif image_data['analyticstype'] == 'PPE_TYPE2':
            object_data = image_data['object_data']
            if len(object_data) != 0:
                final_object_data = []
                person_count = 0
                for ___, jjj in enumerate(object_data):
                    if jjj['class_name'] == 'biker':
                        if jjj['Bike_Helmet'] == False:
                            del jjj['tracking_id']
                            jjj['violation_count'] = jjj['class_name'] #+ str(int(person_count) + int(1))
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
                    if object_data[0]['violation'] == False:
                        pass
                    elif object_data[0]['violation'] == True:
                        if object_data[0]['class_name'] == 'person':
                            del object_data[0]['tracking_id']
                            object_data[0]['violation_count']  = 'person ' #+ str(1)
                            final_object_data.append(object_data[0])
                        else:
                            del object_data[0]['tracking_id']
                            object_data[0]['violation_count']  = object_data[0]['class_name'] #+ str(1)
                            final_object_data.append(object_data[0])
                elif len(object_data) > 1:
                    person_count = 0
                    for ___, jjj in enumerate(object_data):
                        person_count = ___
                        if jjj['violation'] == False:
                            pass
                        elif jjj['violation'] == True:
                            if jjj['class_name'] == 'person':
                                del jjj['tracking_id']
                                jjj['violation_count'] = 'person ' #+ str(int(person_count) + int(1))
                                final_object_data.append(jjj)
                            else:
                                jjj['violation_count'] = jjj['class_name'] #+ str(int(person_count) + int(1))
                                final_object_data.append(jjj)
                image_data['object_data'] = final_object_data
        # elif image_data['analyticstype'] == 'RA':
        #     object_data = image_data['object_data']
        #     if len(object_data) != 0:
        #         final_object_data = []
        #         if len(object_data) == 1:
        #             if object_data[0]['violation'] == False:
        #                 pass
        #             elif object_data[0]['violation'] == True:
        #                 if object_data[0]['class_name'] == 'person':
        #                     del object_data[0]['tracking_id']
        #                     object_data[0]['violation_count']  = 'person '# + str(1)
        #                     final_object_data.append(object_data[0])
        #                 else:
        #                     del object_data[0]['tracking_id']
        #                     object_data[0]['violation_count']  = object_data[0]['class_name'] #+ str(1)
        #                     final_object_data.append(object_data[0])
        #         elif len(object_data) > 1:
        #             person_count = 0
        #             for ___, jjj in enumerate(object_data):
        #                 person_count = ___
        #                 if jjj['violation'] == False:
        #                     pass
        #                 elif jjj['violation'] == True:
        #                     if jjj['class_name'] == 'person':
        #                         del jjj['tracking_id']
        #                         jjj['violation_count'] = 'person ' #+ str(int(person_count) + int(1))
        #                         final_object_data.append(jjj)
        #                     else:
        #                         jjj['violation_count'] = jjj['class_name'] #+ str(int(person_count) + int(1))
        #                         final_object_data.append(jjj)
        #         image_data['object_data'] = final_object_data
    return image_data




def VIolationcountforTRA(live_data):
    ret = False
    if live_data is not None:
        if 1:
        # try:
            if len(live_data['data']) !=0:
                newlivedata = []                    
                for indexlivedata, eachobjectlivedata in enumerate(live_data['data']):
                    if eachobjectlivedata['analyticstype'] == 'RA':
                        object_data = eachobjectlivedata['object_data']
                        if len(object_data) != 0:
                            # try:
                            final_object_data = []                                
                            for ___, jjj in enumerate(object_data):
                                if jjj['violation'] == True:
                                    del jjj['bbox']
                                    del jjj['tracking_id']
                                    jjj['violation_count'] = jjj['class_name'] + str(int(___) + int(1))
                                    if "roi_details" in jjj.keys():
                                        testttt3 = []
                                        for index, inx in enumerate(jjj["roi_details"]):
                                            if inx["analytics_type"] == "2" and inx["violation"] == True:
                                                testttt3.append(inx)
                                        if len(testttt3) !=0:
                                            jjj["roi_details"] = testttt3
                                            final_object_data.append(jjj)    

                            if len(final_object_data) !=0 :                                      
                                eachobjectlivedata['object_data'] =  final_object_data
                                newlivedata.append(eachobjectlivedata)


                        Newanalyticsdata = eachobjectlivedata['analytics_data']
                        # if 'ROI_details' in Newanalyticsdata:
                        #     if len(Newanalyticsdata['ROI_details']) !=0 :
                        #         # print("0000000000000000000000000----------",)

                        #         for new, roiDetails in enumerate(Newanalyticsdata['ROI_details']):
                        #             print("----------roiDetails--------",roiDetails)
                            # except Exception as  error:
                            #     print('(live_data)    line --- 2347 ',  error)   
                if len(newlivedata)   !=0:    
                    live_data['data']=newlivedata    
                else:
                    live_data=[]   
                
            ret = live_data
        # except Exception as  error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  2", str(error), " ----time ---- ", now_time_with_time()]))
    else:
        ret = ret
    return ret

##done
@violationanalysis_data.route('/check_process', methods=['GET'])
def process_checking_for():
    processName = ['docketrun-app', 'python3', 'node', 'dup', 'esi-monitor','smrec','hydra-app','phaseone-app','fire-smoke-dust','spillage_app','tg_steamsuit','vehicalparkingmanagementsystem','wheel-count-missing']
    status = checkProcessRunning(processName)
    ret = {'message': 'something went wrong with process checking','success': False}
    if status['success']:
        ret = status
    else:
        ret = status
    return ret


@violationanalysis_data.route('/violation_excel_download', methods=['GET'])
def violation_excel_result():
    if 1:
    # try:
        list_of_files = glob.glob(os.path.join(os.getcwd(), "violation_excel_sheets/*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        path, filename = os.path.split(latest_file)
        if filename:
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
        else:
            return {'success': False, 'message': 'File is not found.'}
    # except (NameError, RuntimeError, FileNotFoundError, AssertionError,
    #     AttributeError, EOFError, FloatingPointError, TypeError,
    #     GeneratorExit, IndexError, KeyError, KeyboardInterrupt, MemoryError,
    #     NotImplementedError, OSError, OverflowError, ReferenceError,
    #     StopIteration, SyntaxError, IndentationError, TabError, SystemError,
    #     SystemExit, TypeError, UnboundLocalError, UnicodeError,
    #     UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError,
    #     ValueError, ZeroDivisionError, ConnectionError, KeyboardInterrupt,
    #     BaseException, ValueError) as error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_excel_download 1", str(error), " ----time ---- ", now_time_with_time()]))         
    #     return {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_excel_download 2", str(error), " ----time ---- ", now_time_with_time()])) 
    #     return {'success': False, 'message': str(error)}

     
@violationanalysis_data.route('/get_roi_image/<image_file>', methods=['GET'])
def get_roi_image_(image_file):
    try:
        base_path = os.path.join(os.getcwd(), 'rtsp_roi_image')
        response = send_from_directory(base_path, image_file)
        return response
    except Exception as  error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        main_path = os.path.abspath(path)
        return send_from_directory(main_path, filename)
        # return str(error)
    
    



@violationanalysis_data.route('/PPEviolationPercentage', methods=['POST'])
@violationanalysis_data.route('/PPEviolationPercentage', methods=['GET'])
def PPEviolationPercentage():
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
        if request.method == 'POST':
            jsonobject = request.json
            print('-----------------jsonobject---------',jsonobject)
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['ppepercentage']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    all_data = []
                    ppepercentage = jsonobject['ppepercentage'] 
                    if 'crash_helmet'  in ppepercentage and ppepercentage is not None:   
                        Foundfileterdata = mongo.db.filterviolations.find_one({})
                        if Foundfileterdata is not None:
                            id = Foundfileterdata['_id']
                            FILterviolationUPdateresult = mongo.db.filterviolations.update_one({'_id':ObjectId(id)}, {'$set':ppepercentage})
                            if FILterviolationUPdateresult.modified_count > 0:
                                ret = {'message':'filter percentage is set successfully.','success': True}
                            else:
                                ret = {'message':'filter percentage is set already.','success': True}
                        else :
                            filterviolationsinsertionresult =  mongo.db.filterviolations.insert_one(ppepercentage)  
                            if filterviolationsinsertionresult.acknowledged > 0  :
                                ret ={'message':'filter percentage is set successfully.','success':True}   
                            else:
                                ret['message']='something wrong with the insertion of filter percentage.'  
                    elif ppepercentage is not None:
                        Foundfileterdata = mongo.db.filterviolations.find_one({})
                        if Foundfileterdata is not None:
                            id = Foundfileterdata['_id']
                            FILterviolationUPdateresult = mongo.db.filterviolations.update_one({'_id':ObjectId(id)}, {'$set':{"helmet":ppepercentage['helmet'],"vest":ppepercentage['vest']}})
                            if FILterviolationUPdateresult.modified_count > 0:
                                ret = {'message':'filter percentage is set successfully.','success': True}
                            else:
                                ret = {'message':'filter percentage is set already.','success': True}
                        else :
                            filterviolationsinsertionresult =  mongo.db.filterviolations.insert_one(ppepercentage)  
                            if filterviolationsinsertionresult.acknowledged > 0  :
                                ret ={'message':'filter percentage is set successfully.','success':True}   
                            else:
                                ret['message']='something wrong with the insertion of filter percentage.'                
                        
            else:
                ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
        elif request.method == 'GET':
            Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
            if Foundfileterdata is not None:
                ret = {'message':Foundfileterdata,'success': True}
            else :
                ppepercentage = {"helmet":70,"vest":70} 
                newvlaue = ppepercentage
                filterviolationsinsertionresult =  mongo.db.filterviolations.insert_one(ppepercentage)  
                if filterviolationsinsertionresult.acknowledged > 0  :
                    ret ={'message':newvlaue,'success':True}   
                else:
                    ret['message']='something wrong with the of filter percentage.'   
    return jsonify(ret)
    


@violationanalysis_data.route('/live_data1TRA', methods=['GET'])
@violationanalysis_data.route('/live_data1TRA/cameraname/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1TRA/department/<department_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1TRA', methods=['POST'])
def LIVEVIOLATIONOFTRA(violation_type='RA', camera_name=None,department_name =None):
    ret = {'success': False,'message':"something went wrong in Restricted AreaLiveCount apis"}
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type,'violation_status': True}
    if request.method == 'POST':
        jsonobject = request.json
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
                match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and department_name !='') :
                    match_data['camera_name']= camera_name
                    match_data['department']= department_name
                    pipeline = [
                                {'$match': match_data},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]                  
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]                    
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    match_data['department']= department_name
                    pipeline = [
                                {'$match': match_data},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]                    
                else:
                    pipeline = [
                                {'$match': match_data},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]

                data=list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = VIolationcountforTRA(i)
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
    
    elif request.method == 'GET':
        dash_data = []
        if camera_name is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }            
            pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1, 'ticketno': -1}},
                        {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000}
                    ]        
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
            pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1, 'ticketno': -1}},
                        {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000}
                    ]
            
        data=list(mongo.db.data.aggregate(pipeline))
        if len(data) != 0:
            count1 = 0 
            for count, i in enumerate(data):
                wapas_data = VIolationcountforTRA(i)
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
    return jsonify(ret)


@violationanalysis_data.route('/live_data1RA', methods=['GET'])
@violationanalysis_data.route('/live_data1RA/cameraname/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1RA/department/<department_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1RA', methods=['POST'])
def LIVEVIOLATIONOFRA(violation_type='RA', camera_name=None,department_name =None):
    ret = {'success': False,'message':"something went wrong in Restricted AreaLiveCount apis"}
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type,'violation_status': True}
    if request.method == 'POST':
        jsonobject = request.json
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
                match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }
                #'object_data.violation':True,'object_data.roi_details.analytics_type':"0"}
                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and    department_name !='') :
                    match_data['camera_name']= camera_name
                    match_data['department']= department_name
                    pipeline = [
                                {'$match': match_data},
                                # {'$sort': {'timestamp': -1, '_id': -1}},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                # {'$sort': {'_id.ticketno': -1}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]                    
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                # {'$sort': {'timestamp': -1, '_id': -1}},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                # {'$sort': {'_id.ticketno': -1}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]                    
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    match_data['department']= department_name
                    pipeline = [
                                {'$match': match_data},
                                # {'$sort': {'timestamp': -1, '_id': -1}},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                # {'$sort': {'_id.ticketno': -1}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]                    
                else:
                    pipeline = [
                                {'$match': match_data},
                                # {'$sort': {'timestamp': -1, '_id': -1}},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                # {'$sort': {'_id.ticketno': -1}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000}
                            ]
                data=list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = VIolationcountforRA(i)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            count1 +=1         
                            wapas_data['SNo'] = count1
                            if wapas_data not in dash_data:
                                dash_data.append(wapas_data)
                        else:
                            count1 +=1
                            i['SNo'] = count1
                            if i not in dash_data:
                                dash_data.append(i)
                    all_data = RALIVECOUNT(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    elif request.method == 'GET':
        dash_data = []
        if camera_name is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'camera_name': camera_name,
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }
            # match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type,'violation_status': True,'object_data.violation':True,'object_data.roi_details.analytics_type':"0"}
            pipeline = [
                        {'$match': match_data},
                        # {'$sort': {'timestamp': -1, '_id': -1}},
                        {'$sort': {'timestamp': -1, 'ticketno': -1}},
                        {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                        # {'$sort': {'_id.ticketno': -1}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000}
                    ]
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }
            
            # match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type,'violation_status': True,'object_data.violation':True,'object_data.roi_details.analytics_type':"0"}
            # print("================match_data==============",match_data)
            pipeline = [
                        {'$match': match_data},
                        # {'$sort': {'timestamp': -1, '_id': -1}},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 10}
                    ]            
            # pipeline = [
            #                 {'$match': {'violation_status': True, 'analyticstype': 'RA'}},
            #                 {'$project': {
            #                     '_id': 1,
            #                     'ticketno': 1,
            #                     'analyticstype':1,
            #                     'camera_name':1,
            #                     'object_data': {
            #                         '$filter': {
            #                             'input': '$object_data',
            #                             'as': 'obj',
            #                             'cond': {'$eq': ['$$obj.violation', True]}
            #                         }
            #                     },
            #                     'timestamp': 1,
            #                     'imagename': 1,
            #                     'hooter_enabled':1,
            #                     'hooteraknowledgement':1,
            #                     'department':1,
            #                     'violation_status':1,
            #                     'violation_verificaton_status':1
            #                 }},
            #                 {'$match': {'object_data': {'$ne': []}}},  # Ensure only documents with non-empty object_data are included
            #                 {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
            #                 {'$sort': {'_id.ticketno': -1}},
            #                 {'$limit': 4000000}
            #             ]

            
        data=list(mongo.db.data.aggregate(pipeline))
        if len(data) != 0:
            count1 = 0 
            for count, i in enumerate(data):
                wapas_data = VIolationcountforRA(i)
                if type(wapas_data) == list:
                    pass
                elif wapas_data:
                    count1 +=1         
                    wapas_data['SNo'] = count1
                    if wapas_data not in dash_data:
                        dash_data.append(wapas_data)
                else:
                    count1 +=1
                    i['SNo'] = count1
                    if i not in dash_data:
                        dash_data.append(i)
                    # dash_data.append(i)
            if len(dash_data) !=0 :
                ret['message']=parse_json(dash_data)
                ret['success']=True
            else:
                ret['message']='violation data not found.'
            # all_data = RALIVECOUNT(len(dash_data), parse_json(dash_data))
            # print("---------------------------data RestrictedArea000001",len(all_data['message']))
            # ret = all_data
        else:
            ret['message'] = 'data not found'  
    return jsonify(ret)


@violationanalysis_data.route('/latest_dataTRA', methods=['GET'])
@violationanalysis_data.route('/latest_dataTRA/<cameraname>', methods=['GET'])
@violationanalysis_data.route('/latest_dataTRA/department/<department_name>', methods=['GET'])
def latest_dataTRA_( violation_type='RA' ,cameraname=None,department_name=None):
    ret = {'success': False,'message':"something went wrong in RestrictedAreaLiveCount apis"}
    if 1:    
        dash_data = []
        if cameraname is not None :
            # match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': cameraname, 'analyticstype': violation_type}
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'camera_name': cameraname,
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
            # {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}
            data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforTRA(data[0])
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found'
        else:
            # match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': violation_type,
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
            data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},                                                        
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}}, {'$project': {"_id":0,'data':1,}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforTRA(data[0])
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True} #all_data
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return jsonify(parse_json(ret))


@violationanalysis_data.route('/live_data1PPE', methods=['GET','POST'])
@violationanalysis_data.route('/live_data1PPE/cameraname/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1PPE/department/<department_name>', methods=['GET'])
def LIVEVIOLATIONOFPPE(violation_type='PPE_TYPE1', camera_name=None,department_name =None):
    ret = {'success': False,'message':"something went wrong in Personal Protective EquipmentLIveCount apis"}
    dash_data = []
    pipeline = []
    Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type,'violation_status': True}
    if Foundfileterdata  is None:
        Foundfileterdata = {"helmet":70,"vest":70} 
    if request.method == 'POST':
        jsonobject = request.json
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
                    match_data['department']= department_name
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
                data = list(mongo.db.data.aggregate(pipeline))
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
    elif request.method == 'GET':
        if camera_name is not None :
            match_data['camera_name']=camera_name
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]

        if (department_name is not None and department_name != 'none'):
            match_data['department']=department_name
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
        else:
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
        data = list(mongo.db.data.aggregate(pipeline))
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
    return jsonify(ret)




@violationanalysis_data.route('/live_data1CrushHelmet', methods=['GET','POST'])
@violationanalysis_data.route('/live_data1CrushHelmet/cameraname/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1CrushHelmet/department/<department_name>', methods=['GET'])
def CrushHelmetLIveviolation(violation_type='PPE_TYPE2', camera_name=None,department_name =None):
    ret = {'success': False,'message':"something went wrong in Personal Protective EquipmentLIveCount apis"}
    dash_data = []
    pipeline = []
    Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type,'violation_status': True}
    if Foundfileterdata  is None:
        Foundfileterdata = {"helmet":70,"vest":70} 
    if request.method == 'POST':
        jsonobject = request.json
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
                    match_data['department']= department_name
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    count1 = 0 
                    for count, i in enumerate(data):
                        wapas_data = VIolationcountforCrushHelmet(i,Foundfileterdata)
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
                    all_data = CrushHelmetLIveCount(len(dash_data), parse_json(dash_data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found' 
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    elif request.method == 'GET':
        if camera_name is not None :
            match_data['camera_name']=camera_name
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]

        if (department_name is not None and department_name != 'none'):
            match_data['department']=department_name
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
        else:
            pipeline = [
                        {'$match': match_data},
                        {'$limit': 4000000},
                        {'$sort': {'timestamp': -1}},
                    ]
        data = list(mongo.db.data.aggregate(pipeline))
        if len(data) != 0:
            count1 = 0 
            for count, i in enumerate(data):
                wapas_data = VIolationcountforCrushHelmet(i,Foundfileterdata)
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
            all_data = CrushHelmetLIveCount(len(dash_data), parse_json(dash_data))
            ret = all_data
        else:
            ret['message'] = 'data not found' 
    return jsonify(ret)


@violationanalysis_data.route('/live_data1TC', methods=['GET','POST'])
@violationanalysis_data.route('/live_data1TC/<camera_name>', methods=['GET'])#
@violationanalysis_data.route('/live_data1TC/department/<department_name>', methods=['GET'])
def LIVETRAFFICCOUNTDATA(camera_name=None,department_name=None):
    ret = {'success': False,'message':"something went wrong in TrafficCountLiveCount apis"}
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
    pipeline=[]
    if request.method == 'POST':
        jsonobject = request.json
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

                print(":TYPE---------department_name",type(department_name))
                print(":TYPE---------camera_name",type(camera_name))
                print("--------------------------------LIVE_DATA1TC---",jsonobject)
                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and    department_name !='') :
                    print("------------------------------condition 1-----liveTC")
                    match_data['camera_name']= camera_name
                    match_data['department'] = department_name
                    pipeline = [
                                {'$match': match_data},
                                {'$sort': {'timestamp': -1}},
                                {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                            ]
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    print("------------------------------condition 2-----liveTC")
                    match_data['camera_name']= camera_name
                    pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                         ]
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    print("------------------------------condition 3-----liveTC")
                    match_data['department'] = department_name
                    pipeline=[
                                {'$match': match_data},
                                {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$push': '$$ROOT'}}},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                    ]
                else:
                    print("------------------------------condition 4-----liveTC")
                    pipeline=[
                                        {'$match': match_data},
                                        {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$push': '$$ROOT'}}},
                                        {'$limit': 4000000},
                                        {'$sort': {'timestamp': -1}},

                                    ]

            data = list(mongo.db.trafficcountdata.aggregate(pipeline))
        
            if len(data) != 0:
                ret = {"message":data,"success":True}
            else:
                ret['message']='data not found'
    elif request.method == 'GET':   
        print("---------------match_data---GET request--------",match_data) 
        pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': '_id',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$unwind': '$camera_data'},
                        {
                        '$project': {
                            '_id': 0,
                            'data': {
                                '$map': {
                                    'input': '$data',
                                    'as': 'item',
                                    'in': {
                                        'timestamp': '$$item.timestamp',
                                        'camera_name': '$$item.camera_name',
                                        '_id': '$$item._id',
                                        'camera_rtsp': '$$item.camera_rtsp',
                                        'cameraid': '$$item.cameraid',
                                        'count': '$$item.count',
                                        'date': '$$item.date',
                                        'direction': '$$item.direction',
                                        'id_no': '$$item.id_no',
                                        'line_metadata': '$$item.line_metadata',
                                        'line_name': '$$item.line_name',
                                        'violation_status': '$$item.violation_status',
                                        'violation_verificaton_status': '$$item.violation_verificaton_status',
                                        'department': '$camera_data.department'
                                    }
                                }
                            }
                        }
                        }
                    ]
        dash_data = []
        if camera_name is not None :
            
            match_data['camera_name']= camera_name
            pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': '_id',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$unwind': '$camera_data'},
                        {
                        '$project': {
                            '_id': 0,
                            'data': {
                                '$map': {
                                    'input': '$data',
                                    'as': 'item',
                                    'in': {
                                        'timestamp': '$$item.timestamp',
                                        'camera_name': '$$item.camera_name',
                                        '_id': '$$item._id',
                                        'camera_rtsp': '$$item.camera_rtsp',
                                        'cameraid': '$$item.cameraid',
                                        'count': '$$item.count',
                                        'date': '$$item.date',
                                        'direction': '$$item.direction',
                                        'id_no': '$$item.id_no',
                                        'line_metadata': '$$item.line_metadata',
                                        'line_name': '$$item.line_name',
                                        'violation_status': '$$item.violation_status',
                                        'violation_verificaton_status': '$$item.violation_verificaton_status',
                                        'department': '$camera_data.department'
                                    }
                                }
                            }
                        }
                        }
                    ]
        
        if department_name is not None:
            pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                    ]            
        data = list(mongo.db.trafficcountdata.aggregate(pipeline))
        
        if len(data) != 0:
            ret = {"message":data,"success":True}
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
            data = list(mongo.db.trafficcountdata.aggregate([
                                        {'$match': match_data},
                                        {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$push': '$$ROOT'}}},
                                        {'$limit': 4000000},
                                        {'$sort': {'timestamp': -1}},
                                        {'$project': {"_id": 0, 'data': 1}},
                                        {'$unwind': '$data'},
                                        {
                                            '$lookup': {
                                                'from': 'ppera_cameras',
                                                'localField': 'data.camera_name',
                                                'foreignField': 'cameraname',
                                                'as': 'camera_data'
                                            }
                                        },
                                        {'$unwind': '$camera_data'},
                                        {
                                            '$project': {
                                                'data.timestamp': '$data.timestamp',
                                                'data.camera_name': '$data.camera_name',
                                                'data._id':'$data._id',
                                                'data.camera_rtsp':'$data.camera_rtsp',
                                                'data.cameraid':'$data.cameraid',
                                                'data.count':'$data.count',
                                                'data.date':'$data.date',
                                                'data.direction':'$data.direction',
                                                'data.id_no':'$data.id_no',
                                                'data.line_metadata':'$data.line_metadata',
                                                'data.line_name':'$data.line_name',
                                                'data.violation_status':'$data.violation_status',
                                                'data.violation_verificaton_status':'$data.violation_verificaton_status',
                                                'data.department': '$camera_data.department',
                                            }
                                        }
                                    ]))

            if len(data) != 0:
                ret = {"message":data,"success":True}
                
            else:
                ret['message'] = 'data not found'  
    return jsonify(parse_json(ret))




@violationanalysis_data.route('/live_data1CC', methods=['GET','POST'])
@violationanalysis_data.route('/live_data1CC/cameraname/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1CC/department/<department_name>', methods=['GET'])
def LIVEVIOLATIONOFCC(violation_type='CRDCNT', camera_name=None,department_name =None):
    ret = {'success': False,'message':"something went wrong in CrowdcountLive apis"}
    pipeline=[]
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type,'violation_status': True}

    if request.method == 'POST':
        jsonobject = request.json
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
                    match_data['department'] = department_name
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}}
                            ]
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}}
                            ]
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    match_data['department'] = department_name
                    pipeline = [
                            {'$match': match_data},
                            {'$limit': 4000000},
                            {'$sort': {'timestamp': -1}}
                        ]
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    all_data = CCLIVECOUNT(len(data), parse_json(data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'   
        
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    elif request.method == 'GET':    
        dash_data = []    
        if camera_name is not None :
            match_data['camera_name']=camera_name
            pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}}
            ]

        if (department_name is not None and department_name != 'none'):
            match_data['department'] = department_name
            pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}}
            ]
        else:
            pipeline = [
                {'$match': match_data},
                {'$limit': 4000000},
                {'$sort': {'timestamp': -1}},
            ]
        data = list(mongo.db.data.aggregate(pipeline))   
        if len(data) != 0:
            all_data = CCLIVECOUNT(len(data), parse_json(data))
            ret = all_data
        else:
            ret['message'] = 'data not found'  
    return jsonify(ret)




@violationanalysis_data.route('/live_data1', methods=['GET'])
@violationanalysis_data.route('/live_data1/violation/<violation_type>', methods=['GET'])
@violationanalysis_data.route('/live_data1/cameraname/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/live_data1/<camera_name>/<violation_type>', methods=['GET'])
def admin_live_data_with_pagination(violation_type=None, camera_name=None):
    ret = {'success': False,'message':"something went wrong in LIveDataDetails apis"}
    try:
    # if 1:        
        dash_data = []
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70} 
        if camera_name is not None and violation_type is not None:
            if violation_type == 'PPE':
                violation_type = 'PPE_TYPE1'
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
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
            data =list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
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
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
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
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data1 1", str(error), " ----time ---- ", now_time_with_time()]))   
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data1 2", str(error), " ----time ---- ", now_time_with_time()]))   
    return jsonify(ret)


def LIVEDATAcamera_name_wise(live_data,ppepercentage):
    ret = False
    if live_data is not None:
        try:
            if live_data['analyticstype'] == 'PPE_TYPE1':
                live_data['analyticstype'] = 'PPE'
                object_data = live_data['object_data']
                if len(object_data) != 0:
                    try:
                        final_object_data = []
                        if len(object_data) == 1:
                            if object_data[0]['Helmet']  == 'None' or object_data[0]['Helmet']  == None or object_data[0]['Vest']  == None or object_data[0]['Vest']  == 'None' or object_data[0]['Vest']  == 'arc_jacket' and object_data[0]['Helmet']  == True:
                                pass
                            elif object_data[0]['class_name'] == 'irrd':
                                pass
                            elif object_data[0]['class_name'] == 'cool_coat':
                                pass
                            elif object_data[0]['class_name'] == 'person':
                                if object_data[0]['Helmet'] == False:
                                    del object_data[0]['bbox']
                                    del object_data[0]['tracking_id']
                                    object_data[0]['violation_count'] = 'person ' + str(1)
                                    final_object_data.append(object_data[0])
                                elif object_data[0]['Vest'] == 'no_ppe':
                                    del object_data[0]['bbox']
                                    del object_data[0]['tracking_id']
                                    object_data[0]['violation_count'] = 'person ' + str(1)
                                    final_object_data.append(object_data[0])
                        elif len(object_data) > 1:
                            person_count = 0
                            for ___, jjj in enumerate(object_data):
                                if jjj['class_name'] == 'irrd':
                                    pass
                                elif jjj['class_name'] == 'cool_coat':
                                    pass
                                elif jjj['Helmet'] == 'None' or jjj['Helmet'] == None or jjj['Vest'] == None or jjj['Vest'] == 'None' or jjj['Vest'] == 'arc_jacket' and jjj['Helmet'] == True:
                                    pass
                                elif jjj['class_name'] == 'person':
                                    if jjj['Helmet'] == False:
                                        del jjj['bbox']
                                        del jjj['tracking_id']
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1
                                    elif jjj['Vest'] == 'no_ppe':
                                        del jjj['bbox']
                                        del jjj['tracking_id']
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1
                        if len(final_object_data) != 0:
                            live_data['object_data'] = final_object_data
                        else:
                            live_data = []
                    except Exception as  error:
                        print(' live_data_processing_for_66dash_board(live_data) ---- line -2319 ',  error)
                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_processing_for333_dash_board_for_camera_name_wise 1", str(error), " ----time ---- ", now_time_with_time()]))  
            elif live_data['analyticstype'] == 'RA':
                object_data = live_data['object_data']
                if len(object_data) != 0:
                    try:
                        final_object_data = []
                        if len(object_data) == 1:
                            if object_data[0]['violation'] == False:
                                pass
                            elif object_data[0]['violation'] == True:
                                if object_data[0]['class_name'] == 'person':
                                    del object_data[0]['bbox']
                                    del object_data[0]['tracking_id']
                                    object_data[0]['violation_count'] = 'person ' + str(1)
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
                        live_data['object_data'] = final_object_data
                    except Exception as  error:
                        print('(live_data)---line --- 2347 ',  error)
                        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --live_data_processing_for_555dash_board_for_camera_name_wise 2", str(error), " ----time ---- ", now_time_with_time()]))  
            ret = live_data
        except Exception as  error:
            print('def (live_data) line 2350 ', error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --live_data_processing_for_dash_555board_for_camera_name_wise 3", str(error), " ----time ---- ", now_time_with_time()]))             
    else:
        ret = ret
    return ret




#
"""{'$project': {   'appruntime':0,
'datauploadstatus':0,'date':0,'imguploadstatus':0,
'cameraid':0,'id_no':0 ,'ticketno':0,
'object_data':0,'violation_verificaton_status':0,'_id':0}}"""
@violationanalysis_data.route('/latest_data_camera_name', methods=['GET'])
@violationanalysis_data.route('/latest_data_camera_name/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/latest_data_camera_name/department/<department_name>', methods=['GET'])
def latest_data_camera_id(camera_name=None,department_name=None):
    ret = {'success': False, 'message':'something went wrong with camera wise latest data'}
    try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}         
        if camera_name is not None:
            if camera_name == 'all_cameras':
                data = list(mongo.db.data.aggregate([{'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'camera_name': '$camera_name'}, 'data':{'$first':'$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                count1 = 0 
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            elif camera_name is not None:
                match_data = {'camera_name': camera_name}
                data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}}, {'$limit': 1},
                                                     {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                count1 = 0 
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = LIVEDATAcamera_name_wise(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i)
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            else:
                data = list(mongo.db.data.aggregate([{'$sort': {'timestamp': -1}}, {'$group': {'_id': {'camera_name': '$camera_name'},'data': {'$first': '$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                count1 = 0 
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data']['data'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
        else:
            data =list(mongo.db.data.aggregate([{'$sort': {'timestamp': -1}}, {'$limit': 4000000}, {'$group': {'_id': {'camera_name':'$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                                                {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
            dash_data = []
            count1 = 0 
            if len(data) != 0:
                for count, i in enumerate(data):
                    wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                    if type(wapas_data) == list:
                        pass
                    elif wapas_data:
                        dash_data.append(wapas_data)
                    else:
                        dash_data.append(i['data']['data'])
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data_camera_name 1", str(error), " ----time ---- ", now_time_with_time()]))  
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data_camera_name 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return jsonify(ret)


@violationanalysis_data.route('/latest_data_violation_type', methods=['GET'])
@violationanalysis_data.route('/latest_data_violation_type/<violation_type>', methods=['GET'])
def latest_data_analyticstype(violation_type=None):
    ret = {'success': False, 'message':'something went wrong with violation type wise latest data'}
    try:
        
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
        if violation_type is not None:
            if violation_type == 'all_violations':
                data = list(mongo.db.data.aggregate([{'$sort': {'timestamp': -1}}, {'$limit': 4000000}, {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data': {'$first':'$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                count1 = 0 
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            elif violation_type is not None:
                if violation_type == 'PPE':
                    violation_type = 'PPE_TYPE1'
                match_data = {'analyticstype': violation_type}
                data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}, {'$limit': 1}
                                                     ,{'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                count1 = 0 
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i)
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            else:
                data = list(mongo.db.data.aggregate([{'$sort': {'timestamp': -1}}, {'$limit': 4000000}, {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data': {'$first':'$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                count1 = 0 
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
        else:
            data = list(mongo.db.data.aggregate([{'$sort': {'timestamp': -1}}, {'$limit': 4000000}, {'$group': {'_id': {'analyticstype':'$analyticstype'}, 'data': {'$first': '$$ROOT'}}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
            dash_data = []
            count1 = 0 
            if len(data) != 0:
                for count, i in enumerate(data):
                    wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                    if type(wapas_data) == list:
                        pass
                    elif wapas_data:
                        dash_data.append(wapas_data)
                    else:
                        dash_data.append(i['data'])
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data_violation_type 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data_violation_type 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return jsonify(ret)


@violationanalysis_data.route('/camera_details', methods=['GET'])
def camera_id_details():
    ret = {'success': False, 'message':'something went wrong with camera_overdetails details'}
    try:
        match_data =  {
      "$expr": {
        "$and": [
          { "$ne": ["$roi_data", None] },
          { "$ne": [{ "$size": "$roi_data" }, 0] }
        ]
      }
    }
        
        data = list(mongo.db.ppera_cameras.aggregate([{'$sort': {'_id': -1}},{'$group': {'_id': {'cameraname': '$cameraname'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
        # data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}}, {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
        #                                      {'$project': {'data': 0}}]))
        dash_data = []
        if len(data) != 0:
            for count, i in enumerate(data):
                dash_data.append(i['_id']['cameraname'])
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_overall-details 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_overall-details 3", str(error), " ----time ---- ", now_time_with_time()]))          
    return jsonify(ret)




@violationanalysis_data.route('/camera_detailsRA', methods=['GET'])
@violationanalysis_data.route('/camera_detailsRA/<department>', methods=['GET'])
@violationanalysis_data.route('/camera_detailsRA', methods=['POST'])
def camera_id_detailsRA(department=None):
    ret = {'success': False, 'message':'something went wrong with camera_RAdetails details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department = jsonobject['department']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }
                if department and department != 'none':
                    match_data['department']=department
                data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['cameraname'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':
        try:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }

            if department and department != 'none':
                match_data['department']=department
            data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['cameraname'])
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- cameraRA_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- cameraRA_details 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return jsonify(ret)



@violationanalysis_data.route('/camera_detailsTRA', methods=['GET'])
@violationanalysis_data.route('/camera_detailsTRA/<department>', methods=['GET'])
@violationanalysis_data.route('/camera_detailsTRA', methods=['POST'])
def camera_id_detailsTRA(department=None):
    ret = {'success': False, 'message':'something went wrong with cameraTRA_details details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department = jsonobject['department']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                if department and department != 'none':
                    match_data['department']=department
                data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['cameraname'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':
        try:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
            if department and department != 'none':
                match_data['department']=department
            data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['cameraname'])
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- cameraTRA_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- cameraTRA_details 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return jsonify(ret)




@violationanalysis_data.route('/department_detailsRA', methods=['GET'])
@violationanalysis_data.route('/department_detailsRA/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/department_detailsRA', methods=['POST'])
def departmentrr_detailsRA(camera_name=None):
    ret = {'success': False, 'message':'something went wrong with department_rrdetailsRA details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                camera_name= jsonobject['camera_name']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }
                if camera_name and camera_name != 'none':
                    match_data['camera_name']=camera_name
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
                }]            
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':
                
        try:
            dash_data=[]
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                     }
                            }

            if camera_name and camera_name != 'none':
                match_data['camera_name']=camera_name
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
            data = list(mongo.db.data.aggregate(pipeline))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_rrdetailsRA 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_eeedetailsRA 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return jsonify(ret)


@violationanalysis_data.route('/department_detailsTRA', methods=['GET'])
@violationanalysis_data.route('/department_detailsTRA/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/department_detailsTRA', methods=['POST'])
def department_rreddetailsTRA(camera_name=None):
    ret = {'success': False, 'message':'something went wrong with departmentfdddf_detailsRA details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                camera_name = jsonobject['camera_name']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                if camera_name and camera_name !='none':
                    match_data['camera_name']=camera_name
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
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
    elif request.method == 'GET':        
        try:
            dash_data=[]
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
            if camera_name and camera_name !='none':
                match_data['camera_name']=camera_name
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
            data = list(mongo.db.data.aggregate(pipeline))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --DEPARTMENTTR", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- dEPARTMENTTR 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return jsonify(ret)

@violationanalysis_data.route('/camera_detailsPPE', methods=['GET'])
@violationanalysis_data.route('/camera_detailsPPE/<department>', methods=['GET'])
@violationanalysis_data.route('/camera_detailsPPE', methods=['POST'])
def camera_id_detailsPPE(department=None):
    ret = {'success': False, 'message':'something went wrong with camerappe_details details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department = jsonobject['department']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': 'PPE_TYPE1','violation_status': True}
                if department and department !='none':
                    match_data['department']=department
                data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['cameraname'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':        
        try:
            match_data =  {'analyticstype': 'PPE_TYPE1','violation_status': True,'timestamp':{'$regex': '^' + str(date.today())}}    
            if department and department != 'none':
                match_data['department']=department        
            data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['cameraname'])
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camerappe_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camerappe_details 2", str(error), " ----time ---- ", now_time_with_time()]))    
        
    return jsonify(ret)



@violationanalysis_data.route('/camera_detailsCrushHelmet', methods=['GET'])
@violationanalysis_data.route('/camera_detailsCrushHelmet/<department>', methods=['GET'])
@violationanalysis_data.route('/camera_detailsCrushHelmet', methods=['POST'])
def BCrushHelmet(department=None):
    ret = {'success': False, 'message':'something went wrong with cameraCrashHelment_details details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department = jsonobject['department']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': 'PPE_TYPE2','violation_status': True}
                if department and department  !='none':
                    match_data['department']=department
                data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['cameraname'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':        
        try:
            match_data =  {'analyticstype': 'PPE_TYPE2','violation_status': True,'timestamp':{'$regex': '^' + str(date.today())}}     
            if department and department != 'none':
                match_data['department']=department        
            data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['cameraname'])
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- cameracarshHelmet_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_CrashHelmetdetails 2", str(error), " ----time ---- ", now_time_with_time()]))    
        
    return jsonify(ret)

@violationanalysis_data.route('/department_detailsPPE', methods=['GET'])
@violationanalysis_data.route('/department_detailsPPE/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/department_detailsPPE', methods=['POST'])
def department_ddvccddetailsPPE(camera_name=None):
    ret = {'success': False, 'message':'something went wrong with department_ffdddetailsPPE details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                camera_name = jsonobject['camera_name']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': 'PPE_TYPE1','violation_status': True}
                if camera_name and camera_name !='none':
                    match_data['camera_name']= camera_name
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
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
    elif request.method == 'GET':        
        try:
            dash_data =[]
            match_data =  {'analyticstype': 'PPE_TYPE1','violation_status': True,'timestamp':{'$regex': '^' + str(date.today())}}
            if camera_name and camera_name !='none':
                match_data['camera_name']=camera_name
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
                }]            
            data = list(mongo.db.data.aggregate(pipeline))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_llddetailsPPE 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- departmentdddfd_detailsPPE 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)


@violationanalysis_data.route('/department_detailsCrushHelmet', methods=['GET'])
@violationanalysis_data.route('/department_detailsCrushHelmet/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/department_detailsCrushHelmet', methods=['POST'])
def department_2detailsCrushHelmet(camera_name=None):
    ret = {'success': False, 'message':'something went wrong with department_ddfddetailsCrushHelmet details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                camera_name = jsonobject['camera_name']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': 'PPE_TYPE2','violation_status': True}
                if camera_name and camera_name !='none':
                    match_data['camera_name']=camera_name
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
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
    elif request.method == 'GET':        
        try:
            dash_data =[]
            match_data =  {'analyticstype': 'PPE_TYPE2','violation_status': True,'timestamp':{'$regex': '^' + str(date.today())}}
            if camera_name and camera_name !='none':
                match_data['camera_name']=camera_name
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
            
            data = list(mongo.db.data.aggregate(pipeline))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_ssddetailsCrushHelmet 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_ddfdetailsCrushHelmet 2", str(error), " ----time ---- ", now_time_with_time()]))    
       
    return jsonify(ret)





@violationanalysis_data.route('/camera_detailsCRDCNT', methods=['GET'])
@violationanalysis_data.route('/camera_detailsCRDCNT/<department>', methods=['GET'])
@violationanalysis_data.route('/camera_detailsCRDCNT', methods=['POST'])
def camera_id_detailsCRDCNT(department=None):
    ret = {'success': False, 'message':'something went wrong with camera_CRDCNTdetails details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department = jsonobject['department']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': 'CRDCNT','violation_status': True}
                if department and department !='none':
                    match_data['department']=department
                data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['cameraname'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':
        
        try:
            match_data =  {'analyticstype': 'CRDCNT','violation_status': True,'timestamp':{'$regex': '^' + str(date.today())}}  
            if department and department != 'none':
                match_data['department']=department          
            data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$match': match_data},
                                                 {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['cameraname'])
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_CRDCNTdetails 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_CRDCNTdetails 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)



@violationanalysis_data.route('/department_detailsCRDCNT', methods=['GET'])
@violationanalysis_data.route('/department_detailsCRDCNT/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/department_detailsCRDCNT', methods=['POST'])
def departmentdetailsCRDCNT(camera_name=None):
    ret = {'success': False, 'message':'something went wrong with department_11detailsCRDCNT details'}
    dash_data = []
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                camera_name = jsonobject['camera_name']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': 'CRDCNT','violation_status': True}
                if camera_name and camera_name !='none':
                    match_data['camera_name']=camera_name

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
                data = list(mongo.db.data.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':        
        try:
            match_data =  {'analyticstype': 'CRDCNT','violation_status': True,'timestamp':{'$regex': '^' + str(date.today())}}  
            if camera_name and camera_name !='none':
                match_data['camera_name']=camera_name
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
            data = list(mongo.db.data.aggregate(pipeline))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department11_detailsCRDCNT 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_11detailsCRDCNT 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)




@violationanalysis_data.route('/camera_detailsTC', methods=['GET'])
@violationanalysis_data.route('/camera_detailsTC/<department>', methods=['GET'])
@violationanalysis_data.route('/camera_detailsTC', methods=['POST'])
def camera_id_detailsTC(department=None):
    ret = {'success': False, 'message':'something went wrong with cameratc_details details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department = jsonobject['department']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date} }
                if department and department != 'none':
                    match_data['department']=department
                data = list(mongo.db.trafficcountdata.aggregate([{'$sort': {'timestamp': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['cameraname'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
    elif request.method == 'GET':
        try:
            match_data =  {'timestamp':{'$regex': '^' + str(date.today())}}
            if department and department != 'none':
                match_data['department']=department
            data = list(mongo.db.trafficcountdata.aggregate([{'$sort': {'timestamp': -1}},{'$match': match_data},
                                                        {'$group': {'_id': {'cameraname': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},{'$project': {'data': 0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    dash_data.append(i['_id']['cameraname'])
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera-TC_details2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- camera_TCdetails 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)




@violationanalysis_data.route('/department_detailsTC', methods=['GET'])
@violationanalysis_data.route('/department_detailsTC/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/department_detailsTC', methods=['POST'])
def department_id_detailsTC(camera_name=None):
    ret = {'success': False, 'message':'something went wrong with departmentyytdetailsTC details'}
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                dash_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                camera_name = jsonobject['camera_name']
                match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}, }
                if camera_name and camera_name !='none':
                    match_data['camera_name'] = camera_name 
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
                data = list(mongo.db.trafficcountdata.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
    elif request.method == 'GET':
        try:
            dash_data = [] 
            match_data =  {'timestamp':{'$regex': '^' + str(date.today())}}
            if camera_name and camera_name !='none':
                match_data['camera_name']=camera_name
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
            data = list(mongo.db.trafficcountdata.aggregate(pipeline))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department_22detailsTC 2", str(error), " ----time ---- ", now_time_with_time()])) 
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- department22_detailsTC 2", str(error), " ----time ---- ", now_time_with_time()]))     
    return jsonify(ret)





@violationanalysis_data.route('/violation_type_details', methods=['GET'])
def violation_type_details():
    ret = {'success': False, 'message':'something went wrong with violation type details'}
    try:
        dash_data=[]
        # dash_data =['PPE','RA','CRDCNT','TC','FIRESMOKE']
        # ret = {'success': True, 'message': dash_data}
        data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$limit': 40000},  {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data':{'$first': '$$ROOT'}}},{'$project': {'data': 0}} ]))
        dash_data = []
        if len(data) != 0:
            for count, i in enumerate(data):
                if i['_id']['analyticstype'] == 'PPE_TYPE1':
                    i['_id']['analyticstype'] = 'PPE'
                dash_data.append(i['_id']['analyticstype'])

        match_data = {'timestamp':{'$regex': '^' + str(date.today())},
                              'analyticstype': 'RA',
                              'violation_status': True,
                              'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
        tcdata = list(mongo.db.trafficcountdata.aggregate([{'$sort': {'_id': -1}},{'$limit': 1}, {'$project': {'direction': 0  ,'datauploadstatus':0,'violation_verificaton_status':0}},    ]))  
        ProtectedZonetype = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'_id': -1}},{'$limit': 40000},  {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data':{'$first': '$$ROOT'}}},{'$project': {'data': 0}} ]))
        
        
        if len(tcdata) !=0 :
            dash_data.append('TC')
        if len(ProtectedZonetype) !=0:
            dash_data.append('Protection_Zone')
        if len(dash_data    ) !=0: 
            ret = {'success': True, 'message': dash_data}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --violation_type_details--1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --violation_type_details--2", str(error), " ----time ---- ", now_time_with_time()]))    
    return jsonify(parse_json(ret))







@violationanalysis_data.route('/latest_dataPPE', methods=['GET'])
@violationanalysis_data.route('/latest_dataPPE/<cameraname>', methods=['GET'])
@violationanalysis_data.route('/latest_dataPPE/department/<department_name>', methods=['GET'])
def latest_dataPPE_(violation_type='PPE_TYPE1', camera_name=None,department_name=None):
    ret = {'success': False,'message':"something went wrong in PErsonalPRotectiveEquipment apis"}
    if 1:
        dash_data = []
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70} 
        if camera_name is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'_id': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))     
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforPPE(data[0],Foundfileterdata)
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found'
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforPPE(data[0],Foundfileterdata)
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found' 
    return jsonify(ret)
    

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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return jsonify(parse_json(ret))






@violationanalysis_data.route('/latest_dataCrushHelmet', methods=['GET'])
@violationanalysis_data.route('/latest_dataCrushHelmet/<cameraname>', methods=['GET'])
@violationanalysis_data.route('/latest_dataCrushHelmet/department/<department_name>', methods=['GET'])
def latest_dataCrushHelmet(violation_type='PPE_TYPE2', camera_name=None,department_name=None):
    ret = {'success': False,'message':"something went wrong in PErsonalPRotectiveEquipment apis"}
    if 1:
        dash_data = []
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70} 
        if camera_name is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'_id': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))     
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforCrushHelmet(data[0],Foundfileterdata)
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found'
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforCrushHelmet(data[0],Foundfileterdata)
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found' 
    return jsonify(ret)
    

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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return jsonify(parse_json(ret))



@violationanalysis_data.route('/latest_dataRA', methods=['GET'])
@violationanalysis_data.route('/latest_dataRA/<cameraname>', methods=['GET'])
@violationanalysis_data.route('/latest_dataRA/department/<department_name>', methods=['GET'])
def latest_dataRA_( violation_type='RA' ,cameraname=None,department_name=None):
    ret = {'success': False,'message':"something went wrong in RestrictedAreaLiveCount apis"}
    if 1:    
        dash_data = []
        if cameraname is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': cameraname, 'analyticstype': violation_type}# {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}
            data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                                                 {'$limit': 4000000}, {'$sort':{'data.timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforRA(data[0])
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found'
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},                                                        
                                                 {'$limit': 4000000}, {'$sort':{'data.timestamp': -1}}, {'$project': {"_id":0,'data':1,}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                count1 +=1 
                data[0]['SNo'] = count1
                wapas_data = VIolationcountforRA(data[0])
                dash_data.append(wapas_data)
                ret ={'message':parse_json(dash_data),'success':True} #all_data
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return jsonify(parse_json(ret))




@violationanalysis_data.route('/latest_dataCC', methods=['GET'])
@violationanalysis_data.route('/latest_dataCC/<camera_name>', methods=['GET'])
@violationanalysis_data.route('/latest_dataCC/department/<department_name>', methods=['GET'])
def latestdataCC(violation_type='CRDCNT', camera_name=None, department_name =None):
    ret = {'success': False,'message':"something went wrong in CrowDCountLATESTDATA apis"}
    if 1:    
        dash_data = []
        if camera_name is not None :
            match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                for index_cc , i in enumerate(data):   
                    
                    count1 +=1 
                    data[0]['SNo'] = count1
                    i['SNo'] = count1
                    if index_cc==0 :
                        dash_data.append(i)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found'
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}, 'analyticstype': violation_type}
            data = list(mongo.db.data.aggregate([{'$match': match_data},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
            if len(data) != 0:
                count1 = 0 
                for index_cc , i in enumerate(data):   
                    
                    count1 +=1 
                    data[0]['SNo'] = count1
                    i['SNo'] = count1
                    if index_cc==0 :
                        dash_data.append(i)
                ret ={'message':parse_json(dash_data),'success':True}
            else:
                ret['message'] = 'data not found'  
    return jsonify(ret)


@violationanalysis_data.route('/latest_data', methods=['GET'])
@violationanalysis_data.route('/latest_data/cameraname/<cameraname>', methods=['GET'])
@violationanalysis_data.route('/latest_data/violation_type/<violation_type>', methods=['GET'])
@violationanalysis_data.route('/latest_data/cameraname/<cameraname>/violation_type/<violation_type>', methods=['GET'])
@violationanalysis_data.route('/latest_data/<cameraname>/<violation_type>', methods=['GET'])
@violationanalysis_data.route('/latest_data/department/<department_name>', methods=['GET'])
@violationanalysis_data.route('/latest_data', methods=['POST'])
def latest_data_(violation_type=None, cameraname=None, department_name=None):
    ret = {'success': False, 'message':'something went wrong with latest data '}
    try:
        all_data = []
        list1 = []
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
        if violation_type is not None and cameraname is not None:
            if (cameraname == 'all_cameras' and violation_type == 'all_violations'):
                data = list(mongo.db.data.aggregate([{'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'camera_name': '$camera_name', 'analyticstype':'$analyticstype'}, 
                                                                                                                  'data':{'$first': '$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
            elif cameraname == 'all_cameras':
                if violation_type == 'PPE':
                    violation_type = 'PPE_TYPE1'
                match_data = {'analyticstype': violation_type}
                data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'camera_name': '$camera_name'},
                                                                                                                                          'data':{'$first': '$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
            elif violation_type == 'all_violations':
                match_data = {'camera_name': cameraname}
                data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'analyticstype': '$analyticstype'},'data':{'$first': '$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message':  parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            else:
                if violation_type == 'PPE':
                    violation_type = 'PPE_TYPE1'
                match_data = {'camera_name': cameraname, 'analyticstype':
                    violation_type}
                data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$limit': 1},
                                                      {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i)
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
        elif cameraname is not None:
            if cameraname == 'all_cameras':
                data = list(mongo.db.data.aggregate([{'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'camera_name': '$camera_name'}, 'data':{'$first':'$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
            else:
                match_data = {'camera_name': cameraname}
                data =list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$limit': 4000000},
                                                     {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i)
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
        elif violation_type is not None:
            if violation_type == 'all_violations':
                data = list(mongo.db.data.aggregate([{'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'analyticstype': '$analyticstype'}, 
                                                                                                                  'data':{'$first':'$$ROOT'}}},
                                                     {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i['data'])
                    ret = {'success': True, 'message':dash_data}
                else:
                    ret['message'] = 'data not found'
            else:
                if violation_type == 'PPE':
                    violation_type = 'PPE_TYPE1'
                match_data = {'analyticstype': violation_type}
                data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$limit': 4000000},
                                                     {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0,'violation_verificaton_status':0,'_id':0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                        if type(wapas_data) == list:
                            pass
                        elif wapas_data:
                            dash_data.append(wapas_data)
                        else:
                            dash_data.append(i)
                    ret = {'success': True, 'message': dash_data}
                else:
                    ret['message'] = 'data not found'
        else:
            data =list(mongo.db.data.aggregate([{'$sort':{'timestamp': -1}}, {'$limit': 4000000}, {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype': '$analyticstype'}, 'data':{'$first': '$$ROOT'}}},
                                                {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0,'data.violation_verificaton_status':0,'_id':0}}]))
            dash_data = []
            if len(data) != 0:
                for count, i in enumerate(data):
                    wapas_data = live_data_processing_for_dash_board(i['data'],Foundfileterdata)
                    if type(wapas_data) == list:
                        pass
                    elif wapas_data:
                        dash_data.append(wapas_data)
                    else:
                        dash_data.append(i['data'])
                ret = {'success': True, 'message': dash_data}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- latest_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return jsonify(parse_json(ret))


# def calculate_text_position(coords):
#     min_x = min(coords, key=lambda p: p[0])[0]
#     min_y = min(coords, key=lambda p: p[1])[1]
#     max_x = max(coords, key=lambda p: p[0])[0]
#     max_y = max(coords, key=lambda p: p[1])[1]
#     centroid_x = (min_x + max_x) / 2
#     centroid_y = (min_y + max_y) / 2
#     return (centroid_x, centroid_y)


# def calculate_text_size(text, font):
#     font_size = font
#     text_width = font_size * len(text) // 2  # Adjust as needed for accurate width estimation
#     text_height = font_size 
#     return text_width, text_height



# def is_point_inside_polygon(point, polygon):
#     """Check if a point is inside a polygon using the ray-casting algorithm."""
#     x, y = point
#     n = len(polygon)
#     inside = False
#     p1x, p1y = polygon[0]
#     for i in range(n + 1):
#         p2x, p2y = polygon[i % n]
#         if y > min(p1y, p2y):
#             if y <= max(p1y, p2y):
#                 if x <= max(p1x, p2x):
#                     if p1y != p2y:
#                         xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
#                     if p1x == p2x or x <= xinters:
#                         inside = not inside
#         p1x, p1y = p2x, p2y
#     return inside


# def get_text_position_within_polygon(text, polygon, font, padding=5):
#     """Calculate a valid text position within a polygon."""
#     bbox = [min(x for x, y in polygon), min(y for x, y in polygon),
#             max(x for x, y in polygon), max(y for x, y in polygon)]
#     text_width, text_height =  calculate_text_size(text, 50)
    
#     for y in range(bbox[1] + padding, bbox[3] - text_height - padding, 1):
#         for x in range(bbox[0] + padding, bbox[2] - text_width - padding, 1):
#             text_position = (x, y)
#             if is_point_inside_polygon(text_position, polygon):
#                 return text_position
    
#     # Fallback if no position is found (should be rare)
#     return (bbox[0] + padding, bbox[1] + padding)


def draw_arrow(draw, line_coords, arrow_size=20, color='blue'):
    if len(line_coords) < 4:
        print("Error: Not enough coordinates to draw a line and an arrow.")
        return
    
    # Draw the line
    draw.line(line_coords, fill=color, width=5)
    
    # Extract the end point of the line
    x1, y1 = line_coords[-2], line_coords[-1]
    x2, y2 = line_coords[-4], line_coords[-3]
    
    # Calculate direction vector
    dx, dy = x1 - x2, y1 - y2
    
    # Calculate the length of the direction vector
    length = math.sqrt(dx**2 + dy**2)
    
    # Normalize the direction vector
    if length == 0:
        return  # Avoid division by zero
    dx /= length
    dy /= length
    
    # Calculate the perpendicular vector
    perp_dx = -dy
    perp_dy = dx
    
    # Scale the perpendicular vector to the arrowhead size
    arrow_size /= 2  # Arrowhead is symmetric, so divide by 2
    arrow_point1 = (x1 - dx * arrow_size + perp_dx * arrow_size, y1 - dy * arrow_size + perp_dy * arrow_size)
    arrow_point2 = (x1 - dx * arrow_size - perp_dx * arrow_size, y1 - dy * arrow_size - perp_dy * arrow_size)
    
    # Create the arrowhead
    arrow_head = [ (x1, y1), arrow_point1, arrow_point2 ]
    
    # Draw the arrowhead
    draw.polygon(arrow_head, fill=color)

@violationanalysis_data.route('/image/<image_file>', methods=['GET'])
@violationanalysis_data.route('/image/<analyticstype>/<image_file>', methods=['GET'])
def get_img_bbox(analyticstype,image_file):
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
    # try:
    originalANaTYpe = analyticstype
    if analyticstype=='RA':
        analyticstype = 'RA'
    elif analyticstype=='PPE':
        analyticstype = 'PPE_TYPE1'
    elif analyticstype=='CRDCNT':
        analyticstype = 'CRDCNT'
    elif analyticstype == 'TRA':
        analyticstype = 'RA'
    if analyticstype is not None:
        QueryMatch = {"analyticstype":analyticstype,'imagename':{'$in': [ image_file]}}
        # print("-------------------QueryMatch--------------",QueryMatch)
        image_data = mongo.db.data.find_one(QueryMatch,sort=[('_id',  pymongo.DESCENDING)])
        # print("--------------image_data-----",image_data)
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
            CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
            if file_exists(CHECKIMAGE):
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path)
                draw = ImageDraw.Draw(source_img)
                IMage_widthscal = source_img.width
                IMage_heigthscal = source_img.height
                Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
                if Foundfileterdata  is None:
                    Foundfileterdata = {"helmet":70,"vest":70} 
                if image_data['analyticstype']=='PPE_TYPE1':
                    wapas_data = VIolationcountforPPE(image_data,Foundfileterdata)
                    if type(wapas_data) == dict:
                        image_data = image_roi_draw_data(wapas_data)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
                else:
                    image_data = image_roi_draw_data(image_data)
                if image_data['analyticstype']=="PPE": 
                    if len(image_data['object_data']) != 0:
                        try : 
                            for ___, thiru in enumerate(image_data['object_data']):
                                Vestheight , Vestwidth,Vestx_value,Vesty_value=0,0,0,0
                                Helmetheight , Helmetwidth,Helmetx_value,Helmety_value=0,0,0,0
                                if thiru['Vest']=='no_ppe':
                                    Vestheight = thiru['vest_bbox']['H']
                                    Vestwidth = thiru['vest_bbox']['W']
                                    Vestx_value = thiru['vest_bbox']['X']
                                    Vesty_value = thiru['vest_bbox']['Y']     
                                    Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                                    text_width,text_height = calculate_text_size('NO-VEST',objectfont_size)                                    
                                    text_x = Vestx_value + 6
                                    text_y = Vesty_value +(Vestheight- Vesty_value)   

                                    # text_x = Vestx_value + Vestwidth - text_width - 6 
                                    # text_y = Vesty_value + Vestheight - text_height - 6

                                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-VEST')), text_y + text_height )
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.rectangle(Vestshape, outline=vestboxcolor, width=Objectbbox_thickness)
                                    draw.text((text_x, text_y), 'NO-VEST', vestboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                if thiru['Helmet']== False:
                                    Helmetheight = thiru['helmet_bbox']['H']
                                    Helmetwidth = thiru['helmet_bbox']['W']
                                    Helmetx_value = thiru['helmet_bbox']['X']
                                    Helmety_value = thiru['helmet_bbox']['Y']
                                    # Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth - 10, Helmetheight - 10)]#(X + W, Y + H)
                                    Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth , Helmetheight )]#(X + W, Y + H)
                                    text_width,text_height = calculate_text_size("NO-HELMET",objectfont_size)
                                    ############################################# text working one ###############
                                    text_x = Helmetx_value + 5
                                    text_y = Helmety_value +(Helmetheight- Helmety_value)   
                                    # text_bg_position = (text_x - 5, text_y - 5, text_x + text_width + 10, text_y + text_height )
                                    # draw.rectangle(text_bg_position, fill='black')   
                                    draw.rectangle(Helmetshape, outline=helmetboxcolor, width=Objectbbox_thickness)
                                    #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                    #/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf
                                    draw.text((text_x, text_y), "NO-HELMET", helmetboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                                # text_bg_position = (text_x - 5, text_y - 5, text_x + text_width + 10, text_y + text_height )
                                
                                
                                if Helmetheight==0 and Helmetwidth==0  and Helmetx_value==0 and Helmety_value==0 and Vestheight ==0 and Vestwidth ==0 and Vestx_value ==0 and Vesty_value ==0:
                                    height = thiru['bbox']['H']
                                    width = thiru['bbox']['W']
                                    x_value = thiru['bbox']['X']
                                    y_value = thiru['bbox']['Y']
                                    w, h = width, height
                                    shape = [(x_value, y_value), (w - 10, h - 10)]#(X + W, Y + H)
                                    shape = [(x_value, y_value), (w , h )]#(X + W, Y + H)

                                    text_width,text_height = calculate_text_size('NO-PPE',objectfont_size)
                                    text_x = x_value + 6
                                    text_y = y_value +(height- y_value)
                                    draw.rectangle(shape, outline=helmetboxcolor, width=Objectbbox_thickness)
                                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-PPE')), text_y + text_height )
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.text((text_x, text_y), 'NO-PPE', helmetboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',objectfont_size, encoding='unic'))

                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        objectfont_size, encoding='unic'))
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                        except Exception as error :
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)

                elif image_data['analyticstype']=="PPE_TYPE2": 
                    if len(image_data['object_data']) != 0:
                        try : 
                            for ___, thiru in enumerate(image_data['object_data']):  
                                height = thiru['bbox']['H']
                                width = thiru['bbox']['W']
                                x_value = thiru['bbox']['X']
                                y_value = thiru['bbox']['Y']
                                w, h = width, height
                                shape = [(x_value, y_value), (w - 10, h - 10)]#(X + W, Y + H)
                                shape = [(x_value, y_value), (w , h )]#(X + W, Y + H)
                                text_width,text_height = calculate_text_size('BIKER',objectfont_size)
                                text_x = x_value + 6
                                text_y = y_value +(height- y_value)
                                draw.rectangle(shape, outline=bikerboxcolor, width=Objectbbox_thickness)
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-PPE')), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.text((text_x, text_y), 'BIKER', bikerboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))

                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        objectfont_size, encoding='unic'))
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                        except Exception as error :
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
                elif originalANaTYpe=="RA":
                    # print("------------entered RA----------0-",originalANaTYpe)
                    if len(image_data['object_data']) != 0:
                        ROISHAPE = image_data['analytics_data']                        
                        if 'ROI_details' in ROISHAPE:
                            if type(ROISHAPE['ROI_details']) != list :
                                for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                    if BoundingBoxValueFORROI is not None:
                                        BBOXVALUE = list(BoundingBoxValueFORROI.values())[0]
                                        polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                        bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                        # print(f'bbox_values: {bbox_values}')
                                        flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                        draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)                                        
                                        text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)                                        
                                        text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                                
                                        text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                        padding = 5
                                        text_bg_position = (
                                            text_position[0] - padding,
                                            text_position[1] - padding,
                                            text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                            text_position[1] + text_height + padding
                                        )
                                        draw.rectangle(text_bg_position, fill='black')
                                        if str(BoundingBoxValueFORROI['roi_name']) is None and str(BoundingBoxValueFORROI['roi_name'])=='':
                                            BoundingBoxValueFORROI['roi_name']='Region of interest'
                                        draw.text(text_position, str(BoundingBoxValueFORROI['roi_name']), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                        
                            else:
                                if len(ROISHAPE['ROI_details']) !=0 :
                                    for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                        if BoundingBoxValueFORROI is not None:
                                            BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                            if BBOXVALUE is not None:
                                                if 'direction_line' in BoundingBoxValueFORROI.keys():
                                                    # print('---------------BoundingBoxValueFORROI--------second--------',BoundingBoxValueFORROI)
                                                    direction_line = BoundingBoxValueFORROI['direction_line']
                                                    if direction_line is not None and direction_line=='null':
                                                        polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                        bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                        # print(f'bbox_values: {bbox_values}')
                                                        flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                                        draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                                        keys_list = list(BoundingBoxValueFORROI.keys())
                                                        coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]                                                        
                                                        text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                                        
                                                        text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                                        padding = 5
                                                        text_bg_position = (
                                                            text_position[0] - padding,
                                                            text_position[1] - padding,
                                                            text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                                            text_position[1] + text_height + padding
                                                        )                         
                                                        draw.rectangle(text_bg_position, fill='black')
                                                        keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                        if keys_list is None and keys_list=='':
                                                            keys_list='Region of interest'
                                                        draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                                else:
                                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                    # print(f'bbox_values: {bbox_values}')
                                                    flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                                    draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                                    keys_list = list(BoundingBoxValueFORROI.keys())
                                                    coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]
                                                    text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                                    
                                                    text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                                    padding = 5
                                                    text_bg_position = (
                                                        text_position[0] - padding,
                                                        text_position[1] - padding,
                                                        text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                                        text_position[1] + text_height + padding
                                                    )                                          
                                                    draw.rectangle(text_bg_position, fill='black')
                                                    keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                    if keys_list is None and keys_list=='':
                                                        keys_list='Region of interest'
                                                    draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                                        
                        
                        
                        
                        for ___, thiru in enumerate(image_data['object_data']):
                            height = thiru['bbox']['H']
                            width = thiru['bbox']['W']
                            x_value = thiru['bbox']['X']
                            y_value = thiru['bbox']['Y']
                            w, h = width, height
                            shape = [(x_value, y_value), (w - 10, h - 10)]

                            text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                            text_x = x_value + 6
                            text_y = y_value +(height- y_value)
                            # # print('-----text_y-----------',text_y)
                            # text_bg_position = (text_x - 5, text_y - 5, text_x + text_width + 10, text_y + text_height )
                            
                            if thiru['class_name']=='truck':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='car':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='bus':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='bicycle':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='person':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))

                            elif thiru['class_name']=='biker':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=bikerboxcolor, width=Objectbbox_thickness)
                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                draw.text((text_x, text_y), str(thiru['class_name']), bikerboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='rider':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            
                        imgByteArr = io.BytesIO()
                        source_img.save(imgByteArr, format='JPEG')
                        imgByteArr.seek(0)
                        return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)

                elif originalANaTYpe=="TRA":
                    if len(image_data['object_data']) != 0:
                        ROISHAPE = image_data['analytics_data']                        
                        if 'ROI_details' in ROISHAPE:
                            if type(ROISHAPE['ROI_details']) != list :
                                # print()
                                pass                                
                            elif len(ROISHAPE['ROI_details']) !=0 :
                                for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                    if BoundingBoxValueFORROI is not None:
                                        BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                        if BBOXVALUE is not None:
                                            if 'direction_line' in BoundingBoxValueFORROI.keys():
                                                # print('---------------BoundingBoxValueFORROI--------second--------',BoundingBoxValueFORROI)
                                                direction_line = BoundingBoxValueFORROI['direction_line']
                                                if direction_line is not None and direction_line!='null':
                                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                    flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                                    draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                                    keys_list = list(BoundingBoxValueFORROI.keys())
                                                    coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]
                                                    #line################################                                                        
                                                    LINEBBOX = [int(coord) for coord in direction_line.split(';') if coord.strip().isdigit()]
                                                    FinAlIneBBox = scale_polygon(LINEBBOX, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                    # Flatten the list of coordinates
                                                    GivenFlatten = [coord for point in FinAlIneBBox for coord in point]
                                                    # Ensure GivenFlatten has enough coordinates to draw lines and arrows
                                                    if len(GivenFlatten) >= 4:  # We need at least 2 points (4 coordinates) to draw a line
                                                        # Draw the line
                                                        draw.line(GivenFlatten, fill='blue', width=5)
                                                        draw_arrow(draw, GivenFlatten, arrow_size=50, color='blue')
                                                        
                                                    else:
                                                        print("Error: Not enough coordinates in GivenFlatten to draw the line or arrow.")                                               

                                                    text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                                    
                                                    text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                                    padding = 5
                                                    text_bg_position = (
                                                        text_position[0] - padding,
                                                        text_position[1] - padding,
                                                        text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                                        text_position[1] + text_height + padding
                                                    )
                                                    draw.rectangle(text_bg_position, fill='black')
                                                    keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                    if keys_list is None and keys_list=='':
                                                        keys_list='Region of interest'
                                                    draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                                    #draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))
                                            else:
                                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                                draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                                keys_list = list(BoundingBoxValueFORROI.keys())
                                                coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]  
                                                text_position = get_text_position_within_polygon(BoundingBoxValueFORROI['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                                text_width, text_height = calculate_text_size(BoundingBoxValueFORROI['roi_name'], roifont_size)
                                                padding = 5
                                                text_bg_position = (
                                                    text_position[0] - padding,
                                                    text_position[1] - padding,
                                                    text_position[0] + text_width + padding + (len(BoundingBoxValueFORROI['roi_name']) * 5),
                                                    text_position[1] + text_height + padding
                                                )
                                                draw.rectangle(text_bg_position, fill='black')
                                                keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                if keys_list is None and keys_list=='':
                                                    keys_list='Region of interest'
                                                draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                        
                        
                        
                        for ___, thiru in enumerate(image_data['object_data']):
                            height = thiru['bbox']['H']
                            width = thiru['bbox']['W']
                            x_value = thiru['bbox']['X']
                            y_value = thiru['bbox']['Y']
                            w, h = width, height
                            shape = [(x_value, y_value), (w - 10, h - 10)]

                            text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                            text_x = x_value + 6
                            text_y = y_value +(height- y_value)                            
                            if thiru['class_name']=='truck':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)
                                # truckboxcolor#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='car':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='bus':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='bicycle':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='person':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))

                            elif thiru['class_name']=='biker':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                draw.text((text_x, text_y), str(thiru['class_name']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['class_name']=='rider':
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                draw.text((text_x, text_y), str(thiru['class_name']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            
                        imgByteArr = io.BytesIO()
                        source_img.save(imgByteArr, format='JPEG')
                        imgByteArr.seek(0)
                        return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
                elif image_data['analyticstype']=="CRDCNT":
                    # print("image_data=============================",image_data)
                    if isEmpty(image_data['analytics_data']) :
                        # print("------------------------",image_data['analytics_data'])
                        CRDCNTDATA = image_data['analytics_data']
                        if CRDCNTDATA['process_on_full_frame']==0:
                            for EachREgionIndex , EachRoiVALUES in enumerate(CRDCNTDATA['data']):
                                if isEmpty(EachRoiVALUES):
                                    # print("==========EachRoiVALUES=========",EachRoiVALUES)
                                    if EachRoiVALUES is not None:
                                        BBOXVALUE = EachRoiVALUES['ROI_bbox']
                                        if BBOXVALUE is not None:
                                            polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                            bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                            # print(f'bbox_values: {bbox_values}')
                                            flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                            draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                            coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]
                                            text_position = get_text_position_within_polygon(EachRoiVALUES['ROI'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                                
                                            text_width, text_height = calculate_text_size(EachRoiVALUES['ROI'], roifont_size)
                                            padding = 5
                                            text_bg_position = (
                                                text_position[0] - padding,
                                                text_position[1] - padding,
                                                text_position[0] + text_width + padding + (len(EachRoiVALUES['ROI']) * 5),
                                                text_position[1] + text_height + padding
                                            )
                                            
                                            # Draw the background rectangle for the text
                                            draw.rectangle(text_bg_position, fill='black')
                                            keys_list = EachRoiVALUES['ROI']
                                            if keys_list is None and keys_list=='':
                                                keys_list='Crowd Count Detection'
                                            draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")


                    elif 'crowdcountdetails' in image_data:
                        if isEmpty(image_data['crowdcountdetails']):
                            CRROIDETAILS = image_data['crowdcountdetails']
                            if CRROIDETAILS:
                                if CRROIDETAILS['full_frame']==False:
                                    BBOXVALUE = CRROIDETAILS['bb_box']
                                    if BBOXVALUE is not None:
                                        polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                        bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                        flattened_bbox_values = [coord for point in bbox_values for coord in point]
                                        draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                                        coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]
                                        text_position = get_text_position_within_polygon(CRROIDETAILS['area_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))
                                        text_width, text_height = calculate_text_size(CRROIDETAILS['area_name'], roifont_size)
                                        padding = 5
                                        text_bg_position = (
                                            text_position[0] - padding,
                                            text_position[1] - padding,
                                            text_position[0] + text_width + padding + (len(CRROIDETAILS['area_name']) * 5),
                                            text_position[1] + text_height + padding
                                        )

                                        draw.rectangle(text_bg_position, fill='black')
                                        keys_list = CRROIDETAILS['area_name']
                                        if keys_list is None and keys_list=='':
                                            keys_list='Crowd count area'
                                        draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                        
                    if len(image_data['object_data']) != 0:
                        for ___, thiru in enumerate(image_data['object_data']):
                            if thiru['violation']:
                                height = thiru['bbox']['H']
                                width = thiru['bbox']['W']
                                x_value = thiru['bbox']['X']
                                y_value = thiru['bbox']['Y']
                                bbox = [(x_value, y_value), ( width, height)]
                                w, h = width, height
                                shape = [(x_value, y_value), ( width, height)]
                                text_width,text_height = calculate_text_size(thiru['class_name'],objectfont_size)
                                text_position = (x_value + 6, y_value + 2)
                                text_x = x_value + 6
                                text_y = y_value + (height-y_value)
                                text_bg_position = (text_x , text_y , text_x + text_width + 10+(len(thiru['class_name'])), text_y + text_height )
                                draw.rectangle(text_bg_position, fill='black')
                                if thiru['class_name']=='truck':
                                    draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                    #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                    draw.text((text_x, text_y), str(thiru['class_name']), truckboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                    # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['class_name']=='car':
                                    draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                    draw.text((text_x, text_y), str(thiru['class_name']), carboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                    # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['class_name']=='motorcycle' or thiru['class_name']=='motorbike':
                                    draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                    draw.text((text_x, text_y), str(thiru['class_name']), motorcycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                    # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['class_name']=='bus':
                                    draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                    draw.text((text_x, text_y), str(thiru['class_name']), busboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                    # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['class_name']=='bicycle':
                                    draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                    draw.text((text_x, text_y), str(thiru['class_name']), bicycleboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                    # draw.text((x_value + 6, y_value + 2), str(thiru['class_name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['class_name']=='person':
                                    draw.rectangle(shape, outline=personboxcolor, width=Objectbbox_thickness)
                                    # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                    draw.text((text_x, text_y), str(thiru['class_name']), personboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                                # draw.text((x_value + 6, y_value + 2), str('person'), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',        objectfont_size, encoding='unic'))
                        imgByteArr = io.BytesIO()
                        source_img.save(imgByteArr, format='JPEG')
                        imgByteArr.seek(0)
                        return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
            else:
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)
        else:
            print("image_data not found-----2--------",image_file)
            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
    else:
        print("image_data not found--------1-----",image_file)
        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        main_path = os.path.abspath(path)
        return send_from_directory(main_path, filename)
            #return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
            #return {'message': 'given image is not found', 'success': False}
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] =" ".join(["something error has occered in api", str(error)])     
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    #     return {'message': str(error), 'success': False}
    # except Exception as  error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 2", str(error), " ----time ---- ", now_time_with_time()]))     
    
        # return {'message': str(error), 'success': False}
        


@violationanalysis_data.route('/vestimage/<image_file>', methods=['GET'])
def vestimage(image_file):
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
    analyticstype = 'PPE_TYPE1'
    originalANaTYpe = analyticstype    
    if analyticstype is not None:
        QueryMatch = {"analyticstype":analyticstype,'imagename':{'$in': [ image_file]}}
        # print("-------------------QueryMatch--------------",QueryMatch)
        image_data = mongo.db.data.find_one(QueryMatch,sort=[('_id',  pymongo.DESCENDING)])
        # print("--------------image_data-----",image_data)
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
            CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
            if file_exists(CHECKIMAGE):
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path)
                draw = ImageDraw.Draw(source_img)
                IMage_widthscal = source_img.width
                IMage_heigthscal = source_img.height
                Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
                if Foundfileterdata  is None:
                    Foundfileterdata = {"helmet":70,"vest":70} 
                if image_data['analyticstype']=='PPE_TYPE1':
                    wapas_data = VIolationcountforPPE(image_data,Foundfileterdata)
                    if type(wapas_data) == dict:
                        image_data = image_roi_draw_data(wapas_data)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
                else:
                    image_data = image_roi_draw_data(image_data)
                if image_data['analyticstype']=="PPE": 
                    if len(image_data['object_data']) != 0:
                        try : 
                            for ___, thiru in enumerate(image_data['object_data']):
                                Vestheight , Vestwidth,Vestx_value,Vesty_value=0,0,0,0
                                Helmetheight , Helmetwidth,Helmetx_value,Helmety_value=0,0,0,0
                                if thiru['Vest']=='no_ppe':
                                    Vestheight = thiru['vest_bbox']['H']
                                    Vestwidth = thiru['vest_bbox']['W']
                                    Vestx_value = thiru['vest_bbox']['X']
                                    Vesty_value = thiru['vest_bbox']['Y']     
                                    Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                                    text_width,text_height = calculate_text_size('NO-VEST',objectfont_size)                                    
                                    text_x = Vestx_value + 6
                                    text_y = Vesty_value +(Vestheight- Vesty_value)
                                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-VEST')), text_y + text_height )
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.rectangle(Vestshape, outline=vestboxcolor, width=Objectbbox_thickness)
                                    draw.text((text_x, text_y), 'NO-VEST', vestboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                                
                                
                                if Helmetheight==0 and Helmetwidth==0  and Helmetx_value==0 and Helmety_value==0 and Vestheight ==0 and Vestwidth ==0 and Vestx_value ==0 and Vesty_value ==0:
                                    height = thiru['bbox']['H']
                                    width = thiru['bbox']['W']
                                    x_value = thiru['bbox']['X']
                                    y_value = thiru['bbox']['Y']
                                    w, h = width, height
                                    shape = [(x_value, y_value), (w - 10, h - 10)]#(X + W, Y + H)
                                    shape = [(x_value, y_value), (w , h )]#(X + W, Y + H)

                                    text_width,text_height = calculate_text_size('NO-PPE',objectfont_size)
                                    text_x = x_value + 6
                                    text_y = y_value +(height- y_value)
                                    draw.rectangle(shape, outline=helmetboxcolor, width=Objectbbox_thickness)
                                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-PPE')), text_y + text_height )
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.text((text_x, text_y), 'NO-PPE', helmetboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',objectfont_size, encoding='unic'))

                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        objectfont_size, encoding='unic'))
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                        except Exception as error :
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)                
            else:
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)
        else:
            print("image_data not found-----2--------",image_file)
            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
    else:
        print("image_data not found--------1-----",image_file)
        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        main_path = os.path.abspath(path)
        return send_from_directory(main_path, filename)
            #return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
            #return {'message': 'given image is not found', 'success': False}
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] =" ".join(["something error has occered in api", str(error)])     
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    #     return {'message': str(error), 'success': False}
    # except Exception as  error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 2", str(error), " ----time ---- ", now_time_with_time()]))     
    
        # return {'message': str(error), 'success': False}




@violationanalysis_data.route('/helmetimage/<image_file>', methods=['GET'])
def helmetImage(image_file):
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
    # try:
    analyticstype = 'PPE_TYPE1'
    originalANaTYpe = analyticstype
    if analyticstype is not None:
        QueryMatch = {"analyticstype":analyticstype,'imagename':{'$in': [ image_file]}}
        # print("-------------------QueryMatch--------------",QueryMatch)
        image_data = mongo.db.data.find_one(QueryMatch,sort=[('_id',  pymongo.DESCENDING)])
        # print("--------------image_data-----",image_data)
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
            CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
            if file_exists(CHECKIMAGE):
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path)
                draw = ImageDraw.Draw(source_img)
                IMage_widthscal = source_img.width
                IMage_heigthscal = source_img.height
                Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
                if Foundfileterdata  is None:
                    Foundfileterdata = {"helmet":70,"vest":70} 
                if image_data['analyticstype']=='PPE_TYPE1':
                    wapas_data = VIolationcountforPPE(image_data,Foundfileterdata)
                    if type(wapas_data) == dict:
                        image_data = image_roi_draw_data(wapas_data)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
                else:
                    image_data = image_roi_draw_data(image_data)
                if image_data['analyticstype']=="PPE": 
                    if len(image_data['object_data']) != 0:
                        try : 
                            for ___, thiru in enumerate(image_data['object_data']):
                                Vestheight , Vestwidth,Vestx_value,Vesty_value=0,0,0,0
                                Helmetheight , Helmetwidth,Helmetx_value,Helmety_value=0,0,0,0
                                if thiru['Helmet']== False:
                                    Helmetheight = thiru['helmet_bbox']['H']
                                    Helmetwidth = thiru['helmet_bbox']['W']
                                    Helmetx_value = thiru['helmet_bbox']['X']
                                    Helmety_value = thiru['helmet_bbox']['Y']
                                    Helmetshape = [(Helmetx_value, Helmety_value), (Helmetwidth , Helmetheight )]#(X + W, Y + H)
                                    text_width,text_height = calculate_text_size("NO-HELMET",objectfont_size)
                                    ############################################# text working one ###############
                                    text_x = Helmetx_value + 5
                                    text_y = Helmety_value +(Helmetheight- Helmety_value)    
                                    draw.rectangle(Helmetshape, outline=helmetboxcolor, width=Objectbbox_thickness)
                                    #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                    #/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf
                                    draw.text((text_x, text_y), "NO-HELMET", helmetboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                                # text_bg_position = (text_x - 5, text_y - 5, text_x + text_width + 10, text_y + text_height )
                                
                                
                                if Helmetheight==0 and Helmetwidth==0  and Helmetx_value==0 and Helmety_value==0 and Vestheight ==0 and Vestwidth ==0 and Vestx_value ==0 and Vesty_value ==0:
                                    height = thiru['bbox']['H']
                                    width = thiru['bbox']['W']
                                    x_value = thiru['bbox']['X']
                                    y_value = thiru['bbox']['Y']
                                    w, h = width, height
                                    shape = [(x_value, y_value), (w - 10, h - 10)]#(X + W, Y + H)
                                    shape = [(x_value, y_value), (w , h )]#(X + W, Y + H)

                                    text_width,text_height = calculate_text_size('NO-PPE',objectfont_size)
                                    text_x = x_value + 6
                                    text_y = y_value +(height- y_value)
                                    draw.rectangle(shape, outline=helmetboxcolor, width=Objectbbox_thickness)
                                    text_bg_position = (text_x , text_y , text_x + text_width + 10+(len('NO-PPE')), text_y + text_height )
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.text((text_x, text_y), 'NO-PPE', helmetboxcolor, font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',objectfont_size, encoding='unic'))

                                # draw.text((x_value + 6, y_value + 2), str(thiru['violation_count']), 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        objectfont_size, encoding='unic'))
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                        except Exception as error :
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
                    else:
                        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                        main_path = os.path.abspath(path)
                        return send_from_directory(main_path, filename)
            else:
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)
        else:
            print("image_data not found-----2--------",image_file)
            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
    else:
        print("image_data not found--------1-----",image_file)
        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        main_path = os.path.abspath(path)
        return send_from_directory(main_path, filename)
            #return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
            #return {'message': 'given image is not found', 'success': False}
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] =" ".join(["something error has occered in api", str(error)])     
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    #     return {'message': str(error), 'success': False}
    # except Exception as  error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 2", str(error), " ----time ---- ", now_time_with_time()]))     
    
        # return {'message': str(error), 'success': False}






def get_enable_list(from_date =None, to_date=None):
    dash_data=[]
    data = list(mongo.db.data.aggregate([{'$sort': {'_id': -1}},{'$limit': 40000},  {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data':{'$first': '$$ROOT'}}},{'$project': {'data': 0}} ]))
    dash_data = []
    if len(data) != 0:
        for count, i in enumerate(data):
            # if i['_id']['analyticstype'] == 'PPE_TYPE1':
            #     i['_id']['analyticstype'] = 'PPE'
            dash_data.append(i['_id']['analyticstype'])


    if from_date != None and to_date != None:
        match_data = {'timestamp': {'$gte': from_date,'$lt': to_date}, #{'$regex': '^' + str(date.today())},
            'analyticstype': 'RA',
                            'violation_status': True,
                            'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
    
        tcdata = list(mongo.db.trafficcountdata.aggregate([{'$sort': {'_id': -1}},{'$limit': 1}, {'$project': {'direction': 0  ,'datauploadstatus':0,'violation_verificaton_status':0}},    ]))  
        ProtectedZonetype = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'_id': -1}},{'$limit': 40000},  {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data':{'$first': '$$ROOT'}}},{'$project': {'data': 0}} ]))
    
    else:
        match_data = {'timestamp': {'$regex': '^' + str(date.today())},
        'analyticstype': 'RA',
                        'violation_status': True,
                        'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                        }
        tcdata = list(mongo.db.trafficcountdata.aggregate([{'$sort': {'_id': -1}},{'$limit': 1}, {'$project': {'direction': 0  ,'datauploadstatus':0,'violation_verificaton_status':0}},    ]))  
        ProtectedZonetype = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'_id': -1}},{'$limit': 40000},  {'$group': {'_id': {'analyticstype': '$analyticstype'}, 'data':{'$first': '$$ROOT'}}},{'$project': {'data': 0}} ]))

    if len(tcdata) !=0 :
        dash_data.append('TC')
    if len(ProtectedZonetype) !=0:
        dash_data.append('Protection_Zone')
    if len(dash_data ) !=0: 
        ret = {'success': True, 'message': dash_data}
    else:
        ret['message'] = 'data not found'
    return dash_data


@violationanalysis_data.route('/violation_type_list', methods=['POST'])
@violationanalysis_data.route('/violation_type_list', methods=['GET'])
def violation_type_list():
    ret = {'success': False, 'message':'something went wrong with violation type details'}
    try:
        if request.method == 'POST':
            jsonobject = request.json
            data = request.json
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        result['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        dash_data = get_enable_list(data["from_date"], data["to_date"])
                        if len(dash_data ) !=0: 
                            ret = {'success': True, 'message': dash_data}
                        else:
                            ret['message'] = 'data not found'

                else:
                    result = {'message':" ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
        else:
            dash_data = get_enable_list()
            if len(dash_data ) !=0: 
                ret = {'success': True, 'message': dash_data}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_type_details 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- violation_type_details 2", str(error), " ----time ---- ", now_time_with_time()]))    
    return jsonify(parse_json(ret))



@violationanalysis_data.route('/datewise_violation', methods=['POST'])
@violationanalysis_data.route('/datewise_violation/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewise_violation/department/<department_name>', methods=['GET'])
@violationanalysis_data.route('/datewise_violation/department/<department_name>/<pagenumber>/<page_limit>', methods=['GET'])
@violationanalysis_data.route('/datewise_violation/<cameraname>/<pagenumber>/<page_limit>',methods=['POST'])
@violationanalysis_data.route('/datewise_violation/<pagenumber>/<page_limit>', methods=['POST'])
def datewise_violation(cameraname=None, department_name=None,pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
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
                all_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                violation_type = jsonobject['violation_type']
                if violation_type is not None and cameraname is not None:
                    if violation_type == 'PPE':
                        violation_type = 'PPE_TYPE1'
                    data = list(mongo.db.data.find({'timestamp':{'$gte':from_date, '$lte': to_date}, 'camera_name':  cameraname, 'analyticstype': violation_type,'violation_status': True}
                                                   ,{   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                    if len(data) != 0:
                        dash_data = []
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
                                dash_data.append(i['data'])
                        ret = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                elif violation_type is not None:
                    if violation_type == 'PPE':
                        violation_type = 'PPE_TYPE1'
                    data = list(mongo.db.data.find({'timestamp':{'$gte':from_date, '$lte': to_date}, 'analyticstype': violation_type, 'violation_status': True}
                                                   ,{   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                    if len(data) != 0:
                        dash_data = []
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
                                dash_data.append(i['data'])
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                elif cameraname is not None:
                    data = list(mongo.db.data.find({'timestamp':{'$gte':  from_date, '$lte': to_date}, 'camera_name': cameraname, 'violation_status': True}
                                                   ,{   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                    if len(data) != 0:
                        dash_data = []
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
                                dash_data.append(i['data'])
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                else:
                    data = list(mongo.db.data.find({'timestamp':{'$gte':  from_date, '$lte': to_date}, 'violation_status': True}
                                                   ,{   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            wapas_data = live_data_processing_for_dash_board(i,Foundfileterdata)
                            if type(wapas_data) == list:
                                pass
                            elif wapas_data:
                                i = wapas_data
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                            else:
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i['data'])
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise_violation 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise_violation 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return jsonify(ret)

@violationanalysis_data.route('/datewisePPE', methods=['POST'])
@violationanalysis_data.route('/datewisePPE/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewisePPE/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewisePPE/<pagenumber>/<page_limit>', methods=['POST'])
def DATEWISEPPE(cameraname=None,pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
    # try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                department_name = None
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department_name = jsonobject['department_name']
                print("-----------------------datewisePPE----------------department_name---------------department_namedepartment_namedepartment_namedepartment_namedepartment_name",department_name)
                all_data = []
                match_data = {'timestamp': {'$gte': from_date, '$lte': to_date}, 'violation_status': True,'analyticstype': 'PPE_TYPE1'}
                # if cameraname is not None and cameraname != 'none':
                #     match_data['camera_name'] = cameraname
                # if (department_name is not None and department_name != 'none') and (cameraname is not None and cameraname != 'none') :
                if cameraname is not None and cameraname != 'none':
                    match_data['camera_name'] = cameraname
                if (department_name is not None and department_name != 'none'):
                    match_data['department'] = department_name
                    pipeline = [
                            {'$match': match_data},
                            {'$limit': 4000000},
                            {'$sort': {'timestamp': -1}},
                    ]

                    data = list(mongo.db.data.aggregate(pipeline))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = VIolationcountforPPE(i,Foundfileterdata)
                            
                            if type(i) == list:
                                pass
                            elif i:
                                if i['department']==department_name:
                                    count1 +=1
                                    i['SNo'] = count1
                                    if i['analyticstype'] == 'PPE_TYPE1':
                                        i['analyticstype'] = 'PPE'
                                
                                    dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                else:
                    if (department_name is not None and department_name != 'none') and (cameraname is not None and cameraname != 'none') :
                        match_data['department'] = department_name
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforPPE(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    if i['department']==department_name:
                                        count1 +=1
                                        i['SNo'] = count1
                                        if i['analyticstype'] == 'PPE_TYPE1':
                                            i['analyticstype'] = 'PPE'
                                    
                                        dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    elif department_name is not None and department_name != 'none'  :
                        print('---------------dajsdfjasdk department wise ppe -----------------',department_name)
                        match_data['department'] = department_name
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforPPE(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    count1 +=1
                                    i['analyticstype'] = 'PPE'
                                    dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    elif cameraname is not None and cameraname != 'none' :
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforPPE(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    count1 +=1
                                    i['SNo'] = count1
                                    i['analyticstype'] = 'PPE'                                    
                                    dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    else:
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                   
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforPPE(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    count1 +=1
                                    i['SNo'] = count1
                                    i['analyticstype'] = 'PPE'                                    
                                    dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                       
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


@violationanalysis_data.route('/datewiseCrushHelmet', methods=['POST'])
@violationanalysis_data.route('/datewiseCrushHelmet/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewiseCrushHelmet/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewiseCrushHelmet/<pagenumber>/<page_limit>', methods=['POST'])
def DatewiseCrushHelmetViolationDetails(cameraname=None,pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
    # try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                department_name = None
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department_name = jsonobject['department_name']
                print("-----------------------datewiseCrushHelmet----------------department_name---------------department_namedepartment_namedepartment_namedepartment_namedepartment_name",department_name)
                all_data = []
                match_data = {'timestamp': {'$gte': from_date, '$lte': to_date}, 'violation_status': True,'analyticstype': 'PPE_TYPE2'}
                # if cameraname is not None and cameraname != 'none':
                #     match_data['camera_name'] = cameraname
                # if (department_name is not None and department_name != 'none') and (cameraname is not None and cameraname != 'none') :
                if cameraname is not None and cameraname != 'none':
                    match_data['camera_name'] = cameraname
                if (department_name is not None and department_name != 'none'):
                    match_data['department'] = department_name
                    pipeline = [
                            {'$match': match_data},
                            {'$limit': 4000000},
                            {'$sort': {'timestamp': -1}},
                    ]

                    data = list(mongo.db.data.aggregate(pipeline))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = VIolationcountforCrushHelmet(i,Foundfileterdata)
                            
                            if type(i) == list:
                                pass
                            elif i:
                                if i['department']==department_name:
                                    count1 +=1
                                    i['SNo'] = count1
                                    # if i['analyticstype'] == 'PPE_TYPE2':
                                    #     i['analyticstype'] = 'PPE'
                                
                                    dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                else:
                    if (department_name is not None and department_name != 'none') and (cameraname is not None and cameraname != 'none') :
                        match_data['department'] = department_name
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforCrushHelmet(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    if i['department']==department_name:
                                        count1 +=1
                                        i['SNo'] = count1
                                        # if i['analyticstype'] == 'PPE_TYPE2':
                                        #     i['analyticstype'] = 'PPE'
                                    
                                        dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    elif department_name is not None and department_name != 'none'  :
                        print('---------------dajsdfjasdk department wise ppe -----------------',department_name)
                        match_data['department'] = department_name
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforCrushHelmet(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    count1 +=1
                                    #i['analyticstype'] = 'PPE'
                                    dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    elif cameraname is not None and cameraname != 'none' :
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforCrushHelmet(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    count1 +=1
                                    i['SNo'] = count1
                                    #i['analyticstype'] = 'PPE'                                    
                                    dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                        else:
                            ret = {'success': False, 'message': 'data not found'}
                    else:
                        pipeline = [
                                    {'$match': match_data},
                                    {'$limit': 4000000},
                                    {'$sort': {'timestamp': -1}},
                                   
                                ]
                        data = list(mongo.db.data.aggregate(pipeline))
                        if len(data) != 0:
                            dash_data = []
                            count1 = 0 
                            for count, i in enumerate(data):
                                i = VIolationcountforCrushHelmet(i,Foundfileterdata)
                                
                                if type(i) == list:
                                    pass
                                elif i:
                                    count1 +=1
                                    i['SNo'] = count1
                                    # i['analyticstype'] = 'PPE'                                    
                                    dash_data.append(i)
                            result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                            ret = result
                       
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

#TRUCK REVERSAL FUNCTION
@violationanalysis_data.route('/datewiseTRA', methods=['POST'])
@violationanalysis_data.route('/datewiseTRA/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewiseTRA/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewiseTRA/<pagenumber>/<page_limit>', methods=['POST'])
def DATEWISETRA(cameraname=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
    # try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                department_name = None
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department_name = jsonobject['department_name']
                all_data = []
                if (department_name is not None and department_name != 'none') and (cameraname is not None and cameraname != 'none') :
                    # match_data = {'timestamp':{'$gte': from_date, '$lte': to_date},'analyticstype': "RA", 'violation_status': True}
                    match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                        'analyticstype': "RA",
                        'violation_status': True,
                        'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                    match_data['department'] = department_name
                    
                    pipeline =[
                                {'$match': match_data},
                                # {'$sort': {'timestamp': -1, '_id': -1}},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                # {'$sort': {'_id.ticketno': -1}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000},
                                {'$project': {"_id": 0, 'data': 1}}
                            ]
                    data = list(mongo.db.data.aggregate(pipeline))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = VIolationcountforTRA(i)
                            if type(i) == list:
                                pass
                            elif i:
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                    print()
                elif (department_name is not None and department_name != 'none'):
                    # match_data = {'timestamp':{'$gte': from_date, '$lte': to_date},'analyticstype': "RA", 'violation_status': True}
                    match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                        'analyticstype': "RA",
                        'violation_status': True,
                        'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                    match_data['department'] = department_name
                    pipeline =[
                                {'$match': match_data},
                                # {'$sort': {'timestamp': -1, '_id': -1}},
                                {'$sort': {'timestamp': -1, 'ticketno': -1}},
                                {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
                                # {'$sort': {'_id.ticketno': -1}},
                                {'$sort': {'data.timestamp': -1}},
                                {'$limit': 4000000},
                                {'$project': {"_id": 0, 'data': 1}}
                            ]
                    data = list(mongo.db.data.aggregate(pipeline))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = VIolationcountforTRA(i)
                            if type(i) == list:
                                pass
                            elif i:
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                elif cameraname is not None:
                    # match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'camera_name':  cameraname,'analyticstype': "RA", 'violation_status': True}
                    match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                        'analyticstype': "RA",
                        'violation_status': True,
                        'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                    
                    data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = VIolationcountforTRA(i)
                            if type(i) == list:
                                pass
                            elif i:
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                else:
                    # match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'analyticstype': "RA", 'violation_status': True}
                    match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                        'analyticstype': "RA",
                        'violation_status': True,
                        'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                            }
                    
                    data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                                                 {'$limit': 4000000}, {'$sort':{'data.timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                                                 {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = VIolationcountforTRA(i)
                            if type(i) == list:
                                pass
                            else:
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





@violationanalysis_data.route('/datewiseTC', methods=['POST'])
@violationanalysis_data.route('/datewiseTC/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewiseTC/department/<department_name>', methods=['POST'])
@violationanalysis_data.route('/datewiseTC/department/<department_name>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewiseTC/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewiseTC/<pagenumber>/<page_limit>', methods=['POST'])
def DATEWISETC(cameraname=None, department_name=None,pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
    # try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                department_name= None
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department_name = jsonobject['department_name']
                all_data = []
                match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'violation_status': True}
                if cameraname is not None  and cameraname != 'none'  :
                    match_data['camera_name']= cameraname                
                pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                        {'$lookup': {
                            'from': 'ppera_cameras',
                            'localField': '_id',
                            'foreignField': 'cameraname',
                            'as': 'camera_data'
                        }},
                        {'$unwind': '$camera_data'},
                        {
                            '$project': {
                                '_id': 0,
                                'data': {
                                    '$map': {
                                        'input': '$data',
                                        'as': 'item',
                                        'in': {
                                            'timestamp': '$$item.timestamp',
                                            'camera_name': '$$item.camera_name',
                                            '_id': '$$item._id',
                                            'camera_rtsp': '$$item.camera_rtsp',
                                            'cameraid': '$$item.cameraid',
                                            'count': '$$item.count',
                                            'date': '$$item.date',
                                            'direction': '$$item.direction',
                                            'id_no': '$$item.id_no',
                                            'line_metadata': '$$item.line_metadata',
                                            'line_name': '$$item.line_name',
                                            'violation_status': '$$item.violation_status',
                                            'violation_verificaton_status': '$$item.violation_verificaton_status',
                                            'department': '$camera_data.department'
                                        }
                                    }
                                }
                            }
                        }
                    ]
                if department_name is not None  and department_name != 'none'   :
                    match_data['department'] = department_name
                    pipeline = [
                                {'$match': match_data},
                                {'$sort': {'timestamp': -1}},
                                {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                            ]
                    
                data = list(mongo.db.trafficcountdata.aggregate(pipeline))
                if len(data) != 0:                        
                    result = pagination_block(pagenumber, page_limit,parse_json(data))
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

@violationanalysis_data.route('/datewiseRA', methods=['POST'])
@violationanalysis_data.route('/datewiseRA/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewiseRA/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewiseRA/<pagenumber>/<page_limit>', methods=['POST'])
def DATEWISERA(cameraname=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    try:
        jsonobject = request.json or {}
        required_keys = {'from_date', 'to_date', 'department_name'}
        missing_keys = required_keys - jsonobject.keys()

        if missing_keys:
            return jsonify({'success': False, 'message': f"Missing keys: {', '.join(missing_keys)}"})

        empty_values = [key for key, value in jsonobject.items() if value == '']
        if empty_values:
            return jsonify({'success': False, 'message': f"Empty values for keys: {', '.join(empty_values)}"})

        from_date = jsonobject['from_date']
        to_date = jsonobject['to_date']
        department_name = jsonobject['department_name']
        match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                        'analyticstype': "RA",
                        'violation_status': True,
                        'object_data': {
                                '$elemMatch': {
                                'violation': True,
                                '$or': [
                                    { 'roi_details': { '$exists': False } },
                                    { 'roi_details.analytics_type': '0' }
                                ]
                                }
                                }
                            }

        if department_name and department_name != 'none':
            match_data['department'] = department_name
        if cameraname and cameraname != 'none':
            match_data['camera_name'] = cameraname

        pipeline = [
            {'$match': match_data},
            {'$sort': {'timestamp': -1, 'ticketno': -1}},
            {'$group': {'_id': {'ticketno': '$ticketno'}, 'data': {'$push': '$$ROOT'}}},
            # {'$sort': {'_id.ticketno': -1}},
            {'$sort': {'data.timestamp': -1}},
            {'$limit': 4000000},
            {'$project': {"_id": 0, 'data': 1}}
        ]

        data = list(mongo.db.data.aggregate(pipeline))

        if not data:
            return jsonify({'success': False, 'message': 'Data not found'})

        dash_data = []
        for count, item in enumerate(data, 1):
            processed_item = VIolationcountforRA(item)
            if processed_item and isinstance(processed_item, dict):
                processed_item['SNo'] = count
                dash_data.append(processed_item)

        result = pagination_block(pagenumber, page_limit, parse_json(dash_data))
        ret = result

    except (pymongo.errors.PyMongoError, Exception) as error:
        ret['message'] = str(error)

    return jsonify(ret)


@violationanalysis_data.route('/datewiseCC', methods=['POST'])
@violationanalysis_data.route('/datewiseCC/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewiseCC/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewiseCC/<pagenumber>/<page_limit>', methods=['POST'])
def DATEWISECC(cameraname=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if 1:
    # try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date','department_name']#=None,
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                department_name = None
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                department_name= jsonobject['department_name']
                all_data = []
                if (cameraname is not None and cameraname !='none') and (department_name is not None and department_name !='none') :
                    match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'camera_name':  cameraname,'analyticstype': "CRDCNT", 'violation_status': True}
                    match_data['department'] = department_name
                    # data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                    #                              {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                    #                              {'$project': {  'data.appruntime':0,
                    #                                            'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                    #                                            'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                    
                    
                    data = list(mongo.db.data.aggregate([{'$match': match_data},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            # deparFINDtment_name = None
                            # finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp'],"cameraname":i['camera_name']})
                            # if finddepartment is not None :
                            #     deparFINDtment_name = finddepartment['department']
                            # else:
                            #     finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp']})
                            #     if finddepartment is not None :
                            #         deparFINDtment_name = finddepartment['department']
                            #     else:
                            #         finddepartment = mongo.db.ppera_cameras.find_one({"cameraname":i['camera_name']})
                            #         if finddepartment is not None:
                            #             deparFINDtment_name = finddepartment['department']
                            #         else:
                            #             deparFINDtment_name= i['camera_name']
                                        
                            # i['department'] = deparFINDtment_name 
                            if i['department'] == department_name :
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                            
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                elif department_name is not None and department_name !='none':
                    match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'analyticstype': "CRDCNT", 'violation_status': True}
                    match_data['department'] = department_name
                    # data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                    #                              {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                    #                              {'$project': {  'data.appruntime':0,
                    #                                            'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                    #                                            'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                    
                    
                    data = list(mongo.db.data.aggregate([{'$match': match_data},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            # deparFINDtment_name = None
                            # finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp'],"cameraname":i['camera_name']})
                            # if finddepartment is not None :
                            #     deparFINDtment_name = finddepartment['department']
                            # else:
                            #     finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp']})
                            #     if finddepartment is not None :
                            #         deparFINDtment_name = finddepartment['department']
                            #     else:
                            #         finddepartment = mongo.db.ppera_cameras.find_one({"cameraname":i['camera_name']})
                            #         if finddepartment is not None:
                            #             deparFINDtment_name = finddepartment['department']
                            #         else:
                            #             deparFINDtment_name= i['camera_name']
                                        
                            # i['department'] = deparFINDtment_name 
                            if i['department'] == department_name :
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                elif cameraname is not None and cameraname !='none':
                    match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'camera_name':  cameraname,'analyticstype': "CRDCNT", 'violation_status': True}
                    # data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                    #                              {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                    #                              {'$project': {  'data.appruntime':0,
                    #                                            'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                    #                                            'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                    
                    
                    data = list(mongo.db.data.aggregate([{'$match': match_data},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            # deparFINDtment_name = None
                            # finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp'],"cameraname":i['camera_name']})
                            # if finddepartment is not None :
                            #     deparFINDtment_name = finddepartment['department']
                            # else:
                            #     finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp']})
                            #     if finddepartment is not None :
                            #         deparFINDtment_name = finddepartment['department']
                            #     else:
                            #         finddepartment = mongo.db.ppera_cameras.find_one({"cameraname":i['camera_name']})
                            #         if finddepartment is not None:
                            #             deparFINDtment_name = finddepartment['department']
                            #         else:
                            #             deparFINDtment_name= i['camera_name']
                                        
                            # i['department'] = deparFINDtment_name 
                            count1 +=1
                            i['SNo'] = count1
                            dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                else:
                    match_data = {'timestamp':{'$gte': from_date, '$lte': to_date}, 'analyticstype': "CRDCNT", 'violation_status': True}
                    # data = list(mongo.db.data.aggregate([{'$match': match_data},{'$group':{'_id':{'ticketno':'$ticketno'}, 'data':{'$push':'$$ROOT'}}},
                    #                              {'$limit': 4000000}, {'$sort':{'timestamp': -1}},{'$project': {"_id":0,'data':1,}},
                    #                              {'$project': {  'data.appruntime':0,
                    #                                            'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                    #                                            'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                    data = list(mongo.db.data.aggregate([{'$match': match_data},
                                                 {'$limit': 4000000}, {'$sort':{'timestamp': -1}},
                                                 {'$project': {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}}]))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            # department_name = None
                            # finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp'],"cameraname":i['camera_name']})
                            # if finddepartment is not None :
                            #     department_name = finddepartment['department']
                            # else:
                            #     finddepartment = mongo.db.ppera_cameras.find_one({'rtsp_url': i['camera_rtsp']})
                            #     if finddepartment is not None :
                            #         department_name = finddepartment['department']
                            #     else:
                            #         finddepartment = mongo.db.ppera_cameras.find_one({"cameraname":i['camera_name']})
                            #         if finddepartment is not None:
                            #             department_name = finddepartment['department']
                            #         else:
                            #             department_name= i['camera_name']
                                        
                            # i['department'] = department_name 
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


@violationanalysis_data.route('/datewise', methods=['POST'])
@violationanalysis_data.route('/datewise/<cameraname>', methods=['POST'])
@violationanalysis_data.route('/datewise/department/<department_name>', methods=['GET'])
@violationanalysis_data.route('/datewise/department/<department_name>/<pagenumber>/<page_limit>', methods=['GET'])
@violationanalysis_data.route('/datewise/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@violationanalysis_data.route('/datewise/<pagenumber>/<page_limit>', methods=['POST'])
def datewise_camera_id(cameraname=None,department_name=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    try:
        Foundfileterdata = mongo.db.filterviolations.find_one({},{'_id':0})
        if Foundfileterdata  is None:
            Foundfileterdata = {"helmet":70,"vest":70}  
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
                all_data = []
                if cameraname is not None:
                    data = list(mongo.db.data.find({'timestamp':{'$gte': from_date, '$lte': to_date}, 'camera_name':  cameraname, 'violation_status': True},
                                                   {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1),)
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = live_data_processing_for_dash_board(i,Foundfileterdata)
                            if type(i) == list:
                                pass
                            elif i:
                                count1 +=1
                                i['SNo'] = count1
                                dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
                else:
                    data =list(mongo.db.data.find({'timestamp':{'$gte': from_date, '$lte': to_date}, 'violation_status': True}
                                                  ,
                                                  {   'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}
                                                  ).sort('timestamp', -1))
                    if len(data) != 0:
                        dash_data = []
                        count1 = 0 
                        for count, i in enumerate(data):
                            i = live_data_processing_for_dash_board(i,Foundfileterdata)
                            if type(i) == list:
                                pass
                            else:
                                count1 +=1
                                i['SNo'] = count1
                                if i['analyticstype'] == 'PPE_TYPE1':
                                    i['analyticstype'] = 'PPE'
                                dash_data.append(i)
                        result = pagination_block(pagenumber, page_limit,parse_json(dash_data))
                        ret = result
                    else:
                        ret = {'success': False, 'message': 'data not found'}
        else:
            ret = {'success': False, 'message': " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise 1", str(error), " ----time ---- ", now_time_with_time()]))
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return jsonify(ret)



def sortbydepartment(department, fetcheddata ):
    all_data =[]
    for i, new in enumerate(fetcheddata):
        # print("----------------------New_----------------",new)
        if department == 'None' or department==None :
            all_data.append(new)
        else:
            try :
                if 'camera_info' in new:
                    if new['camera_info']['department']== department:
                        all_data.append(new)
                elif new['department']== department:
                    all_data.append(new)
                else:
                    all_data.append(new)

            except Exception as error :
                print("error----------------",error)
    return all_data
                


@violationanalysis_data.route('/create_violation_excelPPE', methods=['POST'])
def PPEVIOLATIONNNNNNSHEET():
    ret = {'success': False, 'message':'Something went wrong, please laterPPE try again '}
    if 1:
    # try:
        if not os.path.exists('violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("data=============create_violation_exc----elPPE==================PPE ",jsonobject)
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                cameraname = jsonobject['cameraname']
                department  = jsonobject['department']
                virtual_cameraname = cameraname
                if type(virtual_cameraname) == str:
                    virtual_cameraname.lower()
                list1 = []
                all_data = []
                if (virtual_cameraname !='none') and (virtual_cameraname !='None') and (virtual_cameraname !=None):
                    print("jsonobject---------------------------if ",virtual_cameraname)
                    if cameraname is not None :
                        if (cameraname == 'all_cameras' ):
                            match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': 'PPE_TYPE1','violation_status': True}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret['message']='data not found.'
                            else:
                                ret = {'success': False, 'message':'data not found.'}                                
                        elif cameraname is not None :
                            match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'analyticstype': 'PPE_TYPE1','violation_status': True}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))                            
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret['message']='data not found.'
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                else:
                    print("jsonobject-----------ppe excel ---",jsonobject)
                    match_data = {'timestamp':{'$gte': from_date,'$lte': to_date},'analyticstype': 'PPE_TYPE1','violation_status': True}
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},                               
                            ]
                    mongo_data = list(mongo.db.data.aggregate(pipeline))                   
                    if len(mongo_data) !=0:
                        if len(mongo_data) !=0:
                            excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                            if excel_create['success'] == True:
                                ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                            else:
                                ret = excel_create
                        else:
                            ret['message']='data not found.'
                    else:
                        ret = {'success': False, 'message':'data not found.'}
        else:
            ret['message']= " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])
                                
                    
                        
                        
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violawewewtion_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation34343_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret




@violationanalysis_data.route('/create_violation_excelCrushHelmet', methods=['POST'])
def CrushHelmetViolationReport():
    ret = {'success': False, 'message':'Something went wrong, please laterPPE try again '}
    if 1:
    # try:
        if not os.path.exists('violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname','department']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("data=============CrushHelmet================== ",jsonobject)
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                cameraname = jsonobject['cameraname']
                department  = jsonobject['department']
                virtual_cameraname = cameraname
                if type(virtual_cameraname) == str:
                    virtual_cameraname.lower()
                list1 = []
                all_data = []
                if (virtual_cameraname !='none') and (virtual_cameraname !='None') and (virtual_cameraname !=None):
                    print("jsonobject---------------------------if ",virtual_cameraname)
                    if cameraname is not None :
                        if (cameraname == 'all_cameras' ):
                            match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': 'PPE_TYPE2','violation_status': True}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret['message']='data not found.'
                            else:
                                ret = {'success': False, 'message':'data not found.'}                                
                        elif cameraname is not None :
                            match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'analyticstype': 'PPE_TYPE2','violation_status': True}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))                            
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret['message']='data not found.'
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                else:
                    print("jsonobject-----------ppe excel ---",jsonobject)
                    match_data = {'timestamp':{'$gte': from_date,'$lte': to_date},'analyticstype': 'PPE_TYPE2','violation_status': True}
                    pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},                               
                            ]
                    mongo_data = list(mongo.db.data.aggregate(pipeline))                   
                    if len(mongo_data) !=0:
                        if len(mongo_data) !=0:
                            excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                            if excel_create['success'] == True:
                                ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                            else:
                                ret = excel_create
                        else:
                            ret['message']='data not found.'
                    else:
                        ret = {'success': False, 'message':'data not found.'}
        else:
            ret['message']= " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violawewewtion_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation34343_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret


@violationanalysis_data.route('/create_violation_excelRA', methods=['POST'])
def RAVIOLATIONNNNNNSHEET():
    ret = {'success': False, 'message':'Something went wrong, please try again laterRA'}
    if 1:
    # try:
        if not os.path.exists('violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname','department']
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
                department  = jsonobject['department']
                virtual_cameraname = cameraname
                if type(virtual_cameraname) == str:
                    virtual_cameraname.lower()
                list1 = []
                all_data = []
                if (virtual_cameraname !='none'):
                    # mongo_db = mongo 
                    if cameraname is not None :
                        if (cameraname == 'all_cameras' ):
                            # match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': 'RA','violation_status': True}
                            match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                                'analyticstype': "RA",
                                'violation_status': True,
                                'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                        }
                                    }
                            # match_data = {"camera_name": 'test'}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))                            
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                        elif cameraname is not None :
                            # match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'analyticstype': 'RA','violation_status': True}
                            match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                                'analyticstype': "RA",
                                'violation_status': True,
                                'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                        }
                                    }
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                    else:
                        # match_data = {'timestamp':{'$gte': from_date,'$lte': to_date},'analyticstype': 'RA','violation_status': True}
                        match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                                'analyticstype': "RA",
                                'violation_status': True,
                                'object_data': {
                                        '$elemMatch': {
                                        'violation': True,
                                        '$or': [
                                            { 'roi_details': { '$exists': False } },
                                            { 'roi_details.analytics_type': '0' }
                                        ]
                                        }
                                        }
                                    }
                        pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},                                
                            ]                        
                        mongo_data = list(mongo.db.data.aggregate(pipeline))
                        if len(mongo_data) !=0:
                            if len(mongo_data) !=0:
                                excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation33_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation_333excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret

@violationanalysis_data.route('/create_violation_excelTRA', methods=['POST'])
def TruckreversalViolationExcel():
    ret = {'success': False, 'message':'Something went wrong, please try again laterRA'}
    if 1:
    # try:
        if not os.path.exists('violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname','department']
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
                department  = jsonobject['department']
                virtual_cameraname = cameraname
                if type(virtual_cameraname) == str:
                    virtual_cameraname.lower()
                list1 = []
                all_data = []
                if (virtual_cameraname !='none'):
                    if cameraname is not None :
                        if (cameraname == 'all_cameras' ):
                            # match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': 'RA','violation_status': True}
                            match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                                'analyticstype': "RA",
                                'violation_status': True,
                                'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                                    }
                            # match_data = {"camera_name": 'test'}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))                            
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = (TRAExcelCreation(mongo_data,from_date,to_date))
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                        elif cameraname is not None :
                            # match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'analyticstype': 'RA','violation_status': True}
                            match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                                'analyticstype': "RA",
                                'violation_status': True,
                                'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                                    }
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = (TRAExcelCreation(mongo_data,from_date,to_date))
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                    else:
                        # match_data = {'timestamp':{'$gte': from_date,'$lte': to_date},'analyticstype': 'RA','violation_status': True}
                        match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},
                                'analyticstype': "RA",
                                'violation_status': True,
                                'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }
                                    }
                        
                        pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},                                
                            ]                        
                        mongo_data = list(mongo.db.data.aggregate(pipeline))
                        if len(mongo_data) !=0:
                            if len(mongo_data) !=0:
                                excel_create = (TRAExcelCreation(mongo_data,from_date,to_date))
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation33_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation_333excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret




@violationanalysis_data.route('/create_violation_excelCRDCNT', methods=['POST'])
def crdcntVIOLATIONNNNNNSHEET():
    ret = {'success': False, 'message':'Something went wrong, please try again CRDCNTlater'}
    # if 1:
    try:
        if not os.path.exists('violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname','department']
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
                department  = jsonobject['department']
                virtual_cameraname = cameraname
                if type(virtual_cameraname) == str:
                    virtual_cameraname.lower()
                list1 = []
                all_data = []
                if (virtual_cameraname !='none'):
                    if cameraname is not None :
                        if (cameraname == 'all_cameras' ):
                            match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': 'CRDCNT','violation_status': True}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))
                            
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                        elif cameraname is not None :
                            match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'analyticstype': 'CRDCNT','violation_status': True}
                            pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                            ]
                            mongo_data = list(mongo.db.data.aggregate(pipeline))
                            if len(mongo_data) !=0:
                                if len(mongo_data) !=0:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                    if excel_create['success'] == True:
                                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                    else:
                                        ret = excel_create
                                else:
                                    ret = {'success': False, 'message':'data not found.'}
                               
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                                
                    else:
                        match_data = {'timestamp':{'$gte': from_date,'$lte': to_date},'analyticstype': 'CRDCNT','violation_status': True}
                        pipeline = [
                                {'$match': match_data},
                                {'$limit': 4000000},
                                {'$sort': {'timestamp': -1}},
                                
                            ]
                        mongo_data = list(mongo.db.data.aggregate(pipeline))
                        
                        if len(mongo_data) !=0:
                            if len(mongo_data) !=0:
                                excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                            
                        else:
                            ret = {'success': False, 'message':'data not found.'}          
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_viol33343ation_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_vi3343olation_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret

# @violationanalysis_data.route('/create_violation_excel', methods=['POST'])
# def VIOLATIONSHEET():
#     ret = {'success': False, 'message':'Something went wrong, please try again ALL TYPES'}
#     try:
#         if not os.path.exists('violation_excel_sheets'):
#             handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
#         jsonobject = request.json
#         if jsonobject == None:
#             jsonobject = {}
#         request_key_array = ['from_date', 'to_date', 'cameraname','violation_type']
#         jsonobjectarray = list(set(jsonobject))
#         missing_key = set(request_key_array).difference(jsonobjectarray)
#         if not missing_key:
#             output = [k for k, v in jsonobject.items() if v == '']
#             if output:
#                 ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
#             else:
#                 from_date = jsonobject['from_date']
#                 to_date = jsonobject['to_date']
#                 cameraname = jsonobject['cameraname']
#                 violation_type = jsonobject['violation_type']
#                 virtual_violation_type = violation_type
#                 virtual_cameraname = cameraname
#                 if type(virtual_cameraname) == str:
#                     virtual_cameraname.lower()
#                 list1 = []
#                 all_data = []
#                 if (virtual_violation_type != 'none' and virtual_cameraname !='none'):
#                     if cameraname is not None and violation_type is not None:
#                         if (cameraname == 'all_cameras' and violation_type == 'all_violations'):
#                             match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
#                             mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}},  {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
#                                                                        ,{'$project': {  'data.appruntime':0,
#                                                                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
#                                                                'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function(mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                         elif cameraname == 'all_cameras' and violation_type is not None:
#                             if violation_type == 'PPE':
#                                 violation_type = 'PPE_TYPE1'
#                             match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': violation_type, 'violation_status': True}
#                             mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push': '$$ROOT'}}}, {'$limit': 4000000}
#                                                                        ,{'$project': {  'data.appruntime':0,
#                                                                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
#                                                                'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function (mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                         elif cameraname is not None and violation_type == 'all_violations':
#                             match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True}
#                             mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000},
#                                                                        {'$project': {  'data.appruntime':0,
#                                                                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
#                                                                'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function(mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                         else:
#                             mongo_data = list(mongo.db.data.find({'timestamp':{  '$gte': from_date, '$lte': to_date},'analyticstype': violation_type,'camera_name': cameraname,'violation_status': True}
#                                                                  ,{   'appruntime':0,
#                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
#                                                                'cameraid':0,'id_no':0 ,'ticketno':0}
#                                                                  ).sort('timestamp', -1))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function(mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                     else:
#                         ret['message'] = 'Violation type or camera name is None.'
#                 elif virtual_violation_type != 'none':
#                     if violation_type is not None:
#                         if violation_type == 'all_violations':
#                             match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
#                             mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
#                                                                        ,{'$project': {  'data.appruntime':0,
#                                                                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
#                                                                'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function(mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                         elif violation_type is not None:
#                             if violation_type == 'PPE':
#                                 violation_type = 'PPE_TYPE1'
#                             mongo_data = list(mongo.db.data.find({'timestamp':{'$gte': from_date, '$lte': to_date},'analyticstype': violation_type,'violation_status': True},
#                                                                  {   'appruntime':0,
#                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
#                                                                'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function (mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                     else:
#                         ret['message'] = 'Violation type is None.'
#                 elif virtual_cameraname != 'none':
#                     if cameraname is not None:
#                         if cameraname == 'all_cameras':
#                             match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
#                             mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push': '$$ROOT' }}}, 
#                                                                        {'$limit': 4000000},
#                                                                        {'$project': {  'data.appruntime':0,
#                                                                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
#                                                                'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}
#                                                                        ]))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function(mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                         elif cameraname is not None:
#                             mongo_data = list(mongo.db.data.find({'timestamp':{  '$gte': from_date, '$lte': to_date},'camera_name': cameraname,'violation_status': True},
#                                                                  {   'appruntime':0,
#                                                                'datauploadstatus':0,'date':0,'imguploadstatus':0,
#                                                                'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
#                             if len(mongo_data) !=0:
#                                 excel_create = (creation_of_excel_function(mongo_data))
#                                 if excel_create['success'] == True:
#                                     ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                                 else:
#                                     ret = excel_create
#                             else:
#                                 ret = {'success': False, 'message':'data not found.'}
#                     else:
#                         ret['message'] = 'Camera name is None.'
#                 else:
#                     # mongo_data = list(mongo.db.data.find({'timestamp':{'$gte':from_date, '$lte': to_date}},{   'appruntime':0,
#                     #                                            'datauploadstatus':0,'date':0,'imguploadstatus':0,
#                     #                                            'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                    
                    
#                     match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}}
#                     pipeline = [
#                         {'$match': match_data},
#                         {'$sort': {'timestamp': -1}},
#                         {'$group': {
#                             '_id': {'camera_name': '$camera_name', 'analyticstype': '$analyticstype'},
#                             'data': {'$push': '$$ROOT'},
#                             'count': {'$sum': 1}
#                         }},
#                         {'$project': {
                              
#                             'data.appruntime': 0,
#                             'data.datauploadstatus': 0,
#                             'data.date': 0,
#                             'data.imguploadstatus': 0,
#                             'data.cameraid': 0,
#                             'data.id_no': 0,
#                             'data.violation_status': 0,
#                             'data.ticketno': 0
#                         }},
#                         {'$project': {
#                             'data': {
#                                 '$slice': ['$data', 2]  # Limit the array size to 2 documents
#                             },
#                             'count': 1
#                         }},
#                         {'$unwind': '$data'},
#                         {'$replaceRoot': {'newRoot': '$data'}}]
                        
#                     mongo_data = list(mongo.db.data.aggregate(pipeline))
#                     if len(mongo_data) !=0:
#                         excel_create = (creation_of_excel_function(mongo_data))
#                         if excel_create['success'] == True:
#                             ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
#                         else:
#                             ret = excel_create
#                     else:
#                         ret = {'success': False, 'message': 'data not found.'}
#     except ( 
#              pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#              pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#              pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#              pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#              pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#              pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#              pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#              pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#              pymongo.errors.WriteError) as error:
#         print("print(,)", str(error))
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation33_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
#         ret['message'] =" ".join(["something error has occered in api", str(error)])
        
#         if restart_mongodb_r_service():
#             print("mongodb restarted")
#         else:
#             if forcerestart_mongodb_r_service():
#                 print("mongodb service force restarted-")
#             else:
#                 print("mongodb service is not yet started.")
#     except Exception as  error:
#         ret = {'success': False, 'message': str(error)}
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violat33ion_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
#     return ret



@violationanalysis_data.route('/create_violation_excel', methods=['POST'])
def VIOLATIONSHEET():
    ret = {'success': False, 'message':'Something went wrong with create_violation_excel, please try again.'}
    try:
        if not os.path.exists('violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "violation_excel_sheets"))
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname', 'violation_type', 'department', 'report_template'] #, 'area_in_charge']
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
                violation_type = jsonobject['violation_type']
                department_list = jsonobject['department']
                report_template = jsonobject['report_template'] #"first"
                # if len(department) == 0:
                # area_in_charge = "Mr.Chetan Sharma" #jsonobject['area_in_charge']
                area_in_charge = "Operations: Mr. Chetan \n Mechanical: Mr. Ajit \n Electrical: Mr. Jitender" 
                virtual_violation_type = violation_type
                virtual_cameraname = cameraname
                if type(virtual_cameraname) == str:
                    virtual_cameraname.lower()
                list1 = []
                all_data = []
                excel_create = {'success': False, 'message': 'Select template and try it.'}
                if (virtual_violation_type != 'none' and virtual_cameraname != 'none'):
                    if cameraname is not None and violation_type is not None:
                        if (cameraname == 'all_cameras' and violation_type == 'all_violations'):
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
                            mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}},  {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
                                                                       ,{'$project': {'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                            if len(mongo_data) !=0:
                                if report_template == "template_1":
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))

                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}

                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}

                        elif cameraname == 'all_cameras' and violation_type is not None:
                            if violation_type == 'PPE':
                                violation_type = 'PPE_TYPE1'
                            
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': violation_type, 'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': violation_type, 'violation_status': True}
                            mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push': '$$ROOT'}}}, {'$limit': 4000000}
                                                                       ,{'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function (mongo_data))
                                if report_template == "template_1":
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))

                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                                
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                        
                        elif cameraname is not None and violation_type == 'all_violations':
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True}
                            mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000},
                                                                       {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function(mongo_data))
                                excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge,from_date,to_date))
                                if report_template == "template_1":
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))

                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create 
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                        
                        else:
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': violation_type,'camera_name': cameraname,'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{  '$gte': from_date, '$lte': to_date},'analyticstype': violation_type,'camera_name': cameraname,'violation_status': True}
                            mongo_data = list(mongo.db.data.find({'$match': match_data}, #{'timestamp':{  '$gte': from_date, '$lte': to_date},'analyticstype': violation_type,'camera_name': cameraname,'violation_status': True}
                                                                {'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}
                                                                 ).sort('timestamp', -1))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function(mongo_data))
                                if report_template == "template_1":
                                   excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))
                                
                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                    else:
                        ret['message'] = 'Violation type or camera name is None.'

                elif virtual_violation_type != 'none':
                    if violation_type is not None:
                        if violation_type == 'all_violations':
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}

                            mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
                                                                       ,{'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function(mongo_data))

                                if report_template == "template_1":
                                   excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,to_date))

                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                                print("EXCEL CREATE:-------------", excel_create)

                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}

                                else:
                                    ret = excel_create

                            else:
                                ret = {'success': False, 'message':'data not found.'}

                        elif violation_type is not None:
                            if violation_type == 'PPE':
                                violation_type = 'PPE_TYPE1'

                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'analyticstype': {"$in":violation_type}, 'violation_status': True, "department":{"$in":department_list}}
                            
                            else:
                                match_data = {'timestamp':{'$gte': from_date, '$lte': to_date},'analyticstype': {"$in":violation_type},'violation_status': True}

                             #{'timestamp':{'$gte': from_date, '$lte': to_date},'analyticstype': violation_type,'violation_status': True},
                            mongo_data = list(mongo.db.data.find(
                                    match_data,
                                    {
                                        'appruntime': 0,
                                        'datauploadstatus': 0,
                                        'date': 0,
                                        'imguploadstatus': 0,
                                        'cameraid': 0,
                                        'id_no': 0,
                                        'ticketno': 0
                                    }
                                ).sort('timestamp', -1))

                            # mongo_data = list(mongo.db.data.aggregate({'$match': match_data},
                            #                                      {'appruntime':0,
                            #                                    'datauploadstatus':0,'date':0,'imguploadstatus':0,
                            #                                    'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function (mongo_data))

                                if report_template == "template_1":
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))

                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}

                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                    else:
                        ret['message'] = 'Violation type is None.'

                elif virtual_cameraname != 'none':
                    if cameraname is not None:
                        if cameraname == 'all_cameras':
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'violation_status': True}
                            mongo_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push': '$$ROOT' }}}, 
                                                                       {'$limit': 4000000},
                                                                       {'$project': {  'data.appruntime':0,
                                                               'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                               'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}
                                                                       ]))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function(mongo_data))

                                if report_template == "template_1":
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))
                                    
                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                        elif cameraname is not None:
                            if len(department_list) != 0: 
                                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True, "department":{"$in":department_list}}
                            else:
                                match_data = {'timestamp':{  '$gte': from_date, '$lte': to_date},'camera_name': cameraname,'violation_status': True}

                            mongo_data = list(mongo.db.data.find({'$match': match_data},  #{'timestamp':{  '$gte': from_date, '$lte': to_date},'camera_name': cameraname,'violation_status': True},
                                                                 {'appruntime':0,
                                                               'datauploadstatus':0,'date':0,'imguploadstatus':0,
                                                               'cameraid':0,'id_no':0 ,'ticketno':0}).sort('timestamp', -1))
                            if len(mongo_data) !=0:
                                # excel_create = (creation_of_excel_function(mongo_data))

                                if report_template == "template_1":
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                                elif report_template == "template_2":
                                    excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                                elif report_template == "template_3":
                                    excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))
                                    
                                else:
                                    excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                                # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                                if excel_create['success'] == True:
                                    ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}

                                else:
                                    ret = excel_create 
                                    
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                    else:
                        ret['message'] = 'Camera name is None.'

                else:
                    if len(department_list) != 0: 
                        match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, "department":{"$in":department_list}}
                    else:
                        match_data = {'timestamp':{'$gte':from_date, '$lte': to_date}}

                    pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {
                            '_id': {'camera_name': '$camera_name', 'analyticstype': '$analyticstype'},
                            'data': {'$push': '$$ROOT'},
                            'count': {'$sum': 1}
                        }},
                        {'$project': {
                              
                            'data.appruntime': 0,
                            'data.datauploadstatus': 0,
                            'data.date': 0,
                            'data.imguploadstatus': 0,
                            'data.cameraid': 0,
                            'data.id_no': 0,
                            'data.violation_status': 0,
                            'data.ticketno': 0
                        }},
                        {'$project': {
                            'data': {
                                '$slice': ['$data', 2]  # Limit the array size to 2 documents
                            },
                            'count': 1
                        }},
                        {'$unwind': '$data'},
                        {'$replaceRoot': {'newRoot': '$data'}}]
                        
                    mongo_data = list(mongo.db.data.aggregate(pipeline))
                    if len(mongo_data) !=0:
                        # print("ELSE CONDITION:---------111111111111:-----",area_in_charge)
                        
                        # excel_create = (creation_of_excel_function(mongo_data))

                        if report_template == "template_1":
                            excel_create = creation_of_excel_function(mongo_data, from_date, to_date)

                        elif report_template == "template_2":
                            excel_create = (creation_CRM2_excel_function(mongo_data, area_in_charge,from_date,to_date))

                        elif report_template == "template_3":
                            excel_create = (creation_DOLVI_excel_function(mongo_data,from_date,to_date))

                        else:
                            excel_create = creation_of_excel_function(mongo_data, from_date, to_date)
                        # excel_create = (creation_CRM2_excel_function (mongo_data, area_in_charge))
                        # print("EXCEL CREATE ELSE CONDITION:----------", excel_create)
                        if excel_create['success'] == True:
                            ret = {'success': True, 'message': 'Excel sheet is created sucessfully'}
                        else:
                            ret = excel_create
                    else:
                        ret = {'success': False, 'message': 'data not found.'}
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation33_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violat33ion_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return ret



def generate_frames(rtsp):
    camera = cv2.VideoCapture(rtsp)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")    
    
@violationanalysis_data.route('/camera_liveview', methods=['GET'])
def search():
    ret = {'message':"something went wrong with camera liveview","successs":False}
    args = request.args
    if args is not None:
        rtsp = args.get("rtsp")
        if rtsp is not None:
            return Response(generate_frames(rtsp), mimetype="multipart/x-mixed-replace; boundary=frame")
        else:
            ret = {'message':"rtsp url should not be None","successs":False}
    else:
        ret = {'message':"arguments are given None","successs":False}
    return parse_json(ret)




@violationanalysis_data.route('/camera_liveview_1', methods=['GET'])
def camera_liveview_1():
    rtsp_url = request.args.get("rtsp")#query_params.get('rtsp', [])[0] if 'rtsp' in query_params else None

    if rtsp_url is None:
        return  {'message':"rtsp url should not be None","successs":False}
    return Response(generate_frames(rtsp_url), mimetype="multipart/x-mixed-replace; boundary=frame")



def creation_wheel_excel_function(list1):
    if 1:
        ret = {'success': False, 'message': 'Something went Worng with creation_wheel_excel_function'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'violation_excel_sheets' ,excel_sheet_name)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Wheel Count details')
        worksheet.set_column('A:F', 35)
        worksheet.set_row(0, 60)
        worksheet.set_row(1, 20)
        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_font_color('navy')
        cell_format.set_font_name('Calibri')
        cell_format.set_font_size(18)
        cell_format.set_align('center_across')
        worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
        #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.png'), {'x_scale': 1.2, 'y_scale':1.1})
        worksheet.write('B1', 'Wheel Count details', cell_format)
        worksheet.merge_range('B1:F1', 'Wheel Count details', cell_format)
        cell_format_1 = workbook.add_format()
        cell_format_1.set_bold()
        cell_format_1.set_font_color('white')
        cell_format_1.set_font_name('Calibri')
        cell_format_1.set_font_size(15)
        cell_format_1.set_align('center_across')
        cell_format_1.set_bg_color('#333300')
        row = 1
        col = 0
        worksheet.write(row, col, 'Sr.No', cell_format_1)
        worksheet.write(row, col + 1, 'Current Count', cell_format_1)
        worksheet.write(row, col + 2, 'Preset Count', cell_format_1)
        worksheet.write(row, col + 3, 'difference Count', cell_format_1)
        worksheet.write(row, col + 4, 'Timestamp', cell_format_1)
        worksheet.write(row, col + 5, 'Time difference in seconds', cell_format_1)        
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
        serail_number = 0   
        # for i in list1:
        for indx, i in enumerate(list1):
            # print("VALUE OF I:----------", indx)
            # try:
            serail_number+=1
            if cols == 0:
                worksheet.write(rows, cols, serail_number, cell_format_2)
            
            if cols1 == 1:
                # cell_format_2.set_text_wrap()   
                print("CURRENT COUNT:--count[wheel]", i['count']['wheel'])
                worksheet.write(rows, cols1, str(i['count']['wheel']), cell_format_2)
                
            if cols2 == 2:
                print("PRESET COUNT:--preset_value", i['preset_value'])
                worksheet.write(rows, cols2, i['preset_value'], cell_format_2)

            if cols3 == 3:
                print("Diffrence COUNT:--",  int(i['preset_value']) - i['count']['wheel'])
                worksheet.write(rows, cols3, int(i['preset_value']) - i['count']['wheel'], cell_format_2)

                # date_time = datetime.strptime(str(i['timestamp']), '%Y-%m-%d %H:%M:%S')
                # date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                # worksheet.write_datetime(rows, cols3, date_time,  date_format)
            
            if cols4 == 4:
                print("TIMESTAMP:--",  i['timestamp'])
                worksheet.write(rows, cols4,  i['timestamp'], cell_format_2)

            if cols5 == 5:
                format = "%Y-%m-%d %H:%M:%S"
                print("************DEIFFRENCE IN TIME*************", i['line_metadata'][0]['timestamp'] )
                dt1 = datetime.strptime(i['line_metadata'][0]['timestamp'], format)
                dt2 = datetime.strptime(i['line_metadata'][-1]['timestamp'], format)

                # Calculate the difference
                difference = dt2 - dt1
                difference.total_seconds()
                worksheet.write(rows, cols5, difference.total_seconds(), cell_format_2)
            rows += 1
            
        try:
            workbook.close()
            print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
            print('FileNotFoundError_count == ', FileNotFoundError_count)
            ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
        except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
            DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
            xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
            xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exc454454el_function 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel45455_function 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_exce44555l_function 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- creation_of_excel_45454function 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret



@violationanalysis_data.route('/create_wheel_count_report_excel', methods=['GET'])
def crrent_date_wheel_rotation_report():
    ret = {'success':False, 'message':'Something went wrong with create_wheel_count_report_excel, please try again.'}
    try:
        if not os.path.exists('wheel_count_violation_excel_sheets'):
            handle_uploaded_file(os.path.join(os.getcwd(), "wheel_count_violation_excel_sheets"))

        match_data = {'date':datetime.now().strftime("%Y%m%d")}
        mongo_data = list(mongo.db.wheelcount.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$limit': 4000000}
                                                    ,{'$project': {'data.appruntime':0,
                                            'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                            'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
        if len(mongo_data) !=0:
            excel_create = (creation_wheel_excel_function(mongo_data))
            
            if excel_create['success'] == True:
                ret = {'success': True, 'message': 'Excel sheet is created sucessfully', 'filename':excel_create['filename']}

            else:
                ret = excel_create
        else:
            ret = {'success': False, 'message':'data not found.'}

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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation33_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violat33ion_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    
    return ret



@violationanalysis_data.route('/create_datewise_wheel_count_excel_report', methods=['POST'])
def create_datewise_wheel_count_excel_report():
    ret = {'success':False, 'message':'Something went wrong with create_datewise_wheel_count_excel_report, please try again.'}
    try:
        request_key_array = ['from_date', 'to_date']
        jsonobject = request.json
        print("jsonobject:-----", jsonobject, jsonobject['from_date'])
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            print("1111111111111111111111111", jsonobjectarray)
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                print("222222222222222222")
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("33333333333333")
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                if not os.path.exists('wheel_count_violation_excel_sheets'):
                    print("444444444444444")
                    handle_uploaded_file(os.path.join(os.getcwd(), "wheel_count_violation_excel_sheets"))
                
                match_data = {'timestamp':{'$gte': from_date,'$lte': to_date}, 'count':{'$ne': {}}} # 'date':datetime.now().strftime("%Y%m%d")}
                mongo_data = list(mongo.db.wheelcount.aggregate([{'$match': match_data}, {'$sort':{'timestamp': -1}}, {'$limit': 4000000}
                                                            ,{'$project': {'data.appruntime':0,
                                                    'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                    'data.cameraid':0,'data.id_no':0,  'data.ticketno':0}}]))
                if len(mongo_data) !=0:
                    print("5555555555555")
                    excel_create = (creation_wheel_excel_function(mongo_data))
                    
                    if excel_create['success'] == True:
                        print("666666666666666666")
                        ret = {'success': True, 'message': 'Excel sheet is created sucessfully', 'filename':excel_create['filename']}

                    else:
                        print("777777777777")
                        ret = excel_create

                else:
                    print("There is no data between these dates")
                    ret = {'success': False, 'message':'data not found.'}
        else:
            ret = {'success': False, 'message':'data not found.'}

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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violation33_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_violat33ion_excel 2", str(error), " ----time ---- ", now_time_with_time()]))          
    
    return ret