from flask import Flask
from app import routes


if __name__ == '__main__':
	routes.app.run(debug=True)