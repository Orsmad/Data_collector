from concurrent.futures import ThreadPoolExecutor

import concurrent
from config.logger import logger
from config.settings import config
from services.services import get_non_compliant_resource_ids, is_valid_ec2_id


def validate_ec2_ids_in_batch(ec2_client, resource_ids_batch):
    """
    Helper function to validate EC2 IDs in a batch.

    Returns:
        list: Valid EC2 IDs from the batch.
    """
    return [
        resource_id
        for resource_id in resource_ids_batch
        if is_valid_ec2_id(ec2_client, resource_id)
    ]


def handle_get_non_compliant_ec2_instances_ids(ssm_client, ec2_client):
    logger.debug("Starting data handler")
    """
    Handles the process of retrieving and validating EC2 instances that are non-compliant.

    Returns:
        list: Valid non-compliant EC2 instance IDs.
    """
    resource_ids: list[str] = get_non_compliant_resource_ids(ssm_client)
    if len(resource_ids) < 1:
        logger.debug("Couldn't find non complient resources")
        return []

    valid_ec2_ids: list[str] = []
    shard_size: int = config.SHARD_SIZE
    max_workers: int = config.MAX_WORKERS
    logger.info("Validating resources as EC2 instances...")
    # Divide the resource IDs into shards
    shards = [
        resource_ids[i : i + shard_size]
        for i in range(0, len(resource_ids), shard_size)
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit validation tasks for each shard
        futures = [
            executor.submit(validate_ec2_ids_in_batch, ec2_client, shard)
            for shard in shards
        ]
        for future in concurrent.futures.as_completed(futures):
            valid_ec2_ids.extend(future.result())
    logger.debug("Finsihed data handler")
    return valid_ec2_ids
