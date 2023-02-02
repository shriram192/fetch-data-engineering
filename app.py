
import boto3
import os
import json
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
from utils import mask_ip, mask_device_id

load_dotenv()

def main():

    #Create SQS Client
    sqs = boto3.client(
        "sqs", endpoint_url=os.getenv('ENDPOINT_URL'),
        region_name=os.getenv('REGION_NAME'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
        )
    
    #Retrieve Message from SQS Queue
    messages = sqs.receive_message(QueueUrl=os.getenv('QUEUE_URL'))
    
    #Modify data for masking
    data_list = []
    for row in messages['Messages']:
        body = json.loads(row['Body'])

        user_id = body['user_id']
        device_type = body['device_type']

        masked_ip = mask_ip(body['ip'])

        masked_device_id = mask_device_id(body['device_id'])
                
        local = body['locale']
        app_version = body['app_version'].split('.')
        app_version = ''.join(app_version)
        create_date = datetime.now()

        data_list.append((user_id,device_type,masked_ip,masked_device_id,local,app_version,create_date))

    #Store data to Postgres Database
    try:
        connection = psycopg2.connect(user=os.getenv('POSTGRES_USER_NAME'),
                                    password=os.getenv('POSTGRES_PASSWORD'),
                                    host=os.getenv('POSTGRES_HOST'),
                                    port=os.getenv('POSTGRES_PORT'),
                                    database=os.getenv('POSTGRES_DATABASE'))
        cursor = connection.cursor()

        for record in data_list:
            postgres_insert_query = """ INSERT INTO user_logins VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(postgres_insert_query, record)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    main()