import yfinance as yf
import datetime
import os

# 추적할 항목 설정 (티커: 이름)
STOCKS = {
    "^KS11": "코스피 (KOSPI)",
    "^GSPC": "S&P 500",
    "USDKRW=X": "원-달러 환율 (USD/KRW)",
    "^VKOSPI": "KVIX (공포 지수)"
}

def get_stock_data():
    summary = ""
    for ticker, name in STOCKS.items():
        try:
            data = yf.Ticker(ticker)
            # 데이터를 5일치로 넉넉히 가져와서 시차/휴장일 누락 방지
            info = data.history(period="5d")
            
            if len(info) < 2:
                summary += f"- **{name}**: 데이터 로드 지연 (영업일 기준 2일치 확보 불가)\n"
                continue

            current_val = info['Close'].iloc[-1]
            prev_val = info['Close'].iloc[-2]
            change = ((current_val - prev_val) / prev_val) * 100
            
            # 항목별 맞춤형 아이콘 및 단위 설정
            if "환율" in name:
                icon = "💸" if change > 0 else "📉"
                unit = "원"
            elif "공포 지수" in name:
                icon = "⚠️" if change > 0 else "✅"
                unit = "pt"
            else:
                icon = "🔺" if change > 0 else "🔹"
                unit = "pt"
                
            summary += f"- **{name}**: {current_val:,.2f}{unit} ({icon} {change:+.2f}%)\n"
        except Exception as e:
            summary += f"- **{name}**: 데이터 로드 실패\n"
            
    return summary

def create_post(stock_summary):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    date_str = now.strftime("%Y-%m-%d")
    file_name = f"_posts/{date_str}-daily-market-scan.md"
    
    content = f"""---
title: "[{date_str}] 증시 시황: 환율 및 공포 지수 체크"
date: {now.strftime("%Y-%m-%d %H:%M:%S +0900")}
categories: [재테크]
tags: [KOSPI, SP500, 환율, KVIX]
---

### 📈 시장 주요 지표 요약
오늘의 국내외 증시 및 주요 경제 지표 현황입니다.

{stock_summary}

---
#### 💡 오늘의 관전 포인트
- **환율**: 환율이 급격히 오르면 외국인 자금이 빠져나갈 수 있으니 주의하세요.
- **KVIX**: 이 지수가 급등한다면 시장 참여자들이 불안해하고 있다는 신호입니다.

*본 포스팅은 깃허브 로봇에 의해 자동 작성되었습니다.*
"""
    os.makedirs("_posts", exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    result = get_stock_data()
    create_post(result)
