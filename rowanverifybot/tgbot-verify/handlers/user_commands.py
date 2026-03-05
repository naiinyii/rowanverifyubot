"""User Command Handler"""
import logging
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command
from utils.messages import (
    get_welcome_message,
    get_about_message,
    get_help_message,
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /start command"""
    if await reject_group_command(update):
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    full_name = user.full_name or ""

    # If already initialized, return directly
    if db.user_exists(user_id):
        await update.message.reply_text(
            f"Welcome back, {full_name}!\n"
            "You have already been initialized.\n"
            "Send /help to see available commands."
        )
        return

    # Handle invitation
    invited_by: Optional[int] = None
    if context.args:
        try:
            invited_by = int(context.args[0])
            if not db.user_exists(invited_by):
                invited_by = None
        except Exception:
            invited_by = None

    # Create user
    if db.create_user(user_id, username, full_name, invited_by):
        welcome_msg = get_welcome_message(full_name, bool(invited_by))
        await update.message.reply_text(welcome_msg)
    else:
        await update.message.reply_text("Registration failed, please try again later.")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /about command"""
    if await reject_group_command(update):
        return

    await update.message.reply_text(get_about_message())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /help command"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    is_admin = user_id == ADMIN_USER_ID
    await update.message.reply_text(get_help_message(is_admin))


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /balance command"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You have been blocked and cannot use this feature.")
        return

    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("Please register first using /start.")
        return

    await update.message.reply_text(
        f"💰 Points Balance\n\nCurrent Points: {user['balance']} points"
    )


async def checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /qd check-in command - temporarily disabled"""
    user_id = update.effective_user.id

    # Check-in feature temporarily disabled (bug fix in progress)
    # await update.message.reply_text(
    #     "⚠️ Check-in feature is temporarily under maintenance\n\n"
    #     "Due to a bug, the check-in feature is temporarily closed for fixing.\n"
    #     "Expected to resume soon, sorry for the inconvenience.\n\n"
    #     "💡 You can earn points in the following ways:\n"
    #     "• Invite friends /invite (+2 points)\n"
    #     "• Use card key /use <card_key>"
    # )
    # return
    
    # ===== Code below is disabled =====
    if db.is_user_blocked(user_id):
        await update.message.reply_text("You have been blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
        return

    # Layer 1 check: at command handler level
    if not db.can_checkin(user_id):
        await update.message.reply_text("❌ You have already checked in today, come back tomorrow.")
        return

    # Layer 2 check: at database level (SQL atomic operation)
    if db.checkin(user_id):
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"✅ Check-in successful!\nPoints earned: +1\nCurrent Points: {user['balance']} points"
        )
    else:
        # If database layer returns False, it means already checked in today (double insurance)
        await update.message.reply_text("❌ You have already checked in today, come back tomorrow.")


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /invite command"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You have been blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
        return

    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🎁 Your exclusive invitation link:\n{invite_link}\n\n"
        "For every 1 person you successfully invite, you will earn 2 points."
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /use command - use card key"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You have been blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /use <card_key>\n\nExample: /use wandouyu"
        )
        return

    key_code = context.args[0].strip()
    result = db.use_card_key(key_code, user_id)

    if result is None:
        await update.message.reply_text("Card key does not exist, please check and try again.")
    elif result == -1:
        await update.message.reply_text("This card key has reached its usage limit.")
    elif result == -2:
        await update.message.reply_text("This card key has expired.")
    elif result == -3:
        await update.message.reply_text("You have already used this card key.")
    else:
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"Card key used successfully!\nPoints earned: {result}\nCurrent Points: {user['balance']}"
        )
