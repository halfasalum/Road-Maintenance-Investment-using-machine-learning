from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))


@app.route("/")
def index():
    result = ''
    state = ''
    RL = ''
    ESAL = ''
    return render_template('index.html', **locals())


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    # accepts value from form request
    hours = (int)(request.form['hours'])
    days = (int)(request.form['days'])
    road = (int)(request.form['road'])
    fe = (int)(request.form['fe']) / 100
    result = model.predict([[days, hours, road]]).astype(int)
    # N number of exales
    # structure number sn = 5
    # design life = 25 years
    N = 2
    FE = 0.010
    AADT = result
    FD = 0.4
    GRN = 41.65
    ESAL = N * FE * AADT * fe * 365 * FD * GRN
    RL = ((((result * 365) - ESAL) / (result * 365)) * 100).astype(int)
    REMAIN = ((25 * RL) / 100).astype(int)
    if RL > 80:
        state = "GOOD, "
    elif RL > 50:
        state = "MEDIUM, "
    else:
        state = "LOW, "

    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.debug = True
    app.run()
