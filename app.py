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
    ret = db.Column(db.String(20))
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
    if isinstance(imported_trades, list):
        return jsonify(imported_trades)
    else:
        return imported_trades, 500


@app.route("/api/trades", methods=["POST"])
def manage_trades():
    tradesdata = request.json
    userid = tradesdata["user"]
    for trade_data in tradesdata["trades"]:
        check_trade = Trades.query.filter_by(user_id=userid,
                                             account_id=trade_data["account_id"], broker=trade_data["broker"], trade_id=trade_data["trade_id"]).first()
        if check_trade:
            continue
        new_trade = Trades(user_id=userid, account_id=trade_data["account_id"], broker=trade_data["broker"], trade_id=trade_data["trade_id"], status=trade_data["status"], open_date=trade_data["open_date"],
                           symbol=trade_data["symbol"], entry=trade_data["entry"], exit=trade_data["exit"], size=trade_data["size"], ret=trade_data["ret"], side=trade_data["side"], setups=trade_data["setups"], mistakes=trade_data["mistakes"])
        db.session.add(new_trade)
        db.session.commit()
        subtrade_1 = trade_data["sub_1"]
        new_sub_1 = SubTrades(user_id=userid, trade_id=trade_data["trade_id"], action=subtrade_1["action"], spread=subtrade_1["spread"],
                              type=subtrade_1["type"], date=subtrade_1["date"], size=subtrade_1["size"], position=subtrade_1["position"], price=subtrade_1["price"])
        db.session.add(new_sub_1)
        db.session.commit()
        subtrade_2 = trade_data["sub_2"]
        new_sub_2 = SubTrades(user_id=userid, trade_id=trade_data["trade_id"], action=subtrade_2["action"], spread=subtrade_2["spread"],
                              type=subtrade_2["type"], date=subtrade_2["date"], size=subtrade_2["size"], position=subtrade_2["position"], price=subtrade_2["price"])
        db.session.add(new_sub_2)
        db.session.commit()
    return jsonify({"success": True})


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
        data_array.append({"id": data.trade_id, "broker": data.broker, "status": data.status, "openDate": data.open_date, "symbol": data.symbol,
                          "entry": data.entry, "exit": data.exit, "size": data.size, "return": data.ret, "side": data.side, "setups": data.setups, "mistakes": data.mistakes, "subs": subs})
    return jsonify(data_array)


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
        avg_return.append(float(trade.ret))
        avg_return_total += float(trade.ret)
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
    return jsonify({"accumulative_return": accumulative_return, "accumulative_return_total": accumulative_return_total, "xvalue_all": xvalue_all, "profit_factor": profit_factor, "avg_profit_factor": total_profit_factor / len(profit_factor), "avg_return": avg_return, "avg_return_total": avg_return_total, "win_ratio": {"total": len(trades), "winning": win_count}, "pnl_total": pnl_total, "pnl_change": pnl_change, "pnl_day": pnl_day, "volume_day": volume_day, "total_pnl": total_pnl, "daily_pnl": daily_pnl, "daily_volume": daily_volume, "total_win_rate": total_win_rate, "daily_win_rate": daily_win_rate, "total_win_or_loss_score": total_win_or_loss_score})


@app.route("/create")
def createdb():
    db.create_all()
    return "db created"


@app.route("/get-filter-item")
def getfilteritem():
    trades = Trades.query.all()
    available_brokers = []
    available_symbols = []
    for trade in trades:
        if not trade.broker in available_brokers:
            available_brokers.append(trade.broker)
        if not trade.symbol in available_symbols:
            available_symbols.append(trade.symbol)
    return jsonify({"brokers": available_brokers, "symbols": available_symbols, "status": ["WIN", "LOSS"]})


if __name__ == '__main__':
    if os.environ.get("DEBUG_MODE") == "TRUE":
        app.run(debug=True)
    else:
        app.run()