from flask import Flask, jsonify, request, render_template, redirect, session, flash, url_for
import dbconn

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('./index.html')

@app.route('/coin60/<coinName>')
def recomm60(coinName):
    return render_template('./coinStatus/coinStatus.html', results=dbconn.coinStat60(coinName))

@app.route('/coin30/<coinName>')
def recomm30(coinName):
    return render_template('./coinStatus/coinStatus.html', results=dbconn.coinStat30(coinName))

@app.route('/coin10/<coinName>')
def recomm10(coinName):
    return render_template('./coinStatus/coinStatus.html', results=dbconn.coinStat10(coinName))

if __name__ == '__main__':
    app.run()