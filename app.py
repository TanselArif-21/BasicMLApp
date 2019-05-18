from flask import Flask, request, jsonify
from functions import return_something, return_something2, get_prediction_lr
import pandas as pd
import random
import string

app=Flask(__name__)

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
        return '''
        <!doctype html>
        <title>Upload an excel file</title>
        <h1>Excel file upload (csv)</h1>
        <form action="" method=post enctype=multipart/form-data><p></p>
    	<label>LotFrontage</label><input type="text" name="LotFrontage">
    	<label>LotArea</label><input type="text" name="LotArea"><p></p>
    	<label>OverallQual</label><input type="text" name="OverallQual">
    	<label>OverallCond</label><input type="text" name="OverallCond"><p></p>
    	<label>YearBuilt</label><input type="text" name="YearBuilt">
    	<label>YearRemodAdd</label><input type="text" name="YearRemodAdd"><p></p>
    	<label>MasVnrArea</label><input type="text" name="MasVnrArea">
    	<label>BsmtFinSF1</label><input type="text" name="BsmtFinSF1"><p></p>
    	<label>BsmtFinSF2</label><input type="text" name="BsmtFinSF2">
    	<label>BsmtUnfSF</label><input type="text" name="BsmtUnfSF"><p></p>
    	<label>TotalBsmtSF</label><input type="text" name="TotalBsmtSF">
    	<label>1stFlrSF</label><input type="text" name="1stFlrSF"><p></p>
    	<label>2ndFlrSF</label><input type="text" name="2ndFlrSF">
    	<label>LowQualFinSF</label><input type="text" name="LowQualFinSF"><p></p>
    	<label>GrLivArea</label><input type="text" name="GrLivArea">
    	<label>BsmtFullBath</label><input type="text" name="BsmtFullBath"><p></p>
    	<label>BsmtHalfBath</label><input type="text" name="BsmtHalfBath">
    	<label>FullBath</label><input type="text" name="FullBath"><p></p>
    	<label>HalfBath</label><input type="text" name="HalfBath">
    	<label>BedroomAbvGr</label><input type="text" name="BedroomAbvGr"><p></p>
    	<label>KitchenAbvGr</label><input type="text" name="KitchenAbvGr">
    	<label>Fireplaces</label><input type="text" name="Fireplaces"><p></p>
    	<label>GarageYrBlt</label><input type="text" name="GarageYrBlt">
    	<label>GarageCars</label><input type="text" name="GarageCars"><p></p>
    	<label>GarageArea</label><input type="text" name="GarageArea">
    	<label>WoodDeckSF</label><input type="text" name="WoodDeckSF"><p></p>
    	<label>OpenPorchSF</label><input type="text" name="OpenPorchSF">
    	<label>EnclosedPorch</label><input type="text" name="EnclosedPorch"><p></p>
    	<label>3SsnPorch</label><input type="text" name="3SsnPorch">
    	<label>ScreenPorch</label><input type="text" name="ScreenPorch"><p></p>
    	<label>PoolArea</label><input type="text" name="PoolArea">
    	<label>MiscVal</label><input type="text" name="MiscVal"><p></p>
    	<label>MoSold</label><input type="text" name="MoSold">
    	<label>YrSoldlabel</label><input type="text" name="YrSold"><p></p>
    	<label>SalePrice</label><label>To be predicted</label>
    	<input type=file name=file><input type=submit value=Upload>
        </form>
        '''


@app.route("/export", methods=['GET'])
def export_records():
    return

if __name__ == "__main__":
    app.run()