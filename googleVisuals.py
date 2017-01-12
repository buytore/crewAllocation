from flask import Flask, render_template
import os
import json
from crew1 import combineFlts, convertDT
import pandas as pd

##MARK's build - the FLASK interface and required connectors to data
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

def formatPairings(pairingList):
    formatGoogle = []
    for newJSON in pairingList:
        print newJSON
        formatGoogle.append(newJSON['ac'])
        formatGoogle.append(newJSON['ac'])
        formatGoogle.append(newJSON['startDate'].strftime('%m/%d/%Y'))
        formatGoogle.append(newJSON['endDate'].strftime('%m/%d/%Y'))
    return True



def getAllData(pairingList):
    #GOOGLE FORMAT FOR GANTT CHART
    #data.addColumn('string', 'Task ID');
    #data.addColumn('string', 'Task Name');
    #data.addColumn('string', 'Resource');
    #data.addColumn('date', 'Start Date');
    #data.addColumn('date', 'End Date');
    #data.addColumn('number', 'Duration');
    #data.addColumn('number', 'Percent Complete');
    #data.addColumn('string', 'Dependencies');

    json1 = pairingList.to_json(orient="values")
#    json1 = json.dumps(pairingList, ensure_ascii=False)
    return json1

pairingsList = combineFlts()
cleanPairings = formatPairings(pairingsList)
pairingsDF = convertDT(pairingsList)

########### ROUTING OPTIONS ###############
@app.route("/")
def main():
    #json1, json2, json3, json4, json5, json6 = getAllData()
    return "Hello World!"

@app.route("/ganttTest")
def ganttTest():
    #json1, json2, json3, json4, json5, json6 = getAllData()
    return render_template('gGantt.html', **locals())

@app.route("/gantt")
def gantt():
    json1 = getAllData(pairingsDF)
    #html1 = pairingDF.to_html()
    return render_template('gGantt.html', **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0')