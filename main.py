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
    },
    1285274806480273509: {
        "LOG_CHANNEL_ID": 1285274807180591210,
        "AUTO_ASSIGN_ROLE_ID": 1285274806500982784,
    },
}

# Presence
@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    await bot.update_presence(
        activity=hikari.Activity(
            name="over the server :)",
            type=hikari.ActivityType.WATCHING,
        )
    )

# Join message
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

# Leave message
@bot.listen(hikari.MemberDeleteEvent)
async def on_member_leave(event: hikari.MemberDeleteEvent) -> None:
    member = event.old_member
    guild_id = event.guild_id
    guild = event.get_guild()

    if guild_id not in GUILD_SETTINGS:
        print(f"Guild ID {guild_id} not found in settings")
        return

    settings = GUILD_SETTINGS[guild_id]
    log_channel_id = settings["LOG_CHANNEL_ID"]

    if member is None or guild is None:
        print(f"Member or Guild is None for member: {member}")
        return

    roles = ', '.join([role.mention for role in member.get_roles()]) if member else "Unknown"

    embed = hikari.Embed(
        title="Member Left",
        description=f"{member.mention}\nRoles: {roles}",
        color=0xe74c3c,
        timestamp=datetime.now().astimezone()
    )
    embed.set_footer(text=f"ID: {member.id}")

    try:
        await bot.rest.create_message(log_channel_id, embed=embed)
        print(f"Sent leave message for {member}")
    except Exception as e:
        print(f"Failed to send leave message for {member}: {e}")

# Welcome embed
@bot.command
@lightbulb.command("welcome", "welcome embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def welcome(ctx: lightbulb.Context):
    CHANNEL_ID = 1285274806500982790
    
    member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
    if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
        await ctx.respond("This isn't a command you should be using. 🤦")
        return

    try:
        channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
    except hikari.NotFoundError:
        await ctx.respond("The specified channel could not be found.")
        return
    
    embed = hikari.Embed(
        title="👋 Welcome! 👋",
        description=(
            f"**Welcome to the official support server for Aiko. Feel free to go through the channels linked in the server map or for quick help go to <#1285274806933131411> and let us know of your issue.**\n\n"
            "**Server Map:**\n\n"
            f"<#1285274806500982791>\nRead the rules here.\n\n"
            f"<#1304310416163213322>\nKeep an eye on announcements, bot updates and issues here.\n\n"
            f"<#1285274806500982793>\nTake a look at the perks you receive by subscribing here.\n\n"
            f"<#1285274806933131406>\nRead the frequently asked questions here.\n\n"
            f"<#1285274806933131408>\nChat with members about Aiko or anything off-topic here.\n\n"
            f"<#1285274806933131409>\nSupporters exclusive channel (Invisible to normal members).\n\n"
            f"<#1285293738368962601>\nDrop your suggestions here.\n\n"
            f"<#1285274806933131411>\nAsk for help here.\n\n"
            f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
        ),
        color=0x2B2D31
    )
    await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

# Rules embed
@bot.command
@lightbulb.command("rules", "rules embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def rules(ctx: lightbulb.Context):
    CHANNEL_ID = 1285274806500982791
    
    member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
    if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
        await ctx.respond("This isn't a command you should be using. 🤦")
        return

    try:
        channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
    except hikari.NotFoundError:
        await ctx.respond("The specified channel could not be found.")
        return
    
    embed = hikari.Embed(
        title="📜 Rules 📜",
        description=(
            "**1.** Do not share any private information.\n\n"
            "**2.** Keep things in their respective channels.\n\n"
            "**3.** Server leeching or raiding will result in an immediate ban.\n\n"
            "**4.** Toxic, racist, sexist, or homophobic slurs are not allowed.\n\n"
            "**5.** Do not advertise servers, accounts, or sell servers or accounts.\n\n"
            "**6.** Try not ghost ping staff members.\n\n"
            "**7.** Flashing emotes are discouraged but allowed, epileptic users are expected to have reduced motion on.\n\n"
            "**8.** Do not talk about sensitive topics like suicide and self-harm. Seek professional help.\n\n"
            "**9.** Do not play around the rules and find out, just use your common sense and be a decent person.\n\n"
            "**Disciplinary System:**\n"
            "Warn in chat -> Timeout (1 day) -> Timeout (1 week) -> Kick -> Ban\n\n"
            f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
        ),
        color=0x2B2D31
    )
    await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

# Premium embed
@bot.command
@lightbulb.command("premium", "premium embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def premium(ctx: lightbulb.Context):
    CHANNEL_ID = 1285274806500982793
    
    member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
    if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
        await ctx.respond("This isn't a command you should be using. 🤦")
        return

    try:
        channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
    except hikari.NotFoundError:
        await ctx.respond("The specified channel could not be found.")
        return
    
    embed = hikari.Embed(
        title="❤️ Premium Perks ❤️",
        description=(
            "**Access To Premium Commands Like:**\n"
            "• Unlimited responses from Aiko.\n"
            "• Aiko can reply in DMs.\n"
            "• Aiko will always remember your conversations.\n"
            "• Remove cool-downs.\n\n"
            "**Support Server Related Perks Like:**\n"
            "• Access to behind the scenes discord channels.\n"
            "• Have a say in the development of Aiko.\n"
            "• Supporter exclusive channels.\n\n"
            f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
        ),
        color=0x2B2D31
    )
    await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

# FAQ embed
@bot.command
@lightbulb.command("faq", "faq embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def faq(ctx: lightbulb.Context):
    CHANNEL_ID = 1285274806933131406
    
    member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
    if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
        await ctx.respond("This isn't a command you should be using. 🤦")
        return

    try:
        channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
    except hikari.NotFoundError:
        await ctx.respond("The specified channel could not be found.")
        return
    
    embed = hikari.Embed(
        title="❓ Frequently Asked Questions ❓",
        description=(
            "**Why is `/customonly` command not working for me?**\n"
            "The command requires you to have at least one custom insult and one custom trigger added to your server to function.\n\n"
            "**Does Aiko have a dashboard/website?**\n"
            "Aiko currently does not have a website but there are plans to develop a dedicated website in the future. The closest thing to a website right now is a [page over at top.gg](https://top.gg/bot/801431445452750879).\n\n"
            "**Why is premium a thing?**\n"
            "AI generation and hosting a bot costs money. Premium is a way for me to cover these costs while providing additional commands and support to users who wish to pay.\n\n"
            "**Why did I receive an `Application did not respond` message even though the bot is online?**\n"
            "These messages are usually sent when the bot is being updated or worked on by me at the same time as the command was run. If you see this message, wait a couple of minutes before trying again.\n\n"
            f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
        ),
        color=0x2B2D31
    )
    # embed.set_image("https://i.imgur.com/qMZebSg.png")
    await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

bot.run()