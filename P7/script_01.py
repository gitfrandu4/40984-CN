import json
import boto3
from datetime import datetime
from typing import Dict, Any, List

def transform_ree_data(data: Dict[str, Any], max_batch_size: int = 450) -> List[str]:
   """
   Transform REE JSON data into batches of Firehose-compatible records
   with properly formatted datetime for partitioning.
   """
   current_batch = ""
   batches = []
   record_count = 0
   
   # Process each demand type in the included array
   for demand in data.get('included', []):
       title = demand.get('attributes', {}).get('title', '')
       
       # Process each value for this demand type
       for value_entry in demand.get('attributes', {}).get('values', []):
           # Parse the datetime string
           dt = datetime.fromisoformat(value_entry['datetime'])
           
           # Format datetime in a way that Firehose can process
           formatted_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
           
           # Create partition keys in the format Firehose expects
           partition_keys = {
               'year': dt.strftime('%Y'),
               'month': dt.strftime('%m'),
               'day': dt.strftime('%d')
           }
           
           # Create record with metadata for partitioning
           record = {
               'data': {
                   'datetime': formatted_datetime,
                   'title': title,
                   'value': float(value_entry['value']),
                   'percentage': float(value_entry['percentage']),
                   'year': dt.strftime('%Y'),
                   'month': dt.strftime('%m'),
                   'day': dt.strftime('%d')
               },
               'metadata': {
                   'partition_keys': partition_keys
               }
           }
           
           # Add record to current batch
           current_batch += json.dumps(record) + '\n'
           record_count += 1
           
           # If we reach batch size limit, start new batch
           if record_count >= max_batch_size:
               batches.append(current_batch)
               current_batch = ""
               record_count = 0
   
   # Add any remaining records as final batch
   if current_batch:
       batches.append(current_batch)
   
   return batches


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
   """
   Lambda handler to process SQS messages containing S3 events
   and forward data to Kinesis Firehose
   """
   # Initialize AWS clients
   s3_client = boto3.client('s3')
   firehose_client = boto3.client('firehose')
   stream_name = 'PUT-S3-p0qpG'
   
   try:
       print(f"Processing {event}")
       # Process each record from SQS
       for record in event['Records']:
           # Parse the SQS message body which contains the S3 event
           s3_event = json.loads(record['body'])
           
           # Extract S3 bucket and key from S3 event structure
           # This is the correct structure for S3 notifications
           bucket = s3_event['Records'][0]['s3']['bucket']['name']
           key = s3_event['Records'][0]['s3']['object']['key']
           
           print(f"Processing file {key} from bucket {bucket}")
           
           # Get the file content from S3
           try:
               response = s3_client.get_object(Bucket=bucket, Key=key)
               file_content = response['Body'].read().decode('utf-8')
               
               # Parse JSON content
               data = json.loads(file_content)
               batches = transform_ree_data(data)
               
               batches_n = len(batches)
               for batch_n, batch in enumerate(batches):
                   response = firehose_client.put_record(
                       DeliveryStreamName=stream_name,
                       Record={
                           'Data': batch
                       }
                   )
                   print(f"Processed batch {batch_n}/{batches_n} with response: {response}")
               
           except Exception as e:
               print(f"Error processing file {key}: {str(e)}")
               # Continue processing other records even if one fails
               continue
       
       return {
           'statusCode': 200,
           'body': json.dumps(f'Successfully processed {len(batches)} batches')
       }
       
   except Exception as e:
       print(f"Error processing event: {str(e)}")
       return {
           'statusCode': 500,
           'body': json.dumps(f'Error processing messages: {str(e)}')
       }
