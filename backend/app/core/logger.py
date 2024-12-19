import logging
from typing import Any, Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    if context:
        logger.error(f"Error: {str(error)}, Context: {context}")
    else:
        logger.error(f"Error: {str(error)}")

def log_info(message: str, context: Dict[str, Any] = None) -> None:
    if context:
        logger.info(f"{message}, Context: {context}")
    else:
        logger.info(message)