import boto3
import json
import os

def lambda_handler(event, context):
    project = os.environ["PROJECT_NAME"]
    base_project_name = os.environ["BASE_PROJECT_NAME"]
    stage = os.environ["ENVIRONMENT"]
    state_machine_arn = os.environ["STATE_MACHINE_ARN"]

    input_data = {
        "project": base_project_name,
        "stage": stage
    }

    sf = boto3.client("stepfunctions")

    sf.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(input_data)
    )

    return {"started": True}
