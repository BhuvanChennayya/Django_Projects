

from .database import mongo
from flask import Flask, url_for, session, request, jsonify, make_response, send_from_directory, Blueprint, render_template, Response,send_file
#https://towardsdatascience.com/a-python-api-for-background-requests-based-on-flask-and-multi-processing-187d0e3049c9


from waitress import serve
from flask_debug import Debug
from flask_cors import CORS
from bson.objectid import ObjectId
from bson import json_util
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, UnidentifiedImageError
import   xlsxwriter, glob,  datetime,  json, os, sys, cv2, csv, math, re, string, secrets, io, pymongo ,imutils,psycopg2,subprocess,openpyxl,random,requests,shutil
import psutil,  yaml,time
import numpy as np
from threading import Thread
from flask_pymongo import PyMongo
from re import L
import sys
from urllib.parse import urlparse

if sys.version_info[:2] >= (3, 8):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping
from datetime import date
import pandas as pd
from openpyxl.styles import PatternFill, Font,Alignment,Border,Side
from openpyxl.styles import Border, Side
from datetime import datetime, timedelta
from urllib.parse import urlsplit
# from Data_recieving_and_Dashboard.final_ping import final_ping

# email alert imports 
from fileinput import filename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import smtplib
from socket import gaierror
import smtplib
import socket
from psycopg2 import sql
import subprocess

###########user management 
from flask_restful import Resource, Api
import pymongo, re, bcrypt, jwt, os, base64 ,random
from werkzeug.security import check_password_hash, generate_password_hash


#########IP ping 
import asyncio 
from collections import defaultdict

######flask,socketio###
from flask_socketio import SocketIO, emit


##########voiceannouncement#####################
import platform
import ipaddress
from pywifi import PyWiFi, const, Profile

###########################
from io import BytesIO
import psutil
import GPUtil
import platform


#vpms EXCEL
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenPyXLImage
from PIL import Image
from collections import defaultdict, OrderedDict


email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
username_regex = re.compile(r"^[a-zA-Z0-9_]{3,10}$")
firstname_regex = re.compile(r"^[a-zA-Z]{3,10}$")           # first name and last name
contact_regex = re.compile(r"^[0-9]{10}$")
diffid_regex = re.compile(r"^[0-9]{1,10}$")             # for admin id and emp id
company_regex = re.compile(r"^[a-zA-Z]{2,15}$")             # for company, department and location
date_regex = re.compile(r"^(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])-(?P<day>0[1-9]|[1-2]\d|3[0-1]) (?P<hour>[0-1]\d|2[0-3]):(?P<minute>[0-5]\d):(?P<second>[0-5]\d)$")     # date format



####################IP PING#################



## Gridsize###############
def get_layout(total_streams):
    if total_streams in range(1, 3):  # 1 or 2
        rows, columns = 1, 2
    elif total_streams in range(3, 5):  # 3 or 4
        rows, columns = 2, 2
    elif total_streams in range(5, 7):  # 5 or 6
        rows, columns = 2, 3
    elif total_streams in range(7, 9):  # 7 or 8
        rows, columns = 2, 4
    elif total_streams in range(9, 11):  # 9 or 10
        rows, columns = 2, 5
    elif total_streams in range(11, 13):  # 11 or 12
        rows, columns = 3, 4
    elif total_streams in range(13, 15):  # 13 or 14
        rows, columns = 3, 5
    elif total_streams in range(15, 17):  # 15 or 16
        rows, columns = 4, 4
    elif total_streams in range(17, 19):  # 17 or 18
        rows, columns = 4, 5
    elif total_streams in range(19, 21):  # 19 or 20
        rows, columns = 4, 5
    elif total_streams in range(21, 25):  # 21 to 24
        rows, columns = 4, 6
    elif total_streams in range(25, 31):  # 25 to 30
        rows, columns = 5, 6
    elif total_streams in range(31, 37):  # 31 to 36
        rows, columns = 6, 6
    elif total_streams in range(37, 43):  # 37 to 42
        rows, columns = 6, 7
    elif total_streams in range(43, 50):  # 43 to 49
        rows, columns = 7, 7
    elif total_streams in range(50, 61):  # 50 to 60
        rows, columns = 7, 8
    elif total_streams in range(61, 73):  # 61 to 72
        rows, columns = 8, 9
    elif total_streams in range(73, 85):  # 73 to 84
        rows, columns = 9, 9
    elif total_streams in range(85, 97):  # 85 to 96
        rows, columns = 10, 10
    elif total_streams in range(97, 111):  # 97 to 110
        rows, columns = 10, 11
    elif total_streams in range(111, 127):  # 111 to 126
        rows, columns = 11, 12
    elif total_streams in range(127, 144):  # 127 to 143
        rows, columns = 12, 12
    elif total_streams in range(144, 161):  # 144 to 160
        rows, columns = 12, 13
    elif total_streams in range(161, 181):  # 161 to 180
        rows, columns = 13, 14
    elif total_streams in range(181, 202):  # 181 to 201
        rows, columns = 14, 15
    elif total_streams in range(202, 225):  # 202 to 224
        rows, columns = 15, 15
    elif total_streams in range(225, 250):  # 225 to 249
        rows, columns = 15, 16
    elif total_streams in range(250, 277):  # 250 to 276
        rows, columns = 16, 17
    elif total_streams in range(277, 300):  # 277 to 300
        rows, columns = 17, 18
    else:
        rows, columns = 1, 2  

    return rows, columns

########## TRAFFIC_JAM_CONFIG_FUNCTIONS#############

def validate_rois_array(arr,keys_array):
    validation_status=False
    for obj in arr:
        if not validation_status:
            validation_status=validate_each_roi(obj,keys_array)
        else :
          return True
    return validation_status

def validate_each_roi(obj,keys):
        validation_status=True
        for key in keys:
            if obj[key] and not ( obj[key]==''or obj[key]== None  ):
                validation_status=True
            else:
                validation_status=False
                break
        return validation_status
        
def resize_roi(roi_points,width_ratio=1,height_ratio=1):
     points_array=roi_points.split(';')
     points_array=points_array[0:(len(points_array)-1)]
     print(points_array)
     new_resized_points=[]
     for index,point in enumerate(points_array):
         if index%2==0:
             new_resized_points.append(str(math.floor( int(point)*width_ratio)))
         else:
             new_resized_points.append(str(math.floor(int(point)*height_ratio)))
     print(';'.join(new_resized_points))
     return ';'.join(new_resized_points)



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


def get_text_position_within_polygon(text, polygon, font, padding=5):
    """Calculate a valid text position within a polygon."""
    bbox = [min(x for x, y in polygon), min(y for x, y in polygon),
            max(x for x, y in polygon), max(y for x, y in polygon)]
    text_width, text_height =  calculate_text_size(text, 50)
    
    for y in range(bbox[1] + padding, bbox[3] - text_height - padding, 1):
        for x in range(bbox[0] + padding, bbox[2] - text_width - padding, 1):
            text_position = (x, y)
            if is_point_inside_polygon(text_position, polygon):
                return text_position
    
    # Fallback if no position is found (should be rare)
    return (bbox[0] + padding, bbox[1] + padding)




