import discord
import datetime
import pytz
import random
import os
import mysql.connector
import sys
home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, home_path)
import config
cf = config.config()

intents = discord.Intents.all()
reactedUserMessageArray = []
noOfMemberPrevious = 0
timezone = pytz.timezone('Asia/Hong_Kong')
lastGayMessageTime = timezone.localize(datetime.datetime(1970, 1, 1, 0, 0, 0))
client = discord.Client(intents=intents)
config = config()
cnx = mysql.connector.connect(user=cf.DATABASE_USER, password=cf.DATABASE_PASSWORD, host=cf.DATABASE_HOST, database='database')
BOT_TOKEN = cf.BOT_TOKEN_PEACH

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content)
    if message.stickers:
        return
    
    if message.author.id == 527087418009190411:
        emojiYum = client.get_emoji(1062731943785013319) 
        emojiDong = client.get_emoji(1062731973879156787)
        emojiChop = client.get_emoji(863383697311006731)
        await message.add_reaction(emojiYum)
        await message.add_reaction(emojiDong)
        await message.add_reaction(emojiChop)
        await message.add_reaction('🍑')
        
    if message.author.id == 317661870054178818 or message.author.id == 454648417797537793:
        await message.add_reaction('🍋')

    if message.author.id == 456060926840274945:
        await message.add_reaction('🐔')
        await message.add_reaction('🐛')

    if message.author.id == 317660422658588674:
        await message.add_reaction('☘️')

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    currentReactUserMessage = str(user.id) + str(message.id)
    folder_path = "./fuck"
    file = 'bonggy_fuck.gif'
    if user.id == client.user.id:
        return

    cursor = cnx.cursor()
    cursor.execute("SELECT content FROM sentences WHERE type = 1")
    result = cursor.fetchall()

    rapeArray = []
    for row in result:
        rapeArray.append(row[0])
        
    badEmojiArray = [1128260053128974378, 790627457224015902, 1031983658124447896, 1062731752172429343]
    bongEmojiArray = [712258118691848262, 1121558125737156718, 620967192178982922, 920663201643892806, 620965705910714398, 701332948062044220, 701332518762446849, 645322807017996370, 1152550733170872320, 1152550636563468368]
    badReaction = False

    try:
        if reaction.emoji.id in badEmojiArray:
            badReaction = True
    except:
        badReaction = False

    if ((reaction.emoji in ('👎','👎🏻','👎🏼','👎🏽','👎🏾','👎🏿','💩','🐔','🐤','🐥','🐣') or badReaction) and user.id == 527087418009190411 and currentReactUserMessage not in reactedUserMessageArray):
        async for msg in message.channel.history(limit=100):
            if msg.id == message.id:
                reactedUserMessageArray.append(str(user.id)+str(message.id))
                await msg.reply('屌你老母大閪頭:middle_finger: :middle_finger: ')
                break
    try:
        if reaction.emoji.id in bongEmojiArray:
            async for msg in message.channel.history(limit=100):
                if msg.id == message.id:
                    for bongEmoji in bongEmojiArray:
                        await msg.add_reaction(client.get_emoji(bongEmoji))
                    break
    except:
        pass

    user_mention = f'<@{user.id}>'
    if (reaction.emoji in ('👍','👍🏻','👍🏼','👍🏽','👍🏾','👍🏿') and currentReactUserMessage not in reactedUserMessageArray):
        async for msg in message.channel.history(limit=100):
            if msg.id == message.id:
                reactedUserMessageArray.append(str(user.id)+str(message.id))
                with open(os.path.join(folder_path, file), "rb") as f:
                    await msg.reply(file=discord.File(f, file), content=user_mention + random.choice(rapeArray))
                    return
                break

@client.event
async def on_voice_state_update(member, before, after):
    global timezone
    channel = after.channel or before.channel
    text_channel = client.get_channel(526604240714465292)
    #text_channel = client.get_channel(789423965990682638) #dev
    global lastGayMessageTime
    global noOfMemberPrevious
    if channel is not None:
        members = channel.members
        threshold = datetime.timedelta(minutes=64)
        time_difference = datetime.datetime.now(timezone) - lastGayMessageTime
        if len(members) == 0 and time_difference > threshold:
            folder_path = "./unbelievable/"
            files = os.listdir(folder_path)
            file = random.choice(files)

            now = datetime.datetime.now(timezone)
            weekday = now.weekday()

            if weekday == 0:
                weekday = '星期一'
            elif weekday == 1:
                weekday = '星期二'
            elif weekday == 2:
                weekday = '星期三'
            elif weekday == 3:
                weekday = '星期四'
            elif weekday == 4:
                weekday = '星期五'
            elif weekday == 5:
                weekday = '星期六'
            elif weekday == 6:
                weekday = '星期日'

            nowHour = now.hour
            if 0 <= nowHour < 6:
                section = "凌晨"
            elif 6 <= nowHour < 12:
                section = "上晝"
            elif 12 <= nowHour < 18:
                section = "晏晝"
            else:
                section = "晚"

            await text_channel.send('<:yam:1062731943785013319><:dong:1062731973879156787>' + weekday + section +'0人打gay？？？')
            lastGayMessageTime = datetime.datetime.now(timezone)
            with open(os.path.join(folder_path, file), "rb") as f:
                await text_channel.send(file=discord.File(f, file))
                return
            
        if (len(members) == 2 and len(members) > noOfMemberPrevious):
            first_user_id = members[0].id
            first_user_mention = f'<@{first_user_id}>'
            await text_channel.send(f"{first_user_mention}自c玩又5叫...")

        noOfMemberPrevious = len(members)


client.run(BOT_TOKEN)