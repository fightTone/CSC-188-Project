import datetime
from itsdangerous import TimestampSigner
from werkzeug.security import generate_password_hash, check_password_hash
from model import *
from sqlalchemy import *
from werkzeug import secure_filename
from engine_cloudinary import *


img_folder = 'app/static/uploads/img/'
audio_folder = 'app/static/uploads/audio/'
profile_folder = 'app/static/uploads/profile/'

img_folder_alter = '/static/uploads/img/'
audio_folder_alter = '/static/uploads/audio/'
profile_folder_alter = '/static/uploads/profile/'

app_dump = 'app/dumps'

available_extension = set(['png', 'jpg', 'PNG', 'JPG', 'mp3', 'm4a', 'flac', 'aac'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension



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
			edited_story = Records.query.filter_by(acc_id=acc_id).filter_by(rec_id=rec_id).first()
			schemes = record_schema.dump(edited_story)
			return jsonify(schemes.data)
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
			recordEdit.title = titleEdited
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

def view_Story():
	data = request.get_json()
	token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		try:
			acc_id = data['acc_id']
			story_id = data['story_id']
			matches = Records.query.filter_by(acc_id=acc_id).filter_by(rec_id = story_id).first()
			result = record_schema.dump(matches)
			return jsonify(result.data)
		except:
			return jsonify({'error':"Story Does Not Match Any."})
	else:
		return itExist

def user_stories(acc_id,token):
	# data = request.get_json()
	# acc_id = data['acc_id']
	# token = data['token']
	itExist = token_checker(token)
	if itExist == True:
		specStories = Records.query.filter_by(acc_id=acc_id).all()
		schemes = records_schema.dump(specStories)
		return jsonify(schemes.data)
	else:
		return itExist

def upload_images():
	token = request.form['token']
	itExist = token_checker(token)
	if itExist == True:
	    acc_id = request.form['acc_id']
	    img_type = request.form['img_type']
	    file1 = request.files['image']
	    typpe1 = request.form['type1']
	    tempid = random.randint(1, 200)
	    
	    msg = cloudinary_upload(acc_id, img_type, file1,tempid, typpe1, allowed_file, app_dump, Images)
	    uploaded = Images.query.filter_by(acc_id = request.form['acc_id']).filter_by(img_type =request.form['img_type']).first()
	    return jsonify({'msg': msg,'id':uploaded.acc_id,'img':uploaded.img})
	else:
		itExist