import json
import os
import asyncio
import aiofiles
import boto3
import aioboto3
from botocore.exceptions import NoCredentialsError, ClientError
from decouple import config

bucket_name = config("BUCKET_NAME")


# set up the S3 client
async def upload_to_yandex_bucket_async(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_name
    # Configure the aioboto3 S3 client inside the async function
    async with aioboto3.session.Session().client(
        "s3",
        endpoint_url=config("S3_ENDPOINT_URL"),
        aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
        region_name=config("REGION_NAME"),
    ) as s3_client:
        try:
            await s3_client.upload_file(file_name, bucket_name, object_name)
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except ClientError as e:
            print(f"Client error during upload: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during upload: {e}")
            return False
        return True


# Get the directory of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the 'saved_history_files' directory exists
saved_files_dir = os.path.join(script_dir, "saved_history_files")
os.makedirs(saved_files_dir, exist_ok=True)


async def save_and_upload_rental_history(serialized_data, user_email):
    lines = [
        f"ID: {item['id']}, Bicycle: {item['bicycle']}, Start: {item['start_time']}, End: {item['end_time']}, Cost: {item['cost']}"
        for item in serialized_data
    ]
    rental_history_text = "\n".join(lines)

    # Asynchronously save the text content to a file
    text_file_name = os.path.join(saved_files_dir, f"rental_history_{user_email}.txt")
    async with aiofiles.open(text_file_name, "w") as file:
        await file.write(rental_history_text)

    # Asynchronously save the JSON content to a file
    json_file_name = os.path.join(saved_files_dir, f"rental_history_{user_email}.json")
    async with aiofiles.open(json_file_name, "w") as file:
        await file.write(json.dumps(serialized_data, indent=4))

    # Upload the text and JSON files to Yandex Object Storage asynchronously
    await upload_to_yandex_bucket_async(
        text_file_name,
        bucket_name,
        f"user_histories/{user_email}/rental_history_{user_email}.txt",
    )
    await upload_to_yandex_bucket_async(
        json_file_name,
        bucket_name,
        f"user_histories/{user_email}/rental_history_{user_email}.json",
    )
