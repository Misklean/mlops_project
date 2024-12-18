import aiohttp
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv("WEBSERVICE_URL", "http://webservice:5000")  # Default to http://webservice:5000
API_URL = f"{URL}/generate-image"  # Set the API endpoint URL

# Set up Discord client
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# API authorization token
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGVtbyIsImlhdCI6MTY5MzY2NjY2Nn0._sCx6DJMKvhG6Dp9tcDw2q8P7TXqEwnCX7H8CfM0OsE"

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Event when the bot receives a message
@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author.bot:
        return

    # Check if the bot is mentioned in the message
    if bot.user in message.mentions:
        user_input = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if not user_input:
            await message.channel.send("Please provide a prompt.")
            return

        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"prompt": user_input}

        try:
            # Use aiohttp for async HTTP request
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, headers=headers, json=payload) as response:
                    if response.status == 200:
                        # Read the image content
                        image_bytes = BytesIO(await response.read())
                        image_bytes.seek(0)

                        # Send the image to the Discord channel
                        await message.channel.send(
                            content=f"{message.author.mention}, here's your image!",
                            file=discord.File(image_bytes, filename="generated_image.png")
                        )
                    else:
                        # Handle non-200 status codes
                        response_text = await response.text()
                        await message.channel.send(
                            f"Sorry {message.author.mention}, I couldn't generate the image. "
                            f"Error: {response.status} - {response_text}"
                        )
        except Exception as e:
            await message.channel.send(
                f"An error occurred while processing your request, {message.author.mention}. Please try again later."
            )
            print(f"Error: {e}")

    # Allow the bot to process commands
    await bot.process_commands(message)

# Run the bot
bot.run(DISCORD_TOKEN)