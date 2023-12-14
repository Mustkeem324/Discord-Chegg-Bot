import asyncio
import datetime
import random
import boto3, secrets
import time
import discord
from bs4 import BeautifulSoup
import requests
import re
import os
from urllib.parse import urlparse
#from webserver import keep_alive

TOKEN = 'MTE2NjA3OTk2NjY2NDk5NDg3Ng.GBKLJd.cT6zYQvHiFzstymvM52LYBQYY5348hzk4piMOU'

intents = discord.Intents.all()  # Ensure the bot intents include messages

client = discord.Client(intents=intents)
running = False

# Check if the guild is allowed
allowed_channel_ids = [
    1164624409068306493, 1062673831896027167, 1163164887090995363,
    1150483600106590268
]


def egg_scrap(url, identifier):
  try:
    print(f"Path: {url}")
    likeapi = "https://nx.aba.vg/nxcode/eggapinxproapi.php?url=" + str(url)
    response = requests.get(likeapi)
    soup = BeautifulSoup(response.content, "html.parser")
    file_answer = f"answers_{identifier}.html"

    with open(file_answer, 'a', encoding='utf-8') as f:
      f.write(soup.prettify())

    return file_answer
  except Exception as e:
    print(e)
    raise e


def bartleby_scrap(url, identifier):
  try:
    print(f"Path: {url}")
    likeapi = "http://nx.aba.vg/bartleby/index.php?url=" + str(url)
    response = requests.get(likeapi)
    soup = BeautifulSoup(response.content, "html.parser")
    file_answer = f"answers_{identifier}.html"

    with open(file_answer, 'a', encoding='utf-8') as f:
      f.write(soup.prettify())

    return file_answer
  except Exception as e:
    print(e)
    raise e


#aws to store s3 files
def generate_unique_token(existing_tokens):
  while True:
    gen_token = secrets.token_hex(16)
    if gen_token not in existing_tokens:
      return gen_token


def upload_to_s3(file_answer):
  s3 = boto3.client(
      's3',
      region_name='us-east-1',
      aws_access_key_id='AKIAWU5JKPD6RSRHV3J4',
      aws_secret_access_key='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',
      config=boto3.session.Config(signature_version='s3v4'))

  bucket_name = 'supernova558866'
  s3.upload_file(file_answer, 'supernova558866', file_answer)
  link = s3.generate_presigned_url('get_object',
                                   Params={
                                       'Bucket': 'AWSBucketName',
                                       'Key': file_answer
                                   },
                                   ExpiresIn=100000)
  print(link)
  existing_tokens = set()  # Assume you're keeping track of generated tokens
  GenToken = generate_unique_token(existing_tokens)
  s3.upload_file(file_answer,
                 bucket_name,
                 f'{GenToken}.html',
                 ExtraArgs={'ContentType': 'text/html'})
  url3 = s3.generate_presigned_url(
      ClientMethod='get_object',
      Params={
          'Bucket': bucket_name,
          'Key': f'{GenToken}.html'
      },
      ExpiresIn=86400  # 1 Day
  )
  return url3


sudos = [1164267844905742387]
async def send_message_answer(message, url, url3, username):
  gifs = [
      'https://media1.giphy.com/media/jnhXd7KT8UTk5WIgiV/giphy.gif',
      'https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3ZmZTFzbnF3OXNyeGd4c3ZtdmczOHBjMG1nejRrNmZ6ZjR5M2RybyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/StKiS6x698JAl9d6cx/giphy.gif',
      'https://media0.giphy.com/media/fBEMsUeGHdpsClFsxM/giphy.gif',
      'https://media4.giphy.com/media/gp3aS4doWX6OYSuOI8/giphy.gif'
  ]

  embed_title1 = "Link Received!"
  embed_description1 = "Your document will be sent in a minute. {}"

  embed1 = discord.Embed(title=embed_title1,
                         description=embed_description1.format(username),
                         color=0xFF5733)
  embed1.set_thumbnail(url=random.choice(gifs))
  embed1.add_field(name="User Link:",
                   value=f"[{username}]({url})",
                   inline=False)
  embed1.set_footer(text="Contact Owner for any issues")
  embed1.timestamp = datetime.datetime.utcnow()
  await message.channel.send(embed=embed1)

  embed_title2 = "Your answer is here!"
  embed_description2 = "Open the link to view the answer.. {}"

  embed2 = discord.Embed(title=embed_title2,
                         description=embed_description2.format(username))
  embed2.set_thumbnail(url=random.choice(gifs))
  embed2.add_field(name="Answer Link:",
                   value=f"[{username}]({url3})",
                   inline=False)
  embed2.set_footer(text="Contact Owner for any issues")
  embed2.timestamp = datetime.datetime.utcnow()
  await message.channel.send(embed=embed2)

  embed_title3 = "Answer Sent!"
  embed_description3 = "Raise a ticket in case of issues <@1038087486808793219>. Find us back here if we disappear: https://solo.to/cheggcoursehero"

  embed3 = discord.Embed(title=embed_title3,
                         description=embed_description3,
                         color=0x009999)
  embed3.set_thumbnail(url=random.choice(gifs))
  embed3.set_footer(text="Contact Owner for any issues")
  embed3.timestamp = datetime.datetime.utcnow()
  await message.author.send(embed=embed3)


