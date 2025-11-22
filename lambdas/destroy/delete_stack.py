import boto3
import os

def lambda_handler(event, context):
    project = event["project"]
    stage = event["stage"]
    type_ = event["type"]

    # Determine stack name & region
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
        stack_name = f"{project}-{stage}-waf"
        region = "us-east-1"

    cf = boto3.client("cloudformation", region_name=region)

    print(f"Deleting: {stack_name} in {region}")

    try:
        cf.delete_stack(StackName=stack_name)
    except Exception as e:
        print("Error:", str(e))
        return {"status": "ERROR", "error": str(e)}

    return {
        "status": "DELETE_TRIGGERED",
        "project": project,
        "stage": stage,
        "type": type_
    }
