import discord
import json
import requests

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