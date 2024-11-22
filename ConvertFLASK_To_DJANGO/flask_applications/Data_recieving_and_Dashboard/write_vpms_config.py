from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_config_funcs import *
import json
from psycopg2.extras import Json 
create_vpms_config=Blueprint('create_vpms_config', __name__)
def connect_to_db(database_details):
    try :
     connection=psycopg2.connect(user=database_details['user'],password=database_details['password'],host=database_details['host'],port=database_details['port'],database=database_details['db_name'], sslmode=database_details['sslmode'])
     
     return connection
    except Exception as err:
        raise Exception
def is_table_exist(conn,table):
        exists=False
        cursor=conn.cursor()
        query=f'''SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public' '''
        try:
            cursor.execute(query)
            tables=[table[0] for table in cursor.fetchall()]
            print('tables',list(tables))
            exists=table in list(tables)
            cursor.close()
            print(exists)
            return exists
        except Exception as e:
            print(e)
        
def insert_vpms_data_to_table(conn,vpms_enabled_camaras):
    # print('------------------------------------vpms--enableed-------dataof ----------------',vpms_enabled_camaras)
    cursor=conn.cursor()
    #keeys needs to be added later='other_time_violation','set_time_option,'date','other_objects_violation
    inserting_data=[]
    temp=[]
    # print('vpms_enabled_camaras========type===',type(vpms_enabled_camaras))
    roi_required_keys=['roi_name','roi_id','selected_objects','bb_box','parking_type','date','other_time_violation','set_time_option','other_objects_violation','alarm_type','alarm_ip_address']
    for i,camera_data in enumerate(vpms_enabled_camaras):
        # print('------------validate_rois_array---------',validate_rois_array(camera_data['vpms_data'],roi_required_keys))
        if validate_rois_array(camera_data['vpms_data'],roi_required_keys):
            # print("-------------------validate_rois_array------------",roi_required_keys)
            temp.append(camera_data['rtsp_url'])
            temp_vpms_data=[]
            width_ratio=960/960#1920/1150
            height_ratio= 544/544
            # width_ratio=1920/1150
            # height_ratio= 1080/647
            for j,roi_data in enumerate(camera_data['vpms_data']):
                # print('-------------roi_data---------------------',roi_data)

                # print('-----------------------validate_each_roi(roi_data,roi_required_keys)------------',validate_each_roi(roi_data,roi_required_keys))
                if validate_each_roi(roi_data,roi_required_keys):
                    # print("roi_data----parking_type-----------",roi_data['parking_type'])
                    if not is_neg_points_in_bbox(roi_data['bb_box']):
                    # diff= roi_objects.difference(roi_data['selected_objects'])
                    # if len(diff)>0 :
                        resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                        # print("---------------type----------------roi_data['set_time_option']",roi_data['set_time_option'])

                        Newdictadd_table = {}
                        # if roi_data['parking_type']== 'no-parking':
                        #     Newdictadd_table['roi_name']='NPA-'+roi_data['roi_name']
                        # else:
                        #     Newdictadd_table['roi_name']='PA-'+roi_data['roi_name']
                        Newdictadd_table['roi_name']=roi_data['roi_name']
                        Newdictadd_table['roi_bbox']=resized_roi_box
                        Newdictadd_table['enable']=1
                        if type(roi_data['selected_objects']) ==list:
                            if len(roi_data['selected_objects']) !=0 :
                                Newdictadd_table['operate_on_label'] = ';'.join("motorbike" if obj.lower() == "motorcycle" else obj.lower() for obj in roi_data['selected_objects']) + ';'
                                # Newdictadd_table['operate_on_label']=';'.join(obj.lower() for obj in roi_data['selected_objects']) + ';'#';'.join(roi_data['selected_objects'])+';'
                            else:
                                Newdictadd_table['operate_on_label']='bicycle;car;motorbike;bus;train;truck'#'NULL'
                        else:
                            Newdictadd_table['operate_on_label']='bicycle;car;motorbike;bus;train;truck'#'NULL'
                        if roi_data['other_objects_violation'] != None:
                            if roi_data['other_objects_violation']['violation']=='yes':
                                Newdictadd_table['violation_label'] = ';'.join( "motorbike" if obj.lower() == "motorcycle" else obj.lower() for obj in roi_data['other_objects_violation']['violation_objects']) + ';'
                                # Newdictadd_table['violation_label']=';'.join(obj.lower() for obj in roi_data['other_objects_violation']['violation_objects']) + ';'#';'.join(roi_data['other_objects_violation']['violation_objects'])+';'
                            else:
                                Newdictadd_table['violation_label']='NULL'

                        else:
                            Newdictadd_table['violation_label']='NULL'
                        if  roi_data['set_time_option']!=None:
                            if roi_data['set_time_option'].lower()=='no':
                                Newdictadd_table['time_slot_enable']=0
                            else:
                                Newdictadd_table['time_slot_enable']=1
                        else:
                            Newdictadd_table['time_slot_enable']=0
                        
                        if roi_data['date'] != None:
                            if roi_data['date']['startDate']:
                                Newdictadd_table['start_time']=roi_data['date']['startDate']
                            else:
                                Newdictadd_table['start_time']='NULL'
                        else:
                            Newdictadd_table['start_time']='NULL'

                        if  roi_data['date']!=None:
                            if roi_data['date']['endDate']: 
                                Newdictadd_table['stop_time']=roi_data['date']['endDate']
                            else:
                                Newdictadd_table['stop_time']='NULL'
                        else:
                            Newdictadd_table['stop_time']='NULL'
                        if roi_data['other_time_violation']=='yes':
                            Newdictadd_table['out_of_time_violation']=1
                        else:
                            Newdictadd_table['out_of_time_violation']=0

                        if (roi_data['parking_type']=='no-parking')  :
                            Newdictadd_table['type']='NPA' 
                        else:
                            Newdictadd_table['type']='PA'

                        if 'vehicle_verification_time' in roi_data:
                            if roi_data['vehicle_verification_time'] is not None :
                                Newdictadd_table['verification_time']=int(roi_data['vehicle_verification_time'])
                            else:
                                Newdictadd_table['verification_time']=10
                        else:
                            Newdictadd_table['verification_time']=10
                        # print("Newdictadd_table---",Newdictadd_table)
                        # # if type(roi_data['set_time_option']) ==None:
                        temp_vpms_data.append(Newdictadd_table)
                            # temp_vpms_data.append({'roi_name':roi_data['roi_name'],'roi_bbox':resized_roi_box,'enable':1,'type':'NPA' if (roi_data['parking_type']=='no-parking') else 'PA','operate_on_label':roi_data['selected_objects'],'violation_label':roi_data['other_objects_violation'],'time_slot_enable':0 if roi_data['set_time_option']!=None else 1,'Start_time':roi_data['date']['startDate'] if roi_data['date'] != None else 'NULL','Stop_time':roi_data['date']['endDate'] if roi_data['date']!=None else 'NULL','Out_ot_time_violation':1 if roi_data['other_time_violation']=='yes' else 0 })
                        # else:
                            # temp_vpms_data.append(Newdictadd_table)
                            # temp_vpms_data.append({'roi_name':roi_data['roi_name'],'roi_bbox':resized_roi_box,'enable':1,'type':'NPA' if (roi_data['parking_type']=='no-parking') else 'PA','operate_on_label':roi_data['selected_objects'],'violation_label':roi_data['other_objects_violation'],'time_slot_enable':0 if roi_data['set_time_option'].lower()=='no' else 1,'Start_time':roi_data['date']['startDate'] if roi_data['date'] != None else 'NULL','Stop_time':roi_data['date']['endDate'] if roi_data['date']!=None else 'NULL','Out_ot_time_violation':1 if roi_data['other_time_violation']=='yes' else 0 })

            temp.append(json.dumps(temp_vpms_data))
            inserting_data.append(temp) 
            print('')
        temp=[]
        temp_vpms_data=[]

    # print('----------------inserting_data-----$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4------',inserting_data)
    for i,data in enumerate(inserting_data):
       try:
        # query='
        cursor.execute('''INSERT INTO configuration_table (camera_rtsp,vpms) VALUES(%s,%s);''',(str(data[0]),data[1]))
        conn.commit()
       except Exception as err:
           raise(err)
    conn.close()
