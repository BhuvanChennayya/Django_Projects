from Data_recieving_and_Dashboard.packages import *
roi_required_keys=['roi_name','traffic_jam_percentage','selected_objects','bb_box','roi_id','min_time']
width_ratio = 960/960
height_ratio = 544/544

def append_lists(ls1, ls2):
    #iterating over list2
    for i in ls2:
        if i not in ls1:
            #appending in list1
            ls1.append(i)

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
        roi_label_names_default = []
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
            # print("label_name_roi_cr===",label_name_roi_cr)
            for cr_cls_name in label_name_roi_cr:
                print("----traffic_count_cls_name_cls_id11",traffic_count_cls_name_cls_id)
                if cr_cls_name not in label_name_roi_cr:
                    tc_val___test = cr_cls_name
                    label_name_roi_cr_default.append(tc_val___test)
        label_name_roi_cr_default_ls = []
        for tc_label_name_test in label_name_roi_cr_default:
            text = str(tc_label_name_test) + ';'
            label_name_roi_cr_default_ls.append(text)
        test_string = ''
        lines.append('inverse-roi=0')
        # lines.append('class-id= {0}\n'.format(test_string.join(label_name_roi_cr_default_ls)))
    else:
        roi_label_names_default = []
        if x["roi_data"] != 0:
            roi__label_names = []
            # print("----traffic_count_cls_name_cls_id22",traffic_count_cls_name_cls_id)
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
        # lines.append('class-id= {0}\n'.format(test_string.join(roi__empty_label_ls)))
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

def roi_data_cf(x, hooter_line, index, roi_enable_cam_ids, lines, traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines):
    roi_objects=set()
    print("-------------RA WITH -----------roi_data_cf---1----------",x)
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
            Newanalyticdetails = '['
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                roi_name = roi_value['roi_name']
                if 'pinch_role' in roi_value:
                    if type(roi_value['pinch_role']) != bool:
                        if 'status' in roi_value['pinch_role']:
                            if roi_value['pinch_role']['status']:
                                testpinchrole= True
                    else:
                        if type(roi_value['pinch_role']) == bool:
                            if roi_value['pinch_role']:
                                testpinchrole= True
                # print("x['alarm_ip_address']==== roi details ===",roi_value)
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
                        print('No label name found in roi data----1')
                        if 'objectdetails' in roi_value:
                            if 'objects_in_motion' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_in_motion'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_in_motion'])
                            if 'objects_tobe_protected' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_tobe_protected'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_tobe_protected'])
                        elif len(label_name) > 1:
                            [label_name_for_hooter.append(i) for i in label_name if i not in label_name_for_hooter]
                else:
                    print('the label name type is not the list -')
                if isEmpty(roi_value['alarm_type']):
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                    if roi_value['alarm_type']['hooter']  == True and roi_value['alarm_type']['relay'] == True :
                        print("both relay and hooter-------------")
                        print("both relay and hooter-------------")
                        if     x['alarm_version']['hooter'] =='old' and x['alarm_version']['relay'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;') 
                        elif  x['alarm_version']['hooter'] =='new'  and x['alarm_version']['relay'] =='new'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')                                     
                                else:
                                    hooter_list_type.append('2;2;') 
                        elif   x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type1'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;')                              
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')  
                                if  x['alarm_ip_address']['hooter_ip'] is not None :
                                    hooter_list_type.append('1;') 
                                if  x['alarm_ip_address']['relay_ip'] is not None :
                                    hooter_list_type.append('2;') 

                        elif  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='new' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;') 

                        elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;0;') 

                        elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type2':
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif   x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;1;')  
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type3'  :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;4;')  

                        elif x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type1' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;0;')  
                        elif  x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type3'    :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;4;')                     
                    elif roi_value['alarm_type']['hooter'] :
                        print(" hooter-------------")
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
                    elif roi_value['alarm_type']['relay']:
                        print(" relay-------------")
                        if  x['alarm_version']['relay'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='new':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='type2':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type3':
                            hooter_list_type.append('4;')
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        elif  x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                else:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        elif x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None :
                                # print('---------------2',x['alarm_ip_address']['hooter_ip'])
                                # print("--------------2 roi name ==", roi_name)                                
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name'])+',null];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['relay_ip'] is not None :
                                if x['alarm_version']['relay'] =='type3':
                                    if 'channel' in roi_value['alarm_type']:
                                        channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    elif x['alarm_version']['relay'] =='type3':
                                        channel = 'OUT'+str(1)
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'
                                else:
                                    hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'


                if Newanalyticdetails != '[' :
                    # print('--------------ROI-----IF--',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            #{"analytics_type": 0, "roi_name":"test1", "time_slots":[]}
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'

                            else:
                                Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

                else:
                    # print('Newanalyticdetails--------else----------- ',Newanalyticdetails)
                    # print('--------------ROI----ELSE---',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            #{"analytics_type": 0, "roi_name":"test1", "time_slots":[]}
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'
                            else:
                                Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

            if Newanalyticdetails != '[':
                Newanalyticdetails=Newanalyticdetails+']'
            else: 
                Newanalyticdetails='none'
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
            # print('-----------------hooter_list_type-----1.0.0-------------',hooter_list_type)
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
            # print('-----------------hooter_list_type-----1.0.6-------------',hooter_list_type)
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3')  
            hooter_line.append('analytics-details ={0}\n'.format(Newanalyticdetails))   
            #analytics-details = [{"analytics_type": 0, "roi_name":"test1", "time_slots":[]},{"analytics_type": 0, "roi_name":"test2", "time_slots": []},{"analytics_type": 0, "roi_name":"test3", "time_slots": []},{"analytics_type": 0, "roi_name":"test4", "time_slots": []},{"analytics_type": 0, "roi_name":"test5", "time_slots": []}]         
            #[192.168.1.46:8000,track_1];[192.168.1.46:8000,track_2]      
        else:
            Newanalyticdetails = '['
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            testpinchrole = False
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                if 'pinch_role' in roi_value:
                    if type(roi_value['pinch_role']) != bool:
                        if 'status' in roi_value['pinch_role']:
                            if roi_value['pinch_role']['status']:
                                testpinchrole= True
                    else:
                        if type(roi_value['pinch_role']) == bool:
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
                        print('No label name found in roi data----2')
                        if 'objectdetails' in roi_value:
                            if 'objects_in_motion' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_in_motion'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_in_motion'])
                            if 'objects_tobe_protected' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_tobe_protected'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_tobe_protected'])
                        elif len(label_name) > 1:
                            [label_name_for_hooter.append(i) for i in label_name if i not in label_name_for_hooter]
                else:
                    print('the label name type is not the list -')
                if isEmpty(roi_value['alarm_type']):
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                    # print("roi_value['alarm_type']====================",roi_value['alarm_type'])
                            
                    if roi_value['alarm_type']['hooter']  == True and roi_value['alarm_type']['relay'] == True :
                        # print("both relay and hooter-------------")
                        # print("both relay and hooter-------------")
                        if     x['alarm_version']['hooter'] =='old' and x['alarm_version']['relay'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;') 
                        elif  x['alarm_version']['hooter'] =='new'  and x['alarm_version']['relay'] =='new'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')                                     
                                else:
                                    hooter_list_type.append('2;2;') 
                        elif   x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type1'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;')                              
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')  
                                if  x['alarm_ip_address']['hooter_ip'] is not None :
                                    hooter_list_type.append('1;') 
                                if  x['alarm_ip_address']['relay_ip'] is not None :
                                    hooter_list_type.append('2;') 

                        elif  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='new' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;') 

                        elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;0;') 

                        elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type2':
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif   x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;1;')  
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type3'  :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;4;')  

                        elif x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type1' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;0;')  
                        elif  x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type3'    :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;4;')  



                    elif roi_value['alarm_type']['hooter'] :
                        # print(" hooter-------------")
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
                    elif roi_value['alarm_type']['relay']:
                        # print(" relay-------------")
                        if  x['alarm_version']['relay'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='new':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='type2':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type3':
                            hooter_list_type.append('4;')
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        elif x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                else:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        elif x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None :
                                # print('---------------2',x['alarm_ip_address']['hooter_ip'])
                                # print("--------------2 roi name ==", roi_name)
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name'])+',null];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['relay_ip'] is not None :
                                if x['alarm_version']['relay'] =='type3':
                                    if 'channel' in roi_value['alarm_type']:
                                        channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    if x['alarm_version']['relay'] =='type3':
                                        channel = 'OUT'+str(1)
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'
                                else:
                                    hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'
                if Newanalyticdetails != '[' :
                    # print('--------------ROI-----IF--',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'

                            else:
                                Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

                else:
                    # print('Newanalyticdetails--------else----------- ',Newanalyticdetails)
                    # print('--------------ROI----ELSE---',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'

                            else:
                                Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

            if Newanalyticdetails != '[':
                Newanalyticdetails=Newanalyticdetails+']'
            else: 
                Newanalyticdetails='none'
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
            print('-----------------hooter_list_type-----1.0.1-------------',hooter_list_type)
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3')  
            hooter_line.append('analytics-details ={0}\n'.format(Newanalyticdetails))       
        lines.append('[roi-filtering-stream-{0}]'.format(index))
        lines.append('enable=1')        
        for test_roi_ra, roi_value in enumerate(x['roi_data']):
            label_name = roi_value['label_name']
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
            lines.append('roi-RA-{0} = {1}'.format(roi_value['roi_name'], roi_bbox))

        if 'trafficjam_data' in x :
            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                # print('str(FinalTime)-------type---3-----0-------')
                config_tjm_lines.append('[TJM{0}]'.format(index))
                config_tjm_lines.append('enable=1' )
                Checkdetails ='details=['
                for j,roi_data in enumerate(x['trafficjam_data']):
                    roi_objects=set()
                    if validate_each_roi(roi_data,roi_required_keys):
                        if Checkdetails == 'details=[' :
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            print("-----------------",NewTIme['hour'])
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            print("-----------------",NewTIme['minute'])
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            print("-----------------",NewTIme['second'])
                                            FinalTime = FinalTime+ NewTIme['second']
                            # print('str(FinalTime)-------type---6------------',type(FinalTime))
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}'
                        else:
                            Checkdetails = Checkdetails+','
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))#my_string.strip()
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            print("-----------------",NewTIme['hour'])
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            print("-----------------",NewTIme['minute'])
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            print("-----------------",NewTIme['second'])
                                            FinalTime = FinalTime+ NewTIme['second']
                            # print('str(FinalTime)-------type---5------------',type(FinalTime))
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}'
                Checkdetails= Checkdetails+']'  
                config_tjm_lines.append(Checkdetails)      
        fun_config_analytics_file = cr_fun_conf_anlytics(x, lines,  traffic_count_cls_name_cls_id)
        roi_enable_cam_ids.append(NewcameraID)
    return True

