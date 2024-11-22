
from Data_recieving_and_Dashboard.packages import *
panel_status = Blueprint('panel_status', __name__)


def sum_array(arr):
    sum = 0
    for i in arr:
        sum = sum + i
    return sum


def check_panel_id(panel_data):
    num_panels_count = 0
    panel_id = []
    if type(panel_data) == list:
        if len(panel_data) != 0:
            for x_val in panel_data:
                roi_data = x_val['roi_data']
                bbox = roi_data['bbox']
                if x_val['panel_id'] != 'NA' and roi_data['bbox'
                    ] != '' and roi_data['bbox'] != ' ':
                    panel_id.append(x_val['panel_id'])
                    num_panels_count += 1
                    pass
                    res = True, panel_id, num_panels_count
                else:
                    res = False, panel_id, num_panels_count
        else:
            res = False, panel_id, num_panels_count
    return res


def get_list_working_not_working_cam_list(find_data):
    working_cam_name = []
    not_working_cam_name = []
    panel_id_data = []
    count__panel_data = 0
    for index, p_data in enumerate(find_data['data']):
        if p_data['ip_address'] == None:
            require_data_details.append(p_data['ip_address'])
            if p_data['rtsp_url'] != None:
                testing_fun = split_rtsp_url(p_data['camera_brand'], p_data['rtsp_url'])
                testing_ip_working = final_ping(testing_fun['ipaddress'])
                if testing_ip_working is True:
                    working_cam_name.append(p_data)
                    panel_id_data.append(p_data['panel_data'])
                    count__panel_data += 1
                    pass
                else:
                    not_working_cam_name.append(p_data['rtsp_url'])
            else:
                image_namereplace = replace_spl_char(p_data['plant'] + '_' +
                    p_data['area'])
                test_rtsp_response_image = verify_rtsp(p_data['rtsp_url'],
                    image_namereplace)
                if test_rtsp_response_image:
                    require_data_details.append(p_data['rtsp_url'])
                    working_cam_name.append(p_data)
                    panel_id_data.append(p_data['panel_data'])
                    count__panel_data += 1
                    pass
                else:
                    not_working_cam_name.append(p_data['rtsp_url'])
        else:
            testing_ip_working = final_ping(p_data['ip_address'])
            if testing_ip_working is True:
                panel_id_data.append(p_data['panel_data'])
                working_cam_name.append(p_data)
                count__panel_data += 1
                pass
            else:
                not_working_cam_name.append(p_data['rtsp_url'])
    return not_working_cam_name, working_cam_name, count__panel_data


@panel_status.route('/camera_wise_count_panel_jobs', methods=['GET'])
def camera_wise_count_panel_jobs():
    result = {'message':
        "Something went wrong with 'camera_wise_count_panel_jobs' API.",
        'success': False}
    job_sheet_data = mongo.db.job_sheet_details.find({'status': 1}).sort(
        'timestamp', -1).limit(1)
    for i in job_sheet_data:
        i['_id'] = str(i['_id'])
        panel_db_data = mongo.db.panel_data.find({'job_sheet_name': i[
            'job_sheet_name'], 'token': i['token'], 'sheet_status': True})
        empty_ls = []
        for jobsheet in panel_db_data:
            jobsheet['_id'] = str(jobsheet['_id'])
            data = jobsheet['data']
            total_jobs = 0
            for data_x in data:
                fun_response = check_panel_id(data_x['panel_data'])
                if type(fun_response) == tuple:
                    if fun_response[0] == True:
                        dict_values = {'camera_name': data_x['camera_name'],
                            'camera_rtsp': data_x['rtsp_url'], 'total_jobs':
                            0, 'proccessed_jobs': 0, 'not_proccessed': 0}
                        dict_values['total_jobs'] = len(fun_response[1])
                        proccess_jobs = 0
                        not_proccessed_jobs = 0
                        for ids in fun_response[1]:
                            riro_data = mongo.db.riro_data.find({'camera_name': data_x['camera_name'],'camera_rtsp': data_x['rtsp_url'],'panel_no': ids})
                            riro_data = list(riro_data)
                            if len(riro_data) != 0:
                                proccess_jobs += 1
                                dict_values['proccessed_jobs'] = proccess_jobs
                            else:
                                not_proccessed_jobs += 1
                                dict_values['not_proccessed' ] = not_proccessed_jobs
                        empty_ls.append(dict_values)
        if len(empty_ls) != 0:
            result = {'message': empty_ls, 'success': True}
        else:
            result = {'message': empty_ls, 'success': False}
    return result


