#   ___   ___                                                                                          
#      / /    /|    //| |     /|    //| |     //   ) ) //   ) ) /__  ___/ // | |     / /        / /    
#     / /    //|   // | |    //|   // | |    //   / / //___/ /    / /    //__| |    / /        / /     
#    / /    // |  //  | |   // |  //  | |   //   / / / ___ (     / /    / ___  |   / /        / /      
#   / /    //  | //   | |  //  | //   | |  //   / / //   | |    / /    //    | |  / /        / /       
#__/ /___ //   |//    | | //   |//    | | ((___/ / //    | |   / /    //     | | / /____/ / / /____/ / 
                                         



import discord, os, keep_alive
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import discord
import time
import typing
from discord_slash import SlashCommand, SlashContext, cog_ext
from datetime import datetime, timedelta
from discord import VoiceChannel
from datetime import timedelta

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)
guild_id = YOUR_CHANNEL_ID

async def remove_role_after_delay(member, role, delay):
    await asyncio.sleep(delay)
    await member.remove_roles(role)

@bot.slash_command(name="punish", description="Punish A Member From The Server Using ⌥ 𝚀𝚄𝙰𝚁𝙰𝙽𝚃𝙸𝙽𝙴🔒")
@commands.has_permissions(manage_roles=True)
async def punish(ctx, member: discord.Member, duration: typing.Optional[int] = None):
    role_name = "⌥ 𝚀𝚄𝙰𝚁𝙰𝙽𝚃𝙸𝙽𝙴🔒"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        return await ctx.respond(f"Error: {role_name} Role Not Found, Please Make A role with the name ⌥ 𝚀𝚄𝙰𝚁𝙰𝙽𝚃𝙸𝙽𝙴🔒")
    if duration and not isinstance(duration, int):
        return await ctx.respond("Error: The Time Should Be A Numebr.")
    try:
        await member.add_roles(role)
        await ctx.respond(f" Member {member.mention} Punished For {duration} Minutes.")
        if duration:
            delay_seconds = duration * 60
            bot.loop.create_task(remove_role_after_delay(member, role, delay_seconds))
    except discord.Forbidden:
        await ctx.respond("The Target Role Is Higher Than Me.")
      
    except commands.MissingPermissions as e:
        missing_perms = [perm.replace('_', ' ').title() for perm in e.missing_perms]
        return await ctx.respond(f"You are missing {missing_perms} permission(s) to run this command.")   





