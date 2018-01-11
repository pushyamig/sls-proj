import boto3


# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/772263914719/dev-pushyami-sls-demo-messages'


def send_messages_to_queue(i):
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The SLS demo'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'Mr Serverless'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Message #  - '+str(i)
        )
    )
    print(response['MessageId'])


# Send message to SQS queue
for i in range(50):
    send_messages_to_queue(i)

