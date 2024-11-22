from Data_recieving_and_Dashboard.packages import *
spillage = Blueprint('spillage', __name__)

    

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
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_lic---ense_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_license---_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_licens---e_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
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





@spillage.route('/add_spillage_roi', methods=['POST'])
def camera_adding_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'spillage_roi_data', 'ai_solutions']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
        else:
            id = data['id']
            roi_data = data['spillage_roi_data']
            ai_solutions = data['ai_solutions']
            print("data ====",data )
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if roi_data is not None:
                    if type(roi_data) == list:
                        if len(roi_data) != 0:
                            if 'spillage_roi_data' in finddata:
                                if roi_data != finddata['spillage_roi_data']:
                                    if ai_solutions is not None:
                                        if type(ai_solutions) == list:
                                            if len(ai_solutions) != 0:
                                                ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                                result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': roi_data,'ai_solution': ai_solutions}}))
                                                if result.modified_count > 0:
                                                    ret = {'message': 'spillage_roi_data added successfully.','success': True}
                                                else:
                                                    ret['message'] = 'spillage_roi_data not adeed.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                        elif type(ai_solutions) == dict:
                                            if isEmpty(ai_solutions) :
                                                finddata['ai_solution'].update(ai_solutions)
                                                result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': roi_data,'ai_solution': finddata['ai_solution']}}))
                                                if result.modified_count > 0:
                                                    ret = {'message': 'spillage_roi_data added successfully.','success': True}
                                                else:
                                                    ret['message'] = 'spillage_roi_data not adeed.'
                                            else:
                                                ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions, it should be list type.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions.'
                                else:
                                    ret['message'] = 'please give proper ai_solutions.'
                            else:
                                if ai_solutions is not None:
                                    if type(ai_solutions) == list:
                                        if len(ai_solutions) != 0:
                                            ai_solutions = list(set(ai_solutions).union(set(finddata['ai_solution'])))
                                            result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': roi_data,'ai_solution': ai_solutions}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'spillage_roi_data added successfully.','success': True}
                                            else:
                                                ret['message'] = 'spillage_roi_data not adeed.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                    elif type(ai_solutions) == dict:
                                        if isEmpty(ai_solutions) :
                                            finddata['ai_solution'].update(ai_solutions)
                                            result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': roi_data,'ai_solution': finddata['ai_solution']}}))
                                            if result.modified_count > 0:
                                                ret = {'message': 'spillage_roi_data added successfully.','success': True}
                                            else:
                                                ret['message'] = 'spillage_roi_data not adeed.'
                                        else:
                                            ret['message'] = 'please give proper ai_solutions, al_solutions should not None type or empty.'
                                    else:
                                        ret['message'] = 'please give proper ai_solutions, it should be list type.'
                                else:
                                    ret['message'] = 'please give proper ai_solutions.'
                        else:
                            ret['message'] = 'please give proper spillage_roi_data.'
                    else:
                        ret['message'] = 'please give proper spillage_roi_data , it should be list type.'
                else:
                    ret['message'] = 'please give proper spillage_roi_data , it should not none type.'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@spillage.route('/edit_spillage_roi', methods=['POST'])
def camera_edit_roi():
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['id', 'ai_solutions', 'spillage_roi_data','roi_id']
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
            roi_data = data['spillage_roi_data']
            finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
            if finddata is not None:
                if type(roi_data) == list:
                    if len(roi_data) != 0:
                        if isEmpty(ai_solutions):
                            fetch_roi_data = finddata['spillage_roi_data']
                            if len(fetch_roi_data) != 0:
                                if len(fetch_roi_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': roi_data, 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'spillage_roi_data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'spillage_roi_data not updated.'
                                elif len(fetch_roi_data) > 1:
                                    update_data = []
                                    if len(roi_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        for __, i in enumerate(fetch_roi_data):
                                            if int(i['roi_id']) == int(roi_data[0][ 'roi_id']):
                                                i['bb_box'] = roi_data[0]['bb_box']
                                                update_data.append(i)
                                            else:
                                                update_data.append(i)
                                        result = (mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'spillage_roi_data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'spillage_roi_data not updated.'
                                    elif len(roi_data) > 1:
                                        update_data = []
                                        finddata['ai_solution'].update(ai_solutions)
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
                                        result = (mongo.db.ppera_cameras. update_one({'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': update_data,'ai_solution': finddata['ai_solution']}}))
                                        if result.modified_count > 0:
                                            ret = {'message': 'spillage_roi_data updated successfully.','success': True}
                                        else:
                                            ret['message'] = 'spillage_roi_data not updated.'
                                    else:
                                        ret['message'] = 'There is no spillage_roi_data region the camrea, please try to add.'
                            else:
                                ret['message'] = 'There is no camrea details exist , please try to add.'
                        elif len(fetch_roi_data) != 0:
                            update_data = []
                            if len(fetch_roi_data) == 1:
                                final_ai = (set(ai_solutions).union(set (finddata['ai_solution'])))
                                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': { 'spillage_roi_data': roi_data, 'ai_solution': final_ai}})
                                if result.modified_count > 0:
                                    ret = {'message': 'spillage_roi_data updated successfully.','success': True}
                                else:
                                    ret['message'] = 'spillage_roi_data not updated.'
                            elif len(fetch_roi_data) > 1:
                                if len(roi_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(fetch_roi_data):
                                        if int(i['roi_id']) == int(roi_data[0]['roi_id']):
                                            i['bb_box'] = roi_data[0]['bb_box']
                                            update_data.append(i)
                                        else:
                                            update_data.append(i)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'spillage_roi_data  updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'spillage_roi_data not updated.'
                                elif len(roi_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
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
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'spillage_roi_data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'spillage_roi_data not updated.'
                                else:
                                    ret['message'] = 'There is no spillage_roi_data region the camrea, please try to add.'
                        else:
                            ret['message'] = 'There is no camrea details exist , please try to add.'
                    else:
                        ret['message'] = 'spillage_roi_data data should not be empty list.'
                else:
                    ret['message'] = 'spillage_roi_data  type should be list'
            else:
                ret['message'] = 'for this particular id, there is no such camera data exists.'
    else:
        ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return ret

@spillage.route('/delete_spillage_roi', methods=['POST'])
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
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                roi_id = data['roi_id']
                ai_solutions = data['ai_solutions']
                print("data ===",data)
                finddata = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if roi_id is not None:
                        if isEmpty(ai_solutions) :
                            roi_data = finddata['spillage_roi_data']
                            if len(roi_data) != 0:
                                update_data = []
                                if len(roi_data) == 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    print("finddata['ai_solution']",finddata['ai_solution'])
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': [], 'ai_solution':finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message':'spillage_roi_data delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'spillage_roi_data not deleted.'
                                elif len(roi_data) > 1:
                                    finddata['ai_solution'].update(ai_solutions)
                                    print("roi_id======================",roi_id)
                                    for __, i in enumerate(roi_data):
                                        if int(i['roi_id']) == int(roi_id):
                                            pass
                                            #roi_data.remove(i)
                                        else:
                                            update_data.append(i)
                                    print("update_data====",update_data)
                                    result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                                    if result.modified_count > 0:
                                        ret = {'message': 'spillage_roi_data  delete successfully.','success': True}
                                    else:
                                        ret['message'] = 'spillage_roi_data not deleted.'
                            else:
                                ret['message'] = 'There is no roi region the camrea, please try to add.'
                        else:
                            ret['message']='there is noooo -- --- adkkdkdk -- ------'
                            # roi_data = finddata['spillage_roi_data']
                            # if len(roi_data) != 0:
                            #     if len(roi_data) == 1:
                            #         finddata['ai_solution'].update(ai_solutions)
                            #         result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': [], 'ai_solution':finddata['ai_solution']}})
                            #         if result.modified_count > 0:
                            #             ret = {'message':'spillage_roi_ data delete successfully.','success': True}
                            #         else:
                            #             ret['message'] = 'spillage_roi_data not deleted.'
                            #     elif len(roi_data) > 1:
                            #         finddata['ai_solution'].update(ai_solutions)
                            #         for __, i in enumerate(roi_data):
                            #             if int(i['roi_id']) == int(roi_id):
                            #                 roi_data.remove(i)
                            #                 pass
                            #             else:
                            #                 update_data.append(i)
                            #         result = mongo.db.ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'spillage_roi_data': update_data,'ai_solution': finddata['ai_solution']}})
                            #         if result.modified_count > 0:
                            #             ret = {'message':'spillage_roi_data data delete successfully.','success': True}
                            #         else:
                            #             ret['message'] = 'spillage_roi_data not deleted.'
                            # else:
                            #     ret['message'] = 'There is no spillage_roi_data region the camrea, please try to add.'
                    else:
                        ret['message'] = 'please give proper spillage_roi_data , it should not none type.'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] =" ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    except Exception as error:
        ret['message'] =" ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_roi 1", str(error), " ----time ---- ", now_time_with_time()]))
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




