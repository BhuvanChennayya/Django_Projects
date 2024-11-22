from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.dashboard_apis import dashboard
# from Data_recieving_and_Dashboard.camera_api import camera_details
from Data_recieving_and_Dashboard.camera_coin_apis import camera_coin
from Data_recieving_and_Dashboard.camera_status_api import camera_status
from Data_recieving_and_Dashboard.verify_excel_data_apis import check_camera
from Data_recieving_and_Dashboard.multi_isolation_jobs import job_sheet_api
from Data_recieving_and_Dashboard.alertemails import alertemails
from Data_recieving_and_Dashboard.write_hydra_config_file import create_hydra_config
from Data_recieving_and_Dashboard.write_config_file import creat_config
from Data_recieving_and_Dashboard.smartrecord_config_write import smart_config
from Data_recieving_and_Dashboard.steamsuitapis import steamsuit
from Data_recieving_and_Dashboard.analysis_data import violationanalysis_data
from Data_recieving_and_Dashboard.users import use
from Data_recieving_and_Dashboard.admin import *
from Data_recieving_and_Dashboard.super_admin import super_admin
from Data_recieving_and_Dashboard.firesmokeconfig import firesmoke
from Data_recieving_and_Dashboard.spillage_apis import spillage
from Data_recieving_and_Dashboard.mechESI import mechesi
from Data_recieving_and_Dashboard.joblinkage import linkagetofieldjob
from Data_recieving_and_Dashboard.implimentingsockets import socketio_bp,init_socketio
from Data_recieving_and_Dashboard.vpmsconfig import vehicle_parking
from Data_recieving_and_Dashboard.write_vpms_config import create_vpms_config
from Data_recieving_and_Dashboard.write_traffic_jam_config import create_traffic_jam_config
from Data_recieving_and_Dashboard.parking_management import parking_manage_data
from Data_recieving_and_Dashboard.traffic_jam_management import traffic_jam_management
from Data_recieving_and_Dashboard.poc import proofofconcept
from Data_recieving_and_Dashboard.voiceannoucement import voice_wifi
# analysis_data
# import logging

# # logging.basicConfig(filename='record.log', level=logging.DEBUG)
# logging.basicConfig(filename='record.log',
#                 level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)
cors = CORS(app, resources={'*': {'origins': '*'}}, supports_credentials=True)
socketio = SocketIO(app, async_mode='gevent',cors_allowed_origins='*', transports=['websocket', 'polling'])
#socketio2= SocketIO(app,async_mode='gevent',cors_allowed_origins='*', transports=['websocket', 'polling'])
# socketio = SocketIO(app, cors_allowed_origins="*")
#socketio1.init_app(app)
#socketio2.init_app(app)
# init_socketio(app)
# Debug(app)
app.debug = True

app.register_blueprint(socketio_bp)
app.register_blueprint(dashboard)
# app.register_blueprint(camera_details)
app.register_blueprint(camera_coin)
app.register_blueprint(camera_status)
app.register_blueprint(check_camera)
app.register_blueprint(job_sheet_api)
app.register_blueprint(alertemails)
app.register_blueprint(create_hydra_config)
app.register_blueprint(creat_config)
app.register_blueprint(smart_config)
app.register_blueprint(steamsuit)
app.register_blueprint(violationanalysis_data)
app.register_blueprint(firesmoke)
app.register_blueprint(spillage)

app.register_blueprint(use)
app.register_blueprint(admin)
app.register_blueprint(super_admin)
app.register_blueprint(mechesi)
app.register_blueprint(linkagetofieldjob)
app.register_blueprint(vehicle_parking)
app.register_blueprint(create_traffic_jam_config)
app.register_blueprint(parking_manage_data)
app.register_blueprint(traffic_jam_management)
app.register_blueprint(create_vpms_config)
app.register_blueprint(proofofconcept)
app.register_blueprint(voice_wifi)

app.config['FLASK_DEBUG_DISABLE_STRICT'] = True
app.config['SECRET_KEY'] = '123nagashanti123@'
app.config['MONGO_DBNAME'] = 'DOCKETRUNDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/DOCKETRUNDB'
init_socketio(app)
mongo.init_app(app)

# CORS(app)

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    return response


