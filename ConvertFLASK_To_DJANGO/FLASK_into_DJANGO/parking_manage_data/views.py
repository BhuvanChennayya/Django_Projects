from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.final_ping import *



# Create your views here.


date = datetime.today().strftime('%Y%m%d')

def get_five_hours_list():
    # Get the current time
    current_time = datetime.now()

    # Calculate the time 5 hours ago
    five_hours_ago = current_time - timedelta(hours=5)

    # Generate the list of times for the latest 5 hours
    times_in_last_five_hours = [five_hours_ago + timedelta(hours=i) for i in range(6)]

    # Print the times
    five_hours_list = []
    for time in times_in_last_five_hours:
        # print(time.strftime("%m/%d/%Y, %H:%M:%S"))
        # five_hours_list.append(time.strftime("%d-%m-%Y %H:%M:%S")) #"%m-%d-%Y, %H:%M:%S"))
        five_hours_list.append(time.strftime("%Y-%m-%d %H:%M:%S")) 

    # print("LATEST FIVE HOURS LIST", five_hours_list)
    return five_hours_list


def VPMSimage_roi_draw_data(image_data,image_file):
    # print("image_data:------------", image_data) #["analytics_log"])
    IsvoilationTrue = False
    test_dict = {}
    if len(image_data) != 0:
        for images_details in image_data:
            # print("------------images_details--------------------",images_details[''])
            for obj_details in images_details["details"]:
                if 'image_name' in obj_details :
                    if obj_details['image_name']==image_file:
                        # print("-------------obj_details------------",obj_details)
                        # print("OBJECT_DETILS:------", obj_details["obj_details"])
                        if 'violation' in obj_details :
                            if obj_details['violation'] == 1:
                                IsvoilationTrue = True
                        object_data = obj_details["obj_details"] #image_data['object_data']
                        if len(object_data) != 0:
                            final_object_data = []
                            person_count = 0
                            motorcycle_count = 0
                            bicycle_count = 0
                            car_count = 0
                            bus_count =0 
                            truck_count = 0
                            for ___, jjj in enumerate(object_data):
                                if jjj['name'] == 'person':
                                    final_object_data.append(jjj)
                                    person_count += 1
                                
                                elif jjj['name'] == 'car':
                                    final_object_data.append(jjj)
                                    car_count += 1

                                elif jjj['name'] == 'motorcycle' or  jjj['name']=='motorbike':
                                    final_object_data.append(jjj)
                                    motorcycle_count += 1

                                elif jjj['name'] == 'bicycle':
                                    final_object_data.append(jjj)
                                    bicycle_count += 1

                                elif jjj['name'] == 'bus':
                                    final_object_data.append(jjj)
                                    bus_count += 1

                                elif jjj['name'] == 'truck':
                                    final_object_data.append(jjj)
                                    truck_count += 1

                            if len(final_object_data) != 0:
                                # print("FINAL OBJECT_DATA:------------------------------------", final_object_data)
                                test_dict['obj_details'] = final_object_data 
                            else:
                                test_dict = final_object_data

                            break
    return test_dict,IsvoilationTrue



# @parking_manage_data.route('/get_latest_five_hours_data', methods=['POST'])
@csrf_exempt
def get_latest_five_hours_data(request):
    ret = {"message":"Something went wrong with 'get_latest_five_hours_data'", "success":False}
    if request.method == 'POST':
        print("Hiii---------------")
        five_hours_list = get_five_hours_list()
        jsonobject = json.loads(request.body)
        print(jsonobject)
        # print("JSONOBJECT:-------------------------", jsonobject)
        request_key_array = ['camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        # print(missing_key)

        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            print(output)

            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            
            else:
                # five_hours_list_data = []
                five_hours_list_PA_data = []
                five_hours_list_NPA_data = []
                start_index = 0
                end_index = 5
                
                # for idx, time_value in enumerate(five_hours_list):
                for idx, time_value in enumerate(five_hours_list[start_index:end_index], start=start_index):
                    violation_counts = 0
                    parked_status_slots_count = 0
                    PA_violation_counts = 0
                    PA_parked_status_slots_count = 0
                    NPA_violation_counts = 0
                    NPA_parked_status_slots_count = 0
                    PA_Free_status_slots_count= 0
                    PA_Error_status_slots_count = 0 
                    # print("ITEM VALUE INDEX:-----------------------", idx, time_value)

                    EAchhourwisequery = {"timestamp":{'$gte':five_hours_list[idx], '$lte': five_hours_list[idx+1]}, "camera_name":jsonobject["camera_name"]}
                    # print ("---------------------EAchhourwisequery----------------",EAchhourwisequery)
                    # VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"timestamp":{'$gte':five_hours_list[idx], '$lte': five_hours_list[idx+1]}}, {"_id":0, "dashboard_log":0}).sort('timestamp', -1))
                    VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"timestamp":{'$gte':five_hours_list[idx], '$lte': five_hours_list[idx+1]}, "camera_name":jsonobject["camera_name"]}, {"_id":0, "dashboard_log":0}).sort('timestamp', -1))
                    # print("VPMS DATA:----dataaaaaaaaaaaa---------------",VPMS_data) # idx, five_hours_list[idx], five_hours_list[idx+1], len(VPMS_data))
                    
                    
                    if len(VPMS_data) !=0 :
                        for analytics_data in VPMS_data:
                            for deatails_data in analytics_data["analytics_log"]:
                                if deatails_data["type"] == "PA":
                                    if deatails_data["status"] == "parked":
                                        PA_parked_status_slots_count +=1
                                    elif  deatails_data["status"] == "free":
                                        PA_Free_status_slots_count +=1
                                    elif  deatails_data["status"] == "Error":
                                        PA_Free_status_slots_count +=1
                                    if len(deatails_data["details"]) !=0:
                                        for violation_data in deatails_data["details"]:
                                            if violation_data["violation"] == 1:
                                                # print("violation_counts DATA:----------------------", PA_violation_counts)
                                                PA_violation_counts += 1
                                            
                                        #     else:
                                        #         # print("parked_status_slots_count DATA:----------------------", PA_parked_status_slots_count)
                                        #         PA_parked_status_slots_count += 1
                                else:
                                    for violation_data in deatails_data["details"]:
                                        if violation_data["violation"] == 1:
                                            # print("NO PARKING violation_counts DATA:----------------------", NPA_violation_counts)
                                            NPA_violation_counts += 1
                                        
                                        else:
                                            # print("NO PARKING parked_status_slots_count DATA:----------------------", NPA_parked_status_slots_count)
                                            NPA_parked_status_slots_count += 1

                        # five_hours_list_data.append({"timestamp": five_hours_list[idx], "violation_count":violation_counts, "parked_status_count":parked_status_slots_count, "camera_name":jsonobject["camera_name"]})
                        five_hours_list_NPA_data.append({"timestamp": five_hours_list[idx], "violation_count":NPA_violation_counts, "parked_status_count":NPA_parked_status_slots_count})
                        five_hours_list_PA_data.append({"timestamp": five_hours_list[idx], "violation_count":PA_violation_counts, "parked_status_count":PA_parked_status_slots_count})

                    else:
                        five_hours_list_NPA_data.append({"timestamp": five_hours_list[idx], "violation_count":0, "parked_status_count":0})
                        five_hours_list_PA_data.append({"timestamp": five_hours_list[idx], "violation_count":0, "parked_status_count":0})
            
                ret = {"PA_message":five_hours_list_PA_data, "NPA_message":five_hours_list_NPA_data,"success":True}
    return JsonResponse(ret)

# @parking_manage_data.route('/get_latest_five_hours_PA_NPA_data', methods=['GET'])
@csrf_exempt
def get_latest_five_hours_PA_NPA_data(request):
    result = {"message":"Something went wrong with 'get_latest_five_hours_data'", "success":False}
    if request.method == 'GET':
        five_hours_list = get_five_hours_list()
        five_hours_list_PA_data = []
        five_hours_list_NPA_data = []
        start_index = 0
        end_index = 5
        
        TotalnumberOFSOLTS= []
        for idx, time_value in enumerate(five_hours_list[start_index:end_index], start=start_index):
            
            
            # print("--------------five_hours_list[idx]------",five_hours_list[idx])
            # print("--------------five_hours_list[idx+1]------",five_hours_list[idx+1])


            Mongodbquery = {'date':date,"timestamp":{'$gte':five_hours_list[idx], '$lte': five_hours_list[idx+1]}}
            # print('-------------------------------Mongodbquery----------------',Mongodbquery)
            VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({'date':date,"timestamp":{'$gte':five_hours_list[idx], '$lte': five_hours_list[idx+1]}}, {"_id":0, "dashboard_log":0}).sort('timestamp', -1))

            # print("VPMS DATA:----dataaaaaaaaaaaa---------------", VPMS_data) # idx, five_hours_list[idx], five_hours_list[idx+1], len(VPMS_data))
            TotalSlotsOFLastFiveHours = VEHICLE_PARKING_MANAGEMENT_DATA.aggregate([
                {"$match": {'date':date,"timestamp": {"$gte": five_hours_list[idx], "$lte": five_hours_list[idx+1]}}},
                {"$group": {"_id": "$roi_name", "count": {"$sum": 1}}}])
            for i , j in enumerate(TotalSlotsOFLastFiveHours):
                if j is not None  and j['_id']  not in TotalnumberOFSOLTS:
                    TotalnumberOFSOLTS.append(j['_id'])
            if len(VPMS_data) !=0 :
                pipeline = [
                            {"$match": {"timestamp": {"$gte": five_hours_list[idx], "$lte": five_hours_list[idx+1]}}},
                            {"$facet": {
                                "PA": [
                                    {"$match": {"analytics_log.type": "PA"}},
                                    {"$unwind": "$analytics_log"},
                                    {"$unwind": "$analytics_log.details"},
                                    {"$match": {"analytics_log.details.violation": 1}},
                                    {"$group": {
                                        "_id": {"roi_name": "$roi_name"},
                                        "total_count": {"$sum": 1},
                                        "free_count": {"$sum": {"$cond": [{"$eq": ["$analytics_log.status", "free"]}, 1, 0]}},
                                        "parked_count": {"$sum": {"$cond": [{"$eq": ["$analytics_log.status", "parked"]}, 1, 0]}},
                                        "error_count": {"$sum": {"$cond": [{"$eq": ["$analytics_log.status", "Error"]}, 1, 0]}},
                                        "total_violations": {"$sum": 1}
                                    }}
                                ],
                                "NPA": [
                                    {"$match": {"analytics_log.type": "NPA"}},
                                    {"$unwind": "$analytics_log"},
                                    {"$unwind": "$analytics_log.details"},
                                    {"$match": {"analytics_log.details.violation": 1}},
                                    {"$group": {
                                        "_id": {"roi_name": "$roi_name"},
                                        "total_count": {"$sum": 1},
                                        "free_count": {"$sum": {"$cond": [{"$eq": ["$analytics_log.status", "free"]}, 1, 0]}},
                                        "unauthorized_count": {"$sum": {"$cond": [{"$eq": ["$analytics_log.status", "Unauthorized Parking"]}, 1, 0]}},
                                        "error_count": {"$sum": {"$cond": [{"$eq": ["$analytics_log.status", "Error"]}, 1, 0]}},
                                        "total_violations": {"$sum": 1}
                                    }}
                                ]
                            }}
                        ]    
                
                # pipeline = [
                #     {"$match": {"timestamp": {"$gte": five_hours_list[idx], "$lte": five_hours_list[idx+1]}}},
                #     # Use $facet to run multiple pipelines
                #     {"$facet": {
                #         # PA Pipeline
                #         "PA": [
                #             {"$match": {"analytics_log.type": "PA"}},
                #             {"$unwind": "$analytics_log"},
                #             # Additional unwind and match for details.violation
                #             {"$unwind": "$analytics_log.details"},
                #             {"$match": {"analytics_log.details.violation": 1}},
                #             {"$group": {
                #                 "_id": {"roi_name": "$roi_name"},
                #                 "total_count": {"$sum": 1},
                #                 "free_count": {
                #                     "$sum": {"$cond": [{"$eq": ["$analytics_log.status", "free"]}, 1, 0]}
                #                 },
                #                 "parked_count": {
                #                     "$sum": {"$cond": [{"$eq": ["$analytics_log.status", "parked"]}, 1, 0]}
                #                 },
                #                 "error_count": {
                #                     "$sum": {"$cond": [{"$eq": ["$analytics_log.status", "Error"]}, 1, 0]}
                #                 },
                #                 "total_violations": {"$sum": 1} 
                #             }}
                #         ],
                        
                #         # NPA Pipeline
                #         "NPA": [
                #             {"$match": {"analytics_log.type": "NPA"}},
                #             {"$unwind": "$analytics_log"},
                #             # Additional unwind and match for details.violation
                #             {"$unwind": "$analytics_log.details"},
                #             {"$match": {"analytics_log.details.violation": 1}},
                #             {"$group": {
                #                 "_id": {"roi_name": "$roi_name"},
                #                 "total_count": {"$sum": 1},
                #                 "free_count": {
                #                     "$sum": {"$cond": [{"$eq": ["$analytics_log.status", "free"]}, 1, 0]}
                #                 },
                #                 "unauthorized_count": {
                #                     "$sum": {"$cond": [{"$eq": ["$analytics_log.status", "Unauthorized Parking"]}, 1, 0]}
                #                 },
                #                 "error_count": {
                #                     "$sum": {"$cond": [{"$eq": ["$analytics_log.status", "Error"]}, 1, 0]}
                #                 },
                #                 "total_violations": {"$sum": 1}  # Count each occurrence as a violation
                #             }}
                #         ]
                #     }}
                # ]
                TotalNPAViolationAcount = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline))
                if len(TotalNPAViolationAcount) !=0 :
                    NPA_violation_counts = 0
                    NPA_parked_status_slots_count = 0
                    PA_violation_counts = 0
                    PA_parked_status_slots_count = 0
                    query = {'date':date,
                        "timestamp": {
                            "$gte": five_hours_list[idx],
                            "$lte": five_hours_list[idx+1]
                        },
                        "analytics_log.type": { "$in": ["PA"] } ,
                        "analytics_log.status":'parked' # Optional additional filtering
                    }

                    # Count documents matching the query
                    parkedcount = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query)
                    

                    for Newindex , AnalyticsType in enumerate(TotalNPAViolationAcount):
                        if len(AnalyticsType['PA']) !=0 :
                            # print("---------------------------********************&&&&&&&&&&&&&&&&&&&&&&&&&&7%**********",AnalyticsType)
                            for Index , ValuePa in enumerate(AnalyticsType['PA']):
                                # print("--------ValuePa------------",ValuePa)
                                if parkedcount is not None:
                                    PA_parked_status_slots_count += parkedcount
                                else:
                                    PA_parked_status_slots_count += ValuePa['parked_count']
                                PA_violation_counts += ValuePa['total_violations']
                        if  len(AnalyticsType['NPA']) !=0 :
                            for Index , ValueNPa in enumerate(AnalyticsType['NPA']):
                                NPA_violation_counts +=ValueNPa['total_violations']
                    five_hours_list_NPA_data.append({"timestamp": five_hours_list[idx], "violation_count":NPA_violation_counts, "parked_status_count":NPA_parked_status_slots_count})
                    five_hours_list_PA_data.append({"timestamp": five_hours_list[idx], "violation_count":PA_violation_counts, "parked_status_count":PA_parked_status_slots_count})
                else:
                    five_hours_list_NPA_data.append({"timestamp": five_hours_list[idx], "violation_count":0, "parked_status_count":0})
                    five_hours_list_PA_data.append({"timestamp": five_hours_list[idx], "violation_count":0, "parked_status_count":0})
            else:
                five_hours_list_NPA_data.append({"timestamp": five_hours_list[idx], "violation_count":0, "parked_status_count":0})
                five_hours_list_PA_data.append({"timestamp": five_hours_list[idx], "violation_count":0, "parked_status_count":0})
        # [{"timestamp": 2024-06-07 11:51:12, "violation_count":, "parked_status_count":},
        # {"timestamp": 2024-06-07 11:51:37, "violation_count":, "parked_status_count":}]

        # print('-----------------------TotalnumberOFSOLTS----------------',TotalnumberOFSOLTS)
        # print('-----------------------TotalnumberOFSOLTS----------------',len(TotalnumberOFSOLTS))
        result = {'totalsoltscount':len(TotalnumberOFSOLTS),"PA_message":five_hours_list_PA_data, "NPA_message":five_hours_list_NPA_data, "success":True}
    return JsonResponse(result)



