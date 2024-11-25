# from django.shortcuts import render
# from django.http import HttpResponse,JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import *
# from Data_Recieving.packages import *
# from Data_Recieving.database import *

# # Create your views here.

# #methods=['GET']
# @csrf_exempt # helps get the csrf token for the session
# def license_count(request):
#     if request.method =='GET':#checks the Valid method
        
#         Return = {'total_license':0,'added_cameras_count':0,'remaining_license':0}
#         if 1:
#             try:
#                 ret = {'message': 'something went wrong with get license_count', 'success': False}
#                 sheet_data = Mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
#                 sheet_camera_count = 0
#                 # print('sheet_data',sheet_data)
#                 if sheet_data is not None:
#                     sheet_data_count = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
#                     #mongo.db.panel_data.count_documents({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']})
#                     unique_iplist = []
#                     if len(sheet_data_count) !=0:
#                         for kl , eachElements in enumerate(sheet_data_count):
#                             # if isEmpty(eachElements['data']) :
#                             #     print("00098865234567888888",eachElements)
#                             if eachElements['ip_address'] not in unique_iplist:
#                                 unique_iplist.append(eachElements['ip_address'])
#                         sheet_camera_count= len(unique_iplist) 
                    
#                 CamCount = mongo.db.ppera_cameras.count_documents({})#find()#find_one()#mongo.db.ppera_cameras.find({}).count()
#                 # print("camera -count ",CamCount)
#                 # print("sheet_data count",sheet_camera_count)
#                 # CamCount = CamCount #+ sheet_camera_count
#                 Total_license = NEWLICENSECOUNT() 
#                 print("type -------------sheet_camera_count",sheet_camera_count)
#                 print("count --------------type ==",type(sheet_camera_count))
#                 Return = {'total_license':Total_license,'added_cameras_count':CamCount+sheet_camera_count,'remaining_license':Total_license-(CamCount+sheet_camera_count)}
#                 ret['message']=Return
#                 ret['success']=True
#             except Exception as error:
#                 ret['message'] = str(error)
#             #     ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- check_licedsdnse_of_camera 4", str(error), " ----time ---- ", now_time_with_time()]))
            
#     #Returns the respose in Json  formate   
#             return JsonResponse({'Message':ret})
#     else:
#         return JsonResponse({'Message':"Method is not Allowed","success":False})
    


# # @dashboard.route('/delete_job_sheet/<id>', methods=['GET'])
# @csrf_exempt
# def delete_job_sheet(request,id=None):
#     if request.method == "GET":
#         ret = {'success': False, 'message':'Something went wrong, please try again later'}
#         try: 
#             if id is not None:
#                 find_result= mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)})
#                 if find_result is not None:
#                     result = mongo.db.job_sheet_details.delete_one({'_id': ObjectId(find_result['_id'])})
#                     if result.deleted_count > 0:
#                         ret = {'message': 'job sheet  deleted successfully.','success': True}
#                     else:
#                         ret['message'] ='job sheet is not deleted.'
#                 else:
#                     ret['message'] = 'job sheet is not found for this mongoid.'
#             else:
#                 ret['message']= 'mongoid should not be none.'  
#         except ( 
#                 pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#                 pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#                 pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#                 pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#                 pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#                 pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#                 pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#                 pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#                 pymongo.errors.WriteError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 1", str(error), " ----time ---- ", now_time_with_time()]))   
#             ret['message'] =" ".join(["something error has occered in api", str(error)])      
#             if restart_mongodb_r_service():
#                 print("mongodb restarted")
#             else:
#                 if forcerestart_mongodb_r_service():
#                     print("mongodb service force restarted-")
#                 else:
#                     print("mongodb service is not yet started.")               
#         except Exception as  error:
#             ret = {'success': False, 'message': str(error)}
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_mechanical_job 2", str(error), " ----time ---- ", now_time_with_time()]))         
#         return JsonResponse(ret)
#     else:
#         return JsonResponse({'Message':"Method is not Allowed","success":False})
    
#     # @dashboard.route('/create_esi_multiconfig', methods=['GET'])
# @csrf_exempt
# def ESICREAeeTECONFIG1121(request):
#     if request.method == "GET":
#         ret = {'message': 'something went wrong with create config.', 'success': False}
#         if 1:
#             esi_app_set_ESI_monitoring_started(True)
#             return_data = ESINEWCAMERAIDupdatenew()
#             # HYDRACREATECONFIG()
#             if return_data:
#                 # stop_application_for_esi_creating_config()
#                 if return_data['success'] == True:
#                     esi_app_set_ESI_monitoring_started(False)
#                     ret = {'message':'esi config files are created successfully.', 'success': True}
#                 else:
#                     ret['message' ] = 'something went wrong  creating config files.'
#             else:
#                 ret['message'] = ' feeder data not found to create config files.'
#         else:
#             ret = ret
#         return JsonResponse(ret)
#     else:
#         return JsonResponse({'Message':"Method is not Allowed","success":False})
    
# # @dashboard.route('/stop_app_common', methods=['GET'])
# @csrf_exempt
# def stop_application_1_app_common(request):
#     if request.method=="GET":
#         ret = {'message': 'something went wrong with create config.', 'success': False}
#         if 1:
#             app_set_common_monitoring_started(True)
#             createHOOTERMETAJSONSTOP()
#             UpdateHooterAcknowldgementstatus()

#             ret = {'message': 'application stopped.', 'success': True}
#         else:
#             ret = ret
#         return JsonResponse(ret)
#     else:
#         return JsonResponse({'Message':"Method is not Allowed","success":False})
    
# # @dashboard.route('/stop_app_esi', methods=['GET'])
# @csrf_exempt
# def stop_application_1_app_esi(request):
#     if request.method == 'GET':
#         ret = {'message': 'something went wrong with create config.', 'success':  False}
#         if 1:
#             esi_app_set_ESI_monitoring_started(True)
#             reset_tsk_riro_table_dataupload_12_to_13()
#             reset_mag_flash_table_dataupload_to_25()
#             ret = {'message': 'application stopped.', 'success': True}
#         else:
#             ret = ret
#         return JsonResponse(ret)
#     else:
#         return JsonResponse({'Message':"Method is not Allowed","success":False})


