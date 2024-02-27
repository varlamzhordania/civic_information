import os
import csv
from google_civic_information_api import elections
from logger import main_logger as logger  # Assuming logger is correctly imported


def handle_elections(csv_filename, API_KEY):
    """
    Fetches election data using the Google Civic Information API and writes it to a CSV file.

    Parameters:
    - csv_filename (str): The filename (including path) for the CSV file.
    - API_KEY (str): The API key for accessing the Google Civic Information API.

    Returns:
    - dict: The JSON data containing election information.
    """

    try:
        # Define the header for the CSV file
        header = ["id", "name", "electionDay", "ocdDivisionId"]

        # Get election data from the Google Civic Information API
        result = elections.elections(api_key=API_KEY)

        # Check if the API request was successful
        if result.ok:
            # Extract JSON data
            data = result.json()

            # Write JSON data to a CSV file
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=',')

                # Check if the file exists; if not, write the header
                file_exists = os.path.exists(csv_filename)
                if not file_exists or csv_file.tell() == 0:
                    csv_writer.writeheader()

                # Iterate through each election and write it as a row
                for election in data["elections"]:
                    csv_writer.writerow(election)

            # Log success message
            logger.info("Election data successfully written to CSV file")

            # Return the JSON data for potential further use
            return data
        else:
            # Log error message with HTTP status code
            logger.error(
                f"Got error while fetching election data from Google Civic Information \n Error code: {result.status_code}"
            )
            return None

    except Exception as e:
        # Log generic exception message
        logger.error(f"An error occurred: {e}")
        return None
