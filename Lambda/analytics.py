import boto3
import re
import json
import matplotlib.pyplot as plt
from io import BytesIO

def parse_error_log(log_content):
    client_dict = {}
    total_requests = 0

    # Extract clients from error.log
    matches = re.findall(r"client: (\d+\.\d+\.\d+\.\d+)", log_content)
    for match in matches:
        total_requests += 1
        if match in client_dict:
            client_dict[match] += 1
        else:
            client_dict[match] = 1

    return client_dict, total_requests

def parse_access_log(log_content):
    total_get_requests = 0
    total_post_requests = 0

    # Extract requests from access.log
    matches = re.findall(r'\"(\w+) /', log_content)
    for match in matches:
        if match == "GET":
            total_get_requests += 1
        elif match == "POST":
            total_post_requests += 1

    return total_get_requests, total_post_requests

def plot_requests(total_get_requests, total_post_requests):
    labels = ['GET Requests', 'POST Requests']
    values = [total_get_requests, total_post_requests]

    plt.bar(labels, values, color=['blue', 'green'])
    plt.xlabel('Request Type')
    plt.ylabel('Number of Requests')
    plt.title('Number of GET and POST Requests')

    # Save the plot as bytes
    plot_bytes = BytesIO()
    plt.savefig(plot_bytes, format='png')
    plot_bytes.seek(0)
    
    return plot_bytes

def upload_to_s3(bucket_name, key, data):
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=data, Bucket=bucket_name, Key=key)

def save_analytics_to_json(bucket_name, analytics_key, analytics_data):
    s3_client = boto3.client('s3')
    json_data = json.dumps(analytics_data)
    s3_client.put_object(Body=json_data, Bucket=bucket_name, Key=analytics_key)

def lambda_handler(event, context):
    # Specify your S3 bucket and file names
    bucket_name = 'mern-1999'
    access_log_key = 'access.log'
    error_log_key = 'error.log'
    plot_key = 'request_plot.png'
    analytics_key = 'quick_analytics.json'

    # Initialize S3 client
    s3_client = boto3.client('s3')

    try:
        # Download Access Log
        access_log_obj = s3_client.get_object(Bucket=bucket_name, Key=access_log_key)
        access_log_content = access_log_obj['Body'].read().decode('utf-8')

        # Download Error Log
        error_log_obj = s3_client.get_object(Bucket=bucket_name, Key=error_log_key)
        error_log_content = error_log_obj['Body'].read().decode('utf-8')

        # Parse logs
        client_dict, total_requests = parse_error_log(error_log_content)
        print("Client Dictionary:", client_dict)

        total_get_requests, total_post_requests = parse_access_log(access_log_content)
        print("Total GET Requests:", total_get_requests)
        print("Total POST Requests:", total_post_requests)

        # Plot requests
        plot_bytes = plot_requests(total_get_requests, total_post_requests)

        # Upload plot to S3
        upload_to_s3(bucket_name, plot_key, plot_bytes)

        # Save analytics to JSON
        analytics_data = {
            'client_dict': client_dict,
            'total_requests': total_requests,
            'total_get_requests': total_get_requests,
            'total_post_requests': total_post_requests
        }
        save_analytics_to_json(bucket_name, analytics_key, analytics_data)

        return {
            'statusCode': 200,
            'body': 'Logs read successfully. Analytics generated and uploaded to S3.'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error processing logs.'
        }
