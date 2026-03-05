"""Global Configuration File"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "pk_oa")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/rowanxading")

# Admin Configuration
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))

# Points Configuration
VERIFY_COST = 1  # Points consumed for verification
CHECKIN_REWARD = 1  # Points reward for check-in
INVITE_REWARD = 2  # Points reward for invitation
REGISTER_REWARD = 1  # Points reward for registration

# Help Links
HELP_NOTION_URL = "https://rowanfolio.netlify.app/"
