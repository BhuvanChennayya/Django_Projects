from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_config_funcs import *
import math

create_hydra_config = Blueprint('create_hydra_config', __name__)


def hydra_data(all_data, hydro_datas, hooter_line, index, roi_label_names, label_name_for_hooter, roi_enable_cam_ids, lines, traffic_count_cls_name_cls_id):
    for test_roi_ra, hydrolic_value in enumerate(all_data):
        if len(all_data) != 0:
            roi_enable_cam_ids.append(index)
            hooter_line.append('[hydra{0}]'.format(str(index)))
            hooter_line.append('enable = 1')
            hooter_line.append("operate-on-label = lock;")
            hooter_line.append("lock-on-verify-time = 10")
            hooter_line.append("lock-off-verify-time = 10\n")

        else:
            roi_enable_cam_ids.append(index)
            hooter_line.append('[hydra{0}]'.format(str(index)))
            hooter_line.append('enable = 0')
            hooter_line.append("operate-on-label = lock;")
            hooter_line.append("lock-on-verify-time = 10")
            hooter_line.append("lock-off-verify-time = 10\n")

        lines.append('[roi-filtering-stream-{0}]'.format(index))
        lines.append('enable=1')
        hydraulic_data = hydrolic_value['hydraulic_data']
        for hydro_key, hydro_value in enumerate(hydraulic_data):
            lines.append('roi-HYDRA-{0} = {1}'.format(hydro_value['panel_no'], hydro_value['bbox']))
        
        index +=1
        lines.append('\n')
    return roi_enable_cam_ids

