import discord
import aiohttp
import json
from discord.ext import commands
from extensions.lnbit import pay_invoice

class AirtimeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_sats_to_ngn_rate(self):
        """Fetch the current sats-to-NGN conversion rate from Mavapay API"""
        url = "https://api.mavapay.co/api/v1/price?currency=ngn"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["data"]["unitPricePerSat"]["amount"]
                else:
                    return None  # Handle error if API is down

    @commands.command(name="buy_airtime")
    async def buy_airtime(self, ctx, phone: str, sats: int):
        """Buy airtime using sats"""
        user_id = str(ctx.author.id)

        # Get conversion rate
        rate = await self.get_sats_to_ngn_rate()
        if rate is None:
            await ctx.send("❌ Error fetching conversion rate. Try again later.")
            return

        # Convert sats to NGN
        naira_value = sats * rate

        # Ensure user has enough balance
        from commands.wallet_commands import WalletCommands
        balance = await WalletCommands.get_balance(user_id)

        if balance < sats:
            await ctx.send("❌ Not enough balance to complete this transaction.")
            return

        # Deduct sats from LNBits
        invoice = pay_invoice(sats)
        if not invoice:
            await ctx.send("❌ Error processing payment.")
            return

        # Process airtime purchase (mock function)
        success = self.buy_airtime_api(phone, int(naira_value))
        if success:
            await ctx.send(f"✅ Successfully bought ₦{int(naira_value)} airtime for {phone}!")
        else:
            await ctx.send("❌ Failed to process airtime purchase.")

    def buy_airtime_api(self, phone, amount):
        """Mock function to call actual airtime provider API"""
        return True  # Replace with actual API integration

async def setup(bot):
    await bot.add_cog(AirtimeCommands(bot))