# # @dashboard.route('/reset_jobsheet', methods=['GET'])
# @csrf_exempt
# def RESETJOB_SHEET(request):
#     if request.method == "GET":
#         ret = {'success': False, 'message':'something went wrong with reset_jobsheet api'}
#         try:
#             sheet_data = list(mongo.db.job_sheet_details.find({'status': 1}, sort=[('_id', pymongo.DESCENDING)]))
#             if len(sheet_data) != 0:
#                 think = 0
#                 app_run_response = esi_app_set_ESI_monitoring_started(True)
#                 for im, simin in enumerate(sheet_data):
#                     filters = {'_id': ObjectId(simin['_id'])}
#                     newvalues = {'$set':{'status': 0,'reset_time':now_time_with_time()}}
#                     result = mongo.db.job_sheet_details.update_one(filters, newvalues)
#                     if result.modified_count > 0:
#                         think += 1
#                 if think > 0:
#                     ret = {'message':'job sheet status reset successfully , please try to upload new job sheet.', 'success': True}
#                 else:
#                     ret['message'] = 'job sheet status not reset, please try again.'
#             else:
#                 ret['message'] = 'job sheet status not reset, please try again.'
#         except ( 
#             pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#             pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#             pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#             pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#             pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#             pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#             pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#             pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#             pymongo.errors.WriteError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- reset_jobsheet 1", str(error), " ----time ---- ", now_time_with_time()]))
#             ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
#             if restart_mongodb_r_service():
#                 print("mongodb restarted")
#             else:
#                 if forcerestart_mongodb_r_service():
#                     print("mongodb service force restarted-")
#                 else:
#                     print("mongodb service is not yet started.") 
#         except Exception as  error:
#             ret['message']=" ".join(["something error has occered in api", str(error)])
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- reset_jobsheet 2", str(error), " ----time ---- ", now_time_with_time()]))
#         return JsonResponse(ret)
#     else:
#         return JsonResponse({'Message':"Method is not Allowed","success":False})


# # @dashboard.route('/sheet_ipaddress', methods=['GET'])
# # @dashboard.route('/sheet_ipaddress', methods=['POST'])
# @csrf_exempt
# def sheet_ipaddress(request):
#     ret = {'success': False, 'message':'something went wrong with get  details api'}
#     sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)]) #None
#     if request.method == 'GET':
#         if sheet_data is not None:
#             # pass
#             match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
#             data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
#                                                         {'$group':{'_id':{'ipdata': '$data.ip_address'}, 'all_data':{'$first': '$$ROOT'}}},
#                                                         {'$limit': 4000000}]))
#             dash_data = []
#             if len(data) != 0:
#                 for count, i in enumerate(data):
#                     if isEmpty(i['all_data']['data']) :
#                         # print("----------------------",i['all_data']['type'])
#                         if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
#                             if len(i['all_data']['data']['panel_data']) !=0  :
#                                 if i['all_data']['data']['ip_address']  not in dash_data:
#                                     dash_data.append(i['all_data']['data']['ip_address'])

                        

#                         elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
#                             if 'hydraulic_data' in i['all_data']['data']:
#                                 if len(i['all_data']['data']['hydraulic_data']) !=0 :
#                                     if i['all_data']['data']['ip_address']  not in dash_data:
#                                         dash_data.append(i['all_data']['data']['ip_address'])

#                         elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
#                             if len(i['all_data']['data']['useal_data']) !=0 :
#                                 if i['all_data']['data']['ip_address']  not in dash_data:
#                                     dash_data.append(i['all_data']['data']['ip_address'])
#                 if len(dash_data) != 0:
#                     ret = {'success': True, 'message': dash_data}
#                 else:
#                     ret['message'] = 'data not found'
#             else:
#                 ret['message'] = 'data not found'
#         else:
#             ret['message'] = 'job sheet is not uploaded yet'
#     elif request.method == 'POST':
#         jsonobject = json.loads(request.body)# request.json ----------changed to ------json.loads(request.body)
#         if jsonobject == None:
#             jsonobject = {}
#         request_key_array = ['department','job_no','type']
#         jsonobjectarray = list(set(jsonobject))
#         missing_key = set(request_key_array).difference(jsonobjectarray)
#         if not missing_key:
#             output = keys_with_none_values(jsonobject) #[k for k, v in data.items() if v in ['', ' ', 'None'] ]
#             if output:
#                 print(" something missing ",output)                
#                 query = {}                               
#                 if jsonobject['type'] is not None:
#                     if jsonobject['type'] != ' ' and jsonobject['type'] != '':
#                         query['type'] = jsonobject['type'] 
#                 if jsonobject['department'] is not None:
#                     if jsonobject['department'] != ' ' and jsonobject['department'] != '':
#                         query['department'] = jsonobject['department']
                        
#                 if jsonobject['job_no'] is not None:
#                     if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
#                         query['job_no']= jsonobject['job_no']
#                 print("query ====",query)
#                 ret = SORTIPADDRESS(query)
#             else:
#                 department = jsonobject['department']
#                 query = {}  
#                 if jsonobject['type'] is not None:
#                     if jsonobject['type'] != ' ' and jsonobject['type'] != '':
#                         query['type'] = jsonobject['type'] 
#                 if jsonobject['department'] is not None:
#                     if jsonobject['department'] != ' ' and jsonobject['department'] != '':
#                         query['department'] = jsonobject['department']
                        
#                 if jsonobject['job_no'] is not None:
#                     if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
#                         query['job_no']= jsonobject['job_no']
#                 print("query ====",query)
#                 ret = SORTIPADDRESS(query)
                
#         else:
#             ret = {'success': False, 'message':  " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
#         # ret['message']="POST METHOD"
#     else:
#         ret['message'] = 'request type wrong, please try once again.'
#     return JsonResponse(ret)# jsonify


# # @dashboard.route('/sheetDepartmentlist', methods=['GET'])
# # @dashboard.route('/sheetDepartmentlist', methods=['POST'])
# @csrf_exempt
# def sheetDepar33dstmentlist(request):
#     try:
#         ret = {'success': False, 'message':'something went wrong with get  details api'}
#         sheet_data = mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])
#         if request.method == 'GET':
            
#             if sheet_data is not None:
#                 match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
#                 data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
#                                                            {'$group':{'_id': '$department', 'all_data':{'$first': '$$ROOT'}}},
#                                                            {'$limit': 4000000}]))
#                 dash_data = []
#                 if len(data) != 0:
#                     for count, i in enumerate(data):
#                         if isEmpty(i['all_data']['data']):
#                             if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
#                                 if len(i['all_data']['data']['panel_data']) !=0  :
#                                     if i['_id']  not in dash_data:
#                                         dash_data.append(i['_id'])
#                                 else:
#                                     if i['_id']  not in dash_data:
#                                         dash_data.append(i['_id'])

