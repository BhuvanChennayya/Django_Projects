from Data_recieving_and_Dashboard.packages import *

def append_lists(ls1, ls2):
    #iterating over list2
    for i in ls2:
        if i not in ls1:
            #appending in list1
            ls1.append(i)
    print(ls1)

def arrange_x_in_ascending_order(x, y):
    for i in range(0, len(x)):
        if x[i] < 0:
            x[i] = 0
    for i in range(0, len(y)):
        if y[i] < 0:
            y[i] = 0
    return x, y

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
        ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- extend_roi_points 2", str(error), " ----time ---- ", now_time_with_time()]))
        return data

    
def cr_fun_conf_anlytics(x,lines,  traffic_count_cls_name_cls_id):
    if len(x['cr_data']) != 0:
        cr_label_names =[]
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            cr_label_names = []
            label_name_1 = cr_value['data_object']
            for label_name in label_name_1:
                cls_label_name = label_name["class_name"]
                if compare(label_name, cr_label_names) == False:
                    # for lab_nam in label_name:
                    if cls_label_name not in cr_label_names:
                        cr_label_names.append(cls_label_name)   
            cr_name = cr_value['area_name']
            try:
                cr_value['bb_box'] =checkNegativevaluesinBbox( cr_value['bb_box'])#extend_roi_points(data=cr_value['bb_box'])
                cr_bbox = cr_value['bb_box']
            except Exception as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- cr_fun_conf_22anlytics 1", str(error), " ----time ---- ", now_time_with_time()]))
                cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
            if len(cr_bbox) != 0:
                lines.append('roi-crdcnt-{0} = {1}'.format(cr_name, cr_bbox)) 
        if x["roi_data"] != 0:
            roi__label_names = []
            for roi__val in x['roi_data']:
                if type(roi__val['label_name'])==list:
                    for roi_val___test in roi__val['label_name']:
                        if roi_val___test not in roi__label_names:
                            roi__label_names.append(roi_val___test)   
                elif type(roi__val['label_name'])==str: 
                    roi__label_names.append(roi__val['label_name'])    
                        
        roi_label_names_1 = roi__label_names
        cr_label_names_1 = cr_label_names
        append_lists(roi_label_names_1, cr_label_names_1)
        label_name_roi_cr = roi_label_names_1
        label_name_roi_cr_default = []
        if type(label_name_roi_cr)==list:
            print("label_name_roi_cr===",label_name_roi_cr)
            for cr_cls_name in label_name_roi_cr:
                print("----traffic_count_cls_name_cls_id11",traffic_count_cls_name_cls_id)
                if traffic_count_cls_name_cls_id[cr_cls_name] not in label_name_roi_cr:
                    tc_val___test = traffic_count_cls_name_cls_id[cr_cls_name]
                    label_name_roi_cr_default.append(tc_val___test)
        label_name_roi_cr_default_ls = []
        for tc_label_name_test in label_name_roi_cr_default:
            text = str(tc_label_name_test) + ';'
            label_name_roi_cr_default_ls.append(text)
        test_string = ''
        lines.append('inverse-roi=0')
        lines.append('class-id= {0}\n'.format(test_string.join(label_name_roi_cr_default_ls)))
    else:
        if x["roi_data"] != 0:
            roi__label_names = []
            print("----traffic_count_cls_name_cls_id22",traffic_count_cls_name_cls_id)
            for roi__val in x['roi_data']:
                if type(roi__val['label_name'])==list:
                    if len(roi__val['label_name']) !=0:
                        for roi_val___test in roi__val['label_name']:
                            if traffic_count_cls_name_cls_id[roi_val___test] not in roi__label_names:
                                roi_val___test = traffic_count_cls_name_cls_id[roi_val___test]
                                roi__label_names.append(roi_val___test) 
                if type(roi__val['label_name'])==str:
                    if traffic_count_cls_name_cls_id[roi__val['label_name']] not in roi__label_names:
                        roi_val___test = traffic_count_cls_name_cls_id[roi__val['label_name']]
                        roi__label_names.append(roi_val___test)           
        roi__empty_label_ls = []
        for tc_label_name_test in roi__label_names:
            text = str(tc_label_name_test) + ';'
            roi__empty_label_ls.append(text)
        test_string = ''
        lines.append('inverse-roi=0')
        lines.append('class-id= {0}\n'.format(test_string.join(roi__empty_label_ls)))
    return True

def compare(l1, l2):
    set1 = set(l1)
    set2 = set(l2)
    if set1 == set2:
        return True
    else:
        return False


def fun_get_str_ls(ls):
    cr_empty_label_ls = []
    for cr_label_name_test in ls:
        text = str(cr_label_name_test) + ';'
        cr_empty_label_ls.append(text)
    test_string = ''

    return cr_empty_label_ls

def roi_data_cf(x, hooter_line, index, roi_enable_cam_ids, lines, traffic_count_cls_name_cls_id):
    roi_label_names =[]
    label_name_for_hooter =[]
    if len(x['roi_data']) != 0:        
        if x['alarm_type'] is not None and x['alarm_ip_address'] is not None  and x['alarm_ip_address'] != '':
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')  
            hooteripstring = '['          
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                print("x['alarm_ip_address']==== roi details ===",roi_value)
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_dataww_cf 1", str(error), " ----time ---- ", now_time_with_time()]))
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
            # hooteripstring =hooteripstring+']' 
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
                
            print("hooteripstringhooteripstringhooteripstringhooteripstring1",hooteripstring)
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            if hooteripstring== '[' :
                hooteripstring='none'
                hooter_line.append('hooter-enable = 0')
            else:
                hooter_line.append('hooter-enable = 1')
            
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3\n')              
            #[192.168.1.46:8000,track_1];[192.168.1.46:8000,track_2]      
        else:
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
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

            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            if hooteripstring== '[' :
                hooteripstring='none'
                hooter_line.append('hooter-enable = 0')
            else:
                hooter_line.append('hooter-enable = 1')
            # hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            # hooter_line.append('hooter-enable = 0')
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            # hooter_line.append('hooter-ip = {0}'.format(x['alarm_ip_address']))
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
        roi_enable_cam_ids.append(index)
    return True

def roi_fun_no_cr_data(x, hooter_line, index, roi_enable_cam_ids, lines):
    label_name_for_hooter =[]
    roi_label_names =[]
    if len(x['roi_data']) != 0:
        if x['alarm_type'] is not None and x['alarm_ip_address'] is not None:
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_cr_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
                            [label_name_for_hooter.append(i) for i in  label_name if i not in  label_name_for_hooter]
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
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_cr_data 2", str(error), " ----time ---- ", now_time_with_time()]))
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
        for test_roi_ra, roi_value in enumerate(x['roi_data']):
            label_name = roi_value['label_name']
            roi_name = roi_value['roi_name']
            try:
                roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
            except Exception as error:
                roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_cr_data 3", str(error), " ----time ---- ", now_time_with_time()]))
            lines.append('[roi-filtering-stream-{0}]'.format(index))
            lines.append('enable=1')
            roi_bbox= checkNegativevaluesinBbox(roi_bbox)
            lines.append('roi-RA-{0} = {1}'.format(roi_name, roi_bbox))                        
        lines.append('inverse-roi=0')
        roi__label_names = []
        for roi_val in x['roi_data']:
            print("roi_val---",roi_val)
            for roi_val___test in roi_val['label_name']:
                roi__label_names.append(roi_val___test)
        roi_empty_label_ls = []
        for roi_label_name_test in ['0']:
            text = str(roi_label_name_test) + ';'
            roi_empty_label_ls.append(text)
        test_string = ''
        lines.append('class-id= {0}\n'.format(test_string.join(roi_empty_label_ls)))
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
        
