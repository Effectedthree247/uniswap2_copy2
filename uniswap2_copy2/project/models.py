from project import db

class Tokens(db.Model):
    __bind_key__ = 'ethereum'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), unique=False, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    tvl = db.Column(db.Float, nullable=False)
    apy = db.Column(db.Float, nullable=False)


class TokensArbitrum(db.Model):
    __bind_key__ = 'arbitrum'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), unique=False, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    tvl = db.Column(db.Float, nullable=False)
    apy = db.Column(db.Float, nullable=False)


class TokensOptimism(db.Model):
    __bind_key__ = 'optimism'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), unique=False, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    tvl = db.Column(db.Float, nullable=False)
    apy = db.Column(db.Float, nullable=False)






