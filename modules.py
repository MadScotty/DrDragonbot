'''
Dr. Dragonbot by MadScotty

BEGIN LICENSE

By existing on the same mortal coil as the author of this software you hereby
allow the author, henceforth known as Dr. Awesomeweiner, to sleep on your couch, 
watch your television, and use your microwave.  By reading this license you agree 
that Lord Satan isn't as bad as everyone says #fakenews

END LICENSE
'''

import random
import json
import discord

# Go ahead and put the json files into memory for faster lookup

spellbook = json.load(open("spells.json", encoding = "utf-8"))
conditions_full_list = json.load(open("conditions.json", encoding = "utf-8"))
gamedate = -1

# helpbox() returns a list of commands and what they do as a string, using Discord's code block formatting
async def helpbox(command_prefix):
    formatted_string = "```"
    formatted_string += "General Commands:\n" + \
                        command_prefix + "help                  - Displays this box\n" + \
                        command_prefix + "spell (spell name)    - Displays info about a spell\n" + \
                        command_prefix + "condition (name)      - Displays info about a status condition. Leave blank for list of conditions\n" + \
                        command_prefix + "magicmissile          - I CAST MAGIC MISSILE\n" + \
                        command_prefix + "changelog             - Sends a PM with this bot's current changelog\n" + \
                        command_prefix + "roll (XdY)            - Roll some dice!  Example: " + command_prefix + "roll 5d8\n"
    formatted_string += "```"
    return formatted_string

# spell_lookup(spell_name) returns a discord embed containing details of spell_name, which is pulled from spells.json
async def spell_lookup(spell_name):
    
    # Grab spell from list
    spell_info = ""
    for i in range(0, len(spellbook)):
        if spellbook[i]["name"].lower() == spell_name:
            spell_info = spellbook[i]
            break;

    # Check to see if the spell was found in the list
    if spell_info == "":
        return -1                       # Parent function will check for a -1 return value and alert the user

    # Begin populating variables from list
    spell_name = str(spell_info["name"])
    spell_type = str(spell_info["type"])
    casting_time = str(spell_info["casting_time"])
    spell_range = str(spell_info["range"])
    components = str(spell_info["components"]["raw"])
    duration = str(spell_info["duration"])
    description = str(spell_info["description"])

    # Add higher levels info to description, if applicable.
    if "higher_levels" in spell_info:
        description += "\n\n"
        description += "**At Higher Levels.**  " + str(spell_info["higher_levels"])

    # Add f_color flair to embed based on spell's school
    f_color = 0x000000
    school = spell_info["school"]
    if school == "transmutation":
        f_color = 0x23af40
    elif school == "abjuration":
        f_color = 0x4d79ff
    elif school == "illusion":
        f_color = 0x944dff
    elif school == "conjuration":
        f_color = 0xffa64d
    elif school == "enchantment":
        f_color = 0xffcc00
    elif school == "evocation":
        f_color = 0xff1a1a
    elif school == "divination":
        f_color = 0xf2f2f2
    else:
        print(spell_name + " borked.  Check on that.")

    # Begin putting everthing together
    # Because of Discord's character limits, everything must go into the description field, (max length 2048 characters)
    # rather than using embed fields (max length 1024 characters)
    embed_description = "----------------------------------------\n"
    embed_description += "*" + spell_type + "*\n\n"

    embed_description += "**Casting time:**\n" + casting_time + "\n"
    embed_description += "**Range:**\n" + spell_range + "\n"
    embed_description += "**Components:**\n" + components + "\n"
    embed_description += "**Duration:**\n" + duration + "\n"
    embed_description += "**Description**\n" + description + "\n"

    # Because some spells are long-winded af, they have to be split into 2 embeds
    if len(embed_description) > 2048:
        divided_embed_description = []
        multi_embed = []
        # Look for the closest paragraph break (\n\n) to the 2048th character (but not over)
        breakpoint = embed_description.rfind("\n\n", 0, 2048)

        # Seperate embed_description at the paragraph break
        divided_embed_description.append(embed_description[0:breakpoint])
        # Add a little styling to part 2

        divided_embed_description.append("----------------------------------------\n")
        divided_embed_description[1] += "*(cont.)*\n\n"
        divided_embed_description[1] += embed_description[breakpoint+2:]        # breakpoint + 2 crops the paragraph break (\n\n)

        multi_embed.append(discord.Embed(title = str(spell_name), description = divided_embed_description[0], color = f_color))
        multi_embed.append(discord.Embed(title = str(spell_name), description = divided_embed_description[1], color = f_color))
        
        return multi_embed

    return discord.Embed(title = str(spell_name), description = embed_description, color = f_color)

# condition_lookup returns info about a specified condition as a string, or if none is specified, it returns a list of conditions
# It needs the command_prefix to cater a helpful reply (how to get info on a specific condition)
async def condition_lookup(condition, command_prefix):

    # Was a condition specified?
    if condition == "condition":
        condition_list_index = ""

        # Create a list of the status conditions
        for i in range(0, len(conditions_full_list)):
            condition_list_index += conditions_full_list[i]["name"]
            # Add commas
            if i != len(conditions_full_list) - 1:
                condition_list_index += ", "
        return "**Conditions:** " + condition_list_index + "\n\nFor details on a specific condition, type " + command_prefix + "condition \"name\" (without quotes)"

    # If not, strip the command and make the argument case insensitive
    condition = condition[10:].lower()

    # Find the condition in the json list and return it's description
    for i in range(0, len(conditions_full_list)):
        if conditions_full_list[i]["name"].lower() == condition:
            return "**" + conditions_full_list[i]["name"] + "**\n" + conditions_full_list[i]["description"]

    return "Condition not found"

# I CAST MAGIC MISSLE
async def magicmissile(caster):
    damage = str(random.randint(1,4) + random.randint(1,4) + random.randint(1,4) + 3)
    return caster + " casts magic missile and deals " + damage + " damage!"

# PM user the current changelog
async def changelog():
    formatted_string = "```"

    try:
        with open("changelog.txt", "r") as logfile:
            loglist = logfile.readlines()
    except:
        print("Changelog file operation failed")
        return "Changelog file operation borked. Scotty has been notified. =["

    for i in loglist:
        formatted_string += i

    formatted_string += "```"
    return formatted_string

# Let's roll some dice!  Takes a string in the format XdY
async def dice_roll(dice):

    # Because people might enter bad data
    try:
        dice = dice.lower()
        if dice.startswith("d"):
            number_of_dice = 1
            number_of_sides = int(dice[1:])
        else:
            dice = dice.split("d")
            number_of_dice = int(dice[0])
            number_of_sides = int(dice[1])

        if number_of_dice >= 100:
            return "You don't really need to roll that many dice.  Maybe try fewer than one hundred next time?"

        # Let's get rolling
        list_of_rolls = []
        for i in range(0, number_of_dice):
            roll = random.randint(1, number_of_sides)
            list_of_rolls.append(roll)

        total = sum(list_of_rolls)
        result = ""

        # Format the answer as d1 + d2 + d3.... = total; for more than 1 die rolled        
        if number_of_dice > 1:
            for i in range(0, len(list_of_rolls)):
                result += str(list_of_rolls[i])
                if i != len(list_of_rolls) - 1:
                    result += " + "
                else:
                    result += " = "

        result += "**" + str(total) + "**"

        return result

    except:
        return "Invalid data.  Rolls must be in the format XdY, where X is the number of dice to roll, and Y is the number of sides on the dice."