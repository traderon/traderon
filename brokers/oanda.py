import datetime
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts


def oanda_import(api_key, account_ID):
    return_value = []
    params = {"beforeID": 500000, "state": "ALL", "count": 500}
    try:
        r = accounts.AccountList()
        Client = API(environment='live', access_token=api_key)
        Client.request(r)
        for i in r.response['accounts']:
            resp = trades.TradesList(i['id'], params=params)
            tradesList = Client.request(resp)
            for trade in tradesList["trades"]:
                found = False
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
                    if len(appended["subs"]) == 2:
                        sub_1 = appended["subs"][0]
                        sub_2 = appended["subs"][1]
                        if appended['symbol'] == instrument and abs((datetime.datetime.fromisoformat(sub_2['date']) - datetime.datetime.fromisoformat(trade["closeTime"])).total_seconds()) < 600:
                            appended['ret'] = str(
                                float(appended['ret']) + float(trade['realizedPL']))
                            appended['size'] = str(
                                float(appended['size']) + float(trade["initialUnits"]))
                            appended['open_date'] = trade["openTime"]
                            appended['entry'] = trade["price"]
                            if float(appended['ret']) > 0:
                                appended['status'] = "WIN"
                            else:
                                appended['status'] = "LOSS"
                            new_subs = [{"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["openTime"], "size": str(abs(float(trade["initialUnits"]))), "position": str(float(sub_1['position']) + float(trade["initialUnits"])), "price": trade["price"]}, {
                                "action": action_2, "spread": "SINGLE", "type": "FOREX", "date": trade["closeTime"], "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["averageClosePrice"]}]
                            appended['subs'].extend(new_subs)
                            found = True
                            break
                if found == True:
                    continue
                return_value.append(
                    {"account_id": account_ID, "broker": "Oanda", "trade_id": trade["id"], "status": status, "open_date": trade["openTime"], "symbol": instrument, "entry": trade["price"], "exit": trade["averageClosePrice"], "size": trade["initialUnits"], "ret": trade["realizedPL"], "side": side, "setups": "", "mistakes": "", "subs": [{"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["openTime"], "size": str(abs(float(trade["initialUnits"]))), "position": trade["initialUnits"], "price": trade["price"]}, {"action": action_2, "spread": "SINGLE", "type": "FOREX", "date": trade["closeTime"], "size": str(abs(float(trade["initialUnits"]))), "position": "0", "price": trade["averageClosePrice"]}]})
        return {'trades': return_value}
    except Exception as e:
        return {'errors': str(e)}