# @parking_manage_data.route('/slots_status_details/VPMS/<val>', methods=['GET'])
@csrf_exempt
def slots_status_details(request,val=None):
    result = {"message": "Something went wrong with 'slots_1status_1details'", "success": False}
    if request.method == 'GET':
        today_date = datetime.today().strftime("%Y%m%d")
        today = datetime.today()
        formatted_date = today.strftime('%Y%m%d')
        if val is not None and val in ['PA', 'NPA']:
            pipeline = [
                {'$match': {
                    'date': date,
                    'analytics_log.type': {'$in': [val]}  # Adjust as per your needs
                }},
                {'$sort': {'analytics_log.timestamp': -1}},  # Sort to get the latest entry first
                {'$group': {
                    '_id': '$roi_name',
                    'latest_analytics_log': {'$last': '$analytics_log'},
                    'total_rois': {'$sum': 1}
                }},
                {'$project': {
                    '_id': 0,
                    'roi_name': '$_id',
                    'total_rois': 1,
                    'latest_analytics_log': 1
                }}
            ]

            result = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline))

            total_slots_count = 0
            PA_available_slot_count = 0
            PA_occupied_slot_count = 0
            PA_notdefined= 0


            for io , kki in enumerate(result):
                total_slots_count += 1
                # print("-----------------------------kki------",len(kki['latest_analytics_log']))
                # print("00000000000000000kki['total_rois']",kki['total_rois'])
                # print("00000000000000000kki['roi_name']",kki['roi_name'])
                if len(kki['latest_analytics_log']) !=0 :
                    LatestData = kki['latest_analytics_log'][-1]
                    # print('--------------------LatestData[status]--------------',LatestData['status'])
                    if LatestData['status'] == 'free':
                        PA_available_slot_count += 1
                    elif LatestData['status'] == 'parked':
                        PA_occupied_slot_count += 1
                    elif LatestData['status'] == 'Error':
                        PA_notdefined += 1
                
            base_query_pa = {"date":formatted_date,'analytics_log.type': "PA"}
            base_query_npa = {"date":formatted_date,'analytics_log.type': "NPA"}
            query_pa_parked = {
                "$and": [
                    base_query_pa,
                    {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "parked"]}}
                ]
            }
            query_pa_free = {
                "$and": [
                    base_query_pa,
                    {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "free"]}}
                ]
            }
            query_npa_parked = {
                "$and": [
                    base_query_npa,
                    {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "parked"]}}
                ]
            }
            query_npa_free = {
                "$and": [
                    base_query_npa,
                    {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "free"]}}
                ]
            }
            count_pa_parked = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_pa_parked)
            count_pa_free = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_pa_free)
            count_npa_parked = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_npa_parked)
            count_npa_free = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_npa_free)
            pipeline_pa_violation_1 = [
                {"$match": base_query_pa},
                {"$unwind": "$analytics_log"},
                {"$unwind": "$analytics_log.details"},
                {"$unwind": "$analytics_log.details"},
                {"$match": {"analytics_log.details.violation": 1}},
                {"$count": "count_violation_1"}
            ]
            pipeline_pa_violation_0 = [
                {"$match": base_query_pa},
                {"$unwind": "$analytics_log"},
                {"$unwind": "$analytics_log.details"},
                {"$unwind": "$analytics_log.details"},
                {"$match": {"analytics_log.details.violation": 0}},
                {"$count": "count_violation_0"}
            ]
            pipeline_npa_violation_1 = [
                {"$match": base_query_npa},
                {"$unwind": "$analytics_log"},
                {"$unwind": "$analytics_log.details"},
                {"$unwind": "$analytics_log.details"},
                {"$match": {"analytics_log.details.violation": 1}},
                {"$count": "count_violation_1"}
            ]
            pipeline_npa_violation_0 = [
                {"$match": base_query_npa},
                {"$unwind": "$analytics_log"},
                {"$unwind": "$analytics_log.details"},
                {"$unwind": "$analytics_log.details"},
                {"$match": {"analytics_log.details.violation": 0}},
                {"$count": "count_violation_0"}
            ]
            result_pa_violation_1 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_pa_violation_1))
            result_pa_violation_0 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_pa_violation_0))
            result_npa_violation_1 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_npa_violation_1))
            result_npa_violation_0 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_npa_violation_0))
            count_pa_violation_1 = result_pa_violation_1[0]['count_violation_1'] if result_pa_violation_1 else 0
            count_pa_violation_0 = result_pa_violation_0[0]['count_violation_0'] if result_pa_violation_0 else 0
            count_npa_violation_1 = result_npa_violation_1[0]['count_violation_1'] if result_npa_violation_1 else 0
            count_npa_violation_0 = result_npa_violation_0[0]['count_violation_0'] if result_npa_violation_0 else 0
            # print("Number of PA documents with status 'parked':", count_pa_parked)
            # print("Number of PA documents with status 'free':", count_pa_free)
            # print("Number of NPA documents with status 'parked':", count_npa_parked)
            # print("Number of NPA documents with status 'free':", count_npa_free)



            if val == 'PA':
                result = {"total_slots_count":total_slots_count,"Available_slot_count":PA_available_slot_count, "Occupied_slot_count":PA_occupied_slot_count,'not_define_slots':PA_notdefined, "violation_count":count_pa_violation_1, "correct_parked_count":0, "success":True}
            elif val == 'NPA':
                result = {"total_slots_count":total_slots_count,"Available_slot_count":PA_available_slot_count, "Occupied_slot_count":PA_occupied_slot_count,'not_define_slots':PA_notdefined, "violation_count":count_npa_violation_1, "correct_parked_count":0, "success":True}
        else:
            result = {"message":"please give proper value", "success":False}
        
    return JsonResponse(result)

#DASHBOARD PAGE APIS
# @parking_manage_data.route('/cameralist', methods=['GET'])
@csrf_exempt
def get_cameralist(request):

    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')
    result = {"message":"Something went wrong with cameralist", "success":False}
    if request.method == 'GET':
        VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"date":formatted_date},{'_id':0, 'dashboard_log':0}).sort('timestamp', -1))
        # print("VPMSDATA:------------", len(VPMS_data))
        cameraname_list = []
        if len(VPMS_data) != 0:
            # print("VPMS DATA:---", len(VPMS_data))
            for cam in VPMS_data:
                if cam["camera_name"] not in cameraname_list:
                    cameraname_list.append(cam["camera_name"])
            
            result = {"message": cameraname_list, "success":True}

        else:
            result = {"message": "Data not found.", "success":False}
    return JsonResponse(result)


# @parking_manage_data.route('/all_camera_slot_details', methods=['GET'])
@csrf_exempt
def all_camera_slot_details(request):
    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')
    match_data = {"date":formatted_date}
    result = {"message":"Something went wrong with all_camera_slot_details", "success":False}
    if request.method == 'GET':
        pipeline = [
        {'$match': {"date": formatted_date}},
        {'$unwind': '$analytics_log'},
        {
            '$sort': {
                'timestamp': -1  # Sort by latest entry_time first
            }
        },
        {
            '$group': {
                '_id': {
                    'camera_name': '$camera_name',
                    'roi_name': '$roi_name'
                },
                'latest_analytics_log': {'$first': '$analytics_log'}  # Get the latest analytics_log entry
            }
        },
        {
            '$group': {
                '_id': '$_id.camera_name',
                'analytics_logs': {'$push': '$latest_analytics_log'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'camera_name': '$_id',
                'total_rois': {'$size': '$analytics_logs'},
                'total_pa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$eq': ['$$log.type', 'PA']}
                        }
                    }
                },
                'total_npa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$eq': ['$$log.type', 'NPA']}
                        }
                    }
                },
                'occupied_pa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'PA']}, {'$eq': ['$$log.status', 'parked']}]}
                        }
                    }
                },
                'available_pa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'PA']}, {'$eq': ['$$log.status', 'free']}]}
                        }
                    }
                },
                'error_pa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'PA']}, {'$eq': ['$$log.status', 'Error']}]}
                        }
                    }
                },
                'occupied_npa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'NPA']}, {'$eq': ['$$log.status', 'parked']}]}
                        }
                    }
                },
                'error_npa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'NPA']}, {'$eq': ['$$log.status', 'Error']}]}
                        }
                    }
                },
                'unauthorized_parking_npa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'NPA']}, {'$eq': ['$$log.status', 'Unauthorized Parking']}]}
                        }
                    }
                },
                'free_npa_rois': {
                    '$size': {
                        '$filter': {
                            'input': '$analytics_logs',
                            'as': 'log',
                            'cond': {'$and': [{'$eq': ['$$log.type', 'NPA']}, {'$eq': ['$$log.status', 'free']}]}
                        }
                    }
                }
            }
        }
    ]
        # Run the pipeline in your MongoDB shell or application and inspect the results.
        results = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline))
        VPMS_data = results
        # Print or use the results as needed
        # for result in results:
        #     print(f"Camera: {result['camera_name']}")
        #     print(f"  PA ROIs: Total={result['total_pa_rois']}, Occupied={result['occupied_pa_rois']}, Available={result['available_pa_rois']}, Error={result['error_pa_rois']}")
        #     print(f"  NPA ROIs: Total={result['total_npa_rois']}, Occupied={result['occupied_npa_rois']}, Available={result['available_npa_rois']}, Error={result['error_npa_rois']}")

        cameraname_list = []
        if len(VPMS_data) != 0:
            result = {"message": VPMS_data, "success":True}

        else:
            result = {"message": "Data not found.", "success":False}
        
    return JsonResponse(result)


