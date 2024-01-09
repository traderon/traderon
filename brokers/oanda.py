import requests
import datetime

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
            found_pair = False
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
            for appended in return_value:
                subtrade = appended["sub_2"]
                subtrade_0 = appended["sub_1"]
                if appended['symbol'] == instrument and abs((datetime.datetime.fromisoformat(
                        subtrade['date']) - datetime.datetime.fromisoformat(trade["closeTime"])).total_seconds()) < 3600:
                    found_pair = True
                    appended['ret'] = str(
                        float(appended['ret']) + float(trade['realizedPL']))
                    appended['size'] = str(
                        float(appended['size']) + float(trade["initialUnits"]))
                    appended['sub_3'] = {"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["openTime"], "size": str(
                        abs(float(trade["initialUnits"]))), "position": str(float(subtrade_0['position']) + float(trade["initialUnits"])), "price": trade["price"]}
                    appended['sub_4'] = {"action": action_2, "spread": "SINGLE", "type": "FOREX", "date": trade["closeTime"], "size": str(
                        abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["averageClosePrice"]}
                    break
                else:
                    continue
            if found_pair == False:
                return_value.append(
                    {"account_id": account_ID, "broker": "Oanda", "trade_id": trade["id"], "status": status, "open_date": trade["openTime"], "symbol": instrument, "entry": trade["price"], "exit": trade["averageClosePrice"], "size": trade["initialUnits"], "ret": trade["realizedPL"], "side": side, "setups": "", "mistakes": "", "sub_1": {"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["openTime"], "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["price"]}, "sub_2": {"action": action_2, "spread": "SINGLE", "type": "FOREX", "date": trade["closeTime"], "size": str(abs(float(trade["initialUnits"]))), "position": "0", "price": trade["averageClosePrice"]}})
        return return_value
    except Exception as e:
        return e
