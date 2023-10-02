from flask import Flask, render_template, request, url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv



load_dotenv()
UPLOAD_FOLDER = str(os.getenv('UPLOAD_PATH'))
ALLOWED_EXTENSIONS = os.getenv('EXTENSIONS')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = str(os.getenv('SECRET_KEY'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route('/', methods=['GET'])
def indexGet():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/success', methods=['POST'])
def indexPost():
    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = filename.split('.')[1]

    if extension in ALLOWED_EXTENSIONS:

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('success.html', filenamePage=filename)
    
    else:
        return render_template('unsuccess.html', filenamePage=filename, extensionPage=extension)


if __name__ == '__main__':
    app.run(debug=True)
