#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request, jsonify

#creating instance of the class
app=Flask(__name__)
loaded_model = pickle.load(open("model.pkl","rb"))


#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        print(request.form)
        to_predict_list = list(map(int, to_predict_list))
        to_predict = np.array(to_predict_list).reshape(1,12)
        result = loaded_model.predict(to_predict)
        
        if int(result)==1:
            prediction='Income more than 50K'
        else:
            prediction='Income less that 50K'
            
        return render_template("result.html",prediction=prediction)

@app.route('/result-api',methods = ['POST'])
def result_api():
    if request.method == 'POST':
        # From JSON to Input Model
        data = request.get_json(force=True)
        loaded_model = pickle.load(open("model.pkl","rb"))
        result = loaded_model.predict([np.array(list(data.values()))])
        
        if int(result)==1:
            prediction='Income more than 50K'
        else:
            prediction='Income less that 50K'

        return jsonify(prediction)    

if __name__ == "__main__":
	app.run(debug=True)