@client.event
async def on_ready():
    global running
    if not running:
        running = True
        print(f'Logged in as {client.user.name} ({client.user.id})')
        print('------')


@client.event
async def on_message(message):
  print(f"Text BOT: {message.content}")
  # Ignore messages sent by the bot itself
  if message.author == client.user:
    return

  if message.channel.id in allowed_channel_ids:
    if message.content.startswith("https://www.chegg.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?chegg.com/homework-help/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          try:
            print(f"Path:{url}")
            existing_tokens = set(
            )  # Assume you're keeping track of generated tokens
            identifier = generate_unique_token(existing_tokens)
            file_answer = egg_scrap(url, identifier)
          except:
            pattern = r'q(\d+)'
            match = re.search(pattern, url)
            '''
                        identifier = match.group(1)
                        '''
            existing_tokens = set(
            )  # Assume you're keeping track of generated tokens
            identifier = generate_unique_token(existing_tokens)
            print(f"Path:{identifier}")
            file_answer = egg_scrap(url, identifier)
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)

    #bartleby
    elif message.content.startswith("https://www.bartleby.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?bartleby.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          file_answer = bartleby_scrap(url, identifier)
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)

    #solutioninn
    elif message.content.startswith("https://www.solutioninn.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?solutioninn.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          likeapi = "http://nx.aba.vg/test/solutioninnapi.php?url=" + str(url)
          responsed = requests.get(likeapi)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)

    #numerade.com
    elif message.content.startswith("https://www.numerade.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?numerade.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          likeapi = "https://numeradeapi.rex699.repl.co/apii?url=" + str(url)
          responsed = requests.get(likeapi)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)
    #zookal
    elif message.content.startswith("https://www.zookal.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?zookal.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          likeapi = "https://nx.aba.vg/zookal/index.php?url=" + str(url)
          responsed = requests.get(likeapi)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)

    #study.com
    elif message.content.startswith("https://homework.study.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?homework.study.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          likeapi = "https://studyapii.rex699.repl.co/apii?url=" + str(url)
          responsed = requests.get(likeapi)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)
    #gauthmath
    elif message.content.startswith("https://www.gauthmath.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?gauthmath.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          responsed = requests.get(url)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)

    #trantutor
    elif message.content.startswith("https://www.transtutors.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?transtutors.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          payload = {}
          headers = {
              'authority':
              'www.transtutors.com',
              'accept':
              'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
              'accept-language':
              'en-US,en;q=0.9',
              'cache-control':
              'max-age=0',
              'cookie':
              'exitPopupAllowed=no; __utmz=267046603.1697268647.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.1.268263061.1697268648; _hjSessionUser_2635539=eyJpZCI6IjI2MjM5YWE3LTRlNTktNTVlNy05MWRiLTMxNDIzMmI4ZjQyZCIsImNyZWF0ZWQiOjE2OTcyNjg2NDcxNzEsImV4aXN0aW5nIjp0cnVlfQ==; chaport-641d4fe33d8cf5e3c87212b3=9854574b-a06a-423f-b9da-6d23f077f10f%2FkRNJMa6TzVDXU9cDRvk2jaYvzg215bnRKoc; ASP.NET_SessionId=pp2swzl5sozpoxrdbmb1plbw; userCookie=d1026062-1347-4039-9291-d766cb907891; ExitPopup=capsule; LandingPage=pageEntityId=10254655&pageEntityType=1; loginViewCookies=55; TT_ClientTimeZoneOffset=-330; TT_AcceptedCookie=no; __utma=267046603.1080832204.1697268647.1697268647.1699955327.2; __utmc=267046603; __utmt=1; _uetsid=01abe8d082d311eeaa32aba0fe21ae4f; _uetvid=97f3ac906a6311eebb01c9948b3046b9; AWSALB=8ct2wHsdfs+bDEZb3/aEC2Bzzn2IVtAgB0o6KjO9qcs/wonfyV5//JeueHU4yEtjiYM/dh50BOGz4RPIGDJnFpf1iUCGJkYWGfg1WNhilIG0/0qwZY8TCLLqksVr; AWSALBCORS=8ct2wHsdfs+bDEZb3/aEC2Bzzn2IVtAgB0o6KjO9qcs/wonfyV5//JeueHU4yEtjiYM/dh50BOGz4RPIGDJnFpf1iUCGJkYWGfg1WNhilIG0/0qwZY8TCLLqksVr; _ga_QLHY2XP7W3=GS1.1.1699955327.2.0.1699955330.0.0.0; __utmb=267046603.4.9.1699955381099; AWSALB=iL6xo7uhuwkgNIzgShCyDSpm92IbNEYwgYwUpfbcLe9woM2u+RqyC3pcjDq4mF4S7Pkcf4Ol7sIumx1tysYyMhAAqENi7Quc2xkdZxTNMmlv9yDObwq5B46h47CY; AWSALBCORS=iL6xo7uhuwkgNIzgShCyDSpm92IbNEYwgYwUpfbcLe9woM2u+RqyC3pcjDq4mF4S7Pkcf4Ol7sIumx1tysYyMhAAqENi7Quc2xkdZxTNMmlv9yDObwq5B46h47CY; ExitPopup=capsule',
              'dnt':
              '1',
              'if-none-match':
              '""',
              'referer':
              'https://www.transtutors.com/',
              'sec-ch-ua':
              '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
              'sec-ch-ua-mobile':
              '?0',
              'sec-ch-ua-platform':
              '"Linux"',
              'sec-fetch-dest':
              'document',
              'sec-fetch-mode':
              'navigate',
              'sec-fetch-site':
              'same-origin',
              'sec-fetch-user':
              '?1',
              'upgrade-insecure-requests':
              '1',
              'user-agent':
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
          }

          responsed = requests.request("GET",
                                       url,
                                       headers=headers,
                                       data=payload)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)

    #brainly.in
    elif message.content.startswith("https://brainly.in/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?brainly.in/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          payload = {}
          headers = {
              'authority':
              'brainly.in',
              'accept':
              'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
              'accept-language':
              'en-US,en;q=0.9',
              'cache-control':
              'max-age=0',
              'dnt':
              '1',
              'sec-ch-device-memory':
              '8',
              'sec-ch-ua':
              '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
              'sec-ch-ua-arch':
              '"x86"',
              'sec-ch-ua-mobile':
              '?0',
              'sec-ch-ua-model':
              '""',
              'sec-ch-ua-platform':
              '"Linux"',
              'sec-fetch-dest':
              'document',
              'sec-fetch-mode':
              'navigate',
              'sec-fetch-site':
              'none',
              'sec-fetch-user':
              '?1',
              'user-agent':
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
          }

          responsed = requests.request(
              "GET",
              f"http://api.scraperapi.com?api_key=3bba6039d77d63fbcb8c7fea7388c956&url={url}",
              headers=headers,
              data=payload)
          soup = BeautifulSoup(responsed.content, "html.parser")
          file_answer = f"answers_{identifier}.html"
          f = open(file_answer, 'a', encoding='utf-8')
          f.write(soup.prettify())
          f.close()
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        url3 = upload_to_s3(file_answer)
        await send_message_answer(message, url, url3, username)
        os.remove(file_answer)
    #slideshare
    elif message.content.startswith("https://www.slideshare.net/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?slideshare.net/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          existing_tokens = set(
          )  # Assume you're keeping track of generated tokens
          identifier = generate_unique_token(existing_tokens)
          likeapi = "https://slidenxapi.rex699.repl.co/api?url=" + str(url)
          responsed = requests.get(likeapi)
          file_answer = f"answers_{identifier}.pdf"
          with open(file_answer, 'wb') as f:
            f.write(responsed.content)
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
      # send the answers.html to user
      if os.path.exists(file_answer):
        await message.channel.send(file=discord.File(file_answer))
        os.remove(file_answer)

    #scribd
    elif message.content.startswith("https://www.scribd.com/"):
      username = message.author.name
      channel = message.channel.id
      url_list = re.findall(r'(https://(?:www.)?scribd.com/\S+)',
                            message.content)
      print(f'Running {url_list}')
      for url in url_list:
        try:
          identifier = 'scribd'
          match = re.search(r'/(\d+)/', url)
          if match:
            document_number = match.group(1)
            print(document_number)
            file_answer = f"https://www.scribd.com/embeds/{document_number}/content"
            url3 = file_answer
            await send_message_answer(message, url, url3, username)
          else:
            print("Document number not found.")
            await message.channel.send(f"Document not found: {url}")
        except Exception as e:
          print(e)
          await message.channel.send(f"Error: {e}")
    #status      
    elif '/status' in message.content:
      urlstatus = 'https://nx.aba.vg/nxcode/check.php'
      response = requests.get(urlstatus)
      if response.status_code == 200:
        datastau = response.json()
        account = len(datastau)
        for index, datastatus in enumerate(datastau):
          if datastatus in ['RELEASED', 'OK']:
            await message.channel.send(f"Account {index + 1}/{account}: Active ✅")
          elif datastatus in ['BLOCKED', 'WARNED']:
            await message.channel.send(f"Account {index + 1}/{account}: Blocked 🚫")
      else:
          await message.channel.send("Failed to fetch status.")
  #else:
  #if isinstance(message.channel, discord.DMChannel):
  #await message.reply("Nice Try!")


running = False

#keep_alive()
# Use your actual token here, and keep it secret!
client.run(TOKEN)