@panel_status.route('/overall_panel_jobs_count', methods=['GET'])
def overall_panel_jobs_count():
    result = {'message': 'Something went wrong with count_panel_jobs API.',
        'success': False}
    job_sheet_data = mongo.db.job_sheet_details.find({'status': 1}).sort(
        'timestamp', -1).limit(1)
    for i in job_sheet_data:
        i['_id'] = str(i['_id'])
        panel_db_data = mongo.db.panel_data.find({'job_sheet_name': i[
            'job_sheet_name'], 'token': i['token'], 'sheet_status': True})
        empty_ls = []
        total_jobs = 0
        proccess_jobs = 0
        proccess_jobs_ls = []
        not_proccessed_jobs = 0
        not_proccessed_jobs_ls = []
        for jobsheet in panel_db_data:
            jobsheet['_id'] = str(jobsheet['_id'])
            data = jobsheet['data']
            for data_x in data:
                print('DATA FOR TESTING __________________________', data_x)
                dict_values = {'total_jobs': 0, 'proccessed_jobs': 0,
                    'not_proccessed': 0}
                fun_response = check_panel_id(data_x['panel_data'])
                print('CHECK FUNCTIOON RESPONSE:----------', fun_response)
                if type(fun_response) == tuple:
                    if fun_response[0] == True:
                        total_jobs += 1
                        dict_values['total_jobs'] = total_jobs
                        for fin_ip in fun_response[1]:
                            print('FUNCTION IP', fin_ip)
                            riro_data = mongo.db.riro_data.find({
                                'camera_name': data_x['camera_name'],
                                'camera_rtsp': data_x['rtsp_url'],
                                'panel_no': fin_ip})
                            riro_data = list(riro_data)
                            if len(riro_data) != 0:
                                proccess_jobs += 1
                                dict_values['proccessed_jobs'] = proccess_jobs
                            else:
                                not_proccessed_jobs += 1
                                dict_values['not_proccessed'
                                    ] = not_proccessed_jobs
                        empty_ls.append(dict_values)
    not_proc_add = 0
    proc_add = 0
    ttl_job = 0
    for ls in empty_ls:
        not_proc_add = not_proc_add + ls['not_proccessed']
        proc_add = proc_add + ls['proccessed_jobs']
        ttl_job = ttl_job + ls['total_jobs']
    dict_val = {'proccessed_counts': proc_add, 'not_proccessed_counts':
        not_proc_add, 'total_jobs': ttl_job}
    if len(empty_ls) != 0:
        result = {'message': dict_val, 'success': True}
    else:
        result = {'message': dict_val, 'success': False}
    return result


@panel_status.route('/camera_status_panel_count', methods=['GET'])
def camera_status_panel_count():
    result = {'message':
        "Something went wrong with 'camera_status_panel_count' api.",
        'success': False}
    job_sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},
        sort=[('timestamp', pymongo.DESCENDING)])
    panel_data_cam_status = mongo.db.panel_data.find({'job_sheet_name':
        job_sheet_data['job_sheet_name'], 'token': job_sheet_data['token'],
        'sheet_status': True})
    panel_data_cam_status = list(panel_data_cam_status)
    test = []
    n_w_cam = []
    working_cam_name_count_test = 0
    not_working_cam_name_count_test = 0
    working_panel_count = 0
    not_working_panel_count = 0
    for find_data in panel_data_cam_status:
        function_response = get_list_working_not_working_cam_list(find_data)
        if function_response[2] != 0:
            working_cam_name_count_test += 1
            data = find_data['data']
            for x_val in data:
                panel_data_val = x_val['panel_data']
                if type(panel_data_val) == list:
                    if len(panel_data_val) != 0:
                        check_panel_id_func = check_panel_id(panel_data_val)
                        test.append(check_panel_id_func[2])
                        working_panel_count = sum_array(test)
                        break
        elif function_response[2] == 0:
            not_working_cam_name_count_test += 1
            data = find_data['data']
            for x_val in data:
                panel_data_val = x_val['panel_data']
                if type(panel_data_val) == list:
                    if len(panel_data_val) != 0:
                        check_panel_id_func = check_panel_id(panel_data_val)
                        if check_panel_id_func[0] == True:
                            n_w_cam.append(check_panel_id_func[2])
                            not_working_panel_count = sum_array(n_w_cam)
                            break
    require_cam_counts = {'total_count': {'total_camera_counts': 
        not_working_cam_name_count_test + working_cam_name_count_test,
        'total_panel_counts': not_working_panel_count + working_panel_count
        }, 'not_working_counts': {'not_working_camera_count':
        not_working_cam_name_count_test, 'not_working_panel_count':
        not_working_panel_count}, 'working_data_counts': {
        'working_camera_count': working_cam_name_count_test,
        'working_panel_count': working_panel_count}}
    result = {'message': require_cam_counts, 'success': True}
    return result


