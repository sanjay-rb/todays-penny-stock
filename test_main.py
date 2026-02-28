# pylint: disable=unused-import
"""
This module contains the test function to test the application.
"""

import logging
from dotenv import load_dotenv

from main import fetch_serpapi_data, generate_recommendation, send_to_telegram
import json


def test():
    """Main function to start the application."""

    logging.info("Starting the application...")

    logging.info("Loading environment variables...")
    load_dotenv()
    logging.info("Environment variables loaded successfully.")

    logging.info("Fetching SerpAPI data...")
    # serp_data = fetch_serpapi_data()
    # serp_data = json.loads(open("serp_data_out.json", "r", encoding="utf-8").read())
    logging.info("SerpAPI data fetched successfully.")

    logging.info("Generating recommendation...")
    # todays_penny_stock = generate_recommendation(serp_data["reconstructed_markdown"])
    # todays_penny_stock = open("todays_penny_stock_out.txt", "r", encoding="utf-8").read()
    logging.info("Recommendation generated successfully.")

    logging.info("Adding URL to the recommendation...")
    # todays_penny_stock += (f"\n*🔗 URL:* {serp_data['search_metadata']['prettify_html_file']}")
    logging.info("URL added successfully.")

    logging.info("Sending recommendation to Telegram...")
    # send_to_telegram(todays_penny_stock)
    logging.info("Recommendation sent to Telegram successfully.")

    logging.info("Application finished.")


if __name__ == "__main__":
    test()
