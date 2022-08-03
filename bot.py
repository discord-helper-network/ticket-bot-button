##Please do not change anything here. All things come into the config.json!
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

#Please do not change anything here. All things come into the config.json

intents = discord.Intents().default()
intents.members = True
with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    guildid = data["GUILDID"]
    erole = data["EROLE"]
    tcategory = data["TCATEGORY"]
    acategory = data["ACATEGORY"]
    
#Please do not change anything here. All things come into the config.json

bot = commands.Bot(intents=intents,command_prefix='!')
slash=SlashCommand(bot, sync_commands=True)
DiscordComponents(bot)
#Do not change anything!
#Do not change anything!
#Do not change anything!

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
guild = bot.get_guild(guildid) ##Please do not change anything here. All things come into the config.json




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

        suprole = discord.utils.get(user.guild.roles, name=erole) #Please do not change anything here. All things come into the config.json
        category = discord.utils.get(user.guild.categories, name=tcategory)  #Please do not change anything here. All things come into the config.json

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
async def close(ctx, channel: discord.TextChannel=None):
    archivcategory = discord.utils.get(ctx.guild.categories, name='archiv')  # archivcategory name here
    if channel == None:
        await ctx.send("Bitte gebe den Channel zur Sicherheitsabfrage an.")
        return
    if "ticket" in ctx.channel.name:
        if channel == ctx.channel:
            await ctx.channel.edit(name=f":archiv-{ctx.channel.name}", category=archivcategory)
            await ctx.send('Das Ticket wurde Archiviert.')
    
        else:
            await ctx.send("Bitte sende den Korrekten Channel zur Sicherheitsabfrage.")
    else:
        await ctx.send("Das hier ist kein Ticket! Dieser Command funktioniert nur in einem.", delete_after=20)

        
#Please do not change anything here. All things come into the config.json
bot.run(token)




