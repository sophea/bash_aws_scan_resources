from datetime import datetime

import json
import boto3
import os

today=datetime.today().strftime('%Y-%m-%d')

ec2 = boto3.client('ec2')

region = os.getenv('REGION')

isHoliday = False

def lambda_handler(event, context):
    

    print("today :" + today)
    print("event " + str(event))
    print("context " + str(context))
    
    days = event["days"]

    if today in days :
        print ("found - it is public holiday : " + today)
        isHoliday = True

    if (not isHoliday):
        print ("It is not public holiday " + today)
        return {'body' : "nothing to process"}
    ## stop all running instances    
    ec2 = boto3.resource('ec2',region_name=region)
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    RunningInstances = [instance.id for instance in instances]
    for i in RunningInstances:
        #stoppingInstances = ec2.instances.stop(i)
        #print(stoppingInstances)
        print ("stop instances : " + i)
    
    return {
        'statusCode': 200,
        'body': json.dumps('success from Lambda!')
    }
    
    
 ### Event bridge
 ## runing at 9AM - Schedule expression: cron(* 2 ? * MON-FRI *)
 
# {   "days": 
#     [     "2021-04-14",
#     "2021-04-15", 
#     "2021-04-16", 
#      ] 
# }