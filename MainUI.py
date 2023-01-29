#nullable disable
import sqlite3
import flask
from flask import request, jsonify
from flask import Flask, send_file, render_template , request
from bs4 import BeautifulSoup as bs
import requests
import re

from flask import Flask, flash, redirect, render_template, request, session, abort,send_from_directory,send_file,jsonify
import pandas as pd
import glob
import random
import json
from flask_sqlalchemy import SQLAlchemy
app = flask.Flask(__name__)
import ML_code
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb3.db'
db = SQLAlchemy(app)


class User (db. Model):
    username = db.Column (db . String ( 80), primary_key=True, nullable=False)
    email = db.Column(db. String(120), unique=True, nullable=True)
    password = db.Column (db. String (120) ,  nullable=False)
    name = db.Column (db. String (120) ,  nullable=True)
    color = db.Column (db. String (120) ,  nullable=True)
    brand = db.Column (db. String (120) ,  nullable=True)
    gender = db.Column(db.String(10),nullable=True)

    # email = db.Column(db.String(120),nullable=False)
    def _repr_(self):
        return '<User %r>' % self. username
#2. Declare data stores
class DataStore():
    Prod= None
    Prod2=None
    Prod3=None
data=DataStore() 
    
@app.route('/')
def home(): 
    return render_template("website.html")  
tup =[]
filtered=False
@app.route("/filter",methods=['GET','POST'])
def filter():
        if request.method=='POST':
            filtered=True
            gender=request.form.get('Gender')
            if(gender==None):
                gender=[]
            color=request.form.getlist("Color")
            brand = request.form.getlist("Brand")
            if(color==''):
                color=[]
            if(brand==''):
                brand=[]
            sortd = request.form.get('sort')
            sort_order=[0,0]
            numlow=request.form.get('low')
            numhigh=request.form.get('high')
            if(sortd=='lowtohigh'):
                sort_order[0]+=1
            if(sortd=='hightolow'):
                sort_order[1]+=1
            
            tup=[gender,color,brand,sort_order,[numlow,numhigh]]
        
@app.route("/register",methods=['GET','POST'])
def register():
    # print(request.method)
    if request.method=='POST':
        # print("Hello World")
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        username = request.form.get('Uname')
        gender=request.form.get('gender')
        if(gender==None):
            gender='#'
        color=request.form.getlist("color")
        str1 = ','.join(color)
        brand = request.form.getlist("brands")
        str2=','.join(brand)
        if(str1==''):
            str1='#'
        if(str2==''):
            str2='#'
        # cursor.execute('INSERT INTO table (table_name) VALUES (%s)',str1)
        user = User(username=username,email=email,name=name,password=password,color=str1,gender = gender,brand=str2)
 
        db.session.add(user)
        db.session.commit()

        return('User registered successfully')
    
    return render_template("register.html")
current_user=None
user_requests=0
@app.route("/login",methods=['GET','POST'])
def login():
    # print(request.method)
    if request.method=='POST':
        # print("Hello World")
        password = request.form.get('password')
        username = request.form.get('Uname')
        
        all_users = User.query.all()
        flag=False
        for user in all_users:
            if(user.username==username):
                flag=True
                break
        if(flag==True):
            for user in all_users:
                if(user.username==username and user.password==password ):
                    current_user=user
                    print(current_user.password)
                    #filter=[['women'],['blue'],['raymond'],[500,600]]
                    filter=tup
                    result = ML_code.run(filtered,current_user.gender,current_user.brand,current_user.color,filter)
                    links=[]
                    prices=[]
                    titles=[]
                    brands=[]
                    for i in range(len(result)):
                        links.append(result[i][0])
                        prices.append(result[i][1])
                        titles.append(result[i][2])
                        brands.append(result[i][3])
                    import time
                    # img_links=[]
                    # for i in range(1):
                    #     ti=time.time()
                    #     x = requests.get(links[i])
                    #     soup = bs(x.content,'html.parser')
                    #     img_link = soup.findAll("img",{'class':'_2r_T1I _396QI4'})
                    #     img_link = str(img_link)
                    #     img_links.append(img_link[42:-4])
                    #     print(time.time()-ti)
                    # print(img_links)

                    from concurrent.futures import ThreadPoolExecutor

                    img_links = []

                    def get_img_link(link):
                        x = requests.get(link)
                        soup = bs(x.content,'html.parser')
                        img_link = soup.findAll("img",{'class':'_2r_T1I _396QI4'})
                        img_link = str(img_link)
                        img_links.append(img_link[42:-4])
                    ti=time.time()
                    with ThreadPoolExecutor(max_workers=6) as executor:
                        executor.map(get_img_link, links[0:12])
                    print(img_links)
                    print(time.time()-ti)
                    
                    return render_template("temp.html",link=links,prices=prices,titles=titles,brands=brands,img_links=img_links)
        
        return render_template("login.html")  
    return render_template("login.html")




@app.route('/contactus', methods=['GET'])
def api_contactus():
    return render_template("website_contactus.html")
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True,host='0.0.0.0',port=port)












