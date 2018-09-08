import datetime
from itsdangerous import TimestampSigner
from werkzeug.security import generate_password_hash, check_password_hash
from model import *

def hello():
	return jsonify({'msg': "Hello World"})

def token_generator(name):
	s = TimestampSigner('sugars-n-salts')
	token = s.sign(name)
	s.unsign(token, max_age=1000000)
	return token

def register():
	data = request.get_json()
	hashed_password = generate_password_hash(data['password'], method='sha256')
	name=data['name']
	token = token_generator(name)
	new_acc = User(name=name, email=data['email'], password=hashed_password, token=token)
	db.session.add(new_acc)
	db.session.commit()
	return jsonify({'message' : 'New user created.', 'name': new_acc.name, 'token': new_acc.token, 'acc_id':new_acc.acc_id, 'email':new_acc.email})

def user_viewer():
	data = request.get_json()
	acc_id = data['acc_id']
	token = data['token']
	accExist = User.query.filter_by(acc_id = acc_id).filter_by(token = token).first()
	if accExist:
		allUser = User.query.all()
		schemes = users_schema.dump(allUser)
		return jsonify(schemes.data)
	else:
		return jsonify({'error':"accountID or token does not match any."})

def loginUser():
	data = request.get_json()
	email = data['email']
	password = data['password']
	checkUser = User.query.filter_by(email = email).first()

	if check_password_hash(checkUser.password, password):
		checkUser.token = token_generator(email)
		return jsonify({'msg':"success",'acc_id':checkUser.acc_id,'token':checkUser.token})
	else: return jsonify({'error':'wrong email/name or password'})