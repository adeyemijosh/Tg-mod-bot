from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import API_TOKEN
import asyncio
import time
import re
from collections import defaultdict

# List of forbidden words (case-insensitive)
FORBIDDEN_WORDS = ["fud", "scam", "farm", "check dm", "fuck", "scam dev", "fudding", "nuke", "rug", "ponzi", "fraud", "exit scam", "dump", "red flag", ""]

# Regular expression pattern to identify external Telegram links
TELEGRAM_LINK_PATTERN = re.compile(r'https?://(?:t\.me|telegram\.me)/[\w-]+')

# Tracking the message IDs and timestamps of pictures sent by users
user_photo_messages = defaultdict(list)
# Time window for detecting spam (in seconds)
SPAM_TIME_WINDOW = 7
# Maximum number of pictures allowed in the time window
MAX_PICTURES = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! I am your bot. Use /help to see available commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "/start - Start the bot\n"
        "/help - Get help on how to use the bot\n"
        "/contacts - Get contact information"
    )
    await update.message.reply_text(help_text)

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact_text = (
        "For any inquiries, contact us at:\n"
        "Email: example@example.com\n"
        "Phone: +123456789"
    )
    await update.message.reply_text(contact_text)

async def is_user_admin(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        chat_administrators = await context.bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in chat_administrators)
    except Exception as e:
        print(f"Failed to check admin status: {e}")
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    current_time = time.time()

    # Skip actions if the user is an admin
    if await is_user_admin(chat_id, user_id, context):
        return

    if message.text:
        message_text_lower = message.text.lower()

        # Check for forbidden words
        if any(word in message_text_lower for word in FORBIDDEN_WORDS):
            try:
                # Send a warning message
                warning_message = await message.reply_text(
                    "You have been muted for using forbidden words."
                )

                # Restrict the user for 1 hour
                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions={
                        'can_send_messages': False,
                        'can_send_media_messages': False,
                        'can_send_polls': False,
                        'can_send_other_messages': False,
                        'can_add_web_page_previews': False,
                    },
                    until_date=int(time.time()) + 60  # Mute for 1 hour
                )

                # Delete the forbidden message sent by the user
                await message.delete()

                # Wait for 0.5 seconds before deleting the warning message
                await asyncio.sleep(0.5)
                await context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=warning_message.message_id
                )

            except Exception as e:
                print(f"Failed to mute/kick user or delete messages: {e}")

        # Check for external Telegram links
        elif TELEGRAM_LINK_PATTERN.search(message.text):
            try:
                print(f"Deleting message with external Telegram link: {message.text}")
                await message.delete()
            except Exception as e:
                print(f"Failed to delete message with external Telegram link: {e}")

    elif message.photo:
        # Store the message ID and timestamp
        user_photo_messages[user_id].append((message.message_id, current_time))

        # Check if the user has exceeded the photo limit
        if len(user_photo_messages[user_id]) > MAX_PICTURES:
            try:
                print(f"Deleting all photos from user {user_id} due to spam")

                # Send a warning message if not an admin
                warning_message = None
                if not await is_user_admin(chat_id, user_id, context):
                    warning_message = await message.reply_text(
                        "You have been muted for spamming photos."
                    )

                # Restrict the user for 1 hour
                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions={
                        'can_send_messages': False,
                        'can_send_media_messages': False,
                        'can_send_polls': False,
                        'can_send_other_messages': False,
                        'can_add_web_page_previews': False,
                    },
                    until_date=int(time.time()) + 60  # Mute for 1 hour
                )

                # Delete all photos sent by the user
                for msg_id, _ in user_photo_messages[user_id]:
                    retry_count = 0
                    while retry_count < 3:  # Retry up to 3 times
                        try:
                            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                            break
                        except Exception as e:
                            print(f"Failed to delete photo message {msg_id}: {e}")
                            retry_count += 1
                            await asyncio.sleep(1)  # Wait before retrying

                # Clear the stored photo messages
                user_photo_messages[user_id] = []

                # Wait for 0.5 seconds before deleting the warning message if not an admin
                if warning_message:
                    await asyncio.sleep(0.5)
                    await context.bot.delete_message(
                        chat_id=chat_id,
                        message_id=warning_message.message_id
                    )

            except Exception as e:
                print(f"Failed to delete photos or mute user: {e}")

def main() -> None:
    # Create Application object and pass it your bot's token
    application = Application.builder().token(API_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contacts", contacts))

    # Register message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
