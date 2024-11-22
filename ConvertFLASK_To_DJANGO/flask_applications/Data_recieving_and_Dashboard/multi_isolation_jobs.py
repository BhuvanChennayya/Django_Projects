from Data_recieving_and_Dashboard.packages import *
job_sheet_api = Blueprint('job_sheet_api', __name__)


#Panle status APIS
def FUNCHECKrepeativeJobSheetstatus(data):
    all_data = []
    try:
        if type(data) == list:
            for __, i in enumerate(data):
                if i['type']== 'HT' or i['type']== 'ht':
                    if isEmpty(i['data']):
                        all_panel_data = i['data']
                        if len(all_panel_data['panel_data']) == 1:
                            i['data']['panel_data'] = i['data']['panel_data'][0]
                            if i['data']['panel_data']['panel_id'] != 'NA':
                                return_1 = REPATATIVERIRODATA(parse_json(i), all_data)
                                if return_1:
                                    all_data.append(return_1)
                        elif len(all_panel_data['panel_data']) > 1:
                            panel_data1 = all_panel_data
                            for __, iii in enumerate(all_panel_data['panel_data']):
                                panel_data1['panel_data'] = iii
                                if panel_data1['panel_data']['panel_id'] != 'NA':
                                    print("ALL DATA:--------", all_data)
                                    i['data'] = panel_data1
                                    return_1 = REPATATIVERIRODATA(parse_json(i), all_data)
                                    if return_1:
                                        all_data.append(return_1)       
                else:
                    return_2 = MUlRIRODATACMECH(i, all_data)
                    if return_2:
                        all_data.append(return_2)                        
    except Exception as error:
        print('ERROR ----- (data)  line 3015 ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- FUNCHECKrepeativeJeeeobSheetstatus 2", str(error), " ----time ---- ", now_time_with_time()]))    
    return all_data



def get_two_elements_of_riro_data_for_latest_(joinedlist):
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

def riro_history_riro_for_sorting_only_two(list_of_dict):
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
            
        else:
            pass
    except Exception as error:
        print('error --- ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- riro_history_riro_for_sorting_only_two 2", str(error), " ----time ---- ", now_time_with_time()]))
        joinedlist = []
    if len(joinedlist) != 0:
        joinedlist = get_two_elements_of_riro_data_for_latest_(joinedlist)
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
                    if rack_process_list[1]['rack_process'] == rack_process_list[0]['rack_process']:
                        panel_status = False
                    elif rack_process_list[0]['rack_process'] == 'rack_out':
                        panel_status = False
                    elif rack_process_list[0]['rack_process'] == 'rack_in':
                        panel_status = True
                    elif rack_process_list[0]['rack_process'] == 'maintenance':
                        panel_status = False
    return panel_status



def check_riro_edit_status(final_data_riro_data):
    riro_edit_status = False
    if len(final_data_riro_data) != 0:
        for i in final_data_riro_data:
            if i['riro_edit_status']:
                riro_edit_status = True
                break
    return riro_edit_status

def check_ppe_violation_at_riro_moment(rtsp_url, panel_id, person_in_time,person_out_time):
    violation_test = False
    find_violation_data = list(mongo.db.data.find({'camera_rtsp': rtsp_url,'timestamp':{'$gte': person_in_time, '$lte': person_out_time},'violation_status': True}).sort('timestamp', -1))
    if len(find_violation_data) != 0:
        for olki, kl in enumerate(find_violation_data):
            for LILA, SHIVA in enumerate(kl['object_data']):
                if 'pannel_details' in SHIVA.keys():
                    if panel_id is not None and SHIVA['pannel_details'] is not None:
                        if panel_id in SHIVA['pannel_details']:
                            violation_test = True
                            break
    else:
        pass
    return violation_test

def riro_history_check_the_riro_data_with_sorting_(rtsp_url, panel_id, check_data):
    match_data = []
    violation_test = False
    panel_status = False
    panel_count = 0
    rack_process_list = []
    lock_list = []
    tag_list = []
    final_data_riro_data = []
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
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])#check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['irrd_in_time'], kiku['irrd_out_time'])
                elif kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                else:
                    pass
                riro_data_test_1 = {'sort_id': kiku['_id'], 'panel_no': kiku['panel_no'], 'rack_method': kiku['rack_method'],'rack_process': kiku['rack_process'], 'irrd_in_time': kiku['irrd_in_time'], 'irrd_out_time': kiku['irrd_out_time'], 'tag': kiku['tag'], 'lock': kiku['lock'], 'lock_time': kiku['lock_time'], 'tag_time':kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher':kiku['magnetic_flasher'],'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image':kiku['riro_merged_image'], 'riro_merged_image_size': kiku['riro_merged_image_size'], 'riro_edit_status':kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)

            elif kiku['rack_method'] == 'manual':
                if kiku['person_in_time'] is not None and kiku['person_out_time'] is not None:
                    violation_test = check_ppe_violation_at_riro_moment(rtsp_url, panel_id, kiku['person_in_time'], kiku['person_out_time'])
                else:
                    pass
                riro_data_test_1 = {'sort_id': kiku['_id'], 'panel_no':kiku['panel_no'], 'rack_method': kiku['rack_method'],'rack_process': kiku['rack_process'], 'irrd_in_time':kiku['person_in_time'], 'irrd_out_time': kiku['person_out_time'], 'tag': kiku['tag'], 'lock': kiku['lock'], 'lock_time': kiku['lock_time'], 'tag_time':kiku['tag_time'], 'five_meter': kiku['five_meter'],'barricading': kiku['barricading'], 'magnetic_flasher':kiku['magnetic_flasher'], 'violation': violation_test,'riro_key_id': kiku['riro_key_id'], 'riro_merged_image': kiku['riro_merged_image'], 'riro_merged_image_size':kiku['riro_merged_image_size'], 'riro_edit_status':kiku['riro_edit_status'], 'lock_tag_image': kiku['cropped_panel_image_path'], 'remarks': kiku['remarks']}
                match_data.append(riro_data_test_1)
                
    if len(rack_process_list) != 0:
        rack_process_for_job = ['rack_out', 'rack_in']
        if rack_process_for_job == rack_process_list:
            panel_status = check_the_rackout_process_(match_data)
        elif 'rack_in' in rack_process_list:
            panel_status = True
    return riro_history_riro_for_sorting_only_two(match_data), check_the_rackout_process_(match_data), check_riro_edit_status(match_data)


def MUPANRRILATION_multi_isolation(data):
    all_data = []
    # print("MUPANRRILATION_multi_isolation DATA:----", data)
    try:
        if type(data) == list:
            for __, i in enumerate(data):
                if i['type'] =='HT' or i['type'] =='ht': 
                    if isEmpty(i['data']) :
                        all_panel_data = i['data']
                        if len(all_panel_data['panel_data']) == 1:
                            yxz = i['data']
                            yxz['panel_data'] = yxz['panel_data'][0]
                            i['data'] = yxz
                            zz = parse_json(i)
                            return_1 = REPATATIVERIRODATA(zz, all_data)
                            if return_1:
                                all_data.append(return_1)
                        elif len(all_panel_data['panel_data']) > 1:
                            panel_data1 = all_panel_data
                            for __, iii in enumerate(all_panel_data['panel_data']):
                                panel_data1['panel_data'] = iii
                                i['data'] = panel_data1
                                i = parse_json(i)
                                return_1 = REPATATIVERIRODATA(i, all_data)
                                if return_1:
                                    all_data.append(return_1)                    
                else:
                    if len(i['data']):
                        return_2 = MUlRIRODATACMECH(i, all_data)
                        if return_2:
                            all_data.append(return_2)                       
            
    except Exception as error:
        print('ERROR -----  (data)    line 2189 to 2231', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- MUPANRRILATION_mu33lti_isolation 2", str(error), " ----time ---- ", now_time_with_time()]))        
    return all_data

def isolation_camaparision_function(tagname):
    database_detail = {'sql_objecttable_name': 'testopc', 'sql_panel_table':'testopc', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrunopc', 'sslmode':'disable'}
    # print("DATABASE DETAILS:", database_detail)
    isolation_status =None
    # conn = 0
    try:
        # print("___________________________________________________________")
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    
        cursor = conn.cursor()
        # print("CURSOR ERROR:---------------------")

        try:
            cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY local_time desc')
        except psycopg2.errors.UndefinedTable as error:
            print('[ERR] from send data encountered error at stage 1 as ', error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- isolation_camaparision_function 2", str(error), " ----time ---- ", now_time_with_time()]))
        except psycopg2.errors.InFailedSqlTransaction as error:
            print('[ERR] from send data encountered error at stage 1 as ', error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- isolation_camaparision_function 3", str(error), " ----time ---- ", now_time_with_time()]))
        l1data_row = cursor.fetchone()
        cols_name = list(map(lambda x: x[0], cursor.description))
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

    except Exception as error:
        print("***************************************************")
        conn = 0
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- isolation_camaparision_function 1", str(error), " ----time ---- ", now_time_with_time()]))
    
    return isolation_status


def time_sort_key_for_history(d):
    return d['riro_data'][0]['irrd_in_time']

def riro_live_data(live_riro_data):
    for index_no, live_form in enumerate(live_riro_data):
        check_data = [{'sort_id': live_form['_id'], 'panel_no': live_form['panel_no'], 'rack_method': None, 'rack_process': None,'irrd_in_time': None, 'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None, 'tag_time': None, 'five_meter': None, 'barricading': None, 'magnetic_flasher': live_form['magnetic_flasher'], 'violation': False, 'riro_key_id': None,'riro_merged_image': None, 'riro_merged_image_size':{'height':None, 'width': None}, 'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}]
    return check_data


def sort_irrd_time_for_history(time_stamp_data):
    final_time_sort = sorted(time_stamp_data, key=time_sort_key_for_history,
        reverse=True)
    return final_time_sort

def riro_for_history(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    live_data = []
    joinedlist = None
    try:
        for mix, i in enumerate(list_of_dict):
            if i['live_status']:
                live_data.append(i)
            elif i['riro_data'][0]['irrd_in_time'] is not None:
                time_stamp_data.append(i)
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
        else:
            pass
    except Exception as error:
        print('error --- ----------------- because of error ------------------------- ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- riro_for_history 1", str(error), " ----time ---- ", now_time_with_time()]))
        joinedlist = []
    return joinedlist


def all_riro_final_sortin(final_test_sort):
    new_final_test_riro = riro_for_history(final_test_sort)
    return new_final_test_riro


def check_magnetic_flasher_status(listOFdata):
    all_data = []
    # print("length of the data====new sorted==",len(listOFdata))
    for index_number , data_element in enumerate(listOFdata):
        if data_element['type'] =='HT'  or   data_element['type'] =='ht' :
            if len(data_element['data']['panel_data']) !=0:
                if data_element['tagname'] is not None and data_element['tagname'] !='' :
                    if 1:
                    # try:
                        if data_element['isolation_status']=='live' and data_element['data']['panel_data']['isolation_status']=='live':
                            data_element['exception_status']=True      
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
    return all_data


#GET MULTI_ISOLATION DATA
def multiiso_fun(job_sheet_name, sheet_token):
    data = list(mongo.db.panel_data.find({'job_sheet_name':job_sheet_name, 'token': sheet_token}, sort=[('_id',   pymongo.DESCENDING)]))
    if data is not None:
        final_panel_data = []   
        data = MUPANRRILATION_multi_isolation(data)
        for ___INNN, emmmi in enumerate(data):
            if emmmi['type']=='HT' or emmmi['type']=='ht':
                if  type(emmmi['data']['panel_data']) != list:
                    if emmmi['data']['panel_data']['panel_id'] is not None:
                        final_panel_data.append(emmmi)
                    else:
                        print('panel id none')
            elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
                final_panel_data.append(emmmi)
        
        if len(final_panel_data) != 0:
            riro_final = []
            for i, each_panel in enumerate(final_panel_data):
                if each_panel['type'] =='HT' or each_panel['type']=='ht':
                    camera_rtsp = each_panel['data']['rtsp_url']
                    show_live_riro = list(mongo.db.riro_data.find({'token':sheet_token, 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': camera_rtsp, 'flasher_status':1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                    if len(show_live_riro) != 0:
                        show_live_riro = riro_live_data(show_live_riro)
                        each_panel['riro_data'] = show_live_riro
                        each_panel['riro_edit_status'] = False
                        each_panel['live_status'] = True
                        each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
                        each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
                        each_panel['exception_status'] = False
                        each_panel = parse_json(each_panel)
                        riro_final.append(each_panel)
                    elif camera_rtsp:
                        find_riro_data = list(mongo.db.riro_data.find({'token': each_panel['token'], 'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': camera_rtsp}, sort=[('_id', pymongo.DESCENDING)]))
                        if len(find_riro_data) != 0:
                            (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(camera_rtsp, each_panel['data']['panel_data']['panel_id'], find_riro_data))
                            if panel_status or len(check_data) != 0:
                                each_panel['data']['panel_data']['panel_status'] = panel_status
                                each_panel['riro_data'] = check_data
                                each_panel['riro_edit_status'] = riro_edit_status
                                each_panel['live_status'] = False
                                each_panel['sort_id'] = check_data[0]['sort_id']
                                each_panel['isolation_status'] = isolation_camaparision_function(each_panel['tagname'])
                                each_panel['exception_status'] = False
                                riro_final.append(each_panel)
                            else:
                                check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
                                                'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                                'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '} ]
                                each_panel['riro_data'] = check_data
                                each_panel['riro_edit_status'] = False
                                each_panel['live_status'] = False
                                each_panel['sort_id'] = None
                                each_panel['isolation_status'] = isolation_camaparision_function(each_panel['tagname'])
                                each_panel['exception_status'] = False
                                riro_final.append(each_panel)
                        else:
                            check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
                                    'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}]
                            each_panel['riro_data'] = check_data
                            each_panel['riro_edit_status'] = False
                            each_panel['live_status'] = False
                            each_panel['sort_id'] = None
                            each_panel['isolation_status'] = isolation_camaparision_function(each_panel['tagname'])
                            each_panel['exception_status'] = False
                            riro_final.append(each_panel)
                else:
                    check_data = [{'sort_id': None,'panel_no': None,'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,'lock': None,
                                    'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,
                                    'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
                                    'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '} ]
                    each_panel['riro_data'] = check_data
                    each_panel['riro_edit_status'] = False
                    each_panel['live_status'] = False
                    each_panel['sort_id'] = None
                    each_panel['isolation_status'] = None
                    each_panel['exception_status'] = False
                    riro_final.append(each_panel)

            else:
                final_test_sort = parse_json(all_riro_final_sortin(riro_final))                        
                ret = {'message': check_magnetic_flasher_status(final_test_sort),'success': True}
                ret['job_sheet_status'] = True
        else:
            ret = {'message': 'panel data not found.', 'success': False}
            ret['job_sheet_status'] = True
    else:
        ret['message'] = 'panel data not found'
        ret['job_sheet_status'] = True

    return ret


def get_previous_jobs(job_sheet_name, sheet_token):
    riro_return_data = []
    data1 = list(mongo.db.panel_data.find({'job_sheet_name': job_sheet_name, 'token': sheet_token}, sort=[('_id', pymongo.DESCENDING)]))
    if len(data1) != 0:
        all_data =FUNCHECKrepeativeJobSheetstatus(data1)
        rack_method_done_count = 0
        rack_method_not_done_count = 0
        total_panel_count = 0
        if len(all_data) != 0:
            for ___12, iisddf in enumerate(all_data):
                total_panel_count += 1
                # print("Testing the total_panel_count:------------------", total_panel_count)
                if iisddf['type']=="HT" or iisddf['type']=='ht':
                    camera_rtsp = iisddf['data']['rtsp_url']
                    find_riro_data = mongo.db.riro_data.find({'token': sheet_token, 'camera_name': iisddf['data']['camera_name'], 'camera_rtsp': camera_rtsp}, sort=[ ('_id', pymongo.DESCENDING)])
                    find_riro_data = list(find_riro_data)
                    # print("RIRO DATA------------------------", find_riro_data)
                    if len(find_riro_data) != 0:
                        check_data, panel_status, hello = (riro_history_check_the_riro_data_with_sorting_(camera_rtsp, iisddf['data']['panel_data']['panel_id'], find_riro_data))
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
                                iisddf['remarks'] = check_data[0]['remarks']
                            if len(check_data) > 1:
                                latest_riro_ = (with_campare_time_and_get_latest_data_of_riro(check_data))
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
                    iisddf['remarks'] = ''
                if 'ip_address' in iisddf.keys():
                    del iisddf['ip_address']
                riro_return_data.append(iisddf)

                print("riro_return_data", riro_return_data)
                all_data = riro_return_data
                # rack_method_done_count = 0
                # rack_method_not_done_count = 0
                # total_panel_count = 0
                # if len(riro_return_data) != 0:
                # for singsing, xml_to in enumerate(riro_return_data):
                # total_panel_count += 1
                if iisddf['type']=="HT" or iisddf['type']=='ht':
                    if iisddf['data']['panel_data']['panel_status']:
                        rack_method_done_count += 1
                    else:
                        rack_method_not_done_count += 1
                else:
                    rack_method_not_done_count += 1

            print("total_panel_count:--", total_panel_count)

            final_data = {'total_panel_count': total_panel_count,'processed_count': rack_method_done_count,'not_processed': rack_method_not_done_count}
            ret = {'message': final_data, 'success': True}
        
        else:
            rack_method_not_done_count += 1
            total_panel_count += 1
            final_data = {'total_panel_count': total_panel_count,'processed_count': rack_method_done_count,'not_processed': rack_method_not_done_count}
            ret = {'message': final_data, 'success': True}
            # ret = {'message': 'this job-sheet does not found riro-data.', 'success': False}
    else:
        # ret['message'] = 'panel_data is not found.'
        ret = {'message':'Given mongo-id has no panel_data.', 'success':False}
    return ret


@job_sheet_api.route('/get_list_job_sheets', methods = ['GET'])
def get_list_job_sheets():
    ret = {'message':"something wrong with ===","success":False}
    electricalsheet_data = list(mongo.db.job_sheet_details.find({},sort=[('_id', pymongo.DESCENDING)]))
    mechanicalsheet_data = list(mongo.db.mechjob_sheet.find({},sort=[('_id', pymongo.DESCENDING)]))
    if len(electricalsheet_data) !=0 and len(mechanicalsheet_data) !=0 :
        shutdownhistory = {'electrical_isolation_history':electricalsheet_data,'mechanical_isolation_history':mechanicalsheet_data}
        ret = {"message":shutdownhistory, "success":True}
    elif len(electricalsheet_data) !=0:
        shutdownhistory = {'electrical_isolation_history':electricalsheet_data,'mechanical_isolation_history':mechanicalsheet_data}
        ret = {"message":shutdownhistory, "success":True}
    
    elif len(mechanicalsheet_data) !=0:
        shutdownhistory = {'electrical_isolation_history':electricalsheet_data,'mechanical_isolation_history':mechanicalsheet_data}
        ret = {"message":shutdownhistory, "success":True}
    else:
        ret['message']='job sheet details not found.'
    return parse_json(ret)






@job_sheet_api.route('/get_job_sheet_status22/<job_mongo_id>', methods = ['GET'])
@job_sheet_api.route('/get_job_sheet_status22', methods = ['GET'])
def get_latest_job_sheet_data(job_mongo_id = None):
    ret = {'message': 'Something went wrong with job sheet status api', 'success': False}
    sheet_data = mongo.db.job_sheet_details.find({},sort=[('_id', pymongo.DESCENDING)])
    job_sh_mongo_ids = []
    for a_data in sheet_data:
        stamp_sheet_names = a_data['_id']
        job_sh_mongo_ids.append(stamp_sheet_names)        
    if job_mongo_id is not None:
        if ObjectId(job_mongo_id) in job_sh_mongo_ids:
            sheet_data_1 = mongo.db.job_sheet_details.find_one({"_id":ObjectId(job_mongo_id)})
            sheet_data_1["_id"] = str(sheet_data_1["_id"])
            if sheet_data_1 is not None:
                job_sheetname = sheet_data_1['job_sheet_name']
                sheet_token = sheet_data_1['token']
                ret = get_previous_jobs(job_sheetname, sheet_token)
                # print("------------------------RET----------------------------", ret)

        else:
            ret['message'] = 'job sheet is not uploaded yet'

    else:
        all_data = []
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        # print("SHEET DATA:", sheet_data)
        if sheet_data is not None:
            job_sheet_name = sheet_data['job_sheet_name']
            sheet_token = sheet_data['token']
            ret = get_previous_jobs(job_sheet_name, sheet_token)   

    # print("RET:------------------------------", ret)
    return ret


# @job_sheet_api.route('/multiisolation/<job_mongo_id>', methods = ['GET'])
# @job_sheet_api.route('/multiisolation', methods=['GET'])
def multiisolation_convayor_pnumertic_hydralic(job_mongo_id = None):
    if 1:
    # try:
        ret = {'success': False, 'message':'Something went wrong, please try again later'}
        sheet_data = mongo.db.job_sheet_details.find({},sort=[('_id', pymongo.DESCENDING)])
    # print("SHEET DATA:", sheet_data)

        job_sh_mongo_ids = []   
        for a_data in sheet_data:
            stamp_sheet_names = a_data['_id']
            job_sh_mongo_ids.append(stamp_sheet_names)

        if job_mongo_id is not None:
            if ObjectId(job_mongo_id) in job_sh_mongo_ids:
                sheet_data_1 = mongo.db.job_sheet_details.find_one({"_id":ObjectId(job_mongo_id)})
                sheet_data_1["_id"] = str(sheet_data_1["_id"])
                print("SHEET DATA 1:-----", sheet_data_1)
                if sheet_data_1 is not None:
                    job_sheet_name = sheet_data_1['job_sheet_name']
                    sheet_token = sheet_data_1['token']
                    ret = multiiso_fun(job_sheet_name, sheet_token)

        else:
            ret['job_sheet_status'] = True
            sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
            if sheet_data is not None:
                job_sheet_name = sheet_data['job_sheet_name']
                sheet_token = sheet_data['token']
                ret = multiiso_fun(job_sheet_name, sheet_token)
            
    return ret




@job_sheet_api.route('/add_hydraulic', methods=['POST'])
def adding_hydraulic_data():
    ret = {'success': False, 'message':'something went wrong with get add_hydraulic  api'}
    if 1:
    # try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['data']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                list_data = jsonobject['data']
                print("list_data",list_data)
                if isEmpty(list_data) :
                    sheet_data = mongo.db.job_sheet_details.find_one({ 'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                    if sheet_data is not None:
                        id = list_data['id']
                        roi_data = list_data['roi_data']
                        image_name = list_data['image_name']
                        panel_key_id = list_data['panel_key_id']
                        if id is not None:
                            if image_name is not None:
                                if panel_key_id is not None:
                                    panel_find_data = mongo.db.panel_data.find_one({'_id': ObjectId(id), 'data.image_name': image_name, 'job_sheet_name': sheet_data[ 'job_sheet_name'], 'token': sheet_data['token'],'type':{"$ne": "HT"}})
                                    if panel_find_data is not None:
                                        panel_find_data_roi = panel_find_data[ 'data']
                                        if isEmpty(panel_find_data_roi) :
                                            if dictionary_key_exists(panel_find_data_roi,'hydraulic_data'):
                                                get_panel_key_id12 = [ioo['panel_key_id'] for __p, ioo in enumerate(panel_find_data_roi['hydraulic_data']) if ioo['panel_key_id']is not None]
                                                if panel_key_id not in get_panel_key_id12:
                                                    data___ = []
                                                    if panel_find_data_roi['image_name'] == image_name:
                                                        print('roi_data ',roi_data)
                                                        if dictionary_key_exists(panel_find_data_roi,'hydraulic_data'):                                                        
                                                            get_panel_key_id = [ioo['panel_key_id'] for __p, ioo in enumerate(panel_find_data_roi['hydraulic_data']) if ioo['panel_key_id']]
                                                            if (panel_key_id is not get_panel_key_id):
                                                                if len(panel_find_data_roi['hydraulic_data']) !=0:
                                                                    data___.append(roi_data)                                                           
                                                                    for __PO, ioo in enumerate(panel_find_data_roi['hydraulic_data']):
                                                                        data___.append(ioo)
                                                                else:
                                                                    data___.append(roi_data)
                                                            else:
                                                                for __PO, ioo in enumerate(panel_find_data_roi[ 'hydraulic_data']):
                                                                    data___.append(ioo)
                                                        else:
                                                            data___.append(roi_data)
                                                        if len(data___) !=0:
                                                            panel_find_data_roi['hydraulic_data'] = data___
                                                    filters = {'_id': ObjectId(id)}
                                                    newvalues = {'$set':{'data': panel_find_data_roi}}
                                                    result = (mongo.db.panel_data.update_one(filters, newvalues))
                                                    if (result.modified_count > 0):
                                                        ret = {'message':  'hydraulic_data is added successfully.',  'success': True}
                                                    else:
                                                        (ret['message']) = ('hydraulic_data roi is not updated.')
                                                else:
                                                    ret['message']='hydraulic key id already exists.'
                                            else:
                                                data___ = []   
                                                if panel_find_data_roi['image_name'] == image_name:                                                        
                                                    data___.append(roi_data)
                                                    if len(data___) !=0:
                                                        panel_find_data_roi['hydraulic_data'] = data___
                                                    else:
                                                        panel_find_data_roi['hydraulic_data'] = data___
                                                filters = {'_id': ObjectId(id)}
                                                newvalues = {'$set':{'data': panel_find_data_roi}}
                                                result = (mongo.db.panel_data.update_one(filters, newvalues))
                                                if (result.modified_count > 0):
                                                    ret = {'message':  'hydraulic_data is added successfully.',  'success': True}
                                                else:
                                                    (ret['message']) = ('hydraulic_data roi is not updated.')
                                        else:
                                            ret['message'] = 'hydraulic_data  is not found.'
                                    else:
                                        ret['message'] = 'hydraulic_data  is not found.'
                                else:
                                    ret['message'] = 'panel key id should not be None'
                            else:
                                ret['message'] = 'image_name should not be none.'
                        else:
                            ret['message'] = 'id should not be none'
                    else:
                        ret['message'] = 'job sheet is not uploaded yet'
                else:
                    ret['message'] = 'data should not be none'
        else:
            ret = {'success': False, 'message':  'You have missed these keys ' + str(missing_key) +' to enter. please enter properly.'}
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- add_hydraulic 1", str(error), " ----time ---- ", now_time_with_time()])) 
    #     ret['message' ] = 'something error has occered in  apis ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")  
    # except Exception as error:
    #     ret = {'success': False, 'message': str(error)}
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- add_hydraulic 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return jsonify(ret)




@job_sheet_api.route('/add_pneumatic', methods=['POST'])
def new_add_pneumatic_data():
    ret = {'success': False, 'message':'something went wrong with get area details api'}
    # if 1:
    try:        
        if request.method == 'POST':
            jsonobject = request.json
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['data']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
                else:
                    list_data = jsonobject['data']
                    print("list_data",list_data)
                    if isEmpty(list_data) :
                        sheet_data = mongo.db.job_sheet_details.find_one({ 'status': 1}, sort=[('_id', pymongo.DESCENDING)])
                        if sheet_data is not None:
                            id = list_data['id']
                            roi_data = list_data['roi_data']
                            image_name = list_data['image_name']
                            panel_key_id = list_data['panel_key_id']
                            if id is not None:
                                if image_name is not None:
                                    if panel_key_id is not None:
                                        panel_find_data = mongo.db.panel_data.find_one({'_id': ObjectId(id), 'data.image_name': image_name, 'job_sheet_name': sheet_data[ 'job_sheet_name'], 'token': sheet_data['token'],'type':{"$ne": "HT"}})
                                        if panel_find_data is not None:
                                            panel_find_data_roi = panel_find_data['data']
                                            if isEmpty(panel_find_data_roi) :
                                                if dictionary_key_exists(panel_find_data_roi,'pneumatic_data'):
                                                    get_panel_key_id12 = [ioo['panel_key_id'] for __p, ioo in enumerate(panel_find_data_roi['pneumatic_data']) if ioo['panel_key_id']is not None]
                                                    if panel_key_id not in get_panel_key_id12:
                                                        data___ = []
                                                        if panel_find_data_roi['image_name'] == image_name: 
                                                            get_panel_key_id = [ioo['panel_key_id'] for __p, ioo in enumerate(panel_find_data_roi['pneumatic_data']) if ioo['panel_key_id']is not None]
                                                            print('get_panel_key_id===',get_panel_key_id)
                                                            if panel_key_id is not get_panel_key_id:
                                                                if len(panel_find_data_roi['pneumatic_data']) !=0:
                                                                    data___.append(roi_data)                                                           
                                                                    for __PO, ioo in enumerate(panel_find_data_roi['pneumatic_data']):
                                                                        data___.append(ioo)
                                                                else:
                                                                    data___.append(roi_data)
                                                                if len(data___) !=0:
                                                                    panel_find_data_roi['pneumatic_data'] = data___
                                                        filters = {'_id': ObjectId(id)}
                                                        newvalues = {'$set':{'data': panel_find_data_roi}}
                                                        result = mongo.db.panel_data.update_one(filters, newvalues)
                                                        if result.modified_count > 0:
                                                            ret = {'message':  'pneumatic_data is added successfully.',  'success': True}
                                                        else:
                                                            ret['message'] = 'pneumatic_data roi is not updated.'
                                                    else:
                                                        ret['message']='pneumatic roi key id already exists.'
                                                else:
                                                    data___ = []
                                                    if panel_find_data_roi['image_name'] == image_name:
                                                        data___.append(roi_data)
                                                        if len(data___) !=0:
                                                            panel_find_data_roi['pneumatic_data'] = data___
                                                    filters = {'_id': ObjectId(id)}
                                                    newvalues = {'$set':{'data': panel_find_data_roi}}
                                                    result = mongo.db.panel_data.update_one(filters, newvalues)
                                                    if (result.modified_count > 0):
                                                        ret = {'message':  'pneumatic_data is added successfully.',  'success': True}
                                                    else:
                                                        (ret['message']) = 'pneumatic_data roi is not updated.'

                                            else:
                                                ret['message'] = 'pneumatic_data data is not found.'
                                        else:
                                            ret['message'] = 'pneumatic_data data is not found.'
                                    else:
                                        ret['message'] = 'panel key id should not be None'
                                else:
                                    ret['message'] = 'image_name should not be none.'
                            else:
                                ret['message'] = 'id should not be none'    
                        else:
                            ret['message'] = 'job sheet is not uploaded yet'
                    else:
                        ret['message'] = 'data should not be none'
            else:
                ret = {'success': False, 'message':  'You have missed these keys ' + str(missing_key) +' to enter. please enter properly.'}
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
        print("print(,)", str(error))
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- add_pneumatic 1", str(error), " ----time ---- ", now_time_with_time()]))
        ret['message' ] = 'something error has occered in  apis ' + str(error)  +'  ----time ----   '+ now_time_with_time()
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.")  
    except Exception as error:
        ret = {'success': False, 'message': str(error)}
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- add_pneumatic 2", str(error), " ----time ---- ", now_time_with_time()]))
    return jsonify(ret)





def remove_delete_hydraulic_from_db(data, image_name, panel_key_id):
    panel_delete_return_value = False
    panel_delete_return_value = {'message':"initial message",'success':False}
    length_measure = False
    if 1:
    # try:
        if data is not None:
            final_panel_data_for_updating = []
            if isEmpty(data['data']) :
                if dictionary_key_exists(data['data'],'hydraulic_data'):   
                    if data['data']['image_name'] == image_name:
                        original_hydraulic_data_length=len(data['data']['hydraulic_data'])                        
                        for jkkee, panel_is_empty_bbox in enumerate(data['data']['hydraulic_data']):
                            if isEmpty(panel_is_empty_bbox):
                                if  panel_is_empty_bbox['panel_key_id'] ==int(panel_key_id):
                                    print('db panel key id ===',panel_is_empty_bbox['panel_key_id'])
                                    print("given panel key id ====", panel_key_id)                                        
                                else:
                                    if panel_is_empty_bbox['bbox']!= '':
                                        final_panel_data_for_updating.append(panel_is_empty_bbox)
                                    else:
                                        pass
                            else:
                                pass
                        print('original length =',original_hydraulic_data_length)
                        print('modified lenght =',len(final_panel_data_for_updating))
                        if len(final_panel_data_for_updating)<original_hydraulic_data_length:
                            length_measure = True  
                        if len(final_panel_data_for_updating) != 0:
                            data['data']['hydraulic_data']  = final_panel_data_for_updating
                        else:
                            data['data']['hydraulic_data'] = []
                else:
                    print(' hydraulic data key is not found... ')
                id = data['_id']
                if length_measure:
                    print('try to update now ')
                    result = result = mongo.db.panel_data.update_one({'_id': ObjectId(id)},{'$set':{'data': data['data']}})
                    if result.matched_count > 0:
                        print('result match count==',result.matched_count)
                        panel_delete_return_value['success']=True
                    else:
                        panel_delete_return_value['message']='not able update in mongodb.'
                else:
                    panel_delete_return_value['message']='given panel key id is not found'
        else:
            print('panel data not found  removing the empty panels 2---')
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- remove_delete_hydrauli333c_from_db 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = 'something error has occered in  apis ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- remove_delete_hydr333aulic_from_db 2", str(error), " ----time ---- ", now_time_with_time()]))
    return panel_delete_return_value


@job_sheet_api.route('/delete_hydraulic', methods=['POST'])
def delete_panel_while():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = [ 'id', 'imagename','panel_key_id']
        print(jsonobject)
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                imagename = jsonobject['imagename']
                id = jsonobject['id']
                panel_key_id = jsonobject['panel_key_id']
                all_data = []
                if id is not None:
                    data = mongo.db.panel_data.find_one({'_id':ObjectId(id)})
                    if data is not None:
                        return_value_for_delete_panel = remove_delete_hydraulic_from_db(data, imagename, panel_key_id)
                        if return_value_for_delete_panel:
                            if return_value_for_delete_panel['success']:
                                ret = {'success': True, 'message':'hydraulic data is deleted successfully'}
                            else:
                                ret=return_value_for_delete_panel
                        else:
                            ret['message'] = 'hydraulic data is not deleted.'
                    else:
                        ret['message'] = 'data not found'
                else:
                    ret['message'] = ('mongo id  should not be none, please enter the proper mongo id.')
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- delete_hydraulic 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = 'something error has occered in  apis ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")     
    # except Exception as error:
    #     ret['message'] = 'error occurred  delete the panel = ' + str(error)  +'  ----time ----   '+ now_time_with_time() 
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- delete_hydraulic 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret





def remove_delete_pneumatic_from_db(data, image_name, panel_key_id):
    panel_delete_return_value = False
    panel_delete_return_value = {'message':"initial message",'success':False}
    length_measure = False
    if 1:
    # try:
        if data is not None:
            if isEmpty(data['data']):
                if dictionary_key_exists(data['data'],'pneumatic_data'):   
                    if data['data']['image_name'] == image_name:
                        original_hydraulic_data_length=len(data['data']['pneumatic_data'])
                        print('pneumatic_data-data',data['data']['pneumatic_data'])
                        print('length ---', len(data['data']['pneumatic_data']))
                        final_panel_data_for_updating = []
                        for jkkee, panel_is_empty_bbox in enumerate(data['data']['pneumatic_data']):
                            if isEmpty(panel_is_empty_bbox):
                                if  panel_is_empty_bbox['panel_key_id'] ==int(panel_key_id):
                                    print('db panel key id ===',panel_is_empty_bbox['panel_key_id'])
                                    print("given panel key id ====", panel_key_id)                                    
                                else:
                                    if panel_is_empty_bbox['bbox']!= '':
                                        final_panel_data_for_updating.append(panel_is_empty_bbox)
                                    else:
                                        pass
                            else:
                                pass
                        print('original length =',original_hydraulic_data_length)
                        print('modified lenght =',len(final_panel_data_for_updating))
                        if len(final_panel_data_for_updating)<original_hydraulic_data_length:
                            length_measure = True          
                        if len(final_panel_data_for_updating) != 0:
                            data['data']['pneumatic_data']  = final_panel_data_for_updating
                        else:
                            data['data']['pneumatic_data'] =[]
                    else:
                        print("for this imagename datanot found.")
                else:
                    print(' pneumatic data key is not found... ')
                id = data['_id']
                if length_measure:
                    print('try to update now ')
                    result = result = mongo.db.panel_data.update_one({'_id': ObjectId(id)},{'$set':{'data': data['data']}})
                    if result.matched_count > 0:
                        print('result match count==',result.matched_count)
                        panel_delete_return_value['success']=True
                    else:
                        panel_delete_return_value['message']='not able update in mongodb.'
                else:
                    panel_delete_return_value['message']='given panel key id is not found'
        else:
            print('panel data not found  removing the empty panels 2---')
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- remove_deleteeee_pneumatic_from_db 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = 'something error has occered in  apis ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- remove_delete_eeepneumatic_from_db 2", str(error), " ----time ---- ", now_time_with_time()]))
    return panel_delete_return_value


@job_sheet_api.route('/delete_pneumatic', methods=['POST'])
def delete_pneumatic_data():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    if 1:
    # try:
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = [ 'id', 'imagename','panel_key_id']
        print(jsonobject)
        print(type(jsonobject))
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                imagename = jsonobject['imagename']
                id = jsonobject['id']
                panel_key_id = jsonobject['panel_key_id']
                if id is not None:
                    data = mongo.db.panel_data.find_one({'_id':ObjectId(id)})
                    if data is not None:
                        return_value_for_delete_panel = remove_delete_pneumatic_from_db(data, imagename, panel_key_id)
                        if return_value_for_delete_panel:
                            if return_value_for_delete_panel['success']:
                                ret = {'success': True, 'message':'pneumatic data is deleted successfully'}
                            else:
                                ret=return_value_for_delete_panel
                        else:
                            ret['message'] = 'pneumatic data is not deleted.'
                    else:
                        ret['message'] = 'data not found'
                else:
                    ret['message'] = ('mongo id  should not be none, please enter the proper mongo id.')
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- delete_pneumatic 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message' ] = 'something error has occered in  apis ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.")     
    # except Exception as error:
    #     ret['message'] = 'error occurred  delete the panel = ' + str(error)  +'  ----time ----   '+ now_time_with_time()
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- delete_pneumatic 2", str(error), " ----time ---- ", now_time_with_time()]))
    return ret



def jobsheetcheck_license_of_camera(CamCount):
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        conn = 0
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- jobsheetchedddck_license_of_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- jobsheetcheck_lidddcense_of_camera 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- jobsheetcheck_ldddicense_of_camera 3", str(error), " ----time ---- ", now_time_with_time()]))
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

        print('max cameras-',split_data[0])
        if CamCount < int((split_data[0])):
            license_status = True
        elif CamCount == int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status

@job_sheet_api.route('/check_license_status', methods=['GET'])
def checking_license():
    ret = {"message":"something went wrong with the check333_license_status", 'success':False}
    sheet_data = mongo.db.job_sheet_details.find_one({ 'status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if sheet_data is not None:
        data =list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
        list_of_ip_address_panel = []
        for i in data:
            if dictionary_key_exists(i, 'data'):
                if isEmpty(i['data']) :
                    if i['data']['ip_address'] not in list_of_ip_address_panel:
                        list_of_ip_address_panel.append(i['data']['ip_address'])
        print('ip list ----- ',list_of_ip_address_panel)
        print('len==== ', len(list_of_ip_address_panel))
        if jobsheetcheck_license_of_camera(len(list_of_ip_address_panel)):
            ret={'success':True,'message':'you have licesense to add the camera'}
        else:
            ret['message']="you have reached maximum licesence of adding cameras."
    else:
        ret['message']='job sheet data is not found, please upload jobsheet.'
    return ret


@job_sheet_api.route('/delete_mechanical_job/<id>', methods=['GET'])
def riro_data_delete(id = None):
    ret ={'message':'something went wrong with delete mechanical','success':False}
    if 1:
        if id is not None:
            x = mongo.db.panel_data.find_one({'_id': ObjectId(id)})
            if x is None:
                ret['message'] = 'no data found for the deletion.'
            else:
                result = mongo.db.panel_data.delete_one({'_id': ObjectId(id)})
                if result.deleted_count > 0:
                    ret = {'message': 'riro_data deleted successfully.','success': True}
                else:
                    ret['message'] = 'riro_data is not deleted ,due to something went wrong with database.'
        else:
            ret['message']='please give proper id'
    return ret


def verify_ip_address(main_list):
    print('data length ==== 0000000000 ======',len(main_list))
    final_list = []
    if 1:
    # try:
        if len(main_list) != 0:
            for ___12, panel_val in enumerate(main_list):
                if len(panel_val['hydraulic_data']) != 0:
                    require_panel_data = {'ip_address': panel_val['ip_adrs' ], 'camera_name': panel_val['camera_name'],'rtsp_url': panel_val['rtsp_url'],
                                           'hydraulic_data':panel_val['hydraulic_data'], 'ai_solution': panel_val['ai_solution'], 'roi_ra': panel_val['roi_ra'],'video_names': panel_val['video_names']}
                    if require_panel_data not in final_list:
                        final_list.append(require_panel_data)
                else:
                    print("empty -------- panel_val['panel_data']--------------- ", panel_val['panel_data'])
        else:
            print('empty pandel data --- ')
    # except Exception as error: 
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- verify_i11p_address 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     final_list = []
    return final_list

def update_cam_id(update_cam_ids_data):
    try:
        data_values = update_cam_ids_data['data']
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
                empty_list = []
                for NTR, d in enumerate(data_field):
                    if d['rtsp_url'] == total_rtsp_url:
                        d['camera_id'] = total_camera_id
                        empty_list.append(d)
                    else:
                        empty_list.append(d)
                result = mongo.db.panel_data.update_one({'_id': ObjectId(id),'data.rtsp_url': total_rtsp_url}, {'$set':{'data':empty_list}})
                if result.matched_count > 0:
                    pass
                else:
                    pass
            ppe_result_data = mongo.db.ppera_cameras.find_one({'rtsp_url':total_rtsp_url, 'cameraname': total_data_camera_name})
            if ppe_result_data is not None:
                ppe_result_data['_id'] = str(ppe_result_data['_id'])
                id = ppe_result_data['_id']
                result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id),'rtsp_url': total_rtsp_url}, {'$set':{'cameraid': total_camera_id}})
                if result.matched_count > 0:
                    pass
                else:
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
        print("print(,)", str(error))
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- update_cam_id 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    except Exception as error :
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- update_cam_id 2", str(error), " ----time ---- ", now_time_with_time()]))
    return '200'



def check_HYDRAPneumatic_data_is_empty_(all_data_to_check_panel):
    if len(all_data_to_check_panel) != 0:
        if dictionary_key_exists(all_data_to_check_panel,'hydraulic_data'):
            if len(all_data_to_check_panel['hydraulic_data']) != 0 :
                pass
        elif  dictionary_key_exists(all_data_to_check_panel,'pneumatic_data'):
            if len(all_data_to_check_panel['pneumatic_data']) != 0 :
                all_data_to_check_panel['hydraulic_data']=all_data_to_check_panel['pneumatic_data']
    return all_data_to_check_panel






def HYDRAcreate_config():
    response = []
    if 1:
    # try:
        panel_data_list = []
        main_list = []
        ip_adds = []
        fetch_panel_data = None
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
        if sheet_data is not None:
            job_sheet_name = sheet_data['job_sheet_name']
            sheet_token = sheet_data['token']
            fetch_panel_data = list(mongo.db.panel_data.find({'job_sheet_name':job_sheet_name, 'token': sheet_token,'type':{"$ne": "HT"}}))
            if len(fetch_panel_data) != 0:
                for ol__io, i in enumerate(fetch_panel_data):
                    return_data = check_HYDRAPneumatic_data_is_empty_(i['data'])
                    if isEmpty(return_data) :
                        video_names = i['video_names']
                        # try:
                        ip_address = i['data']['ip_address']
                        cam_name = i['data']['camera_name']
                        rtsp = i['data']['rtsp_url']
                        hydraulic_data = i['data']['hydraulic_data']
                        if len(hydraulic_data) != 0:
                            require_panel_data = {'ip_adrs': ip_address, 'camera_name': cam_name,'rtsp_url': rtsp,'video_names':video_names,
                                                'hydraulic_data':hydraulic_data, 'ai_solution': ['PPE'],'roi_ra': []}
                            panel_data_list.append(require_panel_data)
                            main_list.append(require_panel_data)
                            ip_adds.append({'ip_adrs': ip_address})
                        # except Exception as error:
                        #     print('================ line 362 -', error)
                        #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- HYDRAc22reate_config 1", str(error), " ----time ---- ", now_time_with_time()]))
                    else:
                        print('empty panel data --------------- ')
            else:
                print('================== NO PANEL AND PPE CAMERAS =====================')
        else:
            print('================== NO PANEL AND PPE CAMERAS =====================')
        response = verify_ip_address(main_list)
        print("verify ip address --- main_list===", len(response))
        if len(response) != 0:
            response = {'data': response}
        else:
            response = []
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
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- HYDRAcreate_222config 2", str(error), " ----time ---- ", now_time_with_time()]))
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    # except Exception as error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- HYDRAcrea22te_config 3", str(error), " ----time ---- ", now_time_with_time()]))
    return response


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
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- extend_roi_points 1", str(error), " ----time ---- ", now_time_with_time()]))
        return data
    

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
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] muti_isolation_jobs -- relocate_data_points 1", str(error), " ----time ---- ", now_time_with_time()]))
        return data



"""Write Config File Code"""
def write_connfig(response):
    sample_config_file = os.path.join(str(os.getcwd()) + '/' +  'smaple_files', 'esi_sample_config.txt')
    deepstream_config_path = (get_current_dir_and_goto_parent_dir()+ '/docketrun_eis_monitor/hydra_configs')
    handle_uploaded_file(deepstream_config_path)
    config_file = os.path.join(deepstream_config_path, 'config.txt')
    config_analytics_file = os.path.join(deepstream_config_path,'config_analytics.txt')
    lines = ['[property]', 'enable=1', 'config-width=960','config-height=544', 'osd-mode=2', 'display-font-size=12', '']
    index = 0
    require_data = []
    roi_enable_cam_ids = []
    ppe_enable_cam_ids = []
    for Cherry, x in enumerate(response):
        print("x---------------- ",x)
        x['camera_id'] = int(index) + 1
        require_data.append(x)
        if  len(x['hydraulic_data']) != 0:
            lines.append('[roi-filtering-stream-{0}]'.format(index))
            lines.append('enable=1')            
            for ___p, vlaue in enumerate(x['hydraulic_data']):
                roi_bbox = vlaue['bbox']
                vlaue['bbox'] = extend_roi_points(data=vlaue['bbox'])
                vlaue['bbox'] = relocate_data_points(vlaue['bbox'])
                roi_bbox = vlaue['bbox']
                if str(vlaue['panel_no']) :
                    panel_num = str(vlaue['panel_no'])
                lines.append('roi-PNL-{0} = {1}'.format(panel_num, roi_bbox))
            lines.append('inverse-roi=0')
            lines.append('class-id=0;1;2;\n')
        index += 1
    with open(config_analytics_file, 'w') as f:
        for item in lines:
            f.write('%s\n' % item)
    lines = []
    with open(sample_config_file) as file:
        for young_TIGER, line in enumerate(file):
            if line.strip() == '[application]':
                lines.append('[application]')
                lines.append('enable-perf-measurement=0')
                lines.append('perf-measurement-interval-sec=5')
            elif line.strip() == '[tiled-display]':
                columns = int(math.sqrt(len(require_data)))
                rows = int(math.ceil(len(require_data) / columns))
                lines.append('[tiled-display]')
                lines.append('enable=1')
                lines.append('rows={0}'.format(str(rows)))
                lines.append('columns={0}'.format(str(columns)))
                lines.append('width=960')
                lines.append('height=544')
                lines.append('gpu-id=0')
                lines.append('nvbuf-memory-type=0')
            elif line.strip() == '[sources]':
                for n, x in enumerate(require_data):
                    cam_id = '{0}'.format(int(n) + 1)
                    roi_enable_cam_ids_exist = roi_enable_cam_ids.count(int(cam_id))
                    ppe_enable_cam_ids_exist = ppe_enable_cam_ids.count(int(cam_id))
                    if (roi_enable_cam_ids_exist > 0 or ppe_enable_cam_ids_exist > 0):
                        find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                        if find_data is not None:
                            if find_data['rtsp_flag'] == '1':
                                if 'rtsp' in x['rtsp_url']:
                                    x['rtsp_url'] = x['rtsp_url'].replace('rtsp', 'rtspt')
                        if x['video_names'] is not None:
                            uri = x['video_names']
                            lines.append('[source{0}]'.format(n))
                            lines.append('enable=1')
                            lines.append('type=3')
                            lines.append('uri = file://../../test_videos/{0}'.format(uri))
                            lines.append('num-sources=1')
                            lines.append('gpu-id=0')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('latency=500')
                            lines.append('camera-id={0}'.format(int(n) + 1))
                            lines.append('camera-name = {0}'.format(x['camera_name']))
                            lines.append('drop-frame-interval = 0\n')
                        elif x['rtsp_url'] is not None:
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
                            lines.append('drop-frame-interval = 3\n')
                    elif x['rtsp_url'] is not None:
                        uri = x['rtsp_url']
                        lines.append('[source{0}]'.format(n))
                        lines.append('enable=0')
                        lines.append('type=4')
                        lines.append('uri = {0}'.format(uri))
                        lines.append('num-sources=1')
                        lines.append('gpu-id=0')
                        lines.append('nvbuf-memory-type=0')
                        lines.append('latency=500')
                        lines.append('camera-id={0}'.format(int(n) + 1))
                        lines.append('camera-name = {0}'.format(x['camera_name']))
                        lines.append('drop-frame-interval = 3\n')
                    elif x['rtsp_url'] is not None:
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
                        lines.append('drop-frame-interval = 3\n')
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
                lines.append('batch-size={0}'.format(len(require_data)))
                lines.append('batched-push-timeout=40000')
                lines.append('width=960')
                lines.append('height=544')
                lines.append('enable-padding=0')
                lines.append('nvbuf-memory-type=0')
            elif line.strip() == '[primary-gie]':
                lines.append('[primary-gie]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('batch-size={0}'.format(len(require_data)))
                lines.append('bbox-border-color0=0;1;0;0.7')
                lines.append('bbox-border-color1=0;1;1;0.7')
                lines.append('bbox-border-color2=0;1;0;0.7')
                lines.append('bbox-border-color3=0;1;0;0.7')
                lines.append('nvbuf-memory-type=0')
                lines.append('interval=0')
                lines.append('gie-unique-id=1')
                lines.append('config-file = ../../models/config_infer_primary_tsk_v_0_2.txt')
            elif line.strip() == '[tracker]':
                lines.append('[tracker]')
            elif line.strip() == '[nvds-analytics]':
                lines.append('[nvds-analytics]')
            elif line.strip() == '[tests]':
                lines.append('[tests]')
            elif line.strip() == '[docketrun-analytics]':
                lines.append('[docketrun-analytics]')
                lines.append('smart-record-stop-buffer = 2\n')
            elif line.strip() == '[docketrun-image]':
                lines.append('[docketrun-image]')
            elif line.strip() == '[restricted-access]':
                lines.append('[restricted-access]')
            elif line.strip() == '[ppe-type-1]':
                lines.append('[ppe-type-1]')
                empty_ppe_ls = []
                for OPI_, n in enumerate(ppe_enable_cam_ids):
                    text = str(n) + ';'
                    empty_ppe_ls.append(text)
                string2 = ''
                if len(empty_ppe_ls) == 0:
                    string2 = '-1;'
                    lines.append('camera-ids = {0}'.format(string2))
                if len(empty_ppe_ls) != 0:
                    string2 = ''
                    lines.append('camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
            else:
                lines.append(line.strip())
    with open(config_file, 'w') as f:
        for O_O_O, item in enumerate(lines):
            f.write('%s\n' % item)
    return roi_enable_cam_ids, ppe_enable_cam_ids, require_data



def HYDRACAMERAIDupdate():
    ret = {'message':'something went wrong with create config .','success': False}
    getdata_response = HYDRAcreate_config()
    print('9999999999999999999999999999999999999999999999',len(getdata_response))
    if len(getdata_response) != 0:
        response = getdata_response['data']
        function__response = write_connfig(response)
        require_cam_ids_data = {'data': list(function__response)}
        return_data_update_camera = update_cam_id(require_cam_ids_data)
        if return_data_update_camera == '200':
            ret = {'message': 'config files are created successfully.','success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'there is no data found for create config file '
    return ret


@job_sheet_api.route('/create_HyDra_config', methods=['GET'])
def HYDRACREATECONFIG():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        esi_app_set_ESI_monitoring_started(True)
        return_data = HYDRACAMERAIDupdate()
        if return_data:
            stop_application_for_esi_creating_config()
            if return_data['success'] == True:
                # esi_app_set_ESI_monitoring_started(False)
                ret = {'message':'esi config files are created successfully.', 'success': True}
            else:
                ret['message' ] = '  some thing went wrong  creating config files.'
        else:
            ret['message'] = 'data not found to create config files.'
    else:
        ret = ret
    return ret