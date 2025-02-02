import hikari
import lightbulb
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
bot = lightbulb.BotApp(
    token=os.getenv("BOT_TOKEN"),
    intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_MEMBERS
)

GUILD_SETTINGS = {
    1006195077409951864: {
        "LOG_CHANNEL_ID": 1268882823574454364,
        "AUTO_ASSIGN_ROLE_ID": 1006199315410190397,
        "WELCOME_CHANNEL_ID": 1006209552557035530,
    },
    1285274806480273509: {
        "LOG_CHANNEL_ID": 1285274807180591210,
        "AUTO_ASSIGN_ROLE_ID": 1285274806500982784,
        "WELCOME_CHANNEL_ID": 1285274806933131408,
    },
}

@bot.listen(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    member = event.member
    guild_id = event.guild_id
    guild = event.get_guild()

    if guild_id not in GUILD_SETTINGS:
        print(f"Guild ID {guild_id} not found in settings")
        return

    settings = GUILD_SETTINGS[guild_id]
    log_channel_id = settings["LOG_CHANNEL_ID"]
    auto_assign_role_id = settings["AUTO_ASSIGN_ROLE_ID"]
    welcome_channel_id = settings["WELCOME_CHANNEL_ID"]

    join_position = len(guild.get_members())

    try:
        await member.add_role(auto_assign_role_id)
        print(f"Assigned role to {member}")
    except Exception as e:
        print(f"Failed to assign role to {member}: {e}")

    embed = hikari.Embed(
        title="Member Joined",
        description=f"{member.mention} | Members: {join_position}",
        color=0x1abc9c,
        timestamp=datetime.now().astimezone()
    )
    embed.set_footer(text=f"ID: {member.id}")

    try:
        await bot.rest.create_message(log_channel_id, embed=embed)
        print(f"Sent join message for {member}")
    except Exception as e:
        print(f"Failed to send join message for {member}: {e}")
    
    try:
        await bot.rest.create_message(welcome_channel_id, content=f"Hey <@{member.id}>, welcome! Feel free to ping our developer <@364400063281102852> if you need any help. And don't worry if the server seems dead, that's usually how support servers for small bots are.")
        print(f"Sent welcome message for {member} in {welcome_channel_id}")
    except Exception as e:
        print(f"Failed to send welcome message for {member}: {e}")

@bot.listen(hikari.MemberDeleteEvent)
async def on_member_leave(event: hikari.MemberDeleteEvent) -> None:
    guild_id = event.guild_id
    member = event.old_member

    if guild_id not in GUILD_SETTINGS:
        print(f"Guild ID {guild_id} not found in settings")
        return

    settings = GUILD_SETTINGS[guild_id]
    log_channel_id = settings["LOG_CHANNEL_ID"]

    embed = hikari.Embed(
        title="Member Left",
        description=f"{member.mention} has left the server.",
        color=0xe74c3c,
        timestamp=datetime.now().astimezone()
    )
    embed.set_footer(text=f"ID: {member.id}")

    try:
        await bot.rest.create_message(log_channel_id, embed=embed)
        print(f"Sent leave message for {member}")
    except Exception as e:
        print(f"Failed to send leave message for {member}: {e}")

bot.run()