def create_configuration_table() :
    connection=None
    database_details={'db_name':'docketrundb','user':'docketrun','password':'docketrun','host':'localhost','port':'5432','sslmode':'disable'}
    try :
     connection=psycopg2.connect(user=database_details['user'],password=database_details['password'],host=database_details['host'],port=database_details['port'],database=database_details['db_name'], sslmode=database_details['sslmode'])
     cursor=connection.cursor()
     if not is_table_exist(connection,'configuration_table'):
         query='''CREATE TABLE configuration_table(camera_rtsp TEXT,vpms JSONB)'''
         cursor.execute(query)
         connection.commit()
     else:
         query="select * from configuration_table"
         cursor.execute(query)
         cursor.fetchone()
         columns=set([col[0] for col in cursor.description])
         new_columns=set(['camera_rtsp','vpms_data'])
        #  print(len(columns.difference(new_columns)))
         if(len(columns.difference(new_columns))==0):
             query='''TRUNCATE TABLE configuration_table'''
             cursor.execute(query)
             connection.commit()
         else:
             query='''DROP TABLE configuration_table'''
             cursor.execute(query)
             connection.commit()
             query='''CREATE TABLE configuration_table(camera_rtsp TEXT,vpms JSONB)'''
             cursor.execute(query)
             connection.commit()
     return connection      
    except [Exception,psycopg2.errors.UndefinedTable,psycopg2.errors.InFailedSqlTransaction] as err:
         raise(err)
def get_classIDs(object_array):
    class_ids_array=[]
    objects_array=['person','bicycle','car','motorbike','motorcycle','airplane','bus','train','truck','boat','fire hydrant']
    for  index,object in enumerate(object_array):
         class_ids_array.append(str(objects_array.index( object.lower())))
    return class_ids_array
    