#                             elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
#                                 if 'hydraulic_data' in i['all_data']['data']:
#                                     if len(i['all_data']['data']['hydraulic_data']) !=0 :
#                                         if i['_id'] not in dash_data:
#                                             dash_data.append(i['_id'])
#                                     else:
#                                         if i['_id']  not in dash_data:
#                                             dash_data.append(i['_id'])

#                             elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
#                                 if len(i['all_data']['data']['useal_data']) !=0 :
#                                     if i['_id']  not in dash_data:
#                                         dash_data.append(i['_id'])
                                        
#                                 else:
#                                     if i['_id']  not in dash_data:
#                                         dash_data.append(i['_id'])
                                
#                     if len(dash_data) != 0:
#                         ret = {'success': True, 'message': dash_data}
#                     else:
#                         ret['message'] = 'data not found'
#                 else:
#                     ret['message'] = 'data not found'
#             else:
#                 ret['message'] = 'job sheet is not uploaded yet'
#         elif request.method == 'POST':
#             jsonobject = request.json
#             if jsonobject == None:
#                 jsonobject = {}
#             request_key_array = ['job_no','type']
#             jsonobjectarray = list(set(jsonobject))
#             missing_key = set(request_key_array).difference(jsonobjectarray)
#             if not missing_key:
#                 output =  keys_with_none_values(jsonobject)
#                 if output:
#                     print(" something missing ",output)                
#                     query = {}                
#                     panel_data = {'panel_data':{"$elemMatch":[]}}                
#                     if jsonobject['type'] is not None:
#                         if jsonobject['type'] != ' ' and jsonobject['type'] != '':
#                             query['type'] = jsonobject['type']                
                            
#                     if jsonobject['job_no'] is not None:
#                         if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
#                             query['job_no']= jsonobject['job_no']
#                     print("query ====",query)                  
                    
                    
#                     ret = SORTDEPARTMENT(query)
#                 else:
#                     job_no = jsonobject['job_no']                    
#                     if sheet_data is not None:
#                         query = {}                              
#                         if jsonobject['type'] is not None:
#                             if jsonobject['type'] != ' ' and jsonobject['type'] != '':
#                                 query['type'] = jsonobject['type']                
                                
#                         if jsonobject['job_no'] is not None:
#                             if jsonobject['job_no'] != '' and  jsonobject['job_no'] != ' ':
#                                 query['job_no']= jsonobject['job_no']
#                         ret = SORTDEPARTMENT(query)
#                         if job_no is not None:
#                             match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token'],'job_no':job_no}
#                             data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
#                                                                         {'$group':{'_id':{'ipdata': '$data.ip_address'}, 'all_data':{'$first': '$$ROOT'}}},
#                                                                         {'$limit': 4000000}]))
#                             dash_data = []
#                             if len(data) != 0:
#                                 for count, i in enumerate(data):
#                                     if isEmpty(i['all_data']['data']):
#                                         if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
#                                             if len(i['all_data']['data']['panel_data']) !=0  :
#                                                 if i['all_data']['department']  not in dash_data:
#                                                     dash_data.append(i['all_data']['department'])
#                                             else:
#                                                 if i['all_data']['department']  not in dash_data:
#                                                     dash_data.append(i['all_data']['department'])

#                                         elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
#                                             if 'hydraulic_data' in i['all_data']['data']:
#                                                 if len(i['all_data']['data']['hydraulic_data']) !=0 :
#                                                     if i['all_data']['department'] not in dash_data:
#                                                         dash_data.append(i['all_data']['department'])
#                                                 else:
#                                                     if i['all_data']['department']  not in dash_data:
#                                                         dash_data.append(i['all_data']['department'])

#                                         elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
#                                             if len(i['all_data']['data']['useal_data']) !=0 :
#                                                 if i['all_data']['department']  not in dash_data:
#                                                     dash_data.append(i['all_data']['department'])
                                                    
#                                             else:
#                                                 if i['all_data']['department'] not in dash_data:
#                                                     dash_data.append(i['all_data']['department'])
                                            
#                                 if len(dash_data) != 0:
#                                     ret = {'success': True, 'message': dash_data}
#                                 else:
#                                     ret['message'] = 'data not found'
#                             else:
#                                 ret['message'] = 'data not found'
#                         else:
#                             ret['message'] = 'given job_no is none.'                            
#                     else:
#                         ret['message'] = 'job sheet is not uploaded yet'
#             else:
#                 ret = {'success': False, 'message':  " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
                
#         else:
#             ret['message'] = 'request type wrong, please try once again.'
#     except ( 
#         pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#         pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#         pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#         pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#         pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#         pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#         pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#         pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#         pymongo.errors.WriteError) as error:
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- sheetDepartmeeerntlist 1", str(error), " ----time ---- ", now_time_with_time()])) 
#         ret['message' ] =" ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
#         if restart_mongodb_r_service():
#             print("mongodb restarted")
#         else:
#             if forcerestart_mongodb_r_service():
#                 print("mongodb service force restarted-")
#             else:
#                 print("mongodb service is not yet started.")    
#     except Exception as  error:
#         ret = {'success': False, 'message': str(error)}
#         ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- sheetDepeerartmentlist 2", str(error), " ----time ---- ", now_time_with_time()])) 
#     return JsonResponse(ret)#jsonify

# ## done for object 
# # @dashboard.route('/listofjobtypes', methods=['GET'])
# @csrf_exempt
# def JOBTYPESORTING(request):
#     ret = {'success': False, 'message':'something went wrong with get  details api'}
#     if request.method == 'GET':
#         sheet_data = Mongo.db.job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])

#         # job_sheet_details=get_or_create_collection("job_sheet_details")#GET THE COLLECTION
#         # sheet_data = job_sheet_details.find_one({'status': 1}, sort=[('_id', pymongo.DESCENDING)])

#         if sheet_data is not None:
#             match_data = {'job_sheet_name': sheet_data['job_sheet_name'], 'token': sheet_data['token']}
#             data = list(mongo.db.panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
#                                                         {'$group':{'_id': '$type', 'all_data':{'$first': '$$ROOT'}}},
#                                                         {'$limit': 4000000}]))

