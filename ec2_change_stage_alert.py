import json
import logging
import os
import boto3
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

##https://jtrustroyal.webhook.office.com/webhookb2/ec620713-0231-4c92-9ce2-24f0ba071804@36fae7a7-647f-49c3-8de3-e0e14ea818ed/IncomingWebhook/a5884126f9b84c92b664d7f4302d5ce0/e0ffbf10-57d5-47bb-bdc4-c416b8bff3d0
HOOK_URL_FINET= os.environ["FINET_HOOK_URL"]
##https://jtrustroyal.webhook.office.com/webhookb2/371de8de-a59c-411b-ad7a-7ce9fa3e928f@36fae7a7-647f-49c3-8de3-e0e14ea818ed/IncomingWebhook/6f4b51cc4d2e4baaaaf9dd6010cc2ab1/e0ffbf10-57d5-47bb-bdc4-c416b8bff3d0
HOOK_URL_INTELLECT= os.environ["INTELLECT_HOOK_URL"]
##https://jtrustroyal.webhook.office.com/webhookb2/2f800b81-1e47-40c5-bdcc-f13184c06f4c@36fae7a7-647f-49c3-8de3-e0e14ea818ed/IncomingWebhook/2d70bd513fa1429ebd85013698075999/e0ffbf10-57d5-47bb-bdc4-c416b8bff3d0
HOOK_URL_POWERCARD= os.environ["POWERCARD_HOOK_URL"]



##default webhook :
##https://jtrustroyal.webhook.office.com/webhookb2/4504aa19-71e0-4697-952d-135dc121ac18@36fae7a7-647f-49c3-8de3-e0e14ea818ed/IncomingWebhook/671f66785ce242e38fd417fd3ece3732/0e3de6ea-9abb-4f7a-95cd-3ec6b796d2ca
HOOK_URL = os.environ["HOOK_URL"]

ENV=os.environ["ENV"]
#Event: 
#{"instance-id": "i-0e2b5d55bdec74f21", 
#"state": "stopping", 
#"time": "2021-04-13T08:42:33Z", 
#"region": "ap-southeast-1", 
#"account": "674352424895",
# "message": "At 2021-04-13T08:42:33Z, the status of your EC2 instance i-093f3ea672017bc9d on account 674352424895 in the AWS Region ap-southeast-1 has changed to stopping."
# }
webhook_map = {'finet':HOOK_URL_FINET,
                'intellect':HOOK_URL_INTELLECT,
                'powercard':HOOK_URL_POWERCARD}

defaultRegion="ap-southeast-1"
##set ec2 instance resources
ec2 = boto3.client('ec2',region_name=defaultRegion)
    
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
