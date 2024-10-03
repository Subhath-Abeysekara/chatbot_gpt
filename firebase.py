import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("meetingdetecting-eaa8d5acd7c7.json")
firebase_admin.initialize_app(cred)
count = 0
def upload_image_to_firebase(image_file):
    global count
    bucket = storage.bucket('meetingdetecting.appspot.com')
    file_name = "eco_image_"+str(count)
    count+=1
    destination_blob_name = f'images_eco_print/{file_name}'
    blob = bucket.blob(destination_blob_name)
    with open(image_file, 'rb') as f:
        blob.upload_from_file(f,content_type='image/jpeg')
    return file_name

def get_sign_url_firebase(file_name):
    bucket = storage.bucket('meetingdetecting.appspot.com')
    destination_blob_name = f'images_eco_print/{file_name}'
    blob = bucket.blob(destination_blob_name)
    expiration_date = 604000  # Set the expiration time (e.g., 1 hour)
    signed_url = blob.generate_signed_url(version='v4',expiration=expiration_date)
    return signed_url

def download_from_firebase():
    # Get a reference to the Firebase Storage bucket
    bucket = storage.bucket('meetingdetecting.appspot.com')
    destination_blob_name = f'chatbot/generation_config.json'
    blob = bucket.blob(destination_blob_name)
    blob.download_to_filename("generation_config.json")
    return


def download_directory_from_firebase(directory_name):
    # Get a reference to the Firebase Storage bucket
    bucket = storage.bucket('meetingdetecting.appspot.com')

    # List all blobs in the specified directory
    blobs = bucket.list_blobs(prefix=directory_name)
    print(blobs)
    # Download each blob
    models_directory = "models"
    if not os.path.exists(models_directory):
        os.makedirs(models_directory)

    # Download each blob
    for blob in blobs:
        try:
            # Construct the local file path within the 'models' directory
            local_file_name = os.path.join(models_directory, blob.name.replace(directory_name, '', 1).strip('/'))

            # Create any necessary subdirectories
            if '/' in local_file_name:
                os.makedirs(os.path.dirname(local_file_name), exist_ok=True)

            # Download the file
            blob.download_to_filename(local_file_name)
            print(f'Downloaded {blob.name} to {local_file_name}')
        except Exception as e:
            print(f"Error downloading {blob.name}: {str(e)}")
    return f'All files from {directory_name} downloaded.'

# download_from_firebase()
# download_directory_from_firebase("chatbot/")