from Data_recieving_and_Dashboard.packages import *

linkagetofieldjob = Blueprint('linkagetofieldjob', __name__)




def NEWCAPTURPANELIMAGE( url):
    print("camera url getting ==",url)
    response = True
    
    verfy_rtsp_response = None
    if response:
        directory_path =  os.path.join(os.getcwd() , 'rtsp_roi_image')
        if not os.path.exists(directory_path):
            handle_uploaded_file(directory_path)
        present_time = replace_spl_char(str(datetime.now()))
        print('verify_rtsp====',url)
        cam = cv2.VideoCapture(url)
        full_path = None
        count=0
        if cam.isOpened() == True:
            name = 'docketrun' + '_' + present_time + '.jpg'
            name1 = 'docketrun' + '_' + present_time + '1' + '.jpg'
            while cam.isOpened():
                ret, frame = cam.read()
                if ret:
                    if count == 10:
                        if frame.shape[-1] == 3:
                            if frame.shape[0] > 10 and frame.shape[1] > 10:
                                if frame.dtype == 'uint8':
                                    full_path = directory_path + '/' + name
                                    full_path1 = directory_path + '/' + name1
                                    cv2.imwrite(full_path, frame)
                                    cv2.imwrite(full_path1, frame)
                                    image_resizing(full_path)
                                    
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'imagename': name}
                                    break
                    elif count == 30:
                        if frame.shape[-1] == 3:
                            if frame.shape[0] > 10 and frame.shape[1] > 10:
                                if frame.dtype == 'uint8':
                                    full_path = directory_path + '/' + name
                                    full_path1 = directory_path + '/' + name1
                                    cv2.imwrite(full_path, frame)
                                    cv2.imwrite(full_path1, frame)
                                    image_resizing(full_path)
                                    
                                    verfy_rtsp_response = {'status': True, 'height': 544,'width': 960, 'imagename': name}
                                    break
                    count += 1
                else:
                    break
            cam.release()
            #cv2.destroyAllWindows()
    return verfy_rtsp_response

def CHECKRTSPISWORKING( camera_brand, camera_username, camera_password,  camera_ip_address):
    print("---------------------------999999999999993333333333333333", camera_brand, camera_username, camera_password,  camera_ip_address)
    data = {}
    rtsp_url = ESIBRANDCAMERASRTSP(camera_ip_address,camera_brand,camera_username,camera_password)
    print('RTSP ------------------------------ ', rtsp_url)
    image_data = NEWCAPTURPANELIMAGE(rtsp_url)
    print("-----file -------------------RTSP ---------------",rtsp_url)
    print('image_data', image_data)
    if image_data is not None:
        if image_data['status'] == True:
            data['rtsp_status'] = image_data['status']
            data['imagename'] = image_data['imagename']
            data['image_size'] = {'height': image_data['height'],'width': image_data['width']}
        return data
    else:
        return None
    
       
def Panel_NEWIMAGE(data):
    ifworked= 0
    if isEmpty(data):
        ImageData=CHECKRTSPISWORKING(data['camera_brand'],data['username'],data['password'], data['camera_ip'])
        if ImageData is not None:
            ifworked = 1
            data['imagename'] =  ImageData['imagename']
    # except Exception as  error:
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- PANELWISEDATAWITH3343IDANDIMAGESNAME 1", str(error), " ----time ---- ", now_time_with_time()]))
    if ifworked : 
        return parse_json(data)
    else:
        return None


@linkagetofieldjob.route('/LinkElectrialJob', methods=['GET','POST'])
def LinkElectrialJob():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    # try:
    if request.method == 'POST':
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['electrical_jobnumber', 'id','mechanical_jobnumber']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output) ,' to enter. please enter properly.' ])   
            else:
                print("=========================")
                # Newdata = data['data']
                id = data['id']
                # print("======Newdata===============",Newdata)
                electrical_jobnumber = data['electrical_jobnumber']
                mechanical_jobnumber = data['mechanical_jobnumber']
                Newinsertdata = {'fieldjobreferencid':id,'electrical_jobnumber':electrical_jobnumber,'mechanical_jobnumber':mechanical_jobnumber}
                result = mongo.db.linkagejobs.insert_one(Newinsertdata)
                if result.acknowledged:
                    ret = {'success': True, 'message': 'job numbers linked successfully.'}
                else:
                    ret['message'] = 'data is not inserted properly, please try once again.'         
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 

    elif request.method == 'GET':
        print('------------------------------')
        
        # data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
        # if data is not None:
        #     return_data = Panel_NEWIMAGE(data)
        #     if return_data is not None:
        #         print("999999999999999988888------------camera_setting--------8888888---88888888899999999999999999999999999999999")
        #         result = mongo.db.ppera_cameras.update_one({ '_id': ObjectId(id)},  {'$set': {"imagename":return_data['imagename']}})
        #         print(result.matched_count)
        #         if result.matched_count > 0:
        #             ret = {'message': return_data, 'success': True}
        #         else:
        #             ret['message'] ='something went wrong updating image.'
        #     else:
        #         ret['message'] ='rtsp is not working or something wrong with rtsp.'
        # else:
            # ret['message'] = 'panel data not found.'   
    # else:
    #     ret['message']='please give proper input data id and imagename.'     
    return ret 




@linkagetofieldjob.route('/removejoblink/<id>', methods=['GET'])
def removejoblink(id):
    ret = {'success': False, 'message':'something went wrong with delete ra camera api'}
    try:
        if id is not None:
            find_data = mongo.db.linkagejobs.find_one({'_id': ObjectId(id)})
            if find_data is not None:
                delete_data = mongo.db.linkagejobs.delete_many({'fieldjobreferencid':find_data['fieldjobreferencid']})
                if delete_data.deleted_count > 0:
                    ret = {'message': 'removed joblink successfully.','success': True}
                else:
                    ret['message' ] = 'data is not deleted, please try once again.'
            else:
                ret['message'] = 'for the given id there no data found, please change the id or try once again.'
        else:
            ret['message'] = 'please give mongoid for deletion of camera details.'
    except Exception as error:
        ret['message'] = str(error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- delete_ra_camera 1", str(error), " ----time ---- ", now_time_with_time()]))
    return ret


@linkagetofieldjob.route('/editlinkjobs', methods=['GET','POST'])
def LinkMechanicallJob():
    ret = {'success': False, 'message':'Something went wrong, please try again later'}
    # try:
    if request.method == 'POST':
        data = request.json
        if data == None:
            data = {}
        request_key_array = ['data', 'id']
        jsonobjectarray = list(set(data))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in data.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output) ,' to enter. please enter properly.' ])   
            else:
                print("=========================")
                Newdata = data['data']
                id = data['id']
                update_data = {}
                if 'electrical_jobnumber' in Newdata:
                    update_data['electrical_jobnumber']=Newdata['electrical_jobnumber']
                if 'mechanical_jobnumber' in Newdata:
                    update_data['mechanical_jobnumber']=Newdata['mechanical_jobnumber']
                Foundlinkdata = mongo.db.linkagejobs.find_one({'_id': ObjectId(id)})
                if Foundlinkdata is not None:
                    print("999999999999999988888------------camera_setting--------8888888---88888888899999999999999999999999999999999")
                    result = mongo.db.linkagejobs.update_one({ '_id': ObjectId(id)},  {'$set': update_data})
                    print(result.matched_count)
                    if result.matched_count > 0:
                        ret = {'message': 'edited successfully', 'success': True}
                    else:
                        ret['message'] ='something went wrong while editing.'
                else:
                    ret['message']='job linkage details not.'                   
                       
        else:
            ret['message'] = " ".join(["you have missed these keys ",str(missing_key), ' to enter. please enter properly.' ]) 

    elif request.method == 'GET':
        print('------------------------------')        
        # data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
        # if data is not None:
        #     return_data = Panel_NEWIMAGE(data)
        #     if return_data is not None:
        #         print("999999999999999988888------------camera_setting--------8888888---88888888899999999999999999999999999999999")
        #         result = mongo.db.ppera_cameras.update_one({ '_id': ObjectId(id)},  {'$set': {"imagename":return_data['imagename']}})
        #         print(result.matched_count)
        #         if result.matched_count > 0:
        #             ret = {'message': return_data, 'success': True}
        #         else:
        #             ret['message'] ='something went wrong updating image.'
        #     else:
        #         ret['message'] ='rtsp is not working or something wrong with rtsp.'
        # else:
            # ret['message'] = 'panel data not found.'   
    # else:
    #     ret['message']='please give proper input data id and imagename.'     
    return ret 



def checkwhichdictionarykeyvaluesChanged(requestdata, finddata):
    changed_values = {}  
    for key in finddata:
        if key in requestdata and finddata[key] != requestdata[key]:
            changed_values[key] =  requestdata[key]
    print("Changed values:")
    for key, value1 in changed_values.items():
        print(f"Key: {key},  New Value: {value1}")

    return changed_values

    
    
def checkdictionarfortruevaluesonly(dictionary,dataobject):
    print("dictionary===data==",dictionary)
    updatestatus = False
    for aidatakey, aidatavalue in dictionary.items():
        print("aisolutionkeyvalues ==",aidatakey)
        if aidatavalue:
            if aidatakey=="PPE" :
                if len(dataobject['ppe_data']) != 0:
                    if dataobject['ppe_data'][0]['helmet'] != False or dataobject['ppe_data'][0]['vest'] != False:
                        updatestatus=True
            elif aidatakey=="RA" :
                if len(dataobject['roi_data']) != 0:
                    updatestatus=True
            elif aidatakey=="CR" :
                if len(dataobject['cr_data']) != 0:
                    updatestatus=True
            elif aidatakey=="TC" :
                if len(dataobject['tc_data']) != 0:
                    updatestatus=True
            elif aidatakey=="fire" :
                if len(dataobject['firesmoke_data']) != 0:
                    if dataobject['firesmoke_data'][0]['fire'] != False or dataobject['firesmoke_data'][0]['smoke'] != False:
                        updatestatus=True
                        
            elif aidatakey=="smoke" :
                if len(dataobject['firesmoke_data']) != 0:
                    if dataobject['firesmoke_data'][0]['fire'] != False or dataobject['firesmoke_data'][0]['smoke'] != False:
                        updatestatus=True
            elif aidatakey=="dust" :
                if len(dataobject['firesmoke_data']) != 0:
                    if dataobject['firesmoke_data'][0]['dust'] != False :
                        updatestatus=True
    return updatestatus
