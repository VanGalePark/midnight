import discord
import json
import requests
import asyncio
import datetime

from dotenv import load_dotenv
import os

from discord.ext import commands, tasks

load_dotenv('midnight.env')

client = discord.Client()
prefix = '?'

def get_char(char_name, realm):
    response = requests.get(f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={char_name}&fields=gear").text

    json_data = json.loads(response)

    #basic information
    name = json_data['name'] #0
    race = json_data['race'] #1
    char_class = json_data['class'] #2
    active_spec = json_data['active_spec_role'] #3
    faction = json_data['faction'] #4
    realm = json_data['realm'] #5
    profile_picture = json_data['thumbnail_url'] #6
    profile_url = json_data['profile_url'] #7
    active_spec_name = json_data['active_spec_name'] #10

    #gear
    ilevel = str(json_data['gear']['item_level_equipped']) #8

    #mythic plus
    mythics = requests.get(f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={char_name}&fields=mythic_plus_recent_runs").text
    json_mythics = json.loads(mythics)

    dungeon = json_mythics['mythic_plus_recent_runs'][0]

    time_milli = dungeon['clear_time_ms']
    seconds = int((time_milli/1000)%60)
    minutes = int((time_milli/(1000*60))%60)
    hours = int((time_milli/(1000*60*60))%24)

    dung_name = dungeon['dungeon'] #0
    mythic_lvl = str(dungeon['mythic_level']) #1
    keys_upgrade = str(dungeon['num_keystone_upgrades']) #2
    time_stamp = dungeon['completed_at'].split('T') #4

    if hours == 0:
        time = f'{minutes} minutes and {seconds} seconds' #3
    else:
        time = f"{hours} hours {minutes} minutes and {seconds} seconds" #3
    
    mythics_array = [dung_name, mythic_lvl, keys_upgrade, time, time_stamp] #9

    #guild
    guild = requests.get(f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={char_name}&fields=guild").text
    json_guild = json.loads(guild)

    guild_name = json_guild['guild']['name'] #11

    #covenant
    covenant = requests.get(f"https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={char_name}&fields=covenant").text
    json_cov = json.loads(covenant)

    covenant_name = json_cov['covenant']['name'] #12

    return([name, race, char_class, active_spec, faction, realm, profile_picture, profile_url, ilevel, mythics_array, active_spec_name, guild_name, covenant_name])


def get_recent_mythic(char_name, realm):
    response = requests.get(f'https://raider.io/api/v1/characters/profile?region=us&realm={realm}&name={char_name}&fields=mythic_plus_recent_runs').text
    json_data = json.loads(response)

    dungeon_array = []

    for dungeon in json_data['mythic_plus_recent_runs']:
        time_milli = dungeon['clear_time_ms']   
        seconds = int((time_milli/1000)%60)
        minutes = int((time_milli/(1000*60))%60)
        hours = int((time_milli/(1000*60*60))%24)

        if hours == 0:
            time = f'{minutes} minutes and {seconds} seconds'
        else:
            time = f'{hours} hours {minutes} minutes and {seconds} seconds'

        name = dungeon['dungeon'] #0
        mythic_lvl = str(dungeon['mythic_level']) #1
        keystone_upgrade = str(dungeon['num_keystone_upgrades']) #2
        #time is 3
        time_stamp = dungeon['completed_at'].split('T') #4


        individual_dungeon = [name, mythic_lvl, keystone_upgrade, time, time_stamp]

        dungeon_array.append(individual_dungeon)

    return(dungeon_array)


@client.event
async def on_ready():
    print ('We have logged in as {0.user}' .format(client))


#team one
numbo_one_id = 821218339560488981
@tasks.loop(hours=12)
async def team_channel_one():
    message_channel = client.get_channel(numbo_one_id)
    print("Team one's character profiles are printed!")

    ranishammer = get_char('Ranishammer', 'Garona')
    morvin = get_char('Morvin', 'Onyxia')
    ryuko = get_char('Ryuko', 'Garona')
    benzo = get_char('Benzonatate', 'Garona')

    team = [ranishammer, morvin, ryuko, benzo]

    team_one = discord.Embed(title="Team One", color=0xe3244a)

    for i in team:
        team_one.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

    await message_channel.send(embed=team_one)

@team_channel_one.before_loop
async def before():
    await client.wait_until_ready()
    print("Team one is done waiting")


#team two
numbo_two_id = 821218408464777226
@tasks.loop(hours=12)
async def team_channel_two():
    message_channel = client.get_channel(numbo_two_id)
    print("Team two's character profiles are printed!")

    klotho = get_char('Klotho', 'Garona')
    lyndane = get_char('Lyndane', 'Onyxia')
    thanea = get_char('Thanea', 'Burning Blade')
    trigger = get_char('Trîggêr', 'Garona')

    team = [klotho, lyndane, thanea, trigger]

    team_two = discord.Embed(title='Team Two', color=0xe3244a)

    for i in team:
        team_two.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

    await message_channel.send(embed=team_two)

@team_channel_two.before_loop
async def before_two():
    await client.wait_until_ready()
    print("Team two is done waiting")


#team three
numbo_three_id = 821249234958417941
@tasks.loop(hours=12)
async def team_channel_three():
    message_channel = client.get_channel(numbo_three_id)
    print("Team three's character profiles are printed!")

    beane = get_char('Beane', 'Garona')
    orcien = get_char('Orcien', 'Garona')
    thiria = get_char('Thirià', 'Garona')
    donna = get_char('Docterdonna', 'Garona')

    team = [beane, orcien, thiria, donna]

    team_three = discord.Embed(title='Team Three', color=0xe3244a)

    for i in team:
        team_three.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

    await message_channel.send(embed=team_three)

@team_channel_three.before_loop
async def before_three():
    await client.wait_until_ready()
    print("Team three is done waiting")


#team four
numbo_four_id = 821249261210828851
@tasks.loop(hours=12)
async def team_channel_four():
    message_channel = client.get_channel(numbo_four_id)
    print("Team four's character profiles are printed!")

    arys = get_char('Arys', 'Onyxia')
    deku = get_char('Dëku', 'Burning Blade')
    cereen = get_char('Cereen', 'Garona')
    valdel = get_char('Valdel', 'Garona')

    team = [arys, deku, cereen, valdel]

    team_four = discord.Embed(title='Team Four', color=0xe3244a)

    for i in team:
        team_four.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

    await message_channel.send(embed=team_four)

@team_channel_four.before_loop
async def before_four():
    await client.wait_until_ready()
    print("Team four is done waiting")


@client.event
async def on_message(message):
    msg = message.content.lower()

    if not msg.startswith(prefix) or message.author == client.user:
        return

    if msg.startswith(prefix+'commands') or msg.startswith(prefix+'help'):
        commands_embed = discord.Embed(title='List of Commands', color=0xe34b9c)
        commands_embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        commands_embed.add_field(name='?char / ?character', value='Answer the bot\'s question to pull up your (or someone else\'s) character card.', inline=False)
        commands_embed.add_field(name='?team <x>', value='Enter team 1 - 4 to pull up a list of the people in that team, their ilvls, and their raider.io profiles.\nONLY ACTIVE DURING EVENTS', inline=False)
        commands_embed.add_field(name='?recent', value='Answer the bot\'s question to see your (or someone else\'s) 10 most recent Mythics.', inline=False)
        commands_embed.add_field(name='?cant touch this', value='I mean, just guess.', inline=False)
        commands_embed.add_field(name='?points', value='Shows the current points for the teams. It\'s not updated automatically so please be patient with me ;w;.\nONLY ACTIVE DURING EVENTS')

        await message.channel.send(embed = commands_embed)

    if msg.startswith(prefix + 'points'):
        time = '4:30 AM'
        points_embed = discord.Embed(title='Current Points', description=f'Updated: March 20th at {time}', color=0xe3244a)
        points_embed.add_field(name='UTI - 11.5', value='Ranishammer: 2.75\nRyuko: 3.25\nMorvin: 2.75\nBenzo: 2.75', inline=False)
        points_embed.add_field(name='LFH - 35.25', value='Klotho: 2.25\nTrigger: 9\nLockie: 17.75\nLyndane: 6.25', inline=False)
        points_embed.add_field(name='Hello Sweetie - 31.25', value='Beane: 9.75\nOrcien: 10.5\nThiria: 5\nDocterdonna: 6', inline=False)
        points_embed.add_field(name='Arystocrats - 18.75', value='Arys: 3.25\nDeku: 3.75\nCereen: 9\nValdel: 2.75', inline=False)

        await message.channel.send(embed = points_embed)


    if msg.startswith(prefix+'char') or msg.startswith(prefix+'character'):
        #ask the name
        await message.channel.send('What is your character\'s name and realm?')
        #wait for message from user for character name
        try:
            user_message = await client.wait_for("message", timeout=30)
        except asyncio.TimeoutError:
            await message.channel.send('You took too long and I\'m bored so bye.')
        except KeyError():
            await message.channel.send('Yea so I don\'t have this character in my records so come back when that gets fixed thanks.')
        except IndexError():
            await message.channel.send('You didn\'t give me enough information to find the character.')
        else:
            user_message.content = user_message.content.lower()

            if ' ' in user_message.content:
                realm_and_character = user_message.content.split(' ')
            elif '-' in user_message.content:
                realm_and_character = user_message.content.split('-')

            if realm_and_character[0] == 'trigger':
                realm_and_character[0] = 'Trîggêr'
            
            if realm_and_character[0] == 'deku':
                realm_and_character[0] = 'Dëku'

            if realm_and_character[0] == 'thiria':
                realm_and_character[0] = 'Thirià'

            character = get_char(realm_and_character[0], realm_and_character[1])

            char_embed = discord.Embed(title=character[1] + ', '+ character[10] + ' ' + character[2], description= '<' + character[11] + '>, ' + character[5], color=0x368cff)
            char_embed.set_author(name=character[0] + ' - ' + character[3], icon_url=character[6])
            char_embed.set_thumbnail(url=character[6])
            char_embed.add_field(name='Profile Link', value=character[7], inline=False)

            char_embed.add_field(name='Most Recent Dungeon', value=character[9][0] + ' +' + character[9][1] + '\nTime: ' + character[9][3] + '\nKeystone Upgrade: ' + character[9][2] + '\nCompleted: ' + character[9][4][0], inline=True)
            char_embed.add_field(name='Item Level', value=character[8], inline=True)

            char_embed.add_field(name='Covenant', value=character[12], inline=False)

            await message.channel.send(embed=char_embed)
    
    if msg.startswith(prefix+'recent'):
        #ask the name
        await message.channel.send('What\'s your character\'s name and realm?')

        try:
            user_message = await client.wait_for("message", timeout=30)
        except asyncio.TimeoutError:
            await message.channel.send('I\'m tired of waiting so i\'m gonna go somewhere else.')
        except KeyError():
            await message.channel.send('Sorry that name is super not ringing a bell.')
        except IndexError():
            await message.channel.send('You didn\'t give me enough information to find the character.')
        else:
            user_message.content = user_message.content.lower()

            if ' ' in user_message.content:
                realm_and_character = user_message.content.split(' ')
            elif '-' in user_message.content:
                realm_and_character = user_message.content.split('-')

            if realm_and_character[0] == 'trigger':
                realm_and_character[0] = 'Trîggêr'
            
            if realm_and_character[0] == 'deku':
                realm_and_character[0] = 'Dëku'

            if realm_and_character[0] == 'thiria':
                realm_and_character[0] = 'Thirià'

            mythics = get_recent_mythic(realm_and_character[0], realm_and_character[1])
            character = get_char(realm_and_character[0], realm_and_character[1])

            mythics_embed = discord.Embed(title=f'{character[0]}\'s recent dungeons', description=character[7] + '\nTIMESTAMPS ARE IN UTC TIMEZONE (5 HOURS AHEAD OF CST)',color=0x77d45d)

            for i in mythics:
                time_split = i[4][1].split('.')
                mythics_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted: ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

            await message.channel.send(embed = mythics_embed)

    if msg.startswith(prefix+'team one') or msg.startswith(prefix+'team 1'):
        ranishammer = get_char('Ranishammer', 'Garona')
        morvin = get_char('Morvin', 'Onyxia')
        ryuko = get_char('Ryuko', 'Garona')
        benzo = get_char('Benzonatate', 'Garona')

        team = [ranishammer, morvin, ryuko, benzo]

        team_one = discord.Embed(title="Team One", color=0xe3244a)

        for i in team:
            team_one.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_one)

    if msg.startswith(prefix+'team two') or msg.startswith(prefix+'team 2'):
        klotho = get_char('Klotho', 'Garona')
        lyndane = get_char('Lyndane', 'Onyxia')
        thanea = get_char('Thanea', 'Burning Blade')
        trigger = get_char('Trîggêr', 'Garona')

        team = [klotho, lyndane, thanea, trigger]

        team_two = discord.Embed(title='Team Two', color=0xe3244a)

        for i in team:
            team_two.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_two)

    if msg.startswith(prefix+'team three') or msg.startswith(prefix+'team 3'):
        beane = get_char('Beane', 'Garona')
        orcien = get_char('Orcien', 'Garona')
        thiria = get_char('Thirià', 'Garona')
        donna = get_char('Docterdonna', 'Garona')

        team = [beane, orcien, thiria, donna]

        team_three = discord.Embed(title='Team Three', color=0xe3244a)

        for i in team:
            team_three.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_three)

    if msg.startswith(prefix+'team four') or msg.startswith(prefix+'team 4'):
        arys = get_char('Arys', 'Onyxia')
        deku = get_char('Dëku', 'Burning Blade')
        cereen = get_char('Cereen', 'Garona')
        valdel = get_char('Valdel', 'Garona')

        team = [arys, deku, cereen, valdel]

        team_four = discord.Embed(title='Team Four', color=0xe3244a)

        for i in team:
            team_four.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_four)

    if msg.startswith(prefix+'can\'t touch this') or msg.startswith(prefix+'cant touch this'):
        await message.channel.send('youtube.com/watch?v=t2pw2bujsKc')

    if msg.startswith(prefix+'hello'):
        await message.channel.send('Hello sweetie ;)')

#team_channel_one.start()
#team_channel_two.start()
#team_channel_three.start()
#team_channel_four.start()

client.run(os.getenv('DISCORD_TOKEN'))