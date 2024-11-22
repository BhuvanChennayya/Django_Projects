

from Data_recieving_and_Dashboard.packages import *
from datetime import date
traffic_jam_management = Blueprint('traffic_jam_management', __name__)

Gettodaydate = datetime.today().strftime('%Y%m%d')

def get_five_hours_list():
    # Get the current time
    current_time = datetime.now()

    # Calculate the time 5 hours ago
    five_hours_ago = current_time - timedelta(hours=5)

    # Generate the list of times for the latest 5 hours
    times_in_last_five_hours = [five_hours_ago + timedelta(hours=i) for i in range(6)]

    five_hours_list = []
    for time in times_in_last_five_hours:
        # print(time.strftime("%m/%d/%Y, %H:%M:%S"))
        # five_hours_list.append(time.strftime("%d-%m-%Y %H:%M:%S")) #"%m-%d-%Y, %H:%M:%S"))
        five_hours_list.append(time.strftime("%d-%m-%Y %H:%M:%S")) 

    # print("LATEST FIVE HOURS LIST", five_hours_list)
    return five_hours_list


# def get_last_five_hours(current_time):
#     # Given time
#     given_time = datetime.strptime(current_time, '%d-%m-%Y %H:%M:%S')

#     # Set minutes and seconds to 00
#     given_time = given_time.replace(minute=0, second=0, microsecond=0)

#     # Subtract 5 hours to get the start time
#     start_time = given_time - timedelta(hours=5)

#     # Generate all timestamps between start_time and given_time
#     timestamps = []
#     current = start_time
#     while current <= given_time:
#         timestamps.append(current.strftime('%d-%m-%Y %H:%M:%S'))
#         current += timedelta(hours=1)

#     print("times_in_last_five_hours:----------", timestamps)
#     return timestamps


def get_last_five_hours(current_time):
    # Given time
    given_time = datetime.strptime(current_time, '%d-%m-%Y %H:%M:%S')

    # Set minutes and seconds to 00
    given_time = given_time.replace(minute=0, second=0, microsecond=0)

    # Subtract 5 hours to get the start time
    start_time = given_time - timedelta(hours=4)

    # Set the end time to one hour after the given time
    end_time = given_time + timedelta(hours=1)

    # Generate all timestamps between start_time and end_time (inclusive)
    timestamps = []
    current = start_time
    while current <= end_time:
        timestamps.append(current.strftime('%d-%m-%Y %H:%M:%S'))
        current += timedelta(hours=1)

    print("times_in_last_five_hours:----------", timestamps)
    return timestamps


def capture_image_rtsp(rtsp_url, image_path):
  # Create a VideoCapture object
    cap = cv2.VideoCapture(rtsp_url)

    # Check if the connection was successful
    if not cap.isOpened():
        print("Error: Could not open video stream")
    else:
        # Read a frame from the stream
        ret, frame = cap.read()
        
        if ret:
            # Define the local path to save the image
            current_time = datetime.now()
            image_name = "tjm_cam_" + str(current_time) + ".jpg"
            image_path = os.path.join(image_path,image_name)
            
            # Save the frame as an image
            cv2.imwrite(image_path, frame)
            
            print(f"Image saved to {image_path}")
        else:
            print("Error: Could not read frame from stream")

    # Release the VideoCapture object
    cap.release()
    return image_name

"""Capture image by reading RTSP"""
@traffic_jam_management.route('/capture_image', methods=['POST'])
def capture_image():
    ret = {'success': False, 'message': 'Something went wrong.'}
    jsonobject = request.json
    if jsonobject == None:
        jsonobject = {}
    request_key_array = ['rtsp_url']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)

    if not missing_key:
        output = [k for k, v in jsonobject.items() if v == '']
        
        if output:
            ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
        
        else:
            base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'flask_applications', 'tjm_frames')

            # Check if the folder exists
            if not os.path.exists(base_path):
                # If it doesn't exist, create the folder
                os.makedirs(base_path)
                # print(f"Folder '{base_path}' created.")
                
            else:
                print(" ")
                # print(f"Folder '{base_path}' already exists.")

            
            image_file = capture_image_rtsp(jsonobject["rtsp_url"], base_path)
            print("IIMAGE Name:----------", image_file)
                

            CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'flask_applications', 'tjm_frames',image_file)
            if file_exists(CHECKIMAGE): 
                # print("EXISTED----------------------------------------")
                file_path = os.path.join(base_path, image_file)
                source_img = Image.open(file_path)
                imgByteArr = io.BytesIO()
                source_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file)
            
            else:
                # print("NOT 1111111111111 EXISTED----------------------------------------")
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)
            
    else:
        ret = {'success': False, 'message':" ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}  
        return ret
            

"""LATEST HOUR DATA OF ALL CAMERA"""
@traffic_jam_management.route('/latest_hour_TJM_data', methods=['GET'])
def latest_hour_TJM_data():
  tjm_data_list = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate([
  {
    "$match": {
      "date": Gettodaydate #,
      # "analytics_log.status": "Detected"
    }
  },
  {
    "$sort": {
      "timestamp": -1
    }
  },
  {
    "$group": {
      "_id": {
        "department": "$department",
        "camera_name": "$camera_name",
        "roi_name": "$roi_name"
      },
      "latestDocument": { "$first": "$$ROOT" }
    }
  },
  {
    "$group": {
      "_id": {
        "department": "$_id.department",
        "camera_name": "$_id.camera_name"
      },
      "rois": {
        "$push": {
          "roi_name": "$_id.roi_name",
          "status": {"$arrayElemAt": ["$latestDocument.analytics_log.status", -1]},
          # "Preset_percentage": {"$arrayElemAt": ["$latestDocument.analytics_log.Preset_percentage", -1]},
          "Preset_percentage": { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] },
          # "traffic_percentage": {"$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1]},
          "timestamp": "$latestDocument.timestamp",
          "traffic_percentage": {
              "$ifNull": [
                { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
                0
              ]}
        }
      },
      "latestDocument": { "$first": "$latestDocument" }
    }
  },
  {
    "$group": {
      "_id": "$_id.department",
      "rois": {
        "$push": {
          "camera_name": "$_id.camera_name",
          "roi_details": "$rois"
        }
      },
      "latestDocument": { "$first": "$latestDocument" }
    }
  },
  {
    "$project": {
      "_id": 0,
      "department": "$latestDocument.department",
      "rois": 1
    }
  },
  {
    "$sort": {
      "rois.camera_name": 1  # Sort by camera_name in ascending order
    }
  }
]))

  # print("tjm_data_listtjm_data_listtjm_data_list:---", tjm_data_list)
  if len(tjm_data_list) != 0:
      result = {"message":tjm_data_list, "success":True}

  else:
      result = {"message":"Data not found.", "success":False}
      
  return result

  # return current_hour_data


