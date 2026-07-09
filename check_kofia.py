import requests
import os
import re

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
LAST_ID_FILE = "last_id.txt"

def get_latest_post():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.kofia.or.kr",
    }
    # JSON API로 직접 호출
    url = "https://www.kofia.or.kr/brd/m_212/list.do"
    params = {
        "srchFr": "", "srchTo": "", "srchWord": "",
        "srchTp": "", "itm_seq_1": "0", "itm_seq_2": "0",
        "multi_itm_seq": "0", "company_cd": "", "company_nm": "",
        "page": "1"
    }
    res = requests.get(url, headers=headers, params=params)
    
    # 글번호 패턴 찾기
    nums = re.findall(r'<td class="first[^"]*"[^>]*>\s*(\d+)\s*</td>', res.text)
    titles = re.findall(r'<a href="[^"]*view\.do[^"]*"[^>]*>\s*([^<]+)\s*</a>', res.text)
    
    print(f"찾은 번호들: {nums[:3]}")
    print(f"찾은 제목들: {titles[:3]}")
    
    if nums and titles:
        return nums[0], titles[0].strip()
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