#             # panel_data=get_or_create_collection("panel_data")
#             # data=list(panel_data.aggregate([{'$match': match_data}, {'$sort':{'job_sheet_time': -1}}, 
#             #                                             {'$group':{'_id': '$type', 'all_data':{'$first': '$$ROOT'}}},
#                                                         # {'$limit': 4000000}]))
#             dash_data = []
#             if len(data) != 0:
#                 for count, i in enumerate(data):
#                     # print("000000000000000000000000000000000000000000000000000&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&------",i)
#                     if isEmpty(i['all_data']['data']) :
#                         if i['all_data']['type']=='HT' or i['all_data']['type']=='ht':
#                             if len(i['all_data']['data']['panel_data']) !=0  :
#                                 if i['_id']  not in dash_data:
#                                     dash_data.append(i['_id'])
#                             else:
#                                 if i['_id']  not in dash_data:
#                                     dash_data.append(i['_id'])

#                         elif i['all_data']['type']=='Hydraulic' or i['all_data']['type']=='hydraulic':
#                             if 'hydraulic_data' in i['all_data']['data']:
#                                 if len(i['all_data']['data']['hydraulic_data']) !=0 :
#                                     if i['_id']  not in dash_data:
#                                         dash_data.append(i['_id'])
#                                 else:
#                                     if i['_id']  not in dash_data:
#                                         dash_data.append(i['_id'])

#                         elif i['all_data']['type']=="Useal" or i['all_data']['type']=='useal':
#                             if len(i['all_data']['data']['useal_data']) !=0 :
#                                 if i['_id']  not in dash_data:
#                                     dash_data.append(i['_id'])
#                             else:
#                                 if i['_id']  not in dash_data:
#                                     dash_data.append(i['_id'])
#                     else:
#                         if i['_id']  not in dash_data:
#                             dash_data.append(i['_id'])

#                 if len(dash_data) != 0:
#                     ret = {'success': True, 'message': dash_data}
#                 else:
#                     ret['message'] = 'data not found'
#             else:
#                 ret['message'] = 'data not found'
#         else:
#             ret['message'] = 'job sheet is not uploaded yet'
#     else:
#         ret['message'] = 'request type wrong, please try once again.'
#     return JsonResponse(ret)#jsonify

# # @dashboard.route('/excel_download', methods=['GET'])
# @csrf_exempt
# def excel_result(request):
#     if request.method == "GET":
#         try:
#             list_of_files = glob.glob(os.path.join(os.getcwd(), "ESI_MONITORING_SHEETS/*"))
#             latest_file = max(list_of_files, key=os.path.getctime)
#             path, filename = os.path.split(latest_file)
#             if filename:
#                 main_path = os.path.abspath(path)
#                 response = make_response(send_from_directory(main_path, filename, as_attachment=True, download_name=filename))
#                 response.headers['Excel_filename'] = filename
#                 return JsonResponse(response)
#             else:
#                 return {'success': False, 'message': 'File is not found.'}
#         except (NameError, RuntimeError, FileNotFoundError, AssertionError,
#             AttributeError, EOFError, FloatingPointError, TypeError,
#             GeneratorExit, IndexError, KeyError, KeyboardInterrupt, MemoryError,
#             NotImplementedError, OSError, OverflowError, ReferenceError,
#             StopIteration, SyntaxError, IndentationError, TabError, SystemError,
#             SystemExit, TypeError, UnboundLocalError, UnicodeError,
#             UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError,
#             ValueError, ZeroDivisionError, ConnectionError, KeyboardInterrupt,
#             BaseException, ValueError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- excel_download 1", str(error), " ----time ---- ", now_time_with_time()])) 
#             return JsonResponse({'success': False, 'message': str(error)})
            
#         except Exception as  error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- excel_download 2", str(error), " ----time ---- ", now_time_with_time()])) 
#             return JsonResponse({'success': False, 'message': str(error)})
#     else:
#         return JsonResponse({'success': False, 'message': 'request type wrong, please try once again.'})

# # @dashboard.route('/violation_excel_download', methods=['GET'])
# @csrf_exempt
# def violation_excel_result(request):
#     if request.method == "GET":
#         # response={"message":'violation_excel_download'}
#         list_of_files = glob.glob(os.path.join(os.getcwd(), "violation_excel_sheets/*"))
#         latest_file = max(list_of_files, key=os.path.getctime)
#         path, filename = os.path.split(latest_file)
#         if filename:
#             main_path = os.path.abspath(path)
#             response = make_response(send_from_directory(main_path, filename, as_attachment=True, download_name=filename))
#             response.headers['Excel_filename'] = filename
#             # return response
#             # return send_from_directory(main_path, filename,headers=headers)
#         else:
#             # return {'success': False, 'message': 'File is not found.'}
#             response={'success': False, 'message': 'File is not found.'}
#     else:
#         response={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(response)


# # @dashboard.route('/delete_riro_data/<key_id>', methods=['GET'])
# @csrf_exempt
# def delete_riro_data_key_id_wise(request,key_id=None):
#     if request.method == "GET":
#         ret = {'message': 'something error occured in delte_riro_data.','success': False}
#         try:
#             if key_id is not None:
#                 find_delete_data = mongo.db.riro_data.find_one({'riro_key_id': key_id})
#                 if find_delete_data is not None:
#                     result = mongo.db.riro_data.delete_one({'_id': ObjectId(find_delete_data['_id'])})
#                     if result.deleted_count > 0:
#                         ret = {'message': 'riro_data deleted successfully.','success': True}
#                     else:
#                         ret['message'] ='riro_data is not deleted ,due to something went wrong with database.'
#                 else:
#                     ret['message' ] = '  riro_data is not found for this id, please try once again.'
#             else:
#                 ret['message' ] = '  riro key id is None type please give proper riro key id.'
#         except ( 
#             pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#             pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#             pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#             pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#             pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#             pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#             pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#             pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#             pymongo.errors.WriteError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_riro_data 1", str(error), " ----time ---- ", now_time_with_time()])) 
#             ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
#             if restart_mongodb_r_service():
#                 print("mongodb restarted")
#             else:
#                 if forcerestart_mongodb_r_service():
#                     print("mongodb service force restarted-")
#                 else:
#                     print("mongodb service is not yet started.") 
#         except Exception as  error:
#             ret['message']=" ".join(["something error has occered in api", str(error)])
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_riro_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
#     else:
#         ret={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(ret)