# @parking_manage_data.route('/slot_details/<val>', methods=['POST'])
# @parking_manage_data.route('/slot_details', methods=['POST'])
# @parking_manage_data.route('/slot_details/<val>', methods=['GET'])
# # @parking_manage_data.route('/slot_details/<val>', methods=['GET'])
@csrf_exempt
def slot_details(request,val=None):
    result = {"message":"Something went wrong with 'slot_details'", "success":False}
    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')
    MainQuery = {"date":formatted_date}
    if request.method == 'POST':
        jsonobject = json.loads(request.body)
        # print("JSONOBJECT:-------------------------", jsonobject)
        request_key_array = ['camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                result['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                NPAtotal_slots_count=0
                PAtotal_slots_count =0
                TotalviolationofPA = 0 
                camera_name = jsonobject["camera_name"]
                if camera_name is not None:
                    MainQuery['camera_name']= camera_name
                if val is not None:
                    MainQuery['analytics_log.type']= val
                print("===========MainQuery",MainQuery)
                VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find(MainQuery, {"_id":0, "dashboard_log":0}).sort('timestamp', -1))
                if len(VPMS_data) != 0:
                    base_query_pa = {'camera_name':camera_name,"date":formatted_date,'analytics_log.type': "PA"}
                    base_query_npa = {'camera_name':camera_name,"date":formatted_date,'analytics_log.type': "NPA"}
                    query_pa_parked = {
                        "$and": [
                            base_query_pa,
                            {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "parked"]}}
                        ]
                    }
                    query_pa_free = {
                        "$and": [
                            base_query_pa,
                            {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "free"]}}
                        ]
                    }
                    query_npa_parked = {
                        "$and": [
                            base_query_npa,
                            {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "parked"]}}
                        ]
                    }
                    query_npa_free = {
                        "$and": [
                            base_query_npa,
                            {"$expr": {"$eq": [{"$arrayElemAt": ["$analytics_log.status", -1]}, "free"]}}
                        ]
                    }
                    count_pa_parked = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_pa_parked)
                    count_pa_free = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_pa_free)
                    count_npa_parked = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_npa_parked)
                    count_npa_free = VEHICLE_PARKING_MANAGEMENT_DATA.count_documents(query_npa_free)
                    pipeline_pa_violation_1 = [
                        {"$match": base_query_pa},
                        {"$unwind": "$analytics_log"},
                        {"$unwind": "$analytics_log.details"},
                        {"$match": {"analytics_log.details.violation": 1}},
                        {"$count": "count_violation_1"}
                    ]
                    pipeline_pa_violation_0 = [
                        {"$match": base_query_pa},
                        {"$unwind": "$analytics_log"},
                        {"$unwind": "$analytics_log.details"},
                        {"$match": {"analytics_log.details.violation": 0}},
                        {"$count": "count_violation_0"}
                    ]
                    pipeline_npa_violation_1 = [
                        {"$match": base_query_npa},
                        {"$unwind": "$analytics_log"},
                        {"$unwind": "$analytics_log.details"},
                        {"$match": {"analytics_log.details.violation": 1}},
                        {"$count": "count_violation_1"}
                    ]
                    pipeline_npa_violation_0 = [
                        {"$match": base_query_npa},
                        {"$unwind": "$analytics_log"},
                        {"$unwind": "$analytics_log.details"},
                        {"$match": {"analytics_log.details.violation": 0}},
                        {"$count": "count_violation_0"}
                    ]
                    result_pa_violation_1 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_pa_violation_1))
                    result_pa_violation_0 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_pa_violation_0))
                    result_npa_violation_1 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_npa_violation_1))
                    result_npa_violation_0 = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline_npa_violation_0))
                    count_pa_violation_1 = result_pa_violation_1[0]['count_violation_1'] if result_pa_violation_1 else 0
                    count_pa_violation_0 = result_pa_violation_0[0]['count_violation_0'] if result_pa_violation_0 else 0
                    count_npa_violation_1 = result_npa_violation_1[0]['count_violation_1'] if result_npa_violation_1 else 0
                    count_npa_violation_0 = result_npa_violation_0[0]['count_violation_0'] if result_npa_violation_0 else 0
                    # print("Number of PA documents with status 'parked':", count_pa_parked)
                    # print("Number of PA documents with status 'free':", count_pa_free)
                    # print("Number of NPA documents with status 'parked':", count_npa_parked)
                    # print("Number of NPA documents with status 'free':", count_npa_free)
                    # print("Number of PA documents with violation = 1:", count_pa_violation_1)
                    # print("Number of PA documents with violation = 0:", count_pa_violation_0)
                    # print("Number of NPA documents with violation = 1:", count_npa_violation_1)
                    # print("Number of NPA documents with violation = 0:", count_npa_violation_0)
                    PAmatch_data = {"date":formatted_date,'camera_name':camera_name,'analytics_log.type':'PA'}    
                    PApipeline = [
                                {'$match': PAmatch_data},
                                {'$sort': {'timestamp': -1}},
                                {
                                    '$group': {
                                        '_id': {
                                            'camera_name': '$camera_name',
                                            'roi_name': '$roi_name'
                                        },
                                        'latest_analytics_log': {'$first': '$analytics_log'},
                                        'total_slots_count': {'$sum': 1},
                                        'occupied_slot_count': {'$sum': {'$cond': [{'$eq': ['$analytics_log.status', 'parked']}, 1, 0]}},
                                        'available_slot_count': {'$sum': {'$cond': [{'$eq': ['$analytics_log.status', 'free']}, 1, 0]}},
                                        'violation_count': {'$sum': {'$cond': [{'$eq': ['$analytics_log.details.violation', 1]}, 1, 0]}},
                                        'correct_parked_count': {'$sum': {'$cond': [{'$eq': ['$analytics_log.details.violation', 0]}, 1, 0]}}
                                    }
                                },
                                {
                                    '$project': {
                                        '_id': 0,
                                        'camera_name': '$_id.camera_name',
                                        'roi_name': '$_id.roi_name',
                                        'type': '$_id.type',
                                        'total_slots_count': 1,
                                        'occupied_slot_count': 1,
                                        'available_slot_count': 1,
                                        'violation_count': 1,
                                        'correct_parked_count': 1
                                    }
                                }
                            ]       
                    PAVPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(PApipeline))

                    total_slots_count= 0
                    # print("--------VPMS_data---------",PAVPMS_data)     
                    NPAmatch_data={"date":formatted_date,'camera_name':camera_name,'analytics_log.type':'NPA'}  
                    pipeline = [
                                {'$match': NPAmatch_data},
                                #{'$sort': {'timestamp': -1}},
                                {
                                    '$group': {
                                        '_id': {
                                            'camera_name': '$camera_name',
                                            'roi_name': '$roi_name'
                                        },
                                        'latest_analytics_log': {'$first': '$analytics_log'},
                                        'roi_count': {'$sum': 1}
                                    }
                                },
                                {
                                    '$project': {
                                        'camera_name': '$_id.camera_name',
                                        'roi_name': '$_id.roi_name',
                                        'roi_count': 1,
                                        'latest_status': {
                                            '$arrayElemAt': [
                                                {
                                                    '$filter': {
                                                        'input': '$latest_analytics_log',
                                                        'as': 'log',
                                                        'cond': {'$ne': ['$$log.status', None]}
                                                    }
                                                }, -1
                                            ]
                                        }
                                    }
                                },
                                {
                                    '$group': {
                                        '_id': '$camera_name',
                                        'total_slots_count': {'$sum': '$roi_count'},
                                        'statuses': {'$push': '$latest_status.status'}
                                    }
                                },
                                {
                                    '$project': {
                                        'cameaname': '$_id',
                                        '_id': 0,
                                        'total_slots_count': 1,
                                        'occupied_slots_count': {
                                            '$size': {
                                                '$filter': {
                                                    'input': '$statuses',
                                                    'as': 'status',
                                                    'cond': {'$eq': ['$$status', 'parked']}
                                                }
                                            }
                                        },
                                        'available_slots_count': {
                                            '$size': {
                                                '$filter': {
                                                    'input': '$statuses',
                                                    'as': 'status',
                                                    'cond': {'$eq': ['$$status', 'free']}
                                                }
                                            }
                                        },
                                        'error_slot_count': {
                                            '$size': {
                                                '$filter': {
                                                    'input': '$statuses',
                                                    'as': 'status',
                                                    'cond': {'$eq': ['$$status', 'Error']}
                                                }
                                            }
                                        }
                                    }
                                }
                            ]            
                    NPAVPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate(pipeline))
                    cameraname_list = []
                    if len(NPAVPMS_data) != 0:
                        print("--------------------NPAtotal_slots_count = NPAVPMS_data[0]['total_slots_count']",len(NPAVPMS_data))
                        NPAtotal_slots_count = NPAVPMS_data[0]['total_slots_count']
                    if len(PAVPMS_data) !=0 :
                        PAtotal_slots_count=PAVPMS_data[0]['total_slots_count']
                        TotalviolationofPA = PAVPMS_data[0]['violation_count']
                        print('-----------TotalviolationofPA----------',TotalviolationofPA)
                    resultpa = {"camera_name":camera_name, "objects_count":0, "occupied_slot_count":count_pa_parked, "violation_count":count_pa_violation_1, 
                                "correct_parked_count":count_pa_violation_0, "total_slots_count":PAtotal_slots_count,'available_slot_count':count_pa_free}
                    

                    resultnpa = {"camera_name":camera_name, "objects_count":0, "occupied_slot_count":count_npa_parked, "violation_count":count_npa_violation_1, 
                                "correct_parked_count":count_npa_violation_0, "total_slots_count":NPAtotal_slots_count,'available_slot_count':count_npa_free}
                    St=[{
                        "type":'PA','results':resultpa
                    },{
                        "type":'NPA','results':resultnpa
                    }]
                    result = {"message":St,"success":True}
                else:
                    result = {"message":"fiven camera doesn't have data.", "success":False}
        else:
            result = {"message":request_key_array, "success":False}
    elif request.method == 'GET':
        if val is not None:
            MainQuery['analytics_log.type']= val
        VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find(MainQuery, {"_id":0, "dashboard_log":0}).sort('timestamp', -1))
        # print("VPMS DATA:----dataaaaaaaaaaaa-----1.1.0----------", len(VPMS_data) )  
        
        if len(VPMS_data) != 0:
            available_slot_count = 0
            occupied_slot_count = 0
            violation_count = 0
            valid_parked_count = 0
            objects_count = 0
            ViolationCOuntData= []
            for PA_data in VPMS_data:
                # print("PARKING DATA:-----------------------", PA_data["roi_name"], type(PA_data["analytics_log"][-1]))
                total_NPA_slots_count =[]
                if PA_data["analytics_log"][-1]["status"] == "parked":
                    occupied_slot_count += 1
                elif PA_data["analytics_log"][-1]["status"] == "free":
                    available_slot_count += 1
                # if PA_data["analytics_log"][-1]["type"] == "PA":
                for analytics_data in PA_data["analytics_log"]:
                    # if PA != None:
                    if val == "PA":
                        # violation_count = 0
                        # valid_parked_count = 0
                        # print("ANALYTICS DATA:-------------------", analytics_data["details"])
                        for violation_detail in analytics_data["details"]:
                            # print("violation_detailviolation_detail:----", violation_detail["violation"])
                            if violation_detail["violation"] == 1:
                                violation_count += 1

                            elif violation_detail["violation"] == 0:
                                valid_parked_count += 1

                        result = {"camera_name":PA_data["camera_name"],"total_count":available_slot_count+ occupied_slot_count, "Available_slot_count":available_slot_count, "Occupied_slot_count":occupied_slot_count, "violation_count":violation_count, "correct_parked_count":valid_parked_count, "success":True}

                    # elif PA_data["analytics_log"][-1]["type"] == "NPA":
                    # elif NPA != None:
                    elif val == "NPA":
                        # {"date":"20240621",  "camera_name":"dfd"}
                        total_NPA_slots_count = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"date":formatted_date, "camera_name":PA_data["camera_name"]}, {"_id":0, "dashboard_log":0}).sort('timestamp', -1))
                        for analytics_data in PA_data["analytics_log"]:
                            # violation_count = 0
                            # valid_parked_count = 0
                            # print("ANALYTICS DATA:-------------------", analytics_data["details"])
                            for violation_detail in analytics_data["details"]:
                                # print("violation_detailviolation_detail:----", violation_detail["violation"])
                                if violation_detail["violation"] == 1:
                                    violation_count += 1
                                    if len(violation_detail["obj_details"]) != 0:
                                        for obj_details in violation_detail["obj_details"]:
                                            if obj_details["violation"] == 1:
                                                objects_count += 1

                                elif violation_detail["violation"] == 0:
                                    valid_parked_count += 1

                ViolationCOuntData.append({"camera_name":PA_data["camera_name"], "objects_count":objects_count, "Occupied_slot_count":occupied_slot_count, "violation_count":violation_count,
                                "correct_parked_count":valid_parked_count, "total_slots_count":len(total_NPA_slots_count) })
                
            if len(ViolationCOuntData) !=0 :
                result = {"message":ViolationCOuntData, "success":True} 
            else:
                result = {"message":"there no data violation data found.", "success":True}    
        else:
            result = {"message":"Given camera doesn't have data.", "success":False}        
    return JsonResponse(result)


# #HISTORY PAGE APIS
# @parking_manage_data.route('/PA_history/<flag>', methods=['GET'])
# @parking_manage_data.route('/PA_history', methods=['GET'])
@csrf_exempt
def get_PA_history(request,flag=None):
    result = {"message":"Something went wrong with 'PA_history'", "success":False}
    if request.method == "GET":
        today = datetime.today()
        formatted_date = today.strftime('%Y%m%d')
        if flag is not None:
            # print("FALG VALUE:-----", type(flag))
            if flag == "True":
                # print("FLAG VALUE:-111111111111----", flag)
                VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"date":formatted_date},{'_id':0, 'dashboard_log':0}).sort('timestamp', -1))
                # print("VPMSDATA:------------", len(VPMS_data))
                PA_history_data = []
                if len(VPMS_data) != 0:
                    for pa_data in VPMS_data:
                        analytics_log_list_1 = []
                        for analytics_para in pa_data["analytics_log"]:
                            # if analytics_para["type"] == "PA" and analytics_para["status"] == "parked":
                            if analytics_para["type"] == "PA" :#and analytics_para["status"] == "parked":
                                analytics_log_list_1.append(analytics_para)                
                        if len(analytics_log_list_1) != 0:
                            analytics_log_list_1 = analytics_log_list_1[::-1]
                            PA_history_data.append({"camera_name":pa_data["camera_name"], "roi_name":pa_data["roi_name"], "department":pa_data["camera_rtsp"], "date":pa_data["date"], "analytics_log":analytics_log_list_1, "timestamp":pa_data["timestamp"]})
                    if len(PA_history_data) != 0:
                        result = {"message":PA_history_data, "success":True}                
                    else:
                        result = {"message":PA_history_data, "success":False}
                else:
                    result = {"message":"data no found.", "success":False}
            elif flag == "False":
                # print("FALG VALUE:--222222222---", flag)
                VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"date":formatted_date},{'_id':0, 'dashboard_log':0}).sort('timestamp', -1))
                # print("VPMSDATA:------------", len(VPMS_data))
                NPA_history_data = []
                if len(VPMS_data) != 0:
                    for pa_data in VPMS_data:
                        # print("PA DATA:-", pa_data) #["analytics_log"])
                        analytics_log_list_2 = []
                        for analytics_para in pa_data["analytics_log"]:
                            # print("analytics_para sSSSTATUS", analytics_para["status"]) # analytics_para["type"])
                            if analytics_para["type"] == "NPA": # or analytics_para["status"] == "parked":
                                analytics_log_list_2.append(analytics_para)                
                        if len(analytics_log_list_2) != 0:
                            analytics_log_list_2 = analytics_log_list_2[::-1]
                            NPA_history_data.append({"camera_name":pa_data["camera_name"], "roi_name":pa_data["roi_name"], "department":pa_data["camera_rtsp"], "date":pa_data["date"], "analytics_log":analytics_log_list_2, "timestamp":pa_data["timestamp"]})
                    result = {"message":NPA_history_data, "success":True}
                else:
                    result = {"message":"data no found.", "success":False}
        else:

            main_man = {"date":formatted_date}
            # print("---------------------------main_man---------------",main_man)
            VPMS_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({"date":formatted_date},{'_id':0, 'dashboard_log':0}).sort('timestamp', -1))
            # print("VPMSDATA:---1.101---------", len(VPMS_data))
            history_data = []
            if len(VPMS_data) != 0:
                for pa_data in VPMS_data:
                    # print("PA DATA:-", pa_data) #["analytics_log"])
                    analytics_log_list_3 = []
                    for analytics_para in pa_data["analytics_log"]:
                        # print("analytics_para",analytics_para["type"])
                        # if analytics_para["status"] == "parked" or analytics_para["status"] == "Unauthorized Parking":
                        analytics_log_list_3.append(analytics_para)
                    if len(analytics_log_list_3) != 0:
                        analytics_log_list_3 = analytics_log_list_3[::-1]
                        history_data.append({"camera_name":pa_data["camera_name"], "roi_name":pa_data["roi_name"], "department":pa_data["camera_rtsp"], "date":pa_data["date"], "analytics_log":analytics_log_list_3, "timestamp":pa_data["timestamp"]})
                result = {"message":history_data, "success":True}
            else:
                result = {"message":"data no found.", "success":False}
    return JsonResponse(result)


