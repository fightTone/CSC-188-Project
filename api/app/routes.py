from __init__ import *
from controller import *
from model import *

@app.route('/')
def index():
	x = hello()
	return x

@app.route('/signup', methods=['POST'])
def signup():
	jayson = register()
	return jayson

@app.route('/alluser', methods=['GET'])
def alluser():
	return user_viewer()

@app.route('/login', methods=['POST'])
def login():
	return loginUser()

@app.route('/addStory', methods=['POST'])
def addStory():
	return add_stories()

@app.route('/editStory', methods=['POST'])
def editStory():
	return edit_Stories()

@app.route('/editTitle', methods=['POST'])
def editTitle():
	return edit_titles()

@app.route('/deleteStory', methods=['POST'])
def deleteStory():
	return delete_Stories()

@app.route('/searchStory', methods=['GET'])
def searchStory():
	return search_Stories()

@app.route('/myStory',methods=['GET'])
def myStory():
	return user_stories()