def set_mongodb_name(db_name='xx'):
    global savefiles_foldername
    savefiles_foldername = 'images/' + db_name
    app.config['MONGO_DBNAME'] = db_name
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/' + app.config['MONGO_DBNAME']
    mongo.init_app(app)


@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'success': 'false', 'message':
        'Ohh Snap! Double Check Your URL'}), 404)


@app.errorhandler(500)
def error500(error):
    return make_response(jsonify({'success': 'false', 'message':'Ohh Snap! Double Check Your URL'}), 500)


@app.errorhandler(405)
def error405(error):
    return make_response(jsonify({'success': 'false', 'message':'Incorrect Method Used, Change The Method .'}), 400)


def turn_hooter_on_turn_hooter_off(result_data):
    if result_data['alarm_type'] == 'hooter':
        url = 'http://' + result_data['alarm_ip_address'] + '/ON'
        # try:
        #     response = requests.get(url)
        # except Exception as error:
        #ERRORLOGdata(" ".join(["\n", "[ERROR] main_api -- turn_hooter_on_turn_hooter_off 1", str(error), " ----time ---- ", now_time_with_time()])) 
    if result_data['alarm_type'] == 'relay':
        url = 'http://' + result_data['alarm_ip_address'] + '/ON'
        # try:
        #     response = requests.get(url)
        # except Exception as error:
        #ERRORLOGdata(" ".join(["\n", "[ERROR] main_api -- turn_hooter_on_turn_hooter_off 2", str(error), " ----time ---- ", now_time_with_time()])) 


def update_hooter_data_to_db(result_data):
    try:
        mongo.db.hooter_on_table.update_one({'_id': ObjectId(result_data['_id'])}, {'$set': {'hooter_status': 'on', 'hooter_time':now_time_with_time()}})
        turn_hooter_on_turn_hooter_off(result_data)
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] main_api -- update_hooter_data_to_db 1", str(error), " ----time ---- ", now_time_with_time()])) 


def dump_hooter_data_To_db(result_data):
    try:
        del result_data['_id']
        del result_data['camera_brand']
        del result_data['rtsp_port']
        del result_data['plant']
        del result_data['password']
        del result_data['username']
        del result_data['area']
        del result_data['imagename']
        del result_data['image_height']
        del result_data['image_width']
        del result_data['cameraid']
        del result_data['roi_data']
        del result_data['tc_data']
        del result_data['cr_data']
        del result_data['ppe_data']
        del result_data['ai_solution']
        del result_data['timestamp']
        del result_data['camera_status']
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] main_api -- dump_hooter_data_To_db 1", str(error), " ----time ---- ", now_time_with_time()]))
    result_data['hooter_status'] = 'on'
    result_data['hooter_time'] = now_time_with_time()
    result = mongo.db.hooter_on_table.insert_one(result_data)
    if result.acknowledged > 0:
        ret = {'message': 'hooter data inserted .', 'success': True}
    else:
        ret['message'] = 'hooter data not inserted.'
    turn_hooter_on_turn_hooter_off(result_data)


def check_todays_date(time_stamp_data):
    from datetime import datetime, timedelta
    if time_stamp_data > now_time_with_time_minus():
        return True
    else:
        return False


