from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *

# Create your views here.
def verify_rtsp(url, image_namereplace):
    directory_path = os.getcwd() + '/' + 'rtsp_roi_image'
    handle_uploaded_file(directory_path)
    present_time = replace_spl_char(str(datetime.datetime.now()))
    cam = cv2.VideoCapture(url)
    full_path = None
    if cam.isOpened() == True:
        while cam.isOpened():
            ret, frame = cam.read()
            if ret:
                name = image_namereplace + '_' + present_time + '.jpg'
                full_path = directory_path + '/' + name
                cv2.imwrite(full_path, frame)
                image_resizing(full_path)
                verfy_rtsp_response = {'image_name': name, 'height': '544', 'width': '960'}
                return verfy_rtsp_response
                break
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()
    else:
        return False
    

def check_license_of_camera(CamCount):
    # print(CamCount)
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =True
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        ERRORLOGdata("\n [ERROR] camera_api  --  check_license_of_camera  1 " + str(error)  +'  ----time ----   '+ now_time_with_time())
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata("\n [ERROR] camera_api  --check_license_of_camera 2 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata("\n [ERROR] camera_api  --check_license_of_camera 3 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        # print('res ===', res)
        # print('\n\n')
        # print('device_location', res['device_location'])
        lic = res['device_location']
        split_data=lic.split('_')[1].split("l")
        # print(lic.split('_')[1].split("l"))
        while '' in split_data:
            split_data.remove('')
        # print(split_data[0])
        # print(type(CamCount))
        # print(type(split_data[0]))
        if CamCount < int((split_data[0])):
            license_status = True
        else:
            license_status = False    
    return license_status

# @camera_details.route('/check_license', methods=['GET'])
@csrf_exempt
def checkingCamlicense(request):
    # if 1:
    if request.method == "GET":
        try:
            ret = {'message': 'something went wrong with get brand details api', 'success': False}
            sheet_data = job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
            sheet_camera_count = 0
            # print('sheet_data',sheet_data)
            if sheet_data is not None:
                sheet_data_count = list(panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
                #mongo.db.panel_data.count_documents({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']})
                unique_iplist = []
                if len(sheet_data_count) !=0:
                    for kl , eachElements in enumerate(sheet_data_count):
                        if len(eachElements['data']) !=0:
                            for i in eachElements['data']:
                                # print(i)
                                if i['ip_address'] not in unique_iplist:
                                    unique_iplist.append(i['ip_address'])
                    sheet_camera_count= len(unique_iplist) 
                
            CamCount = ppera_cameras.count_documents({})#find()#find_one()#mongo.db.ppera_cameras.find({}).count()
            # print("camera -count ",CamCount)#.count('true'))
            # print("sheet_data count",sheet_camera_count)
            CamCount = CamCount + sheet_camera_count
            if check_license_of_camera(CamCount):
                ret['message']='you have license to add the camera'
                ret['success']=True
            else:
                ret['message']="you don't have license to add the camera"
        except Exception as error:
            ret['message'] = str(error)
            ERRORLOGdata("\n [ERROR] camera_api  --check_license_of_camera 4 " + str(error)  +'  ----time ----   '+ now_time_with_time())
    else:
        ret={
            'success': False,
            'message':"request type wrong, please try once again."
        } 
    return JsonResponse(ret)