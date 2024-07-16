import time
import looker_sdk
from looker_sdk import models40
import base64

# Initialize Looker SDK
sdk = looker_sdk.init40("looker.ini")
sdk.delete_dashboard('1864')
# sdk.delete_dashboard('1862')