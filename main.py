import os
import sys
import json
import configparser
from logger import main_logger as logger
from utils import handle_elections
from datetime import datetime


def run_google_civic_script():
    """
    Main script to fetch election data using the Google Civic Information API and write it to a CSV file.

    This script reads configuration from 'config.ini', including API key and CSV path.
    It uses the handle_elections function from the utils module to fetch and write election data.

    Returns:
    - None
    """

    # Read configuration from 'config.ini'
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize logging and script metadata
    logger.info("Google Civic Information API Script Running")
    logger.info(f"Script Run Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Retrieve API key and CSV path from config
    API_KEY = config["General"]["API_KEY"]
    csv_dir = config["General"]["CSV_PATH"]

    # Generate CSV filename based on the current timestamp
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')
    election_csv_filename = os.path.join(csv_dir, f"local_elections_{now}" + ".csv")

    # Check if API key is available
    if not API_KEY:
        logger.error("API key not found in config")
        sys.exit(0)

    try:
        logger.info("Fetching Elections Data")

        # Call the handle_elections function to fetch and write election data
        elections_data = handle_elections(election_csv_filename, API_KEY)

    except Exception as e:
        # Log any exceptions that occur during script execution
        logger.error("An error occurred while trying to get information from Google Civic \n Error: ", e)
    finally:
        logger.info(f"Terminating Script – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sys.exit(1)


if __name__ == "__main__":
    run_google_civic_script()