def tc_fun(x, lines, index,  traffic_count_cls_name_cls_id):
    if len(x['tc_data']) != 0:
        lines.append('[line-crossing-stream-{0}]'.format(index))
        lines.append('enable=1')
        for ___p, value in enumerate(x['tc_data']):
            tc_bbox = value['line_bbox']
            arrow_pts = tc_bbox["arrow"]
            line_pts = tc_bbox["line"]
            exit_pts = arrow_pts + line_pts
            split_tc_values = exit_pts.split(';')
            fin_bbox_ls = " "
            for count, x_l in enumerate(split_tc_values[:-1]):
                try_concat = round(float(x_l))
                fin_bbox_ls_temp = str(try_concat) + ';'
                fin_bbox_ls = fin_bbox_ls + fin_bbox_ls_temp

            tc_name = str(value['area_name'])
            lines.append('line-crossing-{0} = {1}'.format(tc_name, checkNegativevaluesinBbox(fin_bbox_ls)))

        if len(x['tc_data']) != 0:
            tc_label_names = []
            for tc_val in x['tc_data']:
                for tc_val___test in tc_val['class_name']:
                    if traffic_count_cls_name_cls_id[tc_val___test] not in tc_label_names:
                        tc_val___test = traffic_count_cls_name_cls_id[tc_val___test]
                        tc_label_names.append(tc_val___test)


        tc_empty_label_ls = []
        for tc_label_name_test in tc_label_names:
            text = str(tc_label_name_test) + ';'
            tc_empty_label_ls.append(text)
        test_string = ''
        lines.append('class-id= {0}'.format(test_string.join(tc_empty_label_ls)))

        lines.append('extended=1')
        lines.append('mode=loose\n')

    return True

def cr_fun_crowd_conf(x,crowd_line, index,cameraid, cr_enable_cam_ids): 
    print("entered main function_---cr 1====")
    max_cnt_ls =[]
    min_cnt_ls =[]
    cr_label_names=[]
    if len(x['cr_data']) != 0:
        if cameraid not in cr_enable_cam_ids:
            cr_enable_cam_ids.append(cameraid)
        print("appending cr cameraids ==",cr_enable_cam_ids)
        crowd_line.append('[crdcnt{0}]'.format(index))
        crowd_line.append('enable=1')
        try_this_ls = []
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            try_this_ls.append(cr_value['full_frame'])
        print("try_this_ls====",try_this_ls)
        print("------------------------- CR MAIN FUNCTION",True in try_this_ls and False in try_this_ls)
        if True in try_this_ls and False in try_this_ls:
            crowd_line.append('process-on-full-frame = 1')
            for test_cr_ra, cr_value in enumerate(x['cr_data']):
                data_object = cr_value['data_object']
                max_cnt_par = []
                min_cnt_par = []
                label_name = []
                cr_label_names = []
                max_cnt_ls = []
                min_cnt_ls = []
                for data_obj in data_object:
                    if type(data_obj) == list:
                        for d_obj in data_obj:
                            print("DATA OBJECT:", d_obj)
                            label_name.append(d_obj['class_name'])
                            print("LABEL :--", label_name)
                            max_cnt_par.append(d_obj['max_count'])
                            print("MAX_COUNT---", max_cnt_par)
                            min_cnt_par.append(d_obj['min_count'])
                            print("MIN COUNT:", min_cnt_par)
                    else:
                        label_name.append(data_obj["class_name"])
                        print("LABEL :--", label_name)
                        max_cnt_par.append(data_obj['max_count'])
                        print("MAX_COUNT---", max_cnt_par)
                        min_cnt_par.append(data_obj['min_count'])
                        print("MIN COUNT:", min_cnt_par)

                if max_cnt_par != None:
                    if compare(max_cnt_par, max_cnt_ls) == False:
                        for max_c in max_cnt_par:
                            if max_c not in max_cnt_ls:
                                max_cnt_ls.append(max_c)
                
                if min_cnt_par != None:
                    if compare(min_cnt_par, min_cnt_ls) == False:
                        for min_c in min_cnt_par:
                            if min_c not in min_cnt_ls:
                                min_cnt_ls.append(min_c)

                if compare(label_name, cr_label_names) == False:
                    for lab_nam in label_name:
                        if lab_nam not in cr_label_names:
                            cr_label_names.append(lab_nam)
                cr_name = cr_value['area_name']
                try:
                    cr_value['bbox'] = cr_value['bb_box']#extend_roi_points(data=cr_value['bb_box'])
                    cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- cr_fun_cr3434owd_conf 1", str(error), " ----time ---- ", now_time_with_time()]))
                    cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
            test_string = ''
            cr_empty_label_ls = fun_get_str_ls(cr_label_names)
            crowd_line.append('operate-on-label = {0}'.format(test_string.join(cr_empty_label_ls)))            
            max_counts_ls = fun_get_str_ls(max_cnt_ls)
            min_counts_ls = fun_get_str_ls(min_cnt_ls)            
            crowd_line.append('max-count = {0}'.format(test_string.join(max_counts_ls)))
            crowd_line.append('min-count = {0}'.format(test_string.join(min_counts_ls)))
            crowd_line.append('data-save-time-in-sec = 3')

        if False not in try_this_ls:
            crowd_line.append('process-on-full-frame = 1')
            for test_cr_ra, cr_value in enumerate(x['cr_data']):
                data_object = cr_value['data_object']
                max_cnt_par = []
                min_cnt_par = []
                label_name = []
                cr_label_names = []
                max_cnt_ls = []
                min_cnt_ls = []
                for data_obj in data_object:
                    print("------------------", data_obj["class_name"])
                    if type(data_obj) == list:
                        for d_obj in data_obj:
                            print("DATA OBJECT:", d_obj)
                            label_name.append(d_obj['class_name'])
                            print("LABEL :--", label_name)
                            max_cnt_par.append(d_obj['max_count'])
                            print("MAX_COUNT---", max_cnt_par)
                            min_cnt_par.append(d_obj['min_count'])
                            print("MIN COUNT:", min_cnt_par)
                    else:
                        label_name.append(data_obj["class_name"])
                        print("LABEL :--", label_name)
                        max_cnt_par.append(data_obj['max_count'])
                        print("MAX_COUNT---", max_cnt_par)
                        min_cnt_par.append(data_obj['min_count'])
                        print("MIN COUNT:", min_cnt_par)


                if compare(label_name, cr_label_names) == False:
                    for lab_nam in label_name:
                        if lab_nam not in cr_label_names:
                            cr_label_names.append(lab_nam)

                if max_cnt_par != None:
                    if compare(max_cnt_par, max_cnt_ls) == False:
                        for max_c in max_cnt_par:
                            if max_c not in max_cnt_ls:
                                max_cnt_ls.append(max_c)
                
                if min_cnt_par != None:
                    if compare(min_cnt_par, min_cnt_ls) == False:
                        for min_c in min_cnt_par:
                            if min_c not in min_cnt_ls:
                                min_cnt_ls.append(min_c)

                cr_name = cr_value['area_name']
                    # cr_da['bbox'] = cr_value['bb_box']#extend_roi_points(data=cr_value['bb_box'])
                cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
                    
                # except Exception as error:
                #     cr_bbox = cr_value['bb_box']
                #     ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- cr_fun_cro33wd_conf 2", str(error), " ----time ---- ", now_time_with_time()]))
                max_counts_ls = fun_get_str_ls(max_cnt_ls)
                min_counts_ls = fun_get_str_ls(min_cnt_ls)
                cr_empty_label_ls = (cr_label_names)

                test_string = ''
            crowd_line.append('operate-on-label = {0}'.format(test_string.join(cr_empty_label_ls)))
            crowd_line.append('max-count = {0}'.format(test_string.join(max_counts_ls)))
            crowd_line.append('min-count = {0}'.format(test_string.join(min_counts_ls)))
            crowd_line.append('data-save-time-in-sec = 3\n')

        elif True not in try_this_ls:
            max_cnt_ls = []
            min_cnt_ls = []
            label_name = []
            max_cnt_par = []
            min_cnt_par = []
            cr_label_names =  []
            test_it_max = []
            test_it_min = []
            crowd_line.append('process-on-full-frame = 0')
            just_try = []
            for test_cr_ra, cr_value in enumerate(x['cr_data']):
                data_object = cr_value['data_object']
                if data_object not in just_try:
                    just_try.append(data_object)
            print("Just TRAID LOOp", just_try)

            
            for data_object_upt in just_try:
                for data_obj in data_object_upt:
                    # print("DATA OBJECT:", data_object)
                    # res = not all(data_obj.values())
                    # print("RESULT:", res)
                    # if res == False:
                    #print("*******verifying *********", data_obj)
                    if type(data_obj) == list:
                        print("11111111111111111")
                        for d_obj in data_obj:
                            label_name.append(d_obj['class_name'])
                            # print("LABEL :--", label_name)
                            max_cnt_par.append(d_obj['max_count'])
                            # print("MAX_COUNT---", max_cnt_par)
                            min_cnt_par.append(d_obj['min_count'])
                            # print("MIN COUNT:", min_cnt_par)

                    else:
                        # print("DATA OBJECT:", data_obj)
                        print("2222222222222",label_name)
                        label_name.append(data_obj["class_name"])
                        # print("LABEL :--", label_name)
                        max_cnt_par.append(data_obj['max_count'])
                        # print("MAX_COUNT---", max_cnt_par)
                        min_cnt_par.append(data_obj['min_count'])
                        # print("MIN COUNT:11111111", min_cnt_par)
                        
                    # else:
                    #     pass

            if compare(label_name, cr_label_names) == False:
                print("BEGINNING LABEl", label_name)
                for lab_nam in label_name:
                    print("data_object:----------------", len(just_try),  lab_nam)
                    if len(just_try) <= 1:
                        if lab_nam not in cr_label_names:
                            cr_label_names.append(lab_nam)  
                            print("CR LABEL lS--111111", cr_label_names)
                    else:
                        print("LABELLING NAME:", lab_nam)
                        cr_label_names.append(lab_nam)
                        print("CR LABEL lS--2222", cr_label_names)
            
            if len(cr_label_names) <=1:
                if max_cnt_par != None:
                    if compare(max_cnt_par, max_cnt_ls) == False:
                        for lab_nam in cr_label_names:
                            if lab_nam not in test_it_max:
                                for max_c in max_cnt_par:
                                    test_it_max.append(lab_nam)
                                    max_cnt_ls.append(max_c)

                            else:
                                for max_c in max_cnt_par:
                                    if max_c not in max_cnt_ls:
                                        max_cnt_ls.append(max_c)
                
                if min_cnt_par != None:
                    if compare(min_cnt_par, min_cnt_ls) == False:
                        for lab_nam in cr_label_names:
                            if lab_nam not in test_it_min:
                                for min_c in min_cnt_par:
                                    test_it_min.append(lab_nam)
                                    min_cnt_ls.append(min_c)
                            else:
                                for min_c in min_cnt_par:
                                    if min_c not in min_cnt_ls:
                                        min_cnt_ls.append(min_c)
            else:
                if max_cnt_par != None:
                    if compare(max_cnt_par, max_cnt_ls) == False:
                        for max_c in max_cnt_par:
                            max_cnt_ls.append(max_c)
                if min_cnt_par != None:
                    if compare(min_cnt_par, min_cnt_ls) == False:
                        for min_c in min_cnt_par:
                            min_cnt_ls.append(min_c)
            cr_name = cr_value['area_name']
            try:
                cr_value['bbox'] = cr_value['bb_box']#extend_roi_points(data=cr_value['bb_box'])
                cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
            except Exception as error:
                cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- 33 3", str(error), " ----time ---- ", now_time_with_time()]))
            test_string = ''

            if len(data_object) <= 1:
                len_label_nam = len(cr_label_names)
                rem_max_lab = max_cnt_ls[-(len(cr_label_names)):]
                cr_empty_label_ls = fun_get_str_ls(cr_label_names)
                max_counts_ls = fun_get_str_ls(rem_max_lab)
                rem_min_lab = min_cnt_ls[-(len(cr_label_names)):]
                min_counts_ls = fun_get_str_ls(rem_min_lab)
                crowd_line.append('operate-on-label = {0}'.format(test_string.join(cr_empty_label_ls)))
                crowd_line.append('max-count = {0}'.format(test_string.join(max_counts_ls)))
                crowd_line.append('min-count = {0}'.format(test_string.join(min_counts_ls)))
                crowd_line.append('data-save-time-in-sec = 3\n')

        
    else:
        crowd_line.append('[crdcnt{0}]'.format(index))
        # crowd_line.append('[crdcnt{0}]')
        crowd_line.append('enable=0')
        crowd_line.append('process-on-full-frame = 0')
        crowd_line.append('operate-on-label = None;')
        crowd_line.append('max-count = 0;')
        crowd_line.append('min-count = 0;')
        crowd_line.append('data-save-time-in-sec = 3\n')

    return True


