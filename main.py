from bs4 import BeautifulSoup
import requests
import textwrap
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

THEME_COLORS = ["#6a2c70", "#b83b5e", "#f08a5d", "#f9ed69"]


def pull_quotes_list_from_website():
    response = requests.get("https://www.positivityblog.com/success-quotes/")
    quotes_page = response.text
    soup = BeautifulSoup(quotes_page, "html.parser")
    all_quotes = soup.find_all(name="p")
    with open("quotes.txt", mode="w") as file:
        for quote in all_quotes:
            file.write(f"{quote.text}\n")


def generate_quote_items(file_path):
    items =[]
    with open(file_path) as file:
        while True:
            quote = file.readline()
            author = file.readline()
            if not quote or not author:
                break
            items.append({'quote': quote, 'author': author})
    return items


def generate_quote_image(q_i, bg_color, days):
    w = 500
    h = 500

    day = datetime.now() + timedelta(days=days)
    day = day.strftime("%Y%m%d")

    quote_font = ImageFont.truetype("Georgia Italic", 30)
    author_font = ImageFont.truetype("Georgia", 15)

    quote_text = "\n".join(textwrap.wrap(q_i['quote'], 30))
    quote_author = q_i['author']

    image = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(image)
    draw.text(
        (w/2, h/2),
        text=quote_text,
        fill="black",
        anchor="mm",
        align="center",
        font=quote_font)

    draw.text(
        (w, h),
        text=quote_author,
        fill="black",
        anchor="rm",
        align="right",
        font=author_font
    )
    #image.show()
    image.save(f"images/{day}.png")


quotes_items = generate_quote_items("quotes.txt")

for i in range(len(quotes_items)):
    generate_quote_image(quotes_items[i], THEME_COLORS[i % len(THEME_COLORS)], i)