@traffic_jam_management.route('/test_todays_data', methods=['GET'])
def test_todays_data():
    
    # Replace this with your date field format
    start_of_day = datetime.combine(datetime.now().date(), datetime.min.time())
    end_of_day = datetime.combine(datetime.now().date(), datetime.max.time())

    print(f"Debug: Querying between {start_of_day} and {end_of_day}")
    print(f"date================{Gettodaydate}")

    # Test basic find query to check if any document exists for today's date
    test_data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find({
        "date": Gettodaydate
    }))

    print(f"Debug: Test query result: {test_data}")

    if test_data:
        return {"message": "Test query successful", "data": parse_json(test_data), "success": True}
    else:
        return {"message": "No data found for today's date", "success": False}




"""OVERALL TODAYS DATA(Including DETECTED, COMPLETED, ERROR)"""
@traffic_jam_management.route('/overall_todays_TJM_data', methods=['GET'])
def overall_to222days_TJM_data():
    result = {'success': False, 'message': 'Something went wrong with overall_to222days_TJM_data.'}
    tjm_data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate([
    {
      "$match": {
        "date": Gettodaydate
      }
    },
    {
      "$sort": {
        "timestamp": -1
      }
    },
    {
      "$group": {
        "_id": {
          "department": "$department",
          "camera_name": "$camera_name",
          "roi_name": "$roi_name"
        },
        "latestDocument": { "$first": "$$ROOT" }
      }
    },
    # {
    #   "$group": {
    #     "_id": {
    #       "department": "$_id.department",
    #       "camera_name": "$_id.camera_name"
    #     },
    #     "rois": {
    #       "$push": {
    #         "roi_name": "$_id.roi_name",
    #         "status": { "$arrayElemAt": ["$latestDocument.analytics_log.status", -1] },
    #         # "Preset_percentage": { "$arrayElemAt": ["$latestDocument.analytics_log.Preset_percentage", -1] },
    #         "Preset_percentage": { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] },
    #         "detected_percentage": { "$arrayElemAt": ["$latestDocument.analytics_log.detected_percentage", -1] },
    #         "cleared_percentage": { "$arrayElemAt": ["$latestDocument.analytics_log.cleared_percentage", -1] },
    #         # "traffic_percentage": {
    #         #   "$ifNull": [
    #         #     { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
    #         #     0
    #         #   ]
    #         # },
    #         "detected_time": "$latestDocument.timestamp"
    #       }
    #     },
    #     "latestDocument": { "$first": "$latestDocument" }
    #   }
    # }
 
#  {
#   "$group": {
#     "_id": {
#       "department": "$_id.department",
#       "camera_name": "$_id.camera_name"
#     },
#     "rois": {
#       "$push": {
#         "roi_name": { "$ifNull": ["$_id.roi_name", "Unknown"] },
#         "status": {
#           "$ifNull": [
#             { "$arrayElemAt": ["$latestDocument.analytics_log.status", -1] },
#             "Unknown"  # Default to "Unknown" if status is null or missing
#           ]
#         },
#         "Preset_percentage": {
#           "$ifNull": [
#             { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] },
#             0  # Default to 0 if Preset_percentage is missing
#           ]
#         },
#         "detected_percentage": {
#           "$cond": {
#             "if": {
#               "$or": [
#                 { "$eq": [{ "$arrayElemAt": ["$latestDocument.analytics_log.detected_percentage", -1] }, None] },
#                 { "$eq": [{ "$arrayElemAt": ["$latestDocument.analytics_log.detected_percentage", -1] }, 0] }
#               ]
#             },
#             "then": {
#               "$ifNull": [
#                 { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
#                 0  # Default to 0 if traffic_percentage is missing
#               ]
#             },
#             "else": { "$arrayElemAt": ["$latestDocument.analytics_log.detected_percentage", -1] }
#           }
#         },
#         "cleared_percentage": {
#           "$ifNull": [
#             { "$arrayElemAt": ["$latestDocument.analytics_log.cleared_percentage", -1] },
#             None  # Default to null if cleared_percentage is missing
#           ]
#         },
#         "detected_time": {
#           "$ifNull": [
#             "$latestDocument.timestamp",
#             "Unknown"  # Default to "Unknown" if detected_time is missing
#           ]
#         }
#       }
#     },
#     "latestDocument": { "$first": "$latestDocument" }
#   }
# }




#worked one ###################
# {
#   "$group": {
#     "_id": {
#       "department": "$_id.department",
#       "camera_name": "$_id.camera_name"
#     },
#     "rois": {
#       "$push": {
#         "roi_name": { "$ifNull": ["$_id.roi_name", "Unknown"] },
#         "status": {
#           "$ifNull": [
#             { "$arrayElemAt": ["$latestDocument.analytics_log.status", -1] },
#             "free"
#           ]
#         },
#         "Preset_percentage": {
#           "$ifNull": [
#             { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] },
#             0
#           ]
#         },
#         "detected_percentage": {
#           "$cond": {
#             "if": {
#               "$or": [
#                 { "$eq": [ { "$size": "$latestDocument.analytics_log" }, 0 ] }
#               ]
#             },
#             "then": {
#               "$ifNull": [
#                 { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
#                 0
#               ]
#             },
#             "else": { "$arrayElemAt": ["$latestDocument.analytics_log.detected_percentage", -1] }
#           }
#         },
#         "cleared_percentage": {
#           "$ifNull": [
#             { "$arrayElemAt": ["$latestDocument.analytics_log.cleared_percentage", -1] },
#             0
#           ]
#         },
#         "detected_time": {
#           "$ifNull": [
#             "$latestDocument.timestamp",
#             "Unknown"
#           ]
#         }
#       }
#     },
#     "latestDocument": { "$first": "$latestDocument" }
#   }
# }
{
  "$group": {
    "_id": {
      "department": "$_id.department",
      "camera_name": "$_id.camera_name"
    },
    "rois": {
      "$push": {
        "roi_name": { "$ifNull": ["$_id.roi_name", "Unknown"] },
        "status": {
          "$cond": {
            "if": {
              "$gt": [
                { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
                { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] }
              ]
            },
            "then":"Detected",
            "else": "free"
          }
        },
        "Preset_percentage": {
          "$ifNull": [
            { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] },
            0
          ]
        },
        "detected_percentage": {
          "$cond": {
            "if": {
              "$gt": [
                { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
                { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] }
              ]
            },
            "then": {
              "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1]
            },
            "else": {
              "$ifNull": [
                { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
                0
              ]
            }
          }
        },
        "cleared_percentage": {
          "$ifNull": [
            { "$arrayElemAt": ["$latestDocument.analytics_log.cleared_percentage", -1] },
            0
          ]
        },
        "detected_time": {
          "$ifNull": [
            "$latestDocument.timestamp",
            "Unknown"
          ]
        }
      }
    },
    "latestDocument": { "$first": "$latestDocument" }
  }
}





    ,
    {
      "$group": {
        "_id": "$_id.department",
        "rois": {
          "$push": {
            "camera_name": "$_id.camera_name",
            "rtsp_url":"$latestDocument.camera_rtsp",
            "camera_ip":"$latestDocument.camera_ip",
            "roi_details": "$rois"
          }
        },
        "latestDocument": { "$first": "$latestDocument" }
      }
    },
    {
      "$project": {
        "_id": 0,
        "department": "$latestDocument.department",
        "rois": 1
      }
    },
    # {
    #   "$sort": {
    #     "rois.camera_name": 1  # Sort by camera_name in ascending order
    #   }
    # }
  ]))


    if len(tjm_data) != 0:
        result = {"message":parse_json(tjm_data), "success":True}
    else:
        result = {"message":"Data not found.", "success":False}
        
    return result