def validate_rois_array(arr,keys_array):
    validation_status=False
    for obj in arr:
        if not validation_status:
            validation_status=validate_each_roi(obj,keys_array)
        else :
          return True
    return validation_status

# def validate_each_roi(obj,keys):
#     print('---------obj--------------',obj)
#     print('---------keys--------------',keys)
#     validation_status=True
#     for key in keys:
#         if key == 'parking_type':
#             if obj[key] !='no-parking':
#                 if obj[key] and not ( obj[key]==''or obj[key]== None  ):
#                     validation_status=True
#                 else:
#                     print('--------key-----888888888888888888888-----1.0---------------',key)
#                     validation_status=False
#                     break
#         else:
#             if obj[key] and not ( obj[key]==''or obj[key]== None  ):
#                 validation_status=True
#             else:
#                 print('--------key-----888888888888888888888------1.1--------------',key)
#                 validation_status=False
#                 break
#     return validation_status


# def validate_each_roi(obj, keys):
#     # print('---------obj--------------', obj)
#     # print('---------keys--------------', keys)
#     validation_status = True
#     for key in keys:
#         if key == 'parking_type':
#             if obj[key] == 'parking':
#                 if not obj[key] or obj[key] == '':
#                     validation_status = False
#                     print('--------key-----888888888888888888888-----1.0---------------', key)
#                     break
#         elif key in ['selected_objects', 'other_objects_violation', 'set_time_option', 'date', 'other_time_violation']:
#             if obj['parking_type'] != 'no-parking':
#                 if not obj[key] or obj[key] == '':
#                     print('--------key-----888888888888888888888------1.1--------------', key)
#                     validation_status = False
#                     break
#         else:
#             if not obj[key] or obj[key] == '':
#                 print('--------key-----888888888888888888888------1.2--------------', key)
#                 validation_status = False
#                 break

#     return validation_status
def validate_each_roi(obj, keys):
    validation_status = True    
    for key in keys:
        # Debug print statements to trace the validation steps
        # print(f'Checking key: {key}, for object: {obj}')
        
        if key == 'parking_type':
            if not obj.get(key):
                validation_status = False
                # print(f'Validation failed: Missing or empty key - {key}')
                break
        
        elif key in ['selected_objects', 'other_objects_violation', 'set_time_option', 'date', 'other_time_violation']:
            if obj.get('parking_type') == 'no-parking':
                continue
                # if not obj.get(key):
                #     validation_status = False
                #     print(f'Validation failed: Missing or empty key for no-parking type - {key}')
                #     break
            else:
                continue  # Skip validation for these keys if not 'no-parking'
        
        else:
            if not obj.get(key):
                validation_status = False
                # print(f'Validation failed: Missing or empty key - {key}')
                break

    return validation_status
def resize_roi(roi_points,width_ratio=1,height_ratio=1):
     points_array=roi_points.split(';')
     points_array=points_array[0:(len(points_array)-1)]
     print(points_array)
     new_resized_points=[]
     for index,point in enumerate(points_array):
         if index%2==0:
             new_resized_points.append(str(math.floor( int(point)*width_ratio)))
         else:
             new_resized_points.append(str(math.floor(int(point)*height_ratio)))
     print(';'.join(new_resized_points))
     return ';'.join(new_resized_points)
 
def is_neg_points_in_bbox(roi_points,):
     neg_presence=False
     points_array=roi_points.split(';')
     points_array=points_array[0:(len(points_array)-1)]
     for index,point in enumerate(points_array):
          if(int(point)<0):
              neg_presence=True
              break
          else:
              neg_presence=False
     return neg_presence
    
     
def get_sample_parking_config_file():
    sample_config_file=os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'sample_vpms_config_file.txt') 
    if not os.path.exists(sample_config_file):
        with open(sample_config_file,'w') as file:
             file.write("%s\n"%'''################################################################################
# Copyright (c) 2021-2022 DOCKETRUN TECH PRIVATE LIMITED. All rights reserved.
################################################################################

[application]

[tiled-display]

[sources]
[sink0]

[osd]

[streammux]

[primary-gie]


[tracker]


[nvds-analytics]

[application-config]


camera-ids = -1;
data-save-interval = 1''')
    return sample_config_file

def create_vpms_config_folder():
  vpms_config_folder = get_current_dir_and_goto_parent_dir() + '/Vehicle-parking-management-system/configs/'
  vpms_config_file=os.path.join(vpms_config_folder+'/'+"config_1.txt")
  vpms_config_analytics_file=os.path.join(vpms_config_folder+'/'+"config_analytics_1.txt")
  if not os.path.exists(vpms_config_folder):
        os.makedirs(vpms_config_folder)
  else :
       for i,file_name in enumerate(os.listdir(vpms_config_folder)):
           if file_name.endswith('.txt'):
            file_path=os.path.join(vpms_config_folder+file_name)
            os.remove(file_path)
    
  vpms_config_file=os.path.join(vpms_config_folder+'/'+"config_1.txt")
  vpms_config_analytics_file=os.path.join(vpms_config_folder+'/'+'config_analytics_1.txt')
      
  return (vpms_config_folder,vpms_config_file,vpms_config_analytics_file)

