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

# # Welcome embed
# @bot.command
# @lightbulb.command("welcome", "welcome embed")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def welcome(ctx: lightbulb.Context):
#     CHANNEL_ID = 1006206543240364052
    
#     member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
#     if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
#         await ctx.respond("This isn't a command you should be using. 🤦")
#         return

#     try:
#         channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
#     except hikari.NotFoundError:
#         await ctx.respond("The specified channel could not be found.")
#         return
    
#     embed = hikari.Embed(
#         title="👋 Welcome! 👋",
#         description=(
#             f"**Welcome to the official support server for Insult Bot. Feel free to go through the channels linked in the server map or for quick help go to <#1006208568837554226> and let us know of your issue.**\n\n"
#             "**Server Map:**\n\n"
#             f"<#1006206593257459785>\nRead the rules here.\n\n"
#             f"<#1006206637196988426>\nKeep an eye on announcements, bot updates and issues here.\n\n"
#             f"<#1267399130527961149>\nTake a look at the perks you receive by subscribing here.\n\n"
#             f"<#1006227022340706395>\nQuick guide to use Insult Bot here.\n\n"
#             f"<#1267399199843024928>\nRead the frequently asked questions here.\n\n"
#             f"<#1006209552557035530>\nChat with members about Insult Bot or anything off-topic here.\n\n"
#             f"<#1243873717260386325>\nSupporters exclusive channel (Invisible to normal members).\n\n"
#             f"<#1267395551352193157>\nDrop your suggesstions here.\n\n"
#             f"<#1006208568837554226>\nAsk for help here.\n\n"
#             f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
#         ),
#         color=0x2B2D31
#     )
#     embed.set_image("https://i.imgur.com/qMZebSg.png")
#     await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

# # Rules embed
# @bot.command
# @lightbulb.command("rules", "rules embed")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def rules(ctx: lightbulb.Context):
#     CHANNEL_ID = 1006206593257459785
    
#     member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
#     if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
#         await ctx.respond("This isn't a command you should be using. 🤦")
#         return

#     try:
#         channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
#     except hikari.NotFoundError:
#         await ctx.respond("The specified channel could not be found.")
#         return
    
#     embed = hikari.Embed(
#         title="📜 Rules 📜",
#         description=(
#             "**1.** Do not share any private information.\n\n"
#             "**2.** Keep things in their respective channels.\n\n"
#             "**3.** Server leeching or raiding will result in an immediate ban.\n\n"
#             "**4.** Toxic, racist, sexist, or homophobic slurs are not allowed.\n\n"
#             "**5.** Do not advertise servers, accounts, or sell servers or accounts.\n\n"
#             "**6.** Try not ghost ping staff members.\n\n"
#             "**7.** Flashing emotes are discouraged but allowed, epileptic users are expected to have reduced motion on.\n\n"
#             "**8.** Do not talk about sensitive topics like suicide and self-harm. Seek professional help.\n\n"
#             "**9.** Do not play around the rules and find out, just use your common sense and be a decent person.\n\n"
#             "**Disciplinary System:**\n"
#             "Warn in chat -> Timeout (1 day) -> Timeout (1 week) -> Kick -> Ban\n\n"
#             f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
#         ),
#         color=0x2B2D31
#     )
#     embed.set_image("https://i.imgur.com/qMZebSg.png")
#     await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

# # Premium embed
# @bot.command
# @lightbulb.command("premium", "premium embed")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def premium(ctx: lightbulb.Context):
#     CHANNEL_ID = 1267399130527961149
    
#     member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
#     if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
#         await ctx.respond("This isn't a command you should be using. 🤦")
#         return

#     try:
#         channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
#     except hikari.NotFoundError:
#         await ctx.respond("The specified channel could not be found.")
#         return
    
#     embed = hikari.Embed(
#         title="❤️ Premium Perks ❤️",
#         description=(
#             "**Access To Premium Commands Like:**\n"
#             "• Add custom insults.\n"
#             "• Insult Bot will remember your conversations.\n"
#             "• Remove cool-downs.\n\n"
#             "**Support Server Related Perks Like:**\n"
#             "• Access to behind the scenes discord channels.\n"
#             "• Have a say in the development of Insult Bot.\n"
#             "• Supporter exclusive channels.\n\n"
#             f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
#         ),
#         color=0x2B2D31
#     )
#     embed.set_image("https://i.imgur.com/qMZebSg.png")
#     await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

# # FAQ embed
# @bot.command
# @lightbulb.command("faq", "faq embed")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def faq(ctx: lightbulb.Context):
#     CHANNEL_ID = 1267399199843024928
    
#     member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
#     if not any(role.permissions & hikari.Permissions.ADMINISTRATOR for role in member.get_roles()):
#         await ctx.respond("This isn't a command you should be using. 🤦")
#         return

#     try:
#         channel = await ctx.bot.rest.fetch_channel(CHANNEL_ID)
#     except hikari.NotFoundError:
#         await ctx.respond("The specified channel could not be found.")
#         return
    
#     embed = hikari.Embed(
#         title="❓ Frequently Asked Questions ❓",
#         description=(
#             "**Why is `/customonly` command not working for me?**\n"
#             "The command requires you to have at least one custom insult and one custom trigger added to your server to function.\n\n"
#             "**Does Insult Bot have a dashboard/website?**\n"
#             "Insult Bot currently does not have a website but there are plans to develop a dedicated website in the future. The closest thing to a website right now is a [page over at top.gg](https://top.gg/bot/801431445452750879).\n\n"
#             "**Why is premium a thing?**\n"
#             "AI generation and hosting a bot costs money. Premium is a way for me to cover these costs while providing additional commands and support to users who wish to pay.\n\n"
#             f"*Feel free to ping {ctx.author.mention} if you have any questions!*"
#         ),
#         color=0x2B2D31
#     )
#     embed.set_image("https://i.imgur.com/qMZebSg.png")
#     await ctx.bot.rest.create_message(CHANNEL_ID, embed=embed)

bot.run()