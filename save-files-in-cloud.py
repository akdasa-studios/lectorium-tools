import glob
import boto3
import json
import os
import concurrent.futures
from botocore.exceptions import NoCredentialsError, ClientError

from modules.meta.id import extract_id


PATH_OUTPUT = "output"
BASE_URL    = ""

s3_client = boto3.client(
    's3',
    region_name='eu2',
    endpoint_url='https://eu2.contabostorage.com',
    aws_access_key_id='',
    aws_secret_access_key='')


def save_file_url(
    file_id: str,
    cloud_file_name: str,
):
    """
    Save the URL of the file in the output folder.
    """
    file_name = f"{PATH_OUTPUT}/{file_id}.meta.url.json"

    with open(file_name, 'w') as file:
        file.write(json.dumps({
            "url": f"{BASE_URL}{cloud_file_name}"
        }))


def check_file_exists(
    cloud_bucket_name: str,
    cloud_file_name: str,
) -> bool:
    """
    Check if the file exists in the S3 bucket. Return True if it exists, False otherwise.
    """
    try:
        s3_client.head_object(Bucket=cloud_bucket_name, Key=cloud_file_name)
        return True
    except ClientError as e:
        return False


def process_file(
    file_id: str,
    file_name: str,
    cloud_bucket_name: str,
    cloud_file_name: str = None
):
    """
    Process a file. Upload file to S3 bucket if it does not exist.
    Save the URL of the file in the output folder.
    """
    if check_file_exists(cloud_bucket_name, cloud_file_name):
        print(f"File {cloud_file_name} already exists in S3 bucket.")
        return False
    else:
        print(f"Processing {file_name}")

    save_file_url(file_id, cloud_file_name)
    s3_client.upload_file(file_name, cloud_bucket_name, cloud_file_name)


if __name__ == "__main__":
    # configs
    cloud_bucket_name = "library"
    cloud_file_name   = lambda path: extract_id(path) + os.path.splitext(path)[1]

    # get list of files to upload
    files_to_upload = [
        path for path in glob.glob("input/**/*", recursive=True)
        if os.path.isfile(path)
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(
                process_file,
                extract_id(file),
                file,
                cloud_bucket_name,
                cloud_file_name=cloud_file_name(file)
            ) for file in files_to_upload
        ]
