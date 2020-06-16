from flask import Flask, render_template, request,url_for,redirect
import pandas as pd
import getindex
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import folium
from folium.plugins import HeatMap,Fullscreen

# class FormIndex(FlaskForm):
#     ind_education = StringField('index_formcation')
#     submit= SubmitField('Sign up')

app = Flask(__name__)


@app.route('/index', methods=['POST', 'GET'])
def index():
    list_weights=[]
    if request.method == 'POST':

        #obtaining each index from html and adding it to a list
        index_form = request.form["sl_education"]
        list_weights.append(index_form)
        index_form = request.form["sl_educationcount"]
        list_weights.append(index_form)
        index_form = request.form["sl_price"]
        list_weights.append(index_form)
        index_form = request.form["sl_buss"]
        list_weights.append(index_form)
        index_form = request.form["sl_bicing"]
        list_weights.append(index_form)
        index_form = request.form["sl_metro"]
        list_weights.append(index_form)
        index_form = request.form["sl_trasp"]
        list_weights.append(index_form)
        index_form = request.form["sl_tree"]
        list_weights.append(index_form)
        index_form = request.form["sl_hosp"]
        list_weights.append(index_form)
        index_form = request.form["sl_env"]
        list_weights.append(index_form)
        index_form = request.form["sl_pub_ord"]
        list_weights.append(index_form)
        index_form = request.form["sl_nei_coe"]
        list_weights.append(index_form)
        index_form = request.form["sl_safety"]
        list_weights.append(index_form)
        index_form = request.form["sl_road_sys"]
        list_weights.append(index_form)
        index_form = request.form["sl_hire_rep"]
        list_weights.append(index_form)

        final_index = getindex.fun_getindex(list_weights)

        #print(final_index)

        return redirect(url_for('mapindex',ind=final_index))#, ind=index_form)
    else:
        # form=FormIndex()
        return render_template('index.html')


@app.route('/<ind>', methods=['POST', 'GET'])
def mapindex(ind):

    #return f"<h1>{ind}</h1>"
    return render_template('Green_Index_1.html')


if __name__ == '__main__':
    app.run(debug=True)