def cr_fun_conf_analytics(x,  lines):
    cr_label_names=[]
    print("entered analytics firstfunctions-===")
    if len(x['cr_data']) != 0:
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            print("cr_valuecr_valuecr_valuecr_value",cr_value)
            label_name = cr_value['data_object'][0]['class_name']
            if compare(label_name, cr_label_names) == False:
                cr_label_names.append(label_name)
            cr_name = cr_value['area_name']
            try:
                cr_value['bb_box'] =checkNegativevaluesinBbox(cr_value['bb_box']) #extend_roi_points(data=cr_value['bb_box'])
                cr_bbox = cr_value['bb_box']
            except Exception as error:
                cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- cr_fun_conf_222analytics 2", str(error), " ----time ---- ", now_time_with_time()]))
            if len(cr_bbox) != 0:
                lines.append('roi-crdcnt-{0} = {1}'.format(cr_name, cr_bbox))

        cr_label_names =['0','2']
        cr_empty_label_ls = []
        for tc_label_name_test in cr_label_names:
            text = str(tc_label_name_test) + ';'
            cr_empty_label_ls.append(text)
        test_string = ''
        

        lines.append('inverse-roi=0')
        lines.append('class-id= {0}\n'.format(test_string.join(cr_empty_label_ls)))
    return True



def cr_fun_conf_analyticsPASSINGWRITE(x, index, lines):
    cr_label_names=[]
    print("entered ===second function ")
    if len(x['cr_data']) != 0:
        lines.append('[roi-filtering-stream-{0}]'.format(str(index)))
        lines.append('enable=1')
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            print("cr_valuecr_vaanalyticsPASSINGWRITEluecr_valuecr_value",cr_value)
            label_name = cr_value['data_object'][0]['class_name']
            if compare(label_name, cr_label_names) == False:
                cr_label_names.append(label_name)
            cr_name = cr_value['area_name']
            try:
                cr_value['bb_box'] =checkNegativevaluesinBbox(cr_value['bb_box']) #extend_roi_points(data=cr_value['bb_box'])
                cr_bbox = cr_value['bb_box']
            except Exception as error:
                cr_bbox = checkNegativevaluesinBbox(cr_value['bb_box'])
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- cr_fun_conf_333analytics 2", str(error), " ----time ---- ", now_time_with_time()]))
            if len(cr_bbox) != 0:
                lines.append('roi-crdcnt-{0} = {1}'.format(cr_name, cr_bbox))

        cr_label_names_default = []


        cr_empty_label_ls = []
        cr_label_names_default =['0','2']
        for tc_label_name_test in cr_label_names_default:
            text = str(tc_label_name_test) + ';'
            cr_empty_label_ls.append(text)
        test_string = ''
        lines.append('inverse-roi=0')
        lines.append('class-id= {0}\n'.format(test_string.join(cr_empty_label_ls)))
    return True