def FETCHSPILLAGEDATAFROMMONGO():
    data = []#pictures: { $exists: true, $type: 'array', $ne: [] }
    fetch_require_data = list(mongo.db.ppera_cameras.find({'camera_status': True, "analytics_status": 'true','spillage_roi_data':{'$exists':True,"$ne": []}}))
    
    
    #print("fetch_require_data--spillage--",fetch_require_data)
    if len(fetch_require_data) != 0:
        for i in fetch_require_data:
            print("---i-----------------",i['spillage_roi_data'])
            if len(i['spillage_roi_data']) !=0:
                J={}
            # if ENABLED_SOLUTION_IS_EMPTY_DICT(J) :
                J['spillage_roi_data']=i['spillage_roi_data']
                J['cameraname']=i['cameraname']
                J['alarm_type']=i['alarm_type']
                J['alarm_ip_address']=i['alarm_ip_address']
                J['rtsp_url']=i['rtsp_url']
                data.append(J)
    return data



def SpillageCONFIG(media,data_save_interval):
    ret = {'message': 'something went wrong with create config update_cam_id__.', 'success': False}
    getdata_response = FETCHSPILLAGEDATAFROMMONGO()
    if len(getdata_response) != 0:
        function__response = WRITESPILLAGEMULTICONFIG(getdata_response,media,data_save_interval)
        return_data_update_camera ='200'
        if return_data_update_camera == '200':
            ret = { 'message': 'Spillage application is started successfully.', 'success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'please enable and add the ai analytics solutions.'
    return ret



    


@spillage.route('/start_spillage', methods=['GET'])
@spillage.route('/start_spillage', methods=['POST'])
def start_spillage():
    ret = {'message': 'something went wrong with start_spillage config.', 'success': False}
    if request.method == 'POST':
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
                common_return_data = SpillageCONFIG(media_type,data_interval)
                if common_return_data:
                    spillage_app_monitoring_started(True)
                    stop_application_for_spillageapp_creating_config()
                    if common_return_data['success'] == True:
                        spillage_app_monitoring_started(False)
                        ret = common_return_data
                    else:
                        ret['message'] = common_return_data['message']
                else:
                    ret['message'] = 'data not found to create config files.'
                        
    elif request.method == 'GET':
        media_type = 'image'
        data_interval = 10
        if media_type == 'video':
            media_type = 0
        elif media_type == 'image' :
            media_type = 1 
        else : 
            media_type = 1             
        print("media_typemedia_type",media_type)
        print("data_interval",data_interval)
        common_return_data = SpillageCONFIG(media_type,data_interval)
        if common_return_data:
            spillage_app_monitoring_started(True)
            stop_application_for_spillageapp_creating_config()
            if common_return_data['success'] == True:
                spillage_app_monitoring_started(False)
                ret = common_return_data
            else:
                ret['message'] = common_return_data['message']
        else:
            ret['message'] = 'data not found to create config files.'
        
    return ret


@spillage.route('/stop_spillageapp', methods=['GET'])
def stop_application_1_phaseoneapp():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        spillage_app_monitoring_started(True)
        # Truncatefiresmokecamera()
        ret = {'message': 'Spillage application stopped.', 'success': True}
    else:
        ret = ret
    return ret




def Spillageroi_function(x, hooter_line, index, roi_enable_cam_ids, lines):
    label_name_for_hooter =[]
    roi_label_names =[]
    if len(x['spillage_roi_data']) != 0:
        if x['alarm_type'] is not None and x['alarm_ip_address'] is not None:
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            for test_roi_ra, roi_value in enumerate(x['spillage_roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                try:
                    roi_bbox = checkNegativeValuesInBbox(roi_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_crdd_data 1", str(error), " ----time ---- ", now_time_with_time()]))
                    roi_bbox = checkNegativeValuesInBbox(roi_value['bb_box'])
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
                            [label_name_for_hooter.append(i) for i in  label_name if i not in  label_name_for_hooter]
                    else:
                        print('No label name found in roi data')
                else:
                    print('the label name type is not the list -')

                
                try :
                    if isEmpty(roi_value['alarm_type']):
                        if hooteripstring != '[' :
                            if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                                hooteripstring= hooteripstring+'['
                        
                        print("came into iiiiii====================",roi_value['alarm_type'] )
                        if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                            if isEmpty(roi_value['alarm_ip_address']):
                                if roi_value['alarm_ip_address']['hooter_ip'] is not None and roi_value['alarm_ip_address']['relay_ip'] is not None:
                                    print('---------------1',roi_value['alarm_ip_address']['hooter_ip'])
                                    print("--------------1 roi name ==", roi_name)
                                    hooteripstring=hooteripstring+roi_value['alarm_ip_address']['hooter_ip']+','+str(roi_name) +'];['+roi_value['alarm_ip_address']['relay_ip']+','+str(roi_name)+']'
                                
                        elif roi_value['alarm_type']['hooter']==True :
                            if isEmpty(roi_value['alarm_ip_address']):
                                if roi_value['alarm_ip_address']['hooter_ip'] is not None :
                                    print('---------------2',roi_value['alarm_ip_address']['hooter_ip'])
                                    print("--------------2 roi name ==", roi_name)
                                    
                                    hooteripstring=hooteripstring+roi_value['alarm_ip_address']['hooter_ip']+','+str(roi_name)+'];'
                                    
                        elif roi_value['alarm_type']['relay']==True :
                            if isEmpty(roi_value['alarm_ip_address']):
                                if roi_value['alarm_ip_address']['relay_ip'] is not None :
                                    print('--------------------3',roi_value['alarm_ip_address']['relay_ip'])
                                    print("--------------3 roi name ==", roi_name)
                                    hooteripstring=hooteripstring+roi_value['alarm_ip_address']['relay_ip']+','+str(roi_name)+'];'
                except Exception as error :
                    print("0000000000000000ERROR OF ---",error )
            hooter_empty_label_ls = []
            hooter_final_label = 'person;'
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
            print("hooter_empty_label_lshooter_empty_label_lshooter_empty_label_lshooter_empty_label_ls11==",hooter_empty_label_ls)
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            if hooteripstring== '[' :
                hooteripstring='none'
                hooter_line.append('hooter-enable = 0')
            else:
                hooter_line.append('hooter-enable = 1')
            # hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            # hooter_line.append('hooter-enable = 1')
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3\n')
        else:
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            for test_roi_ra, roi_value in enumerate(x['spillage_roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                try:
                    roi_bbox = checkNegativeValuesInBbox(roi_value['bb_box'])
                except Exception as error:
                    roi_bbox = checkNegativeValuesInBbox(roi_value['bb_box'])
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_crdd_data 2", str(error), " ----time ---- ", now_time_with_time()]))
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
                        print('No label name found in roi data')
                else:
                    print('the label name type is not the list -')

                if isEmpty(roi_value['alarm_type']):
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                    
                    print("came into iiiiii====================",roi_value['alarm_type'] )
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(roi_value['alarm_ip_address']):
                            if roi_value['alarm_ip_address']['hooter_ip'] is not None and roi_value['alarm_ip_address']['relay_ip'] is not None:
                                print('---------------1',roi_value['alarm_ip_address']['hooter_ip'])
                                print("--------------1 roi name ==", roi_name)
                                hooteripstring=hooteripstring+roi_value['alarm_ip_address']['hooter_ip']+','+str(roi_name) +'];['+roi_value['alarm_ip_address']['relay_ip']+','+str(roi_name)+']'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(roi_value['alarm_ip_address']):
                            if roi_value['alarm_ip_address']['hooter_ip'] is not None :
                                print('---------------2',roi_value['alarm_ip_address']['hooter_ip'])
                                print("--------------2 roi name ==", roi_name)
                                
                                hooteripstring=hooteripstring+roi_value['alarm_ip_address']['hooter_ip']+','+str(roi_name)+'];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(roi_value['alarm_ip_address']):
                            if roi_value['alarm_ip_address']['relay_ip'] is not None :
                                print('--------------------3',roi_value['alarm_ip_address']['relay_ip'])
                                print("--------------3 roi name ==", roi_name)
                                hooteripstring=hooteripstring+roi_value['alarm_ip_address']['relay_ip']+','+str(roi_name)+'];'
            hooter_empty_label_ls = []
            hooter_final_label = 'person;'
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
            print("hooter_empty_label_lshooter_empty_label_lshooter_empty_label_lshooter_empty_label_ls12==",hooter_empty_label_ls)
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            if hooteripstring== '[' :
                hooteripstring='none'
                hooter_line.append('hooter-enable = 0')
            else:
                hooter_line.append('hooter-enable = 1')
            # hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            # hooter_line.append('hooter-enable = 0')
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3\n')
        for test_roi_ra, roi_value in enumerate(x['spillage_roi_data']):
            label_name = roi_value['label_name']
            roi_name = roi_value['roi_name']
            try:
                roi_bbox = checkNegativeValuesInBbox(roi_value['bb_box'])
            except Exception as error:
                roi_bbox = checkNegativeValuesInBbox(roi_value['bb_box'])
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_crdd_data 3", str(error), " ----time ---- ", now_time_with_time()]))
            lines.append('[roi-filtering-stream-{0}]'.format(index))
            lines.append('enable=1')
            roi_bbox= checkNegativeValuesInBbox(roi_bbox)
            lines.append('roi-RA-{0} = {1}'.format(roi_name, roi_bbox))                        
        lines.append('inverse-roi=0')
        roi__label_names = []
        for roi_val in x['spillage_roi_data']:
            print("roi_val---",roi_val)
            for roi_val___test in roi_val['label_name']:
                roi__label_names.append(roi_val___test)
        roi_empty_label_ls = []
        for roi_label_name_test in ['0']:
            text = str(roi_label_name_test) + ';'
            roi_empty_label_ls.append(text)
        test_string = ''
        lines.append('class-id= {0}'.format(test_string.join(roi_empty_label_ls)))
    else:
        hooter_line.append('[RA{0}]'.format(str(index)))
        hooter_line.append('enable = 0')
        hooter_line.append('operate-on-label = ;')
        hooter_line.append('hooter-enable = 0')
        hooter_line.append('hooter-ip = None')
        hooter_line.append('hooter-stop-buffer-time = 3')
        hooter_line.append('data-save-time-in-sec = 3\n')
    roi_enable_cam_ids.append(index)
    return True

def WRITESPILLAGEMULTICONFIG(response,media,data_save_interval):
    allWrittenSourceCAmIds =[]
    numberofsources_= 4
    new_response = split_list(response,numberofsources_)
    camera_id =1 
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'spillageSampleconfig.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/docketrun_app_spillage'+'/configs'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)       
    remove_text_files(deepstream_config_path)  
    
    for config_index, writingresponse in enumerate(new_response):  
        config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
        config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
        lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', 'display-font-size=12', '']
        roi_enable_cam_ids = []
        cr_enable_cam_ids = []
        normal_config_file = 0
        normal_analytics_config_file = 0
        hooter_line = []   
        print("length == === ", len(writingresponse))
        for index, x in enumerate(writingresponse):
            x['cameraid'] = camera_id
            if type(x['spillage_roi_data']) == list :
                if len(x['spillage_roi_data']) != 0 :
                    print("***************111111************")
                    roi_fun_with_cr_fun = Spillageroi_function(x, hooter_line, index,roi_enable_cam_ids, lines)
                else:
                    print("asdasdfasd0000-----ddd")
        total_stream_for_stremux_union = list(set().union( roi_enable_cam_ids,cr_enable_cam_ids))
        print("roi_enable cam ids =====", roi_enable_cam_ids)
        with open(config_analytics_file, 'w') as f:
            for item in lines:
                f.write('%s\n' % item)

        lines = []
        with open(sample_config_file) as file:
            for write_config, line in enumerate(file):
                if line.strip() == '[application]':
                    lines.append('[application]')
                    lines.append('enable-perf-measurement=1')
                    lines.append('perf-measurement-interval-sec=1')

                elif line.strip() == '[tiled-display]':
                    total_stream_for_stremux_union = roi_enable_cam_ids
                    num = math.sqrt(int(len(roi_enable_cam_ids)))
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
                            if len(roi_enable_cam_ids)>3:
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
                    print("newlength===", len(writingresponse))
                    for n, x in enumerate(writingresponse):
                        cam_id = '{0}'.format(int(n))
                        roi_enable_cam_ids_exist = roi_enable_cam_ids.count(int(cam_id))
                        print("newecammeakdkkdk===", roi_enable_cam_ids_exist)
                        print("cam_idcam_idcam_id-",cam_id)
                        print("cr_enable_cam_ids-",cr_enable_cam_ids)
                        print("camera_id == 9999",camera_id)
                        print(" hello 9999",camera_id)
                        find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                        if find_data is not None:
                            if find_data['rtsp_flag'] == '1':
                                if 'rtsp' in x['rtsp_url']:
                                    x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                            
                        
                        if roi_enable_cam_ids_exist > 0:
                            print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                            print("adstatsd====", roi_enable_cam_ids)
                            print('[source{0}]'.format(normal_config_file))
                            uri = x['rtsp_url']
                            lines.append('[source{0}]'.format(normal_config_file))
                            # lines.append('enable=1')
                            # lines.append('type=4')
                            # lines.append('uri = {0}'.format(uri))
                            # lines.append('num-sources=1')
                            # lines.append('gpu-id=0')
                            # lines.append('nvbuf-memory-type=0')
                            # lines.append('latency=150')
                            # lines.append('camera-id={0}'.format(camera_id))
                            # camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                            # allWrittenSourceCAmIds.append(camera_required_data)
                            # lines.append('camera-name={0}'.format(x['cameraname']))
                            # lines.append("rtsp-reconnect-interval-sec=2")
                            # lines.append('drop-frame-interval = 1\n')
                            lines.append('enable=1')
                            lines.append('type=4')
                            lines.append('uri = {0}'.format(uri))
                            lines.append('num-sources=1')
                            lines.append('gpu-id=0')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('latency=150')
                            lines.append('camera-id={0}'.format(camera_id))
                            lines.append('smart-record=2')
                            lines.append('smart-rec-video-cache= 40')
                            lines.append('smart-rec-duration= {0}'.format(data_save_interval))
                            lines.append('smart-rec-default-duration= {0}'.format(data_save_interval))
                            # lines.append('smart-rec-duration= 60')
                            # lines.append('smart-rec-default-duration= 60')
                            lines.append('smart-rec-container= 0')
                            lines.append('smart-rec-interval= 1')
                            lines.append('smart-rec-file-prefix=sm_rec_FS_CAM')
                            lines.append('smart-rec-dir-path= images/spillage')
                            lines.append('smart-rec-start-time = 20')
                            # lines.append('smart-record=2')
                            # lines.append('smart-rec-video-cache= 40')                            
                            # lines.append('smart-rec-container= 0')
                            # lines.append('smart-rec-interval= 1')
                            # lines.append('smart-rec-file-prefix=sm_rec_FS_CAM')
                            # lines.append('smart-rec-dir-path= images/sm_rec')
                            # lines.append('smart-rec-start-time = 20')
                            camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                            allWrittenSourceCAmIds.append(camera_required_data)
                            lines.append('camera-name={0}'.format(x['cameraname']))
                            lines.append("rtsp-reconnect-interval-sec=2")
                            lines.append('drop-frame-interval = 1\n')
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
                    lines.append('enable=0')
                    lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('bbox-border-color0=0;1;0;1.0')
                    lines.append('bbox-border-color1=0;1;1;0.7')
                    lines.append('bbox-border-color2=0;1;0;0.7')
                    lines.append('bbox-border-color3=0;1;0;0.7')
                    lines.append('nvbuf-memory-type=0')
                    lines.append('interval=0')
                    lines.append('gie-unique-id=1')
                    lines.append( 'config-file = ../../models/{0}_{1}.txt'.format('test',config_index+1))     

                elif line.strip() == '[tracker]':
                    lines.append('[tracker]')

                elif line.strip() == '[nvds-analytics]':
                    lines.append('[nvds-analytics]')
                    lines.append('enable = 1')
                    lines.append('config-file = ./config_analytics_{0}.txt'.format(config_index+1))

                elif line.strip() == '[tests]':
                    lines.append('[tests]')

                elif line.strip() == '[docketrun-analytics]':
                    lines.append('[docketrun-analytics]')
                    lines.append('smart-record-stop-buffer = 2\n')

                elif line.strip() == '[docketrun-image]':
                    lines.append('[docketrun-image]')

                elif line.strip() == '[spillage]':
                    lines.append('[spillage]')
                    lines.append('process-mode = {}'.format(media))
                    lines.append('image-save-interval = {}'.format(data_save_interval))
                    lines.append('Average_area_percentage = 0.5')
                    lines.append('Frame_process_count = 10')    
                
                else:
                    lines.append(line.strip())

        

            

        with open(config_file, 'w') as f:
            for O_O_O, item in enumerate(lines):
                f.write('%s\n' % item)
    return allWrittenSourceCAmIds
    
    

@spillage.route('/getSpillageVideo/<vidoename>', methods=['GET'])
def Spillagevidoe(vidoename):
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
    
    
@spillage.route('/GETSPILLAGEIMAGE/<imagename>', methods=['GET'])
def SPILLAGEIMAGE(imagename):
    try:
        base_path = get_current_dir_and_goto_parent_dir()+'/images/spillage'
        video_path = os.path.join(base_path, imagename)
        image_data = mongo.db.spillageviolations.find_one({'video_file_name': imagename})
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
                draw.text((x_value + 6, y_value + 2), 'Spillage', 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 28,encoding='unic'))
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
                        draw.text((x_value + 6, y_value + 2),  'Spillage', 'red', font=ImageFont.truetype        ('/usr/share/fonts/truetype/freefont/FreeMono.ttf',        28, encoding='unic'))
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
    

    

@spillage.route('/DeleteSpillageViolation/<id>', methods=['GET'])
def DeleteSpillageviolation(id=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    try:
        if id is not None:
            find_data = mongo.db.spillageviolations.find_one({'_id': ObjectId(id)})
            if find_data is not None:
                result = mongo.db.spillageviolations.delete_one({'_id':ObjectId(id)})
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


@spillage.route('/Spillageverification/<id>/<flag>', methods=['GET'])
def SpillageVERIFICATIONviolation(id=None, flag=None):
    ret = {'message': 'something went wrong with violation status .','success': False}
    try:
        if id is not None:
            if flag is not None:
                if flag != 'undefined':
                    find_data = mongo.db.spillageviolations.find_one({'_id': ObjectId(id)})
                    if find_data is not None:
                        print("flag ===",flag)
                        if flag == 'false':
                            result = mongo.db.spillageviolations.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': False, 'violation_verificaton_status': True}})
                            if result.modified_count > 0:
                                ret = {'message':'violation status updated successfully.','success': True}
                            else:
                                ret = {'message':'violation status not updated .','success': False}
                        elif flag == 'true':
                            result = mongo.db.spillageviolations.update_one({'_id':ObjectId(id)}, {'$set':{'violation_status': True,  'violation_verificaton_status': True}})
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


@spillage.route('/SpillageLiveviolationdata', methods=['GET'])
@spillage.route('/SpillageLiveviolationdata/<camera_name>', methods=['GET'])
def SpillageLiveviolationdata( camera_name=None):
    ret = {'success': False,'message':"something went wrong in live_data1 apis"}
    if 1:    
        dash_data = []
        if camera_name is not None :
            match_data = {'start_time':{'$regex': '^' + str(date.today())},'camera_name': camera_name,'violation_status': True}# {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}
            data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}},
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
            data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data},  {'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}},                                                  
                                                 {'$limit': 4000000}, {'$sort':{'_id': -1}},
                                                #  {'$project': {"_id":0,'data':1,}},
                                                #  {'$project': {'data.camera_rtsp': 0,'data.appruntime':0,
                                                #                'data.datauploadstatus':0,'data.date':0,'data.imguploadstatus':0,
                                                #                'data.cameraid':0,'data.id_no':0,'data.violation_status':0,'data.ticketno':0}}
                                                 ]))
            if len(data) != 0:
                for count, i in enumerate(data):
                    # print("video_file_name----------------",i)
                    i['SNo'] = count
                    dash_data.append(i)
                ret =live_data_pagination(len(dash_data), parse_json(dash_data)) 
            else:
                ret['message'] = 'data not found'  
    return jsonify(ret)


