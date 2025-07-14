import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from dateutil import parser as date_parser
from crypto_report import (
    get_market_data
)

# ------------------ 🧠 News Sentiment ------------------
def label_sentiment(title):
    bullish = ["rally", "surge", "buy", "bull", "gain", "record", "rise", "moon", "pump", "spike"]
    bearish = ["crash", "dump", "sell", "bear", "loss", "decline", "hacked", "rug pull"]
    title = title.lower()
    if any(w in title for w in bullish): return "🟢 Bullish"
    elif any(w in title for w in bearish): return "🔴 Bearish"
    return "⚪ Neutral"

# ------------------ 🗞 News Aggregator ------------------
def get_news(limit_per_source=3):
    feeds = {
        "Cointelegraph": "https://cointelegraph.com/rss",
        "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
        "CryptoSlate": "https://cryptoslate.com/feed/"
    }
    all_news = []
    for source, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit_per_source]:
                pub = entry.get("published", "") or entry.get("updated", "")
                all_news.append({
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "published": pub,
                    "parsed_date": date_parser.parse(pub) if pub else datetime.utcnow()
                })
        except Exception as e:
            print(f"[ERROR] {source}: {e}")
    return sorted(all_news, key=lambda x: x["parsed_date"], reverse=True)

# ------------------ 💡 Buy/Sell Signal Table ------------------
def get_signal_table(df):
    signals = []
    for _, row in df.iterrows():
        change = row['price_change_percentage_24h']
        if change > 3:
            action, reason = "🟢 BUY", "Strong momentum"
        elif change < -2:
            action, reason = "🔴 SELL", "Price drop"
        else:
            action, reason = "⚪ HOLD", "Stable"
        signals.append({
            "Coin": row['name'],
            "Action": action,
            "24h Change": f"{change:.2f}%",
            "Reason": reason
        })
    return pd.DataFrame(signals)

# ------------------ 🎛 Streamlit Page Setup ------------------
st.set_page_config(page_title="Crypto Lab", layout="wide")
st.title("📊 Real-Time Crypto Market Dashboard")
st.caption("Live data from CoinGecko, CoinDesk, Cointelegraph & CryptoSlate")

# ------------------ 📈 Market Data ------------------
try:
    df = get_market_data()
except Exception as e:
    st.error(f"Failed to fetch market data: {e}")
    st.stop()

# ------------------ 🔝 Top 10 Coins ------------------
st.subheader("🔹 Top 10 by Market Cap")
st.dataframe(df[["name", "symbol", "current_price", "price_change_percentage_24h"]], use_container_width=True)

# ------------------ 🚀 Gainers & Losers ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Top Gainers (24h)")
    top_gainers = df.sort_values("price_change_percentage_24h", ascending=False).head(3)
    st.table(top_gainers[["name", "current_price", "price_change_percentage_24h"]])

with col2:
    st.subheader("🔻 Top Losers (24h)")
    top_losers = df.sort_values("price_change_percentage_24h", ascending=True).head(3)
    st.table(top_losers[["name", "current_price", "price_change_percentage_24h"]])

# ------------------ 🗞 News & Sentiment ------------------
st.subheader("🗞️ Crypto Headlines + Sentiment")
for item in get_news():
    sentiment = label_sentiment(item["title"])
    st.markdown(
        f"**{item['title']}**  \n*{sentiment} — {item['source']} – {item['published']}*  \n[🔗 Read more]({item['link']})\n",
        unsafe_allow_html=True
    )

# ------------------ 💡 Signal Table ------------------
st.subheader("💡 Buy/Sell Signals")
st.dataframe(get_signal_table(df), use_container_width=True)