# # @dashboard.route('/deleteRemark/<key_id>', methods=['GET'])
# @csrf_exempt
# def deleteRemark(request,key_id=None):
#     if request.method == "GET":
#         ret = {'message': 'something error occured in delte_riro_data.','success': False}
#         try:
#             if key_id is not None:
#                 find_delete_data = mongo.db.riro_data.find_one({'riro_key_id': key_id})
#                 if find_delete_data is not None:
#                     result = mongo.db.riro_data.update_one({'_id': ObjectId(find_delete_data['_id'])},  {'$set': {"remarks":''}})
#                     if result.matched_count > 0:
#                         ret = {'message': 'riro_data deleted successfully.','success': True}
#                     else:
#                         ret['message'] ='riro_data is not deleted ,due to something went wrong with database.'
#                 else:
#                     ret['message' ] = '  riro_data is not found for this id, please try once again.'
#             else:
#                 ret['message' ] = '  riro key id is None type please give proper riro key id.'
#         except ( 
#             pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#             pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#             pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#             pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#             pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#             pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#             pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#             pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#             pymongo.errors.WriteError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_riro_data 1", str(error), " ----time ---- ", now_time_with_time()])) 
#             ret['message' ] = " ".join(["error ", str(error) , '  ----time ----   ' , now_time_with_time()])
#             if restart_mongodb_r_service():
#                 print("mongodb restarted")
#             else:
#                 if forcerestart_mongodb_r_service():
#                     print("mongodb service force restarted-")
#                 else:
#                     print("mongodb service is not yet started.") 
#         except Exception as  error:
#             ret['message']=" ".join(["something error has occered in api", str(error)])
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- delete_riro_data 2", str(error), " ----time ---- ", now_time_with_time()]))        
       
#     else:
#         ret={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(ret)



# # @dashboard.route('/multiisolation/<id>', methods = ['GET'])
# @csrf_exempt
# def multii44solation_convayor_pnumertic_hydralic23323(request,id = None):
#     if request.method == "GET":
#         if 1:
#         # try:
#             ret = {'success': False, 'message':'Something went wrong, please try again later'}
#             ret['job_sheet_status'] = False
#             sheet_data=None
#             if id is not None:
#                 sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
#             else:            
#                 sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])     
#             if sheet_data is not None:
#                 data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',   pymongo.DESCENDING)]))
#                 if len(data) !=0:# is not None:
#                     final_panel_data = []   
#                     data = MUPANRRILATION_multi_isolation(data)
#                     riro_final = []
#                     for ___INNN, emmmi in enumerate(data):
#                         if (emmmi['type']=='HT' or emmmi['type']=='ht' ) :
#                             if isEmpty(emmmi['data']) :
#                                 if (type(emmmi['data']['panel_data']) != list) :
#                                     if emmmi['data']['panel_data']['panel_id'] is not None:
#                                         #list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url'], 'flasher_status':1, 'panel_no': emmmi['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
#                                         show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url'], 'panel_no': emmmi['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
                                        
#                                         if len(show_live_riro) != 0:
#                                             show_live_riro = riro_live_data(show_live_riro)
#                                             emmmi['riro_data'] = show_live_riro
#                                             emmmi['riro_edit_status'] = False
#                                             emmmi['live_status'] = True
#                                             emmmi['sort_id'] = show_live_riro[0]['sort_id'] 
#                                             if emmmi['tagname']  is not None and emmmi['tagname']  !='':
#                                                 emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
#                                             else:
#                                                 emmmi['isolation_status'] = None
#                                             emmmi['exception_status'] = False
#                                             riro_final.append(emmmi)
#                                         elif emmmi['data']['rtsp_url']:
#                                             find_riro_data = list(mongo.db.riro_data.find({'token': emmmi['token'], 'camera_name': emmmi['data']['camera_name'], 'camera_rtsp': emmmi['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
#                                             if len(find_riro_data) != 0:
#                                                 (check_data, panel_status, riro_edit_status) = riro_history_check_the_riro_data_with_sorting_(emmmi['data']['rtsp_url'], emmmi['data']['panel_data']['panel_id'], find_riro_data)
#                                                 check_data = list(check_data)
#                                                 if panel_status or len(check_data) != 0:
#                                                     emmmi['data']['panel_data']['panel_status'] = panel_status
#                                                     emmmi['riro_data'] = check_data
#                                                     emmmi['riro_edit_status'] = riro_edit_status
#                                                     emmmi['live_status'] = False
#                                                     emmmi['sort_id'] = check_data[0]['sort_id']
#                                                     if emmmi['tagname']  is not None and emmmi['tagname']  !='':
#                                                         emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
#                                                     else:
#                                                         emmmi['isolation_status'] = None
#                                                     emmmi['exception_status'] = False
#                                                     riro_final.append(emmmi)
#                                                 else:
#                                                     check_data = [{'sort_id': None,'panel_no': emmmi['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
#                                                                     'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
#                                                                     'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
#                                                     emmmi['riro_data'] = check_data
#                                                     emmmi['riro_edit_status'] = False
#                                                     emmmi['live_status'] = False
#                                                     emmmi['sort_id'] = None
#                                                     if emmmi['tagname']  is not None and emmmi['tagname']  !='':
#                                                         emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
#                                                     else:
#                                                         emmmi['isolation_status'] = None
#                                                     emmmi['exception_status'] = False
#                                                     riro_final.append(emmmi)
#                                             else:
#                                                 check_data = [{'sort_id': None, 'panel_no':emmmi['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
#                                                         'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
#                                                 emmmi['riro_data'] = check_data
#                                                 emmmi['riro_edit_status'] = False
#                                                 emmmi['live_status'] = False
#                                                 emmmi['sort_id'] = None
#                                                 if emmmi['tagname']  is not None and emmmi['tagname']  !='':
#                                                     emmmi['isolation_status']  = isolation_camaparision_function(emmmi['tagname'])
#                                                 else:
#                                                     emmmi['isolation_status'] = None
#                                                 emmmi['exception_status'] = False
#                                                 riro_final.append(emmmi)
#                                 else:
#                                     emmmi['riro_data'] = []
#                                     emmmi['riro_edit_status'] = False
#                                     emmmi['live_status'] = False
#                                     emmmi['sort_id'] = None
#                                     emmmi['isolation_status'] = None
#                                     emmmi['exception_status'] = False
#                                     riro_final.append(emmmi)
#                             else:
#                                 emmmi['riro_data'] = []
#                                 emmmi['riro_edit_status'] = False
#                                 emmmi['live_status'] = False
#                                 emmmi['sort_id'] = None
#                                 emmmi['isolation_status'] = None
#                                 emmmi['exception_status'] = False
#                                 riro_final.append(emmmi)
#                         elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
#                             hydata , panel_status = hydralockdataFetch(emmmi)
#                             check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
#                             emmmi['riro_data'] = check_data
#                             emmmi['riro_edit_status'] = False
#                             emmmi['live_status'] = False
#                             emmmi['sort_id'] = None
#                             emmmi['isolation_status'] = None
#                             emmmi['exception_status'] = False
#                             riro_final.append(emmmi)
#                         else:
#                             emmmi['riro_data'] = []
#                             emmmi['riro_edit_status'] = False
#                             emmmi['live_status'] = False
#                             emmmi['sort_id'] = None
#                             emmmi['isolation_status'] = None
#                             emmmi['exception_status'] = False
#                             riro_final.append(emmmi)
                            
