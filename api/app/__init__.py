from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sqlalchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('data', MigrateCommand)



if __name__ == '__main__':
	manager.run()

# def createDB():
#     engine = sqlalchemy.create_engine("postgres://localhost/mydb")# connects to server
#     engine.execute("CREATE DATABASE IF NOT EXISTS data") #create db
#     if not database_exists(engine.url):
#     	create_database(engine.url)
#     print(database_exists(engine.url))

# def createTables():
#     db.create_all()

# createDB()