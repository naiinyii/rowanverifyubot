# SheerID Auto-Verification Telegram Bot

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> 🤖 Telegram bot that automatically completes SheerID student/teacher verification
> 
> Improved based on [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond's legacy code

---

## 📋 Project Introduction

This is a Python-based Telegram bot that can automatically complete SheerID student/teacher identity verification for multiple platforms. The bot automatically generates identity information, creates verification documents, and submits them to the SheerID platform, greatly simplifying the verification process.

> **⚠️ Important Notice**:
> 
> - **Gemini One Pro**, **ChatGPT Teacher K12**, **Spotify Student**, **YouTube Premium Student** and other services require updating the `programId` and other verification information in each module's configuration file before use. Please refer to the "Before Using" section below.
> - This project also provides implementation ideas and API documentation for **ChatGPT Military Verification**. For details, see [`military/README.md`](military/README.md). Users can integrate it according to the documentation.

### 🎯 Supported Verification Services

| Command | Service | Type | Status | Description |
|---------|---------|------|--------|-------------|
| `/verify` | Gemini One Pro | Teacher Verification | ✅ Complete | Google AI Studio Educational Discount |
| `/verify2` | ChatGPT Teacher K12 | Teacher Verification | ✅ Complete | OpenAI ChatGPT Educational Discount |
| `/verify3` | Spotify Student | Student Verification | ✅ Complete | Spotify Student Subscription Discount |
| `/verify4` | Bolt.new Teacher | Teacher Verification | ✅ Complete | Bolt.new Educational Discount (Auto-get code) |
| `/verify5` | YouTube Premium Student | Student Verification | ⚠️ Beta | YouTube Premium Student Discount (see notes below) |

> **⚠️ YouTube Verification Special Notes**:
> 
> YouTube verification is currently in beta status. Please read [`youtube/HELP.MD`](youtube/HELP.MD) carefully before using.
> 
> **Main Differences**:
> - YouTube's original link format differs from other services
> - Need to manually extract `programId` and `verificationId` from browser network logs
> - Then manually compose the standard SheerID link format
> 
> **Usage Steps**:
> 1. Visit YouTube Premium Student Verification Page
> 2. Open browser developer tools (F12) → Network tab
> 3. Start verification process, search for `https://services.sheerid.com/rest/v2/verification/`
> 4. Get `programId` from request payload, `verificationId` from response
> 5. Manually compose link: `https://services.sheerid.com/verify/{programId}/?verificationId={verificationId}`
> 6. Submit using `/verify5` command

> **💡 ChatGPT Military Verification Ideas**:
> 
> This project provides implementation ideas and API documentation for ChatGPT Military SheerID verification. The military verification process differs from regular student/teacher verification, requiring first executing the `collectMilitaryStatus` interface to set military status, then submitting the personal information form. For detailed implementation ideas and API documentation, see [`military/README.md`](military/README.md). Users can integrate it into the bot according to the documentation.

### ✨ Core Features

- 🚀 **Automated Process**: Complete information generation, document creation, and verification submission in one click
- 🎨 **Smart Generation**: Automatically generate student/teacher ID PNG images
- 💰 **Points System**: Multiple ways to earn points through check-in, invitations, and card key redemption
- 🔐 **Secure & Reliable**: Uses MySQL database with environment variable configuration support
- ⚡ **Concurrency Control**: Intelligent management of concurrent requests for stability
- 👥 **Management Features**: Comprehensive user and points management system

---

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Bot Framework**: python-telegram-bot 20.0+
- **Database**: MySQL 5.7+
- **Browser Automation**: Playwright
- **HTTP Client**: httpx
- **Image Processing**: Pillow, reportlab, xhtml2pdf
- **Environment Management**: python-dotenv

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Environment Variables

Copy `env.example` to `.env` and fill in the configuration:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel
ADMIN_USER_ID=your_admin_id

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=tgbot_verify
```

### 4. Start the Bot

```bash
python bot.py
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# 1. Modify .env file configuration
cp env.example .env
nano .env

# 2. Start services
docker-compose up -d

# 3. View logs
docker-compose logs -f
```

### Manual Docker Deployment

```bash
# Build image
docker build -t tgbot-verify .

# Run container
docker run -d \
  --name tgbot-verify \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  tgbot-verify
```

---

## 📖 Usage Guide

### User Commands

```bash
/start              # Start using (register)
/about              # Learn about bot features
/balance            # Check points balance
/qd                 # Daily check-in (+1 point)
/invite             # Generate invitation link (+2 points/person)
/use <card_key>     # Use card key to redeem points
/verify <link>      # Gemini One Pro verification
/verify2 <link>     # ChatGPT Teacher K12 verification
/verify3 <link>     # Spotify Student verification
/verify4 <link>     # Bolt.new Teacher verification
/verify5 <link>     # YouTube Premium Student verification
/getV4Code <id>     # Get Bolt.new authentication code
/help               # View help information
```

### Admin Commands

```bash
/addbalance <user_id> <points>      # Add points to user
/block <user_id>                    # Block user
/white <user_id>                    # Unblock user
/blacklist                          # View blacklist
/genkey <card_key> <points> [uses] [days]  # Generate card key
/listkeys                           # View card key list
/broadcast <text>                   # Broadcast message to all users
```

### Usage Flow

1. **Get Verification Link**
   - Visit the corresponding service's verification page
   - Start the verification process
   - Copy the complete URL from the browser address bar (including `verificationId`)

2. **Submit Verification Request**
   ```
   /verify3 https://services.sheerid.com/verify/xxx/?verificationId=yyy
   ```

3. **Wait for Processing**
   - Bot automatically generates identity information
   - Creates student/teacher ID images
   - Submits to SheerID platform

4. **Get Results**
   - Review usually completes within minutes
   - Returns redirect link on success

---

## 📁 Project Structure

```
tgbot-verify/
├── bot.py                  # Bot main program
├── config.py               # Global configuration
├── database_mysql.py       # MySQL database management
├── .env                    # Environment variable configuration (create manually)
├── env.example             # Environment variable template
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image build
├── docker-compose.yml      # Docker Compose configuration
├── handlers/               # Command handlers
│   ├── user_commands.py    # User commands
│   ├── admin_commands.py   # Admin commands
│   └── verify_commands.py  # Verification commands
├── one/                    # Gemini One Pro verification module
├── k12/                    # ChatGPT K12 verification module
├── spotify/                # Spotify Student verification module
├── youtube/                # YouTube Premium verification module
├── Boltnew/                # Bolt.new verification module
├── military/               # ChatGPT Military verification documentation
└── utils/                  # Utility functions
    ├── messages.py         # Message templates
    ├── concurrency.py      # Concurrency control
    └── checks.py           # Permission checks
```

---

## ⚙️ Configuration Guide

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `BOT_TOKEN` | ✅ | Telegram Bot Token | - |
| `CHANNEL_USERNAME` | ❌ | Channel username | pk_oa |
| `CHANNEL_URL` | ❌ | Channel link | https://t.me/pk_oa |
| `ADMIN_USER_ID` | ✅ | Admin Telegram ID | - |
| `MYSQL_HOST` | ✅ | MySQL host address | localhost |
| `MYSQL_PORT` | ❌ | MySQL port | 3306 |
| `MYSQL_USER` | ✅ | MySQL username | - |
| `MYSQL_PASSWORD` | ✅ | MySQL password | - |
| `MYSQL_DATABASE` | ✅ | Database name | tgbot_verify |

### Points Configuration

You can customize points rules in `config.py`:

```python
VERIFY_COST = 1        # Points consumed for verification
CHECKIN_REWARD = 1     # Points reward for check-in
INVITE_REWARD = 2      # Points reward for invitation
REGISTER_REWARD = 1    # Points reward for registration
```

---

## ⚠️ Important Notes

### 🔴 Must Read Before Using

**Before using the bot, please check and update the verification configuration for each module!**

Since SheerID's `programId` may be updated periodically, the following services **must** update the verification information in their configuration files before use:

- `one/config.py` - **Gemini One Pro** verification (need to update `PROGRAM_ID`)
- `k12/config.py` - **ChatGPT Teacher K12** verification (need to update `PROGRAM_ID`)
- `spotify/config.py` - **Spotify Student** verification (need to update `PROGRAM_ID`)
- `youtube/config.py` - **YouTube Premium Student** verification (need to update `PROGRAM_ID`)
- `Boltnew/config.py` - Bolt.new Teacher verification (recommend checking `PROGRAM_ID`)

**How to Get the Latest programId**:
1. Visit the corresponding service's verification page
2. Open browser developer tools (F12) → Network tab
3. Start the verification process
4. Find the `https://services.sheerid.com/rest/v2/verification/` request
5. Extract `programId` from the URL or request payload
6. Update the corresponding module's `config.py` file

> **Tip**: If verification keeps failing, it's likely that `programId` has expired. Please update it following the steps above.

---

## 🔗 Related Links

- 📺 **Telegram Channel**: https://t.me/pk_oa
- 🐛 **Issue Feedback**: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)
- 📖 **Deployment Documentation**: [DEPLOY.md](DEPLOY.md)