#                     if len(riro_final) !=0:             
#                         ret = {'message': check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final)) ),'success': True}
#                         ret['job_sheet_status'] = True
#                     else:
#                         ret = {'message': 'panel data not found.', 'success': False}
#                         ret['job_sheet_status'] = True
#                 else:
#                     ret['message'] = 'panel data not found'
#                     ret['job_sheet_status'] = True
#             else:
#                 ret['message'] ="jobsheet is not yet uploaded, please upload the jobsheet"

#         # # except ( 
#         # #          pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#         # #          pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#         # #          pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#         # #          pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#         # #          pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#         # #          pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#         # #          pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#         # #          pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#         # #          pymongo.errors.WriteError) as error:
#         # #     print("print(,)", str(error))
#         # # ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 1", str(error), " ----time ---- ", now_time_with_time()]))
#         # #     ret['message'] = str(error)
#         # #     ret['success'] = False
#         # #     if restart_mongodb_r_service():
#         # #         print("mongodb restarted")
#         # #     else:
#         # #         if forcerestart_mongodb_r_service():
#         # #             print("mongodb service force restarted-")
#         # #         else:
#         # #             print("mongodb service is not yet started.")  
#         # # except Exception as  error:
#         # #     ret['message'] = str(error)
#         # #     ret['success'] = False
#         # # ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- multiiso44lation 2", str(error), " ----time ---- ", now_time_with_time()]))
#         # return ret
#     else:
#         ret={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(ret)

# # @dashboard.route('/SORTINGIPWISE/<ip_address>', methods=['GET'])
# @csrf_exempt
# def SORTINGJOBSIPWISE(request,ip_address = None ):
#     if request.method == "GET":
#         if 1:
#         # try:
#             ret = {'success': False, 'message':'Something went wrong, please try again later'}
#             ret['job_sheet_status'] = False
#             sheet_data = None
#             sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])        
#             if sheet_data is not None:
#                 if ip_address is not None:
#                     data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token'],"data.ip_address": ip_address}, sort=[('_id',   pymongo.DESCENDING)]))
#                     # print("data=====",len(data))
#                     if len(data) !=0 :
#                         final_panel_data = []   
#                         data = MUPANRRILATION_multi_isolation(data)
#                         for ___INNN, emmmi in enumerate(data):
#                             if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and emmmi['data']['panel_data']['panel_id'] is not None:
#                                 final_panel_data.append(emmmi)
#                             elif emmmi['type']=='conveyor' or emmmi['type']=='CONVEYOR' or emmmi['type']=='hydraulic' or emmmi['type']=='pneumatic' or emmmi['type']=='Hydraulic' or emmmi['type']=='Pneumatic':
#                                 final_panel_data.append(emmmi)
#                         print("find panel data ====",len(final_panel_data) )
#                         if len(final_panel_data) != 0:
#                             riro_final = []
#                             for i, each_panel in enumerate(final_panel_data):
#                                 if each_panel['type'] =='HT' or each_panel['type']=='ht':
#                                     show_live_riro = list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status':1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
#                                     if len(show_live_riro) != 0:
#                                         show_live_riro = riro_live_data(show_live_riro)
#                                         each_panel['riro_data'] = show_live_riro
#                                         each_panel['riro_edit_status'] = False
#                                         each_panel['live_status'] = True
#                                         each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
#                                         if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                             each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                         else:
#                                             each_panel['isolation_status'] = None
#                                         each_panel['exception_status'] = False
#                                         riro_final.append(each_panel)
#                                     elif each_panel['data']['rtsp_url']:
#                                         find_riro_data = list(mongo.db.riro_data.find({'token': each_panel['token'], 'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
#                                         if len(find_riro_data) != 0:
#                                             (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
#                                             check_data = list(check_data)
#                                             if panel_status or len(check_data) != 0:
#                                                 each_panel['data']['panel_data']['panel_status'] = panel_status
#                                                 each_panel['riro_data'] = check_data
#                                                 each_panel['riro_edit_status'] = riro_edit_status
#                                                 each_panel['live_status'] = False
#                                                 each_panel['sort_id'] = check_data[0]['sort_id']
#                                                 if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                                     each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                                 else:
#                                                     each_panel['isolation_status'] = None
#                                                 each_panel['exception_status'] = False
#                                                 riro_final.append(each_panel)
#                                             else:
#                                                 check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,
#                                                             'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':None, 'riro_merged_image': None,
#                                                             'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None,'remarks': ' '} ]
#                                                 each_panel['riro_data'] = check_data
#                                                 each_panel['riro_edit_status'] = False
#                                                 each_panel['live_status'] = False
#                                                 each_panel['sort_id'] = None
#                                                 if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                                     each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                                 else:
#                                                     each_panel['isolation_status'] = None
#                                                 each_panel['exception_status'] = False
#                                                 riro_final.append(each_panel)
#                                         else:
#                                             check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None,
#                                                 'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None,'within_15_min':None, 'remarks': ' '}]
#                                             each_panel['riro_data'] = check_data
#                                             each_panel['riro_edit_status'] = False
#                                             each_panel['live_status'] = False
#                                             each_panel['sort_id'] = None
#                                             if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                                 each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                             else:
#                                                 each_panel['isolation_status'] = None
#                                             each_panel['exception_status'] = False
#                                             riro_final.append(each_panel)
#                                 else:
#                                     hydata , panel_status = hydralockdataFetch(each_panel)
#                                     check_data = [{'panel_status': panel_status,'hydra_data': hydata}]
#                                     each_panel['riro_data'] = check_data
#                                     each_panel['riro_edit_status'] = False
#                                     each_panel['live_status'] = False
#                                     each_panel['sort_id'] = None
#                                     each_panel['isolation_status'] = None
#                                     each_panel['exception_status'] = False
#                                     riro_final.append(each_panel)

#                             else:                        
#                                 ret = {'message': check_magnetic_flasher_status(parse_json(all_riro_final_sortin(riro_final))  ),'success': True}
#                                 ret['job_sheet_status'] = True
#                         else:
#                             ret = {'message': 'panel data not found.', 'success': False}
#                             ret['job_sheet_status'] = True                
#                     else:
#                         ret['message'] = 'panel data not found'
#                         ret['job_sheet_status'] = True
#                 else:
#                     ret['message'] = 'ip address given none value, please try to send correct one.'
#                     ret['job_sheet_status'] = True
#             else:
#                 ret['message'] = 'job sheet is not uploaded, please upload the jobsheet.'
#                 ret['job_sheet_status'] = False