def roi_fun_no_cr_data(x, hooter_line, index, roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines):
    roi_objects=set()
    print("0000000000000000000000000----x-------------roi_fun_no_cr_data-----------------hooter realay ----",x)
    label_name_for_hooter =[]
    roi_label_names =[]
    hooter_list_type =[]
    if len(x['roi_data']) != 0:
        if x['alarm_type'] is not None and x['alarm_ip_address'] is not None:
            hooteripstring = '['  
            Newanalyticdetails = '['
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')            
            testpinchrole = False
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                if  'pinch_role' in roi_value:
                    if type(roi_value['pinch_role']) != bool:
                        if 'status' in roi_value['pinch_role']:
                            if roi_value['pinch_role']['status']:
                                testpinchrole= True
                    else:
                        if type(roi_value['pinch_role']) == bool:
                            if roi_value['pinch_role']:
                                testpinchrole= True
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_crdd_data 1", str(error), " ----time ---- ", now_time_with_time()]))
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
                        print('No label name found in roi data---3')
                        if 'objectdetails' in roi_value:
                            if 'objects_in_motion' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_in_motion'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_in_motion'])
                            if 'objects_tobe_protected' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_tobe_protected'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_tobe_protected'])
                        elif len(label_name) > 1:
                            [label_name_for_hooter.append(i) for i in label_name if i not in label_name_for_hooter]
                else:
                    print('the label name type is not the list -')
                if isEmpty(roi_value['alarm_type']):
                    # print("--------------------1.0.2-----------roi_value['alarm_type']-----",roi_value['alarm_type'])
                    # print("--------------------1.0.2-----------x['alarm_version']-----",x['alarm_version'])
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                        # elif x['alarm_type']['hooter'] or x['alarm_type']['relay']:
                        #     hooteripstring= hooteripstring+'['                    
                    if roi_value['alarm_type']['hooter']  == True and roi_value['alarm_type']['relay'] == True :
                        print("both relay and hooter-------------")
                        if     x['alarm_version']['hooter'] =='old' and x['alarm_version']['relay'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;') 
                        elif  x['alarm_version']['hooter'] =='new'  and x['alarm_version']['relay'] =='new'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')                                     
                                else:
                                    hooter_list_type.append('2;2;') 
                        elif   x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type1'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;')                              
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')  
                                if  x['alarm_ip_address']['hooter_ip'] is not None :
                                    hooter_list_type.append('1;') 
                                if  x['alarm_ip_address']['relay_ip'] is not None :
                                    hooter_list_type.append('2;') 

                        elif  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='new' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;') 

                        elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;0;') 

                        elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type2':
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif   x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;1;')  
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type3'  :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;4;')  

                        elif x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type1' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;0;')  
                        elif  x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type3'    :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;4;')    

                    elif roi_value['alarm_type']['hooter'] :
                        print(" hooter-------------")
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
                    elif roi_value['alarm_type']['relay']:
                        print(" relay-------------")
                        if  x['alarm_version']['relay'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='new':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='type2':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type3':
                            hooter_list_type.append('4;')
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        elif  x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                else:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)

                                        elif x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None :
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name'])+',null];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['relay_ip'] is not None :
                                if x['alarm_version']['relay'] =='type3':
                                    if 'channel' in roi_value['alarm_type']:
                                        channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    elif x['alarm_version']['relay'] =='type3':
                                        channel = 'OUT'+str(1)
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'
                                else:
                                    hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'
                else:
                    print("-----------------------adfjaksdfkaskdfhooter ",roi_value['alarm_type'])

                if Newanalyticdetails != '[' :
                    # print('--------------ROI-----IF--',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'

                            else:
                                Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

                else:
                    # print('Newanalyticdetails--------else----------- ',Newanalyticdetails)
                    # print('--------------ROI----ELSE---',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'

                            else:
                                Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

            if Newanalyticdetails != '[':
                Newanalyticdetails=Newanalyticdetails+']'
            else: 
                Newanalyticdetails='none'
            hooter_empty_label_ls = []
            hooter_final_label = 'person;'
            print('--------------------------------label_name_for_hooter----------------------',label_name_for_hooter)
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            # print("---------------------------------------------------------hooter_list_type----------------------hooter_list_type-------------------------hooter_list_type",hooter_list_type)
            if len(hooter_list_type) ==0:
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
            # print('-----------------hooter_list_type-----1.0.2-------------',hooter_list_type)
            # print('-----------------hooteripstring-----1.0.2-------------',hooteripstring)
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3') 
            hooter_line.append('analytics-details ={0}\n'.format(Newanalyticdetails))   
        else:
            hooteripstring = '['  
            hooter_line.append('[RA{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            testpinchrole = False
            for test_roi_ra, roi_value in enumerate(x['roi_data']):
                label_name = roi_value['label_name']
                if 'pinch_role' in roi_value:
                    if type(roi_value['pinch_role']) != bool:
                        if 'status' in roi_value['pinch_role']:
                            if roi_value['pinch_role']['status']:
                                testpinchrole= True
                    else:
                        if type(roi_value['pinch_role']) == bool:
                            if roi_value['pinch_role']:
                                testpinchrole= True
                try:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                except Exception as error:
                    roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
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
                        print('No label name found in roi data-----4')
                        if 'objectdetails' in roi_value:
                            if 'objects_in_motion' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_in_motion'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_in_motion'])
                            if 'objects_tobe_protected' in roi_value['objectdetails']:
                                if roi_value['objectdetails']['objects_tobe_protected'] not in label_name_for_hooter:
                                    label_name_for_hooter.append(roi_value['objectdetails']['objects_tobe_protected'])
                        elif len(label_name) > 1:
                            [label_name_for_hooter.append(i) for i in label_name if i not in label_name_for_hooter]
                else:
                    print('the label name type is not the list -')
                # print("roi_value['alarm_type']=======2=============",roi_value['alarm_type'])
                if isEmpty(roi_value['alarm_type']):
                    if hooteripstring != '[' :
                        if roi_value['alarm_type']['hooter'] or  roi_value['alarm_type']['relay']  : 
                            hooteripstring= hooteripstring+'['
                    if roi_value['alarm_type']['hooter']  == True and roi_value['alarm_type']['relay'] == True :
                        print("both relay and hooter-------------")
                        print("both relay and hooter-------------")
                        if  x['alarm_version']['hooter'] =='old' and x['alarm_version']['relay'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;') 
                        elif  x['alarm_version']['hooter'] =='new'  and x['alarm_version']['relay'] =='new'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')                                     
                                else:
                                    hooter_list_type.append('2;2;') 
                        elif   x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type1'   :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;')                                     
                                else:
                                    hooter_list_type.append('0;0;')                              
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('3;')  
                                if  x['alarm_ip_address']['hooter_ip'] is not None :
                                    hooter_list_type.append('1;') 
                                if  x['alarm_ip_address']['relay_ip'] is not None :
                                    hooter_list_type.append('2;') 

                        elif  x['alarm_version']['relay'] =='old' and  x['alarm_version']['hooter'] =='new' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;') 

                        elif  x['alarm_version']['relay'] =='new' and  x['alarm_version']['hooter'] =='old' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;0;') 

                        elif  x['alarm_version']['relay'] =='type1' and  x['alarm_version']['hooter'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type2':
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;1;')  

                        elif   x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type2' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;1;')  
                        elif  x['alarm_version']['hooter'] =='type2' and x['alarm_version']['relay'] =='type3'  :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('1;4;')  

                        elif x['alarm_version']['hooter'] =='type3' and x['alarm_version']['relay'] =='type1' :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('4;0;')  
                        elif  x['alarm_version']['hooter'] =='type1' and x['alarm_version']['relay'] =='type3'    :
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] != x['alarm_ip_address']['relay_ip']:
                                    hooter_list_type.append('0;4;')  
                    elif roi_value['alarm_type']['hooter'] :
                        print(" hooter-------------")
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
                    elif roi_value['alarm_type']['relay']:
                        print(" relay-------------")
                        if  x['alarm_version']['relay'] =='old':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='new':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type1':
                            hooter_list_type.append('0;')
                        elif   x['alarm_version']['relay'] =='type2':
                            hooter_list_type.append('2;')
                        elif   x['alarm_version']['relay'] =='type3':
                            hooter_list_type.append('4;')
                    if roi_value['alarm_type']['hooter']==True and roi_value['alarm_type']['relay']==True:
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None and x['alarm_ip_address']['relay_ip'] is not None:
                                if x['alarm_ip_address']['hooter_ip'] == x['alarm_ip_address']['relay_ip']:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        elif x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];'
                                else:
                                    if x['alarm_version']['relay'] =='type3':
                                        if 'channel' in roi_value['alarm_type']:
                                            channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                       
                                        elif x['alarm_version']['relay'] =='type3':
                                            channel = 'OUT'+str(1)
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                        
                                        else:
                                            hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name']) +',null];['+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null]'
                            
                    elif roi_value['alarm_type']['hooter']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['hooter_ip'] is not None :
                                # print('---------------2',x['alarm_ip_address']['hooter_ip'])
                                # print("--------------2 roi name ==", roi_name)                                
                                hooteripstring=hooteripstring+x['alarm_ip_address']['hooter_ip']+','+str(roi_value['roi_name'])+',null];'
                                
                    elif roi_value['alarm_type']['relay']==True :
                        if isEmpty(x['alarm_ip_address']):
                            if x['alarm_ip_address']['relay_ip'] is not None :
                                if x['alarm_version']['relay'] =='type3':
                                    if 'channel' in roi_value['alarm_type']:
                                        channel = 'OUT'+str(roi_value['alarm_type']['channel'])
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    elif x['alarm_version']['relay'] =='type3':
                                        channel = 'OUT'+str(1)
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',{0}];'.format(channel)
                                    else:
                                        hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'
                                else:
                                    hooteripstring=hooteripstring+x['alarm_ip_address']['relay_ip']+','+str(roi_value['roi_name'])+',null];'

                if Newanalyticdetails != '[' :
                    # print('--------------ROI-----IF--',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'
                            else:
                                Newanalyticdetails=Newanalyticdetails+',{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+',{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'

                else:
                    # print('Newanalyticdetails--------else----------- ',Newanalyticdetails)
                    # print('--------------ROI----ELSE---',roi_value)
                    if 'analyticstype' in roi_value:
                        if roi_value['analyticstype'] is not None:
                            if int(roi_value['analyticstype']) == 2:
                                if 'arrow_line' in roi_value:
                                    #{"analytics_type": 2, "roi_name":"truck reversal", "direction":"464;501;458;312;", "sensitivity": 110, "in_motion": "car", "to_be_protected": "person", "time_slots":[]}
                                    Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "direction":"'+roi_value['arrow_line']+'", "in_motion":"'+roi_value['objectdetails']['objects_in_motion']+'", "sensitivity":'+str(roi_value['objectdetails']['sensitivity'])+', "to_be_protected":"'+roi_value['objectdetails']['objects_tobe_protected']+'","time_slots":[]}'

                            else:
                                Newanalyticdetails=Newanalyticdetails+'{"analytics_type":'+str(roi_value['analyticstype'])+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                        else:
                            Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
                    else:
                        Newanalyticdetails=Newanalyticdetails+'{"analytics_type":0'+', "roi_name":"'+str(roi_value['roi_name']) +'", "time_slots":[]}'
            
            if Newanalyticdetails != '[':
                Newanalyticdetails=Newanalyticdetails+']'
            else: 
                Newanalyticdetails='none'
            hooter_empty_label_ls = []
            hooter_final_label = 'person;'
            for label_names_test in label_name_for_hooter:
                if label_names_test is not None:
                    text = str(label_names_test) + ';'
                    hooter_empty_label_ls.append(text)
                hooter_final_label = ''
            # print("hooter_empty_label_lshooter_empty_label_lshooter_empty_label_lshooter_empty_label_ls12==",hooter_empty_label_ls)
            hooter_line.append('operate-on-label = {0}'.format(hooter_final_label.join(hooter_empty_label_ls)))
            if len(hooter_list_type) == 0 :
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
            print('-----------------hooter_list_type-----1.0.3-------------',hooter_list_type)
            hooter_line.append('hooter-ip = {0}'.format(hooteripstring))
            hooter_line.append('hooter-stop-buffer-time = 3')
            hooter_line.append('data-save-time-in-sec = 3') 
            hooter_line.append('analytics-details ={0}\n'.format(Newanalyticdetails))  
        lines.append('[roi-filtering-stream-{0}]'.format(index))
        lines.append('enable=1') 
        for test_roi_ra, roi_value in enumerate(x['roi_data']):
            label_name = roi_value['label_name']
            try:
                roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
            except Exception as error:
                roi_bbox = checkNegativevaluesinBbox(roi_value['bb_box'])
                ERRORLOGdata(" ".join(["\n", "[ERROR] write_config_funs -- roi_fun_no_crdd_data 3", str(error), " ----time ---- ", now_time_with_time()]))            
            roi_bbox= checkNegativevaluesinBbox(roi_bbox)
            lines.append('roi-RA-{0} = {1}'.format(roi_value['roi_name'], roi_bbox))  
        if 'trafficjam_data' in x :
            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                print('str(FinalTime)-------type---3-----0-------')
                config_tjm_lines.append('[TJM{0}]'.format(index))
                config_tjm_lines.append('enable=1' )
                Checkdetails ='details=['
                for j,roi_data in enumerate(x['trafficjam_data']):
                    roi_objects=set()
                    if validate_each_roi(roi_data,roi_required_keys):
                        if Checkdetails == 'details=[' :
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            FinalTime = FinalTime+ NewTIme['second']
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}'
                        else:
                            Checkdetails = Checkdetails+','
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            FinalTime = FinalTime+ NewTIme['second']
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}' 
                Checkdetails= Checkdetails+']'  
                config_tjm_lines.append(Checkdetails)   
                # lines.append('\n')
                # config_tjm_lines.append('\n')
        #     else:
        #         lines.append("enable=0")
        # else:
        #     lines.append("enable=0")

        lines.append('inverse-roi=0')
        roi__label_names = []
        for roi_val in x['roi_data']:
            # print("roi_val---",roi_val)
            for roi_val___test in roi_val['label_name']:
                roi__label_names.append(roi_val___test)
        roi_empty_label_ls = []
        for roi_label_name_test in ['0']:
            text = str(roi_label_name_test) + ';'
            roi_empty_label_ls.append(text)
        test_string = ''
        # lines.append('class-id= {0}'.format(test_string.join(roi_empty_label_ls)))
    else:
        hooter_line.append('[RA{0}]'.format(str(index)))
        hooter_line.append("enable = 0")
        hooter_line.append('analytics-type = 0')
        hooter_line.append("operate-on-label = person;")
        hooter_line.append("hooter-enable = 0")
        hooter_line.append('hooter-type = 0;')
        hooter_line.append('hooter-shoutdown-time = 10')
        print('-----------------hooter_list_type-----1.0.5-------------',hooter_list_type)
        hooter_line.append("hooter-ip = none")
        hooter_line.append("hooter-stop-buffer-time = 3")
        hooter_line.append("data-save-time-in-sec = 3") 
        hooter_line.append('analytics-details = none\n')  
    roi_enable_cam_ids.append(NewcameraID)
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
                    # if traffic_count_cls_name_cls_id[tc_val___test] not in tc_label_names:
                    # if traffic_count_cls_name_cls_id[tc_val___test] not in tc_label_names:
                    #     tc_val___test = traffic_count_cls_name_cls_id[tc_val___test]
                    tc_label_names.append(tc_val___test)


        tc_empty_label_ls = []
        for tc_label_name_test in tc_label_names:
            text = str(tc_label_name_test) + ';'
            tc_empty_label_ls.append(text)
        test_string = ''
        # lines.append('class-id= {0}'.format(test_string.join(tc_empty_label_ls)))
        lines.append('extended=1')
        lines.append('mode=loose\n')

    return True