def hooter__function(data):
    if data is not None:
        if data['analyticstype'] == 'RA':
            check_time_now_time = check_todays_date(data['timestamp'])
            if check_time_now_time:
                result_data = mongo.db.ppera_cameras.find_one({'rtsp_url':
                    data['camera_rtsp'], 'cameraname': data['camera_name']})
                if result_data is not None:
                    if result_data['alarm_ip_address'] is not None:
                        hooter_on_of = mongo.db.hooter_on_table.find_one({'rtsp_url': data['camera_rtsp'], 'cameraname': data['camera_name']})
                        if hooter_on_of is not None:
                            if hooter_on_of['hooter_status'] == 'off':
                                update_hooter_data_to_db(hooter_on_of)
                            elif hooter_on_of['hooter_status'] == 'on':
                                time_dif = get_time_in_seconds( now_time_with_time(), hooter_on_of['hooter_time'])
                                config_time = hooter_time_set()
                                if time_dif > int(config_time):
                                    update_hooter_data_to_db(hooter_on_of)
                            else:
                                print('Result is none')
                        elif hooter_on_of is None:
                            dump_hooter_data_To_db(result_data)
                    else:
                        print('alarm ip address is none')
                else:
                    pass
            else:
                print( '----------------- Previous data--- hooter --------------- ')
        elif data['analyticstype'] == 'ONB':
            check_time_now_time = check_todays_date(data['timestamp'])
            if check_time_now_time:
                result_data = mongo.db.ppera_cameras.find_one({'rtsp_url':data['camera_rtsp'], 'cameraname': data['camera_name']})
                if result_data is not None:
                    hooter_on_of = mongo.db.hooter_on_table.find_one({ 'rtsp_url': data['camera_rtsp'], 'cameraname': data['camera_name']})
                    if hooter_on_of is not None:
                        if hooter_on_of['hooter_status'] == 'off':
                            update_hooter_data_to_db(hooter_on_of)
                        elif hooter_on_of['hooter_status'] == 'on':
                            time_dif = get_time_in_seconds(now_time_with_time(), hooter_on_of['hooter_time'])
                            config_time = hooter_time_set()
                            if time_dif > int(config_time):
                                update_hooter_data_to_db(hooter_on_of)
                    elif hooter_on_of is None:
                        dump_hooter_data_To_db(result_data)
                else:
                    pass
            else:
                print('----------------- Previous data--- hooter --------------- ')
    return 'hooter on'


@app.route('/data_upload', methods=['POST'])
def HONDA_data_upload():
    if 1:
        ret = {'success': False, 'message': 'An unexpected error has occurred, please try again later'}
        data1 = request.json
        x = mongo.db.data.find_one({'appruntime': data1['appruntime'],  'imagename': {'$all': data1['imagename']}})
        if x is not None:
            print('updated')
            mongo.db.data.update_one({'imagename': {'$all': data1['imagename']}}, {'$set': {'object_data': data1['object_data']}} )
            ret = 'updated '
        else:
            ret = 'inserted '
            data1['violation_status'] = True
            data1['violation_verificaton_status'] = False
            result = mongo.db.data.insert_one(data1)
            if result.acknowledged > 0:
                ret = {'message': 'violation data inserted successfully.','success': True}
            else:
                ret['message'] = 'violation data is not inserted.'
        return ret


@app.route('/riro_data', methods=['POST'])
def riro_data_data_upload():
    if 1:
        ret = {'success': False, 'message': 'An unexpected error has occurred, please try again later'}
        sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
        data1 = request.json
        print("riro data === ", data1)
        riro_key_token = genarate_alphanumeric_key_for_riro_data()
        x = mongo.db.riro_data.find_one({'date': data1['date'], 'id_no':  data1['id_no'], 'appruntime': data1['appruntime'], 'analytics_id': data1['analytics_id']})
        if sheet_data is not None:
            if x is None:
                print('riro data inserted')
                data1['job_sheet_name'] = sheet_data['job_sheet_name']
                data1['token'] = sheet_data['token']
                data1['riro_key_id'] = riro_key_token
                data1['other'] = None
                data1['remarks'] = ''
                data1['riro_edit_status'] = False
                data1['cropped_panel_image_path'] = None
                data1['riro_merged_image'] = None
                data1['lock_time'] = None
                data1['tag_time'] = None
                data1['flasher_status'] = 0
                result = mongo.db.riro_data.insert_one(data1)
                if result.acknowledged > 0:
                    ret = {'message': 'violation data inserted successfully.', 'success': True}
                else:
                    ret['message'] = 'violation data is not inserted.'
            else:
                new_change = {'rack_process': data1['rack_process'],   'rack_method': data1['rack_method'], 'person_in_time': data1['person_in_time'], 'person_out_time': data1['person_out_time'], 
                              'irrd_in_time': data1['irrd_in_time'], 'irrd_out_time': data1['irrd_out_time'], 'five_meter': data1['five_meter'], 'barricading':data1['barricading'], 'riro_image': data1['riro_image'],
                              'datauploadstatus': data1['datauploadstatus'], 'riro_merged_image': data1['riro_merged_image'],'riro_merged_image_size': data1['riro_merged_image_size']}
                # print('new change --------', new_change)
                mongo.db.riro_data.update_one({'_id': ObjectId(x['_id'])}, {'$set': new_change})
                print('riro_data updated successfully!.')
                ret['message'] = 'already inserted.'
        else:
            ret['message'] = 'job sheet not yet uploaded.'
        return ret


