import os
import jwt
import uuid
from flask import Flask, request, jsonify, make_response, abort
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY")
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
    token = jwt.encode({'public_id': new_user.public_id, 'email': new_user.email, 'iat': datetime.utcnow(), 'exp': datetime.utcnow(
    ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
    return jsonify({"success": True, "token": "Bearer " + token})


@app.route("/api/user/login", methods=["POST"])
def login_user():
    data = request.json
    user = Users.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"email": "User not found"}), 400
    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'public_id': user.public_id, 'email': user.email, 'iat': datetime.utcnow(), 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({"success": True, "token": "Bearer " + token})
    else:
        return jsonify({"password": "Incorrect password"}), 400


@app.route("/api/user/current", methods=["GET"])
@token_required
def get_current_user(current_user):
    user = Users.query.filter_by(email=current_user.email).first()
    return jsonify({"id": user.public_id, "email": user.email, "firstname": user.firstname, "lastname": user.lastname, "membership": user.membership, "paydate": user.paydate})


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
        data_array.append({"id": data.trade_id, "status": data.status, "openDate": data.open_date, "symbol": data.symbol,
                          "entry": data.entry, "exit": data.exit, "size": data.size, "return": data.ret, "side": data.side, "setups": data.setups, "mistakes": data.mistakes, "subs": subs})
    return data_array


# @app.route("/create")
# def createdb():
#     db.create_all()
#     return "db created"
