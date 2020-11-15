from datetime import *
import pybithumb

from BasicPractice.BitumbOfficialSampleCode.key_file import my_api_key, my_api_secret
from BasicPractice.BitumbOfficialSampleCode.xcoin_api_client import *

api_key = my_api_key;
api_secret = my_api_secret;

bithumb = pybithumb.Bithumb(api_key, api_secret)

# api = XCoinAPI(api_key, api_secret);
#
# rgParams = {
# 	"order_currency" : "BTC",
# 	"payment_currency" : "KRW"
# };
#
#
# #
# # public api
# #
# # /public/ticker
# # /public/recent_ticker
# # /public/orderbook
# # /public/recent_transactions
#
# result = api.xcoinApiCall("/public/ticker", rgParams);
# print("status: " + result["status"]);
# print("last: " + result["data"]["closing_price"]);
#
# #
# # private api
# #
# # endpoint		=> parameters
# # /info/current
# # /info/account
# # /info/balance
# # /info/wallet_address
#
# #result = api.xcoinApiCall("/info/account", rgParams);
# #print("status: " + result["status"]);
# #print("created: " + result["data"]["created"]);
# #print("account id: " + result["data"]["account_id"]);
# #print("trade fee: " + result["data"]["trade_fee"]);
# #print("balance: " + result["data"]["balance"]);
#
# sys.exit(0);
#
