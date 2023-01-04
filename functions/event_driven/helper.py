"""helper logic for event driven function"""

import os
from logging import Logger
from typing import Tuple

from utils.storage import StorageClient

STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_CNX_STR = os.getenv("STORAGE_ACCOUNT_CNX_STR")
STORAGE_ACCOUNT_INPUT_CONTAINER = os.getenv("STORAGE_ACCOUNT_INPUT_CONTAINER")
STORAGE_ACCOUNT_OUTPUT_CONTAINER = os.getenv("STORAGE_ACCOUNT_OUTPUT_CONTAINER")


def help(logger: Logger, blob_url: str) -> Tuple[int, str]:
    """event driven helper function"""
    status = 200
    message = "file copied successfully!"

    try:
        # get file name
        file_name = blob_url.split("/")[-1]
        logger.info(f"blob name: {file_name}")

        # connect to storage client
        storage_client = StorageClient(
            account_name=STORAGE_ACCOUNT_NAME,
            cnx_str=STORAGE_ACCOUNT_CNX_STR
        )
        logger.info(f"{storage_client.__repr__()}")

        copy_result = storage_client.copy_file(
            container_name=STORAGE_ACCOUNT_INPUT_CONTAINER,
            source=file_name,
            dest_container=STORAGE_ACCOUNT_OUTPUT_CONTAINER,
            dest=file_name,
        )
        if not copy_result:
            status = 500
            message = "unable to copy file between storage containers!"
    except Exception as ex:
        status = 500
        message = f"exception occurred during file copy: {ex}"
        logger.error(message)
        pass
    
    return status, message
