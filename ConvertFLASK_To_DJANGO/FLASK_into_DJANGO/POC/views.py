from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.final_ping import *

# date = datetime



def Getwheelcountdata():
    data = []#pictures: { $exists: true, $type: 'array', $ne: [] }
    fetch_require_data = list(ppera_cameras.find({'camera_status': True, "analytics_status": 'true','poc.wheel_count':{'$exists':True,"$ne": []}}))
    if len(fetch_require_data) != 0:
        for i in fetch_require_data:
            J={}
            if ENABLED_SOLUTION_IS_EMPTY_DICT(i['poc']):
                if 'wheel_count' in i['poc']:
                    roi_parameters = i['poc']['wheel_count']
                    if len(roi_parameters) !=0:  
                        J['poc']=i['poc']  
            if ENABLED_SOLUTION_IS_EMPTY_DICT(J) :
                J['cameraname']=i['cameraname']
                J['alarm_type']=i['alarm_type']
                J['alarm_ip_address']=i['alarm_ip_address']
                J['rtsp_url']=i['rtsp_url']
                data.append(J)
    return data

def wheelcountdumpvoiceannaoumentdataintodatatable(getdata_response):
    if "voice_announcement_status" not in mongo.db.list_collection_names():
        print("Collection 'voice_announcement_status' does not exist-VPMS")
        # raise Exception("Collection 'voice_announcement_status' does not exist")
    else:
        voice_announcement_status.delete_many({"violation_type": { "$in": ["wheelcount"] }})
    for i , j in enumerate(getdata_response):

        if len(j['poc']) !=0:
            WheelcountAreadata = j['poc']['wheel_count']
            insertvoice_datawheelcount = []
            for roiindex , roivalues in enumerate(WheelcountAreadata):
                print('------roivalues-------------',roivalues)
                if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
                    if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
                            # if roivalues['full_frame']==True:
                            insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'wheelcount','violation_type':'wheelcount','violation_time':None,'valid_time':None,'roi_name':roivalues['area_name']}
                            if insertvalue  not in insertvoice_datawheelcount:
                                insertvoice_datawheelcount.append(insertvalue)
                            # else:
                            #     insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'wheelcount','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                            #     if insertvalue  not in insertvoice_dataFSD:
                            #         insertvoice_dataFSD.append(insertvalue)

            if len(insertvoice_datawheelcount) !=0:
                voice_announcement_status.insert_many(insertvoice_datawheelcount)

