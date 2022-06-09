from project import app
from flask import render_template, request

from project.models import Tokens, TokensOptimism, TokensArbitrum

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loadingPage", methods=['GET', 'POST'])
def loadingPage():
    network = request.args.get('type')
    return render_template("loading.html", network=network)

@app.route("/arbitrum", methods=("POST", "GET"))
def arbitrum():
    tokens = TokensArbitrum.query.all()
    return render_template("arbitrum.html", tokens=tokens )

@app.route("/optimism", methods=("POST", "GET"))
def optimism():
    tokens = TokensOptimism.query.all()
    return render_template("optimism.html", tokens=tokens)

@app.route("/ethereum", methods=("POST", "GET"))
def ethereum():
    tokens = Tokens.query.all()
    return render_template("ethereum.html", tokens=tokens )

