from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_config_funcs import *


########## TRAFFIC_JAM_CONFIG_FUNCTIONS#############

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
tracker-width=1920
tracker-height=1080
ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so
ll-config-file=../../models/config_tracker_NvDCF_perf.yml
gpu-id=0
user-meta-pool-size=64
#enable-batch-process applicable to DCF only

[nvds-analytics]

[application-config]

[ppe-type-1]

[restricted-access]

[crowd-counting]

[traffic-jam]
                        
[traffic-counting]                  
                        
[steam-suit]
camera-ids = -1;
data-save-interval = 1''')
    return sample_config_file





def create_parking_config_folder():
  parking_config_folder = get_current_dir_and_goto_parent_dir() + '/docketrun_app/configs/'
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



def create_json_file(filename):
    data = {
        "models": {
                    "trafficcamnet": {
                        "enable": 0,
                        "modelpath": "config_infer_primary_trafficamnet.txt",
                        "class_id": "2"
                    },
                    "objectDetector_Yolo": {
                        "enable": 0,
                        "modelpath": "objectDetector_Yolo/config_infer_primary_yoloV3.txt",
                        "class_id": "0"
                    },
                    "peoplenet": {
                        "enable": 0,
                        "modelpath": "config_infer_primary_peoplenet.txt",
                        "class_id": "2"
                    }
                    ,
                    "yoloV8": {
                        "enable": 1,
                        "modelpath": "yoloV8/config_infer_primary_yolox.txt",
                        "class_id": "0"
                    }
                },
        "secondarymodels":{
                    "helmet": {
                        "enable": 1,
                        "version":5,
                        "modelpath": "config_infer_secandary_helmet_v5.txt",
                        "class_id": "0"
                    }
                    ,
                    "vest": {
                        "enable": 1,
                        "version":5,
                        "modelpath": "config_infer_secandary_vest_v5.txt",
                        "class_id": "0"
                    }
                    ,
                    "steamsuit": {
                        "enable": 1,
                        "version":1,
                        "modelpath": "config_infer_primary_tsk_ss.txt",
                        "class_id": "0"
                    }
                    ,
                    "hydraliclock": {
                        "enable": 1,
                        "version":1,
                        "modelpath": "config_infer_primary_vgg16_lock.txt",
                        "class_id": "0"
                    }
                    ,
                    "esiprimarymodel": {
                        "enable": 1,
                        "version":2,
                        "modelpath": "config_infer_primary_tsk_v_0_2.txt",
                        "class_id": "0"
                    }
                    ,
                    "archjacket": {
                        "enable": 1,
                        "version":5,
                        "modelpath": "config_infer_secandary_arc_jacket_v5.txt",
                        "class_id": "0"
                    }
                    ,
                    "irrd": {
                        "enable": 1,
                        "version":2,
                        "modelpath": "config_infer_secandary_irrd_v2.txt",
                        "class_id": "0"
                    }
                }
        }
    # data = {
    #     "models": {
    #         "trafficcamnet": {
    #             "enable": 0,
    #             "modelpath": "config_infer_primary_trafficamnet.txt",
    #             "class_id": "2"
    #         },
    #         "objectDetector_Yolo": {
    #             "enable": 1,
    #             "modelpath": "objectDetector_Yolo/config_infer_primary_yoloV3.txt",
    #             "class_id": "0"
    #         },
    #         "peoplenet": {
    #             "enable": 0,
    #             "modelpath": "config_infer_primary_peoplenet.txt",
    #             "class_id": "2"
    #         }
    #         ,
    #         "yoloV8": {
    #             "enable": 1,
    #             "modelpath": "yoloV8/config_infer_primary_yolox.txt",
    #             "class_id": "0"
    #     }
    #     }
    # }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    file.close()


def fetch_enabled_data(filename):
    with open(filename, 'r') as file:
        models_data = json.load(file)
    enabled_model = None
    secondanrymodels = []
    for model, config in models_data["models"].items():
        if config["enable"] == 1:
            if "objectDetector_Yolo" in model:
                enabled_model = {model: config, "modeltype": "yolo3"}
            if "trafficcamnet" in model:
                enabled_model = {model: config, "modeltype": "trafficcam"}
            if "peoplenet" in model:
                enabled_model = {model: config, "modeltype": "people"}
            if "yoloV8" in model:
                enabled_model = {model: config, "modeltype": "yolo8"}
            break

    for secondmodel, config in models_data["secondarymodels"].items():
        if config["enable"] == 1:
            if "helmet" in secondmodel:
                secondanrymodels.append({secondmodel: config})
            if "vest" in secondmodel:
                secondanrymodels.append({secondmodel: config})
            # if "peoplenet" in model:
            #     secondanrymodels = {secondmodel: config, "modeltype": "people"}
            # if "yoloV8" in model:
            #     secondanrymodels = {secondmodel: config, "modeltype": "yolo8"}
    file.close()
    return enabled_model,secondanrymodels


def get_model_config_details():
    json_filename = os.path.join(  str(os.getcwd()) + '/' + 'smaple_files', "model_config.json")
    if not file_exists(json_filename):
        create_json_file(json_filename)
        # print(f"JSON file '{json_filename}' created successfully!")
    enabled_data,secondarymodels = fetch_enabled_data(json_filename)
    # print(json.dumps(enabled_data, indent=4))
    # print("secondarymodels==============",secondarymodels)
    return enabled_data ,secondarymodels # json.dumps(enabled_data, indent=4)



def createSTEAMSUITconfig():
    response = []
    main_list = []
    fetch_panel_data = mongo.db.steamsuit_cameras.find_one({})
    if fetch_panel_data is not None:
        if (fetch_panel_data['main_camera']) is not None :
            ip_address =fetch_panel_data['main_camera']['camera_ip']
            cam_name = fetch_panel_data['main_camera']['cameraname']
            rtsp = fetch_panel_data['main_camera']['rtsp_url']
            if rtsp is not None:
                require_panel_data = {'ip_adrs': ip_address, 'cameraname': cam_name,'rtsp_url': rtsp}
                main_list.append(require_panel_data)    
    if len(main_list) != 0:
        response =  main_list    
    return response


def parse_nvidia_smi_output(output):
    overall_index_count =0
    GPU_configuration = []
    for index,line in enumerate(output.split('\n')):
        if 'NVIDIA' in line and 'NVIDIA-SMI' not in line:
            parts = [part.strip() for part in line.split('|') if part.strip()]
            # print("----------------------nvidia---------parts-----",parts)
            GPUDICT ={}
            for _index , value in enumerate(parts):
                value_parts = [part.strip() for part in value.split(' ') if part.strip()]
                value_concatenated = '-'.join(value_parts)
                # print('=====================value',value_concatenated)
                if _index==0:
                    GPUDICT['gpu_index']=overall_index_count
                    GPUDICT['gpu_name'] = value_concatenated
                elif _index==1:
                    GPUDICT['gpu_display'] = value_concatenated
                elif _index==2:
                    GPUDICT['gpu_volatile'] = value_concatenated
            GPU_configuration.append(GPUDICT)
            overall_index_count+=1
    # print("-----------------GPU_configuration=============================",GPU_configuration)
    return {"gpu_details":GPU_configuration}

def execute_nvidia_smi(Gpuindex):
    returnValue = False
    # print("------------------Gpuindex------------------",Gpuindex)
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            display_info = parse_nvidia_smi_output(result.stdout)
            # print("------------------------------display info---------------",display_info)
            if display_info is not None:
                IMD= display_info['gpu_details']
                # print("-------------------------IMD----",IMD)
                for i , j in enumerate(IMD):
                    # print('-----------------------',j)
                    if Gpuindex ==j['gpu_index']:
                        # print("gpu_display----------------",j['gpu_display'])
                        if 'On' in j['gpu_display']:
                            returnValue= True
                        else:
                            returnValue= False
        else:
            print("Error executing nvidia-smi:")
            print(result.stderr)
    except FileNotFoundError:
        print("nvidia-smi command not found. Please ensure NVIDIA drivers are installed.")
    return returnValue


def GPUSsplit_list(lst, m):
    n = len(lst)
    k, remainder = divmod(n, m)
    return [lst[i * k + min(i, remainder):(i + 1) * k + min(i + 1, remainder)] for i in range(m)]


def get_layout(total_streams):
    if total_streams in range(1, 3):  # 1 or 2
        rows, columns = 1, 2
    elif total_streams in range(3, 5):  # 3 or 4
        rows, columns = 2, 2
    elif total_streams in range(5, 7):  # 5 or 6
        rows, columns = 2, 3
    elif total_streams in range(7, 9):  # 7 or 8
        rows, columns = 2, 4
    elif total_streams in range(9, 11):  # 9 or 10
        rows, columns = 2, 5
    elif total_streams in range(11, 13):  # 11 or 12
        rows, columns = 3, 4
    elif total_streams in range(13, 15):  # 13 or 14
        rows, columns = 3, 5
    elif total_streams in range(15, 17):  # 15 or 16
        rows, columns = 4, 4
    elif total_streams in range(17, 19):  # 17 or 18
        rows, columns = 4, 5
    elif total_streams in range(19, 21):  # 19 or 20
        rows, columns = 4, 5
    elif total_streams in range(21, 25):  # 21 to 24
        rows, columns = 4, 6
    elif total_streams in range(25, 31):  # 25 to 30
        rows, columns = 5, 6
    elif total_streams in range(31, 37):  # 31 to 36
        rows, columns = 6, 6
    elif total_streams in range(37, 43):  # 37 to 42
        rows, columns = 6, 7
    elif total_streams in range(43, 50):  # 43 to 49
        rows, columns = 7, 7
    elif total_streams in range(50, 61):  # 50 to 60
        rows, columns = 7, 8
    elif total_streams in range(61, 73):  # 61 to 72
        rows, columns = 8, 9
    elif total_streams in range(73, 85):  # 73 to 84
        rows, columns = 9, 9
    elif total_streams in range(85, 97):  # 85 to 96
        rows, columns = 10, 10
    elif total_streams in range(97, 111):  # 97 to 110
        rows, columns = 10, 11
    elif total_streams in range(111, 127):  # 111 to 126
        rows, columns = 11, 12
    elif total_streams in range(127, 144):  # 127 to 143
        rows, columns = 12, 12
    elif total_streams in range(144, 161):  # 144 to 160
        rows, columns = 12, 13
    elif total_streams in range(161, 181):  # 161 to 180
        rows, columns = 13, 14
    elif total_streams in range(181, 202):  # 181 to 201
        rows, columns = 14, 15
    elif total_streams in range(202, 225):  # 202 to 224
        rows, columns = 15, 15
    elif total_streams in range(225, 250):  # 225 to 249
        rows, columns = 15, 16
    elif total_streams in range(250, 277):  # 250 to 276
        rows, columns = 16, 17
    elif total_streams in range(277, 300):  # 277 to 300
        rows, columns = 17, 18
    else:
        rows, columns = 1, 2  

    return rows, columns


def WRITEMULTICONFIG(response):
    valid_camera_list=[]
    roi_required_keys=['roi_name','traffic_jam_percentage','selected_objects','bb_box','roi_id','min_time']
    TitledDisplayEnable = True
    defaultsecondmodels = True
    Hemetdetails = {}
    Vestdetails = {}
    steamsuitaddedstatus = False
    GPUSINDEX = 0  
    allWrittenSourceCAmIds =[]
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
    classId = '0'
    print("Genral_configurations===",Genral_configurations)
    batch_pushouttime = 40000
    drop_frame_interval=1
    ticket_reset_time =10
    gridview_true = True
    numberofsources_= 4
    rtsp_reconnect_interval = 3
    displayfontsize = 12
    display_tracker =True
    if ('drop_frame_interval' in Genral_configurations and Genral_configurations['drop_frame_interval'] is not None) and ('camera_fps' in Genral_configurations and  Genral_configurations['camera_fps'] is not None) :
        camera_fps = Genral_configurations['camera_fps']
        drop_frame_interval = Genral_configurations['drop_frame_interval']
        Newpushouttime = math.ceil(int(camera_fps)/int(drop_frame_interval))
        batch_pushouttime= math.ceil(1000000/Newpushouttime)
    
    if ('rtsp_reconnect_interval' in Genral_configurations and Genral_configurations['rtsp_reconnect_interval'] is not None):
        rtsp_reconnect_interval = Genral_configurations['rtsp_reconnect_interval'] 
    

    if ('grid_view' in Genral_configurations and Genral_configurations['grid_view'] is not None):
        gridview_true = Genral_configurations['grid_view'] 
    if ('grid_size' in Genral_configurations and Genral_configurations['grid_size'] is not None):
        numberofsources_ = int(Genral_configurations['grid_size'])


    if ('ticket_reset_time' in Genral_configurations and Genral_configurations['ticket_reset_time'] is not None):
        ticket_reset_time = int(Genral_configurations['ticket_reset_time'])
    
    if 'display_font_size' in Genral_configurations :
        displayfontsize = Genral_configurations['display_font_size']

    if 'display_tracker' in Genral_configurations :
        display_tracker = Genral_configurations['display_tracker']
    
    print("number of sources-- fetched----222 --------------0000000000000000000000000",len(response))
    Total_source_count = len(response)
    GPU_data = mongo.db.gpu_configurations.find_one({})
    # new_response = split_list(response,numberofsources_)
    camera_id = 1 
    NewcameraID = 1
    modelconfigfile = '/objectDetector_Yolo/config_infer_primary_yoloV3_1.txt'
    modelconfigwrite = []
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'phase_one_sample_config.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/docketrun_app'+'/configs'
    yolo_config_path = get_current_dir_and_goto_parent_dir() + '/models/objectDetector_Yolo'
    yolo8_config_path = get_current_dir_and_goto_parent_dir() + '/models/yoloV8'
    traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)
    if not os.path.exists(yolo_config_path):
        os.makedirs(yolo_config_path)
    if not os.path.exists(traffic_config_path):
        os.makedirs(traffic_config_path)
    if not os.path.exists(yolo8_config_path):
        os.makedirs(yolo8_config_path)           
    remove_text_files(deepstream_config_path)  
    modelthreshold = getthreshholdmodelconfig_details()
    person_threshold = '0.7'
    helmet_threshold = '0.5'
    vest_threshold = '0.5'
    CrashHelment_threshold = '0.3'
    Bicycle_threshold= '0.3'
    Motorbike_threshold ='0.3'
    car_threshold = '0.3'
    bus_threshold = '0.3'
    truck_threshold = '0.3'
    if modelthreshold is not None:
        if len(modelthreshold['threshold']) !=0:
            for new,classname in enumerate(modelthreshold['threshold']):
                if classname['class']=='person':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            person_threshold = int(classname['value'])/100
                            if person_threshold==1:
                                person_threshold ='0.9'
                        else:
                            person_threshold = '0.1'           
                elif  classname['class']=='helmet':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            helmet_threshold =  int(classname['value'])/100
                            if helmet_threshold==1:
                                helmet_threshold ='0.9'
                        else:
                            helmet_threshold ='0.1' 
                elif  classname['class']=='vest':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            vest_threshold = int(classname['value'])/100
                            if vest_threshold==1:
                                vest_threshold ='0.9'
                        else:
                            vest_threshold ='0.1'
                elif  classname['class']=='crash_helmet':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            CrashHelment_threshold = int(classname['value'])/100
                            if CrashHelment_threshold==1:
                                CrashHelment_threshold ='0.9'
                        else:
                            CrashHelment_threshold ='0.1'
                elif  classname['class']=='bicycle':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            Bicycle_threshold = int(classname['value'])/100
                            if Bicycle_threshold==1:
                                Bicycle_threshold ='0.9'
                        else:
                            Bicycle_threshold ='0.1'
                elif  classname['class']=='motorbike':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            Motorbike_threshold = int(classname['value'])/100
                            if Motorbike_threshold==1:
                                Motorbike_threshold ='0.9'
                        else:
                            Motorbike_threshold ='0.1'
                elif  classname['class']=='car':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            car_threshold = int(classname['value'])/100
                            if car_threshold==1:
                                car_threshold ='0.9'
                        else:
                            car_threshold ='0.1'

                elif  classname['class']=='bus':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            bus_threshold = int(classname['value'])/100
                            if bus_threshold==1:
                                bus_threshold ='0.9'
                        else:
                            bus_threshold ='0.1'
                elif  classname['class']=='truck':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            truck_threshold = int(classname['value'])/100
                            if truck_threshold==1:
                                truck_threshold ='0.9'
                        else:
                            truck_threshold ='0.1'
    model_config_details,secondarymodelconfigdetails = get_model_config_details()
    # print("second model config===",secondarymodelconfigdetails)
    # print("====model_config_details====",model_config_details)
    if model_config_details is not None:
        if model_config_details['modeltype'] == 'yolo3':
            classId = model_config_details['objectDetector_Yolo']['class_id']
            modelconfigfile = model_config_details['objectDetector_Yolo']['modelpath']
        elif model_config_details['modeltype'] == 'yolo8':
            classId = model_config_details['yoloV8']['class_id']
            modelconfigfile = model_config_details['yoloV8']['modelpath']
        elif model_config_details['modeltype'] == 'trafficcam':
            classId = model_config_details['trafficcamnet']['class_id']
            modelconfigfile = model_config_details['trafficcamnet']['modelpath']
        elif model_config_details['modeltype'] == 'people':
            classId = model_config_details['peoplenet']['class_id']
            modelconfigfile = model_config_details['peoplenet']['modelpath']
    if type(secondarymodelconfigdetails)== list  and len(secondarymodelconfigdetails)!=0 :
        defaultsecondmodels = False
        for indexmo, Modedetails in enumerate(secondarymodelconfigdetails):
            print("indexmo===",indexmo,Modedetails)
            for MAINKey , Values  in Modedetails.items():
                if "helmet" in MAINKey:
                    Hemetdetails= Modedetails
                if "vest" in MAINKey:
                    Vestdetails= Modedetails
    steamsuitcameradetails = createSTEAMSUITconfig()
    steamsuitcameradetails =[]
    if  len(response)!=0 and  len(steamsuitcameradetails) !=0:#len(response)!=0 and  len(steamsuitcameradetails)
        if GPU_data is not None:
            directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app', 'configs')
            
            txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
            print('-----txt_files---------------1.0.1------',txt_files)

            # Check if there are any .txt files in the directory
            if txt_files:
                try:
                    # Remove each .txt file individually
                    for txt_file in txt_files:
                        os.remove(os.path.join(directory_path, txt_file))
                    print("Text files deleted successfully.---1.9.0----")
                except Exception as e:
                    print(f"Error deleting text files:---1.9.0---- {e}")
            else:
                print("No text files found in the directory.---1.9.0----")
            NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
            # print("=====NEwcount====",NEwcount)
            new_response=GPUSsplit_list(response,GPU_data['system_gpus'])
                
            # print("----create___STEAMSUIT_______config",steamsuitcameradetails)
            for config_index, writingresponse in enumerate(new_response):  
                if GPU_data['system_gpus']==1 :
                    GPUSINDEX = GPUSINDEX
                elif config_index ==0  :
                    GPUSINDEX = config_index
                elif camera_id >= NEwcount:
                    GPUSINDEX= GPUSINDEX+1 
                else:   
                    GPUSINDEX= GPUSINDEX
                # GPUSINDEX =1
                config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
                crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
                config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
                hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
                PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))
                parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
                lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
                config_tjm_lines=[]
                # roi_objects=set()
                roi_enable_cam_ids = []
                ppe_enable_cam_ids = []
                traffic_count_enabledcameraids=[]
                cr_enable_cam_ids = []
                tc_label_names = []
                normal_config_file = 0
                final_roi_existed_cam_ids = []
                final_truck_cam_ids = []
                hooter_line = []
                crowd_line = []  
                PPELINE = [] 
                onlyCrashHelmet =[]     
                PPEFINALCAMERAIDS =[]
                traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
                steamsuit_cameraid =[]
                # print("length == === ", len(writingresponse))
                Steamsuitdata = steamsuitcameradetails
                # print("Steamsuitdata====",Steamsuitdata)
                lines.append("[roi-filtering-stream-0]")
                lines.append("enable=0")
                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                lines.append("inverse-roi=0")
                lines.append("class-id= 0;\n")
                
                crowd_line.append("[crdcnt0]")
                crowd_line.append("enable=0")
                crowd_line.append("process-on-full-frame=1")
                crowd_line.append("operate-on-label=person;")
                crowd_line.append("max-count=1;")
                crowd_line.append("min-count=0;")
                crowd_line.append("data-save-time-in-sec=3\n")
                hooter_line.append("[RA0]")
                hooter_line.append("enable = 0")
                hooter_line.append("operate-on-label = person;")
                hooter_line.append("hooter-enable = 0")
                hooter_line.append("hooter-ip = none")
                hooter_line.append('hooter-type = 0;')
                hooter_line.append("hooter-stop-buffer-time = 3")
                hooter_line.append("data-save-time-in-sec = 3\n")
                for index, x in enumerate(writingresponse):
                    x['cameraid'] = NewcameraID
                    if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
                        if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("***************111111************")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("TC-CR_PPE===2")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:    
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)

                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("TC-CR_RA===3")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("cr-ra_PPE===5")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)

                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("RA-TC_PPE===handled")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("cr-ra===6")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                                        
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("ra_TC===7")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID) 
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("ra_PPE===8")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)   
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("CR_TC===9")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("PPE_TC===10")
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)   
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)    
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("PPE_CR===11")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)  
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("CR===12")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                                        
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("RA===13")    
                            roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("TC===14") 
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("PPE===14") 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        
                        width_ratio=960/960
                        height_ratio= 544/544
                        if 'trafficjam_data' in x :
                            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----1-------')
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
                                                # print('str(FinalTime)-------type---4------------',type(FinalTime))
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
                                                # print('str(FinalTime)-------type---3------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'

                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                else:
                                    print()
                            
                        # print("INDEX------------------------------------------",index)    
                        if '[crdcnt{}]'.format(index) not in crowd_line:
                            # print("-----")
                            crowd_line.append('[crdcnt{0}]'.format(index))
                            crowd_line.append("enable=0")
                            crowd_line.append("process-on-full-frame=1")
                            crowd_line.append("operate-on-label=person;")
                            crowd_line.append("max-count=1;")
                            crowd_line.append("min-count=0;")
                            crowd_line.append("data-save-time-in-sec=3\n")
                            
                        if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                            lines.append('[roi-filtering-stream-{0}]'.format(index))
                            if 'trafficjam_data' in x :
                                if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----00-0-------')
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
                                                # print('str(FinalTime)-------type---1------------',type(FinalTime))
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

                                                # print('str(FinalTime)-------type---2------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                else:
                                    lines.append("enable=0")
                                    lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            else:
                                lines.append("enable=0")
                                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            lines.append("inverse-roi=0")
                            # lines.append("class-id= 0;\n")
                            
                        if '[RA{}]'.format(index) not in hooter_line:
                            # print("-----")
                            hooter_line.append('[RA{0}]'.format(index))
                            hooter_line.append("enable = 0")
                            hooter_line.append("operate-on-label = person;")
                            hooter_line.append("hooter-enable = 0")
                            hooter_line.append("hooter-ip = none")
                            hooter_line.append('hooter-type = 0;')
                            hooter_line.append('hooter-shoutdown-time = 10')
                            hooter_line.append("hooter-stop-buffer-time = 3")
                            hooter_line.append("data-save-time-in-sec = 3\n")

                        if '[PPE{}]'.format(index) not in PPELINE:
                            # print("-----")
                            PPELINE.append('[PPE{0}]'.format(index))
                            PPELINE.append("enable = 0")
                            PPELINE.append("hooter-enable = 0")
                            PPELINE.append("hooter-ip = none")
                            PPELINE.append('hooter-type = 0;')
                            PPELINE.append('hooter-shoutdown-time = 10')
                            PPELINE.append("hooter-stop-buffer-time = 3")
                            PPELINE.append('analytics-details =[{"analytics_type":0, "operate_on": "null;"},{"analytics_type":1, "operate_on": "null;"}]')
                            PPELINE.append("data-save-time-in-sec = 3\n")
                        
                        NewcameraID+=1
                total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids))
                # print("roi_enable cam ids =====", roi_enable_cam_ids)
                # print("ppeppe_333enable_cam_ids",ppe_enable_cam_ids)
                # print("=================total_stream_for_stremux_union===============",total_stream_for_stremux_union)
                with open(config_analytics_file, 'w') as f:
                    for item in lines:
                        f.write('%s\n' % item)

                with open(hooter_config_file_path, 'w') as hooter_file:
                    for jim in hooter_line:
                        hooter_file.write('%s\n' % jim)

                with open(PPE_config_file_path, 'w') as PPE_file:
                    for jim in PPELINE:
                        PPE_file.write('%s\n' % jim)

                with open(crowd_config_file, 'w') as crowd_file:
                    for O_O_O, item in enumerate(crowd_line):
                        crowd_file.write('%s\n' % item)
                # print('----------------------len---------',len(config_tjm_lines))
                with open(parking_roi_config_file, 'w') as file:
                    write_array_to_file(file,config_tjm_lines)
                    file.close()
                lines = []
                final_both_roi_cam_ids = []
                with open(sample_config_file) as file:
                    for write_config, line in enumerate(file):
                        if line.strip() == '[application]':
                            lines.append('[application]')
                            lines.append('enable-perf-measurement=1')
                            lines.append('perf-measurement-interval-sec=1')

                        elif line.strip() == '[tiled-display]':
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                            total_stream_for_stremux_union = finaL_RA_PPE
                            num = math.sqrt(int(len(finaL_RA_PPE)))
                            rows,columns= get_layout(len(total_stream_for_stremux_union))
                            # print("num----",num )
                            # print("num----",num )
                            # if 1 < num < 1.4:
                            #     rows = 1
                            #     columns = 2
                            # elif num == 1:
                            #     rows = 1
                            #     columns = 2
                            # else:
                            #     if 1 > num >= 1.4:
                            #         if len(finaL_RA_PPE)>3:
                            #             rows = 2
                            #             columns = 2
                            #         else:
                            #             rows = 1
                            #             columns = 2
                                        
                            #     else:
                            #         rows = int(round(num))
                            #         columns = 2
                                # print("row====s ",rows)
                                # print("columns====s ",columns)

                            lines.append('[tiled-display]')
                            if execute_nvidia_smi(GPUSINDEX):
                                lines.append('enable=1')
                            elif TitledDisplayEnable:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('rows={0}'.format(str(rows)))
                            lines.append('columns={0}'.format(str(columns)))
                            lines.append('width=960')
                            lines.append('height=544')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('nvbuf-memory-type=0')

                        elif line.strip() == '[sources]':    
                            # print("newlength===", len(writingresponse))
                            steamsuitaddedstatus = False
                            for n, x in enumerate(writingresponse):
                                cam_id = '{0}'.format(int(n))
                                # print("-------------------------------------ROI CAMERA IDS ---------2---------",roi_enable_cam_ids)
                                # print("-------------------------------------PPE CAMERA IDS ---------2---------",ppe_enable_cam_ids)
                                # print("-------------------------------------CRDCNT CAMERA IDS -----------2-------",cr_enable_cam_ids)
                                # print("-------------------------------------camera_id in roi_enable_cam_ids -------2-----------",camera_id,camera_id in roi_enable_cam_ids)
                                # print("-------------------------------------camera_id in ppe_enable_cam_ids --------2----------",camera_id,camera_id in ppe_enable_cam_ids)
                                # print("-------------------------------------camera_id in cr_enable_cam_ids ---------2---------",camera_id,camera_id in cr_enable_cam_ids)
                                # print("PPEFINALCAMERAIDS==========camera1.0=",PPEFINALCAMERAIDS)
                                if camera_id in roi_enable_cam_ids:
                                    roi_enable_cam_ids_exist = 1
                                if camera_id in ppe_enable_cam_ids:
                                    ppe_enable_cam_ids_exist = 1
                                if camera_id in cr_enable_cam_ids:
                                    newcrowdcount = 1
                                # print("newcrowdcountnewcrowdcountnewcrowdcount===newcrowdcount> 0 ",newcrowdcount)
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')

                                # print("Steamsui44---4tda----ta===55544=",Steamsuitdata)
                                if len(Steamsuitdata) !=0 and steamsuitaddedstatus == False:
                                    uri = Steamsuitdata[0]['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  55544 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(Steamsuitdata[0]['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1    
                                    steamsuit_cameraid.append(camera_id)                        
                                    camera_id += 1
                                    steamsuitaddedstatus = True
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    # print("normal_config_file += 1 ------------------------",normal_config_file  )
                                if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  1222222222222222222222222222222222222222222 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0        
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ):
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) += 333 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec=2")
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                    
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  ^^^^^^^^^^^^^^^^^^^122334 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif roi_enable_cam_ids_exist > 0:
                                    print("normal_config_file += 5555522 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif ppe_enable_cam_ids_exist > 0:
                                    print("normal_config_file += 666666666666666 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  #####################11122 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                
                                elif len(traffic_count_enabledcameraids)>0:
                                    print("normal_config_file += 777777777777777777 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdtraffic_count_enabledcameraidsfkajsdkfkasdjk=============", traffic_count_enabledcameraids)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                    
                                elif newcrowdcount >0:
                                    print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                            
                        elif line.strip() == '[sink0]':
                            lines.append('[sink0]')
                            lines.append('enable=1')
                            # if execute_nvidia_smi(GPUSINDEX):
                            #     lines.append('type=2')
                            # if TitledDisplayEnable:

                            #     lines.append('type=2')
                            # elif TitledDisplayEnable:

                            #     lines.append('type=2')

                            if gridview_true is True:
                                lines.append('type=2')
                            else:
                                lines.append('type=1')
                            #lines.append('type=2')
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
                            lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            if batch_pushouttime == 40000:
                                lines.append('batched-push-timeout=40000')
                            else:
                                lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            lines.append('width=1920')
                            lines.append('height=1080')
                            lines.append('enable-padding=0')
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[primary-gie]':
                            lines.append('[primary-gie]')
                            lines.append('enable=1')
                            lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            # lines.append('bbox-border-color0=0;1;0;1.0')
                            # lines.append('bbox-border-color1=0;1;1;0.7')
                            # lines.append('bbox-border-color2=0;1;0;0.7')
                            # lines.append('bbox-border-color3=0;1;0;0.7')
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
                            modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                            lines.append('model-engine-file=../../models/yoloV8/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                            lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                        elif line.strip() == '[primary-gie-ss]':
                            lines.append('[primary-gie-ss]')
                            if len(steamsuit_cameraid) !=0:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('batch-size={0}'.format(str(1)))
                            lines.append('bbox-border-color0=0;1;1;0.7')
                            lines.append('bbox-border-color1=0;1;1;0.7')
                            lines.append('bbox-border-color2=0;1;1;0.7')
                            lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            lines.append('config-file = ../../models/config_infer_primary_tsk_ss.txt')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            
                            
                        elif line.strip() == '[secondary-gie0]':
                            lines.append('[secondary-gie0]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 6')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('gie-unique-id = 4')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 0;0;0;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                                secondaryconfig_file = []                                
                                secondaryconfig_file.append('[property]')
                                secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(HelmetEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                # secondaryconfig_file.append('tlt-encoded-model=./helmet_detector_v5/resnet18_helmet_detector_v5.etlt')
                                # secondaryconfig_file.append('labelfile-path=./helmet_detector_v5/labels.txt')
                                # secondaryconfig_file.append('model-engine-file=./helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                secondaryconfig_file.append('infer-dims=3;320;320')
                                secondaryconfig_file.append('uff-input-blob-name=input_1')
                                secondaryconfig_file.append('batch-size=1')
                                secondaryconfig_file.append('process-mode=2')
                                secondaryconfig_file.append('model-color-format=0')
                                secondaryconfig_file.append('network-mode=2')
                                secondaryconfig_file.append('num-detected-classes=2')
                                secondaryconfig_file.append('interval=0')
                                secondaryconfig_file.append('gie-unique-id=2')
                                secondaryconfig_file.append('operate-on-gie-id=1')
                                secondaryconfig_file.append('operate-on-class-ids=0;')
                                secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_file.append('network-type=0')
                                secondaryconfig_file.append('uff-input-order=0\n')
                                secondaryconfig_file.append('[class-attrs-0]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20\n')
                                secondaryconfig_file.append('[class-attrs-1]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20')
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_file):
                                        f.write('%s\n' % item)
                            else:
                                if Hemetdetails is not None:
                                    HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                                    Hemeltversion= Hemetdetails['helmet']['version']
                                    lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                    lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                                    secondaryconfig_file = []                                    
                                    secondaryconfig_file.append('[property]')
                                    secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                    HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(HelmetEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    # secondaryconfig_file.append('tlt-encoded-model=./helmet_detector_v{0}/resnet18_helmet_detector_v5.etlt'.format(Hemeltversion))
                                    # secondaryconfig_file.append('labelfile-path=./helmet_detector_v{0}/labels.txt'.format(Hemeltversion))
                                    # secondaryconfig_file.append('model-engine-file=./helmet_detector_v{0}/resnet18_helmet_detector_v5.etlt_b1_gpu{1}_fp16.engine'.format(Hemeltversion,GPUSINDEX))
                                    secondaryconfig_file.append('infer-dims=3;320;320')
                                    secondaryconfig_file.append('uff-input-blob-name=input_1')
                                    secondaryconfig_file.append('batch-size=1')
                                    secondaryconfig_file.append('process-mode=2')
                                    secondaryconfig_file.append('model-color-format=0')
                                    secondaryconfig_file.append('network-mode=2')
                                    secondaryconfig_file.append('num-detected-classes=2')
                                    secondaryconfig_file.append('interval=0')
                                    secondaryconfig_file.append('gie-unique-id=2')
                                    secondaryconfig_file.append('operate-on-gie-id=1')
                                    secondaryconfig_file.append('operate-on-class-ids=0;')
                                    secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_file.append('network-type=0')
                                    secondaryconfig_file.append('uff-input-order=0\n')
                                    secondaryconfig_file.append('[class-attrs-0]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20\n')
                                    secondaryconfig_file.append('[class-attrs-1]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_file):
                                            f.write('%s\n' % item)
                        elif line.strip() == '[secondary-gie1]':
                            lines.append('[secondary-gie1]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 7')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                            # lines.append('gie-unique-id = 5')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                                secondaryconfig_filevest = []
                                secondaryconfig_filevest.append('[property]')
                                secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_filevest.append('tlt-model-key=tlt_encode')

                                VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(VestEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                                # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                                # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('infer-dims=3;320;320')
                                secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                secondaryconfig_filevest.append('batch-size=1')
                                secondaryconfig_filevest.append('process-mode=2')
                                secondaryconfig_filevest.append('model-color-format=0')
                                secondaryconfig_filevest.append('network-mode=2')
                                secondaryconfig_filevest.append('num-detected-classes=3')
                                secondaryconfig_filevest.append('interval=0')
                                secondaryconfig_filevest.append('gie-unique-id=2')
                                secondaryconfig_filevest.append('operate-on-gie-id=1')
                                secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_filevest.append('network-type=0')
                                secondaryconfig_filevest.append('uff-input-order=0\n')
                                secondaryconfig_filevest.append('[class-attrs-0]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20\n')
                                secondaryconfig_filevest.append('[class-attrs-1]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')                                
                                secondaryconfig_filevest.append('[class-attrs-2]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')      
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_filevest):
                                        f.write('%s\n' % item)

                            else:
                                if Vestdetails is not None:
                                    Vestconfigfile = Vestdetails['vest']['modelpath']
                                    Vestversion= Vestdetails['vest']['version']
                                    lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                    lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                                    secondaryconfig_filevest = []
                                    secondaryconfig_filevest.append('[property]')
                                    secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                    VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(VestEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))



                                    # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v{0}/resnet18_vest_detector_v{1}.etlt'.format(Vestversion,Vestversion))
                                    # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v{0}/labels.txt'.format(Vestversion))
                                    # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v{0}/resnet18_vest_detector_v{1}.etlt_b1_gpu{2}_fp16.engine'.format(Vestversion,Vestversion,GPUSINDEX))
                                    secondaryconfig_filevest.append('infer-dims=3;320;320')
                                    secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                    secondaryconfig_filevest.append('batch-size=1')
                                    secondaryconfig_filevest.append('process-mode=2')
                                    secondaryconfig_filevest.append('model-color-format=0')
                                    secondaryconfig_filevest.append('network-mode=2')
                                    secondaryconfig_filevest.append('num-detected-classes=3')
                                    secondaryconfig_filevest.append('interval=0')
                                    secondaryconfig_filevest.append('gie-unique-id=2')
                                    secondaryconfig_filevest.append('operate-on-gie-id=1')
                                    secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                    secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_filevest.append('network-type=0')
                                    secondaryconfig_filevest.append('uff-input-order=0\n')
                                    secondaryconfig_filevest.append('[class-attrs-0]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20\n')
                                    secondaryconfig_filevest.append('[class-attrs-1]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')                                    
                                    secondaryconfig_filevest.append('[class-attrs-2]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_filevest):
                                            f.write('%s\n' % item)

                        elif line.strip() == '[secondary-gie2]':
                            lines.append('[secondary-gie2]')
                            if len(onlyCrashHelmet) !=0:
                                lines.append('enable = 1')
                            else:
                                lines.append('enable = 0')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 8')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                if os.path.exists(anotherenginFilePath):
                                    print('----------------------')
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(anotherenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                elif os.path.exists(secondenginFilePath):
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(secondenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                else:
                                    lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")



                            if 1:#defaultsecondmodels == True :
                                # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/crash_helmet_nano_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                                ScondaryCrushhelmet = []
                                ScondaryCrushhelmet.append('[property]')
                                ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                                ScondaryCrushhelmet.append('model-color-format=0')
                                # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                                CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(CrushHelmet):
                                    # print("yolov3 EngineFIle exists.")
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    # print("yolov3 EngineFIle does not exist.")
                                    # ScondaryCrushhelmet.append('tlt-encoded-model={0}/models/yoloV8_crash_helmet/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    # ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    # #yoloV8_crash_helmet/engine/model_b4_gpu0_fp16.engine
                                    # ScondaryCrushhelmet.append('model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                                # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                                # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('batch-size=1')
                                ScondaryCrushhelmet.append('network-mode=2')
                                ScondaryCrushhelmet.append('num-detected-classes=2')
                                ScondaryCrushhelmet.append('interval=0')
                                ScondaryCrushhelmet.append('gie-unique-id=1')
                                ScondaryCrushhelmet.append('process-mode=2')
                                ScondaryCrushhelmet.append('network-type=0')
                                ScondaryCrushhelmet.append('cluster-mode=2')
                                ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                                ScondaryCrushhelmet.append('operate-on-gie-id=1')
                                ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                                ScondaryCrushhelmet.append('symmetric-padding=1')
                                ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                                ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                                ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                                ScondaryCrushhelmet.append('[class-attrs-0]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300\n')

                                ScondaryCrushhelmet.append('[class-attrs-1]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300')     
                                with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                                    for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                        f.write('%s\n' % item)
                        elif line.strip() == '[tracker]':
                            lines.append('[tracker]')
                            lines.append('enable=1')
                            lines.append('tracker-width=960')
                            lines.append('tracker-height=554')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('#enable-batch-process=0')
                            if display_tracker :
                                lines.append('display-tracking-id=1')
                            else:
                                lines.append('display-tracking-id=0')
                            lines.append('user-meta-pool-size=64')
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
                        elif line.strip()== '[application-config]':
                            lines.append('[application-config]')     
                        elif line.strip() == '[restricted-access]':
                            lines.append('[restricted-access]')
                            final_index = 0
                            final_roi_empty_ls = []
                            check_camera_id_for_RA = []
                            for Cherry, x in enumerate(writingresponse):
                                string2 = '-1;'
                                if len(x['roi_data']) != 0:
                                    for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                        label_name = roi_value['label_name']
                                        if ('person' in label_name and 'truck' in label_name):
                                            final_both_roi_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'truck' in label_name:
                                            final_truck_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' in label_name:
                                            final_roi_existed_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' not in label_name and 'truck' not in label_name:
                                            pass
                                        else:
                                            pass
                                final_index += 1
                            string_test = '-1;'
                            if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                                check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                            final_roi_existed_cam_ids = roi_enable_cam_ids
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            
                            # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",len(roi_enable_cam_ids))
                            # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",roi_enable_cam_ids)
                            if len(roi_enable_cam_ids)== 0:
                                lines.append('enable = 0')

                            else:
                                lines.append('enable = 1')
                            lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                            lines.append('roi-overlay-enable = 1')
                            lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))

                        elif line.strip() == '[ppe-type-1]':
                            lines.append('[PPE]')
                            # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                            empty_ppe_ls = []
                            for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                                text = str(n) + ';'
                                empty_ppe_ls.append(text)
                            string2 = ''
                            if len(empty_ppe_ls) == 0:
                                # string2 = '-1;'
                                # lines.append('camera-ids = {0}'.format(string2))
                                lines.append('enable = 0')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            else:
                                # string2 = ''
                                # lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                                lines.append('enable = 1')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            # lines.append('[ppe-type-1]')
                            # # print("==============PPEFINALCAMERAIDS=1======,",PPEFINALCAMERAIDS)
                            # empty_ppe_ls = []
                            # for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                            #     text = str(n) + ';'
                            #     empty_ppe_ls.append(text)
                            # string2 = ''
                            # if len(empty_ppe_ls) == 0:
                            #     string2 = '-1;'
                            #     lines.append('camera-ids = {0}'.format(string2))
                            # else:
                            #     string2 = ''
                            #     lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))

                        elif line.strip() == '[crowd-counting]':
                            lines.append('[crowd-counting]')
                            cr_final_index = 0
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['cr_data']) != 0:
                                    cr_final_index += 1

                            if cr_final_index == 0:
                                enable_val = 0
                                lines.append('enable = {0}'.format(enable_val))
                            else:
                                enable_val = 1
                                lines.append('enable = {0}'.format(enable_val))
                            lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                            lines.append("roi-overlay-enable=1")

                        elif line.strip()=='[steam-suit]':
                            lines.append('[steam-suit]')
                            lines.append('camera-ids = -1;')
                            lines.append('data-save-interval = 1')  

                        elif line.strip() == '[traffic-count]':
                            lines.append('[traffic-count]')
                            tc_final_index = 0
                            final_tc_empty_ls = []
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['tc_data']) != 0:
                                    final_tc_existed_cam_ids = []
                                    for tc_val in x['tc_data']:
                                        for tc_val___test in tc_val['label_name']:
                                            if tc_val___test not in tc_label_names:
                                                tc_label_names.append(tc_val___test)
                                        if len(tc_val['traffic_count']) != 0:
                                            final_tc_existed_cam_ids.append(
                                                tc_final_index + 1)
                                            for n in final_tc_existed_cam_ids:
                                                text = str(n) + ';'
                                                final_tc_empty_ls.append(text)
                                            string2 = ''
                                tc_final_index += 1
                            if len(final_tc_empty_ls) == 0:
                                final_tc_empty_ls.append(string2)
                            tc_empty_label_ls = []
                            for tc_label_name_test in tc_label_names:
                                text = str(tc_label_name_test) + ';'
                                tc_empty_label_ls.append(text)
                            test_string = ''
                            lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))
                        
                        elif line.strip() == '[traffic-jam]':
                            lines.append('[traffic-jam]')
                            if len(Traffic_JAM) !=0:
                                lines.append( 'enable = 1')
                            else:
                                lines.append( 'enable = 0')
                            lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                            lines.append('data-save-interval=10\n')

                        elif line.strip() == '[traffic-counting]':
                            lines.append('[traffic-counting]')
                            lines.append( 'enable = 0')
                            lines.append('details=[]\n')
                        
                        else:
                            lines.append(line.strip())

                model_config_details,secondarymodelconfigdetails = get_model_config_details()
                if model_config_details is not None:
                    if model_config_details['modeltype'] == 'yolo3':
                        classId = model_config_details['objectDetector_Yolo']['class_id']
                        modelconfigfile = model_config_details['objectDetector_Yolo']['modelpath']
                        modelconfigwrite =[]
                        modelconfigwrite.append('[property]')
                        modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                        modelconfigwrite.append('model-color-format=0')
                        modelconfigwrite.append('custom-network-config={0}/models/objectDetector_Yolo/yolov3.cfg'.format(get_current_dir_and_goto_parent_dir()))
                        enginFilePath = '{2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                        if os.path.exists(enginFilePath):
                            # print("yolov3 EngineFIle exists.")
                            modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            # print("yolov3 EngineFIle does not exist.")
                            anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(anotherenginFilePath):
                                print('----------------------')
                                destination= '{0}/models/objectDetector_Yolo/engine/'.format(get_current_dir_and_goto_parent_dir())
                                shutil.copy(anotherenginFilePath, destination)
                                if os.path.exists(enginFilePath):
                                    print('----------------') 
                                    modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            elif os.path.exists(secondenginFilePath):
                                print('----------------------')
                                destination= '{0}/models/objectDetector_Yolo/engine/'.format(get_current_dir_and_goto_parent_dir())
                                shutil.copy(secondenginFilePath, destination)
                                if os.path.exists(enginFilePath):
                                    print('----------------') 
                                    modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            else:
                                modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            # modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                            # modelconfigwrite.append('model-engine-file={0}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('labelfile-path={0}/models/objectDetector_Yolo/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('int8-calib-file={0}/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('network-mode=1')
                        modelconfigwrite.append('num-detected-classes=80')
                        modelconfigwrite.append('gie-unique-id=1')
                        modelconfigwrite.append('network-type=0')
                        modelconfigwrite.append('is-classifier=0')
                        modelconfigwrite.append('cluster-mode=2')
                        modelconfigwrite.append('maintain-aspect-ratio=1')
                        modelconfigwrite.append( 'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
                        modelconfigwrite.append('custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
                        modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                        modelconfigwrite.append('[class-attrs-all]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=1.0')
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold={0}'.format(person_threshold))
                        modelconfigwrite.append('[class-attrs-1]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-2]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-3]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-5]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-7]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')

                    elif  model_config_details['modeltype'] == 'yolo8':
                        classId = model_config_details['yoloV8']['class_id']
                        modelconfigfile = model_config_details['yoloV8']['modelpath']
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
                            # print("yolov8 EngineFIle does not exist.")

                            anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
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
                            # modelconfigwrite.append('model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                            # modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
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

                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('nms-iou-threshold=0.45')
                        modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                        modelconfigwrite.append('topk=300')

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

                    elif model_config_details['modeltype'] == 'trafficcam':
                        classId = model_config_details['trafficcamnet']['class_id']
                        modelconfigfile = model_config_details['trafficcamnet']['modelpath']
                        modelconfigwrite =[]
                        modelconfigwrite.append('[property]')
                        modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                        modelconfigwrite.append('tlt-model-key=tlt_encode')
                        modelconfigwrite.append('tlt-encoded-model=./trafficcamnet/resnet18_trafficcamnet_pruned.etlt')
                        modelconfigwrite.append('labelfile-path=./trafficcamnet/labels_trafficnet.txt')
                        modelconfigwrite.append('int8-calib-file=./trafficcamnet/trafficnet_int8.bin')
                        modelconfigwrite.append('model-engine-file=./trafficcamnet/engine/resnet18_trafficcamnet_pruned.etlt_b4_gpu{0}_int8.engine'.format(GPUSINDEX))
                        modelconfigwrite.append('input-dims=3;544;960;0')
                        modelconfigwrite.append('uff-input-blob-name=input_1')
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('process-mode=1')
                        modelconfigwrite.append('model-color-format=0')
                        modelconfigwrite.append('network-mode=1')
                        modelconfigwrite.append('num-detected-classes=4')
                        modelconfigwrite.append('interval=0')
                        modelconfigwrite.append('gie-unique-id=1')
                        modelconfigwrite.append('output-blob-names=output_bbox/BiasAdd;output_cov/Sigmoid')
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('pre-cluster-threshold=1.0')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2\n')
                        modelconfigwrite.append('[class-attrs-1]')
                        modelconfigwrite.append('pre-cluster-threshold=1.0')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2\n')

                        modelconfigwrite.append('[class-attrs-2]')
                        modelconfigwrite.append('pre-cluster-threshold=0.14')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2')
                        modelconfigwrite.append('detected-min-h=70\n')

                        modelconfigwrite.append('[class-attrs-3]')
                        modelconfigwrite.append('pre-cluster-threshold=1.0')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2\n')

                    elif model_config_details['modeltype'] == 'people':
                        classId = model_config_details['peoplenet']['class_id']
                        modelconfigfile = model_config_details['peoplenet']['modelpath']
                        modelconfigwrite =[]
                        modelconfigwrite.append('[property]')
                        modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                        modelconfigwrite.append('model-color-format=0')
                        modelconfigwrite.append( 'custom-network-config={0}/models/objectDetector_Yolo/yolov3.cfg'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append( 'model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append( '#model-engine-file={1}/models/objectDetector_Yolo/engine/model_b8_gpu{0}_int8.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append( 'labelfile-path={0}/models/objectDetector_Yolo/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('int8-calib-file={0}/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('network-mode=1')
                        modelconfigwrite.append('num-detected-classes=80')
                        modelconfigwrite.append('gie-unique-id=1')
                        modelconfigwrite.append('network-type=0')
                        modelconfigwrite.append('is-classifier=0')
                        modelconfigwrite.append('cluster-mode=2')
                        modelconfigwrite.append('maintain-aspect-ratio=1')
                        modelconfigwrite.append(  'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
                        modelconfigwrite.append( 'custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
                        modelconfigwrite.append( 'engine-create-func-name=NvDsInferYoloCudaEngineGet')
                        modelconfigwrite.append('[class-attrs-all]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=1.0')
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.7')         
                modelconfigfile  = os.path.splitext(modelconfigfile)[0]    
                with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                    for O_O_O, item in enumerate(modelconfigwrite):
                        f.write('%s\n' % item)

                with open(config_file, 'w') as f:
                    for O_O_O, item in enumerate(lines):
                        f.write('%s\n' % item)

    elif len(response)!=0 :
        GPUCOUNT = 1
        Totalcamera_pereachGpu = 2
        print("NEW____RESPONSE_data==",)
        print("====================len(response)=================",len(response))
        # print("----------------------------GPU_data--------------------------",GPU_data)
        if GPU_data is not None:
            directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app', 'configs')
            print('------------------directory_path----',directory_path)
            txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
            print("Text Files:", txt_files)
            if txt_files:
                try:
                    for txt_file in txt_files:
                        os.remove(os.path.join(directory_path, txt_file))
                    print("Text files deleted successfully ---1.0.1---")
                except Exception as e:
                    print(f"Error deleting text files---1.0.1---: {e}")
            else:
                print("No text files found in the directory.---1.0.1---")
            NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
            new_response=split_list(response,numberofsources_)
            if 'system_gpus' in GPU_data:
                GPUCOUNT = GPU_data['system_gpus']

            print("======================maximum===camera count for each GPU===",GPU_data['gpu_details'])
            
            if len(GPU_data['gpu_details']) !=0 :
                for jindex, iooojjn in enumerate(GPU_data['gpu_details']):
                    Totalcamera_pereachGpu = iooojjn['camera_limit']
                    break
                    

            # print("--------------------------new_response-----------",len(new_response))
            # print("--------------------------------------new_response---------only mechanical-jobs--",len(new_response))
            for config_index, writingresponse in enumerate(new_response):   
                # print("------------------------------------writingresponse=========len----------------",len(writingresponse))
                # print("--------------------------000GPUSINDEX-===",GPUSINDEX)
                # print("--------------------------===",config_index)
                # print("======Totalcamera_pereachGpu ={0} camera_id {1}".format(Totalcamera_pereachGpu,camera_id))
                # print("====================================Totalcamera_pereachGpu <= camera_id=====================",Totalcamera_pereachGpu <= camera_id)
                # print("====================================Totalcamera_pereachGpu >= camera_id=====================",Totalcamera_pereachGpu >= camera_id)
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
                # GPUSINDEX= 0
                config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
                crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
                config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
                hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
                PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))

                parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
                lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
                roi_enable_cam_ids = []
                ppe_enable_cam_ids = []
                config_tjm_lines =[]
                # roi_objects=set()
                traffic_count_enabledcameraids=[]
                cr_enable_cam_ids = []
                tc_label_names = []
                normal_config_file = 0
                final_roi_existed_cam_ids = []
                final_truck_cam_ids = []
                hooter_line = []
                crowd_line = []  
                onlyCrashHelmet =[]
                PPELINE = []     
                PPEFINALCAMERAIDS =[]
                Traffic_JAM = []
                traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
                steamsuit_cameraid =[]
                for index, x in enumerate(writingresponse): 
                    x['cameraid'] = camera_id
                    if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
                        if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("***************111111************")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("TC-CR_PPE===2")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:    
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("TC-CR_RA===3")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("cr-ra_PPE===5")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("RA-TC_PPE===handled")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("cr-ra===6")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("ra_TC===7")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID) 
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("ra_PPE===8")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("CR_TC===9")
                            if len(x['cr_data']) !=0:
                                print("-----------------x-----------999999---------")
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                print('-----------------print("-----------------x-----------999999---------")-----------------')
                                if x['cr_data'][0]['full_frame'] == False:
                                    print('-----------------print("-----------------x-----------999999-.01111111111111111111111111--------")-----------------')
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        print('-----------------print("-----------------x-----------999999-.02222222222222222222222222222--------")-----------------')
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        print('-----------------print("-----------------x-----------999999-.03333333333333333333333333333--------")-----------------')
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("PPE_TC===10")
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)  
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)    
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("PPE_CR===11")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)  
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("CR===12")    
                            if len(x['cr_data']) !=0:
                                print("-------------CR-------12---------kkkk-------------")
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                print("-------------CR-------12.0---------kkkk-------------")
                                if x['cr_data'][0]['full_frame'] == False:
                                    print("-------------CR-------12.1---------kkkk-------------")
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        print("-------------CR-------12.2---------kkkk-------------")
                                        cr_fun_conf_analytics(x, lines,config_tjm_lines)
                                        print("-------------CR-------12.3---------kkkk-------------")
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                                        print("-------------CR-------12.4---------kkkk-------------")
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("RA===13")    
                            roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("TC===14") 
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("PPE===14") 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        width_ratio=960/960
                        height_ratio= 544/544
                        if 'trafficjam_data' in x :
                            # print("---------------------validate_rois_array(x['trafficjam_data'],roi_required_keys)------------",validate_rois_array(x['trafficjam_data'],roi_required_keys))
                            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----00-------')
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
                                                # print('str(FinalTime)-------type---8------------',type(FinalTime))
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
                                                # print('str(FinalTime)-------type---7------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                    Traffic_JAM.append(NewcameraID)
                                else:
                                    print()
                            
                        # print("INDEX------------------------------------------",index)    
                        if '[crdcnt{}]'.format(index) not in crowd_line:
                            # print("-----")
                            crowd_line.append('[crdcnt{0}]'.format(index))
                            crowd_line.append("enable=0")
                            crowd_line.append("process-on-full-frame=1")
                            crowd_line.append("operate-on-label=person;")
                            crowd_line.append("max-count=1;")
                            crowd_line.append("min-count=0;")
                            crowd_line.append("data-save-time-in-sec=3\n")
                            
                        if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                            lines.append('[roi-filtering-stream-{0}]'.format(index))
                            if 'trafficjam_data' in x :
                                if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                    lines.append("enable=1")
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
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                    Traffic_JAM.append(NewcameraID)
                                else:
                                    lines.append("enable=0")
                                    lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            else:
                                lines.append("enable=0")
                                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            lines.append("inverse-roi=0")
                            # lines.append("class-id= 0;\n")
                            
                        if '[RA{}]'.format(index) not in hooter_line:
                            # print("-----")
                            hooter_line.append('[RA{0}]'.format(index))
                            hooter_line.append("enable = 0")
                            hooter_line.append("operate-on-label = person;")
                            hooter_line.append("hooter-enable = 0")
                            hooter_line.append("hooter-ip = none")
                            hooter_line.append('hooter-type = 0;')
                            hooter_line.append('hooter-shoutdown-time = 10')
                            hooter_line.append("hooter-stop-buffer-time = 3")
                            hooter_line.append("data-save-time-in-sec = 3\n")
                        # if '[crdcnt{}]'.format(index) not in crowd_line:
                        #     crowd_line.append('[crdcnt{0}]'.format(index))
                        #     crowd_line.append("enable=0")
                        #     crowd_line.append("process-on-full-frame=1")
                        #     crowd_line.append("operate-on-label=person;")
                        #     crowd_line.append("max-count=1;")
                        #     crowd_line.append("min-count=0;")
                        #     crowd_line.append("data-save-time-in-sec=3\n")
                        # if '[roi-filtering-stream-{0}]'.format(index) not in lines:                       
                        #     lines.append('[roi-filtering-stream-{0}]'.format(index))
                        #     lines.append("enable=0")
                        #     lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                        #     lines.append("inverse-roi=0")
                        #     lines.append("class-id= 0;\n")           

                        if '[PPE{}]'.format(index) not in PPELINE:
                            # print("-----")
                            PPELINE.append('[PPE{0}]'.format(index))
                            PPELINE.append("enable = 0")
                            PPELINE.append("hooter-enable = 0")
                            PPELINE.append("hooter-ip = none")
                            PPELINE.append('hooter-type = 0;')
                            PPELINE.append('hooter-shoutdown-time = 10')
                            PPELINE.append("hooter-stop-buffer-time = 3")
                            PPELINE.append('analytics-details =[{"analytics_type":0, "operate_on": "null;"},{"analytics_type":1, "operate_on": "null;"}]')
                            PPELINE.append("data-save-time-in-sec = 3\n")
                        NewcameraID+=1                            
                total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids,Traffic_JAM))
                with open(config_analytics_file, 'w') as f:
                    for item in lines:
                        f.write('%s\n' % item)
                with open(hooter_config_file_path, 'w') as hooter_file:
                    for jim in hooter_line:
                        hooter_file.write('%s\n' % jim)

                with open(PPE_config_file_path, 'w') as PPE_file:
                    for jim in PPELINE:
                        PPE_file.write('%s\n' % jim)
                with open(crowd_config_file, 'w') as crowd_file:
                    for O_O_O, item in enumerate(crowd_line):
                        crowd_file.write('%s\n' % item)

                # print('----------------------len---------',len(config_tjm_lines))
                with open(parking_roi_config_file, 'w') as file:
                    write_array_to_file(file,config_tjm_lines)
                    file.close()
                lines = []
                final_both_roi_cam_ids = []
                with open(sample_config_file) as file:
                    for write_config, line in enumerate(file):
                        if line.strip() == '[application]':
                            lines.append('[application]')
                            lines.append('enable-perf-measurement=1')
                            lines.append('perf-measurement-interval-sec=1')
                        elif line.strip() == '[tiled-display]':
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, Traffic_JAM)
                            total_stream_for_stremux_union = finaL_RA_PPE
                            num = math.sqrt(int(len(finaL_RA_PPE)))
                            rows,columns= get_layout(len(total_stream_for_stremux_union))
                            # if 1 < num < 1.4:
                            #     rows = 1
                            #     columns = 2
                            # elif num == 1:
                            #     rows = 1
                            #     columns = 2
                            # else:
                            #     if 1 > num >= 1.4:
                            #         if len(finaL_RA_PPE)>3:
                            #             rows = 2
                            #             columns = 2
                            #         else:
                            #             rows = 1
                            #             columns = 2                                            
                            #     else:
                            #         rows = int(round(num))
                            #         columns = 2
                            lines.append('[tiled-display]')
                            if execute_nvidia_smi(GPUSINDEX):
                                lines.append('enable=1')
                            elif TitledDisplayEnable:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('rows={0}'.format(str(rows)))
                            lines.append('columns={0}'.format(str(columns)))
                            lines.append('width=960')
                            lines.append('height=544')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[sources]':    
                            # print("newlength===", len(writingresponse))                            
                            for n, x in enumerate(writingresponse):
                                cam_id = '{0}'.format(int(n))
                                ppe_enable_cam_ids_exist=0
                                newcrowdcount=0
                                roi_enable_cam_ids_exist =0
                                trafficJamcount = 0 
                                if camera_id in roi_enable_cam_ids:
                                    roi_enable_cam_ids_exist = 1
                                elif camera_id in ppe_enable_cam_ids:
                                    ppe_enable_cam_ids_exist = 1
                                elif camera_id in cr_enable_cam_ids:
                                    newcrowdcount = 1

                                elif camera_id in Traffic_JAM:
                                    trafficJamcount= 1
                                if camera_id in ppe_enable_cam_ids:
                                    PPEFINALCAMERAIDS.append(camera_id)
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                                if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 and trafficJamcount > 0  :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  678990 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount= 0 

                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0   :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  678990 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0

                                elif roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 and trafficJamcount > 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  345677 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount= 0 
                                
                                elif roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  345677 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and trafficJamcount > 0 ) :
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  9876543 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount = 0 
                                
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  9876543 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif roi_enable_cam_ids_exist > 0:
                                    # print("normal_config_file += 555551 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif ppe_enable_cam_ids_exist > 0:
                                    # print("normal_config_file += 666666666666666 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  123456789 ------------------------",camera_id)
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif len(traffic_count_enabledcameraids)>0:
                                    # print("normal_config_file += 777777777777777777 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif newcrowdcount >0:
                                    # print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0

                                elif trafficJamcount >0:
                                    # print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount = 0 


                        elif line.strip() == '[sink0]':
                            lines.append('[sink0]')
                            lines.append('enable=1')
                            # if execute_nvidia_smi(GPUSINDEX):
                            #     lines.append('type=2')
                            # elif TitledDisplayEnable:
                            #     lines.append('type=2')
                            # else:
                            #     lines.append('type=1')
                            if gridview_true is True:
                                lines.append('type=2')
                            else:
                                lines.append('type=1')
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
                            lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            if batch_pushouttime == 40000:
                                lines.append('batched-push-timeout=40000')
                            else:
                                lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            lines.append('width=1920')
                            lines.append('height=1080')
                            lines.append('enable-padding=0')
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[primary-gie]':
                            lines.append('[primary-gie]')
                            lines.append('enable=1')
                            lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            # lines.append('bbox-border-color0=0;1;0;1.0')
                            # lines.append('bbox-border-color1=0;1;1;0.7')
                            # lines.append('bbox-border-color2=0;1;0;0.7')
                            # lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('bbox-border-color0=0.3;0;0;1')# dark shade of red or choclate
                            # lines.append('bbox-border-color1=0;1;1;1')# red 
                            lines.append('bbox-border-color1=1;0.3;0.9;1')#pinkish-purple or magenta
                            lines.append('bbox-border-color2=0.545;0;1;1')#purple
                            lines.append('bbox-border-color3=1;0.659;0;1')#orange
                            # lines.append('bbox-border-color3=0;1;0;1')
                            lines.append('bbox-border-color4=0.561;0.737;0.561;1')#dark sea green 
                            lines.append('bbox-border-color5=0.502;0.502;0;1')#olive color
                            lines.append('bbox-border-color6=0.392;0.584;0.929;1')#corn flower blue
                            lines.append('bbox-border-color7=0.941;0.502;0.502;1')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                            lines.append('model-engine-file=../../models/yoloV8/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                            lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                        elif line.strip() == '[primary-gie-ss]':
                            lines.append('[primary-gie-ss]')
                            if len(steamsuit_cameraid) !=0:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('batch-size={0}'.format(str(1)))
                            lines.append('bbox-border-color0=0;1;1;0.7')
                            lines.append('bbox-border-color1=0;1;1;0.7')
                            lines.append('bbox-border-color2=0;1;1;0.7')
                            lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            lines.append( 'config-file = ../../models/config_infer_primary_tsk_ss.txt')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))    
                        elif line.strip() == '[secondary-gie0]':
                            lines.append('[secondary-gie0]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            # lines.append('gie-unique-id = 4')
                            lines.append('gie-unique-id = 6')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 0;0;0;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                                secondaryconfig_file = []                                    
                                secondaryconfig_file.append('[property]')
                                secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(HelmetEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    

                                # secondaryconfig_file.append('tlt-encoded-model=./helmet_detector_v5/resnet18_helmet_detector_v5.etlt')
                                # secondaryconfig_file.append('labelfile-path=./helmet_detector_v5/labels.txt')
                                # secondaryconfig_file.append('model-engine-file=./helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                secondaryconfig_file.append('infer-dims=3;320;320')
                                secondaryconfig_file.append('uff-input-blob-name=input_1')
                                secondaryconfig_file.append('batch-size=1')
                                secondaryconfig_file.append('process-mode=2')
                                secondaryconfig_file.append('model-color-format=0')
                                secondaryconfig_file.append('network-mode=2')
                                secondaryconfig_file.append('num-detected-classes=2')
                                secondaryconfig_file.append('interval=0')
                                secondaryconfig_file.append('gie-unique-id=2')
                                secondaryconfig_file.append('operate-on-gie-id=1')
                                secondaryconfig_file.append('operate-on-class-ids=0;')
                                secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_file.append('network-type=0')
                                secondaryconfig_file.append('uff-input-order=0\n')
                                secondaryconfig_file.append('[class-attrs-0]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20\n')
                                secondaryconfig_file.append('[class-attrs-1]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20')
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_file):
                                        f.write('%s\n' % item)
                            else:
                                if Hemetdetails is not None:
                                    HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                                    Hemeltversion= Hemetdetails['helmet']['version']
                                    lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                    lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                                    secondaryconfig_file = []                                    
                                    secondaryconfig_file.append('[property]')
                                    secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                    HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(HelmetEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                    # secondaryconfig_file.append('tlt-encoded-model=./helmet_detector_v{0}/resnet18_helmet_detector_v5.etlt'.format(Hemeltversion))
                                    # secondaryconfig_file.append('labelfile-path=./helmet_detector_v{0}/labels.txt'.format(Hemeltversion))
                                    # secondaryconfig_file.append('model-engine-file=./helmet_detector_v{0}/resnet18_helmet_detector_v5.etlt_b1_gpu{1}_fp16.engine'.format(Hemeltversion,GPUSINDEX))
                                    secondaryconfig_file.append('infer-dims=3;320;320')
                                    secondaryconfig_file.append('uff-input-blob-name=input_1')
                                    secondaryconfig_file.append('batch-size=1')
                                    secondaryconfig_file.append('process-mode=2')
                                    secondaryconfig_file.append('model-color-format=0')
                                    secondaryconfig_file.append('network-mode=2')
                                    secondaryconfig_file.append('num-detected-classes=2')
                                    secondaryconfig_file.append('interval=0')
                                    secondaryconfig_file.append('gie-unique-id=2')
                                    secondaryconfig_file.append('operate-on-gie-id=1')
                                    secondaryconfig_file.append('operate-on-class-ids=0;')
                                    secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_file.append('network-type=0')
                                    secondaryconfig_file.append('uff-input-order=0\n')
                                    secondaryconfig_file.append('[class-attrs-0]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20\n')
                                    secondaryconfig_file.append('[class-attrs-1]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_file):
                                            f.write('%s\n' % item)                                
                        elif line.strip() == '[secondary-gie1]':
                            lines.append('[secondary-gie1]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            # lines.append('gie-unique-id = 5')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('gie-unique-id = 7')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                            if defaultsecondmodels == True :
                                lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                                secondaryconfig_filevest = []
                                secondaryconfig_filevest.append('[property]')
                                secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(VestEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                                # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                                # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('infer-dims=3;320;320')
                                secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                secondaryconfig_filevest.append('batch-size=1')
                                secondaryconfig_filevest.append('process-mode=2')
                                secondaryconfig_filevest.append('model-color-format=0')
                                secondaryconfig_filevest.append('network-mode=2')
                                secondaryconfig_filevest.append('num-detected-classes=3')
                                secondaryconfig_filevest.append('interval=0')
                                secondaryconfig_filevest.append('gie-unique-id=2')
                                secondaryconfig_filevest.append('operate-on-gie-id=1')
                                secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_filevest.append('network-type=0')
                                secondaryconfig_filevest.append('uff-input-order=0\n')
                                secondaryconfig_filevest.append('[class-attrs-0]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20\n')
                                secondaryconfig_filevest.append('[class-attrs-1]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')                                
                                secondaryconfig_filevest.append('[class-attrs-2]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')      
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_filevest):
                                        f.write('%s\n' % item)
                            else:
                                if Vestdetails is not None:
                                    Vestconfigfile = Vestdetails['vest']['modelpath']
                                    Vestversion= Vestdetails['vest']['version']
                                    lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                    lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                                    secondaryconfig_filevest = []
                                    secondaryconfig_filevest.append('[property]')
                                    secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                    VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(VestEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v{0}/resnet18_vest_detector_v{1}.etlt'.format(Vestversion,Vestversion))
                                    # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v{0}/labels.txt'.format(Vestversion))
                                    # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v{0}/resnet18_vest_detector_v{1}.etlt_b1_gpu{2}_fp16.engine'.format(Vestversion,Vestversion,GPUSINDEX))
                                    secondaryconfig_filevest.append('infer-dims=3;320;320')
                                    secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                    secondaryconfig_filevest.append('batch-size=1')
                                    secondaryconfig_filevest.append('process-mode=2')
                                    secondaryconfig_filevest.append('model-color-format=0')
                                    secondaryconfig_filevest.append('network-mode=2')
                                    secondaryconfig_filevest.append('num-detected-classes=3')
                                    secondaryconfig_filevest.append('interval=0')
                                    secondaryconfig_filevest.append('gie-unique-id=2')
                                    secondaryconfig_filevest.append('operate-on-gie-id=1')
                                    secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                    secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_filevest.append('network-type=0')
                                    secondaryconfig_filevest.append('uff-input-order=0\n')
                                    secondaryconfig_filevest.append('[class-attrs-0]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20\n')
                                    secondaryconfig_filevest.append('[class-attrs-1]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')                                        
                                    secondaryconfig_filevest.append('[class-attrs-2]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_filevest):
                                            f.write('%s\n' % item)

                        elif line.strip() == '[secondary-gie2]':                            
                            lines.append('[secondary-gie2]')
                            if len(onlyCrashHelmet) !=0:
                                lines.append('enable = 1')
                            else:
                                lines.append('enable = 0')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 8')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')

                            CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                if os.path.exists(anotherenginFilePath):
                                    print('----------------------')
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(anotherenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                elif os.path.exists(secondenginFilePath):
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(secondenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                else:
                                    lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            if 1:#defaultsecondmodels == True :
                                # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/crash_helmet_nano_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                                ScondaryCrushhelmet = []
                                ScondaryCrushhelmet.append('[property]')
                                ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                                ScondaryCrushhelmet.append('model-color-format=0')
                                # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                                CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(CrushHelmet):
                                    # print("yolov3 EngineFIle exists.")
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    # print("yolov3 EngineFIle does not exist.")
                                    # ScondaryCrushhelmet.append('tlt-encoded-model={0}/models/yoloV8_crash_helmet/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    # ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    # #yoloV8_crash_helmet/engine/model_b4_gpu0_fp16.engine
                                    # ScondaryCrushhelmet.append('model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                                # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                                # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('batch-size=1')
                                ScondaryCrushhelmet.append('network-mode=2')
                                ScondaryCrushhelmet.append('num-detected-classes=2')
                                ScondaryCrushhelmet.append('interval=0')
                                ScondaryCrushhelmet.append('gie-unique-id=1')
                                ScondaryCrushhelmet.append('process-mode=2')
                                ScondaryCrushhelmet.append('network-type=0')
                                ScondaryCrushhelmet.append('cluster-mode=2')
                                ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                                ScondaryCrushhelmet.append('operate-on-gie-id=1')
                                ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                                ScondaryCrushhelmet.append('symmetric-padding=1')
                                ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                                ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                                ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                                ScondaryCrushhelmet.append('[class-attrs-0]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300\n')

                                ScondaryCrushhelmet.append('[class-attrs-1]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300')     
                                with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                                    for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                        f.write('%s\n' % item)
                            
                        elif line.strip() == '[tracker]':
                            lines.append('[tracker]')
                            lines.append('enable=1')
                            lines.append('tracker-width=960')
                            lines.append('tracker-height=544')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('#enable-batch-process=0')
                            if display_tracker :
                                lines.append('display-tracking-id=1')
                            else:
                                lines.append('display-tracking-id=0')
                            lines.append('user-meta-pool-size=64')
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
                        elif line.strip() == '[restricted-access]':
                            lines.append('[restricted-access]')
                            final_index = 0
                            final_roi_empty_ls = []
                            check_camera_id_for_RA = []
                            for Cherry, x in enumerate(writingresponse):
                                string2 = '-1;'
                                if len(x['roi_data']) != 0:
                                    for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                        label_name = roi_value['label_name']
                                        if ('person' in label_name and 'truck' in label_name):
                                            final_both_roi_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'truck' in label_name:
                                            final_truck_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' in label_name:
                                            final_roi_existed_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' not in label_name and 'truck' not in label_name:
                                            pass
                                        else:
                                            pass
                                final_index += 1
                            string_test = '-1;'
                            if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                                check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                            final_roi_existed_cam_ids = roi_enable_cam_ids
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            if len(roi_enable_cam_ids)== 0:
                                lines.append('enable = 0')
                            else:
                                lines.append('enable = 1')
                            lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                            lines.append('roi-overlay-enable = 1')
                            lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))
                        elif line.strip() == '[ppe-type-1]':
                            lines.append('[PPE]')
                            # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                            empty_ppe_ls = []
                            for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                                text = str(n) + ';'
                                empty_ppe_ls.append(text)
                            string2 = ''
                            if len(empty_ppe_ls) == 0:
                                # string2 = '-1;'
                                # lines.append('camera-ids = {0}'.format(string2))
                                lines.append('enable = 0')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            else:
                                # string2 = ''
                                # lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                                lines.append('enable = 1')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            # lines.append('[ppe-type-1]')
                            # empty_ppe_ls = []
                            # for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                            #     text = str(n) + ';'
                            #     empty_ppe_ls.append(text)
                            # string2 = ''
                            # if len(empty_ppe_ls) == 0:
                            #     string2 = '-1;'
                            #     lines.append('camera-ids = {0}'.format(string2))
                            # else:
                            #     string2 = ''
                            #     lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                        elif line.strip() == '[crowd-counting]':
                            lines.append('[crowd-counting]')
                            cr_final_index = 0
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['cr_data']) != 0:
                                    cr_final_index += 1
                            if cr_final_index == 0:
                                enable_val = 0
                                lines.append('enable = {0}'.format(enable_val))
                            else:
                                enable_val = 1
                                lines.append('enable = {0}'.format(enable_val))
                            lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                            lines.append("roi-overlay-enable=1")

                        elif line.strip()=='[steam-suit]':
                            lines.append('[steam-suit]')
                            lines.append('camera-ids = -1;')
                            lines.append('data-save-interval = 1')  

                        elif line.strip() == '[traffic-count]':
                            lines.append('[traffic-count]')
                            tc_final_index = 0
                            final_tc_empty_ls = []
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['tc_data']) != 0:
                                    final_tc_existed_cam_ids = []
                                    for tc_val in x['tc_data']:
                                        for tc_val___test in tc_val['label_name']:
                                            if tc_val___test not in tc_label_names:
                                                tc_label_names.append(tc_val___test)
                                        if len(tc_val['traffic_count']) != 0:
                                            final_tc_existed_cam_ids.append(
                                                tc_final_index + 1)
                                            for n in final_tc_existed_cam_ids:
                                                text = str(n) + ';'
                                                final_tc_empty_ls.append(text)
                                            string2 = ''
                                tc_final_index += 1
                            if len(final_tc_empty_ls) == 0:
                                final_tc_empty_ls.append(string2)
                            # lines.append('camera-ids = {0}'.format(string2.join(final_tc_empty_ls)))
                            tc_empty_label_ls = []
                            for tc_label_name_test in tc_label_names:
                                text = str(tc_label_name_test) + ';'
                                tc_empty_label_ls.append(text)
                            test_string = ''
                            lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))


                        elif line.strip() == '[traffic-jam]':
                            lines.append('[traffic-jam]')
                            if len(Traffic_JAM) !=0:
                                lines.append( 'enable = 1')
                            else:
                                lines.append( 'enable = 0')
                            lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                            lines.append('data-save-interval=10\n')
                        elif line.strip() == '[traffic-counting]':
                            lines.append('[traffic-counting]')
                            lines.append( 'enable = 0')
                            lines.append('details=[]\n')
                        else:
                            lines.append(line.strip())
                model_config_details ,secondarymodelconfigdetails= get_model_config_details()
                if model_config_details is not None:
                    if model_config_details['modeltype'] == 'yolo3':
                        classId = model_config_details['objectDetector_Yolo']['class_id']
                        modelconfigfile = model_config_details['objectDetector_Yolo']['modelpath']
                        modelconfigwrite =[]
                        modelconfigwrite.append('[property]')
                        modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                        modelconfigwrite.append('model-color-format=0')
                        modelconfigwrite.append('custom-network-config={0}/models/objectDetector_Yolo/yolov3.cfg'.format(get_current_dir_and_goto_parent_dir()))
                        enginFilePath = '{2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                        if os.path.exists(enginFilePath):
                            # print("yolov3 EngineFIle exists.")
                            modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            # print("yolov3 EngineFIle does not exist.")
                            anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(anotherenginFilePath):
                                print('----------------------')
                                destination= '{0}/models/objectDetector_Yolo/engine/'.format(get_current_dir_and_goto_parent_dir())
                                shutil.copy(anotherenginFilePath, destination)
                                if os.path.exists(enginFilePath):
                                    print('----------------') 
                                    modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            elif os.path.exists(secondenginFilePath):
                                print('----------------------')
                                destination= '{0}/models/objectDetector_Yolo/engine/'.format(get_current_dir_and_goto_parent_dir())
                                shutil.copy(secondenginFilePath, destination)
                                if os.path.exists(enginFilePath):
                                    print('----------------') 
                                    modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            else:
                                modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                                modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            # modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                            # modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('labelfile-path={0}/models/objectDetector_Yolo/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('int8-calib-file={0}/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('network-mode=1')
                        modelconfigwrite.append('num-detected-classes=80')
                        modelconfigwrite.append('gie-unique-id=1')
                        modelconfigwrite.append('network-type=0')
                        modelconfigwrite.append('is-classifier=0')
                        modelconfigwrite.append('cluster-mode=2')
                        modelconfigwrite.append('maintain-aspect-ratio=1')
                        modelconfigwrite.append( 'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
                        modelconfigwrite.append('custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
                        modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                        modelconfigwrite.append('[class-attrs-all]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=1.0')
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold={0}'.format(person_threshold))
                        modelconfigwrite.append('[class-attrs-1]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-2]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-3]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-5]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                        modelconfigwrite.append('[class-attrs-7]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.4')
                    elif  model_config_details['modeltype'] == 'yolo8':
                        classId = model_config_details['yoloV8']['class_id']
                        modelconfigfile = model_config_details['yoloV8']['modelpath']
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
                            anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
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
                            # print("yolov8 EngineFIle does not exist.")
                            # modelconfigwrite.append('model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                            # modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
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
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('nms-iou-threshold=0.45')
                        modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                        modelconfigwrite.append('topk=300')

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
                    elif model_config_details['modeltype'] == 'trafficcam':
                        classId = model_config_details['trafficcamnet']['class_id']
                        modelconfigfile = model_config_details['trafficcamnet']['modelpath']
                        modelconfigwrite =[]
                        modelconfigwrite.append('[property]')
                        modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                        modelconfigwrite.append('tlt-model-key=tlt_encode')
                        modelconfigwrite.append('tlt-encoded-model=./trafficcamnet/resnet18_trafficcamnet_pruned.etlt')
                        modelconfigwrite.append('labelfile-path=./trafficcamnet/labels_trafficnet.txt')
                        modelconfigwrite.append('int8-calib-file=./trafficcamnet/trafficnet_int8.bin')
                        modelconfigwrite.append('model-engine-file=./trafficcamnet/engine/resnet18_trafficcamnet_pruned.etlt_b4_gpu{0}_int8.engine'.format(GPUSINDEX))
                        modelconfigwrite.append('input-dims=3;544;960;0')
                        modelconfigwrite.append('uff-input-blob-name=input_1')
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('process-mode=1')
                        modelconfigwrite.append('model-color-format=0')
                        modelconfigwrite.append('network-mode=1')
                        modelconfigwrite.append('num-detected-classes=4')
                        modelconfigwrite.append('interval=0')
                        modelconfigwrite.append('gie-unique-id=1')
                        modelconfigwrite.append('output-blob-names=output_bbox/BiasAdd;output_cov/Sigmoid')
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('pre-cluster-threshold=1.0')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2\n')
                        modelconfigwrite.append('[class-attrs-1]')
                        modelconfigwrite.append('pre-cluster-threshold=1.0')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2\n')
                        modelconfigwrite.append('[class-attrs-2]')
                        modelconfigwrite.append('pre-cluster-threshold=0.14')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2')
                        modelconfigwrite.append('detected-min-h=70\n')
                        modelconfigwrite.append('[class-attrs-3]')
                        modelconfigwrite.append('pre-cluster-threshold=1.0')
                        modelconfigwrite.append('group-threshold=1')
                        modelconfigwrite.append('eps=0.2\n')
                    elif model_config_details['modeltype'] == 'people':
                        classId = model_config_details['peoplenet']['class_id']
                        modelconfigfile = model_config_details['peoplenet']['modelpath']
                        modelconfigwrite =[]
                        modelconfigwrite.append('[property]')
                        modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                        modelconfigwrite.append('batch-size=1')
                        modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                        modelconfigwrite.append('model-color-format=0')
                        modelconfigwrite.append( 'custom-network-config={0}/models/objectDetector_Yolo/yolov3.cfg'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append( '#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append( '#model-engine-file={1}/models/objectDetector_Yolo/engine/model_b8_gpu{0}_int8.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append( 'labelfile-path={0}/models/objectDetector_Yolo/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('int8-calib-file={0}/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('network-mode=1')
                        modelconfigwrite.append('num-detected-classes=80')
                        modelconfigwrite.append('gie-unique-id=1')
                        modelconfigwrite.append('network-type=0')
                        modelconfigwrite.append('is-classifier=0')
                        modelconfigwrite.append('cluster-mode=2')
                        modelconfigwrite.append('maintain-aspect-ratio=1')
                        modelconfigwrite.append(  'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
                        modelconfigwrite.append( 'custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
                        modelconfigwrite.append( 'engine-create-func-name=NvDsInferYoloCudaEngineGet')
                        modelconfigwrite.append('[class-attrs-all]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=1.0')
                        modelconfigwrite.append('[class-attrs-0]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=0.7')
                        modelconfigwrite.append('[class-attrs-7]')
                        modelconfigwrite.append('nms-iou-threshold=0.3')
                        modelconfigwrite.append('threshold=1.0')            
                modelconfigfile  = os.path.splitext(modelconfigfile)[0]  
                with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                    for O_O_O, item in enumerate(modelconfigwrite):
                        f.write('%s\n' % item) 
                # with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                #     for O_O_O, item in enumerate(modelconfigwrite):
                #         f.write('%s\n' % item)
                with open(config_file, 'w') as f:
                    for O_O_O, item in enumerate(lines):
                        f.write('%s\n' % item)
        
    elif len(steamsuitcameradetails) !=0:
        print("steamsutid==",len(steamsuitcameradetails) )
        directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app_ss', 'configs')
        txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
        if txt_files:
            try:
                os.system("rm -r " + os.path.join(directory_path, '*.txt'))
                print("Text files deleted successfully.---1.0.2--")
            except Exception as e:
                print(f"Error deleting text files: ---1.0.2--{e}")
        else:
            print("No text files found in the directory.---1.0.2--")
        NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
        # print("=====NEwcount====",NEwcount)
        config_index = 0 
        config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
        crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
        config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
        hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
        PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))
        parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
        lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
        roi_enable_cam_ids = []
        ppe_enable_cam_ids = []
        traffic_count_enabledcameraids=[]
        cr_enable_cam_ids = []
        tc_label_names = []
        normal_config_file = 0
        final_roi_existed_cam_ids = []
        final_truck_cam_ids = []
        hooter_line = []
        crowd_line = [] 
        PPELINE = [] 
        onlyCrashHelmet =[]      
        PPEFINALCAMERAIDS =[]
        traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
        steamsuit_cameraid =[]        
        Steamsuitdata = steamsuitcameradetails   
        lines = []
        final_both_roi_cam_ids = []
        with open(sample_config_file) as file:
            for write_config, line in enumerate(file):
                if line.strip() == '[application]':
                    lines.append('[application]')
                    lines.append('enable-perf-measurement=1')
                    lines.append('perf-measurement-interval-sec=1')

                elif line.strip() == '[tiled-display]':
                    finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                    finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                    finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                    total_stream_for_stremux_union = finaL_RA_PPE
                    rows,columns= get_layout(len(total_stream_for_stremux_union))
                    num = math.sqrt(int(1))
                    # print("num----",num )
                    # print("num----",num )
                    # if 1 < num < 1.4:
                    #     rows = 1
                    #     columns = 2
                    # elif num == 1:
                    #     rows = 1
                    #     columns = 2
                    # else:
                    #     if 1 > num >= 1.4:
                    #         if len(finaL_RA_PPE)>3:
                    #             rows = 2
                    #             columns = 2
                    #         else:
                    #             rows = 1
                    #             columns = 2                                
                    #     else:
                    #         rows = int(round(num))
                    #         columns = 2
                        # print("row====s ",rows)
                        # print("columns====s ",columns)

                    lines.append('[tiled-display]')
                    if execute_nvidia_smi(GPUSINDEX):
                        lines.append('enable=1')
                    elif TitledDisplayEnable:
                        lines.append('enable=1')
                    else:
                        lines.append('enable=0')
                    lines.append('rows={0}'.format(str(1)))
                    lines.append('columns={0}'.format(str(columns)))
                    lines.append('width=960')
                    lines.append('height=544')
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[sources]':  
                    find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                    if find_data is not None:
                        if find_data['rtsp_flag'] == '1':
                            if 'rtsp' in x['rtsp_url']:
                                x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')


                    # print("Steamsuitdata====",Steamsuitdata)
                    if len(Steamsuitdata) !=0 :
                        uri = Steamsuitdata[0]['rtsp_url']
                        lines.append('[source{0}]'.format(normal_config_file))
                        lines.append('enable=1')
                        lines.append('type=4')
                        lines.append('uri = {0}'.format(uri))
                        lines.append('num-sources=1')
                        lines.append('gpu-id={0}'.format(GPUSINDEX))
                        lines.append('nvbuf-memory-type=0')
                        lines.append('latency=150')
                        lines.append('camera-id={0}'.format(camera_id))
                        camera_required_data= {"cameraname":Steamsuitdata[0]['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                        allWrittenSourceCAmIds.append(camera_required_data)
                        # print("-------------(camera_id) +=  123ertyu8888 ------------------------")
                        PPEFINALCAMERAIDS.append(camera_id)
                        lines.append('camera-name={0}'.format(Steamsuitdata[0]['cameraname']))
                        lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                        lines.append('operate-on-class = {0}'.format(x['selected_object']))
                        lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                        if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                            lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                        else:
                            lines.append('drop-frame-interval = 1\n')
                        normal_config_file += 1    
                        steamsuit_cameraid.append(camera_id)                        
                        camera_id += 1                    
                elif line.strip() == '[sink0]':
                    lines.append('[sink0]')
                    lines.append('enable=1')
                    # if execute_nvidia_smi(GPUSINDEX):
                    #     lines.append('type=2')
                    # elif TitledDisplayEnable:
                    #     lines.append('type=2')
                    # else:
                    #     lines.append('type=1')
                    if gridview_true is True:
                        lines.append('type=2')
                    else:
                        lines.append('type=1')
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
                    lines.append( 'batch-size={0}'.format(len(Steamsuitdata)))
                    if batch_pushouttime == 40000:
                        lines.append('batched-push-timeout=40000')
                    else:
                        lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                    lines.append('width=1920')
                    lines.append('height=1080')
                    lines.append('enable-padding=0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[primary-gie]':
                    lines.append('[primary-gie]')
                    lines.append('enable=1')
                    lines.append('batch-size={0}'.format(len(Steamsuitdata)))
                    # lines.append('bbox-border-color0=0;1;0;1.0')
                    # lines.append('bbox-border-color1=0;1;1;0.7')
                    # lines.append('bbox-border-color2=0;1;0;0.7')
                    # lines.append('bbox-border-color3=0;1;0;0.7')
                    lines.append('bbox-border-color0=0.3;0;0;1')# dark shade of red or choclate
                    # lines.append('bbox-border-color1=0;1;1;1')# red 
                    lines.append('bbox-border-color1=1;0.3;0.9;1')#pinkish-purple or magenta
                    lines.append('bbox-border-color2=0.545;0;1;1')#purple
                    lines.append('bbox-border-color3=1;0.659;0;1')#orange
                    # lines.append('bbox-border-color3=0;1;0;1')
                    lines.append('bbox-border-color4=0.561;0.737;0.561;1')#dark sea green 
                    lines.append('bbox-border-color5=0.502;0.502;0;1')#olive color
                    lines.append('bbox-border-color6=0.392;0.584;0.929;1')#corn flower blue
                    lines.append('bbox-border-color7=0.941;0.502;0.502;1')
                    lines.append('nvbuf-memory-type=0')
                    lines.append('interval=0')
                    lines.append('gie-unique-id=1')
                    modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                    lines.append('model-engine-file=../../models/yoloV8/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                    lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                elif line.strip() == '[primary-gie-ss]':
                    lines.append('[primary-gie-ss]')
                    if len(steamsuit_cameraid) !=0:
                        lines.append('enable=1')
                    else:
                        lines.append('enable=0')
                    lines.append('batch-size={0}'.format(str(1)))
                    lines.append('bbox-border-color0=0;1;1;0.7')
                    lines.append('bbox-border-color1=0;1;1;0.7')
                    lines.append('bbox-border-color2=0;1;1;0.7')
                    lines.append('bbox-border-color3=0;1;0;0.7')
                    lines.append('nvbuf-memory-type=0')
                    lines.append('interval=0')
                    lines.append('gie-unique-id=1')
                    lines.append( 'config-file = ../../models/config_infer_primary_tsk_ss.txt')
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                    
                elif line.strip() == '[secondary-gie0]':
                    lines.append('[secondary-gie0]')
                    lines.append('enable = 1')
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                    lines.append('gie-unique-id = 6')
                    lines.append('operate-on-gie-id = 1')
                    lines.append('operate-on-class-ids = 0;')
                    lines.append('batch-size = 1')
                    lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                    lines.append('bbox-border-color1 = 1;0;0;0.7')
                    # lines.append('gie-unique-id = 4')
                    # lines.append('operate-on-gie-id = 1')
                    # lines.append('operate-on-class-ids = 0;')
                    # lines.append('batch-size = 1')
                    # lines.append('bbox-border-color0 = 0;0;0;0.7')
                    # lines.append('bbox-border-color1 = 1;0;0;0.7')
                    if defaultsecondmodels == True :
                        lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                        lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                        secondaryconfig_file = []
                        secondaryconfig_file.append('[property]')
                        secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                        secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                        secondaryconfig_file.append('tlt-model-key=tlt_encode')
                        HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                        if os.path.exists(HelmetEngineFile):
                            # print("yolov3 EngineFIle exists.")
                            secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            # print("yolov3 EngineFIle does not exist.")
                            secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                        # secondaryconfig_file.append('tlt-encoded-model=./helmet_detector_v5/resnet18_helmet_detector_v5.etlt')
                        # secondaryconfig_file.append('labelfile-path=./helmet_detector_v5/labels.txt')
                        # secondaryconfig_file.append('model-engine-file=./helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                        secondaryconfig_file.append('infer-dims=3;320;320')
                        secondaryconfig_file.append('uff-input-blob-name=input_1')
                        secondaryconfig_file.append('batch-size=1')
                        secondaryconfig_file.append('process-mode=2')
                        secondaryconfig_file.append('model-color-format=0')
                        secondaryconfig_file.append('network-mode=2')
                        secondaryconfig_file.append('num-detected-classes=2')
                        secondaryconfig_file.append('interval=0')
                        secondaryconfig_file.append('gie-unique-id=2')
                        secondaryconfig_file.append('operate-on-gie-id=1')
                        secondaryconfig_file.append('operate-on-class-ids=0;')
                        secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                        secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                        secondaryconfig_file.append('network-type=0')
                        secondaryconfig_file.append('uff-input-order=0\n')
                        secondaryconfig_file.append('[class-attrs-0]')
                        secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                        secondaryconfig_file.append('group-threshold=1')
                        secondaryconfig_file.append('eps=0.4')
                        secondaryconfig_file.append('#minBoxes=3')
                        secondaryconfig_file.append('#detected-min-w=20')
                        secondaryconfig_file.append('#detected-min-h=20\n')
                        secondaryconfig_file.append('[class-attrs-1]')
                        secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                        secondaryconfig_file.append('group-threshold=1')
                        secondaryconfig_file.append('eps=0.4')
                        secondaryconfig_file.append('#minBoxes=3')
                        secondaryconfig_file.append('#detected-min-w=20')
                        secondaryconfig_file.append('#detected-min-h=20')
                        with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                            for O_O_O, item in enumerate(secondaryconfig_file):
                                f.write('%s\n' % item)
                    else:
                        if Hemetdetails is not None:
                            HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                            Hemeltversion= Hemetdetails['helmet']['version']
                            lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                            lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                            secondaryconfig_file = []
                            secondaryconfig_file.append('[property]')
                            secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                            secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                            secondaryconfig_file.append('tlt-model-key=tlt_encode')
                            HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                            if os.path.exists(HelmetEngineFile):
                                # print("yolov3 EngineFIle exists.")
                                secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            else:
                                # print("yolov3 EngineFIle does not exist.")
                                secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                            # secondaryconfig_file.append('tlt-encoded-model=./helmet_detector_v{0}/resnet18_helmet_detector_v5.etlt'.format(Hemeltversion))
                            # secondaryconfig_file.append('labelfile-path=./helmet_detector_v{0}/labels.txt'.format(Hemeltversion))
                            # secondaryconfig_file.append('model-engine-file=./helmet_detector_v{0}/resnet18_helmet_detector_v5.etlt_b1_gpu{1}_fp16.engine'.format(Hemeltversion,GPUSINDEX))
                            secondaryconfig_file.append('infer-dims=3;320;320')
                            secondaryconfig_file.append('uff-input-blob-name=input_1')
                            secondaryconfig_file.append('batch-size=1')
                            secondaryconfig_file.append('process-mode=2')
                            secondaryconfig_file.append('model-color-format=0')
                            secondaryconfig_file.append('network-mode=2')
                            secondaryconfig_file.append('num-detected-classes=2')
                            secondaryconfig_file.append('interval=0')
                            secondaryconfig_file.append('gie-unique-id=2')
                            secondaryconfig_file.append('operate-on-gie-id=1')
                            secondaryconfig_file.append('operate-on-class-ids=0;')
                            secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                            secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                            secondaryconfig_file.append('network-type=0')
                            secondaryconfig_file.append('uff-input-order=0\n')
                            secondaryconfig_file.append('[class-attrs-0]')
                            secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                            secondaryconfig_file.append('group-threshold=1')
                            secondaryconfig_file.append('eps=0.4')
                            secondaryconfig_file.append('#minBoxes=3')
                            secondaryconfig_file.append('#detected-min-w=20')
                            secondaryconfig_file.append('#detected-min-h=20\n')
                            secondaryconfig_file.append('[class-attrs-1]')
                            secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                            secondaryconfig_file.append('group-threshold=1')
                            secondaryconfig_file.append('eps=0.4')
                            secondaryconfig_file.append('#minBoxes=3')
                            secondaryconfig_file.append('#detected-min-w=20')
                            secondaryconfig_file.append('#detected-min-h=20')
                            with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                for O_O_O, item in enumerate(secondaryconfig_file):
                                    f.write('%s\n' % item)
                elif line.strip() == '[secondary-gie1]':
                    lines.append('[secondary-gie1]')
                    lines.append('enable = 1')
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                    lines.append('gie-unique-id = 7')
                    lines.append('operate-on-gie-id = 1')
                    lines.append('operate-on-class-ids = 0;')
                    lines.append('batch-size = 1')
                    lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                    lines.append('bbox-border-color1 = 1;0;0;0.7')
                    lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                    # lines.append('gie-unique-id = 5')
                    # lines.append('operate-on-gie-id = 1')
                    # lines.append('operate-on-class-ids = 0;')
                    # lines.append('batch-size = 1')
                    # lines.append('bbox-border-color0 = 1;0;1;0.7')
                    # lines.append('bbox-border-color1 = 1;0;0;0.7')
                    if defaultsecondmodels == True :
                        lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                        lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                        secondaryconfig_filevest = []
                        secondaryconfig_filevest.append('[property]')
                        secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                        secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                        secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                        VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                        if os.path.exists(VestEngineFile):
                            # print("yolov3 EngineFIle exists.")
                            secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            # print("yolov3 EngineFIle does not exist.")
                            secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            
                        # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                        # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                        # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                        secondaryconfig_filevest.append('infer-dims=3;320;320')
                        secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                        secondaryconfig_filevest.append('batch-size=1')
                        secondaryconfig_filevest.append('process-mode=2')
                        secondaryconfig_filevest.append('model-color-format=0')
                        secondaryconfig_filevest.append('network-mode=2')
                        secondaryconfig_filevest.append('num-detected-classes=3')
                        secondaryconfig_filevest.append('interval=0')
                        secondaryconfig_filevest.append('gie-unique-id=2')
                        secondaryconfig_filevest.append('operate-on-gie-id=1')
                        secondaryconfig_filevest.append('operate-on-class-ids=0;')
                        secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                        secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                        secondaryconfig_filevest.append('network-type=0')
                        secondaryconfig_filevest.append('uff-input-order=0\n')
                        secondaryconfig_filevest.append('[class-attrs-0]')
                        secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                        secondaryconfig_filevest.append('group-threshold=1')
                        secondaryconfig_filevest.append('eps=0.4')
                        secondaryconfig_filevest.append('#minBoxes=3')
                        secondaryconfig_filevest.append('#detected-min-w=20')
                        secondaryconfig_filevest.append('#detected-min-h=20\n')
                        secondaryconfig_filevest.append('[class-attrs-1]')
                        secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                        secondaryconfig_filevest.append('group-threshold=1')
                        secondaryconfig_filevest.append('eps=0.4')
                        secondaryconfig_filevest.append('#minBoxes=3')
                        secondaryconfig_filevest.append('#detected-min-w=20')
                        secondaryconfig_filevest.append('#detected-min-h=20')                        
                        secondaryconfig_filevest.append('[class-attrs-2]')
                        secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                        secondaryconfig_filevest.append('group-threshold=1')
                        secondaryconfig_filevest.append('eps=0.4')
                        secondaryconfig_filevest.append('#minBoxes=3')
                        secondaryconfig_filevest.append('#detected-min-w=20')
                        secondaryconfig_filevest.append('#detected-min-h=20')        
                        with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                            for O_O_O, item in enumerate(secondaryconfig_filevest):
                                f.write('%s\n' % item)

                    else:
                        if Vestdetails is not None:
                            Vestconfigfile = Vestdetails['vest']['modelpath']
                            Vestversion= Vestdetails['vest']['version']
                            lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                            lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                            secondaryconfig_filevest = []
                            secondaryconfig_filevest.append('[property]')
                            secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                            secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                            secondaryconfig_filevest.append('tlt-model-key=tlt_encode')

                            VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                            if os.path.exists(VestEngineFile):
                                # print("yolov3 EngineFIle exists.")
                                secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            else:
                                # print("yolov3 EngineFIle does not exist.")
                                secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v{0}/resnet18_vest_detector_v{1}.etlt'.format(Vestversion,Vestversion))
                            # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v{0}/labels.txt'.format(Vestversion))
                            # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v{0}/resnet18_vest_detector_v{1}.etlt_b1_gpu{2}_fp16.engine'.format(Vestversion,Vestversion,GPUSINDEX))
                            secondaryconfig_filevest.append('infer-dims=3;320;320')
                            secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                            secondaryconfig_filevest.append('batch-size=1')
                            secondaryconfig_filevest.append('process-mode=2')
                            secondaryconfig_filevest.append('model-color-format=0')
                            secondaryconfig_filevest.append('network-mode=2')
                            secondaryconfig_filevest.append('num-detected-classes=3')
                            secondaryconfig_filevest.append('interval=0')
                            secondaryconfig_filevest.append('gie-unique-id=2')
                            secondaryconfig_filevest.append('operate-on-gie-id=1')
                            secondaryconfig_filevest.append('operate-on-class-ids=0;')
                            secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                            secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                            secondaryconfig_filevest.append('network-type=0')
                            secondaryconfig_filevest.append('uff-input-order=0\n')
                            secondaryconfig_filevest.append('[class-attrs-0]')
                            secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                            secondaryconfig_filevest.append('group-threshold=1')
                            secondaryconfig_filevest.append('eps=0.4')
                            secondaryconfig_filevest.append('#minBoxes=3')
                            secondaryconfig_filevest.append('#detected-min-w=20')
                            secondaryconfig_filevest.append('#detected-min-h=20\n')
                            secondaryconfig_filevest.append('[class-attrs-1]')
                            secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                            secondaryconfig_filevest.append('group-threshold=1')
                            secondaryconfig_filevest.append('eps=0.4')
                            secondaryconfig_filevest.append('#minBoxes=3')
                            secondaryconfig_filevest.append('#detected-min-w=20')
                            secondaryconfig_filevest.append('#detected-min-h=20')
                            secondaryconfig_filevest.append('[class-attrs-2]')
                            secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                            secondaryconfig_filevest.append('group-threshold=1')
                            secondaryconfig_filevest.append('eps=0.4')
                            secondaryconfig_filevest.append('#minBoxes=3')
                            secondaryconfig_filevest.append('#detected-min-w=20')
                            secondaryconfig_filevest.append('#detected-min-h=20')
                            with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                for O_O_O, item in enumerate(secondaryconfig_filevest):
                                    f.write('%s\n' % item)
                elif line.strip() == '[secondary-gie2]':
                    lines.append('[secondary-gie2]')
                    if len(onlyCrashHelmet) !=0:
                        lines.append('enable = 1')
                    else:
                        lines.append('enable = 0')
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                    lines.append('gie-unique-id = 8')
                    lines.append('operate-on-gie-id = 1')
                    lines.append('operate-on-class-ids = 0;')
                    lines.append('batch-size = 1')
                    lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                    lines.append('bbox-border-color1 = 1;0;0;0.7')
                    # lines.append('bbox-border-color0 = 1;0;1;0.7')
                    # lines.append('bbox-border-color1 = 1;0;0;0.7')
                    CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(CrushHelmetEngine):
                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                    else:
                        anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                        secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                        if os.path.exists(anotherenginFilePath):
                            print('----------------------')
                            destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                            shutil.copy(anotherenginFilePath, destination)
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                        elif os.path.exists(secondenginFilePath):
                            destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                            shutil.copy(secondenginFilePath, destination)
                            if os.path.exists(CrushHelmetEngine):
                               lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                        else:
                            lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")



                    if 1:#defaultsecondmodels == True :
                        # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                        lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                        ScondaryCrushhelmet = []
                        ScondaryCrushhelmet.append('[property]')
                        ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                        ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                        ScondaryCrushhelmet.append('model-color-format=0')
                        # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                        CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                        if os.path.exists(CrushHelmet):
                            # print("yolov3 EngineFIle exists.")
                            ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                            ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                            ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                            # print("yolov3 EngineFIle does not exist.")
                            # ScondaryCrushhelmet.append('tlt-encoded-model={0}/models/yoloV8_crash_helmet/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                            # ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                            # #yoloV8_crash_helmet/engine/model_b4_gpu0_fp16.engine
                            # ScondaryCrushhelmet.append('model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                        # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                        # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                        ScondaryCrushhelmet.append('batch-size=1')
                        ScondaryCrushhelmet.append('network-mode=2')
                        ScondaryCrushhelmet.append('num-detected-classes=2')
                        ScondaryCrushhelmet.append('interval=0')
                        ScondaryCrushhelmet.append('gie-unique-id=1')
                        ScondaryCrushhelmet.append('process-mode=2')
                        ScondaryCrushhelmet.append('network-type=0')
                        ScondaryCrushhelmet.append('cluster-mode=2')
                        ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                        ScondaryCrushhelmet.append('operate-on-gie-id=1')
                        ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                        ScondaryCrushhelmet.append('symmetric-padding=1')
                        ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                        ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                        ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                        ScondaryCrushhelmet.append('[class-attrs-0]')
                        ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                        ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                        ScondaryCrushhelmet.append('topk=300\n')

                        ScondaryCrushhelmet.append('[class-attrs-1]')
                        ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                        ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                        ScondaryCrushhelmet.append('topk=300')     
                        with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                            for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                f.write('%s\n' % item)

                elif line.strip() == '[tracker]':
                    lines.append('[tracker]')
                    lines.append('enable=1')
                    lines.append('tracker-width=960')
                    lines.append('tracker-height=544')
                    if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                        lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                    else:
                        shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                        lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                    if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                        lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                    else:
                        shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                        lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                    lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                    lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                    lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                    lines.append('#enable-batch-process=0')
                    if display_tracker :
                        lines.append('display-tracking-id=1')
                    else:
                        lines.append('display-tracking-id=0')
                    lines.append('user-meta-pool-size=64')

                elif line.strip() == '[tests]':
                    lines.append('[tests]')

                elif line.strip() == '[docketrun-analytics]':
                    lines.append('[docketrun-analytics]')
                    lines.append('smart-record-stop-buffer = 2\n')

                elif line.strip() == '[docketrun-image]':
                    lines.append('[docketrun-image]')

                elif line.strip() == '[restricted-access]':
                    lines.append('[restricted-access]')
                    final_index = 0
                    final_roi_empty_ls = []
                    check_camera_id_for_RA = []
                    
                    string_test = '-1;'
                    if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                        check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                    final_roi_existed_cam_ids = roi_enable_cam_ids
                    for n in roi_enable_cam_ids:
                        text = str(n) + ';'
                        text = str(n) + ';'
                        if text not in final_roi_empty_ls:
                            final_roi_empty_ls.append(text)

                    for n in roi_enable_cam_ids:
                        text = str(n) + ';'
                        if text not in final_roi_empty_ls:
                            final_roi_empty_ls.append(text)
                    # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",len(roi_enable_cam_ids))
                    # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",roi_enable_cam_ids)
                    if len(roi_enable_cam_ids)== 0:
                        lines.append('enable = 0')

                    else:
                        lines.append('enable = 0')
                    lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                    lines.append('roi-overlay-enable = 1')
                    lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))

                elif line.strip() == '[ppe-type-1]':
                    # lines.append('[ppe-type-1]')
                    lines.append('[PPE]')
                    # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                    empty_ppe_ls = []
                    for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                        text = str(n) + ';'
                        empty_ppe_ls.append(text)
                    string2 = ''
                    if len(empty_ppe_ls) == 0:
                        # string2 = '-1;'
                        # lines.append('camera-ids = {0}'.format(string2))
                        lines.append('enable = 0')
                        lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                    else:
                        # string2 = ''
                        # lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                        lines.append('enable = 1')
                        lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))

                elif line.strip() == '[crowd-counting]':
                    lines.append('[crowd-counting]')
                    cr_final_index = 0
                    for Cherry, x in enumerate(response):
                        string2 = '-1;'
                        if len(x['cr_data']) != 0:
                            cr_final_index += 1

                    if cr_final_index == 0:
                        enable_val = 0
                        lines.append('enable = {0}'.format(enable_val))
                    else:
                        enable_val = 1
                        lines.append('enable = {0}'.format(enable_val))
                    lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                    lines.append("roi-overlay-enable=1")

                elif line.strip()=='[steam-suit]':
                    lines.append('[steam-suit]')
                    lines.append('camera-ids = -1;')
                    lines.append('data-save-interval = 1')  

                elif line.strip() == '[traffic-count]':
                    lines.append('[traffic-count]')
                    tc_final_index = 0
                    final_tc_empty_ls = []
                    for Cherry, x in enumerate(response):
                        string2 = '-1;'
                        if len(x['tc_data']) != 0:
                            final_tc_existed_cam_ids = []
                            for tc_val in x['tc_data']:
                                for tc_val___test in tc_val['label_name']:
                                    if tc_val___test not in tc_label_names:
                                        tc_label_names.append(tc_val___test)
                                if len(tc_val['traffic_count']) != 0:
                                    final_tc_existed_cam_ids.append(
                                        tc_final_index + 1)
                                    for n in final_tc_existed_cam_ids:
                                        text = str(n) + ';'
                                        final_tc_empty_ls.append(text)
                                    string2 = ''
                        tc_final_index += 1
                    if len(final_tc_empty_ls) == 0:
                        final_tc_empty_ls.append(string2)
                    # lines.append('camera-ids = {0}'.format(string2.join(final_tc_empty_ls)))
                    tc_empty_label_ls = []
                    for tc_label_name_test in tc_label_names:
                        text = str(tc_label_name_test) + ';'
                        tc_empty_label_ls.append(text)
                    test_string = ''
                    lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))

                elif line.strip() == '[traffic-jam]':
                    lines.append('[traffic-jam]')
                    if len(Traffic_JAM) !=0:
                        lines.append( 'enable = 1')
                    else:
                        lines.append( 'enable = 0')
                    lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                    lines.append('data-save-interval=10\n')
                elif line.strip() == '[traffic-counting]':
                    lines.append('[traffic-counting]')
                    lines.append( 'enable = 0')
                    lines.append('details=[]\n')

                else:
                    lines.append(line.strip())

        model_config_details ,secondarymodelconfigdetails= get_model_config_details()
        if model_config_details is not None:
            if model_config_details['modeltype'] == 'yolo3':
                classId = model_config_details['objectDetector_Yolo']['class_id']
                modelconfigfile = model_config_details['objectDetector_Yolo']['modelpath']
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('batch-size=1')
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('custom-network-config={0}/models/objectDetector_Yolo/yolov3.cfg'.format(get_current_dir_and_goto_parent_dir()))
                enginFilePath = '{2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                if os.path.exists(enginFilePath):
                    # print("yolov3 EngineFIle exists.")
                    modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                    modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                else:
                    # print("yolov3 EngineFIle does not exist.")
                    anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(anotherenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/objectDetector_Yolo/engine/'.format(get_current_dir_and_goto_parent_dir())
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
                        destination= '{0}/models/objectDetector_Yolo/engine/'.format(get_current_dir_and_goto_parent_dir())
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
                    # modelconfigwrite.append('model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                    # modelconfigwrite.append('model-engine-file={2}/models/objectDetector_Yolo/engine/model_b{0}_gpu{1}_int8.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('labelfile-path={0}/models/objectDetector_Yolo/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('int8-calib-file={0}/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('network-mode=1')
                modelconfigwrite.append('num-detected-classes=80')
                modelconfigwrite.append('gie-unique-id=1')
                modelconfigwrite.append('network-type=0')
                modelconfigwrite.append('is-classifier=0')
                modelconfigwrite.append('cluster-mode=2')
                modelconfigwrite.append('maintain-aspect-ratio=1')
                modelconfigwrite.append( 'parse-bbox-func-name=NvDsInferParseCustomYoloV3')
                modelconfigwrite.append('custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
                modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                modelconfigwrite.append('[class-attrs-all]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=1.0')
                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold={0}'.format(person_threshold))
                modelconfigwrite.append('[class-attrs-1]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=0.4')
                modelconfigwrite.append('[class-attrs-2]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=0.4')
                modelconfigwrite.append('[class-attrs-3]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=0.4')
                modelconfigwrite.append('[class-attrs-5]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=0.4')
                modelconfigwrite.append('[class-attrs-7]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=0.4')

            elif  model_config_details['modeltype'] == 'yolo8':
                classId = model_config_details['yoloV8']['class_id']
                modelconfigfile = model_config_details['yoloV8']['modelpath']
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
                    # print("yolov8 EngineFIle does not exist.")
                    anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
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
                    # modelconfigwrite.append('model-file={0}/models/yoloV8/yolov8x.wts'.format(get_current_dir_and_goto_parent_dir()))
                    # modelconfigwrite.append('model-engine-file={2}/models/yoloV8/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                
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
                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                modelconfigwrite.append('topk=300')
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

            elif model_config_details['modeltype'] == 'trafficcam':
                classId = model_config_details['trafficcamnet']['class_id']
                modelconfigfile = model_config_details['trafficcamnet']['modelpath']
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('batch-size=1')
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('tlt-model-key=tlt_encode')
                modelconfigwrite.append('tlt-encoded-model=./trafficcamnet/resnet18_trafficcamnet_pruned.etlt')
                modelconfigwrite.append('labelfile-path=./trafficcamnet/labels_trafficnet.txt')
                modelconfigwrite.append('int8-calib-file=./trafficcamnet/trafficnet_int8.bin')
                modelconfigwrite.append('model-engine-file=./trafficcamnet/engine/resnet18_trafficcamnet_pruned.etlt_b4_gpu{0}_int8.engine'.format(GPUSINDEX))
                modelconfigwrite.append('input-dims=3;544;960;0')
                modelconfigwrite.append('uff-input-blob-name=input_1')
                modelconfigwrite.append('batch-size=1')
                modelconfigwrite.append('process-mode=1')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('network-mode=1')
                modelconfigwrite.append('num-detected-classes=4')
                modelconfigwrite.append('interval=0')
                modelconfigwrite.append('gie-unique-id=1')
                modelconfigwrite.append('output-blob-names=output_bbox/BiasAdd;output_cov/Sigmoid')
                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('pre-cluster-threshold=1.0')
                modelconfigwrite.append('group-threshold=1')
                modelconfigwrite.append('eps=0.2\n')
                modelconfigwrite.append('[class-attrs-1]')
                modelconfigwrite.append('pre-cluster-threshold=1.0')
                modelconfigwrite.append('group-threshold=1')
                modelconfigwrite.append('eps=0.2\n')
                modelconfigwrite.append('[class-attrs-2]')
                modelconfigwrite.append('pre-cluster-threshold=0.14')
                modelconfigwrite.append('group-threshold=1')
                modelconfigwrite.append('eps=0.2')
                modelconfigwrite.append('detected-min-h=70\n')
                modelconfigwrite.append('[class-attrs-3]')
                modelconfigwrite.append('pre-cluster-threshold=1.0')
                modelconfigwrite.append('group-threshold=1')
                modelconfigwrite.append('eps=0.2\n')
            elif model_config_details['modeltype'] == 'people':
                classId = model_config_details['peoplenet']['class_id']
                modelconfigfile = model_config_details['peoplenet']['modelpath']
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('batch-size=1')
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('custom-network-config={0}/models/objectDetector_Yolo/yolov3.cfg'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('#model-file={0}/models/objectDetector_Yolo/yolov3.weights'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('#model-engine-file={1}/models/objectDetector_Yolo/engine/model_b8_gpu{0}_int8.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('labelfile-path={0}/models/objectDetector_Yolo/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('int8-calib-file={0}/models/objectDetector_Yolo/yolov3-calibration.table.trt7.0'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('network-mode=1')
                modelconfigwrite.append('num-detected-classes=80')
                modelconfigwrite.append('gie-unique-id=1')
                modelconfigwrite.append('network-type=0')
                modelconfigwrite.append('is-classifier=0')
                modelconfigwrite.append('cluster-mode=2')
                modelconfigwrite.append('maintain-aspect-ratio=1')
                modelconfigwrite.append('parse-bbox-func-name=NvDsInferParseCustomYoloV3')
                modelconfigwrite.append('custom-lib-path=nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so')
                modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                modelconfigwrite.append('[class-attrs-all]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=1.0')
                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=0.7')
                modelconfigwrite.append('[class-attrs-7]')
                modelconfigwrite.append('nms-iou-threshold=0.3')
                modelconfigwrite.append('threshold=1.0')            
        modelconfigfile  = os.path.splitext(modelconfigfile)[0]    
        with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
            for O_O_O, item in enumerate(modelconfigwrite):
                f.write('%s\n' % item)

        with open(config_file, 'w') as f:
            for O_O_O, item in enumerate(lines):
                f.write('%s\n' % item)

                
    return allWrittenSourceCAmIds





def Loaddocketrunmodel(response):
    valid_camera_list=[]
    roi_required_keys=['roi_name','traffic_jam_percentage','selected_objects','bb_box','roi_id','min_time']
    TitledDisplayEnable = True
    defaultsecondmodels = True
    Hemetdetails = {}
    Vestdetails = {}
    steamsuitaddedstatus = False
    GPUSINDEX = 0  
    allWrittenSourceCAmIds =[]
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
    classId = '0'
    print("Genral_configurations===",Genral_configurations)
    batch_pushouttime = 40000
    drop_frame_interval=1
    ticket_reset_time =10
    gridview_true = True
    numberofsources_= 4
    rtsp_reconnect_interval = 3
    displayfontsize = 12
    display_tracker =True
    if ('drop_frame_interval' in Genral_configurations and Genral_configurations['drop_frame_interval'] is not None) and ('camera_fps' in Genral_configurations and  Genral_configurations['camera_fps'] is not None) :
        camera_fps = Genral_configurations['camera_fps']
        drop_frame_interval = Genral_configurations['drop_frame_interval']
        Newpushouttime = math.ceil(int(camera_fps)/int(drop_frame_interval))
        batch_pushouttime= math.ceil(1000000/Newpushouttime)
    
    if ('rtsp_reconnect_interval' in Genral_configurations and Genral_configurations['rtsp_reconnect_interval'] is not None):
        rtsp_reconnect_interval = Genral_configurations['rtsp_reconnect_interval'] 
    

    if ('grid_view' in Genral_configurations and Genral_configurations['grid_view'] is not None):
        gridview_true = Genral_configurations['grid_view'] 
    if ('grid_size' in Genral_configurations and Genral_configurations['grid_size'] is not None):
        numberofsources_ = int(Genral_configurations['grid_size'])


    if ('ticket_reset_time' in Genral_configurations and Genral_configurations['ticket_reset_time'] is not None):
        ticket_reset_time = int(Genral_configurations['ticket_reset_time'])
    
    if 'display_font_size' in Genral_configurations :
        displayfontsize = Genral_configurations['display_font_size']

    if 'display_tracker' in Genral_configurations :
        display_tracker = Genral_configurations['display_tracker']
    
    print("number of sources-- fetched----222 --------------0000000000000000000000000",len(response))
    Total_source_count = len(response)
    GPU_data = mongo.db.gpu_configurations.find_one({})
    # new_response = split_list(response,numberofsources_)
    camera_id = 1 
    NewcameraID = 1
    modelconfigfile = '/DI_model_V1/config_infer_primary_DI_s_V1.txt'
    modelconfigwrite = []
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'phase_one_sample_config.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/docketrun_app'+'/configs'
    DIMODEL = get_current_dir_and_goto_parent_dir() + '/models/DI_model_V1'
    traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)
    if not os.path.exists(traffic_config_path):
        os.makedirs(traffic_config_path)
    if not os.path.exists(DIMODEL):
        os.makedirs(DIMODEL)           
    remove_text_files(deepstream_config_path)  
    modelthreshold = getthreshholdmodelconfig_details()
    person_threshold = '0.7'
    helmet_threshold = '0.5'
    vest_threshold = '0.5'
    CrashHelment_threshold = '0.3'
    Bicycle_threshold= '0.3'
    Motorbike_threshold ='0.3'
    car_threshold = '0.3'
    bus_threshold = '0.3'
    truck_threshold = '0.3'
    if modelthreshold is not None:
        if len(modelthreshold['threshold']) !=0:
            for new,classname in enumerate(modelthreshold['threshold']):
                if classname['class']=='person':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            person_threshold = int(classname['value'])/100
                            if person_threshold==1:
                                person_threshold ='0.9'
                        else:
                            person_threshold = '0.1'           
                elif  classname['class']=='helmet':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            helmet_threshold =  int(classname['value'])/100
                            if helmet_threshold==1:
                                helmet_threshold ='0.9'
                        else:
                            helmet_threshold ='0.1' 
                elif  classname['class']=='vest':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            vest_threshold = int(classname['value'])/100
                            if vest_threshold==1:
                                vest_threshold ='0.9'
                        else:
                            vest_threshold ='0.1'
                elif  classname['class']=='crash_helmet':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            CrashHelment_threshold = int(classname['value'])/100
                            if CrashHelment_threshold==1:
                                CrashHelment_threshold ='0.9'
                        else:
                            CrashHelment_threshold ='0.1'
                elif  classname['class']=='bicycle':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            Bicycle_threshold = int(classname['value'])/100
                            if Bicycle_threshold==1:
                                Bicycle_threshold ='0.9'
                        else:
                            Bicycle_threshold ='0.1'
                elif  classname['class']=='motorbike':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            Motorbike_threshold = int(classname['value'])/100
                            if Motorbike_threshold==1:
                                Motorbike_threshold ='0.9'
                        else:
                            Motorbike_threshold ='0.1'
                elif  classname['class']=='car':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            car_threshold = int(classname['value'])/100
                            if car_threshold==1:
                                car_threshold ='0.9'
                        else:
                            car_threshold ='0.1'

                elif  classname['class']=='bus':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            bus_threshold = int(classname['value'])/100
                            if bus_threshold==1:
                                bus_threshold ='0.9'
                        else:
                            bus_threshold ='0.1'
                elif  classname['class']=='truck':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            truck_threshold = int(classname['value'])/100
                            if truck_threshold==1:
                                truck_threshold ='0.9'
                        else:
                            truck_threshold ='0.1'
    model_config_details,secondarymodelconfigdetails = get_model_config_details()
    if type(secondarymodelconfigdetails)== list  and len(secondarymodelconfigdetails)!=0 :
        defaultsecondmodels = False
        for indexmo, Modedetails in enumerate(secondarymodelconfigdetails):
            print("indexmo===",indexmo,Modedetails)
            for MAINKey , Values  in Modedetails.items():
                if "helmet" in MAINKey:
                    Hemetdetails= Modedetails
                if "vest" in MAINKey:
                    Vestdetails= Modedetails
    steamsuitcameradetails = createSTEAMSUITconfig()
    steamsuitcameradetails =[]
    if  len(response)!=0 and  len(steamsuitcameradetails) !=0:#len(response)!=0 and  len(steamsuitcameradetails)
        if GPU_data is not None:
            directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app', 'configs')
            
            txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
            print('-----txt_files---------------1.0.1------',txt_files)
            if txt_files:
                try:
                    for txt_file in txt_files:
                        os.remove(os.path.join(directory_path, txt_file))
                    print("Text files deleted successfully.---1.9.0----")
                except Exception as e:
                    print(f"Error deleting text files:---1.9.0---- {e}")
            else:
                print("No text files found in the directory.---1.9.0----")
            NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
            # print("=====NEwcount====",NEwcount)
            new_response=GPUSsplit_list(response,GPU_data['system_gpus'])
            for config_index, writingresponse in enumerate(new_response):  
                if GPU_data['system_gpus']==1 :
                    GPUSINDEX = GPUSINDEX
                elif config_index ==0  :
                    GPUSINDEX = config_index
                elif camera_id >= NEwcount:
                    GPUSINDEX= GPUSINDEX+1 
                else:   
                    GPUSINDEX= GPUSINDEX
                # GPUSINDEX =1
                config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
                crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
                config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
                hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
                PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))
                parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
                lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
                config_tjm_lines=[]
                # roi_objects=set()
                roi_enable_cam_ids = []
                ppe_enable_cam_ids = []
                traffic_count_enabledcameraids=[]
                cr_enable_cam_ids = []
                tc_label_names = []
                normal_config_file = 0
                final_roi_existed_cam_ids = []
                final_truck_cam_ids = []
                hooter_line = []
                crowd_line = []  
                PPELINE = [] 
                onlyCrashHelmet =[]     
                PPEFINALCAMERAIDS =[]
                traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
                steamsuit_cameraid =[]
                # print("length == === ", len(writingresponse))
                Steamsuitdata = steamsuitcameradetails
                lines.append("[roi-filtering-stream-0]")
                lines.append("enable=0")
                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                lines.append("inverse-roi=0")
                lines.append("class-id= 0;\n")
                
                crowd_line.append("[crdcnt0]")
                crowd_line.append("enable=0")
                crowd_line.append("process-on-full-frame=1")
                crowd_line.append("operate-on-label=person;")
                crowd_line.append("max-count=1;")
                crowd_line.append("min-count=0;")
                crowd_line.append("data-save-time-in-sec=3\n")
                hooter_line.append("[RA0]")
                hooter_line.append("enable = 0")
                hooter_line.append("operate-on-label = person;")
                hooter_line.append("hooter-enable = 0")
                hooter_line.append("hooter-ip = none")
                hooter_line.append('hooter-type = 0;')
                hooter_line.append("hooter-stop-buffer-time = 3")
                hooter_line.append("data-save-time-in-sec = 3\n")
                for index, x in enumerate(writingresponse):
                    x['cameraid'] = NewcameraID
                    if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
                        if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("***************111111************")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("TC-CR_PPE===2")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:    
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)

                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("TC-CR_RA===3")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("cr-ra_PPE===5")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)

                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("RA-TC_PPE===handled")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("cr-ra===6")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                                        
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("ra_TC===7")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID) 
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("ra_PPE===8")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)   
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("CR_TC===9")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("PPE_TC===10")
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)   
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)    
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("PPE_CR===11")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)  
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("CR===12")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                                        
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("RA===13")    
                            roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("TC===14") 
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("PPE===14") 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        
                        width_ratio=960/960
                        height_ratio= 544/544
                        if 'trafficjam_data' in x :
                            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----1-------')
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
                                                # print('str(FinalTime)-------type---4------------',type(FinalTime))
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
                                                # print('str(FinalTime)-------type---3------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'

                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                else:
                                    print()   
                        if '[crdcnt{}]'.format(index) not in crowd_line:
                            # print("-----")
                            crowd_line.append('[crdcnt{0}]'.format(index))
                            crowd_line.append("enable=0")
                            crowd_line.append("process-on-full-frame=1")
                            crowd_line.append("operate-on-label=person;")
                            crowd_line.append("max-count=1;")
                            crowd_line.append("min-count=0;")
                            crowd_line.append("data-save-time-in-sec=3\n")                            
                        if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                            lines.append('[roi-filtering-stream-{0}]'.format(index))
                            if 'trafficjam_data' in x :
                                if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----00-0-------')
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
                                                # print('str(FinalTime)-------type---1------------',type(FinalTime))
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

                                                # print('str(FinalTime)-------type---2------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                else:
                                    lines.append("enable=0")
                                    lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            else:
                                lines.append("enable=0")
                                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            lines.append("inverse-roi=0")
                            # lines.append("class-id= 0;\n")
                            
                        if '[RA{}]'.format(index) not in hooter_line:
                            # print("-----")
                            hooter_line.append('[RA{0}]'.format(index))
                            hooter_line.append("enable = 0")
                            hooter_line.append("operate-on-label = person;")
                            hooter_line.append("hooter-enable = 0")
                            hooter_line.append("hooter-ip = none")
                            hooter_line.append('hooter-type = 0;')
                            hooter_line.append('hooter-shoutdown-time = 10')
                            hooter_line.append("hooter-stop-buffer-time = 3")
                            hooter_line.append("data-save-time-in-sec = 3\n")

                        if '[PPE{}]'.format(index) not in PPELINE:
                            # print("-----")
                            PPELINE.append('[PPE{0}]'.format(index))
                            PPELINE.append("enable = 0")
                            PPELINE.append("hooter-enable = 0")
                            PPELINE.append("hooter-ip = none")
                            PPELINE.append('hooter-type = 0;')
                            PPELINE.append('hooter-shoutdown-time = 10')
                            PPELINE.append("hooter-stop-buffer-time = 3")
                            PPELINE.append('analytics-details =[{"analytics_type":0, "operate_on": "null;"},{"analytics_type":1, "operate_on": "null;"}]')
                            PPELINE.append("data-save-time-in-sec = 3\n")
                        
                        NewcameraID+=1
                total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids))
                # print("roi_enable cam ids =====", roi_enable_cam_ids)
                # print("ppeppe_333enable_cam_ids",ppe_enable_cam_ids)
                # print("=================total_stream_for_stremux_union===============",total_stream_for_stremux_union)
                with open(config_analytics_file, 'w') as f:
                    for item in lines:
                        f.write('%s\n' % item)

                with open(hooter_config_file_path, 'w') as hooter_file:
                    for jim in hooter_line:
                        hooter_file.write('%s\n' % jim)

                with open(PPE_config_file_path, 'w') as PPE_file:
                    for jim in PPELINE:
                        PPE_file.write('%s\n' % jim)

                with open(crowd_config_file, 'w') as crowd_file:
                    for O_O_O, item in enumerate(crowd_line):
                        crowd_file.write('%s\n' % item)
                # print('----------------------len---------',len(config_tjm_lines))
                with open(parking_roi_config_file, 'w') as file:
                    write_array_to_file(file,config_tjm_lines)
                    file.close()
                lines = []
                final_both_roi_cam_ids = []
                with open(sample_config_file) as file:
                    for write_config, line in enumerate(file):
                        if line.strip() == '[application]':
                            lines.append('[application]')
                            lines.append('enable-perf-measurement=1')
                            lines.append('perf-measurement-interval-sec=1')

                        elif line.strip() == '[tiled-display]':
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                            total_stream_for_stremux_union = finaL_RA_PPE
                            num = math.sqrt(int(len(finaL_RA_PPE)))
                            rows,columns= get_layout(len(total_stream_for_stremux_union))
                            lines.append('[tiled-display]')
                            if execute_nvidia_smi(GPUSINDEX):
                                lines.append('enable=1')
                            elif TitledDisplayEnable:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('rows={0}'.format(str(rows)))
                            lines.append('columns={0}'.format(str(columns)))
                            lines.append('width=960')
                            lines.append('height=544')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('nvbuf-memory-type=0')

                        elif line.strip() == '[sources]':    
                            # print("newlength===", len(writingresponse))
                            steamsuitaddedstatus = False
                            for n, x in enumerate(writingresponse):
                                cam_id = '{0}'.format(int(n))
                                if camera_id in roi_enable_cam_ids:
                                    roi_enable_cam_ids_exist = 1
                                if camera_id in ppe_enable_cam_ids:
                                    ppe_enable_cam_ids_exist = 1
                                if camera_id in cr_enable_cam_ids:
                                    newcrowdcount = 1
                                # print("newcrowdcountnewcrowdcountnewcrowdcount===newcrowdcount> 0 ",newcrowdcount)
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')

                                # print("Steamsui44---4tda----ta===55544=",Steamsuitdata)
                                if len(Steamsuitdata) !=0 and steamsuitaddedstatus == False:
                                    uri = Steamsuitdata[0]['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  55544 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(Steamsuitdata[0]['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1    
                                    steamsuit_cameraid.append(camera_id)                        
                                    camera_id += 1
                                    steamsuitaddedstatus = True
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    # print("normal_config_file += 1 ------------------------",normal_config_file  )
                                if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  1222222222222222222222222222222222222222222 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0        
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ):
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) += 333 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec=2")
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                    
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  ^^^^^^^^^^^^^^^^^^^122334 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif roi_enable_cam_ids_exist > 0:
                                    print("normal_config_file += 5555522 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif ppe_enable_cam_ids_exist > 0:
                                    print("normal_config_file += 666666666666666 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  #####################11122 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                
                                elif len(traffic_count_enabledcameraids)>0:
                                    print("normal_config_file += 777777777777777777 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdtraffic_count_enabledcameraidsfkajsdkfkasdjk=============", traffic_count_enabledcameraids)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                    
                                elif newcrowdcount >0:
                                    print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                            
                        elif line.strip() == '[sink0]':
                            lines.append('[sink0]')
                            lines.append('enable=1')
                            if gridview_true is True:
                                lines.append('type=2')
                            else:
                                lines.append('type=1')
                            #lines.append('type=2')
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
                            lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            if batch_pushouttime == 40000:
                                lines.append('batched-push-timeout=40000')
                            else:
                                lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            lines.append('width=1920')
                            lines.append('height=1080')
                            lines.append('enable-padding=0')
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[primary-gie]':
                            lines.append('[primary-gie]')
                            lines.append('enable=1')
                            lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            # lines.append('bbox-border-color0=0;1;0;1.0')
                            # lines.append('bbox-border-color1=0;1;1;0.7')
                            # lines.append('bbox-border-color2=0;1;0;0.7')
                            # lines.append('bbox-border-color3=0;1;0;0.7')
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
                            modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                            lines.append('model-engine-file=../../models/DI_model_V1/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                            lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                        elif line.strip() == '[primary-gie-ss]':
                            lines.append('[primary-gie-ss]')
                            if len(steamsuit_cameraid) !=0:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('batch-size={0}'.format(str(1)))
                            lines.append('bbox-border-color0=0;1;1;0.7')
                            lines.append('bbox-border-color1=0;1;1;0.7')
                            lines.append('bbox-border-color2=0;1;1;0.7')
                            lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            lines.append('config-file = ../../models/config_infer_primary_tsk_ss.txt')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            
                            
                        elif line.strip() == '[secondary-gie0]':
                            lines.append('[secondary-gie0]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 6')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('gie-unique-id = 4')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 0;0;0;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                                secondaryconfig_file = []                                
                                secondaryconfig_file.append('[property]')
                                secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(HelmetEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                
                                secondaryconfig_file.append('infer-dims=3;320;320')
                                secondaryconfig_file.append('uff-input-blob-name=input_1')
                                secondaryconfig_file.append('batch-size=1')
                                secondaryconfig_file.append('process-mode=2')
                                secondaryconfig_file.append('model-color-format=0')
                                secondaryconfig_file.append('network-mode=2')
                                secondaryconfig_file.append('num-detected-classes=2')
                                secondaryconfig_file.append('interval=0')
                                secondaryconfig_file.append('gie-unique-id=2')
                                secondaryconfig_file.append('operate-on-gie-id=1')
                                secondaryconfig_file.append('operate-on-class-ids=0;')
                                secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_file.append('network-type=0')
                                secondaryconfig_file.append('uff-input-order=0\n')
                                secondaryconfig_file.append('[class-attrs-0]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20\n')
                                secondaryconfig_file.append('[class-attrs-1]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20')
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_file):
                                        f.write('%s\n' % item)
                            else:
                                if Hemetdetails is not None:
                                    HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                                    Hemeltversion= Hemetdetails['helmet']['version']
                                    lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                    lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                                    secondaryconfig_file = []                                    
                                    secondaryconfig_file.append('[property]')
                                    secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                    HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(HelmetEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('infer-dims=3;320;320')
                                    secondaryconfig_file.append('uff-input-blob-name=input_1')
                                    secondaryconfig_file.append('batch-size=1')
                                    secondaryconfig_file.append('process-mode=2')
                                    secondaryconfig_file.append('model-color-format=0')
                                    secondaryconfig_file.append('network-mode=2')
                                    secondaryconfig_file.append('num-detected-classes=2')
                                    secondaryconfig_file.append('interval=0')
                                    secondaryconfig_file.append('gie-unique-id=2')
                                    secondaryconfig_file.append('operate-on-gie-id=1')
                                    secondaryconfig_file.append('operate-on-class-ids=0;')
                                    secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_file.append('network-type=0')
                                    secondaryconfig_file.append('uff-input-order=0\n')
                                    secondaryconfig_file.append('[class-attrs-0]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20\n')
                                    secondaryconfig_file.append('[class-attrs-1]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_file):
                                            f.write('%s\n' % item)
                        elif line.strip() == '[secondary-gie1]':
                            lines.append('[secondary-gie1]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 7')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                            if defaultsecondmodels == True :
                                lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                                secondaryconfig_filevest = []
                                secondaryconfig_filevest.append('[property]')
                                secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_filevest.append('tlt-model-key=tlt_encode')

                                VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(VestEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                
                                secondaryconfig_filevest.append('infer-dims=3;320;320')
                                secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                secondaryconfig_filevest.append('batch-size=1')
                                secondaryconfig_filevest.append('process-mode=2')
                                secondaryconfig_filevest.append('model-color-format=0')
                                secondaryconfig_filevest.append('network-mode=2')
                                secondaryconfig_filevest.append('num-detected-classes=3')
                                secondaryconfig_filevest.append('interval=0')
                                secondaryconfig_filevest.append('gie-unique-id=2')
                                secondaryconfig_filevest.append('operate-on-gie-id=1')
                                secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_filevest.append('network-type=0')
                                secondaryconfig_filevest.append('uff-input-order=0\n')
                                secondaryconfig_filevest.append('[class-attrs-0]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20\n')
                                secondaryconfig_filevest.append('[class-attrs-1]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')                                
                                secondaryconfig_filevest.append('[class-attrs-2]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')      
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_filevest):
                                        f.write('%s\n' % item)

                            else:
                                if Vestdetails is not None:
                                    Vestconfigfile = Vestdetails['vest']['modelpath']
                                    Vestversion= Vestdetails['vest']['version']
                                    lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                    lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                                    secondaryconfig_filevest = []
                                    secondaryconfig_filevest.append('[property]')
                                    secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                    VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(VestEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))

                                    secondaryconfig_filevest.append('infer-dims=3;320;320')
                                    secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                    secondaryconfig_filevest.append('batch-size=1')
                                    secondaryconfig_filevest.append('process-mode=2')
                                    secondaryconfig_filevest.append('model-color-format=0')
                                    secondaryconfig_filevest.append('network-mode=2')
                                    secondaryconfig_filevest.append('num-detected-classes=3')
                                    secondaryconfig_filevest.append('interval=0')
                                    secondaryconfig_filevest.append('gie-unique-id=2')
                                    secondaryconfig_filevest.append('operate-on-gie-id=1')
                                    secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                    secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_filevest.append('network-type=0')
                                    secondaryconfig_filevest.append('uff-input-order=0\n')
                                    secondaryconfig_filevest.append('[class-attrs-0]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20\n')
                                    secondaryconfig_filevest.append('[class-attrs-1]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')                                    
                                    secondaryconfig_filevest.append('[class-attrs-2]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_filevest):
                                            f.write('%s\n' % item)

                        elif line.strip() == '[secondary-gie2]':
                            lines.append('[secondary-gie2]')
                            if len(onlyCrashHelmet) !=0:
                                lines.append('enable = 1')
                            else:
                                lines.append('enable = 0')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 8')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                if os.path.exists(anotherenginFilePath):
                                    print('----------------------')
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(anotherenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                elif os.path.exists(secondenginFilePath):
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(secondenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                else:
                                    lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")



                            if 1:#defaultsecondmodels == True :
                                # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/crash_helmet_nano_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                                ScondaryCrushhelmet = []
                                ScondaryCrushhelmet.append('[property]')
                                ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                                ScondaryCrushhelmet.append('model-color-format=0')
                                # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                                CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(CrushHelmet):
                                    # print("yolov3 EngineFIle exists.")
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                ScondaryCrushhelmet.append('batch-size=1')
                                ScondaryCrushhelmet.append('network-mode=2')
                                ScondaryCrushhelmet.append('num-detected-classes=2')
                                ScondaryCrushhelmet.append('interval=0')
                                ScondaryCrushhelmet.append('gie-unique-id=1')
                                ScondaryCrushhelmet.append('process-mode=2')
                                ScondaryCrushhelmet.append('network-type=0')
                                ScondaryCrushhelmet.append('cluster-mode=2')
                                ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                                ScondaryCrushhelmet.append('operate-on-gie-id=1')
                                ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                                ScondaryCrushhelmet.append('symmetric-padding=1')
                                ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                                ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                                ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                                ScondaryCrushhelmet.append('[class-attrs-0]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300\n')

                                ScondaryCrushhelmet.append('[class-attrs-1]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300')     
                                with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                                    for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                        f.write('%s\n' % item)
                        elif line.strip() == '[tracker]':
                            lines.append('[tracker]')
                            lines.append('enable=1')
                            lines.append('tracker-width=960')
                            lines.append('tracker-height=554')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('#enable-batch-process=0')
                            if display_tracker :
                                lines.append('display-tracking-id=1')
                            else:
                                lines.append('display-tracking-id=0')
                            lines.append('user-meta-pool-size=64')
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
                        elif line.strip()== '[application-config]':
                            lines.append('[application-config]')     
                        elif line.strip() == '[restricted-access]':
                            lines.append('[restricted-access]')
                            final_index = 0
                            final_roi_empty_ls = []
                            check_camera_id_for_RA = []
                            for Cherry, x in enumerate(writingresponse):
                                string2 = '-1;'
                                if len(x['roi_data']) != 0:
                                    for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                        label_name = roi_value['label_name']
                                        if ('person' in label_name and 'truck' in label_name):
                                            final_both_roi_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'truck' in label_name:
                                            final_truck_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' in label_name:
                                            final_roi_existed_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' not in label_name and 'truck' not in label_name:
                                            pass
                                        else:
                                            pass
                                final_index += 1
                            string_test = '-1;'
                            if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                                check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                            final_roi_existed_cam_ids = roi_enable_cam_ids
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            
                            # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",len(roi_enable_cam_ids))
                            # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",roi_enable_cam_ids)
                            if len(roi_enable_cam_ids)== 0:
                                lines.append('enable = 0')

                            else:
                                lines.append('enable = 1')
                            lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                            lines.append('roi-overlay-enable = 1')
                            lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))

                        elif line.strip() == '[ppe-type-1]':
                            lines.append('[PPE]')
                            # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                            empty_ppe_ls = []
                            for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                                text = str(n) + ';'
                                empty_ppe_ls.append(text)
                            string2 = ''
                            if len(empty_ppe_ls) == 0:
                                # string2 = '-1;'
                                # lines.append('camera-ids = {0}'.format(string2))
                                lines.append('enable = 0')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            else:
                                # string2 = ''
                                # lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                                lines.append('enable = 1')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))

                        elif line.strip() == '[crowd-counting]':
                            lines.append('[crowd-counting]')
                            cr_final_index = 0
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['cr_data']) != 0:
                                    cr_final_index += 1

                            if cr_final_index == 0:
                                enable_val = 0
                                lines.append('enable = {0}'.format(enable_val))
                            else:
                                enable_val = 1
                                lines.append('enable = {0}'.format(enable_val))
                            lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                            lines.append("roi-overlay-enable=1")

                        elif line.strip()=='[steam-suit]':
                            lines.append('[steam-suit]')
                            lines.append('camera-ids = -1;')
                            lines.append('data-save-interval = 1')  

                        elif line.strip() == '[traffic-count]':
                            lines.append('[traffic-count]')
                            tc_final_index = 0
                            final_tc_empty_ls = []
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['tc_data']) != 0:
                                    final_tc_existed_cam_ids = []
                                    for tc_val in x['tc_data']:
                                        for tc_val___test in tc_val['label_name']:
                                            if tc_val___test not in tc_label_names:
                                                tc_label_names.append(tc_val___test)
                                        if len(tc_val['traffic_count']) != 0:
                                            final_tc_existed_cam_ids.append(
                                                tc_final_index + 1)
                                            for n in final_tc_existed_cam_ids:
                                                text = str(n) + ';'
                                                final_tc_empty_ls.append(text)
                                            string2 = ''
                                tc_final_index += 1
                            if len(final_tc_empty_ls) == 0:
                                final_tc_empty_ls.append(string2)
                            tc_empty_label_ls = []
                            for tc_label_name_test in tc_label_names:
                                text = str(tc_label_name_test) + ';'
                                tc_empty_label_ls.append(text)
                            test_string = ''
                            lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))
                        
                        elif line.strip() == '[traffic-jam]':
                            lines.append('[traffic-jam]')
                            if len(Traffic_JAM) !=0:
                                lines.append( 'enable = 1')
                            else:
                                lines.append( 'enable = 0')
                            lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                            lines.append('data-save-interval=10\n')

                        elif line.strip() == '[traffic-counting]':
                            lines.append('[traffic-counting]')
                            lines.append( 'enable = 0')
                            lines.append('details=[]\n')
                        
                        else:
                            lines.append(line.strip())
                    
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('custom-network-config={0}/models/DI_model_V1/DI_s_V1.cfg'.format(get_current_dir_and_goto_parent_dir()))
                enginFilePath = '{2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                if os.path.exists(enginFilePath):
                    # print("yolov8 EngineFIle exists.")
                    modelconfigwrite.append('#model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                    modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                else:
                    anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(anotherenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(anotherenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    elif os.path.exists(secondenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(secondenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    else:
                        modelconfigwrite.append('model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    
                modelconfigwrite.append('#int8-calib-file=calib.table')
                modelconfigwrite.append('labelfile-path={0}/models/DI_model_V1/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append(f'batch-size={len(list(total_stream_for_stremux_union))}')
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
                modelconfigwrite.append('custom-lib-path={0}/models/DI_model_V1/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')

                modelconfigwrite.append('[class-attrs-all]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.3')
                modelconfigwrite.append('topk=300')

                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                modelconfigwrite.append('topk=300')

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

                modelconfigwrite.append('[class-attrs-4]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.3')
                modelconfigwrite.append('topk=300')

                
                        
                modelconfigfile  = os.path.splitext(modelconfigfile)[0]    
                with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                    for O_O_O, item in enumerate(modelconfigwrite):
                        f.write('%s\n' % item)

                with open(config_file, 'w') as f:
                    for O_O_O, item in enumerate(lines):
                        f.write('%s\n' % item)

    elif len(response)!=0 :
        GPUCOUNT = 1
        Totalcamera_pereachGpu = 2
        print("NEW____RESPONSE_data==",)
        # print("----------------------------GPU_data--------------------------",GPU_data)
        if GPU_data is not None:
            directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app', 'configs')
            print('------------------directory_path----',directory_path)
            txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
            print("Text Files:", txt_files)
            if txt_files:
                try:
                    for txt_file in txt_files:
                        os.remove(os.path.join(directory_path, txt_file))
                    print("Text files deleted successfully ---1.0.1---")
                except Exception as e:
                    print(f"Error deleting text files---1.0.1---: {e}")
            else:
                print("No text files found in the directory.---1.0.1---")
            NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
            new_response=split_list(response,numberofsources_)
            if 'system_gpus' in GPU_data:
                GPUCOUNT = GPU_data['system_gpus']

            print("======================maximum===camera count for each GPU===",GPU_data['gpu_details'])
            
            if len(GPU_data['gpu_details']) !=0 :
                for jindex, iooojjn in enumerate(GPU_data['gpu_details']):
                    Totalcamera_pereachGpu = iooojjn['camera_limit']
                    break
            for config_index, writingresponse in enumerate(new_response): 
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
                # GPUSINDEX= 0
                config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
                crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
                config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
                hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
                PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))

                parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
                lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
                roi_enable_cam_ids = []
                ppe_enable_cam_ids = []
                config_tjm_lines =[]
                # roi_objects=set()
                traffic_count_enabledcameraids=[]
                cr_enable_cam_ids = []
                tc_label_names = []
                normal_config_file = 0
                final_roi_existed_cam_ids = []
                final_truck_cam_ids = []
                hooter_line = []
                crowd_line = []  
                onlyCrashHelmet =[]
                PPELINE = []     
                PPEFINALCAMERAIDS =[]
                Traffic_JAM = []
                traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
                steamsuit_cameraid =[]
                for index, x in enumerate(writingresponse): 
                    x['cameraid'] = camera_id
                    if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
                        if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("***************111111************")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("TC-CR_PPE===2")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:    
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("TC-CR_RA===3")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("cr-ra_PPE===5")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("RA-TC_PPE===handled")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("cr-ra===6")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("ra_TC===7")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID) 
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("ra_PPE===8")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("CR_TC===9")
                            if len(x['cr_data']) !=0:
                                print("-----------------x-----------999999---------")
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                print('-----------------print("-----------------x-----------999999---------")-----------------')
                                if x['cr_data'][0]['full_frame'] == False:
                                    print('-----------------print("-----------------x-----------999999-.01111111111111111111111111--------")-----------------')
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        print('-----------------print("-----------------x-----------999999-.02222222222222222222222222222--------")-----------------')
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        print('-----------------print("-----------------x-----------999999-.03333333333333333333333333333--------")-----------------')
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("PPE_TC===10")
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)  
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)    
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("PPE_CR===11")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)  
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("CR===12")    
                            if len(x['cr_data']) !=0:
                                print("-------------CR-------12---------kkkk-------------")
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                print("-------------CR-------12.0---------kkkk-------------")
                                if x['cr_data'][0]['full_frame'] == False:
                                    print("-------------CR-------12.1---------kkkk-------------")
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        print("-------------CR-------12.2---------kkkk-------------")
                                        cr_fun_conf_analytics(x, lines,config_tjm_lines)
                                        print("-------------CR-------12.3---------kkkk-------------")
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                                        print("-------------CR-------12.4---------kkkk-------------")
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("RA===13")    
                            roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("TC===14") 
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("PPE===14") 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        width_ratio=960/960
                        height_ratio= 544/544
                        if 'trafficjam_data' in x :
                            # print("---------------------validate_rois_array(x['trafficjam_data'],roi_required_keys)------------",validate_rois_array(x['trafficjam_data'],roi_required_keys))
                            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----00-------')
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
                                                # print('str(FinalTime)-------type---8------------',type(FinalTime))
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
                                                # print('str(FinalTime)-------type---7------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                    Traffic_JAM.append(NewcameraID)
                                else:
                                    print()
                            
                        # print("INDEX------------------------------------------",index)    
                        if '[crdcnt{}]'.format(index) not in crowd_line:
                            # print("-----")
                            crowd_line.append('[crdcnt{0}]'.format(index))
                            crowd_line.append("enable=0")
                            crowd_line.append("process-on-full-frame=1")
                            crowd_line.append("operate-on-label=person;")
                            crowd_line.append("max-count=1;")
                            crowd_line.append("min-count=0;")
                            crowd_line.append("data-save-time-in-sec=3\n")
                            
                        if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                            lines.append('[roi-filtering-stream-{0}]'.format(index))
                            if 'trafficjam_data' in x :
                                if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                    lines.append("enable=1")
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
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                    Traffic_JAM.append(NewcameraID)
                                else:
                                    lines.append("enable=0")
                                    lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            else:
                                lines.append("enable=0")
                                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            lines.append("inverse-roi=0")
                            # lines.append("class-id= 0;\n")
                            
                        if '[RA{}]'.format(index) not in hooter_line:
                            # print("-----")
                            hooter_line.append('[RA{0}]'.format(index))
                            hooter_line.append("enable = 0")
                            hooter_line.append("operate-on-label = person;")
                            hooter_line.append("hooter-enable = 0")
                            hooter_line.append("hooter-ip = none")
                            hooter_line.append('hooter-type = 0;')
                            hooter_line.append('hooter-shoutdown-time = 10')
                            hooter_line.append("hooter-stop-buffer-time = 3")
                            hooter_line.append("data-save-time-in-sec = 3\n")        

                        if '[PPE{}]'.format(index) not in PPELINE:
                            # print("-----")
                            PPELINE.append('[PPE{0}]'.format(index))
                            PPELINE.append("enable = 0")
                            PPELINE.append("hooter-enable = 0")
                            PPELINE.append("hooter-ip = none")
                            PPELINE.append('hooter-type = 0;')
                            PPELINE.append('hooter-shoutdown-time = 10')
                            PPELINE.append("hooter-stop-buffer-time = 3")
                            PPELINE.append('analytics-details =[{"analytics_type":0, "operate_on": "null;"},{"analytics_type":1, "operate_on": "null;"}]')
                            PPELINE.append("data-save-time-in-sec = 3\n")
                        NewcameraID+=1                            
                total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids,Traffic_JAM))
                with open(config_analytics_file, 'w') as f:
                    for item in lines:
                        f.write('%s\n' % item)
                with open(hooter_config_file_path, 'w') as hooter_file:
                    for jim in hooter_line:
                        hooter_file.write('%s\n' % jim)

                with open(PPE_config_file_path, 'w') as PPE_file:
                    for jim in PPELINE:
                        PPE_file.write('%s\n' % jim)
                with open(crowd_config_file, 'w') as crowd_file:
                    for O_O_O, item in enumerate(crowd_line):
                        crowd_file.write('%s\n' % item)

                # print('----------------------len---------',len(config_tjm_lines))
                with open(parking_roi_config_file, 'w') as file:
                    write_array_to_file(file,config_tjm_lines)
                    file.close()
                lines = []
                final_both_roi_cam_ids = []
                with open(sample_config_file) as file:
                    for write_config, line in enumerate(file):
                        if line.strip() == '[application]':
                            lines.append('[application]')
                            lines.append('enable-perf-measurement=1')
                            lines.append('perf-measurement-interval-sec=1')
                        elif line.strip() == '[tiled-display]':
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, Traffic_JAM)
                            total_stream_for_stremux_union = finaL_RA_PPE
                            num = math.sqrt(int(len(finaL_RA_PPE)))
                            rows,columns= get_layout(len(total_stream_for_stremux_union))
                            lines.append('[tiled-display]')
                            if execute_nvidia_smi(GPUSINDEX):
                                lines.append('enable=1')
                            elif TitledDisplayEnable:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('rows={0}'.format(str(rows)))
                            lines.append('columns={0}'.format(str(columns)))
                            lines.append('width=960')
                            lines.append('height=544')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[sources]':    
                            # print("newlength===", len(writingresponse))                            
                            for n, x in enumerate(writingresponse):
                                cam_id = '{0}'.format(int(n))
                                ppe_enable_cam_ids_exist=0
                                newcrowdcount=0
                                roi_enable_cam_ids_exist =0
                                trafficJamcount = 0 
                                if camera_id in roi_enable_cam_ids:
                                    roi_enable_cam_ids_exist = 1
                                elif camera_id in ppe_enable_cam_ids:
                                    ppe_enable_cam_ids_exist = 1
                                elif camera_id in cr_enable_cam_ids:
                                    newcrowdcount = 1

                                elif camera_id in Traffic_JAM:
                                    trafficJamcount= 1
                                if camera_id in ppe_enable_cam_ids:
                                    PPEFINALCAMERAIDS.append(camera_id)
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                                if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 and trafficJamcount > 0  :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  678990 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount= 0 

                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0   :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  678990 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0

                                elif roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 and trafficJamcount > 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  345677 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount= 0 
                                
                                elif roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  345677 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and trafficJamcount > 0 ) :
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  9876543 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount = 0 
                                
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  9876543 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif roi_enable_cam_ids_exist > 0:
                                    # print("normal_config_file += 555551 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif ppe_enable_cam_ids_exist > 0:
                                    # print("normal_config_file += 666666666666666 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  123456789 ------------------------",camera_id)
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif len(traffic_count_enabledcameraids)>0:
                                    # print("normal_config_file += 777777777777777777 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif newcrowdcount >0:
                                    # print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0

                                elif trafficJamcount >0:
                                    # print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount = 0 


                        elif line.strip() == '[sink0]':
                            lines.append('[sink0]')
                            lines.append('enable=1')
                            if gridview_true is True:
                                lines.append('type=2')
                            else:
                                lines.append('type=1')
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
                            lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            if batch_pushouttime == 40000:
                                lines.append('batched-push-timeout=40000')
                            else:
                                lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            lines.append('width=1920')
                            lines.append('height=1080')
                            lines.append('enable-padding=0')
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[primary-gie]':
                            lines.append('[primary-gie]')
                            lines.append('enable=1')
                            lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            # lines.append('bbox-border-color0=0;1;0;1.0')
                            # lines.append('bbox-border-color1=0;1;1;0.7')
                            # lines.append('bbox-border-color2=0;1;0;0.7')
                            # lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('bbox-border-color0=0.3;0;0;1')# dark shade of red or choclate
                            # lines.append('bbox-border-color1=0;1;1;1')# red 
                            lines.append('bbox-border-color1=1;0.3;0.9;1')#pinkish-purple or magenta
                            lines.append('bbox-border-color2=0.545;0;1;1')#purple
                            lines.append('bbox-border-color3=1;0.659;0;1')#orange
                            # lines.append('bbox-border-color3=0;1;0;1')
                            lines.append('bbox-border-color4=0.561;0.737;0.561;1')#dark sea green 
                            lines.append('bbox-border-color5=0.502;0.502;0;1')#olive color
                            lines.append('bbox-border-color6=0.392;0.584;0.929;1')#corn flower blue
                            lines.append('bbox-border-color7=0.941;0.502;0.502;1')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                            lines.append('model-engine-file=../../models/DI_model_V1/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                            lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                        elif line.strip() == '[primary-gie-ss]':
                            lines.append('[primary-gie-ss]')
                            if len(steamsuit_cameraid) !=0:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('batch-size={0}'.format(str(1)))
                            lines.append('bbox-border-color0=0;1;1;0.7')
                            lines.append('bbox-border-color1=0;1;1;0.7')
                            lines.append('bbox-border-color2=0;1;1;0.7')
                            lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            lines.append( 'config-file = ../../models/config_infer_primary_tsk_ss.txt')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))    
                        elif line.strip() == '[secondary-gie0]':
                            lines.append('[secondary-gie0]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            # lines.append('gie-unique-id = 4')
                            lines.append('gie-unique-id = 6')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 0;0;0;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                                secondaryconfig_file = []                                    
                                secondaryconfig_file.append('[property]')
                                secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(HelmetEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                 
                                secondaryconfig_file.append('infer-dims=3;320;320')
                                secondaryconfig_file.append('uff-input-blob-name=input_1')
                                secondaryconfig_file.append('batch-size=1')
                                secondaryconfig_file.append('process-mode=2')
                                secondaryconfig_file.append('model-color-format=0')
                                secondaryconfig_file.append('network-mode=2')
                                secondaryconfig_file.append('num-detected-classes=2')
                                secondaryconfig_file.append('interval=0')
                                secondaryconfig_file.append('gie-unique-id=2')
                                secondaryconfig_file.append('operate-on-gie-id=1')
                                secondaryconfig_file.append('operate-on-class-ids=0;')
                                secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_file.append('network-type=0')
                                secondaryconfig_file.append('uff-input-order=0\n')
                                secondaryconfig_file.append('[class-attrs-0]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20\n')
                                secondaryconfig_file.append('[class-attrs-1]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20')
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_file):
                                        f.write('%s\n' % item)
                            else:
                                if Hemetdetails is not None:
                                    HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                                    Hemeltversion= Hemetdetails['helmet']['version']
                                    lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                    lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                                    secondaryconfig_file = []                                    
                                    secondaryconfig_file.append('[property]')
                                    secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                    HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(HelmetEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                    
                                    secondaryconfig_file.append('infer-dims=3;320;320')
                                    secondaryconfig_file.append('uff-input-blob-name=input_1')
                                    secondaryconfig_file.append('batch-size=1')
                                    secondaryconfig_file.append('process-mode=2')
                                    secondaryconfig_file.append('model-color-format=0')
                                    secondaryconfig_file.append('network-mode=2')
                                    secondaryconfig_file.append('num-detected-classes=2')
                                    secondaryconfig_file.append('interval=0')
                                    secondaryconfig_file.append('gie-unique-id=2')
                                    secondaryconfig_file.append('operate-on-gie-id=1')
                                    secondaryconfig_file.append('operate-on-class-ids=0;')
                                    secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_file.append('network-type=0')
                                    secondaryconfig_file.append('uff-input-order=0\n')
                                    secondaryconfig_file.append('[class-attrs-0]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20\n')
                                    secondaryconfig_file.append('[class-attrs-1]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_file):
                                            f.write('%s\n' % item)                                
                        elif line.strip() == '[secondary-gie1]':
                            lines.append('[secondary-gie1]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            # lines.append('gie-unique-id = 5')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('gie-unique-id = 7')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                            if defaultsecondmodels == True :
                                lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                                secondaryconfig_filevest = []
                                secondaryconfig_filevest.append('[property]')
                                secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(VestEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                                # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                                # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('infer-dims=3;320;320')
                                secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                secondaryconfig_filevest.append('batch-size=1')
                                secondaryconfig_filevest.append('process-mode=2')
                                secondaryconfig_filevest.append('model-color-format=0')
                                secondaryconfig_filevest.append('network-mode=2')
                                secondaryconfig_filevest.append('num-detected-classes=3')
                                secondaryconfig_filevest.append('interval=0')
                                secondaryconfig_filevest.append('gie-unique-id=2')
                                secondaryconfig_filevest.append('operate-on-gie-id=1')
                                secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_filevest.append('network-type=0')
                                secondaryconfig_filevest.append('uff-input-order=0\n')
                                secondaryconfig_filevest.append('[class-attrs-0]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20\n')
                                secondaryconfig_filevest.append('[class-attrs-1]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')                                
                                secondaryconfig_filevest.append('[class-attrs-2]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')      
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_filevest):
                                        f.write('%s\n' % item)
                            else:
                                if Vestdetails is not None:
                                    Vestconfigfile = Vestdetails['vest']['modelpath']
                                    Vestversion= Vestdetails['vest']['version']
                                    lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                    lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                                    secondaryconfig_filevest = []
                                    secondaryconfig_filevest.append('[property]')
                                    secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                    VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(VestEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('infer-dims=3;320;320')
                                    secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                    secondaryconfig_filevest.append('batch-size=1')
                                    secondaryconfig_filevest.append('process-mode=2')
                                    secondaryconfig_filevest.append('model-color-format=0')
                                    secondaryconfig_filevest.append('network-mode=2')
                                    secondaryconfig_filevest.append('num-detected-classes=3')
                                    secondaryconfig_filevest.append('interval=0')
                                    secondaryconfig_filevest.append('gie-unique-id=2')
                                    secondaryconfig_filevest.append('operate-on-gie-id=1')
                                    secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                    secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_filevest.append('network-type=0')
                                    secondaryconfig_filevest.append('uff-input-order=0\n')
                                    secondaryconfig_filevest.append('[class-attrs-0]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20\n')
                                    secondaryconfig_filevest.append('[class-attrs-1]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')                                        
                                    secondaryconfig_filevest.append('[class-attrs-2]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_filevest):
                                            f.write('%s\n' % item)

                        elif line.strip() == '[secondary-gie2]':                            
                            lines.append('[secondary-gie2]')
                            if len(onlyCrashHelmet) !=0:
                                lines.append('enable = 1')
                            else:
                                lines.append('enable = 0')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 8')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')

                            CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                if os.path.exists(anotherenginFilePath):
                                    print('----------------------')
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(anotherenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                elif os.path.exists(secondenginFilePath):
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(secondenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                else:
                                    lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            if 1:#defaultsecondmodels == True :
                                # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/crash_helmet_nano_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                                ScondaryCrushhelmet = []
                                ScondaryCrushhelmet.append('[property]')
                                ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                                ScondaryCrushhelmet.append('model-color-format=0')
                                # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                                CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(CrushHelmet):
                                    # print("yolov3 EngineFIle exists.")
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                ScondaryCrushhelmet.append('batch-size=1')
                                ScondaryCrushhelmet.append('network-mode=2')
                                ScondaryCrushhelmet.append('num-detected-classes=2')
                                ScondaryCrushhelmet.append('interval=0')
                                ScondaryCrushhelmet.append('gie-unique-id=1')
                                ScondaryCrushhelmet.append('process-mode=2')
                                ScondaryCrushhelmet.append('network-type=0')
                                ScondaryCrushhelmet.append('cluster-mode=2')
                                ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                                ScondaryCrushhelmet.append('operate-on-gie-id=1')
                                ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                                ScondaryCrushhelmet.append('symmetric-padding=1')
                                ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                                ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                                ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                                ScondaryCrushhelmet.append('[class-attrs-0]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300\n')

                                ScondaryCrushhelmet.append('[class-attrs-1]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300')     
                                with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                                    for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                        f.write('%s\n' % item)
                            
                        elif line.strip() == '[tracker]':
                            lines.append('[tracker]')
                            lines.append('enable=1')
                            lines.append('tracker-width=960')
                            lines.append('tracker-height=544')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('#enable-batch-process=0')
                            if display_tracker :
                                lines.append('display-tracking-id=1')
                            else:
                                lines.append('display-tracking-id=0')
                            lines.append('user-meta-pool-size=64')
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
                        elif line.strip() == '[restricted-access]':
                            lines.append('[restricted-access]')
                            final_index = 0
                            final_roi_empty_ls = []
                            check_camera_id_for_RA = []
                            for Cherry, x in enumerate(writingresponse):
                                string2 = '-1;'
                                if len(x['roi_data']) != 0:
                                    for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                        label_name = roi_value['label_name']
                                        if ('person' in label_name and 'truck' in label_name):
                                            final_both_roi_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'truck' in label_name:
                                            final_truck_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' in label_name:
                                            final_roi_existed_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' not in label_name and 'truck' not in label_name:
                                            pass
                                        else:
                                            pass
                                final_index += 1
                            string_test = '-1;'
                            if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                                check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                            final_roi_existed_cam_ids = roi_enable_cam_ids
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            if len(roi_enable_cam_ids)== 0:
                                lines.append('enable = 0')
                            else:
                                lines.append('enable = 1')
                            lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                            lines.append('roi-overlay-enable = 1')
                            lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))
                        elif line.strip() == '[ppe-type-1]':
                            lines.append('[PPE]')
                            # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                            empty_ppe_ls = []
                            for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                                text = str(n) + ';'
                                empty_ppe_ls.append(text)
                            string2 = ''
                            if len(empty_ppe_ls) == 0:
                                lines.append('enable = 0')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            else:
                                lines.append('enable = 1')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                        elif line.strip() == '[crowd-counting]':
                            lines.append('[crowd-counting]')
                            cr_final_index = 0
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['cr_data']) != 0:
                                    cr_final_index += 1
                            if cr_final_index == 0:
                                enable_val = 0
                                lines.append('enable = {0}'.format(enable_val))
                            else:
                                enable_val = 1
                                lines.append('enable = {0}'.format(enable_val))
                            lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                            lines.append("roi-overlay-enable=1")

                        elif line.strip()=='[steam-suit]':
                            lines.append('[steam-suit]')
                            lines.append('camera-ids = -1;')
                            lines.append('data-save-interval = 1')  

                        elif line.strip() == '[traffic-count]':
                            lines.append('[traffic-count]')
                            tc_final_index = 0
                            final_tc_empty_ls = []
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['tc_data']) != 0:
                                    final_tc_existed_cam_ids = []
                                    for tc_val in x['tc_data']:
                                        for tc_val___test in tc_val['label_name']:
                                            if tc_val___test not in tc_label_names:
                                                tc_label_names.append(tc_val___test)
                                        if len(tc_val['traffic_count']) != 0:
                                            final_tc_existed_cam_ids.append(
                                                tc_final_index + 1)
                                            for n in final_tc_existed_cam_ids:
                                                text = str(n) + ';'
                                                final_tc_empty_ls.append(text)
                                            string2 = ''
                                tc_final_index += 1
                            if len(final_tc_empty_ls) == 0:
                                final_tc_empty_ls.append(string2)
                            # lines.append('camera-ids = {0}'.format(string2.join(final_tc_empty_ls)))
                            tc_empty_label_ls = []
                            for tc_label_name_test in tc_label_names:
                                text = str(tc_label_name_test) + ';'
                                tc_empty_label_ls.append(text)
                            test_string = ''
                            lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))


                        elif line.strip() == '[traffic-jam]':
                            lines.append('[traffic-jam]')
                            if len(Traffic_JAM) !=0:
                                lines.append( 'enable = 1')
                            else:
                                lines.append( 'enable = 0')
                            lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                            lines.append('data-save-interval=10\n')
                        elif line.strip() == '[traffic-counting]':
                            lines.append('[traffic-counting]')
                            lines.append( 'enable = 0')
                            lines.append('details=[]\n')
                        else:
                            lines.append(line.strip())
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('custom-network-config={0}/models/DI_model_V1/DI_s_V1.cfg'.format(get_current_dir_and_goto_parent_dir()))
                enginFilePath = '{2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                if os.path.exists(enginFilePath):
                    # print("yolov8 EngineFIle exists.")
                    modelconfigwrite.append('#model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                    modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                else:
                    anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(anotherenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(anotherenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    elif os.path.exists(secondenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(secondenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    else:
                        modelconfigwrite.append('model-file={0}/models/DI_model_V1/DI_s_V1.wts'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    
                modelconfigwrite.append('#int8-calib-file=calib.table')
                modelconfigwrite.append('labelfile-path={0}/models/DI_model_V1/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append(f'batch-size={len(list(total_stream_for_stremux_union))}')
                modelconfigwrite.append('network-mode=2')
                modelconfigwrite.append('num-detected-classes=5')
                modelconfigwrite.append('interval=0')
                modelconfigwrite.append('gie-unique-id=1')
                modelconfigwrite.append('process-mode=1')
                modelconfigwrite.append('network-type=0')
                modelconfigwrite.append('cluster-mode=2')
                modelconfigwrite.append('maintain-aspect-ratio=1')
                modelconfigwrite.append('symmetric-padding=1')
                modelconfigwrite.append('parse-bbox-func-name=NvDsInferParseYolo')
                modelconfigwrite.append('custom-lib-path={0}/models/DI_model_V1/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                modelconfigwrite.append('[class-attrs-all]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.45')
                modelconfigwrite.append('topk=300')
                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                modelconfigwrite.append('topk=300')

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

                modelconfigwrite.append('[class-attrs-4]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.3')
                modelconfigwrite.append('topk=300')

                modelconfigfile  = os.path.splitext(modelconfigfile)[0]  
                with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                    for O_O_O, item in enumerate(modelconfigwrite):
                        f.write('%s\n' % item) 
                with open(config_file, 'w') as f:
                    for O_O_O, item in enumerate(lines):
                        f.write('%s\n' % item)    
    return allWrittenSourceCAmIds





def Loaddocketrun_V1_1_model(response):
    valid_camera_list=[]
    roi_required_keys=['roi_name','traffic_jam_percentage','selected_objects','bb_box','roi_id','min_time']
    TitledDisplayEnable = True
    defaultsecondmodels = True
    Hemetdetails = {}
    Vestdetails = {}
    steamsuitaddedstatus = False
    GPUSINDEX = 0  
    allWrittenSourceCAmIds =[]
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
    classId = '0'
    print("Genral_configurations===",Genral_configurations)
    batch_pushouttime = 40000
    drop_frame_interval=1
    ticket_reset_time =10
    gridview_true = True
    numberofsources_= 4
    rtsp_reconnect_interval = 3
    displayfontsize = 12
    display_tracker =True
    if ('drop_frame_interval' in Genral_configurations and Genral_configurations['drop_frame_interval'] is not None) and ('camera_fps' in Genral_configurations and  Genral_configurations['camera_fps'] is not None) :
        camera_fps = Genral_configurations['camera_fps']
        drop_frame_interval = Genral_configurations['drop_frame_interval']
        Newpushouttime = math.ceil(int(camera_fps)/int(drop_frame_interval))
        batch_pushouttime= math.ceil(1000000/Newpushouttime)
    
    if ('rtsp_reconnect_interval' in Genral_configurations and Genral_configurations['rtsp_reconnect_interval'] is not None):
        rtsp_reconnect_interval = Genral_configurations['rtsp_reconnect_interval'] 
    

    if ('grid_view' in Genral_configurations and Genral_configurations['grid_view'] is not None):
        gridview_true = Genral_configurations['grid_view'] 
    if ('grid_size' in Genral_configurations and Genral_configurations['grid_size'] is not None):
        numberofsources_ = int(Genral_configurations['grid_size'])


    if ('ticket_reset_time' in Genral_configurations and Genral_configurations['ticket_reset_time'] is not None):
        ticket_reset_time = int(Genral_configurations['ticket_reset_time'])
    
    if 'display_font_size' in Genral_configurations :
        displayfontsize = Genral_configurations['display_font_size']

    if 'display_tracker' in Genral_configurations :
        display_tracker = Genral_configurations['display_tracker']
    
    print("number of sources-- fetched----222 --------------0000000000000000000000000",len(response))
    Total_source_count = len(response)
    GPU_data = mongo.db.gpu_configurations.find_one({})
    # new_response = split_list(response,numberofsources_)
    camera_id = 1 
    NewcameraID = 1
    modelconfigfile = '/DI_model_V1_1/config_infer_primary_DI_s_V1_1.txt'
    modelconfigwrite = []
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'phase_one_sample_config.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/docketrun_app'+'/configs'
    DIMODEL = get_current_dir_and_goto_parent_dir() + '/models/DI_model_V1_1'
    traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)
    if not os.path.exists(traffic_config_path):
        os.makedirs(traffic_config_path)
    if not os.path.exists(DIMODEL):
        os.makedirs(DIMODEL)           
    remove_text_files(deepstream_config_path)  
    modelthreshold = getthreshholdmodelconfig_details()
    person_threshold = '0.7'
    helmet_threshold = '0.5'
    vest_threshold = '0.5'
    CrashHelment_threshold = '0.3'
    Bicycle_threshold= '0.3'
    Motorbike_threshold ='0.3'
    car_threshold = '0.3'
    bus_threshold = '0.3'
    truck_threshold = '0.3'
    if modelthreshold is not None:
        if len(modelthreshold['threshold']) !=0:
            for new,classname in enumerate(modelthreshold['threshold']):
                if classname['class']=='person':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            person_threshold = int(classname['value'])/100
                            if person_threshold==1:
                                person_threshold ='0.9'
                        else:
                            person_threshold = '0.1'           
                elif  classname['class']=='helmet':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            helmet_threshold =  int(classname['value'])/100
                            if helmet_threshold==1:
                                helmet_threshold ='0.9'
                        else:
                            helmet_threshold ='0.1' 
                elif  classname['class']=='vest':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            vest_threshold = int(classname['value'])/100
                            if vest_threshold==1:
                                vest_threshold ='0.9'
                        else:
                            vest_threshold ='0.1'
                elif  classname['class']=='crash_helmet':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            CrashHelment_threshold = int(classname['value'])/100
                            if CrashHelment_threshold==1:
                                CrashHelment_threshold ='0.9'
                        else:
                            CrashHelment_threshold ='0.1'
                elif  classname['class']=='bicycle':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            Bicycle_threshold = int(classname['value'])/100
                            if Bicycle_threshold==1:
                                Bicycle_threshold ='0.9'
                        else:
                            Bicycle_threshold ='0.1'
                elif  classname['class']=='motorbike':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            Motorbike_threshold = int(classname['value'])/100
                            if Motorbike_threshold==1:
                                Motorbike_threshold ='0.9'
                        else:
                            Motorbike_threshold ='0.1'
                elif  classname['class']=='car':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            car_threshold = int(classname['value'])/100
                            if car_threshold==1:
                                car_threshold ='0.9'
                        else:
                            car_threshold ='0.1'

                elif  classname['class']=='bus':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            bus_threshold = int(classname['value'])/100
                            if bus_threshold==1:
                                bus_threshold ='0.9'
                        else:
                            bus_threshold ='0.1'
                elif  classname['class']=='truck':
                    if classname['value'] is not None:
                        if int(classname['value']) >0:
                            truck_threshold = int(classname['value'])/100
                            if truck_threshold==1:
                                truck_threshold ='0.9'
                        else:
                            truck_threshold ='0.1'
    model_config_details,secondarymodelconfigdetails = get_model_config_details()
    if type(secondarymodelconfigdetails)== list  and len(secondarymodelconfigdetails)!=0 :
        defaultsecondmodels = False
        for indexmo, Modedetails in enumerate(secondarymodelconfigdetails):
            print("indexmo===",indexmo,Modedetails)
            for MAINKey , Values  in Modedetails.items():
                if "helmet" in MAINKey:
                    Hemetdetails= Modedetails
                if "vest" in MAINKey:
                    Vestdetails= Modedetails
    steamsuitcameradetails = createSTEAMSUITconfig()
    steamsuitcameradetails =[]
    if  len(response)!=0 and  len(steamsuitcameradetails) !=0:#len(response)!=0 and  len(steamsuitcameradetails)
        if GPU_data is not None:
            directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app', 'configs')
            
            txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
            print('-----txt_files---------------1.0.1------',txt_files)
            if txt_files:
                try:
                    for txt_file in txt_files:
                        os.remove(os.path.join(directory_path, txt_file))
                    print("Text files deleted successfully.---1.9.0----")
                except Exception as e:
                    print(f"Error deleting text files:---1.9.0---- {e}")
            else:
                print("No text files found in the directory.---1.9.0----")
            NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
            # print("=====NEwcount====",NEwcount)
            new_response=GPUSsplit_list(response,GPU_data['system_gpus'])
            for config_index, writingresponse in enumerate(new_response):  
                if GPU_data['system_gpus']==1 :
                    GPUSINDEX = GPUSINDEX
                elif config_index ==0  :
                    GPUSINDEX = config_index
                elif camera_id >= NEwcount:
                    GPUSINDEX= GPUSINDEX+1 
                else:   
                    GPUSINDEX= GPUSINDEX
                # GPUSINDEX =1
                config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
                crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
                config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
                hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
                PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))
                parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
                lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
                config_tjm_lines=[]
                # roi_objects=set()
                roi_enable_cam_ids = []
                ppe_enable_cam_ids = []
                traffic_count_enabledcameraids=[]
                cr_enable_cam_ids = []
                tc_label_names = []
                normal_config_file = 0
                final_roi_existed_cam_ids = []
                final_truck_cam_ids = []
                hooter_line = []
                crowd_line = []  
                PPELINE = [] 
                onlyCrashHelmet =[]     
                PPEFINALCAMERAIDS =[]
                traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
                steamsuit_cameraid =[]
                # print("length == === ", len(writingresponse))
                Steamsuitdata = steamsuitcameradetails
                lines.append("[roi-filtering-stream-0]")
                lines.append("enable=0")
                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                lines.append("inverse-roi=0")
                lines.append("class-id= 0;\n")
                
                crowd_line.append("[crdcnt0]")
                crowd_line.append("enable=0")
                crowd_line.append("process-on-full-frame=1")
                crowd_line.append("operate-on-label=person;")
                crowd_line.append("max-count=1;")
                crowd_line.append("min-count=0;")
                crowd_line.append("data-save-time-in-sec=3\n")
                hooter_line.append("[RA0]")
                hooter_line.append("enable = 0")
                hooter_line.append("operate-on-label = person;")
                hooter_line.append("hooter-enable = 0")
                hooter_line.append("hooter-ip = none")
                hooter_line.append('hooter-type = 0;')
                hooter_line.append("hooter-stop-buffer-time = 3")
                hooter_line.append("data-save-time-in-sec = 3\n")
                for index, x in enumerate(writingresponse):
                    x['cameraid'] = NewcameraID
                    if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
                        if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("***************111111************")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("TC-CR_PPE===2")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:    
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)

                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("TC-CR_RA===3")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("cr-ra_PPE===5")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)

                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("RA-TC_PPE===handled")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                            
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("cr-ra===6")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                                        
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("ra_TC===7")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID) 
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("ra_PPE===8")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)   
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("CR_TC===9")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("PPE_TC===10")
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)   
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)    
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("PPE_CR===11")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)  
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("CR===12")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines) 
                                        
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("RA===13")    
                            roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("TC===14") 
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            print("PPE===14") 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        
                        width_ratio=960/960
                        height_ratio= 544/544
                        if 'trafficjam_data' in x :
                            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----1-------')
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
                                                # print('str(FinalTime)-------type---4------------',type(FinalTime))
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
                                                # print('str(FinalTime)-------type---3------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'

                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                else:
                                    print()   
                        if '[crdcnt{}]'.format(index) not in crowd_line:
                            # print("-----")
                            crowd_line.append('[crdcnt{0}]'.format(index))
                            crowd_line.append("enable=0")
                            crowd_line.append("process-on-full-frame=1")
                            crowd_line.append("operate-on-label=person;")
                            crowd_line.append("max-count=1;")
                            crowd_line.append("min-count=0;")
                            crowd_line.append("data-save-time-in-sec=3\n")                            
                        if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                            lines.append('[roi-filtering-stream-{0}]'.format(index))
                            if 'trafficjam_data' in x :
                                if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----00-0-------')
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
                                                # print('str(FinalTime)-------type---1------------',type(FinalTime))
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

                                                # print('str(FinalTime)-------type---2------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                else:
                                    lines.append("enable=0")
                                    lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            else:
                                lines.append("enable=0")
                                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            lines.append("inverse-roi=0")
                            # lines.append("class-id= 0;\n")
                            
                        if '[RA{}]'.format(index) not in hooter_line:
                            # print("-----")
                            hooter_line.append('[RA{0}]'.format(index))
                            hooter_line.append("enable = 0")
                            hooter_line.append("operate-on-label = person;")
                            hooter_line.append("hooter-enable = 0")
                            hooter_line.append("hooter-ip = none")
                            hooter_line.append('hooter-type = 0;')
                            hooter_line.append('hooter-shoutdown-time = 10')
                            hooter_line.append("hooter-stop-buffer-time = 3")
                            hooter_line.append("data-save-time-in-sec = 3\n")

                        if '[PPE{}]'.format(index) not in PPELINE:
                            # print("-----")
                            PPELINE.append('[PPE{0}]'.format(index))
                            PPELINE.append("enable = 0")
                            PPELINE.append("hooter-enable = 0")
                            PPELINE.append("hooter-ip = none")
                            PPELINE.append('hooter-type = 0;')
                            PPELINE.append('hooter-shoutdown-time = 10')
                            PPELINE.append("hooter-stop-buffer-time = 3")
                            PPELINE.append('analytics-details =[{"analytics_type":0, "operate_on": "null;"},{"analytics_type":1, "operate_on": "null;"}]')
                            PPELINE.append("data-save-time-in-sec = 3\n")
                        
                        NewcameraID+=1
                total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids))
                # print("roi_enable cam ids =====", roi_enable_cam_ids)
                # print("ppeppe_333enable_cam_ids",ppe_enable_cam_ids)
                # print("=================total_stream_for_stremux_union===============",total_stream_for_stremux_union)
                with open(config_analytics_file, 'w') as f:
                    for item in lines:
                        f.write('%s\n' % item)

                with open(hooter_config_file_path, 'w') as hooter_file:
                    for jim in hooter_line:
                        hooter_file.write('%s\n' % jim)

                with open(PPE_config_file_path, 'w') as PPE_file:
                    for jim in PPELINE:
                        PPE_file.write('%s\n' % jim)

                with open(crowd_config_file, 'w') as crowd_file:
                    for O_O_O, item in enumerate(crowd_line):
                        crowd_file.write('%s\n' % item)
                # print('----------------------len---------',len(config_tjm_lines))
                with open(parking_roi_config_file, 'w') as file:
                    write_array_to_file(file,config_tjm_lines)
                    file.close()
                lines = []
                final_both_roi_cam_ids = []
                with open(sample_config_file) as file:
                    for write_config, line in enumerate(file):
                        if line.strip() == '[application]':
                            lines.append('[application]')
                            lines.append('enable-perf-measurement=1')
                            lines.append('perf-measurement-interval-sec=1')

                        elif line.strip() == '[tiled-display]':
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                            total_stream_for_stremux_union = finaL_RA_PPE
                            num = math.sqrt(int(len(finaL_RA_PPE)))
                            rows,columns= get_layout(len(total_stream_for_stremux_union))
                            lines.append('[tiled-display]')
                            if execute_nvidia_smi(GPUSINDEX):
                                lines.append('enable=1')
                            elif TitledDisplayEnable:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('rows={0}'.format(str(rows)))
                            lines.append('columns={0}'.format(str(columns)))
                            lines.append('width=960')
                            lines.append('height=544')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('nvbuf-memory-type=0')

                        elif line.strip() == '[sources]':    
                            # print("newlength===", len(writingresponse))
                            steamsuitaddedstatus = False
                            for n, x in enumerate(writingresponse):
                                cam_id = '{0}'.format(int(n))
                                if camera_id in roi_enable_cam_ids:
                                    roi_enable_cam_ids_exist = 1
                                if camera_id in ppe_enable_cam_ids:
                                    ppe_enable_cam_ids_exist = 1
                                if camera_id in cr_enable_cam_ids:
                                    newcrowdcount = 1
                                # print("newcrowdcountnewcrowdcountnewcrowdcount===newcrowdcount> 0 ",newcrowdcount)
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')

                                # print("Steamsui44---4tda----ta===55544=",Steamsuitdata)
                                if len(Steamsuitdata) !=0 and steamsuitaddedstatus == False:
                                    uri = Steamsuitdata[0]['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  55544 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(Steamsuitdata[0]['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1    
                                    steamsuit_cameraid.append(camera_id)                        
                                    camera_id += 1
                                    steamsuitaddedstatus = True
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    # print("normal_config_file += 1 ------------------------",normal_config_file  )
                                if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  1222222222222222222222222222222222222222222 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0        
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ):
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) += 333 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec=2")
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                    
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  ^^^^^^^^^^^^^^^^^^^122334 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif roi_enable_cam_ids_exist > 0:
                                    print("normal_config_file += 5555522 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif ppe_enable_cam_ids_exist > 0:
                                    print("normal_config_file += 666666666666666 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdfkajsdkfkasdjk=============", roi_enable_cam_ids_exist)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  #####################11122 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                
                                elif len(traffic_count_enabledcameraids)>0:
                                    print("normal_config_file += 777777777777777777 ------------------------",normal_config_file  )
                                    # print("asdjfkasdfjaksdfkjaksdfkjaskdtraffic_count_enabledcameraidsfkajsdkfkasdjk=============", traffic_count_enabledcameraids)
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                                    
                                elif newcrowdcount >0:
                                    print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0                            
                        elif line.strip() == '[sink0]':
                            lines.append('[sink0]')
                            lines.append('enable=1')
                            if gridview_true is True:
                                lines.append('type=2')
                            else:
                                lines.append('type=1')
                            #lines.append('type=2')
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
                            lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            if batch_pushouttime == 40000:
                                lines.append('batched-push-timeout=40000')
                            else:
                                lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            lines.append('width=1920')
                            lines.append('height=1080')
                            lines.append('enable-padding=0')
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[primary-gie]':
                            lines.append('[primary-gie]')
                            lines.append('enable=1')
                            lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            # lines.append('bbox-border-color0=0;1;0;1.0')
                            # lines.append('bbox-border-color1=0;1;1;0.7')
                            # lines.append('bbox-border-color2=0;1;0;0.7')
                            # lines.append('bbox-border-color3=0;1;0;0.7')
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
                            modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                            lines.append('model-engine-file=../../models/DI_model_V1_1/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                            lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                        elif line.strip() == '[primary-gie-ss]':
                            lines.append('[primary-gie-ss]')
                            if len(steamsuit_cameraid) !=0:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('batch-size={0}'.format(str(1)))
                            lines.append('bbox-border-color0=0;1;1;0.7')
                            lines.append('bbox-border-color1=0;1;1;0.7')
                            lines.append('bbox-border-color2=0;1;1;0.7')
                            lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            lines.append('config-file = ../../models/config_infer_primary_tsk_ss.txt')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            
                            
                        elif line.strip() == '[secondary-gie0]':
                            lines.append('[secondary-gie0]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 6')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('gie-unique-id = 4')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 0;0;0;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                                secondaryconfig_file = []                                
                                secondaryconfig_file.append('[property]')
                                secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(HelmetEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                
                                secondaryconfig_file.append('infer-dims=3;320;320')
                                secondaryconfig_file.append('uff-input-blob-name=input_1')
                                secondaryconfig_file.append('batch-size=1')
                                secondaryconfig_file.append('process-mode=2')
                                secondaryconfig_file.append('model-color-format=0')
                                secondaryconfig_file.append('network-mode=2')
                                secondaryconfig_file.append('num-detected-classes=2')
                                secondaryconfig_file.append('interval=0')
                                secondaryconfig_file.append('gie-unique-id=2')
                                secondaryconfig_file.append('operate-on-gie-id=1')
                                secondaryconfig_file.append('operate-on-class-ids=0;')
                                secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_file.append('network-type=0')
                                secondaryconfig_file.append('uff-input-order=0\n')
                                secondaryconfig_file.append('[class-attrs-0]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20\n')
                                secondaryconfig_file.append('[class-attrs-1]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20')
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_file):
                                        f.write('%s\n' % item)
                            else:
                                if Hemetdetails is not None:
                                    HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                                    Hemeltversion= Hemetdetails['helmet']['version']
                                    lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                    lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                                    secondaryconfig_file = []                                    
                                    secondaryconfig_file.append('[property]')
                                    secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                    HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(HelmetEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('infer-dims=3;320;320')
                                    secondaryconfig_file.append('uff-input-blob-name=input_1')
                                    secondaryconfig_file.append('batch-size=1')
                                    secondaryconfig_file.append('process-mode=2')
                                    secondaryconfig_file.append('model-color-format=0')
                                    secondaryconfig_file.append('network-mode=2')
                                    secondaryconfig_file.append('num-detected-classes=2')
                                    secondaryconfig_file.append('interval=0')
                                    secondaryconfig_file.append('gie-unique-id=2')
                                    secondaryconfig_file.append('operate-on-gie-id=1')
                                    secondaryconfig_file.append('operate-on-class-ids=0;')
                                    secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_file.append('network-type=0')
                                    secondaryconfig_file.append('uff-input-order=0\n')
                                    secondaryconfig_file.append('[class-attrs-0]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20\n')
                                    secondaryconfig_file.append('[class-attrs-1]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_file):
                                            f.write('%s\n' % item)
                        elif line.strip() == '[secondary-gie1]':
                            lines.append('[secondary-gie1]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 7')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                            if defaultsecondmodels == True :
                                lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                                secondaryconfig_filevest = []
                                secondaryconfig_filevest.append('[property]')
                                secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_filevest.append('tlt-model-key=tlt_encode')

                                VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(VestEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                
                                secondaryconfig_filevest.append('infer-dims=3;320;320')
                                secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                secondaryconfig_filevest.append('batch-size=1')
                                secondaryconfig_filevest.append('process-mode=2')
                                secondaryconfig_filevest.append('model-color-format=0')
                                secondaryconfig_filevest.append('network-mode=2')
                                secondaryconfig_filevest.append('num-detected-classes=3')
                                secondaryconfig_filevest.append('interval=0')
                                secondaryconfig_filevest.append('gie-unique-id=2')
                                secondaryconfig_filevest.append('operate-on-gie-id=1')
                                secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_filevest.append('network-type=0')
                                secondaryconfig_filevest.append('uff-input-order=0\n')
                                secondaryconfig_filevest.append('[class-attrs-0]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20\n')
                                secondaryconfig_filevest.append('[class-attrs-1]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')                                
                                secondaryconfig_filevest.append('[class-attrs-2]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')      
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_filevest):
                                        f.write('%s\n' % item)

                            else:
                                if Vestdetails is not None:
                                    Vestconfigfile = Vestdetails['vest']['modelpath']
                                    Vestversion= Vestdetails['vest']['version']
                                    lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                    lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                                    secondaryconfig_filevest = []
                                    secondaryconfig_filevest.append('[property]')
                                    secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                    VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(VestEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))

                                    secondaryconfig_filevest.append('infer-dims=3;320;320')
                                    secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                    secondaryconfig_filevest.append('batch-size=1')
                                    secondaryconfig_filevest.append('process-mode=2')
                                    secondaryconfig_filevest.append('model-color-format=0')
                                    secondaryconfig_filevest.append('network-mode=2')
                                    secondaryconfig_filevest.append('num-detected-classes=3')
                                    secondaryconfig_filevest.append('interval=0')
                                    secondaryconfig_filevest.append('gie-unique-id=2')
                                    secondaryconfig_filevest.append('operate-on-gie-id=1')
                                    secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                    secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_filevest.append('network-type=0')
                                    secondaryconfig_filevest.append('uff-input-order=0\n')
                                    secondaryconfig_filevest.append('[class-attrs-0]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20\n')
                                    secondaryconfig_filevest.append('[class-attrs-1]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')                                    
                                    secondaryconfig_filevest.append('[class-attrs-2]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_filevest):
                                            f.write('%s\n' % item)

                        elif line.strip() == '[secondary-gie2]':
                            lines.append('[secondary-gie2]')
                            if len(onlyCrashHelmet) !=0:
                                lines.append('enable = 1')
                            else:
                                lines.append('enable = 0')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 8')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                if os.path.exists(anotherenginFilePath):
                                    print('----------------------')
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(anotherenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                elif os.path.exists(secondenginFilePath):
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(secondenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                else:
                                    lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")



                            if 1:#defaultsecondmodels == True :
                                # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/crash_helmet_nano_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                                ScondaryCrushhelmet = []
                                ScondaryCrushhelmet.append('[property]')
                                ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                                ScondaryCrushhelmet.append('model-color-format=0')
                                # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                                CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(CrushHelmet):
                                    # print("yolov3 EngineFIle exists.")
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                ScondaryCrushhelmet.append('batch-size=1')
                                ScondaryCrushhelmet.append('network-mode=2')
                                ScondaryCrushhelmet.append('num-detected-classes=2')
                                ScondaryCrushhelmet.append('interval=0')
                                ScondaryCrushhelmet.append('gie-unique-id=1')
                                ScondaryCrushhelmet.append('process-mode=2')
                                ScondaryCrushhelmet.append('network-type=0')
                                ScondaryCrushhelmet.append('cluster-mode=2')
                                ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                                ScondaryCrushhelmet.append('operate-on-gie-id=1')
                                ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                                ScondaryCrushhelmet.append('symmetric-padding=1')
                                ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                                ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                                ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                                ScondaryCrushhelmet.append('[class-attrs-0]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300\n')

                                ScondaryCrushhelmet.append('[class-attrs-1]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300')     
                                with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                                    for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                        f.write('%s\n' % item)
                        elif line.strip() == '[tracker]':
                            lines.append('[tracker]')
                            lines.append('enable=1')
                            lines.append('tracker-width=960')
                            lines.append('tracker-height=554')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('#enable-batch-process=0')
                            if display_tracker :
                                lines.append('display-tracking-id=1')
                            else:
                                lines.append('display-tracking-id=0')
                            lines.append('user-meta-pool-size=64')
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
                        elif line.strip()== '[application-config]':
                            lines.append('[application-config]')     
                        elif line.strip() == '[restricted-access]':
                            lines.append('[restricted-access]')
                            final_index = 0
                            final_roi_empty_ls = []
                            check_camera_id_for_RA = []
                            for Cherry, x in enumerate(writingresponse):
                                string2 = '-1;'
                                if len(x['roi_data']) != 0:
                                    for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                        label_name = roi_value['label_name']
                                        if ('person' in label_name and 'truck' in label_name):
                                            final_both_roi_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'truck' in label_name:
                                            final_truck_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' in label_name:
                                            final_roi_existed_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' not in label_name and 'truck' not in label_name:
                                            pass
                                        else:
                                            pass
                                final_index += 1
                            string_test = '-1;'
                            if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                                check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                            final_roi_existed_cam_ids = roi_enable_cam_ids
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            
                            # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",len(roi_enable_cam_ids))
                            # print("roi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_idsroi_enable_cam_ids==",roi_enable_cam_ids)
                            if len(roi_enable_cam_ids)== 0:
                                lines.append('enable = 0')

                            else:
                                lines.append('enable = 1')
                            lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                            lines.append('roi-overlay-enable = 1')
                            lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))

                        elif line.strip() == '[ppe-type-1]':
                            lines.append('[PPE]')
                            # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                            empty_ppe_ls = []
                            for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                                text = str(n) + ';'
                                empty_ppe_ls.append(text)
                            string2 = ''
                            if len(empty_ppe_ls) == 0:
                                # string2 = '-1;'
                                # lines.append('camera-ids = {0}'.format(string2))
                                lines.append('enable = 0')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            else:
                                # string2 = ''
                                # lines.append( 'camera-ids = {0}'.format(string2.join(empty_ppe_ls)))
                                lines.append('enable = 1')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))

                        elif line.strip() == '[crowd-counting]':
                            lines.append('[crowd-counting]')
                            cr_final_index = 0
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['cr_data']) != 0:
                                    cr_final_index += 1

                            if cr_final_index == 0:
                                enable_val = 0
                                lines.append('enable = {0}'.format(enable_val))
                            else:
                                enable_val = 1
                                lines.append('enable = {0}'.format(enable_val))
                            lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                            lines.append("roi-overlay-enable=1")

                        elif line.strip()=='[steam-suit]':
                            lines.append('[steam-suit]')
                            lines.append('camera-ids = -1;')
                            lines.append('data-save-interval = 1')  

                        elif line.strip() == '[traffic-count]':
                            lines.append('[traffic-count]')
                            tc_final_index = 0
                            final_tc_empty_ls = []
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['tc_data']) != 0:
                                    final_tc_existed_cam_ids = []
                                    for tc_val in x['tc_data']:
                                        for tc_val___test in tc_val['label_name']:
                                            if tc_val___test not in tc_label_names:
                                                tc_label_names.append(tc_val___test)
                                        if len(tc_val['traffic_count']) != 0:
                                            final_tc_existed_cam_ids.append(
                                                tc_final_index + 1)
                                            for n in final_tc_existed_cam_ids:
                                                text = str(n) + ';'
                                                final_tc_empty_ls.append(text)
                                            string2 = ''
                                tc_final_index += 1
                            if len(final_tc_empty_ls) == 0:
                                final_tc_empty_ls.append(string2)
                            tc_empty_label_ls = []
                            for tc_label_name_test in tc_label_names:
                                text = str(tc_label_name_test) + ';'
                                tc_empty_label_ls.append(text)
                            test_string = ''
                            lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))
                        
                        elif line.strip() == '[traffic-jam]':
                            lines.append('[traffic-jam]')
                            if len(Traffic_JAM) !=0:
                                lines.append( 'enable = 1')
                            else:
                                lines.append( 'enable = 0')
                            lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                            lines.append('data-save-interval=10\n')

                        elif line.strip() == '[traffic-counting]':
                            lines.append('[traffic-counting]')
                            lines.append( 'enable = 0')
                            lines.append('details=[]\n')
                        
                        else:
                            lines.append(line.strip())
                    
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('custom-network-config={0}/models/DI_model_V1_1/DI_s_V1_1.cfg'.format(get_current_dir_and_goto_parent_dir()))
                enginFilePath = '{2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                if os.path.exists(enginFilePath):
                    # print("yolov8 EngineFIle exists.")
                    modelconfigwrite.append('#model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                    modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                else:
                    anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(anotherenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1_1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(anotherenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    elif os.path.exists(secondenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1_1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(secondenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    else:
                        modelconfigwrite.append('model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    
                modelconfigwrite.append('#int8-calib-file=calib.table')
                modelconfigwrite.append('labelfile-path={0}/models/DI_model_V1_1/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append(f'batch-size={len(list(total_stream_for_stremux_union))}')
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
                modelconfigwrite.append('custom-lib-path={0}/models/DI_model_V1_1/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')

                modelconfigwrite.append('[class-attrs-all]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.3')
                modelconfigwrite.append('topk=300')

                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                modelconfigwrite.append('topk=300')

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

                modelconfigwrite.append('[class-attrs-4]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.3')
                modelconfigwrite.append('topk=300')

                
                        
                modelconfigfile  = os.path.splitext(modelconfigfile)[0]    
                with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                    for O_O_O, item in enumerate(modelconfigwrite):
                        f.write('%s\n' % item)

                with open(config_file, 'w') as f:
                    for O_O_O, item in enumerate(lines):
                        f.write('%s\n' % item)

    elif len(response)!=0 :
        GPUCOUNT = 1
        Totalcamera_pereachGpu = 2
        print("NEW____RESPONSE_data==",)
        # print("----------------------------GPU_data--------------------------",GPU_data)
        if GPU_data is not None:
            directory_path = os.path.join(get_current_dir_and_goto_parent_dir(), 'docketrun_app', 'configs')
            print('------------------directory_path----',directory_path)
            txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
            print("Text Files:", txt_files)
            if txt_files:
                try:
                    for txt_file in txt_files:
                        os.remove(os.path.join(directory_path, txt_file))
                    print("Text files deleted successfully ---1.0.1---")
                except Exception as e:
                    print(f"Error deleting text files---1.0.1---: {e}")
            else:
                print("No text files found in the directory.---1.0.1---")
            NEwcount =math.ceil(Total_source_count /  GPU_data['system_gpus']) 
            new_response=split_list(response,numberofsources_)
            if 'system_gpus' in GPU_data:
                GPUCOUNT = GPU_data['system_gpus']

            print("======================maximum===camera count for each GPU===",GPU_data['gpu_details'])
            
            if len(GPU_data['gpu_details']) !=0 :
                for jindex, iooojjn in enumerate(GPU_data['gpu_details']):
                    Totalcamera_pereachGpu = iooojjn['camera_limit']
                    break
            for config_index, writingresponse in enumerate(new_response): 
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
                # GPUSINDEX= 0
                config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
                crowd_config_file = os.path.join(deepstream_config_path, 'crowd_{0}.txt'.format(config_index+1))
                config_analytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
                hooter_config_file_path = os.path.join( deepstream_config_path, 'restricted_access_{0}.txt'.format(config_index+1))
                PPE_config_file_path = os.path.join( deepstream_config_path, 'PPE_config_{0}.txt'.format(config_index+1))

                parking_roi_config_file = os.path.join( deepstream_config_path, 'config_TJM_{0}.txt'.format(config_index+1))
                lines = ['[property]', 'enable=1', 'config-width=960', 'config-height=544', 'osd-mode=2', f'display-font-size={displayfontsize}', '']
                roi_enable_cam_ids = []
                ppe_enable_cam_ids = []
                config_tjm_lines =[]
                # roi_objects=set()
                traffic_count_enabledcameraids=[]
                cr_enable_cam_ids = []
                tc_label_names = []
                normal_config_file = 0
                final_roi_existed_cam_ids = []
                final_truck_cam_ids = []
                hooter_line = []
                crowd_line = []  
                onlyCrashHelmet =[]
                PPELINE = []     
                PPEFINALCAMERAIDS =[]
                Traffic_JAM = []
                traffic_count_cls_name_cls_id = {"person": classId, "car": "2", 'bicycle':"1",'motorcycle':"3",'bus':"5",'truck':"7"}
                steamsuit_cameraid =[]
                for index, x in enumerate(writingresponse): 
                    x['cameraid'] = camera_id
                    if type(x['roi_data']) == list and type(x['ppe_data']) == list and type(x['tc_data']) == list and type(x['cr_data']) == list:
                        if len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("***************111111************")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("TC-CR_PPE===2")
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:    
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            # print("TC-CR_RA===3")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index,  traffic_count_cls_name_cls_id)
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x,index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("cr-ra_PPE===5")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf( x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("RA-TC_PPE===handled")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("cr-ra===6")
                            roi_fun_with_cr_fun = roi_data_cf(x, hooter_line, index,   roi_enable_cam_ids,  lines,  traffic_count_cls_name_cls_id,NewcameraID,config_tjm_lines)
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("ra_TC===7")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID) 
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("ra_PPE===8")
                            roi_fun_with_cr_fun = roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) != 0:
                            print("CR_TC===9")
                            if len(x['cr_data']) !=0:
                                print("-----------------x-----------999999---------")
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                print('-----------------print("-----------------x-----------999999---------")-----------------')
                                if x['cr_data'][0]['full_frame'] == False:
                                    print('-----------------print("-----------------x-----------999999-.01111111111111111111111111--------")-----------------')
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        print('-----------------print("-----------------x-----------999999-.02222222222222222222222222222--------")-----------------')
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        print('-----------------print("-----------------x-----------999999-.03333333333333333333333333333--------")-----------------')
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id)   
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            # print("PPE_TC===10")
                            tc_fun_conf_anlytics_file = tc_fun(  x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)  
                            res_ppe_fun = ppe_fun(x,  index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)    
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            # print("PPE_CR===11")    
                            if len(x['cr_data']) !=0:
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                if x['cr_data'][0]['full_frame'] == False:
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        cr_fun_conf_analytics(x,  lines,config_tjm_lines)
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)  
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) != 0:
                            print("CR===12")    
                            if len(x['cr_data']) !=0:
                                print("-------------CR-------12---------kkkk-------------")
                                cr_fun_crowd_confg = cr_fun_crowd_conf(   x, crowd_line, index,NewcameraID, cr_enable_cam_ids,config_tjm_lines)
                            if x['cr_data']:
                                print("-------------CR-------12.0---------kkkk-------------")
                                if x['cr_data'][0]['full_frame'] == False:
                                    print("-------------CR-------12.1---------kkkk-------------")
                                    if '[roi-filtering-stream-{0}]'.format(index)  in lines:
                                        print("-------------CR-------12.2---------kkkk-------------")
                                        cr_fun_conf_analytics(x, lines,config_tjm_lines)
                                        print("-------------CR-------12.3---------kkkk-------------")
                                    else:
                                        cr_fun_conf_analyticsPASSINGWRITE(x, index, lines,config_tjm_lines) 
                                        print("-------------CR-------12.4---------kkkk-------------")
                        elif len(x['roi_data']) != 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("RA===13")    
                            roi_fun_with_cr_fun =roi_fun_no_cr_data(x, hooter_line, index,roi_enable_cam_ids, lines,NewcameraID,config_tjm_lines)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) == 0 and len(x['tc_data']) != 0 and len(x['cr_data']) == 0:
                            print("TC===14") 
                            tc_fun_conf_anlytics_file = tc_fun(x, lines, index, traffic_count_cls_name_cls_id) 
                            if tc_fun_conf_anlytics_file:
                                traffic_count_enabledcameraids.append(NewcameraID)
                        elif len(x['roi_data']) == 0 and len(x['ppe_data']) != 0 and len(x['tc_data']) == 0 and len(x['cr_data']) == 0:
                            # print("PPE===14") 
                            res_ppe_fun = ppe_fun(x, index, ppe_enable_cam_ids,NewcameraID,PPELINE,onlyCrashHelmet)
                        width_ratio=960/960
                        height_ratio= 544/544
                        if 'trafficjam_data' in x :
                            # print("---------------------validate_rois_array(x['trafficjam_data'],roi_required_keys)------------",validate_rois_array(x['trafficjam_data'],roi_required_keys))
                            if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                                    lines.append('[roi-filtering-stream-{0}]'.format(index))
                                    lines.append("enable=1")
                                    # print('str(FinalTime)-------type---3-----00-------')
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
                                                # print('str(FinalTime)-------type---8------------',type(FinalTime))
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
                                                # print('str(FinalTime)-------type---7------------',type(FinalTime))
                                                Checkdetails = Checkdetails + '{"roi_name":"' + str(roi_data['roi_name'].strip()) + '",' + \
                                                                                '"operate-on-label":"' + str(';'.join([obj.lower() for obj in roi_objects])) + '",' + \
                                                                                '"jamming-percent":' + str(roi_data['traffic_jam_percentage']) + ',' + \
                                                                                '"verify-time":' + str(FinalTime) + '}'
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                    Traffic_JAM.append(NewcameraID)
                                else:
                                    print()
                            
                        # print("INDEX------------------------------------------",index)    
                        if '[crdcnt{}]'.format(index) not in crowd_line:
                            # print("-----")
                            crowd_line.append('[crdcnt{0}]'.format(index))
                            crowd_line.append("enable=0")
                            crowd_line.append("process-on-full-frame=1")
                            crowd_line.append("operate-on-label=person;")
                            crowd_line.append("max-count=1;")
                            crowd_line.append("min-count=0;")
                            crowd_line.append("data-save-time-in-sec=3\n")
                            
                        if '[roi-filtering-stream-{0}]'.format(index) not in lines:
                            lines.append('[roi-filtering-stream-{0}]'.format(index))
                            if 'trafficjam_data' in x :
                                if  validate_rois_array(x['trafficjam_data'],roi_required_keys):
                                    lines.append("enable=1")
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
                                    lines.append('\n')
                                    Checkdetails= Checkdetails+']'  
                                    config_tjm_lines.append(Checkdetails) 
                                    config_tjm_lines.append('\n')
                                    Traffic_JAM.append(NewcameraID)
                                else:
                                    lines.append("enable=0")
                                    lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            else:
                                lines.append("enable=0")
                                lines.append("roi-RA-ww = 433;59;524;58;543;161;411;172")
                            lines.append("inverse-roi=0")
                            # lines.append("class-id= 0;\n")
                            
                        if '[RA{}]'.format(index) not in hooter_line:
                            # print("-----")
                            hooter_line.append('[RA{0}]'.format(index))
                            hooter_line.append("enable = 0")
                            hooter_line.append("operate-on-label = person;")
                            hooter_line.append("hooter-enable = 0")
                            hooter_line.append("hooter-ip = none")
                            hooter_line.append('hooter-type = 0;')
                            hooter_line.append('hooter-shoutdown-time = 10')
                            hooter_line.append("hooter-stop-buffer-time = 3")
                            hooter_line.append("data-save-time-in-sec = 3\n")        

                        if '[PPE{}]'.format(index) not in PPELINE:
                            # print("-----")
                            PPELINE.append('[PPE{0}]'.format(index))
                            PPELINE.append("enable = 0")
                            PPELINE.append("hooter-enable = 0")
                            PPELINE.append("hooter-ip = none")
                            PPELINE.append('hooter-type = 0;')
                            PPELINE.append('hooter-shoutdown-time = 10')
                            PPELINE.append("hooter-stop-buffer-time = 3")
                            PPELINE.append('analytics-details =[{"analytics_type":0, "operate_on": "null;"},{"analytics_type":1, "operate_on": "null;"}]')
                            PPELINE.append("data-save-time-in-sec = 3\n")
                        NewcameraID+=1                            
                total_stream_for_stremux_union = list(set().union(ppe_enable_cam_ids, roi_enable_cam_ids,traffic_count_enabledcameraids,cr_enable_cam_ids,Traffic_JAM))
                with open(config_analytics_file, 'w') as f:
                    for item in lines:
                        f.write('%s\n' % item)
                with open(hooter_config_file_path, 'w') as hooter_file:
                    for jim in hooter_line:
                        hooter_file.write('%s\n' % jim)

                with open(PPE_config_file_path, 'w') as PPE_file:
                    for jim in PPELINE:
                        PPE_file.write('%s\n' % jim)
                with open(crowd_config_file, 'w') as crowd_file:
                    for O_O_O, item in enumerate(crowd_line):
                        crowd_file.write('%s\n' % item)

                # print('----------------------len---------',len(config_tjm_lines))
                with open(parking_roi_config_file, 'w') as file:
                    write_array_to_file(file,config_tjm_lines)
                    file.close()
                lines = []
                final_both_roi_cam_ids = []
                with open(sample_config_file) as file:
                    for write_config, line in enumerate(file):
                        if line.strip() == '[application]':
                            lines.append('[application]')
                            lines.append('enable-perf-measurement=1')
                            lines.append('perf-measurement-interval-sec=1')
                        elif line.strip() == '[tiled-display]':
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( roi_enable_cam_ids, ppe_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, traffic_count_enabledcameraids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, cr_enable_cam_ids)
                            finaL_RA_PPE = remove_duplicate_elements_from_two_list( finaL_RA_PPE, Traffic_JAM)
                            total_stream_for_stremux_union = finaL_RA_PPE
                            num = math.sqrt(int(len(finaL_RA_PPE)))
                            rows,columns= get_layout(len(total_stream_for_stremux_union))
                            lines.append('[tiled-display]')
                            if execute_nvidia_smi(GPUSINDEX):
                                lines.append('enable=1')
                            elif TitledDisplayEnable:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('rows={0}'.format(str(rows)))
                            lines.append('columns={0}'.format(str(columns)))
                            lines.append('width=960')
                            lines.append('height=544')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[sources]':    
                            # print("newlength===", len(writingresponse))                            
                            for n, x in enumerate(writingresponse):
                                cam_id = '{0}'.format(int(n))
                                ppe_enable_cam_ids_exist=0
                                newcrowdcount=0
                                roi_enable_cam_ids_exist =0
                                trafficJamcount = 0 
                                if camera_id in roi_enable_cam_ids:
                                    roi_enable_cam_ids_exist = 1
                                elif camera_id in ppe_enable_cam_ids:
                                    ppe_enable_cam_ids_exist = 1
                                elif camera_id in cr_enable_cam_ids:
                                    newcrowdcount = 1

                                elif camera_id in Traffic_JAM:
                                    trafficJamcount= 1
                                if camera_id in ppe_enable_cam_ids:
                                    PPEFINALCAMERAIDS.append(camera_id)
                                find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                                if find_data is not None:
                                    if find_data['rtsp_flag'] == '1':
                                        if 'rtsp' in x['rtsp_url']:
                                            x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                                if (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0 and trafficJamcount > 0  :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  678990 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount= 0 

                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 ) and newcrowdcount> 0   :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 1222222222222222222222222222222222222222222 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  678990 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0

                                elif roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 and trafficJamcount > 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  345677 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount= 0 
                                
                                elif roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and len(traffic_count_enabledcameraids)> 0 :
                                    uri = x['rtsp_url']
                                    # print("normal_config_file += 33 ------------------------",normal_config_file  )
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  345677 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 and trafficJamcount > 0 ) :
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  9876543 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount = 0 
                                
                                elif (roi_enable_cam_ids_exist > 0 and ppe_enable_cam_ids_exist > 0 ):
                                    # print("normal_config_file += 4444 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  9876543 ------------------------")
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif roi_enable_cam_ids_exist > 0:
                                    # print("normal_config_file += 555551 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif ppe_enable_cam_ids_exist > 0:
                                    # print("normal_config_file += 666666666666666 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    # print("-------------(camera_id) +=  123456789 ------------------------",camera_id)
                                    PPEFINALCAMERAIDS.append(camera_id)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1                            
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif len(traffic_count_enabledcameraids)>0:
                                    # print("normal_config_file += 777777777777777777 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                elif newcrowdcount >0:
                                    # print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0

                                elif trafficJamcount >0:
                                    # print("normal_config_file += 8888888888888888888 ------------------------",normal_config_file  )
                                    uri = x['rtsp_url']
                                    lines.append('[source{0}]'.format(normal_config_file))
                                    lines.append('enable=1')
                                    lines.append('type=4')
                                    lines.append('uri = {0}'.format(uri))
                                    lines.append('num-sources=1')
                                    lines.append('gpu-id={0}'.format(GPUSINDEX))
                                    lines.append('nvbuf-memory-type=0')
                                    lines.append('latency=150')
                                    lines.append('camera-id={0}'.format(camera_id))   
                                    camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                                    allWrittenSourceCAmIds.append(camera_required_data)
                                    lines.append('camera-name={0}'.format(x['cameraname']))
                                    lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                                    lines.append('operate-on-class = {0}'.format(x['selected_object']))
                                    lines.append('#pre-process-bbox = [{"label":"car", "min_bbox_w":5, "min_bbox_h": 5, "max_bbox_w": 100, "max_bbox_h": 100}]')
                                    if 'drop_frame_interval' in Genral_configurations and drop_frame_interval is not None:
                                        lines.append('drop-frame-interval = {0}\n'.format(drop_frame_interval))
                                    else:
                                        lines.append('drop-frame-interval = 1\n')
                                    normal_config_file += 1
                                    camera_id += 1
                                    ppe_enable_cam_ids_exist = 0
                                    roi_enable_cam_ids_exist = 0
                                    newcrowdcount = 0
                                    trafficJamcount = 0 


                        elif line.strip() == '[sink0]':
                            lines.append('[sink0]')
                            lines.append('enable=1')
                            if gridview_true is True:
                                lines.append('type=2')
                            else:
                                lines.append('type=1')
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
                            lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            if batch_pushouttime == 40000:
                                lines.append('batched-push-timeout=40000')
                            else:
                                lines.append('batched-push-timeout={0}'.format(batch_pushouttime))
                            lines.append('width=1920')
                            lines.append('height=1080')
                            lines.append('enable-padding=0')
                            lines.append('nvbuf-memory-type=0')
                        elif line.strip() == '[primary-gie]':
                            lines.append('[primary-gie]')
                            lines.append('enable=1')
                            lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                            # lines.append('bbox-border-color0=0;1;0;1.0')
                            # lines.append('bbox-border-color1=0;1;1;0.7')
                            # lines.append('bbox-border-color2=0;1;0;0.7')
                            # lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('bbox-border-color0=0.3;0;0;1')# dark shade of red or choclate
                            # lines.append('bbox-border-color1=0;1;1;1')# red 
                            lines.append('bbox-border-color1=1;0.3;0.9;1')#pinkish-purple or magenta
                            lines.append('bbox-border-color2=0.545;0;1;1')#purple
                            lines.append('bbox-border-color3=1;0.659;0;1')#orange
                            # lines.append('bbox-border-color3=0;1;0;1')
                            lines.append('bbox-border-color4=0.561;0.737;0.561;1')#dark sea green 
                            lines.append('bbox-border-color5=0.502;0.502;0;1')#olive color
                            lines.append('bbox-border-color6=0.392;0.584;0.929;1')#corn flower blue
                            lines.append('bbox-border-color7=0.941;0.502;0.502;1')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            modelconfigfile  = os.path.splitext(modelconfigfile)[0]
                            lines.append('model-engine-file=../../models/DI_model_V1_1/engine/model_b{0}_gpu0_fp16.engine'.format(len(list(total_stream_for_stremux_union))))
                            lines.append( 'config-file = ../../models/{0}_{1}.txt'.format(modelconfigfile,config_index+1))
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                        elif line.strip() == '[primary-gie-ss]':
                            lines.append('[primary-gie-ss]')
                            if len(steamsuit_cameraid) !=0:
                                lines.append('enable=1')
                            else:
                                lines.append('enable=0')
                            lines.append('batch-size={0}'.format(str(1)))
                            lines.append('bbox-border-color0=0;1;1;0.7')
                            lines.append('bbox-border-color1=0;1;1;0.7')
                            lines.append('bbox-border-color2=0;1;1;0.7')
                            lines.append('bbox-border-color3=0;1;0;0.7')
                            lines.append('nvbuf-memory-type=0')
                            lines.append('interval=0')
                            lines.append('gie-unique-id=1')
                            lines.append( 'config-file = ../../models/config_infer_primary_tsk_ss.txt')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))    
                        elif line.strip() == '[secondary-gie0]':
                            lines.append('[secondary-gie0]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            # lines.append('gie-unique-id = 4')
                            lines.append('gie-unique-id = 6')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 0;0;0;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            if defaultsecondmodels == True :
                                lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                lines.append('config-file = ../../models/config_infer_secandary_helmet_v5.txt')
                                secondaryconfig_file = []                                    
                                secondaryconfig_file.append('[property]')
                                secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(HelmetEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                 
                                secondaryconfig_file.append('infer-dims=3;320;320')
                                secondaryconfig_file.append('uff-input-blob-name=input_1')
                                secondaryconfig_file.append('batch-size=1')
                                secondaryconfig_file.append('process-mode=2')
                                secondaryconfig_file.append('model-color-format=0')
                                secondaryconfig_file.append('network-mode=2')
                                secondaryconfig_file.append('num-detected-classes=2')
                                secondaryconfig_file.append('interval=0')
                                secondaryconfig_file.append('gie-unique-id=2')
                                secondaryconfig_file.append('operate-on-gie-id=1')
                                secondaryconfig_file.append('operate-on-class-ids=0;')
                                secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_file.append('network-type=0')
                                secondaryconfig_file.append('uff-input-order=0\n')
                                secondaryconfig_file.append('[class-attrs-0]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20\n')
                                secondaryconfig_file.append('[class-attrs-1]')
                                secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                secondaryconfig_file.append('group-threshold=1')
                                secondaryconfig_file.append('eps=0.4')
                                secondaryconfig_file.append('#minBoxes=3')
                                secondaryconfig_file.append('#detected-min-w=20')
                                secondaryconfig_file.append('#detected-min-h=20')
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_helmet_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_file):
                                        f.write('%s\n' % item)
                            else:
                                if Hemetdetails is not None:
                                    HEmeltconfigfile = Hemetdetails['helmet']['modelpath']
                                    Hemeltversion= Hemetdetails['helmet']['version']
                                    lines.append('model-engine-file=../../models/helmet_detector_v5/model_b1_gpu0_fp16.engine')
                                    lines.append('config-file = ../../models/{0}'.format(HEmeltconfigfile))
                                    secondaryconfig_file = []                                    
                                    secondaryconfig_file.append('[property]')
                                    secondaryconfig_file.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_file.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_file.append('tlt-model-key=tlt_encode')
                                    HelmetEngineFile = get_current_dir_and_goto_parent_dir()+'/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(HelmetEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('#model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_file.append('tlt-encoded-model={0}/models/helmet_detector_v5/resnet18_helmet_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('labelfile-path={0}/models/helmet_detector_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_file.append('model-engine-file={1}/models/helmet_detector_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                    
                                    secondaryconfig_file.append('infer-dims=3;320;320')
                                    secondaryconfig_file.append('uff-input-blob-name=input_1')
                                    secondaryconfig_file.append('batch-size=1')
                                    secondaryconfig_file.append('process-mode=2')
                                    secondaryconfig_file.append('model-color-format=0')
                                    secondaryconfig_file.append('network-mode=2')
                                    secondaryconfig_file.append('num-detected-classes=2')
                                    secondaryconfig_file.append('interval=0')
                                    secondaryconfig_file.append('gie-unique-id=2')
                                    secondaryconfig_file.append('operate-on-gie-id=1')
                                    secondaryconfig_file.append('operate-on-class-ids=0;')
                                    secondaryconfig_file.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_file.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_file.append('network-type=0')
                                    secondaryconfig_file.append('uff-input-order=0\n')
                                    secondaryconfig_file.append('[class-attrs-0]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20\n')
                                    secondaryconfig_file.append('[class-attrs-1]')
                                    secondaryconfig_file.append('pre-cluster-threshold={0}'.format(helmet_threshold))
                                    secondaryconfig_file.append('group-threshold=1')
                                    secondaryconfig_file.append('eps=0.4')
                                    secondaryconfig_file.append('#minBoxes=3')
                                    secondaryconfig_file.append('#detected-min-w=20')
                                    secondaryconfig_file.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(HEmeltconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_file):
                                            f.write('%s\n' % item)                                
                        elif line.strip() == '[secondary-gie1]':
                            lines.append('[secondary-gie1]')
                            lines.append('enable = 1')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            # lines.append('gie-unique-id = 5')
                            # lines.append('operate-on-gie-id = 1')
                            # lines.append('operate-on-class-ids = 0;')
                            # lines.append('batch-size = 1')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('gie-unique-id = 7')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            lines.append('bbox-border-color2 = 1.0;0;1.0;0.7')
                            if defaultsecondmodels == True :
                                lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/config_infer_secandary_vest_v5.txt')       
                                secondaryconfig_filevest = []
                                secondaryconfig_filevest.append('[property]')
                                secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(VestEngineFile):
                                    # print("yolov3 EngineFIle exists.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    # print("yolov3 EngineFIle does not exist.")
                                    secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                # secondaryconfig_filevest.append('tlt-encoded-model=./vest_detection_v5/resnet18_vest_detector_v5.etlt')
                                # secondaryconfig_filevest.append('labelfile-path=./vest_detection_v5/labels.txt')
                                # secondaryconfig_filevest.append('model-engine-file=./vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX))
                                secondaryconfig_filevest.append('infer-dims=3;320;320')
                                secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                secondaryconfig_filevest.append('batch-size=1')
                                secondaryconfig_filevest.append('process-mode=2')
                                secondaryconfig_filevest.append('model-color-format=0')
                                secondaryconfig_filevest.append('network-mode=2')
                                secondaryconfig_filevest.append('num-detected-classes=3')
                                secondaryconfig_filevest.append('interval=0')
                                secondaryconfig_filevest.append('gie-unique-id=2')
                                secondaryconfig_filevest.append('operate-on-gie-id=1')
                                secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                secondaryconfig_filevest.append('network-type=0')
                                secondaryconfig_filevest.append('uff-input-order=0\n')
                                secondaryconfig_filevest.append('[class-attrs-0]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20\n')
                                secondaryconfig_filevest.append('[class-attrs-1]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')                                
                                secondaryconfig_filevest.append('[class-attrs-2]')
                                secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                secondaryconfig_filevest.append('group-threshold=1')
                                secondaryconfig_filevest.append('eps=0.4')
                                secondaryconfig_filevest.append('#minBoxes=3')
                                secondaryconfig_filevest.append('#detected-min-w=20')
                                secondaryconfig_filevest.append('#detected-min-h=20')      
                                with open(get_current_dir_and_goto_parent_dir()+'/models/config_infer_secandary_vest_v5.txt', 'w') as f:
                                    for O_O_O, item in enumerate(secondaryconfig_filevest):
                                        f.write('%s\n' % item)
                            else:
                                if Vestdetails is not None:
                                    Vestconfigfile = Vestdetails['vest']['modelpath']
                                    Vestversion= Vestdetails['vest']['version']
                                    lines.append("model-engine-file=../../models/vest_detection_v5/model_b1_gpu0_fp16.engine")
                                    lines.append('config-file = ../../models/{0}'.format(Vestconfigfile))    
                                    secondaryconfig_filevest = []
                                    secondaryconfig_filevest.append('[property]')
                                    secondaryconfig_filevest.append('gpu-id={0}'.format(GPUSINDEX))
                                    secondaryconfig_filevest.append('net-scale-factor=0.00392156862745098')
                                    secondaryconfig_filevest.append('tlt-model-key=tlt_encode')
                                    VestEngineFile = get_current_dir_and_goto_parent_dir()+'/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                    if os.path.exists(VestEngineFile):
                                        # print("yolov3 EngineFIle exists.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('#model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    else:
                                        # print("yolov3 EngineFIle does not exist.")
                                        secondaryconfig_filevest.append('tlt-encoded-model={0}/models/vest_detection_v5/resnet18_vest_detector_v5.etlt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('labelfile-path={0}/models/vest_detection_v5/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                        secondaryconfig_filevest.append('model-engine-file={1}/models/vest_detection_v5/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    secondaryconfig_filevest.append('infer-dims=3;320;320')
                                    secondaryconfig_filevest.append('uff-input-blob-name=input_1')
                                    secondaryconfig_filevest.append('batch-size=1')
                                    secondaryconfig_filevest.append('process-mode=2')
                                    secondaryconfig_filevest.append('model-color-format=0')
                                    secondaryconfig_filevest.append('network-mode=2')
                                    secondaryconfig_filevest.append('num-detected-classes=3')
                                    secondaryconfig_filevest.append('interval=0')
                                    secondaryconfig_filevest.append('gie-unique-id=2')
                                    secondaryconfig_filevest.append('operate-on-gie-id=1')
                                    secondaryconfig_filevest.append('operate-on-class-ids=0;')
                                    secondaryconfig_filevest.append('output-blob-names=output_cov/Sigmoid;output_bbox/BiasAdd')
                                    secondaryconfig_filevest.append('offsets=0.0;0.0;0.0')
                                    secondaryconfig_filevest.append('network-type=0')
                                    secondaryconfig_filevest.append('uff-input-order=0\n')
                                    secondaryconfig_filevest.append('[class-attrs-0]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20\n')
                                    secondaryconfig_filevest.append('[class-attrs-1]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')                                        
                                    secondaryconfig_filevest.append('[class-attrs-2]')
                                    secondaryconfig_filevest.append('pre-cluster-threshold={0}'.format(vest_threshold))
                                    secondaryconfig_filevest.append('group-threshold=1')
                                    secondaryconfig_filevest.append('eps=0.4')
                                    secondaryconfig_filevest.append('#minBoxes=3')
                                    secondaryconfig_filevest.append('#detected-min-w=20')
                                    secondaryconfig_filevest.append('#detected-min-h=20')
                                    with open(get_current_dir_and_goto_parent_dir()+'/models/{0}'.format(Vestconfigfile), 'w') as f:
                                        for O_O_O, item in enumerate(secondaryconfig_filevest):
                                            f.write('%s\n' % item)

                        elif line.strip() == '[secondary-gie2]':                            
                            lines.append('[secondary-gie2]')
                            if len(onlyCrashHelmet) !=0:
                                lines.append('enable = 1')
                            else:
                                lines.append('enable = 0')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('gie-unique-id = 8')
                            lines.append('operate-on-gie-id = 1')
                            lines.append('operate-on-class-ids = 0;')
                            lines.append('batch-size = 1')
                            lines.append('bbox-border-color0 = 1.0;1.0;1.0;0.7')
                            lines.append('bbox-border-color1 = 1;0;0;0.7')
                            # lines.append('bbox-border-color0 = 1;0;1;0.7')
                            # lines.append('bbox-border-color1 = 1;0;0;0.7')

                            CrushHelmetEngine = '{2}/models/yoloV8_crash_helmet/engine/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                            if os.path.exists(CrushHelmetEngine):
                                lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            else:
                                anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(1,GPUSINDEX,get_current_dir_and_goto_parent_dir())
                                if os.path.exists(anotherenginFilePath):
                                    print('----------------------')
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(anotherenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                elif os.path.exists(secondenginFilePath):
                                    destination= '{0}/models/yoloV8_crash_helmet/'.format(get_current_dir_and_goto_parent_dir())
                                    shutil.copy(secondenginFilePath, destination)
                                    if os.path.exists(CrushHelmetEngine):
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                    else:
                                        lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                                else:
                                    lines.append("model-engine-file=../../models/yoloV8_crash_helmet/engine/model_b1_gpu0_fp16.engine")
                            if 1:#defaultsecondmodels == True :
                                # lines.append("model-engine-file=../../models/yoloV8_crash_helmet/crash_helmet_nano_b1_gpu0_fp16.engine")
                                lines.append('config-file = ../../models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt')       
                                ScondaryCrushhelmet = []
                                ScondaryCrushhelmet.append('[property]')
                                ScondaryCrushhelmet.append('gpu-id={0}'.format(GPUSINDEX))
                                ScondaryCrushhelmet.append('net-scale-factor=0.0039215697906911373')
                                ScondaryCrushhelmet.append('model-color-format=0')
                                # ScondaryCrushhelmet.append('tlt-model-key=tlt_encode')
                                CrushHelmet = get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX)
                                if os.path.exists(CrushHelmet):
                                    # print("yolov3 EngineFIle exists.")
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                else:
                                    ScondaryCrushhelmet.append("custom-network-config={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.cfg".format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('model-file={0}/models/yoloV8_crash_helmet/yolov8_Crash_helmet_nano_v1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('labelfile-path={0}/models/yoloV8_crash_helmet/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                                    ScondaryCrushhelmet.append('#model-engine-file={1}/models/yoloV8_crash_helmet/engine/model_b1_gpu{0}_fp16.engine'.format(GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                                    
                                ScondaryCrushhelmet.append('batch-size=1')
                                ScondaryCrushhelmet.append('network-mode=2')
                                ScondaryCrushhelmet.append('num-detected-classes=2')
                                ScondaryCrushhelmet.append('interval=0')
                                ScondaryCrushhelmet.append('gie-unique-id=1')
                                ScondaryCrushhelmet.append('process-mode=2')
                                ScondaryCrushhelmet.append('network-type=0')
                                ScondaryCrushhelmet.append('cluster-mode=2')
                                ScondaryCrushhelmet.append('maintain-aspect-ratio=1')
                                ScondaryCrushhelmet.append('operate-on-gie-id=1')
                                ScondaryCrushhelmet.append('operate-on-class-ids=0;')
                                ScondaryCrushhelmet.append('symmetric-padding=1')
                                ScondaryCrushhelmet.append('parse-bbox-func-name=NvDsInferParseYolo')
                                ScondaryCrushhelmet.append('custom-lib-path={0}/models/yoloV8_crash_helmet/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                                ScondaryCrushhelmet.append('engine-create-func-name=NvDsInferYoloCudaEngineGet\n')
                                ScondaryCrushhelmet.append('[class-attrs-0]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300\n')

                                ScondaryCrushhelmet.append('[class-attrs-1]')
                                ScondaryCrushhelmet.append('nms-iou-threshold=0.6')
                                ScondaryCrushhelmet.append('pre-cluster-threshold={0}'.format('0.7'))
                                ScondaryCrushhelmet.append('topk=300')     
                                with open(get_current_dir_and_goto_parent_dir()+'/models/yoloV8_crash_helmet/config_infer_secondary_crash_helemt_yoloV8_nano_1.txt', 'w') as f:
                                    for O_O_O, item in enumerate(ScondaryCrushhelmet):
                                        f.write('%s\n' % item)
                            
                        elif line.strip() == '[tracker]':
                            lines.append('[tracker]')
                            lines.append('enable=1')
                            lines.append('tracker-width=960')
                            lines.append('tracker-height=544')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so'):
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/libnvds_nvmultiobjecttracker.so', get_current_dir_and_goto_parent_dir()+'/models/libnvds_nvmultiobjecttracker.so')
                                lines.append('ll-lib-file=../../models/libnvds_nvmultiobjecttracker.so')
                            if os.path.exists(get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml'):
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            else:
                                shutil.copy(str(os.getcwd())+'/smaple_files/config_tracker_NvDCF_perf.yml', get_current_dir_and_goto_parent_dir()+'/models/config_tracker_NvDCF_perf.yml')
                                lines.append('ll-config-file=../../models/config_tracker_NvDCF_perf.yml')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-6.2/lib/libnvds_nvmultiobjecttracker.so')
                            lines.append('#ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                            lines.append('gpu-id={0}'.format(GPUSINDEX))
                            lines.append('#enable-batch-process=0')
                            if display_tracker :
                                lines.append('display-tracking-id=1')
                            else:
                                lines.append('display-tracking-id=0')
                            lines.append('user-meta-pool-size=64')
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
                        elif line.strip() == '[restricted-access]':
                            lines.append('[restricted-access]')
                            final_index = 0
                            final_roi_empty_ls = []
                            check_camera_id_for_RA = []
                            for Cherry, x in enumerate(writingresponse):
                                string2 = '-1;'
                                if len(x['roi_data']) != 0:
                                    for test_roi_ra, roi_value in enumerate(x['roi_data']):
                                        label_name = roi_value['label_name']
                                        if ('person' in label_name and 'truck' in label_name):
                                            final_both_roi_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'truck' in label_name:
                                            final_truck_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' in label_name:
                                            final_roi_existed_cam_ids.append(final_index + 1)
                                            string2 = ''
                                        elif 'person' not in label_name and 'truck' not in label_name:
                                            pass
                                        else:
                                            pass
                                final_index += 1
                            string_test = '-1;'
                            if len(final_roi_existed_cam_ids) != 0 or len(final_both_roi_cam_ids) != 0:
                                check_camera_id_for_RA.append(final_roi_existed_cam_ids)
                            final_roi_existed_cam_ids = roi_enable_cam_ids
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            for n in roi_enable_cam_ids:
                                text = str(n) + ';'
                                if text not in final_roi_empty_ls:
                                    final_roi_empty_ls.append(text)
                            if len(roi_enable_cam_ids)== 0:
                                lines.append('enable = 0')
                            else:
                                lines.append('enable = 1')
                            lines.append('config-file = ./restricted_access_{0}.txt'.format(config_index+1))
                            lines.append('roi-overlay-enable = 1')
                            lines.append('ticket-reset-timer = {0}'.format(ticket_reset_time))
                        elif line.strip() == '[ppe-type-1]':
                            lines.append('[PPE]')
                            # print("==============PPEFINALCAMERAIDS=3======,",PPEFINALCAMERAIDS)
                            empty_ppe_ls = []
                            for OPI_, n in enumerate(PPEFINALCAMERAIDS):
                                text = str(n) + ';'
                                empty_ppe_ls.append(text)
                            string2 = ''
                            if len(empty_ppe_ls) == 0:
                                lines.append('enable = 0')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                            else:
                                lines.append('enable = 1')
                                lines.append('config-file = PPE_config_{0}.txt'.format(config_index+1))
                        elif line.strip() == '[crowd-counting]':
                            lines.append('[crowd-counting]')
                            cr_final_index = 0
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['cr_data']) != 0:
                                    cr_final_index += 1
                            if cr_final_index == 0:
                                enable_val = 0
                                lines.append('enable = {0}'.format(enable_val))
                            else:
                                enable_val = 1
                                lines.append('enable = {0}'.format(enable_val))
                            lines.append('config-file = ./crowd_{0}.txt'.format(config_index+1))#config-file = ./crowd
                            lines.append("roi-overlay-enable=1")

                        elif line.strip()=='[steam-suit]':
                            lines.append('[steam-suit]')
                            lines.append('camera-ids = -1;')
                            lines.append('data-save-interval = 1')  

                        elif line.strip() == '[traffic-count]':
                            lines.append('[traffic-count]')
                            tc_final_index = 0
                            final_tc_empty_ls = []
                            for Cherry, x in enumerate(response):
                                string2 = '-1;'
                                if len(x['tc_data']) != 0:
                                    final_tc_existed_cam_ids = []
                                    for tc_val in x['tc_data']:
                                        for tc_val___test in tc_val['label_name']:
                                            if tc_val___test not in tc_label_names:
                                                tc_label_names.append(tc_val___test)
                                        if len(tc_val['traffic_count']) != 0:
                                            final_tc_existed_cam_ids.append(
                                                tc_final_index + 1)
                                            for n in final_tc_existed_cam_ids:
                                                text = str(n) + ';'
                                                final_tc_empty_ls.append(text)
                                            string2 = ''
                                tc_final_index += 1
                            if len(final_tc_empty_ls) == 0:
                                final_tc_empty_ls.append(string2)
                            # lines.append('camera-ids = {0}'.format(string2.join(final_tc_empty_ls)))
                            tc_empty_label_ls = []
                            for tc_label_name_test in tc_label_names:
                                text = str(tc_label_name_test) + ';'
                                tc_empty_label_ls.append(text)
                            test_string = ''
                            lines.append('operate-on-label = {0}'.format(test_string.join(tc_empty_label_ls)))


                        elif line.strip() == '[traffic-jam]':
                            lines.append('[traffic-jam]')
                            if len(Traffic_JAM) !=0:
                                lines.append( 'enable = 1')
                            else:
                                lines.append( 'enable = 0')
                            lines.append('tjm-config-file=./config_TJM_{0}.txt'.format(config_index+1))
                            lines.append('data-save-interval=10\n')
                        elif line.strip() == '[traffic-counting]':
                            lines.append('[traffic-counting]')
                            lines.append( 'enable = 0')
                            lines.append('details=[]\n')
                        else:
                            lines.append(line.strip())
                modelconfigwrite =[]
                modelconfigwrite.append('[property]')
                modelconfigwrite.append('gpu-id={0}'.format(GPUSINDEX))
                modelconfigwrite.append('net-scale-factor=0.0039215697906911373')
                modelconfigwrite.append('model-color-format=0')
                modelconfigwrite.append('custom-network-config={0}/models/DI_model_V1_1/DI_s_V1_1.cfg'.format(get_current_dir_and_goto_parent_dir()))
                enginFilePath = '{2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                if os.path.exists(enginFilePath):
                    # print("yolov8 EngineFIle exists.")
                    modelconfigwrite.append('#model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                    modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                else:
                    anotherenginFilePath = '{2}/docketrun_app/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(anotherenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1_1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(anotherenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    elif os.path.exists(secondenginFilePath):
                        print('----------------------')
                        destination= '{0}/models/DI_model_V1_1/engine/'.format(get_current_dir_and_goto_parent_dir())
                        shutil.copy(secondenginFilePath, destination)
                        if os.path.exists(enginFilePath):
                            print('----------------') 
                            modelconfigwrite.append('#model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                        else:
                            modelconfigwrite.append('model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                            modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    else:
                        modelconfigwrite.append('model-file={0}/models/DI_model_V1_1/DI_s_V1_1.wts'.format(get_current_dir_and_goto_parent_dir()))
                        modelconfigwrite.append('model-engine-file={2}/models/DI_model_V1_1/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),GPUSINDEX,get_current_dir_and_goto_parent_dir()))
                    
                modelconfigwrite.append('#int8-calib-file=calib.table')
                modelconfigwrite.append('labelfile-path={0}/models/DI_model_V1_1/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append(f'batch-size={len(list(total_stream_for_stremux_union))}')
                modelconfigwrite.append('network-mode=2')
                modelconfigwrite.append('num-detected-classes=5')
                modelconfigwrite.append('interval=0')
                modelconfigwrite.append('gie-unique-id=1')
                modelconfigwrite.append('process-mode=1')
                modelconfigwrite.append('network-type=0')
                modelconfigwrite.append('cluster-mode=2')
                modelconfigwrite.append('maintain-aspect-ratio=1')
                modelconfigwrite.append('symmetric-padding=1')
                modelconfigwrite.append('parse-bbox-func-name=NvDsInferParseYolo')
                modelconfigwrite.append('custom-lib-path={0}/models/DI_model_V1_1/utils/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                modelconfigwrite.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                modelconfigwrite.append('[class-attrs-all]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.45')
                modelconfigwrite.append('topk=300')
                modelconfigwrite.append('[class-attrs-0]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold={0}'.format(person_threshold))
                modelconfigwrite.append('topk=300')

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

                modelconfigwrite.append('[class-attrs-4]')
                modelconfigwrite.append('nms-iou-threshold=0.45')
                modelconfigwrite.append('pre-cluster-threshold=0.3')
                modelconfigwrite.append('topk=300')

                modelconfigfile  = os.path.splitext(modelconfigfile)[0]  
                with open(get_current_dir_and_goto_parent_dir()+'/models/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                    for O_O_O, item in enumerate(modelconfigwrite):
                        f.write('%s\n' % item) 
                with open(config_file, 'w') as f:
                    for O_O_O, item in enumerate(lines):
                        f.write('%s\n' % item)    
    return allWrittenSourceCAmIds