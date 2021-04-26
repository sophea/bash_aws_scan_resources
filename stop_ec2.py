from datetime import datetime

import json
import boto3
import os

today=datetime.today().strftime('%Y-%m-%d')

ec2 = boto3.client('ec2')

region = os.getenv('REGION')

ec2 = boto3.client('ec2',region_name=region)
ec2_resource = boto3.resource('ec2',region_name=region)

def lambda_handler(event, context):
    
    isHoliday = False

    print("today :" + today)
    print("event " + str(event))
    print("context " + str(context))
    
    days = event["days"]
    excludes = event["excludes"]
    if today in days :
        print ("found - it is public holiday : " + today)
        isHoliday = True

    if (not isHoliday):
        print ("It is not public holiday " + today)
        return {'body' : "nothing to process"}
    ## stop all running instances    
   
    instances = ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    running_instances = [instance.id  for instance in instances if instance.id not in excludes]
    for id in running_instances:
        ec2.stop_instances(InstanceIds=[id])
        print ("stop_instances : " + id)
    
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

##UAT
#{
#  "days": [
#    "2021-01-01",
#    "2021-01-07",
#    "2021-03-08",
#    "2021-04-14",
#    "2021-04-15",
#    "2021-04-16",
#    "2021-04-26",
#    "2021-04-30",
#    "2021-05-01",
#    "2021-05-14",
#    "2021-06-18",
#    "2021-09-24",
#    "2021-10-05",
#    "2021-10-06",
#    "2021-10-07",
#    "2021-10-15",
#    "2021-10-29",
#    "2021-11-09",
#    "2021-11-18", 
#    "2021-11-19",
#    "2021-11-20"
#  ],
#  "excludes": [
#    "i-034ce6eff6a80b19e",
#    "i-07cac7d6f38981ed5",
#    "i-08977b585d6ce1126",
#    "i-07584266f63b38afa",
#    "i-0b321329cc8e8cc7f",
#    "i-0fb313cb290940e46"
#  ]
#}