def is_point_inside_polygon(point, polygon):
    """Check if a point is inside a polygon using the ray-casting algorithm."""
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def create_thresholdjson_file(filename):
    data = {
        "threshold":[
            {
                "class": "person",
                "value": "70"
            },
            {
                "class": "vest",
                "value": "50"
            },

            {
                "class": "helmet",
                "value": "50"
            },            
            {
                "class": "crash_helmet",
                "value": '50'
            },
            {
                "class": "fire_smoke_dust",
                "value": '50'
            },
            {
                "class": "bicycle",
                "value": '50'
            },
            {
                "class": "motorbike",
                "value": '50'
            },
            {
                "class": "car",
                "value": '50'
            },
            {
                "class": "bus",
                "value": '50'
            },
            {
                "class": "truck",
                "value": '50'
            },
            {
                "class": "wheel",
                "value": '40'
            }   
            ]
        
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    file.close()




def fetch_configuration_data(filename):
    with open(filename, 'r') as file:
        models_data = json.load(file)
    enabled_model = None
    if models_data is not None:
        enabled_model = models_data
    file.close()
    return enabled_model

def getthreshholdmodelconfig_details():
    json_filename = os.path.join( str(os.getcwd()) + '/' + 'smaple_files', "threshold_config.json")
    if not file_exists(json_filename):
        create_thresholdjson_file(json_filename)
        print(f"JSON file '{json_filename}' created successfully!")
    enabled_data = fetch_configuration_data(json_filename)
    # print(json.dumps(enabled_data, indent=4))
    return enabled_data 

def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
    match = re.search(pattern, password)
    return match is not None

def validate_password1(new_password):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
    match = re.search(pattern, new_password)
    return match is not None    


def scale_bbox(panel_bbox, original_width, original_height, target_width, target_height, increase_factor=1):
    width_scale = (target_width * increase_factor) / original_width
    height_scale = (target_height * increase_factor) / original_height    
    scaled_bbox = [int(coordinate * width_scale) if idx % 2 == 0 else int(coordinate * height_scale) for idx, coordinate in enumerate(panel_bbox)]
    return scaled_bbox



def GETCAMERALICENSE():
    Return = {'total_license':0,'added_cameras_count':0,'remaining_license':0}
    ret = {'message': 'something went wrong with get license_count', 'success': False}
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
    sheet_camera_count = 0
    # print('sheet_data',sheet_data)
    if sheet_data is not None:
        sheet_data_count = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
        unique_iplist = []
        if len(sheet_data_count) !=0:
            for kl , eachElements in enumerate(sheet_data_count):
                if eachElements['ip_address'] not in unique_iplist:
                    unique_iplist.append(eachElements['ip_address'])
            sheet_camera_count= len(unique_iplist) 
        
    CamCount = mongo.db.ppera_cameras.count_documents({})#find()#find_one()#mongo.db.ppera_cameras.find({}).count()
    # print("camera -count ",CamCount)
    # print("sheet_data count",sheet_camera_count)
    # CamCount = CamCount #+ sheet_camera_count
    Total_license = NEWLICENSECOUNT() 
    print("type -------------sheet_camera_count",sheet_camera_count)
    print("count --------------type ==",type(sheet_camera_count))
    Return = {'total_license':Total_license,'added_cameras_count':CamCount+sheet_camera_count,'remaining_license':Total_license-(CamCount+sheet_camera_count)}
    ret['message']=Return
    ret['success']=True
    return ret


def Getipaddresslist(file_path,column_names):
    try:
        try:
            df = pd.read_excel(file_path)
            df = df.dropna(how='all')
            existing_columns = df['IP Address'].tolist()
            existing_columns = [element if isinstance(element, ( str)) else None for element in existing_columns]
            return existing_columns
        except Exception as  error:  
            print("second try for reading excel ====")
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.dropna(how='all')
            existing_columns = df['IP Address'].tolist()
            existing_columns = [(element) if isinstance(element, ( str)) else None for element in existing_columns]
            return existing_columns
    
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
def GETLISTOFIPSEXISTS():
    getdatajobnumberdata = list(mongo.db.ppera_cameras.find({}))
    sheet_data = mongo.db.job_sheet_details.find_one({'status': 1},sort=[('_id', pymongo.DESCENDING)])
    sheet_camera_count = 0
    unique_iplist = []
    print('sheet_data',sheet_data)
    if sheet_data is not None:
        sheet_data_count = list(mongo.db.panel_data.find({'job_sheet_name':sheet_data['job_sheet_name'], 'token': sheet_data['token']}, sort=[('_id', pymongo.DESCENDING)]))
        
        if len(sheet_data_count) !=0:
            for kl , eachElements in enumerate(sheet_data_count):
                if eachElements['ip_address'] not in unique_iplist:
                    unique_iplist.append(eachElements['ip_address'])
    ipADDRESSLIST = []
    if len(getdatajobnumberdata) !=0 :
        for i, eachjobnumber in enumerate(getdatajobnumberdata):
            if 'camera_ip' in eachjobnumber:
                if eachjobnumber['camera_ip'] not in ipADDRESSLIST :
                    ipADDRESSLIST.append(eachjobnumber['camera_ip'])

    if len(unique_iplist) !=0 and len(ipADDRESSLIST) !=0:
        ipADDRESSLIST.extend(unique_iplist)
    return ipADDRESSLIST



def NEWLICENSECOUNT():
    database_detail = {'sql_panel_table':'device_path_table', 'user': 'docketrun', 'password': 'docketrun', 'host':'localhost', 'port': '5432', 'database': 'docketrundb', 'sslmode':'disable'}
    license_status =0
    conn = None
    try:
        conn = psycopg2.connect(user=database_detail['user'], password=  database_detail['password'], 
                                host=database_detail['host'], port =database_detail['port'], database=database_detail['database'],sslmode=database_detail['sslmode'])
    except Exception as error :
        print("*************************8888888888888888888888  POSTGRES CONNECTION ERROR ___________________________________---ERROR ",error )
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICE000NSECOUNT 1", str(error), " ----time ---- ", now_time_with_time()]))
        conn = 0
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM ' + database_detail['sql_panel_table'] + ' ORDER BY insertion_time desc')
    except psycopg2.errors.UndefinedTable as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICEN-==00SECOUNT 2", str(error), " ----time ---- ", now_time_with_time()]))
    except psycopg2.errors.InFailedSqlTransaction as error:
        print('[ERR] from send data encountered error at stage 1 as ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] camera_api -- NEWLICEN009897SECOUNT 3", str(error), " ----time ---- ", now_time_with_time()]))
    l1data_row = cursor.fetchone()
    cols_name = list(map(lambda x: x[0], cursor.description))
    cursor.close()
    conn.close()
    if l1data_row is not None:
        res = dict(zip(cols_name, list(l1data_row)))
        # print('res ===', res)
        # print('device_location', res['device_location'])
        lic = res['device_location']
        split_data=lic.split('_')[1].split("l")
        while '' in split_data:
            split_data.remove('')

        print(split_data[0])
        print(type(split_data[0]))
        # if CamCount < int((split_data[0])):
        license_status = int((split_data[0]))
        # else:
        #     license_status = False    
    return license_status



# def scale_polygon(polygon, original_width, original_height, target_width, target_height, increase_factor=1.1):
#     width_scale = (target_width * increase_factor) / original_width
#     height_scale = (target_height * increase_factor) / original_height
#     scaled_polygon = [(int(x * width_scale), int(y * height_scale)) for x, y in polygon]
#     return scaled_polygon


# def scale_polygon(polygon, original_width, original_height, target_width, target_height, increase_factor=1):
#     # Calculate scaling factors
#     width_scale = (target_width * increase_factor) / original_width
#     height_scale = (target_height * increase_factor) / original_height
    
#     # Scale each point in the polygon
#     scaled_polygon = [(int(x * width_scale), int(y * height_scale)) for x, y in polygon]
#     return scaled_polygon

def scale_polygon(polygon, original_width, original_height, target_width, target_height, increase_factor=1.1):
    width_scale = (target_width * increase_factor) / original_width
    height_scale = (target_height * increase_factor) / original_height
    if len(polygon) % 2 != 0:
        raise ValueError("Polygon should have an even number of coordinates.")
    points = [(polygon[i], polygon[i+1]) for i in range(0, len(polygon), 2)]
    scaled_polygon = [(int(x * width_scale), int(y * height_scale)) for x, y in points]
    return scaled_polygon
# from ultralytics import YOLO
# PANRACKWINDOW = YOLO(os.getcwd()+"/Data_recieving_and_Dashboard/RackDetectionV8_18_02_2024.pt")



# def extract_rw_bbox_details( point_details, img ):
#     img = cv2.resize(img,(960,544))
#     print("=====full_path",img)
#     print("=====point_details",point_details)
#     split_data = point_details.split(";")
#     points = []

#     for i in range( 0, len(split_data)-1 ):
#         if i % 2 == 0:
#             point = (int(split_data[i]), int(split_data[i+1]) )
#             points.append( point )

#     points = np.array(points)
#     x,y,w,h = cv2.boundingRect(points)

#     black_img = np.zeros((544, 960, 3), dtype = np.uint8)
#     cv2.fillConvexPoly(black_img, points, color=(255, 255, 255))
#     print("type of image ==",type(img))
#     # print(",img.shape())--",img.shape())

#     mask = cv2.bitwise_and(black_img, img)

#     pnl = mask[ y:y+h, x:x+w ]

#     results = PANRACKWINDOW.predict( pnl )
    
#     result = results[0]
#     if len(result) !=0 :

#         # for box in result.boxes:
#         class_id = result.names[result.boxes[0].cls[0].item()]
#         cords = result.boxes[0].xyxy[0].tolist()
#         cords = [round(x) for x in cords]
#         conf = round(result.boxes[0].conf[0].item(), 2)
#         if conf > 0.4:
#             # print("Object type:", class_id)
#             print("Coordinates:", cords)
#             # print("Probability:", conf)
#             print("---")

#             # Rackwindowpoints = str(cords[0])+";"+str(cords[1])+";"+str(cords[2]-cords[0])+";"+str(cords[3]-cords[1])+";"
#             Rackwindowpoints = str(cords[0]+x)+";"+str(cords[1]+y)+";"+str(cords[2]+x)+";"+str(cords[3]+y)+";"

#             # cv2.rectangle(pnl,(cords[0],cords[1]),(cords[2],cords[3]),(0,255,0), 2)
#             # cv2.imshow("TEst", pnl)
#             # key = cv2.waitKey(0)

#             return Rackwindowpoints
#         else:
#             return None
#     else:
#         return None

def extract_rw_bbox_details_cv2( point_details, img_path, model_path ):
    IMAGE_READ_RW = False
    try:
        img = cv2.imread( img_path )
        img = cv2.resize( img, (960,544) )
        IMAGE_READ_RW = True
    except:
        print("[Rack-Window ERR] Unable to read the image")
        return None
    try :
        if IMAGE_READ_RW == True:
            split_data = point_details.split(";")
            points = []

            for i in range( 0, len(split_data)-1 ):
                if i % 2 == 0:
                    point = (int(split_data[i]), int(split_data[i+1]) )
                    points.append( point )

            points = np.array(points)
            ox,oy,ow,oh = cv2.boundingRect(points)

            black_img = np.zeros((544, 960, 3), dtype = np.uint8)
            cv2.fillConvexPoly(black_img, points, color=(255, 255, 255))

            mask = cv2.bitwise_and(black_img, img)

            pnl = mask[ oy:oy+oh, ox:ox+ow ]

            if os.path.exists( model_path ):
                net = cv2.dnn.readNet( model_path )
                net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

                INPUT_WIDTH = 640
                INPUT_HEIGHT = 640
                SCORE_THRESHOLD = 0.2
                NMS_THRESHOLD = 0.4
                CONFIDENCE_THRESHOLD = 0.4

                blob = cv2.dnn.blobFromImage(pnl, 1/255.0, (INPUT_WIDTH, INPUT_HEIGHT), swapRB=True, crop=False)
                net.setInput(blob)
                preds = net.forward()
                preds = preds.transpose((0, 2, 1))

                # Extract output detection
                class_ids, confs, boxes = list(), list(), list()

                image_height, image_width, _ = pnl.shape
                x_factor = image_width / INPUT_WIDTH
                y_factor = image_height / INPUT_HEIGHT

                rows = preds[0].shape[0]

                CLASESS = ['rw']

                for i in range(rows):
                    row = preds[0][i]
                    conf = row[4]
                    
                    classes_score = row[4:]
                    _,_,_, max_idx = cv2.minMaxLoc(classes_score)
                    class_id = max_idx[1]
                    if (classes_score[class_id] > .20):
                        confs.append(conf)
                        label = CLASESS[int(class_id)]
                        class_ids.append(label)
                        
                        #extract boxes
                        x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item() 
                        left = int((x - 0.5 * w) * x_factor)
                        top = int((y - 0.5 * h) * y_factor)
                        width = int(w * x_factor)
                        height = int(h * y_factor)
                        box = np.array([left, top, width, height])
                        boxes.append(box)

                indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.20, 0.45)
                if len(indexes) != 0:
                    box = boxes[indexes[0]]
                    left = int(box[0])
                    top = int(box[1])
                    width = int(box[2])
                    height = int(box[3])

                    ret_str = str( int(ox+left) )+ ";" + str( int(oy+top) ) + ";" + str( int(ox+left+width) ) + ";" + str( int(oy+top+height) ) + ";"
                    return ret_str
                else:
                    None
            else:
                print("[Rack-Window ERR] Unable to find the model")
                return None
    except :
        return None


def ERRORLOGdata(message):
    with open("ALL_API_ERROR.log", "a") as f:
        f.write(message+"\n")


########################################################### docketrun start stop application functions ##########################
def hooter_time_set():
    delay_time = 3
    data = mongo.db.hooter_timeset_table.find_one()
    if data is not None:
        delay_time = data['hooter_time_delay']
    else:
        mongo.db.hooter_timeset_table.insert_one({'hooter_time_delay':delay_time})
        delay_time = delay_time
    return delay_time

def set_the_data_in_app_status():
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started':  True, "smrec":True, "hydra_app":True , "phaseone_app":True ,'firesmokeapp':True,'vpms':True, 'system_restart': False, 'esi_sleep_time': 10,  'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    print('dictionary -- ', dict11)
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        print(hooter_on_of)
    else:
        mongo.db.docket_app_status.insert_one(dict11)
    return '1'

def esi_app_get_ESI_monitoring_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'esi_monitoring_started':
                ret_val = val
    else:
        pass
    return ret_val

def esi_app_get_Enable_system_restart():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        print(hooter_on_of)
        for key, val in hooter_on_of.items():
            if key == 'system_restart':
                ret_val = val
    else:
        pass
    return ret_val

def esi_app_get_sleep_time():
    ret_val = 0
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'esi_sleep_time':
                ret_val = val
    else:
        pass
    return ret_val

def esi_app_set_ESI_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started': True, "smrec":True,"hydra_app":True , "phaseone_app":True,'firesmokeapp':True,'vpms':True, 'system_restart': False, 'esi_sleep_time': 10, 'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id)}, {'$set': {'esi_monitoring_started': val, 'esi_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count esi --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)




def esi_app_set_STEAMSUIT_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started': True, "smrec":True,"hydra_app":True , "phaseone_app":True,'vpms':True, 'system_restart': False, 'esi_sleep_time': 10, 'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id)}, {'$set': {'steamsuit': val, 'esi_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count esi --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)

########################phase one #######################
def get_phaseone_app_monitoring_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'phaseone_app':
                ret_val = val
    else:
        pass
    return ret_val


def get_phaseone_app_Enable_system_restart():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'system_restart':
                ret_val = val
    else:
        pass
    return ret_val


def phaseone_app_get_sleep_time():
    ret_val = 0
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'docketrun_app_sleep_time':
                ret_val = val
    else:
        pass
    return ret_val


def app_set_phaseoneapp_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started':  True,"phaseone_app":True,"smrec":True,"hydra_app":True,'firesmokeapp':True,'vpms':True,  'system_restart': False, 'esi_sleep_time': 10,  'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id) }, {'$set': {'phaseone_app': val,'docketrun_app_started':  val,'docketrun_app_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count phaseone app --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)


def app_set_VPMS_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started':True,"phaseone_app":True,"smrec":True,"hydra_app":True,'firesmokeapp':True, 'vpms':True, 'system_restart': False, 'esi_sleep_time': 10,  'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id) }, {'$set': {'vpms': val,'docketrun_app_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count app_set_VPMS_monitoring_started app --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)



##################################### smart record ##############################
def get_SMART_RECORDING_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'smrec':
                ret_val = val
    else:
        pass
    return ret_val

def get_SMART_RECORDING_Enable_system_restart():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        print(hooter_on_of)
        for key, val in hooter_on_of.items():
            if key == 'system_restart':
                ret_val = val
    else:
        pass
    return ret_val

def SMART_RECORDING_get_sleep_time():
    ret_val = 0
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'esi_sleep_time':
                ret_val = val
    else:
        pass
    return ret_val


def SET_SMART_RECORDING_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started': True, "smrec":True,"hydra_app":True, "phaseone_app":True ,'firesmokeapp':True, 'vpms':True,'system_restart': False, 'esi_sleep_time': 10, 'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id)}, {'$set': {'smrec': val, 'esi_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count smrec --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)

################################## hydra application ########################
def get_HYDRAAPP_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'hydra_app':
                ret_val = val
    else:
        pass
    return ret_val

def get_HYDRAAPP_Enable_system_restart():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        print(hooter_on_of)
        for key, val in hooter_on_of.items():
            if key == 'system_restart':
                ret_val = val
    else:
        pass
    return ret_val

def HYDRAAPP_get_sleep_time():
    ret_val = 0
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'esi_sleep_time':
                ret_val = val
    else:
        pass
    return ret_val


def SET_HYDRAAPP_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started': True, "smrec":True,"hydra_app":True,  "phaseone_app":True ,'firesmokeapp':True,'vpms':True,'system_restart': False, 'esi_sleep_time': 10, 'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id)}, {'$set': {'hydra_app': val, 'esi_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count hydra --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)


    

############################# mongodb service functions #######################
def check_the_status_mongodb_service():
    mongodb_r_status_filename = 'mongodb_rtatusoutput.txt'
    try:
        result = os.system('service mongod status > '+mongodb_r_status_filename)
        if result == 0:
            if os.path.exists(mongodb_r_status_filename):
                fp = open(mongodb_r_status_filename, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_r_status_filename)
                if "Active: active (running)" in output :
                    return True
                else:
                    return False
            else:
                return False
        else:
            result1 = os.system('service mongodb status > '+mongodb_r_status_filename)
            if result1 == 0:
                if os.path.exists(mongodb_r_status_filename):
                    fp = open(mongodb_r_status_filename, "r")
                    output = fp.read()
                    fp.close()
                    os.remove(mongodb_r_status_filename)
                    print(output)
                    if "Active: active (running)" in output :
                        return True
                    else:
                        return False
                else:
                    return False
            return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- check_the_status_mongodb_service 1", str(error), " ----time ---- ", now_time_with_time()]))
        return False
    


def restart_mongodb_r_service():
    try:
        if check_the_status_mongodb_service():
            print("mongodb service already running")
            return True
            
        else:
            result = os.system('echo "docketrun" | sudo -S service mongod restart')
            if result == 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                result1 = os.system('echo "docketrun" | sudo -S service mongodb restart')
                if result1== 0:
                    if check_the_status_mongodb_service():
                        return True
                    else:
                        return False
                else:
                    return False
            
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- restart_mongodb_r_service 1", str(error), " ----time ---- ", now_time_with_time()]))        
        return False
    

def forcerestart_mongodb_r_service():
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod restart')
        if result == 0:
            if check_the_status_mongodb_service():
                return True
            else:
                return False
        else:
            result1 = os.system('echo "docketrun" | sudo -S service mongodb restart')
            if result1== 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                return False            
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- forcerestart_mongodb_r_service 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return False
    
# print("forcerestart_mongodb_r_service",forcerestart_mongodb_r_service())
# print("s()",restart_mongodb_r_service())
def start_mongodb_r_service():
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod start ')
        if result == 0:
            if check_the_status_mongodb_service():
                return True
            else:
                return False
        else:
            result = os.system('echo "docketrun" | sudo -S service mongodb start ')
            if result == 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- start_mongodb_r_service 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return False
    

def stop_mongodb_service():
    try:#sudo service mongod stop
        result = os.system('echo "docketrun" | sudo -S service mongod stop')
        if result == 0:
            if check_the_status_mongodb_service():
                return True
            else:
                return False
        else:
            result1 = os.system('echo "docketrun" | sudo -S service mongodb stop')
            if result1 == 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_mongodb_service 1", str(error), " ----time ---- ", now_time_with_time()]))       
        return False
    
def enable_mongodb_r_service_to_system():
    mongodb_r_status_filename = 'mongodb_rtatusenableoutput.txt'
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod enable  > '+mongodb_r_status_filename)
        if result == 0:
            if os.path.exists(mongodb_r_status_filename):
                fp = open(mongodb_r_status_filename, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_r_status_filename)
                print(output)
                return True
            else:
                return False
        else:
            result = os.system('echo "docketrun" | sudo -S service mongodb enable  > '+mongodb_r_status_filename)
            if result == 0:
                if os.path.exists(mongodb_r_status_filename):
                    fp = open(mongodb_r_status_filename, "r")
                    output = fp.read()
                    fp.close()
                    os.remove(mongodb_r_status_filename)
                    print(output)
                    return True
                else:
                    return False
            else:
                return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- enable_mongodb_r_service_to_system 1", str(error), " ----time ---- ", now_time_with_time()]))      
        return False
    
def disable_mongodb_r_service_to_system():
    mongodb_r_status_filename = 'mongodb_rtatusdisableoutput.txt'
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod disable  > '+mongodb_r_status_filename)
        if result == 0:
            if os.path.exists(mongodb_r_status_filename):
                fp = open(mongodb_r_status_filename, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_r_status_filename)
                print(output)
                return True
            else:
                return False
        else:
            return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- disable_mongodb_r_service_to_system 1", str(error), " ----time ---- ", now_time_with_time()]))      
        return False
    


def check_the_mongodb_r_installed_version():
    mongodb_rversion_file = "mongodb_rversion.txt"
    try:
        result = os.system('mongod --version> '+mongodb_rversion_file)#('echo "docketrun" | sudo -S service mongod disable  > '+mongodb_rversion_file)
        if result == 0:
            if os.path.exists(mongodb_rversion_file):
                fp = open(mongodb_rversion_file, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_rversion_file)
                print(output)
                return True
            else:
                return False
        else:
            result2 = os.system('mongod -V> '+mongodb_rversion_file)
            if result2 ==0:
                if os.path.exists(mongodb_rversion_file):
                    fp = open(mongodb_rversion_file, "r")
                    output = fp.read()
                    fp.close()
                    os.remove(mongodb_rversion_file)
                    print(output)
                    return True
                else:

                    return False
            else:
                result2 = os.system('mongodb --version > '+mongodb_rversion_file)
                if result2 ==0:
                    if os.path.exists(mongodb_rversion_file):
                        fp = open(mongodb_rversion_file, "r")
                        output = fp.read()
                        fp.close()
                        os.remove(mongodb_rversion_file)
                        print(output)
                        return True
                    else:

                        return False
                else:
                    result3 = os.system('mongodb -V> '+mongodb_rversion_file)
                    if result3 ==0:
                        if os.path.exists(mongodb_rversion_file):
                            fp = open(mongodb_rversion_file, "r")
                            output = fp.read()
                            fp.close()
                            os.remove(mongodb_rversion_file)
                            print(output)
                            return True
                        else:
                            return False
                    else:
                        return False
    except Exception as error:
        return False
    
####################once again #################
####################################### ESI realated functions ################
def MULTIKEYSREMOVING(i, data):
    if i in data:
        return False
    else:
        if isEmpty(i['data']):
            i = delete_keys_from_dict(i, ['ip_status', 'panel', 'sheet_status'])
            camera_data = i['data']
            camera_data = delete_keys_from_dict(camera_data, ['camera_brand','rtsp_status', 'inserted_time', 'camera_id'])
            i['data'] = camera_data
    return i


def REPATATIVERIRODATA(i, data):
    if i in data:
        return False
    else:
        if isEmpty(i['data']):
            i = delete_keys_from_dict(i, ['ip_status', 'panel', 'sheet_status'])
            camera_data = i['data']
            camera_data = delete_keys_from_dict(camera_data, ['camera_brand','rtsp_status', 'inserted_time'])
            i['data'] = camera_data
    return i


def MUlRIRODATACMECH(i, data):
    if i in data:
        return False
    else:
        if isEmpty(i['data']):
            i = delete_keys_from_list_of_dict_multi_isolation(i, ['ip_status', 'sheet_status'])
            camera_data = i['data']
            camera_data = delete_keys_from_list_of_dict_multi_isolation(camera_data, ['camera_brand','rtsp_status', 'inserted_time'])
            i['data'] = camera_data
    return i


def DELETINGCAMERABRANDRTSP(data):
    return_data = []
    for count, i in enumerate(data):
        i = delete_keys_from_dict(i, ['camera_brand', 'rtsp_status', 'inserted_time', 'camera_id'])
        return_data.append(i)
    return return_data

#########################ppe related functions ####################
def object_data_keys(object_data):
    showcase_keys = []
    keys_required = ['Vest', 'Helmet']
    for ij in object_data:
        for xx in ij.keys():
            if xx in keys_required:
                if xx not in showcase_keys:
                    showcase_keys.append(xx)
    return showcase_keys

#################################ALPHANUMERIC TOKEN GENERATION FUNCTIONS #############
def genarate_alphanumeric_key():
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(200))
    return key


def genarate_alphanumeric_key_for_riro_data():
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(25))
    return key


