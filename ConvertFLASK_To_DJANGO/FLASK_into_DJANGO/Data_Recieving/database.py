# from flask_pymongo import PyMongo
# mongo = PyMongo()


from pymongo import MongoClient
from django.conf import settings

# Establish a connection to MongoDB
mongo = MongoClient(settings.MONGO_URI)

# Access the database
DATABASE = mongo[settings.MONGO_DB_NAME]


riro_data = DATABASE['riro_data']
job_sheet_details=DATABASE['job_sheet_details']
rtsp_flagcollection = DATABASE['rtsp_flag']
PPERAVIOLATIONCOLLECTION=DATABASE['data']
panel_data = DATABASE['panel_data']
mechesi = DATABASE['mechesi']
filterviolations = DATABASE['filterviolations']
flasherlogdata = DATABASE['flasherlogdata']
gpu_configurations = DATABASE['gpu_configurations']
linkagejobs = DATABASE['linkagejobs']
live_data_count = DATABASE['live_data_count']
mechjob_sheet = DATABASE['mechjob_sheet']
mockdrill = DATABASE['mockdrill']
ppera_cameras = DATABASE['ppera_cameras']
steamsuit_cameras= DATABASE['steamsuit_cameras']
trafficcountdata = DATABASE['trafficcountdata']
RAlive_data_count= DATABASE['RAlive_data_count']
PPElive_data_count= DATABASE['PPElive_data_count']
CRlive_data_count= DATABASE['CRlive_data_count']
live_data_countCollection = DATABASE['live_data_count']
riro_unplanned = DATABASE['riro_unplanned']
unplanedLivecount  = DATABASE['unplanedLivecount']
mechjob_sheet = DATABASE['mechjob_sheet']
mechesi = DATABASE['mechesi']
MEchHydracollection = DATABASE['hydra_data']


firesmokeviolationdata=DATABASE["firesmokeviolationdata"]
coin_id_violation_data=DATABASE["coin_id_violation_data"]
firesmokecamerastatus=DATABASE["firesmokecamerastatus"]
voice_announcement_status=DATABASE["voice_announcement_status"]
rtsp_flag=DATABASE["rtsp_flag"]
VEHICLE_PARKING_MANAGEMENT_DATA=DATABASE["VEHICLE_PARKING_MANAGEMENT_DATA"]
VPMS_DATA=DATABASE["VPMS_DATA"]