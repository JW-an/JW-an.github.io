import requests
import datetime
import os

# 깃허브 금고에서 열쇠를 꺼내옵니다
API_KEY = os.environ.get('NEWS_API_KEY')
QUERY = "S&P500" # 관심 있는 키워드로 바꾸세요 (예: 주식, 부동산, 육아 등)

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q={QUERY}&sortBy=publishedAt&apiKey={API_KEY}&language=ko"
    response = requests.get(url).json()
    return response.get('articles', [])[:5] # 최신 뉴스 5개만 가져오기

def create_post(articles):
    if not articles:
        return
    
    now = datetime.datetime.now() + datetime.timedelta(hours=9) # 한국 시간 기준
    date_str = now.strftime("%Y-%m-%d")
    file_name = f"_posts/{date_str}-daily-news.md"

    content = f"""---
title: "[{date_str}] 오늘의 주요 뉴스 요약"
date: {now.strftime("%Y-%m-%d %H:%M:%S +0900")}
categories: [뉴스]
tags: [자동포스팅, {QUERY}]
---

### 📰 오늘의 {QUERY} 관련 주요 뉴스

"""
    for art in articles:
        content += f"- **[{art['title']}]({art['url']})**\n  > {art['description'][:100]}...\n\n"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    news = fetch_news()
    create_post(news)
