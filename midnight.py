import discord
import asyncio
import datetime
import midnight_methods

from dotenv import load_dotenv
import os

from discord.ext import commands, tasks

load_dotenv('midnight.env')

client = discord.Client()
prefix = '?'

@client.event
async def on_ready():
    print ('We have logged in as {0.user}' .format(client))

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
        time = '6:30 AM'
        points_embed = discord.Embed(title='Current Points', description=f'Updated: March 22nd at {time}', color=0xe3244a)
        points_embed.add_field(name='UTI - 18', value='Ranishammer: 3.75\nRyuko: 5.25\nMorvin: 5.25\nBenzo: 3.75', inline=False)
        points_embed.add_field(name='LFH - 51.75', value='Klotho: 3.75\nTrigger: 11\nLockie: 29.75\nLyndane: 7.25', inline=False)
        points_embed.add_field(name='Hello Sweetie - 39.75', value='Beane: 13.75\nOrcien: 13\nThiria: 6.5\nDocterdonna: 6.5', inline=False)
        points_embed.add_field(name='Arystocrats - 21.25', value='Arys: 3.25\nDeku: 4.75\nCereen: 9.5\nValdel: 3.75', inline=False)

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

            character = midnight_methods.get_char(realm_and_character[0], realm_and_character[1])

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

            mythics = midnight_methods.get_recent_mythic(realm_and_character[0], realm_and_character[1])
            character = midnight_methods.get_char(realm_and_character[0], realm_and_character[1])

            mythics_embed = discord.Embed(title=f'{character[0]}\'s recent dungeons', description=character[7] + '\nTIMESTAMPS ARE IN UTC TIMEZONE (5 HOURS AHEAD OF CST)',color=0x77d45d)

            for i in mythics:
                time_split = i[4][1].split('.')
                mythics_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted: ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

            await message.channel.send(embed = mythics_embed)

    if msg.startswith(prefix+'team one') or msg.startswith(prefix+'team 1'):
        ranishammer = midnight_methods.get_char('Ranishammer', 'Garona')
        morvin = midnight_methods.get_char('Morvin', 'Onyxia')
        ryuko = midnight_methods.get_char('Ryuko', 'Garona')
        benzo = midnight_methods.get_char('Benzonatate', 'Garona')

        team = [ranishammer, morvin, ryuko, benzo]

        team_one = discord.Embed(title="Team One", color=0xe3244a)

        for i in team:
            team_one.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_one)

        await message.channel.send('Would you like to see the 10 most recent dungeons that team one did?')
        try:
            yes_or_no = await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await message.channel.send('I guess that\'s a no then!')
        else:
            if yes_or_no.content.lower() == 'no':
                await message.channel.send('Okay then!')
            elif yes_or_no.content.lower() == 'yes':
                ranish_mythics = midnight_methods.get_recent_mythic(ranishammer[0], ranishammer[5])
                morvin_mythics = midnight_methods.get_recent_mythic(morvin[0], morvin[5])
                ryuko_mythics = midnight_methods.get_recent_mythic(ryuko[0], ryuko[5])
                benzo_mythics = midnight_methods.get_recent_mythic(benzo[0], benzo[5])

                ranish_embed = discord.Embed(title='Ranishammer\'s recent dungeons', description=ranishammer[7], color=0xe3244a)

                for i in ranish_mythics:
                    time_split = i[4][1].split('.')
                    ranish_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC') 

                morvin_embed = discord.Embed(title='Morvin\'s recent dungeons', description=morvin[7], color=0xe3244a)

                for i in morvin_mythics:
                    time_split = i[4][1].split('.')
                    morvin_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')
                
                ryuko_embed = discord.Embed(title='Ryuko\'s recent dungeons', description=ryuko[7], color=0xe3244a)

                for i in ryuko_mythics:
                    time_split = i[4][1].split('.')
                    ryuko_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                benzo_embed = discord.Embed(title='Benzonatate\'s recent dungeons', description=benzo[7], color=0xe3244a)

                for i in benzo_mythics:
                    time_split = i[4][1].split('.')
                    benzo_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                mythics_array = [ranish_embed, morvin_embed, ryuko_embed, benzo_embed]

                for a in mythics_array:
                    await message.channel.send(embed = a)

    if msg.startswith(prefix+'team two') or msg.startswith(prefix+'team 2'):
        klotho = midnight_methods.get_char('Klotho', 'Garona')
        lyndane = midnight_methods.get_char('Lyndane', 'Onyxia')
        thanea = midnight_methods.get_char('Thanea', 'Burning Blade')
        trigger = midnight_methods.get_char('Trîggêr', 'Garona')

        team = [klotho, lyndane, thanea, trigger]

        team_two = discord.Embed(title='Team Two', color=0xe3244a)

        for i in team:
            team_two.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_two)

        await message.channel.send('Would you like to see the 10 most recent dungeons that team two did?')
        try:
            yes_or_no = await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await message.channel.send('I guess that\'s a no then!')
        else:
            if yes_or_no.content.lower() == 'no':
                await message.channel.send('Okay then!')
            elif yes_or_no.content.lower() == 'yes':
                klotho_mythics = midnight_methods.get_recent_mythic(klotho[0], klotho[5])
                lyndane_mythics = midnight_methods.get_recent_mythic(lyndane[0], lyndane[5])
                thanea_mythics = midnight_methods.get_recent_mythic(thanea[0], thanea[5])
                trigger_mythics = midnight_methods.get_recent_mythic(trigger[0], trigger[5])

                klotho_embed = discord.Embed(title='Klotho\'s recent dungeons', description=klotho[7], color=0xe3244a)

                for i in klotho_mythics:
                    time_split = i[4][1].split('.')
                    klotho_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC') 

                lyndane_embed = discord.Embed(title='Lyndane\'s recent dungeons', description=lyndane[7], color=0xe3244a)

                for i in lyndane_mythics:
                    time_split = i[4][1].split('.')
                    lyndane_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')
                
                thanea_embed = discord.Embed(title='Thanea\'s recent dungeons', description=thanea[7], color=0xe3244a)

                for i in thanea_mythics:
                    time_split = i[4][1].split('.')
                    thanea_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                trigger_embed = discord.Embed(title='Trigger\'s recent dungeons', description=trigger[7], color=0xe3244a)

                for i in trigger_mythics:
                    time_split = i[4][1].split('.')
                    trigger_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                mythics_array = [klotho_embed, lyndane_embed, trigger_embed, thanea_embed]

                for a in mythics_array:
                    await message.channel.send(embed = a)

    if msg.startswith(prefix+'team three') or msg.startswith(prefix+'team 3'):
        beane = midnight_methods.get_char('Beane', 'Garona')
        orcien = midnight_methods.get_char('Orcien', 'Garona')
        thiria = midnight_methods.get_char('Thirià', 'Garona')
        donna = midnight_methods.get_char('Docterdonna', 'Garona')

        team = [beane, orcien, thiria, donna]

        team_three = discord.Embed(title='Team Three', color=0xe3244a)

        for i in team:
            team_three.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_three)

        await message.channel.send('Would you like to see the 10 most recent dungeons that team two did?')
        try:
            yes_or_no = await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await message.channel.send('I guess that\'s a no then!')
        else:
            if yes_or_no.content.lower() == 'no':
                await message.channel.send('Okay then!')
            elif yes_or_no.content.lower() == 'yes':
                beane_mythics = midnight_methods.get_recent_mythic(beane[0], beane[5])
                orcien_mythics = midnight_methods.get_recent_mythic(orcien[0], orcien[5])
                thiria_mythics = midnight_methods.get_recent_mythic(thiria[0], thiria[5])
                donna_mythics = midnight_methods.get_recent_mythic(donna[0], donna[5])

                beane_embed = discord.Embed(title='Beane\'s recent dungeons', description=beane[7], color=0xe3244a)

                for i in beane_mythics:
                    time_split = i[4][1].split('.')
                    beane_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC') 

                orcien_embed = discord.Embed(title='Orcien\'s recent dungeons', description=orcien[7], color=0xe3244a)

                for i in orcien_mythics:
                    time_split = i[4][1].split('.')
                    orcien_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')
                
                thiria_embed = discord.Embed(title='Thirià\'s recent dungeons', description=thiria[7], color=0xe3244a)

                for i in thiria_mythics:
                    time_split = i[4][1].split('.')
                    thiria_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                donna_embed = discord.Embed(title='Donna\'s recent dungeons', description=donna[7], color=0xe3244a)

                for i in donna_mythics:
                    time_split = i[4][1].split('.')
                    donna_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                mythics_array = [beane_embed, orcien_embed, donna_embed, thiria_embed]

                for a in mythics_array:
                    await message.channel.send(embed = a)

    if msg.startswith(prefix+'team four') or msg.startswith(prefix+'team 4'):
        arys = midnight_methods.get_char('Arys', 'Onyxia')
        deku = midnight_methods.get_char('Dëku', 'Burning Blade')
        cereen = midnight_methods.get_char('Cereen', 'Garona')
        valdel = midnight_methods.get_char('Valdel', 'Garona')

        team = [arys, deku, cereen, valdel]

        team_four = discord.Embed(title='Team Four', color=0xe3244a)

        for i in team:
            team_four.add_field(name=i[0] + ' - ' + i[8], value=i[7], inline=False)

        await message.channel.send(embed=team_four)

        await message.channel.send('Would you like to see the 10 most recent dungeons that team two did?')
        try:
            yes_or_no = await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await message.channel.send('I guess that\'s a no then!')
        else:
            if yes_or_no.content.lower() == 'no':
                await message.channel.send('Okay then!')
            elif yes_or_no.content.lower() == 'yes':
                arys_mythics = midnight_methods.get_recent_mythic(arys[0], arys[5])
                deku_mythics = midnight_methods.get_recent_mythic(deku[0], deku[5])
                cereen_mythics = midnight_methods.get_recent_mythic(cereen[0], cereen[5])
                valdel_mythics = midnight_methods.get_recent_mythic(valdel[0], valdel[5])

                arys_embed = discord.Embed(title='Arys\'s recent dungeons', description=arys[7], color=0xe3244a)

                for i in arys_mythics:
                    time_split = i[4][1].split('.')
                    arys_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC') 

                deku_embed = discord.Embed(title='Deku\'s recent dungeons', description=deku[7], color=0xe3244a)

                for i in deku_mythics:
                    time_split = i[4][1].split('.')
                    deku_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')
                
                cereen_embed = discord.Embed(title='Cereen\'s recent dungeons', description=cereen[7], color=0xe3244a)

                for i in cereen_mythics:
                    time_split = i[4][1].split('.')
                    cereen_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                valdel_embed = discord.Embed(title='Valdel\'s recent dungeons', description=valdel[7], color=0xe3244a)

                for i in valdel_mythics:
                    time_split = i[4][1].split('.')
                    valdel_embed.add_field(name=i[0] + ' +' + i[1], value='Keystone Upgrade: ' + i[2] + '\nTime: ' + i[3] + '\nCompleted ' + i[4][0] + ' at ' + time_split[0] + ' UTC')

                mythics_array = [arys_embed, deku_embed, valdel_embed, cereen_embed]

                for a in mythics_array:
                    await message.channel.send(embed = a)

    if msg.startswith(prefix+'can\'t touch this') or msg.startswith(prefix+'cant touch this'):
        await message.channel.send('youtube.com/watch?v=t2pw2bujsKc')

client.run(os.getenv('DISCORD_TOKEN'))