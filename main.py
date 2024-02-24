import os

import discord
import requests

from webdriver import keep_alive

keep_alive()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
my_secret = os.environ['TOKEN']


@client.event
async def on_message(message):
  if message.content.startswith("?ark"):
    server_code = message.content.replace("?ark ", "")

    # Battlemetrics API에서 Ark 어센디드 서버 정보를 가져오는 함수 호출
    server_info = get_battlemetrics_server_info(server_code)

    if server_info:
      # 서버 정보 출력
      players_text = f'**{server_info["players"]} / 70**'
      embed = discord.Embed(title=f"Official-PVP-TheIsland {server_code}",
                            description="Ark : Survival Asended Server Info",
                            color=0xa552bc)
      embed.set_thumbnail(
          url=
          "https://cdn.discordapp.com/attachments/841500187637448714/1210838732865929306/1_1.png?ex=65ec0472&is=65d98f72&hm=5acab0e3d138d1b84cb14486e730d2c53eea0046051ececcfe91e44faed9d718&"
      )
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name='Players 👤', value=players_text, inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name='Map 🗺',
                      value=f"**{server_info['map']}**",
                      inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name='Status❗',
                      value=f"**{server_info['status']}**",
                      inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text="Made by WELCIKS")
      await message.channel.send(embed=embed)
    else:
      embed = discord.Embed(title=f"Official-PVP-TheIsland {server_code}",
                            description="Ark : Survival Asended Server Info",
                            color=0xa552bc)
      embed.set_thumbnail(
          url=
          "https://cdn.discordapp.com/attachments/841500187637448714/1210838732865929306/1_1.png?ex=65ec0472&is=65d98f72&hm=5acab0e3d138d1b84cb14486e730d2c53eea0046051ececcfe91e44faed9d718&"
      )
      embed.add_field(name=" ", value=" ", inline=True)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(
          name='Sorry... 😥',
          value=
          f"**Unable to retrieve information for the {server_code} server.**",
          inline=True)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.add_field(name=" ", value=" ", inline=False)
      embed.set_footer(text="Made by WELCIKS")
      await message.channel.send(embed=embed)


def get_battlemetrics_server_info(server_code):
  api_url = f'https://api.battlemetrics.com/servers?filter[game]=arksa&filter[search]={server_code}&sort=-players'

  try:
    response = requests.get(api_url)
    data = response.json()

    if 'data' in data and len(data['data']) > 0:
      # 서버 중에서 플레이어 수가 가장 많은 서버를 선택
      server = data['data'][0]
      players = server['attributes']['players']
      map_name = server['attributes']['details']['map']
      status = server['attributes']['status']

      return {'players': players, 'map': map_name, 'status': status}

  except Exception as e:
    print(f"Error fetching server info: {e}")

  return None


client.run(my_secret)
