import json
import logging
import os
import boto3
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HOOK_URL = os.environ["HookUrl"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)



#Event: 
#{"instance-id": "i-093f3ea672017bc9d", 
#"state": "stopping", 
#"time": "2021-04-13T08:42:33Z", 
#"region": "ap-southeast-1", 
#"account": "674352424895",
# "message": "At 2021-04-13T08:42:33Z, the status of your EC2 instance i-093f3ea672017bc9d on account 674352424895 in the AWS Region ap-southeast-1 has changed to stopping."
# }
 

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
    
 
def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    instanceId = event["instance-id"]
    state = event["state"]
    region = event["region"]
    account= event["account"]
    message = event["message"]
    
    
    ec2 = boto3.client('ec2',region_name=region)
    ##instances with tag and running state
    #instances = ec2.instances.filter(InstanceIds=[instanceId])
    instances = get_instance_details(ec2, instanceId)
    instanceName="NA"
    for i in instances:
        instanceName = get_name(i)
        logger.info("instance name :" + instanceName)
    
    message = message.replace(instanceId, "name " + instanceName + " [" + instanceId + "] ")
    logger.info("message" + message)
 
    
    messages = {
    "@context": "https://schema.org/extensions",
    "@type": "MessageCard",
    "themeColor": "64a837",
    "title": "[SIT] server " + instanceName + " has changed state to " + state,
    "text": message
    }
    

    req = Request(HOOK_URL, json.dumps(messages).encode("utf-8"))
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