def GENERATEALPHANUMERICKEYFOREXCELTEST50():
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(50))
    return key

############################ dict and json #############################
def read_json_for_roi(json_fileName):
    with open(json_fileName, 'r') as f:
        data = json.load(f)
    return data

def parse_json(data):
    return json.loads(json_util.dumps(data))


def parse_json_dictionary(data):
    return json_util.dumps(data)


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def isEmpty(dictionary):
    for element in dictionary:
        if element:
            return True
        return False
    
def check_dictionaryishavinganynonevalue(dictionary):
    dictionary_status = True
    for element in dictionary:
        if element is None or element ==' ':
            dictionary_status= True
    return dictionary_status

def check_arraydictionaryishavinganynonevalue(dictionary):
    # print("ajdasdjfk", dictionary)
    dictionary_status = True
    for dic in dictionary:
        if any([v==None for v in dic.values()]):
            dictionary_status= False
            break
    return dictionary_status

def delete_keys_from_dict(dictionary, keys):
    keys_set = set(keys)
    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict

def delete_keys_from_list_of_dict_multi_isolation(list_of_dict, keys):
    keys_set = set(keys)
    modified_dict = {}
    if type(list_of_dict) == list:
        for mirror in list_of_dict:
            dictionary = mirror
            for key, value in dictionary.items():
                if key not in keys_set:
                    if isinstance(value, MutableMapping):
                        modified_dict[key] = delete_keys_from_dict(value, keys_set)
                    else:
                        modified_dict[key] = value
    elif type(list_of_dict) == dict:
        dictionary = list_of_dict 
        for key, value in dictionary.items():
            if key not in keys_set:
                if isinstance(value, MutableMapping):
                    modified_dict[key] = delete_keys_from_dict(value, keys_set)
                else:
                    modified_dict[key] = value
    return modified_dict


def dictionary_key_exists(dictionary,key):
    if key in dictionary.keys():
        return True
    else:
        return False

############################ relative path functions ###################
def get_current_dir_and_goto_parent_dir():
    return os.path.dirname(os.getcwd())


def parent_directory_grandpa_dir():
    relative_parent = os.path.join(os.getcwd(), "../..") 
    return os.path.abspath(relative_parent)


##################CREAT FOLDER AND FILES #################
def create_multiple_dir(path):
    os.makedirs(path, exist_ok=True)

def handle_uploaded_file(target_dir):
    os.umask(0)
    os.makedirs(target_dir, mode=511, exist_ok=True)


def try_chmod_command(file):
    os.chmod(file, 511)


"""VERIFY FILE IS EXCEL OR NOT"""
def CHECKEXCELFILEEXTENTION(filename):
    """check the file format using endswith fun"""
    excel_formats = [".xls", ".ods", ".csv", ".xlsx", ".xlsm", ".xltx",".xltm"]
    res = []
    for f in excel_formats:
        x = filename.endswith(f)
        res.append(x)
    if True in res:
        return True    
    else:
        return False



############################ CAMERA AND RTSP RELATED  FUNCTION  ####################
# #Function to check rtsp is online or not
def check_rtsp_is_working(url):
    verfy_rtsp_response = False
    cam = cv2.VideoCapture(url)
    if cam.isOpened() == True:
        verfy_rtsp_response = True
    else:
        verfy_rtsp_response = False
    cam.release()
    #cv2.destroyAllWindows()
    return verfy_rtsp_response
# #Function to check rtsp is online or not
def CHECKRTSPWORKINGORNOT(url):
    cam = cv2.VideoCapture(url)
    if cam.isOpened() == True:
        while(cam.isOpened()):
            ret,frame = cam.read()
            if ret:
                return "rtsp_working"
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()        
    else:
        return "rtsp_not_working"   


# def ESIBRANDCAMERASRTSP(camera_ip_address,  camera_brand ,camera_username='admin', camera_password='TATA_tsk123'):
#     channelNo='1'
#     # camera_username='admin'
#     # camera_password='TATA_tsk123'
#     port='554'
#     # if 1:
#     try:
#         if channelNo == 'None' or port == 'None':
#             if camera_brand == 'dahua':
#                 url = ('rtsp' + ':' + '//' + camera_username + ':'  +  camera_password + '@' + camera_ip_address + ':'  +  '554/cam/realmonitor?channel=1&subtype=0')
#             elif camera_brand == 'hikvision':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':'  +  '554/Streaming/Channels/101')
#             elif camera_brand == 'samsung':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/profile1/media.smp')
#             elif camera_brand == 'cp_plus':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':'  +  '/cam/realmonitor?channel=1&subtype=0')
#             elif camera_brand == 'bosch':
#                 if camera_username is None and camera_password is None:
#                     url = 'rtsp://' + camera_ip_address + '/'
#                 else:
#                     url ='rtsp://'  +camera_username+":"+camera_password+'@'+camera_ip_address +':554' +'/cam/realmonitor?channel=1&subtype=0'
#                     #url = ('rtsp://' + camera_ip_address + ':554'  +      '/user=' + camera_username + '&password='  +      camera_password + '&channel=1&stream=0.sdp?')
#             elif camera_brand == 'pelco':
#                 if camera_username is None and camera_password is None:
#                     url = 'rtsp://' + camera_ip_address + '/'
#                 else:
#                     #rtsp://admin:TATA_tsk123@10.152.182.103/stream1
#                     url = 'rtsp://'+camera_username +':'+camera_password+"@"+ camera_ip_address + ':' + port  +  '/stream1'
#             # url = 'rtsp://' + camera_ip_address + '/stream1'
#                 # url = 'rtsp://' + camera_ip_address + '/stream1'
#             elif camera_brand == 'uniview':
#                 url = 'rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/media/video1'
#             elif camera_brand == 'univision':
#                 url = 'rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/unicast/ch1/s0/live'
#             elif camera_brand == 'secur_eye':
#                 url = 'rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address  +  '/user=admin_password=admin_channel=1_stream=0.sdp'
#             elif camera_brand == 'axis':
#                 url = 'rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/axis-media/media.amp'
#             elif camera_brand == 'geovision':
#                 url = "rtsp://" + camera_username + ':' + camera_password  +  '@' + camera_ip_address +"/media/video1"
#             elif camera_brand == 'honeywell':
#                 url = 'NOT defined '
#             elif camera_brand == 'hixecure':
#                 url = "rtsp://" +camera_username + + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/ch0_0.264'
#             elif camera_brand == 'hifocus':
#                 url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/ch0_0.264'            
#             elif camera_brand=='ganz':
#                 url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/snl/live/1/1'  
#             elif camera_brand == 'docketrun':
#                 url = "rtsp://"+ camera_ip_address + ':8554/ds-test'
#             else:
#                 return False
#         elif camera_brand == 'dahua':
#             url ='rtsp' + ':' + '//' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) +'/cam/realmonitor?channel=' + channelNo + '&subtype=0'
#         elif camera_brand == 'hikvision':
#             url = 'rtsp://' + camera_username + ':' + camera_password +'@' + camera_ip_address + ':' + str(port) +'/Streaming/Channels/101'
#         elif camera_brand == 'samsung':
#             url = 'rtsp://' + camera_username + ':' + camera_password +'@' + camera_ip_address + ':' + port + '/profile1/media.smp'
#         elif camera_brand == 'cp_plus':
#             url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) +'/cam/realmonitor?channel=' + channelNo + '&subtype=0'
#         elif camera_brand == 'bosch':
#             if camera_username is None and camera_password is None:
#                 url = 'rtsp://' + camera_ip_address + '/'
#             else:
#                 url ='rtsp://'  +camera_username+":"+camera_password+'@'+camera_ip_address +':554' +'/cam/realmonitor?channel=1&subtype=0'
#                 # url = 'rtsp://' + camera_ip_address + ':' + port  +  '/user=' + camera_username + '&password='  +  camera_password + '&channel=' + channelNo  +  '&stream=0.sdp?'
#         elif camera_brand == 'pelco':
#             if camera_username is None and camera_password is None:
#                 url = 'rtsp://' + camera_ip_address + '/'
#             else:
#                 #rtsp://admin:TATA_tsk123@10.152.182.103/stream1
#                 url = 'rtsp://'+camera_username +':'+camera_password+"@"+ camera_ip_address + ':' + port  +  '/stream1'
#             # url = 'rtsp://' + camera_ip_address + '/stream1'
#         elif camera_brand == 'uniview':
#             if camera_username is None and camera_password is None:
#                 url = 'rtsp://' + 'admin' + ':' + 'admin123' + '@'  +  camera_ip_address + ':' + str(port) + '/media/video1'
#             else:
#                 url = 'rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + str(port) + '/media/video1'
#         elif camera_brand == 'univision':
#             url = 'rtsp://' + camera_username + ':' + camera_password +'@' + camera_ip_address + ':' + str(port) + '/unicast/ch' + str(channelNo) + '/s0/live'
#         elif camera_brand == 'secur_eye':
#             url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address +  '/user=admin_password=admin_channel=' + str(channelNo) +'_stream=0.sdp'
#         elif camera_brand == 'axis':
#             url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/axis-media/media.amp'
#         elif camera_brand == 'geovision':
#                 url = "rtsp://" + camera_username + ':' + camera_password  +  '@' + camera_ip_address +"/media/video1"                
#         elif camera_brand == 'honeywell':
#             url = 'NOT defined '
#         elif camera_brand == 'hixecure':
#             url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + str(port) +'/ch0_0.264'
#         elif camera_brand == 'hifocus':
#             url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + str(port) +'/ch0_0.264'
#         elif camera_brand=='ganz':
#                 url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/snl/live/1/1'
#         elif camera_brand == 'docketrun':
#             url = "rtsp://"+ camera_ip_address +':'+str(port) +'/ds-test'
#         else:
#             return False
#         return url
#     except Exception as error:
#         print(error)
#         ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- create_rtsp_for34_all_brand 1", str(error), " ----time ---- ", now_time_with_time()]))         
#         return False



