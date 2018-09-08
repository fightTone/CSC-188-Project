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
	jayson = user_viewer()
	return jayson

@app.route('/login', methods=['POST'])
def login():
	jayson = loginUser()
	return jayson