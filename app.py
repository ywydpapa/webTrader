from flask import Flask, jsonify, request, render_template, redirect, session, flash, url_for
import dbconn
import dbconn

app = Flask(__name__)

def home():
    return render_template('./login/login.html')
@app.route('/start')
def hello_world():
    return render_template('./index.html', coinlist = dbconn.coinCombo())

@app.route('/coinrate')
def indexrate():
    return render_template('./indexrate.html', coinlist = dbconn.coinCombo())

@app.route('/coin60/<coinName>')
def recomm60(coinName):
    return render_template('./coinStatus/coinStatus.html', results=dbconn.coinStat60(coinName))

@app.route('/coin30/<coinName>')
def recomm30(coinName):
    return render_template('./coinStatus/coinStatus.html', results=dbconn.coinStat30(coinName))

@app.route('/coin10/<coinName>')
def recomm10(coinName):
    return render_template('./coinStatus/coinStatus.html', results=dbconn.coinStat10(coinName))

@app.route('/coinrate10/<coinName>')
def raiseCoin10(coinName):
    return render_template('./coinStatus/raiseCoinlist.html', results=dbconn.coinRate10(coinName))

@app.route('/coinrate30/<coinName>')
def raiseCoin30(coinName):
    return render_template('./coinStatus/raiseCoinlist.html', results=dbconn.coinRate30(coinName))

@app.route('/coinrate60/<coinName>')
def raiseCoin60(coinName):
    return render_template('./coinStatus/raiseCoinlist.html', results=dbconn.coinRate60(coinName))

@app.route('/coinScore10')
def coinScore10():
    return render_template('./coinStatus/coinScore10.html', results=dbconn.getScore10())

@app.route('/coinScore20')
def coinScore20():
    return render_template('./coinStatus/coinScore20.html', results=dbconn.getScore10())

@app.route('/coinScore30')
def coinScore30():
    return render_template('./coinStatus/coinScore30.html', results=dbconn.getScore10())

@app.route('/startTrade')
def buy10():
    return render_template('./coinStatus/autoResult10.html', results=dbconn.buy10())

@app.route('/startSell')
def sell10():
    return render_template('./coinStatus/sellResult.html', results=dbconn.sell10())

@app.route('/setup')
def setup():
    return render_template('./setup/setupmain.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('./login/login.html')
    else:
        uid = request.form.get('uid')
        upw = request.form.get('upw')
        row = dbconn.selectUsers(uid, upw)
        if row:
            session['userNo'] = row['userNo']
            session['userName'] = row['userName']
            session['userRole'] = row['userRole']
            return redirect('/start')
        else:
            return '''
                <script>
                    // 경고창 
                    alert("로그인 실패, 다시 시도하세요")
                    // 이전페이지로 이동
                    history.back()
                </script>
            '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
