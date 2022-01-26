import urllib3
import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

http = urllib3.PoolManager()


ENV=os.getenv("ENV", "-")
##default webhook :
HOOK_URL = os.environ["HOOK_URL"]

###map webhook by Tag Name
webhook_map = {
    'apihub-1': os.environ["APIHUB_HOOK_URL"],
    'sftp-1':os.environ["APIHUB_HOOK_URL"],
    'beamnet-app-1':os.environ["BEAMNET_APP_HOOK_URL"],
    'beamnet-db-1':os.environ["BEAMNET_DB_HOOK_URL"],
    'beamnet-web-1':os.environ["BEAMNET_WEB_HOOK_URL"],
    'controlm-app-1':os.environ["CONTROL_M_APP_WEB_HOOK_URL"],
    'controlm-slave-1':os.environ["CONTROL_M_SLAVE_HOOK_URL"],
    'finet-app-1':os.environ["FINET_APP_HOOK_URL"],
    'finet-db-1':os.environ["FINET_DB_HOOK_URL"],
    'fns-app-1':os.environ["FNS_HOOK_URL"],
    'intellect-db-1':os.environ["INTELLECT_DB_HOOK_URL"],
    'intellect-app-1':os.environ["INTELLECT_HOOK_URL"],
    'jasper-1':os.environ["JASPER_HOOK_URL"],
    'powercard-bo-1':os.environ["POWERCARD_APP_HOOK_URL"],
    'powercard-auth-1':os.environ["POWERCARD_APP_HOOK_URL"],
    'powercard-db-1':os.environ["POWERCARD_DB_HOOK_URL"],
    'controlm-db-1':os.environ["SHAREDSQL_DB_HOOK_URL"],
    'kartel-web-1':os.environ["WEB_HOOK_URL"]
}