def cr_fun_crowd_conf(x,crowd_line, index,cameraid, cr_enable_cam_ids,config_tjm_lines): 
    # print("entered main function_---cr 1====")
    max_cnt_ls =[]
    min_cnt_ls =[]
    cr_label_names=[]
    if len(x['cr_data']) != 0:
        if cameraid not in cr_enable_cam_ids:
            cr_enable_cam_ids.append(cameraid)
        # print("appending cr cameraids ==",cr_enable_cam_ids)
        crowd_line.append('[crdcnt{0}]'.format(index))
        crowd_line.append('enable=1')
        try_this_ls = []
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            try_this_ls.append(cr_value['full_frame'])
        # print("try_this_ls====",try_this_ls)
        # print("------------------------- CR MAIN FUNCTION",True in try_this_ls and False in try_this_ls)
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
                            # print("DATA OBJECT:", d_obj)
                            label_name.append(d_obj['class_name'])
                            # print("LABEL :--", label_name)
                            max_cnt_par.append(d_obj['max_count'])
                            # print("MAX_COUNT---", max_cnt_par)
                            min_cnt_par.append(d_obj['min_count'])
                            # print("MIN COUNT:", min_cnt_par)
                    else:
                        label_name.append(data_obj["class_name"])
                        # print("LABEL :--", label_name)
                        max_cnt_par.append(data_obj['max_count'])
                        # print("MAX_COUNT---", max_cnt_par)
                        min_cnt_par.append(data_obj['min_count'])
                        # print("MIN COUNT:", min_cnt_par)

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
                    # print("------------------", data_obj["class_name"])
                    if type(data_obj) == list:
                        for d_obj in data_obj:
                            # print("DATA OBJECT:", d_obj)
                            label_name.append(d_obj['class_name'])
                            # print("LABEL :--", label_name)
                            max_cnt_par.append(d_obj['max_count'])
                            # print("MAX_COUNT---", max_cnt_par)
                            min_cnt_par.append(d_obj['min_count'])
                            # print("MIN COUNT:", min_cnt_par)
                    else:
                        label_name.append(data_obj["class_name"])
                        # print("LABEL :--", label_name)
                        max_cnt_par.append(data_obj['max_count'])
                        # print("MAX_COUNT---", max_cnt_par)
                        min_cnt_par.append(data_obj['min_count'])
                        # print("MIN COUNT:", min_cnt_par)


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
            # print("Just TRAID LOOp", just_try)

            
            for data_object_upt in just_try:
                for data_obj in data_object_upt:
                    # print("DATA OBJECT:", data_object)
                    # res = not all(data_obj.values())
                    # print("RESULT:", res)
                    # if res == False:
                    #print("*******verifying *********", data_obj)
                    if type(data_obj) == list:
                        # print("11111111111111111")
                        for d_obj in data_obj:
                            label_name.append(d_obj['class_name'])
                            # print("LABEL :--", label_name)
                            max_cnt_par.append(d_obj['max_count'])
                            # print("MAX_COUNT---", max_cnt_par)
                            min_cnt_par.append(d_obj['min_count'])
                            # print("MIN COUNT:", min_cnt_par)

                    else:
                        # print("DATA OBJECT:", data_obj)
                        # print("2222222222222",label_name)
                        label_name.append(data_obj["class_name"])
                        # print("LABEL :--", label_name)
                        max_cnt_par.append(data_obj['max_count'])
                        # print("MAX_COUNT---", max_cnt_par)
                        min_cnt_par.append(data_obj['min_count'])
                        # print("MIN COUNT:11111111", min_cnt_par)
                        
                    # else:
                    #     pass

            if compare(label_name, cr_label_names) == False:
                # print("BEGINNING LABEl", label_name)
                for lab_nam in label_name:
                    # print("data_object:----------------", len(just_try),  lab_nam)
                    if len(just_try) <= 1:
                        if lab_nam not in cr_label_names:
                            cr_label_names.append(lab_nam)  
                            # print("CR LABEL lS--111111", cr_label_names)
                    else:
                        # print("LABELLING NAME:", lab_nam)
                        cr_label_names.append(lab_nam)
                        # print("CR LABEL lS--2222", cr_label_names)
            
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
            
        # if 'trafficjam_data' in x :
        #     if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
        #         print('str(FinalTime)-------type---3-----0-------')
        #         config_tjm_lines.append('[TJM{0}]'.format(index))
        #         config_tjm_lines.append('enable=1' )
        #         Checkdetails ='details=['
        #         for j,roi_data in enumerate(x['trafficjam_data']):
        #             roi_objects=set()
        #             if validate_each_roi(roi_data,roi_required_keys):
        #                 if Checkdetails == 'details=[' :
        #                     roi_objects= roi_objects.union(roi_data['selected_objects'])
                            #   roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
        #                     resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
        #                     lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
        #                     FinalTime = 0
        #                     if roi_data['min_time'] is not None:
        #                         NewTIme = roi_data['min_time']
        #                         if type(roi_data['min_time']) != int :
        #                             if 'hour' in NewTIme:
        #                                 if NewTIme['hour'] is not None:
        #                                     print("-----------------",NewTIme['hour'])
        #                                     FinalTime = 60*60*NewTIme['hour']
        #                             if 'minute' in NewTIme:
        #                                 if NewTIme['minute'] is not None:
        #                                     print("-----------------",NewTIme['minute'])
        #                                     FinalTime = FinalTime+ 60*NewTIme['minute']
        #                             if 'second' in NewTIme:
        #                                 if NewTIme['second'] is not None:
        #                                     print("-----------------",NewTIme['second'])
        #                                     FinalTime = FinalTime+ NewTIme['second']
        #                     print('str(FinalTime)-------type---6------------',type(FinalTime))
        #                     Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
        #                                                     '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
        #                                                     '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
        #                                                     '"verify-time":' + str(FinalTime) + '}'
        #                 else:
        #                     Checkdetails = Checkdetails+','
        #                     roi_objects= roi_objects.union(roi_data['selected_objects'])
        #roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
        #                     resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
        #                     lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
        #                     FinalTime = 0
        #                     if roi_data['min_time'] is not None:
        #                         NewTIme = roi_data['min_time']
        #                         if type(roi_data['min_time']) != int :
        #                             if 'hour' in NewTIme:
        #                                 if NewTIme['hour'] is not None:
        #                                     print("-----------------",NewTIme['hour'])
        #                                     FinalTime = 60*60*NewTIme['hour']
        #                             if 'minute' in NewTIme:
        #                                 if NewTIme['minute'] is not None:
        #                                     print("-----------------",NewTIme['minute'])
        #                                     FinalTime = FinalTime+ 60*NewTIme['minute']
        #                             if 'second' in NewTIme:
        #                                 if NewTIme['second'] is not None:
        #                                     print("-----------------",NewTIme['second'])
        #                                     FinalTime = FinalTime+ NewTIme['second']
        #                     print('str(FinalTime)-------type---5------------',type(FinalTime))
        #                     Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
        #                                                     '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
        #                                                     '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
        #                                                     '"verify-time":' + str(FinalTime) + '}' 
        #         Checkdetails= Checkdetails+']'  
        #         config_tjm_lines.append(Checkdetails) 


        
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


