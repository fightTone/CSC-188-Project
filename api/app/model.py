from __init__ import *
import datetime




class User(db.Model):
    acc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100), unique=False)
    token = db.Column(db.String(300))
    id_rec = db.relationship("Records", uselist=False, backref="record")


    def __init__(self, name, email, password, token):
        self.name = name
        self.email = email
        self.password = password
        self.token = token

class UserSchema(ma.Schema):
    class Meta:
        fields = ('acc_id','name','email','token')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Records(db.Model):
    id_stor =db.relationship("Images",uselist=False, backref="image")
    rec_id = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.Integer, db.ForeignKey('user.acc_id'))
    title = db.Column(db.String(30))
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, acc_id, title, text):
		self.acc_id = acc_id
		self.title = title
		self.text = text

class RecordSchema(ma.Schema):
    class Meta:
        fields = ('rec_id','acc_id','title','text','created_date')

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

class Images(db.Model):
    img_id = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.Integer, db.ForeignKey('user.acc_id'))
    story_id = db.Column(db.Integer, db.ForeignKey('records.rec_id'))
    img_type = db.Column(db.String(50))
    img = db.Column(db.String(500))

    def __init__(self,acc_id, img_type, story_id, img):
        self.acc_id = acc_id
        self.img_type = img_type
        self.story_id = story_id
        self.img = img

class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('img_id', 'acc_id', 'story_id', 'img_type', 'img')

image_schema = ImagesSchema()
images_schema = ImagesSchema(many=True)

db.create_all()