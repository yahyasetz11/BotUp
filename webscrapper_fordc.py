import time
import os
import requests

import discord
import asyncio
from discord.ext import commands

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Masukkan token bot dari Discord Developer Portal
TOKEN = "MTMzOTM3MDkwMTI5NjEyMzkyNA.GTwi9T.JOiKEhaW6V3eFHjGRUWsP8hWE8PmYO-O65mdXM"

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fungsi untuk scraping gambar
def scrape_images():
    # Setup WebDriver
    # Gunakan WebDriver Manager untuk otomatis download ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://sakurazaka46.com/s/s46/diary/detail/58786?ima=0000&cd=blog")
    print(driver.title)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
    images = driver.find_elements(By.TAG_NAME, "img")

    image_urls = []
    for img in images:
        src = img.get_attribute('src')
        print(f'Requesting Pict {img} from {src}')
        if src and "mob" in src.split("/")[-1]:
            image_urls.append(src)
            
    
    driver.quit()
    return image_urls

@bot.event
async def on_ready():
    print(f"Bot telah login sebagai {bot.user}")

# Command untuk bot
@bot.command()
async def scrape(ctx):
    # Mulai proses scraping
    await ctx.send("Scraping images... Please wait.")
    
    image_urls = scrape_images()
    
    if image_urls:
        await ctx.send(f"Found {len(image_urls)} images!")
        for url in image_urls:
            await ctx.send(url)  # Kirimkan URL gambar satu per satu
    else:
        await ctx.send("No images found.")

# Run bot
bot.run(TOKEN)