def cr_fun_conf_analytics(x,  lines,config_tjm_lines):
    cr_label_names=[]
    # print("entered analytics firstfunctions-===")
    if len(x['cr_data']) != 0:
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            # print("cr_valuecr_valuecr_valuecr_value",cr_value)
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
        if 'trafficjam_data' in x :
            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                # print('str(FinalTime)-------type---3-----0-------')
                config_tjm_lines.append('[TJM{0}]'.format(index))
                config_tjm_lines.append('enable=1' )
                Checkdetails ='details=['
                for j,roi_data in enumerate(x['trafficjam_data']):
                    roi_objects=set()
                    if validate_each_roi(roi_data,roi_required_keys):
                        if Checkdetails == 'details=[' :
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            print("-----------------",NewTIme['hour'])
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            print("-----------------",NewTIme['minute'])
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            print("-----------------",NewTIme['second'])
                                            FinalTime = FinalTime+ NewTIme['second']
                            # print('str(FinalTime)-------type---6------------',type(FinalTime))
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}'
                        else:
                            Checkdetails = Checkdetails+','
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            print("-----------------",NewTIme['hour'])
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            print("-----------------",NewTIme['minute'])
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            print("-----------------",NewTIme['second'])
                                            FinalTime = FinalTime+ NewTIme['second']
                            # print('str(FinalTime)-------type---5------------',type(FinalTime))
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}' 
                Checkdetails= Checkdetails+']'  
                config_tjm_lines.append(Checkdetails) 

        lines.append('inverse-roi=0')
        # lines.append('class-id= {0}\n'.format(test_string.join(cr_empty_label_ls)))
    return True



def cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines):
    cr_label_names=[]
    print("entered ===second function ")
    if len(x['cr_data']) != 0:
        lines.append('[roi-filtering-stream-{0}]'.format(str(index)))
        lines.append('enable=1')
        for test_cr_ra, cr_value in enumerate(x['cr_data']):
            # print("cr_valuecr_vaanalyticsPASSINGWRITEluecr_valuecr_value",cr_value)
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

        if 'trafficjam_data' in x :
            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                # print('str(FinalTime)-------type---3-----0-------')
                config_tjm_lines.append('[TJM{0}]'.format(index))
                config_tjm_lines.append('enable=1' )
                Checkdetails ='details=['
                for j,roi_data in enumerate(x['trafficjam_data']):
                    roi_objects=set()
                    if validate_each_roi(roi_data,roi_required_keys):
                        if Checkdetails == 'details=[' :
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            print("-----------------",NewTIme['hour'])
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            print("-----------------",NewTIme['minute'])
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            print("-----------------",NewTIme['second'])
                                            FinalTime = FinalTime+ NewTIme['second']
                            # print('str(FinalTime)-------type---6------------',type(FinalTime))
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}'
                        else:
                            Checkdetails = Checkdetails+','
                            # roi_objects= roi_objects.union(roi_data['selected_objects'])
                            roi_objects = roi_objects.union({"motorbike" if obj.lower() == "motorcycle" else obj for obj in roi_data['selected_objects']})
                            resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                            lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'].strip(), resized_roi_box))
                            FinalTime = 0
                            if roi_data['min_time'] is not None:
                                NewTIme = roi_data['min_time']
                                if type(roi_data['min_time']) != int :
                                    if 'hour' in NewTIme:
                                        if NewTIme['hour'] is not None:
                                            print("-----------------",NewTIme['hour'])
                                            FinalTime = 60*60*NewTIme['hour']
                                    if 'minute' in NewTIme:
                                        if NewTIme['minute'] is not None:
                                            print("-----------------",NewTIme['minute'])
                                            FinalTime = FinalTime+ 60*NewTIme['minute']
                                    if 'second' in NewTIme:
                                        if NewTIme['second'] is not None:
                                            print("-----------------",NewTIme['second'])
                                            FinalTime = FinalTime+ NewTIme['second']
                            # print('str(FinalTime)-------type---5------------',type(FinalTime))
                            Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                            '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                            '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                            '"verify-time":' + str(FinalTime) + '}' 
                Checkdetails= Checkdetails+']'  
                config_tjm_lines.append(Checkdetails) 
        lines.append('inverse-roi=0')
        # lines.append('class-id= {0}\n'.format(test_string.join(cr_empty_label_ls)))
    return True



