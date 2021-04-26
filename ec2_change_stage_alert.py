import json
import logging
import os
import boto3
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV=os.environ["ENV"]

##default webhook :
HOOK_URL = os.environ["HOOK_URL"]
HOOK_URL_FINET= os.environ["FINET_HOOK_URL"]
HOOK_URL_INTELLECT= os.environ["INTELLECT_HOOK_URL"]
HOOK_URL_POWERCARD= os.environ["POWERCARD_HOOK_URL"]
HOOK_URL_POWERCARD= os.environ["APIHUB_HOOK_URL"]

webhook_map = {'finet':HOOK_URL_FINET,
                'intellect':HOOK_URL_INTELLECT,
                'powercard':HOOK_URL_POWERCARD,
                'apihub':HOOK_URL_APIHUB
              }

defaultRegion="ap-southeast-1"
##set ec2 instance resources
ec2 = boto3.client('ec2',region_name=defaultRegion)

#json payload Event: 
#{"instance-id": "i-0e2b5d55bdec74f21", 
#"state": "stopping", 
#"time": "2021-04-13T08:42:33Z", 
#"region": "ap-southeast-1", 
#"account": "674352424895",
# "message": "At 2021-04-13T08:42:33Z, the status of your EC2 instance i-093f3ea672017bc9d on account 674352424895 in the AWS Region ap-southeast-1 has changed to stopping."
# }


def lambda_handler(event, context):
    global ec2 
    logger.info("Event: " + str(event))
    instanceId = event["instance-id"]
    state = event["state"]
    region = event["region"]
    account= event["account"]
    message = event["message"]
    ## region not same as defaultRegion
    if defaultRegion != region:
        
        ec2 = boto3.client('ec2',region_name=region)
        
    instances = get_instance_details(ec2, instanceId)
    instanceName="NA"
    webhook_url=""
    for i in instances:
        instanceName = get_name(i)
        applicationName= get_application_name(i)
        logger.info("instance name :" + instanceName + " , application : " + applicationName)
        webhook_url=get_webhook_url(applicationName)
    
    message = message.replace(instanceId, "name " + instanceName + " [" + instanceId + "] ")
    logger.info("message" + message)
 
    ##check webhook_url is not found from the map
    if webhook_url is None:
        webhook_url=HOOK_URL
    
    ##populate team message
    messages = {
    "@context": "https://schema.org/extensions",
    "@type": "MessageCard",
    "themeColor": "64a837",
    "title": "[" + ENV +"] server " + instanceName + " has changed state to " + state,
    "text": message
    }
    logger.info(webhook_url)

    req = Request(webhook_url, json.dumps(messages).encode("utf-8"))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to team")
        return { "status": "200 OK"}
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

    # EventBridge	
    #Input Transfomer
    #{"instance-id":"$.detail.instance-id","state":"$.detail.state","time":"$.time","region":"$.region","account":"$.account"}
    #
    #{"instance-id":"<instance-id>","state":"<state>","time":"<time>","region":"<region>","account":"<account>",
    #"message":
    #"At <time>, the status of your EC2 instance <instance-id> on account <account> in the AWS Region <region> has changed to <state>."
    #}
    
def get_webhook_url(application):
    return webhook_map.get(application)
    
def get_application_name(instance):
    for t in instance["Tags"]:
        if t["Key"] == "application":
            return t["Value"]
    return instance["InstanceId"]
    
def get_name(instance):
    for t in instance["Tags"]:
        if t["Key"] == "Name":
            return t["Value"]
    return instance["InstanceId"]

def get_instance_details(client, instanceId):
    instances = []
    data = client.describe_instances(InstanceIds=[instanceId])
    for res in data["Reservations"]:
        instances.extend(res["Instances"])

    return instances
    
 