@spillage.route('/datewiseSpillage', methods=['POST'])
@spillage.route('/datewiseSpillage/<cameraname>', methods=['POST'])
@spillage.route('/datewiseSpillage/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@spillage.route('/datewiseSpillage/<pagenumber>/<page_limit>', methods=['POST'])
def datewiseSpillage(cameraname=None, pagenumber=None, page_limit=None):
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
                    data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}}   ]))
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
                    match_data = {'start_time':{'$gte': from_date, '$lte': to_date}}
                    data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data},{'$group':{'_id':{'ticket':'$ticket'}, 'data':{'$push':'$$ROOT'}}}, ]))
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



@spillage.route('/Spillagecameradetails', methods=['GET'])
@spillage.route('/Spillagecameradetails', methods=['POST'])
def Spillagecameradetails():
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
                data = list(mongo.db.spillageviolations.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                                                    {'$project': {'data': 0}}]))
                dash_data = []
                if len(data) != 0:
                    for count, i in enumerate(data):
                        dash_data.append(i['_id']['camera_name'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found'
            
    elif request.method == 'GET':
        match_data =  {'start_time':{'$regex': '^' + str(date.today())}}
        try:
            data = list(mongo.db.spillageviolations.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
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
    #     data = list(mongo.db.spillageviolations.aggregate([{'$sort': {'start_time': -1}}, {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
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


@spillage.route('/Spillagedepartmentdetails', methods=['GET'])
@spillage.route('/Spillagedepartmentdetails', methods=['POST'])
def Spillagedepartmentdetails():
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
                dash_data = []
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
            
                data = list(mongo.db.spillageviolations.aggregate(pipeline))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        if i['department'] not in dash_data:
                            dash_data.append(i['department'])
                    ret = {'success': True, 'message': parse_json(dash_data)}
                else:
                    ret['message'] = 'data not found' 
                # data = list(mongo.db.spillageviolations.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
                #                                     {'$project': {'data': 0}}]))
                
                # if len(data) != 0:
                #     for count, i in enumerate(data):
                #         finddata = mongo.db.ppera_cameras.find_one({'cameraname': i['_id']['camera_name']})
                #         if finddata is not None :
                #             dash_data.append(finddata['department'])
                        
                #     ret = {'success': True, 'message': parse_json(dash_data)}
                # else:
                #     ret['message'] = 'data not found'
            
    elif request.method == 'GET':
        match_data =  {'start_time':{'$regex': '^' + str(date.today())}}
        dash_data = []
        try:
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
            
            data = list(mongo.db.spillageviolations.aggregate(pipeline))
            if len(data) != 0:
                for count, i in enumerate(data):
                    if i['department'] not in dash_data:
                        dash_data.append(i['department'])
                ret = {'success': True, 'message': parse_json(dash_data)}
            else:
                ret['message'] = 'data not found' 
                
            # data = list(mongo.db.spillageviolations.aggregate([{'$sort': {'start_time': -1}},{'$match': match_data},{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
            #                                         {'$project': {'data': 0}}]))
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
    # try:
    #     data = list(mongo.db.spillageviolations.aggregate([{'$sort': {'start_time': -1}}, {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$first': '$$ROOT'}}},
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


@spillage.route('/create_violation_excelSpillage', methods=['POST'])
def create_violation_excelSpillage():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        if not os.path.exists('SpillageViolationsExcel'):
            handle_uploaded_file(os.path.join(os.getcwd(), "SpillageViolationsExcel"))
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
                            mongo_data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}},  {'$group':{'_id':{'camera_name':'$camera_name'}, 'data':{'$push':'$$ROOT'}}}, {'$limit': 4000000}
                                                                       ]))
                            if len(mongo_data) !=0:
                                
                                excel_create = (CREATESPILLAGEVIOLATIONEXCEL(mongo_data))
                                if excel_create['success'] == True:
                                    ret = excel_create#{'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}                                
                        elif cameraname is not None :
                            match_data = {'start_time':{'$gte': from_date,'$lte': to_date}, 'camera_name': cameraname,'violation_status': True}
                            mongo_data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000}
                                                                       ]))
                            if len(mongo_data) !=0:
                                excel_create = (CREATESPILLAGEVIOLATIONEXCEL(mongo_data))
                                if excel_create['success'] == True:
                                    ret = excel_create#{'success': True, 'message': 'Excel sheet is created sucessfully'}
                                else:
                                    ret = excel_create
                            else:
                                ret = {'success': False, 'message':'data not found.'}
                else:
                    match_data = {'start_time':{'$gte': from_date,'$lte': to_date},'violation_status': True}
                    mongo_data = list(mongo.db.spillageviolations.aggregate([{'$match': match_data}, {'$sort':{'_id': -1}}, {'$limit': 4000000} ]))
                    if len(mongo_data) !=0:
                        print("length===========",len(mongo_data))
                        excel_create = (CREATESPILLAGEVIOLATIONEXCEL(mongo_data))
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
    img = Image.open(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'spillage', image_path))
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
        img.save(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'spillage', imagename+'_1.jpg'))
        worksheet.insert_image(row, column, os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'spillage', imagename+'_1.jpg'), {'x_scale': 0.16, 'y_scale': 0.212})
        
        # try:
        #     os.remove(os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'spillage', imagename+'_1.jpg'))
        # except Exception as error:
        #     print(f"Error removing temporary image: {error}")

