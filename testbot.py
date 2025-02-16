import discord
import os
import configparser

# Baca config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Ambil token dari config.ini
TOKEN = config["DISCORD"]["TOKEN"]

# Inisialisasi bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Perhatikan ini untuk akses ke isi pesan
intents.guilds = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot telah login sebagai {bot.user}")

@bot.event
async def on_message(message):
    print(f"Menerima pesan: {repr(message.content)} dari {message.author}")  # Gunakan repr untuk melihat karakter tersembunyi

    if message.author == bot.user:
        return

    if message.content.lower() == "halo bot":
        print("Menerima pesan halo bot!")
        await message.channel.send("Halo! Aku siap bekerja 🚀")




# Jalankan bot
bot.run(TOKEN)
