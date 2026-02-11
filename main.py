"""
Today's Penny Stock - Indian Market
Author: Sanjay Reddy B
"""

import os
import datetime
import logging

import requests
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# from ollama import chat  # Uncomment if using Ollama

# =============================
# CONFIG
# =============================
load_dotenv()  # Load environment variables from .env file


# =============================
# STEP 1: SERPAPI QUERY
# =============================
def get_serp_data():
    """Fetch data from SerpAPI."""
    today = datetime.date.today().strftime("%B %d, %Y")

    params = {
        "engine": "google_ai",
        "q": (
            f"Top penny stocks to buy in India for long-term investment, "
            f"including stock names and IDs for {today}"
        ),
        "api_key": os.getenv("SERPAPI_KEY"),
    }

    url = "https://serpapi.com/search"

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        logging.info(response.text)
    else:
        logging.error("Error fetching SerpAPI data: %s", response.status_code)

    return response.json()


# =============================
# STEP 2: EXTRACT TEXT (like your JS node)
# =============================
def extract_text(item):
    """Recursively extract text from nested structures."""
    texts = []

    if isinstance(item, dict):
        if "snippet" in item and isinstance(item["snippet"], str):
            texts.append(item["snippet"])

        if "list" in item and isinstance(item["list"], list):
            for el in item["list"]:
                texts.extend(extract_text(el))

    elif isinstance(item, list):
        for el in item:
            texts.extend(extract_text(el))

    return texts


def combine_text_blocks(data):
    """Combine all text blocks into a single string."""
    all_texts = []

    text_blocks = data.get("text_blocks", [])
    for item in text_blocks:
        all_texts.extend(extract_text(item))

    return " ".join(all_texts)


# =============================
# STEP 3: LLM ANALYSIS
# =============================
def analyze_with_llm(user_prompt):
    """Use OpenAI API to analyze the combined text and generate a recommendation."""

    system_prompt = """
You are a highly intelligent financial research assistant specialized in the Indian stock market.
Choose the best long-term, future-focused Indian penny stock.
Retain the exact stock symbol from the text.
Format output exactly as:

📈 *Best Penny Stock for Today — Indian Market*

*Company:* {Company Name} (`{Stock Symbol}`)
🚀 *Growth Potential:* ...
📌 *Key Reason:* ...
⚠️ *Key Risks:* ...
"""

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_KEY")
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content


# =============================
# STEP 4: SEND TO TELEGRAM
# =============================
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


# =============================
# MAIN FLOW
# =============================
if __name__ == "__main__":
    print("Fetching SerpAPI data...")
    serp_data = get_serp_data()

    print("Combining text blocks...")
    COMBINED_TEXT = combine_text_blocks(serp_data)

    print("Analyzing with LLM...")
    result = analyze_with_llm(COMBINED_TEXT)

    print("Sending to Telegram...")
    send_to_telegram(result)

    print("Done ✅")
