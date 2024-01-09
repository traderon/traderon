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
            if float(trade["realizedPL"]) == 0:
                continue
            else:
                if float(trade["realizedPL"]) > 0:
                    status = "WIN"
                else:
                    status = "LOSS"
            instrument = '$' + trade['instrument'].replace('_', '')
            if not 'averageClosePrice' in trade:
                continue
            if float(trade['realizedPL']) > 0:
                if float(trade['price']) > float(trade['averageClosePrice']):
                    side = "SHORT"
                else:
                    side = "LONG"
            else:
                if float(trade['price']) < float(trade['averageClosePrice']):
                    side = "SHORT"
                else:
                    side = "LONG"
            if side == 'LONG':
                action = 'Buy'
                action_2 = 'Sell'
            else:
                action = 'Sell'
                action_2 = 'Buy'
            return_value.append(
                {"account_id": account_ID, "broker": "Oanda", "trade_id": trade["id"], "status": status, "open_date": trade["openTime"], "symbol": instrument, "entry": trade["price"], "exit": trade["averageClosePrice"], "size": trade["initialUnits"], "ret": trade["realizedPL"], "side": side, "setups": "", "mistakes": "", "sub_1": {"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["openTime"], "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["price"]}, "sub_2": {"action": action_2, "spread": "SINGLE", "type": "FOREX", "date": trade["closeTime"], "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["averageClosePrice"]}})
        return return_value
    except Exception as e:
        return e
