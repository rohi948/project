from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME']= 'intellipaat'
app.config['MONGO_URI'] ='mongodb+srv://krrohi:<qvqOVAt5AvD1hvTT>@cluster0.cxikcfz.mongodb.net/'

mongo = PyMongo(app)

@app.route('/')

def index():
    if 'username' in session:
        return 'you are logged in as the following user: ' +session['username']
    

    return render_template('sample.html')

@app.route('/login',methods=['POST'])
def login():

  users = mongo.db.users
  login_user = users.find_one({'name': request.form['username']})
  
  if login_user:
      if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
         session['username'] = request.form['username'] 
         return redirect(url_for('index'))

  return 'invalid username or password combination'

@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method== 'POST':
        users= mongo.db.users
        existing_user =users.find_one({'name': request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
        return redirect(url_for('index'))
    return 'username already in database'
    return render_template('register.html')      
              
if __name__ == '__main__':
    app.secret_key= 'secretivekeyagain'
    app.run(debug=True)      
          