defaultRegion="ap-southeast-1"
##set ec2 instance resources
ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.info("Message: " + str(message))
    alarm_name = message['AlarmName']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    region = message['Region']
    ### 1  how to get instance Id CPU & Memory first 
    instanceId=""
    try:
        instanceId = message['Trigger']['Dimensions'][0]['value']
    except:
        ## 2 DISK SPACE second
        metrics=message['Trigger']['Metrics']
        instanceId=get_instance_id(metrics)
    logger.info("InstanceId: "+ instanceId)
    
    instance_detail = get_instance_details(ec2, instanceId)
    instanceName="NA"
    webhook_url=""
    instanceName = get_name(instance_detail)
    applicationName= get_application_name(instance_detail)
    logger.info("instance name :" + instanceName + " , application : " + applicationName)
    webhook_url=get_webhook_url(instanceName)
    #generic
    if (webhook_url is None):
        webhook_url=HOOK_URL
    base_data = {
        "colour": "64a837",
        "title": "%s is resolved" %alarm_name,
        "text": "**%s** has changed from %s to %s - %s" %(alarm_name, old_state, new_state, region)
    }
    if new_state.lower() == 'alarm':
        base_data = {
            "colour": "d63333",
            "title": "Red Alert - There is an issue %s" %alarm_name,
            "text": "**%s** has changed from %s to %s - %s" %(alarm_name, old_state, new_state, region)
        }

    messages = {
        ('ALARM', 'my-alarm-name'): {
            "colour": "d63333",
            "title": "Red Alert - A bad thing happened.",
            "text": "These are the specific details of the bad thing."
        },
        ('OK', 'my-alarm-name'): {
            "colour": "64a837",
            "title": "The bad thing stopped happening",
            "text": "These are the specific details of how we know the bad thing stopped happening"
        }
    }
    data = messages.get((new_state, alarm_name), base_data)

    msg = {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": data["colour"],
        "title": "[" + ENV + "] - " + data["title"],
        "text": data["text"]
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    for i in range(3):
        try:
            resp = http.request('POST',webhook_url, body=encoded_msg)
            logger.info("POST message success")
            # print({
            #     "message": event['Records'][0]['Sns']['Message'],
            #     "status_code": resp.status,
            #     "response": resp.data
            # })
            return { "status": "200 OK"}
        except:
            logger.error("Request failed: " + str(i))


def get_instance_id(metrics):
    for item in metrics:
        # check ["MetricStat"] ["Metric"]
        instanceId=""
        try:
            dimensions=item["MetricStat"]["Metric"]["Dimensions"]
            for dimension in dimensions:
                if dimension["name"].lower() == 'instanceid':
                    instanceId=(dimension["value"])
                    break
        except:continue
    
    return instanceId

    
def get_webhook_url(tag):
    return webhook_map.get(tag)

def get_application_name(instance):
    ##test if component tag is db --return it
    if (get_component_name(instance) == 'db'):
        return 'db'

    for t in instance["Tags"]:
        if t["Key"] == "application":
            return t["Value"]
    return instance["InstanceId"]

    
def get_component_name(instance):
    for t in instance["Tags"]:
        if t["Key"] == "component":
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

    return instances[0]


# {
#     "Records": [
#         {
#             "Sns": {
#                 "Message": "{\"AlarmName\":\"Critical - powercard-bo-1 CPU Utilization >=70%\",\"AWSAccountId\":\"127201881249\",\"NewStateValue\":\"ALARM\",\"NewStateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints [6.0 (17/05/21 07:31:00)] was greater than or equal to the threshold (5.0) (minimum 1 datapoint for OK -> ALARM transition).\",\"StateChangeTime\":\"2021-05-17T07:36:57.490+0000\",\"Region\":\"Asia Pacific (Singapore)\",\"AlarmArn\":\"arn:aws:cloudwatch:ap-southeast-1:127201881249:alarm:Critical - powercard-bo-1 CPU Utilization >=70%\",\"OldStateValue\":\"OK\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Namespace\":\"AWS/EC2\",\"StatisticType\":\"Statistic\",\"Statistic\":\"AVERAGE\",\"Dimensions\":[{\"value\":\"i-045ec59178c193707\",\"name\":\"InstanceId\"}],\"Period\":300,\"EvaluationPeriods\":1,\"ComparisonOperator\":\"GreaterThanOrEqualToThreshold\",\"Threshold\":5.0,\"TreatMissingData\":\"- TreatMissingData:                    missing\",\"EvaluateLowSampleCountPercentile\":\"\"}}"
#             }
#         }
#     ]
# }

###Payload Diskspace
#{
#  "Records": [
#    {
#      "Sns": {
#        "Message": "{\"AlarmName\":\"TESTING DiskSpace Warning-APIHUB -db-1/u01volumediskspacefree<=30%\",\"AlarmDescription\":\"\",\"AWSAccountId\":\"391246823000\",\"NewStateValue\":\"ALARM\",\"NewStateReason\":\"ThresholdCrossed:1outofthelast1datapoints[29.963851339914484(25/01/2223:00:00)]waslessthanorequaltothethreshold(30.0)(minimum1datapointforOK->ALARMtransition).\",\"StateChangeTime\":\"2022-01-25T23:05:48.226+0000\",\"Region\":\"AsiaPacific(Singapore)\",\"AlarmArn\":\"arn:aws:cloudwatch:ap-southeast-1:391246823000:alarm:Warning-Intellect-db-1/u01volumediskspacefree<=30%\",\"OldStateValue\":\"OK\",\"Trigger\":{\"Period\":300,\"EvaluationPeriods\":1,\"ComparisonOperator\":\"LessThanOrEqualToThreshold\",\"Threshold\":30,\"TreatMissingData\":\"missing\",\"EvaluateLowSampleCountPercentile\":\"\",\"Metrics\":[{\"Expression\":\"(m2/m1*100)\",\"Id\":\"e1\",\"Label\":\"Intellect-db-1/u01volumediskspacefree%\",\"ReturnData\":\"True\"},{\"Id\":\"m2\",\"MetricStat\":{\"Metric\":{\"Dimensions\":[{\"value\":\"/u01\",\"name\":\"path\"},{\"value\":\"i-04dcd03f207365696\",\"name\":\"InstanceId\"},{\"value\":\"nvme1n1\",\"name\":\"device\"},{\"value\":\"ext4\",\"name\":\"fstype\"}],\"MetricName\":\"disk_free\",\"Namespace\":\"CWAgent\"},\"Period\":300,\"Stat\":\"Average\"},\"ReturnData\":\"False\"},{\"Id\":\"m1\",\"MetricStat\":{\"Metric\":{\"Dimensions\":[{\"value\":\"/u01\",\"name\":\"path\"},{\"value\":\"i-09498a5680e490e2c\",\"name\":\"InstanceId\"},{\"value\":\"nvme1n1\",\"name\":\"device\"},{\"value\":\"ext4\",\"name\":\"fstype\"}],\"MetricName\":\"disk_total\",\"Namespace\":\"CWAgent\"},\"Period\":300,\"Stat\":\"Average\"},\"ReturnData\":\"False\"}]}}"
#      }
#    }
#  ]
#}