def ESIBRANDCAMERASRTSP(camera_ip_address, camera_brand, camera_username='admin', camera_password='TATA_tsk123'):
    channelNo = '1'
    port = '554'

    try:
        if channelNo == 'None' or port == 'None':
            if camera_brand == 'dahua':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/cam/realmonitor?channel=1&subtype=0'
            elif camera_brand == 'hikvision':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/Streaming/Channels/101'
            elif camera_brand == 'samsung':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/profile1/media.smp'
            elif camera_brand == 'cp_plus':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/cam/realmonitor?channel=1&subtype=0'
            elif camera_brand == 'bosch':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/cam/realmonitor?channel=1&subtype=0' if camera_username and camera_password else f'rtsp://{camera_ip_address}/'
            elif camera_brand == 'pelco':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/stream1' if camera_username and camera_password else f'rtsp://{camera_ip_address}/'
            elif camera_brand == 'uniview':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/media/video1'
            elif camera_brand == 'univision':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/unicast/ch1/s0/live'
            elif camera_brand == 'secur_eye':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/user=admin_password=admin_channel=1_stream=0.sdp'
            elif camera_brand == 'axis':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/axis-media/media.amp'
            elif camera_brand == 'geovision':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/media/video1'
            elif camera_brand == 'honeywell':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/Streaming/Channels/101'
            elif camera_brand == 'aviron':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/cam/realmonitor?channel=1&subtype=0'
            elif camera_brand == 'hixecure':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/ch0_0.264'
            elif camera_brand == 'hifocus':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/ch0_0.264'
            elif camera_brand == 'ganz':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/snl/live/1/1'
            elif camera_brand == 'docketrun':
                url = f'rtsp://{camera_ip_address}:8554/ds-test'
            else:
                return False
        else:
            if camera_brand == 'dahua':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/cam/realmonitor?channel={channelNo}&subtype=0'
            elif camera_brand == 'hikvision':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/Streaming/Channels/101'
            elif camera_brand == 'samsung':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/profile1/media.smp'
            elif camera_brand == 'cp_plus':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/cam/realmonitor?channel={channelNo}&subtype=0'
            elif camera_brand == 'bosch':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/cam/realmonitor?channel=1&subtype=0' if camera_username and camera_password else f'rtsp://{camera_ip_address}/'
            elif camera_brand == 'pelco':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/stream1' if camera_username and camera_password else f'rtsp://{camera_ip_address}/'
            elif camera_brand == 'uniview':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/media/video1' if camera_username and camera_password else f'rtsp://admin:admin123@{camera_ip_address}:{port}/media/video1'
            elif camera_brand == 'univision':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/unicast/ch{channelNo}/s0/live'
            elif camera_brand == 'secur_eye':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/user=admin_password=admin_channel={channelNo}_stream=0.sdp'
            elif camera_brand == 'axis':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/axis-media/media.amp'
            elif camera_brand == 'geovision':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/media/video1'
            elif camera_brand == 'honeywell':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/Streaming/Channels/101'
            elif camera_brand == 'aviron':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/cam/realmonitor?channel={channelNo}&subtype=0'
            elif camera_brand == 'hixecure':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/ch0_0.264'
            elif camera_brand == 'hifocus':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/ch0_0.264'
            elif camera_brand == 'ganz':
                url = f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:554/snl/live/1/1'
            elif camera_brand == 'docketrun':
                url = f'rtsp://{camera_ip_address}:{port}/ds-test'
            else:
                return False
        return url
    except Exception as error:
        print(error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- ESIBRANDCAMERASRTSP", str(error), " ----time ---- ", now_time_with_time()]))
        return False


############# for all brands 
# def create_rtsp_for_all_brand(camera_ip_address, channelNo='1',camera_username='admin', camera_password='TATA_tsk123', camera_brand = 'hikvision', port='554'):
#     try:
#         if channelNo == 'None' or port == 'None':
#             if camera_brand == 'dahua':
#                 url = ('rtsp' + ':' + '//' + camera_username + ':'  +  camera_password + '@' + camera_ip_address + ':'  +  '554/cam/realmonitor?channel=1&subtype=0')
#             elif camera_brand == 'hikvision':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':'  +  '554/Streaming/Channels/101')
#             elif camera_brand == 'samsung':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/profile1/media.smp')
#             elif camera_brand == 'cp_plus':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':'  +  '/cam/realmonitor?channel=1&subtype=0')
#             elif camera_brand == 'bosch':
#                 if camera_username is None and camera_password is None:
#                     url = 'rtsp://' + camera_ip_address + '/'
#                 else:
#                     url ='rtsp://'  +camera_username+":"+camera_password+'@'+camera_ip_address +':554' +'/cam/realmonitor?channel=1&subtype=0'
#                     #url = ('rtsp://' + camera_ip_address + ':554'  +      '/user=' + camera_username + '&password='  +      camera_password + '&channel=1&stream=0.sdp?')
#             elif camera_brand == 'pelco':
#                 if camera_username is None and camera_password is None:
#                     url = 'rtsp://' + camera_ip_address + '/'
#                 else:
#                     #rtsp://admin:TATA_tsk123@10.152.182.103/stream1
#                     url = ('rtsp://'+camera_username +':'+camera_password+"@"+ camera_ip_address + ':' + port  +  '/stream1')
#             # url = 'rtsp://' + camera_ip_address + '/stream1'
#                 # url = 'rtsp://' + camera_ip_address + '/stream1'
#             elif camera_brand == 'uniview':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/media/video1')
#             elif camera_brand == 'univision':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/unicast/ch1/s0/live')
#             elif camera_brand == 'secur_eye':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address  +  '/user=admin_password=admin_channel=1_stream=0.sdp')
#             elif camera_brand == 'axis':
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/axis-media/media.amp')
#             elif camera_brand == 'geovision':
#                 url = "rtsp://" + camera_username + ':' + camera_password  +  '@' + camera_ip_address +"/media/video1"
#             elif camera_brand == 'honeywell':
#                 url = 'NOT defined '
#             elif camera_brand == 'hixecure':
#                 url = "rtsp://" +camera_username + + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/ch0_0.264'
#             elif camera_brand == 'hifocus':
#                 url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/ch0_0.264'

#             elif camera_brand=='ganz':
#                 url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/snl/live/1/1'
#             elif camera_brand == 'docketrun':
#                 url = "rtsp://"+ camera_ip_address + ':8554/ds-test'
#             else:
#                 return False
#         elif camera_brand == 'dahua':
#             url = ('rtsp' + ':' + '//' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) +'/cam/realmonitor?channel=' + channelNo + '&subtype=0')
#         elif camera_brand == 'hikvision':
#             url = ('rtsp://' + camera_username + ':' + camera_password +'@' + camera_ip_address + ':' + str(port) +'/Streaming/Channels/101')
#         elif camera_brand == 'samsung':
#             url = ('rtsp://' + camera_username + ':' + camera_password +'@' + camera_ip_address + ':' + port + '/profile1/media.smp')
#         elif camera_brand == 'cp_plus':
#             url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) +'/cam/realmonitor?channel=' + channelNo + '&subtype=0')
#         elif camera_brand == 'bosch':
#             if camera_username is None and camera_password is None:
#                 url = 'rtsp://' + camera_ip_address + '/'
#             else:
#                 url ='rtsp://'  +camera_username+":"+camera_password+'@'+camera_ip_address +':554' +'/cam/realmonitor?channel=1&subtype=0'
#                 #url = ('rtsp://' + camera_ip_address + ':' + port  +  '/user=' + camera_username + '&password='  +  camera_password + '&channel=' + channelNo  +  '&stream=0.sdp?')
#         elif camera_brand == 'pelco':
#             if camera_username is None and camera_password is None:
#                 url = 'rtsp://' + camera_ip_address + '/'
#             else:
#                 url = ('rtsp://'+camera_username +':'+camera_password+"@"+ camera_ip_address + ':' + port  +  '/stream1')
#         elif camera_brand == 'uniview':
#             if camera_username is None and camera_password is None:
#                 url = ('rtsp://' + 'admin' + ':' + 'admin123' + '@'  +  camera_ip_address + ':' + str(port) + '/media/video1')
#             else:
#                 url = ('rtsp://' + camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + str(port) + '/media/video1')
#         elif camera_brand == 'univision':
#             url = ('rtsp://' + camera_username + ':' + camera_password +'@' + camera_ip_address + ':' + str(port) + '/unicast/ch' + str(channelNo) + '/s0/live')
#         elif camera_brand == 'secur_eye':
#             url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address +  '/user=admin_password=admin_channel=' + str(channelNo) +'_stream=0.sdp')
#         elif camera_brand == 'axis':
#             url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/axis-media/media.amp')
#         elif camera_brand == 'geovision':
#                 url = "rtsp://" + camera_username + ':' + camera_password  +  '@' + camera_ip_address +"/media/video1"                
#         elif camera_brand == 'honeywell':
#             url = 'NOT defined '
#         elif camera_brand == 'hixecure':
#             url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + str(port) +'/ch0_0.264'
#         elif camera_brand == 'hifocus':
#             url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + str(port) +'/ch0_0.264'
#         elif camera_brand=='ganz':
#             url = "rtsp://" +camera_username + ':' + camera_password  +  '@' + camera_ip_address + ':' + '554/snl/live/1/1'
#         elif camera_brand == 'docketrun':
#             url = "rtsp://"+ camera_ip_address +':'+str(port) +'/ds-test'
#         else:
#             return False
#         return url
#     except Exception as error:
#         print(error)
#         ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- create_rtsp_for_all2_brand 1", str(error), " ----time ---- ", now_time_with_time()]))         
#         return False


def create_rtsp_for_all_brand(camera_ip_address, channelNo='1', camera_username='admin', camera_password='TATA_tsk123', camera_brand='hikvision', port='554'):
    try:
        if channelNo == 'None' or port == 'None':
            if camera_brand == 'dahua':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/cam/realmonitor?channel=1&subtype=0')
            elif camera_brand == 'hikvision':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/Streaming/Channels/101')
            elif camera_brand == 'samsung':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/profile1/media.smp')
            elif camera_brand == 'cp_plus':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/cam/realmonitor?channel=1&subtype=0')
            elif camera_brand == 'bosch':
                if camera_username is None and camera_password is None:
                    url = 'rtsp://' + camera_ip_address + '/'
                else:
                    url = 'rtsp://' + camera_username + ":" + camera_password + '@' + camera_ip_address + ':554/cam/realmonitor?channel=1&subtype=0'
            elif camera_brand == 'pelco':
                if camera_username is None and camera_password is None:
                    url = 'rtsp://' + camera_ip_address + '/'
                else:
                    url = 'rtsp://' + camera_username + ':' + camera_password + "@" + camera_ip_address + ':554/stream1'
            elif camera_brand == 'uniview':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/media/video1'
            elif camera_brand == 'univision':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/unicast/ch1/s0/live'
            elif camera_brand == 'secur_eye':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + '/user=admin_password=admin_channel=1_stream=0.sdp'
            elif camera_brand == 'axis':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/axis-media/media.amp'
            elif camera_brand == 'geovision':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + '/media/video1'
            elif camera_brand == 'honeywell':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/honeywell/stream'
            elif camera_brand == 'hixecure':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/ch0_0.264'
            elif camera_brand == 'hifocus':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/ch0_0.264'
            elif camera_brand == 'ganz':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/snl/live/1/1'
            elif camera_brand == 'docketrun':
                url = 'rtsp://' + camera_ip_address + ':8554/ds-test'
            elif camera_brand == 'aviron':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':554/aviron/stream'
            else:
                return False
        else:
            if camera_brand == 'dahua':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/cam/realmonitor?channel=' + channelNo + '&subtype=0')
            elif camera_brand == 'hikvision':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/Streaming/Channels/101')
            elif camera_brand == 'samsung':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + port + '/profile1/media.smp')
            elif camera_brand == 'cp_plus':
                url = ('rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/cam/realmonitor?channel=' + channelNo + '&subtype=0')
            elif camera_brand == 'bosch':
                if camera_username is None and camera_password is None:
                    url = 'rtsp://' + camera_ip_address + '/'
                else:
                    url = 'rtsp://' + camera_username + ":" + camera_password + '@' + camera_ip_address + ':554/cam/realmonitor?channel=1&subtype=0'
            elif camera_brand == 'pelco':
                if camera_username is None and camera_password is None:
                    url = 'rtsp://' + camera_ip_address + '/'
                else:
                    url = 'rtsp://' + camera_username + ':' + camera_password + "@" + camera_ip_address + ':' + port + '/stream1'
            elif camera_brand == 'uniview':
                if camera_username is None and camera_password is None:
                    url = 'rtsp://' + 'admin' + ':' + 'admin123' + '@' + camera_ip_address + ':' + str(port) + '/media/video1'
                else:
                    url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/media/video1'
            elif camera_brand == 'univision':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/unicast/ch' + str(channelNo) + '/s0/live'
            elif camera_brand == 'secur_eye':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + '/user=admin_password=admin_channel=' + str(channelNo) + '_stream=0.sdp'
            elif camera_brand == 'axis':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/axis-media/media.amp'
            elif camera_brand == 'geovision':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + '/media/video1'
            elif camera_brand == 'honeywell':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/honeywell/stream'
            elif camera_brand == 'hixecure':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/ch0_0.264'
            elif camera_brand == 'hifocus':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/ch0_0.264'
            elif camera_brand == 'ganz':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + '554/snl/live/1/1'
            elif camera_brand == 'docketrun':
                url = 'rtsp://' + camera_ip_address + ':' + str(port) + '/ds-test'
            elif camera_brand == 'aviron':
                url = 'rtsp://' + camera_username + ':' + camera_password + '@' + camera_ip_address + ':' + str(port) + '/aviron/stream'
            else:
                return False
        return url
    except Exception as error:
        print(error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- create_rtsp_for_all2_brand 1", str(error), " ----time ---- ", now_time_with_time()]))
        return False

    


def Samplerurl_for_all_brand(camera_ip_address, channelNo='1', camera_username='admin', camera_password='TATA_tsk123', camera_brand='hikvision', port='554'):
    try:
        if channelNo == 'None' or port == 'None':
            channelNo = '1'
            port = '554'

        rtsp_formats = {
            'dahua': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/cam/realmonitor?channel={channelNo}&subtype=0',
            'hikvision': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/Streaming/Channels/101',
            'samsung': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/profile1/media.smp',
            'cp_plus': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/cam/realmonitor?channel={channelNo}&subtype=0',
            'bosch': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/cam/realmonitor?channel={channelNo}&subtype=0',
            'pelco': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/stream1',
            'uniview': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/media/video1',
            'univision': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/unicast/ch{channelNo}/s0/live',
            'secur_eye': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/user=admin_password=admin_channel={channelNo}_stream=0.sdp',
            'axis': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/axis-media/media.amp',
            'geovision': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}/media/video1',
            'hixecure': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/ch0_0.264',
            'hifocus': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/ch0_0.264',
            'ganz': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/snl/live/1/1',
            'docketrun': f'rtsp://{camera_ip_address}:8554/ds-test',
            'honeywell': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/honeywell/stream',  
            'aviron': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/aviron/stream', 
            'default': f'rtsp://{camera_username}:{camera_password}@{camera_ip_address}:{port}/stream'
        }

        if camera_brand in rtsp_formats:
            url = rtsp_formats[camera_brand]
        else:
            url = rtsp_formats['default']

        return url
    except Exception as error:
        print(error)        
        return False




################### Date time FUNCTION #################
def testing_today_date():
    today_date = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'))
    return today_date

def now_time():
    return datetime.now().replace(second=0, microsecond=0)


