#ABM Agent

Overview
The ABM Agent (Account-Based Marketing Agent) is an asynchronous Python script designed to scrape LinkedIn profiles for current position and company information, track changes in profile data, and send notifications via a webhook when changes are detected. The results are saved to a CSV file for further analysis.
Features

Profile Scraping: Extracts the current position and company of individuals from LinkedIn profiles listed in a profiles.json file.
Change Detection: Compares new data with previous data stored in linkedin_results.csv to identify updates in position or company.
Webhook Notifications: Sends change notifications to a specified webhook URL.
CSV Output: Saves extracted data to linkedin_results.csv with columns for LinkedIn URL, position, and company.
Asynchronous Processing: Uses Python's asyncio for efficient execution.

Prerequisites

Python: Version 3.8 or higher.
Dependencies: Install required packages using:pip install -r requirements.txt


Environment Variables: Create a .env file in the project root with the following variables:EMAIL_ID=your_linkedin_email
PASWD=your_linkedin_password
WEBHOOK_URL=your_webhook_url


Input File: A profiles.json file containing a list of LinkedIn profile URLs (e.g., ["https://www.linkedin.com/in/example1", "https://www.linkedin.com/in/example2"]).

Installation

Clone the repository or download the script.
Install dependencies:pip install aiohttp python-dotenv requests

Note: The browser_use and browser_use.llm modules (including Agent and ChatOpenAI) are assumed to be custom or part of a specific library. Ensure these are available or replace with equivalent functionality.
Create and configure the .env file with your LinkedIn credentials and webhook URL.
Prepare the profiles.json file with the LinkedIn profile URLs to scrape.

Usage

Ensure the .env file and profiles.json are set up correctly.
Run the script:python abm_agent.py


The script will:
Load LinkedIn profile URLs from profiles.json.
Log in to LinkedIn using the provided credentials (if required).
Extract position and company data for each profile.
Compare with previous data (if linkedin_results.csv exists).
Send webhook notifications for any changes detected.
Save results to linkedin_results.csv.



Output

CSV File: linkedin_results.csv with columns:
LinkedIn URL: The LinkedIn profile URL.
Position: The person's current position (or "Error" if extraction failed).
Company: The person's current company (or error message if extraction failed).


Webhook Payload: On change detection, a JSON payload is sent to the WEBHOOK_URL with:{
  "profile": "linkedin_url",
  "old_position": "previous_position",
  "new_position": "current_position",
  "old_company": "previous_company",
  "new_company": "current_company"
}



Notes

LinkedIn Access: Ensure the provided LinkedIn credentials have access to the profiles. LinkedIn may impose rate limits or require CAPTCHA verification, which could cause errors.
Error Handling: The script logs errors for failed profile extractions and webhook requests but continues processing. Check the console output for details.
Concurrency: The current implementation processes profiles sequentially. For better performance, consider modifying the main function to use asyncio.gather for concurrent processing.
Custom Modules: The script uses browser_use.Agent and browser_use.llm.ChatOpenAI. Replace these with appropriate libraries or custom implementations if needed.

Example
Input (profiles.json)
[
  "https://www.linkedin.com/in/johndoe",
  "https://www.linkedin.com/in/janesmith"
]

Output (linkedin_results.csv)
LinkedIn URL,Position,Company
https://www.linkedin.com/in/johndoe,Software Engineer,Tech Corp
https://www.linkedin.com/in/janesmith,Product Manager,Innovate Inc

Webhook Payload (on change)
{
  "profile": "https://www.linkedin.com/in/johndoe",
  "old_position": "Software Engineer",
  "new_position": "Senior Software Engineer",
  "old_company": "Tech Corp",
  "new_company": "Tech Corp"
}

Limitations

LinkedIn Rate Limits: Excessive scraping may trigger LinkedIn's anti-bot measures.
Data Format: The script assumes the extracted data is in the format "Position at Company". Variations may cause parsing errors.
Dependencies: The browser_use and ChatOpenAI modules are not standard; ensure they are available or adapt the script accordingly.

License
This project is licensed under the MIT License.
