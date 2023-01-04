"""common logging for easy integration with application insights"""

import logging
import sys

from typing import Any, Dict, Optional

from opencensus.ext.azure.log_exporter import AzureLogHandler


class FunctionName:
    ED = "event_driven"


PACKAGES = {
    FunctionName.ED: "event_driven",
}


class OptionalCustomDimensionsFilter(logging.Formatter):
    """filter that outputs `custom_dimensions` if present"""

    def __init__(self, message_fmt: str, function_name: str) -> None:
        logging.Formatter.__init__(self, message_fmt, None)
        self.function_name = function_name
    
    def format(self, record: logging.LogRecord) -> str:
        if "custom_dimensions" not in record.__dict__:
            record.__dict__["custom_dimensions"] = ""
        else:
            # add the function name to custom_dimensions so it's queryable
            record.__dict__["custom_dimensions"]["function"] = self.function_name
        return super().format(record)


class CustomDimensionsFilter(logging.Filter):
    """filter for azure-targeted messages containing `custom_dimensions`"""

    def filter(self, record: logging.LogRecord) -> bool:
        return bool(record.__dict__["custom_dimensions"])


def init_logging(function_name: str, cnx_str: Optional[str] = None) -> logging.Logger:
    """initialize log handlers"""
    package = PACKAGES[function_name]
    logger = logging.getLogger(package)
    logger.setLevel(logging.INFO)

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_format = "[%(levelname)s] %(asctime)s - %(message)s %(custom_dimensions)s"
    formatter = OptionalCustomDimensionsFilter(console_format, function_name)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # azure log handler
    if cnx_str is not None:
        azure_handler = AzureLogHandler(connection_string=cnx_str)
        azure_handler.addFilter(CustomDimensionsFilter())
        logger.addHandler(azure_handler)
    else:
        logger.info(f"azure log handler not attached: {package} (missing key)")
    return logger


def get_custom_dimensions(
    dimensions: Dict[str, Any], function_name: str
) -> Dict[str, Any]:
    """merge the base dimensions with the given dimensions"""
    base_dimensions = {"function": function_name}
    base_dimensions.update(dimensions)
    return {"custom_dimensions": base_dimensions}
