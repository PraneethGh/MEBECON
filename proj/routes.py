from proj import app,db
from flask import render_template,url_for,redirect,flash,request
import speech_recognition as sr
from flask import jsonify
from flask import json
import pickle
import numpy as np
import sklearn
import psycopg2
from googleapiclient.discovery import build
from sklearn import preprocessing
from proj.models import Clinic

api_key = 'AIzaSyBd-50SqCJtbgCvrLPiL6csncK4X4fQf9M'
model = pickle.load(open('model2.pkl', 'rb'))
ans=''
vids = ''
#global dep
dep=''
def func(f):
        with open(r'proj\aud.wav','wb') as audio:
            #f.save(audio)
            f.save(audio)
        print('file uploaded successfully')
        r=sr.Recognizer()
        filename = r"proj\aud.wav"
        with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
          audio_data = r.record(source)
          word = r.recognize_google(audio_data)
          #print(word)
          word=word.strip()
          word=word.lower()
          print(word)
          return word
@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html',title='Home')

@app.route('/tt',methods=['POST','GET'])
def tt():
    if request.method == "POST":
         f = request.files['audio_data']
         ans=func(f)
         #print(ans)
         l=[]
         l.append(ans)
         sample = model[1].transform(l)
         #print(l,sample)
         global predic
         predic = model[2].inverse_transform(model[0].predict(sample.toarray()))
         print("1",predic)
         ans=''
         
         depts={}
         depts['Dermatology']=["Fungal infection","Acne","Psoriasis","Impetigo"]
         depts["Osteopathic medicine"]=["AIDS"]
         depts["Hepatology"]=['Alcoholic hepatitis','hepatitis A',"Hepatitis E","Hepatitis D","Hepatitis C","Hepatitis B"]
         depts["General Physician"]=['Allergy','Chicken pox','Common Cold','Dengue','Drug Reaction','Jaundice','Malaria', 'Migraine','Paralysis ','Typhoid',' Paroymsal Positional Vertigo','Urinary tract infection', 'Varicose veins']
         depts["Pulmonology"]=['Pneumonia','Tuberculosis','Bronchial Asthma']
         depts["Gastrology"]=['Chronic cholestasis','Dimorphic hemmorhoids','GERD','Gastroenteritis','Peptic ulcer diseae']
         depts["orthopedics"]=[ 'Cervical spondylosis','Arthritis','Osteoarthristis']
         depts["Endocrinology"]=['Diabetes ','Hyperthyroidism','Hypoglycemia','Hypothyroidism']
         depts["Cardiology"]=['Heart attack','Hypertension ']

         #global dep
         #print(predic[0])
         for dt,symp in depts.items():
            for j in symp:
               if(j==predic[0]):
                  global dep
                  #print(dt)
                  dep=dt
         #vis=video()
         print('1',dep)
         ans="PREDICTED DISEASE: "+predic[0].upper()+"<br><br>"+"DISCIPLINE OF MEDICINE: "+dep.upper()
         return jsonify(ans)
@app.route('/main_js',methods=['POST','GET'])
def main_js():
   return render_template("/js/main.js")

@app.route('/medical',methods=['POST','GET'])
def medical():

   return render_template('medical.html',title='medical',request="POST")