def CREATESPILLAGEVIOLATIONEXCEL(list1):
    # print("list1 ===",list1)
    if 1:
    # try:
        ret = {'success': False, 'message': 'Something went Worng'}
        now = datetime.now()
        date_formats = 'dd/mm/yyyy hh:mm:ss'
        excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
        filename = os.path.join(os.getcwd() , 'SpillageViolationsExcel' ,excel_sheet_name)
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
        worksheet1 = workbook.add_worksheet('Summary Data')
        worksheet1.set_column('A:E', 30)
        worksheet1.set_row(0, 30)
        worksheet1.set_row(1, 20)
        violation_counts = Counter()
        locations = []
        x_axis_labels = []

        for row_data in list1:
            row_data['analytics_details']= 'spillage'
            row_data['location'] = row_data['camera_name']
            location = row_data.get('location', 'Unknown')
            violation = row_data.get('analytics_details', 'Unknown').strip(',')
            start_time = row_data.get('start_time', 'Unknown')
            start_time = start_time.split(' ')[0]
            key = f"{location}--{violation}--{start_time}"
            violation_counts[key] += 1

        summary_data = [{'location': key.split('--')[0], 'analytics_details': key.split('--')[1], 'start_time': key.split('--')[2], 'violation_count': count} for key, count in violation_counts.items()]

        worksheet1.write('A2', 'DATE', cell_format_7)
        worksheet1.write('B2', 'Location Details', cell_format_7)
        worksheet1.write('C2', 'Violation Type', cell_format_7)
        worksheet1.write('D2', 'Number of times', cell_format_7)

        for row_num, row_data in enumerate(summary_data, start=2):
            worksheet1.write(row_num, 0, row_data['start_time'], cell_format_2)
            worksheet1.write(row_num, 1, row_data['location'], cell_format_2)
            worksheet1.write(row_num, 2, row_data['analytics_details'], cell_format_2)
            worksheet1.write(row_num, 3, row_data['violation_count'], cell_format_2)
            x_axis_labels.append(f"{row_data['location']} - {row_data['start_time']}")
            if row_data['location'] not in locations:
                locations.append(row_data['location'])
                
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'categories': f'=Summary Data!$A$2:$A${len(x_axis_labels) + 1}',
            'values': f'=Summary Data!$D$2:$D${len(x_axis_labels) + 1}',
        })

        chart.set_x_axis({'name': 'Date and Location', 'text_axis': True, 'categories': x_axis_labels})
        chart.set_title({'name': 'Violation Counts by Location'})
        chart.set_size({'width': 720, 'height': 576})
        worksheet1.insert_chart('G2', chart)
        
        for i in list1:
            try:
                if cols == 0:
                    worksheet.write(rows, cols, i['camera_name'], cell_format_2)
                if cols1 == 1:
                    worksheet.write(rows, cols1, i['analytics_details'], cell_format_2)                    
                if cols2 == 2:
                    worksheet.write(rows, cols2, i['camera_name'], cell_format_2)
                if cols3 == 3:
                    date_time = datetime.strptime(str(i['start_time']), '%Y-%m-%d %H:%M:%S')
                    date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    worksheet.write_datetime(rows, cols3, date_time,  date_format)
                if cols4 == 4:
                    # if i['stop_time'] is not None and i['stop_time'] != 'None':
                    #     date_time = datetime.strptime(str(i['stop_time']), '%Y-%m-%d %H:%M:%S')
                    #     date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
                    #     worksheet.write_datetime(rows, cols4, date_time,  date_format)
                    # else:
                    worksheet.write(rows, cols4, "-----", cell_format_2)
                if cols5 ==5 :
                    if i['video_file_name'] is not None:
                        if  'jpg' in i['video_file_name'] :
                            verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/spillage' + '/' +i['video_file_name'] )
                            verify_img.verify()
                            worksheet.set_row(rows, 180)
                            if len(i['object_details']) !=0:
                                draw_bbox_and_insert_image(worksheet, i['video_file_name'],i['object_details'],rows,cols5)                               
                                # worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/spillage' + '/Temparary.jpg' , {'x_scale': 0.16, 'y_scale': 0.212})
                            else:
                                print("else_condition-----")
                                worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/spillage' + '/' + str(i['video_file_name']), {'x_scale': 0.16, 'y_scale': 0.212})
                                
                        
                        else:                            
                            video_file_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'spillage', i['video_file_name'])

                            worksheet.write_url(0, 0, 'external:' + video_file_path, string='Click to play video')
                            # worksheet.write_url(rows,cols5,  get_current_dir_and_goto_parent_dir() +  '/images/sm_rec' + '/' + str(i['video_file_name']), string='Click to play video')

                    else :
                        worksheet.write(rows, cols5, "-----", cell_format_2)
                rows += 1
            except UnidentifiedImageError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel1 1", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
                UnidentifiedImageError_count += 1
            except FileNotFoundError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel2 2", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
                FileNotFoundError_count += 1
            except UserWarning as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel3 3", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except ImportError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel4 4", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except xlsxwriter.exceptions.FileCreateError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel5 5", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except PermissionError as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel6 6", str(error), " ----time ---- ", now_time_with_time()]))
                ret = {'success': False, 'message': str(error)}
            except xlsxwriter.exceptions.XlsxWriterException as  error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel7 7", str(error), " ----time ---- ", now_time_with_time()]))
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
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel8 8", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except PermissionError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel9 9", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
        except AttributeError as error:
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel10 10", str(error), " ----time ---- ", now_time_with_time()]))
            ret = {'success': False, 'message': str(error)}
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel11 11", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret = {'success': False, 'message': str(error)}
    return ret




