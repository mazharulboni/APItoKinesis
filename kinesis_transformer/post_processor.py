import boto3
import logging
import time

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        # Get the bucket name and the object key from the event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        source_key = event['Records'][0]['s3']['object']['key']

        # Define the destination key using the current epoch time
        current_epoch_time = int(time.time())
        dest_key = f"changedata/CDC{current_epoch_time}.csv"
        logging.info("Destination Key: {}".format(dest_key))

        # Define the destination bucket
        dest_bucket = "kinesis-dms-source-bucket"

        # Copy the S3 object with the new name
        s3.copy_object(Bucket=dest_bucket, CopySource={'Bucket': source_bucket, 'Key': source_key}, Key=dest_key)

        # Optionally, delete the original object (uncomment the following line if required)
        # s3.delete_object(Bucket=bucket, Key=key)

        logger.info(f"Copied object from {source_key} to {dest_key} to bucket {dest_bucket}")
        return {
            'statusCode': 200,
            'body': f"Successfully copied {source_key} to {dest_key} to bucket {dest_bucket}"
        }
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f"Failed to copy object. Error: {e}"
        }