# @parking_manage_data.route('/violations_data', methods=['GET'])
@csrf_exempt
def get_VPMS_history(request):
    result = {"message":"Something went wrong with 'VPMS_history'", "success":False}
    if request.method == "GET":
        today = datetime.today()
        formatted_date = today.strftime('%Y%m%d')
        all_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find(
            {"date": formatted_date, 'analytics_log.details.violation': 1},
            {'_id': 0, 'dashboard_log': 0}
        ).sort('timestamp', -1))

        # print("---------------------all_data-------------------------", len(all_data))
        for ViolationData in all_data:
            ViolationData['analytics_log'] = ViolationData['analytics_log'][::-1]
        violations_data_list = []
        if all_data:
            for pa_data in all_data:
                analytics_log_list_4 = []
                for analytics_para in pa_data["analytics_log"]:
                    for violated_data in analytics_para["details"]:
                        if violated_data["violation"] == 1:
                            analytics_log_list_4.append(analytics_para)
                
                if analytics_log_list_4:
                    violations_data_list.append({
                        "camera_name": pa_data["camera_name"], 
                        "roi_name": pa_data["roi_name"],
                        "department": pa_data["camera_rtsp"], 
                        "timestamp": pa_data["date"], 
                        "analytics_log": analytics_log_list_4
                    })
            result = {"message": violations_data_list, "success": True}
        else:
            result = {"message": "data not found.", "success": False}

    return JsonResponse(result)


# from datetime.datetime import date
# @parking_manage_data.route('/list_PA_slots', methods=['POST'])
# # @parking_manage_data.route('/list_PA_slots/<camera_name>', methods=['POST'])
@csrf_exempt
def PA_Slots(request):
    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')
    result = {'success': False, 'message': 'Something went wrong in list_PA_slots.'}
    if request.method == "POST":
        jsonobject = json.loads(request.body)
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['camera_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                result['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                print("jsonobject:-----------------", jsonobject)
                all_slots= list(VPMS_DATA.find({"camera_rtsp":jsonobject["camera_name"], "date":formatted_date},{'analytics_log':0,'date':0, 'id':0, 'dashboard_log':0, '_id':0, 'camera_rtsp':0, 'analytics_type':0}).sort('date', -1))
                # print("all_slots:------------", all_slots)
                slot_list = []
                for x in all_slots:
                    slot_list.append(x["roi_name"])
                if len(all_slots) != 0: 
                    result = {"message":slot_list, "success":True}
                else:
                    result = {"message":"No data found !!", "success":False}

    return JsonResponse(result)


# @parking_manage_data.route('/latest_parking_history', methods=['GET'])
@csrf_exempt
def latest_history(request):
    result = {"message":"Something went wrong with 'latest_parking_history'", "success":False}
    if request.method == "GET":
        today = datetime.today()
        formatted_date = today.strftime('%Y%m%d')
        match_data = {"date":formatted_date}
        data = list(VEHICLE_PARKING_MANAGEMENT_DATA.aggregate([{'$match': match_data}, {'$limit': 4000000}, {'$sort':{'timestamp': -1}}, {'$limit': 1},
                                                        {'$project': {'dashboard_log':0, '_id':0}}]))    # print("data:0---------------",len(data))
        latest_history_list = []
        if len(data) !=0 :
            # print("-------1.101---data---------------------")
            for vpms_date in data:
                # print("-------1.102---data---------------------")
                if len(vpms_date["analytics_log"]) !=0:
                    # print("-------1.103---data---------------------")
                    vpms_date["analytics_log"] = vpms_date["analytics_log"][-1]
                    latest_history_list.append(vpms_date)
                
            # if vpms_date["analytics_log"][-1]["status"] == "parked":
            #     vpms_date["analytics_log"] = vpms_date["analytics_log"][-1]
            #     latest_history_list.append(vpms_date)
            #     result = {"message":latest_history_list, "success":True}

            if len(latest_history_list) !=0 :
                result = {"message":latest_history_list, "success":True}
            else:
                # print("-------1.104---data---------------------")
                result = {"message":"data not found.", "success":False}

        else:
            result = {"message":"data not found.", "success":False}
    return JsonResponse(result)


# @parking_manage_data.route('/datewise_camera_list', methods=['POST'])
@csrf_exempt
def datewise_camera_list(request):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if request.method == 'POST':
        jsonobject = json.loads(request.body)
        # print("parking_type", jsonobject) # jsonobject["parking_type"])
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)

        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            
            else:
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find({'timestamp':{'$gte':from_date, '$lte': to_date}},
                                                            {'dashboard_log':0}).sort('date', -1))
                camera_list = []
                for cam_par in data:
                    if cam_par["camera_name"] not in camera_list:
                        camera_list.append(cam_par["camera_name"])

                if len(camera_list) != 0:
                    ret = {"message":camera_list, "success":True}

                else:
                    ret = {"message":"There is no cameras.", "success":False}

        else:
            ret = {'success': False, 'message':" ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}

    return JsonResponse(ret)


# @parking_manage_data.route('/datewise_history', methods=['POST'])
@csrf_exempt
def datewise_violation(request):
    ret = {'success': False, 'message': 'Something went wrong.'}
    if request.method == 'POST':
        jsonobject = json.loads(request.body)
        try:
            mainQuery= {}
            # jsonobject = request.json
            # print("parking_type", jsonobject) 
            if jsonobject == None:
                jsonobject = {}
            request_key_array = ['from_date', 'to_date', 'cameraname', 'department', 'parking_type', 'violation_value']
            jsonobjectarray = list(set(jsonobject))
            missing_key = set(request_key_array).difference(jsonobjectarray)
            if not missing_key:
                output = [k for k, v in jsonobject.items() if v == '']
                if output:
                    ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
                else:
                    all_data = []
                    from_date = jsonobject['from_date']
                    to_date = jsonobject['to_date']
                    parking_type = jsonobject['parking_type']
                    cameraname = jsonobject['cameraname']
                    violation_value = jsonobject['violation_value']
                    department = jsonobject['department']
                    if from_date is not None and to_date is not None:
                        mainQuery['timestamp']={'$gte':from_date, '$lte': to_date}
                    if cameraname is not None:
                        mainQuery['camera_name']=cameraname
                    if department is not None:
                        mainQuery['department']=department
                    if parking_type is not None:
                        mainQuery['analytics_log.type']=parking_type
                    if 'violation_value' in jsonobject:
                        if violation_value is not None:
                            mainQuery['analytics_log.details.violation']=1
                        # else:
                        #     mainQuery['analytics_log.details.violation']=parking_type
                    print("--------------------------mainQuery-----------------",mainQuery)
                    violation_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find(mainQuery
                                                            ,{'dashboard_log':0, '_id':0}).sort('date', -1))
                    print("-----------------------violation_data---------------",len(violation_data))
                    NPA_history_data = []
                    FINALNewarray= [] 
                    if len(violation_data) != 0:                    
                        if violation_value is not None:
                            
                            if parking_type is None:
                                for pa_data in violation_data[::-1]:
                                    analytics_log_list_2 = []
                                    for analytics_para in pa_data["analytics_log"][::-1]:
                                        Newarray=[]
                                        if (parking_type is None and analytics_para["type"] in ['NPA', 'PA']) or analytics_para["type"] == parking_type:
                                            filtered_details = [
                                                detail for detail in analytics_para["details"] 
                                                if detail["violation"] == 1
                                            ]
                                            if filtered_details:
                                                filtered_analytics_para = analytics_para.copy()
                                                analytics_para["details"] = filtered_details
                                                analytics_log_list_2.append(analytics_para)

                                            for i , j in enumerate(analytics_log_list_2):
                                                if j not in Newarray:
                                                    Newarray.append(j)

                                    pa_data["analytics_log"]= Newarray
                                    if pa_data not in FINALNewarray:
                                        FINALNewarray.append(pa_data)
                                
                            elif parking_type == 'PA':
                                
                                for pa_data in violation_data[::-1]:
                                    print("------datewise-----PA-----------")
                                    analytics_log_list_2 = []
                                    for analytics_para in pa_data["analytics_log"][::-1]:
                                        Newarray=[]
                                        if (parking_type is None and analytics_para["type"] in ['PA']) or analytics_para["type"] == parking_type:
                                            # filtered_details = [
                                            #     detail for detail in analytics_para["details"] 
                                            #     if detail["violation"] == 1
                                            # ]
                                            filtered_details = []
                                            for Newidex , NewValue in enumerate(analytics_para['details']):
                                                if NewValue['violation']==1:
                                                    # print("--------NewValue--------------",NewValue)
                                                    filtered_details.append(NewValue)
                                            # print("------------analytics_para[details]------",len(analytics_para["details"]))
                                            # print("------------------------filtered_details-------------------",filtered_details)
                                            # for i,j in enumerate(filtered_details):
                                            #     print('------------j---------',j)
                                            # print("\n")
                                            if len(filtered_details) !=0 :
                                                filtered_analytics_para = analytics_para.copy()
                                                filtered_analytics_para["details"] = filtered_details
                                                analytics_log_list_2.append(filtered_analytics_para)
                                        for i , j in enumerate(analytics_log_list_2):
                                            if j not in Newarray:
                                                Newarray.append(j)

                                    pa_data["analytics_log"]= Newarray
                                    if pa_data not in FINALNewarray:
                                        FINALNewarray.append(pa_data)
                            elif parking_type == 'NPA':
                                for pa_data in violation_data[::-1]:
                                    Newarray=[]
                                    analytics_log_list_2 = []
                                    for analytics_para in pa_data["analytics_log"][::-1]:
                                        if (parking_type is None and analytics_para["type"] in ['NPA']) or analytics_para["type"] == parking_type:
                                            filtered_details = [
                                                detail for detail in analytics_para["details"] 
                                                if detail["violation"] == 1
                                            ]
                                            if filtered_details:
                                                filtered_analytics_para = analytics_para.copy()
                                                analytics_para["details"] = filtered_details
                                                analytics_log_list_2.append(analytics_para)

                                        for i , j in enumerate(analytics_log_list_2):
                                            if j not in Newarray:
                                                Newarray.append(j)

                                    pa_data["analytics_log"]= Newarray
                                    if pa_data not in FINALNewarray:
                                        FINALNewarray.append(pa_data)
                            # for KKKKDLLLLD, NNNDKKDKDKD in enumerate(FINALNewarray):
                            #     print("---------NNNDKKDKDKD-------------",NNNDKKDKDKD)
                            #     print("---------NNNDKKDKDKD----analytics_log---------",NNNDKKDKDKD['analytics_log'])
                            
                        else:
                            analytics_log_list_2 = violation_data
                            if parking_type is None:
                                analytics_log_list_2 = [
                                    pa_data
                                    for pa_data in violation_data[::-1]
                                    for analytics_para in pa_data["analytics_log"][::-1]
                                    if analytics_para["type"] in ['NPA', 'PA']
                                ]

                                for i , j in enumerate(analytics_log_list_2):
                                    if j not in FINALNewarray:
                                        FINALNewarray.append(j)
                            elif  parking_type == 'PA':
                                analytics_log_list_2 = [
                                    pa_data 
                                    for pa_data in violation_data[::-1] 
                                    for analytics_para in pa_data["analytics_log"][::-1] 
                                    if analytics_para["type"] ==  'PA'
                                ]
                                for i , j in enumerate(analytics_log_list_2):
                                    if j not in FINALNewarray:
                                        FINALNewarray.append(j)


                            elif  parking_type == 'NPA':
                                analytics_log_list_2 = [
                                    pa_data 
                                    for pa_data in violation_data[::-1] 
                                    for analytics_para in pa_data["analytics_log"][::-1] 
                                    if analytics_para["type"] ==  'NPA'
                                ]
                                for i , j in enumerate(analytics_log_list_2):
                                    if j not in FINALNewarray:
                                        FINALNewarray.append(j)

                        if len(FINALNewarray) !=0:
                            ret = {'success':True, 'message':FINALNewarray}
                        else:
                            ret= {'success':False, 'message':FINALNewarray}
                    else:
                        ret = {'success': False, 'message': 'data not found'}
            else:
                ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
        
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
            print("print(,)", str(error))
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise_violation 1", str(error), " ----time ---- ", now_time_with_time()])) 
            ret['message'] =" ".join(["something error has occered in api", str(error)])
            
            if restart_mongodb_r_service():
                print("mongodb restarted")
            else:
                if forcerestart_mongodb_r_service():
                    print("mongodb service force restarted-")
                else:
                    print("mongodb service is not yet started.")
        except Exception as  error:
            ret = {'success': False, 'message': str(error)}
            ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise_violation 2", str(error), " ----time ---- ", now_time_with_time()]))         
    return JsonResponse(ret)




###########################################VPMS EXCEL CREATION###########################################################################
# from openpyxl import Workbook
# from openpyxl.drawing.image import Image as OpenPyXLImage
# from io import BytesIO
# from PIL import Image

# import os




