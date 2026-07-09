import requests
import os
import re

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
LAST_ID_FILE = "last_id.txt"

def get_latest_post():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    res = requests.get("https://www.kofia.or.kr/brd/m_212/list.do", headers=headers)
    
    # 번호 찾기
    nums = re.findall(r'<td class="first[^"]*"[^>]*>\s*(\d+)\s*</td>', res.text)
    
    # 제목 링크 찾기 - 다양한 패턴 시도
    titles = re.findall(r'<a[^>]+href[^>]+>\s*\[?([^\[<]{5,}?)\s*</a>', res.text)
    titles = [t.strip() for t in titles if len(t.strip()) > 5 and 'function' not in t]
    
    print(f"찾은 번호들: {nums[:3]}")
    print(f"찾은 제목들: {titles[:3]}")
    
    if nums:
        title = titles[0] if titles else "제목 없음"
        return
