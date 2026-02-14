"""
Quick test to verify TGDĐ is scrapable
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.thegioididong.com/dtdd/iphone-14-pro-max-512gb"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "vi-VN,vi;q=0.9",
}

print(" Testing TGDĐ...\n")

response = requests.get(url, headers=headers, timeout=10)

print(f"Status Code: {response.status_code}")
print(f"Response Size: {len(response.content)} bytes")

if response.status_code != 200:
    print(" Request failed")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Title
title = soup.select_one("h1")
print("Title:", title.text.strip() if title else "NOT FOUND")

# Current price
price = soup.select_one(".box-price-present")
print("Current price:", price.text.strip() if price else "NOT FOUND")

# Old price
old_price = soup.select_one(".box-price-old")
print("Old price:", old_price.text.strip() if old_price else "No discount")

