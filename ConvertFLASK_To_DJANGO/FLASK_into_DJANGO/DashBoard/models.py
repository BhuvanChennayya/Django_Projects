from django.db import models
from pymongo import MongoClient
from django.conf import settings

# Establish a connection to MongoDB
Mongo = MongoClient(settings.MONGO_URI)

# Access the database
db = Mongo[settings.MONGO_DB_NAME]