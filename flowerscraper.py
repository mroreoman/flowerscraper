import requests
from bs4 import BeautifulSoup
import csv
import unicodedata

page = requests.get("https://www.epicgardening.com/types-of-flowers/")
soup = BeautifulSoup(page.content, "html.parser")

flowers = []

names = soup.find_all("h2", class_="wp-block-heading")

for i in range(len(names) - 1):
    name = names[i]
    pic = name.find_next("figure")
    sci = pic.find_next("p")
    desc = sci.find_next("p")
    
    flowers.append({
        "name": name.get_text().strip(),
        "pic": pic.img["src"],
        "sci": sci.get_text()[17::].strip(),
        "desc": desc.get_text().strip()
    })

    if i == 190:
        flowers[-1]["desc"] += desc.find_next("p").get_text().strip()

fields = ["name", "pic", "sci", "desc"]
with open('test.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(flowers)