# bot.py

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands.wallet_commands import WalletCommands
from commands.airtime_commands import AirtimeCommands

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
LNBITS_URL = os.getenv('LNBITS_URL')
LNBITS_ADMIN_KEY = os.getenv('LNBITS_ADMIN_KEY')
FLUTTERWAVE_API_KEY = os.getenv('FLUTTERWAVE_API_KEY')
MAVAPAY_API_KEY = os.getenv('MAVAPAY_API_KEY')

# Setup logging
import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

# Bot initialization
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'{bot.user.name} has connected to Discord!')

# Add commands
bot.add_cog(WalletCommands(bot, LNBITS_URL, LNBITS_ADMIN_KEY))
bot.add_cog(AirtimeCommands(bot, LNBITS_URL, LNBITS_ADMIN_KEY, FLUTTERWAVE_API_KEY))

@bot.command(name='help')
async def help_command(ctx):
    """Display available commands"""
    help_text = """
⚡ **ZapBot Commands** ⚡

🔹 **!start** - Create your Lightning wallet
🔹 **!balance** - Check your wallet balance
🔹 **!zap @user amount** - Send sats to another user
🔹 **!invoice amount** - Generate a Lightning invoice to receive sats
🔹 **!buy_airtime amount_ngn phone_number** - Buy MTN airtime
🔹 **!transactions** - View your recent transactions
🔹 **!help** - Display this help message
"""
    await ctx.send(help_text)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)