#         # except ( 
#         #          pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#         #          pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#         #          pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#         #          pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#         #          pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#         #          pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#         #          pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#         #          pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#         #          pymongo.errors.WriteError) as error:
#         #     print("print(,)", str(error))
#         #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGIPWISE 1", str(error), " ----time ---- ", now_time_with_time()]))
#         #     ret['message'] = str(error)
#         #     ret['success'] = False
#         #     if restart_mongodb_r_service():
#         #         print("mongodb restarted")
#         #     else:
#         #         if forcerestart_mongodb_r_service():
#         #             print("mongodb service force restarted-")
#         #         else:
#         #             print("mongodb service is not yet started.")  
#         # except Exception as  error:
#         #     ret['message'] = str(error)
#         #     ret['success'] = False
#         #ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- SORTINGIPWISE 2", str(error), " ----time ---- ", now_time_with_time()]))
#     else:
#         ret={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(ret)



# # @dashboard.route('/create_excel/<id>', methods=['GET'])
# @csrf_exempt
# def TSKEXCELGENERATION(request,id = None):
#     if request.method == "GET":
#         ret = {'success': False, 'message':'Something went wrong, please try again later'}
#         if 1:
#         # try:
#             sheet_data=None
#             if id is not None:
#                 sheet_data = mongo.db.job_sheet_details.find_one({'_id': ObjectId(id)},sort=[('_id', pymongo.DESCENDING)])
#             else:            
#                 sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
#             if sheet_data is not None:
#                 data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
#                 if len(data) !=0 :
#                     final_panel_data = []
#                     data = PANELWISERIRODATAFUNCTION(data)
#                     for ___INNN, emmmi in enumerate(data):
#                         if emmmi['data']['panel_data']['panel_id'] is not None:
#                             final_panel_data.append(emmmi)
#                     if len(final_panel_data) != 0:
#                         riro_final = []
#                         for i, each_panel in enumerate(final_panel_data):
#                             show_live_riro =list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status': 1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
#                             if len(show_live_riro) != 0:
#                                 show_live_riro = riro_live_data(show_live_riro)
#                                 each_panel['riro_data'] = show_live_riro
#                                 each_panel['riro_edit_status'] = False
#                                 each_panel['live_status'] = True
#                                 each_panel['sort_id'] = show_live_riro[0]['sort_id'] 
#                                 if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                     each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                 else:
#                                     each_panel['isolation_status'] = None
#                                 #each_panel = parse_json(each_panel)
#                                 riro_final.append(each_panel)
#                             elif each_panel['data']['rtsp_url']:
#                                 find_riro_data =list(mongo.db.riro_data.find({ 'token': each_panel['token'], 'camera_name':  each_panel['data']['camera_name'],'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
#                                 if len(find_riro_data) != 0:
#                                     (check_data, panel_status, riro_edit_status) = GENERATIONEXCELRIRODATA(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data)#(riro_history_check_the_riro_data_with_sorting_(camera_rtsp, each_panel['data']['panel_data']['panel_id'], find_riro_data))
                                    
#                                     if panel_status or len(check_data) != 0:
#                                         each_panel['data']['panel_data']['panel_status'] = panel_status
#                                         each_panel['riro_data'] = check_data
#                                         each_panel['riro_edit_status'] = riro_edit_status
#                                         each_panel['live_status'] = False
#                                         each_panel['sort_id'] = check_data[0]['sort_id']
#                                         if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                             each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                         else:
#                                             each_panel['isolation_status'] = None
#                                         riro_final.append(each_panel)
#                                     else:
#                                         check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 'rack_process':
#                                             None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None,'tag_time': None, 'five_meter':
#                                             None, 'barricading': None,'magnetic_flasher': None,'violation': False, 'riro_key_id':
#                                             None, 'riro_merged_image': None,'riro_merged_image_size':{'height':
#                                             None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}  ]
#                                         each_panel['riro_data'] = check_data
#                                         each_panel['riro_edit_status'] = False
#                                         each_panel['live_status'] = False
#                                         each_panel['sort_id'] = None
#                                         if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                             each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                         else:
#                                             each_panel['isolation_status'] = None
#                                         riro_final.append(each_panel)
#                                 else:
#                                     check_data = [{'sort_id': None, 'panel_no':
#                                         each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 'irrd_in_time':
#                                         None, 'irrd_out_time': None, 'tag':
#                                         None, 'lock': None, 'lock_time': None,'tag_time': None, 'five_meter': None,'barricading': None, 'magnetic_flasher':
#                                         None, 'violation': False, 'riro_key_id':
#                                         None, 'riro_merged_image': None,'riro_merged_image_size':{'height':
#                                         None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}]
#                                     each_panel['riro_data'] = check_data
#                                     each_panel['riro_edit_status'] = False
#                                     each_panel['live_status'] = False
#                                     each_panel['sort_id'] = None
#                                     if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                         each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                     else:
#                                         each_panel['isolation_status'] = None
#                                     riro_final.append(each_panel) 
#                         newdata = merge_multi_isolation_jobs(parse_json(riro_final))      
#                         ret =TSKSHEET123(newdata)
#                     else:
#                         ret = {'message': 'panel data not found.', 'success': False}
#                 else:
#                     ret['message'] = 'panel data not found'
#         # except ( 
#         #          pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#         #          pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#         #          pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#         #          pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#         #          pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#         #          pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#         #          pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#         #          pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#         #          pymongo.errors.WriteError) as error:
#         #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create22_excel 1", str(error), " ----time ---- ", now_time_with_time()]))
#         #     ret['message'] = " ".join(["something error has occered in api", str(error)])
#         #     if restart_mongodb_r_service():
#         #         print("mongodb restarted")
#         #     else:
#         #         if forcerestart_mongodb_r_service():
#         #             print("mongodb service force restarted-")
#         #         else:
#         #             print("mongodb service is not yet started.") 
#         # except Exception as  error:
#         #     ret['message'] = str(error)
#         #     ret['success'] = False
#         #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- create_33excel 2", str(error), " ----time ---- ", now_time_with_time()]))
#     else:
#         ret={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(ret)

