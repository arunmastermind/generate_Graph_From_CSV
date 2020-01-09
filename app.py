#!/usr/local/bin/python
# coding=utf8

import random
from io import BytesIO

from flask import Flask, render_template, request, make_response, send_file
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def test():
#     return "HELLO ARUN"

# @app.route('/', defaults={'str1':'test', 'str2':'test'}, methods=['GET', 'POST'])
# @app.route('/<str1>/<str2>/', methods=['GET', 'POST'])
# def landing_page(str1, str2):
#     matching_ratio = failureMatcher.matchPercent(str1, str2)
#     diff_str1 = str1.split(' ')
#     diff_str2 = str2.split(' ')
#     html = differ.make_file(diff_str1, diff_str2, context=True)
#     return render_template('test.html', str1 = str1, str2 = str2, matching_ratio = matching_ratio, html=Markup(html))

@app.route('/', methods=['GET','POST'])
def addInputs():
    return render_template('input_form.html')

@app.route('/submitted', methods=['GET','POST'])
def getInputs():
    data = request.form
    filename = data['filename']
    try:
        df = pd.read_csv(filename)
    except:
        try:
            df = pd.read_excel(filename)
        except:
            return "bad filename"
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid()
    k = []
    for i in range(int(data['ycount'])):
        s = "row_" + str(i+1)
        k.append(df[data[s]])
    # ys = df['val1']
    xs = df[data['xaxis']]
    for i in k:
        axis.plot(xs, i)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    fig.savefig('graph.png')
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
