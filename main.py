# pylint: disable=consider-using-with

"""
This module contains the main function to start the application.
"""

import os
import logging
import requests

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ask_llm(user_prompt):
    """Use OpenAI API to generate a response to the user's prompt."""

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_KEY")
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.1,
    )

    return response.choices[0].message.content


def fetch_serpapi_data():
    """Get today's penny stocks details from the SerpAPI using Google AI Mode engine."""

    params = {
        "engine": "google_ai_mode",
        "q": "today's penny stocks to buy for long term in india under 100 rupees.",
        "api_key": os.getenv("SERPAPI_KEY"),
    }

    url = "https://serpapi.com/search"

    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 200:
        return response.json()

    logging.error("Error fetching SerpAPI data: %s", response.status_code)
    raise ValueError(f"SerpAPI error: {response.status_code} - {response.text}")


def generate_recommendation(summarized_data):
    """Generate a recommendation based on the summarized data."""

    prompt_template = open(
        "financial_research_assistant_prompt.txt", encoding="utf-8"
    ).read()
    prompt = prompt_template.format(summarized_data=summarized_data)
    recommendation = ask_llm(prompt)
    logging.info("Recommendation:\n%s", recommendation)
    return recommendation


def send_to_telegram(message):
    """Send the generated message to Telegram."""
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"

    payload = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": message,
        "parse_mode": "Markdown",
    }

    response = requests.post(url, data=payload, timeout=10)
    if response.status_code != 200:
        print("Error sending to Telegram:", response.status_code, response.text)
    else:
        print("Message sent to Telegram")


def main():
    """Main function to start the application."""

    logging.info("Starting the application...")

    logging.info("Loading environment variables...")
    load_dotenv()
    logging.info("Environment variables loaded successfully.")

    logging.info("Fetching SerpAPI data...")
    serp_data = fetch_serpapi_data()
    logging.info("SerpAPI data fetched successfully.")

    logging.info("Generating recommendation...")
    todays_penny_stock = generate_recommendation(serp_data["reconstructed_markdown"])
    logging.info("Recommendation generated successfully.")

    logging.info("Adding URL to the recommendation...")
    todays_penny_stock += (
        f"\n*🔗 URL:* {serp_data['search_metadata']['prettify_html_file']}"
    )
    logging.info("URL added successfully.")

    logging.info("Sending recommendation to Telegram...")
    send_to_telegram(todays_penny_stock)
    logging.info("Recommendation sent to Telegram successfully.")

    logging.info("Application finished.")


if __name__ == "__main__":
    main()
