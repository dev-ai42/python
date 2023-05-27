import json
import re
import time
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
sns = boto3.client('sns')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
        text = response['Body'].read().decode()
        #print(text)
        count = len(re.findall(r'\w+', text))
        #print(count)
        
        topic_name = "s3_wordcount"
        topic_arn = ""
        is_created = False
        
        topics = sns.list_topics()['Topics']
        #print("Topics list:")
        #print(topics)
        #print("\n")
        for topic in topics:
            if topic_name in topic['TopicArn'].split(":")[5]:
                is_created = True
                topic_arn = topic['TopicArn']
        
        if not is_created:
            topic_resp = sns.create_topic(Name=topic_name)
            #print("Topic resp:")
            #print(topic_resp)
            #print("\n")
            topic_arn = topic_resp['TopicArn']
            sub_resp = sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint='lambda-test@maildrop.cc',
                ReturnSubscriptionArn=True
            )
            #print("Subscription resp:")
            #print(sub_resp)
            #print("\n")
            #sub_arn = sub_resp['SubscriptionArn']
            #sub_resp = sns.get_subscription_attributes(
            #    SubscriptionArn=sub_arn
            #)
            #print("Confirmation status:")
            #print(sub_resp)
            #print("\n")
            #has_confirmed = sub_resp['Attributes']['ConfirmationWasAuthenticated']
            #while has_confirmed == "false":
            #    time.sleep(10)
            #    has_confirmed = sns.get_subscription_attributes(
            #        SubscriptionArn=sub_arn
            #    )['Attributes']['ConfirmationWasAuthenticated']
            #    print(has_confirmed)
            
        message_str = "The word count in the file " + key + " is " + str(count) + "."
        publish_resp = sns.publish(
            TopicArn=topic_arn,
            Message=message_str,
            Subject='Word Count Result'
        )
        #print("Publish resp:")
        #print(publish_resp)
        #print("\n")
        return {
            'statusCode': 200,
            'body': json.dumps('Report sent.')
        }

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
