from flask import Flask, jsonify, render_template, request
import json
import pandas as pd
from pandas.io.json import json_normalize

## my imports
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import collections
import numpy as np
import networkx as nx
from bokeh.plotting import from_networkx
import matplotlib.pyplot as plt
import hvplot.networkx as hvnx
import holoviews as hv
hv.extension('bokeh')
from bokeh.io import show, curdoc
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, ColumnDataSource
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/view/')
def view():
    return render_template('view.html')

# I am not using that at the moment, but maybe I'll
@app.route('/loadJson')
def loadJson():
    with open("C:/Users/Luciene/PycharmProjects/app/templates/vt-to-maec-output-1.json", "r") as read_file:
        df = json_normalize(read_file['data'], record_path=['pages', 'questions'], meta='id',
                            record_prefix='question_')
        print(df)

# Method to post the images back to the plot.html page
# THis is if a static analysis is uploaded
@app.route('/plot', methods=['GET', 'POST'])
def plot():
    img = BytesIO()
    img2 = BytesIO()
    if request.method == 'POST':
        file = request.files['file']
        content = json.load(file)
        class_data = content['observable_objects']['0']['extensions']['x-maec-avclass']
        df = pd.DataFrame(class_data)
        print(df)
        fig = plt.figure(figsize=(20,5))
        df.classification_name.value_counts().plot.bar()
        plt.suptitle("Frequency a malware class was detected by the antivirus")
        plt.ylabel('Frequency', fontsize=15)
        plt.xlabel('Malware classes', fontsize=15)
        plt.savefig(img, format='png',dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        fig =plt.figure(figsize=(20,5))
        df.is_detected.value_counts().plot.bar()
        plt.suptitle("Did the Antivirus detected the malware instance?")
        plt.ylabel('Frequency', fontsize=15)
        plt.xlabel('Detections', fontsize=15)
        plt.savefig(img2, format='png',dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        plt.close()
        img2.seek(0)
        plot2_url = base64.b64encode(img2.getvalue()).decode('utf8')
        return render_template('/plot.html', plot_url=plot2_url, plot2_url=plot_url)

# THis is if a Dynamic analysis is uploaded
@app.route('/plotDynamic', methods=['GET', 'POST'])
def plotDynamic():
    imgPlot = BytesIO()
    imgPlot3 = BytesIO()
    imgPlotByType = BytesIO()

    if request.method == 'POST':
        file = request.files['file']
        content = json.load(file)

        # Graph for Type of Relationship Frequence
        class_data = content['relationships']
        df = pd.DataFrame(class_data)
        print(df)
        fig = plt.figure(figsize=(8, 3))
        df.relationship_type.value_counts().plot.bar()
        plt.suptitle("Graph - Frequency of Type of Relationship")
        plt.ylabel('Frequency', fontsize=15)
        plt.xlabel('Type ofRelationship', fontsize=15)
        plt.savefig(imgPlot, format='png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        plt.close()
        imgPlot.seek(0)
        plot2_url = base64.b64encode(imgPlot.getvalue()).decode('utf8')

        # Graph for Type of Relationship Frequence
        fig = plt.figure(figsize=(8, 3))
        results = content['observable_objects']

        for key in results.keys(): # iteraction through the results (dictionaty) and print each line
            values = results.values()
            typList = [] # creates a list to hold the type values
            # loop over the dictionary
            for eachValue in values:
                typeOb = eachValue['type']  # and takes the value type
                typList.append(typeOb)  # and stores in the list

        # creates the graph horizontal
        resultCounterByType = collections.Counter(typList)  # counts the frequency by type and stores in a variable
        names = list(resultCounterByType.keys())
        valuesList = list(resultCounterByType.values())

        index = names
        df = pd.DataFrame({'Frequency': valuesList}, index=index)
        ax = df.plot.barh()
        plt.show(ax)
        plt.suptitle("Graph - ByType of Relationship")
        plt.ylabel('Frequency', fontsize=15)
        plt.xlabel('Type ofRelationship', fontsize=15)
        plt.savefig(imgPlotByType, format='png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        plt.close()
        imgPlotByType.seek(0)
        imgPlotByType_url = base64.b64encode(imgPlot.getvalue()).decode('utf8')

        return render_template('/plot.html', plot2_url=imgPlotByType_url, imgPlotByType_url=plot2_url)

if __name__ == '__main__':
    app.run(debug=True)