def ppe_fun(x, index, ppe_enable_cam_ids):
    if type(x['ppe_data']) == dict:
        if isEmpty(x['ppe_data']):
            ppe_objects = ['vest', 'helmet', 'shoes']
            for keys, val in x['ppe_data'].items():
                if keys in ppe_objects:
                    if (val == True and index + 1 not in ppe_enable_cam_ids):
                        (to_check_the_truck_label_in_roi_data) = []
                        if len(x['roi_data']) != 0:
                            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                label_name = roi_value['label_name']
                                if len(label_name) == 1:
                                    if ('truck' in label_name):
                                        to_check_the_truck_label_in_roi_data.append(index + 1)
                                elif len(label_name) > 1:
                                    if ('truck' in label_name and 'person' in label_name):
                                        pass
                            if len(to_check_the_truck_label_in_roi_data) == 0:
                                ppe_enable_cam_ids.append(index)
                        else:
                            ppe_enable_cam_ids.append(index )
    elif type(x['ppe_data']) == list:
        if len(x['ppe_data']) != 0:
            if len(x['ppe_data']) == 1:
                dictionary_of_ppe = x['ppe_data'][0]
                if type(dictionary_of_ppe) == dict:
                    if isEmpty(dictionary_of_ppe):
                        ppe_objects = ['vest', 'helmet', 'shoes']
                        for keys, val in dictionary_of_ppe.items():
                            if keys in ppe_objects:
                                if (val == True and index + 1 not in ppe_enable_cam_ids):
                                    (to_check_the_truck_label_in_roi_data) = []
                                    if len(x['roi_data']) != 0:
                                        for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                            (label_name) = (roi_value['label_name'])
                                            if len(label_name) == 1:
                                                if ('truck' in label_name):
                                                    to_check_the_truck_label_in_roi_data.append(index + 1)
                                            elif len(label_name) > 1:
                                                if ('truck' in label_name and 'person' in label_name):
                                                    pass
                                        if len(to_check_the_truck_label_in_roi_data) == 0:
                                            ppe_enable_cam_ids.append(index )
                                    else:
                                        ppe_enable_cam_ids.append(index )




# def WRITEMULTICONFIG(response):
#     allWrittenSourceCAmIds =[]
#     classId = '0'
#     numberofsources_= 4
#     new_response = split_list(response,numberofsources_)
#     camera_id =1 
#     modelconfigfile = '/objectDetector_Yolo/config_infer_primary_yoloV3_1.txt'
#     modelconfigwrite = []
#     sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'phase_one_sample_config.txt')
#     deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/docketrun_app'+'/configs'
#     yolo_config_path = get_current_dir_and_goto_parent_dir() + '/models/objectDetector_Yolo'
#     traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models'
#     if not os.path.exists(deepstream_config_path):
#         os.makedirs(deepstream_config_path)
#     if not os.path.exists(yolo_config_path):
#         os.makedirs(yolo_config_path)
#     if not os.path.exists(traffic_config_path):
#         os.makedirs(traffic_config_path)         
#     remove_text_files(deepstream_config_path)  
#     modelthreshold = getthreshholdmodelconfig_details()
#     person_threshold = '0.7'
#     helmet_threshold = '0.5'
#     vest_threshold = '0.5'
#     if modelthreshold is not None:
#         # print("modelthreshold================",modelthreshold)
#         if len(modelthreshold['threshold']) !=0:
#             for new,classname in enumerate(modelthreshold['threshold']):
#                 if classname['class']=='person':
#                     if classname['value'] is not None:
#                         if int(classname['value']) >0:
#                             person_threshold = int(classname['value'])/100
#                             if person_threshold==1:
#                                 person_threshold ='0.9'
#                         else:
#                             person_threshold = '0.0'           
#                 elif  classname['class']=='helmet':
#                     if classname['value'] is not None:
#                         if int(classname['value']) >0:
#                             helmet_threshold =  int(classname['value'])/100
#                             if helmet_threshold==1:
#                                 helmet_threshold ='0.9'
#                         else:
#                             helmet_threshold ='0.0' 
#                 elif  classname['class']=='vest':
#                     if classname['value'] is not None:
#                         if int(classname['value']) >0:
#                             vest_threshold = int(classname['value'])/100
#                             if vest_threshold==1:
#                                 vest_threshold ='0.9'
#                         else:
#                             vest_threshold ='0.0'
#     model_config_details = get_model_config_details()
#     if model_config_details is not None:
#         if model_config_details['modeltype'] == 'yolo':
#             classId = model_config_details['objectDetector_Yolo']['class_id']
#             modelconfigfile = model_config_details['objectDetector_Yolo']['modelpath']
            

#         elif model_config_details['modeltype'] == 'trafficcam':
#             classId = model_config_details['trafficcamnet']['class_id']
#             modelconfigfile = model_config_details['trafficcamnet']['modelpath']

#         elif model_config_details['modeltype'] == 'people':
#             classId = model_config_details['peoplenet']['class_id']
#             modelconfigfile = model_config_details['peoplenet']['modelpath']
#     for config_index, writingresponse in enumerate(new_response):  
#         config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
#         crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
#         config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
#         hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
#         lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', 'display-font-size=12', '']
#         truck_lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', 'display-font-size=12', '']
#         # index = 0
#         roi_enable_cam_ids = []
#         ppe_enable_cam_ids = []
#         traffic_count_enabledcameraids=[]
#         cr_enable_cam_ids = []
#         tc_label_names = []
#         truck_cam_ids_exist = []
#         truck_final_cam_ids = []
#         normal_config_file = 0
#         truck_conifg_file = 0
#         final_roi_existed_cam_ids = []
#         final_truck_cam_ids = []
#         hooter_line = []
#         crowd_line = []       
#         PPEFINALCAMERAIDS =[]
#         traffic_count_cls_name_cls_id = {"person": classId, "car": "1", "bike": "3"}
#         print("length == === ", len(writingresponse))
#         for index, x in enumerate(writingresponse):
#             x['cameraid'] = camera_id
#             if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
#                 if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
#                     print("***************111111************")
#                     roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # if x['cr_data']:
#                     #     if x['cr_data'][0]['full_frame'] == False:
#                     #         if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                     #             cr_fun_conf_analytics(x,  lines)
#                     #         else:
#                     #             cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index)
#                     res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids)
                    
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
#                     print("TC-CR_PPE===2")
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     if x['cr_data']:    
#                         if x['cr_data'][0]['full_frame'] == False:
#                             if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                                 cr_fun_conf_analytics(x,  lines)
#                             else:
#                                 cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index)

#                     res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids)
                    
#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
#                     print("TC-CR_RA===3")
#                     roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)                    
#                     # if len(x['cr_data']) !=0:
#                     #     cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # if x['cr_data']:
#                     #     if x['cr_data'][0]['full_frame'] == False:
#                     #         if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                     #             cr_fun_conf_analytics(x,  lines)
#                     #         else:
#                     #             cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index)
#                     res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids)
                    
#                 # elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
#                 #     print("TC-ra_===4")
#                 #     roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids, lines,  traffic_count_cls_name_cls_id)
                   
#                 #     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
#                 #     if tc_fun_conf_anlytics_file:
#                 #         traffic_count_enabledcameraids.append(index)
#                 #     res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids)
                    
#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
#                     print("cr-ra_PPE===5")
#                     roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,lines, traffic_count_cls_name_cls_id)
#                     # if len(x['cr_data']) !=0:
#                     #     cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # if x['cr_data']:
#                     #     if x['cr_data'][0]['full_frame'] == False:
#                     #         if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                     #             cr_fun_conf_analytics(x,  lines)
#                     #         else:
#                     #             cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
#                     res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids)

#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
#                     print("RA-TC_PPE===handled")
#                     roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,lines, traffic_count_cls_name_cls_id)
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index) 
#                     res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids)
                    
#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
#                     print("cr-ra===6")
#                     roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id)
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,lines,  traffic_count_cls_name_cls_id)
#                     # if len(x['cr_data']) !=0:
#                     #     cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     # if x['cr_data']:
#                     #     if x['cr_data'][0]['full_frame'] == False:
#                     #         if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                     #             cr_fun_conf_analytics(x,  lines)
#                     #         else:
#                     #             cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                                
#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
#                     print("ra_TC===7")
#                     roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,lines,  traffic_count_cls_name_cls_id)
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index)  
#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
#                     print("ra_PPE===8")
#                     roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_data_cf(x, hooter_line, index,roi_enable_cam_ids,lines,  traffic_count_cls_name_cls_id)
#                     res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids)   
                    
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
#                     print("CR_TC===9")
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     if x['cr_data']:
#                         if x['cr_data'][0]['full_frame'] == False:
#                             if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                                 cr_fun_conf_analytics(x,  lines)
#                             else:
#                                 cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
#                     print("PPE_TC===10")
#                     tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id) 
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index)   
#                     res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids)    
                    
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
#                     print("PPE_CR===11")    
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     if x['cr_data']:
#                         if x['cr_data'][0]['full_frame'] == False:
#                             if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                                 cr_fun_conf_analytics(x,  lines)
#                             else:
#                                 cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
#                     res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids)  
                    
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
#                     print("CR===12")    
#                     if len(x['cr_data']) !=0:
#                         cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,camera_id, cr_enable_cam_ids)
#                     if x['cr_data']:
#                         if x['cr_data'][0]['full_frame'] == False:
#                             if '[roi-filtering-stream-{0}]'.format(index)  in lines:
#                                 cr_fun_conf_analytics(x,  lines)
#                             else:
#                                 cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                                
#                 elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
#                     print("RA===13")    
#                     roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines)#roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines) #roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,lines,  traffic_count_cls_name_cls_id)
                    
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
#                     print("TC===14") 
#                     tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
#                     if tc_fun_conf_anlytics_file:
#                         traffic_count_enabledcameraids.append(index)
                    
