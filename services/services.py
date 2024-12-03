from typing import List
from pydantic import ValidationError
from config.logger import logger
from models.resource_model import NonCompliantResource
from botocore.exceptions import ClientError


def get_non_compliant_resource_ids(ssm_client) -> List[str]:
    """Function to validate ids as EC2 IDs."""
    logger.debug("Start")
    instance__ids: str = []
    next_token = None
    params = {
        "Filters": [{"Key": "Status", "Values": ["NON_COMPLIANT"], "Type": "EQUAL"}]
    }

    while True:
        if next_token:
            params["NextToken"] = next_token

        try:
            response = ssm_client.list_resource_compliance_summaries(**params)
            instances = response.get("ResourceComplianceSummaryItems", [])

            for instance in instances:
                try:
                    non_complianed_item = NonCompliantResource(**instance)
                    instance__ids.append(non_complianed_item.resource_id)
                except ValidationError as e:
                    logger.debug(f"Validation failed moving on")

            next_token = response.get("NextToken")

            if not next_token:
                break

        except Exception as e:
            logger.critical(f"Error retrieving data: {e}")
            break
    logger.info(f"Received {len(instance__ids)} compatible entities")
    logger.debug("End")
    return instance__ids


def is_valid_ec2_id(ec2_client, resource_id) -> bool:
    """
    Function to validate a single ID as an EC2 ID.

    Returns:
        bool: True if the ID is valid, False otherwise.
    """
    try:
        ec2_client.describe_instances(InstanceIds=[resource_id])
        return True
    except ClientError as e:
        if e.response.get("Error", {}):
            return False
        else:
            raise e
