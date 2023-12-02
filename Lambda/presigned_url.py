import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

def lambda_handler(event, context):
    bucket_name = event["bucket-name"]
    object_key = event["object-key"]
    
    # Expiration time to the link
    expiration_time = datetime.utcnow() + timedelta(minutes=3)
    
    # Presigned URL
    presigned_url = generate_presigned_url(bucket_name, object_key, expiration_time)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'presigned_url': presigned_url})
    }
    
# Fxn presigned URL
def generate_presigned_url(bucket_name, object_key, expiration_time):

    try:
        # Generate the presigned URL
        presigned_url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key
            },
            ExpiresIn=30
        )
        
        return presigned_url

    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None