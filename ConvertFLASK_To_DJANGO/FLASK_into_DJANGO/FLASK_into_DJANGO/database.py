# from flask_pymongo import PyMongo
# mongo = PyMongo()


from pymongo import MongoClient
from django.conf import settings

# Establish a connection to MongoDB
mongo = MongoClient(settings.MONGO_URI)

# Access the database
db = mongo[settings.MONGO_DB_NAME]

# def get_or_create_collection(collection_name):
#     """
#     Get the specified collection if it exists. 
#     If it doesn't exist, create it and return the collection object.
#     """
#     # Establish connection to MongoDB
#     client = MongoClient(settings.MONGO_URI)
#     db = client[settings.MONGO_DB_NAME]

#     # Check if the collection exists
#     if collection_name in db.list_collection_names():
#         # Collection exists; return it
#         return db[collection_name]
#     else:
#         db.create_collection(collection_name)
#         # print(f"Collection '{collection_name}' created successfully!")
       
#         # Return the collection object
    
#         return db[collection_name]