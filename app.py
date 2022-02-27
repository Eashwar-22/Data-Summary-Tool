from flask import Flask,render_template,request,redirect,url_for,session
from analysis import data_analysis_v2
import numpy as np


import pandas as pd
import os
app = Flask(__name__)
app.config['SECRET_KEY']='ti3dfhwewfwo9e0203e'
ALLOWED_EXTENSIONS = {'csv','xlsx','xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

df_list = [0]

@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # upload no file
        if request.files['file'].filename=='':
            return render_template('error_file.html',empty=True,wrong=False)

        file = request.files['file']

        # upload wrong file
        if file and allowed_file(file.filename)==False:
            return render_template('error_file.html',empty=False,wrong=True)

        if '.csv' in file.filename:
            df=pd.read_csv(file)
        elif '.xls' in file.filename:
            df=pd.read_excel(file)
        df_list.append(df)
        return redirect(url_for('.dashboard_page',f=file.filename,data=df))
    return render_template('upload.html')

@app.route('/dashboard',methods=['GET'])
def dashboard_page():
    filename= request.args.get('f')
    # df = request.args['data']
    df = df_list[-1]
    process(df)
    return render_template('blocks.html',
                           filename=filename,
                           df=df,
                           nrows=len(df.head()),
                           ncols=len(df.columns),
                           obj=obj)

def process(df):
    global obj
    obj = data_analysis_v2(df)
    # print(obj.column_summary())



if __name__=='__main__':
    app.run(debug=True)