def wheelconfig():
    ret = {'message': 'something went wrong with create config update_cam_id__.', 'success': False}
    getdata_response = Getwheelcountdata()
    if len(getdata_response) != 0:
        wheelcountdumpvoiceannaoumentdataintodatatable(getdata_response)
        function__response = WriteconfigofWheel(getdata_response)
        # return_data_update_camera = UPdatemulticonfigCamid(function__response)
        return_data_update_camera ='200'
        if return_data_update_camera == '200':
            ret = { 'message': 'wheel monitoring app is started successfully.', 'success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'please enable and add the ai analytics solutions.'
    return ret


def WriteconfigofWheel(response):
    # print("------------------------response---------------------",response)
    Genral_configurations = mongo.db.rtsp_flag.find_one({})
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
        # if 'display_font_size' in Genral_configurations['']
    allWrittenSourceCAmIds =[]
    numberofsources_= 4
    new_response = split_list(response,numberofsources_)
    camera_id =1 
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'wheelsampleconfig.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() +  '/wheel_rotation'+'/configs'
    yolo_config_path = get_current_dir_and_goto_parent_dir() + '/models/wheelmodel'
    traffic_config_path = get_current_dir_and_goto_parent_dir()+'/models/wheelmodel/engine'
    if not os.path.exists(deepstream_config_path):
        os.makedirs(deepstream_config_path)
    if not os.path.exists(yolo_config_path):
        os.makedirs(yolo_config_path)
    if not os.path.exists(traffic_config_path):
        os.makedirs(traffic_config_path)         
    remove_text_files(deepstream_config_path)   
    # print("------------------------new_response-----------",new_response)  
    for config_index, writingresponse in enumerate(new_response):  
        config_file = os.path.join(deepstream_config_path, 'config_{0}.txt'.format(config_index+1))
        configanalytics_file = os.path.join(deepstream_config_path, 'config_analytics_{0}.txt'.format(config_index+1))
        lines = [ '']
        normal_config_file = 0
        analyticsdetailsline = []
        print("length == === 1", len(writingresponse))
        with open(sample_config_file) as file:
            for write_config, line in enumerate(file):
                if line.strip() == '[application]':
                    lines.append('[application]')
                    lines.append('enable-perf-measurement=1')
                    lines.append('perf-measurement-interval-sec=5\n')
                elif line.strip() == '[tiled-display]':
                    finaL_RA_PPE = writingresponse
                    total_stream_for_stremux_union = finaL_RA_PPE
                    rows,columns = get_layout(total_stream_for_stremux_union)
                    lines.append('[tiled-display]')
                    lines.append('enable=1')
                    lines.append('rows={0}'.format(str(rows)))
                    lines.append('columns={0}'.format(str(columns)))
                    lines.append('width=1280')
                    lines.append('height=720')
                    lines.append('gpu-id=0')
                    lines.append('nvbuf-memory-type=0\n')
                elif line.strip() == '[sources]': 
                    print("newlength===2", len(writingresponse))
                    analyticsdetailsline.append('[property]')
                    analyticsdetailsline.append('enable=1')
                    analyticsdetailsline.append('config-width=960')
                    analyticsdetailsline.append('config-height=544')
                    analyticsdetailsline.append('osd-mode=2')
                    analyticsdetailsline.append(f'display-font-size={displayfontsize}\n')
                    for n, x in enumerate(writingresponse):
                        print("-----------------------x-------------------firesmo33keconfig-1",x)
                        cam_id = '{0}'.format(int(n))
                        find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])
                        if find_data is not None:
                            if find_data['rtsp_flag'] == '1':
                                if 'rtsp' in x['rtsp_url']:
                                    x['rtsp_url'] = x['rtsp_url'].replace( 'rtsp', 'rtspt')
                        if ENABLED_SOLUTION_IS_EMPTY_DICT(x['poc']):
                            Camerawiselabels =[]
                            if 'wheel_count' in x['poc']:
                                roi_parameters = x['poc']['wheel_count']
                                FSdstring = '['   
                                if len(roi_parameters) != 0:
                                    analyticsdetailsline.append('[line-crossing-stream-{0}]'.format(normal_config_file))
                                    analyticsdetailsline.append('enable=1')
                                    for ___p, value in enumerate(roi_parameters):
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
                                        analyticsdetailsline.append('line-crossing-{0} = {1}'.format(tc_name, checkNegativevaluesinBbox(fin_bbox_ls)))
                                    test_string = ''
                                    analyticsdetailsline.append('class-id= {0}'.format('0;'))
                                    analyticsdetailsline.append('extended=1')
                                    analyticsdetailsline.append('mode=loose\n')
                            uri = x['rtsp_url']
                            lines.append('[source{0}]'.format(normal_config_file))
                            lines.append('enable=1')
                            lines.append('type=4')
                            lines.append('uri = {0}'.format(uri))
                            lines.append('num-sources=1')
                            lines.append('gpu-id=0')
                            lines.append('nvbuf-memory-type=0')
                            # lines.append('latency=150')
                            lines.append('camera-id={0}'.format(camera_id))
                            camera_required_data= {"cameraname":x['cameraname'],'rtsp_url':uri,"cameraid":camera_id}
                            allWrittenSourceCAmIds.append(camera_required_data)
                            lines.append('camera-name={0}'.format(x['cameraname']))
                            lines.append("rtsp-reconnect-interval-sec={0}".format(rtsp_reconnect_interval))
                            lines.append('drop-frame-interval = {0}'.format(drop_frame_interval))     
                            x['cameraid']=camera_id
                            normal_config_file += 1
                            camera_id += 1
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
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[osd]':
                    lines.append('[osd]')
                    lines.append('enable=1')
                    lines.append('gpu-id=0')
                    lines.append('border-width=1')
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
                    lines.append('live-source=0')
                    lines.append( 'batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('batched-push-timeout=40000')
                    lines.append('width=1920')
                    lines.append('height=1080')
                    lines.append('enable-padding=0')
                    lines.append('nvbuf-memory-type=0')

                elif line.strip() == '[primary-gie]':
                    lines.append('[primary-gie]')
                    lines.append('enable=1')
                    lines.append('gpu-id=0')
                    lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                    lines.append('bbox-border-color0=1;0;0;1')
                    lines.append('bbox-border-color1=0;1;1;1')
                    lines.append('bbox-border-color2=0;1;1;1')
                    lines.append('bbox-border-color3=0;1;0;1')
                    lines.append('nvbuf-memory-type=0')
                    lines.append('interval=0')
                    lines.append('gie-unique-id=1')
                    # '{0}/models/fsd/engine/'.format(get_current_dir_and_goto_parent_dir())
                    lines.append('model-engine-file={0}/models/wheelmodel/engine/model_b{1}_gpu0_fp16.engine'.format(get_current_dir_and_goto_parent_dir(),len(list(total_stream_for_stremux_union))))
                    modelconfigfile = 'config_infer_primary_yoloV8'
                    lines.append('config-file=../../models/wheelmodel/{0}_{1}.txt'.format(modelconfigfile,config_index+1) )                    
                    FIRESMOKEDUSTMODEL =[]
                    FIRESMOKEDUSTMODEL.append('[property]')
                    FIRESMOKEDUSTMODEL.append('gpu-id={0}'.format(0))
                    FIRESMOKEDUSTMODEL.append('batch-size=1')
                    FIRESMOKEDUSTMODEL.append('net-scale-factor=0.0039215697906911373')
                    FIRESMOKEDUSTMODEL.append('model-color-format=0')
                    FIRESMOKEDUSTMODEL.append('custom-network-config={0}/models/wheelmodel/yolov8_best.cfg'.format(get_current_dir_and_goto_parent_dir()))
                    enginFilePath = '{2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir())
                    if os.path.exists(enginFilePath):
                        # print("yolov3 EngineFIle exists.")
                        FIRESMOKEDUSTMODEL.append('#model-file={0}/models/wheelmodel/yolov8_best.wts'.format(get_current_dir_and_goto_parent_dir()))
                        FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir()))
                    else:
                        # print("yolov3 EngineFIle does not exist.")
                        anotherenginFilePath = '{2}/fire_and_smoke/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir())
                        secondenginFilePath = '{2}/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir())
                        if os.path.exists(anotherenginFilePath):
                            print('----------------------')
                            destination= '{0}/models/wheelmodel/engine/'.format(get_current_dir_and_goto_parent_dir())
                            
                            shutil.copy(anotherenginFilePath, destination)
                            if os.path.exists(enginFilePath):
                                print('----------------') 
                                FIRESMOKEDUSTMODEL.append('#model-file={0}/models/wheelmodel/yolov8_best.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir()))
                            else:
                                FIRESMOKEDUSTMODEL.append('model-file={0}/models/wheelmodel/yolov8_best.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir()))
                        elif os.path.exists(secondenginFilePath):
                            print('----------------------')
                            destination= '{0}/models/wheelmodel/engine/'.format(get_current_dir_and_goto_parent_dir())
                            shutil.copy(secondenginFilePath, destination)
                            if os.path.exists(enginFilePath):
                                FIRESMOKEDUSTMODEL.append('#model-file={0}/models/wheelmodel/yolov8_best.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir()))
                            else:
                                FIRESMOKEDUSTMODEL.append('model-file={0}/models/wheelmodel/yolov8_best.wts'.format(get_current_dir_and_goto_parent_dir()))
                                FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir()))
                        else:
                            FIRESMOKEDUSTMODEL.append('model-file={0}/models/wheelmodel/yolov8_best.wts'.format(get_current_dir_and_goto_parent_dir()))
                            FIRESMOKEDUSTMODEL.append('model-engine-file={2}/models/wheelmodel/engine/model_b{0}_gpu{1}_fp16.engine'.format(len(list(total_stream_for_stremux_union)),0,get_current_dir_and_goto_parent_dir()))
                        
                    FIRESMOKEDUSTMODEL.append('labelfile-path={0}/models/wheelmodel/labels.txt'.format(get_current_dir_and_goto_parent_dir()))
                    # FIRESMOKEDUSTMODEL.append('int8-calib-file={0}/models/wheelmodel/calib.table'.format(get_current_dir_and_goto_parent_dir()))
                    FIRESMOKEDUSTMODEL.append('network-mode=2')
                    FIRESMOKEDUSTMODEL.append('num-detected-classes=1')
                    FIRESMOKEDUSTMODEL.append('interval=0')
                    FIRESMOKEDUSTMODEL.append('gie-unique-id=1')
                    FIRESMOKEDUSTMODEL.append('network-type=0')
                    FIRESMOKEDUSTMODEL.append('cluster-mode=2')
                    FIRESMOKEDUSTMODEL.append('maintain-aspect-ratio=1')
                    FIRESMOKEDUSTMODEL.append('symmetric-padding=1')
                    FIRESMOKEDUSTMODEL.append('parse-bbox-func-name=NvDsInferParseYolo')
                    FIRESMOKEDUSTMODEL.append('custom-lib-path={0}/models/yoloV8/nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so'.format(get_current_dir_and_goto_parent_dir()))
                    FIRESMOKEDUSTMODEL.append('engine-create-func-name=NvDsInferYoloCudaEngineGet')
                    FIRESMOKEDUSTMODEL.append('[class-attrs-all]')
                    FIRESMOKEDUSTMODEL.append('nms-iou-threshold=0.45')
                    FIRESMOKEDUSTMODEL.append('pre-cluster-threshold=0.3')
                    FIRESMOKEDUSTMODEL.append('topk=300')
                    with open(get_current_dir_and_goto_parent_dir()+'/models/wheelmodel/'+'{0}_{1}.txt'.format(modelconfigfile,config_index+1), 'w') as f:
                        for O_O_O, modelline in enumerate(FIRESMOKEDUSTMODEL):
                            f.write('%s\n' % modelline)

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
                    lines.append('gpu-id={0}'.format(0))
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

                elif line.strip() == '[application-config]':
                    lines.append('[application-config]')
                    lines.append('app-title = SafetyEye')
                    lines.append('image-save-path = images/frame\n')

                elif line.strip() == '[fsd]':
                    lines.append('[fsd]')
                    lines.append('enable=1')
                    lines.append('fsd-config-file=./fsd_custom_{0}.txt'.format(config_index+1))
                else:
                    lines.append(line.strip())  
        with open(config_file, 'w') as f:
            for O_O_O, item in enumerate(lines):
                f.write('%s\n' % item)

        with open(configanalytics_file, 'w') as analyticsFILE:
            for _1111, Newvlaues  in enumerate(analyticsdetailsline):
                analyticsFILE.write('%s\n' % Newvlaues)
    return allWrittenSourceCAmIds



def wheelrotationcount(live_data_count, all_data):
    try:
        data = Wheelrotationcount.find_one()
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
            result = Wheelrotationcount.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = Wheelrotationcount.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_paginqqqation 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30



def wheelrotationcount(live_data_count, all_data):
    try:
        data = Wheelrotationcount.find_one()
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
            result = Wheelrotationcount.update_one({'_id': ObjectId(data['_id'])}, {'$set':{'live_data_count': data['live_data_count'],'page_limit': data['page_limit'], 'page_num': data['page_num']}})
            if result.matched_count > 0:
                pass
            else:
                pass
        else:
            dictionary = {'live_data_count': live_data_count, 'page_limit': 10,'page_num': 1}
            result = Wheelrotationcount.insert_one(dictionary)
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
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_paginqqqation 1", str(error), " ----time ---- ", now_time_with_time()]))
        if restart_mongodb_r_service():
            print("mongodb restarted")
        else:
            if forcerestart_mongodb_r_service():
                print("mongodb service force restarted-")
            else:
                print("mongodb service is not yet started.") 
    return live_data_30

def calculate_text_size(text, font):
    font_size = font
    text_width = font_size * len(text) // 2  # Adjust as needed for accurate width estimation
    text_height = font_size 
    return text_width, text_height    



# Create your views here.


# @proofofconcept.route('/add_wheelcount_data', methods=['POST'])
@csrf_exempt
def add_wheelcount_data(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id', 'wheel_count']#,'ai_solutions']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
            else:
                id = data['id']
                tc_data = data['wheel_count']
                ai_solutions = data['ai_solutions']
                if id is not None:
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if finddata is not None:
                        if 'poc' in finddata:
                            if tc_data is not None:
                                if type(tc_data) == list:
                                    if len(tc_data) != 0:
                                        if len(tc_data) ==1:
                                            print("tc -data ", tc_data[0])
                                            fetched_tc_data =  tc_data[0]
                                            print("fetchec_wheel_count---", fetched_tc_data)
                                            if len(fetched_tc_data['class_name']) !=0:
                                                if isEmpty(fetched_tc_data['line_bbox']):
                                                    if check_dictionaryishavinganynonevalue(fetched_tc_data['line_bbox']):
                                                        if 'wheel_count' in finddata['poc']:
                                                            if check_the_tc_data_is_key_idisexist(finddata['poc']['wheel_count'],fetched_tc_data['roi_id']):
                                                                returntcdata = tc_data_modification(finddata['poc']['wheel_count'],tc_data)
                                                                if ai_solutions is not None:
                                                                    if isEmpty(ai_solutions):
                                                                        finddata['ai_solution'].update(ai_solutions)
                                                                        result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': returntcdata,'ai_solution': finddata['ai_solution']}}))
                                                                        if result.modified_count > 0:
                                                                            ret = {'message': 'wheel count data added successfully.', 'success': True}
                                                                        else:
                                                                            ret['message'] = 'wheel count data not adeed.'
                                                                    else:
                                                                        ret['message'] = 'please give proper ai_solutions, it should be object type.'
                                                                else:
                                                                    ret['message' ] = 'please give proper ai_solutions.' 
                                                            else:
                                                                ret['message']='roi key id already exists, please give different one while adding the tc data.'
                                                        else:
                                                            if ai_solutions is not None:
                                                                if isEmpty(ai_solutions):
                                                                    finddata['ai_solution'].update(ai_solutions)
                                                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': tc_data,'ai_solution': finddata['ai_solution']}}))
                                                                    if result.modified_count > 0:
                                                                        ret = {'message': 'wheel count data added successfully.', 'success': True}
                                                                    else:
                                                                        ret['message'] = 'wheel count data not adeed.'
                                                                else:
                                                                    ret['message'] = 'please give proper ai_solutions, it should be object type.'
                                                            else:
                                                                ret['message' ] = 'please give proper ai_solutions.'
                                                    else:
                                                        ret['message']='line bbox should not be have any none or empty values in dictionary.'
                                                else:
                                                    ret['message']='line bbox should not be empty dictionary.'
                                            else:
                                                ret['message']='in tc data class name should not be empty list.'
                                        else:
                                            ret['message'] ='tc data is containing multiple data objects.'
                                else:
                                    ret['message'] = 'please give proper traffic data, it should be list type.'
                            else:
                                ret['message'] = 'please give proper traffic data, it should not none type.'

                        else:
                            if ai_solutions is not None:
                                if isEmpty(ai_solutions):
                                    finddata['ai_solution'].update(ai_solutions)
                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': tc_data,'ai_solution': finddata['ai_solution']}}))
                                    if result.modified_count > 0:
                                        ret = {'message': 'wheel count data added successfully.', 'success': True}
                                    else:
                                        ret['message'] = 'wheel count data not adeed.'
                                else:
                                    ret['message'] = 'please give proper ai_solutions, it should be object type.'
                            else:
                                ret['message' ] = 'please give proper ai_solutions.' 
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
                else:
                    ret['message'] =  'give the proper mongodb id, id should not be none type.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)


# @proofofconcept.route('/edit_wheelcount_data', methods=['POST'])
@csrf_exempt
def edit_wheelcount_data(request):
    ret = {'success': False, 'message': 'something went wrong with add roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if data == None:
            data = {}
        request_key_array = ['id',  'wheel_count','roi_id','ai_solutions']
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
                tc_data = data['wheel_count']
                finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                if finddata is not None:
                    if type(tc_data) == list:
                        if len(tc_data) != 0:
                            if isEmpty(ai_solutions):
                                fetch_tc_data = finddata['poc']['wheel_count']
                                if len(fetch_tc_data) != 0:                                
                                    update_data = []
                                    finddata['ai_solution'].update(ai_solutions)
                                    for __, i in enumerate(fetch_tc_data):
                                        if i['roi_id']==roi_id:
                                            replacevalue ={}
                                            for newindex , newvalue in enumerate(tc_data):
                                                if roi_id==newvalue['roi_id']:
                                                    replacevalue=newvalue
                                            i=replacevalue
                                            update_data.append(i)
                                            
                                        else:
                                            if i not in update_data:
                                                update_data.append(i)
                                    result = (ppera_cameras.update_one({'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': update_data,'ai_solution': finddata['ai_solution']}}))
                                    if result.modified_count > 0:
                                        ret = {'message': 'wheel count data updated successfully.','success': True}
                                    else:
                                        ret['message'] = 'wheel count data not updated.'
                                else:
                                    ret['message'] = 'There is no wheel count data for the camrea, please try to add.'
                            else:
                                ret['message'] = 'ai solution should not be empty list.'
                        else:
                            ret['message'] = 'wheel count data should not be empty list.'
                    else:
                        ret['message'] = 'wheel count data should be list'
                else:
                    ret['message'] = 'for this particular id, there is no such camera data exists.'
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
    return JsonResponse(ret)


# @proofofconcept.route('/delete_wheelcount_data', methods=['POST'])
@csrf_exempt
def camera_delete_tc_data(request):
    ret = {'success': False, 'message':'something went wrong with delete_cr_data roi api'}
    if request.method == "POST":
        data = json.loads(request.body)
        if 1:
        # try:
            # data = request.json
            print('--------------------data----------',data)
            if data == None:
                data = {}
            request_key_array = ['id', 'roi_id', 'ai_solutions']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] =" ".join(["You have missed these parameters ",str(output), ' to enter. please enter properly.' ]) 
                else:
                    id = data['id']
                    roi_id = data['roi_id']
                    ai_solutions = data['ai_solutions']
                    finddata = ppera_cameras.find_one({'_id': ObjectId(id)})
                    if finddata is not None:
                        if roi_id is not None:
                            print('-----------------------akkd-----1.0----',roi_id)
                            if isEmpty(ai_solutions):
                                tc_data = finddata['poc']
                                if 'wheel_count' in tc_data:
                                    print('------------------101-------',tc_data)
                                    if isEmpty(tc_data) :
                                        update_data = []
                                        if len(tc_data['wheel_count']) == 1:
                                            finddata['ai_solution'].update(ai_solutions)
                                            result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': [], 'ai_solution':finddata['ai_solution']}})
                                            if result.modified_count > 0:
                                                ret = {'message':'wheel count data delete successfully.','success': True}
                                            else:
                                                ret['message'] = 'wheel count data not deleted.'
                                        elif len(tc_data['wheel_count']) > 1:
                                            finddata['ai_solution'].update(ai_solutions)
                                            for __, i in enumerate(tc_data['wheel_count']):
                                                if i['roi_id'] == roi_id:
                                                # if int(i['roi_id']) == int(roi_id):
                                                    pass
                                                    # tc_data.remove(i)
                                                else:
                                                    update_data.append(i)
                                            result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': update_data,'ai_solution': finddata['ai_solution']}})
                                            if result.modified_count > 0:
                                                ret = {'message': 'wheel count data delete successfully.','success': True}
                                            else:
                                                ret['message'] = 'wheel count data not deleted.'
                                    else:
                                        ret['message'] = 'There is no wheel count data region the camrea, please try to add.'
                                else:
                                    ret = {'message': 'wheel count data already empty.','success': True}

                            else:
                                print("delete tc data === ,",ai_solutions)
                                tc_data = finddata['poc.wheel_count']
                                if len(tc_data) != 0:
                                    update_data=[]
                                    if len(tc_data) == 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': [], 'ai_solution':finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'wheel count data data delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'wheel count data not deleted.'
                                    elif len(tc_data) > 1:
                                        finddata['ai_solution'].update(ai_solutions)
                                        print("tc_datatc_datatc_data==",tc_data)
                                        for __, i in enumerate(tc_data):
                                            print("---i",i)
                                            if i['roi_id'] == roi_id:
                                            # if int(i['roi_id']) == int(roi_id):
                                                pass
                                            else:
                                                update_data.append(i)
                                        result = ppera_cameras.update_one( {'_id': ObjectId(id)}, {'$set': {'poc.wheel_count': update_data,'ai_solution': finddata['ai_solution']}})
                                        if result.modified_count > 0:
                                            ret = {'message':'wheel count data  delete successfully.','success': True}
                                        else:
                                            ret['message'] = 'wheel count data not deleted.'
                                else:
                                    ret['message'] = 'There is no wheel count data in the camrea, please try to add.'
                        else:
                            ret['message'] = 'please give proper wheel count data data, it should not none type.'
                    else:
                        ret['message'] = 'for this particular id, there is no such camera data exists.'
            else:
                ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 
        # except Exception as error:
        #     ret['message'] = " ".join(["something error occurred in delete roi ",str(error), '  ----time ----   ',now_time_with_time() ]) 
        #ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_tc_data 2", str(error), " ----time ---- ", now_time_with_time()]))
    return JsonResponse(ret)



# @proofofconcept.route('/start_wheelapplication', methods=['GET'])
# @proofofconcept.route('/start_wheelapplication', methods=['POST'])
@csrf_exempt
def start_firesmoke(request):
    ret = {'message': 'something went wrong with start_wheelapplication.', 'success': False}
    if request.method in ['GET','POST']:
        if 1:
            common_return_data = wheelconfig()
            # print('common_return_data--------------------',common_return_data)
            if common_return_data:
                Wheelapp_monitoring_started(True)

                stop_application_for_firesmokeapp_creating_config()
                if common_return_data['success'] == True:
                    Wheelapp_monitoring_started(False)
                    ret = common_return_data
                else:
                    ret['message'] = common_return_data['message']
            else:
                ret['message'] = 'data not found to create config files.'
    return JsonResponse(ret)


# @proofofconcept.route('/stop_wheelapplication', methods=['GET'])
@csrf_exempt
def stop_application_1_phaseoneapp(request):
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if request.method == "GET":
        if 1:
            Wheelapp_monitoring_started(True)
            if "voice_announcement_status" not in DATABASE.list_collection_names():
                print("Collection 'voice_announcement_status' does not exist-wheelcount")
                # raise Exception("Collection 'voice_announcement_status' does not exist")
            else:
                voice_announcement_status.delete_many({"violation_type": { "$in": ["wheelcount"] }})
            ret = {'message': 'wheel monitoring app stopped.', 'success': True}
        else:
            ret = ret
    return JsonResponse(ret)


# @proofofconcept.route('/wheelcountlive', methods=['GET','POST'])
# @proofofconcept.route('/wheelcountlive/<camera_name>', methods=['GET'])#
# @proofofconcept.route('/wheelcountlive/department/<department_name>', methods=['GET'])
@csrf_exempt
def LIVEwheelcount(request,camera_name=None,department_name=None):
    ret = {'success': False,'message':"something went wrong in TrafficCountLiveCount apis"}
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
    pipeline=[]
    if request.method == 'POST':
        jsonobject = json.loads(request.body)
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

            data = list(wheelcount.aggregate(pipeline))

            if data :
                if len(data) != 0:
                    ret = {"message":data,"success":True}
                else:
                    ret['message']='data not found'
            else:
                ret['message']='data not found'
    elif request.method == 'GET':   
        print("---------------match_data---GET request--------",match_data) 
        pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                        # {'$lookup': {
                        #     'from': 'ppera_cameras',
                        #     'localField': '_id',
                        #     'foreignField': 'cameraname',
                        #     'as': 'camera_data'
                        # }},
                        # {'$unwind': '$camera_data'},
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
                                        'department': '$camera_data.department',
                                        "processing_status":'$$item.processing_status',
                                        "preset_value":'$$item.preset_value'
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
                        # {'$lookup': {
                        #     'from': 'ppera_cameras',
                        #     'localField': '_id',
                        #     'foreignField': 'cameraname',
                        #     'as': 'camera_data'
                        # }},
                        # {'$unwind': '$camera_data'},
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
                                        'department': '$camera_data.department',
                                        "processing_status":'$$item.processing_status',
                                        "preset_value":'$$item.preset_value'
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
        data = list(wheelcount.aggregate(pipeline))
        if data :
            if len(data) != 0:
                ret = {"message":data,"success":True}
            else:
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
                data = list(wheelcount.aggregate([
                                            {'$match': match_data},
                                            {'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$push': '$$ROOT'}}},
                                            {'$limit': 4000000},
                                            {'$sort': {'timestamp': -1}},
                                            {'$project': {"_id": 0, 'data': 1}},
                                            # {'$unwind': '$data'},
                                            # {
                                            #     '$lookup': {
                                            #         'from': 'ppera_cameras',
                                            #         'localField': 'data.camera_name',
                                            #         'foreignField': 'cameraname',
                                            #         'as': 'camera_data'
                                            #     }
                                            # },
                                            # {'$unwind': '$camera_data'},
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
                                                    "processing_status":'$$item.processing_status',
                                                    "preset_value":'$$item.preset_value'
                                                }
                                            }
                                        ]))

                if len(data) != 0:
                    ret = {"message":data,"success":True}
                    
                else:
                    ret['message'] = 'data not found'
        else:
            ret['message'] = 'data not found'  
    return JsonResponse(parse_json(ret))