def write_connfig1_common_app(response):
    print('-------------------------length--------------',len(response))
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'sample_config_hydrolic.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir() + '/docketrun_app_hydra/configs/'
    isExist = os.path.exists(deepstream_config_path)
    if not isExist:
        os.makedirs(deepstream_config_path)

    config_file = os.path.join(deepstream_config_path, 'config.txt')
    config_analytics_file = os.path.join(deepstream_config_path,'config_analytics.txt')
    hooter_config_file_path = os.path.join(deepstream_config_path,'config_hydra.txt')
    lines = ['[property]', 'enable=1', 'config-width=960','config-height=544', 'osd-mode=2', 'display-font-size=12', '']
    index = 0
    require_hydro_data = []
    roi_enable_cam_ids = []
    roi_label_names = []
    normal_config_file = 0
    label_name_for_hooter = []
    hooter_line = []
    traffic_count_cls_name_cls_id = {"truck":"0", "car":"1", "person":"2", "bike":"3"}
    uniqui_rtsp = []
    for Cherry, x in enumerate(response):
        if isEmpty(x):
            # print('-------------------response==============',response)
            if x['ip_address'] not in uniqui_rtsp:
                uniqui_rtsp.append(x['ip_address'])
            
            if "hydraulic_data" in x:
                if len(x['hydraulic_data']):
                    for hydra_bbox_idx, hydra_bbox in enumerate(x["hydraulic_data"]):
                        x['cameraid'] = int(index) + 1
                        if x not in require_hydro_data:
                            require_hydro_data.append(x)
                elif "pneumatic_data" in x :
                    print('-------------------pneumatic_data==============',x)
                    x["hydraulic_data"] = x["pneumatic_data"]
                    for hydra_bbox_idx, hydra_bbox in enumerate(x["hydraulic_data"]):
                        x['cameraid'] = int(index) + 1
                        if x not in require_hydro_data:
                            require_hydro_data.append(x)
            elif "pneumatic_data" in x or 'Pneumatic' in x:
                print('-------------------pneumatic_data==============',x)
                x["hydraulic_data"] = x["pneumatic_data"]
                for hydra_bbox_idx, hydra_bbox in enumerate(x["hydraulic_data"]):
                    x['cameraid'] = int(index) + 1
                    if x not in require_hydro_data:
                        require_hydro_data.append(x)
    roi_fun_with_cr_fun = hydra_data(require_hydro_data, x, hooter_line, index, roi_label_names, label_name_for_hooter, roi_enable_cam_ids, lines, traffic_count_cls_name_cls_id)
    roi_enable_cam_ids = roi_fun_with_cr_fun
    print("hydra ip-address", uniqui_rtsp)
    total_stream_for_stremux_union =uniqui_rtsp #list(set().union(roi_enable_cam_ids))

    with open(config_analytics_file, 'w') as f:
        for item in lines:
            f.write('%s\n' % item)

    with open(hooter_config_file_path, 'w') as hooter_file:
        for jim in hooter_line:
            hooter_file.write('%s\n' % jim)

    lines = []
    with open(sample_config_file) as file:
        for write_config, line in enumerate(file):
            if line.strip() == '[application]':
                lines.append('[application]')
                lines.append('enable-perf-measurement=0')
                lines.append('perf-measurement-interval-sec=5\n')
            
            elif line.strip() == '[tiled-display]':
                num = math.sqrt(int(len(roi_enable_cam_ids)))
                print("TILED DISPLY NUM:-", num)
                if len(roi_enable_cam_ids) == 1 or len(roi_enable_cam_ids) == 2:
                    rows = 1
                    columns = 2                 
                elif len(roi_enable_cam_ids) == 3 or len(roi_enable_cam_ids) == 4:
                    rows =2 
                    columns =2 
                
                elif len(roi_enable_cam_ids) == 5 or len(roi_enable_cam_ids) == 6:
                    rows =2
                    columns =3
                elif len(roi_enable_cam_ids) == 7 or len(roi_enable_cam_ids) == 8:
                    rows =2 
                    columns =4 
                elif len(roi_enable_cam_ids) == 9 or len(roi_enable_cam_ids) == 10 :
                    rows =2 
                    columns =5

                if len(roi_enable_cam_ids) == 11 or len(roi_enable_cam_ids) == 12:
                    rows = 3
                    columns = 4                 
                elif len(roi_enable_cam_ids) == 13 or len(roi_enable_cam_ids) == 14:
                    rows =3 
                    columns =5                 
                elif len(roi_enable_cam_ids) == 15 or len(roi_enable_cam_ids) == 16:
                    rows =4
                    columns =4
                elif len(roi_enable_cam_ids) == 17 or len(roi_enable_cam_ids) == 18:
                    rows =4
                    columns =5 
                elif len(roi_enable_cam_ids) == 19 or len(roi_enable_cam_ids) == 20 :
                    rows =4 
                    columns =5
               

                # if 1 < num < 1.4:
                #     rows = 1
                #     columns = 2
                # elif num == 1:
                #     rows = 1
                #     columns = 1
                # else:
                #     rows = int(round(num))
                #     columns = int(round(num))
                
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

                for n, xc in enumerate(require_hydro_data):
                    cam_id = '{0}'.format(int(n) + 1)
                    roi_enable_cam_ids_exist = roi_enable_cam_ids.count(int(cam_id))

                    if int(n) + 1 not in source_added:
                        uri = xc['rtsp_url']
                        lines.append('[source{0}]'.format(normal_config_file))
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
                        lines.append('camera-name={0}'.format(xc['camera_name']))
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
                lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                lines.append('batched-push-timeout=40000')
                lines.append('width=1920')
                lines.append('height=1080')
                lines.append('enable-padding=0')
                lines.append('nvbuf-memory-type=0\n')
            
            elif line.strip() == '[primary-gie]':
                lines.append('[primary-gie]')
                lines.append('enable=1')
                lines.append('gpu-id=0')
                lines.append('batch-size=4')
                lines.append('bbox-border-color0=0;1;0;1.0')
                lines.append('bbox-border-color1=0;1;1;0.7')
                lines.append('bbox-border-color2=0;1;0;0.7')
                lines.append('bbox-border-color3=0;1;0;0.7')
                lines.append('nvbuf-memory-type=0')
                lines.append('interval=0')
                lines.append('gie-unique-id=1')
                lines.append('config-file = ../../models/config_infer_primary_vgg16_lock.txt\n')

                lines.append('[secondary-gie0]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 5')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('config-file = ../../models/classification_vest.txt\n')

                lines.append('[secondary-gie1]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 4')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('config-file = ../../models/classification_helmet.txt\n')

                lines.append('[secondary-gie2]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 6')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('bbox-border-color0 = 0;0;0;0.7')
                lines.append('bbox-border-color1 = 1;0;0;0.7')
                lines.append('config-file = ../../models/config_infer_secandary_helmet_v2.txt\n')

                lines.append('[secondary-gie3]')
                lines.append('enable = 0')
                lines.append('gpu-id = 0')
                lines.append('gie-unique-id = 7')
                lines.append('operate-on-gie-id = 1')
                lines.append('operate-on-class-ids = 0;')
                lines.append('batch-size = 1')
                lines.append('bbox-border-color0 = 1;0;1;0.7')
                lines.append('bbox-border-color1 = 1;0;0;0.7')
                lines.append('config-file = ../../models/config_infer_secandary_arc_jacket_v2_pruned_16_02_23.txt\n')

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
                # lines.append("ll-config-file=/opt/nvidia/deepstream/deepstream-6.4/samples/configs/deepstream-app/config_tracker_NvDCF_perf.yml")
                # lines.append('ll-lib-file=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_mot_klt.so')
                lines.append('gpu-id=0\n')
                # lines.append('enable-batch-process=0\n')
            
            elif line.strip() == '[nvds-analytics]':
                lines.append('[nvds-analytics]')
                lines.append('enable = 1')
                lines.append('config-file = ./config_analytics.txt\n')
            
            elif line.strip() == '[tests]':
                lines.append('[tests]')
                lines.append('file-loop=1\n')
                lines.append('[docketrun-device]')
                lines.append('gui-title = DOCKETRUN VA - 1 - TSK SYSTEM')
                lines.append('data-upload = 1\n')
            
            elif line.strip() == '[docketrun-analytics]':
                lines.append('[docketrun-analytics]')
                lines.append('smart-record-stop-buffer = 2\n')
            
            elif line.strip() == '[application-config]':
                lines.append('[application-config]')
                lines.append('image-save-path = images/hydra')
                lines.append('app-title = SafetyEye 1 to 1\n')
            
            elif line.strip() == '[docketrun-image]':
                lines.append('[docketrun-image]')
                lines.append('frame-enable = 1')
                lines.append('frameimg-folder = images/hydra')
                lines.append('frame-save-interval = 5')
                lines.append('image-save-prefix = Tata_steel_kalinganagar\n')

                lines.append('[hydraulic]')
                if len(require_hydro_data) != 0:
                    lines.append('enable = 1')

                else:
                    lines.append('enable = 0')

                lines.append('config-file = ./config_hydra.txt\n')

    with open(config_file, 'w') as f:
        for O_O_O, item in enumerate(lines):
            f.write('%s\n' % item)
            
    return require_hydro_data

