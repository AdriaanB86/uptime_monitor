# Uptime Monitor

Uptime Monitor is a Python program that automatically checks if websites are online, logs the results, and sends a Telegram alert when a site goes down.

## Status
🚧 Work in progress

## Features
- [x] Check if a single website is up
- [x] Check a list of websites
- [x] Log results to a file
- [x] Send a Telegram alert when a site goes down
- [x] Run checks automatically on a schedule
- [x] Save each user's site list in a JSON file
- [x] Bot reads incoming Telegram messages
- [x] `/list` command: show your monitored sites
- [x] `/add <url>` command: add a site (max 10 per user)
- [x] `/remove <number>` command: remove a site
- [x] Alert only when a site's status changes (no repeated alerts)
- [x] Multiple users, each with their own independent list
- [x] `/start` and `/help` show a welcome message and the commands

## Roadmap
- [ ] Deploy to a server so it runs 24/7

## Built with
- Python
- requests
- python-dotenv
- Telegram Bot API

## How to run
1. Clone the repo and create a virtual environment
2. Install the packages: `pip install -r requirements.txt`
3. Create a `.env` file in the project folder with:
   ```
   TELEGRAM_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```
4. Create a `sites.json` file with your chat ID and the sites to monitor:
   ```
   {
     "your_chat_id": ["https://www.google.com"]
   }
   ```   
5. Run: `python uptime_monitor.py`