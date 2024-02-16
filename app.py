import os
import jwt
import uuid
import stripe
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from brokers.oanda import oanda_import
from brokers.metatrader import metatrader_import

load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY")
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
# print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(200))
    membership = db.Column(db.String(10))
    paydate = db.Column(db.DateTime, default=datetime.utcnow())


class Trades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    account_id = db.Column(db.String(30))
    broker = db.Column(db.String(20))
    trade_id = db.Column(db.String(20))
    status = db.Column(db.String(5))
    open_date = db.Column(db.String(50))
    symbol = db.Column(db.String(20))
    entry = db.Column(db.String(20))
    exit = db.Column(db.String(20))
    size = db.Column(db.String(20))
    pips = db.Column(db.String(20))
    ret_pips = db.Column(db.String(30))
    ret = db.Column(db.String(20))
    ret_percent = db.Column(db.String(20))
    ret_net = db.Column(db.String(20))
    side = db.Column(db.String(10))
    setups = db.Column(db.String(100))
    mistakes = db.Column(db.String(100))


class SubTrades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    trade_id = db.Column(db.String(20))
    action = db.Column(db.String(10))
    spread = db.Column(db.String(10))
    type = db.Column(db.String(10))
    date = db.Column(db.String(50))
    size = db.Column(db.String(20))
    position = db.Column(db.String(20))
    price = db.Column(db.String(20))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({'error': 'a valid token is missing'})
        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = Users.query.filter_by(
                public_id=data['public_id']).first()
            if current_user is None:
                return jsonify({'error': 'Unauthorized'})
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorated


def sort_by_date(dic):
    return dic.open_date


@app.route("/")
def testRoute():
    return "HELLO, this is a test. server working!!!"