@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="⟮  𝐈 𝐌 𝐌 𝐎 𝐑 𝐓 𝐀 𝐋  ⟯  𝐅𝐚𝐦𝐢𝐥𝐲"))
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(YOUR_CHANNEL_ID) # Replace with the ID of the channel you want to send the embed to
    embed = discord.Embed(title="IMMORTAL HAS BEEN STARTED 🟢", color=0x00ff00)
    embed.add_field(name="Reason", value="Cycle", inline=False)
    embed.add_field(name="Date", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Tags", value="<@ROLE_ID_TO_MENTION>", inline=False)
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png", text="IMMORTAL")
    await channel.send(embed=embed)
    channel_id = YOUR_CHANNEL_ID
    channel = bot.get_channel(channel_id)
    if channel is not None and isinstance(channel, discord.VoiceChannel):
        await channel.connect()

@bot.event
async def on_member_update(previous, current):
    quarantine_role_id = YOUR_QUARANTINE_ROLE_ID
    if quarantine_role_id not in [role.id for role in previous.roles] and quarantine_role_id in [role.id for role in current.roles]:
        channel_id = YOUR_CHANNEL_ID
        channel = bot.get_channel(channel_id)
        user_tag = f"{current.mention}"
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tags = "<@&ROLE_ID_TO_MENTION>"
        embed = discord.Embed(title="Member Punished 🔒", color=discord.Color.red())
        embed.add_field(name="Member", value=user_tag, inline=False)
        embed.add_field(name="Date", value=date, inline=False)
        embed.add_field(name="Tags", value=tags, inline=False)
        embed.set_footer(text="IMMORTAL", icon_url="https://cdn.discordapp.com/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png")
        await channel.send(embed=embed)
    elif quarantine_role_id in [role.id for role in previous.roles] and quarantine_role_id not in [role.id for role in current.roles]:
        channel_id = YOUR_CHANNEL_ID
        channel = bot.get_channel(channel_id)
        user_tag = f"{current.mention}"
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tags = "<@&ROLE_ID_TO_MENTION>"
        embed = discord.Embed(title="Member UnPunished 🔓", color=discord.Color.green())
        embed.add_field(name="Member", value=user_tag, inline=False)
        embed.add_field(name="Date", value=date, inline=False)
        embed.add_field(name="Tags", value=tags, inline=False)
        embed.set_footer(text="IMMORTAL", icon_url="https://cdn.discordapp.com/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member:
            reason = entry.reason or "N/A"
            
            channel = bot.get_channel(YOUR_CHANNEL_ID) # replace with your channel id
          
            embed = discord.Embed(title="Member Kicked", color=discord.Color.red())
            
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Dalil", value=reason)
            embed.add_field(name="Tavasot", value=entry.user.mention, inline=False)
            embed.add_field(name="Member", value=member.mention, inline=False)
            embed.add_field(name="Date", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            embed.add_field(name="Tags", value='<@&ROLE_ID_TO_MENTION>', inline=False)
            embed.set_footer(text="IMMORTAL", icon_url="https://cdn.discordapp.com/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png")
            
            await channel.send(embed=embed)



@bot.event
async def on_member_ban(guild, user):
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        if entry.target == user:
            
            reason = entry.reason or "N/A"
            
            channel = bot.get_channel(YOUR_CHANNEL_ID) # replace with your channel id
         
            embed = discord.Embed(title="Member Banned", color=discord.Color.red())
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Dalil", value=reason)
            embed.add_field(name="Tavasot", value=entry.user.mention)
            embed.add_field(name="Member", value=user.mention)
            embed.add_field(name="Date", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            embed.add_field(name="Tags", value='<@&ROLE_ID_TO_MENTION>', inline=False)
            embed.set_footer(text="IMMORTAL", icon_url="https://cdn.discordapp.com/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png")
            
            await channel.send(embed=embed)

@bot.event
async def on_member_unban(guild, user):
    
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
        if entry.target == user:
            reason = entry.reason or "N/A"
            
            channel = bot.get_channel(YOUR_CHANNEL_ID) # replace with your channel id
            
            embed = discord.Embed(title="Member Unbanned", color=discord.Color.green())
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Author", value=entry.user.mention)
            embed.add_field(name="Member", value=user.mention)
            embed.add_field(name="Date", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            embed.add_field(name="Tags", value='<@&ROLE_ID_TO_MENTION>', inline=False)
            embed.set_footer(text="IMMORTAL", icon_url="https://cdn.discordapp.com/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png")
            
            await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    embed = discord.Embed(title="Yek Member Jadid Join Shod!", color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    total_members = len(member.guild.members)
    embed.add_field(name=f"{total_members}th Member Has Joined us🥰", value=f"Member: {member.mention}\nDate: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}", inline=False)
    embed.set_footer(icon_url="https://media.discordapp.net/attachments/1079436774184591512/1082019888991830016/177D0EDA-8EF7-45E4-8151-6A0ED39A71DE.png", text="IMORTAL")
    await channel.send(embed=embed)

@bot.event
async def on_member_join(member):

    await member.edit(nick="'ঌ " + member.name + " ∾ ɪᴍᴍᴏʀᴛᴀʟ")

  
keep_alive.keep_alive()
print("""
      Developed By ARSAM#4141
     https://github.com/tllnll
      
___________.__  .__         .__  .__   
\__    ___/|  | |  |   ____ |  | |  |  
  |    |   |  | |  |  /    \|  | |  |  
  |    |   |  |_|  |_|   |  \  |_|  |__
  |____|   |____/____/___|  /____/____/
                          \/         
""")
bot.run(os.getenv("TOKEN"))

