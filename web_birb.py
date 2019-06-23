#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import os
import json

#get and set the file path for the json file
dn = os.path.dirname(os.path.realpath(__file__))
json_file = os.path.join(dn, 'search_terms.json')

app = Flask(__name__)

#function that loads json file
def load_json(json_file):
	with open(json_file, "r") as read_file:
		return json.load(read_file)

#function that saves(dumps) the json file
def save_json(json_obj, json_file):
	with open(json_file, "w") as write_file:
		json.dump(json_obj, write_file)

#renders the "home page"
@app.route('/')
def index():
	data = load_json(json_file)
	terms_list = data['terms']
	return render_template('index.html', terms_list = terms_list)

#function that adds a search term to the json file when submitted through the online form
@app.route('/add', methods=['POST'])
def add():
	data = load_json(json_file)
	new_term = request.form['searchterm']
	data['terms'].append(new_term)
	data['terms'].sort() #leave in for alphabetical sorting, comment out for order entered 
	save_json(data, json_file)

	return redirect(url_for('index'))

#function the deletes search term(s) when submitted through the online form
@app.route('/delete', methods=['POST'])
def delete():
	data = load_json(json_file)
	to_delete = request.form.to_dict()
	for key in to_delete:
		data['terms'].remove(key)
	save_json(data, json_file)

	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)