# def CREATESPILLAGEVIOLATIONEXCEL(list1):
#     # print("list1 ===",list1)
#     if 1:
#     # try:
#         ret = {'success': False, 'message': 'Something went Worng'}
#         now = datetime.now()
#         date_formats = 'dd/mm/yyyy hh:mm:ss'
#         excel_sheet_name = 'Violation_report_' + now.strftime('%m-%d-%Y-%H-%M-%S') + '.xlsx'
#         filename = os.path.join(os.getcwd() , 'SpillageViolationsExcel' ,excel_sheet_name)
#         workbook = xlsxwriter.Workbook(filename)
#         worksheet = workbook.add_worksheet('Violation Data')
#         worksheet.set_column('A:E', 30)
#         worksheet.set_column('F:F', 43)
#         worksheet.set_row(0, 100)
#         worksheet.set_row(1,  20)
#         cell_format = workbook.add_format()
#         cell_format.set_bold()
#         cell_format.set_font_color('navy')
#         cell_format.set_font_name('Calibri')
#         cell_format.set_font_size(40)
#         cell_format.set_align('center_across')
#         #worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/Docketrun_logo.jpg'), {'x_scale': 0.09, 'y_scale':0.09})
#         worksheet.insert_image('A1', os.path.join(os.getcwd() ,'smaple_files/JSW_Group_Logo.jpg'), {'x_scale': 0.4, 'y_scale':0.2})
#         worksheet.write('B1', 'Violation Data', cell_format)
#         worksheet.merge_range('B1:F1', 'Violation Details', cell_format)
#         cell_format_1 = workbook.add_format()
#         cell_format_1.set_bold()
#         cell_format_1.set_font_color('white')
#         cell_format_1.set_font_name('Calibri')
#         cell_format_1.set_font_size(18)
#         cell_format_1.set_align('center_across')
#         cell_format_1.set_bg_color('#333300')
        
        
#         cell_format_7 = workbook.add_format()
#         cell_format_7.set_bold()
#         cell_format_7.set_font_color('white')
#         cell_format_7.set_font_name('Calibri')
#         cell_format_7.set_font_size(18)
#         cell_format_7.set_align('center_across')
#         cell_format_7.set_bg_color('#800080')        
#         row = 1
#         col = 0
#         worksheet.write(row, col ,"Camera Name" , cell_format_1)
#         worksheet.write(row, col + 1, 'Violation Type', cell_format_1)
#         worksheet.write(row, col + 2, 'Location', cell_format_1)
#         worksheet.write(row, col + 3, 'Detected Time', cell_format_1)
#         worksheet.write(row, col + 4, 'Ended Time', cell_format_1)
#         worksheet.write(row, col + 5, 'Violation', cell_format_1)
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
        
