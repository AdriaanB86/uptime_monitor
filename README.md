# Uptime Monitor

Uptime Monitor is a Telegram bot written in Python that checks websites every 5 minutes and messages you when a site goes down or comes back up. Each user manages their own list of sites with simple bot commands.

## Status
✅ Live: running 24/7 on an Oracle Cloud server

## Bot commands
| Command | What it does |
|---|---|
| `/start` or `/help` | Show the welcome message and the commands |
| `/list` | Show your monitored sites |
| `/add <url>` | Add a site, e.g. `/add https://example.com` (max 10 per user) |
| `/remove <number>` | Remove a site, using the number from `/list` |

Alerts look like this:
```
🔴 DOWN: https://example.com (500)
🟢 BACK UP: https://example.com (200)
```

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
- [x] Deployed to an Oracle Cloud server (Ubuntu, systemd) so it runs 24/7

## Roadmap
- [ ] Remember last status across restarts (save to a file)
- [ ] `/add` strips tracking parameters (everything after `?`) from URLs

## Built with
- Python
- requests
- python-dotenv
- Telegram Bot API
- Oracle Cloud (Always Free Ubuntu server) and systemd

## How to run
1. Create a bot with [@BotFather](https://t.me/BotFather) in Telegram and copy its token
2. Clone the repo and create a virtual environment
3. Install the packages: `pip install -r requirements.txt`
4. Create a `.env` file in the project folder with:
   ```
   TELEGRAM_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```
5. Run: `python uptime_monitor.py`
6. Open your bot in Telegram, tap **Start**, and add sites with `/add`

`sites.json` (each user's site list) and `uptime_log.txt` are created automatically, and are kept out of Git.

## Running 24/7 on a server
On the server, the bot runs as a systemd service, so it starts at boot and restarts itself if it crashes:

```ini
[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/uptime_monitor
ExecStart=/home/ubuntu/uptime_monitor/.venv/bin/python uptime_monitor.py
Restart=always
```

To update the server after pushing changes: `git pull`, then `sudo systemctl restart uptime-monitor`.