"""TRAFFIC JAM LIVE DATA CAMERA NAME WISE"""
@traffic_jam_management.route('/live_traffic_jam_data', methods=['GET'])
def live_traffic_jam_data():
    result = {'success': False, 'message': 'Something went wrong with live_traffic_jam_data.'}
    # tjm_data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find({"date":Gettodaydate, "analytics_log.status":"Detected"}, {"_id":0}).sort("timestamp", -1))
    
    tjm_data_list = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate([
  {
    "$match": {
      "date": Gettodaydate,
      "analytics_log.status": "Detected"
    }
  },
  {
    "$sort": {
      "timestamp": -1
    }
  },
  {
    "$group": {
      "_id": "$camera_name",
      "rois": {
            "$push": {
            "roi_name": "$roi_name",
            "status": {"$arrayElemAt": ["$analytics_log.status", -1] },
            "analytics_log": {"$arrayElemAt": ["$analytics_log.Preset_percentage", -1] }, #"$analytics_log.Preset_percentage",
            "dashboard_log": {"$arrayElemAt": ["$dashboard_log.traffic_percentage", -1] }, # "$dashboard_log.traffic_percentage",
            "timestamp": "$timestamp"
            }
        },
        "latestDocument": { "$first": "$$ROOT" }
        }
    },
  {
    "$project": {
      "_id": 0,
      "camera_name": "$latestDocument.camera_name",
      "department": "$latestDocument.department",
      "camera_rtsp":"$latestDocument.camera_rtsp",
      "rois": 1
      }
  },
  {
    "$sort": {
      "department": 1  # Sort by camera_name in ascending order
    }
  }
]))
    
    if len(tjm_data_list) != 0:
        result = {"message":tjm_data_list, "success":True}

    else:
        result = {"message":"Data not found.", "success":False}
        
    return result


"""TRAFFIC JAM LIVE DATA DEPARTMENT NAME WISE"""
@traffic_jam_management.route('/live_trafficjam_data', methods=['GET'])
def live_trafficjam_data():
    result = {'success': False, 'message': 'Something went wrong with live_trafficjam_data.'}
    
    tjm_data_list = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate([
  {
    "$match": {
      "date": Gettodaydate #,
      #"analytics_log.status": "Detected"
    }
  },
  {
    "$sort": {
      "timestamp": -1
    }
  },
  {
    "$group": {
      "_id": {
        "department": "$department",
        "camera_name": "$camera_name",
        "roi_name": "$roi_name"
      },
      "latestDocument": { "$first": "$$ROOT" }
    }
  },
  {
    "$group": {
      "_id": {
        "department": "$_id.department",
        "camera_name": "$_id.camera_name"

      },
      "rois": {
        "$push": {
          "roi_name": "$_id.roi_name",
          # "rtsp":"$latestDocument.camera_rtsp",
          "status": {"$arrayElemAt": ["$latestDocument.analytics_log.status", -1]},
          # "Preset_percentage": {"$arrayElemAt": ["$latestDocument.analytics_log.Preset_percentage", -1]},
          "Preset_percentage": { "$arrayElemAt": ["$latestDocument.dashboard_log.Preset_percentage", -1] },
          "remark": {"$arrayElemAt": ["$latestDocument.analytics_log.remark", -1]},
          "timestamp": "$latestDocument.timestamp",
          "traffic_percentage": {
              "$ifNull": [
                { "$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1] },
                0
              ]}
        }
      },
      "latestDocument": { "$first": "$latestDocument" }
    }
  },
  {
    "$group": {
      "_id": "$_id.department",
      "rois": {
        "$push": {
          "camera_name": "$_id.camera_name",
          "rtsp_url":"$latestDocument.camera_rtsp",
          "roi_details": "$rois"
        }
      },
      "latestDocument": { "$first": "$latestDocument" }
    }
  },
  {
    "$project": {
      "_id": 0,
      "department": "$latestDocument.department",
      "rois": 1
    }
  },
  {
    "$sort": {
      "rois.camera_name": 1  # Sort by camera_name in ascending order
    }
  }
]))

    if len(tjm_data_list) != 0:
        result = {"message":tjm_data_list, "success":True}

    else:
        result = {"message":"Data not found.", "success":False}
        
    return result

"""TODAYS ROI-NAMES LIST"""
@traffic_jam_management.route('/TJM/rois_list', methods=['GET'])
def get_rois_list():
    result = {"message":"Something went wrong with cameralist", "success":False}
    # TJM_cameras_Data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find({"date":Gettodaydate},{'_id':0, 'dashboard_log':0}).sort('timestamp', -1))
    TJM_rois = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.distinct("roi_name", {"date": Gettodaydate})

    if len(TJM_rois) != 0:
        result = {"message": TJM_rois, "status":True}

    else:
        result = {"message": "Data not found.", "status":False}
    return result


