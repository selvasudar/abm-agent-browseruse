import asyncio
import sys
import json
import os
import csv
import requests
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()
EMAIL = os.getenv("EMAIL_ID")
PASSWORD = os.getenv("PASWD")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Load LinkedIn profiles from JSON
with open("profiles.json", "r") as f:
    profiles = json.load(f)

# Prepare CSV output
output_file = "linkedin_results.csv"
fieldnames = ["LinkedIn URL", "Position", "Company"]

# Load previous data if exists
previous_data = {}
if os.path.exists(output_file):
    with open(output_file, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            previous_data[row["LinkedIn URL"]] = {
                "Position": row["Position"],
                "Company": row["Company"]
            }

async def extract_profile_info(profile_url):
    task = (
        f"Open {profile_url} on LinkedIn. "
        f"If login is required, use email: {EMAIL} and password: {PASSWORD}. "
        f"Then, extract the current position and company of the person. "
        f"Return it in a plain text format like: Position at Company."
    )

    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="o4-mini", temperature=1),
    )

    result = await agent.run()
    return result

async def main():
    updated_data = {}

    for url in profiles:
        print(f"Processing: {url}")
        try:
            info = await extract_profile_info(url)
            print(f"Extracted Info: {info.final_result()}")

            position, _, company = info.final_result().partition(" at ")
            position = position.strip()
            company = company.strip()

            previous = previous_data.get(url)
            if previous:
                if previous["Position"] != position or previous["Company"] != company:
                    # Change detected - trigger webhook
                    payload = {
                        "profile": url,
                        "old_position": previous["Position"],
                        "new_position": position,
                        "old_company": previous["Company"],
                        "new_company": company
                    }
                    print(f"🔔 Change detected for {url}. Triggering webhook.")
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        print(f"Webhook status: {response.status_code}")
                    except Exception as wh_error:
                        print(f"Webhook failed: {wh_error}")

            # Store latest data
            updated_data[url] = {"Position": position, "Company": company}

        except Exception as e:
            print(f"Error while processing {url}: {str(e)}")
            updated_data[url] = {"Position": "Error", "Company": str(e)}

    # Write updated data to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url, data in updated_data.items():
            writer.writerow({
                "LinkedIn URL": url,
                "Position": data["Position"],
                "Company": data["Company"]
            })

    print(f"✅ Done. Results saved in: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