# # @dashboard.route('/all_riro_data_history_new_concept', methods=['GET'])
# @csrf_exempt
# def all_riro_data_history_new_concept(request):
#     if request.method == "GET":
#         ret = {'success': False, 'message':'Something went wrong, please try again later'}
#         ret['job_sheet_status'] = False
#         try:
#             sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
#             print(" sheet data ontains ----------",sheet_data)
#             if sheet_data is not None:
#                 data = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id',pymongo.DESCENDING)]))
#                 if len(data) !=0:
#                     final_panel_data = []
#                     data = PANELWISERIRODATAFUNCTION(data)
#                     # final_panel_data = [emmmi for ___INNN, emmmi  in enumerate(data) if emmmi['type']=='HT' or emmmi['type']=='ht' and type(emmmi['data']['panel_data']) != list and  emmmi['data']['panel_data']['panel_id'] is not None]
#                     for ___INNN, emmmi in enumerate(data):
#                         if emmmi['data']['panel_data']['panel_id'] is not None:
#                             final_panel_data.append(emmmi)
#                     if len(final_panel_data) != 0:
#                         riro_final = []
#                         for i, each_panel in enumerate(final_panel_data):
#                             show_live_riro =list(mongo.db.riro_data.find({'token':sheet_data['token'], 'datauploadstatus': 11,'camera_name': each_panel['data']['camera_name'], 'camera_rtsp': each_panel['data']['rtsp_url'], 'flasher_status': 1, 'panel_no': each_panel['data']['panel_data']['panel_id']}, sort=[('_id', pymongo.DESCENDING)]))
#                             if len(show_live_riro) != 0:
#                                 show_live_riro = riro_live_data(show_live_riro)
#                                 each_panel['riro_data'],each_panel['riro_edit_status'],each_panel['live_status'],each_panel['sort_id']  = show_live_riro,False,True,show_live_riro[0]['sort_id'] 
#                                 if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                     each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                 else:
#                                     each_panel['isolation_status'] = None
#                                 # each_panel = parse_json(each_panel)
#                                 riro_final.append(each_panel)
#                             elif each_panel['data']['rtsp_url']:
#                                 find_riro_data =list(mongo.db.riro_data.find({ 'token': each_panel['token'], 'camera_name':  each_panel['data']['camera_name'],'camera_rtsp': each_panel['data']['rtsp_url']}, sort=[('_id', pymongo.DESCENDING)]))
#                                 if len(find_riro_data) != 0:
#                                     (check_data, panel_status, riro_edit_status) = (riro_history_check_the_riro_data_with_sorting_(each_panel['data']['rtsp_url'], each_panel['data']['panel_data']['panel_id'], find_riro_data))
#                                     if panel_status or len(check_data) != 0:
#                                         each_panel['data']['panel_data']['panel_status'] = panel_status
#                                         each_panel['riro_data'] = check_data
#                                         each_panel['riro_edit_status'] = riro_edit_status
#                                         each_panel['live_status'] = False
#                                         each_panel['sort_id'] = check_data[0]['sort_id']
#                                         if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                             each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                         else:
#                                             each_panel['isolation_status'] = None
#                                         riro_final.append(each_panel)
#                                     else:
#                                         check_data = [{'sort_id': None,'panel_no': each_panel['data']['panel_data']['panel_id'],'rack_method': None, 
#                                                     'rack_process':None, 'irrd_in_time': None,'irrd_out_time': None, 'tag': None,'lock': None, 'lock_time': None,
#                                                     'tag_time': None, 'five_meter':None, 'barricading': None,'magnetic_flasher': None,'violation': False, 
#                                                     'riro_key_id': None, 'riro_merged_image': None,
#                                                     'riro_merged_image_size':{'height': None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '} ]
#                                         each_panel['riro_data'] = check_data
#                                         each_panel['riro_edit_status'] = False
#                                         each_panel['live_status'] = False
#                                         each_panel['sort_id'] = None
#                                         if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                             each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                         else:
#                                             each_panel['isolation_status'] = None                                    
#                                         riro_final.append(each_panel)
#                                 else:
#                                     check_data = [{'sort_id': None, 'panel_no':each_panel['data']['panel_data']['panel_id'], 'rack_method': None,'rack_process': None, 
#                                                 'irrd_in_time':None, 'irrd_out_time': None, 'tag':None, 'lock': None, 'lock_time': None,'tag_time': None, 
#                                                 'five_meter': None,'barricading': None, 'magnetic_flasher':None, 'violation': False, 'riro_key_id':None, 
#                                                 'riro_merged_image': None,'riro_merged_image_size':{'height':None, 'width': None},'riro_edit_status': False,'lock_tag_image': None, 'remarks': ' '}]
#                                     each_panel['riro_data'] = check_data
#                                     each_panel['riro_edit_status'] = False
#                                     each_panel['live_status'] = False
#                                     each_panel['sort_id'] = None
#                                     if each_panel['tagname']  is not None and each_panel['tagname']  !='':
#                                         each_panel['isolation_status']  = isolation_camaparision_function(each_panel['tagname'])
#                                     else:
#                                         each_panel['isolation_status'] = None
#                                     riro_final.append(each_panel)
#                         else:
#                             ret = {'message': merge_multi_isolation_jobs(parse_json(all_riro_final_sortin(parse_json(riro_final)))), 'success': True}
#                             ret['job_sheet_status'] = True
#                     else:
#                         ret = {'message': 'panel data not found.', 'success': False }
#                         ret['job_sheet_status'] = True
#                 else:
#                     ret['message'] = 'panel data not found'
#                     ret['job_sheet_status'] = True
#             else:
#                 ret['message'] = 'job sheet data is not found.'
#                 ret['job_sheet_status'] = False
#         except ( 
#                 pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
#                 pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
#                 pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
#                 pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
#                 pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
#                 pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
#                 pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
#                 pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
#                 pymongo.errors.WriteError) as error:
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- all_riro_data_history_new_concept 1", str(error), " ----time ---- ", now_time_with_time()]))
#             ret['message'] = " ".join(["something error has occered in api", str(error)])
#             if restart_mongodb_r_service():
#                 print("mongodb restarted")
#             else:
#                 if forcerestart_mongodb_r_service():
#                     print("mongodb service force restarted-")
#                 else:
#                     print("mongodb service is not yet started.") 
#         except Exception as  error:
#             ret['message'] = str(error)
#             ret['success'] = False
#             ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- all_riro_data_history_new_concept 2", str(error), " ----time ---- ", now_time_with_time()]))
#     else:
#         ret={'success': False, 'message': 'request type wrong, please try once again.'}
#     return JsonResponse(ret)
