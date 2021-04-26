import json
import boto3
import os

#region = "ap-southeast-1"
region = os.getenv('REGION')
ec2 = boto3.client("ec2", region_name=region)

### stop ec2 instances
def stop(instance_ids):
    #ec2.stop_instances(InstanceIds=instance_ids)
    print ("stopped your instances: " + str(instance_ids))
    return "stopped:OK"

### start ec2 instances
def start(instance_ids):
    #ec2.start_instances(InstanceIds=instance_ids)
    print ("started your instances: " + str(instance_ids))
    return "started:OK"



def lambda_handler(event, context):
    
    print(event)
    #instances = ['i-07f7c4e73af277834']

    instance_ids = event.get('ids')
    action = event.get('action')
    if ('stop' == action):
        stop(instance_ids)
        
    elif (action == 'start'):
        print('start action')
        start(instance_ids)

    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }
    
### Event bridge  intellect team  stop at 12:30 local phnom penh time 
 ## runing at 8AM - Schedule expression: cron(30 5 ? * MON-FRI *)
 
# {   "action": "stop",     
#     "ids" : [ "i-0b321329cc8e8cc7f","i-0fb313cb290940e46"]
# }