"""DATEWISE ROI-NAMES LIST"""
@traffic_jam_management.route('/TJM/datewise_rois_list', methods=['POST'])
def datewise_rois_list():
    ret = {'success': False, 'message': 'Something went wrong.'}
    jsonobject = request.json
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
            TJM_roi_names_list = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.distinct("roi_name", {'timestamp':{'$gte':from_date, '$lte': to_date}})
            
            if len(TJM_roi_names_list) != 0:
                ret = {"message":TJM_roi_names_list, "status":True}

            else:
                ret = {"message":"There is no cameras.", "status":False}

    else:
        ret = {'success': False, 'message':" ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}

    return ret

"""TODAYS CAMERAS LIST"""
@traffic_jam_management.route('/TJM/cameralist', methods=['GET'])
def get_cameralist():
    result = {"message":"Something went wrong with cameralist", "success":False}
    # TJM_cameras_Data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find({"date":Gettodaydate},{'_id':0, 'dashboard_log':0}).sort('timestamp', -1))
    TJM_cameras = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.distinct("camera_name", {"date": Gettodaydate})

    if len(TJM_cameras) != 0:
        result = {"message": TJM_cameras, "status":True}

    else:
        result = {"message": "Data not found.", "status":False}
    return result

"""DATEWISE CAMERA LIST"""
@traffic_jam_management.route('/TJM/datewise_camera_list', methods=['POST'])
def datewise_camera_list():
    ret = {'success': False, 'message': 'Something went wrong.'}
    jsonobject = request.json
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
            TJM_cameras_list = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.distinct("camera_name", {'timestamp':{'$gte':from_date, '$lte': to_date}})
            
            if len(TJM_cameras_list) != 0:
                ret = {"message":TJM_cameras_list, "status":True}

            else:
                ret = {"message":"There is no cameras.", "status":False}

    else:
        ret = {'success': False, 'message':" ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}

    return ret



def hour_time_tjm_percent(hourly_log, analytics_log, TJM_data, five_hours_list, idx):
    # print("Hourly_log-----------------------------------------", len(hourly_log))
    # print("analytics_log-----------------------------------------",five_hours_list)
    for analytics_data in TJM_data: 
        taking_available_data = []

        for h_log in hourly_log:
            
            # Debugging information to understand the values of time ranges and conditions
            print("h_logh_log:--------------", five_hours_list[idx][-8:], five_hours_list[idx + 1][-8:])
            
            # Check if the log's start and stop times fall within the specified five-hour interval
            if h_log["start_time"] <= five_hours_list[idx][-8:] and h_log["stop_time"] <= five_hours_list[idx + 1][-8:]:
                traffic_percent = h_log["traffic_percentage"]
                
                # Check if analytics data has the necessary logs
                if len(analytics_data["dashboard_log"]) != 0 and len(analytics_data["analytics_log"]) != 0:
                    
                    # Add h_log to the list if it's not already there
                    if h_log not in taking_available_data:
                        taking_available_data.append(h_log)
            else:
                print("--------WRONG----")
                pass
                # taking_available_data = []


    return taking_available_data 

#REPLACE THIS FUN IN traffic_jam_mangement.py
"""UPDATED LATEST FIVE HOURS DATA"""
@traffic_jam_management.route('/latest_five_hours_traffic_jam', methods=['POST'])
def updated_latest_five_hours_traffic_jam():
    result = {'success': False, 'message': 'Something went wrong.'}
    current_time = datetime.now()

    five_hours_list = get_last_five_hours(datetime.now().strftime('%d-%m-%Y %H:%M:%S')) # '%Y-%m-%d %H:%M:%S'))
    print("five_hours_list 2222222222222222222", five_hours_list) #[0], five_hours_list[-1]) -5] + '00:00'
    jsonobject = request.json
    request_key_array = ['camera_name', 'department', 'roi_name']
    jsonobjectarray = list(set(jsonobject))
    missing_key = set(request_key_array).difference(jsonobjectarray)
    if not missing_key:
      output = [k for k, v in jsonobject.items() if v == '']
      if output:
          result['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
      
      else:
        five_hours_list_data = []
        TJM_rois = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.distinct("roi_name", {"date": Gettodaydate})
        # print("TJM_ROIS:---------------", TJM_rois)
        start_index = 0
        end_index = 5
        traffic_jam_true_status_roi_data = []
        traffic_jam_empty_status_roi_data = []
        # traffic_percent=0.0
        for idx, time_value in enumerate(five_hours_list[start_index:end_index], start=start_index):
            if len(jsonobject["roi_name"]) != 0:
                for roi_n in jsonobject["roi_name"]:
                    # Convert to datetime object
                    # print("five_hours_list[idx + 1][-8:]", five_hours_list[idx + 1])
                    datetime_obj = datetime.strptime(five_hours_list[idx + 1], "%d-%m-%Y %H:%M:%S")

                    # Format as "YYYYMMDD"
                    formatted_date = datetime_obj.strftime("%Y%m%d")

                    variable = {
                        "$and": [
                            {"hourly_log.stop_time": {"$lte": five_hours_list[idx + 1][-8:]}},
                            {"hourly_log.start_time": {"$gte": five_hours_list[idx][-8:]}}
                        ],
                        "camera_name": jsonobject["camera_name"],
                        "department": jsonobject["department"],
                        "roi_name": roi_n, "date":formatted_date
                        # "analytics_log.cleared_time": {"$gte": five_hours_list[0], "$lte": five_hours_list[-1]}
                    }

                    TJM_data = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find_one(variable, {"_id": 0}) #.sort('timestamp', -1))
                    # print("TJM DATA:----------------------", len(TJM_data))
                    traffic_percent=0.0
                    if TJM_data != None:
                        analytics_data = TJM_data
                        # print("analytics_data:-----------------------", analytics_data["hourly_log"])
                        for h_log in analytics_data["hourly_log"]:
                            if five_hours_list[idx][-8:] <= h_log["start_time"] <= five_hours_list[idx + 1][-8:] and five_hours_list[idx][-8:] <= h_log["stop_time"] <= five_hours_list[idx + 1][-8:]:
                                # print("HOURLY LOG",five_hours_list[idx][-8:], five_hours_list[idx + 1][-8:], h_log["traffic_percentage"]) # analytics_data["hourly_log"])
                                traffic_percent = h_log["traffic_percentage"]
                            # else:
                            #     print("HOURLY LOG else condition111111111111111111111",five_hours_list[idx][-8:], five_hours_list[idx + 1][-8:], h_log["traffic_percentage"])
                                

                        # if len(analytics_data["dashboard_log"]) != 0 and len(analytics_data["analytics_log"]) != 0 and len(analytics_data["hourly_log"]) != 0:
                        if len(analytics_data["analytics_log"]) != 0:
                            traffic_jam_true_status_roi_data.append({
                                "from_interval_timestamp": five_hours_list[idx][-8:], #five_hours_list[idx + 1][-8:],
                                "to_interval_timestamp":five_hours_list[idx + 1][-8:],
                                "camera_name": analytics_data["camera_name"],
                                "department": analytics_data["department"],
                                "roi_name": roi_n,
                                "traffic_percentage": traffic_percent,
                                "Preset_percentage": analytics_data["analytics_log"][-1]["Preset_percentage"],
                                "cleared_percentage": analytics_data["analytics_log"][-1]["cleared_percentage"]
                            })


                    else:
                        traffic_jam_true_status_roi_data.append({
                            # "timestamp": five_hours_list[idx + 1][-8:],
                            "from_interval_timestamp": five_hours_list[idx][-8:], #five_hours_list[idx + 1][-8:],
                            "to_interval_timestamp":five_hours_list[idx + 1][-8:],
                            "camera_name": jsonobject["camera_name"],
                            "department": jsonobject["department"],
                            "roi_name": roi_n,
                            "traffic_percentage": 0,
                            "Preset_percentage": 0.0,
                            "cleared_percentage":0.0
                        })

            else:
                datetime_obj = datetime.strptime(five_hours_list[idx + 1], "%d-%m-%Y %H:%M:%S")
                # Format as "YYYYMMDD"
                formatted_date = datetime_obj.strftime("%Y%m%d")
                for roi_name in TJM_rois:
                    variable = {
                        "$and": [
                            {"hourly_log.stop_time": {"$lte": five_hours_list[idx + 1][-8:]}},
                            {"hourly_log.start_time": {"$gte": five_hours_list[idx][-8:]}}
                        ],
                        "camera_name": jsonobject["camera_name"],
                        "department": jsonobject["department"],
                        "roi_name": roi_name,  "date":formatted_date
                        # "analytics_log.cleared_time": {"$gte": five_hours_list[0], "$lte": five_hours_list[-1]}
                    }
                    
                    TJM_data = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find_one(variable, {"_id": 0}) #.sort('timestamp', -1))
                    # print("TJM DATA:----------------------", len(TJM_data))
                    traffic_percent=0.0
                    if TJM_data != None:
                        analytics_data = TJM_data
                        for h_log in analytics_data["hourly_log"]:
                            if five_hours_list[idx][-8:] <= h_log["start_time"] <= five_hours_list[idx + 1][-8:] and five_hours_list[idx][-8:] <= h_log["stop_time"] <= five_hours_list[idx + 1][-8:]:
                                print("HOURLY LOG", h_log["traffic_percentage"]) # analytics_data["hourly_log"])
                                traffic_percent = h_log["traffic_percentage"]

                        # if len(analytics_data["dashboard_log"]) != 0 and len(analytics_data["analytics_log"]) != 0 and len(analytics_data["hourly_log"]) != 0:
                        if len(analytics_data["analytics_log"]) != 0:
                            traffic_jam_true_status_roi_data.append({
                                "from_interval_timestamp": five_hours_list[idx][-8:], # five_hours_list[idx + 1][-8:],
                                "to_interval_timestamp":five_hours_list[idx + 1][-8:], #five_hours_list[idx][-8:],
                                "camera_name": analytics_data["camera_name"],
                                "department": analytics_data["department"],
                                "roi_name": roi_name,
                                "traffic_percentage": traffic_percent,
                                "Preset_percentage": analytics_data["analytics_log"][-1]["Preset_percentage"],
                                "cleared_percentage": analytics_data["analytics_log"][-1]["cleared_percentage"]
                            })
                    else:
                        traffic_jam_true_status_roi_data.append({
                            # "timestamp": five_hours_list[idx + 1][-8:],
                            # "to_timestamp":five_hours_list[idx][-8:],
                            "from_interval_timestamp": five_hours_list[idx][-8:], # five_hours_list[idx + 1][-8:],
                            "to_interval_timestamp":five_hours_list[idx + 1][-8:],
                            "camera_name": jsonobject["camera_name"],
                            "department": jsonobject["department"],
                            "roi_name": roi_name,
                            "traffic_percentage": 0,
                            "Preset_percentage": 0.0,
                            "cleared_percentage":0.0
                        })

        result = {"message": {"traffic_true_message":traffic_jam_true_status_roi_data, "traffic_false_message":traffic_jam_empty_status_roi_data}, "success": True}

        formatted_data = {"message": [], "success": result["success"]}

        department_dict = {}

        for msg_type in ["traffic_false_message", "traffic_true_message"]:
            for item in result["message"][msg_type]:
                department = item["department"]
                camera_name = item["camera_name"]
                roi_name = item["roi_name"]
                # status = item["status"]
                from_interval_timestamp = item["from_interval_timestamp"]
                to_interval_timestamp = item["to_interval_timestamp"]
                Preset_percentage = item["Preset_percentage"]
                traffic_percentage = item["traffic_percentage"]
                cleared_percentage= item["cleared_percentage"]

                if department not in department_dict:
                    department_dict[department] = {}
                
                if camera_name not in department_dict[department]:
                    department_dict[department][camera_name] = []

                department_dict[department][camera_name].append({
                    "Preset_percentage": Preset_percentage,  # Assuming default value as 0, update if required
                    "detected_percentage": traffic_percentage,  # Assuming default value as 0.0, update if required
                    "roi_name": roi_name,
                    # "status": status,
                    "from_interval_timestamp": from_interval_timestamp,
                    "to_interval_timestamp":to_interval_timestamp,
                    "cleared_percentage":cleared_percentage
                })

        for department, cameras in department_dict.items():
            rois = []
            for camera_name, roi_details in cameras.items():
                rois.append({
                    "camera_name": camera_name,
                    "roi_details": roi_details
                })
            formatted_data["message"].append({
                "department": department,
                "rois": rois
            })

    if len(result) != 0:
      result = formatted_data

    else:
      result = {"message":"Data not found.", "success":False}

    return result



"""LATEST TRAFFIC JAM DATA"""
@traffic_jam_management.route('/latest_traffic_jam_history', methods=['GET'])
def latest_history():
    result = {"message":"Something went wrong with 'latest_traffic_jam_history'", "success":False}
    data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate([
  {
    "$match": {
      "date": Gettodaydate,
      "analytics_log.status": "Detected"
    }
  },
  {
    "$sort": {
      "timestamp": -1
    }
  },
  {
      "$project":{
          "_id":0
      }
  },
  {
    "$limit": 1
  }
]))

    if len(data) != 0:
      result = {"message":data, "success":True}

    else:
        result = {"message":"Data not found.", "success":False}

    return result

@traffic_jam_management.route('/tjm_datewise_history', methods=['POST'])
def tj_datewise_history():
    ret = {'success': False, 'message': 'Something went wrong with tjm_datewise_history.'}
    try:
        jsonobject = request.json
        # print("parking_type", jsonobject) # jsonobject["parking_type"])
        if jsonobject == None:
            jsonobject = {}

        request_key_array = ['from_date', 'to_date', 'cameraname', 'department', 'tjm_value']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        print("jsonobjectjsonobject:---------", jsonobject)

        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            
            if output:
                ret['message'] = "You have missed these parameters " + str(output) + " to enter. Please enter properly."
            
            else:
                from_date = jsonobject['from_date']
                to_date = jsonobject['to_date']
                tjm_value = jsonobject['tjm_value']
                cameraname = jsonobject['cameraname']
                department = jsonobject['department']
                
                match_query = {}
                
                if from_date and to_date:
                    match_query['timestamp'] = {'$gte': from_date, '$lte': to_date}

                if cameraname:
                    match_query['camera_name'] = cameraname

                if department:
                    match_query['department'] = department

                if tjm_value is not None:
                    print("TJM VALUE:", tjm_value)
                    if tjm_value == True:
                        match_query['analytics_log.status'] = "Detected"
                    
                    else:
                        match_query['analytics_log.status'] = "Completed"
                    # match_query['analytics_log.status'] = "Detected" if tjm_value else "Completed"
    
                tjm_data_list = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate([
                                    {"$match": match_query},
                                    {"$addFields": {
                                        "timestamp": {
                                            "$cond": {
                                                "if": {"$isNumber": "$timestamp"},
                                                "then": {"$toDate": "$timestamp"},
                                                "else": {
                                                    "$cond": {
                                                        "if": {"$eq": [{"$type": "$timestamp"}, "string"]},
                                                        "then": {"$dateFromString": {"dateString": "$timestamp"}},
                                                        "else": "$timestamp"
                                                    }
                                                }
                                            }
                                        }
                                    }},
                                    {"$sort": {"timestamp": -1}},
                                    {"$group": {
                                        "_id": {"department": "$department", "camera_name": "$camera_name", "roi_name": "$roi_name"},
                                        "latestDocument": {"$first": "$$ROOT"}
                                    }},
                                    {"$project": {
                                        "latestDocument._id": 0  # Exclude _id field from latestDocument
                                    }},
                                    {"$group": {
                                        "_id": {"department": "$_id.department", "camera_name": "$_id.camera_name"},
                                        "rois": {"$push": {
                                            "roi_name": "$_id.roi_name",
                                            # "traffic_percentage": {"$arrayElemAt": ["$latestDocument.dashboard_log.traffic_percentage", -1]},
                                            # "timestamp": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$latestDocument.timestamp"}},
                                            "log_details": "$latestDocument.analytics_log"

                                        }},
                                        "latestDocument": {"$first": "$latestDocument"}
                                    }},
                                    {"$group": {
                                        "_id": "$_id.department",
                                        "rois": {"$push": {
                                            "camera_name": "$_id.camera_name",
                                            "camera_ip": "$latestDocument.camera_ip",
                                            "roi_details": "$rois"
                        }},
                        "latestDocument": {"$first": "$latestDocument"}
                    }},
                    {"$project": {
                        "_id": 0,
                        "department": "$latestDocument.department",
                        "rois": 1
                    }},
                    {"$sort": {"rois.camera_name": 1}}
                  ]))
            
                if tjm_data_list:
                    ret = {'success': True, 'message': tjm_data_list}
                else:
                    ret = {'success': False, 'message': 'data not found'}
        else:
            ret = {'success': False, 'message': 'Missing required keys: ' + str(missing_key)}

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
    return jsonify(ret)



"""DATEWISE  HOURS DATA"""
@traffic_jam_management.route('/datewise_hours_traffic_jam', methods=['POST'])
def datewise_hours_traffic_jam():
  # result = {'success': False, 'message': 'Something went wrong.'}
  # from datetime import datetime, timedelta

  result = {'success': False, 'message': 'Something went wrong.'}
  jsonobject = request.json
  request_key_array = ['from_date', 'to_date'] #'camera_name', 'department', 'roi_name', 'from_date', 'to_date']
  jsonobjectarray = list(set(jsonobject))
  missing_key = set(request_key_array).difference(jsonobjectarray)

  if not missing_key:
      output = [k for k, v in jsonobject.items() if v == '']
      if output:
          result['message'] = "You have missed these parameters " + str(output) + " to enter. Please enter properly."
      else:
          from_date_str = jsonobject['from_date']
          to_date_str = jsonobject['to_date']
          from_date = datetime.strptime(from_date_str, '%Y-%m-%d %H:%M:%S')
          to_date = datetime.strptime(to_date_str, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)  # Include the end date

          TJM_rois = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.distinct(
                "roi_name",
                {"timestamp": {'$gte': from_date_str, '$lt': to_date_str}}
            )
          print("TJM ROIS:", len(TJM_rois))
          traffic_jam_true_status_roi_data = []
          traffic_jam_empty_status_roi_data = []
          
          current_date = from_date
          while current_date < to_date:
              for hour in range(24):
                  start_time = current_date + timedelta(hours=hour)
                  end_time = start_time + timedelta(hours=1)

                  for roi_name in TJM_rois:
                      print("ROI_name", roi_name)
                      TJM_all_roi_data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find({
                          "timestamp": {'$gte': start_time, '$lt': end_time},
                          "roi_name": roi_name
                      }, {"_id": 0}).sort('timestamp', -1))

                      print("TJM_all_roi_data", len(TJM_all_roi_data))
                      if TJM_all_roi_data:
                          print("jsonobject------------------------11111111111------------['roi_name]", len(TJM_all_roi_data))
                          for analytics_data in TJM_all_roi_data:
                              if len(analytics_data["dashboard_log"]) != 0 and len(analytics_data["analytics_log"]) != 0:
                                  traffic_jam_true_status_roi_data.append({
                                      "timestamp": end_time.strftime('%Y-%m-%d %H:%M:%S'),
                                      "camera_name": analytics_data["camera_name"],
                                      "department": analytics_data["department"],
                                      "roi_name": analytics_data["roi_name"],
                                      "status": analytics_data["analytics_log"][-1]["status"],
                                      "traffic_percentage": analytics_data["dashboard_log"][-1]["traffic_percentage"],
                                      "Preset_percentage": analytics_data["analytics_log"][-1]["Preset_percentage"]
                                  })
                      else:
                          TJM_all_roi_data_1 = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find({
                              "roi_name": roi_name
                          }, {"_id": 0}).sort('timestamp', -1))
                          print("TJM_all_roi_data_1", len(TJM_all_roi_data_1))
                          if len(TJM_all_roi_data_1) != 0:
                              for tjm_data in TJM_all_roi_data_1:
                                  print("tjm_datatjm_data", type(tjm_data), tjm_data["department"],  tjm_data.keys())
                                  print("jsonobject------------------------222222222222------------['roi_name]", len(TJM_all_roi_data))
                                  traffic_jam_true_status_roi_data.append({
                                      "timestamp": end_time.strftime('%Y-%m-%d %H:%M:%S'),
                                      "camera_name": tjm_data["camera_name"],
                                      "department": tjm_data["department"],
                                      "roi_name": roi_name,
                                      "status": "empty",
                                      "traffic_percentage": 0,
                                      "Preset_percentage": 0.0
                                  })

              current_date += timedelta(days=1)

          result = {
              "message": {
                  "traffic_true_message": traffic_jam_true_status_roi_data,
                  "traffic_false_message": traffic_jam_empty_status_roi_data
              },
              "success": True
          }

          formatted_data = {"message": [], "success": result["success"]}
          department_dict = {}

          for msg_type in ["traffic_false_message", "traffic_true_message"]:
              for item in result["message"][msg_type]:
                  department = item["department"]
                  camera_name = item["camera_name"]
                  roi_name = item["roi_name"]
                  status = item["status"]
                  timestamp = item["timestamp"]
                  Preset_percentage = item["Preset_percentage"]
                  traffic_percentage = item["traffic_percentage"]

                  if department not in department_dict:
                      department_dict[department] = {}
                  
                  if camera_name not in department_dict[department]:
                      department_dict[department][camera_name] = []

                  department_dict[department][camera_name].append({
                      "Preset_percentage": Preset_percentage,
                      "traffic_percentage": traffic_percentage,
                      "roi_name": roi_name,
                      "status": status,
                      "timestamp": timestamp
                  })

          for department, cameras in department_dict.items():
              rois = []
              for camera_name, roi_details in cameras.items():
                  rois.append({
                      "camera_name": camera_name,
                      "roi_details": roi_details
                  })
              formatted_data["message"].append({
                  "department": department,
                  "rois": rois
              })

          result = formatted_data

  # For demonstration, printing the formatted data
  # import json
  # print(json.dumps(formatted_data, indent=4))


    # else:
    #   result = {"message":"Data not found.", "success":False}

  return result