def write_array_to_file(file,arr):
    for line in arr:
        file.write('%s\n'%line)
    file.write('\n')
    
def create_vpms_config_file(vpms_enabled_cameras):
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
    classId = '0'
    gridview_true =True
    print("Genral_configurations===",Genral_configurations)
    batch_pushouttime = 40000
    drop_frame_interval=1
    ticket_reset_time =10
    displayfontsize = 12
    display_tracker =True
    if ('drop_frame_interval' in Genral_configurations and Genral_configurations['drop_frame_interval'] is not None) and ('camera_fps' in Genral_configurations and  Genral_configurations['camera_fps'] is not None) :
        camera_fps = Genral_configurations['camera_fps']
        drop_frame_interval = Genral_configurations['drop_frame_interval']
        Newpushouttime = math.ceil(int(camera_fps)/int(drop_frame_interval))
        batch_pushouttime= math.ceil(1000000/Newpushouttime)
    rtsp_reconnect_interval = 3
    
    if ('rtsp_reconnect_interval' in Genral_configurations and Genral_configurations['rtsp_reconnect_interval'] is not None):
        rtsp_reconnect_interval = Genral_configurations['rtsp_reconnect_interval'] 
    

    if ('grid_view' in Genral_configurations and Genral_configurations['grid_view'] is not None):
        gridview_true = Genral_configurations['grid_view'] 
    numberofsources_= 4
    if ('grid_size' in Genral_configurations and Genral_configurations['grid_size'] is not None):
        numberofsources_ = int(Genral_configurations['grid_size'])


    if ('ticket_reset_time' in Genral_configurations and Genral_configurations['ticket_reset_time'] is not None):
        ticket_reset_time = int(Genral_configurations['ticket_reset_time'])

    if 'display_font_size' in Genral_configurations :
        displayfontsize = Genral_configurations['display_font_size']

    if 'display_tracker' in Genral_configurations :
        display_tracker = Genral_configurations['display_tracker']

    creation_status={'message':"Vehicle parking management application started succesfully",'success':True}
    valid_camera_list=list()
    vpms_config_folder,vpms_config_file,vpms_config_analytics_file=create_vpms_config_folder()
    sample_config_file=get_sample_parking_config_file()
    lines=[]
    config_tjm_lines=[]
    config_analytics_lines=[]
    #keeys needs to be added later='other_time_violation','set_time_option,'date','other_objects_violation
    roi_required_keys=['roi_name','roi_id','selected_objects','bb_box','parking_type']
    solution_enabled_camera_count=len(vpms_enabled_cameras)
    #writing config_TJM file
    count_analytics=-1
    for i,camera_data in enumerate(vpms_enabled_cameras):
        if validate_rois_array(camera_data['vpms_data'],roi_required_keys):
            count_analytics=count_analytics+1
            valid_camera_list.append(camera_data)
            config_analytics_lines.append('[roi-filtering-stream-{0}]'.format(count_analytics))
            config_analytics_lines.append('enable=1' if camera_data['analytics_status']=='true'else 'enable=0')
            roi_objects=set()
            width_ratio=960/960#1920/1150
            height_ratio= 544/544#1080/647
            for j,roi_data in enumerate(camera_data['vpms_data']):
                if validate_each_roi(roi_data,roi_required_keys):
                    if not is_neg_points_in_bbox(roi_data['bb_box']):
                        # diff= roi_objects.difference(roi_data['selected_objects'])
                        # if len(diff)>0 :
                        roi_objects= roi_objects.union(get_classIDs(roi_data['selected_objects']))
                        resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                        # if roi_data['parking_type']=='no-parking':
                        #     config_analytics_lines.append('roi-VPMS-NPA-{0}={1}'.format(roi_data['roi_name'], resized_roi_box))
                        # else:
                        #     config_analytics_lines.append('roi-VPMS-PA-{0}={1}'.format(roi_data['roi_name'], resized_roi_box))

                        config_analytics_lines.append('roi-VPMS-{0}={1}'.format(roi_data['roi_name'], resized_roi_box))


            if len(list(roi_objects)) !=0:
                config_analytics_lines.append('inverse-roi=0')
                # config_analytics_lines.append('class-id={0}'.format(';'.join(list(roi_objects))+';'))
                config_analytics_lines.append('class-id=1;2;3;5;6;7;')
                config_analytics_lines.append('\n')
            else:
                config_analytics_lines.append('inverse-roi=0')
                config_analytics_lines.append('class-id=1;2;3;5;6;7;')
                config_analytics_lines.append('\n')
    if len(valid_camera_list)>0:
       solution_enabled_camera_count=len(valid_camera_list)                   
      #writing config_analytics_file      
       with open(vpms_config_analytics_file, 'w') as file:
        init_line=f'''[property]\nenable=1\n
config-width=960
config-height=544
#osd-mode 0: Dont display any lines, rois and text
#         1: Display only lines, rois and static text i.e. labels
#         2: Display all info from 1 plus information about counts
osd-mode=2\n
#Set OSD font size that has to be displayed
display-font-size={displayfontsize}\n'''
        file.write('%s\n'%init_line)
        write_array_to_file(file,config_analytics_lines)
        file.close()
    if len(valid_camera_list)>0:     
     with open(sample_config_file) as file:
        for index, line in enumerate(file):
            if line.strip() == '[application]':
                lines.append('[application]')
                lines.append('enable-perf-measurement=0')
                lines.append('perf-measurement-interval-sec=5\n')
            
            elif line.strip() == '[tiled-display]': 
                rows,columns = get_layout(solution_enabled_camera_count)
                lines.append('[tiled-display]')
                if gridview_true is True:
                    lines.append('enable=1')
                else:
                    lines.append('enable=0')
                lines.append('rows={0}'.format(str(rows)))
                lines.append('columns={0}'.format(str(columns)))
                lines.append('width=1280')
                lines.append('height=720')
                lines.append('gpu-id=0')
                lines.append('nvbuf-memory-type=0\n')
            elif line.strip() == '[sources]':
                source_added = []
                normal_config_file = 0

                for n, camera_details in enumerate(valid_camera_list):
                    cam_id = '{0}'.format(int(n) + 1)
                    #roi_enable_cam_ids_exist = roi_enable_cam_ids.count(int(cam_id))

                    if n+ 1 not in source_added:
                        uri = camera_details['rtsp_url']
                        lines.append('[source{0}]'.format(n))
                        lines.append('enable=1')
                        if ".mp4" in uri or ".mp3" in uri:
                            lines.append('type=3')
                        else:
                            lines.append('type=4')
                        lines.append('uri = {0}'.format(uri))
                        lines.append('num-sources=1')
                        lines.append('gpu-id=0')
                        lines.append('nvbuf-memory-type=0')
                        lines.append('latency=500')
                        lines.append('camera-id={0}'.format(int(n) + 1))
                        lines.append('camera-name={0}'.format(camera_details['cameraname']))
                        if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                            lines.append('drop-frame-interval = {0}'.format(drop_frame_interval))
                        else:
                            lines.append('drop-frame-interval = 1')
                        lines.append('rtsp-reconnect-interval-sec=1\n')
                        normal_config_file += 1
                        source_added.append(int(n) + 1)
            
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
                lines.append('nvbuf-memory-type=0\n')
            
            elif line.strip() == '[osd]':
                lines.append('[osd]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('border-width=4')
                lines.append('text-size=15')
                lines.append('text-color=1;1;1;1;')
                # lines.append('text-bg-color=0.3;0.3;0.3;1;')#dark
                lines.append('text-bg-color=1;0;0;0;')
                lines.append('font=Arial')
                lines.append('show-clock=0')
                lines.append('clock-x-offset=800')
                lines.append('clock-y-offset=820')
                lines.append('clock-text-size=12')
                lines.append('clock-color=1;0;0;0')
                lines.append('nvbuf-memory-type=0\n')
            
            elif line.strip() == '[streammux]':
                lines.append('[streammux]')
                lines.append('gpu-id=0')
                lines.append('live-source=1')
                lines.append('batch-size={0}'.format(len(list(valid_camera_list))))
                if batch_pushouttime == 40000:
                    lines.append('batched-push-timeout=40000')
                else:
                    lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                # lines.append('batched-push-timeout=40000')
                lines.append('width=960')
                lines.append('height=544')
                lines.append('enable-padding=0')
                lines.append('nvbuf-memory-type=0\n')
            
            elif line.strip() == '[primary-gie]':
                lines.append('[primary-gie]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('batch-size={0}'.format(len(list(valid_camera_list))))
                # lines.append('bbox-border-color0=0;1;0;0.7')#person --green 
                # lines.append('bbox-border-color0=1;0.3;0.9;1')#bus --pink 
                lines.append('bbox-border-color0=0.3;0;0;1')# dark shade of red or choclate
                # lines.append('bbox-border-color1=0;1;1;1')# red 
                lines.append('bbox-border-color1=1;0.3;0.9;1')#pinkish-purple or magenta
                lines.append('bbox-border-color2=0.545;0;1;1')#purple
                lines.append('bbox-border-color3=1;0.659;0;1')#orange
                # lines.append('bbox-border-color3=0;1;0;1')
                lines.append('bbox-border-color4=0.561;0.737;0.561;1')#dark sea green 
                lines.append('bbox-border-color5=0.502;0.502;0;1')#olive color
                lines.append('bbox-border-color6=0.392;0.584;0.929;1')#corn flower blue
                lines.append('bbox-border-color7=0.941;0.502;0.502;1')#light coral
                lines.append('nvbuf-memory-type=0')
                lines.append('interval=0')
                lines.append('gie-unique-id=1')
                # lines.append('model-engine-file=../model_b2_gpu0_fp16.engine')
                lines.append('config-file = ../../models/yoloV8/vpms_config_1.txt\n')

            elif line.strip() == '[tracker]':
                lines.append('[tracker]')
                lines.append('enable=1')
                lines.append('tracker-width=960')
                lines.append('tracker-height=544')
                lines.append("ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so")
                lines.append("ll-config-file=../../models/config_tracker_NvDCF_perf.yml")
                lines.append('gpu-id=0')
                if display_tracker :
                    lines.append('display-tracking-id=1')
                else:
                    lines.append('display-tracking-id=0')

            
            elif line.strip() == '[tests]':
                lines.append('[tests]')
                lines.append('file-loop=1\n')
                lines.append('[docketrun-device]')
                lines.append('gui-title = DOCKETRUN-VA-1-SYSTEM')
                lines.append('data-upload = 1\n')
            
                        
            elif line.strip() == '[nvds-analytics]':
                lines.append('[nvds-analytics]')
                lines.append('enable = 1')
                lines.append('config-file = ./config_analytics_1.txt\n')
            elif line.strip()=='[tests]':
                lines.append('[tests]')
                lines.append('file-loop=1')
            
            elif line.strip() == '[application-config]':
                lines.append('[application-config]')
                lines.append('app-title =   DocketEye-Road-Safety\n')
                lines.append('image-save-path = images/frame')
            else:
                pass
               
        with open(vpms_config_file, 'w') as f:
         for O_O_O, item in enumerate(lines):
            f.write('%s\n' % item)

        #len(list(valid_camera_list))
        index=1
        modelFileWritingYolo8(index, valid_camera_list)
    else:
        creation_status['message']="Proper AI solution details are not added to any cameras"
        creation_status['success']=False
    return creation_status



def CheckforOnlyParkingORNOparking(VPSM_Enableddata ):
    FinalEnableVPMS = VPSM_Enableddata
    # print("------------Vpmsenabled -------",VPSM_Enableddata)
    no_parking= False
    Onlyparking = False
    aisolutions = VPSM_Enableddata['ai_solution']
    newdata= []
    # print('------------ai_solution----',aisolutions)
    if 'NO_Parking' in aisolutions:
        if aisolutions['NO_Parking']:
            no_parking=True
    if 'Parking' in aisolutions:
        if aisolutions['Parking']:
            Onlyparking=True

    
    if 'vpms_data' in VPSM_Enableddata:
        VPMSDatachecking =  VPSM_Enableddata['vpms_data'] 
        # print('---------VPMSDatachecking--------------',VPMSDatachecking )
        for Indexdata , ActualdataofVpms in enumerate(VPMSDatachecking):
            # print('----------ActualdataofVpms-------',ActualdataofVpms)
            if no_parking==True and Onlyparking ==True:
                if ActualdataofVpms['parking_type']=='no-parking' or ActualdataofVpms['parking_type']=='parking':
                    newdata.append(ActualdataofVpms)
            elif no_parking==True :
                if ActualdataofVpms['parking_type']=='no-parking' :
                    newdata.append(ActualdataofVpms)
            elif  Onlyparking ==True:
                if ActualdataofVpms['parking_type']=='parking':
                    newdata.append(ActualdataofVpms)
    FinalEnableVPMS['vpms_data']= newdata

    return FinalEnableVPMS

        

    
    

def get_vpms_added_cameras():
    #,{'trafficjam_data':{'bb_box':{'$exists':True},'roi_name':{'$exists':True}}}
    temp=list([])
    # cameras_data=list(mongo.db.ppera_cameras.find({'$and':[{ 'camera_status':True},{'ai_solution.Parking':{'$exists':True}},{'ai_solution.Parking':True},{'analytics_status':'true'} ,{'vpms_data':{'$exists':True}},{'vpms_data.0':{'$exists':True}}]}))
    cameras_data= list(mongo.db.ppera_cameras.find({
    '$and': [
        {'camera_status': True},
        {'analytics_status': 'true'},
        {'vpms_data': {'$exists': True}},
        {'vpms_data.0': {'$exists': True}},
        {
            '$or': [
                {'ai_solution.Parking': {'$exists': True}},
                {'ai_solution.NO_Parking': {'$exists': True}}
            ]
        }
    ]
}))
    for i,camera_data in enumerate(cameras_data):
        #    print('camera index',i,camera_data)
           Newdata= CheckforOnlyParkingORNOparking(camera_data)
           temp.append(Newdata)
    return temp


def modelFileWritingYolo8(configindex,total_stream_for_stremux_union):
    GPUSINDEX=0
    vpms_modelconfigfile = get_current_dir_and_goto_parent_dir() + '/models/yoloV8/vpms_config_{0}.txt'.format(configindex)
    person_threshold=0.7
    modelconfigwrite =[]
    modelconfigwrite.append('[property]')
    modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
    modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
    modelconfigwrite.append('model-color-format=0')
    modelconfigwrite.append('custom-network-config={0}/models/yoloV8/yolov8x.cfg'.format(get_current_dir_and_goto_parent_dir()))
    enginFilePath = '{2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
    if os.path.exists(enginFilePath):
        # print("yolov8 EngineFIle exists.")
        modelconfigwrite.append('#model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
        modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
    else:
        anotherenginFilePath = '{2}/Vehicle-parking-management-system/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
        secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
        if os.path.exists(anotherenginFilePath):
            print('----------------------')
            destination= '{0}/models/yoloV8/engine/'.format(get_current_dir_and_goto_parent_dir())
            shutil.copy(anotherenginFilePath, destination)
            if os.path.exists(enginFilePath):
                print('----------------') 
                modelconfigwrite.append('#model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
            else:
                modelconfigwrite.append('model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
        elif os.path.exists(secondenginFilePath):
            print('----------------------')
            destination= '{0}/models/yoloV8/engine/'.format(get_current_dir_and_goto_parent_dir())
            shutil.copy(secondenginFilePath, destination)
            if os.path.exists(enginFilePath):
                print('----------------') 
                modelconfigwrite.append('#model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
            else:
                modelconfigwrite.append('model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
        else:
            modelconfigwrite.append('model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
            modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))

    modelconfigwrite.append('#int8-calib-file=calib.table')
    modelconfigwrite.append('labelfile-path={0}/models/yoloV8/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
    modelconfigwrite.append('batch-size=1')
    modelconfigwrite.append('network-mode=2')
    modelconfigwrite.append('num-detected-classes=80')
    modelconfigwrite.append('interval=0')
    modelconfigwrite.append('gie-unique-id=1')
    modelconfigwrite.append('process-mode=1')
    modelconfigwrite.append('network-type=0')
    modelconfigwrite.append('cluster-mode=2')
    modelconfigwrite.append('maintain-aspect-ratio=1')
    modelconfigwrite.append('symmetric-padding=1')
    modelconfigwrite.append('parse-bbox-func-name=NvDsInferParseYolo')
    modelconfigwrite.append('custom-lib-path={0}/models/yoloV8/nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
    modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')

    modelconfigwrite.append('[class-attrs-all]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=1.0')
    modelconfigwrite.append('topk=300')

    # modelconfigwrite.append('[class-attrs-0]')
    # modelconfigwrite.append('nms-iou-threshold=0.45')
    # modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
    # modelconfigwrite.append('topk=300')

    modelconfigwrite.append('[class-attrs-1]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=0.3')
    modelconfigwrite.append('topk=300')

    modelconfigwrite.append('[class-attrs-2]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=0.3')
    modelconfigwrite.append('topk=300')

    modelconfigwrite.append('[class-attrs-3]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=0.3')
    modelconfigwrite.append('topk=300')

    modelconfigwrite.append('[class-attrs-5]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=0.3')
    modelconfigwrite.append('topk=300')

    modelconfigwrite.append('[class-attrs-6]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=0.3')
    modelconfigwrite.append('topk=300')

    modelconfigwrite.append('[class-attrs-7]')
    modelconfigwrite.append('nms-iou-threshold=0.45')
    modelconfigwrite.append('pre-cluster-threshold=0.3')
    modelconfigwrite.append('topk=300')
    with open(vpms_modelconfigfile, 'w') as f:
        for O_O_O, item in enumerate(modelconfigwrite):
            f.write('%s\n' % item)




def VPMSdumpvoiceannaoumentdataintodatatable(getdata_response):
    # mongo.db.voice_announcement_status.delete_many({"violation_type":"VPMS"})
    if "voice_announcement_status" not in mongo.db.list_collection_names():
        print("Collection 'voice_announcement_status' does not exist-VPMS")
        # raise Exception("Collection 'voice_announcement_status' does not exist")
    else:
        mongo.db.voice_announcement_status.delete_many({"violation_type": { "$in": ["VPMS"] }})
    for i , j in enumerate(getdata_response):

        if len(j['vpms_data']) !=0:
            VPMSAreadata = j['vpms_data']
            insertvoice_dataVPMS = []
            for roiindex , roivalues in enumerate(VPMSAreadata):
                print('------roivalues-------------',roivalues)
                if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
                    if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
                            if roivalues['parking_type']=='no-parking':
                                insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'Unauthorized Parking','violation_type':'VPMS','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                if insertvalue  not in insertvoice_dataVPMS:
                                    insertvoice_dataVPMS.append(insertvalue)
                            elif roivalues['parking_type']=='parking':
                                insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'parked','violation_type':'VPMS','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                                if insertvalue  not in insertvoice_dataVPMS:
                                    insertvoice_dataVPMS.append(insertvalue)

            if len(insertvoice_dataVPMS) !=0:
                mongo.db.voice_announcement_status.insert_many(insertvoice_dataVPMS)
        # if len(j['ppe_data']) !=0:
        #     print('=======ppe_voice_anno999uncement_status data======================')
        #     # print('--------------------',j['ppe_data'][0])
        #     ppealertdata = j['ppe_data'][0]
        #     insertvoice_data = []
        #     ppe= False
        #     crushhelmet = False
        #     if ppealertdata['helmet'] == True and ppealertdata['vest']== True:
        #         ppe= True
        #     elif ppealertdata['helmet'] == True:
        #         ppe= True
        #     elif ppealertdata['vest']== True:
        #         ppe= True
            
        #     if 'crash_helmet' in ppealertdata:
        #         if ppealertdata['crash_helmet']== True:
        #             crushhelmet = True

        #     if 'alert_details' in ppealertdata:
        #         if len(ppealertdata['alert_details']) !=0:
        #             for kkfkkfkjffjjindex, value in enumerate(ppealertdata['alert_details']):
        #                 if 'voice_announcement' in value:
        #                     if value['voice_announcement'] !={} and value['voice_announcement_ip'] is not None:
        #                         if ppe == True and (value['label'] =='helmet' or value['label'] =='vest'):
        #                             insertvalue = {'ip_address':value['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':value['voice_announcement']['audio_files'],'type':None,'violation_type':'PPE_TYPE1','violation_time':None,'valid_time':None,'roi_name':None}
        #                             if insertvalue  not in insertvoice_data:
        #                                 insertvoice_data.append(insertvalue)

        #                         elif crushhelmet == True and value['label'] =='crash_helmet':
        #                             insertvalue = {'ip_address':value['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':value['voice_announcement']['audio_files'],'type':None,'violation_type':'PPE_TYPE2','violation_time':None,'valid_time':None,'roi_name':None}
        #                             if insertvalue  not in insertvoice_data:
        #                                 insertvoice_data.append(insertvalue)
        #         if len(insertvoice_data) !=0:
        #             mongo.db.voice_announcement_status.insert_many(insertvoice_data)

        # if len(j['roi_data']) !=0:
        #     RestrictedAreadata = j['roi_data']
        #     insertvoice_dataRA = []
        #     for roiindex , roivalues in enumerate(RestrictedAreadata):
        #         if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
        #             if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
        #                 if 'analyticstype' in roivalues:
        #                     insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':str(roivalues['analyticstype']),'violation_type':'RA','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
        #                     if insertvalue  not in insertvoice_dataRA:
        #                         insertvoice_dataRA.append(insertvalue)
        #                 else:
        #                     insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':str(roivalues['analyticstype']),'violation_type':'RA','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
        #                     if insertvalue  not in insertvoice_dataRA:
        #                         insertvoice_dataRA.append(insertvalue)

        #     if len(insertvoice_dataRA) !=0:
        #         mongo.db.voice_announcement_status.insert_many(insertvoice_dataRA)
        #     print('=======roi_data======================')
        # if len(j['cr_data']) !=0:
        #     Crowdcountdata = j['cr_data']
        #     insertvoice_dataCRDCNT = []
        #     for roiindex , roivalues in enumerate(Crowdcountdata):
        #         if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
        #             if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
        #                 if roivalues['full_frame']== True:
        #                         insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'fullframe','violation_type':'CRDCNT','violation_time':None,'valid_time':None,'roi_name':'fullframe'}
        #                         if insertvalue  not in insertvoice_dataCRDCNT:
        #                             insertvoice_dataCRDCNT.append(insertvalue)
        #                 else:
        #                     insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'CRDCNT','violation_time':None,'valid_time':None,'roi_name':roivalues['area_name']}
        #                     if insertvalue  not in insertvoice_dataCRDCNT:
        #                         insertvoice_dataCRDCNT.append(insertvalue)

        #     if len(insertvoice_dataCRDCNT) !=0:
        #         mongo.db.voice_announcement_status.insert_many(insertvoice_dataCRDCNT)
        #     print('=======cr_data======================')

        # if len(j['trafficjam_data']) !=0:
        #     trafficjamtdata = j['trafficjam_data']
        #     insertvoice_dataTJM = []
        #     for roiindex , roivalues in enumerate(trafficjamtdata):
        #         if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
        #             if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
        #                 insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':None,'violation_type':'TJM','violation_time':None,'valid_time':None,'roi_name':None}
        #                 if insertvalue  not in insertvoice_dataTJM:
        #                     insertvoice_dataTJM.append(insertvalue)

        #     if len(insertvoice_dataTJM) !=0:
        #         mongo.db.voice_announcement_status.insert_many(insertvoice_dataTJM)
        #     print('=======cr_data======================')
    

@create_vpms_config.route('/start_vpms_application', methods=['GET'])
def create_parking_config_fun():
    status={'message':'Vehicle Parking Management configeration files created successfully','success':True}
    app_set_VPMS_monitoring_started(True)
    parking_enabled_cameras= get_vpms_added_cameras()
    if len(parking_enabled_cameras) >0:
        VPMSdumpvoiceannaoumentdataintodatatable(parking_enabled_cameras)
        status= create_vpms_config_file(parking_enabled_cameras)
        try:
            connection= create_configuration_table()  
            insert_vpms_data_to_table(connection,parking_enabled_cameras)
            app_set_VPMS_monitoring_started(False)
        except Exception as err:
            print('error while uploading data to postgres')
        

    else:
        status= {'message':"No camera is added with the solution or proper solution details are not given to the any cameras",'success':False}
    return status

@create_vpms_config.route('/stop_vpms_application', methods=['GET'])
def stop_vpms_application():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        app_set_VPMS_monitoring_started(True)
        if "voice_announcement_status" not in mongo.db.list_collection_names():
            print("Collection 'voice_announcement_status' does not exist-VPMS")
        else:
            mongo.db.voice_announcement_status.delete_many({"violation_type": { "$in": ["VPMS"] }})
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret