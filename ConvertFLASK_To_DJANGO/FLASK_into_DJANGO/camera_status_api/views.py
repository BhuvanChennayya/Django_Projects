from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.implimentingsockets import RTSPVERIFY


def get_ppe_helmet_violation(details,percent=30):
    helmet_percentage = (details['helmet'] / details['frame_count']) * 100
    no_helmet_percentage = (details['no_helmet'] /details['frame_count']) * 100
    if helmet_percentage >= int(percent) or no_helmet_percentage >= int(percent):
        if helmet_percentage > no_helmet_percentage:
            return "true"
        elif helmet_percentage < no_helmet_percentage:
            return "false"
        else:
            return "null"
    return "null"


def get_ppe_vest_violation(details,percent=30):
    vest_percentage = (details['vest'] / details['frame_count']) * 100
    arc_jacket_percentage = (details['arc_jacket'] / details['frame_count']) * 100
    no_vest_jacket_percentage = (details['no_ppe'] / details['frame_count']) * 100
    if vest_percentage >= int(percent) or arc_jacket_percentage >= int(percent) or no_vest_jacket_percentage >= int(percent):
        if vest_percentage > arc_jacket_percentage and vest_percentage > no_vest_jacket_percentage:
            return "vest"
        elif arc_jacket_percentage > vest_percentage and arc_jacket_percentage > no_vest_jacket_percentage:
            return "arc_jacket"
        elif no_vest_jacket_percentage > vest_percentage and no_vest_jacket_percentage > arc_jacket_percentage:
            return "no_ppe"
        else:
            return "null"
    return "null"


# async def QuickPINGIP(ip, timeout=0.4):
#     start_time = time.time()
#     try:
#         process = await asyncio.create_subprocess_shell(
#             f"ping -c 1 -W {timeout} {ip} > /dev/null 2>&1",
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE
#         )
#         await asyncio.wait_for(process.communicate(), timeout=timeout)
#         end_time = time.time()
#         response_time = end_time - start_time
#         return process.returncode == 0, response_time
#     except asyncio.TimeoutError:
#         end_time = time.time()
#         response_time = end_time - start_time
#         return False, response_time

# async def CHECKIPPING(ip):
#     status, response_time = await QuickPINGIP(ip)
#     return status, response_time



# def run_ping(ip_address):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         result = loop.run_until_complete(CHECKIPPING(ip_address))
#     finally:
#         loop.close()
#     return result



# async def QuickPINGIP(ip, timeout=0.4):
#     start_time = time.time()
#     try:
#         process = await asyncio.create_subprocess_shell(
#             f"ping -c 1 -W {timeout} {ip} > /dev/null 2>&1",
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE
#         )
#         await asyncio.wait_for(process.communicate(), timeout=timeout)
#         end_time = time.time()
#         response_time = end_time - start_time
#         return process.returncode == 0, response_time
#     except asyncio.TimeoutError:
#         end_time = time.time()
#         response_time = end_time - start_time
#         return False, response_time

# async def CHECKIPPING(ip):
#     status, response_time = await QuickPINGIP(ip)
#     return status, response_time

# def run_ping(ip_address):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         result = loop.run_until_complete(CHECKIPPING(ip_address))
#     finally:
#         loop.close()
#     return result


async def QuickPINGIP(ip, timeout=0.2):
    start_time = time.time()
    try:
        process = await asyncio.create_subprocess_shell(
            f"ping -c 1 -W {timeout} {ip} > /dev/null 2>&1",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            await process.communicate()
            end_time = time.time()
            response_time = end_time - start_time
            return False, response_time
        
        end_time = time.time()
        response_time = end_time - start_time
        return process.returncode == 0, response_time
    except Exception as e:
        print(f"Error during ping: {e}")
        end_time = time.time()
        response_time = end_time - start_time
        return False, response_time

async def CHECKIPPING(ip):
    status, response_time = await QuickPINGIP(ip)
    return status, response_time

async def run_ping(ip_address):
    return await CHECKIPPING(ip_address)


def RTSPVERIFY(url):
    cam = cv2.VideoCapture(url)
    if cam.isOpened() == True:
        while cam.isOpened():
            ret, frame = cam.read()
            if ret:
                verfy_rtsp_response = True
                return verfy_rtsp_response
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()
    else:
        return False

def get_list_working_not_working_cam_list(find_data):
    working_cam_name =[]
    not_working_cam_name =[]
    for ppera_data in find_data:
        if ppera_data['camera_ip'] == None:
            if ppera_data['rtsp_url'] != None:
                # testing_ip_working = final_ping(ppera_data['camera_ip'])
                # testing_ip_working, response_time =  ping_ip(ppera_data['camera_ip'])
                # result = asyncio.run(run_ping(ppera_data['camera_ip']))
                # if testing_ip_working is True:
                # result =run_ping(ppera_data['camera_ip'])
                result = asyncio.run(run_ping(ppera_data['camera_ip']))
                if result[0] is True:
                    working_cam_name.append(ppera_data)
                else:
                    not_working_cam_name.append(ppera_data)
            else:
                test_rtsp_response_image = RTSPVERIFY(ppera_data['rtsp_url'])
                if test_rtsp_response_image:
                    working_cam_name.append(ppera_data)
                else:
                    not_working_cam_name.append(ppera_data)

        else:
            # testing_ip_working = final_ping(ppera_data['camera_ip'])
            # testing_ip_working, response_time =  ping_ip(ppera_data['camera_ip'])
            # if testing_ip_working is True:
            # result = asyncio.run(run_ping(ppera_data['camera_ip']))
            # result =run_ping(ppera_data['camera_ip'])
            result = asyncio.run(run_ping(ppera_data['camera_ip']))
            if result[0] is True:
                working_cam_name.append(ppera_data)
            else:
                not_working_cam_name.append(ppera_data)

    return working_cam_name


def GETNOTWORKINGCAMERADETAILS(find_data):
    working_cam_name =[]
    not_working_cam_name =[]
    for ppera_data in find_data:
        if ppera_data['camera_ip'] == None:
            if ppera_data['rtsp_url'] != None:
                if RTSPVERIFY(ppera_data['rtsp_url']):
                    working_cam_name.append(ppera_data)
                else:
                    not_working_cam_name.append(ppera_data)
        else:
            # testing_ip_working, response_time =  ping_ip(ppera_data['camera_ip'])
            # if final_ping(ppera_data['camera_ip']) is True:
            # if testing_ip_working is True:
            # result = asyncio.run(run_ping(ppera_data['camera_ip']))
            # result =run_ping(ppera_data['camera_ip'])
            result = asyncio.run(run_ping(ppera_data['camera_ip']))
            if result[0] is True:
                working_cam_name.append(ppera_data)
            else:
                not_working_cam_name.append(ppera_data)
    return not_working_cam_name

def GETWORKINGANDNOTWORKINGcamCOUNT(find_data):
    workingcount = 0
    notworkingcount=0
    totalcountNew = 0
    totalcount = {'total_cameras':totalcountNew,'working_camcount':workingcount,'notworkingcamcount':notworkingcount}
    for ppera_data in find_data:
        totalcountNew += 1 
        if ppera_data['camera_ip'] == None:
            if ppera_data['rtsp_url'] != None:
                if RTSPVERIFY(ppera_data['rtsp_url']):
                    workingcount += 1
                else:
                    notworkingcount += 1
        else:
            # testing_ip_working = final_ping(ppera_data['camera_ip'])
            # testing_ip_working, response_time =  ping_ip(ppera_data['camera_ip'])
            # if testing_ip_working is True:
            # result = asyncio.run(run_ping(ppera_data['camera_ip']))
            # result =run_ping(ppera_data['camera_ip'])
            result = asyncio.run(run_ping(ppera_data['camera_ip']))
            if result[0] is True:
                workingcount += 1
            else:
                notworkingcount += 1
    totalcount={'total_cameras':totalcountNew,'working_camcount':workingcount,'notworkingcamcount':notworkingcount}
    return totalcount


def GETWORKINGCAMERADETAILS(find_data):
    working_cam_name =[]
    for ppera_data in find_data:
        if ppera_data['camera_ip'] == None:
            if ppera_data['rtsp_url'] != None:
                if RTSPVERIFY(ppera_data['rtsp_url']):
                    working_cam_name.append(ppera_data)
        else:
            # testing_ip_working, response_time =  ping_ip(ppera_data['camera_ip'])
            # if testing_ip_working is True:
            # if final_ping(ppera_data['camera_ip']) is True:
            # result = asyncio.run(run_ping(ppera_data['camera_ip']))
            # result =run_ping(ppera_data['camera_ip'])
            result = asyncio.run(run_ping(ppera_data['camera_ip']))
            if result[0] is True:
                working_cam_name.append(ppera_data)
    return working_cam_name


def get_enable_cam_disable_cam(find_data): 
    enable_cam_names = []
    for f_data in find_data:
        if len(f_data['roi_data']) != 0 and len(f_data['tc_data']) != 0 and len(f_data['cr_data']) != 0 and (len(f_data['ppe_data']) != 0  and (any(value is True for value in f_data['ppe_data'][0].values())) != 0) :
            enable_cam_names.append(f_data) 
    return enable_cam_names


"""def NewEnabledcameras(find_data): 
    enable_cam_names = []
    for f_data in find_data:
        if len(f_data['roi_data']) != 0 or len(f_data['tc_data']) != 0 or  len(f_data['cr_data']) != 0 or  (len(f_data['ppe_data']) != 0  and  (any(value is True for value in f_data['ppe_data'][0].values())) != 0) :
            enable_cam_names.append(f_data) 

        if "firesmoke_data" in f_data.keys():
            firesmoke_data = f_data['firesmoke_data']
            if len(firesmoke_data) != 0:
                enable_cam_names.append(f_data) 
        
    return enable_cam_names
"""

def NewEnabledcameras(find_data): 
    enable_cam_names = []
    for f_data in find_data:
        if len(f_data['roi_data']) != 0 or len(f_data['tc_data']) != 0 or  len(f_data['cr_data']) != 0 or  (len(f_data['ppe_data']) != 0  and  (any(value is True for value in f_data['ppe_data'][0].values())) != 0) :
            enable_cam_names.append(f_data) 

        if "firesmoke_data" in f_data.keys():
            firesmoke_data = f_data['firesmoke_data']
            if len(firesmoke_data) != 0:
                if f_data not in enable_cam_names:
                    enable_cam_names.append(f_data) 

        if "trafficjam_data" in f_data.keys():
            trafficjam_data = f_data['trafficjam_data']
            if len(trafficjam_data) != 0:
                if f_data not in enable_cam_names:
                    enable_cam_names.append(f_data) 

        
        if "vpms_data" in f_data.keys():
            vpms_data = f_data['vpms_data']
            if len(vpms_data) != 0:
                if f_data not in enable_cam_names:
                    enable_cam_names.append(f_data) 

    return enable_cam_names


def fun_ppe_violations_count(all_data):
    ppepercentage = mongo.db.filterviolations.find_one({},{'_id':0})
    if ppepercentage is None:
        ppepercentage = {"helmet":30,"vest":30}
    ppe_count = 0   
    helmet_counts = 0
    vest_counts = 0
    for count, i in enumerate(all_data):
        object_data = i['object_data']
        if len(object_data) == 1:
            # print("VALUE OF I FOR PPE_VIOLATIONS:---", i)
            if object_data[0]['class_name'] == 'person':
                if object_data[0]['Helmet'] == False:
                    if get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                        ppe_count += 1
                        helmet_counts += 1
                    elif get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                        ppe_count += 1
                        vest_counts += 1
                        
                elif object_data[0]['Vest'] == 'no_ppe':
                    if get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                        ppe_count += 1
                        vest_counts += 1
                    elif get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                        ppe_count += 1
                        helmet_counts += 1

        elif len(object_data) > 1:
            for ___, jjj in enumerate(object_data):
                if jjj['class_name'] == 'person':
                    if jjj['Helmet'] == False:
                        if jjj['algorithm_details']:
                            if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                ppe_count += 1
                                helmet_counts += 1
                            elif get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                ppe_count += 1
                                vest_counts += 1
                        else:
                            ppe_count += 1
                            helmet_counts += 1

                    elif jjj['Vest'] == 'no_ppe':
                        if jjj['algorithm_details']:
                            if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                ppe_count += 1
                                vest_counts += 1

                            elif get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                ppe_count += 1
                                helmet_counts += 1

                        else:
                            ppe_count += 1
                            vest_counts += 1

                 
    perimeter_violation_counts = {"ppe_counts": ppe_count, "vest_cnts" : vest_counts, "helmet_cnts" : helmet_counts}
    # return ppe_count
    return perimeter_violation_counts


def fun_ppe_violations_count___():
    match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE1'}
    all_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}])) 
    ppepercentage = mongo.db.filterviolations.find_one({},{'_id':0})
    if ppepercentage  is None:
        ppepercentage = {"helmet":30,"vest":30}
    ppe_count = 0   
    helmet_counts = 0
    vest_counts = 0
    for count, i in enumerate(all_data):
        object_data = i['object_data']
        if len(object_data) == 1:
            if object_data[0]['class_name'] == 'person':
                if object_data[0]['Helmet'] == False:
                    if get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                        ppe_count += 1
                        helmet_counts += 1
                    elif get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                        ppe_count += 1
                        vest_counts += 1
                elif object_data[0]['Vest'] == 'no_ppe':
                    if get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                        ppe_count += 1
                        vest_counts += 1
                    elif get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                        ppe_count += 1
                        helmet_counts += 1

        elif len(object_data) > 1:
            for ___, jjj in enumerate(object_data):
                if jjj['class_name'] == 'person':
                    if jjj['Helmet'] == False:
                        if jjj['algorithm_details']:
                            if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                ppe_count += 1
                                # helmet_counts += 1
                            elif get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                ppe_count += 1
                                # vest_counts += 1
                        else:
                            ppe_count += 1
                            # helmet_counts += 1

                    elif jjj['Vest'] == 'no_ppe':
                        if jjj['algorithm_details']:
                            if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                ppe_count += 1
                                # vest_counts += 1

                            elif get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                ppe_count += 1
                                # helmet_counts += 1

                        else:
                            ppe_count += 1
                            # vest_counts += 1
    # perimeter_violation_counts = {"ppe_counts": ppe_count, "vest_cnts" : vest_counts, "helmet_cnts" : helmet_counts}
    return ppe_count
    # return perimeter_violation_counts


def date_wise_fun_ppe_violations_count(all_data):
    ppepercentage = mongo.db.filterviolations.find_one({},{'_id':0})
    if ppepercentage  is None:
        ppepercentage = {"helmet":30,"vest":30}
    ppe_count = 0   
    helmet_counts = 0
    vest_counts = 0
    for count, i in enumerate(all_data):
        object_data = i['object_data']
        if len(object_data) == 1:
            if object_data[0]['class_name'] == 'person':
                if object_data[0]['Helmet'] == False:
                    if get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                        ppe_count += 1
                        helmet_counts += 1
                    elif get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                        ppe_count += 1
                        vest_counts += 1
                elif object_data[0]['Vest'] == 'no_ppe':
                    if get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                        ppe_count += 1
                        vest_counts += 1
                    elif get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                        ppe_count += 1
                        helmet_counts += 1

        elif len(object_data) > 1:
            for ___, jjj in enumerate(object_data):
                if jjj['class_name'] == 'person':
                    if jjj['Helmet'] == False:
                        if jjj['algorithm_details']:
                            if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                ppe_count += 1
                                # helmet_counts += 1
                            elif get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                ppe_count += 1
                                # vest_counts += 1
                        else:
                            ppe_count += 1
                            # helmet_counts += 1

                    elif jjj['Vest'] == 'no_ppe':
                        if jjj['algorithm_details']:
                            if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                ppe_count += 1
                                # vest_counts += 1

                            elif get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                ppe_count += 1
                                # helmet_counts += 1

                        else:
                            ppe_count += 1
                            # vest_counts += 1
    # perimeter_violation_counts = {"ppe_counts": ppe_count, "vest_cnts" : vest_counts, "helmet_cnts" : helmet_counts}
    return ppe_count
    # return perimeter_violation_counts









# Create your views here.






#@camera_status.route('/CrashHelmentviolationCount', methods=['GET','POST'])
@csrf_exempt
def CrashHelmentviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get CrashHelmentviolationCount api'}    
    CrashHelmetViolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'PPE_TYPE2'}
                    if department and department != 'none':
                        match_data['department'] = department
                    if camera_name and camera_name != 'none':
                        match_data['camera_name'] = camera_name                    
                    # CrashHelmetViolationCount = mongo.db.data.count_documents(match_data)
                    CrashHelmetViolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)

                    ret = {'success': True, 'message': {'crashhelmetviolationcount':CrashHelmetViolationCount}}
                    
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        print("----------hello123 mic testing")
        # CrashHelmetViolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE2'}) 
        # CrashHelmetViolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE2'}) 
        CrashHelmetViolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE2'})        
               
               
        ret = {'success': True, 'message': {'crashhelmetviolationcount':CrashHelmetViolationCount}}  
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)



# @camera_status.route('/PPEviolationCount', methods=['GET','POST'])
@csrf_exempt
def PPEviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get CrashHelmentviolationCount api'}    
    PPEViolationCount = 0
    if request.method == 'POST':
        
        data = json.loads(request.body)

        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'PPE_TYPE1'
            #                       , '$or': [
            # {"object_data.Helmet": False},
            # {"object_data.Vest": "no_ppe"}]
                                  }
                    if department and department != 'none':
                        match_data['department'] = department
                    if camera_name and camera_name != 'none':
                        match_data['camera_name'] = camera_name                    
                    # PPEViolationCount = mongo.db.data.count_documents(match_data)
                    PPEViolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)
                    Vestpipeline = [
                                    {
                                        '$match': match_data
                                    },
                                    {
                                        '$unwind': '$object_data'
                                    },
                                    {
                                        '$match': {
                                            'object_data.Vest': "no_ppe"
                                        }
                                    },
                                    {
                                        '$count': 'vest_violation_count'
                                    }
                                ]
        
                    # result = list(mongo.db.data.aggregate(Vestpipeline))
                    result = list(PPERAVIOLATIONCOLLECTION.aggregate(Vestpipeline))#getting  info diretly from collection

                    vest_violation_count = result[0]['vest_violation_count'] if result else 0
                    pipeline = [
                        {
                            '$match': match_data
                        },
                        {
                            '$unwind': '$object_data'
                        },
                        {
                            '$match': {
                                'object_data.Helmet': False
                            }
                        },
                        {
                            '$count': 'helmet_violation_count'
                        }
                    ]
                    # result = list(mongo.db.data.aggregate(pipeline))
                    result = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))

                    helmet_violation_count = result[0]['helmet_violation_count'] if result else 0

                    ret = {
                            'success': True,
                            'message': {
                                'ppeviolationcount': PPEViolationCount,
                                'vest_violation_count': vest_violation_count,
                                'helmet_violation_count': helmet_violation_count
                            }
                        }
                    # ret = {'success': True, 'message': {'ppeviolationcount':PPEViolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        match_data = {
        'timestamp': {'$regex': '^' + str(date.today())},
        'analyticstype': 'PPE_TYPE1',
        '$or': [
            {"object_data.Helmet": False},
            {"object_data.Vest": "no_ppe"}
        ]
        }
        # PPEViolationCount = mongo.db.data.count_documents(match_data)
        PPEViolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)

        Vestpipeline = [
                    {
                        '$match': {
                            'timestamp': {'$regex': '^' + str(date.today())},
                            'analyticstype': 'PPE_TYPE1'
                        }
                    },
                    {
                        '$unwind': '$object_data'
                    },
                    {
                        '$match': {
                            'object_data.Vest': "no_ppe"
                        }
                    },
                    {
                        '$count': 'vest_violation_count'
                    }
                ]
        
        # result = list(mongo.db.data.aggregate(Vestpipeline))
        result = list(PPERAVIOLATIONCOLLECTION.aggregate(Vestpipeline))

        vest_violation_count = result[0]['vest_violation_count'] if result else 0
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$regex': '^' + str(date.today())},
                    'analyticstype': 'PPE_TYPE1'
                }
            },
            {
                '$unwind': '$object_data'
            },
            {
                '$match': {
                    'object_data.Helmet': False
                }
            },
            {
                '$count': 'helmet_violation_count'
            }
        ]
        # result = list(mongo.db.data.aggregate(pipeline))
        result = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))

        helmet_violation_count = result[0]['helmet_violation_count'] if result else 0
        ret = {
            'success': True,
            'message': {
                'ppeviolationcount': PPEViolationCount,
                'vest_violation_count': vest_violation_count,
                'helmet_violation_count': helmet_violation_count
            }
        } 
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)

# @camera_status.route('/RAviolationCount', methods=['GET','POST'])
@csrf_exempt
def RAviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get CrashHelmentviolationCount api'}    
    RAviolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'RA','violation_status': True,
                                  'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}}
                    if department and department != 'none':
                        match_data['department'] = department
                    if camera_name and camera_name != 'none':
                        match_data['camera_name'] = camera_name                    
                    # RAviolationCount = mongo.db.data.count_documents(match_data)
                    RAviolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)

                    ret = {'success': True, 'message': {'raviolationcount':RAviolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        # RAviolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
        #                           'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}})   
        RAviolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
                                  'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}})      
        ret = {'success': True, 'message': {'raviolationcount':RAviolationCount}}  
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)

# @camera_status.route('/ProtectionZoneviolationCount', methods=['GET','POST'])
@csrf_exempt
def ProtectionZoneviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get CrashHelmentviolationCount api'}    
    protectionzoneviolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'RA','violation_status': True,
                                  'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }}
                    if department and department != 'none':
                        match_data['department'] = department
                    if camera_name and camera_name != 'none':
                        match_data['camera_name'] = camera_name         

                    # protectionzoneviolationCount = mongo.db.data.count_documents(match_data)
                    protectionzoneviolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)

                    ret = {'success': True, 'message': {'protectionzoneviolationCount':protectionzoneviolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    
    elif request.method == 'GET':
        # protectionzoneviolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
        #                           'object_data': {
        #                                         '$elemMatch': {
        #                                             'violation': True,
        #                                             'roi_details': {
        #                                                 '$exists': True,
        #                                                 '$elemMatch': {
        #                                                     'violation': True,
        #                                                     'analytics_type': '2'
        #                                                 }
        #                                             }
        #                                         }
        #                                     }})     
        protectionzoneviolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
                                  'object_data': {
                                                '$elemMatch': {
                                                    'violation': True,
                                                    'roi_details': {
                                                        '$exists': True,
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'analytics_type': '2'
                                                        }
                                                    }
                                                }
                                            }})  
        ret = {'success': True, 'message': {'protectionzoneviolationCount':protectionzoneviolationCount}}
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)

# @camera_status.route('/CrowdCountviolationCount', methods=['GET','POST'])
@csrf_exempt
def CrowdCountviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get CrashHelmentviolationCount api'}    
    CrowcontviolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'CRDCNT','violation_status': True}
                    if department and department != 'none':
                        match_data['department'] = department
                    if camera_name and camera_name != 'none':
                        match_data['camera_name'] = camera_name                    
                    # CrowcontviolationCount = mongo.db.data.count_documents(match_data)
                    CrowcontviolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)

                    ret = {'success': True, 'message': {'crowcontviolationCount':CrowcontviolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        # CrowcontviolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'CRDCNT'})  
        CrowcontviolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'CRDCNT'})      
        ret = {'success': True, 'message': {'crowcontviolationCount':CrowcontviolationCount}}  
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)

# @camera_status.route('/totalViolationCount', methods=['GET','POST'])
@csrf_exempt
def totalViolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get CrashHelmentviolationCount api'}    
    totalviolationcount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'violation_status': True}
                    print("MATCHED DATA:------", match_data)
                    if department and department != 'none':
                        match_data['department'] = department
                    if camera_name and camera_name != 'none':
                        match_data['camera_name'] = camera_name               
                    totalviolationcount = mongo.db.data.count_documents(match_data)
                    ret = {'success': True, 'message': {'totalviolationcount':totalviolationcount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        # totalviolationcount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())},'violation_status': True})      
        # CrowcontviolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'CRDCNT'})
        # CrashHelmetViolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE2'})
        CrowcontviolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'CRDCNT'})
        CrashHelmetViolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE2'})
        match_data = {
                'timestamp': {'$regex': '^' + str(date.today())},
                'analyticstype': 'PPE_TYPE1',
                '$or': [
                    {"object_data.Helmet": False},
                    {"object_data.Vest": "no_ppe"}
                ]
            }

        # PPEViolationCount = mongo.db.data.count_documents(match_data)
        PPEViolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)
        protectionzoneviolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
                                        'object_data': {
                                                        '$elemMatch': {
                                                            'violation': True,
                                                            'roi_details': {
                                                                '$exists': True,
                                                                '$elemMatch': {
                                                                    'violation': True,
                                                                    'analytics_type': '2'
                                                                }
                                                            }
                                                        }
                                                    }})


        # RAviolationCount = mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
        # 'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}})  
        RAviolationCount = PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'RA','violation_status': True,
        'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}})  
    
        totalviolationcount = CrowcontviolationCount + CrashHelmetViolationCount + PPEViolationCount + protectionzoneviolationCount + RAviolationCount
        # print("MATCHED DATA:------", totalviolationcount)
        ret = {'success': True, 'message': {'totalviolationcount':totalviolationcount}}
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)


# @camera_status.route('/get_cam_status_enable_cam_count', methods=['GET'])
@csrf_exempt
def get_cam_status_enable_cam_count(request):
    ret = {'success': False, 'message': 'something went wrong with get all solutions count api'}
    if request.method == 'GET':
        if 1:
        # try:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True}))        
            if len(find_data_cam_status) !=0:
                disable_data_count = 0
                enable_data_count = 0
                workingcount = 0
                notworkingcount=0
                totalcountNew = 0
                for find_data in find_data_cam_status:
                    counts_enable_cam = 0
                    totalcountNew += 1
                    if find_data['camera_ip'] == None:
                        if find_data['rtsp_url'] != None:
                            if RTSPVERIFY(find_data['rtsp_url']):
                                workingcount += 1
                            else:
                                notworkingcount += 1
                    else:
                        result = asyncio.run(run_ping(find_data['camera_ip']))
                        if result[0] is True:
                            workingcount += 1
                        else:
                            notworkingcount += 1
                    for x_k in list(find_data.keys()):
                        if type(find_data[x_k]) == list and x_k in ['vpms_data','trafficjam_data','firesmoke_data','roi_data','cr_data','ppe_data','tc_data']:
                            if find_data["analytics_status"] == 'true':
                                counts_enable_cam += 1
                                break

                    if counts_enable_cam > 0:
                        enable_data_count += 1  

                    else:
                        disable_data_count += 1
                REQUIRED = [{'total_cam_count': totalcountNew, 'working_cam_count':workingcount, 'not_working_cam_count': notworkingcount, 'disable_data_count': disable_data_count, 'enable_data_count': enable_data_count}]
                ret = {'message': REQUIRED, 'success': True}
            else:
                ret['message']='there are no cameras added for analytics.'
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)

# @camera_status.route('/get_solution_data_details', methods=['GET'])
@csrf_exempt
def get_solution_data_details(request):
    ret = {'message':'Someting went wrong with get all solutions details api','success':False}
    if request.method == 'GET':
        if 1:
        # try:
            cr_require_data_details = []
            ppe_require_data_details = []
            tc_require_data_details = []
            roi_require_data_details = []
            final_require_data_details = []
            """Calling function to get the working camera list and not woorking camera list"""
            wcam_list_and_nwcam_list = get_list_working_not_working_cam_list(list(ppera_cameras.find({'camera_status': True})))
            if len(wcam_list_and_nwcam_list) !=0:
                for url in wcam_list_and_nwcam_list:
                    cr_data = url['cr_data']
                    tc_data = url['tc_data']
                    ppe_data = url['ppe_data']
                    roi_data = url['roi_data']
                    Camerainformation = {'camera_name':  url['cameraname'], 'camera_ip': url['camera_ip' ], 'rtsp_url': url['rtsp_url'], 'imagename':  url['imagename']}
                    if type(cr_data) == list:
                        if len(cr_data) != 0:
                            if url["ai_solution"]["CR"] == True:
                                cr_require_data_details.append(Camerainformation)
                                        
                    if type(tc_data) == list:
                        if len(tc_data) !=0:
                            if url["ai_solution"]["TC"] == True:
                                tc_require_data_details.append(Camerainformation)

                    if type(ppe_data) == list:
                        if (len(ppe_data) != 0  and  (any(value is True for value in ppe_data[0].values())) != 0):
                            if url["ai_solution"]["PPE"] == True:
                                ppe_require_data_details.append(Camerainformation)

                    if type(roi_data) == list:
                        if len(roi_data) != 0:
                            if url["ai_solution"]["RA"] == True:
                                roi_require_data_details.append(Camerainformation)

                REQUIRED = {'roi_cam_details': roi_require_data_details,  'cr_cam_details': cr_require_data_details, 'tc_cam_details': tc_require_data_details, 'ppe_cam_details': ppe_require_data_details}
                final_require_data_details.append(REQUIRED)
                ret = {'message': final_require_data_details, 'success': True}
            else:
                ret['message']='there are no cameras added for analytics.'
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_solution_data_details 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_solution_data_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
    # else:
    #     ret={
    #         'success': False,
    #         'message':"request type wrong, please try once again."
    #     } 
    return JsonResponse(ret)


# @camera_status.route('/get_current_date_violation_counts', methods=['GET'])
@csrf_exempt
def get_current_date_violations(request):
    ret = {'message':'Someting went wrong api','success':False}
    if request.method == 'GET':
        if 1:
        # try:
            # match_data = {'timestamp': {'$regex': '^' + str(date.today())}}
            # data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}])) 
            
            camera_status_true_data = list(ppera_cameras.find({'camera_status': True})) #'camera_rtsp': x_data['rtsp_url']
            # ppepercentage = mongo.db.filterviolations.find_one({},{'_id':0})
            # if ppepercentage is None:
            #     ppepercentage = {"helmet":30,"vest":30}
            ppe_count = 0
            ra_count = 0
            tc_count = 0
            cr_count = 0
            protected_zone = 0
            ppe_crash_helemt_counts = 0
            total_count = 0
            if len(camera_status_true_data) != 0:
                ppe_count += mongo.db.data.count_documents({'timestamp': {'$regex': '^' + str(date.today())},   'analyticstype': 'PPE_TYPE1', '$or': [
                {"object_data.Helmet": False},
                {"object_data.Vest": "no_ppe"}
            ]})
                ppe_crash_helemt_counts += PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())}, 'analyticstype': 'PPE_TYPE2'})
                cr_count += PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$regex': '^' + str(date.today())},  'analyticstype': 'CRDCNT'}) 
                protected_zone += PPERAVIOLATIONCOLLECTION.count_documents({
                    'timestamp': {'$regex': '^' + str(date.today())},
                    'analyticstype': 'RA',
                    'violation_status': True,
                    'object_data': {
                                    '$elemMatch': {
                                        'violation': True,
                                        'roi_details': {
                                            '$exists': True,
                                            '$elemMatch': {
                                                'violation': True,
                                                'analytics_type': '2'
                                            }
                                        }
                                    }
                                                }}) 
                match_data_1 = {'timestamp':{'$regex': '^' + str(date.today())},
                                'analyticstype': 'RA',
                                'violation_status': True,
                                'object_data': {
                                            '$elemMatch': {
                                            'violation': True,
                                            '$or': [
                                                { 'roi_details.analytics_type': '0' }
                                            ]
                                            }
                                        }
                                }
                ra_count += PPERAVIOLATIONCOLLECTION.count_documents(match_data_1)
                total_count = cr_count +  ra_count + ppe_count +  protected_zone + ppe_crash_helemt_counts
                # total_count = cr_count +  ra_count + ppe_count +  protected_zone
                ret = {'message': {'total_count': total_count, 'ppe_count': ppe_count, 'ra_count': ra_count, 'tc_count': tc_count,'cr_count': cr_count, 'protection_zone': protected_zone, "ppe_crash_helemt_counts": ppe_crash_helemt_counts}, 'success': True}
                
            else:
                ret = {'message': 'data not found', 'success': False}       
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)


# @camera_status.route('/disable_camera_details', methods=['GET'])
@csrf_exempt
def disable_camera_details(request):
    ret = {'success': False, 'message':'something went wrong with get all solutions count api'}
    if request.method == 'GET':
        if 1:
        # try:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True}))
            if len(find_data_cam_status ) !=0 :
                disable_camara_details = []
                for fetch_data in find_data_cam_status:
                    ai_sln_dict = {}
                    if len(fetch_data['ai_solution']) !=0:
                        # print("fetch_data['ai_solution']------------------------------1111111111111", fetch_data["ai_solution"])
                        require_data = {'camera_name':fetch_data['cameraname'],'camera_ip': fetch_data['camera_ip'],'imagename':fetch_data['imagename'],'ai_solutions':ai_sln_dict}
                        if len(fetch_data['roi_data']) == 0 and len(fetch_data['tc_data']) == 0 and len(fetch_data['cr_data']) == 0 and len(fetch_data['ppe_data']) == 0 and fetch_data["analytics_status"] == 'false':
                            if len(fetch_data['ppe_data']) == 0 or fetch_data["analytics_status"] == 'false':
                                ai_sln_dict.update({"PPE" : False})
                                if (require_data not in disable_camara_details):
                                    disable_camara_details.append(require_data)
                            if len(fetch_data['roi_data']) == 0 or fetch_data["analytics_status"] == 'false':
                                ai_sln_dict.update({"RA" : False})
                                if (require_data not in disable_camara_details):
                                    disable_camara_details.append(require_data)
                            if len(fetch_data['tc_data']) == 0 or fetch_data["analytics_status"] == 'false':
                                ai_sln_dict.update({"TC" : False})
                                if (require_data not in disable_camara_details):
                                    disable_camara_details.append(require_data)
                            if len(fetch_data['cr_data']) == 0 or fetch_data["analytics_status"] == 'false':
                                if "CR" in fetch_data["ai_solution"]:
                                    if fetch_data["ai_solution"]["CR"] == True or fetch_data["ai_solution"]["CR"] == False or fetch_data["analytics_status"] == 'false': 
                                        ai_sln_dict.update({"CR" : False})
                                        if (require_data not in disable_camara_details):
                                            disable_camara_details.append(require_data)

                        if True not in fetch_data['ai_solution'].values() or fetch_data["analytics_status"] == 'false':
                            ai_sln_dict.update({"CR" : False})
                            require_data['ai_solutions'] = fetch_data["ai_solution"]
                            if (require_data not in disable_camara_details):
                                disable_camara_details.append(require_data)

                        if "firesmoke_data" in fetch_data.keys():
                            firesmoke_data = fetch_data['firesmoke_data']
                            if len(firesmoke_data) != 0:
                                # print("fetch_data['ai_solution']", fetch_data["ai_solution"])
                                if "dust" in fetch_data["ai_solution"].keys():
                                    if fetch_data["ai_solution"]["dust"] == False and fetch_data['analytics_status'] == 'False':
                                        ai_sln_dict['Dust']=True

                                if "fire" in fetch_data["ai_solution"].keys():
                                    if fetch_data["ai_solution"]["fire"] == False and fetch_data['analytics_status'] == 'False':
                                        ai_sln_dict['Fire']=True
            else:
                ret['message']='analytics disabled for all the cameras.'
                    
            ret = {'message': disable_camara_details, 'success': True}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- disable_camera_details 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- disable_camera_details 2", str(error), " ----time ---- ", now_time_with_time()]))         
    
    return JsonResponse(ret)

# @camera_status.route('/get_not_working_camera_details', methods=['GET'])
@csrf_exempt
def get_not_working_camera_details(request):
    ret = {'message':'Somthing went wrong.','success':False}
    if request.method == 'GET':
        if 1:
        # try:
            EnabledCameras = list(ppera_cameras.find({'camera_status': True}))
            not_working_cam_data_details = []
            """Calling function to get the working camera list and not woorking camera list"""
            wcam_list_and_nwcam_list = EnabledCameras#GETNOTWORKINGCAMERADETAILS(EnabledCameras)
            if len(wcam_list_and_nwcam_list) !=0:
                for url in wcam_list_and_nwcam_list:
                    if url['camera_ip'] == None:
                        if url['rtsp_url'] != None:
                            if RTSPVERIFY(url['rtsp_url']):
                                print()
                            else:
                                not_working_cam_data_details.append({'camera_name': url['cameraname'],'camera_ip': url['camera_ip'], 'rtsp_url': url['rtsp_url'], 'imagename': url['imagename']})
                                # not_working_cam_data = {'camera_name': url['cameraname'],'camera_ip': url['camera_ip'], 'rtsp_url': url['rtsp_url'], 'imagename': url['imagename']}
                    else:
                        result = asyncio.run(run_ping(url['camera_ip']))
                        if result[0] is True:
                            print()
                        else:
                            not_working_cam_data_details.append({'camera_name': url['cameraname'],'camera_ip': url['camera_ip'], 'rtsp_url': url['rtsp_url'], 'imagename': url['imagename']})
                            # not_working_cam_data = {'camera_name': url['cameraname'],'camera_ip': url['camera_ip'], 'rtsp_url': url['rtsp_url'], 'imagename': url['imagename']}
                    # not_working_cam_data_details.append(not_working_cam_data)
                ret = {'message': not_working_cam_data_details, 'success': True}
            else:
                ret['message']='all the cameras are working. or please add the camera.'
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_not_working_camera_details 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_not_working_camera_details 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return JsonResponse(ret)

#UPDATE "get_all_solns_enable_cam_details" FUNCTION
# @camera_status.route('/get_all_solns_enable_cam_details', methods=['GET'])
@csrf_exempt
def get_all_solns_enable_cam_count(request):
    ret = {'success': False, 'message':'something went wrong with get all solutions count api'}
    if request.method == 'GET':
        if 1:
        # try:
            require_data_details = []
            """Calling function to get the diable camera list."""
            fun_get_enable_cam_list = NewEnabledcameras(list(ppera_cameras.find({'camera_status': True, 'analytics_status':'true'}))) 
            # print("fun_get_enable_cam_list:--------------", fun_get_enable_cam_list)
            if len(fun_get_enable_cam_list) !=0 :
                for enable_cam_nam in fun_get_enable_cam_list:
                    # print("enable_cam_nam-----------------", enable_cam_nam.keys())
                    cr_data = enable_cam_nam['cr_data']
                    tc_data = enable_cam_nam['tc_data']
                    ppe_data = enable_cam_nam['ppe_data']
                    roi_data = enable_cam_nam['roi_data']
                    ai_sln_dict = {"CR" : False,"TC" : False,"RA":False,"PPE":False, "Dust":False, "Fire":False, 'crash_helmet':False, 'Traffic_Jam':False, 'Vehicle_parking':False}
                    if len(enable_cam_nam['ai_solution']) !=0:
                        require_data = {'camera_name':enable_cam_nam['cameraname'],'camera_ip': enable_cam_nam['camera_ip'],'imagename':enable_cam_nam['imagename'],'ai_solutions':ai_sln_dict}            
                        if len(cr_data) != 0 or len(tc_data) != 0 or len(ppe_data) != 0 or len(roi_data) != 0: 
                            if len(cr_data) != 0:
                                if enable_cam_nam["ai_solution"]["CR"] == True and enable_cam_nam['analytics_status'] == 'true': 
                                    ai_sln_dict['CR']=True
                                    
                            if len(tc_data) != 0:
                                if enable_cam_nam["ai_solution"]["TC"] == True and enable_cam_nam['analytics_status'] == 'true':
                                    ai_sln_dict['TC']=True

                            if len(ppe_data) != 0:
                                if (len(ppe_data) and any(value is True for value in ppe_data[0].values())) != 0:           
                                    if enable_cam_nam["ai_solution"]["PPE"] == True  and enable_cam_nam['analytics_status'] == 'true':
                                        ai_sln_dict['PPE']=True
                                
                                if 'crash_helmet' in ppe_data[0].keys():
                                    ai_sln_dict['crash_helmet']=True 

                            if len(roi_data) != 0:
                                if "RA" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["RA"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        # print("")
                                        ai_sln_dict['RA']=True

                                if "Protection_Zone" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["Protection_Zone"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        # print("")
                                        ai_sln_dict['Protection_Zone']=True

                        if "firesmoke_data" in enable_cam_nam.keys():
                            firesmoke_data = enable_cam_nam['firesmoke_data']
                            if len(firesmoke_data) != 0:
                                if "dust" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["dust"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        ai_sln_dict['Dust']=True

                                if "fire" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["fire"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        ai_sln_dict['Fire']=True

                        if "trafficjam_data" in enable_cam_nam.keys():
                            traffic_jam_data = enable_cam_nam['trafficjam_data']
                            if len(traffic_jam_data) != 0:
                                if "Traffic_Jam" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["Traffic_Jam"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        ai_sln_dict['Traffic_Jam']=True

                        if "vpms_data" in enable_cam_nam.keys():
                            vpms_data = enable_cam_nam['vpms_data']
                            if len(vpms_data) != 0:
                                print("************************", enable_cam_nam["ai_solution"].keys())
                                if "Parking" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["Parking"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        ai_sln_dict['Parking']=True

                                if "NO_Parking" in enable_cam_nam["ai_solution"].keys():
                                    if enable_cam_nam["ai_solution"]["NO_Parking"] == True and enable_cam_nam['analytics_status'] == 'true':
                                        ai_sln_dict['NO_Parking']=True
                                    
                    require_data['ai_solutions'] = ai_sln_dict
                    require_data_details.append(require_data)
                    
                if len(require_data_details) !=0:
                    ret = {'message': require_data_details, 'success': True}    
                else:
                    ret['message']='analytics disabled for all the cameras.'               
                    
            else:
                ret['message']='there are no cameras added for analytics or cameras analytics is disabled.'
    return JsonResponse(ret)


# @camera_status.route('/get_enble_ppe_violation_count', methods=['GET'])
@csrf_exempt
def get_enble_ppe_violation_count(request):
    ret = {'message':'Someting went wrong api','success':False}
    if request.method == 'GET':
        if 1:
        # try:
            find_data_cam_status =ppera_cameras.find({'camera_status': True})
            HELMET_count = 0
            VEST_count = 0
            for find_data in find_data_cam_status:
                if len(find_data['ppe_data']) == 0:
                    print('YES NO VIOLATIONS ARE THERE')
                
                else:
                    ppe_data = find_data['ppe_data']
                    if len(ppe_data) != 0:
                        ppe_objects = ['vest', 'helmet', 'shoes']
                        for ppe_array in ppe_data:
                            if any(ppe_key in ppe_objects for ppe_key in ppe_array.keys()):
                                if any(ppe_val is True for ppe_val in ppe_array.values()):
                                    match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': find_data['rtsp_url'], 'analyticstype': 'PPE_TYPE1', '$or': [
                {"object_data.Helmet": False},
                {"object_data.Vest": "no_ppe"}
            ]}
                                    data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}])) # , {'$limit': 2}])
                                    if len(data) != 0:
                                        ppepercentage = filterviolations.find_one({},{'_id':0})
                                        if ppepercentage  is None:
                                            ppepercentage = {"helmet":30,"vest":30}                                  
                                        for count, i in enumerate(data):
                                            if i['analyticstype'] == 'PPE_TYPE1':
                                                object_data = i['object_data']
                                                if len(object_data) == 1:
                                                    if object_data[0]['class_name'] == 'person':
                                                        if object_data[0]['Helmet'] == False:
                                                            if object_data[0]['algorithm_details']:
                                                                if get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                                                                    HELMET_count += 1

                                                                elif get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                                                    VEST_count += 1

                                                        elif object_data[0]['Vest'] == 'no_ppe':
                                                            if object_data[0]['algorithm_details']:
                                                                if get_ppe_vest_violation(object_data[0]['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                                                    VEST_count += 1

                                                                elif get_ppe_helmet_violation(object_data[0]['algorithm_details'],ppepercentage['helmet'])=='false':
                                                                    HELMET_count += 1


                                                elif len(object_data) > 1:
                                                    for ___, jjj in enumerate(object_data):
                                                        if jjj['class_name'] == 'person':
                                                            if jjj['Helmet'] == False:
                                                                if jjj['algorithm_details']:
                                                                    if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                                                        HELMET_count += 1

                                                                    elif get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                                                        VEST_count += 1

                                                            elif jjj['Vest'] == 'no_ppe':
                                                                if jjj['algorithm_details']:
                                                                    if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                                                        VEST_count += 1

                                                                    elif get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                                                        HELMET_count += 1
                                    

            ret = {'message': [{'helmet_count': HELMET_count, 'vest_count': VEST_count}], 'success': True}

        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- 4 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- get_enble_ppe_viola44tion_count 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(ret)

# @camera_status.route('/to_get_today_data', methods=['POST'])
@csrf_exempt
def to_get_today_data(request):
    ret = {'message':'Something went wrong to get today data','success':False}
    if request.method == 'POST':
        if 1:
        # try:
            data = json.loads(request.body)
            request_key_array = ['camera_name', 'camera_rtsp']
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    if data['analyticstype'] == 'PPE_TYPE1':
                        match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': data['camera_rtsp'], 'camera_name': data['camera_name'], 'analyticstype': 'PPE_TYPE1', '$or': [
                {"object_data.Helmet": False},
                {"object_data.Vest": "no_ppe"}
            ]}
                    else:
                        match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': data['camera_rtsp'], 'camera_name':data['camera_name'], 'analyticstype': data['analyticstype']}
                    testing = len(list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data},{'$sort': {'timestamp': -1}}])))
                    fetch_to_verify_rtsp = PPERAVIOLATIONCOLLECTION.find_one({'timestamp': { '$regex': '^' + str(date.today())}, 'camera_rtsp': data['camera_rtsp']})
                    fetch_to_verify_cam_name = PPERAVIOLATIONCOLLECTION.find_one({'timestamp':{'$regex': '^' + str(date.today())}, 'camera_name': data['camera_name']})
                    if testing != 0:
                        ret = {'message': {'violation_counts_testing': testing},'success': True}
                    elif fetch_to_verify_rtsp == None and fetch_to_verify_cam_name == None:
                        ret = {'message': "Given 'camera_name' and 'camera_rtsp' is not existed, please give the valid one.", 'success': False}
                    elif fetch_to_verify_cam_name == None:
                        ret = {'message':"Given 'camera_name' is not existed, please give the valid one." , 'success': False}
                    elif fetch_to_verify_rtsp == None:
                        ret = {'message': "Given 'camera_rtsp' is not existed, please give the valid one." , 'success': False}
                    else:
                        ret = {'message':   "You have given invalid 'camera_name' and 'camera_rtsp', give the valid one.", 'success': False}
            else:
                ret = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- to_get_today_data 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- to_get_today_data 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)


# @camera_status.route('/data_betweem_violations_count', methods=['POST'])
@csrf_exempt
def data_betweem_violations_count(request):
    result = {'message': "something went wrong",'success':False}
    if request.method == 'POST':
        if 1:
        # try:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        from_date = data['from_date']
                        to_date = data['to_date']
                        list_data = list(PPERAVIOLATIONCOLLECTION.find({'timestamp': {'$gte': from_date, '$lt': to_date}}))
                        if len(list_data) != 0:
                            ppe_count = 0
                            ra_count = 0
                            tc_count = 0
                            cr_count = 0
                            total_count = 0
                            for count, i in enumerate(list_data):
                                total_count += 1
                                if i['analyticstype'] == 'PPE_TYPE1':
                                    ppe_count += 1
                                if i['analyticstype'] == 'RA':
                                    ra_count += 1
                                if i['analyticstype'] == 'TC':
                                    tc_count += 1
                                if i['analyticstype'] == 'CR':
                                    cr_count += 1
                            result = {'message': {'total_count': total_count,'ppe_count': ppe_count, 'ra_count': ra_count, 'tc_count': tc_count, 'cr_count': cr_count},'success': True}
                else:
                    result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- data_betweem_violations_count 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     result['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     result['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- data_betweem_violations_count 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(result)


# @camera_status.route('/date_wise_violations_count', methods=['POST'])
@csrf_exempt
def date_wise_given_violation_count(request):
    result = {'message': 'Something went wrong to the violation count API.','success':False}
    if request.method == 'POST':
        if 1:
        # try:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date'] #, 'violation_type']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        result['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        from_date = data['from_date']
                        to_date = data['to_date']
                        ppepercentage = filterviolations.find_one({},{'_id':0})
                        if ppepercentage  is None:
                            ppepercentage = {"helmet":30,"vest":30}
                        ppe_count = 0
                        ra_count = 0
                        tc_count = 0
                        cr_count = 0
                        total_count = 0
                        protected_zone = 0
                        require_data_test = {'total_count':total_count,'ppe_count':ppe_count,'ra_count':ra_count,'cr_count':cr_count,'tc_count':tc_count}
                        camera_status_true_data = list(ppera_cameras.find({'camera_status': True}))
                        match_stage = {
                                        'timestamp': {'$gte': from_date, '$lt': to_date},
                                        'analyticstype': 'RA',
                                        'violation_status': True
                                    }

                        # Define the aggregation pipeline with $facet to separate the counts
                        pipeline = [
                            {'$match': match_stage},
                            {'$facet': {
                                'count_type_0': [
                                    {'$match': {'object_data': {'$elemMatch': {'violation': True, 'roi_details.analytics_type': '0'}}}},
                                    {'$count': 'count'}
                                ],
                                'count_type_2': [
                                    {'$match': {'object_data': {
                                                    '$elemMatch': {
                                                        'violation': True,
                                                        'roi_details': {
                                                            '$exists': True,
                                                            '$elemMatch': {
                                                                'violation': True,
                                                                'analytics_type': '2'
                                                            }
                                                        }
                                                    }
                                                }}},
                                    {'$count': 'count'}
                                ]
                            }}
                        ]

                        # Execute the aggregation query
                        result = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))

                        # Extract counts from the result
                        ra_count = result[0]['count_type_0'][0]['count'] if result[0]['count_type_0'] else 0
                        protected_zone = result[0]['count_type_2'][0]['count'] if result[0]['count_type_2'] else 0

                        print("Count for analytics_type 0:", ra_count)
                        print("Count for analytics_type 2:", protected_zone)
                    
                        for data in camera_status_true_data:
                            match_data = {'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': data['rtsp_url']}
                            
                            list_data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}]))
                            ppe_values = data['ppe_data'] #[0] 
                            if len(data['ppe_data']) != 0 and (ppe_values[0]['helmet'] == True or ppe_values[0]['vest'] == True): 
                                ppe_data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': {'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': data['rtsp_url'], 'analyticstype': 'PPE_TYPE1', '$or': [
                {"object_data.Helmet": False},
                {"object_data.Vest": "no_ppe"}
            ]}}, {'$sort': {'timestamp': -1}}])) 
                                ppe_overall_data = fun_ppe_violations_count(ppe_data)      
                                
                                ppe_count += ppe_overall_data["ppe_counts"]
                            if len(data['cr_data']) != 0:
                                cr_count += PPERAVIOLATIONCOLLECTION.count_documents({'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': data['rtsp_url'], 'analyticstype': 'CRDCNT'}) #list(mongo.db.data.aggregate([{'$match': {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': x_data['rtsp_url'], 'analyticstype': 'CRDCNT'}}, {'$sort': {'timestamp': -1}}]))
                                

                        total_count = cr_count+ ra_count + ppe_count + protected_zone
                        result = {'message': {'total_count':total_count, 'ppe_count': ppe_count, 'ra_count': ra_count, 'tc_count': tc_count, 'cr_count': cr_count, 'protection_zone':protected_zone}, 'success': True}
                        
                else: 
                    result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- date_wise_given_violation_count 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     result['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     result['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- date_wise_given_violation_count 2", str(error), " ----time ---- ", now_time_with_time()])) 
    return JsonResponse(result)

# @camera_status.route('/data_between_date', methods=['POST'])
@csrf_exempt
def data_between_date(request):
    result = {'message': 'something went wrong with data_between_date','success':False}
    if request.method == 'POST':
        if 1:
        # try:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        from_date = data['from_date']
                        to_date = data['to_date']
                        FOUNDDATA =list(PPERAVIOLATIONCOLLECTION.find({'timestamp': {'$gte':from_date, '$lt': to_date}},{"_id":0}))
                        if len(FOUNDDATA)  !=0:
                            result = {'message': FOUNDDATA, 'success': True}
                        else:
                            result['message']='there is no violation data found.'
                else:
                    result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- data_between_date 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     result['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     result['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- data_between_date 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(result)

# @camera_status.route('/cam_wise_PPE_violations_count', methods=['GET'])
@csrf_exempt
def ppe_violations_count_cam_wise(request):
    ret = {'message': 'something went wrong with ppe_violation coutn cam wise ','success': False}
    if request.method == 'GET':
    # try:
        if 1:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True,'ppe_data':{'$exists':True,"$ne": []}}))
            if len(find_data_cam_status) !=0 :
                ppe_require_data = []
                for let, ppe_da in enumerate(find_data_cam_status):
                    ppe_values = ppe_da['ppe_data'] #[0]
                    print('-----------------ppe_values----------ppe_values',ppe_values)
                    if type(ppe_da['ppe_data'][0]) == dict :
                        match_data = {}
                        if 'helmet' in ppe_values[0] and 'vest' in ppe_values[0]:
                            if  (ppe_values[0]['helmet'] == True or ppe_values[0]['vest'] == True):
                                match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': ppe_da['rtsp_url'], 'analyticstype': 'PPE_TYPE1', '$or': [
                                                    {"object_data.Helmet": False},
                                                    {"object_data.Vest": "no_ppe"}
                                                ]}
                        elif  'helmet' in ppe_values[0] :
                            if  (ppe_values[0]['helmet'] == True ):
                                match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': ppe_da['rtsp_url'], 'analyticstype': 'PPE_TYPE1', '$or': [
                                                    {"object_data.Helmet": False},
                                                    {"object_data.Vest": "no_ppe"}
                                                ]}
                        elif   'vest' in ppe_values[0] :
                            if  (ppe_values[0]['vest'] == True ):
                                match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': ppe_da['rtsp_url'], 'analyticstype': 'PPE_TYPE1', '$or': [
                                                    {"object_data.Helmet": False},
                                                    {"object_data.Vest": "no_ppe"}
                                                ]}
                        # match_data = {
                        #         'timestamp': {'$regex': '^' + str(date.today())},
                        #         'camera_rtsp': ppe_da['rtsp_url'],
                        #         'analyticstype': 'PPE_TYPE1',
                        #         '$and': [
                        #             {"object_data.Helmet": False},
                        #             {"object_data.Vest": "no_ppe"}
                        #         ]
                        #     }
                        ppe_data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}])) 
                        if len(ppe_data) != 0:
                            # ppe_count = fun_ppe_violations_count(ppe_data)
                            ppe_require_data.append({'camera_name':ppe_da['cameraname'], 'camera_ip': ppe_da[ 'camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'ppe_type_counts': len(ppe_data)}) # ppe_count["ppe_counts"], 'helmet_count':ppe_count["helmet_cnts"], 'vest_count':ppe_count["vest_cnts"]}) #ppe_count}) #len(ppe_data)})
                        # else:
                        #     ppe_require_data.append({'camera_name': ppe_da['cameraname'], 'camera_ip': ppe_da['camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'ppe_type_counts':len(ppe_data), 'helmet_count':0, 'vest_count':0})

                if len(ppe_require_data) != 0:
                    ret = {'message': ppe_require_data, 'success': True}
                else:
                    ret['message'] = 'No PPE Violations Detected' #'ppe data not found.'
            else:
                ret['message']= "No cameras have been added for PPE analytics. Please add a camera." #'there no camera enabled for ppe,please add camera and enable for ppe'
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)

"""CURRENT DATE TC VIOLATIONS CAMERA DETAILS"""
# @camera_status.route('/cam_wise_TC_violations_details', methods=['GET'])
@csrf_exempt
def TC_violations_count_cam_wise(request):
    ret = {'message':'Someting went wrong cam_wise_TC_violations_details','success':False}
    if request.method == 'GET':
        if 1:
        # try:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True}))
            if len(find_data_cam_status):
                tc_require_data_details = []
                for find_data in find_data_cam_status:
                    """Calling function to get the working camera list and not woorking camera list"""
                    match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': find_data['rtsp_url']} #, 'analyticstype': 'TC'}
                    tc_data = list(trafficcountdata.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}]))
                    if len(tc_data) != 0:
                        tc_require_data = {'camera_name':find_data['cameraname'], 'camera_ip':find_data['camera_ip'], 'rtsp_url':find_data['rtsp_url'], 'imagename': find_data['imagename'],'tc_type_counts': len(tc_data)}
                        if (tc_require_data not in tc_require_data_details):
                            tc_require_data_details.append(tc_require_data)

                if len(tc_require_data_details) !=0:
                    ret = {'message': tc_require_data_details, 'success': True}

                else:
                    ret['message']= 'No TC Violations Detected' #'there is no violation found.'

            else:
                ret['message']= "No cameras have been added for TC analytics. Please add a camera" 

        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- TC_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()]))  
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- TC_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)

# @camera_status.route('/cam_wise_RA_violations_count', methods=['GET'])
@csrf_exempt
def RA_violations_count_cam_wise(request):
    ret = {'message': 'Something went wrong cam_wise_RA_violations_details', 'success': False}
    if request.method == "GET":
        find_data_cam_status = ppera_cameras.find({'camera_status': True}, {'cameraname': 1, 'camera_ip': 1, 'rtsp_url': 1, 'imagename': 1, 'roi_data': 1})
        
        roi_require_data_details = []

        camera_rtsp_urls = []
        camera_details = {}
        
        for find_data in find_data_cam_status:
            if find_data.get('roi_data'):
                camera_rtsp_urls.append(find_data['rtsp_url'])
                camera_details[find_data['rtsp_url']] = {
                    'camera_name': find_data['cameraname'],
                    'camera_ip': find_data['camera_ip'],
                    'rtsp_url': find_data['rtsp_url'],
                    'imagename': find_data['imagename']
                }
        
        if camera_rtsp_urls:
            today_str = str(date.today())
            match_data = {
                'timestamp': {'$regex': '^' + today_str},
                'camera_rtsp': {'$in': camera_rtsp_urls},
                'analyticstype': 'RA',
                'violation_status': True,
                'object_data': {
                    '$elemMatch': {
                        'violation': True,
                        '$or': [{'roi_details.analytics_type': '0'}]
                    }
                }
            }
            
            violation_data = PPERAVIOLATIONCOLLECTION.aggregate([
                {'$match': match_data},
                {'$group': {'_id': '$camera_rtsp', 'violation_count': {'$sum': 1}}},
                {'$sort': {'_id': 1}}
            ])
            
            for vd in violation_data:
                camera_info = camera_details.get(vd['_id'])
                if camera_info:
                    roi_require_data_details.append({
                        'camera_name': camera_info['camera_name'],
                        'camera_ip': camera_info['camera_ip'],
                        'rtsp_url': camera_info['rtsp_url'],
                        'imagename': camera_info['imagename'],
                        'roi_type_counts': vd['violation_count']
                    })

        if roi_require_data_details:
            ret = {'message': roi_require_data_details, 'success': True}
        else:
            ret['message'] = 'No RA Violations Detected'

    return JsonResponse(ret)


"""CURRENT DATE TRUCK REVERSAL VIOLATION CAMERA DETAILS"""
# @camera_status.route('/cam_wise_truck_reversal_RA_violations_count', methods=['GET'])
@csrf_exempt
def cam_wise_truck_reversal_RA_violations_count(request):
    ret = {'message':'Someting went wrong cam_wise_truck_reversal_RA_violations_count','success':False}
    if request.method == "GET":
        if 1:
        # try:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True}))
            roi_require_data_details = []
            if len(find_data_cam_status) !=0:
                for find_data in find_data_cam_status:
                    """Calling function to get the working camera list and not woorking camera list"""
                    match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': find_data['rtsp_url']}
                    roi_data = find_data['roi_data']
                    if len(roi_data) != 0:
                        # match_data['analyticstype']='RA'
                        match_data_RA = {'timestamp':{'$regex': '^' + str(date.today())},'camera_rtsp': find_data['rtsp_url'],
                                'analyticstype': 'RA',
                                'violation_status': True,
                                'object_data': {
                                            '$elemMatch': {
                                            'violation': True,
                                            '$or': [
                                                { 'roi_details.analytics_type': '0' }
                                            ]
                                            }
                                        }
                                }
                        # print("-----------------------------TESTING-roi_data-----------------------------", match_data)
                        # if "object_data" in match_data.keys():
                        #     for obj_d in match_data['object_data']: 
                        #         print("OBJECT_DATA OF ROI:-------------", obj_d)
                        ViolationFOUNDDATAfinddata = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data_RA}, {'$sort': {'_id': -1}}]))
                        
                        match_data_TRA = {'timestamp':{'$regex': '^' + str(date.today())},'camera_rtsp': find_data['rtsp_url'],
                                'analyticstype': 'RA',
                                'violation_status': True,
                                'object_data': {
                                                    '$elemMatch': {
                                                        'violation': True,
                                                        'roi_details': {
                                                            '$exists': True,
                                                            '$elemMatch': {
                                                                'violation': True,
                                                                'analytics_type': '2'
                                                            }
                                                        }
                                                    }
                                                }
                                }

                        # # truck_reversal_count = 0
                        # if len(ViolationFOUNDDATAfinddata) != 0:
                        #     truck_reversal_count = 0
                        #     for x_viol_data in ViolationFOUNDDATAfinddata:
                        #         print("truck_reversal_count LIST:----", truck_reversal_count)
                        #         if "object_data" in x_viol_data.keys() :
                        #             for obj_d in x_viol_data['object_data']: 
                        #                 print("OBJECT_DATA OF ROI:-------------", obj_d["roi_details"])
                        #                 if len(obj_d["roi_details"]) ==1:
                        #                     if obj_d["roi_details"][0]["analytics_type"] == "2" and obj_d["roi_details"][0]["violation"] == True:
                        #                         truck_reversal_count +=1
                        #                         print("truck_reversal_count LIST:---11111111111111-", truck_reversal_count)

                        #                 else:
                        #                     print("OBJECT_DATA OF ROI:------------222222222222", obj_d["roi_details"])
                        #                     for x in obj_d["roi_details"]:
                        #                         print("VALUE OF x---------------", x)
                        #                         if x["analytics_type"] == "2" and x["violation"] == True:
                        #                             truck_reversal_count +=1
                        #                             print("truck_reversal_count LIST:---22222222222-", truck_reversal_count)
                        truck_reversal_counts = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data_TRA}]))
                        if len(truck_reversal_counts) != 0:
                            roi_require_data = {'camera_name': find_data['cameraname'], 'camera_ip': find_data['camera_ip'], 'rtsp_url': find_data['rtsp_url'], 'imagename':find_data['imagename'],'protection_zone_type_counts': len(truck_reversal_counts)} #len(ViolationFOUNDDATAfinddata)}

                    # roi_require_data = {'camera_name': find_data['cameraname'], 'camera_ip': find_data['camera_ip'], 'rtsp_url': find_data['rtsp_url'], 'imagename':find_data['imagename'],'roi_type_counts': len(ViolationFOUNDDATAfinddata)}
                    # if (roi_require_data not in roi_require_data_details):
                            if roi_require_data not in roi_require_data_details:
                                roi_require_data_details.append(roi_require_data)
                        # print(x_viol_data)
                        # else:
                        #     ViolationFOUNDDATAfinddata = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'_id': -1}}]))
                        #     roi_require_data = {'camera_name': find_data['cameraname'], 'camera_ip': find_data['camera_ip'], 'rtsp_url': find_data['rtsp_url'], 'imagename':find_data['imagename'],'roi_type_counts': len(ViolationFOUNDDATAfinddata)}
                        #     # if (roi_require_data not in roi_require_data_details):
                        #     roi_require_data_details.append(roi_require_data)
                            
                if len(roi_require_data_details) !=0:
                    ret = {'message': roi_require_data_details, 'success': True} 

                else:
                    ret['message']= 'No PROTECTED-ZONE violations detected' #'there is no data found for RA camera .'
            else:
                ret['message']= "No cameras have been added for PROTECTED-ZONE analytics. Please add a camera"  #'there are no cameras are added for RA analytics please add the camera.'
                

            #ret = {'message': roi_require_data_details, 'success': True} 
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- RA_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()]))  
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- RA_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)

"""CURRENT DATE CR VIOLATION CAMERA DETAILS"""
# @camera_status.route('/cam_wise_CR_violations_count', methods=['GET'])
@csrf_exempt
def CR_violations_count_cam_wise(request):
    ret = {'message':'Someting went wrong cam_wise_CR_violations_details','success':False}
    if request.method == "GET":
        if 1:
        # try:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True, 'cr_data':{'$exists':True,"$ne": []}}))
            if len(find_data_cam_status) !=0:
                cr_require_data_details = []
                for find_data in find_data_cam_status:
                    match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': find_data['rtsp_url'], 'analyticstype': 'CRDCNT'}
                    FoundCrData = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, { '$sort': {'timestamp': -1}}]))
                    if len(FoundCrData) != 0:
                        cr_require_data = {'camera_name': find_data['cameraname'],'camera_ip': find_data['camera_ip'], 'rtsp_url': find_data['rtsp_url'], 'imagename': find_data['imagename'],'cr_type_counts': len(FoundCrData)}
                        if (cr_require_data not in cr_require_data_details):
                            cr_require_data_details.append(cr_require_data)
                if len(cr_require_data_details) !=0:
                    ret = {'message': cr_require_data_details, 'success': True}
                else:
                    ret['message']= 'No CR Violations Detected' #'there is no violation found.'
            else:
                ret['message']= "No cameras have been added for CR analytics. Please add a camera"  #'there are no cameras are added for CR analytics please add the camera.' #'there is no camera added.'        
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- CR_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()]))   
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- CR_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(ret)

"""CURRENT DATE CRASH HELMET VIOLATION CAMERA DETAILS"""
# @camera_status.route('/cam_wise_PPE_Crash_helmet_violations_count', methods=['GET'])
@csrf_exempt
def ppe_Crash_helmet_violations_count_cam_wise(request):
    ret = {'message': 'something went wrong with cam_wise_PPE_Crash_helmet_violations_count api ','success': False}
    if request.method == "GET":
        if 1:
            find_data_cam_status = list(ppera_cameras.find({'camera_status': True,'ppe_data':{'$exists':True,"$ne": []}}))
            if len(find_data_cam_status) !=0 :
                ppe_ch_require_data = []
                for let, ppe_da in enumerate(find_data_cam_status):
                    ppe_values = ppe_da['ppe_data'] #[0]
                    if type(ppe_da['ppe_data'][0]) == dict:
                        if 'crash_helmet' in ppe_values[0].keys():
                            if ppe_values[0]['crash_helmet'] == True:
                                match_data = {'timestamp': {'$regex': '^' + str(date.today())}, 'camera_rtsp': ppe_da['rtsp_url'], 'analyticstype': 'PPE_TYPE2'}
                                ppe_ch_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}])) 
                                if len(ppe_ch_data) != 0:
                                    # crash_helmet_counts = fun_ppe_crash_helmet_violations_count(ppe_data) 
                                    ppe_ch_require_data.append({'camera_name':ppe_da['cameraname'], 'camera_ip': ppe_da[ 'camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'crash_helmet_count':len(ppe_ch_data)}) #, crash_helmet_counts["crash_helmet_cnts"]}) #ppe_count}) #len(ppe_data)})
                                # else:
                                #     ppe_require_data.append({'camera_name': ppe_da['cameraname'], 'camera_ip': ppe_da['camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'crash_helmet_count':0})


                if len(ppe_ch_require_data) != 0:
                    ret = {'message': ppe_ch_require_data, 'success': True}
                else:
                    ret['message'] = 'No CRASH-HELMET Violations Detected' #'ppe data not found.'
            else:
                ret['message']= "No cameras have been added for CRASH-HELMET analytics. Please add a camera" #'there no camera enabled for ppe,please add camera and enable for ppe'
                
    return JsonResponse(ret)

"""CURRENT DATE FIRE CAMERAS COUNT"""
# @camera_status.route('/FIREviolationCount', methods=['GET','POST'])
def FIREviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get FIREviolationCount api'}    
    FIREviolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    rtsp_url = data['rtsp_url']
                    # match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'firesmoke_data','violation_status': True,
                                #   'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}}
                    match_data = {
                        'timestamp':{'$gte': from_date, '$lte': to_date}, 
                        'camera_name':  department, #d_data['cameraname'], 
                        'camera_rtsp':rtsp_url, #d_data['rtsp_url'],
                        'analytics_details.details.obj_details.class_name':'fire'
                        }
                    # FIRE_violation_data = firesmokedustDetails.count_documents(match_data)
                    # Use distinct to get unique ticket numbers matching the query
                    distinct_ticket_nos = firesmokeviolationdata.distinct('ticket_no', match_data)

                    # The length of this list gives you the count of unique ticket_no values
                    # FIRE_violation_data = len(distinct_ticket_nos)
                    # FIRESMOKEviolationCount = mongo.db.data.count_documents(match_data)
                    ret = {'success': True, 'message': {'raviolationcount': len(distinct_ticket_nos)}} #FIRESMOKEviolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        match_data = {
                        'timestamp': {'$regex': '^' + str(date.today())}, 
                        # 'camera_name':  department, #d_data['cameraname'], 
                        # 'camera_rtsp': rtsp_url, #d_data['rtsp_url'],
                        'analytics_details.details.obj_details.class_name':'fire',
                        'analytics_details.details.obj_details.violation':True
                        }
        
        distinct_ticket_nos = firesmokeviolationdata.distinct('ticket_no', match_data)

            # The length of this list gives you the count of unique ticket_no values
        FIREviolationCount = len(distinct_ticket_nos)
        ret = {'success': True, 'message': {'firesmokeviolationcount':FIREviolationCount}}  
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)


# 25/11/2024
"""FIRE SOLUTION ENABLED CAMERAS """
# @camera_status.route('/cam_wise_FIRE_violations_details', methods=['GET'])
@csrf_exempt
def fire_violations_count_cam_wise(request):
    ret = {'message': 'Something went wrong cam_wise_FIRE_violations_details', 'success': False}
    if request.method == "GET":
        find_data_cam_status = ppera_cameras.find({'camera_status': True}, {'cameraname': 1, 'camera_ip': 1, 'rtsp_url': 1, 'imagename': 1, 'firesmoke_data': 1})
        
        FIRE_require_data_details = []
        camera_rtsp_urls = []
        camera_details = {}
        
        for find_data in find_data_cam_status:
            if find_data.get('firesmoke_data'):
                camera_rtsp_urls.append(find_data['rtsp_url'])
                camera_details[find_data['rtsp_url']] = {
                    'camera_name': find_data['cameraname'],
                    'camera_ip': find_data['camera_ip'],
                    'rtsp_url': find_data['rtsp_url'],
                    'imagename': find_data['imagename']
                }
        
        if camera_rtsp_urls:
            match_data = {
                            'timestamp': {'$regex': '^' + str(date.today())}, 
                            'analytics_details.details.obj_details.class_name':'fire',
                            'analytics_details.details.obj_details.violation':True
                            
                            }
            
            
            violation_data = firesmokeviolationdata.aggregate([
                {'$match': match_data},
                {'$group': {'_id': '$camera_rtsp', 'violation_count': {'$sum': 1}}},
                {'$sort': {'_id': 1}}
            ])
            
            for vd in violation_data:
                camera_info = camera_details.get(vd['_id'])
                if camera_info:
                    FIRE_require_data_details.append({
                        'camera_name': camera_info['camera_name'],
                        'camera_ip': camera_info['camera_ip'],
                        'rtsp_url': camera_info['rtsp_url'],
                        'imagename': camera_info['imagename'],
                        'fire_type_counts': vd['violation_count']
                    })

        if FIRE_require_data_details:
            ret = {'message': FIRE_require_data_details, 'success': True}

        else:
            ret['message'] = 'No FIRE Violations Detected'

    return JsonResponse(ret)


"""CURRENT DATE SMOKE CAMERAS COUNT"""
# @camera_status.route('/SMOKEviolationCount', methods=['GET','POST'])
@csrf_exempt
def SMOKEviolationCount(request):
    ret = {'success': False, 'message': 'something went wrong with get SMOKEviolationCount api'}    
    SMOKEviolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    rtsp_url = data['rtsp_url']
                    match_data = {
                        'timestamp':{'$gte': from_date, '$lte': to_date}, 
                        'camera_name':  department, #d_data['cameraname'], 
                        'camera_rtsp':rtsp_url, #d_data['rtsp_url'],
                        'analytics_details.details.obj_details.class_name':'smoke'
                        }
                    distinct_ticket_nos = firesmokeviolationdata.distinct('ticket_no', match_data)
                    # The length of this list gives you the count of unique ticket_no values
                    ret = {'success': True, 'message': {'raviolationcount': len(distinct_ticket_nos)}} #FIRESMOKEviolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        match_data = {
                        'timestamp': {'$regex': '^' + str(date.today())}, 
                        # 'camera_name':  department, #d_data['cameraname'], 
                        # 'camera_rtsp': rtsp_url, #d_data['rtsp_url'],
                        'analytics_details.details.obj_details.class_name':'smoke',
                        'analytics_details.details.obj_details.violation':True
                        
                        }
        
        distinct_ticket_nos = firesmokeviolationdata.distinct('ticket_no', match_data)

            # The length of this list gives you the count of unique ticket_no values
        SMOKEviolationCount = len(distinct_ticket_nos)
        ret = {'success': True, 'message': {'smokeviolationcount':SMOKEviolationCount}}  
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)

"""SMOKE SOLUTION ENABLED CAMERAS DETAILS"""
# @camera_status.route('/cam_wise_SMOKE_violations_details', methods=['GET'])
@csrf_exempt
def SMOKE_violations_count_cam_wise(request):
    ret = {'message': 'Something went wrong cam_wise_SMOKE_violations_details', 'success': False}
    if request.method == "GET":
        find_data_cam_status = ppera_cameras.find({'camera_status': True}, {'cameraname': 1, 'camera_ip': 1, 'rtsp_url': 1, 'imagename': 1, 'firesmoke_data': 1})
        
        SMOKE_require_data_details = []
        camera_rtsp_urls = []
        camera_details = {}
        
        for find_data in find_data_cam_status:
            if find_data.get('firesmoke_data'):
                camera_rtsp_urls.append(find_data['rtsp_url'])
                camera_details[find_data['rtsp_url']] = {
                    'camera_name': find_data['cameraname'],
                    'camera_ip': find_data['camera_ip'],
                    'rtsp_url': find_data['rtsp_url'],
                    'imagename': find_data['imagename']
                }
        
        if camera_rtsp_urls:
            match_data = {
                            'timestamp': {'$regex': '^' + str(date.today())}, 
                            'analytics_details.details.obj_details.class_name':'smoke',
                            'analytics_details.details.obj_details.violation':True
                            
                            }
            
            
            violation_data = firesmokeviolationdata.aggregate([
                {'$match': match_data},
                {'$group': {'_id': '$camera_rtsp', 'violation_count': {'$sum': 1}}},
                {'$sort': {'_id': 1}}
            ])
            
            for vd in violation_data:
                camera_info = camera_details.get(vd['_id'])
                if camera_info:
                    SMOKE_require_data_details.append({
                        'camera_name': camera_info['camera_name'],
                        'camera_ip': camera_info['camera_ip'],
                        'rtsp_url': camera_info['rtsp_url'],
                        'imagename': camera_info['imagename'],
                        'fire_type_counts': vd['violation_count']
                    })

        if SMOKE_require_data_details:
            ret = {'message': SMOKE_require_data_details, 'success': True}

        else:
            ret['message'] = 'No SMOKE Violations Detected'

    return JsonResponse(ret)

