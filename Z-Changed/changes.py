from flask import Flask, render_template, request
import json
import pandas as pd
## my imports
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)



############################################   Mt Method to post the images back to the plot.html page
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
        plt.ylabel('Frquency', fontsize=15)
        plt.xlabel('Malware classes', fontsize=15)
        plt.savefig(img, format='png',dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        fig =plt.figure(figsize=(20,5))
        df.is_detected.value_counts().plot.bar()
        plt.ylabel('Frquency', fontsize=15)
        plt.xlabel('Detections', fontsize=15)
        plt.savefig(img2, format='png',dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        plt.close()
        img2.seek(0)
        plot2_url = base64.b64encode(img2.getvalue()).decode('utf8')
        return render_template('/plot.html', plot_url=plot2_url, plot2_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)
