from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from FLASK_into_DJANGO.packages import *
from FLASK_into_DJANGO.database import *


# Create your views here.
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
                    PPEViolationCount = mongo.db.data.count_documents(match_data)

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
        
                    result = list(mongo.db.data.aggregate(Vestpipeline))
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
                    result = list(mongo.db.data.aggregate(pipeline))
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
    else:
        match_data = {
        'timestamp': {'$regex': '^' + str(date.today())},
        'analyticstype': 'PPE_TYPE1',
        '$or': [
            {"object_data.Helmet": False},
            {"object_data.Vest": "no_ppe"}
        ]
        }
        PPEViolationCount = mongo.db.data.count_documents(match_data)
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
        
        result = list(mongo.db.data.aggregate(Vestpipeline))
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
        result = list(mongo.db.data.aggregate(pipeline))
        helmet_violation_count = result[0]['helmet_violation_count'] if result else 0
        ret = {
            'success': True,
            'message': {
                'ppeviolationcount': PPEViolationCount,
                'vest_violation_count': vest_violation_count,
                'helmet_violation_count': helmet_violation_count
            }
        } 
    return JsonResponse(ret) 
