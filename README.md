# 🧠 Crypto Lab — Real-Time Crypto Market Dashboard

Welcome to **Crypto Lab** — a real-time cryptocurrency dashboard built with [Streamlit](https://streamlit.io), powered by:

- 🦎 [**CoinGecko API**](https://www.coingecko.com/en/api) — for live market data  
- 📰 [**CoinDesk**](https://www.coindesk.com/), [**CoinTelegraph**](https://cointelegraph.com/), and [**CryptoSlate**](https://cryptoslate.com/) — for crypto news aggregation

🔗 **Live App**: [https://crypto-lab-j9mhwjdqrxrtmqcti6xxuv.streamlit.app](https://crypto-lab-j9mhwjdqrxrtmqcti6xxuv.streamlit.app/)  
📊 **Built with**: Python • Streamlit • Pandas • Matplotlib • RSS

---

## ✨ Features

- 🔹 **Top 10 Coins** by market cap (live prices and 24h % change)
- 🚀 **Top Gainers & Losers** (24h price movers)
- 💡 **Buy/Sell/Hold Signals** based on price performance
- 🗞️ **News Aggregator** with sentiment detection from:
  - CoinTelegraph  
  - CoinDesk  
  - CryptoSlate  

---

## 🛠️ Local Setup

1. **Clone the repo:**

   ```bash
   git clone https://github.com/alexehrich/crypto-lab.git
   cd crypto-lab
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**

   ```bash
   streamlit run dashboard.py
   ```

---

## 📬 Feedback / Contributions

This is a side project — feel free to fork, submit issues, or open pull requests. Contributions and feedback are very welcome!

---

## 📄 License

MIT License. Use freely for personal or educational projects. Attribution appreciated.
