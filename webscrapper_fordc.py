import time
import os
import requests

import discord
import asyncio
from discord.ext import commands

from googletrans import Translator

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import configparser

# Baca config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Ambil token dari config.ini
TOKEN = config["DISCORD"]["TOKEN"]

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fungsi untuk scraping gambar untuk sakamichi
def sakamichi_scrape_and_translate(url, category):
    # Setup WebDriver
    # Gunakan WebDriver Manager untuk otomatis download ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
            return f"⚠️ Gagal mengakses halaman. Status Code: {response.status_code}"

    driver.get(url)
    print(driver.title)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
    images = driver.find_elements(By.TAG_NAME, "img")

    image_urls = []
    if category == "-sakamichi":
        for img in images:
            src = img.get_attribute('src')
            print(f'Requesting Pict {img} from {src}')
            if src and "mob" in src.split("/")[-1]:
                image_urls.append(src)
    elif category == "-bokuao":
        for img in images:
            src = img.get_attribute('src')
            print(f'Requesting Pict {img} from {src}')
            if src and src.lower().endswith(".jpeg"):
                image_urls.append(src)
    else:
        return f"⚠️ Argumen salah, saat ini hanya tersedia kategori -sakamichi dan -bokuao"
    
    # Mengambil teks di halaman untuk diterjemahkan
    # text_elements = driver.find_elements(By.XPATH, '//p')  # Cari elemen <p> (paragraf)
    # text_content = ' '.join([elem.text for elem in text_elements])
    
    # translated_text = translate_text(text_content, 'id')  # Terjemahkan ke bahasa Indonesia
            
    driver.quit()
    return image_urls #, translated_text

# Fungsi untuk translate text
def translate_text(text, dest_lang='id'):  # Default ke bahasa Indonesia
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

def split_text(text, max_length=1000):
    """Membagi teks panjang menjadi beberapa bagian dengan batas karakter tertentu."""
    parts = []
    while len(text) > max_length:
        split_index = text.rfind(" ", 0, max_length)  # Coba pecah di spasi terdekat
        if split_index == -1:  # Jika tidak ada spasi, potong langsung
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].strip()
    parts.append(text)  # Tambahkan bagian terakhir
    return parts


@bot.event
async def on_ready():
    print(f"Bot telah login sebagai {bot.user}")

# Command untuk translate
@bot.command()
async def translate(ctx, lang: str, *, text: str):
    translated_text = translate_text(text, lang)
    text_parts = split_text(translated_text)
    for part in text_parts:
        await ctx.send(part)

# Command untuk bot
@bot.command()
async def scrape(ctx, category: str, url: str):
    # Mulai proses scraping
    await ctx.send(f"Scraping images from {url} with category {category} ... Please wait.")
    image_urls = sakamichi_scrape_and_translate(url, category)
    # image_urls, translated_text = sakamichi_scrape_and_translate(url)
    
    if image_urls:
        await ctx.send(f"Found {len(image_urls)} images!")
        #   text_parts = split_text(translated_text)
        #   for part in text_parts:
        #       await ctx.send(part)
        for url in image_urls:
            await ctx.send(url)  # Kirimkan URL gambar satu per satu
    else:
        await ctx.send("No images found.")

# Run bot
bot.run(TOKEN)