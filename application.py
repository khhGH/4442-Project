from flask import Flask, request, render_template
import pandas as pd
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/summary")
def summary_page():
    summary_df = pd.read_csv("csv_file/summary.csv")
    summary_df = summary_df.groupby(["driverID", "carPlateNumber"]).sum()
    summary_df = summary_df.reset_index()
    summary = []
    for index, row in summary_df.iterrows():
        current = {
            'driverID': row['driverID'],
            'carPlateNumber': row['carPlateNumber'],
            'num_rapidly_speedup': row['num_rapidly_speedup'],
            'num_rapidly_slowdown': row['num_rapidly_slowdown'],
            'num_neutral_slide': row['num_neutral_slide'],
            'total_neutral_slide_time': row['total_neutral_slide_time'],
            'num_overspeed': row['num_overspeed'],
            'total_overspeed_time': row['total_overspeed_time'],
            'num_fatigue_driving': row['num_fatigue_driving'],
            'num_hthrottle_stop': row['num_hthrottle_stop'],
            'num_oil_leak': row['num_oil_leak']
        }
        summary.append(current)
    return render_template('summary_report.html', summary=summary)

@app.route("/summary-graph")
def summary_graph():
    summary_df = pd.read_csv("csv_file/summary.csv")
    summary_df = summary_df.groupby(["driverID", "carPlateNumber"]).sum()
    summary_df = summary_df.reset_index()
    summary = []
    for index, row in summary_df.iterrows():
        current = {
            'driverID': row['driverID'],
            'carPlateNumber': row['carPlateNumber'],
            'num_rapidly_speedup': row['num_rapidly_speedup'],
            'num_rapidly_slowdown': row['num_rapidly_slowdown'],
            'num_neutral_slide': row['num_neutral_slide'],
            'total_neutral_slide_time': row['total_neutral_slide_time'],
            'num_overspeed': row['num_overspeed'],
            'total_overspeed_time': row['total_overspeed_time'],
            'num_fatigue_driving': row['num_fatigue_driving'],
            'num_hthrottle_stop': row['num_hthrottle_stop'],
            'num_oil_leak': row['num_oil_leak']
        }
        summary.append(current)
    return render_template('summary_graph.html', summary=summary)


target_driver = "null"
number_of_record = 0
@app.route("/driver" ,methods = ['POST','GET'])
def choose_page():
 return render_template('driver.html')


@app.route("/api/data" ,methods = ['POST','GET'])
def monitor_data():
    driverID = request.values.get("driverID")
    time = int(request.values.get("time"))
    print(time)
    target_file_path = os.path.join("csv_file", "speed_report", "{}.csv".format(driverID))
    driver_df = pd.read_csv(target_file_path)
    related_data = driver_df.loc[driver_df['unix_Time'].between(time-30, time, 'right')].sort_values('unix_Time')[['unix_Time', 'AverageSpeed', 'OverspeedIncident']]

    return_payload = {
        "driverID": driverID,
        "time": time,
        "speed": related_data.values.tolist()
    }

    return json.dumps(return_payload)


@app.route("/monitor" ,methods = ['POST','GET'])
def monitor_page():
    target_driver = request.values.get("driverID")
    return render_template('monitor.html', driverID = target_driver)

if __name__ == "__main__":
    app.run(port=8000, debug=True)