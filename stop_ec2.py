from datetime import datetime

import json
import boto3
import os

today=datetime.today().strftime('%Y-%m-%d')

region = os.getenv('REGION')
ec2 = boto3.resource('ec2',region_name=region)

def lambda_handler(event, context):
    
    isHoliday = False

    print("today :" + today)
    print("event " + str(event))
   # print("context " + str(context))
    
    days = event["days"]
    excludes = event["excludes"]
    if today in days :
        print ("found - it is public holiday : " + today)
        isHoliday = True

    if (not isHoliday):
        print ("It is not public holiday " + today)
        return {'body' : "nothing to process"}
    ## stop all running instances    
   
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    RunningInstances = [instance.id for instance in instances]
    for i in RunningInstances:
        if (not i in excludes) :
            #stoppingInstances = ec2.instances.stop(i)
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
#      ],
#     "excludes" : [ "i-0d62303a89e7839fe","i-0af520a0246b8a3e2"]
# }