import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Default to INFO if not set

# Create a basic logger
logger = logging.getLogger(__name__)  # __name__ gets the current module's name
logger.setLevel(LOG_LEVEL)

# Create console handler (outputs to the terminal)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