#         df = pd.DataFrame(list1)
#         # df = pd.DataFrame(list1)

#         df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
#         result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
#         result_dict = {
#             'date': result_df['date'].tolist(),
#             'cameraname': result_df['camera_name'].tolist(),
#             'No of times': result_df['No of times'].tolist()
#         }
#         df = pd.DataFrame(result_dict)

#         # df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
#         # result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
#         # result_dict = {
#         #     'date': result_df['date'].tolist(),
#         #     'cameraname': result_df['camera_name'].tolist(),
#         #     'No of times': result_df['No of times'].tolist()
#         # }
#         excel_file =filename# 'grouped_column.xlsx'
#         sheet_name = 'sheet 2'

#         df.to_excel(excel_file, sheet_name=sheet_name, index=False)

#         with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
#             df.to_excel(writer, sheet_name=sheet_name, index=False)
#             workbook = writer.book
#             worksheet = writer.sheets[sheet_name]
#             worksheet.set_column("A:D", 20)
#             worksheet.merge_range('A1:D1', 'MIS-Fugitive Emission Report', workbook.add_format({
#                 'bold': True,
#                 'align': 'center',
#                 'valign': 'vcenter',
#                 'size': 14
#             }))
#             cell_format_title = workbook.add_format({
#                 'bold': True,
#                 'align': 'center',
#                 'valign': 'vcenter',
#                 'size': 18,
#                 'font_color': 'white',
#                 'font_name': 'Calibri',
#                 'bg_color': '#333300',
#                 'center_across': True
#             })

