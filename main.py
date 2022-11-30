import discord
from discord.ext import commands
from termcolor import colored
from discord.utils import get
from discord.ext.commands import has_permissions
import discord
from discord.ext import commands



token = "YOUR TOKEN HERE"
prefix = "ts."
client = commands.Bot(command_prefix= prefix, intents=discord.Intents.all())
client.remove_command("help") 
players = {}
roles = []








@client.event
async def on_command_error(ctx, error):
    await ctx.respond(f"Error: {error}")    


@client.event
async def on_ready():
    print(colored("We have logged in as {0.user} ".format(client) , "green"))
    for guild in client.guilds:
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))
    activity = discord.Game(name=f"/help", type=3)               
    await client.change_presence(status=discord.Status.online, activity=activity)   
    client.add_view(Ticket()) # Registers a View for persistent listening
    client.add_view(Ticketbuttons()) # Registers a View for persistent listening
 
 
 
 
 
 
 

@client.slash_command(name="help",description="Sends a quick Help")  
async def help(ctx):
    embed = discord.Embed(title="🎫 Help Center 🎫",color=0x00FFFF)
    embed.add_field(name="Commands :",value="`/ticketsetup  :` Set up a custom Message to create Tickets!" ,inline=False)
    await ctx.respond(embed=embed)
    print(colored("/help executed", "blue"))  
    
    
    
    
    
    
    
    
    
    

class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None

    @discord.ui.button(label="Close Ticket",custom_id="button-6", style=discord.ButtonStyle.primary, emoji="🔑")
    async def first_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Closing Ticket")
        guild = interaction.guild
        kanal = interaction.channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        await kanal.edit(overwrites=overwrites)
        await kanal.edit(name=str(kanal) + "closed")
        print(colored("Ticket closed", "blue"))

    @discord.ui.button(label="Delete Ticket",custom_id="button-7", style=discord.ButtonStyle.danger, emoji="🚮") # Create a button with the label "😎 Click me!" with color Blurple
    async def second_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Deleting Ticket") # Send a message when the button is clicked
        await interaction.channel.delete()
        print(colored("Ticket deleted", "blue"))



class Ticketbuttons(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None

    @discord.ui.button(label="Create Ticket",custom_id="button-5", style=discord.ButtonStyle.primary, emoji="✉️") # Create a button with the label "😎 Click me!" with color Blurple
    async def a_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
        }
        global Channel
        Channel = await guild.create_text_channel(str(member) + "s Ticket" , overwrites=overwrites, category=interaction.channel.category)
        await interaction.response.send_message("Created Ticket <#" + str(Channel.id) + ">", ephemeral=True)
        embed=discord.Embed(title="Ticket", description="<@" + str(member.id) + ">\nSupport will be given shortly...", color=0x2F3136)
        embed.set_author(name = str(interaction.user), icon_url = interaction.user.avatar.url)
        await Channel.send(embed=embed, view=Ticket())
        print(colored("Ticket created", "blue")) 

@client.slash_command(name="ticketsetup",description="Sends a Message with a button to create a Ticket --> /help")
@commands.cooldown(1, 10, commands.BucketType.channel) # it is used for the cooldown to prevent the bot from spam attack
@has_permissions(administrator=True)
async def ticketsetup(ctx, message):
    await ctx.delete()
    l = await ctx.respond("Starting setup")
    await l.delete()
    embed=discord.Embed(title="Ticket", description=str(message), color=0x2F3136)
    await ctx.send(embed=embed, view=Ticketbuttons())
    print(colored("Ticketsetup created", "blue"))

    
    
    
    
    
    
    
    
    
    
    
    

client.run(token)