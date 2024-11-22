from Data_recieving_and_Dashboard.packages import *
# from Data_recieving_and_Dashboard.smartrecord_config_function import *

smart_config = Blueprint('smart_config', __name__)


def FETCHTHEONLYCOINIDDATA():
    data = []
    fetch_require_data = mongo.db.ppera_cameras.find({'camera_status': True,"alarm_type":"sensegiz","coin_details": { "$exists": True,"$type": 'array', "$not": {"$size": 0} }})
    for i in fetch_require_data:
        data.append(i)
    print("data === ", len(data))
    return data


def update_cam_id_common_app(update_cam_ids_data):
    for RRR, total_data in enumerate(update_cam_ids_data):
        final_data_camera_name = total_data['cameraname']
        final_rtsp_url = total_data['rtsp_url']
        update_camera_id = total_data['cameraid']
        result_data = mongo.db.ppera_cameras.find_one({'rtsp_url': final_rtsp_url, 'cameraname': final_data_camera_name})
        if result_data is not None:
            result_data['_id'] = str(result_data['_id'])
            id = result_data['_id']
            result = mongo.db.ppera_cameras.update_one({'_id': ObjectId(id),'rtsp_url': final_rtsp_url}, {'$set':{'cameraid':  update_camera_id}})
            if result.matched_count > 0:
                pass
            else:
                pass
    return '200'

def WRITESMARTRECORDFILE(response):
    sample_config_file = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', 'smaplesmartrecord.txt')
    deepstream_config_path = get_current_dir_and_goto_parent_dir()+'/smart_record'+'/configs'
    isExist = os.path.exists(deepstream_config_path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(deepstream_config_path)
    config_file = os.path.join(deepstream_config_path, 'config.txt')
    lines = ['[property]', 'enable=1', 'config-width=960','config-height=544', 'osd-mode=2', 'display-font-size=12', '']
    index = 0
    require_data = []
    normal_config_file = 0
    for Cherry, x in enumerate(response):
        if x['camera_status'] == True:
            x['cameraid'] = int(index) + 1
            require_data.append(x)
        index += 1
    total_stream_for_stremux_union = str(len(response))
    lines = []
    with open(sample_config_file) as file:
        for write_config, line in enumerate(file):
            if line.strip() == '[application]':
                lines.append('[application]')
                lines.append('enable-perf-measurement=0')
                lines.append('perf-measurement-interval-sec=5')
            
            elif line.strip() == '[tiled-display]':
                num = math.sqrt(int(len(response)))
                if 1 < num < 1.4:
                    rows = 1
                    columns = 2
                elif num == 1:
                    rows = 1
                    columns = 1
                else:
                    rows = int(round(num))
                    columns = int(round(num))
                
                lines.append('[tiled-display]')
                lines.append('enable=1')
                lines.append('rows={0}'.format(str(rows)))
                lines.append('columns={0}'.format(str(columns)))
                lines.append('width=960')
                lines.append('height=544')
                lines.append('gpu-id=0')
                lines.append('nvbuf-memory-type=0')
            
            elif line.strip() == '[sources]':
                source_added = []
                normal_config_file = 0

                for n, x in enumerate(require_data):
                    cam_id = '{0}'.format(int(n) + 1)
                    find_data = mongo.db.rtsp_flag.find_one({}, sort=[('_id', pymongo.DESCENDING)])

                    if find_data is not None:
                        if find_data['rtsp_flag'] == '1':
                            if 'rtsp' in x['rtsp_url']:
                                x['rtsp_url'] = x['rtsp_url'].replace('rtsp','rtspt')
                    
                    if 1:
                        uri = x['rtsp_url']
                        lines.append('[source{0}]'.format(str(normal_config_file)))
                        lines.append('enable=1')
                        lines.append('type=4')
                        lines.append('uri = {0}'.format(uri))
                        lines.append('num-sources=1')
                        lines.append('gpu-id=0')
                        lines.append('nvbuf-memory-type=0')
                        lines.append('latency=500')
                        lines.append('camera-id={0}'.format(int(n) + 1))
                        lines.append('camera-name={0}'.format(x['cameraname']))
                        # lines.append('drop-frame-interval = 3\n')
                        # lines.append('smart-record=2')
                        # lines.append('smart-rec-video-cache= 70')
                        # lines.append('smart-rec-duration= 3600')
                        # lines.append('smart-rec-default-duration= 3600')
                        # lines.append('smart-rec-container= 0')
                        # lines.append('smart-rec-interval= 1')
                        # lines.append('smart-rec-file-prefix=sm_rec_CAM')
                        # lines.append('smart-rec-dir-path= images/sm_rec')
                        # lines.append('smart-rec-start-time = 60')
                        lines.append('smart-record=2')
                        lines.append('smart-rec-video-cache= 10')
                        lines.append('smart-rec-duration= 370')
                        lines.append('smart-rec-default-duration= 370')
                        lines.append('smart-rec-container= 0')
                        lines.append('smart-rec-interval= 1')
                        lines.append('smart-rec-file-prefix=sm_rec_CAM')
                        lines.append('smart-rec-dir-path= images/sm_rec')
                        lines.append('smart-rec-start-time = 10')
                        normal_config_file += 1
                        source_added.append(int(n) + 1)
            
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
                lines.append('batch-size={0}'.format(len(list(total_stream_for_stremux_union))))
                lines.append('batched-push-timeout=40000')
                lines.append('width=1920')
                lines.append('height=1080')
                lines.append('enable-padding=0')
                lines.append('nvbuf-memory-type=0')
            
            elif line.strip() == '[primary-gie]':
                lines.append('[primary-gie]')
            
            elif line.strip() == '[tracker]':
                lines.append('[tracker]')
            
            elif line.strip() == '[tests]':
                lines.append('[tests]')
            
            elif line.strip() == '[docketrun-image]':
                lines.append('[docketrun-image]') 
            else:
                lines.append(line.strip())
    with open(config_file, 'w') as f:
        for O_O_O, item in enumerate(lines):
            f.write('%s\n' % item)
            
    return require_data


def CHECKUPDATECAMERAID():
    ret = {'message':'something went wrong with create config update_cam_id__.','success': False}
    getdata_response = FETCHTHEONLYCOINIDDATA()
    if len(getdata_response) != 0:
        function__response = WRITESMARTRECORDFILE(getdata_response)
        return_data_update_camera = update_cam_id_common_app(function__response)
        if return_data_update_camera == '200':
            ret = {'message':'smart record config files are created successfully.', 'success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'there is no data found for create config file '
    return ret

@smart_config.route('/create_smart_config', methods=['GET'])
def COMMONCREATECONFIG():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        common_return_data = CHECKUPDATECAMERAID()
        print("common_return_data", common_return_data)
        if common_return_data['success']:
            # print("FUN RESPONSE:", common_return_data)
            SET_SMART_RECORDING_monitoring_started(True)
            stop_smartrecordapp_creating_config()
            if common_return_data['success'] == True:
                SET_SMART_RECORDING_monitoring_started(False)
                ret = common_return_data
            else:
                ret['message' ] = 'some thing went wrong  creating config files.'
        else:
            print("")
            ret=common_return_data
    else:
        ret = ret
    return ret




@smart_config.route('/stop_smart_record', methods=['GET'])
def stop_application_1_app_common():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        SET_SMART_RECORDING_monitoring_started(True)
        ret = {'message': 'application stopped.', 'success': True}
    else:
        ret = ret
    return ret