def now_time_with_time():
    now = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    return now



def only_date():
    now = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'))
    return now


def now_time_with_time_minus():
    now = str(datetime.strptime((datetime.now() - timedelta(seconds=30)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    return now


def get_time_in_seconds(cutime, dbtime):
    hour_seconds = cutime.split(' ')[1]
    hour_seconds = hour_seconds.strip()
    chr, cmin, csec = hour_seconds.split(':')
    current_in_seconds = int(int(chr) * 60 * 60) + int(int(cmin) * 60) + int(int(csec))
    db_hour_seconds = dbtime.split(' ')[1]
    db_hour_seconds = db_hour_seconds.strip()
    db_hr, db_min, db_sec = db_hour_seconds.split(':')
    db_in_seconds = int(int(db_hr) * 60 * 60) + int(int(db_min) * 60) + int(int(db_sec))
    return current_in_seconds - db_in_seconds


################################## lists realated function ################
def compare(l1, l2):
    set1 = set(l1)
    set2 = set(l2)
    if set1 == set2:
        return True
    else:
        return False
    
def remove_empty_elements_from_list(split_data):
    while '' in split_data:
        split_data.remove('')
    return split_data
    

##########list of dictionary and keys checking
def check_the_data_keys(key_in_riro_data, dataKeys):
    similar_keys = [i for i in list(dataKeys) if i in key_in_riro_data]
    check_dict_status = all(x in key_in_riro_data for x in list(dataKeys))
    return check_dict_status

def remove_duplicate_elements_from_two_list(first_list, second_list):
    in_first = set(first_list)
    in_second = set(second_list)
    in_second_but_not_in_first = in_second - in_first
    result = first_list + list(in_second_but_not_in_first)
    return result

def empty_list_function(list1):
    list2 = [x for x in list1 if x != []]
    return list2

    
##################### pagination functions ######################
def pagination_block(pagenumber, page_limit, all_data):
    ret = {}
    if len(all_data) != 0:
        if pagenumber and page_limit:
            if int(page_limit) < len(all_data):
                chucked_data = []
                for i in range(0, len(all_data), int(page_limit)):
                    chunk = all_data[i:i + int(page_limit)]
                    chucked_data.append(chunk)
                page_count1 = 0
                for count, i in enumerate(chucked_data):
                    page_count1 = count + 1
                if int(pagenumber) <= page_count1:
                    for count, i in enumerate(chucked_data):
                        page_count = count + 1
                        if page_count == int(pagenumber):
                            ret = {'success': True, 'message': chucked_data[count]}
                else:
                    for count, i in enumerate(chucked_data):
                        page_count = count + 1
                        if page_count == int(page_count1):
                            ret = {'success': True, 'message': chucked_data[count]}
            else:
                chucked_data = []
                for i in range(0, len(all_data), int(30)):
                    chunk = all_data[i:i + int(page_limit)]
                    chucked_data.append(chunk)
                page_count1 = 0
                for count, i in enumerate(chucked_data):
                    page_count1 = count + 1
                if page_count1:
                    for count, i in enumerate(chucked_data):
                        page_count = count + 1
                        if page_count == int(page_count1):
                            ret = {'success': True, 'message': chucked_data [count]}
        else:
            ret = {'success': True, 'message': all_data}
    else:
        ret = {'success': False, 'message': 'data not found'}
    return ret

######################################### STRING FUNCTIONS ##########################################
try:
    def remove_underscore(state_name):
        if state_name is not None:
            final_string = state_name.replace('_', ' ')
            return final_string
        else:
            return None
except Exception as error:
    ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- remove_underscore 1", str(error), " ----time ---- ", now_time_with_time()])) 
    print(str(error))

try:
    def replace_spl_char(string):
        not_require =[":","-","."," "] #[':', '-', '.', ' ']
        for i in not_require:
            if i in string:
                string = string.replace(i, '_')
        return string
except Exception as error:
    ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- replace_spl_char 1", str(error), " ----time ---- ", now_time_with_time()])) 
    print(str(error))

try:
    def remove_all_specail_char_with_hifhen(test_string):
        special=[';', ':', '!', "*",'@','#','&','%',' ','.'] 
        for i in special :
            test_string = test_string.replace(i,'-') 
        return test_string
except  Exception as error :
    ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- remove_all_specail_char_with_hifhen 1", str(error), " ----time ---- ", now_time_with_time()])) 
    print('error  removing the special character---')


def replace_spl_char_panel_area_plant(string):
    not_require = [':', '.', ' ']
    for i in not_require:
        if i in string:
            string = string.replace(i, '-')
    return string

def replace_spl_char_panel_subarea(string):
    not_require = [':', '.', ' ']
    for i in not_require:
        if i in string:
            string = string.replace(i, '-')
    return string


def replace_spl_char_time_to(string):
    not_require = [':', '.', ' ']
    for i in not_require:
        if i in string:
            string = string.replace(i, '-')
    return string

try:
    def remove_space_character(state_name):
        if state_name is not None:
            final_string = state_name.replace(' ', '-')
            return final_string
        else:
            return None
except Exception as error:
    ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- remove_space_character 1", str(error), " ----time ---- ", now_time_with_time()])) 
    print(str(error))

try:
    def remove_ampercent(state_name):
        if state_name is not None:
            final_string = state_name.replace('&', '-')
            return final_string
        else:
            return None
except Exception as error:
    ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- remove_ampercent 1", str(error), " ----time ---- ", now_time_with_time()])) 
    print(str(error))


def clean(txt):
    try:
        txt.replace('Â', '')
    except:
        txt = txt
    return txt

def clear_asci(myString):
    return myString.replace('\xa0', '')

#######################################################################################
def split_for_bbox_points(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]


##################### mongodb realted functions ##############################
def upsert_function_in_mongodb(collection_name, filter, new_values):
    print(collection_name, filter, new_values)
    result = mongo.db.collection_name.update_one(filter, new_values, upsert=True)
    if result.modified_count > 0:
        print(result.modified_count)
    else:
        print('Not worked out')


def delete_one_data_from_collection(id):
    delete_data = mongo.db.ppera_cameras.delete_one({'_id': ObjectId(id)})
    print(delete_data.deleted_count)
    if delete_data.deleted_count > 0:
        return True
    else:
        return False


def find_one_data_from_collection(id):
    find_data = mongo.db.ppera_cameras.find_one({'_id': ObjectId(id)})
    if find_data is not None:
        print(find_data)
        return find_data
    else:
        return False
    


################################## dashboard apis functions ########################### 


def check_riro_edit_status(final_data_riro_data):
    riro_edit_status = False
    if len(final_data_riro_data) != 0:
        for i in final_data_riro_data:
            if i['riro_edit_status']:
                riro_edit_status = True
                break
    return riro_edit_status

# reset the riro table dataupload status ==== 12 to 13 for the none is done for panel and make panel to normal state
def reset_tsk_riro_table_dataupload_12_to_13():
    try:
        conn = psycopg2.connect(user = "docketrun",password = "docketrun", host = "localhost",port = "5432",database = "docketrundb", sslmode="disable")
    except Exception as  error:
        print("[ERR] reset_tsk_riro_table_dataupl44oad_12_to_13 - CONNECT", error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- reset_tsk_rir444o_table_dataupload_12_to_13 1", str(error), " ----time ---- ", now_time_with_time()])) 
        conn = 0
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE tsk_riro SET datauploadstatus=13 WHERE datauploadstatus=12 OR datauploadstatus=11;')
            # print("updated")
        except Exception as  error:
            print("[ERR] reset_tsk_riro_table_data44upload_12_to_13 - UPDATE", error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- reset_tsk_riro_table_444dataupload_12_to_13 2", str(error), " ----time ---- ", now_time_with_time()])) 
        conn.commit()
        conn.close()

# reset the magflasher dataupload status 21,22,23,24 to 25 for the nothing is done for the panel and make panel to normal state 
def reset_mag_flash_table_dataupload_to_25():
    try:
        conn = psycopg2.connect(user = "docketrun",password = "docketrun", host = "localhost",port = "5432",database = "docketrundb", sslmode="disable")
    except Exception as  error:
        print("[ERR] reset_mag_flash_table_dataupload_to_25 - CONNECT", error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- reset_mag_flash_table_dataupload_to_25 CONNECT 1", str(error), " ----time ---- ", now_time_with_time()])) 
        conn = 0
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE mag_flah SET datauploadstatus=25 where datauploadstatus=20 or datauploadstatus=21 or datauploadstatus=22 or datauploadstatus=23 or datauploadstatus=24 ;')
            # print("updated")
        except Exception as  error:
            print("[ERR] reset_mag_flash_table_dataupload_to_25 - UPDATE", error)
            ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- reset_mag_flash_table_dataupload_to_25 UPDATE 4", str(error), " ----time ---- ", now_time_with_time()])) 
        conn.commit()
        conn.close()

############################# checking the  rack window co_ordinates from detected panels 
def COORIDINATES_FROM_DETECTED_PANEL(result):
    only_coordinates = []
    if len(result) != 0:
        for ___, i in enumerate(result):
            if i['rack_window_co_ordinates'] is not None and i['rack_window_co_ordinates'] != '':
                only_coordinates.append({'bbox': i['co_ordinates'],'panel_no': i['panel_number'], 'panel_key_id': str(int(___) + 1), 'RW': i['rack_window_co_ordinates'],'unallocated_job_status': False})
            else:
                only_coordinates.append({'bbox': i['co_ordinates'],'panel_no': i['panel_number'], 'panel_key_id': str(int(___) + 1), 'RW': [], 'unallocated_job_status': False})
    return only_coordinates

####################################analytic related functions ############################
def live_data_processing_for_dash_board(live_data,ppepercentage):
    # ret = False
    # print("live-data===",live_data)
    if live_data is not None:
        if 1:
        # try:
            if live_data['analyticstype'] == 'PPE_TYPE1':
                live_data['analyticstype'] = 'PPE'
                object_data = live_data['object_data']
                if len(object_data) != 0:
                    if 1:
                    # try:
                        final_object_data = []
                        if len(object_data) == 1:
                            if object_data[0]['Helmet']  == 'None' or object_data[0]['Helmet']  == None or object_data[0]['Vest']  == None or object_data[0]['Vest']  == 'None' or object_data[0]['Vest']  == 'arc_jacket' and object_data[0]['Helmet']  == True:
                                pass
                            elif object_data[0]['class_name'] == 'cool_coat':
                                pass
                            elif object_data[0]['class_name'] == 'irrd':
                                pass
                            elif object_data[0]['class_name'] == 'truck':
                                pass
                            elif object_data[0]['class_name'] == 'person':
                                if object_data[0]['Helmet'] == False:
                                    del object_data[0]['bbox']
                                    del object_data[0]['tracking_id']
                                    object_data[0]['violation_count'] = 'person ' + str(1)
                                    final_object_data.append(object_data[0])
                                elif object_data[0]['Vest'] == 'no_ppe':
                                    del object_data[0]['bbox']
                                    del object_data[0]['tracking_id']
                                    object_data[0]['violation_count'] = 'person ' + str(1)
                                    final_object_data.append(object_data[0])
                        elif len(object_data) > 1:
                            person_count = 0
                            for ___, jjj in enumerate(object_data):
                                if jjj['class_name'] == 'irrd':
                                    pass
                                elif jjj['class_name'] == 'cool_coat':
                                    pass
                                elif jjj['class_name'] == 'truck':
                                    pass
                                elif jjj['Helmet'] == 'None' or jjj['Helmet'] == None or jjj['Vest'] == None or jjj['Vest'] == 'None' or jjj['Vest'] == 'arc_jacket' and jjj['Helmet'] == True:
                                    pass
                                elif jjj['class_name'] == 'person':
                                    if jjj['Helmet'] == False:
                                        del jjj['bbox']
                                        del jjj['tracking_id']
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1
                                    elif jjj['Vest'] == 'no_ppe':
                                        del jjj['bbox']
                                        del jjj['tracking_id']
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1
                        if len(final_object_data) != 0:
                            live_data['object_data'] = final_object_data
                        else:
                            live_data = []
                    # except Exception as  error:
                    #     print(' (live_data) ---- line -2319 ',  error)
                    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_processing_for_dash_board 1", str(error), " ----time ---- ", now_time_with_time()]))
            elif live_data['analyticstype'] == 'RA':
                object_data = live_data['object_data']
                if len(object_data) != 0:
                    if 1:
                    # try:
                        final_object_data = []
                        if len(object_data) == 1:
                            if object_data[0]['violation'] == False:
                                pass
                            elif object_data[0]['violation'] == True:
                                if object_data[0]['class_name'] == 'person':
                                    del object_data[0]['bbox']
                                    del object_data[0]['tracking_id']
                                    object_data[0]['violation_count'
                                        ] = 'person ' + str(1)
                                    final_object_data.append(object_data[0])
                        elif len(object_data) > 1:
                            for ___, jjj in enumerate(object_data):
                                if jjj['violation'] == False:
                                    pass
                                elif jjj['violation'] == True:
                                    if jjj['class_name'] == 'person':
                                        del jjj['bbox']
                                        del jjj['tracking_id']
                                        jjj['violation_count'] = 'person ' + str(int(___) + int(1))
                                        final_object_data.append(jjj)
                        live_data['object_data'] = final_object_data
                    # except Exception as  error:
                    #     print('(live_data)    line --- 2347 ',  error)
            ret = live_data
        # except Exception as  error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- live_data_processing_for_dash_board 2", str(error), " ----time ---- ", now_time_with_time()]))
    else:
        ret = ret
    return ret

def get_ppe_helmet_violation(details,percent=70):
    helmet_percentage = (details['helmet'] / details['frame_count']) * 100    
    no_helmet_percentage = (details['no_helmet'] /details['frame_count']) * 100
    if int(percent) < 100:
        if helmet_percentage >= int(percent) or no_helmet_percentage >= int(percent):
            if helmet_percentage > no_helmet_percentage:
                return "true"
            elif helmet_percentage < no_helmet_percentage:
                if no_helmet_percentage>=int(percent):
                    return "false"
                else:
                    return 'null'
            else:
                return "null"
    else:
        percent =90
        if helmet_percentage >= int(percent) or no_helmet_percentage >= int(percent):
            if helmet_percentage > no_helmet_percentage:
                return "true"
            elif helmet_percentage < no_helmet_percentage:
                if no_helmet_percentage>=int(percent):
                    return "false"
                else:
                    return 'null'
            else:
                return "null"
    return "null"



def CrushHelmetPercentageCalculations(details,percent=70):
    helmet_percentage = (details['Bike_Helmet'] / details['frame_count']) * 100    
    no_helmet_percentage = (details['no_Bike_Helmet'] /details['frame_count']) * 100
    if int(percent) < 100:
        if helmet_percentage >= int(percent) or no_helmet_percentage >= int(percent):
            if helmet_percentage > no_helmet_percentage:
                return "true"
            elif helmet_percentage < no_helmet_percentage:
                if no_helmet_percentage>=int(percent):
                    return "false"
                else:
                    return 'null'
            else:
                return "null"
    else:
        percent =90
        if helmet_percentage >= int(percent) or no_helmet_percentage >= int(percent):
            if helmet_percentage > no_helmet_percentage:
                return "true"
            elif helmet_percentage < no_helmet_percentage:
                if no_helmet_percentage>=int(percent):
                    return "false"
                else:
                    return 'null'
            else:
                return "null"
    return "null"


def get_ppe_vest_violation(details,percent=70):
    vest_percentage = (details['vest'] / details['frame_count']) * 100
    arc_jacket_percentage = (details['arc_jacket'] / details['frame_count']) * 100
    no_vest_jacket_percentage = (details['no_ppe'] / details['frame_count']) * 100
    if int(percent) < 100:
        if vest_percentage >= int(percent) or arc_jacket_percentage >= int(percent) or no_vest_jacket_percentage >= int(percent):
            if vest_percentage > arc_jacket_percentage and vest_percentage > no_vest_jacket_percentage:
                return "vest"
            elif arc_jacket_percentage > vest_percentage and arc_jacket_percentage > no_vest_jacket_percentage:
                return "arc_jacket"
            elif no_vest_jacket_percentage > vest_percentage and no_vest_jacket_percentage > arc_jacket_percentage:
                # print("no_vest_jacket_percentage >=int(percent)====",no_vest_jacket_percentage >=int(percent))
                if no_vest_jacket_percentage >=int(percent):
                    return "no_ppe"
                else:
                    return 'null'
            else:
                return "null"
    else:
        percent = 90
        if vest_percentage >= int(percent) or arc_jacket_percentage >= int(percent) or no_vest_jacket_percentage >= int(percent):
            if vest_percentage > arc_jacket_percentage and vest_percentage > no_vest_jacket_percentage:
                return "vest"
            elif arc_jacket_percentage > vest_percentage and arc_jacket_percentage > no_vest_jacket_percentage:
                return "arc_jacket"
            elif no_vest_jacket_percentage > vest_percentage and no_vest_jacket_percentage > arc_jacket_percentage:
                # print("no_vest_jacket_percentage >=int(percent)====",no_vest_jacket_percentage >=int(percent))
                if no_vest_jacket_percentage >=int(percent):
                    return "no_ppe"
                else:
                    return 'null'
            else:
                return "null"

    return "null"


def VIolationcountforPPE(live_data,ppepercentage):
    # print("ppepercentage=========================",ppepercentage)
    ret = False
    if live_data is not None:
        if live_data['analyticstype'] == 'PPE_TYPE1':
            live_data['analyticstype'] = 'PPE'
            object_data = live_data['object_data']
            if len(object_data) != 0:
                # try:
                final_object_data = []               
                person_count = 0
                # print("=================lenobject_data===========",len(object_data))
                for ___, jjj in enumerate(object_data):
                    # print("------------------in------------ppe percentage===========",jjj)
                    if jjj['class_name'] == 'irrd':
                        pass
                    elif jjj['class_name'] == 'cool_coat':
                        pass
                    elif jjj['class_name'] == 'truck':
                        pass
                    elif jjj['Helmet'] == 'None' or jjj['Helmet'] == None or jjj['Vest'] == None or jjj['Vest'] == 'None' or jjj['Vest'] == 'arc_jacket' and jjj['Helmet'] == True:
                        pass
                    elif jjj['class_name'] == 'person':
                        if jjj['Helmet'] == False:
                            del jjj['tracking_id']   
                            if 1:
                            # try:
                                
                                if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                    if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1  
                                    else:
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1  
                                else:
                                    if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1  
                                    # else:
                                    #     print("vest condition failed 1 ============================",get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']))
                            # except:
                            #     jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                            #     final_object_data.append(jjj)
                            #     person_count += 1
                        elif jjj['Vest'] == 'no_ppe':
                            # del jjj['bbox']
                            del jjj['tracking_id']
                            if 1:
                            # try:
                                if get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']) == 'no_ppe':
                                    if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1   
                                    else:
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1   
                                else:
                                    if get_ppe_helmet_violation(jjj['algorithm_details'],ppepercentage['helmet'])=='false':
                                        jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                                        final_object_data.append(jjj)
                                        person_count += 1  
                            # except:
                            #     jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                            #     final_object_data.append(jjj)
                            #     person_count += 1
                # print("=================final_object_data len ======",len(final_object_data))
                if len(final_object_data) != 0:
                    live_data['object_data'] = final_object_data
                else:
                    live_data = []
                        # except Exception as  error:
                        #     print(' (live_data) ---- line -2319 ',  error)
                        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  1", str(error), " ----time ---- ", now_time_with_time()]))
                
        ret = live_data
        # except Exception as  error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  2", str(error), " ----time ---- ", now_time_with_time()]))
    else:
        ret = ret
    return ret




def VIolationcountforCrushHelmet(live_data,ppepercentage):
    # print("ppepercentage=========================",ppepercentage)
    ret = False
    if live_data is not None:
        if live_data['analyticstype'] == 'PPE_TYPE2':
            object_data = live_data['object_data']
            if len(object_data) != 0:
                # try:
                final_object_data = []               
                person_count = 0
                # print("=================lenobject_data===========",len(object_data))
                for ___, jjj in enumerate(object_data):
                    if jjj['class_name'] == 'biker':
                        if jjj['Bike_Helmet'] == False:
                            del jjj['tracking_id']   
                            if 1:
                            # try:                                
                                if CrushHelmetPercentageCalculations(jjj['algorithm_details'],ppepercentage['crash_helmet'])=='false':
                                    jjj['violation_count'] =  jjj['class_name']#+ str(int(person_count) + int(1))
                                    final_object_data.append(jjj)
                                    person_count += 1  
                                
                                    #     print("vest condition failed 1 ============================",get_ppe_vest_violation(jjj['algorithm_details'],ppepercentage['vest']))
                            # except:
                            #     jjj['violation_count'] = 'person ' + str(int(person_count) + int(1))
                            #     final_object_data.append(jjj)
                            #     person_count += 1
                        
                # print("=================final_object_data len ======",len(final_object_data))
                if len(final_object_data) != 0:
                    live_data['object_data'] = final_object_data
                else:
                    live_data = []
                        # except Exception as  error:
                        #     print(' (live_data) ---- line -2319 ',  error)
                        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  1", str(error), " ----time ---- ", now_time_with_time()]))
                
        ret = live_data
        # except Exception as  error:
        #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis --  2", str(error), " ----time ---- ", now_time_with_time()]))
    else:
        ret = ret
    return ret





#####



# email alert imports 



def ERRORLOGdata(message):
    with open("ALL_API_ERROR.log", "a") as f:
        f.write(message+"\n")



############################## ip and network functions ##########################
def ping_test(ip):
    response = os.system('ping -w 1 ' + ip)
    if response == 0:
        print(ip, 'is up')
        return "ip_working"
    else:
        print(ip, 'is down')
        return "ip_not_working"  


##################################### common app #############################################
def get_common_app_monitoring_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'docketrun_app_started':
                ret_val = val
    else:
        pass
    return ret_val


def get_common_app_Enable_system_restart():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'system_restart':
                ret_val = val
    else:
        pass
    return ret_val


def common_app_get_sleep_time():
    ret_val = 0
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'docketrun_app_sleep_time':
                ret_val = val
    else:
        pass
    return ret_val


def app_set_common_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started':  True,"smrec":True,"hydra_app":True, "phaseone_app":True,'firesmokeapp':True,'vpms':True,'system_restart': False, 'esi_sleep_time': 10,  'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id) }, {'$set': {'docketrun_app_started': val,'docketrun_app_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count common app --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)
        
        
###################################firesmoke###############################################################
def get_firesmoke_app_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'firesmokeapp':
                ret_val = val
    else:
        pass
    return ret_val


def firesmoke_app_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started':  True,"smrec":True,"hydra_app":True, "phaseone_app":True,'firesmokeapp':True,'vpms':True,'system_restart': False, 'esi_sleep_time': 10,  'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id) }, {'$set': {'firesmokeapp': val,'docketrun_app_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count common app --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)

######################################wheel ##################################
def get_Wheelapp_started():
    ret_val = False
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        for key, val in hooter_on_of.items():
            if key == 'wheelapp':
                ret_val = val
    else:
        pass
    return ret_val


def Wheelapp_monitoring_started(val):
    dict11 = {'esi_monitoring_started': True, 'docketrun_app_started':  True,"smrec":True,"hydra_app":True, "phaseone_app":True,'firesmokeapp':True,'vpms':True,'wheelapp':True,'system_restart': False, 'esi_sleep_time': 10,  'docketrun_app_sleep_time': 10, 'inserted_time': str(now_time_with_time()), 'all_apps_status': 1}
    hooter_on_of = mongo.db.docket_app_status.find_one({'all_apps_status': 1}, sort=[('_id', pymongo.DESCENDING)])
    if hooter_on_of is not None:
        id = hooter_on_of['_id']
        result = mongo.db.docket_app_status.update_one({'_id': ObjectId(id) }, {'$set': {'wheelapp': val,'docketrun_app_sleep_time': 1}})
        if result.matched_count > 0:
            print('result.matched_count common app --', result.matched_count)
            pass
        else:
            pass
    else:
        mongo.db.docket_app_status.insert_one(dict11)



#################################### image related functions #######################
def image_resizing(image_path):
    image = cv2.imread(image_path)
    max_height = 544
    max_width = 960
    dim = max_width, max_height
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, resized)
    #cv2.destroyAllWindows()
    return True

def image_size_function(image_name_list, base_path):
    image_width_height = []
    for zzzz in image_name_list:
        if zzzz:
            try:
                image_name = Image.open(base_path + '/' + zzzz)
                width, height = image_name.size
                heigth_width = {'width': width, 'height': height}
                image_width_height.append(heigth_width)
            except Exception as error:
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- image_size_function 1", str(error), " ----time ---- ", now_time_with_time()]))
                image_width_height.append(None)
        else:
            image_width_height.append(None)
    return image_width_height

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def compress_pic(file_path, qual):
    picture = Image.open(file_path)
    dim = picture.size
    picture.save(file_path, 'JPEG', optimize=True, quality=qual)
    processed_size = os.stat(file_path).st_size
    return processed_size

    

############################# mongodb service functions #######################
def check_the_status_mongodb_service():
    mongodb_r_status_filename = 'mongodb_rtatusoutput.txt'
    try:
        result = os.system('service mongod status > '+mongodb_r_status_filename)
        if result == 0:
            if os.path.exists(mongodb_r_status_filename):
                fp = open(mongodb_r_status_filename, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_r_status_filename)
                if "Active: active (running)" in output :
                    return True
                else:
                    return False
            else:
                return False
        else:
            result1 = os.system('service mongodb status > '+mongodb_r_status_filename)
            if result1 == 0:
                if os.path.exists(mongodb_r_status_filename):
                    fp = open(mongodb_r_status_filename, "r")
                    output = fp.read()
                    fp.close()
                    os.remove(mongodb_r_status_filename)
                    print(output)
                    if "Active: active (running)" in output :
                        return True
                    else:
                        return False
                else:
                    return False
            return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- check_the_status_mongodb_service 1", str(error), " ----time ---- ", now_time_with_time()]))
        return False

def restart_mongodb_r_service():
    try:
        if check_the_status_mongodb_service():
            print("mongodb service already running")
            return True
            
        else:
            result = os.system('echo "docketrun" | sudo -S service mongod restart')
            if result == 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                result1 = os.system('echo "docketrun" | sudo -S service mongodb restart')
                if result1== 0:
                    if check_the_status_mongodb_service():
                        return True
                    else:
                        return False
                else:
                    return False
            
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- restart_mongodb_r_service 1", str(error), " ----time ---- ", now_time_with_time()]))        
        return False
    

def forcerestart_mongodb_r_service():
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod restart')
        if result == 0:
            if check_the_status_mongodb_service():
                return True
            else:
                return False
        else:
            result1 = os.system('echo "docketrun" | sudo -S service mongodb restart')
            if result1== 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                return False            
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- forcerestart_mongodb_r_service 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return False
    
def start_mongodb_r_service():
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod start ')
        if result == 0:
            if check_the_status_mongodb_service():
                return True
            else:
                return False
        else:
            result = os.system('echo "docketrun" | sudo -S service mongodb start ')
            if result == 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- start_mongodb_r_service 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return False
    

def stop_mongodb_service():
    try:#sudo service mongod stop
        result = os.system('echo "docketrun" | sudo -S service mongod stop')
        if result == 0:
            if check_the_status_mongodb_service():
                return True
            else:
                return False
        else:
            result1 = os.system('echo "docketrun" | sudo -S service mongodb stop')
            if result1 == 0:
                if check_the_status_mongodb_service():
                    return True
                else:
                    return False
            else:
                return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_mongodb_service 1", str(error), " ----time ---- ", now_time_with_time()]))       
        return False
    
def enable_mongodb_r_service_to_system():
    mongodb_r_status_filename = 'mongodb_rtatusenableoutput.txt'
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod enable  > '+mongodb_r_status_filename)
        if result == 0:
            if os.path.exists(mongodb_r_status_filename):
                fp = open(mongodb_r_status_filename, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_r_status_filename)
                print(output)
                return True
            else:
                return False
        else:
            result = os.system('echo "docketrun" | sudo -S service mongodb enable  > '+mongodb_r_status_filename)
            if result == 0:
                if os.path.exists(mongodb_r_status_filename):
                    fp = open(mongodb_r_status_filename, "r")
                    output = fp.read()
                    fp.close()
                    os.remove(mongodb_r_status_filename)
                    print(output)
                    return True
                else:
                    return False
            else:
                return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- enable_mongodb_r_service_to_system 1", str(error), " ----time ---- ", now_time_with_time()]))      
        return False
    
def disable_mongodb_r_service_to_system():
    mongodb_r_status_filename = 'mongodb_rtatusdisableoutput.txt'
    try:
        result = os.system('echo "docketrun" | sudo -S service mongod disable  > '+mongodb_r_status_filename)
        if result == 0:
            if os.path.exists(mongodb_r_status_filename):
                fp = open(mongodb_r_status_filename, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_r_status_filename)
                print(output)
                return True
            else:
                return False
        else:
            return False
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- disable_mongodb_r_service_to_system 1", str(error), " ----time ---- ", now_time_with_time()]))      
        return False
    


def check_the_mongodb_r_installed_version():
    mongodb_rversion_file = "mongodb_rversion.txt"
    try:
        result = os.system('mongod --version> '+mongodb_rversion_file)#('echo "docketrun" | sudo -S service mongod disable  > '+mongodb_rversion_file)
        if result == 0:
            if os.path.exists(mongodb_rversion_file):
                fp = open(mongodb_rversion_file, "r")
                output = fp.read()
                fp.close()
                os.remove(mongodb_rversion_file)
                print(output)
                return True
            else:
                return False
        else:
            result2 = os.system('mongod -V> '+mongodb_rversion_file)
            if result2 ==0:
                if os.path.exists(mongodb_rversion_file):
                    fp = open(mongodb_rversion_file, "r")
                    output = fp.read()
                    fp.close()
                    os.remove(mongodb_rversion_file)
                    print(output)
                    return True
                else:

                    return False
            else:
                result2 = os.system('mongodb --version > '+mongodb_rversion_file)
                if result2 ==0:
                    if os.path.exists(mongodb_rversion_file):
                        fp = open(mongodb_rversion_file, "r")
                        output = fp.read()
                        fp.close()
                        os.remove(mongodb_rversion_file)
                        print(output)
                        return True
                    else:

                        return False
                else:
                    result3 = os.system('mongodb -V> '+mongodb_rversion_file)
                    if result3 ==0:
                        if os.path.exists(mongodb_rversion_file):
                            fp = open(mongodb_rversion_file, "r")
                            output = fp.read()
                            fp.close()
                            os.remove(mongodb_rversion_file)
                            print(output)
                            return True
                        else:
                            return False
                    else:
                        return False
    except Exception as error:
        return False
    
####################once again #################
####################################### ESI realated functions ################
def MULTIKEYSREMOVING(i, data):
    if i in data:
        return False
    else:
        i = delete_keys_from_dict(i, ['ip_status', 'panel', 'sheet_status'])
        camera_data = i['data']
        camera_data = delete_keys_from_dict(camera_data, ['camera_brand','rtsp_status', 'inserted_time', 'camera_id'])
        i['data'] = camera_data
    return i




def MUlRIRODATACMECH(i, data):
    if i in data:
        return False
    else:
        i = delete_keys_from_list_of_dict_multi_isolation(i, ['ip_status', 'sheet_status'])
        camera_data = i['data']
        camera_data = delete_keys_from_list_of_dict_multi_isolation(camera_data, ['camera_brand','rtsp_status', 'inserted_time'])
        i['data'] = camera_data
    return i


def DELETINGCAMERABRANDRTSP(data):
    return_data = []
    for count, i in enumerate(data):
        i = delete_keys_from_dict(i, ['camera_brand', 'rtsp_status', 'inserted_time', 'camera_id'])
        return_data.append(i)
    return return_data

#########################ppe related functions ####################
def object_data_keys(object_data):
    showcase_keys = []
    keys_required = ['Vest', 'Helmet']
    for ij in object_data:
        for xx in ij.keys():
            if xx in keys_required:
                if xx not in showcase_keys:
                    showcase_keys.append(xx)
    return showcase_keys

#################################ALPHANUMERIC TOKEN GENERATION FUNCTIONS #############
def genarate_alphanumeric_key():
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(200))
    return key


def genarate_alphanumeric_key_for_riro_data():
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(25))
    return key


def GENERATEALPHANUMERICKEYFOREXCELTEST50():
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(50))
    return key

############################ dict and json #############################
def read_json_for_roi(json_fileName):
    with open(json_fileName, 'r') as f:
        data = json.load(f)
    return data

def parse_json(data):
    return json.loads(json_util.dumps(data))


def parse_json_dictionary(data):
    return json_util.dumps(data)


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def isEmpty(dictionary):
    for element in dictionary:
        if element:
            return True
        return False

def ENABLED_SOLUTION_IS_EMPTY_DICT(dictionary):
    for element in dictionary.values():
        if len(element) !=0:
            return True
        return False
    
def check_dictionaryishavinganynonevalue(dictionary):
    dictionary_status = True
    for element in dictionary:
        if element is None or element ==' ':
            dictionary_status= True
    return dictionary_status

def check_arraydictionaryishavinganynonevalue(dictionary):
    # print("ajdasdjfk", dictionary)
    dictionary_status = True
    for dic in dictionary:
        if any([v==None for v in dic.values()]):
            dictionary_status= False
            break
    return dictionary_status

def delete_keys_from_dict(dictionary, keys):
    keys_set = set(keys)
    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict

def delete_keys_from_list_of_dict_multi_isolation(list_of_dict, keys):
    keys_set = set(keys)
    modified_dict = {}
    if type(list_of_dict) == list:
        for mirror in list_of_dict:
            dictionary = mirror
            for key, value in dictionary.items():
                if key not in keys_set:
                    if isinstance(value, MutableMapping):
                        modified_dict[key] = delete_keys_from_dict(value, keys_set)
                    else:
                        modified_dict[key] = value
    elif type(list_of_dict) == dict:
        dictionary = list_of_dict 
        for key, value in dictionary.items():
            if key not in keys_set:
                if isinstance(value, MutableMapping):
                    modified_dict[key] = delete_keys_from_dict(value, keys_set)
                else:
                    modified_dict[key] = value
    return modified_dict


def dictionary_key_exists(dictionary,key):
    if key in dictionary.keys():
        return True
    else:
        return False

############################ relative path functions ###################
def get_current_dir_and_goto_parent_dir():
    return os.path.dirname(os.getcwd())


def parent_directory_grandpa_dir():
    relative_parent = os.path.join(os.getcwd(), "../..") 
    return os.path.abspath(relative_parent)


##################CREAT FOLDER AND FILES #################
def create_multiple_dir(path):
    os.makedirs(path, exist_ok=True)

def handle_uploaded_file(target_dir):
    os.umask(0)
    os.makedirs(target_dir, mode=511, exist_ok=True)


def try_chmod_command(file):
    os.chmod(file, 511)
    

def file_exists(filename):
    return os.path.isfile(filename)



def remove_text_files(configfolderpath):
    test=os.listdir(configfolderpath)
    for item in test:
        if item.endswith(".txt"):
            os.remove(os.path.join(configfolderpath, item))


"""VERIFY FILE IS EXCEL OR NOT"""
def CHECKEXCELFILEEXTENTION(filename):
    """check the file format using endswith fun"""
    excel_formats = [".xls", ".ods", ".csv", ".xlsx", ".xlsm", ".xltx",".xltm"]
    res = []
    for f in excel_formats:
        x = filename.endswith(f)
        res.append(x)
    if True in res:
        return True    
    else:
        return False



############################ CAMERA AND RTSP RELATED  FUNCTION  ####################
# #Function to check rtsp is online or not
def check_rtsp_is_working(url):
    verfy_rtsp_response = False
    cam = cv2.VideoCapture(url)
    if cam.isOpened() == True:
        verfy_rtsp_response = True
    else:
        verfy_rtsp_response = False
    cam.release()
    #cv2.destroyAllWindows()
    return verfy_rtsp_response
# #Function to check rtsp is online or not
def CHECKRTSPWORKINGORNOT(url):
    cam = cv2.VideoCapture(url)
    if cam.isOpened() == True:
        while(cam.isOpened()):
            ret,frame = cam.read()
            if ret:
                return "rtsp_working"
            else:
                break
        cam.release()
        #cv2.destroyAllWindows()        
    else:
        return "rtsp_not_working"   


#bosch  
#rtsp://admin:admin@192.168.1.100/rtsp_live0
#rtsp://admin:admin@192.168.1.100/rtsp_live0




def split_rtsp_url(brand, rtsp_url):
    return_data = None
    try:
        if brand == 'cp_plus':
            try:
                # print("rtsp -url ===========",rtsp_url)
                data = rtsp_url.split('//')
                username_with_ip = data[1].split('/', 1)
                channel_number = username_with_ip[1].split('channel=', 1)[1].split('&', 1)[0]
                subtype = username_with_ip[1].split('subtype=')[1]
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel':channel_number, 'subtype': subtype}
            except Exception as error:
                print('cp_plus', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 1", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username':None, 'password': None, 'channel': None, 'subtype': None}
        elif brand == 'dahua':
            try:
                data = rtsp_url.split('//')
                username_with_ip = data[1].split('/', 1)
                channel_number = username_with_ip[1].split('channel=', 1)[1].split('&', 1)[0]
                subtype = username_with_ip[1].split('subtype=')[1]
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel':channel_number, 'subtype': subtype}
            except Exception as error:
                print('dahua', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 2", str(error), " ----time ---- ", now_time_with_time()]))
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
        elif brand == 'hikvision':
            try:
                data = rtsp_url.split('//')
                username_with_ip = data[1].split('/', 1)
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel':None, 'subtype': None}
            except Exception as error:
                print('hikvision', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 3", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username':None, 'password': None, 'channel': None, 'subtype': None}
        elif brand == 'samsung':
            try:
                data = rtsp_url.split('//')
                username_with_ip = data[1].split('/', 1)
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel':None, 'subtype': None}
            except Exception as error:
                print('samsung', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 4", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
        elif brand == 'uniview':
            try:
                data = rtsp_url.split('//')
                username_with_ip = data[1].split('/', 1)
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel': None, 'subtype': None}
            except Exception as error:
                print('uniview === ', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 5", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
        elif brand == 'bosch':
            try:
                data = rtsp_url.split('//')
                return_data = {'ipaddress': data[1], 'port': None,'username': None, 'password': None, 'channel': None,'subtype': None}
            except Exception as error:
                print('bosch ', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 6", str(error), " ----time ---- ", now_time_with_time()])) 
                data = rtsp_url.split('//')
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
        elif brand =='geovision':
            try :
                data = rtsp_url.split("//")
                username_with_ip = data[1].split('/', 1)
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel': None, 'subtype': None}
            except Exception as error:
                print('geovision ', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 7", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
        elif brand =='hixecure':
            try :
                data = rtsp_url.split("//")
                username_with_ip = data[1].split('/', 1)
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel': None, 'subtype': None}
            except Exception as error:
                print('hixecure ', str(error))
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 8", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
        elif brand =='hifocus':
            try :
                data = rtsp_url.split("//")
                username_with_ip = data[1].split('/', 1)
                username_password = username_with_ip[0].split('@', 1)
                username_list = username_password[0].split(':', 1)
                ipaddress_list1 = username_password[1].split(':', 1)
                username = username_list[0]
                password = username_list[1]
                ipaddress = ipaddress_list1[0]
                port = ipaddress_list1[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel': None, 'subtype': None}
                print("return_data ---- return_data", return_data)
            except Exception as error:
            # else:
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 8", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}

        elif brand =='docketrun':
            try :
                data = rtsp_url.split("//")
                # print("data===",data)
                username_with_ip = data[1].split('/', 1)
                # print("username_with_ip", username_with_ip)
                # username_password = username_with_ip[0].split('@', 1)
                username_list = username_with_ip[0].split(':', 1)
                # print("username_list---",username_list)
                ipaddress_list1 = username_list[0]#.split(':', 1)
                username = 'docketrun'
                password = 'docketrun'#username_list[1]
                ipaddress = ipaddress_list1
                dom =[item[::-1] for item in ipaddress[::-1].split('.', 1)][::-1] #ipaddress.split(ipaddress, -1)
                # print('------{0} '.format(dom))
                last_digit = random.randint(2,255)
                # print("last_digit ---", dom[0]+'.'+str(last_digit))
                ipaddress = dom[0]+'.'+str(last_digit)
                port = username_list[1]
                return_data = {'ipaddress': ipaddress, 'port': port,'username': username, 'password': password, 'channel': None, 'subtype': None}
                print(return_data)
            # else:

            except Exception as error:
                print('geovision ', str(error))
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 9", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
                
        elif brand =='pelco':
            try:
                parsed_url = urlparse(rtsp_url)
                scheme = parsed_url.scheme
                username, password = parsed_url.username, parsed_url.password
                ip_address = parsed_url.hostname
                port = parsed_url.port
                path_parts = parsed_url.path.split('/')
                channel, subtype = None, None

                if len(path_parts) >= 2:
                    channel = path_parts[1]
                if len(path_parts) >= 3:
                    subtype = path_parts[2]
                return_data = {'ipaddress': ip_address, 'port': port, 'username':username, 'password': password, 'channel': channel, 'subtype': subtype}
            except Exception as error:
                print('geovision ', str(error))
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
                ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_33rtsp_url 10", str(error), " ----time ---- ", now_time_with_time()])) 
                return_data = {'ipaddress': None, 'port': None, 'username': None, 'password': None, 'channel': None, 'subtype': None}
    
        elif brand =='ganz':
            try:
                parsed_url = urlparse(rtsp_url)
                scheme = parsed_url.scheme
                username, password = parsed_url.username, parsed_url.password
                ip_address = parsed_url.hostname
                port = parsed_url.port
                path_parts = parsed_url.path.split('/')
                channel, subtype = None, None

                if len(path_parts) >= 2:
                    channel = path_parts[1]
                if len(path_parts) >= 3:
                    subtype = path_parts[2]

                return_data = {
                    'ipaddress': ip_address,
                    'port': port,
                    'username': username,
                    'password': password,
                    'channel': channel,
                    'subtype': subtype
                }
                
            except Exception as error:
                print(f'{brand} error: {str(error)}')
                return_data = {
                    'ipaddress': None,
                    'port': None,
                    'username': None,
                    'password': None,
                    'channel': None,
                    'subtype': None
                }
                # Log error (assuming ERRORLOGdata and now_time_with_time are defined elsewhere)
                ERRORLOGdata(f"[ERROR] packages -- split_33rtsp_url {brand} {str(error)} ----time ---- {now_time_with_time()}") 
    
    except Exception as error:
        print('brand ,rtsp_url):  line 429  ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- split_rtsp_url 10", str(error), " ----time ---- ", now_time_with_time()])) 
    return return_data

################### Date time FUNCTION #################
def testing_today_date():
    today_date = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'))
    return today_date

def now_time():
    return datetime.now().replace(second=0, microsecond=0)


def now_time_with_time():
    now = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    return now

def only_date():
    now = str(datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'))
    return now


def now_time_with_time_minus():
    from datetime import datetime, timedelta
    now = str(datetime.strptime((datetime.now() - timedelta(seconds=30)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    return now


def get_time_in_seconds(cutime, dbtime):
    hour_seconds = cutime.split(' ')[1]
    hour_seconds = hour_seconds.strip()
    chr, cmin, csec = hour_seconds.split(':')
    current_in_seconds = int(int(chr) * 60 * 60) + int(int(cmin) * 60) + int(int(csec))
    db_hour_seconds = dbtime.split(' ')[1]
    db_hour_seconds = db_hour_seconds.strip()
    db_hr, db_min, db_sec = db_hour_seconds.split(':')
    db_in_seconds = int(int(db_hr) * 60 * 60) + int(int(db_min) * 60) + int(int(db_sec))
    return current_in_seconds - db_in_seconds




############################---- system and process related function ---############################## 


# def checkProcessRunning(process_name):
#     process_data = []
#     if 1:
#     # try:
#         Systemprocesinformation = psutil.process_iter(['pid', 'name'])
#         for name in process_name:
#             if name in Systemprocesinformation:
#                 if name.lower() not in process_data:
#                     process_data.append({'process_name': name.lower(), 'process_status': True})
#                     # Terminate the process
#                 else:
#                     print(f"No process with name {name} found.")
#                     if name.lower() not in process_data:
#                         process_data.append({'process_name': name.lower(), 'process_status': False})
#             else:
#                 process_data.append({'process_name': name.lower(), 'process_status': False})
#     # except Exception as e:
#     #     print(f"Error killing process {process_name}: {e}")

#     if process_data:
#         ret = {'message': process_data, 'success': True}
#     else:
#         ret = {'message': process_data, 'success': False}

#     return ret



def checkProcessRunning(processName):
    ret = {'message': 'Something went wrong with checking process running', 'success': False}
    process_data = []
    if isinstance(processName, list):
        if processName:
            for name in processName:
                try:
                    subprocess.check_output(['pgrep', name.lower()])
                    process_data.append({'process_name': name.lower(), 'process_status': True})
                except subprocess.CalledProcessError:
                    if ({'process_name': name.lower(), 'process_status': True} or {'process_name': name.lower(), 'process_status': False})  in  process_data:
                        pass
                    else:
                        for process in psutil.process_iter(['pid', 'name']):
                            if ({'process_name': name.lower(), 'process_status': True} or {'process_name': name.lower(), 'process_status': False}) in  process_data:
                                pass
                            else:
                                if process.info['name'].lower() == name.lower():
                                    pid = process.info['pid']
                                    process_data.append({'process_name': name.lower(), 'process_status': True})

                    if {'process_name': name.lower(), 'process_status': False} in  process_data:
                        # print("--------------1.0.2-------------")
                        pass
                        
                        
                    elif {'process_name': name.lower(), 'process_status': True}   in  process_data:
                        # print("--------------1.0.1-------------")
                        pass
                        
                    else:
                        # print("--------------1.0.3-------------")
                        process_data.append({'process_name': name.lower(), 'process_status': False})
        else:
            print('Warning: Process list is empty')
            process_data.append({'process_name': name.lower(), 'process_status': False})
    elif processName is not None:
        try:
            subprocess.check_output(['pgrep', processName.lower()])
            process_data.append({'process_name': processName.lower(), 'process_status': True})
        except subprocess.CalledProcessError:

            for process in psutil.process_iter(['pid', 'name']):
                if processName.lower() not in  process_data:
                    if process.info['name'].lower() == processName.lower():
                        pid = process.info['pid']
                        process_data.append({'process_name': processName.lower(), 'process_status': True})

            if processName.lower() not in  process_data:
                process_data.append({'process_name': processName.lower(), 'process_status': False})

    if process_data:
        ret = {'message': process_data, 'success': True}
    else:
        ret = {'message': process_data, 'success': False}

    return ret


def CHECKHOOTERJSONEXISTs():
    json_filename = os.path.join(get_current_dir_and_goto_parent_dir() + '/' + 'docketrun_app', "hooter_meta.json")
    if not file_exists(json_filename):
        createHOOTERMETAJSON(json_filename)
        return True
    else:
        return True # json.dumps(enabled_data, indent=4)

def fetch_configuration_data(filename):
    with open(filename, 'r') as file:
        models_data = json.load(file)
    enabled_model = None
    if models_data is not None:
        enabled_model = models_data
    file.close()
    return enabled_model


def createHOOTERMETAJSONSTART():
    json_filename = os.path.join(get_current_dir_and_goto_parent_dir() + '/' + 'docketrun_app', "hooter_meta.json")
    if not file_exists(json_filename):
        CreateJSONFILEFORHOOTERMETA(json_filename)
        # print(f"JSON file '{json_filename}' created successfully!")
    # enabled_data = fetch_configuration_data(json_filename)
    # print(json.dumps(enabled_data, indent=4))
    else:
        update_hooter_metaStart(json_filename)
    return True 

def update_hooter_metaStart(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    data["hooter_work_status"] = 1
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def CreateJSONFILEFORHOOTERMETA(filename):
    data = {"hooter_work_status":1}
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    file.close()


def createHOOTERMETAJSONSTOP():
    json_filename = os.path.join(get_current_dir_and_goto_parent_dir() + '/' + 'docketrun_app', "hooter_meta.json")
    if not file_exists(json_filename):
        CreateJSONFILEFORHOOTERMETASTOP(json_filename)
        # print(f"JSON file '{json_filename}' created successfully!")
    # enabled_data = fetch_configuration_data(json_filename)
    else:
        update_hooter_meta(json_filename)
    # print(json.dumps(enabled_data, indent=4))
    return True 


def update_hooter_meta(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    data["hooter_work_status"] = 0
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def CreateJSONFILEFORHOOTERMETASTOP(filename):
    data = {"hooter_work_status":0}
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    file.close()


    
# def checkProcessRunning(processName):
#     ret = {'message': 'something went wrong with check process running','success': False}
#     process_data = []
#     if type(processName) == list:
#         if len(processName) != 0:
#             for ___i, mouse in enumerate(processName):
#                 try:
#                     running = subprocess.check_output('pgrep ' + str(mouse.lower()), shell=True)
#                     process_data.append({'process_name': mouse.lower(),'process_status': True})
#                 except Exception as error:
#                     process_data.append({'process_name': mouse.lower(),'process_status': False})
#                     #ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- checkProcess44Running 1", str(error), " ----time ---- ", now_time_with_time()])) 
#             if len(process_data) != 0:
#                 ret = {'message': process_data, 'success': True}
#             else:
#                 ret = {'message': 'proccess are not working', 'success': False}
#         else:
#             print('FUNCTION_checkProeecessRunning PROCESS LIST IS EMPTY')
#     elif processName is not None:
#         try:
#             running = subprocess.check_output('pgrep ' + str(processName.lower()), shell=True)
#             process_data.append({'process_name': processName.lower(),'process_status': True})
#         except Exception as error:
#             #ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- checkPr44ocessRunning 2", str(error), " ----time ---- ", now_time_with_time()])) 
#             process_data.append({'process_name': processName.lower(),'process_status': False})            
#         if len(process_data) != 0:
#             ret = {'message': process_data, 'success': True}
#         else:
#             ret = {'message': 'proccess are not working', 'success': False}
#     return ret

def stop_application_for_docketrun_creating_config():
    try:
        os.system('pkill -9 docketrun-app')
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_application_for_docketrun_creating_config 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return True
    

def stop_application_for_firesmokeapp_creating_config():
    try:
        os.system('pkill -9 fire_smoke_app')
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_application_for_docketrun_creating_config 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return True
    
def stop_application_for_phaseoneapp_creating_config():
    try:
        os.system('pkill -9 phaseone-app')
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_application_for_phaseoneapp_creating_config 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return True
    
def stop_smartrecordapp_creating_config():
    try:
        os.system('pkill -9 smrec')
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_smartrecordapp_creating_config 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return True
    
def stop_MECHHYDRA_creating_config():
    try:
        os.system('pkill -9 hydra-app')
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_MECHHYDRA_creating_config 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return True

def stop_application_for_esi_creating_config():
    try:
        os.system('pkill -9 esi-monitor')
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- stop_application_for_esi_creating_config 1", str(error), " ----time ---- ", now_time_with_time()])) 
        return True
    
def reset_cuda_memory():
    try:
        from numba import cuda
        device = cuda.get_current_device()
        device.reset()
        return True
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- reset_cuda_memory 1", str(error), " ----time ---- ", now_time_with_time()])) 
        print('Cuda didnt reset ', error)


################################## lists realated function ################


def split_list(input_list, sublist_length):
    return [input_list[i:i+sublist_length] for i in range(0, len(input_list), sublist_length)]

def compare(l1, l2):
    set1 = set(l1)
    set2 = set(l2)
    if set1 == set2:
        return True
    else:
        return False
    
def remove_empty_elements_from_list(split_data):
    while '' in split_data:
        split_data.remove('')
    return split_data
    




def checkNegativevaluesinBbox(text):
    try:
        values = text.split(';')
        processed_values = [str(max(int(value) if value else 0, 0)) for value in values]
        result = ';'.join(processed_values)
    except:
        result = text
    return result



def checkNegativeValuesInBbox(text):
    try:
        values = text.split(';')
        processed_values = [str(max(int(value) if value else 0, 0)) for value in values]
        result = ';'.join(processed_values)
    except:
        result = text
    return result
    
#################### sorting function of list #################
def time_sort_key(d):
    return d['irrd_in_time']


def job_sheet_time_sort_key(d):
    # print("JOBSHEETWISE ------------------------------------------------------------", d)
    return d['sort_id']#d['job_sheet_time']


def sort_irrd_time_(time_stamp_data):
    final_time_sort = sorted(time_stamp_data, key=time_sort_key, reverse=True)
    return final_time_sort


def sort_job_sheet_time_sort_key_(mongo_id_data):    
    final_time_sort = sorted(mongo_id_data, key=job_sheet_time_sort_key,reverse=True)
    return final_time_sort


def pass_all_panel_data_for_sorting(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    joinedlist = None
    try:
        for mix, i in enumerate(list_of_dict):
            if i['irrd_in_time'] is not None:
                time_stamp_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_(time_stamp_data)
            mongo_id_data = sort_job_sheet_time_sort_key_(mongo_id_data)
            joinedlist = time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            joinedlist = sort_irrd_time_(time_stamp_data)
        elif len(mongo_id_data) != 0:
            joinedlist = sort_job_sheet_time_sort_key_(mongo_id_data)
        else:
            pass
    except Exception as error:
        print('error --- ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- pass_all_panel_data_for_sorting 1", str(error), " ----time ---- ", now_time_with_time()])) 
        joinedlist = None
    return joinedlist

########################### for excel sorting list ###############
def time_sort_key_for_excel(d):
    return d['riro_data'][0]['irrd_in_time']


def job_sheet_time_sort_key_for_excel(d):
    return d['sort_id']#d['job_sheet_time']


def sort_irrd_time_for_excel(time_stamp_data):
    final_time_sort = sorted(time_stamp_data, key=time_sort_key_for_excel,reverse=True)
    return final_time_sort


def sort_job_sheet_time_sort_key_for_excel(mongo_id_data):
    final_time_sort = sorted(mongo_id_data, key= job_sheet_time_sort_key_for_excel, reverse=True)
    return final_time_sort


def riro_for_sorting_for_excel(list_of_dict):
    time_stamp_data = []
    mongo_id_data = []
    joinedlist = None
    try:
        for mix, i in enumerate(list_of_dict):
            if i['riro_data'][0]['irrd_in_time'] is not None:
                time_stamp_data.append(i)
            else:
                mongo_id_data.append(i)
        if len(time_stamp_data) != 0 and len(mongo_id_data) != 0:
            time_stamp_data = sort_irrd_time_for_excel(time_stamp_data)
            mongo_id_data = sort_job_sheet_time_sort_key_for_excel(mongo_id_data)
            joinedlist = time_stamp_data + mongo_id_data
        elif len(time_stamp_data) != 0:
            joinedlist = sort_irrd_time_for_excel(time_stamp_data)
        elif len(mongo_id_data) != 0:
            joinedlist = sort_job_sheet_time_sort_key_for_excel(mongo_id_data)
        else:
            pass
    except Exception as error:
        print('error --- ', error)
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- riro_for_sorting_for_excel 1", str(error), " ----time ---- ", now_time_with_time()])) 
        joinedlist = None
    return joinedlist

######################## camera api functions ######################## 
def check_dataobjects_of_cr_data(dataobjects):
    datacrobjectsstatus = True
    print('data objects ',dataobjects)
    for i,j in enumerate(dataobjects):
        print(j)
        if j['min_count'] < j['max_count']:
            datacrobjectsstatus = True
        elif j['min_count'] != j['max_count']:
            datacrobjectsstatus = True
        else:
            datacrobjectsstatus=False  
            break 
    return datacrobjectsstatus

def check_the_tc_data_is_key_idisexistCRdata(find_data,roiid):
    print("find_data===", find_data)
    print("roi-id",roiid)
    id_status = True
    for i , j in enumerate(find_data['cr_data']):  
        print('lllll====lllll ',j)
        if j['roi_id']=='' or j['roi_id'] == None:
            pass
        elif j['roi_id']==roiid:
            id_status = False
    return id_status

def update_cr_data_to_existing_one(fINDCRDATA,GivenCRDATA):
    find_cr = fINDCRDATA['cr_data']
    initial_len = len(find_cr)
    find_cr.append(GivenCRDATA)
    if initial_len > len(find_cr) :
        print('finall cr data ===', len(find_cr))
    return find_cr

def tc_data_modification(dbtcdata,requestdata):
    if dbtcdata is not None and requestdata is not None :
        if len(dbtcdata) !=0:
            if len(requestdata)==1:
                if requestdata[0] is not None:
                    dbtcdata.append(requestdata[0])
        else:
            dbtcdata = requestdata
    return dbtcdata

def check_the_tc_data_is_key_idisexist(find_data,roiid):
    id_status = True
    for i , j in enumerate(find_data):  
        if j['roi_id']==roiid:
            id_status = False
    return id_status

def delete_hooter_data(find_data):
    try:
        hooter_find_data = mongo.db.hooter_on_table.find_one({'rtsp_url':find_data['camera_rtsp'], 'cameraname': find_data['camera_name']})
        if hooter_find_data is not None:
            delete_data = mongo.db.hooter_on_table.delete_one({'rtsp_url':hooter_find_data['camera_rtsp'], 'cameraname': hooter_find_data['camera_name']})
            if delete_data.deleted_count > 0:
                ret = {'message': 'hooter is deleted successfully.','success': True}
            else:
                ret['message'] = 'data is not deleted, please try once again.'
        else:
            ret['message'] = 'for the given id there no data found, please change the id or try once again.'
    except Exception as error:
        ERRORLOGdata(" ".join(["\n", "[ERROR] packages -- delete_hooter_data 1", str(error), " ----time ---- ", now_time_with_time()])) 
        print(error)


