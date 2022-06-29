# Requirements

- The Bash shell. For Linux and macOS, this is included by default. In Windows 10, you can install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to get a Windows-integrated version of Ubuntu and Bash.
- [The AWS CLI v1](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).


# bash_aws_scan_resources
aws scan resoureces for optimization costs

-   EC2
-   EIP
-	ELB
-	AMI / SNAPSHOT / VOLUMES
-	RDS SNAPSHOT
-	Security Group
-	Cloudwatch
-	CloudFormation
-	LAMBDA
-	APIGETWAY
-	S3


# Tools
You need to install the following tools
- shellscripts
- aws cli
- jq tool
# set aws-cli as local environment
You need to install aws cli command set up ~/.aws/credentails

[default]
aws_access_key_id = xxxxxxx
aws_secret_access_key = xxxxxxxxxxxx/5V+o7CXv283Ep

# how to run it

sh scan.sh

````
DATE SCAN : 18-03-2021
REGION : ap-southeast-1, ACCOUNT_ID : 32900xxxxx
=========Elastic IP - unassociated with instances=========
=============AMIs==============
    AIM Found 5
    ============EC2 instances used by AMIs============
       ec2-instance-id:i-00d16 - imageId : ami-01d7ced9e19e9
       ec2-instance-id:i-03b677e367846 - imageId : ami-02f3d7454
    ============UNUSED AMIs============
    - ID:ami-060e52fa40fa - Name : beamnet-
    - ID:ami-068300ac214e - Name : web-server-instance
    - ID:ami-086cfda2807b85 - Name : fns-app-1-102
    - ID:ami-09ab861fbf34 - Name : cbs-devbackup
====================2 snapshots found=======
====================2 snapshots exist for non-existing volumes:=======
  - snap-061f365-vol-0470de3
  - snap-04f9ba2bb38-vol-0bea52833
 
=========Unused Snaphosts- (no ami attached)=========
=========Unattached Volumes=====(aws ec2 delete-volume --volume-id)====
============Scanning RDS snapshots=============
================Active Security Groups ==============
Security Groug used by instance: sg-0a6c2xxxd8
Security Groug used by instance: sg-0027674xxx3bdc491a
================Unused Security Groups==============
ID:sg-06aee49ea0f6c8-Name:default
ID:sg-07bcae3eab181d-Name:default
ID:sg-0930186429974b8-Name:route53-internalzone-SG
ID:sg-0ab6711a1879c-Name:dev-r53-resolver
ID:sg-0bf2096e6d7b3fc3-Name:dev-vpc-endpoints
ID:sg-0e0d7cf03246b-Name:ssh-from-vpn
================ELB ==============

````


=========Elastic IP - unassociated with instances=========
13.251.193.246
18.139.37.54
3.0.53.234
