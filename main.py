from flask import request, Flask, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join
from datetime import datetime
import sqlite3 
import uuid
import sqlite3 

  
app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = 'files/'

databasename = 'datazain.db'
column_names = ['user', 'caption', 'fileloc', 'time']

connect = sqlite3.connect(databasename) 
connect.execute(
    'CREATE TABLE IF NOT EXISTS POSTS (USER TEXT, CAPTION TEXT, FILELOC TEXT, TIME TEXT)') 

@app.route('/')
def home():
    return {'are you here': 'this is home page it is useless'}

@app.route('/getPhoto/<filename>', methods = ['GET'])
def getPhoto(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/addAZ', methods = ['POST']) 
def addAZ():
    print(request.data, request.args, request.form)
    if 'file' not in request.files:
        return '', 304

    file = request.files['file']
    caption = str(request.form.get('caption', ''))
    user = str(request.form.get('user', ''))

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '' or not file or not caption or not user:
        return '', 305

    filename = str(uuid.uuid4()) + file.filename
    file.save(join(app.config['UPLOAD_FOLDER'], filename))

    with sqlite3.connect(databasename) as users: 
        cursor = users.cursor() 
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cursor.execute("""INSERT INTO POSTS 
        (USER,CAPTION,FILELOC,TIME) VALUES (?,?,?,?)""", 
                        (user, caption, filename, upload_time)) 
        users.commit() 
    return '', 200

@app.route('/getAZ', methods = ['GET']) 
def getAZ():
    
    no = str(request.args.get('number', '0'))
    # user = str(request.data.get('user', ''))

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    with sqlite3.connect(databasename) as users: 
        cursor = users.cursor() 
        cursor.execute(f'SELECT * FROM POSTS LIMIT {no}') 
        data = cursor.fetchall() 
        result = {i: {column_names[j]: data[i][j] for j in range(len(data[i]))} for i in range(int(no))} # fuck yea
    return result



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)