@panel_status.route('/camera_wise_panel_count', methods=['GET'])
def camera_wise_panel_count():
    result = {'message':
        "Something went wrong with 'camera_wise_panel_count' api.",
        'success': False}
    job_sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},
        sort=[('timestamp', pymongo.DESCENDING)])
    panel_data_cam_status = mongo.db.panel_data.find({'job_sheet_name':
        job_sheet_data['job_sheet_name'], 'token': job_sheet_data['token'],
        'sheet_status': True})
    panel_data_cam_status = list(panel_data_cam_status)
    test = []
    n_w_cam = []
    require_data_details = []
    not_require_data_details = []
    working_cam_name_count_test = 0
    not_working_cam_name_count_test = 0
    for find_data in panel_data_cam_status:
        function_response = get_list_working_not_working_cam_list(find_data)
        require_panel_data = {'job_sheet_name': None, 'camera_name': None,
            'camera_rtsp': None, 'camera_ip': None, 'num_panels': None,
            'image_name': None, 'token': None}
        if function_response[2] != 0:
            working_cam_name_count_test += 1
            data = find_data['data']
            for x_val in data:
                panel_data_val = x_val['panel_data']
                if type(panel_data_val) == list:
                    if len(panel_data_val) != 0:
                        check_panel_id_func = check_panel_id(panel_data_val)
                        test.append(check_panel_id_func[2])
                        working_panel_count = sum_array(test)
                        require_panel_data['job_sheet_name'] = find_data[
                            'job_sheet_name']
                        require_panel_data['token'] = find_data['token']
                        require_panel_data['camera_ip'] = x_val['ip_address']
                        require_panel_data['camera_name'] = x_val['camera_name'
                            ]
                        require_panel_data['camera_rtsp'] = x_val['rtsp_url']
                        require_panel_data['image_name'] = x_val['image_name']
                        require_panel_data['num_panels'] = check_panel_id_func[
                            2]
                        require_data_details.append(require_panel_data)
                        break
        else:
            not_working_cam_name_count_test += 1
            data = find_data['data']
            for x_val in data:
                panel_data_val = x_val['panel_data']
                if type(panel_data_val) == list:
                    if len(panel_data_val) != 0:
                        check_panel_id_func = check_panel_id(panel_data_val)
                        n_w_cam.append(check_panel_id_func[2])
                        not_working_panel_count = sum_array(n_w_cam)
                        require_panel_data['job_sheet_name'] = find_data['job_sheet_name']
                        require_panel_data['token'] = find_data['token']
                        require_panel_data['camera_ip'] = x_val['ip_address']
                        require_panel_data['camera_name'] = x_val['camera_name']
                        require_panel_data['camera_rtsp'] = x_val['rtsp_url']
                        require_panel_data['image_name'] = x_val['image_name']
                        require_panel_data['num_panels'] = check_panel_id_func[2]
                        not_require_data_details.append(require_panel_data)
                        break
    require_cam_counts = {'not_working_camera_details':
        not_require_data_details, 'working_data_counts': require_data_details}
    result = {'message': require_cam_counts, 'success': True}
    return result


