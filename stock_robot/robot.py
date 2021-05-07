import asyncio
import websockets
import requests
from csv import DictReader
from io import StringIO


HTTP_PROTOCOL = "http://"
WS_PROTOCOL = "ws://"
HOSTNAME = "some-webchat:5000"
LOGIN_ENDPOINT = "/login/bots"
CHAT_ENDPOINT = "/ws/chat"
BOT_NAME = "operator"
BOT_PASSWORD = "ChangeItn0w!"


def get_stock_quote(stock_code):
    if not stock_code or len(stock_code) == 0:
        return None
    r = requests.get(f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h&e=csv​")

    s = StringIO(r.content.decode("UTF8"))
    c = DictReader(s)
    result = list(c)[0]

    if result["Close"] != "N/D":
        stock = result["Symbol"]
        quote = result["Close"]
        msg = f"{stock} quote is ${float(quote):.2f} per share"
    else:
        msg = f"Stock {stock_code} not found"
    return msg


def receive_msg(msg):
    result = None
    if msg and msg.find("/stock=") >= 0:
        stock_code = msg.split("=")[1]
        result = get_stock_quote(stock_code)

    return result


def get_token():
    data = {"username": BOT_NAME, "password": BOT_PASSWORD}
    url = HTTP_PROTOCOL + HOSTNAME + LOGIN_ENDPOINT
    result = requests.post(url, data=data)
    return result.content.decode("UTF-8")[1:-1]


async def listen():
    token = get_token()
    uri = WS_PROTOCOL + HOSTNAME + CHAT_ENDPOINT + "?token=" + token

    async with websockets.connect(uri) as ws:
        await ws.send("Hello!")
        while True:
            msg = await ws.recv()
            result = receive_msg(msg)
            if result:
                await ws.send(result)


asyncio.get_event_loop().run_until_complete(listen())
