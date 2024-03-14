import os
import discord
from bot import TOKEN
from bot import BENEFACTORS_CHANNEL
from bot import UPLOAD_MB
from discord.ext import tasks

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@tasks.loop( seconds = 5 )
async def UploadMedia():

    await client.wait_until_ready()

    if os.path.exists( f'file.mp4' ):
        i = os.path.getsize( f'file.mp4')
        o = UPLOAD_MB * 1024 * 1024
        if i > o:
            print(f'File too big! {i}/{o} Retriyng...')
            os.remove( f'file.mp4' )
        else:
            with open( f'file.mp4', 'rb') as file:
                media = discord.File(file)
                channel = client.get_channel( BENEFACTORS_CHANNEL )
                if channel:
                    message = await channel.send(file=media)
                    await message.add_reaction('❌')
                file.close()
            os.remove( f'file.mp4' )

@client.event
async def on_raw_reaction_add(payload):
    channel_id = payload.channel_id
    message_id = payload.message_id
    emoji = payload.emoji.name
    if payload.user_id != client.user.id:
        if channel_id == BENEFACTORS_CHANNEL:
            if emoji == '❌' or emoji == '❎':
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                await message.delete()

@client.event
async def on_message(message):
    if message.channel.id == BENEFACTORS_CHANNEL:
        if message.reference is not None:
            replied_message = await message.channel.fetch_message(message.reference.message_id)

            if replied_message:
                if any(reaction.emoji == '✅' for reaction in replied_message.reactions) or not replied_message.attachments:
                    await message.delete()
                    return

                for destination in message.channel_mentions:
                    print( f'{destination}')
                    mstr = ""
                    for attachment in replied_message.attachments:
                            mstr += attachment.url
                    if mstr:
                        await destination.send(mstr)
                        await replied_message.add_reaction('✅')
                await message.delete()

@client.event
async def on_ready():
    print('¡Bot connected as ', client.user, '!')

    UploadMedia.start()

    Cult = client.get_guild(1216162825307820042)
    LP = client.get_guild(744769532513615922)
    rol = discord.utils.get(LP.roles, name="The Cult Member")
    if rol:
        for miembro in Cult.members:
            miembroLP = LP.get_member(miembro.id)
            if miembroLP and not rol in miembroLP.roles:
                print(f'Added role to {miembro.name}\n')
                await miembroLP.add_roles(rol)

    channel = client.get_channel( BENEFACTORS_CHANNEL )

    if channel:
        role = client.get_guild(1216162825307820042).get_role( 1216208707268907139 )
        await channel.send( f"Hello World!\nPlease help me deciding what to do with these videos i've download Woof! {role.mention}")

client.run(TOKEN)