@csrf_exempt
def datewise_violation_excel(request,from_date, to_date):
    ret = {'success': False, 'message': 'Something went wrong.'}
    try:
        mainQuery= {}
        jsonobject = json.loads(request.body)
        # print("parking_type", jsonobject) 
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['from_date', 'to_date', 'cameraname', 'department', 'parking_type', 'violation_value']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                parking_type = jsonobject['parking_type']
                cameraname = jsonobject['cameraname']
                violation_value = jsonobject['violation_value']
                #print("1111111111111111111111violation_value111111111111111111",violation_value)
                department = jsonobject['department']
                if from_date is not None and to_date is not None:
                    mainQuery['timestamp']={'$gte':from_date, '$lte': to_date}
                if cameraname is not None:
                    mainQuery['camera_name']=cameraname
                if department is not None:
                    mainQuery['department']=department
                if parking_type is not None:
                    mainQuery['analytics_log.type']=parking_type
                if 'violation_value' in jsonobject:
                    if violation_value is not None:
                        mainQuery['analytics_log.details.violation']=1
                    # else:
                    #     mainQuery['analytics_log.details.violation']=parking_type
                #print("--------------------------mainQuery-----------------",mainQuery)
                violation_data = list(VEHICLE_PARKING_MANAGEMENT_DATA.find(mainQuery
                                                        ,{'dashboard_log':0, '_id':0}).sort('date', -1))
                #print("-----------------------violation_data-666666--------------",violation_data)
                NPA_history_data = []
                FINALNewarray= [] 
                if len(violation_data) != 0:                    
                    if violation_value is not None:
                        
                        if parking_type is None:
                            for pa_data in violation_data[::-1]:
                                analytics_log_list_2 = []
                                for analytics_para in pa_data["analytics_log"][::-1]:
                                    Newarray=[]
                                    if (parking_type is None and analytics_para["type"] in ['NPA', 'PA']) or analytics_para["type"] == parking_type:
                                        filtered_details = [
                                            detail for detail in analytics_para["details"] 
                                            if detail["violation"] == 1
                                        ]
                                        if filtered_details:
                                            filtered_analytics_para = analytics_para.copy()
                                            analytics_para["details"] = filtered_details
                                            analytics_log_list_2.append(analytics_para)

                                        for i , j in enumerate(analytics_log_list_2):
                                            if j not in Newarray:
                                                Newarray.append(j)

                                pa_data["analytics_log"]= Newarray
                                if pa_data not in FINALNewarray:
                                    FINALNewarray.append(pa_data)
                            
                        elif parking_type == 'PA':
                            
                            for pa_data in violation_data[::-1]:
                                print("------datewise-----PA-----------")
                                analytics_log_list_2 = []
                                for analytics_para in pa_data["analytics_log"][::-1]:
                                    Newarray=[]
                                    if (parking_type is None and analytics_para["type"] in ['PA']) or analytics_para["type"] == parking_type:
                                        
                                        filtered_details = []
                                        for Newidex , NewValue in enumerate(analytics_para['details']):
                                            if NewValue['violation']==1:
                                                # print("--------NewValue--------------",NewValue)
                                                filtered_details.append(NewValue)
                                    
                                        if len(filtered_details) !=0 :
                                            filtered_analytics_para = analytics_para.copy()
                                            filtered_analytics_para["details"] = filtered_details
                                            analytics_log_list_2.append(filtered_analytics_para)
                                    for i , j in enumerate(analytics_log_list_2):
                                        if j not in Newarray:
                                            Newarray.append(j)

                                pa_data["analytics_log"]= Newarray
                                if pa_data not in FINALNewarray:
                                    FINALNewarray.append(pa_data)
                        elif parking_type == 'NPA':
                            for pa_data in violation_data[::-1]:
                                Newarray=[]
                                analytics_log_list_2 = []
                                for analytics_para in pa_data["analytics_log"][::-1]:
                                    if (parking_type is None and analytics_para["type"] in ['NPA']) or analytics_para["type"] == parking_type:
                                        filtered_details = [
                                            detail for detail in analytics_para["details"] 
                                            if detail["violation"] == 1
                                        ]
                                        if filtered_details:
                                            filtered_analytics_para = analytics_para.copy()
                                            analytics_para["details"] = filtered_details
                                            analytics_log_list_2.append(analytics_para)

                                    for i , j in enumerate(analytics_log_list_2):
                                        if j not in Newarray:
                                            Newarray.append(j)

                                pa_data["analytics_log"]= Newarray
                                if pa_data not in FINALNewarray:
                                    FINALNewarray.append(pa_data)
                        
                    else:
                        analytics_log_list_2 = violation_data
                        if parking_type is None:
                            analytics_log_list_2 = [
                                pa_data
                                for pa_data in violation_data[::-1]
                                for analytics_para in pa_data["analytics_log"][::-1]
                                if analytics_para["type"] in ['NPA', 'PA']
                            ]

                            for i , j in enumerate(analytics_log_list_2):
                                if j not in FINALNewarray:
                                    FINALNewarray.append(j)
                        elif  parking_type == 'PA':
                            analytics_log_list_2 = [
                                pa_data 
                                for pa_data in violation_data[::-1] 
                                for analytics_para in pa_data["analytics_log"][::-1] 
                                if analytics_para["type"] ==  'PA'
                            ]
                            for i , j in enumerate(analytics_log_list_2):
                                if j not in FINALNewarray:
                                    FINALNewarray.append(j)


                        elif  parking_type == 'NPA':
                            analytics_log_list_2 = [
                                pa_data 
                                for pa_data in violation_data[::-1] 
                                for analytics_para in pa_data["analytics_log"][::-1] 
                                if analytics_para["type"] ==  'NPA'
                            ]
                            for i , j in enumerate(analytics_log_list_2):
                                if j not in FINALNewarray:
                                    FINALNewarray.append(j)

                    if len(FINALNewarray) !=0:
                        return {'success':True, 'data':FINALNewarray}
                        
                    else:
                        return {'success':False, 'data':FINALNewarray}
                return FINALNewarray
                # else:
                #    ret={'success': False, 'message': 'data not found'}
        else:
            ret= {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    
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
        print("print(,)", str(error))
        ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- datewise_violation 1", str(error), " ----time ---- ", now_time_with_time()])) 
        ret['message'] =" ".join(["something error has occered in api", str(error)])
        return FINALNewarray
       
    




def VPMScreate_chart(workbook, from_date, to_date, violation_types, FINALNewarray, title=None):
    try:
        start_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date format! Please enter the date in 'YYYY-MM-DD HH:MM:SS' format.")
        return

    header_font = workbook.add_format({'bold': True, 'color': 'FFFFFF', 'bg_color': '4F81BD', 'size': 12})
    border_style = workbook.add_format({'border': 1})

    violations_by_date = defaultdict(lambda: {'PA': 0, 'NPA': 0})  # For date-wise counting
    violations_by_timestamp = defaultdict(lambda: {'PA': 0, 'NPA': 0})  # For timestamp-wise counting
    type_presence = {'PA': False, 'NPA': False}

    date_range_exceeds_three_days = (end_date - start_date).days > 3
    print("Date range exceeds three days:", date_range_exceeds_three_days)

    # Process FINALNewarray to fill violations_by_date and violations_by_timestamp
    for record in FINALNewarray:
        analytics_type = record.get('analytics_type')
        for log in record.get('analytics_log', []):
            violation_type = log.get('type')
            timestamp = record.get("timestamp")
            if timestamp and violation_type in ['PA', 'NPA']:
                timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if start_date <= timestamp_obj <= end_date:
                    if date_range_exceeds_three_days:
                        violations_by_date[timestamp_obj.date()][violation_type] += 1
                    else:
                        violations_by_timestamp[timestamp_obj][violation_type] += 1
                    type_presence[violation_type] = True

    # Ensure all timestamps within the range are included (hourly if timestamp-wise)
    if not date_range_exceeds_three_days:
        current_time = start_date
        while current_time <= end_date:
            if current_time not in violations_by_timestamp:
                violations_by_timestamp[current_time] = {'PA': 0, 'NPA': 0}
            current_time += timedelta(hours=1)

    # Ensure all dates within the range are included (if date-wise)
    if date_range_exceeds_three_days:
        current_date = start_date.date()
        while current_date <= end_date.date():
            if current_date not in violations_by_date:
                violations_by_date[current_date] = {'PA': 0, 'NPA': 0}
            current_date += timedelta(days=1)

    # Sort the timestamps or dates
    if date_range_exceeds_three_days:
        sorted_dates = OrderedDict(sorted(violations_by_date.items()))
    else:
        sorted_timestamps = OrderedDict(sorted(violations_by_timestamp.items()))

    # Prepare headers based on violation types
    headers = ['Date' if date_range_exceeds_three_days else 'Timestamp']
    if type_presence['PA']:
        headers.append('PA Count')
    if type_presence['NPA']:
        headers.append('NPA Count')

    sheet_name = f"{analytics_type} - Violations Summary"
    existing_sheets = [sheet.get_name() for sheet in workbook.worksheets_objs]
    if sheet_name not in existing_sheets:
        sheet = workbook.add_worksheet(sheet_name)
    else:
        return  # Skip if the sheet already exists

    # Write headers to the sheet
    for col_num, header in enumerate(headers):
        sheet.write(0, col_num, header, header_font)

    # Fill data into the sheet
    row_index = 1
    total_counts = {'PA': 0, 'NPA': 0}

    if date_range_exceeds_three_days:
        # Write date-wise data
        for date, counts in sorted_dates.items():
            sheet.write(row_index, 0, date.strftime("%Y-%m-%d"), border_style)
            col_index = 1
            if type_presence['PA']:
                sheet.write(row_index, col_index, counts['PA'], border_style)
                total_counts['PA'] += counts['PA']
                col_index += 1
            if type_presence['NPA']:
                sheet.write(row_index, col_index, counts['NPA'], border_style)
                total_counts['NPA'] += counts['NPA']
            row_index += 1
    else:
        # Write timestamp-wise data
        for timestamp, counts in sorted_timestamps.items():
            sheet.write(row_index, 0, timestamp.strftime("%Y-%m-%d %H:%M:%S"), border_style)
            col_index = 1
            if type_presence['PA']:
                sheet.write(row_index, col_index, counts['PA'], border_style)
                total_counts['PA'] += counts['PA']
                col_index += 1
            if type_presence['NPA']:
                sheet.write(row_index, col_index, counts['NPA'], border_style)
                total_counts['NPA'] += counts['NPA']
            row_index += 1

    # Write total counts at the bottom
    total_row_index = row_index + 1
    sheet.write(total_row_index, 0, "Total Violations:", header_font)
    col_index = 1
    if type_presence['PA']:
        sheet.write(total_row_index, col_index, total_counts['PA'], border_style)
        col_index += 1
    if type_presence['NPA']:
        sheet.write(total_row_index, col_index, total_counts['NPA'], border_style)

    # Create the chart
    chart = workbook.add_chart({'type': 'column'})
    if type_presence['PA'] and not type_presence['NPA']:
        chart_title = f"{title or sheet_name} | PA Total: {total_counts['PA']}"
    elif type_presence['NPA'] and not type_presence['PA']:
        chart_title = f"{title or sheet_name} | NPA Total: {total_counts['NPA']}"
    else:
        chart_title = f"{title or sheet_name} | PA Total Counts: {total_counts['PA']}, NPA Total Counts: {total_counts['NPA']}"

    chart.set_title({'name': chart_title})
    chart.set_x_axis({'name': 'Date' if date_range_exceeds_three_days else 'Violation Time'})
    chart.set_y_axis({'name': 'Violation Count'})
    chart.set_size({'width': 1100, 'height': 700})

    # Set the ranges for the chart
    categories_range = f"'{sheet_name}'!A2:A{row_index}"
    col_offset = 1
    if type_presence['PA']:
        data_range_PA = f"'{sheet_name}'!B2:B{row_index}"
        chart.add_series({
            'name': 'PA Violations',
            'categories': categories_range,
            'values': data_range_PA,
        })
        col_offset += 1
    if type_presence['NPA']:
        data_range_NPA = f"'{sheet_name}'!{chr(65 + col_offset)}2:{chr(65 + col_offset)}{row_index}"
        chart.add_series({
            'name': 'NPA Violations',
            'categories': categories_range,
            'values': data_range_NPA,
        })

    # Insert the chart into the sheet
    sheet.insert_chart('E2', chart)
    sheet.set_column(0, 0, 20)  # Increase the width of "Timestamp" or "Date" to 20 units
    sheet.set_column(1, 1, 10)  # Adjust the width of the next columns as needed
    sheet.set_column(2, 2, 10)  # Adjust the width of the next columns as needed




def VPMScreatecamerawisechart(workbook, FINALNewarray, from_date, to_date, title="Camera-wise Violation Chart"):
    violations_by_camera = defaultdict(int)

    # Count violations by camera
    for record in FINALNewarray:
        camera_name = record.get("camera_name", "Unknown Camera")
        violations_by_camera[camera_name] += 1

    # Create a worksheet and add chart data
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        # Headers
        sheet.write(0, 0, "Camera", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        # Populate data
        row_index = 1
        for camera, count in violations_by_camera.items():
            sheet.write(row_index, 0, camera)
            sheet.write(row_index, 1, count)
            row_index += 1

        # Add the column chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': "Violation Counts",
            'categories': f"'{sheet_name}'!A2:A{row_index}",
            'values': f"'{sheet_name}'!B2:B{row_index}",
            'data_labels': {'value': True}
        })
        chart.set_title({
            'name': f'Camera-wise Violation Counts\n({from_date} to {to_date})'
        })
        chart.set_x_axis({'name': 'Camera'})
        chart.set_y_axis({'name': 'Violation Count'})
        chart.set_size({'width': 1200, 'height': 600})  # Adjusted size

    
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)

def VPMScreatedepartmentwisechart(workbook,FINALNewarray, from_date, to_date, title="Department-wise Violation Chart"):
    violations_by_department = defaultdict(int)

    # Count violations by department
    for record in FINALNewarray:
        department = (
            record.get("department") or
            (record.get("camera_info", {}).get("department")) or
            "Unknown Department"
        )
        violations_by_department[department] += 1

    # Create a worksheet and add chart data
    sheet_name = title
    if sheet_name not in [sheet.get_name() for sheet in workbook.worksheets_objs]:
        sheet = workbook.add_worksheet(sheet_name)

        # Headers
        sheet.write(0, 0, "Department", workbook.add_format({'bold': True}))
        sheet.write(0, 1, "Violation Count", workbook.add_format({'bold': True}))

        # Populate data
        row_index = 1
        for department, count in violations_by_department.items():
            sheet.write(row_index, 0, department)
            sheet.write(row_index, 1, count)
            row_index += 1

        # Add the column chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': "Violation Counts",
            'categories': f"'{sheet_name}'!A2:A{row_index}",
            'values': f"'{sheet_name}'!B2:B{row_index}",
            'data_labels': {'value': True}
        })
        chart.set_title({
            'name': f'Department-wise Violation Counts\n({from_date} to {to_date})'
        })
        chart.set_x_axis({'name': 'Department'})
        chart.set_y_axis({'name': 'Violation Count'})
        chart.set_size({'width': 1200, 'height': 600})  # Adjusted size

        # Insert the chart in the sheet
        sheet.insert_chart('D2', chart)
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 15)





       
       
