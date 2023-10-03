from flask import Flask, render_template, request, url_for, session, redirect, g, send_from_directory
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv



load_dotenv()
UPLOAD_FOLDER = str(os.getenv('UPLOAD_PATH'))
ALLOWED_EXTENSIONS = os.getenv('EXTENSIONS')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.secret_key = str(os.getenv('SECRET_KEY'))


class User:
    def __init__(self, id, username, password, name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        return f'<User: {self.username}>'



users = []
users.append(User(id=1, 
                  username=str(os.getenv('FIRST_USER')), 
                  password=str(os.getenv('FIRST_PASSWORD')), 
                  name=str(os.getenv('FIRST_NAME'))))

users.append(User(id=2, 
                  username=str(os.getenv('SECOND_USER')), 
                  password=str(os.getenv('SECOND_PASSWORD')), 
                  name=str(os.getenv('SECOND_NAME'))))


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/')
def index():
    if request.method == 'GET':    
        if not g.user:
            return redirect(url_for('login'))
        return render_template('index.html')




@app.route('/file_submitted', methods=['POST'])
def fileSumbit():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    justFilename = filename.split('.')[0]
    extension = filename.split('.')[1]
    
    if extension in ALLOWED_EXTENSIONS:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('file_submit.html', filenamePage=justFilename, extensionPage=extension)

    else:
        return render_template('file_fail.html', filenamePage=filename, extensionPage=extension)




@app.route('/list', methods=['GET'])
def fileList():
    if not g.user:
        return redirect(url_for('login'))
    pathFolder = app.config['UPLOAD_FOLDER'] + '/'
    array = os.listdir(pathFolder)

    extArray = []
    fileSizeArray = []

    for item in array:
        ext = item.split('.')
        extArray.append(ext[-1].upper())
        
        sizeFile = os.path.getsize(pathFolder + item)
        sizeFile /= 1000000
        sizeFile = f'{sizeFile:.2f}MB'
        fileSizeArray.append(sizeFile)

    arraySize = len(array)
    return render_template('list.html', array=array, extArray=extArray, fileSizeArray=fileSizeArray, arraySize=arraySize)




@app.route('/list/<name>')
def downloadFile(name):
    if not g.user:
        return redirect(url_for('login'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


if __name__ == '__main__':
    app.run(debug=True)