def update_cam_id_common_app(update_cam_ids_data):
    camera_ids = []
    for RRR, total_data in enumerate(update_cam_ids_data):
        final_rtsp_url = total_data['rtsp_url']
        update_camera_id = total_data['camera_id']
        camera_ids.append(update_camera_id)
        result_data = mongo.db.ppera_cameras.find_one({'rtsp_url': final_rtsp_url})
        if result_data is not None:
            result_data['_id'] = str(result_data['_id'])
            id = result_data['_id']
            result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id),'rtsp_url': final_rtsp_url}, {'$set':{'cameraid':  update_camera_id}})
            if result.matched_count > 0:
                pass
            else:
                pass
    return '200'

def update_cam_id1__common_app():
    ret = {'message':'something went wrong with create config update_cam_id__.','success': False}
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
    if sheet_data is not None:
        job_sheet_name = sheet_data['job_sheet_name']
        sheet_token = sheet_data['token']
        getdata_response_1 = list(mongo.db.panel_data.find({'job_sheet_name': job_sheet_name, 'token': sheet_token, "$or": [ { "type": "Hydraulic" } , { "type": "hydraulic" },{ "type": "Pneumatic" }, { "type": "pneumatic" } ]}, sort=[('_id', pymongo.DESCENDING)]))
        if len(getdata_response_1) != 0:
            getdata_response = []
            for d in getdata_response_1:
                getdata_response.append(d['data'])

            if len(getdata_response) != 0:
                function__response = write_connfig1_common_app(getdata_response)
                return_data_update_camera = update_cam_id_common_app(function__response)
                if return_data_update_camera == '200':
                    ret = {'message':'hydra config files are created successfully.', 'success': True}
                else:
                    ret = {'message': 'camera id not updated .', 'success': False}
            else:
                ret['message'] = 'there is no data found for create config file '
        else:
                ret['message'] = 'there is no data found for create config file '
    else:
        ret ={'message': 'camera id not updated .', 'success': False}
    return ret

