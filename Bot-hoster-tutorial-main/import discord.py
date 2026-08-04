import discord
from discord.ext import commands
import asyncio
import random

# ---------- CONFIG ----------
TRIGGER = ""                # Trigger command to start batch ban
MEMBER_IDS = []             # Optional: list of specific member IDs to ban
IGNORED_IDS = []            # List of member IDs to skip
BAN_ALL = True              # True = ban multiple members
AMOUNT = 5                  # Total members to ban (ignored if MEMBER_IDS is set)
BATCH_AMOUNT = 2            # Members per batch
BATCH_SPEED = 1.0           # Delay (seconds) between individual bans
BATCH_DELAY = 3.0           # Delay (seconds) between batches
GUILD_ID = 1534200849507553360  # Your server ID
# ----------------------------

# ---- Intents ----
intents = discord.Intents.default()
intents.guilds = True
intents.members = True          # needed to access members
intents.messages = True         # required to read messages
intents.message_content = True  # REQUIRED for triggers

bot = commands.Bot(command_prefix="", intents=intents)

# ---- Core batch ban logic ----
async def run_batch_ban(guild):
    # Ban specific members by ID
    if MEMBER_IDS:
        for member_id in MEMBER_IDS:
            if member_id in IGNORED_IDS:
                print(f"Skipping ignored member ID {member_id}")
                continue
            member = guild.get_member(member_id)
            if member:
                try:
                    await member.ban(reason="Selected ban")
                    print(f"Banned {member.name}")
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Failed to ban {member.name}: {e}")
                await asyncio.sleep(BATCH_SPEED)
        return

    # Ban multiple members (BAN_ALL)
    if BAN_ALL:
        members = [
            m for m in guild.members
            if not m.bot and m.id not in IGNORED_IDS and m != bot.user
        ]
        total_to_ban = min(AMOUNT, len(members)) if AMOUNT else len(members)
        to_ban = random.sample(members, total_to_ban)

        for i in range(0, len(to_ban), BATCH_AMOUNT):
            batch = to_ban[i:i+BATCH_AMOUNT]

            for member in batch:
                try:
                    await member.ban(reason="Batch ban")
                    print(f"Banned {member.name}")
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Failed to ban {member.name}: {e}")
                await asyncio.sleep(BATCH_SPEED)

            await asyncio.sleep(BATCH_DELAY)

# ---- Trigger handling ----
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().strip() != TRIGGER.lower():
        return

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Guild not found")
        return

    await run_batch_ban(guild)

bot.run("MTUzNDE5OTIxMjkzMjIwNjY4Mw.G1sg6B.upQAY8oOukI5evT8Xnhyw-b9-sQK8C3__3lI10")