#             cell_format_column = workbook.add_format({
#                 'align': 'center',
#                 'valign': 'vcenter',
#                 'font_name': 'Calibri',
#                 'center_across': True
#             })

#             worksheet.set_row(0, 40)
#             worksheet.set_row(1, 20)

#             column_names = df.columns
#             for col_num, value in enumerate(column_names):
#                 worksheet.write(1, col_num, value, cell_format_title)

#             logo_path = 'Untitled.jpeg'
#             worksheet.insert_image('D1', logo_path, {'x_scale': 0.27, 'y_scale': 0.15, 'x_offset': 1, 'y_offset': 10, 'width': 640, 'height': 640})

#             for i, row in enumerate(df.itertuples(), 2):
#                 for col_num, value in enumerate(row[1:]): 
#                     worksheet.write(i, col_num, value, cell_format_column)

#             chart = workbook.add_chart({'type': 'column'})
#             for i, row in enumerate(df.itertuples(), 1):
#                 color = 'blue'
#                 category_label = f'{row.date} - {row.cameraname}'
#                 chart.add_series({
#                     'name': category_label,
#                     'categories': ['Sheet1', 1, 0, len(df), 0],
#                     'values': ['Sheet1', 1, i, len(df), i],
#                     'fill': {'color': color},
#                     'gap': 300,
#                     'overlap': -50,
#                 })

#             chart.set_x_axis({'name': 'Date '})
#             chart.set_y_axis({'name': 'Number of Times', 'major_gridlines': {'visible': False}})
#             chart.set_title({'name': 'Number of Times by Location and Date'})
#             chart.set_size({'width': 960, 'height': 720})
#             worksheet.insert_chart('G2', chart)
#         # worksheet1 = workbook.add_worksheet('Summary Data')
#         # worksheet1.set_column('A:E', 30)
#         # df = pd.DataFrame(list1)

#         # df['date'] = pd.to_datetime(df['start_time']).dt.strftime('%d-%m-%Y')
#         # result_df = df.groupby(['date', 'camera_name']).size().reset_index(name='No of times')
#         # result_dict = {
#         #     'date': result_df['date'].tolist(),
#         #     'cameraname': result_df['camera_name'].tolist(),
#         #     'No of times': result_df['No of times'].tolist()
#         # }
        
#         # # df.to_excel(writer, sheet_name=sheet_name, index=False)
#         # # workbook = writer.book
#         # # worksheet1 = writer.sheets[sheet_name]
#         # worksheet1.set_column("A:D", 20)
#         # worksheet1.merge_range('A1:D1', 'MIS-Fugitive Emission Report', workbook.add_format({
#         #     'bold': True,
#         #     'align': 'center',
#         #     'valign': 'vcenter',
#         #     'size': 14
#         # }))
#         # cell_format_title = workbook.add_format({
#         #     'bold': True,
#         #     'align': 'center',
#         #     'valign': 'vcenter',
#         #     'size': 18,
#         #     'font_color': 'white',
#         #     'font_name': 'Calibri',
#         #     'bg_color': '#333300',
#         #     'center_across': True
#         # })

#         # cell_format_column = workbook.add_format({
#         #     'align': 'center',
#         #     'valign': 'vcenter',
#         #     'font_name': 'Calibri',
#         #     'center_across': True
#         # })

#         # worksheet1.set_row(0, 40)
#         # worksheet1.set_row(1, 20)

#         # column_names = df.columns
#         # for col_num, value in enumerate(column_names):
#         #     worksheet1.write(1, col_num, value, cell_format_title)

#         # logo_path = 'Untitled.jpeg'
#         # worksheet1.insert_image('D1', logo_path, {'x_scale': 0.27, 'y_scale': 0.15, 'x_offset': 1, 'y_offset': 10, 'width': 640, 'height': 640})

#         # for i, row in enumerate(df.itertuples(), 2):
#         #     for col_num, value in enumerate(row[1:]): 
#         #         worksheet1.write(i, col_num, value, cell_format_column)

#         # chart = workbook.add_chart({'type': 'column'})
#         # for i, row in enumerate(df.itertuples(), 1):
#         #     color = 'blue'
#         #     category_label = f'{row.date} - {row.cameraname}'
#         #     chart.add_series({
#         #         'name': category_label,
#         #         'categories': ['Sheet1', 1, 0, len(df), 0],
#         #         'values': ['Sheet1', 1, i, len(df), i],
#         #         'fill': {'color': color},
#         #         'gap': 300,
#         #         'overlap': -50,
#         #     })

#         # chart.set_x_axis({'name': 'Date '})
#         # chart.set_y_axis({'name': 'Number of Times', 'major_gridlines': {'visible': False}})
#         # chart.set_title({'name': 'Number of Times by Location and Date'})
#         # chart.set_size({'width': 960, 'height': 720})
#         # worksheet1.insert_chart('G2', chart)
#         # worksheet1.set_row(0, 30)
#         # worksheet1.set_row(1, 20)
#         # violation_counts = Counter()
#         # locations = []
#         # x_axis_labels = []

