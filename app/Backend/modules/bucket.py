from google.cloud import storage
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import *  # Assuming this imports google_credentials and vertex_project_id

# Global variable for storage client
storage_client = None
check_bucket_existing = False

def authenticate_with_credentials(credentials_json, project_id):
    """Authenticates using the provided credentials JSON string."""
    global storage_client
    temp_dir = tempfile.gettempdir()
    credentials_path = os.path.join(temp_dir, 'temp_credentials.json')
    with open(credentials_path, 'w+') as temp_file:
        temp_file.write(credentials_json)
        temp_file.flush()
    
    storage_client = storage.Client.from_service_account_json(credentials_path, project=project_id)

# Authenticate once globally
authenticate_with_credentials(google_credentials, vertex_project_id)

def list_buckets():
    """Lists all buckets in the Google Cloud project."""
    print("Buckets:")
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        print(bucket.name)

def list_blobs(bucket_name):    
    """Lists all blobs (files and folders) in a specified bucket."""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    return {blob.name for blob in blobs}  # Return a set of blob names

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file without progress tracking
    with open(source_file_name, "rb") as file_obj:
        blob.upload_from_file(file_obj)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"

def upload_file_with_progress(args):
    """Wrapper function for uploading files with arguments unpacking."""
    return upload_blob(*args)

def upload_files_from_directory(bucket_name, directory):
    """Uploads all new files from a specified directory to the bucket in parallel, creating necessary folders."""
    if check_bucket_existing:
        existing_blobs = list_blobs(bucket_name)  # Get existing blobs in the bucket
    else :
        existing_blobs = set()

    uploaded_files = []
    skipped_files = []
    upload_args = []

    for root, _, files in os.walk(directory):
        for file in files:
            source_file_name = os.path.join(root, file)
            destination_blob_name = os.path.relpath(source_file_name, directory).replace("\\", "/")  # Ensure consistent path format

            # Create the folder structure in the bucket
            folder_path = os.path.dirname(destination_blob_name)
            if folder_path and folder_path not in existing_blobs:
                # Create an empty blob to represent the folder
                storage_client.bucket(bucket_name).blob(folder_path + "/").upload_from_string('')

            # Check if the file already exists in the bucket
            if destination_blob_name not in existing_blobs:
                upload_args.append((bucket_name, source_file_name, destination_blob_name))
            else:
                print(f"File {destination_blob_name} already exists in the bucket. Skipping upload.")
                skipped_files.append(destination_blob_name)

    # Upload files in parallel with improved threading
    max_workers = 8  # You can adjust this number based on your needs and environment
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(upload_file_with_progress, args): args for args in upload_args}
        
        for future in as_completed(future_to_file):
            try:
                result = future.result()
                uploaded_files.append(result)
            except Exception as e:
                print(f"Error uploading file: {e}")

    return uploaded_files, skipped_files

def list_all_data(bucket_name):
    """Lists all data (files and folders) in the specified Google Cloud Storage bucket."""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    
    # Create a set to keep track of unique folder paths
    folder_structure = set()
    
    print(f"Listing all data in bucket: {bucket_name}\n")
    
    # Iterate over each blob to determine its folder structure
    for blob in blobs:
        # Extract folder structure from the blob name
        folder_path = os.path.dirname(blob.name)  # Get the folder path from the blob name
        folder_structure.add(folder_path)  # Add the folder to the set

        # Print the full path of the blob
        print(blob.name)

    print("\nFolder structure:")
    for folder in folder_structure:
        print(folder)

def upload_individual_files(bucket_name, file_paths):
    """Uploads individual files to the bucket in parallel, creating the necessary folder structure."""
    if check_bucket_existing:
        existing_blobs = list_blobs(bucket_name)  # Get existing blobs in the bucket
    else :
        existing_blobs = set()

    uploaded_files = []
    skipped_files = []
    upload_args = []

    for source_file_name in file_paths:
        if os.path.isfile(source_file_name):
            # Get the relative path from the base directory (./bucket)
            base_directory = './bucket/'
            relative_path = os.path.relpath(source_file_name, base_directory)

            # Destination blob name should include the folder structure
            destination_blob_name = relative_path.replace("\\", "/")  # Normalize path for GCS
            
            if destination_blob_name not in existing_blobs:
                upload_args.append((bucket_name, source_file_name, destination_blob_name))
            else:
                print(f"File {destination_blob_name} already exists in the bucket. Skipping upload.")
                skipped_files.append(destination_blob_name)
        else:
            print(f"File {source_file_name} does not exist. Skipping upload.")
            skipped_files.append(source_file_name)

    # Upload files in parallel with improved threading
    max_workers = 8  # You can adjust this number based on your needs and environment
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(upload_file_with_progress, args): args for args in upload_args}
        
        for future in as_completed(future_to_file):
            try:
                result = future.result()
                uploaded_files.append(result)
            except Exception as e:
                print(f"Error uploading file: {e}")
   
    return uploaded_files, skipped_files

