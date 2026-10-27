## Imports
import requests
import tempfile
import boto3
from botocore.exceptions import ClientError

# Generate the source URL for the NYC taxi data based on year and month.
def build_source_url(year: int, month: int) -> str:
    """
    Generate the source URL for the NYC taxi data based on year and month.
    
    :param year: The year.
    :param month: The month.
    :return: The source URL.
    """
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    file_name = f"yellow_tripdata_{year:04d}-{month:02d}.parquet"
    return f"{base_url}/{file_name}"

# Generate the S3 key for storing the NYC taxi data based on year and month.
def build_s3_key(year: int, month: int) -> str:
    """
    Generate the S3 key for storing the NYC taxi data based on year and month.
    
    :param year: The year.
    :param month: The month.
    :return: The S3 key.
    """
    return f"taxi/yellow/year={year:04d}/month={month:02d}/yellow_tripdata_{year:04d}-{month:02d}.parquet"

# Check if a file exists in an S3 bucket. In this case, we are checking for the s3_key in the specified bucket_name using the provided s3_client. If the file exists, it returns True; if it does not exist (404 error), it returns False. For any other errors, it raises the exception.
def file_exists_in_s3(s3_client, bucket_name: str, s3_key: str) -> bool:
    """
    Check if a file exists in an S3 bucket.
    
    :param s3_client: The S3 client.
    :param bucket_name: The name of the S3 bucket.
    :param s3_key: The key of the file in the S3 bucket.
    :return: True if the file exists, False otherwise.
    """
    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_key)
        return True
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def download_file(url: str) -> None:
    """
    Download a file from a URL and save it to a temp path.
    
    :param url: The URL of the file to download.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            print(f"Temporary file created as : {temp_file.name}")
            with requests.get(url, stream=True) as response:
                response.raise_for_status()  # Raise an error for bad responses
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
            temp_file.seek(0)
            print("Download complete and temporary file is ready for use.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
        raise

def upload_file_to_s3(file_path: str, bucket: str, key: str):
    """
    Upload a file to s3 client

    :param file_path: The location of the file to be uploaded
    :param bucket: Bucket the file is being uploaded to in s3
    :param key: Name of the object in s3
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, key)
        print("Upload successful!")
    except ClientError as e:
        print(e)
        return False
    return True