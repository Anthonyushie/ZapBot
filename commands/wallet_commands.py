import discord
from discord.ext import commands
from extensions.lnbit import LNBitsAPI
from typing import Optional
import os

class WalletCommands(commands.Cog):
    def __init__(self, bot, lnbits_url, lnbits_admin_key):
        self.bot = bot
        self.lnbits_api = LNBitsAPI(lnbits_url, lnbits_admin_key)
    
    @commands.command(name='start')
    async def start(self, ctx):
        """Register a new LNBits wallet for the user"""
        user_id = str(ctx.author.id)
        user_name = ctx.author.name
        
        # Create a new wallet
        wallet_data = self.lnbits_api.create_wallet(user_name)
        if not wallet_data:
            await ctx.send("❌ Error creating wallet. Please try again later.")
            return
        
        await ctx.send(f"🎉 Welcome {ctx.author.mention}! Your wallet is now set up. Use !balance to check your sats.")
    
    @commands.command(name='balance')
    async def balance(self, ctx):
        """Check wallet balance"""
        user_id = str(ctx.author.id)
        
        # Get wallet balance
        balance_data = self.lnbits_api.get_wallet_balance(user_id)
        if not balance_data:
            await ctx.send("❌ Error retrieving balance. Please try again later.")
            return
        
        balance_sats = balance_data['balance'] / 1000  # LNBits uses msat internally
        
        await ctx.send(f"💰 Your current balance is {balance_sats:.0f} sats.")
    
    @commands.command(name='zap')
    async def zap(self, ctx, recipient: discord.Member, amount: int):
        """Send sats to another user"""
        sender_id = str(ctx.author.id)
        recipient_id = str(recipient.id)
        
        # Check if amount is valid
        if amount <= 0:
            await ctx.send("❌ Amount must be greater than 0.")
            return
        
        # Perform the transfer
        memo = f"Zap from {ctx.author.name} to {recipient.name}"
        payment = self.lnbits_api.internal_transfer(sender_id, recipient_id, amount, memo)
        
        if not payment:
            await ctx.send("❌ Error sending payment. Please try again later.")
            return
        
        await ctx.send(f"⚡ You zapped {recipient.mention} {amount} sats!")
    
    @commands.command(name='invoice')
    async def invoice(self, ctx, amount: int):
        """Generate a Lightning invoice to receive sats"""
        user_id = str(ctx.author.id)
        
        # Check if amount is valid
        if amount <= 0:
            await ctx.send("❌ Amount must be greater than 0.")
            return
        
        # Create invoice
        memo = f"Payment to {ctx.author.name} on Discord"
        invoice_data = self.lnbits_api.create_invoice(user_id, amount, memo)
        
        if not invoice_data:
            await ctx.send("❌ Error creating invoice. Please try again later.")
            return
        
        payment_request = invoice_data['payment_request']
        
        await ctx.send(f"⚡ Send {amount} sats to this invoice:\n```{payment_request}```")
    
    @commands.command(name='transactions')
    async def transactions(self, ctx):
        """View recent transactions"""
        user_id = str(ctx.author.id)
        
        # Get transactions
        transactions_data = self.lnbits_api.get_transactions(user_id, 5)
        if not transactions_data:
            await ctx.send("❌ Error retrieving transactions or no transactions found.")
            return
        
        # Format transactions
        transaction_list = []
        for tx in transactions_data:
            amount = tx['amount'] / 1000  # Convert msats to sats
            
            if tx['pending']:
                status = "⏳ Pending"
            else:
                status = "✅ Completed"
            
            memo = tx['memo'] if tx['memo'] else "No description"
            
            if tx['out']:
                transaction_list.append(f"- Sent {amount:.0f} sats • {memo} • {status}")
            else:
                transaction_list.append(f"- Received {amount:.0f} sats • {memo} • {status}")
        
        if not transaction_list:
            await ctx.send("📜 No transactions found.")
            return
        
        transactions_message = "📜 Last 5 Transactions:\n" + "\n".join(transaction_list)
        await ctx.send(transactions_message)
