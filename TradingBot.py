
!pip install alpaca-trade-api
import alpaca_trade_api as tradeapi
APCA_API_KEY_ID = "X"
APCA_API_SECRET_KEY = "X"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

account = api.get_account()
print(account)
