from handlers.data_handler import handle_get_non_compliant_ec2_instances_ids
from clients.aws_client import get_aws_ec2_client, get_aws_ssm_client
from config.logger import logger


def data_collector():
    logger.info("Data_Collector starting...")
    ec2_client, ssm_client = get_aws_ec2_client(), get_aws_ssm_client()
    non_compliant_ec2_instances_ids = handle_get_non_compliant_ec2_instances_ids(
        ssm_client, ec2_client
    )

    if non_compliant_ec2_instances_ids:
        logger.info(
            f"Found {len(non_compliant_ec2_instances_ids)} non compliant EC2 instances"
        )
        logger.info(
            "Non-compliant EC2 instance IDs:\n%s",
            "\n".join(non_compliant_ec2_instances_ids),
        )

    logger.info("Done!")


if __name__ == "__main__":
    data_collector()
