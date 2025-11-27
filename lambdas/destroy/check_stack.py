import boto3
import os

def lambda_handler(event, context):
    project = event["project"]
    stage = event["stage"]
    type_ = event["type"]

    if type_ == "backend":
        stack_name = f"{project}-backend-{stage}"
        region = os.environ.get("DEFAULT_REGION", "ap-south-1")

    elif type_ == "frontend":
        stack_name = f"{project}-frontend-{stage}"
        region = os.environ.get("DEFAULT_REGION", "ap-south-1")

    elif type_ == "core":
        stack_name = f"{project}-{stage}"
        region = os.environ.get("DEFAULT_REGION", "ap-south-1")

    elif type_ == "waf":
        stack_name = f"{project}-waf-{stage}"
        region = "us-east-1"

    cf = boto3.client("cloudformation", region_name=region)

    try:
        resp = cf.describe_stacks(StackName=stack_name)
        status = resp["Stacks"][0]["StackStatus"]
        print("Stack:", stack_name, "Status:", status)
        return {"status": status, "project": project, "stage": stage, "type": type_}
    except cf.exceptions.ClientError as e:
        if "does not exist" in str(e):
            return {"status": "DELETE_COMPLETE", "project": project, "stage": stage, "type": type_}
        return {"status": "ERROR", "error": str(e)}
