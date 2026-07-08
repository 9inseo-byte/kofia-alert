import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
LAST_ID_FILE = "last_id.txt"

def get_latest_post():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get("https://www.kofia.or.kr/brd/m_212/list.do", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table tbody tr")
    for row in rows:
        num_td = row.select_one("td.first")
        title_a = row.select_one("td a")
        if num_td and title_a:
            num = num_td.get_text(strip=True)
            title = title_a.get_text(strip=True)
            return num, title
    return None, None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

num, title = get_latest_post()
if num:
    try:
        with open(LAST_ID_FILE, "r") as f:
            last = f.read().strip()
    except:
        last = ""
    if num != last:
        send_telegram(f"📢 KOFIA 새 글!\n{title}\nhttps://www.kofia.or.kr/brd/m_212/list.do")
        with open(LAST_ID_FILE, "w") as f:
            f.write(num)
        print(f"새 글 발견: {title}")
    else:
        print("새 글 없음")
