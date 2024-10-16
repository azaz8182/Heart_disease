from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np

# Load the trained model
model_path = 'heart.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

app=Flask(__name__,template_folder='Templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from form
    age = [a for a in request.form.values()]
    sex = [a for a in request.form.values()]
    chestpaintype = [a for a in request.form.values()]
    restingBP = [a for a in request.form.values()]
    cholesterol = [a for a in request.form.values()]
    fastingBS = [a for a in request.form.values()]
    restingECG = [a for a in request.form.values()]
    maxHR = [a for a in request.form.values()]
    exerciseAngina = [a for a in request.form.values()]
    oldpeak = [a for a in request.form.values()]
    sT_Slope = [a for a in request.form.values()]
    
    final_features = pd.DataFrame([age,sex,chestpaintype,restingBP,cholesterol,fastingBS,restingECG,maxHR,exerciseAngina,oldpeak,sT_Slope],columns=['Age','Sex','ChestPainType','RestingBP','Cholesterol','FastingBS','RestingECG','MaxHR','ExerciseAngina','Oldpeak','ST_Slope'])
    final_features["ExerciseAngina"].replace(to_replace={'no':0,'yes':1,'No':0,'Yes':1,'NO':0,'YES':1},inplace=True)
    final_features["ChestPainType"].replace(to_replace={'ASY':0,'ATA':1,'NAP':2,'TA':3,'Asy':0,'Ata':1,'Nap':2,'Ta':3,'asy':0,'ata':1,'nap':2,'ta':3},inplace=True)
    final_features["RestingECG"].replace(to_replace={'NORMAL':0,'LVH':1,'ST':2,'Normal':0,'Lvh':1,'St':2,'normal':0,'lvh':1,'st':2},inplace=True)
    final_features["ST_Slope"].replace(to_replace={'DOWN':0,'FLAT':1,'UP':2,'Down':0,'Flat':1,'Up':2,'down':0,'flat':1,'up':2},inplace=True)
    final_features["Sex"].replace(to_replace={'MALE':1,'FEMALE':0,'Male':1,'Female':0,'male':1,'female':0},inplace=True)
    final_features["FastingBS"].replace(to_replace={'no':0,'yes':1,'No':0,'Yes':1,'NO':0,'YES':1},inplace=True)
    
    
    
    # Make prediction
    prediction =model.predict(final_features)
    #prediction.replace(to_replace ={0:'Not Have Heart Disease',1:'Have Heart Disease'},inplace=True)
    output = prediction[0]
    return render_template('index.html', prediction_text='You not have heart disease' if output ==0 else 'You have heart disease')

    #return render_template('index.html', prediction_text='You {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)