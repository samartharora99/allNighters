from flask import Flask, render_template, url_for, flash, redirect, request
from cardination.forms import RegistrationForm, LoginForm 
from cardination.models import Patient, PatientRecords
from cardination import app,db,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import random
import re
import sys
import math
import time
import subprocess
import pyautogui 
import webbrowser
from googlesearch import search 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.support.ui import WebDriverWait 
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup 
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'user.jpg')
    return render_template("login.html", image = full_filename)

@app.route("/registerPatient", methods=['GET', 'POST'])
def registerPatient():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        patient = Patient(username = form.username.data,email = form.email.data,password=hashed_password)
        db.session.add(patient)
        db.session.commit()
        flash(f'Account created for {form.username.data}, Now you can login!', 'success')
        return redirect(url_for('loginPatient'))
    return render_template('registerPatient.html', title='Register Patient', form=form)

@app.route("/loginPatient", methods=['GET', 'POST'])
def loginPatient():
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(email = form.email.data).first()
        if patient and bcrypt.check_password_hash(patient.password,form.password.data):
            login_user(patient,remember = form.remember.data)
            return redirect(url_for('viewRecords'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginPatient.html', title='Login Patient', form=form)

@app.route("/registerDoc", methods=['GET', 'POST'])
def registerDoc():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('registerDoc.html', title='Register Doctor', form=form)

@app.route("/loginDoc", methods=['GET', 'POST'])
def loginDoc():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'samarth@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('doctor'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('loginDoc.html', title='Login Doctor', form=form)

@app.route("/doctor",methods=['GET','POST'])
def doctor():
    return render_template('doctor.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')
@app.route("/addRecord")
@login_required
def addRecord():
    return render_template('addRecordPat.html')

@app.route("/addRecord1",methods=["POST","GET"])
@login_required
def addRecord1():
    if request.method == 'GET':
        name = request.args.get('full_name')
        age = request.args.get('age')
        cholestrol = request.args.get('cholestrol')
        glucose = request.args.get('glucose')
        bp = request.args.get('bp')
        skin = request.args.get('skin')
        insulin = request.args.get('insulin')
        bmi = request.args.get('bmi')
        pedi = request.args.get('pedi')
        pregnancy = request.args.get('pregnancy')
        patientRecord = PatientRecords(username = name,age = age,cholestrol=cholestrol,glucose=glucose,bp=bp,skin=skin,insulin=insulin,bmi=bmi,pedi=pedi,pregnancies=pregnancy)
        db.session.add(patientRecord)
        db.session.commit()
        flash(f'Record added Successfully', 'success')
        import csv   
        fields=[pregnancy,glucose,bp,skin,insulin,bmi,pedi,age,1]
        with open(r'diabetes.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        return redirect(url_for('viewRecords'))
        return render_template('addRecordPat.html')


@app.route("/assistMe")
@login_required
def assistMe():
    return render_template('diagnoseMe.html')

df1 = pd.read_csv('diabetes.csv')
X1, y1 = df1.iloc[:, :-1], df1.iloc[:, -1]
mod = RandomForestClassifier()
mod.fit(X1,y1)
df = pd.read_csv('Training.csv')
df.head()
X = df.iloc[:, :-1]
y = df['prognosis']
rf_clf = RandomForestClassifier()
rf_clf.fit(X, y)
@app.route("/diagnoseMe")
@login_required
def diagnoseMe():
    return render_template('diagnoseMe.html')

@app.route("/viewRecords")
@login_required
def viewRecords():
    record = PatientRecords.query.all()
    return render_template('viewRecords.html',records = record)

# @app.route("/bhalla")
# @login_required
# def bhalla():
#     return render_template('bhalla.html',diseases=[0.1,0.2,0.3,0.3,0.1],probabilities=["typhoid","hepatitis","aids","cancer","tuberculosis"])


diagnoseMe = False
symptom = []
counter = 1
diabetes = False
values=[]
count=0
ques =[" Number of Pregnancy?","Glucose Level?","Blood Pressure?","Skin Thickness in mm?","Insulin Levels?","BMI?","Diabetes Pedigree Function Score?","Age?"]
data = []
med = False
presname = False
medfirst = False
sum1=0
num=0
test = False
depr = ["Do you ever feel sucidial?", "Are you experiencing difficulty to sleep?","Are you feeling anxious?","Do you experiece inappropriate guilt?","Do you experience any fatigue or loss in energy?","Are you felling difficulty in concentrating or making decisions ?","Do you remain in depressed mood most of the day?","Are you experiencing change in apetite?","Have you recently gained or lost a lot of weight?","Are you feeling worthless,helpless and hopeless"]
@app.route('/response')
@login_required
def response():
      global diagnoseMe,counter,symptom,count,values,ques,diabetes,med,data,presname,medfirst,sum1,num,depr,test
      result = request.args.get('message')
      if result!=None:
           

            if diagnoseMe == True and result!="done":
                  result = result.replace(" ","_")
                  symptom.append(result)
            if result =="diagnose me":
                  diagnoseMe = True
                  return render_template("answer.html",result = "Give symptoms you are facing, Say done when completed")
            if diagnoseMe == True and result=="done":
                  diagnoseMe=False
                  pr = predict(symptom)
                  symptom = []
                  counter = 0
                  return render_template("answer.html",result = "You might have "+str(pr))
            if diagnoseMe is True and result!="done":
                  counter+=1
                  res = "Give me symptom number "+str(counter+1)
                  return render_template("answer.html",result = res)


            if diabetes ==True:
                values.append(result)
            if result == "check for diabetes":
                diabetes = True 
                return render_template("answer.html",result = "Enter Number of pregnancies")
            if diabetes ==True and count<7:
                count=count+1
                return render_template("answer.html",result = ques[count])
            if diabetes ==True and count==7:
                diabetes = False
                pr1 = predict1(values)
                values=[]
                count=0
                return render_template("answer.html",result=pr1)
            

            if result =="note prescription":
                presname = True
                return render_template("answer.html",result = "Ok! What is Patient Name?")
            if presname==True:
                data.append(result)
                presname=False
                med = True
                medfirst = True
                return render_template("answer.html",result = "What is First Medicine, Say Done when completed")  
            if result == "done":
                med=False
                medfirst=False
                presname=False
                data1 = data.copy()
                data=[]
                return render_template("answer.html",result = "Ok! Prescription Saved in PDF")
            if medfirst == True:
                data.append(result)
                medfirst=False
                return render_template("answer.html",result = "What is Dosage")

            if result == "done":
                med=False
                return render_template("answer.html",result = "Ok! Prescription Saved")
            if med==True and medfirst==False:
                data.append(result)
                medfirst=True
                return render_template("answer.html",result = "Give Medicine Name")



            if result=="test for depression":
                test = True
                return render_template("answer.html",result = depr[0])
            if test==True and result=="yes" and num<9:
                sum1=sum1+1
                num=num+1
                return render_template("answer.html",result = depr[num])
            if test==True and result=="no" and num<9:
                num=num+1
                return render_template("answer.html",result = depr[num])
            if num==len(depr)-1:
                res = check(sum1)
                sum1=0
                num=0
                test=False
                return render_template("answer.html",result = res )

      if result!=None:
            rect = searching(result)
            if rect is None:
                  rect = worker(result)
            return render_template("answer.html",result = rect)
      else:
            return render_template("diagnoseMe.html")


flag = False
food = ""
restaurant_check = False
line_num = -1
driver = ""

diagnoseMe = False
symptom = []
counter = 0

f = open("response.txt","r")
num_of_lines = sum(1 for line in open('response.txt'))

def worker(mesg):
      global food,restaurant_check,driver,diagnoseMe,symptom,counter
      f = open("response.txt","r")
      lines = f.readlines()
      num_of_lines = len(lines)
      counter = -1
      num = 0
      line_to_print = -1

      if restaurant_check==True and mesg.lower()!="cancel order":
            from selenium import webdriver
            from selenium.webdriver.common.keys import Keys
            try:
                  mesg = mesg.title()
                  restaurant = driver.find_element_by_link_text(mesg)
                  restaurant.click()
                  time.sleep(2)
                  order_button = driver.find_element_by_link_text("Order Food Online")
                  order_button.click()
                  time.sleep(4)
                  search2 = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div[2]/div[2]/div/input')
                  search2.send_keys(food)
                  restaurant_check = False
                  time.sleep(10)
                  browser.quit()
                  return "Order placed successfully"
            except:
                  restaurant_check = False
                  driver.quit()
                  return "Order placed. Bingo!"
            return

    
      if mesg.lower() =="open chrome":
            subprocess.call("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")

      elif len(re.findall("calculate ",mesg.lower()))>0:
            b=mesg.lower().split("calculate ")[1].strip()
            a=b.replace(" ","")
            return eval(a)
            
      elif len(re.findall("play ",mesg.lower()))>0:
            song = mesg.lower().split("play ")[1].strip()
            qry = "youtube" + song
            for j in search(qry, tld="co.in", num=1, stop=1, pause=2): 
                  webbrowser.open(j) 
                  break

      elif len(re.findall("search ",mesg.lower()))>0:
            query = mesg.lower().split("search ")[1].strip()
            for j in search(query, tld="co.in", num=1, stop=1, pause=2): 
                  webbrowser.open(j) 
                  break


      elif len(re.findall(("order"),mesg.lower()))>0 and len(re.findall(("from"),mesg.lower()))==0:
            from selenium import webdriver
            from selenium.webdriver.common.keys import Keys
            order_what = mesg.split("order")[1].strip()
            driver = webdriver.Chrome("C:\\Users\\LENOVO\\Desktop\\chromedriver.exe")
            driver.maximize_window()
            driver.get("https://www.zomato.com/vellore")
            driver.implicitly_wait(10)
            search_bar = driver.find_element_by_id("keywords_input")
            search_bar.send_keys(order_what)
            time.sleep(8)
            pyautogui.typewrite(["enter"])
            pyautogui.typewrite(["enter"])
            restaurant_check = True
            food = order_what
            time.sleep(10)
            return "Which Restaurant do you want to order from?"


      for i in range(num_of_lines):
            wordset = lines[i].strip()
            a = checkMaxOccurence(wordset.split("|"),mesg)
            if num<a:
                  num = a
                  line_to_print = counter+1
            counter+=1

      if line_to_print is not -1:
            return lines[line_to_print].strip().split("|")[1]



def checkMaxOccurence(wordset,message):
    count = 0
    message_arr = message.split(" ")
    wordset_arr = wordset[0].split(".")
    for i in range(len(message_arr)):
        search_list = wordset_arr.count(message_arr[i].lower())
        count = count + search_list
    return count

def searching(mes):
      global flag
      global line_num   
      h= open("sentences.txt","r")
      line = h.readlines()
      num_of_line = len(line)
            
      if flag==True:
            x = line[line_num].split("|")
            y = x[0].split("{")

            matchfrom = y[0].split(",")
            matchfromnext = []
            for i in range(1,len(y)):
                  matchfromnext.append(y[i].split("*")[0])
            responsenext = []
            for i in range(1,len(y)):
                  responsenext.append(y[i].split("*")[1])
            for i in range(len(matchfromnext)):
                  if mes==matchfromnext[i]:
                        flag=False
                        return responsenext[i]

            if flag==True:
                  flag = False
                  for i in range(num_of_line):
                        res = line[i].split("|")
                        z = res[0].split("{")
                        if len(z)<2:
                              sentences = res[0].split(",")
                              if sentences.count(mes.lower())>0:
                                    choices=res[1].split("@")
                                    a=random.choice(choices)
                                    line_num = i
                                    return a
                        else:
                              matchfrom = z[0].split(",")
                              if matchfrom.count(mes.lower())>0:
                                    line_num = i
                                    flag = True
                                    some = res[1].split("@")
                                    return random.choice
                              else:
                                    flag = False 

      elif flag==False:
            for i in range(num_of_line):
                  res = line[i].split("|")
                  z = res[0].split("{")
                  if len(z)<2:
                        sentences = res[0].split(",")
                        if sentences.count(mes.lower())>0:
                              choices=res[1].split("@")
                              a=random.choice(choices)
                              h.close()
                              line_num = i
                              return a
                  else:
                        matchfrom = z[0].split(",")
                        if matchfrom.count(mes.lower())>0:
                              line_num = i
                              flag = True
                              some = res[1].split("@")
                              return random.choice(some)
                        else:
                              flag = False                 


def predict1(sym):
    symps = np.array([sym])
    pr = mod.predict(symps)
    if (pr[0]==1):
        return "Yes, you have Diabetes"
    else:
        return "No, you do not have Diabetes"

def predict(sym):
      global rf_clf,X,Y
      symptoms_dict = {}
      for index, symptom in enumerate(X):
            symptoms_dict[symptom] = index
      input_vector = np.zeros(len(symptoms_dict))
      for i in sym:
        input_vector[[symptoms_dict[i]]] = 1
      problist = rf_clf.predict_proba([input_vector])
    #   problist = problist.sort(reverse=True)
    #   toplist = problist[0:5]
      pred = rf_clf.predict([input_vector])
      return pred[0]

def check(count1):
    if count1>=8:
        return "Immediately refer Psychaiatrist"
    elif count1>5 and count1<8:
        return "you need help, my friend!!"
    else:
        return "Stay the same friend!!"