#         # for row_data in list1:
#         #     location = row_data.get('location', 'Unknown')
#         #     violation = row_data.get('analytics_details', 'Unknown').strip(',')
#         #     start_time = row_data.get('start_time', 'Unknown')
#         #     start_time = start_time.split(' ')[0]
#         #     key = f"{location}--{violation}--{start_time}"
#         #     violation_counts[key] += 1

#         # summary_data = [{'location': key.split('--')[0], 'analytics_details': key.split('--')[1], 'start_time': key.split('--')[2], 'violation_count': count} for key, count in violation_counts.items()]

#         # worksheet1.write('A2', 'DATE', cell_format_7)
#         # worksheet1.write('B2', 'Location Details', cell_format_7)
#         # worksheet1.write('C2', 'Violation Type', cell_format_7)
#         # worksheet1.write('D2', 'Number of times', cell_format_7)

#         # for row_num, row_data in enumerate(summary_data, start=2):
#         #     worksheet1.write(row_num, 0, row_data['start_time'], cell_format_2)
#         #     worksheet1.write(row_num, 1, row_data['location'], cell_format_2)
#         #     worksheet1.write(row_num, 2, row_data['analytics_details'], cell_format_2)
#         #     worksheet1.write(row_num, 3, row_data['violation_count'], cell_format_2)
#         #     x_axis_labels.append(f"{row_data['location']} - {row_data['start_time']}")
#         #     if row_data['location'] not in locations:
#         #         locations.append(row_data['location'])
                
#         # chart = workbook.add_chart({'type': 'column'})
#         # chart.add_series({
#         #     'categories': f'=Summary Data!$A$2:$A${len(x_axis_labels) + 1}',
#         #     'values': f'=Summary Data!$D$2:$D${len(x_axis_labels) + 1}',
#         # })

#         # chart.set_x_axis({'name': 'Date and Location', 'text_axis': True, 'categories': x_axis_labels})
#         # chart.set_title({'name': 'Violation Counts by Location'})
#         # chart.set_size({'width': 720, 'height': 576})
#         # worksheet1.insert_chart('G2', chart)
        
#         for i in list1:
#             try:
#                 if cols == 0:
#                     worksheet.write(rows, cols, i['camera_name'], cell_format_2)
#                 if cols1 == 1:
#                     worksheet.write(rows, cols1, i['analytics_details'], cell_format_2)                    
#                 if cols2 == 2:
#                     worksheet.write(rows, cols2, i['location'], cell_format_2)
#                 if cols3 == 3:
#                     date_time = datetime.strptime(str(i['start_time']), '%Y-%m-%d %H:%M:%S')
#                     date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
#                     worksheet.write_datetime(rows, cols3, date_time,  date_format)
#                 if cols4 == 4:
#                     if i['stop_time'] is not None and i['stop_time'] != 'None':
#                         date_time = datetime.strptime(str(i['stop_time']), '%Y-%m-%d %H:%M:%S')
#                         date_format = workbook.add_format({'num_format': date_formats, 'align': 'center'})
#                         worksheet.write_datetime(rows, cols4, date_time,  date_format)
#                     else:
#                         worksheet.write(rows, cols4, "-----", cell_format_2)
#                 if cols5 ==5 :
#                     if i['video_file_name'] is not None:
#                         if  'jpg' in i['video_file_name'] :
#                             verify_img = Image.open(get_current_dir_and_goto_parent_dir() +  '/images/spillage' + '/' +i['video_file_name'] )
#                             verify_img.verify()
#                             worksheet.set_row(rows, 180)
#                             if len(i['object_details']) !=0:
#                                 draw_bbox_and_insert_image(worksheet, i['video_file_name'],i['object_details'],rows,cols5)                               
#                                 # worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/spillage' + '/Temparary.jpg' , {'x_scale': 0.16, 'y_scale': 0.212})
#                             else:
#                                 print("else_condition-----")
#                                 worksheet.insert_image(rows, cols5,get_current_dir_and_goto_parent_dir() +  '/images/spillage' + '/' + str(i['video_file_name']), {'x_scale': 0.16, 'y_scale': 0.212})
                                
                        
#                         else:
                            
#                             video_file_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'images', 'sm_rec', i['video_file_name'])

#                             worksheet.write_url(0, 0, 'external:' + video_file_path, string='Click to play video')
#                             # worksheet.write_url(rows,cols5,  get_current_dir_and_goto_parent_dir() +  '/images/sm_rec' + '/' + str(i['video_file_name']), string='Click to play video')

#                     else :
#                         worksheet.write(rows, cols5, "-----", cell_format_2)
#                 rows += 1
#             except UnidentifiedImageError as error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel12 1", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#                 UnidentifiedImageError_count += 1
#             except FileNotFoundError as error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel13 2", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#                 FileNotFoundError_count += 1
#             except UserWarning as error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel14 3", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#             except ImportError as error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel15 4", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#             except xlsxwriter.exceptions.FileCreateError as error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel16 5", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#             except PermissionError as error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel17 6", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#             except xlsxwriter.exceptions.XlsxWriterException as  error:
#                 ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel18 7", str(error), " ----time ---- ", now_time_with_time()]))
#                 ret = {'success': False, 'message': str(error)}
#         try:
#             workbook.close()
#             print('UnidentifiedImageError_count == ',UnidentifiedImageError_count)
#             print('FileNotFoundError_count == ', FileNotFoundError_count)
#             ret = {'success': True, 'message':'Excel File is Created Successfully.','filename':excel_sheet_name}
#         except (xlsxwriter.exceptions.UnsupportedImageFormat, xlsxwriter. exceptions.EmptyChartSeries, xlsxwriter.exceptions.
#             DuplicateTableName, xlsxwriter.exceptions.InvalidWorksheetName,xlsxwriter.exceptions.DuplicateWorksheetName,
#             xlsxwriter.exceptions.XlsxWriterException, xlsxwriter.exceptions.XlsxFileError, xlsxwriter.exceptions.FileCreateError,
#             xlsxwriter.exceptions.UndefinedImageSize, xlsxwriter.exceptions.FileSizeError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel19 8", str(error), " ----time ---- ", now_time_with_time()]))
#             ret = {'success': False, 'message': str(error)}
#         except PermissionError as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel20 9", str(error), " ----time ---- ", now_time_with_time()]))
#             ret = {'success': False, 'message': str(error)}
#         except AttributeError as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel21 10", str(error), " ----time ---- ", now_time_with_time()]))
#             ret = {'success': False, 'message': str(error)}
#     # except Exception as  error:
#     #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SPillageExcel22 11", str(error), " ----time ---- ", now_time_with_time()]))
#     #     ret = {'success': False, 'message': str(error)}
#     return ret


@spillage.route('/Spillageviolation_excel_download', methods=['GET'])
def Spillageviolation_excel_download():
    if 1:
    # try:
        list_of_files = glob.glob(os.path.join(os.getcwd(), "SpillageViolationsExcel/*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        path, filename = os.path.split(latest_file)
        if filename:
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
        else:
            return {'success': False, 'message': 'File is not found.'}