def create_excel_workbook():
    now = datetime.now()
    excel_sheet_name = f'Violation_report_{now.strftime("%m-%d-%Y-%H-%M-%S")}.xlsx'
    filename = os.path.join(os.getcwd(), 'VPMS_violation_excel_sheets', excel_sheet_name)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Violation Data')
    
   
    worksheet.set_column('A:A', 46)  # image Name
    worksheet.set_column('B:B', 30)#roiname
    worksheet.set_column('C:C', 30)  # Camera Name
    worksheet.set_column('D:D', 30)  # Violation Type
    worksheet.set_column('E:E', 30)  # Detected Time
    worksheet.set_column('F:F', 30)  # Ended Time
    worksheet.set_column('G:G', 60) #message
    worksheet.set_column('H:H', 30) #cameraname
    worksheet.set_row(0, 100)
    worksheet.set_row(1, 20)
    worksheet.insert_image('A1', os.path.join(os.getcwd(), 'smaple_files/DocketRun_logo.png'), {'x_scale': 0.07, 'y_scale': 0.07})
    
    # Write header information
    cell_format = workbook.add_format({'bold': True, 'font_color': 'navy', 'font_name': 'Calibri', 'font_size': 20, 'align': 'center_across'})
    worksheet.write('B1', 'Violation Data', cell_format)
    worksheet.merge_range('B1:F1', 'Violation Details', cell_format)
    
    return workbook, worksheet, filename






def fill_excel_with_data(worksheet, workbook, FINALNewarray,from_date,to_date):
    header_format = workbook.add_format({
        'bold': True, 'font_color': 'white', 'font_name': 'Calibri', 
        'font_size': 18, 'align': 'center_across', 'bg_color': '#333300'
    })

   
    headers = ['Image', 'Department Name','ROI_Name', 'Violation Type', 'Entry Time', 'Exit Time', 'Message', 'Camera Name']
    for col, header in enumerate(headers):
        worksheet.write(1, col, header, header_format)

    data_format = workbook.add_format({'font_name': 'Calibri', 'align': 'center_across'})
    row = 2

   
    for record in FINALNewarray:
        department = record.get('department', 'N/A')
        camera_name = record.get('camera_name', 'N/A')
        for log in record.get('analytics_log', []):
            violation_type = log.get('type', 'N/A')
            entry_time = log.get('entry_time', 'N/A')
            exit_time = log.get('exit_time', 'N/A')
            ROI_Name = record.get('roi_name')
            
            for detail in log.get('details', []):
                image_name = detail.get('image_name')
                message = detail.get('message', 'N/A')

                if image_name:
                    if violation_type == "PA":
                        img_byte_arr = get_bbox_image(image_name, roiname=record.get('roi_name'))
                    elif violation_type == "NPA":
                        img_byte_arr = NPA_bbox_image(image_name, roiname=record.get('roi_name'))
                    else:
                        img_byte_arr = None
                    
                    if img_byte_arr:
                        worksheet.set_row(row, 120)
                        worksheet.insert_image(row, 0, 'image.jpg', {'image_data': img_byte_arr, 'x_scale': 0.13, 'y_scale': 0.11})

                worksheet.write(row, 1, department, data_format)
                worksheet.write(row, 2, ROI_Name, data_format)
                worksheet.write(row, 3, violation_type, data_format)
                worksheet.write(row, 4, entry_time, data_format)
                worksheet.write(row, 5, exit_time, data_format)
                worksheet.write(row, 6, message, data_format)
                worksheet.write(row, 7, camera_name, data_format)
                row += 1
    for log in record.get('analytics_log', []):
        violation_types = log.get('type', 'N/A')
    VPMScreate_chart(workbook, from_date, to_date, violation_types, FINALNewarray, title="Violations Chart")
    VPMScreatecamerawisechart(workbook, FINALNewarray,from_date,to_date)
    VPMScreatedepartmentwisechart(workbook, FINALNewarray,from_date,to_date)

    return worksheet

def get_bbox_image(image_file,roiname =None):
    #print("image_file1111111111111111111111111111111",image_file)
    boundingboxdetails =  {
     "object_thickness": 5,
    "roi_thickness": 5,
    "object_font_size": 12,
    "roi_font_size": 50,
    "roi": "#fa0707",
    "person": "#ff0015",
    "helmet": "#ff0000",
    "vest": "#FFFF00",
    "fsd": "#5ce65c",
    "bicycle": "#ff4de6",
    "motorcycle": "#ffa800",
    "car": "#8b00ff",
    "bus": "#808000",
    "truck": "#f08080",
    "biker": "#ff0000"
  }
    if "rtsp_flag" in mongo.db.list_collection_names():
        finddataboxdata = mongo.db.rtsp_flag.find_one()
        if finddataboxdata is not None:
            if 'bb_box_settings' in finddataboxdata:
                if finddataboxdata['bb_box_settings'] is not None:
                    boundingboxdetails = finddataboxdata['bb_box_settings']

    else:
        print("Collection 'rtsp_flag' does not exist")
    helmetboxcolor= boundingboxdetails['helmet']    
    vestboxcolor= boundingboxdetails['vest']
    personboxcolor= boundingboxdetails['person']
    fsdboxcolor= boundingboxdetails['fsd']
    bicycleboxcolor= boundingboxdetails['bicycle']
    motorcycleboxcolor= boundingboxdetails['motorcycle']
    carboxcolor= boundingboxdetails['car']
    busboxcolor= boundingboxdetails['bus']
    truckboxcolor= boundingboxdetails['truck']
    bikerboxcolor= boundingboxdetails['biker']
    objectfont_size= boundingboxdetails['object_font_size']
    Objectbbox_thickness= boundingboxdetails['object_thickness']
    ROIbboxthickness= boundingboxdetails['roi_thickness']
    roiboxcolor= boundingboxdetails['roi']
    roifont_size = boundingboxdetails['roi_font_size']  
    if roiname is not None :
        QueryMatch = {"roi_name":roiname,"analytics_log.type":"PA","analytics_log.details.image_name":image_file}
    else:
        QueryMatch = {"analytics_log.type":"PA","analytics_log.details.image_name":image_file}
    image_data= VEHICLE_PARKING_MANAGEMENT_DATA.find_one(
    QueryMatch,
    sort=[('_id', -1)])
    if image_data is not None:
        base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
        CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
        if file_exists(CHECKIMAGE): 
            file_path = os.path.join(base_path, image_file)
            source_img = Image.open(file_path) 
            draw = ImageDraw.Draw(source_img) 
            IMage_widthscal = source_img.width
            IMage_heigthscal = source_img.height  
            image_data_func,IsvoilationTrue = VPMSimage_roi_draw_data(image_data["analytics_log"],image_file)
            if len(image_data_func) != 0:
                for imgs in image_data["analytics_log"]:
                    if len(image_data_func['obj_details']) != 0: 
                        BoundingBoxValueFORROI = imgs['roi_bbox']
                        if 'roi_bbox' in imgs:
                            if type(BoundingBoxValueFORROI) != list :
                                if BoundingBoxValueFORROI is not None:
                                    BoundingBoxValueFORROI1=BoundingBoxValueFORROI.rstrip(';')
                                    coords_list = [int(coord) for coord in BoundingBoxValueFORROI1.split(';')]
                                    IMage_widthscal = source_img.width
                                    IMage_heigthscal = source_img.height
                                    orig_width = 960
                                    orig_height = 544
                                    bbox_values = scale_polygon_1(coords_list, orig_width, orig_height, IMage_widthscal, IMage_heigthscal)
                                    coords = [(bbox_values[i], bbox_values[i+1]) for i in range(0, len(bbox_values), 2)]
                                    text_position = calculate_text_position(coords)
                                    if imgs['type']=='NPA':
                                        if imgs['status']=='Unauthorized Parking':
                                            if IsvoilationTrue :
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            else:
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                        elif imgs['status']=='free':
                                            if IsvoilationTrue :
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            else:
                                                draw.polygon(coords, outline='yellow', width=7)
                                        elif imgs['status']=='Error':
                                            if IsvoilationTrue :
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            else:
                                                draw.polygon(coords, outline='yellow', width=ROIbboxthickness)
                                    elif  imgs['type']=='PA':
                                        draw.polygon(coords, outline='#00FF00', width=ROIbboxthickness)
                                    text_width,text_height = calculate_text_size(image_data['roi_name'],roifont_size)
                                    text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + roifont_size, text_position[1] + text_height + 5)
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.text(text_position, image_data['roi_name'], font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                            else:
                                if len(BoundingBoxValueFORROI['ROI_details']) !=0 :
                                    for BoundingBoxValueFORROI in BoundingBoxValueFORROI['ROI_details']:
                                        if BoundingBoxValueFORROI is not None:
                                            BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                            if BBOXVALUE is not None:
                                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                draw.polygon(bbox_values, outline='red', width=ROIbboxthickness)
                                                keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                if keys_list is None and keys_list=='':
                                                    keys_list='Region of interest'
                                                draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))
                                   
                        for ___, thiru in enumerate(image_data_func['obj_details']):
                            height = thiru['H'] #height = thiru['bbox']['H']
                            width = thiru['W'] #width = thiru['bbox']['W']
                            x_value = thiru['X'] #x_value = thiru['bbox']['X']
                            y_value = thiru['Y'] #y_value = thiru['bbox']['Y']
                            w, h = width, height 
                            shape = [(x_value, y_value), (w - 10, h - 10)]
                            text_width,text_height = calculate_text_size(thiru['name'],objectfont_size)
                            text_position = (x_value + 6, y_value + 2)
                            text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + 10, text_position[1] + text_height )
                            # draw.rectangle(text_bg_position, fill='black')
                            draw.rectangle(text_bg_position, fill='black')
                            if thiru['name']=='truck':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='car':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='motorcycle' or  thiru['name']=='motorbike':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='bus':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='bicycle':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            
                        imgByteArr = io.BytesIO()
                        source_img.save(imgByteArr, format='JPEG')
                        # print("imgByteArr33333333333333333333333333333",imgByteArr)
                        # print("source_img55555555555555555555555",source_img)
                        imgByteArr.seek(0)
                        return imgByteArr
                    
                    else:
                        not_found_path = os.path.join(os.getcwd(), "smaple_files", "NOT_FOUND_IMAGE.png")
                        with Image.open(not_found_path) as not_found_img:
                            imgByteArr = io.BytesIO()
                            not_found_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return imgByteArr
        else:
            not_found_path = os.path.join(os.getcwd(), "smaple_files", "NOT_FOUND_IMAGE.png")
            with Image.open(not_found_path) as not_found_img:
                imgByteArr = io.BytesIO()
                not_found_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                return imgByteArr
    else:
        not_found_path = os.path.join(os.getcwd(), "smaple_files", "NOT_FOUND_IMAGE.png")
        with Image.open(not_found_path) as not_found_img:
            imgByteArr = io.BytesIO()
            not_found_img.save(imgByteArr, format='JPEG')
            imgByteArr.seek(0)
            return imgByteArr
        


