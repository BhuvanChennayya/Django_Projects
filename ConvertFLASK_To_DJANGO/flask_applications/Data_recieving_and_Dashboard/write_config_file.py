from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.write_config_funcs import *
from Data_recieving_and_Dashboard.steam_suit_mechanical import * 

creat_config = Blueprint('creat_config', __name__)


def create_json_file(filename):
    data = {
        "models": {
            "trafficcamnet": {
                "enable": 0,
                "modelpath": "config_infer_primary_trafficamnet.txt",
                "class_id": "2"
            },
            "objectDetector_Yolo": {
                "enable": 1,
                "modelpath": "/objectDetector_Yolo/config_infer_primary_yoloV3.txt",
                "class_id": "0"
            },
            "peoplenet": {
                "enable": 0,
                "modelpath": "config_infer_primary_peoplenet.txt",
                "class_id": "2"
            }
        }
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    file.close()


def fetch_enabled_data(filename):
    with open(filename, 'r') as file:
        models_data = json.load(file)
    enabled_model = None
    for model, config in models_data["models"].items():
        if config["enable"] == 1:
            if "objectDetector_Yolo" in model:
                enabled_model = {model: config, "modeltype": "yolo"}
            if "trafficcamnet" in model:
                enabled_model = {model: config, "modeltype": "trafficcam"}
            if "peoplenet" in model:
                enabled_model = {model: config, "modeltype": "people"}
            break
    file.close()
    return enabled_model


def get_model_config_details():
    json_filename = os.path.join(  str(os.getcwd()) + '/' + 'smaple_files', "model_config.json")
    if not file_exists(json_filename):
        create_json_file(json_filename)
        print(f"JSON file '{json_filename}' created successfully!")
    enabled_data = fetch_enabled_data(json_filename)
    # print(json.dumps(enabled_data, indent=4))
    return enabled_data  # json.dumps(enabled_data, indent=4)



def dumpvoiceannaoumentdataintodatatable(getdata_response):
    # mongo.db.voice_announcement_status.drop()
    # mongo.db.voice_announcement_status.delete_many({"violation_type":"VPMS"})
    if "voice_announcement_status" not in mongo.db.list_collection_names():
        print("Collection 'voice_announcement_status' does not exist")
    else:
        mongo.db.voice_announcement_status.delete_many({"violation_type": { "$in": ["RA", "PPE_TYPE1", "PPE_TYPE2","CRDCNT",'TJM'] }})
    for i , j in enumerate(getdata_response):
        if len(j['ppe_data']) !=0:
            # print('=======ppe_voice_anno999uncement_status data======================')
            # print('--------------------',j['ppe_data'][0])
            ppealertdata = j['ppe_data'][0]
            insertvoice_data = []
            ppe= False
            crushhelmet = False
            if ppealertdata['helmet'] == True and ppealertdata['vest']== True:
                ppe= True
            elif ppealertdata['helmet'] == True:
                ppe= True
            elif ppealertdata['vest']== True:
                ppe= True
            
            if 'crash_helmet' in ppealertdata:
                if ppealertdata['crash_helmet']== True:
                    crushhelmet = True

            if 'alert_details' in ppealertdata:
                if len(ppealertdata['alert_details']) !=0:
                    for kkfkkfkjffjjindex, value in enumerate(ppealertdata['alert_details']):
                        if 'voice_announcement' in value:
                            if value['voice_announcement'] !={} and value['voice_announcement_ip'] is not None:
                                if ppe == True and (value['label'] =='helmet' or value['label'] =='vest'):
                                    insertvalue = {'ip_address':value['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':value['voice_announcement']['audio_files'],'type':None,'violation_type':'PPE_TYPE1','violation_time':None,'valid_time':None,'roi_name':None}
                                    if insertvalue  not in insertvoice_data:
                                        insertvoice_data.append(insertvalue)

                                elif crushhelmet == True and value['label'] =='crash_helmet':
                                    insertvalue = {'ip_address':value['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':value['voice_announcement']['audio_files'],'type':None,'violation_type':'PPE_TYPE2','violation_time':None,'valid_time':None,'roi_name':None}
                                    if insertvalue  not in insertvoice_data:
                                        insertvoice_data.append(insertvalue)
                if len(insertvoice_data) !=0:
                    mongo.db.voice_announcement_status.insert_many(insertvoice_data)

        if len(j['roi_data']) !=0:
            RestrictedAreadata = j['roi_data']
            insertvoice_dataRA = []
            for roiindex , roivalues in enumerate(RestrictedAreadata):
                if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
                    if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
                        if 'analyticstype' in roivalues:
                            insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':str(roivalues['analyticstype']),'violation_type':'RA','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                            if insertvalue  not in insertvoice_dataRA:
                                insertvoice_dataRA.append(insertvalue)
                        else:
                            insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':str(roivalues['analyticstype']),'violation_type':'RA','violation_time':None,'valid_time':None,'roi_name':roivalues['roi_name']}
                            if insertvalue  not in insertvoice_dataRA:
                                insertvoice_dataRA.append(insertvalue)

            if len(insertvoice_dataRA) !=0:
                mongo.db.voice_announcement_status.insert_many(insertvoice_dataRA)
            # print('=======roi_data======================')
        if len(j['cr_data']) !=0:
            Crowdcountdata = j['cr_data']
            insertvoice_dataCRDCNT = []
            for roiindex , roivalues in enumerate(Crowdcountdata):
                # print('--------roivalues========CRDCNT--------',roivalues)
                if 'alarm_ip_address' in roivalues:
                    if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
                        if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
                            if roivalues['full_frame']== True:
                                    insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'fullframe','violation_type':'CRDCNT','violation_time':None,'valid_time':None,'roi_name':'fullframe'}
                                    if insertvalue  not in insertvoice_dataCRDCNT:
                                        insertvoice_dataCRDCNT.append(insertvalue)
                            else:
                                insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':'roi','violation_type':'CRDCNT','violation_time':None,'valid_time':None,'roi_name':roivalues['area_name']}
                                if insertvalue  not in insertvoice_dataCRDCNT:
                                    insertvoice_dataCRDCNT.append(insertvalue)

            if len(insertvoice_dataCRDCNT) !=0:
                mongo.db.voice_announcement_status.insert_many(insertvoice_dataCRDCNT)
            # print('=======cr_data======================')

        if 'trafficjam_data' in j: 
            if len(j['trafficjam_data']) !=0:
                trafficjamtdata = j['trafficjam_data']
                insertvoice_dataTJM = []
                for roiindex , roivalues in enumerate(trafficjamtdata):
                    if 'voice_announcement_ip' in roivalues['alarm_ip_address']:
                        if roivalues['alarm_ip_address']['voice_announcement_ip'] is not None:
                            insertvalue = {'ip_address':roivalues['alarm_ip_address']['voice_announcement_ip'],'camera_rtsp':j['rtsp_url'],'audio_file':roivalues['alarm_type']['voice_announcement']['audio_files'],'type':None,'violation_type':'TJM','violation_time':None,'valid_time':None,'roi_name':None}
                            if insertvalue  not in insertvoice_dataTJM:
                                insertvoice_dataTJM.append(insertvalue)

                if len(insertvoice_dataTJM) !=0:
                    mongo.db.voice_announcement_status.insert_many(insertvoice_dataTJM)
                # print('=======cr_data======================')



def CameraIdupdateFORMUlticonfig():
    ret = {'message': 'something went wrong with create config update_cam_id__.', 'success': False}
    getdata_response = DOCKETRUNMULTICONFIGGETDATA()
    # print('----------------------------',getdata_response)
    if len(getdata_response) != 0 or len(createSTEAMSUITconfig()) !=0 :
        dumpvoiceannaoumentdataintodatatable(getdata_response)
        function__response = None
        if "modelconfigurations" not in mongo.db.list_collection_names():
            # print("Collection 'voice_announcement_status' does not exist")
            function__response = WRITEMULTICONFIG(getdata_response)
        else:
            # mongo.db.voice_announcement_status.delete_many({"violation_type": { "$in": ["RA", "PPE_TYPE1", "PPE_TYPE2","CRDCNT",'TJM'] }})
            Findmodels = mongo.db.modelconfigurations.find_one({})
            if Findmodels is not None:
                print('------------Findmodels-----------------------------',Findmodels)
                if 'primary_modal_type' in Findmodels:
                    if Findmodels['primary_modal_type'] is not None:
                        if Findmodels['primary_modal_type'] =='docketrun_version1':
                            function__response = Loaddocketrun_V1_1_model(getdata_response)
                        else:
                            function__response = WRITEMULTICONFIG(getdata_response)
                    else:
                        function__response = WRITEMULTICONFIG(getdata_response)
                else:
                    function__response = WRITEMULTICONFIG(getdata_response)
            else:
                function__response = WRITEMULTICONFIG(getdata_response)

        return_data_update_camera = UPdatemulticonfigCamid(function__response)
        if return_data_update_camera == '200':
            ret = { 'message': 'application is started successfully.', 'success': True}
        else:
            ret = {'message': 'camera id not updated .', 'success': False}
    else:
        ret['message'] = 'please enable and add the ai analytics solutions.'
    return ret



def create_table_pintchrole(conn):
    ret = 0
    cursor = conn.cursor()

    try:
        create_table_query = sql.SQL(
            "CREATE TABLE IF NOT EXISTS pinch_role_status (camera_rtsp text, process integer )"
        )

        cursor.execute(create_table_query)
        conn.commit()
        print("\n[INFO] pinch_role_status table created.")
        ret = 1

    except psycopg2.Error as e:
        if e.pgcode == '42P07':  # Check if table already exists
            print("\n[INFO] pinch_role_status table already exists.")
            ret = 1
        else:
            print(f"PostgreSQL error: {e}")
            ret = 0

            # Log the error
            error_message = f"PostgreSQL error: {e}\n"

    finally:
        cursor.close()

    return ret

def delete_table_data(conn):
    ret = 0
    cursor = conn.cursor()

    try:
        delete_query = sql.SQL("DELETE FROM pinch_role_status")

        cursor.execute(delete_query)
        conn.commit()
        print("\n[INFO] All data deleted from pinch_role_status table.")
        ret = 1

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        ret = 0

        # Log the error
        error_message = f"PostgreSQL error: {e}\n"

    finally:
        cursor.close()

    return ret


def ONlyperimeterDangerzone(DangerZoneRoidetails):
    NewDetails =[]
    if len(DangerZoneRoidetails) !=0:
        for DanKEy , DanValue in enumerate(DangerZoneRoidetails):
            if 'analyticstype' in DanValue:
                if DanValue['analyticstype']==0:
                    NewDetails.append(DanValue)
            else:
                NewDetails.append(DanValue)
    return NewDetails

def ONlYPROTECTIONzone(DangerZoneRoidetails):
    NewDetails =[]
    if len(DangerZoneRoidetails) !=0:
        for DanKEy , DanValue in enumerate(DangerZoneRoidetails):
            if 'analyticstype' in DanValue:
                if DanValue['analyticstype']==2:
                    NewDetails.append(DanValue)
            else:
                NewDetails.append(DanValue)
    return NewDetails



def CheckAndGetObjectdetails(Camerainputdata):
    makelistObjects =[]
    joined_string =''
    if 'cr_data' in Camerainputdata:
        if len(Camerainputdata['cr_data']) !=0 :
            for k , value in enumerate(Camerainputdata['cr_data']):
                # print('---------------value ------------',value['data_object'])
                try:
                    if value['data_object'][0]['class_name'].lower() not in makelistObjects:
                        if value['data_object'][0]['class_name']=='motorbike' or value['data_object'][0]['class_name'].lower()=='motorcycle' :
                            makelistObjects.append('motorbike')
                        else:
                            makelistObjects.append(value['data_object'][0]['class_name'])
                except Exception as error:
                    print("000000000000=====000000Error----222--")
    if 'ppe_data' in Camerainputdata :
        if len(Camerainputdata['ppe_data']) !=0 :
            if 'crash_helmet' in Camerainputdata['ppe_data'][0]:
                if Camerainputdata['ppe_data'][0]['helmet'] != False or Camerainputdata['ppe_data'][0]['vest'] != False or Camerainputdata['ppe_data'][0]['crash_helmet'] != False:
                    if 'motorbike' not in makelistObjects:
                        makelistObjects.append('motorbike')
                    if 'person' not in makelistObjects:
                        makelistObjects.append('person')
            else:
                if Camerainputdata['ppe_data'][0]['helmet'] != False or Camerainputdata['ppe_data'][0]['vest'] != False :
                    if 'person' not in makelistObjects:
                        makelistObjects.append('person')
 
    if 'roi_data' in Camerainputdata :
        if len(Camerainputdata['roi_data']) !=0 :
            for k , value in enumerate(Camerainputdata['roi_data']):
                try:
                    if len(value['label_name']) ==1:
                        if value['label_name'][0].lower() not in makelistObjects:
                            if value['label_name'][0]=='motorbike' or value['label_name'][0].lower()=='motorcycle' :
                                makelistObjects.append('motorbike')
                            else:
                                makelistObjects.append(value['label_name'][0])
                    elif len(value['label_name']) >1:
                        for Newedd in value['label_name']:
                            if Newedd.lower() not in makelistObjects:
                                if Newedd=='motorbike' or Newedd.lower()=='motorcycle' :
                                    makelistObjects.append('motorbike')
                                else:
                                    makelistObjects.append(Newedd)
                except Exception as error:
                    print("0000000000000000----000000000Error----11--")

    if 'trafficjam_data' in Camerainputdata:
        if len(Camerainputdata['trafficjam_data']) !=0 :
            for k , value in enumerate(Camerainputdata['trafficjam_data']):
                try:
                    if len(value['selected_objects']) ==1:
                        if value['selected_objects'][0].lower() not in makelistObjects:
                            if value['selected_objects'][0]=='motorbike' or value['selected_objects'][0].lower()=='motorcycle' :
                                makelistObjects.append('motorbike')
                            else:
                                makelistObjects.append(value['selected_objects'][0])
                    elif len(value['selected_objects']) >1:
                        for Newedd in value['selected_objects']:
                            if Newedd.lower() not in makelistObjects:
                                if Newedd=='motorbike' or Newedd.lower()=='motorcycle' :
                                    makelistObjects.append('motorbike')
                                else:
                                    makelistObjects.append(Newedd)
                except Exception as error:
                    print("0000000000000000----000000000Error----11--")

    if 'tc_data' in Camerainputdata :
        if len(Camerainputdata['tc_data']) !=0 :
            for k , value in enumerate(Camerainputdata['tc_data']):
                try:
                    if len(value['class_name']) ==1:
                        if value['class_name'][0].lower() not in makelistObjects:
                            if value['class_name'][0]=='motorbike' or value['class_name'][0].lower()=='motorcycle' :
                                makelistObjects.append('motorbike')
                            else:
                                makelistObjects.append(value['class_name'][0])
                    elif len(value['class_name']) >1:
                        for Newedd in value['class_name']:
                            if Newedd.lower() not in makelistObjects:
                                if Newedd=='motorbike' or Newedd.lower()=='motorcycle' :
                                    makelistObjects.append('motorbike')
                                else:
                                    makelistObjects.append(Newedd)
                except Exception as error:
                    print("0000000000000000----000000000Error----11--")

    if len(makelistObjects) != 0:
        unique_elements = set(makelistObjects)
        joined_string = ";".join(unique_elements).lower()
    else:
        joined_string = 'person'
    return joined_string

                





def DOCKETRUNMULTICONFIGGETDATA():
    data = []
    fetch_require_data = list(mongo.db.ppera_cameras.find({'camera_status': True, "analytics_status": 'true'}))
    pintch_role_cameras = []
    if len(fetch_require_data) != 0:
        solution_datakeys=['roi_data','tc_data','cr_data','ppe_data']
        for i in fetch_require_data:
            # print("__________________i_________",i)
            J={}
            # print("ai_solution====",i['ai_solution'])
            if type(i['ai_solution'])==dict:
                for asdd,jjjs in i['ai_solution'].items():

                    # print('-----------------key {0}------value --------{1}'.format(asdd,jjjs))
                    if jjjs == True:
                        if asdd=='RA':
                            if len(i['roi_data']) != 0:
                                # print("roi data === ")
                                NewROIDetails = ONlyperimeterDangerzone(i['roi_data'])

                                if len(NewROIDetails) !=0:
                                    if 'roi_data' in J:
                                        if len(J['roi_data']) !=0 :
                                            NaddROid = J['roi_data']
                                            NaddROid= NaddROid+NewROIDetails
                                            J['roi_data'] = NaddROid
                                        else:
                                            J['roi_data']= NewROIDetails
                                    else:
                                        J['roi_data']=NewROIDetails
                                    # J['roi_data']=NewROIDetails
                                    Pintchrole= False
                                    try:
                                        for roiindex , roivalues in enumerate(NewROIDetails):
                                            # print("roivalues===========",roivalues)
                                            if roivalues['pinch_role']:
                                                Pintchrole= True

                                    except Exception as error :
                                        print("error----------------",error)
                                    if Pintchrole:
                                        #CREATE TABLE pinch_role_status ( camera_rtsp text, process integer );
                                        pintch_role_cameras.append({'camera_rtsp':i['rtsp_url'],'process':0})

                                    # print("-------------------NewROIDetails000000000000",NewROIDetails)
                        elif asdd=='TC':
                            if len(i['tc_data']) != 0:
                                J['tc_data']=i['tc_data']
                        elif  asdd=='CR':
                            if len(i['cr_data']) != 0:
                                J['cr_data']=i['cr_data']
                        elif  asdd=='PPE':
                            if len(i['ppe_data']) != 0:
                                if 'crash_helmet' in i['ppe_data'][0]:
                                    if i['ppe_data'][0]['helmet'] != False or i['ppe_data'][0]['vest'] != False or i['ppe_data'][0]['crash_helmet'] != False:
                                        J['ppe_data']=i['ppe_data']
                                else:
                                    if i['ppe_data'][0]['helmet'] != False or i['ppe_data'][0]['vest'] != False :
                                        J['ppe_data']=i['ppe_data']
                        elif asdd =='Traffic_Jam':
                            if len(i['trafficjam_data']) !=0:
                                J['trafficjam_data']=i['trafficjam_data']

                        if asdd=='Protection_Zone':
                            if len(i['roi_data']) != 0:
                                # print("roi data === ")
                                NewROIDetails = ONlYPROTECTIONzone(i['roi_data'])

                                if len(NewROIDetails) !=0:
                                    if 'roi_data' in J:
                                        if len(J['roi_data']) !=0 :
                                            NaddROid = J['roi_data']
                                            NaddROid= NaddROid+NewROIDetails
                                            J['roi_data'] = NaddROid
                                        else:
                                            J['roi_data']= NewROIDetails
                                    else:
                                        J['roi_data']=NewROIDetails
                                    Pintchrole= False
                                    try:
                                        for roiindex , roivalues in enumerate(NewROIDetails):
                                            # print("roivalues===========",roivalues)
                                            if roivalues['pinch_role']:
                                                Pintchrole= True

                                    except Exception as error :
                                        print("error----------------",error)
                                    if Pintchrole:
                                        #CREATE TABLE pinch_role_status ( camera_rtsp text, process integer );
                                        pintch_role_cameras.append({'camera_rtsp':i['rtsp_url'],'process':0})
                                    # print("-------------------NewROIDetails000000000000",NewROIDetails)
            for checkkey in solution_datakeys:
                if checkkey not in J:
                    J[checkkey]=[]                    
                
            if ENABLED_SOLUTION_IS_EMPTY_DICT(J) :
                J['cameraname']=i['cameraname']
                J['alarm_type']=i['alarm_type']
                J['alarm_ip_address']=i['alarm_ip_address']
                try:
                    J['alarm_version']=i['alarm_version']
                except :
                    J['alarm_version']={'hooter':'new','relay':''}
                J['rtsp_url']=i['rtsp_url']
                J['selected_object']= CheckAndGetObjectdetails(J)
                # print("-------------------j-",J)
                data.append(J)
    if len(pintch_role_cameras)!=0:
        connection = None
        try:
            connection = psycopg2.connect(
                user="docketrun",
                password="docketrun",
                host="localhost",
                port="5432",
                database="docketrundb"
            )
            create_table_pintchrole(connection)
            delete_table_data(connection)
            for new, camera in enumerate(pintch_role_cameras):
                postgres_insert_query = """ insert into pinch_role_status (camera_rtsp,process) 
                                values (%s,%s)"""
                record_to_insert = ( str(camera['camera_rtsp']),str(camera['process']))


                if True:
                    cursor = connection.cursor()
                # try :
                    cursor.execute(postgres_insert_query, record_to_insert)
                    connection.commit()
                    print("success")

        except psycopg2.Error as e:
            print(f"Unable to connect to the database. Error: {e}")
        finally:
            if connection:
                connection.close()
        print("Create Table ----------------------")
    return data




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


def remove_text_files(configfolderpath):
    test=os.listdir(configfolderpath)
    for item in test:
        if item.endswith(".txt"):
            os.remove(os.path.join(configfolderpath, item))


def split_list(input_list, sublist_length):
    return [input_list[i:i+sublist_length] for i in range(0, len(input_list), sublist_length)]


def file_exists(filename):
    return os.path.isfile(filename)






def UPdatemulticonfigCamid(update_cam_ids_data):
    for RRR, total_data in enumerate(update_cam_ids_data):
        final_data_camera_name = total_data['cameraname']
        final_rtsp_url = total_data['rtsp_url']
        update_camera_id = total_data['cameraid']
        result_data = mongo.db.ppera_cameras.find_one(  {'rtsp_url': final_rtsp_url, 'cameraname': final_data_camera_name})
        if result_data is not None:
            result_data['_id'] = str(result_data['_id'])
            id = result_data['_id']
            result = mongo.db.ppera_cameras.update_one({'_id': ObjectId( id), 'rtsp_url': final_rtsp_url}, {'$set': {'cameraid':  update_camera_id}})
            if result.matched_count > 0:
                pass
    return '200'

@creat_config.route('/create_phaseone_config', methods=['GET'])
def multiconfig():
    ret = {'message': 'something went wrong with create config.', 'success': False}
    if 1:
        common_return_data = CameraIdupdateFORMUlticonfig()
        createHOOTERMETAJSONSTART()
        if common_return_data:
            # print("FUN RESPONSE:", common_return_data)
            app_set_common_monitoring_started(True)
            
            stop_application_for_docketrun_creating_config()
            # app_set_phaseoneapp_monitoring_started(True)
            # stop_application_for_phaseoneapp_creating_config()
            if common_return_data['success'] == True:
                # app_set_phaseoneapp_monitoring_started(False)
                app_set_common_monitoring_started(False)
                
                ret = common_return_data
            else:
                ret['message'] = common_return_data['message']
        else:
            ret['message'] = 'data not found to create config files.'
    else:
        ret = ret
    return ret





@creat_config.route('/modelthresshold', methods=['GET'])
def makeaccutemodel():
    ret = {'message': "something went wrong with updatingthreshold", "success": False}
    if 1:
        configurationdetails = None
        json_filename = os.path.join(
            str(os.getcwd()) + '/' + 'smaple_files', "threshold_config.json")
        if not file_exists(json_filename):
            create_thresholdjson_file(json_filename)
            configurationdetails = fetch_configuration_data(json_filename)
            if configurationdetails is not None:
                ret = {'message': configurationdetails, "success": True}
            else:
                ret['message'] = "there is no data for model configuration."
        else:
            configurationdetails = fetch_configuration_data(json_filename)
            if configurationdetails is not None:
                ret = {'message': configurationdetails, "success": True}
            else:
                ret['message'] = "there is no data for model configuration."
    else:
        ret = ret
    return ret


@creat_config.route('/loadmodel', methods=['GET','POST'])
def loadmodel():
    ret = {'message': "something went wrong with updatingthreshold", "success": False}
    if request.method == 'POST':
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['data']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
            else:
                data = data['data']
                # {"primary_modal_type": "",
                # "crash_helmet_modal_type":"",
                # "helmet_modal_version":"",
                # "vest_modal_version":"",
                # "crash_helmet_modal_version":""}
                if data is not None:
                    find_data = mongo.db.modelconfigurations.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
                    if find_data is not None:
                        id = find_data['_id']
                        result = mongo.db.modelconfigurations.update_one({'_id': ObjectId (id)}, {'$set':data})
                        if result.modified_count > 0:
                            ret = {'message': 'model configuration updated successfully.','success': True}                        
                        else:
                            ret['message'] = 'model configuration already set.'     
                    else:
                        result = mongo.db.modelconfigurations.insert_one(data)
                        if result.acknowledged > 0:
                            ret = {'message':'model configuration updated successfully', 'success': True}
                        else:
                            ret['message'] = 'model configuration already set.'   
                else:
                    ret['message'] = 'please give proper input parametes.'     
        else:
            ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    else:
        find_data = mongo.db.modelconfigurations.find_one({}, sort=[('_id',  pymongo.DESCENDING)])
        if find_data is not None:
            ret={'message':find_data, 'success':True}
        else:
            ret['message'] = "there is no data for model configuration."
    return parse_json(ret)


@creat_config.route('/updatethreshold', methods=['POST'])
def updatethreshold():
    ret = {'message': "something went wrong with updatingthreshold", "success": False}
    data = request.json
    if data == None:
        data = {}
    request_key_array = ['data']
    jsonobjectarray = list(set(data))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
        output = [k for k, v in data.items() if v == '']
        if output:
            ret['message'] = 'You have missed these parameters ' + str(output) + ' to enter. please enter properly.'
        else:
            data = data['data']
            if data is not None:
                json_filename = os.path.join(str(os.getcwd()) + '/' + 'smaple_files', "threshold_config.json")  
                with open(json_filename, 'r') as file:
                    existing_data = json.load(file)
                existing_data["threshold"] = data['data']['threshold']
                with open(json_filename, 'w') as file:
                    json.dump(existing_data, file, indent=4)                    
                ret = {'message': "successfully updated", "success": True}                    
            else:
                ret['message']='given parameter is not in the correct format.'
    else:
        ret['message'] = 'you have missed these keys ' + str(missing_key) + ' to enter. please enter properly.'
    return ret

