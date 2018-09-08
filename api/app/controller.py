import datetime
from itsdangerous import TimestampSigner
from werkzeug.security import generate_password_hash, check_password_hash
from model import *
from sqlalchemy import *

def hello():
	return jsonify({'msg': "Hello World"})

def token_generator(name):
	s = TimestampSigner('sugars-n-salts')
	token = s.sign(name)
	s.unsign(token, max_age=1000000)
	return token

def token_checker(token):
	itExist = User.query.filter_by(token = token).first()
	if itExist: return True
	else: return jsonify({'error':"token does not match."})

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
		db.session.commit()
		return jsonify({'msg':"success",'acc_id':checkUser.acc_id,'token':checkUser.token})
	else: return jsonify({'error':'wrong email/name or password'})

def add_stories():
	data = request.get_json()
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		try:
			acc_id = data['acc_id']
			title = data['title']
			text = data['text']
			story = Records(acc_id = acc_id, title = title, text=text)
			db.session.add(story)
			db.session.commit()
			return jsonify({'msg':"Successfully added."})
		except:
			return jsonify({'error':"Fail to add."})
	else:
		return itExist

def edit_Stories():
	data = request.get_json()
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		try:
			acc_id = data['acc_id']
			rec_id = data['rec_id']
			dataEdited = data['dataEdited']
			recordEdit = Records.query.filter_by(acc_id=acc_id).filter_by(rec_id=rec_id).first()
			recordEdit.text = dataEdited
			db.session.commit()
			return jsonify({'msg':"Successfully Edited."})
		except:
			return jsonify({'error':"Fail to Edit."})
	else:
		return itExist


def edit_titles():
	data = request.get_json()
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		try:
			acc_id = data['acc_id']
			rec_id = data['rec_id']
			titleEdited = data['titleEdited']
			recordEdit = Records.query.filter_by(acc_id=acc_id).filter_by(rec_id=rec_id).first()
			recordEdit.text = titleEdited
			db.session.commit()
			return jsonify({'msg':"Successfully Edited."})
		except:
			return jsonify({'error':"Fail to Edit."})
	else:
		return itExist


def delete_Stories():
	data = request.get_json()
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		try:
			acc_id = data['acc_id']
			rec_id = data['rec_id']
			recordDelete = Records.query.filter_by(acc_id=acc_id).filter_by(rec_id=rec_id).first()
			db.session.delete(recordDelete)
			db.session.commit()
			return jsonify({'msg':"Successfully Deleted."})
		except:
			return jsonify({'error':"Fail to Delete."})
	else: return itExist

def search_Stories():
	data = request.get_json()
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		try:
			acc_id = data['acc_id']
			search = data['search']
			matches = Records.query.filter_by(acc_id=acc_id).filter(or_(Records.title.ilike("%"+search+"%"),Records.text.ilike("%"+search+"%"))).all()
			result = records_schema.dump(matches)
			return jsonify(result.data)
		except:
			return jsonify({'error':"Search Does Not Match Any."})
	else:
		return itExist

def user_stories():
	data = request.get_json()
	acc_id = data['acc_id']
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		specStories = Records.query.filter_by(acc_id=acc_id).all()
		schemes = records_schema.dump(specStories)
		return jsonify(schemes.data)
	else:
		return itExist