@create_hydra_config.route('/create_hydra_config', methods=['GET'])
def HYDRACREATECONFIG():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        common_return_data = update_cam_id1__common_app()
        if common_return_data['success']:
            SET_HYDRAAPP_monitoring_started(True)
            # stop_MECHHYDRA_creating_config()
            if common_return_data['success'] == True:
                SET_HYDRAAPP_monitoring_started(False)
                ret = common_return_data
            else:
                ret['message' ] = 'some thing went wrong  creating config files.'
        else:
            ret=common_return_data#['message'] = 'data not found to create config files.'
    else:
        ret = ret
    return ret


@create_hydra_config.route('/stop_hydraapp', methods=['GET'])
def stop_application_1_app_esi():
    ret = {'message': 'something went wrong with create config.', 'success':  False}
    if 1:
        SET_HYDRAAPP_monitoring_started(True)
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret



def MechHydrconfig_ESI():
    ret = {'message':'something went wrong with create config update_cam_id__.','success': False}
    sheet_data = mongo.db.mechjob_sheet.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
    if sheet_data is not None:
        job_sheet_name = sheet_data['job_sheet_name']
        sheet_token = sheet_data['token']
        getdata_response_1 = list(mongo.db.mechesi.find({'job_sheet_name': job_sheet_name, 'token': sheet_token, "$or": [ { "type": "Hydraulic" } , { "type": "hydraulic" },{ "type": "Pneumatic" }, { "type": "pneumatic" } ]}, sort=[('_id', pymongo.DESCENDING)]))
        
        
        # print('-----------;getdata_response_1',getdata_response_1)
        if len(getdata_response_1) != 0:
            getdata_response = []
            for d in getdata_response_1:
                # print('--------------------------',d)
                if 'data' in d :
                    # print('----------------------------------------2')
                    if isEmpty(d['data']): 
                        # print('----------------------------------------3')
                        getdata_response.append(d['data'])

            print('----------------------getdata_response3333-----',getdata_response)
            if len(getdata_response) != 0:
                function__response = write_connfig1_common_app(getdata_response)
                return_data_update_camera = update_cam_id_common_app(function__response)
                if return_data_update_camera == '200':
                    ret = {'message':'hydra config files are created successfully.', 'success': True}
                else:
                    ret = {'message': 'camera id not updated .', 'success': False}
            else:
                ret['message'] = 'there is no data found for create config file '
        else:
                ret['message'] = 'there is no data found for create config file '
    else:
        ret ={'message': 'camera id not updated .', 'success': False}
    return ret





@create_hydra_config.route('/Mechcreate_hydra_config', methods=['GET'])
def Mechcreate_hydra_config():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        common_return_data = MechHydrconfig_ESI()
        if common_return_data['success']:
            SET_HYDRAAPP_monitoring_started(True)
            # stop_MECHHYDRA_creating_config()
            if common_return_data['success'] == True:
                SET_HYDRAAPP_monitoring_started(False)
                ret = common_return_data
            else:
                ret['message' ] = 'some thing went wrong  creating config files.'
        else:
            ret=common_return_data#['message'] = 'data not found to create config files.'
    else:
        ret = ret
    return ret


@create_hydra_config.route('/Mechstop_hydraapp', methods=['GET'])
def Mechstop_hydraapp():
    ret = {'message': 'something went wrong with create config.', 'success':  False}
    if 1:
        SET_HYDRAAPP_monitoring_started(True)
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret