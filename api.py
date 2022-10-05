import numpy as np
import pandas as pd
import datetime as dt
from sklearn.cluster import DBSCAN
import pickle
from flask import Flask, render_template,request, jsonify
from flask import Flask, redirect, url_for, render_template, request, flash

model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

#default page of our web-app
@app.route('/')
def home():
    return render_template('index.html')


def get_infected_names(input_name):

    df = pd.read_json('data.json')

    epsilon = 0.0024384 # a radial distance of 6 feet in kilometers
    model = DBSCAN(eps=epsilon, min_samples=2, metric='haversine').fit(df[['latitude', 'longitude']])
    df['cluster'] = model.labels_.tolist()

    input_name_clusters = []
    for i in range(len(df)):
        if df['id'][i] == input_name:
            if df['cluster'][i] in input_name_clusters:
                pass
            else:
                input_name_clusters.append(df['cluster'][i])
    
    infected_names = []
    for cluster in input_name_clusters:
        if cluster != -1:
            ids_in_cluster = df.loc[df['cluster'] == cluster, 'id']
            for i in range(len(ids_in_cluster)):
                member_id = ids_in_cluster.iloc[i]
                if (member_id not in infected_names) and (member_id != input_name):
                    infected_names.append(member_id)
                else:
                    pass
    
    return infected_names

@app.route('/get_infected',methods=['GET', 'POST'])
def get_infected():
    if(request.method=="POST"):
    
    	input_name = request.form.get('fname')
    	infected_names = get_infected_names(input_name)
    	if(len(infected_names)==0):
            st="No Person Found.!"
            return render_template("/infected.html",inp=input_name,sname=st)
        
    	return render_template("/infected.html",inp=input_name,inf_list=infected_names)
   
    

if __name__ == '__main__':
    app.run(debug=True) 
