from __init__ import *
from controller import *
from model import *
from engine_cloudinary import *

@app.route('/')
def index():
	return hello()

@app.route('/signup', methods=['POST'])
def signup():
	return register()

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

@app.route('/api/v3/image', methods=['POST'])
def image():
	return upload_images()