# @proofofconcept.route('/wheelcountlive1', methods=['GET','POST'])
# @proofofconcept.route('/wheelcountlive1/<camera_name>', methods=['GET'])#
# @proofofconcept.route('/wheelcountlive1/department/<department_name>', methods=['GET'])
def testwheelcount(request,camera_name=None,department_name=None):
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

            data = list(wheelcount.aggregate(pipeline))
        
            if len(data) != 0:
                ret = {"message":data,"success":True}
            else:
                ret['message']='data not found'
    elif request.method == 'GET':   
        print("---------------match_data---GET request--------",match_data) 
        pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        # {'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                        # {'$lookup': {
                        #     'from': 'ppera_cameras',
                        #     'localField': '_id',
                        #     'foreignField': 'cameraname',
                        #     'as': 'camera_data'
                        # }},
                        # {'$unwind': '$camera_data'},
                        # {
                        # '$project': {
                        #     '_id': 0,
                        #     'data': {
                        #         '$map': {
                        #             'input': '$data',
                        #             'as': 'item',
                        #             'in': {
                        #                 'timestamp': '$$item.timestamp',
                        #                 'camera_name': '$$item.camera_name',
                        #                 '_id': '$$item._id',
                        #                 'camera_rtsp': '$$item.camera_rtsp',
                        #                 'cameraid': '$$item.cameraid',
                        #                 'count': '$$item.count',
                        #                 'date': '$$item.date',
                        #                 'direction': '$$item.direction',
                        #                 'id_no': '$$item.id_no',
                        #                 'line_metadata': '$$item.line_metadata',
                        #                 'line_name': '$$item.line_name',
                        #                 'violation_status': '$$item.violation_status',
                        #                 'violation_verificaton_status': '$$item.violation_verificaton_status',
                        #                 'department': '$camera_data.department',
                        #                 "processing_status":'$$item.processing_status',
                        #                 "preset_value":'$$item.preset_value'
                        #             }
                        #         }
                        #     }
                        # }
                        # }
                    ]
        dash_data = []
        if camera_name is not None :
            
            match_data['camera_name']= camera_name
            pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        #{'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                        # {'$lookup': {
                        #     'from': 'ppera_cameras',
                        #     'localField': '_id',
                        #     'foreignField': 'cameraname',
                        #     'as': 'camera_data'
                        # }},
                        # {'$unwind': '$camera_data'},
                        # {
                        # '$project': {
                        #     '_id': 0,
                        #     'data': {
                        #         '$map': {
                        #             'input': '$data',
                        #             'as': 'item',
                        #             'in': {
                        #                 'timestamp': '$$item.timestamp',
                        #                 'camera_name': '$$item.camera_name',
                        #                 '_id': '$$item._id',
                        #                 'camera_rtsp': '$$item.camera_rtsp',
                        #                 'cameraid': '$$item.cameraid',
                        #                 'count': '$$item.count',
                        #                 'date': '$$item.date',
                        #                 'direction': '$$item.direction',
                        #                 'id_no': '$$item.id_no',
                        #                 'line_metadata': '$$item.line_metadata',
                        #                 'line_name': '$$item.line_name',
                        #                 'violation_status': '$$item.violation_status',
                        #                 'violation_verificaton_status': '$$item.violation_verificaton_status',
                        #                 'department': '$camera_data.department',
                        #                 "processing_status":'$$item.processing_status',
                        #                 "preset_value":'$$item.preset_value'
                        #             }
                        #         }
                        #     }
                        # }
                        # }
                    ]
        
        if department_name is not None:
            pipeline = [
                        {'$match': match_data},
                        {'$sort': {'timestamp': -1}},
                        #{'$group': {'_id': '$camera_name', 'data': {'$push': '$$ROOT'}}},
                    ]            
        data = list(wheelcount.aggregate(pipeline))
        
        if len(data) != 0:
            ret = {"message":data,"success":True}
        else:
            match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
            data = list(wheelcount.aggregate([
                                        {'$match': match_data},
                                        #{'$group': {'_id': {'camera_name': '$camera_name'}, 'data': {'$push': '$$ROOT'}}},
                                        {'$limit': 4000000},
                                        {'$sort': {'timestamp': -1}},
                                        # {'$project': {"_id": 0, 'data': 1}},
                                        # {'$unwind': '$data'},
                                        # {
                                        #     '$lookup': {
                                        #         'from': 'ppera_cameras',
                                        #         'localField': 'data.camera_name',
                                        #         'foreignField': 'cameraname',
                                        #         'as': 'camera_data'
                                        #     }
                                        # },
                                        # {'$unwind': '$camera_data'},
                                        # {
                                        #     '$project': {
                                        #         'data.timestamp': '$data.timestamp',
                                        #         'data.camera_name': '$data.camera_name',
                                        #         'data._id':'$data._id',
                                        #         'data.camera_rtsp':'$data.camera_rtsp',
                                        #         'data.cameraid':'$data.cameraid',
                                        #         'data.count':'$data.count',
                                        #         'data.date':'$data.date',
                                        #         'data.direction':'$data.direction',
                                        #         'data.id_no':'$data.id_no',
                                        #         'data.line_metadata':'$data.line_metadata',
                                        #         'data.line_name':'$data.line_name',
                                        #         'data.violation_status':'$data.violation_status',
                                        #         'data.violation_verificaton_status':'$data.violation_verificaton_status',
                                        #         'data.department': '$camera_data.department',
                                        #         "processing_status":'$$item.processing_status',
                                        #         "preset_value":'$$item.preset_value'
                                        #     }
                                        # }
                                    ]))

            if len(data) != 0:
                ret = {"message":data,"success":True}
                
            else:
                ret['message'] = 'data not found!'  
    return JsonResponse(parse_json(ret))



