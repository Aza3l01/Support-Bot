import hikari
import lightbulb
import os
from datetime import datetime

bot = lightbulb.BotApp(
    token=os.getenv('DISCORD_BOT_TOKEN'),
    intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_MEMBERS
)

LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))
AUTO_ASSIGN_ROLE_ID = int(os.getenv('AUTO_ASSIGN_ROLE_ID'))

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
    guild = event.get_guild()
        
    join_position = len(guild.get_members())
    
    try:
        await member.add_role(AUTO_ASSIGN_ROLE_ID)
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
        await bot.rest.create_message(LOG_CHANNEL_ID, embed=embed)
        print(f"Sent join message for {member}")
    except Exception as e:
        print(f"Failed to send join message for {member}: {e}")

# Leave message
@bot.listen(hikari.MemberDeleteEvent)
async def on_member_leave(event: hikari.MemberDeleteEvent) -> None:
    member = event.old_member
    guild = event.get_guild()
    
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
        await bot.rest.create_message(LOG_CHANNEL_ID, embed=embed)
        print(f"Sent leave message for {member}")
    except Exception as e:
        print(f"Failed to send leave message for {member}: {e}")

# Embed
@bot.command
@lightbulb.command("premium", "premium embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def premium(ctx: lightbulb.Context):
    CHANNEL_ID = 1267399130527961149
    
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
            "• Add insults/triggers.\n"
            "• Insult Bot will remember your conversations.\n"
            "• Customize AI Chatbot style.\n"
            "• Remove cool-downs.\n\n"
            "**Support Server Related Perks Like:**\n"
            "• Access to behind the scenes discord channels.\n"
            "• Have a say in the development of Insult Bot.\n"
            "• Supporter exclusive channels.\n\n"
            f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
        ),
        color=0x2B2D31
    )
    embed.set_image("https://i.imgur.com/qMZebSg.png")
    await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

bot.run()