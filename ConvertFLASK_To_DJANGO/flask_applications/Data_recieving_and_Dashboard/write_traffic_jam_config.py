from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_config_funcs import *
from Data_recieving_and_Dashboard.steam_suit_mechanical import * 
import math

create_traffic_jam_config=Blueprint('create_traffic_jam_config', __name__)

def validate_rois_array(arr,keys_array):
    validation_status=False
    for obj in arr:
        if not validation_status:
            validation_status=validate_each_roi(obj,keys_array)
        else :
          return True
    return validation_status

def validate_each_roi(obj,keys):
        validation_status=True
        for key in keys:
            if obj[key] and not ( obj[key]==''or obj[key]== None  ):
                validation_status=True
            else:
                validation_status=False
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
    
     
def get_sample_parking_config_file():
    sample_config_file=os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'sample_parking_config_file.txt') 
    if not os.path.exists(sample_config_file):
        with open(sample_config_file,'w') as file:
             file.write("%s\n"%'''################################################################################
# Copyright (c) 2021-2022 DOCKETRUN TECH PRIVATE LIMITED. All rights reserved.
################################################################################

[application]

[tiled-display]

[sources]
[sink0]
enable=1
#Type - 1=FakeSink 2=EglSink 3=File
type=2
sync=0
source-id=0
gpu-id=0
nvbuf-memory-type=0

[sink2]
enable=0
type=3
#1=mp4 2=mkv
container=1
#1=h264 2=h265 3=mpeg4
## only SW mpeg4 is supported right now.
codec=3
sync=1
bitrate=2000000
output-file=out11.mp4
source-id=0

[osd]

[streammux]

[primary-gie]
enable=1
gpu-id=0
batch-size=4
## 0=FP32, 1=INT8, 2=FP16 mode
bbox-border-color0=0;1;0;1.0
bbox-border-color1=0;1;1;0.7
bbox-border-color2=0;1;0;0.7
bbox-border-color3=0;1;0;0.7
nvbuf-memory-type=0
interval=0
gie-unique-id=1
#config-file = ../../models/config_infer_primary_trafficamnet.txt
#config-file = ../../models/config_infer_primary_tsk_v_0_2.txt
config-file = ../../models/config_infer_primary_yoloV8.txt

[secondary-gie0]
enable = 0
gpu-id = 0
gie-unique-id = 5
operate-on-gie-id = 1
operate-on-class-ids = 0;
batch-size = 1
config-file =../../models/classification_vest.txt

[secondary-gie1]
enable = 0
gpu-id = 0
gie-unique-id = 4
operate-on-gie-id = 1
operate-on-class-ids = 0;
batch-size = 1
config-file =../../models/classification_helmet.txt

[secondary-gie4]
enable = 1
gpu-id = 0
gie-unique-id = 8
operate-on-gie-id = 1
operate-on-class-ids = 1;
batch-size = 1
config-file = ../../models/config_infer_secandary_irrd.txt

[tracker]
enable=1
tracker-width=960
tracker-height=544
ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so
ll-config-file=../../models/config_tracker_NvDCF_perf.yml
gpu-id=0
#enable-batch-process applicable to DCF only

[nvds-analytics]

[application-config]

[ppe-type-1]

[restricted-access]

[crowd-counting]

[traffic-jam]
                        
[steam-suit]
camera-ids = -1;
data-save-interval = 1''')
    return sample_config_file

def create_parking_config_folder():
  parking_config_folder = get_current_dir_and_goto_parent_dir() + '/Traffic_management/configs/'
  parking_video_config_file=os.path.join(parking_config_folder+'/'+"config.txt")
  parking_rois_config_file=os.path.join(parking_config_folder+'/'+"config_TJM.txt")
  if not os.path.exists(parking_config_folder):
        os.makedirs(parking_config_folder)
  else :
       for i,file_name in enumerate(os.listdir(parking_config_folder)):
           if file_name.endswith('.txt'):
            file_path=os.path.join(parking_config_folder+file_name)
            os.remove(file_path)
    
  parking_video_config_file=os.path.join(parking_config_folder+'/'+"config.txt")
  parking_rois_config_file=os.path.join(parking_config_folder+'/'+"config_TJM.txt")
  config_analytics_file=os.path.join(parking_config_folder+'/'+'config_analytics.txt')
      
  return (parking_config_folder,parking_video_config_file,parking_rois_config_file,config_analytics_file)

def write_array_to_file(file,arr):
    for line in arr:
        file.write('%s\n'%line)
    file.write('\n')
    