def NPA_bbox_image(image_file,roiname =None):
    boundingboxdetails =  {
     "object_thickness": 5,
    "roi_thickness": 5,
    "object_font_size": 12,
    "roi_font_size": 50,
    "roi": "#fa0707",
    "person": "#ff0015",
    "helmet": "#ff0000",
    "vest": "#FFFF00",
    "fsd": "#5ce65c",
    "bicycle": "#ff4de6",
    "motorcycle": "#ffa800",
    "car": "#8b00ff",
    "bus": "#808000",
    "truck": "#f08080",
    "biker": "#ff0000"
  }
    if "rtsp_flag" in mongo.db.list_collection_names():
        finddataboxdata = mongo.db.rtsp_flag.find_one()
        if finddataboxdata is not None:
            if 'bb_box_settings' in finddataboxdata:
                if finddataboxdata['bb_box_settings'] is not None:
                    boundingboxdetails = finddataboxdata['bb_box_settings']

    else:
        print("Collection 'rtsp_flag' does not exist")
    helmetboxcolor= boundingboxdetails['helmet']    
    vestboxcolor= boundingboxdetails['vest']
    personboxcolor= boundingboxdetails['person']
    fsdboxcolor= boundingboxdetails['fsd']
    bicycleboxcolor= boundingboxdetails['bicycle']
    motorcycleboxcolor= boundingboxdetails['motorcycle']
    carboxcolor= boundingboxdetails['car']
    busboxcolor= boundingboxdetails['bus']
    truckboxcolor= boundingboxdetails['truck']
    bikerboxcolor= boundingboxdetails['biker']
    objectfont_size= boundingboxdetails['object_font_size']
    Objectbbox_thickness= boundingboxdetails['object_thickness']
    ROIbboxthickness= boundingboxdetails['roi_thickness']
    roiboxcolor= boundingboxdetails['roi']
    roifont_size = boundingboxdetails['roi_font_size']  
    QueryMatch ={}
    if roiname is not None:
        QueryMatch = {"roi_name":roiname,"analytics_log.type":"NPA","analytics_log.details.image_name":image_file}
    else:
        QueryMatch = {"analytics_log.type":"NPA","analytics_log.details.image_name":image_file}
    image_data= VEHICLE_PARKING_MANAGEMENT_DATA.find_one(
    QueryMatch,
    sort=[('_id', -1)]
)
    # image_data = VEHICLE_PARKING_MANAGEMENT_DATA.find_one({"analytics_log.details.image_name": image_file})
    # print("IMAGE DATA:-----------------", image_data)  #["analytics_log"])
    if image_data is not None:
        base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
        # print("BASEPATH:---------------", base_path)
        CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
        if file_exists(CHECKIMAGE): 
            # print("EXISTED----------------------------------------")
            file_path = os.path.join(base_path, image_file)
            source_img = Image.open(file_path) 
            draw = ImageDraw.Draw(source_img) 
            IMage_widthscal = source_img.width
            IMage_heigthscal = source_img.height  
            # print("IMAGE DATAAAAAAAAAAAAAAAAAAAAAAA:-------------", image_data["analytics_log"])
            image_data_func,IsvoilationTrue = VPMSimage_roi_draw_data(image_data["analytics_log"],image_file)
            # print("IMAGE DATA:--------------------222222222222222222222-------",image_data_func,)
            # if image_data['analyticstype']=="VPMS":
            if len(image_data_func) != 0:
                for imgs in image_data["analytics_log"]:
                    # print("====================image_data-RA=====",imgs) #["obj_details"], imgs["details"][0]["obj_details"])
                    if len(image_data_func['obj_details']) != 0: 
                        BoundingBoxValueFORROI = imgs['roi_bbox']
                        # print("********************11111111111111111********************", imgs['roi_bbox'])
                        # print("--------------image_data--------------ROIName-----",image_data['roi_name'])
                        
                        if 'roi_bbox' in imgs:
                            if type(BoundingBoxValueFORROI) != list : #['ROI_details']) != list :
                                # print("********************22222222222********************")
                                # for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                if BoundingBoxValueFORROI is not None:
                                    BoundingBoxValueFORROI1=BoundingBoxValueFORROI.rstrip(';')
                                    coords_list = [int(coord) for coord in BoundingBoxValueFORROI1.split(';')]
                                    IMage_widthscal = source_img.width
                                    IMage_heigthscal = source_img.height
                                    orig_width = 960
                                    orig_height = 544
                                    bbox_values = scale_polygon_1(coords_list, orig_width, orig_height, IMage_widthscal, IMage_heigthscal)
                                    coords = [(bbox_values[i], bbox_values[i+1]) for i in range(0, len(bbox_values), 2)]
                                    text_position = calculate_text_position(coords)
                                    # file_path = "/home/docketrun/Documents/images/frame/Docketrun_1_Test1_4886_20240603_123010.jpg"  # Replace with the path to your image file
                                    if imgs['type']=='NPA':
                                        if imgs['status']=='Unauthorized Parking':
                                            if IsvoilationTrue :
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            else:
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                        elif imgs['status']=='free':
                                            if IsvoilationTrue :
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            else:
                                                draw.polygon(coords, outline='yellow', width=ROIbboxthickness)
                                            #draw.polygon(coords, outline='red', width=7)
                                        elif imgs['status']=='Error':
                                            if IsvoilationTrue :
                                                draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            else:
                                                draw.polygon(coords, outline='yellow', width=ROIbboxthickness)
                                            #draw.polygon(coords, outline='red', width=7)
                                    elif  imgs['type']=='PA':
                                        draw.polygon(coords, outline='#00FF00', width=7)
                                        
                                    text_width,text_height = calculate_text_size(image_data['roi_name'],roifont_size)
                                    text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + roifont_size, text_position[1] + text_height + 5)
                                    draw.rectangle(text_bg_position, fill='black')
                                    draw.text(text_position, image_data['roi_name'], font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")

                                    # draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))

                            else:
                                # print("********************33333333333333********************")
                                if len(BoundingBoxValueFORROI['ROI_details']) !=0 :
                                    for BoundingBoxValueFORROI in BoundingBoxValueFORROI['ROI_details']:
                                        if BoundingBoxValueFORROI is not None:
                                            BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                            if BBOXVALUE is not None:
                                                polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                draw.polygon(bbox_values, outline='red', width=ROIbboxthickness)
                                                keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                if keys_list is None and keys_list=='':
                                                    keys_list='Region of interest'
                                                draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))
                                        
                        # print("image_data_funcimage_data_funcimage_data_func", image_data_func)
                        for ___, thiru in enumerate(image_data_func['obj_details']):
                            # print("********************44444444444444444********************")
                            height = thiru['H'] #height = thiru['bbox']['H']
                            width = thiru['W'] #width = thiru['bbox']['W']
                            x_value = thiru['X'] #x_value = thiru['bbox']['X']
                            y_value = thiru['Y'] #y_value = thiru['bbox']['Y']
                            w, h = width, height 
                            shape = [(x_value, y_value), (w - 10, h - 10)]
                            text_width,text_height = calculate_text_size(thiru['name'],objectfont_size)
                            text_position = (x_value + 6, y_value + 2)
                            text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + 10, text_position[1] + text_height )
                            # draw.rectangle(text_bg_position, fill='black')
                            draw.rectangle(text_bg_position, fill='black')
                            if thiru['name']=='truck':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='car':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='motorcycle' or  thiru['name']=='motorbike':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='bus':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            elif thiru['name']=='bicycle':
                                if thiru['violation'] == 1:
                                    draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                else:
                                    draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                            
                            
                          
                            
                        imgByteArr = io.BytesIO()
                        source_img.save(imgByteArr, format='JPEG')
                        imgByteArr.seek(0)
                        return imgByteArr
                    
                    else:
                        not_found_path = os.path.join(os.getcwd(), "smaple_files", "NOT_FOUND_IMAGE.png")
                        with Image.open(not_found_path) as not_found_img:
                            imgByteArr = io.BytesIO()
                            not_found_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            return imgByteArr
            

        else:
          
            not_found_path = os.path.join(os.getcwd(), "smaple_files", "NOT_FOUND_IMAGE.png")
            with Image.open(not_found_path) as not_found_img:
                imgByteArr = io.BytesIO()
                not_found_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                return imgByteArr
    else:
        not_found_path = os.path.join(os.getcwd(), "smaple_files", "NOT_FOUND_IMAGE.png")
        with Image.open(not_found_path) as not_found_img:
            imgByteArr = io.BytesIO()
            not_found_img.save(imgByteArr, format='JPEG')
            imgByteArr.seek(0)
            return imgByteArr
        


    
############################################################################################################################



# Function to scale polygon points
def scale_polygon_1(polygon, orig_width, orig_height, new_width, new_height):
    scaled_polygon = []
    for i in range(0, len(polygon), 2):
        x = polygon[i] * new_width / orig_width
        y = polygon[i + 1] * new_height / orig_height
        scaled_polygon.extend([x, y])
    return scaled_polygon


def calculate_text_position(coords):
    min_x = min(coords, key=lambda p: p[0])[0]
    min_y = min(coords, key=lambda p: p[1])[1]
    max_x = max(coords, key=lambda p: p[0])[0]
    max_y = max(coords, key=lambda p: p[1])[1]
    centroid_x = (min_x + max_x) / 2
    centroid_y = (min_y + max_y) / 2
    return (centroid_x, centroid_y)


def calculate_text_size(text, font):
    font_size = font
    text_width = font_size * len(text) // 2  # Adjust as needed for accurate width estimation
    text_height = font_size 
    return text_width, text_height




# @parking_manage_data.route('/create_violation_excelVPMS', methods=['POST'])
@csrf_exempt
def create_violation_excelVPMS(request):
    ret = {'success': False, 'message': 'Something went wrong, please try again later'}
    if request.method == 'POST':
        # jsonobject = json.loads(request.body) or {}
        if not os.path.exists('VPMS_violation_excel_sheets'):
            os.makedirs('VPMS_violation_excel_sheets')
            
        jsonobject = json.loads(request.body) 
        required_keys = ['from_date', 'to_date']
        missing_keys = [key for key in required_keys if key not in jsonobject]
        
        if missing_keys:
            ret['message'] = f"Missing keys: {', '.join(missing_keys)}. Please enter all required fields."
            return JsonResponse(ret)
        
        from_date = jsonobject['from_date']
        to_date = jsonobject['to_date']
    
        mongo_data = datewise_violation_excel(request,from_date, to_date)
        
        if mongo_data and mongo_data.get('success'):
            data_records = mongo_data.get('data', [])
            workbook, worksheet, filename = create_excel_workbook()
            worksheet = fill_excel_with_data(worksheet, workbook, data_records, from_date, to_date,)
            workbook.close()
            
            ret = {'success': True, 'message': 'Excel sheet created successfully.', 'filename': filename}
        else:
            ret['message'] = 'No data found for the specified criteria.'
        
    return JsonResponse(ret)


# @parking_manage_data.route('/VPMS_violation_excel_download', methods=['GET'])
@csrf_exempt
def VPMS_violation_excel_download(request):
    ret = {'success': False, 'message': 'Something went wrong, please try again later'}
    if request.method == 'GET':
        if 1:
        # try:
            list_of_files = glob.glob(os.path.join(os.getcwd(), "VPMS_violation_excel_sheets/*"))
            latest_file = max(list_of_files, key=os.path.getctime)
            path, filename = os.path.split(latest_file)
            if filename:
                main_path = os.path.abspath(path)
                file_path = os.path.join(main_path, filename)
    
                if os.path.exists(file_path):
                    # Open the file in binary mode and return it as an attachment
                    with open(file_path, 'rb') as f:
                        return FileResponse(f, as_attachment=True, filename=filename)
                else:
                        # If the file doesn't exist, return an error message
                    return JsonResponse({'success': False, 'message': 'File not found.'},) 
            else:
                ret= {'success': False, 'message': 'File is not found.'}
    return JsonResponse(ret)


# @parking_manage_data.route('/VPMSimage/VPMS/PA/<roiname>/<image_file>', methods=['GET'])
# @parking_manage_data.route('/VPMSimage/VPMS/PA/<image_file>', methods=['GET'])
@csrf_exempt
def get_img_bbox(request,image_file,roiname =None):
    ret = {'success': False, 'message': 'Something went wrong, please try again later'}
    if request.method == 'GET':
        boundingboxdetails =  {
        "object_thickness": 5,
        "roi_thickness": 5,
        "object_font_size": 12,
        "roi_font_size": 50,
        "roi": "#fa0707",
        "person": "#ff0015",
        "helmet": "#ff0000",
        "vest": "#FFFF00",
        "fsd": "#5ce65c",
        "bicycle": "#ff4de6",
        "motorcycle": "#ffa800",
        "car": "#8b00ff",
        "bus": "#808000",
        "truck": "#f08080",
        "biker": "#ff0000"
    }
        if "rtsp_flag" in DATABASE.list_collection_names():
            finddataboxdata = rtsp_flag.find_one()
            if finddataboxdata is not None:
                if 'bb_box_settings' in finddataboxdata:
                    if finddataboxdata['bb_box_settings'] is not None:
                        boundingboxdetails = finddataboxdata['bb_box_settings']

        else:
            print("Collection 'rtsp_flag' does not exist")
        helmetboxcolor= boundingboxdetails['helmet']    
        vestboxcolor= boundingboxdetails['vest']
        personboxcolor= boundingboxdetails['person']
        fsdboxcolor= boundingboxdetails['fsd']
        bicycleboxcolor= boundingboxdetails['bicycle']
        motorcycleboxcolor= boundingboxdetails['motorcycle']
        carboxcolor= boundingboxdetails['car']
        busboxcolor= boundingboxdetails['bus']
        truckboxcolor= boundingboxdetails['truck']
        bikerboxcolor= boundingboxdetails['biker']
        objectfont_size= boundingboxdetails['object_font_size']
        Objectbbox_thickness= boundingboxdetails['object_thickness']
        ROIbboxthickness= boundingboxdetails['roi_thickness']
        roiboxcolor= boundingboxdetails['roi']
        roifont_size = boundingboxdetails['roi_font_size']  
        if roiname is not None :
            QueryMatch = {"roi_name":roiname,"analytics_log.type":"PA","analytics_log.details.image_name":image_file}
        else:
            QueryMatch = {"analytics_log.type":"PA","analytics_log.details.image_name":image_file}
        image_data= VEHICLE_PARKING_MANAGEMENT_DATA.find_one(
        QueryMatch,
        sort=[('_id', -1)])
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
            CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
            if file_exists(CHECKIMAGE): 
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path) 
                draw = ImageDraw.Draw(source_img) 
                IMage_widthscal = source_img.width
                IMage_heigthscal = source_img.height  
                image_data_func,IsvoilationTrue = VPMSimage_roi_draw_data(image_data["analytics_log"],image_file)
                if len(image_data_func) != 0:
                    for imgs in image_data["analytics_log"]:
                        if len(image_data_func['obj_details']) != 0: 
                            BoundingBoxValueFORROI = imgs['roi_bbox']
                            if 'roi_bbox' in imgs:
                                if type(BoundingBoxValueFORROI) != list :
                                    if BoundingBoxValueFORROI is not None:
                                        BoundingBoxValueFORROI1=BoundingBoxValueFORROI.rstrip(';')
                                        coords_list = [int(coord) for coord in BoundingBoxValueFORROI1.split(';')]
                                        IMage_widthscal = source_img.width
                                        IMage_heigthscal = source_img.height
                                        orig_width = 960
                                        orig_height = 544
                                        bbox_values = scale_polygon_1(coords_list, orig_width, orig_height, IMage_widthscal, IMage_heigthscal)
                                        coords = [(bbox_values[i], bbox_values[i+1]) for i in range(0, len(bbox_values), 2)]
                                        text_position = calculate_text_position(coords)
                                        if imgs['type']=='NPA':
                                            if imgs['status']=='Unauthorized Parking':
                                                if IsvoilationTrue :
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                                else:
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            elif imgs['status']=='free':
                                                if IsvoilationTrue :
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                                else:
                                                    draw.polygon(coords, outline='yellow', width=7)
                                            elif imgs['status']=='Error':
                                                if IsvoilationTrue :
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                                else:
                                                    draw.polygon(coords, outline='yellow', width=ROIbboxthickness)
                                        elif  imgs['type']=='PA':
                                            draw.polygon(coords, outline='#00FF00', width=ROIbboxthickness)
                                        text_width,text_height = calculate_text_size(image_data['roi_name'],roifont_size)
                                        text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + roifont_size, text_position[1] + text_height + 5)
                                        draw.rectangle(text_bg_position, fill='black')
                                        draw.text(text_position, image_data['roi_name'], font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                else:
                                    if len(BoundingBoxValueFORROI['ROI_details']) !=0 :
                                        for BoundingBoxValueFORROI in BoundingBoxValueFORROI['ROI_details']:
                                            if BoundingBoxValueFORROI is not None:
                                                BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                                if BBOXVALUE is not None:
                                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                    draw.polygon(bbox_values, outline='red', width=ROIbboxthickness)
                                                    keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                    if keys_list is None and keys_list=='':
                                                        keys_list='Region of interest'
                                                    draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))
                                    
                            for ___, thiru in enumerate(image_data_func['obj_details']):
                                height = thiru['H'] #height = thiru['bbox']['H']
                                width = thiru['W'] #width = thiru['bbox']['W']
                                x_value = thiru['X'] #x_value = thiru['bbox']['X']
                                y_value = thiru['Y'] #y_value = thiru['bbox']['Y']
                                w, h = width, height 
                                shape = [(x_value, y_value), (w - 10, h - 10)]
                                text_width,text_height = calculate_text_size(thiru['name'],objectfont_size)
                                text_position = (x_value + 6, y_value + 2)
                                text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + 10, text_position[1] + text_height )
                                # draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(text_bg_position, fill='black')
                                if thiru['name']=='truck':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                    #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='car':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='motorcycle' or  thiru['name']=='motorbike':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='bus':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='bicycle':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            ret=  send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
                        
                        else:
                            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                            main_path = os.path.abspath(path)
                            file_path = os.path.join(main_path, filename)
    
                            if os.path.exists(file_path):
                                # Open the file in binary mode and return it as an attachment
                                with open(file_path, 'rb') as f:
                                    return FileResponse(f, as_attachment=True, filename=filename)
                            else:
                                # If the file doesn't exist, return an error message
                                return JsonResponse({'success': False, 'message': 'File not found.'})
            else:
                # print("NOT 1111111111111 EXISTED----------------------------------------")
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                file_path = os.path.join(main_path, filename)
    
                if os.path.exists(file_path):
                    # Open the file in binary mode and return it as an attachment
                    with open(file_path, 'rb') as f:
                        return FileResponse(f, as_attachment=True, filename=filename)
                else:
                    # If the file doesn't exist, return an error message
                    return JsonResponse({'success': False, 'message': 'File not found.'})
        else:
            # print("image_data not found-----2--------",image_file)
            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
            main_path = os.path.abspath(path)
            file_path = os.path.join(main_path, filename)
    
            if os.path.exists(file_path):
                # Open the file in binary mode and return it as an attachment
                with open(file_path, 'rb') as f:
                    return FileResponse(f, as_attachment=True, filename=filename)
            else:
                # If the file doesn't exist, return an error message
                return JsonResponse({'success': False, 'message': 'File not found.'})
        
    return JsonResponse(ret)
          



