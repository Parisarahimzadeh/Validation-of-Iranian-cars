
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import difflib


uri = "mongodb+srv://parisarahimzadeh35:1xpkplq5iiM9Wryo@cluster0.wun21.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["car_tracking"]  # Create or access a 'car_tracking' database

# # Main collection
main_collection = db["Main"]
records_collection = db["Records"]

# Manually defined car records to insert
# car_records = [
#     {"car_license": "12-الف-345-67", "car_color": "سفید", "color_model": "پراید", "owner_name": "علی"},
#     {"car_license": "34-ب-678-12", "car_color": "مشکی", "color_model": " هایما", "owner_name": "حسین"},
#     {"car_license": "56-ج-789-34", "car_color": "آبی", "color_model": "  سمند", "owner_name": "مریم"},
#     {"car_license": "78-د-890-45", "car_color": "قرمز", "color_model": "پارس", "owner_name": "سمیرا"},
#     {"car_license": "90-ه-123-67", "car_color": "نقره‌ای", "color_model": "407 ", "owner_name": "فاطمه"},
#     {"car_license": "11-و-234-78", "car_color": "سفید", "color_model": "  206", "owner_name": "علی"},
#     {"car_license": "22-ز-345-89", "car_color": "مشکی", "color_model": "207", "owner_name": "حسین"},
#     {"car_license": "33-ح-456-90", "car_color": "آبی", "color_model": " زانتیا", "owner_name": "مریم"},
#     {"car_license": "44-ط-567-01", "car_color": "قرمز", "color_model": "جک  ", "owner_name": "سمیرا"},
#     {"car_license": "55-ی-678-12", "car_color": "نقره‌ای", "color_model": "مزدا", "owner_name": "فاطمه"},
# ]

# # Insert records into the Main collection
# main_collection.insert_many(car_records)

# print("10 car records added successfully to the 'Main' collection.")


# Helper function to check if exactly one character or digit has changed
def one_change_away(license1, license2):
    if len(license1) != len(license2):
        return False
    differences = 0
    for ch1, ch2 in zip(license1, license2):
        if ch1 != ch2:
            differences += 1
        if differences > 1:
            return False
    return differences == 1

# Function to compare car license and insert into Records if one digit differs
def compare_and_insert_car_license(givenCarLicense, givenColor, givenModel, latitude, longitude):
    # Fetch all documents from the Main collection
    for mainDoc in main_collection.find():
        # Check if the color and model match exactly
        if mainDoc['car_color'] != givenColor or mainDoc['color_model'] != givenModel:
            print(f"Skipping document {mainDoc['_id']}: color or model do not match.")
            continue  # Skip this document if color or model do not match

        # Get the car license from the main document
        mainCarLicense = mainDoc['car_license']  # Assuming car_license is stored as a single string

        # Check if only one digit or character differs
        if one_change_away(mainCarLicense, givenCarLicense):
            # Insert into the Records collection
            records_collection.insert_one({
                "main_id": mainDoc['_id'],    # Reference to the _id in Main collection
                "latitude": latitude,         # Latitude where it was recognized
                "longitude": longitude,       # Longitude where it was recognized
                "timestamp": datetime.now()   # Current timestamp
            })
            print(f"Inserted record for main_id {mainDoc['_id']} into Records.")
        else:
            print(f"Not inserting for document {mainDoc['_id']}: more than one character differs.")

# Example usage with given car license
givenCarLicense = "11-الف-345-67"  # Example given car license with one digit change (22 instead of 12)
givenColor = "سفید"               # Example color (must match)
givenModel = "پراید"              # Example model (must match)
latitude = 35.6892               # Example latitude
longitude = 51.3890              # Example longitude

# Call the function
compare_and_insert_car_license(givenCarLicense, givenColor, givenModel, latitude, longitude)





# # Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)