#                 elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
#                     print("PPE===14") 
                    
                    
#                     res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids)
                    
#             # index += 1
#         total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids))
#         print("roi_enable cam ids =====", roi_enable_cam_ids)
#         print("ppeppe_333enable_cam_ids",ppe_enable_cam_ids)
#         with open(config_analytics_file, 'w') as f:
#             for item in lines:
#                 f.write('%s\n' % item)

#         with open(hooter_config_file_path, 'w') as hooter_file:
#             for jim in hooter_line:
#                 hooter_file.write('%s\n' % jim)

#         with open(crowd_config_file, 'w') as crowd_file:
#             for O_O_O, item in enumerate(crowd_line):
#                 crowd_file.write('%s\n' % item)

#         lines = []
#         truck_lines = []
#         traffic_lines = []
#         final_both_roi_cam_ids = []
#         with open(sample_config_file) as file:
#             for write_config, line in enumerate(file):
#                 if line.strip() == '[application]':
#                     truck_lines.append('[application]')
#                     truck_lines.append('enable-perf-measurement=1')
#                     truck_lines.append('perf-measurement-interval-sec=1')
#                     lines.append('[application]')
#                     lines.append('enable-perf-measurement=1')
#                     lines.append('perf-measurement-interval-sec=1')
#                     traffic_lines.append('[application]')
#                     traffic_lines.append('enable-perf-measurement=1')
#                     traffic_lines.append('perf-measurement-interval-sec=1')

#                 elif line.strip() == '[tiled-display]':
#                     finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
#                     finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
#                     finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
#                     total_stream_for_stremux_union = finaL_RA_PPE
#                     num = math.sqrt(int(len(finaL_RA_PPE)))
#                     print("num----",num )
#                     print("num----",num )
#                     if 1 < num < 1.4:
#                         rows = 1
#                         columns = 2
#                     elif num == 1:
#                         rows = 1
#                         columns = 2
#                     else:
#                         if 1 > num >= 1.4:
#                             if len(finaL_RA_PPE)>3:
#                                 rows = 2
#                                 columns = 2
#                             else:
#                                 rows = 1
#                                 columns = 2
                                
#                         else:
#                             rows = int(round(num))
#                             columns = 2
#                         print("row====s ",rows)
#                         print("columns====s ",columns)
#                     if len(truck_final_cam_ids) != 0:
#                         truck_num = math.sqrt(len(truck_final_cam_ids))
#                         if 1 < truck_num > 1.4:
#                             truck_rows = 1
#                             truck_columns = 2
#                         elif truck_num == 1:
#                             truck_rows = 1
#                             truck_columns = 1
#                         else:
#                             truck_rows = int(truck_num - (truck_num - 1))
#                             truck_columns = int(truck_num)
#                         truck_lines.append('[tiled-display]')
#                         truck_lines.append('enable=1')
#                         truck_lines.append('rows={0}'.format(str(truck_rows)))
#                         truck_lines.append('columns={0}'.format(str(truck_columns)))
#                         truck_lines.append('width=960')
#                         truck_lines.append('height=544')
#                         truck_lines.append('gpu-id=0')
#                         truck_lines.append('nvbuf-memory-type=0')

#                     lines.append('[tiled-display]')
#                     lines.append('enable=1')
#                     lines.append('rows={0}'.format(str(rows)))
#                     lines.append('columns={0}'.format(str(columns)))
#                     lines.append('width=960')
#                     lines.append('height=544')
#                     lines.append('gpu-id=0')
#                     lines.append('nvbuf-memory-type=0')

#                 elif line.strip() == '[sources]':                    
#                     truck_conifg_file = 0
#                     print("newlength===", len(writingresponse))
#                     for n, x in enumerate(writingresponse):
#                         cam_id = '{0}'.format(int(n))
#                         roi_enable_cam_ids_exist = roi_enable_cam_ids.count(int(cam_id))
#                         print("newecammeakdkkdk===", roi_enable_cam_ids_exist)
#                         ppe_enable_cam_ids_exist = ppe_enable_cam_ids.count( int(cam_id))
#                         truck_cam_ids_exist = truck_final_cam_ids.count(int(cam_id))
#                         print("cam_idcam_idcam_id-",cam_id)
#                         print("cr_enable_cam_ids-",cr_enable_cam_ids)
#                         print("camera_id == 9999",camera_id)
#                         print(" hello 9999",camera_id)
#                         newcrowdcount = cr_enable_cam_ids.count(int(camera_id))
#                         print("newcrowdcountnewcrowdcountnewcrowdcount===newcrowdcount> 0 ",newcrowdcount)
#                         find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
#                         if find_data is not None:
#                             if find_data['rtsp_flag'] == '1':
#                                 if 'rtsp' in x['rtsp_url']:
#                                     x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')

#                         if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 :
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(normal_config_file))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             PPEFINALCAMERAIDS.append(camera_id)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1                            
#                             camera_id += 1
                            
                            
#                         elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ):
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(normal_config_file))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             PPEFINALCAMERAIDS.append(camera_id)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1                            
#                             camera_id += 1
                            
#                         elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(normal_config_file))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             PPEFINALCAMERAIDS.append(camera_id)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1                            
#                             camera_id += 1

#                         elif roi_enable_cam_ids_exist > 0:
#                             print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
#                             print("adstatsd====", roi_enable_cam_ids)
#                             print('[source{0}]'.format(normal_config_file))
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(normal_config_file))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1
#                             camera_id += 1

#                         elif ppe_enable_cam_ids_exist > 0:
#                             print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
#                             print("adstatsd====", roi_enable_cam_ids)
#                             print('[source{0}]'.format(normal_config_file))
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(n))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             PPEFINALCAMERAIDS.append(camera_id)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1                            
#                             camera_id += 1
                        
#                         elif len(traffic_count_enabledcameraids)>0:
#                             print("asdjfkasdfjaksdfkjaksdfkjaskdtraffic_count_enabledcameraidsfkajsdkfkasdjk=============", traffic_count_enabledcameraids)
#                             print("adstatsd====", roi_enable_cam_ids)
#                             print('[source{0}]'.format(normal_config_file))
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(n))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1
#                             camera_id += 1
                            
#                         elif newcrowdcount >0:
#                             uri = x['rtsp_url']
#                             lines.append('[source{0}]'.format(n))
#                             lines.append('enable=1')
#                             lines.append('type=4')
#                             lines.append('uri = {0}'.format(uri))
#                             lines.append('num-sources=1')
#                             lines.append('gpu-id=0')
#                             lines.append('nvbuf-memory-type=0')
#                             lines.append('latency=150')
#                             lines.append('camera-id={0}'.format(camera_id))   
#                             camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
#                             allWrittenSourceCAmIds.append(camera_required_data)
#                             lines.append('camera-name={0}'.format(x['cameraname']))
#                             lines.append("rtsp-reconnect-interval-sec=2")
#                             lines.append('drop-frame-interval = 1\n')
#                             normal_config_file += 1
#                             camera_id += 1