---

## 🤝 Secondary Development

Secondary development is welcome! Please follow these rules:

1. **Preserve Original Author Information**
   - Keep the original repository address in code and documentation
   - Indicate secondary development based on this project

2. **Open Source License**
   - This project uses MIT open source license
   - Secondary development projects must also be open source

3. **Commercial Use**
   - Personal use is free
   - For commercial use, please optimize and take responsibility yourself
   - No technical support or warranty provided

---

## 📜 Open Source License

This project is licensed under [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 PastKing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- Thanks to [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond for providing the legacy code base
- Thanks to all developers who contributed to this project
- Thanks to SheerID platform for providing verification services

---

## 📊 Project Statistics

[![Star History Chart](https://api.star-history.com/svg?repos=PastKing/tgbot-verify&type=Date)](https://star-history.com/#PastKing/tgbot-verify&Date)

---

## 📝 Changelog

### v2.0.0 (2025-01-12)

- ✨ Added Spotify Student and YouTube Premium Student verification (YouTube is beta, refer to youtube/HELP.MD for usage)
- 🚀 Optimized concurrency control and performance
- 📝 Improved documentation and deployment guide
- 🐛 Fixed known bugs

### v1.0.0

- 🎉 Initial release
- ✅ Support for Gemini, ChatGPT, Bolt.new verification

---

<p align="center">
  <strong>⭐ If this project helps you, please give it a Star to show your support!</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/PastKing">PastKing</a>
</p>
