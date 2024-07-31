from mongo_utils import *

client = connect_to_mongo()

print("Connected to MongoDB")

insert_data(client)

print("Data inserted")

insert_vs(client)

print("VS inserted")