"""CURRENT DATE DUST CAMERAS COUNT"""
# @camera_status.route('/DUSTviolationCount', methods=['GET','POST'])
@csrf_exempt
def DUSTviolationCount(request):
    result = {'success': False, 'message': 'something went wrong with get DUSTviolationCount api'}    
    DUSTviolationCount = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)
        request_key_array = ['from_date', 'to_date','camera_name','department']
        if data != None:
            jsonobjectarray = list(set(data))
            # print(jsonobjectarray)
            missing_key = set(request_key_array).difference(jsonobjectarray)
            # print(missing_key)
            if not missing_key:
                output = [k for k, v in data.items() if v == '']
                if output:
                    # print(output)
                    result['message'] = " ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                else:
                    from_date = data['from_date']
                    to_date = data['to_date']
                    department = data['department']
                    camera_name =  data['camera_name']
                    rtsp_url = data['rtsp_url']
                    # match_data = {'timestamp': {'$gte': from_date, '$lt': to_date}, 'analyticstype': 'firesmoke_data','violation_status': True,
                                #   'object_data': {'$elemMatch': {'violation': True, '$or': [ { 'roi_details': { '$exists': False } },{ 'roi_details.analytics_type': '0' }]}}}
                    match_data = {
                        'timestamp':{'$gte': from_date, '$lte': to_date}, 
                        'camera_name':  department, #d_data['cameraname'], 
                        'camera_rtsp':rtsp_url, #d_data['rtsp_url'],
                        'analytics_details.details.obj_details.class_name':'dust'
                        }
                    # FIRE_violation_data = firesmokedustDetails.count_documents(match_data)
                    # Use distinct to get unique ticket numbers matching the query
                    distinct_ticket_nos = firesmokeviolationdata.distinct('ticket_no', match_data)

                    # The length of this list gives you the count of unique ticket_no values
                    # FIRE_violation_data = len(distinct_ticket_nos)
                    # FIRESMOKEviolationCount = mongo.db.data.count_documents(match_data)
                    ret = {'success': True, 'message': {'raviolationcount': len(distinct_ticket_nos)}} #FIRESMOKEviolationCount}}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
        else:
            result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']), 'success': False}
    elif request.method == 'GET':
        match_data = {
                        'timestamp': {'$regex': '^' + str(date.today())}, 
                        # 'camera_name':  department, #d_data['cameraname'], 
                        # 'camera_rtsp': rtsp_url, #d_data['rtsp_url'],
                        'analytics_details.details.obj_details.class_name':'dust',
                        'analytics_details.details.obj_details.violation':True
                        }
        
        distinct_ticket_nos = firesmokeviolationdata.distinct('ticket_no', match_data)

        # # The length of this list gives you the count of unique ticket_no values
        # DUSTviolationCount = len(distinct_ticket_nos)
        result = {'success': True, 'message': {'dustviolationcount':len(distinct_ticket_nos)}}  
    else:
        result={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(result)

"""DUST SOLUTION ENABLED CAMERAS """
# @camera_status.route('/cam_wise_DUST_violations_details', methods=['GET'])
@csrf_exempt
def DUST_violations_count_cam_wise(request):
    ret = {'message': 'Something went wrong cam_wise_DUST_violations_details', 'success': False}
    if request.method == "GET":
        find_data_cam_status = ppera_cameras.find({'camera_status': True}, {'cameraname': 1, 'camera_ip': 1, 'rtsp_url': 1, 'imagename': 1, 'firesmoke_data': 1})
        
        DUST_require_data_details = []
        camera_rtsp_urls = []
        camera_details = {}
        
        for find_data in find_data_cam_status:
            if find_data.get('firesmoke_data'):
                camera_rtsp_urls.append(find_data['rtsp_url'])
                camera_details[find_data['rtsp_url']] = {
                    'camera_name': find_data['cameraname'],
                    'camera_ip': find_data['camera_ip'],
                    'rtsp_url': find_data['rtsp_url'],
                    'imagename': find_data['imagename']
                }
        
        if camera_rtsp_urls:
            match_data = {
                            'timestamp': {'$regex': '^' + str(date.today())}, 
                            'analytics_details.details.obj_details.class_name':'dust',
                            'analytics_details.details.obj_details.violation':True
                            }
            
            violation_data = firesmokeviolationdata.aggregate([
                {'$match': match_data},
                {'$group': {'_id': '$camera_rtsp', 'violation_count': {'$sum': 1}}},
                {'$sort': {'_id': 1}}
            ])
            
            for vd in violation_data:
                camera_info = camera_details.get(vd['_id'])
                if camera_info:
                    DUST_require_data_details.append({
                        'camera_name': camera_info['camera_name'],
                        'camera_ip': camera_info['camera_ip'],
                        'rtsp_url': camera_info['rtsp_url'],
                        'imagename': camera_info['imagename'],
                        'dust_type_counts': vd['violation_count']
                    })

        if DUST_require_data_details:
            ret = {'message': DUST_require_data_details, 'success': True}

        else:
            ret['message'] = 'No DUST Violations Detected'

    return JsonResponse(ret)

"""CURRECT DATE ALL CAMERAS DETAILS violations"""
# @camera_status.route('/current_date_violations_cam_wise', methods=['GET'])
@csrf_exempt
def current_date_violations_details(request):
    result = {'message': 'something went wrong', 'success': False}
    if request.method == "GET":
        today_str = str(date.today())

        try:
            find_data_cam_status = list(ppera_cameras.find(
                {'camera_status': True},
                {'cameraname': 1, 'camera_ip': 1, 'rtsp_url': 1, 'imagename': 1}
            ))

            if not find_data_cam_status:
                result['message'] = 'There is no camera added for analytics, please add the camera.'
                # return jsonify(result)
                return JsonResponse(result)

            camera_rtsp_urls = [cam['rtsp_url'] for cam in find_data_cam_status]

            pipeline = [
                {'$match': {
                    'timestamp': {'$regex': '^' + today_str},
                    'camera_rtsp': {'$in': camera_rtsp_urls}
                }},
                {'$facet': {
                    'ppe_type_counts': [
                        {'$match': {
                            'analyticstype': 'PPE_TYPE1',
                            '$or': [
                                {"object_data.Helmet": False},
                                {"object_data.Vest": "no_ppe"}
                            ]
                        }},
                        {'$group': {'_id': '$camera_rtsp', 'count': {'$sum': 1}}}
                    ],
                    'ppe_crash_helemt_counts': [
                        {'$match': {'analyticstype': 'PPE_TYPE2'}},
                        {'$group': {'_id': '$camera_rtsp', 'count': {'$sum': 1}}}
                    ],
                    'cr_type_counts': [
                        {'$match': {'analyticstype': 'CRDCNT'}},
                        {'$group': {'_id': '$camera_rtsp', 'count': {'$sum': 1}}}
                    ],
                    'protection_zone_counts': [
                        {'$match': {
                            'analyticstype': 'RA',
                            'violation_status': True,
                            'object_data': {
                                '$elemMatch': {
                                    'violation': True,
                                    'roi_details': {
                                        '$exists': True,
                                        '$elemMatch': {
                                            'violation': True,
                                            'analytics_type': '2'
                                        }
                                    }
                                }
                            }
                        }},
                        {'$group': {'_id': '$camera_rtsp', 'count': {'$sum': 1}}}
                    ],
                    'roi_type_counts': [
                        {'$match': {
                            'analyticstype': 'RA',
                            'violation_status': True,
                            'object_data': {
                                '$elemMatch': {
                                    'violation': True,
                                    'roi_details.analytics_type': '0'
                                }
                            }
                        }},
                        {'$group': {'_id': '$camera_rtsp', 'count': {'$sum': 1}}}
                    ]
                }}
            ]

            violations = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
            if not violations:
                result['message'] = 'No violations found'
                result['success'] = False
                # return jsonify(result)
                return JsonResponse(result)

            all_violations = []

            camera_details = {cam['rtsp_url']: cam for cam in find_data_cam_status}

            for violation_type in ['ppe_type_counts', 'ppe_crash_helemt_counts', 'cr_type_counts', 'protection_zone_counts', 'roi_type_counts']:
                for violation in violations[0][violation_type]:
                    cam_rtsp = violation['_id']
                    if cam_rtsp in camera_details:
                        cam_detail = camera_details[cam_rtsp]
                        if not any(cam_rtsp == v['rtsp_url'] for v in all_violations):
                            all_violations.append({
                                'camera_name': cam_detail['cameraname'],
                                'camera_ip': cam_detail['camera_ip'],
                                'rtsp_url': cam_rtsp,
                                'imagename': cam_detail['imagename'],
                                'ppe_type_counts': 0,
                                'ppe_crash_helemt_counts': 0,
                                'cr_type_counts': 0,
                                'protection_zone_counts': 0,
                                'roi_type_counts': 0
                            })

                        for violation_data in all_violations:
                            if violation_data['rtsp_url'] == cam_rtsp:
                                violation_data[violation_type] = violation['count']
                                break

            if all_violations:
                result = {'message': all_violations, 'success': True}
            else:
                result = {'message': 'No violations found', 'success': False}
        except Exception as e:
            result['message'] = f'Error occurred: {str(e)}'

    return JsonResponse(result)

"""DATE WISE ALL VIOLATION COUNTS"""
# @camera_status.route('/cam_wise_violations_count_by_date', methods=['POST'])
@csrf_exempt
def cam_wise_violations_count_by_date(request):
    result = {'message': 'something went wrong ','success':False}
    if request.method == "POST":
        if 1:
        # try:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        result['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        from_date = data['from_date']
                        to_date = data['to_date']
                        all_violations=[]
                        camera_status_true_data = list(ppera_cameras.find({'camera_status': True}))
                        for find_data in camera_status_true_data:
                            rtsp_url = find_data['rtsp_url']
                            """Calling function to get the working camera list and not woorking camera list"""
                            query_base = {
                                #'timestamp': {'$regex': '^' + str(date.today())},
                                'timestamp': {'$gte': from_date,'$lt': to_date},
                                'camera_rtsp': rtsp_url  # Replace this with actual rtsp_url from find_data
                            }
                            print("FOR LOOP0---------------------------------------------------------")
                            # Aggregation pipeline
                            pipeline = [
                                {'$match': query_base},
                                {
                                    '$facet': {
                                        'ppe_type_counts': [
                                            {'$match': {
                                                'analyticstype': 'PPE_TYPE1',
                                                '$or': [
                                                    {"object_data.Helmet": False},
                                                    {"object_data.Vest": "no_ppe"}
                                                ]
                                            }},
                                            {'$count': 'count'}
                                        ],
                                        'ppe_crash_helemt_counts': [
                                            {'$match': {'analyticstype': 'PPE_TYPE2'}},
                                            {'$count': 'count'}
                                        ],
                                        'cr_type_counts': [
                                            {'$match': {'analyticstype': 'CRDCNT'}},
                                            {'$count': 'count'}
                                        ],
                                        'protection_zone_counts': [
                                            {'$match': {
                                                'analyticstype': 'RA',
                                                'violation_status': True,
                                                'object_data': {
                                                    '$elemMatch': {
                                                        'violation': True,
                                                        'roi_details': {
                                                            '$exists': True,
                                                            '$elemMatch': {
                                                                'violation': True,
                                                                'analytics_type': '2'
                                                            }
                                                        }
                                                    }
                                                }
                                            }},
                                            {'$count': 'count'}
                                        ],
                                        'roi_type_counts': [
                                            {'$match': {
                                                'analyticstype': 'RA',
                                                'violation_status': True,
                                                'object_data': {
                                                    '$elemMatch': {
                                                        'violation': True,
                                                        'roi_details.analytics_type': '0'
                                                    }
                                                }
                                            }},
                                            {'$count': 'count'}
                                        ]
                                    }
                                }
                            ]
                          

                            print("FOR LOOP0-----------------PIPELINE111111111111----------------------------------------")
                            # Aggregation firesmoke_pipeline
                            # firesmoke_pipeline= [
                            #     {'$match': query_base},
                            #     {
                            #         '$facet': {
                                        
                            #             'fire_type_counts':[{
                            #                 'timestamp': {'$regex': '^' + str(date.today())},
                            #                 'analytics_details.details.obj_details.class_name':'fire',
                            #                 'analytics_details.details.obj_details.violation':True}, 
                            #                 {'$count': 'count'}
                            #                 ],

                            #             'dust_type_counts':[{
                            #                 'timestamp': {'$regex': '^' + str(date.today())},
                            #                 'analytics_details.details.obj_details.class_name':'dust',
                            #                 'analytics_details.details.obj_details.violation':True}, 
                            #                 {'$count': 'count'}
                            #                 ],
                                            
                            #             'smoke_type_counts':[{
                            #                 'timestamp': {'$regex': '^' + str(date.today())},
                            #                 'analytics_details.details.obj_details.class_name':'smoke',
                            #                 'analytics_details.details.obj_details.violation':True}, 
                            #                 {'$count': 'count'}
                            #                 ]
                            #         }
                            #     }
                            # ]
                            firesmoke_pipeline = [
                                {'$match': query_base},
                                {
                                    '$facet': {
                                        'fire_type_counts': [
                                            {'$match': {
                                                'timestamp': {'$regex': '^' + str(date.today())},
                                                'analytics_details.details.obj_details.class_name': 'fire',
                                                'analytics_details.details.obj_details.violation': True
                                            }},
                                            {'$count': 'count'}
                                        ],
                                        'dust_type_counts': [
                                            {'$match': {
                                                'timestamp': {'$regex': '^' + str(date.today())},
                                                'analytics_details.details.obj_details.class_name': 'dust',
                                                'analytics_details.details.obj_details.violation': True
                                            }},
                                            {'$count': 'count'}
                                        ],
                                        'smoke_type_counts': [
                                            {'$match': {
                                                'timestamp': {'$regex': '^' + str(date.today())},
                                                'analytics_details.details.obj_details.class_name': 'smoke',
                                                'analytics_details.details.obj_details.violation': True
                                            }},
                                            {'$count': 'count'}
                                        ]
                                    }
                                }
                            ]


                            # Running the aggregation
                            result = list(PPERAVIOLATIONCOLLECTION.aggregate(pipeline))
                            print("FOR LOOP0-----------------PIPELINE2222222222222----------------------------------------")
                            firesmoke_result = list(firesmokeviolationdata.aggregate(firesmoke_pipeline))
                            print("FOR LOOP0-----------------PIPELINE2222222222222-------------------11111111111---------------------")

                            # Initialize an empty required_data dictionary
                            required_data = {}
                            print("firesmoke_result[0]---------", firesmoke_result)
                            # Check if any of the counts is greater than zero and build the required_data dictionary
                            if (result[0]['ppe_type_counts'] and result[0]['ppe_type_counts'][0]['count'] > 0) or \
                            (result[0]['ppe_crash_helemt_counts'] and result[0]['ppe_crash_helemt_counts'][0]['count'] > 0) or \
                            (result[0]['cr_type_counts'] and result[0]['cr_type_counts'][0]['count'] > 0) or \
                            (result[0]['protection_zone_counts'] and result[0]['protection_zone_counts'][0]['count'] > 0) or \
                            (result[0]['roi_type_counts'] and result[0]['roi_type_counts'][0]['count'] > 0) or \
                            (firesmoke_result[0]['fire_type_counts'] and firesmoke_result[0]['fire_type_counts'][0]['count'] > 0) or \
                            (firesmoke_result[0]['dust_type_counts'] and firesmoke_result[0]['dust_type_counts'][0]['count'] > 0) or \
                            (firesmoke_result[0]['smoke_type_counts'] and firesmoke_result[0]['smoke_type_counts'][0]['count'] > 0):
                                print("FOR LOOP0-----------------IF COND----------------------------------------")

                                # Add camera details since at least one count is greater than zero
                                required_data = {
                                    'camera_name': find_data['cameraname'],
                                    'camera_ip': find_data['camera_ip'],
                                    'rtsp_url': rtsp_url,
                                    'imagename': find_data['imagename'],
                                    'ppe_type_counts':0,
                                    'ppe_crash_helemt_counts':0,
                                    'cr_type_counts':0,
                                    'protection_zone_counts':0,
                                    'roi_type_counts':0,
                                    'fire_type_counts':0,
                                    'smoke_type_counts':0,
                                    'dust_type_counts':0,
                                    
                                }
                                print("FOR LOOP0-----------------IF COND---------111111111111-------------------------------")

                                # Add only non-zero counts
                                if result[0]['ppe_type_counts'] and result[0]['ppe_type_counts'][0]['count'] > 0:
                                    required_data['ppe_type_counts'] = result[0]['ppe_type_counts'][0]['count']

                                if result[0]['ppe_crash_helemt_counts'] and result[0]['ppe_crash_helemt_counts'][0]['count'] > 0:
                                    required_data['ppe_crash_helemt_counts'] = result[0]['ppe_crash_helemt_counts'][0]['count']

                                if result[0]['cr_type_counts'] and result[0]['cr_type_counts'][0]['count'] > 0:
                                    required_data['cr_type_counts'] = result[0]['cr_type_counts'][0]['count']

                                if result[0]['protection_zone_counts'] and result[0]['protection_zone_counts'][0]['count'] > 0:
                                    required_data['protection_zone_counts'] = result[0]['protection_zone_counts'][0]['count']

                                if result[0]['roi_type_counts'] and result[0]['roi_type_counts'][0]['count'] > 0:
                                    required_data['roi_type_counts'] = result[0]['roi_type_counts'][0]['count']

                                if firesmoke_result[0]['fire_type_counts'] and firesmoke_result[0]['fire_type_counts'][0]['count'] > 0:
                                    print("-----------------111111")
                                    required_data['fire_type_counts'] = firesmoke_result[0]['fire_type_counts'][0]['count']

                                if firesmoke_result[0]['smoke_type_counts'] and firesmoke_result[0]['smoke_type_counts'][0]['count'] > 0:
                                    print("-----------------2222")
                                    required_data['smoke_type_count'] = firesmoke_result[0]['smoke_type_counts'][0]['count']

                                if firesmoke_result[0]['dust_type_counts'] and firesmoke_result[0]['dust_type_counts'][0]['count'] > 0:
                                    print("-----------------3333")
                                    required_data['dust_type_counts'] = firesmoke_result[0]['dust_type_counts'][0]['count']

                            if required_data != {}:
                                print("FOR LOOP0-----------------IF COND--IF COndition--------------------------------------")
                                all_violations.append(required_data)

                        if len(all_violations) !=0:
                            result = {'message': all_violations, 'success': True}
                        else:
                            result= {'message': 'No violations detected for the selected date range' , 'success': False} # 'there is no solution found.'
                else:
                    result = {'message':" ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
            else:
                result = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
  
    return JsonResponse(result)

"""DATE WISE PPE VIOLATION COUNTS"""
# @camera_status.route('/cam_wise_PPE_violations_by_date', methods=['POST'])
@csrf_exempt
def date_wise_ppe_violations_details(request):
    ret = {'message': 'something went wrong in date_wise_PPE_violations_details API.','success': False}
    if request.method== "POST":
        if 1:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        ret['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        print("#########################################################################-----222222222222")
                        from_date = data['from_date']
                        to_date = data['to_date']
            
                        find_data_cam_status = list(ppera_cameras.find({'camera_status': True,'ppe_data':{'$exists':True,"$ne": []}}))
                        # print(find_data_cam_status)
                        if len(find_data_cam_status) !=0 :
                            ppe_require_data = []
                            for let, ppe_da in enumerate(find_data_cam_status):
                                ppe_values = ppe_da['ppe_data'] #[0]
                                if type(ppe_da['ppe_data'][0]) == dict and (ppe_values[0]['helmet'] == True or ppe_values[0]['vest'] == True):
                                    match_data = {'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': ppe_da['rtsp_url'], 'analyticstype': 'PPE_TYPE1'}
                                    # ppe_data = list(mongo.db.data.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}]))                   
                                    PPEViolationCount = PPERAVIOLATIONCOLLECTION.count_documents(match_data)
                                    if PPEViolationCount != 0:
                                        # ppe_count = fun_ppe_violations_count(ppe_data)
                                        # if ppe_count["ppe_counts"] != 0:
                                        ppe_require_data.append({'camera_name':ppe_da['cameraname'], 'camera_ip': ppe_da[ 'camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'ppe_type_counts': PPEViolationCount}) # ppe_count["ppe_counts"], 'helmet_count':ppe_count["helmet_cnts"], 'vest_count':ppe_count["vest_cnts"]}) #ppe_count}) #len(ppe_data)})
                                    # else:
                                    #     ppe_require_data.append({'camera_name': ppe_da['cameraname'], 'camera_ip': ppe_da['camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'ppe_type_counts':len(ppe_data), 'helmet_count':0, 'vest_count':0})

                            if len(ppe_require_data) != 0:
                                ret = {'message': ppe_require_data, 'success': True}
                            else:
                                ret['message'] = 'No PPE violations detected for the selected date range' #'ppe data not found.'
                        else:
                            ret['message']= "No cameras have been added for PPE analytics. Please add a camera" #'there no camera enabled for ppe,please add camera and enable for ppe'

                else:
                    ret = {'message':" ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
            else:
                ret = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)


"""DATE WISE RA VIOLATION COUNTS"""
# @camera_status.route('/cam_wise_RA_violations_by_date', methods=['POST']) 
@csrf_exempt
def date_wise_RA_violations_counts(request):
    ret = {'message': 'something went wrong in date_wise_RA_violations_details API.', 'success': False}
    if request.method == "POST":
        # try:
        data = json.loads(request.body)
        print('------cam_wise_RA_violations_by_date------------------data----------',data)
        request_key_array = ['from_date', 'to_date']

        if data:
            missing_keys = set(request_key_array) - data.keys()
            if missing_keys:
                ret['message'] = f"You have missed these keys: {', '.join(missing_keys)}. Please enter them properly."
                return JsonResponse(ret)
            
            output = [key for key in request_key_array if not data[key]]
            if output:
                ret['message'] = f"You have missed these parameters: {', '.join(output)}. Please enter them properly."
                return JsonResponse(ret)

            # from_date = datetime.strptime(data['from_date'], "%Y-%m-%d")
            # to_date = datetime.strptime(data['to_date'], "%Y-%m-%d")

            find_data_cam_status = list(ppera_cameras.find({
                'camera_status': True,
                'roi_data': {'$exists': True, "$ne": []}
            }))

            if find_data_cam_status:
                roi_require_data_details = []

                for find_data in find_data_cam_status:
                    roi_data = find_data['roi_data']
                    if roi_data:
                        match_data = {
                            'timestamp': {'$gte': data['from_date'], '$lt': data['to_date']},
                            'camera_rtsp': find_data['rtsp_url'],
                            'analyticstype': 'RA',
                            'violation_status': True,
                            'object_data': {
                                '$elemMatch': {
                                    'violation': True,
                                    'roi_details.analytics_type': '0'
                                }
                            }
                        }

                        violation_data =PPERAVIOLATIONCOLLECTION.count_documents(match_data)

                        if violation_data > 0:
                            roi_require_data = {
                                'camera_name': find_data['cameraname'],
                                'camera_ip': find_data['camera_ip'],
                                'rtsp_url': find_data['rtsp_url'],
                                'imagename': find_data['imagename'],
                                'roi_type_counts': violation_data
                            }
                            roi_require_data_details.append(roi_require_data)
                
                print("roi_require_data_details000000000000000", roi_require_data_details)
                if roi_require_data_details:
                    print("roi_require_data_detailsroi_require_data_details", roi_require_data_details)
                    ret = {'message': roi_require_data_details, 'success': True} 

                else:
                    ret['message'] = 'No RA violations detected for the selected date range' #'There is no data found for RA camera.'
            else:
                ret['message'] = "No cameras have been added for RA analytics. Please add a camera." #'There are no cameras added for RA analytics. Please add the camera.'
        else:
            ret['message'] = "You have missed these keys: from_date, to_date. Please enter them properly."
        # except Exception as e:
        #     ret['message'] = str(e)

    
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)

"""DATE WISE CR VIOLATION COUNTS"""
# @camera_status.route('/cam_wise_CR_violations_by_date', methods=['POST'])
@csrf_exempt
def date_wise_CR_violations_cam_details(request):
    ret = {'message': 'something went wrong in date_wise_CR_violations_details API.','success': False}
    if request.method == "POST":
        if 1:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        ret['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        print("#########################################################################-----222222222222")
                        from_date = data['from_date']
                        to_date = data['to_date']
                        find_data_cam_status = list(ppera_cameras.find({'camera_status': True,'cr_data':{'$exists':True,"$ne": []}}))
                        if len(find_data_cam_status) !=0:
                            cr_require_data_details = []
                            for find_data in find_data_cam_status:
                                match_data = {'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': find_data['rtsp_url'], 'analyticstype': 'CRDCNT'}
                                FoundCrData = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, { '$sort': {'timestamp': -1}}]))
                                if len(FoundCrData) != 0:
                                    cr_require_data = {'camera_name': find_data['cameraname'],'camera_ip': find_data['camera_ip'], 'rtsp_url': find_data['rtsp_url'], 'imagename': find_data['imagename'],'cr_type_counts': len(FoundCrData)}
                                    if (cr_require_data not in cr_require_data_details):
                                        cr_require_data_details.append(cr_require_data)
                            if len(cr_require_data_details) !=0:
                                ret = {'message': cr_require_data_details, 'success': True}
                            else:
                                ret['message']= "No CR violations detected for the selected date range." #'there is no violation found.'
                        else:
                            ret['message']= "No cameras have been added for CR analytics. Please add a camera." #'there is no camera added.'        
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- CR_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()]))   
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- CR_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(ret)