@traffic_jam_management.route('/trafficjamlivedata', methods=['GET'])
@traffic_jam_management.route('/trafficjamlivedata/cameraname/<camera_name>', methods=['GET'])
@traffic_jam_management.route('/trafficjamlivedata/department/<department_name>', methods=['GET'])
@traffic_jam_management.route('/trafficjamlivedata', methods=['POST'])
def trafficjamlivedata( camera_name=None,department_name =None):
    ret = {'success': False,'message':"something went wrong in trafficjamlivedata apis"}
    match_data = {'timestamp':{'$regex': '^' + str(date.today())}, }
    if request.method == 'POST':
        jsonobject = request.json
        if jsonobject == None:
            jsonobject = {}
        request_key_array = ['camera_name', 'department_name']
        jsonobjectarray = list(set(jsonobject))
        missing_key = set(request_key_array).difference(jsonobjectarray)
        if not missing_key:
            output = [k for k, v in jsonobject.items() if v == '']
            if output:
                ret['message'] = " ".join(["You have missed these parameters ", str(output), "to enter. please enter properly.'"])
            else:
                all_data = []
                camera_name = jsonobject['camera_name']
                department_name = jsonobject['department_name']
                dash_data = []
                if  (camera_name is not None and camera_name !='none' and  camera_name !='')  and (department_name is not None and department_name !='none' and    department_name !='') :
                    match_data['camera_name']= camera_name
                    match_data['department']= department_name
                    pipeline = [
                        {'$match': {
                            '$and': [
                                match_data,
                                {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
                            ]
                        }},
                        {'$sort': {'timestamp': -1}},
                        {
                            '$project': {
                                "_id": 0,  
                                'roi_name': 1,
                                'timestamp': 1,
                                'camera_name': 1,
                                'deviceid': 1,
                                'camera_ip': 1,
                                'department': 1,
                                'area': 1,
                                'datauploadstatus': 1,
                                'analytics_log': {'$slice': ['$analytics_log', -1]}  
                            }
                        },
                        {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000},
                        {
                            '$project': {
                                '_id': 0, 
                                'data': 1
                            }
                        }
                    ]                 
                elif (camera_name is not None and camera_name !='none' and  camera_name !='')  :
                    match_data['camera_name']= camera_name
                    pipeline =  [
                        {'$match': {
                            '$and': [
                                match_data,
                                {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
                            ]
                        }},
                        {'$sort': {'timestamp': -1}},
                        {
                            '$project': {
                                "_id": 0,  
                                'roi_name': 1,
                                'timestamp': 1,
                                'camera_name': 1,
                                'deviceid': 1,
                                'camera_ip': 1,
                                'department': 1,
                                'area': 1,
                                'datauploadstatus': 1,
                                'analytics_log': {'$slice': ['$analytics_log', -1]}  
                            }
                        },
                        {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000},
                        {
                            '$project': {
                                '_id': 0, 
                                'data': 1
                            }
                        }
                    ]                 
                elif (department_name is not None and department_name !='none' and    department_name !=''):
                    match_data['department']= department_name
                    pipeline =  [
                        {'$match': {
                            '$and': [
                                match_data,
                                {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
                            ]
                        }},
                        {'$sort': {'timestamp': -1}},
                        {
                            '$project': {
                                "_id": 0,  
                                'roi_name': 1,
                                'timestamp': 1,
                                'camera_name': 1,
                                'deviceid': 1,
                                'camera_ip': 1,
                                'department': 1,
                                'area': 1,
                                'datauploadstatus': 1,
                                'analytics_log': {'$slice': ['$analytics_log', -1]}  
                            }
                        },
                        {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000},
                        {
                            '$project': {
                                '_id': 0, 
                                'data': 1
                            }
                        }
                    ]                     
                else:
                    pipeline = [
                        {'$match': {
                            '$and': [
                                match_data,
                                {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
                            ]
                        }},
                        {'$sort': {'timestamp': -1}},
                        {
                            '$project': {
                                "_id": 0,  
                                'roi_name': 1,
                                'timestamp': 1,
                                'camera_name': 1,
                                'deviceid': 1,
                                'camera_ip': 1,
                                'department': 1,
                                'area': 1,
                                'datauploadstatus': 1,
                                'analytics_log': {'$slice': ['$analytics_log', -1]}  
                            }
                        },
                        {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000},
                        {
                            '$project': {
                                '_id': 0, 
                                'data': 1
                            }
                        }
                    ]   
                data=list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate(pipeline))
                if len(data) != 0:
                    all_data = RALIVECOUNT(len(data), parse_json(data))
                    ret = all_data
                else:
                    ret['message'] = 'data not found'
        else:
            ret = {'success': False, 'message':   " ".join(["You have missed these keys", str(missing_key), "to enter. please enter properly.'"])}
    elif request.method == 'GET':
        dash_data = []
        if camera_name is not None :
            match_data['camera_name'] =  camera_name
            pipeline =  [
                        {'$match': {
                            '$and': [
                                match_data,
                                {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
                            ]
                        }},
                        {'$sort': {'timestamp': -1}},
                        {
                            '$project': {
                                "_id": 0,  
                                'roi_name': 1,
                                'timestamp': 1,
                                'camera_name': 1,
                                'deviceid': 1,
                                'camera_ip': 1,
                                'department': 1,
                                'area': 1,
                                'datauploadstatus': 1,
                                'analytics_log': {'$slice': ['$analytics_log', -1]}  
                            }
                        },
                        {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000},
                        {
                            '$project': {
                                '_id': 0, 
                                'data': 1
                            }
                        }
                    ]
        else:
            # pipeline = [
            #                     {'$match': match_data},
            #                     # {'$sort': {'timestamp': -1, '_id': -1}},
            #                     {'$sort': {'timestamp': -1}},
            #                     {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
            #                     {'$sort': {'data.timestamp': -1}},
            #                     {'$limit': 4000000}
            #                 ]          
            

            pipeline =  [
                        {'$match': {
                            '$and': [
                                match_data,
                                {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
                            ]
                        }},
                        {'$sort': {'timestamp': -1}},
                        {
                            '$project': {
                                "_id": 0,  
                                'roi_name': 1,
                                'timestamp': 1,
                                'camera_name': 1,
                                'deviceid': 1,
                                'camera_ip': 1,
                                'department': 1,
                                'area': 1,
                                'datauploadstatus': 1,
                                'analytics_log': {'$slice': ['$analytics_log', -1]}  
                            }
                        },
                        {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
                        {'$sort': {'data.timestamp': -1}},
                        {'$limit': 4000000},
                        {
                            '$project': {
                                '_id': 0, 
                                'data': 1
                            }
                        }
                    ]
        data=list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate(pipeline))
        if len(data) != 0:
            ret['message']=parse_json(data)
            ret['success']=True
        else:
            ret['message'] = 'data not found'  
    return jsonify(ret)



@traffic_jam_management.route('/trafficjamDatewise', methods=['POST'])
@traffic_jam_management.route('/trafficjamDatewise/<cameraname>', methods=['POST'])
@traffic_jam_management.route('/trafficjamDatewise/<cameraname>/<pagenumber>/<page_limit>', methods=['POST'])
@traffic_jam_management.route('/trafficjamDatewise/<pagenumber>/<page_limit>', methods=['POST'])
def DATEWISERA(cameraname=None, pagenumber=None, page_limit=None):
    ret = {'success': False, 'message': 'Something went wrong.'}
    try:
        jsonobject = request.json or {}
        required_keys = {'from_date', 'to_date', 'department_name'}
        missing_keys = required_keys - jsonobject.keys()
        if missing_keys:
            return jsonify({'success': False, 'message': f"Missing keys: {', '.join(missing_keys)}"})
        empty_values = [key for key, value in jsonobject.items() if value == '']
        if empty_values:
            return jsonify({'success': False, 'message': f"Empty values for keys: {', '.join(empty_values)}"})
        from_date = jsonobject['from_date']
        to_date = jsonobject['to_date']
        department_name = jsonobject['department_name']
        match_data = {'timestamp': {'$gte': from_date, '$lte': to_date},}
        if department_name and department_name != 'none':
            match_data['department'] = department_name
        if cameraname and cameraname != 'none':
            match_data['camera_name'] = cameraname
        pipeline = [
    {'$match': {
        '$and': [
            match_data,
            {'$expr': {'$gt': [{'$size': '$analytics_log'}, 0]}} 
        ]
    }},
    {'$sort': {'timestamp': -1}},
    {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
    {'$sort': {'data.timestamp': -1}},
    {'$limit': 4000000},
    {
        '$project': {
            '_id': 0,  # Exclude `_id` in final output
            'data': 1
        }
    }
]
        # [
        #               {'$match': match_data},
        #               {'$sort': {'timestamp': -1}},
        #               {'$group': {'_id': {'roi_name': '$roi_name'}, 'data': {'$push': '$$ROOT'}}},
        #               {'$sort': {'data.timestamp': -1}},
        #               {'$limit': 4000000}
        #           ]    

        data = list(mongo.db.TRAFFICJAM_MANAGEMENT_DATA.aggregate(pipeline))

        if not data:
            return jsonify({'success': False, 'message': 'Data not found'})

        if len(data) !=0 : 
          ret = pagination_block(pagenumber, page_limit, parse_json(data))

    except (pymongo.errors.PyMongoError, Exception) as error:
        ret['message'] = str(error)

    return jsonify(ret)


@traffic_jam_management.route('/TJMimage/<image_file>', methods=['GET'])
@traffic_jam_management.route('/TJMimage/<roiname>/<image_file>', methods=['GET'])
def TJMIMage(roiname,image_file):
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
        # QueryMatch = {"roi_name":roiname,'analytics_log.image_name': image_file}
        # # print("-------------------QueryMatch--------------",QueryMatch)
        # image_data = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find_one(QueryMatch,sort=[('_id',  pymongo.DESCENDING)])

    QueryMatch = {"roi_name": roiname, "analytics_log.image_name": image_file}
    image_data = mongo.db.TRAFFICJAM_MANAGEMENT_DATA.find_one(
        QueryMatch,
        sort=[('_id', pymongo.DESCENDING)],
        projection={
            "roi_name": 1,
            "timestamp": 1,
            "camera_name": 1,
            "analytics_log": {"$elemMatch": {"image_name": image_file}}
        }
    )
    # print("--------------image_data-----",image_data)
    if image_data is not None:
        base_path = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame')
        CHECKIMAGE = os.path.join(get_current_dir_and_goto_parent_dir(),'images', 'frame',image_file)
        if file_exists(CHECKIMAGE):
            file_path = os.path.join(base_path, image_file)
            source_img = Image.open(file_path)
            draw = ImageDraw.Draw(source_img)
            IMage_widthscal = source_img.width
            IMage_heigthscal = source_img.height
            if len(image_data['analytics_log']) != 0:
                ROISHAPE = image_data['analytics_log'][0]                        
                if 'roi_bbox' in ROISHAPE:                        
                  if len(ROISHAPE['roi_bbox']) !=0 :
                    BBOXVALUE = ROISHAPE['roi_bbox']
                    polygon_bbox = [int(coord) for coord in BBOXVALUE.split(";") if coord.strip()]
                    bbox_values = scale_polygon(polygon_bbox, 960, 544, IMage_widthscal, IMage_heigthscal, increase_factor=1)
                    # print(f'bbox_values: {bbox_values}')
                    flattened_bbox_values = [coord for point in bbox_values for coord in point]
                    draw.polygon(flattened_bbox_values, outline=roiboxcolor, width=ROIbboxthickness)
                    coords = [(bbox_values[i][0], bbox_values[i][1]) for i in range(len(bbox_values))]
                    text_position = get_text_position_within_polygon(image_data['roi_name'], bbox_values, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', roifont_size, encoding='unic'))                                                    
                    text_width, text_height = calculate_text_size(image_data['roi_name'], roifont_size)
                    padding = 5
                    text_bg_position = (
                        text_position[0] - padding,
                        text_position[1] - padding,
                        text_position[0] + text_width + padding + (len(image_data['roi_name']) * 5),
                        text_position[1] + text_height + padding
                    )                                          
                    draw.rectangle(text_bg_position, fill='black')
                    keys_list = image_data['roi_name']#list(BoundingBoxValueFORROI.keys())
                    if keys_list is None and keys_list=='':
                        keys_list='Region of interest'
                    draw.text(text_position, str(keys_list), font=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',roifont_size, encoding='unic'), fill='white', stroke_width=2, stroke_fill="black")   
                                
                
                    
                imgByteArr = io.BytesIO()
                source_img.save(imgByteArr, format='JPEG')
                imgByteArr.seek(0)
                return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
            else:
                path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
                main_path = os.path.abspath(path)
                return send_from_directory(main_path, filename)

            
        else:
            path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
            main_path = os.path.abspath(path)
            return send_from_directory(main_path, filename)
    else:
        print("image_data not found-----2--------",image_file)
        path, filename = (os.path.join(os.getcwd(), "smaple_files"),'NOT_FOUND_IMAGE.png')
        main_path = os.path.abspath(path)
        return send_from_directory(main_path, filename)
    
            #return send_file(imgByteArr, mimetype='image/JPEG', as_attachment=True, download_name=image_file) 
            #return {'message': 'given image is not found', 'success': False}
    # except ( 
    #          pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
    #          pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
    #          pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
    #          pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
    #          pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
    #          pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
    #          pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
    #          pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
    #          pymongo.errors.WriteError) as error:
    #     print("print(,)", str(error))
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 1", str(error), " ----time ---- ", now_time_with_time()]))
    #     ret['message'] =" ".join(["something error has occered in api", str(error)])     
    #     if restart_mongodb_r_service():
    #         print("mongodb restarted")
    #     else:
    #         if forcerestart_mongodb_r_service():
    #             print("mongodb service force restarted-")
    #         else:
    #             print("mongodb service is not yet started.") 
    #     return {'message': str(error), 'success': False}
    # except Exception as  error :
    #     ERRORLOGdata(" ".join(["\n", "[ERROR] dashboard_apis -- image 2", str(error), " ----time ---- ", now_time_with_time()]))     
    
        # return {'message': str(error), 'success': False}