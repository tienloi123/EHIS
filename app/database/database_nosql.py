from pymongo import MongoClient

from app.constant import DATABASE_NAME
from app.core import settings

# Create a new client and connect to the server
client = MongoClient(settings.MONGODB_URI)
db = client[DATABASE_NAME]