def ppe_fun(x, index, ppe_enable_cam_ids,cameraid,PPELINE,onlyCrashHelmet):
    ppe_objects = ['vest', 'helmet', 'shoes','crash_helmet']
    if type(x['ppe_data']) == dict:
        if isEmpty(x['ppe_data']):
            ppe_objects = ['vest', 'helmet', 'shoes','crash_helmet']
            for keys, val in x['ppe_data'].items():
                if keys in ppe_objects:
                    if (val == True and cameraid not in ppe_enable_cam_ids):
                        ppe_enable_cam_ids.append(cameraid)
                        break
    elif type(x['ppe_data']) == list:
        if len(x['ppe_data']) != 0:
            if len(x['ppe_data']) == 1:
                dictionary_of_ppe = x['ppe_data'][0]
                if type(dictionary_of_ppe) == dict:
                    if isEmpty(dictionary_of_ppe):
                        ppe_objects = ['vest', 'helmet', 'shoes','crash_helmet']
                        for keys, val in dictionary_of_ppe.items():
                            if keys in ppe_objects:
                                if (val == True and cameraid not in ppe_enable_cam_ids):
                                    ppe_enable_cam_ids.append(cameraid)
                                    break

                                  
    roi_objects=set()
    # print("-------------RA WITH -----------roi_data_cf---1----------",x)
    roi_label_names =[]
    label_name_for_hooter =[]
    hooter_list_type =[] 
    if type(x['ppe_data']) == dict:
        if isEmpty(x['ppe_data']):
            PPELINE.append('[PPE{0}]'.format(str(index)))
            ANENABLEstring = '[' 
            for keys, val in x['ppe_data'].items():
                if keys in ppe_objects:
                    if val is True and keys=='helmet':
                        if ANENABLEstring != '[' :
                            if '[{"analytics_type":0, "operate_on": "vest;' ==ANENABLEstring:
                                ANENABLEstring=ANENABLEstring+'helmet;"}'
                            elif '[{"analytics_type":1, "operate_on": "crash_helmet;"},{"analytics_type":0, "operate_on": "vest;'==ANENABLEstring:
                                ANENABLEstring=ANENABLEstring+'helmet;"}'
                            elif '{"analytics_type": 0' in ANENABLEstring:
                                ANENABLEstring=ANENABLEstring+'helmet;"}'
                            else:
                                ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "helmet;'
                        else:
                            ANENABLEstring =ANENABLEstring+'{"analytics_type":0, "operate_on": "helmet;'
                    if val is True and keys=='vest':
                        if ANENABLEstring != '[' :
                            if '[{"analytics_type":0, "operate_on": "helmet;' ==ANENABLEstring:
                                ANENABLEstring=ANENABLEstring+'vest;"}'
                            elif '[{"analytics_type":1, "operate_on": "crash_helmet;"},{"analytics_type":0, "operate_on": "helmet;'==ANENABLEstring:
                                ANENABLEstring=ANENABLEstring+'vest;"}'
                            elif '{"analytics_type":0' in ANENABLEstring:
                                ANENABLEstring=ANENABLEstring+'vest;"}'
                            else:
                                ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "vest;'
                        else:
                            ANENABLEstring =ANENABLEstring+'{"analytics_type":0, "operate_on": "vest;'
                    if val is True and keys=='crash_helmet':
                        onlyCrashHelmet.append(cameraid)
                        if ANENABLEstring != '[' :
                            ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "crash_helmet;"}'
                        else:
                            ANENABLEstring =ANENABLEstring+'{"analytics_type":1, "operate_on": "crash_helmet;"}'
            if ANENABLEstring != '[':
                print('---------------------1---ANENABLEstring',ANENABLEstring)
                if '"}]' in ANENABLEstring:
                    ANENABLEstring=ANENABLEstring
                elif '"}' in ANENABLEstring:
                    if '[{"analytics_type":1, "operate_on": "crash_helmet;"}'==ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "helmet;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "vest;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "helmet;vest;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "vest;helmet;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    else:
                        ANENABLEstring=ANENABLEstring+']' 
                else:
                    if '[{"analytics_type":1, "operate_on": "crash_helmet;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "helmet;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "vest;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "helmet;vest;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    elif '[{"analytics_type":0, "operate_on": "vest;helmet;"}' == ANENABLEstring:
                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                    else:
                        ANENABLEstring=ANENABLEstring+'"}]' 
                PPELINE.append('enable = 1') 
            else:
                PPELINE.append('enable = 0') 
            if len(hooter_list_type) == 0:
                PPELINE.append('hooter-type = {0}'.format('0;'))            
            # PPELINE.append('analytics-type = 0')
            PPELINE.append('hooter-enable = 0')
            PPELINE.append('hooter-shoutdown-time = 10 ')
            PPELINE.append('hooter-ip = {0}'.format('none'))
            PPELINE.append('hooter-stop-buffer-time = 3')
            PPELINE.append('data-save-time-in-sec = 3')  
            PPELINE.append('analytics-details ={0}\n'.format(ANENABLEstring)) 
    elif type(x['ppe_data']) == list:
        if len(x['ppe_data']) != 0:
            if len(x['ppe_data']) == 1:
                dictionary_of_ppe = x['ppe_data'][0]
                # print('----------dictionary_of_ppe-------------1111----------',dictionary_of_ppe)
                

                if type(dictionary_of_ppe) == dict:
                    if isEmpty(dictionary_of_ppe):
                        PPELINE.append('[PPE{0}]'.format(str(index)))
                        ANENABLEstring = '[' 
                        for keys, val in dictionary_of_ppe.items():
                            if keys in ppe_objects:
                                if val is True and keys=='helmet':
                                    if ANENABLEstring != '[' :
                                        if '[{"analytics_type":0, "operate_on": "vest;' ==ANENABLEstring:
                                            ANENABLEstring=ANENABLEstring+'helmet;"}'
                                        elif '[{"analytics_type":1, "operate_on": "crash_helmet;"},{"analytics_type":0, "operate_on": "vest;'==ANENABLEstring:
                                            ANENABLEstring=ANENABLEstring+'helmet;"}'
                                        elif '{"analytics_type":0' in ANENABLEstring:
                                            ANENABLEstring=ANENABLEstring+'helmet;"}'
                                        else:
                                            ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "helmet;'
                                    else:
                                        ANENABLEstring =ANENABLEstring+'{"analytics_type":0, "operate_on": "helmet;'
                                if val is True and keys=='vest':
                                    if ANENABLEstring != '[' :
                                        if '[{"analytics_type":0, "operate_on": "helmet;' ==ANENABLEstring:
                                            ANENABLEstring=ANENABLEstring+'vest;"}'
                                        elif '[{"analytics_type":1, "operate_on": "crash_helmet;"},{"analytics_type":0, "operate_on": "helmet;'==ANENABLEstring:
                                            ANENABLEstring=ANENABLEstring+'vest;"}'
                                        elif '{"analytics_type": 0' in ANENABLEstring:
                                            ANENABLEstring=ANENABLEstring+'vest;"}'
                                        else:
                                            ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "vest;'
                                    else:
                                        ANENABLEstring =ANENABLEstring+'{"analytics_type":0, "operate_on": "vest;'
                                if val is True and keys=='crash_helmet':
                                    onlyCrashHelmet.append(cameraid)
                                    if ANENABLEstring != '[' :
                                        ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "crash_helmet;"}'
                                    else:
                                        ANENABLEstring =ANENABLEstring+'{"analytics_type":1, "operate_on": "crash_helmet;"}'
                        if ANENABLEstring != '[':
                            # print('------------------------ANENABLEstring',ANENABLEstring)
                            if '"}]' in ANENABLEstring:
                                ANENABLEstring=ANENABLEstring
                            elif '"}' in ANENABLEstring:
                                if '[{"analytics_type":1, "operate_on": "crash_helmet;"}' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+',{"analytics_type":0, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "helmet;"}' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "vest;"}' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "helmet;vest;"}' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "vest;helmet;"}' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+',{"analytics_type":1, "operate_on": "null;"}]'
                                else:
                                    ANENABLEstring=ANENABLEstring+']' 
                            else:
                                if '[{"analytics_type":1, "operate_on": "crash_helmet;' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+'"},{"analytics_type":0, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "helmet;' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+'"},{"analytics_type":1, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "vest;' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+'"},{"analytics_type":1, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "helmet;vest;' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+'"},{"analytics_type":1, "operate_on": "null;"}]'
                                elif '[{"analytics_type":0, "operate_on": "vest;helmet;' == ANENABLEstring:
                                    ANENABLEstring=ANENABLEstring+'"},{"analytics_type":1, "operate_on": "null;"}]'
                                else:
                                    ANENABLEstring=ANENABLEstring+'"}]' 
                            PPELINE.append('enable = 1') 
                        else:
                            PPELINE.append('enable = 0') 
                        if len(hooter_list_type) == 0:
                            PPELINE.append('hooter-type = {0}'.format('0;'))            
                        # PPELINE.append('analytics-type = 0')
                        if 'alert_details' in dictionary_of_ppe:
                            # print('=============dictionary_of_ppe[alert_details]====',dictionary_of_ppe['alert_details'])
                            if len(dictionary_of_ppe['alert_details'])!=0:
                                hooter_enable =0
                                nexthooterip = 'none'
                                for enableindex ,enblehooter in enumerate(dictionary_of_ppe['alert_details']):
                                    # print('--------enblehooter--ppe------',enblehooter)
                                    if 'hooter' in enblehooter and 'relay' in enblehooter:                                        
                                        if enblehooter['hooter']== True and enblehooter['relay']== True:
                                            hooter_enable=1
                                            if enblehooter['hooter_ip']==enblehooter['relay_ip']:
                                                nexthooterip=enblehooter['hooter_ip']
                                            elif enblehooter['hooter_ip']:
                                                nexthooterip=enblehooter['hooter_ip']
                                            elif enblehooter['relay_ip']:
                                                nexthooterip=enblehooter['hooter_ip']
                                        elif enblehooter['hooter']== True :
                                            hooter_enable=1
                                            nexthooterip=enblehooter['hooter_ip']
                                        elif  enblehooter['relay']== True:
                                            hooter_enable=1
                                            nexthooterip=enblehooter['hooter_ip']
                                    else:
                                        print('---------------enableindex else------------')



                                PPELINE.append('hooter-enable = {0}'.format(hooter_enable))
                                PPELINE.append('hooter-shoutdown-time = 10 ')
                                PPELINE.append('hooter-ip = {0}'.format(nexthooterip))
                                PPELINE.append('hooter-stop-buffer-time = 3')
                                PPELINE.append('data-save-time-in-sec = 3')  
                                PPELINE.append('analytics-details ={0}\n'.format(ANENABLEstring))

                            else:

                                PPELINE.append('hooter-enable = 0')
                                PPELINE.append('hooter-shoutdown-time = 10 ')
                                PPELINE.append('hooter-ip = {0}'.format('none'))
                                PPELINE.append('hooter-stop-buffer-time = 3')
                                PPELINE.append('data-save-time-in-sec = 3')  
                                PPELINE.append('analytics-details ={0}\n'.format(ANENABLEstring))
                        else:
                            PPELINE.append('hooter-enable = 0')
                            PPELINE.append('hooter-shoutdown-time = 10 ')
                            PPELINE.append('hooter-ip = {0}'.format('none'))
                            PPELINE.append('hooter-stop-buffer-time = 3')
                            PPELINE.append('data-save-time-in-sec = 3')  
                            PPELINE.append('analytics-details ={0}\n'.format(ANENABLEstring)) 
            



