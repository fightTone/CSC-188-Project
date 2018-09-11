from __init__ import *
from controller import *
from model import *

@app.route('/')
def index():
	return hello()

@app.route('/sample')
def sample():
	return "<h1>Sample</h1>"


@app.route('/signup', methods=['POST'])
def signup():
	return register()

@app.route('/alluser', methods=['POST'])
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

@app.route('/searchStory', methods=['POST'])
def searchStory():
	return search_Stories()

@app.route('/myStory',methods=['POST'])
def myStory():
	return user_stories()

@app.route('/api/v3/image', methods=['POST'])
def image():
	return upload_images()