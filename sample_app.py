from flask import Flask
from flask import request, render_template

sample = Flask(__name__)

@sample.route("/")
def main():
	return render_template('index.html')

if __name__ == '__main__':
	sample.run(port=8888, host="0.0.0.0")