@app.route('/delete_riro_data', methods=['POST'])
def riro_data_delete():
    if 1:
        data1 = request.json
        x = mongo.db.riro_data.find_one({'date': data1['date'], 'id_no':data1['id_no'], 'appruntime': data1['appruntime'],'analytics_id': data1['analytics_id']})
        if x is None:
            ret = 'no data found for the deletion.'
        else:
            result = mongo.db.riro_data.delete_one({'_id': ObjectId(x['_id'])})
            if result.deleted_count > 0:
                ret = {'message': 'riro_data deleted successfully.','success': True}
            else:
                ret['message'] = ('riro_data is not deleted ,due to something went wrong with database.')
        return ret


@app.route('/rtsp_data', methods=['POST'])
def KIA_rstp_data():
    data = request.form.to_dict()
    print(data)
    picture = request.files.get('image')
    file = request.files['image']
    collection_data = mongo.db.camera_data.find_one({'camera_id': data['camera_id'], 'device_id': data['device_id']})
    filename = data['device_id'] + '_' + data['camera_id'] + '.jpg'
    if collection_data is None:
        data['insertion_date'] = str(datetime.now())
        data['image_name'] = filename
        result = mongo.db.camera_data.insert_one(data)
        if result.acknowledged > 0:
            ret = {'message': 'camera data inserted successfully.', 'success': True}
        else:
            ret['message'] = 'camera data is not inserted.'
    else:
        filters = {'camera_id': data['camera_id'], 'device_id': data['device_id']}
        mongo.db.camera_data.update_one(filters, {'$set': data})
    filename_db = os.getcwd() + '/' + 'images/rtsp_image/' + filename
    if not os.path.exists('images/rtsp_image'):
        os.makedirs('images/rtsp_image')
    picture.save(filename_db)
    return 'ok', 200


@app.route('/data_remove', methods=['POST'])
def data_remove_():
    data = request.form.to_dict()
    collection_data = mongo.db.camera_data.find({'device_id': data[
        'device_id']})
    if collection_data is not None:
        for i in collection_data:
            filename_db = os.getcwd() + '/' + 'images/rtsp_image/' + i['image_name']
            os.remove(filename_db)
            result = mongo.db.camera_data.delete_one({'device_id': data['device_id'], 'camera_id': i['camera_id']})
            if result.deleted_count > 0:
                ret = {'message': 'riro_data deleted successfully.', 'success': True}
            else:
                ret['message'] = ('riro_data is not deleted ,due to something went wrong with database.')
    return 'ok', 200


@app.route('/frame_image', methods=['POST'])
def KIA_frame_image():
    picture = request.files.get('frame')
    file = request.files['frame']
    filename = file.filename
    empPicture = picture.read()
    filename_db = os.getcwd() + '/' + 'tsk_images/frame/' + filename
    target_dir = os.getcwd() + '/' + 'tsk_images/frame'
    handle_uploaded_file(target_dir)
    picture.seek(0)
    picture.save(filename_db)
    return 'ok', 200


@app.route('/data_delete/<imagename>', methods=['GET'])
def Datadelete(imagename):
    collection_data = mongo.db.data.find_one({'imagename': imagename})
    if collection_data is not None:
        result = mongo.db.data.delete_one({'imagename': imagename})
        if result.deleted_count > 0:
            ret = {'message': 'riro_data deleted successfully.', 'success': True}
        else:
            ret['message'] = ('riro_data is not deleted ,due to something went wrong with database.')
    return 'ok', 200

# @app.route('/')
# def main():
# #   # showing different logging levels
# #   app.logger.debug("debug log info")
# #   app.logger.info("Info log information")
# #   app.logger.warning("Warning log info")
#   app.logger.error("Error log info")
#   app.logger.critical("Critical log info")
#   return "testing logging levels."


if __name__ == '__main__':
    
    # serve(app, port=5000)
    #app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    # import logging
    # from logging.handlers import RotatingFileHandler
    # file_handler = RotatingFileHandler('APIS_LOGFILE.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    # file_handler.setLevel(logging.ERROR)
    # app.logger.setLevel(logging.ERROR)
    # app.logger.addHandler(file_handler)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)