@panel_status.route('/violation_data_counts', methods=['GET'])
def violation_data_counts():
    result = {'message':
        "Something went wrong with 'violation_data_counts' API.", 'success':
        False}
    job_sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},
        sort=[('timestamp', pymongo.DESCENDING)])
    panel_data_cam_status = mongo.db.panel_data.find({'job_sheet_name':
        job_sheet_data['job_sheet_name'], 'token': job_sheet_data['token'],
        'sheet_status': True})
    panel_data_cam_status = list(panel_data_cam_status)
    for panel_data in panel_data_cam_status:
        for data_value in panel_data['data']:
            check_fun = check_panel_id(data_value['panel_data'])
            if type(check_fun) == tuple:
                if check_fun[0] == True:
                    for panel_ids in check_fun[1]:
                        riro_data = mongo.db.riro_data.find({'camera_name':
                            data_value['camera_name'], 'camera_rtsp':
                            data_value['rtsp_url'], 'panel_no': panel_ids})
                        riro_data = list(riro_data)
                        violation_data_count_ls = []
                        for x_riro_data in riro_data:
                            print('RIRO DATA:------------------',
                                x_riro_data['panel_no'])
                            violation_data = mongo.db.data.find({
                                'camera_name': x_riro_data['camera_name'],
                                'camera_rtsp': x_riro_data['camera_rtsp'],
                                'timestamp': {'$gte': x_riro_data[
                                'person_in_time'], '$lt': x_riro_data[
                                'person_out_time']}, 'analyticstype':'PPE_TYPE1'})
                            violation_data_count = list(violation_data)
                            print('VIOLATION DATA :-------------------',
                                x_riro_data['person_in_time'],
                                violation_data_count, x_riro_data['person_out_time'])
                            if len(violation_data_count) != 0:
                                for i_viol_val in violation_data_count:
                                    obj_data = i_viol_val['object_data']
                                    for obj_val in obj_data:
                                        if obj_val['class_name'] == 'person':
                                            print('OBJECT VALUE:', obj_val)
                                            if x_riro_data['panel_no'] in obj_val[
                                                'pannel_details']:
                                                result = {'message': {'job_sheet_name':
                                                    job_sheet_data['job_sheet_name'],
                                                    'token': job_sheet_data['token'],
                                                    'violation_data_count': len(
                                                    violation_data_count)}, 'status': True}
                                            else:
                                                result = {'message': 'Data not found.','status': False}
                            else:
                                result = {'message': 'Data not found.',
                                    'status': False}
    return result


@panel_status.route('/detect_not_detected_panel_counts', methods=['GET'])
def detect_not_detected_panel_counts():
    result = {'message':
        "Something went wrong with 'detect_not_detected_panel_counts' API.",
        'success': False}
    job_sheet_datails = mongo.db.job_sheet_details.find_one({'status': 1},
        sort=[('timestamp', pymongo.DESCENDING)])
    print('JOB SHEET DATA:', job_sheet_datails)
    sheet_refrence_panel_data = mongo.db.panel_data.find({'job_sheet_name':
        job_sheet_datails['job_sheet_name'], 'token': job_sheet_datails[
        'token'], 'sheet_status': True})
    camera_list_detected = []
    camera_list_not_detected = []
    detected_panel_count = []
    not_detected_panel_count = []
    total_camera_list = []
    working_cam_count = []
    not_working_cam_count = []
    for panel_datas in list(sheet_refrence_panel_data):
        if panel_datas['data'] != 0:
            total_camera_list.append(panel_datas['data'])
            for data_values in panel_datas['data']:
                ip_address = data_values['ip_address']
                print('PANEL DATA:-------------------------', ip_address)
                job_sheet_data = mongo.db.job_sheet_data.find({
                    'job_sheet_name': panel_datas['job_sheet_name'],
                    'token': panel_datas['token'], 'sheet_status': True})
                job_sheet_data = list(job_sheet_data)
                for job_sht_data in job_sheet_data:
                    if type(job_sht_data['ip_address']) == list:
                        for ips in job_sht_data['ip_address']:
                            if ip_address in ips:
                                working_cam_count.append(ip_address)
                                print(
                                    'length WORKING CAMERA IP:--------------------'
                                    , len(working_cam_count))
                            elif len(ips) == 0:
                                pass
                            else:
                                not_working_cam_count.append(ip_address)
                    elif ip_address in job_sht_data['ip_address']:
                        working_cam_count.append(ip_address)
                        print('length WORKING CAMERA IP:--------------------',
                            len(working_cam_count))
                    else:
                        not_working_cam_count.append(ip_address)
                if len(data_values['panel_data']) != 0:
                    total_cameras_count = 0
                    for panel_val in data_values['panel_data']:
                        if panel_val['panel_id'] == 'NA':
                            not_detected_panel_count.append(panel_val[
                                'panel_id'])
                            if data_values not in camera_list_detected:
                                camera_list_detected.append(data_values)
                        else:
                            detected_panel_count.append(panel_val['panel_id'])
    result = {'message': [{'total_camera_count': len(total_camera_list),
        'detected_panel_count': len(detected_panel_count),
        'not_detected_panel_count': len(not_detected_panel_count),
        'total_panels_count': len(detected_panel_count) + len(
        not_detected_panel_count), 'working_cam_count': len(
        working_cam_count), 'not_working_cam_count': len(
        not_working_cam_count)}], 'success': True}
    return result