def create_parking_config_file(parking_enabled_cameras):
    creation_status={'message':"Traffic Jam Config files created succesfully",'success':True}
    valid_camera_list=list()
    parking_config_folder,parking_config_file,parking_roi_config_file,config_analytics_file=create_parking_config_folder()
    sample_config_file=get_sample_parking_config_file()
    lines=[]
    config_tjm_lines=[]
    config_analytics_lines=[]
    roi_required_keys=['roi_name','traffic_jam_percentage','selected_objects','bb_box','roi_id','min_time']
    solution_enabled_camera_count=len(parking_enabled_cameras)
    #writing config_TJM file
    count_tjm=-1
    count_analytics=-1
    for i,camera_data in enumerate(parking_enabled_cameras):
            if validate_rois_array(camera_data['trafficjam_data'],roi_required_keys):
             count_analytics=count_analytics+1
             count_tjm=count_tjm+1
             valid_camera_list.append(camera_data)
             config_analytics_lines.append('[roi-filtering-stream-{0}]'.format(count_analytics))
             config_analytics_lines.append('enable=1' if camera_data['analytics_status']=='true'else 'enable=0')
             config_tjm_lines.append('[TJM{0}]'.format(count_tjm))
             config_tjm_lines.append('enable=1' if camera_data['analytics_status']=='true'else 'enable=0')
             roi_objects=set()
             width_ratio=1920/960
             height_ratio= 1080/544
             for j,roi_data in enumerate(camera_data['trafficjam_data']):
                  if validate_each_roi(roi_data,roi_required_keys):
                    # diff= roi_objects.difference(roi_data['selected_objects'])
                    # if len(diff)>0 :
                    roi_objects= roi_objects.union(roi_data['selected_objects'])
                    resized_roi_box= resize_roi(roi_data['bb_box'],width_ratio,height_ratio)
                    # config_tjm_lines.append( 'jamming-percent = {0}'.format(roi_data['traffic_jam_percentage'])) 
                    # config_tjm_lines.append('verify-time = {0}'.format(roi_data['min_time']))
                    config_analytics_lines.append('roi-TJM-{0}={1}'.format(roi_data['roi_name'], resized_roi_box))
             config_tjm_lines.append('operate-on-label={0}'.format(';'.join(list(roi_objects))+';'))
             config_tjm_lines.append( 'jamming-percent = {0}'.format(camera_data['trafficjam_data'][j]['traffic_jam_percentage']))
             config_tjm_lines.append('verify-time = {0}'.format(camera_data['trafficjam_data'][j]['min_time']))
             config_analytics_lines.append('\n')
             config_tjm_lines.append('\n')
    if len(valid_camera_list)>0:
     with open(parking_roi_config_file, 'w') as file:
        write_array_to_file(file,config_tjm_lines)
        file.close()
                  
      #writing config_analytics_file      
     with open(config_analytics_file, 'w') as file:
        init_line='''[property]\nenable=1\n
config-width=1920
config-height=1080
#osd-mode 0: Dont display any lines, rois and text
#         1: Display only lines, rois and static text i.e. labels
#         2: Display all info from 1 plus information about counts
osd-mode=2\n
#Set OSD font size that has to be displayed
display-font-size=12\n'''
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
                if solution_enabled_camera_count == 1 or solution_enabled_camera_count == 2:
                    rows = 1
                    columns = 2                 
                elif solution_enabled_camera_count== 3 or solution_enabled_camera_count== 4:
                    rows =2 
                    columns =2 
                
                elif solution_enabled_camera_count == 5 or solution_enabled_camera_count == 6:
                    rows =2
                    columns =3
                elif solution_enabled_camera_count == 7 or solution_enabled_camera_count == 8:
                    rows =2 
                    columns =4 
                elif solution_enabled_camera_count == 9 or solution_enabled_camera_count == 10 :
                    rows =2 
                    columns =5

                if solution_enabled_camera_count == 11 or solution_enabled_camera_count == 12:
                    rows = 3
                    columns = 4                 
                elif solution_enabled_camera_count == 13 or solution_enabled_camera_count== 14:
                    rows =3 
                    columns =5                 
                elif solution_enabled_camera_count == 15 or solution_enabled_camera_count== 16:
                    rows =4
                    columns =4
                elif solution_enabled_camera_count == 17 or solution_enabled_camera_count == 18:
                    rows =4
                    columns =5 
                elif solution_enabled_camera_count == 19 or solution_enabled_camera_count == 20 :
                    rows =4 
                    columns =5
                lines.append('[tiled-display]')
                lines.append('enable=1')
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
                        lines.append('drop-frame-interval = 1\n')
                        normal_config_file += 1
                        source_added.append(int(n) + 1)
            
            elif line.strip() == '[sink0]':
                lines.append('[sink0]')
                lines.append('enable=1')
                lines.append('type=2')
                lines.append('sync=0')
                lines.append('source-id=0')
                lines.append('gpu-id=0')
                lines.append('nvbuf-memory-type=0\n')

                lines.append('[sink2]')
                lines.append('enable=0')
                lines.append('type=3')
                lines.append('container=1')
                lines.append('codec=3')
                lines.append('sync=1')
                lines.append('bitrate=2000000')
                lines.append('output-file=out11.mp4')
                lines.append('source-id=0\n')
            
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
                lines.append('nvbuf-memory-type=0\n')
            
            elif line.strip() == '[streammux]':
                lines.append('[streammux]')
                lines.append('gpu-id=0')
                lines.append('live-source=1')
                lines.append('batch-size={0}'.format(len(list(valid_camera_list))))
                lines.append('batched-push-timeout=40000')
                lines.append('width=1920')
                lines.append('height=1080')
                lines.append('enable-padding=0')
                lines.append('nvbuf-memory-type=0\n')
            
            elif line.strip() == '[primary-gie]':
                lines.append('[primary-gie]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('batch-size={0}'.format(len(list(valid_camera_list))))
                lines.append('bbox-border-color0=0;1;0;1.0')
                lines.append('bbox-border-color1=0;1;1;0.7')
                lines.append('bbox-border-color2=0;1;0;0.7')
                lines.append('bbox-border-color3=0;1;0;0.7')
                lines.append('nvbuf-memory-type=0')
                lines.append('interval=0')
                lines.append('gie-unique-id=1')
                lines.append('config-file = ../../models/yoloV8/config_infer_primary_yoloV8.txt\n')

                lines.append('[secondary-gie0]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 6')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('bbox-border-color0 = 0;0;0;0.7')
                lines.append('bbox-border-color1 = 1;0;0;0.7')
                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt\n')

                lines.append('[secondary-gie1]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 4')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('bbox-border-color0 = 0;0;0;0.7')
                lines.append('bbox-border-color1 = 1;0;0;0.7')
                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt\n')

                lines.append('[secondary-gie4]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 8')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 1;')
                lines.append('batch-size = 1')
                lines.append('config-file = ../../models/config_infer_secandary_irrd.txt\n')
            
            elif line.strip() == '[tracker]':
                lines.append('[tracker]')
                lines.append('enable=1')
                lines.append('tracker-width=960')
                lines.append('tracker-height=544')
                lines.append("ll-config-file=../../models/config_tracker_NvDCF_perf.yml")
                lines.append("ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so")
                lines.append('gpu-id=0')
                lines.append('display-tracking-id=1')

            
            elif line.strip() == '[tests]':
                lines.append('[tests]')
                lines.append('file-loop=1\n')
                lines.append('[docketrun-device]')
                lines.append('gui-title = DOCKETRUN VA - 1 - TSK SYSTEM')
                lines.append('data-upload = 1\n')
            
                        
            elif line.strip() == '[nvds-analytics]':
                lines.append('[nvds-analytics]')
                lines.append('enable = 1')
                lines.append('config-file = ./config_analytics.txt\n')
                
            
            elif line.strip() == '[application-config]':
                lines.append('[application-config]')
                lines.append('image-save-path = images/frame')
                lines.append('app-title = DocketEye - Road Safety\n')
            
            elif line.strip() == '[ppe-type-1]':
                lines.append('[ppe-type-1]')
                lines.append('camera-ids = -1;')
                lines.append('data-save-interval = 1\n')
                
            elif line.strip() == '[restricted-access]':
                lines.append('[restricted-access]')
                lines.append('enable = 0')

                lines.append('config-file = ./restricted_access_1.txt')
                lines.append('roi-overlay-enable = 1\n')
                
            elif line.strip() == '[crowd-counting]':
                lines.append('[crowd-counting]')
                lines.append('enable = 0')

                lines.append('config-file = ./crowd.txt')
                lines.append('roi-overlay-enable = 1\n')
            elif line.strip()=='[steam-suit]':
                 lines.append('[steam-suit]')
                 lines.append('camera-ids = -1;')
                 lines.append('data-save-interval = 1')    
            elif line.strip() == '[traffic-jam]':
                lines.append('[traffic-jam]')
                lines.append( 'enable = 1'if len(valid_camera_list)>0 else 'enable = 0')
                lines.append('tjm-config-file=./config_TJM.txt')
                lines.append('data-save-interval=10\n')
            else:
                pass
               
        with open(parking_config_file, 'w') as f:
         for O_O_O, item in enumerate(lines):
            f.write('%s\n' % item)
    else:
        creation_status['message']="Proper AI solution details are not added to any cameras"
        creation_status['success']=False
    return creation_status

    
    

def get_parking_camera_details():
    #,{'trafficjam_data':{'bb_box':{'$exists':True},'roi_name':{'$exists':True}}}
    temp=list([])
    cameras_data=list(mongo.db.ppera_cameras.find({'$and':[{ 'camera_status':True},{'ai_solution.Traffic_Jam':True},{'analytics_status':'true'} ,{'trafficjam_data':{'$exists':True}},{'trafficjam_data.0':{'$exists':True}}]}))
    for i,camera_data in enumerate(cameras_data):
           print('camera index',i,camera_data)
           temp.append(camera_data)
    return temp


    

@create_traffic_jam_config.route('/create_traffic_jam_config', methods=['GET'])
def create_parking_config_fun():
    status={'message':'Traffic Jam configeration files created successfully','success':True}
    parking_enabled_cameras= get_parking_camera_details()
    if len(parking_enabled_cameras) >0:
     status= create_parking_config_file(parking_enabled_cameras)
     
    else:
        status= {'message':"No camera is added with the solution or proper solution details are not given to the any cameras",'success':False}
    return status