#                         if truck_cam_ids_exist != 0:
#                             if n + 1 in truck_final_cam_ids:
#                                 uri = x['rtsp_url']
#                                 truck_lines.append('[source{0}]'.format(normal_config_file))
#                                 truck_lines.append('enable=1')
#                                 truck_lines.append('type=4')
#                                 truck_lines.append('uri = {0}'.format(uri))
#                                 truck_lines.append('num-sources=1')
#                                 truck_lines.append('gpu-id=0')
#                                 truck_lines.append('nvbuf-memory-type=0')
#                                 truck_lines.append('latency=150')
#                                 truck_lines.append('camera-id={0}'.format(camera_id))
#                                 truck_lines.append( 'camera-name={0}'.format(x['cameraname']))
#                                 truck_lines.append('drop-frame-interval = 1\n')
#                                 truck_conifg_file += 1

#                 elif line.strip() == '[sink0]':
#                     lines.append('[sink0]')
#                     truck_lines.append('[sink0]')

#                 elif line.strip() == '[osd]':
#                     truck_lines.append('[osd]')
#                     lines.append('[osd]')
#                     lines.append('enable=1')
#                     lines.append('gpu-id=0')
#                     lines.append('border-width=2')
#                     lines.append('text-size=15')
#                     lines.append('text-color=1;1;1;1;')
#                     lines.append('text-bg-color=0.3;0.3;0.3;1;')
#                     lines.append('font=Arial')
#                     lines.append('show-clock=0')
#                     lines.append('clock-x-offset=800')
#                     lines.append('clock-y-offset=820')
#                     lines.append('clock-text-size=12')
#                     lines.append('clock-color=1;0;0;0')
#                     lines.append('nvbuf-memory-type=0')
#                     truck_lines.append('gpu-id=0')
#                     truck_lines.append('live-source=1')
#                     truck_lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
#                     truck_lines.append('batched-push-timeout=40000')
#                     truck_lines.append('width=1920')
#                     truck_lines.append('height=1080')
#                     truck_lines.append('enable-padding=0')
#                     truck_lines.append('nvbuf-memory-type=0\n')

#                 elif line.strip() == '[streammux]':
#                     lines.append('[streammux]')
#                     lines.append('gpu-id=0')
#                     lines.append('live-source=1')
#                     lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
#                     lines.append('batched-push-timeout=40000')
#                     lines.append('width=1920')
#                     lines.append('height=1080')
#                     lines.append('enable-padding=0')
#                     lines.append('nvbuf-memory-type=0')

#                 elif line.strip() == '[primary-gie]':
#                     lines.append('[primary-gie]')
#                     lines.append('enable=1')
#                     lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
#                     lines.append('bbox-border-color0=0;1;0;1.0')
#                     lines.append('bbox-border-color1=0;1;1;0.7')
#                     lines.append('bbox-border-color2=0;1;0;0.7')
#                     lines.append('bbox-border-color3=0;1;0;0.7')
#                     lines.append('nvbuf-memory-type=0')
#                     lines.append('interval=0')
#                     lines.append('gie-unique-id=1')
#                     modelconfigfile  = os.path.splitext(modelconfigfile)[0]
#                     lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
#                     truck_lines.append('[primary-gie]')
                    
                    
#                 elif line.strip() == '[secondary-gie2]':
#                     lines.append('[secondary-gie2]')
#                     lines.append('enable = 1')
#                     lines.append('gpu-id = 0')
#                     lines.append('gie-unique-id = 4')
#                     lines.append('operate-on-gie-id = 1')
#                     lines.append('operate-on-class-ids = 0;2;')
#                     lines.append('batch-size = 1')
#                     lines.append('bbox-border-color0 = 0;0;0;0.7')
#                     lines.append('bbox-border-color1 = 1;0;0;0.7')
#                     lines.append('config-file = ../../models/config_infer_secandary_helmet_gnet_v3.txt')
#                     secondaryconfig_file = []
                    
#                     secondaryconfig_file.append('[property]')
#                     secondaryconfig_file.append('gpu-id=0')
#                     secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
#                     secondaryconfig_file.append('tlt-model-key=tlt_encode')
#                     secondaryconfig_file.append('tlt-encoded-model=./helmet_gnet_v3/googlenet_helmet_detector_pruned.etlt')
#                     secondaryconfig_file.append('labelfile-path=./helmet_gnet_v3/labels.txt')
#                     secondaryconfig_file.append('model-engine-file=./helmet_gnet_v3/googlenet_helmet_detector_pruned.etlt_b1_gpu0_fp16.engine')
#                     secondaryconfig_file.append('infer-dims=3;320;320')
#                     secondaryconfig_file.append('uff-input-blob-name=input_1')
#                     secondaryconfig_file.append('batch-size=1')
#                     secondaryconfig_file.append('process-mode=2')
#                     secondaryconfig_file.append('model-color-format=0')
#                     secondaryconfig_file.append('network-mode=2')
#                     secondaryconfig_file.append('num-detected-classes=2')
#                     secondaryconfig_file.append('interval=0')
#                     secondaryconfig_file.append('gie-unique-id=2')
#                     secondaryconfig_file.append('operate-on-gie-id=1')
#                     secondaryconfig_file.append('operate-on-class-ids=0;1;2;3')
#                     secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
#                     secondaryconfig_file.append('offsets=0.0;0.0;0.0')
#                     secondaryconfig_file.append('network-type=0')
#                     secondaryconfig_file.append('uff-input-order=0\n')
#                     secondaryconfig_file.append('[class-attrs-0]')
#                     secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
#                     secondaryconfig_file.append('group-threshold=1')
#                     secondaryconfig_file.append('eps=0.4')
#                     secondaryconfig_file.append('#minBoxes=3')
#                     secondaryconfig_file.append('#detected-min-w=20')
#                     secondaryconfig_file.append('#detected-min-h=20\n')
#                     secondaryconfig_file.append('[class-attrs-1]')
#                     secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
#                     secondaryconfig_file.append('group-threshold=1')
#                     secondaryconfig_file.append('eps=0.4')
#                     secondaryconfig_file.append('#minBoxes=3')
#                     secondaryconfig_file.append('#detected-min-w=20')
#                     secondaryconfig_file.append('#detected-min-h=20')
#                     with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_gnet_v3.txt', 'w') as f:
#                         for O_O_O, item in enumerate(secondaryconfig_file):
#                             f.write('%s\n' % item)
                    
#                 elif line.strip() == '[secondary-gie3]':
#                     lines.append('[secondary-gie3]')
#                     lines.append('enable = 1')
#                     lines.append('gpu-id = 0')
#                     lines.append('gie-unique-id = 5')
#                     lines.append('operate-on-gie-id = 1')
#                     lines.append('operate-on-class-ids = 0;2;')
#                     lines.append('batch-size = 1')
#                     lines.append('bbox-border-color0 = 1;0;1;0.7')
#                     lines.append('bbox-border-color1 = 1;0;0;0.7')
#                     lines.append('config-file = ../../models/config_infer_secandary_vest_v4.txt')       
#                     secondaryconfig_filevest = []
#                     secondaryconfig_filevest.append('[property]')
#                     secondaryconfig_filevest.append('gpu-id=0')
#                     secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
#                     secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
#                     secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v4/vest_v4_resnet18_detector.etlt')
#                     secondaryconfig_filevest.append('labelfile-path=./vest_detection_v4/labels.txt')
#                     secondaryconfig_filevest.append('model-engine-file=./vest_detection_v4/vest_v4_resnet18_detector.etlt_b1_gpu0_fp16.engine')
#                     secondaryconfig_filevest.append('infer-dims=3;320;320')
#                     secondaryconfig_filevest.append('uff-input-blob-name=input_1')
#                     secondaryconfig_filevest.append('batch-size=1')
#                     secondaryconfig_filevest.append('process-mode=2')
#                     secondaryconfig_filevest.append('model-color-format=0')
#                     secondaryconfig_filevest.append('network-mode=2')
#                     secondaryconfig_filevest.append('num-detected-classes=3')
#                     secondaryconfig_filevest.append('interval=0')
#                     secondaryconfig_filevest.append('gie-unique-id=2')
#                     secondaryconfig_filevest.append('operate-on-gie-id=1')
#                     secondaryconfig_filevest.append('operate-on-class-ids=0;1;2;3')
#                     secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
#                     secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
#                     secondaryconfig_filevest.append('network-type=0')
#                     secondaryconfig_filevest.append('uff-input-order=0\n')
#                     secondaryconfig_filevest.append('[class-attrs-0]')
#                     secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
#                     secondaryconfig_filevest.append('group-threshold=1')
#                     secondaryconfig_filevest.append('eps=0.4')
#                     secondaryconfig_filevest.append('#minBoxes=3')
#                     secondaryconfig_filevest.append('#detected-min-w=20')
#                     secondaryconfig_filevest.append('#detected-min-h=20\n')

#                     secondaryconfig_filevest.append('[class-attrs-1]')
#                     secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
#                     secondaryconfig_filevest.append('group-threshold=1')
#                     secondaryconfig_filevest.append('eps=0.4')
#                     secondaryconfig_filevest.append('#minBoxes=3')
#                     secondaryconfig_filevest.append('#detected-min-w=20')
#                     secondaryconfig_filevest.append('#detected-min-h=20')
                    
#                     secondaryconfig_filevest.append('[class-attrs-2]')
#                     secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
#                     secondaryconfig_filevest.append('group-threshold=1')
#                     secondaryconfig_filevest.append('eps=0.4')
#                     secondaryconfig_filevest.append('#minBoxes=3')
#                     secondaryconfig_filevest.append('#detected-min-w=20')
#                     secondaryconfig_filevest.append('#detected-min-h=20')
                    
                    
#                     with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v4.txt', 'w') as f:
#                         for O_O_O, item in enumerate(secondaryconfig_filevest):
#                             f.write('%s\n' % item)


#                 elif line.strip() == '[tracker]':
#                     lines.append('[tracker]')
#                     truck_lines.append('[tracker]')

#                 elif line.strip() == '[nvds-analytics]':
#                     lines.append('[nvds-analytics]')
#                     lines.append('enable = 1')
#                     lines.append('config-file = ./config_analytics_{0}.txt'.format(config_index+1))
#                     truck_lines.append('[nvds-analytics]')
#                     truck_lines.append('enable = 1')
#                     truck_lines.append('config-file = ./config_analytics_{0}.txt'.format(config_index+1))

#                 elif line.strip() == '[tests]':
#                     lines.append('[tests]')
#                     truck_lines.append('[tests]')

#                 elif line.strip() == '[docketrun-analytics]':
#                     lines.append('[docketrun-analytics]')
#                     lines.append('smart-record-stop-buffer = 2\n')
#                     truck_lines.append('[docketrun-analytics]')
#                     truck_lines.append('smart-record-stop-buffer = 2\n')

#                 elif line.strip() == '[docketrun-image]':
#                     lines.append('[docketrun-image]')
#                     truck_lines.append('[docketrun-image]')

#                 elif line.strip() == '[restricted-access]':
#                     lines.append('[restricted-access]')
#                     truck_lines.append('[restricted-access]')
#                     final_index = 0
#                     final_roi_empty_ls = []
#                     final_truck_empty_ls = []
#                     check_camera_id_for_RA = []
#                     for Cherry, x in enumerate(writingresponse):
#                         string2 = '-1;'
#                         if len(x['roi_data']) != 0:
#                             for test_roi_ra, roi_value in enumerate(x['roi_data']):
#                                 label_name = roi_value['label_name']
#                                 if ('person' in label_name and 'truck' in label_name):
#                                     final_both_roi_cam_ids.append(final_index + 1)
#                                     string2 = ''
#                                 elif 'truck' in label_name:
#                                     final_truck_cam_ids.append(final_index + 1)
#                                     string2 = ''
#                                 elif 'person' in label_name:
#                                     final_roi_existed_cam_ids.append(final_index + 1)
#                                     string2 = ''
#                                 elif 'person' not in label_name and 'truck' not in label_name:
#                                     pass
#                                 else:
#                                     pass
#                         final_index += 1
#                     string_test = '-1;'
#                     if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
#                         check_camera_id_for_RA.append(final_roi_existed_cam_ids)
#                     final_roi_existed_cam_ids = roi_enable_cam_ids
#                     for n in roi_enable_cam_ids:
#                         text = str(n) + ';'
#                         text = str(n) + ';'
#                         if text not in final_roi_empty_ls:
#                             final_roi_empty_ls.append(text)

#                     for n in final_truck_cam_ids:
#                         text = str(n) + ';'
#                         if text not in final_truck_empty_ls:
#                             final_truck_empty_ls.append(text)

#                     for n in roi_enable_cam_ids:
#                         text = str(n) + ';'
#                         if text not in final_roi_empty_ls:
#                             final_roi_empty_ls.append(text)

#                     if len(check_camera_id_for_RA) == 0:
#                         if len(final_truck_empty_ls) == 0:
#                             final_truck_empty_ls.append(string_test)

#                     if len(final_truck_empty_ls) != 0:
#                         string1 = ''
#                         truck_lines.append('camera-ids = {0}'.format(string1.join(final_truck_empty_ls)))

#                     else:
#                         truck_string = '-1;'
#                         truck_lines.append('camera-ids = {0}'.format(truck_string.join(final_truck_empty_ls)))
                        
                        
#                     print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",len(roi_enable_cam_ids))
#                     print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",roi_enable_cam_ids)
#                     if len(roi_enable_cam_ids)== 0:
#                         lines.append('enable = 0')

#                     else:
#                         lines.append('enable = 1')
#                     lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))

#                     truck_lines.append('draw-person-bbox-in-roi = 0')
#                     truck_empty_label_ls = []                   
#                     test_string = ''
#                     truck_test_string = ''
#                     truck_lines.append('operate-on-label = {0}'.format(truck_test_string.join(truck_empty_label_ls)))

#                 elif line.strip() == '[ppe-type-1]':
#                     lines.append('[ppe-type-1]')
#                     truck_lines.append('[ppe-type-1]')
#                     empty_ppe_ls = []
#                     for OPI_, n in enumerate(PPEFINALCAMERAIDS):
#                         text = str(n) + ';'
#                         empty_ppe_ls.append(text)
#                     string2 = ''
#                     if len(empty_ppe_ls) == 0:
#                         string2 = '-1;'
#                         lines.append('camera-ids = {0}'.format(string2))
#                         truck_lines.append('camera-ids = {0}'.format(string2))
#                     else:
#                         string2 = ''
#                         lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
#                         truck_lines.append('camera-ids = {0}'.format('-1'))

#                 elif line.strip() == '[crowd-counting]':
#                     lines.append('[crowd-counting]')
#                     cr_final_index = 0
#                     for Cherry, x in enumerate(response):
#                         string2 = '-1;'
#                         if len(x['cr_data']) != 0:
#                             cr_final_index += 1

#                     if cr_final_index == 0:
#                         enable_val = 0
#                         lines.append('enable = {0}'.format(enable_val))
#                     else:
#                         enable_val = 1
#                         lines.append('enable = {0}'.format(enable_val))
#                     lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
#                     lines.append("roi-overlay-enable=1")

#                 elif line.strip() == '[traffic-count]':
#                     lines.append('[traffic-count]')
#                     tc_final_index = 0
#                     final_tc_empty_ls = []
#                     for Cherry, x in enumerate(response):
#                         string2 = '-1;'
#                         if len(x['tc_data']) != 0:
#                             final_tc_existed_cam_ids = []
#                             for tc_val in x['tc_data']:
#                                 for tc_val___test in tc_val['label_name']:
#                                     if tc_val___test not in tc_label_names:
#                                         tc_label_names.append(tc_val___test)
#                                 if len(tc_val['traffic_count']) != 0:
#                                     final_tc_existed_cam_ids.append(
#                                         tc_final_index + 1)
#                                     for n in final_tc_existed_cam_ids:
#                                         text = str(n) + ';'
#                                         final_tc_empty_ls.append(text)
#                                     string2 = ''
#                         tc_final_index += 1
#                     if len(final_tc_empty_ls) == 0:
#                         final_tc_empty_ls.append(string2)
#                     lines.append('camera-ids = {0}'.format(string2.join(final_tc_empty_ls)))
#                     tc_empty_label_ls = []
#                     for tc_label_name_test in tc_label_names:
#                         text = str(tc_label_name_test) + ';'
#                         tc_empty_label_ls.append(text)
#                     test_string = ''
#                     lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))

