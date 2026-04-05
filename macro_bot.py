import os
import requests
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv("telegram.env")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ── 重大事件行事曆（自己維護，格式 MM-DD）──────────────────────
IMPORTANT_EVENTS = {
    "04-07": "🇺🇸 美國 CPI 公布",
    "04-08": "🏦 Fed Williams 演講",
    "04-10": "🇹🇼 台灣央行理監事會議",
    "05-01": "🇺🇸 FOMC 利率決議",
    "05-14": "🇺🇸 美國 CPI 公布",
    "05-22": "🇺🇸 美國 GDP 初值",
    "06-05": "🇺🇸 非農就業報告",
}

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": str(CHAT_ID),
        "text": message,
        "parse_mode": "HTML",
    }
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        print(f"發送失敗：{resp.text}")
    else:
        print("✅ 訊息發送成功")

def get_ticker(symbol: str, label: str):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="2d")
        if len(hist) < 2:
            return f"{label}: 無法取得"
        prev_close = hist["Close"].iloc[-2]
        last_close = hist["Close"].iloc[-1]
        change_pct = (last_close - prev_close) / prev_close * 100
        arrow = "▲" if change_pct >= 0 else "▼"
        return f"{label}: {last_close:.2f}（{arrow}{abs(change_pct):.2f}%）"
    except Exception as e:
        return f"{label}: 錯誤（{e}）"

def check_events_today():
    today_str = datetime.now().strftime("%m-%d")
    events = []
    for date_key, event in IMPORTANT_EVENTS.items():
        if date_key == today_str:
            events.append(f"  ⚠️ 今日：{event}")
    upcoming = []
    for i in range(1, 8):
        future = (datetime.now() + timedelta(days=i)).strftime("%m-%d")
        if future in IMPORTANT_EVENTS:
            upcoming.append(f"  📅 {future}：{IMPORTANT_EVENTS[future]}")
    return events, upcoming

def build_report():
    today = datetime.now().strftime("%Y/%m/%d")
    lines = [f"📊 <b>總經早報 {today}</b>\n"]

    # 匯率 & 美元
    lines.append("💱 <b>匯率</b>")
    lines.append(get_ticker("TWD=X",    "💵 USD/TWD"))
    lines.append(get_ticker("EURUSD=X", "💶 EUR/USD"))
    lines.append(get_ticker("DX-Y.NYB", "🦅 美元指數(DXY)"))
    lines.append("")

    # 美股指數
    lines.append("📈 <b>美股指數</b>")
    lines.append(get_ticker("^GSPC",  "🇺🇸 S&P 500"))
    lines.append(get_ticker("^NDX",   "💻 Nasdaq 100"))
    lines.append(get_ticker("^SOX",   "🔬 費城半導體"))
    lines.append(get_ticker("^VIX",   "😱 VIX 恐慌指數"))
    lines.append("")

    # 台股
    lines.append("🇹🇼 <b>台股</b>")
    lines.append(get_ticker("^TWII",  "🇹🇼 台灣加權"))
    lines.append(get_ticker("TSM",    "🏭 台積電 ADR(TSM)"))
    lines.append("")

    # 債券
    lines.append("🏦 <b>債券</b>")
    lines.append(get_ticker("TLT",    "📉 美債ETF(TLT)"))
    lines.append(get_ticker("^IRX",   "⏱️ 美3月債殖利率"))
    lines.append("")

    # 能源 & 原物料
    lines.append("⛏️ <b>原物料</b>")
    lines.append(get_ticker("USO",    "🛢️ WTI 油價(USO)"))
    lines.append(get_ticker("UNG",    "🔥 天然氣(UNG)"))
    lines.append(get_ticker("GLD",    "🥇 黃金(GLD)"))
    lines.append(get_ticker("CPER",   "🔩 銅(CPER)"))
    lines.append("")

    # 運費
    lines.append("🚢 <b>運費</b>")
    lines.append(get_ticker("BDRY",   "⚓ 乾散貨ETF(BDRY)"))
    lines.append(get_ticker("ZIM",    "📦 貨櫃航運(ZIM)"))
    lines.append(get_ticker("MATX",   "🚤 貨櫃航運(MATX)"))
    lines.append("")

    # 重大事件
    today_events, upcoming_events = check_events_today()
    if today_events:
        lines.append("🔔 <b>今日重大事件：</b>")
        lines.extend(today_events)
        lines.append("")
    if upcoming_events:
        lines.append("📅 <b>近7日事件：</b>")
        lines.extend(upcoming_events)

    return "\n".join(lines)

if __name__ == "__main__":
    report = build_report()
    print(report)
    send_telegram(report)
