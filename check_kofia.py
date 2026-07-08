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
        cols = row.find_all("td")
        if len(cols) >= 2:
            num = cols[0].get_text(strip=True)
            title_a = cols[1].find("a")
            if num.isdigit() and title_a:
                title = title_a.get_text(strip=True)
                return num, title
    return None, None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

num, title = get_latest_post()
print(f"최신 글: {num} - {title}")

if num:
    try:
        with open(LAST_ID_FILE, "r") as f:
            last = f.read().strip()
    except:
        last = ""
    
    print(f"저장된 마지막 ID: {last}")
    
    if num != last:
        send_telegram(f"📢 KOFIA 새 글!\n{title}\nhttps://www.kofia.or.kr/brd/m_212/list.do")
        with open(LAST_ID_FILE, "w") as f:
            f.write(num)
        print(f"새 글 발견 및 저장: {num}")
    else:
        print("새 글 없음")
