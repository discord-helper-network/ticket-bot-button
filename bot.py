import asyncio
import datetime
import discord
from discord.ext import commands
import json
import io
from discord_components import *
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import *

intents = discord.Intents().default()
intents.members = True


intents = discord.Intents().default()
intents.members = True
with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    guildid = data["GUILDID"]
    erole = data["EROLE"]
    tcategory = data["TCATEGORY"]
    acategory = data["ACATEGORY"]

bot = commands.Bot(intents=intents,command_prefix='!')
slash=SlashCommand(bot, sync_commands=True)
DiscordComponents(bot)


@bot.event
async def on_ready():

    print('██████╗ ███████╗ █████╗ ██████╗ ██╗   ██╗')
    print('██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝')
    print('██████╔╝█████╗  ███████║██║  ██║ ╚████╔╝ ')
    print('██╔══██╗██╔══╝  ██╔══██║██║  ██║  ╚██╔╝  ')
    print('██║  ██║███████╗██║  ██║██████╔╝   ██║   ')
    print('╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝   ')


    bot.loop.create_task(status_task())


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('created by Discord Helper Network'),
                                     status=discord.Status.online)
        await asyncio.sleep(10)
        #await client.change_presence(activity=discord.Game('/help'), status=discord.Status.online)
        #await asyncio.sleep(10)


global guild
guild = bot.get_guild(guildid) #GUILDID here




@bot.command()
async def ticket(ctx):
    embed=discord.Embed(title="Support Ticket", description="Du brauchst Support? Dann zöger nicht lange, und eröffne ein Ticket!", color=0x2f3136)
    buttons = [
        create_button(style=ButtonStyle.green, label="Ticket öffnen")
    ]
    action_row = create_actionrow(*buttons)
    await ctx.send(embed=embed, components=[action_row])

    await ctx.message.delete()


@bot.event
async def on_interaction(interaction):
    print("triggered")
    messageticketalert = await interaction.send(content=f"Ticket wird erstellt. Bitte warten...")

    user = interaction.author
    if interaction.component.label == "Ticket öffnen":

        suprole = discord.utils.get(user.guild.roles, name=erole)  # NAME FROM TEAMROLE HERE
        category = discord.utils.get(user.guild.categories, name=tcategory)  # ticketcategory name here

        role = discord.utils.get(user.guild.roles, name="@everyone")
        chan = await user.guild.create_text_channel(name=f'support ticket - {user}',
                                                    category=category)
        await chan.set_permissions(role, send_messages=False, read_messages=False, add_reactions=False,
                                   embed_links=False, attach_files=False, read_message_history=False,
                                   external_emojis=False)
        await chan.set_permissions(suprole, send_messages=True, read_messages=True, add_reactions=True,
                                   embed_links=True,
                                   attach_files=True, read_message_history=True, external_emojis=True)
        await chan.set_permissions(user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True,
                                   attach_files=True, read_message_history=True, external_emojis=True)
        embed = discord.Embed(
            title=f"Support Ticket",
            description=f"Hey {user.name}, \r\n"
                        f"Beschreibe bitte hier dein Anliegen. Das nächste freie Teammitglied wird sich um dich kümmern.",
            color=0x2f3136
        )

        msg = await chan.send(f'{user.mention}', embed=embed)



@bot.command()
@commands.has_permissions(manage_channels=True)
async def close(ctx, channel: discord.TextChannel):
    archivcategory = discord.utils.get(ctx.guild.categories, name=acategory)  # archivcategory name here

    if channel == ctx.channel:
        await ctx.channel.edit(name=f":archiv-{ctx.channel.name}", category=archivcategory)
        await ctx.send('Das Ticket wurde Archiviert.')




    else:
        await ctx.send("Bitte gebe den richtigen Channel zur Sicherheitsabfrage an")


bot.run(token)




