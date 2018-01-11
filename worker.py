import boto3
import timeit
import sys
import os


# getting messages from the SQS Queue
def get_sqs_msgs(queue_url, sqs):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        AttributeNames=[
            'All'
        ],
        VisibilityTimeout=60,
        WaitTimeSeconds=10
    )
    return response

# Process Message : simply printing the message here, ideally you would store it to a DB/S3
def get_message(messages,sqs, queue_url):
    event_data = []
    if messages:
        # for msg in messages:
        for i in range(len(messages)):
            i_ = messages[i]
            receipt_handle = i_['ReceiptHandle']
            each_message=i_['Body']
            event_data.append(each_message)
            delete_msg(receipt_handle, sqs, queue_url)
        print('Total message for this Invoke/fetch '+str(len(event_data)))
        print(*event_data)

# delete the message once sent to storage
def delete_msg(receipt_handle, sqs, queue_url):
    deleted_response = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    print('Message Deleted ',deleted_response['ResponseMetadata']['RequestId'])

# forming the Queue URL
def get_Queue_url(context):
    queue_name = os.environ['sqs']
    region = os.environ['region']
    print("lambda arn: " + context.invoked_function_arn)
    account_id = context.invoked_function_arn.split(":")[4]
    print("Account ID=" + account_id)
    queue_url = 'https://sqs.' + region + '.amazonaws.com/' + account_id + '/' + queue_name
    print('Queue_url ' + queue_url)
    return queue_url

# start of lambda function
def handler(event, context):
    print("This Starting of the function ")
    sqs = boto3.client('sqs')
    queue_url = get_Queue_url(context)
    response=get_sqs_msgs(queue_url,sqs)
    response_code = response['ResponseMetadata']['HTTPStatusCode']
    print('http_code '+str(response_code))
    messages = response['Messages']
    # print('number of msgs '+str(len(messages)))
    get_message(messages,sqs, queue_url)
    print('End of the Function')


