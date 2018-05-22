'''
Dr. Dragonbot by MadScotty

BEGIN LICENSE

By existing on the same mortal coil as the author of this software you hereby
allow the author, henceforth known as Dr. Awesomeweiner, to sleep on your couch, 
watch your television, and use your microwave.  By reading this license you agree 
that Lord Satan isn't as bad as everyone says #fakenews

END LICENSE
'''

import discord
import modules

description = "Rolled a nat 1 for shitposting.  Great news!"
version = "0.1"

client = discord.Client()
admins = ["MadScotty#1628"]
command_prefix = "!"

@client.event
async def on_message(message):

    # The bot will ignore itself
    if message.author == client.user:
        return
    
    # Listener for commands
    elif message.content.startswith(command_prefix):        
        # Clean up command (remove prefix, force to string, and lowercase it)
        command = str(message.content[1:])
        command = command.lower()

        # Begin listening for commands

        # Bot is misbehaving.  Time to die!
        if command == "die" and str(message.author) in admins:
            await client.send_message(message.channel, "Committing Sudoku...")
            await client.logout()

        # PM user with list of commands
        elif command == "help":
            await client.send_message(message.author, await modules.helpbox(command_prefix))

        # Spell lookup module. (Don't forget space)
        elif command.startswith("spell "):
            lookup_return = await modules.spell_lookup(command[6:])
            if lookup_return == -1:
                await client.send_message(message.channel, "Spell not found.")
            # Did we get one embed or two back?
            elif type(lookup_return) is discord.Embed:
                await client.send_message(message.channel, embed = lookup_return)
            else:
                await client.send_message(message.channel, embed = lookup_return[0])
                await client.send_message(message.channel, embed = lookup_return[1])

        # Condition lookup module.  Space intentionally absent.
        elif command.startswith("condition"):
            await client.send_message(message.channel, await modules.condition_lookup(command, command_prefix))

        # I CAST MAGIC MISSILE
        elif command == "magicmissile":
            caster = "<@" + message.author.id + ">"
            await client.send_message(message.channel, await modules.magicmissile(caster))

        # PM user current changelog
        elif command == "changelog":
            await client.send_message(message.author, await modules.changelog())

        # Let's roll some dice! (Don't forget the space!)
        elif command.startswith("roll "):
            await client.send_message(message.channel, await modules.dice_roll(command[5:]))

# Reminds me in console that the damn thing is running
@client.event
async def on_ready():
    print(client.user.name, "Logged in and running")


# Let's get this party started
auth_token_file = open("bot.token")
token = auth_token_file.read()
client.run(token)