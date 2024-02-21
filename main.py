import os
import discord
import openai

with open("chat.txt","r") as f:
  chat = f.read()
chat = ""
# Set your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Get your Discord bot token
token = os.environ.get("SECRET_KEY")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}\n"
        try:
            print(f'Message from {message.author}: {message.content}')
            print(message.mentions)
            if self.user != message.author and self.user in message.mentions:
                channel = message.channel
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"{chat}\nGirijaGPT: ",
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                message_to_send = response.choices[0].text
                await channel.send(message_to_send)
        except Exception as e:
            print(f"An error occurred: {e}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
