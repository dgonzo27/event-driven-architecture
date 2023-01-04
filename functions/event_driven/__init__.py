"""event driven function entrypoint"""

import os
import json

import azure.functions as func

from .helper import help
from utils.logging import FunctionName, init_logging

APP_INSIGHTS_CNX_STR = os.getenv("APP_INSIGHTS_CNX_STR")

logger = init_logging(function_name=FunctionName.ED, cnx_str=APP_INSIGHTS_CNX_STR)


def main(msg: func.QueueMessage) -> None:
    logger.info("\n\n event driven function has been invoked!")

    # parse msg data
    try:
        msg_data = msg.get_body().decode("utf-8")
        msg_json = json.loads(msg_data)
        blob_url = msg_json["data"]["url"]
    except Exception as ex:
        logger.exception(f"unexpected exception occurred: {ex}")
        logger.error("unable to parse blob url from msg")
        raise
    
    # core function logic
    status, message = help(logger, blob_url)

    if status == 200:
        logger.info(message)
    if status > 300:
        logger.error(message)
        raise
