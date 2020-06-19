import random
import time
import discord
import asyncio
from discord.ext import commands
import requests, json
from datetime import datetime
import tzlocal  # $ pip install tzlocal

music = None
client = commands.Bot(command_prefix="w!")
client.remove_command("help")
list_of_commands = [['help', "shows help info"],
                    ['weather [city]', "retrives weather for the given city"]]


api_key = "b07369fa8bd3e46d242c90d4fe4da87f"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def unix_to_time(unix):
    unix_timestamp = float(unix)
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    return str(local_time)[len("2020-06-18")+1:len(str(local_time))-6]


def convert_to_far(kelvin):
    return (kelvin - 273.15) * 9/5 + 32


def get_weather(city):
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        feels_like = y["feels_like"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]

        w = x["sys"]
        sunrise = unix_to_time(w["sunrise"])
        sunset = unix_to_time(w["sunset"])

        wind = x['wind']
        wind_speed = wind['speed']
        wind_deg = wind['deg']

        weather_description = z[0]["description"]
        dic = {'temp': convert_to_far(current_temperature), 'feels_like': convert_to_far(feels_like), 'pressure': current_pressure, 'humidity': current_humidiy, 'desc': weather_description, 'wind_speed': wind_speed, 'wind_deq': wind_deg, 'sunrise': sunrise, 'sunset': sunset}
        return dic
    else:
        return 0


def embed_help(list_of_list):
    total = len(list_of_list)
    embed = discord.Embed(title="Commands List", description=f"{total} Total\n", color=0xff0000)
    embed.set_author(name="Homework Bot", icon_url="https://i.imgur.com/5TFj51C.jpg")
    embed.set_thumbnail(url="https://dv-website.s3.amazonaws.com/uploads/2019/05/jz_csweather_060619.jpg")
    for list in list_of_list:
        embed.add_field(name=list[0], value=list[1], inline=False)
    embed.set_footer(text="Thank you for using weather Bot! Devloped by Nman5#3094 https://github.com/NMan1")
    return embed


@client.command(pass_context=True)
async def help(ctx):
    await ctx.send(embed=embed_help(list_of_commands))


@client.command(pass_context=True)
async def weather(ctx, *, city, city_two="", city_three=""):
    await ctx.send(f"One momment {ctx.author}, retriving weather for {city}...")

    city_name = city + " " + city_two + " " + city_three
    dic = get_weather(city_name)
    if dic == 0:
        r = random.randint(0, 5)
        if r == 0:
            await ctx.send(f"'{city_name}' was not found... Your a fucking idiot, can you not spell? https://learnenglish.britishcouncil.org/")
        elif r == 1:
            await ctx.send(f"'{city_name}' was not found...")
        elif r == 2:
            await ctx.send(f"'{city_name}' was not found... Are you illetrate? Learn to spell dip shit...")
        elif r == 3:
            await ctx.send(f"'{city_name}' was not found... God you fucking anyyuoung... QUIT WASTING MY TIME AND LEARN ENGLISH YOU FOREIGN FUCK!")
        elif r == 4:
            await ctx.send(f"'{city_name}' was not found... Get it wrong one more time and you'll make sure to sleep with your fucking doors locked...")
            await ctx.send("https://tenor.com/view/psycho-gif-9317595")
    else:
        sunset = dic['sunset']
        sunrise = dic['sunrise']
        if int(dic['sunset'][:2]) > 12:
            dic['sunset'] = dic['sunset'].replace(dic['sunset'][:2], str(int(dic['sunset'][:2]) - 12))
            sunset = dic['sunset']

        if sunrise[:2].find("0") != -1:
            temp = sunrise[:2].replace("0", "")
            sunrise = sunrise.replace(sunrise[:2], temp)

        url = "https://www.pinclipart.com/picdir/big/5-51534_clipart-of-a-sun-sunny-icon-png-download.png"
        if dic['temp'] > 86:
            url = "https://cdn2.iconfinder.com/data/icons/weather-and-seasons-1/110/Icons__heat-512.png"
        elif dic['temp'] < 86 and dic['temp'] > 70:
            url = "https://www.nbc12.com/pb/resources/images/weather/weather-condition-icons/400x400/69_daily_forecast.png"
        elif dic['temp'] < 70:
            url = "https://cdn3.iconfinder.com/data/icons/circle-weather/512/weather_16-512.png"

        embed = discord.Embed(title=f"{city_name[:len(city_name)-1]}'s Weather", description=dic['desc'])
        embed.set_thumbnail(url=url)
        embed.add_field(name="Tempature", value=f"°{str(dic['temp'])[:3]}", inline=False)
        embed.add_field(name="Feels like", value=f"°{str(dic['feels_like'])[:3]}", inline=False)
        embed.add_field(name="Pressure", value=f"{str(dic['pressure'])} SI, hPa", inline=False)
        embed.add_field(name="Humidity", value=f"%{str(dic['humidity'])}", inline=False)
        embed.add_field(name="Wind speed", value=f"{str(dic['wind_speed'])} mph", inline=False)
        embed.add_field(name="Wind angle", value=f"{str(dic['wind_deq'])}°", inline=False)
        embed.add_field(name="Sunrise", value=f"{sunrise} am", inline=False)
        embed.add_field(name="Sunset", value=f"{sunset} pm", inline=False)
        await ctx.send(embed=embed)


@client.event
async def on_ready():
    print("The bot is ready!", flush=True)


if __name__ == '__main__':
    client.run("NzIzMzM4OTcxNzkwMzExNDU0.XuwMDA.e-DCoXJUOMxrSbhHf_DIPsqmtLs")
