from flask import Flask, request, jsonify, render_template, send_from_directory
from functions import return_something, return_something2, get_prediction_lr
import pandas as pd
import random
import string
import os

app=Flask(__name__)

# The home route
@app.route('/', methods=['GET'])
def home_page():
    # Show the index page
    return render_template('index.html')

# A route to the test page that simply returns hello
@app.route('/plot', methods=['GET'])
def plot():
    return render_template("plot.html")

# A route to the test page that simply returns hello
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'

# The dosomething route
@app.route('/dosomething', methods=['GET'])
def dosomething():
    # Show something
    return str(return_something())

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        data_xls = pd.read_csv(f)
        return data_xls.to_html()
        #return "anna"
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''

# The dosomething2 route
@app.route('/dosomething2', methods=['GET', 'POST'])
def dosomething2():
    # If the request is a post request
    if request.method == 'POST':

        if 'Download' in request.form:
            filePath = str(os.path.dirname(os.path.realpath(__file__)))
            return send_from_directory(filename="HousePrice.csv",directory=os.path.join(filePath,"TestFiles"), as_attachment=True)

        if 'Default' in request.form:
            filePath = str(os.path.dirname(os.path.realpath(__file__)))
            df = pd.read_csv(os.path.join(filePath,"TestFiles","HousePrice.csv"))
        else:
            # This line creates a dataframe from a list of lists
            f = request.files['file']
            df = pd.read_csv(f)

        # These are the values given for the fields
        input_list = list(request.form.values())

        filename = ''
        for i in range(4):
            filename = filename + random.choice(string.ascii_letters)

        # # These are the names of the fields, i.e. LotFrontage, LotArea etc...
        input_names = list(request.form)

        result = get_prediction_lr(df, input_list, filename)

        # # This code section creates a dictionary where each key is a row in the dataframe
        res = dict()
        for i in range(len(df)):
            res[i] = list(df.iloc[i, :])

        # # Return the result
        # #return 'The predicted Sale Price of this house is: ' + str(round(result, 2)) + '. \n <button><a href="/plot/' + filename + '">See Sales Price Distribution</a></button><p></p>'
        return 'The predicted Sale Price of this house is: ' + str(round(result, 2)) + '. <p></p> <img src="static/' + filename + '.png"><p></p>'
    else:
        # Show the form page
        return render_template("dosomethingform.html")

if __name__ == "__main__":
    app.run()