# def ppe_fun(x, index, ppe_enable_cam_ids,cameraid):
#     if type(x['ppe_data']) == dict:
#         if isEmpty(x['ppe_data']):
#             ppe_objects = ['vest', 'helmet', 'shoes','crash_helmet']
#             for keys, val in x['ppe_data'].items():
#                 if keys in ppe_objects:
#                     if (val == True and cameraid not in ppe_enable_cam_ids):
#                         (to_check_the_truck_label_in_roi_data) = []
#                         if len(x['roi_data']) != 0:
#                             for test_roi_ra, roi_value in enumerate(x['roi_data']):
#                                 label_name = roi_value['label_name']
#                                 if len(label_name) == 1:
#                                     if ('truck' in label_name):
#                                         to_check_the_truck_label_in_roi_data.append(cameraid)
#                                 elif len(label_name) > 1:
#                                     if ('truck' in label_name and 'person' in label_name):
#                                         pass
#                             if len(to_check_the_truck_label_in_roi_data) == 0:
#                                 ppe_enable_cam_ids.append(cameraid)
#                         else:
#                             ppe_enable_cam_ids.append(cameraid)
#     elif type(x['ppe_data']) == list:
#         if len(x['ppe_data']) != 0:
#             if len(x['ppe_data']) == 1:
#                 dictionary_of_ppe = x['ppe_data'][0]
#                 if type(dictionary_of_ppe) == dict:
#                     if isEmpty(dictionary_of_ppe):
#                         ppe_objects = ['vest', 'helmet', 'shoes','crash_helmet']
#                         for keys, val in dictionary_of_ppe.items():
#                             if keys in ppe_objects:
#                                 if (val == True and cameraid not in ppe_enable_cam_ids):
#                                     (to_check_the_truck_label_in_roi_data) = []
#                                     if len(x['roi_data']) != 0:
#                                         for test_roi_ra, roi_value in enumerate(x['roi_data']):
#                                             (label_name) = (roi_value['label_name'])
#                                             if len(label_name) == 1:
#                                                 if ('truck' in label_name):
#                                                     to_check_the_truck_label_in_roi_data.append(cameraid)
#                                             elif len(label_name) > 1:
#                                                 if ('truck' in label_name and 'person' in label_name):
#                                                     pass
#                                         if len(to_check_the_truck_label_in_roi_data) == 0:
#                                             ppe_enable_cam_ids.append(cameraid)
#                                     else:
#                                         ppe_enable_cam_ids.append(cameraid)
