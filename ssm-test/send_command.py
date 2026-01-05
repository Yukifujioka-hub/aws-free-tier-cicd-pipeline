import boto3
import time
from botocore.exceptions import ClientError

INSTANCE_ID = "i-073b770df4e9e361b"
REGION = "us-east-1"
CONTAINER_NAME = "myapp"
IMAGE_NAME = "myapp:latest"

ssm = boto3.client("ssm", region_name=REGION)

commands = [
    "echo '=== Deploy start ==='",

    "cd ~/aws-free-tier-cicd-pipeline && git pull origin main",

    f"sudo docker build -t {IMAGE_NAME} ./app",

    f"sudo docker stop {CONTAINER_NAME} || true",
    f"sudo docker rm {CONTAINER_NAME} || true",
    f"sudo docker run -d --name {CONTAINER_NAME} -p 80:5000 {IMAGE_NAME}",

    "echo '=== Image cleanup ==='",
    "sudo docker image prune -f",

    "echo '=== Deploy end ==='"
]

response = ssm.send_command(
    InstanceIds=[INSTANCE_ID],
    DocumentName="AWS-RunShellScript",
    Parameters={"commands": commands}
)

command_id = response["Command"]["CommandId"]
print("Command ID:", command_id)

while True:
    try:
        result = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=INSTANCE_ID
        )
        status = result["Status"]
        print("Current Status:", status)

        if status in ["Success", "Failed", "Cancelled", "TimedOut"]:
            break

    except ClientError as e:
        if "InvocationDoesNotExist" in str(e):
            print("Waiting for invocation to be created...")
        else:
            raise e

    time.sleep(5)

print("Final Status:", status)
print(result["StandardOutputContent"])
