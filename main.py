import os, requests, time
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
CHAT_ID = os.getenv("CHAT_ID")
PAIRS = ["STEEM", "TRX", "XRP", "XLM", "ATOM", "DASH", "XNO"]
MIN_MARGIN = 0.02
SLEEP = 300

EXCHANGES = {
  "MEXC": lambda p: float(requests.get(
      f"https://www.mexc.com/open/api/v2/market/ticker?symbol={p}usdt").json()['data'][0]['lastPrice']),
  "CoinEx": lambda p: float(requests.get(
      f"https://api.coinex.com/v1/market/ticker?market={p}usdt").json()['data']['ticker']['last']),
  "KuCoin": lambda p: float(requests.get(
      f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={p}-USDT").json()['data']['price'])
}

def check_pair(p):
    try:
        buy = EXCHANGES["MEXC"](p)
        for name, get_price in EXCHANGES.items():
            if name == "MEXC": continue
            sell = get_price(p)
            margin = (sell - buy) / buy
            if margin >= MIN_MARGIN:
                bot.send_message(
                    CHAT_ID,
                    f"✅ {p}: MEXC → {name} margen = {margin*100:.2f}%"
                )
    except Exception as e:
        print(f"Error en {p}: {e}")

if __name__ == "__main__":
    while True:
        for p in PAIRS:
            check_pair(p)
        time.sleep(SLEEP)