#                 else:
#                     lines.append(line.strip())
#                     truck_lines.append(line.strip())

#         model_config_details = get_model_config_details()
#         if model_config_details is not None:
#             if model_config_details['modeltype'] == 'yolo':
#                 classId = model_config_details['objectDetector_Yolo']['class_id']
#                 modelconfigfile = model_config_details['objectDetector_Yolo']['modelpath']
#                 modelconfigwrite =[]
#                 modelconfigwrite.append('[property]')
#                 modelconfigwrite.append('gpu-id=0')
#                 modelconfigwrite.append('batch-size=1')
#                 modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
#                 modelconfigwrite.append('model-color-format=0')
#                 modelconfigwrite.append('custom-network-config=/home/docketrun/streamapp/models/objectDetector_Yolo/yolov3.cfg')
#                 modelconfigwrite.append('#model-file=/home/docketrun/streamapp/models/objectDetector_Yolo/yolov3.weights')
#                 modelconfigwrite.append('model-engine-file=/home/docketrun/streamapp/models/objectDetector_Yolo/engine/model_b{0}_gpu0_int8.engine'.format(len(list(total_stream_for_stremux_union))))
#                 modelconfigwrite.append('labelfile-path=/home/docketrun/streamapp/models/objectDetector_Yolo/labels.txt')
#                 modelconfigwrite.append('int8-calib-file=/home/docketrun/streamapp/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0')
#                 modelconfigwrite.append('network-mode=1')
#                 modelconfigwrite.append('num-detected-classes=80')
#                 modelconfigwrite.append('gie-unique-id=1')
#                 modelconfigwrite.append('network-type=0')
#                 modelconfigwrite.append('is-classifier=0')
#                 modelconfigwrite.append('cluster-mode=2')
#                 modelconfigwrite.append('maintain-aspect-ratio=1')
#                 modelconfigwrite.append( 'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
#                 modelconfigwrite.append('custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
#                 modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
#                 modelconfigwrite.append('[class-attrs-all]')
#                 modelconfigwrite.append('nms-iou-threshold=0.3')
#                 modelconfigwrite.append('threshold=1.0')
#                 modelconfigwrite.append('[class-attrs-0]')
#                 modelconfigwrite.append('nms-iou-threshold=0.3')
#                 modelconfigwrite.append('threshold={0}'.format(person_threshold))
#                 modelconfigwrite.append('[class-attrs-7]')
#                 modelconfigwrite.append('nms-iou-threshold=0.3')
#                 modelconfigwrite.append('threshold=1.0')

#             elif model_config_details['modeltype'] == 'trafficcam':
#                 classId = model_config_details['trafficcamnet']['class_id']
#                 modelconfigfile = model_config_details['trafficcamnet']['modelpath']
#                 modelconfigwrite =[]
#                 modelconfigwrite.append('[property]')
#                 modelconfigwrite.append('gpu-id=0')
#                 modelconfigwrite.append('batch-size=1')
#                 modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
#                 modelconfigwrite.append('tlt-model-key=tlt_encode')
#                 modelconfigwrite.append('tlt-encoded-model=./trafficcamnet/resnet18_trafficcamnet_pruned.etlt')
#                 modelconfigwrite.append('labelfile-path=./trafficcamnet/labels_trafficnet.txt')
#                 modelconfigwrite.append('int8-calib-file=./trafficcamnet/trafficnet_int8.bin')
#                 modelconfigwrite.append('model-engine-file=./trafficcamnet/engine/resnet18_trafficcamnet_pruned.etlt_b4_gpu0_int8.engine')
#                 modelconfigwrite.append('input-dims=3;544;960;0')
#                 modelconfigwrite.append('uff-input-blob-name=input_1')
#                 modelconfigwrite.append('batch-size=1')
#                 modelconfigwrite.append('process-mode=1')
#                 modelconfigwrite.append('model-color-format=0')
#                 modelconfigwrite.append('network-mode=1')
#                 modelconfigwrite.append('num-detected-classes=4')
#                 modelconfigwrite.append('interval=0')
#                 modelconfigwrite.append('gie-unique-id=1')
#                 modelconfigwrite.append('output-blob-names=output_bbox/BiasAdd;output_cov/Sigmoid')
#                 modelconfigwrite.append('[class-attrs-0]')
#                 modelconfigwrite.append('pre-cluster-threshold=1.0')
#                 modelconfigwrite.append('group-threshold=1')
#                 modelconfigwrite.append('eps=0.2\n')
#                 modelconfigwrite.append('[class-attrs-1]')
#                 modelconfigwrite.append('pre-cluster-threshold=1.0')
#                 modelconfigwrite.append('group-threshold=1')
#                 modelconfigwrite.append('eps=0.2\n')

#                 modelconfigwrite.append('[class-attrs-2]')
#                 modelconfigwrite.append('pre-cluster-threshold=0.14')
#                 modelconfigwrite.append('group-threshold=1')
#                 modelconfigwrite.append('eps=0.2')
#                 modelconfigwrite.append('detected-min-h=70\n')

#                 modelconfigwrite.append('[class-attrs-3]')
#                 modelconfigwrite.append('pre-cluster-threshold=1.0')
#                 modelconfigwrite.append('group-threshold=1')
#                 modelconfigwrite.append('eps=0.2\n')

#             elif model_config_details['modeltype'] == 'people':
#                 classId = model_config_details['peoplenet']['class_id']
#                 modelconfigfile = model_config_details['peoplenet']['modelpath']
#                 modelconfigwrite =[]
#                 modelconfigwrite.append('[property]')
#                 modelconfigwrite.append('gpu-id=0')
#                 modelconfigwrite.append('batch-size=1')
#                 modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
#                 modelconfigwrite.append('model-color-format=0')
#                 modelconfigwrite.append( 'custom-network-config=/home/docketrun/streamapp/models/objectDetector_Yolo/yolov3.cfg')
#                 modelconfigwrite.append( 'model-file=/home/docketrun/streamapp/models/objectDetector_Yolo/yolov3.weights')
#                 modelconfigwrite.append( '#model-engine-file=/home/docketrun/streamapp/models/objectDetector_Yolo/engine/model_b8_gpu0_int8.engine')
#                 modelconfigwrite.append( 'labelfile-path=/home/docketrun/streamapp/models/objectDetector_Yolo/labels.txt')
#                 modelconfigwrite.append('int8-calib-file=/home/docketrun/streamapp/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0')
#                 modelconfigwrite.append('network-mode=1')
#                 modelconfigwrite.append('num-detected-classes=80')
#                 modelconfigwrite.append('gie-unique-id=1')
#                 modelconfigwrite.append('network-type=0')
#                 modelconfigwrite.append('is-classifier=0')
#                 modelconfigwrite.append('cluster-mode=2')
#                 modelconfigwrite.append('maintain-aspect-ratio=1')
#                 modelconfigwrite.append(  'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
#                 modelconfigwrite.append( 'custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
#                 modelconfigwrite.append( 'engine-create-func-name=NvDsInferYoloCudaEngineGet')
#                 modelconfigwrite.append('[class-attrs-all]')
#                 modelconfigwrite.append('nms-iou-threshold=0.3')
#                 modelconfigwrite.append('threshold=1.0')
#                 modelconfigwrite.append('[class-attrs-0]')
#                 modelconfigwrite.append('nms-iou-threshold=0.3')
#                 modelconfigwrite.append('threshold=0.7')
#                 modelconfigwrite.append('[class-attrs-7]')
#                 modelconfigwrite.append('nms-iou-threshold=0.3')
#                 modelconfigwrite.append('threshold=1.0')            
#         modelconfigfile  = os.path.splitext(modelconfigfile)[0]    
#         with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
#             for O_O_O, item in enumerate(modelconfigwrite):
#                 f.write('%s\n' % item)

#         with open(config_file, 'w') as f:
#             for O_O_O, item in enumerate(lines):
#                 f.write('%s\n' % item)
#     return allWrittenSourceCAmIds

