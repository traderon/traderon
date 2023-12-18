import requests

base_url = "https://api-fxtrade.oanda.com/v3/accounts/"
params = "//trades?state=CLOSED&count=500"


def oanda_import(api_key, account_ID):
    try:
        url = base_url + account_ID + params
        token = 'Bearer ' + api_key
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        res = requests.get(url=url, headers=headers)
        trades = (res.json())["trades"]
        return_value = []
        for trade in trades:
            if float(trade["realizedPL"]) > 0:
                status = "WIN"
            else:
                status = "LOSS"
            if "takeProfitOrder" not in trade:
                side = "UNKNOWN"
            else:
                takeProfitOrder = trade["takeProfitOrder"]
                if float(trade["price"]) > float(takeProfitOrder["price"]):
                    side = "SHORT"
                else:
                    side = "LONG"
            if "takeProfitOrder" not in trade:
                action = "UNKNOWN"
            else:
                takeProfitOrder = trade["takeProfitOrder"]
                if float(trade["price"]) > float(takeProfitOrder["price"]):
                    action = "Sell"
                else:
                    action = "Buy"
            if "stopLossOrder" in trade:
                stopLossOrder = trade["stopLossOrder"]
                price = stopLossOrder["price"]
                if "filledTime" in stopLossOrder:
                    date = stopLossOrder["filledTime"]
                else:
                    date = stopLossOrder["cancelledTime"]
            else:
                date = "UNKNOWN"
                price = "NO STOPLOSS"
            return_value.append(
                {"account_id": account_ID, "broker": "Oanda", "trade_id": trade["id"], "status": status, "open_date": trade["openTime"], "symbol": trade["instrument"], "entry": trade["price"], "exit": trade["averageClosePrice"], "size": trade["initialUnits"], "ret": trade["realizedPL"], "side": side, "setups": "", "mistakes": "", "sub_1": {"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["openTime"], "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["price"]}, "sub_2": {"action": action, "spread": "SINGLE", "type": "FOREX", "date": date, "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": price}})
        return return_value
    except Exception as e:
        return e