def direct_upload_individual_file(bucket_name, file_path, file_data):
    """
    Uploads a single file to the Google Cloud Storage bucket, handling the necessary folder structure.
    
    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket.
        file_path (str): The relative path where the file should be uploaded in the bucket.
        file_data (werkzeug.datastructures.FileStorage): The file data object from form input.
        
    Returns:
        str: The public URL of the uploaded file or an error message if the file already exists.
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        
        # Normalize file path to ensure correct format (replace backslashes with forward slashes)
        destination_blob_name = file_path.replace("\\", "/")
        
        # Get existing blobs in the bucket to check for duplicates
        if check_bucket_existing:
            existing_blobs = list_blobs(bucket_name)  # Get existing blobs in the bucket
        else :
            existing_blobs = set()
        
        # Check if the file already exists in the bucket
        if destination_blob_name in existing_blobs:
            return f"File {destination_blob_name} already exists in the bucket. Skipping upload."
        
        # Upload the file data from the form directly
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file_data, content_type=file_data.content_type)
        
        # Optionally, make the file publicly accessible
        blob.make_public()
        
        # Return the public URL of the uploaded file
        url=get_signed_url_for_file(bucket_name, destination_blob_name)
        return url

    except Exception as e:
        return str(e)



def delete_file_or_folder(bucket_name, path):
    """Deletes a file or a folder in the specified bucket. If a folder is specified, all its contents will be deleted."""
    bucket = storage_client.bucket(bucket_name)

    # Check if the path is a folder or a file
    if path.endswith('/'):
        # It's a folder; delete all blobs within this folder
        blobs = bucket.list_blobs(prefix=path)
        blob_names = [blob.name for blob in blobs]
        
        if blob_names:
            bucket.delete_blobs(blob_names)  # Delete all blobs in the folder
            print(f"Deleted contents of folder: {path}")
        else:
            print(f"No contents found in the folder: {path}")

        # Optionally delete the folder itself by adding an empty blob with the same prefix
        folder_blob = bucket.blob(path)
        folder_blob.upload_from_string('')  # Create an empty blob to represent the folder
        folder_blob.delete()  # Now delete the empty blob to effectively remove the folder
        print(f"Deleted folder: {path}")
        
    else:
        # It's a file; delete the specific blob
        blob = bucket.blob(path)
        if blob.exists():
            blob.delete()
            print(f"Deleted file: {path}")
        else:
            print(f"File not found: {path}")


from google.cloud import storage
import os

from google.cloud import storage
from datetime import timedelta

def get_signed_url_for_file(bucket_name, blob_name, expiration_minutes=60):
    """
    Generates a signed URL for a file in the specified Google Cloud Storage bucket, valid for a limited time.
    
    Args:
        bucket_name (str): The name of the bucket.
        blob_name (str): The name of the blob (file) in the bucket.
        expiration_minutes (int): The number of minutes the signed URL should be valid for (default is 60 minutes).
    
    Returns:
        str: The signed URL for the file.
    """
    # Initialize storage client
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Check if the blob exists
    if not blob.exists():
        raise FileNotFoundError(f"The file '{blob_name}' does not exist in the bucket '{bucket_name}'")
    
    # Generate a signed URL valid for the specified duration
    signed_url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes))

    print(f"Generated signed URL for file '{blob_name}': {signed_url}")
    
    return signed_url

from google.cloud import storage
import json
import os
import datetime
from google.cloud import storage
import json
import os
import datetime
from io import StringIO
from google.cloud import storage
import json
import datetime
from io import StringIO

def create_jsonl_gcs(bucket_name, chats_folder="/chats/", ticket_folder="/tickets/"):
    """
    Create a JSONL file in GCS with all the JSON files from the chats_folder and ticket_folder in the bucket.
    
    Args:
        bucket_name (str): The name of the GCS bucket.
        chats_folder (str): Path to the chats folder in the GCS bucket.
        ticket_folder (str): Path to the ticket folder in the GCS bucket.
    
    Returns:
        str: The signed URL for the uploaded JSONL file.
    """
    # Initialize Google Cloud Storage client
    bucket = storage_client.bucket(bucket_name)
    
    json_files = []

    # Function to get all JSON files from a GCS folder and its subdirectories
    def get_json_files_from_gcs_folder(folder_name):
        blobs = bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            print(f"Found blob: {blob.name}")  # Print all blobs found
            if blob.name.endswith(".json"):
                # Extract the file path and directory name
                dir_name = os.path.basename(os.path.dirname(blob.name))
                json_files.append((blob, dir_name))
                print(f"Found JSON file: {blob.name} in directory: {dir_name}")

    # Get JSON files from chats folder and ticket folder in GCS
    get_json_files_from_gcs_folder(chats_folder)
    get_json_files_from_gcs_folder(ticket_folder)

    # Check if any JSON files were found
    if not json_files:
        print("No JSON files found in the specified folders.")
        return None

    # Create a unique name for the output JSONL file
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    jsonl_filename = f"nullbyte_{current_date}.jsonl"
    jsonl_blob = bucket.blob(jsonl_filename)

    # Write JSON objects to JSONL file in GCS
    try:
        # Create an in-memory file to write data
        jsonl_data = StringIO()

        for blob, dir_name in json_files:
            try:
                # Download and parse the JSON file content
                json_content = json.loads(blob.download_as_text())
                wrapped_data = {dir_name: json_content}
                # Write the wrapped JSON object as a line in the JSONL file
                jsonl_data.write(json.dumps(wrapped_data) + "\n")
                print(f"Processed file: {blob.name}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error in file {blob.name}: {e}")
            except Exception as e:
                print(f"Skipping problematic file {blob.name}: {e}")

        # Ensure that we have data to upload
        if jsonl_data.getvalue():
            # Upload the generated JSONL content to GCS
            jsonl_blob.upload_from_string(jsonl_data.getvalue(), content_type='application/jsonl')
            print(f"Uploaded JSONL file: {jsonl_filename}")

            # Generate a signed URL for the JSONL file, valid for 1 hour
            url = jsonl_blob.generate_signed_url(expiration=datetime.timedelta(hours=1))

            # Return the signed URL of the uploaded JSONL file
            return url
        else:
            print("No data to upload to JSONL file.")
            return None

    except Exception as e:
        print(f"Error creating JSONL file: {e}")
        return None

