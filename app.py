from flask import Flask, render_template, request
from joblib import load
import pandas as pd

app = Flask(__name__)
scaler_ = None
model_ = None

def get_x(dep_time, ar_time, source, destination, stops, airline):
    journey_day = 0
    journey_month = 0
    depature_hour = 0
    departure_minute = 0
    arrival_hour = 0
    arrival_minute = 0
    duration_hour = 0
    duration_minute = 0
    stops_ = 0
    Air_India = 0
    GoAir = 0
    IndiGo = 0
    Jet_Airways = 0
    Multiple_carriers = 0
    SpiceJet = 0
    Vistara = 0
    Chennai = 0
    Delhi = 0
    Kolkata = 0
    Mumbai = 0
    Cochin_d = 0
    Delhi_d = 0
    Hyderabad_d = 0
    Kolkata_d = 0

    duration = dep_time-ar_time

    journey_day = int(dep_time.day)
    journey_month = int(dep_time.month)
    depature_hour = int(dep_time.hour)
    departure_minute = int(dep_time.minute)
    arrival_hour = int(ar_time.hour)
    arrival_minute = int(ar_time.minute)
    duration_hour = int(str(duration).split()[2].split(':')[0])
    duration_minute = int(str(duration).split()[2].split(':')[1])

    stops_ = int(stops)

    if airline == 'IndiGo':
        IndiGo = 1
    if airline =='Air India':
        Air_India = 1
    if airline =='Jet Airways':
        Jet_Airways = 1
    if airline =='SpiceJet':
        SpiceJet = 1
    if airline =='GoAir':
        GoAir = 1
    if airline =='Vistara':
        Vistara = 1        
    if airline =='Multiple carriers':
        Multiple_carriers = 1

    if source =='Delhi':
        Delhi = 1
    if source =='Kolkata':
        Kolkata = 1
    if source =='Mumbai':
        Mumbai = 1        
    if source =='Chennai':
        Chennai = 1

    if destination =='Delhi':
        Delhi_d = 1
    if destination =='Kolkata':
        Kolkata_d = 1
    if destination =='Cochin':
        Cochin_d = 1        
    if destination =='Hyderabad':
        Hyderabad_d = 1

    return([journey_day,
    journey_month,
    depature_hour,
    departure_minute,
    arrival_hour,
    arrival_minute,
    duration_hour,
    duration_minute,
    stops_,
    Air_India,
    GoAir,
    IndiGo,
    Jet_Airways,
    Multiple_carriers,
    SpiceJet,
    Vistara,
    Chennai,
    Delhi,
    Kolkata,
    Mumbai,
    Cochin_d,
    Delhi_d,
    Hyderabad_d,
    Kolkata_d])

@app.route('/', methods = ['GET','POST'])
def hello_world():

    global scaler_
    global model_
    pred=''

    if model_ is None:
        model_ = load('./static/model.bin')

    if scaler_ is None:
        scaler_ = load('./static/std_scaler.bin')

    if request.method == 'POST':
        dep_time = request.form['dep_time']
        ar_time = request.form['ar_time']
        source = request.form['source']
        destination = request.form['destination']
        stops = request.form['stops']
        airline = request.form['airline']

        dep_time = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M")
        ar_time = pd.to_datetime(ar_time, format="%Y-%m-%dT%H:%M")

        if source == destination or dep_time>=ar_time:
            pred = 'E'
        else:
            x = [get_x(dep_time, ar_time, source, destination, stops, airline)]
            x = scaler_.transform(x)
            print(x)
            pred = model_.predict(x)
            print(model_.predict(x))

    return render_template("index.html", pred = pred)

if __name__ == "__main__":
    app.run(debug=True)