# @parking_manage_data.route('/VPMSimage/VPMS/NPA/<roiname>/<image_file>', methods=['GET'])
# @parking_manage_data.route('/VPMSimage/VPMS/NPA/<image_file>', methods=['GET'])
def NPAimage(request,image_file,roiname =None):
    ret = {'success': False, 'message': 'Something went wrong, please try again later'}
    if request.method == 'GET':
        boundingboxdetails =  {
        "object_thickness": 5,
        "roi_thickness": 5,
        "object_font_size": 12,
        "roi_font_size": 50,
        "roi": "#fa0707",
        "person": "#ff0015",
        "helmet": "#ff0000",
        "vest": "#FFFF00",
        "fsd": "#5ce65c",
        "bicycle": "#ff4de6",
        "motorcycle": "#ffa800",
        "car": "#8b00ff",
        "bus": "#808000",
        "truck": "#f08080",
        "biker": "#ff0000"
    }
        if "rtsp_flag" in DATABASE.list_collection_names():
            finddataboxdata = rtsp_flag.find_one()
            if finddataboxdata is not None:
                if 'bb_box_settings' in finddataboxdata:
                    if finddataboxdata['bb_box_settings'] is not None:
                        boundingboxdetails = finddataboxdata['bb_box_settings']

        else:
            print("Collection 'rtsp_flag' does not exist")
        helmetboxcolor= boundingboxdetails['helmet']    
        vestboxcolor= boundingboxdetails['vest']
        personboxcolor= boundingboxdetails['person']
        fsdboxcolor= boundingboxdetails['fsd']
        bicycleboxcolor= boundingboxdetails['bicycle']
        motorcycleboxcolor= boundingboxdetails['motorcycle']
        carboxcolor= boundingboxdetails['car']
        busboxcolor= boundingboxdetails['bus']
        truckboxcolor= boundingboxdetails['truck']
        bikerboxcolor= boundingboxdetails['biker']
        objectfont_size= boundingboxdetails['object_font_size']
        Objectbbox_thickness= boundingboxdetails['object_thickness']
        ROIbboxthickness= boundingboxdetails['roi_thickness']
        roiboxcolor= boundingboxdetails['roi']
        roifont_size = boundingboxdetails['roi_font_size']  
        QueryMatch ={}
        if roiname is not None:
            QueryMatch = {"roi_name":roiname,"analytics_log.type":"NPA","analytics_log.details.image_name":image_file}
        else:
            QueryMatch = {"analytics_log.type":"NPA","analytics_log.details.image_name":image_file}
        image_data= VEHICLE_PARKING_MANAGEMENT_DATA.find_one(
        QueryMatch,
        sort=[('_id', -1)]
    )
        # image_data = mongo.db.VEHICLE_PARKING_MANAGEMENT_DATA.find_one({"analytics_log.details.image_name": image_file})
        # print("IMAGE DATA:-----------------", image_data)  #["analytics_log"])
        if image_data is not None:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
            # print("BASEPATH:---------------", base_path)
            CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
            if file_exists(CHECKIMAGE): 
                # print("EXISTED----------------------------------------")
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path) 
                draw = ImageDraw.Draw(source_img) 
                IMage_widthscal = source_img.width
                IMage_heigthscal = source_img.height  
                # print("IMAGE DATAAAAAAAAAAAAAAAAAAAAAAA:-------------", image_data["analytics_log"])
                image_data_func,IsvoilationTrue = VPMSimage_roi_draw_data(image_data["analytics_log"],image_file)
                # print("IMAGE DATA:--------------------222222222222222222222-------",image_data_func,)
                # if image_data['analyticstype']=="VPMS":
                if len(image_data_func) != 0:
                    for imgs in image_data["analytics_log"]:
                        # print("====================image_data-RA=====",imgs) #["obj_details"], imgs["details"][0]["obj_details"])
                        if len(image_data_func['obj_details']) != 0: 
                            BoundingBoxValueFORROI = imgs['roi_bbox']
                            # print("********************11111111111111111********************", imgs['roi_bbox'])
                            # print("--------------image_data--------------ROIName-----",image_data['roi_name'])
                            
                            if 'roi_bbox' in imgs:
                                if type(BoundingBoxValueFORROI) != list : #['ROI_details']) != list :
                                    # print("********************22222222222********************")
                                    # for BoundingBoxValueFORROI in ROISHAPE['ROI_details']:
                                    if BoundingBoxValueFORROI is not None:
                                        BoundingBoxValueFORROI1=BoundingBoxValueFORROI.rstrip(';')
                                        coords_list = [int(coord) for coord in BoundingBoxValueFORROI1.split(';')]
                                        IMage_widthscal = source_img.width
                                        IMage_heigthscal = source_img.height
                                        orig_width = 960
                                        orig_height = 544
                                        bbox_values = scale_polygon_1(coords_list, orig_width, orig_height, IMage_widthscal, IMage_heigthscal)
                                        coords = [(bbox_values[i], bbox_values[i+1]) for i in range(0, len(bbox_values), 2)]
                                        text_position = calculate_text_position(coords)
                                        # file_path = "/home/docketrun/Documents/images/frame/Docketrun_1_Test1_4886_20240603_123010.jpg"  # Replace with the path to your image file
                                        if imgs['type']=='NPA':
                                            if imgs['status']=='Unauthorized Parking':
                                                if IsvoilationTrue :
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                                else:
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            elif imgs['status']=='free':
                                                if IsvoilationTrue :
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                                else:
                                                    draw.polygon(coords, outline='yellow', width=ROIbboxthickness)
                                                #draw.polygon(coords, outline='red', width=7)
                                            elif imgs['status']=='Error':
                                                if IsvoilationTrue :
                                                    draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                                else:
                                                    draw.polygon(coords, outline='yellow', width=ROIbboxthickness)
                                                #draw.polygon(coords, outline='red', width=7)
                                        elif  imgs['type']=='PA':
                                            draw.polygon(coords, outline='#00FF00', width=7)
                                            # if imgs['status']=='parked':
                                            #     if IsvoilationTrue :
                                            #         draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            #     else:
                                            #         draw.polygon(coords, outline='#00FF00', width=ROIbboxthickness)
                                            # elif imgs['status']=='free':
                                            #     if IsvoilationTrue :
                                            #         draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            #     else:
                                            #         draw.polygon(coords, outline='#00FF00', width=ROIbboxthickness)
                                            # elif imgs['status']=='Error':
                                            #     if IsvoilationTrue :
                                            #         draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                            #     else:
                                            #         draw.polygon(coords, outline='#00FF00', width=ROIbboxthickness)
                                                # draw.polygon(coords, outline='red', width=ROIbboxthickness)
                                        text_width,text_height = calculate_text_size(image_data['roi_name'],roifont_size)
                                        text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + roifont_size, text_position[1] + text_height + 5)
                                        draw.rectangle(text_bg_position, fill='black')
                                        draw.text(text_position, image_data['roi_name'], font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")

                                        # draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))

                                else:
                                    # print("********************33333333333333********************")
                                    if len(BoundingBoxValueFORROI['ROI_details']) !=0 :
                                        for BoundingBoxValueFORROI in BoundingBoxValueFORROI['ROI_details']:
                                            if BoundingBoxValueFORROI is not None:
                                                BBOXVALUE = BoundingBoxValueFORROI['roi_bbox']
                                                if BBOXVALUE is not None:
                                                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                                                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                                                    draw.polygon(bbox_values, outline='red', width=ROIbboxthickness)
                                                    keys_list = BoundingBoxValueFORROI['roi_name']#list(BoundingBoxValueFORROI.keys())
                                                    if keys_list is None and keys_list=='':
                                                        keys_list='Region of interest'
                                                    draw.text((bbox_values[0][0] , bbox_values[0][1] ), str(keys_list), 'red', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'))
                                            
                            # print("image_data_funcimage_data_funcimage_data_func", image_data_func)
                            for ___, thiru in enumerate(image_data_func['obj_details']):
                                # print("********************44444444444444444********************")
                                height = thiru['H'] #height = thiru['bbox']['H']
                                width = thiru['W'] #width = thiru['bbox']['W']
                                x_value = thiru['X'] #x_value = thiru['bbox']['X']
                                y_value = thiru['Y'] #y_value = thiru['bbox']['Y']
                                w, h = width, height 
                                shape = [(x_value, y_value), (w - 10, h - 10)]
                                text_width,text_height = calculate_text_size(thiru['name'],objectfont_size)
                                text_position = (x_value + 6, y_value + 2)
                                text_bg_position = (text_position[0] - 5, text_position[1] - 5, text_position[0] + text_width + 10, text_position[1] + text_height )
                                # draw.rectangle(text_bg_position, fill='black')
                                draw.rectangle(text_bg_position, fill='black')
                                if thiru['name']=='truck':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=truckboxcolor, width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                    #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='car':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=carboxcolor, width=Objectbbox_thickness)#Electric Purple
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='motorcycle' or  thiru['name']=='motorbike':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=motorcycleboxcolor, width=Objectbbox_thickness)#Dark Orange
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='bus':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=busboxcolor, width=Objectbbox_thickness)#Olive
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                elif thiru['name']=='bicycle':
                                    if thiru['violation'] == 1:
                                        draw.rectangle(shape, outline='red', width=Objectbbox_thickness)
                                    else:
                                        draw.rectangle(shape, outline=bicycleboxcolor, width=Objectbbox_thickness)#Hot Pink
                                    draw.text((x_value + 6, y_value + 2), str(thiru['name']), 'white', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                                
                                #backend color combination ====
                                # draw.text(text_position, image_data['roi_name'], font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")
                                # if thiru['name']=='truck':
                                #     draw.rectangle(shape, outline='#f08080', width=Objectbbox_thickness)#Light Coral#'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf' 
                                #     #/usr/share/fonts/truetype/freefont/FreeMono.ttf
                                #     draw.text((x_value + 6, y_value + 2), str(thiru['name']), '#f08080', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # elif thiru['name']=='car':
                                #     draw.rectangle(shape, outline='#8b00ff', width=Objectbbox_thickness)#Electric Purple
                                #     draw.text((x_value + 6, y_value + 2), str(thiru['name']), '#8b00ff', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # elif thiru['name']=='motorcycle' or  thiru['name']=='motorbike':
                                #     draw.rectangle(shape, outline='#ffa800', width=Objectbbox_thickness)#Dark Orange
                                #     draw.text((x_value + 6, y_value + 2), str(thiru['name']), '#ffa800', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # elif thiru['name']=='bus':
                                #     draw.rectangle(shape, outline='#808000', width=Objectbbox_thickness)#Olive
                                #     draw.text((x_value + 6, y_value + 2), str(thiru['name']), '#808000', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                # elif thiru['name']=='bicycle':
                                #     draw.rectangle(shape, outline='#ff4de6', width=Objectbbox_thickness)#Hot Pink
                                #     draw.text((x_value + 6, y_value + 2), str(thiru['name']), '#ff4de6', font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',objectfont_size, encoding='unic'))
                                
                            imgByteArr = io.BytesIO()
                            source_img.save(imgByteArr, format='JPEG')
                            imgByteArr.seek(0)
                            ret=  send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
                        
                        else:
                            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                            main_path = os.path.abspath(path)
                            file_path = os.path.join(main_path, filename)
    
                            if os.path.exists(file_path):
                                # Open the file in binary mode and return it as an attachment
                                with open(file_path, 'rb') as f:
                                    return FileResponse(f, as_attachment=True, filename=filename)
                            else:
                                # If the file doesn't exist, return an error message
                                return JsonResponse({'success': False, 'message': 'File not found.'})
                
                # else:

            else:
                # print("NOT 1111111111111 EXISTED----------------------------------------")
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                file_path = os.path.join(main_path, filename)
    
                if os.path.exists(file_path):
                    # Open the file in binary mode and return it as an attachment
                    with open(file_path, 'rb') as f:
                        return FileResponse(f, as_attachment=True, filename=filename)
                else:
                    # If the file doesn't exist, return an error message
                    return JsonResponse({'success': False, 'message': 'File not found.'})
        else:
            # print("image_data not found-----2--------",image_file)
            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
            main_path = os.path.abspath(path)
            file_path = os.path.join(main_path, filename)
    
            if os.path.exists(file_path):
                # Open the file in binary mode and return it as an attachment
                with open(file_path, 'rb') as f:
                    return FileResponse(f, as_attachment=True, filename=filename)
            else:
                # If the file doesn't exist, return an error message
                return JsonResponse({'success': False, 'message': 'File not found.'})
        # else:
        #     print("image_data not found--------1-----",image_file)
        #     path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        #     main_path = os.path.abspath(path)
        #     return send_from_directory(main_path, filename)
    return JsonResponse(ret)   