# @proofofconcept.route('/wheelrotationlive', methods=['GET'])
# @proofofconcept.route('/wheelrotationlive/<camera_name>', methods=['GET'])
def wheelroationlivedata(request, camera_name=None):
    ret = {'success': False,'message':"something went wrong in live_data1 apis"}
    if request.method =="GET":
        if 1:    
            dash_data = []
            if camera_name is not None :
                match_data = {'timestamp':{'$regex': '^' + str(date.today())},'camera_name': camera_name}# {'$group':{'_id':{'camera_name':'$camera_name', 'analyticstype':'$analyticstype'}, 'data':{'$push':'$$ROOT'}}
                data = list(wheelrotation.aggregate([{'$match': match_data},{'$limit': 4000000}, {'$sort':{'timestamp': -1}} ]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        i['SNo'] = count+1
                        dash_data.append(i)
                    ret = wheelrotationcount(len(dash_data), parse_json(dash_data))
                else:
                    ret['message'] = 'data not found'
            else:
                match_data = {'timestamp':{'$regex': '^' + str(date.today())}}
                data = list(wheelrotation.aggregate([{'$match': match_data},                                                  
                                                    {'$limit': 4000000}    ,  {'$sort':{'timestamp': -1}}                     
                                                    ]))
                if len(data) != 0:
                    for count, i in enumerate(data):
                        i['SNo'] = count+1
                        dash_data.append(i)
                    ret =wheelrotationcount(len(dash_data), parse_json(dash_data)) 
                else:
                    ret['message'] = 'data not found'  
    return JsonResponse(ret)



# @proofofconcept.route('/wheelroationimage/<imagename>', methods=['GET'])
def wheelroationimage(request,imagename):
    if request.method =="GET":
        if 1:
        # try:
            base_path = get_current_dir_and_goto_parent_dir()+'/FLASK_into_DJANGO/images/frame'
            file_path = os.path.join(base_path, imagename)
            print("file path----------------",file_path)
            image_data = wheelrotation.find_one({'object_details.details.image_name':imagename})#({'video_file_name': imagename})
            if image_data is not None:
                if isEmpty(image_data['object_details']) :
                    imagedetaildata = image_data['object_details']
                    for i, kkkkkdkkddk in enumerate(imagedetaildata):

                        ALlimagedeta = kkkkkdkkddk['details']
                        if len(ALlimagedeta) !=0:
                            for imageindex , imaged in enumerate(ALlimagedeta):
                                if imaged['image_name']==imagename:
                                    source_img = Image.open(file_path)
                                    draw = ImageDraw.Draw(source_img)
                                    if len(imaged['obj_details']) !=0:
                                        for j,lkkkbbox in enumerate(imaged['obj_details']):
                                            # print('----------lkkkbbox-------',lkkkbbox)
                                            Vestheight = lkkkbbox['H']
                                            Vestwidth = lkkkbbox['W']
                                            Vestx_value = lkkkbbox['X']
                                            Vesty_value = lkkkbbox['Y']     
                                            # Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                                            # Vestshape = [(Vestx_value, Vestx_value),(Vestx_value+Vestwidth, Vesty_value+Vestheight)]
                                            Vestshape = [(Vestx_value, Vesty_value), (Vestwidth , Vestheight )]
                                            text_width,text_height = calculate_text_size(lkkkbbox['name'].upper(),20)                                    
                                            text_x = Vestx_value + 6
                                            text_y = Vesty_value + Vestheight    
                                            text_position = (Vestx_value + 6, Vesty_value + Vestheight)
                                            text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + 10, text_position[1] + text_height )
                                            # text_bg_position = (text_position[0] , text_position[1] , text_position[0] + text_position[1] + 10+(len(lkkkbbox['name'].upper())), text_y + text_height )
                                            # draw.rectangle(text_bg_position, fill='black')
                                            # draw.rectangle(text_bg_position, fill='black')              
                                            
                                            # draw.rectangle(text_bg_position, fill='black')
                                            # draw.rectangle(text_bg_position, fill=(0, 0, 0, 128)) 
                                            draw.rectangle(Vestshape, outline=(127, 255, 0), width=6)#127, 255, 0#(34, 139, 34)
                                            draw.text((Vestx_value + 6, Vesty_value + 2), lkkkbbox['name'].upper(), (127, 255, 0), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',20, encoding='unic')) 
                                        imgByteArr = io.BytesIO()
                                        source_img.save(imgByteArr, format='JPEG')
                                        imgByteArr.seek(0)
                                    response = HttpResponse(imgByteArr, content_type='image/jpeg')
    
                                    # Set the 'Content-Disposition' header to suggest the image should be downloaded
                                    response['Content-Disposition'] = f'attachment; filename="{imagename}"'

                                    return response
                
                else:
                
                    if os.path.exists(file_path):
                        # Open the file in binary mode and return it as an attachment
                        with open(file_path, 'rb') as f:
                            return FileResponse(f, as_attachment=True, filename=imagename)
                    else:
                        # If the file doesn't exist, return an error message
                        return JsonResponse({'success': False, 'message': 'File not found.'})
            # return JsonResponse({'success': False, 'message': 'given image data not found.'}) 
            if os.path.exists(file_path):
                        # Open the file in binary mode and return it as an attachment
                f=open(file_path, 'rb') 
                return FileResponse(f, as_attachment=True, filename=imagename)
            else:
                        # If the file doesn't exist, return an error message
                return JsonResponse({'success': False, 'message': 'File not found.'})                      
        # except Exception as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- get_roi_image 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     return str(error)