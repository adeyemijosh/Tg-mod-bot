# Telegram moderator bot
Telegram Mod Bot
This project is a Telegram moderation bot designed to automate tasks in crypto project group chat. It helps with managing user activities, enforcing rules, and ensuring a smooth chat experience. Built using the Telegram Bot API and a python programming language, the bot is highly customizable and extensible, i welcome further customizing of the bot.

# Features
Automated Moderation

Delete messages with forbidden words.
Remove spam or flood messages.
Enforce group rules automatically.
User Management

Kick, mute, or ban users.
Warn users for violations.
Handle join/leave announcements.
Utility Commands

Provide group statistics.
Enable/disable moderation features.
Custom commands for group management.

# Tech Stack
Programming Language: Python/Node.js 
Python: python-telegram-bot
Node.js: telegraf

# Setup Instructions
Prerequisites
Telegram Bot Token: Obtain a bot token from BotFather.
Python/Node.js Installed
Installation

# Commands
Admin Commands
/warn <user>: Warn a user.
/kick <user>: Kick a user from the group.
/ban <user>: Ban a user permanently.
/mute <user>: Mute a user temporarily.

# Utility Commands
/rules: Display group rules.
/stats: Show group activity statistics.
/help: Display help and available commands.

# Testing
Test basic moderation features:

Used forbidden words and ensured they were deleted.
Simulated spam and checked if the bot acted accordingly.

# Test user commands:
Issue warnings, kicks, and bans to validate functionality.
Test group announcements:

Add/remove users and observe how the bot responds.
Customizing the Bot
Add New Commands:
Modify the main.py

# Example Usage
Delete Spam:
A user sends a repeated message. The bot detects spam and deletes the messages, warning the user.

Kick for Violations:
A user violates group rules after multiple warnings. The bot automatically kicks the user.

Statistics:
An admin uses /stats to see group activity, including the number of active users and message counts.
Contact
For questions or contributions:

# Contacts
X(twitter): https://x.com/iam_Joshberry
Email:adeyemijoshua360@gmail.com