"""DATE WISE CRASH HELMET PPE VIOLATION COUNTS"""
# @camera_status.route('/cam_wise_PPE_crash_helmet_violations_by_date', methods=['POST'])
@csrf_exempt
def date_wise_ppe_crash_helmet_violations_details(request):
    ret = {'message': 'something went wrong in date_wise_PPE_violations_details API.','success': False}
    if request.method == "POST":
        if 1:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        ret['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        from_date = data['from_date']
                        to_date = data['to_date']
            
                        find_data_cam_status = list(ppera_cameras.find({'camera_status': True,'ppe_data':{'$exists':True,"$ne": []}}))
                        if len(find_data_cam_status) !=0 :
                            ppe_require_data = []
                            for let, ppe_da in enumerate(find_data_cam_status):
                                ppe_values = ppe_da['ppe_data'] #[0]
                                if type(ppe_da['ppe_data'][0]) == dict and (ppe_values[0]['helmet'] == True or ppe_values[0]['vest'] == True):
                                    match_data = {'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': ppe_da['rtsp_url'], 'analyticstype': 'PPE_TYPE2'}
                                    ppe_data = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$sort': {'timestamp': -1}}])) 
                                    if len(ppe_data) != 0:
                                        # crash_helmet_counts = fun_ppe_crash_helmet_violations_count(ppe_data)
                                        ppe_require_data.append({'camera_name':ppe_da['cameraname'], 'camera_ip': ppe_da[ 'camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'crash_helmet_count': len(ppe_data)}) # crash_helmet_counts["crash_helmet_cnts"]}) #ppe_count}) #len(ppe_data)})
                                    # else:
                                    #     ppe_require_data.append({'camera_name': ppe_da['cameraname'], 'camera_ip': ppe_da['camera_ip'], 'rtsp_url': ppe_da['rtsp_url'], 'imagename': ppe_da['imagename'], 'crash_helmet_count':0})

                            if len(ppe_require_data) != 0:
                                ret = {'message': ppe_require_data, 'success': True}
                            else:
                                ret['message'] = "No CRASH-HELMET violations detected for the selected date range." #'ppe data not found.'
                        else:
                            ret['message']= "No cameras have been added for CRASH-HELMET analytics. Please add a camera." #'there no camera enabled for ppe,please add camera and enable for ppe'

                else:
                    ret = {'message':" ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
            else:
                ret = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
    return JsonResponse(ret)

"""DATE WISE Truck REVERSAL VIOLATION COUNTS"""
# @camera_status.route('/cam_wise_truck_reversal_RA_violations_by_date', methods=['POST'])
@csrf_exempt
def cam_wise_truck_reversal_RA_violations_by_date(request):
    ret = {'message': 'something went wrong in date_wise_RA_violations_details API.','success': False}
    if request.method == "POST":
        if 1:
            data = json.loads(request.body)
            request_key_array = ['from_date', 'to_date']
            if data != None:
                jsonobjectarray = list(set(data))
                missing_key = set(request_key_array).difference(jsonobjectarray)
                if not missing_key:
                    output = [k for k, v in data.items() if v == '']
                    if output:
                        ret['message'] =" ".join(["You have missed these parameters", str(output), ' to enter. please enter properly.']) 
                    else:
                        from_date = data['from_date']
                        to_date = data['to_date']
            
                        find_data_cam_status = list(ppera_cameras.find({'camera_status': True, 'roi_data':{'$exists':True,"$ne": []}}))
                        if len(find_data_cam_status) !=0:
                            roi_require_data_details = []
                            for find_data in find_data_cam_status:
                                """Calling function to get the working camera list and not woorking camera list"""
                                # match_data = {'timestamp': {'$gte': from_date,'$lt': to_date}, 'camera_rtsp': find_data['rtsp_url']}
                                roi_data = find_data['roi_data']
                                if len(roi_data) != 0:
                                    # match_data['analyticstype']='RA'
                                    match_data = {'timestamp':{'$gte': from_date,'$lt': to_date},'camera_rtsp': find_data['rtsp_url'],
                                'analyticstype': 'RA',
                                'violation_status': True,
                                'object_data': {
                                                    '$elemMatch': {
                                                        'violation': True,
                                                        'roi_details': {
                                                            '$exists': True,
                                                            '$elemMatch': {
                                                                'violation': True,
                                                                'analytics_type': '2'
                                                            }
                                                        }
                                                    }
                                                }
                                }
                                    ViolationFOUNDDATAfinddata = list(PPERAVIOLATIONCOLLECTION.aggregate([{'$match': match_data}, {'$sort': {'_id': -1}}]))
                                    roi_require_data = {'camera_name': find_data['cameraname'], 'camera_ip': find_data['camera_ip'], 'rtsp_url': find_data['rtsp_url'], 'imagename':find_data['imagename'],'protection_zone_type_counts': len(ViolationFOUNDDATAfinddata)}
                                    if (roi_require_data not in roi_require_data_details):
                                        roi_require_data_details.append(roi_require_data)
                            if len(roi_require_data_details) !=0:
                                ret = {'message': roi_require_data_details, 'success': True} 
                            else:
                                ret['message']= "No PROTECTED-ZONE violations detected for the selected date range." #'there is no data found for RA camera .'
                        else:
                            ret['message']= "No cameras have been added for PROTECTED-ZONE analytics. Please add a camera." #'there are no cameras are added for analytics please add the camera.'

                else:
                    ret = {'message':" ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
            else:
                ret = {'message': " ".join(["You have missed these keys", str(missing_key), ' to enter. please enter properly.']),'success': False}
        # except ( 
        #     pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
        #     pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
        #     pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
        #     pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
        #     pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
        #     pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
        #     pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
        #     pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
        #     pymongo.errors.WriteError) as error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 1", str(error), " ----time ---- ", now_time_with_time()])) 
        #     ret['message' ] = " ".join(["something error has occured in  apis", str(error), " ----time ---- ", now_time_with_time()]) 
        #     if restart_mongodb_r_service():
        #         print("mongodb restarted")
        #     else:
        #         if forcerestart_mongodb_r_service():
        #             print("mongodb service force restarted-")
        #         else:
        #             print("mongodb service is not yet started.")
        # except Exception as error:
        #     ret['message']=" ".join(["something error has occured in  apis", str(error)]) 
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_status_api -- ppe_violations_count_cam_wise 2", str(error), " ----time ---- ", now_time_with_time()]))          
    return JsonResponse(ret)