@app.route("/api/user/register", methods=["POST"])
def register_user():
    data = request.json
    check_email = Users.query.filter_by(email=data['email']).first()
    if check_email:
        return jsonify({"email": "Email already exists"}), 400
    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256')
    new_user = Users(public_id=str(uuid.uuid4(
    )), firstname=data['firstname'], lastname=data['lastname'], password=hashed_password, email=data['email'], membership='trial')
    db.session.add(new_user)
    db.session.commit()
    token = jwt.encode({'public_id': new_user.public_id, 'email': new_user.email, 'membership': 'trial', 'expired': 0, 'iat': datetime.utcnow(), 'exp': datetime.utcnow(
    ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
    return jsonify({"success": True, "token": "Bearer " + str(token)})


@app.route("/api/user/login", methods=["POST"])
def login_user():
    data = request.json
    user = Users.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"email": "User not found"}), 400
    if check_password_hash(user.password, data['password']):
        if user.membership == 'trial':
            expireday = 7
        else:
            expireday = 30
        if user.paydate + timedelta(days=expireday) > datetime.utcnow():
            expired = 0
        else:
            expired = 1
        token = jwt.encode({'public_id': user.public_id, 'email': user.email, 'membership': user.membership, 'expired': expired, 'iat': datetime.utcnow(), 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({"success": True, "token": "Bearer " + str(token)})
    else:
        return jsonify({"password": "Incorrect password"}), 400


@app.route("/api/user/current", methods=["GET"])
@token_required
def get_current_user(current_user):
    user = Users.query.filter_by(email=current_user.email).first()
    return jsonify({"id": user.public_id, "email": user.email, "firstname": user.firstname, "lastname": user.lastname, "membership": user.membership, "paydate": user.paydate})


@app.route("/api/import_trades", methods=["POST"])
def import_trades():
    tokens = request.json
    broker = tokens["broker"]
    if broker == "Oanda":
        imported_trades = oanda_import(tokens["key"], tokens["id"])
    if broker == "Metatrader":
        imported_trades = metatrader_import(
            tokens["id"], tokens["password"], tokens["mtType"], tokens["passphrase"])
    if 'trades' in imported_trades:
        userid = tokens["user"]
        for trade_data in imported_trades['trades']:
            check_trade = Trades.query.filter_by(user_id=userid,
                                                 account_id=trade_data["account_id"], broker=trade_data["broker"], trade_id=trade_data["trade_id"]).first()
            if check_trade:
                continue
            new_trade = Trades(user_id=userid, account_id=trade_data["account_id"], broker=trade_data["broker"], trade_id=trade_data["trade_id"], status=trade_data["status"], open_date=trade_data["open_date"],
                               symbol=trade_data["symbol"], entry=trade_data["entry"], exit=trade_data["exit"], size=trade_data["size"], pips=trade_data["pips"], ret_pips=trade_data["ret_pips"], ret=trade_data["ret"], ret_percent=trade_data["ret_percent"], ret_net=trade_data["ret_net"], side=trade_data["side"], setups=trade_data["setups"], mistakes=trade_data["mistakes"])
            db.session.add(new_trade)
            for sub in trade_data["subs"]:
                new_sub = SubTrades(user_id=userid, trade_id=trade_data["trade_id"], action=sub["action"], spread=sub["spread"],
                                    type=sub["type"], date=sub["date"], size=sub["size"], position=sub["position"], price=sub["price"])
                db.session.add(new_sub)
            db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Error occured"}), 500


@app.route("/api/get_trades", methods=["POST"])
def get_trade_data():
    rdata = request.json
    userid = rdata["user"]
    data_display = Trades.query.filter_by(
        user_id=userid).all()
    data_array = []
    for data in data_display:
        subdata_display = SubTrades.query.filter_by(
            trade_id=data.trade_id, user_id=userid).all()
        subs = []
        for sub in subdata_display:
            subs.append({"action": sub.action, "spread": sub.spread, "type": sub.type,
                        "date": sub.date, "size": sub.size, "position": sub.position, "price": sub.price, })
        data_array.append({"id": data.trade_id, "accountId": data.account_id, "broker": data.broker, "status": data.status, "openDate": data.open_date, "symbol": data.symbol,
                          "entry": data.entry, "exit": data.exit, "size": data.size, "pips": data.pips, "returnPips": data.ret_pips, "return": data.ret, "returnPercent": data.ret_percent, "returnNet": data.ret_net, "side": data.side, "setups": data.setups, "mistakes": data.mistakes, "subs": subs})
    return jsonify(data_array)


@app.route("/api/delete_trades", methods=["POST"])
def delete_trade_data():
    params = request.json
    user_id = params["userId"]
    trade_ids = params["tradeId"]
    trades = Trades.query.filter_by(user_id=user_id).all()
    for trade in trades:
        if trade.trade_id in trade_ids:
            db.session.delete(trade)
            subtrades = SubTrades.query.filter_by(
                user_id=user_id, trade_id=trade.trade_id).all()
            for subtrade in subtrades:
                db.session.delete(subtrade)
    db.session.commit()
    return "succeed"


@app.route("/create-payment-intent", methods=["POST"])
def create_payment():
    try:
        stripe_keys = {
            "secret_key": os.environ.get("STRIPE_SECRET_KEY"),
            "publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
        }
        stripe.api_key = stripe_keys["secret_key"]
        data = request.json
        intent = stripe.PaymentIntent.create(
            amount=data["price"],
            currency="usd",
            # automatic_payment_methods={
            #     'enabled': True,
            # },
            payment_method_types=["card"],
        )
        return jsonify({'clientSecret': intent['client_secret']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/api/payment-success", methods=["POST"])
def payment_success():
    data = request.json
    user = Users.query.filter_by(email=data["email"]).first()
    user.membership = data["membership"]
    user.paydate = datetime.utcnow()
    db.session.commit()
    token = jwt.encode({'public_id': user.public_id, 'email': user.email, 'membership': user.membership, 'expired': 0, 'iat': datetime.utcnow(), 'exp': datetime.utcnow(
    ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
    return jsonify({"success": True, "token": "Bearer " + token})


@app.route("/api/get-chart", methods=["POST"])
def get_chartdata():
    data = request.json
    trades = Trades.query.filter_by(user_id=data["userId"]).all()
    trades.sort(key=sort_by_date)
    xvalue_all = []
    trade_count = 0
    accumulative_return = []
    accumulative_return_total = 0
    profit_factor = []
    total_profit_factor = 0
    avg_return = []
    avg_return_total = 0
    win_count = 0
    pnl_total = 0
    pnl_change = 0
    volume_total = 0
    pnl_day = 0
    volume_day = 0
    total_pnl = []
    daily_pnl = []
    daily_volume = []
    total_win_rate = []
    daily_win_rate = []
    total_win_or_loss_score = []
    win_or_loss_score = 0
    for trade in trades:
        trade_count += 1
        xvalue_all.append(trade.open_date[0:10])
        accumulative_return_total += float(trade.ret)
        accumulative_return.append(accumulative_return_total)
        profit_factor.append(abs(float(trade.ret)) / float(trade.entry))
        total_profit_factor += abs(float(trade.ret)) / float(trade.entry)
        avg_return_total += float(trade.ret)
        avg_return.append(avg_return_total / trade_count)
        if trade.status == "WIN":
            win_count += 1
            daily_win_rate.append(100)
            win_or_loss_score += 3
        else:
            daily_win_rate.append(0)
            win_or_loss_score -= 2
        volume_total += float(trade.entry)
        total_pnl.append(round(accumulative_return_total, 2))
        daily_pnl.append(round(float(trade.ret), 2))
        daily_volume.append(round(float(trade.entry)))
        total_win_rate.append(round(100 * win_count / trade_count, 2))
        total_win_or_loss_score.append(win_or_loss_score)
    pnl_total = accumulative_return_total
    pnl_change = pnl_total / volume_total * 100
    pnl_day = pnl_total / len(trades)
    volume_day = volume_total / len(trades)
    return jsonify({"accumulative_return": accumulative_return, "accumulative_return_total": accumulative_return_total, "xvalue_all": xvalue_all, "profit_factor": profit_factor, "avg_profit_factor": total_profit_factor / len(profit_factor), "avg_return": avg_return, "avg_return_total": avg_return_total / len(trades), "win_ratio": {"total": len(trades), "winning": win_count}, "pnl_total": pnl_total, "pnl_change": pnl_change, "pnl_day": pnl_day, "volume_day": volume_day, "total_pnl": total_pnl, "daily_pnl": daily_pnl, "daily_volume": daily_volume, "total_win_rate": total_win_rate, "daily_win_rate": daily_win_rate, "total_win_or_loss_score": total_win_or_loss_score})


@app.route("/api/get-reports", methods=["POST"])
def get_reports():
    data = request.json
    trades = Trades.query.filter_by(user_id=data["userId"]).all()
    selectedIds = data["selected"]
    trades.sort(key=sort_by_date)
    total_return_x = []
    total_return_y = []
    total_return = 0
    total_dates = []
    daily_return = []
    temp_date = ""
    return_winner = []
    return_winner_total = 0
    return_loser = []
    return_loser_total = 0
    return_long = []
    return_short = []
    return_long_total = 0
    return_short_total = 0
    biggestProfit = 0
    biggestLose = 0
    closed_trades = []
    closed_trades_total = 0
    open_trades = []
    open_trades_total = 0
    daily_trades = []
    win_count = 0
    loss_count = 0
    win_total = []
    loss_total = []
    be_count = 0
    be_total = []
    for trade in trades:
        if len(selectedIds) > 0 and not trade.trade_id in selectedIds:
            continue
        total_return_x.append(trade.open_date[0:10])
        total_return += float(trade.ret)
        total_return_y.append(total_return)
        if trade.open_date[0:10] == temp_date:
            daily_return[-1] += float(trade.ret)
            daily_trades[-1] += 1
            if float(trade.ret) == 0:
                be_total[-1] += 1
                be_count += 1
            if trade.status == "WIN" or trade.status == "LOSS":
                closed_trades[-1] += 1
                closed_trades_total += 1
                if trade.status == "WIN":
                    win_total[-1] += 1
                    win_count += 1
                else:
                    loss_total[-1] += 1
                    loss_count += 1
            else:
                open_trades[-1] += 1
                open_trades_total += 1
        else:
            total_dates.append(trade.open_date[0:10])
            daily_return.append(float(trade.ret))
            daily_trades.append(1)
            if trade.status == "WIN" or trade.status == "LOSS":
                closed_trades.append(1)
                closed_trades_total += 1
                open_trades.append(0)
                if trade.status == "WIN":
                    win_count += 1
                    win_total.append(1)
                    loss_total.append(0)
                else:
                    loss_count += 1
                    win_total.append(0)
                    loss_total.append(1)
            else:
                closed_trades.append(0)
                open_trades.append(1)
                open_trades_total += 1
            if float(trade.ret) == 0:
                be_total.append(1)
                be_count += 1
            else:
                be_total.append(0)
            temp_date = trade.open_date[0:10]
        if trade.status == "WIN":
            return_winner.append(float(trade.ret))
            return_winner_total += float(trade.ret)
        else:
            return_loser.append(float(trade.ret))
            return_loser_total += float(trade.ret)
        if trade.side == "LONG":
            return_long.append(float(trade.ret))
            return_long_total += float(trade.ret)
        else:
            return_short.append(float(trade.ret))
            return_short_total += float(trade.ret)
        if float(trade.ret) > biggestProfit:
            biggestProfit = float(trade.ret)
        if float(trade.ret) < biggestLose:
            biggestLose = float(trade.ret)
    return jsonify({"totalReturnY": total_return_y, "totalReturnX": total_return_x, "totalReturn": total_return, "totalDates": total_dates, "dailyReturn": daily_return, "returnWin": return_winner, "returnWinTotal": return_winner_total, "returnLose": return_loser, "returnLoseTotal": return_loser_total, "returnLong": return_long, "returnLongTotal": return_long_total, "returnShort": return_short, "returnShortTotal": return_short_total, "biggestProfit": biggestProfit, "biggestLose": biggestLose, "totalClosedTrades": closed_trades_total, "closedTrades": closed_trades, "totalOpenTrades": open_trades_total, "openTrades": open_trades, "totalTrades": len(total_return_x), "dailyTrades": daily_trades, "totalWinner": win_count, "totalLoser": loss_count, "dailyWinners": win_total, "dailyLosers": loss_total, "beCount": be_count, "dailyBe": be_total})


@app.route("/create")
def createdb():
    db.create_all()
    return "db created"


@app.route("/get-filter-item")
def getfilteritem():
    trades = Trades.query.all()
    available_brokers = []
    available_symbols = []
    broker_account = []
    for trade in trades:
        if not trade.broker in available_brokers:
            available_brokers.append(trade.broker)
        if not trade.symbol in available_symbols:
            available_symbols.append(trade.symbol)
    if len(available_brokers) > 0:
        for broker in available_brokers:
            available_accounts = []
            trades_broker = Trades.query.filter_by(broker=broker).all()
            for trade_broker in trades_broker:
                if not trade_broker.account_id in available_accounts:
                    available_accounts.append(trade_broker.account_id)
                    broker_account.append(
                        broker + " " + available_accounts[-1])
    return jsonify({"brokers": broker_account, "symbols": available_symbols, "status": ["WIN", "LOSS"]})


if __name__ == '__main__':
    if os.environ.get("DEBUG_MODE") == "TRUE":
        app.run(debug=True)
    else:
        app.run()
