import boto3
from config.settings import config


def get_aws_ssm_client():
    ssm_client = boto3.client(
        "ssm",
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION,
    )

    return ssm_client


def get_aws_ec2_client():
    ec2_client = boto3.client(
        "ec2",
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION,
    )

    return ec2_client
