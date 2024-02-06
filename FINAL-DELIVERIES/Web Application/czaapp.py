from flask import Flask, render_template, request, redirect, url_for,session
import os
import ibm_db
import bcrypt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=certificate.crt;PROTOCOL=TCPIP;UID=bkk21708;PWD=CqbgdenpsDJbwhug;",'','')

app = Flask(__name__)
app.secret_key = b'\xb5\x89K(\x93'


@app.route('/')
def index():
  return redirect(url_for('home'))
@app.route('/index', methods=['GET','POST'])
def home():
  if 'name' in session:
    return render_template('index.html',name=session['name']+"'s account")
  else:
    return render_template('index.html')

@app.route("/registercus",methods=['GET','POST'])
def registercus():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if not email or not name or not password or not cpassword:
      return render_template('registercus.html',error='Please fill all fields')
    if password != cpassword:
        return render_template('registercus.html',error='The password is not same')
    else:
        hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    query = "SELECT * FROM USER WHERE EMAIL=?;"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO USER VALUES(?, ?, ?);"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, hash)
      ibm_db.execute(prep_stmt)
      return render_template('registercus.html',success="You can login")
    else:
      return render_template('registercus.html',error='Invalid Credentials')

  return render_template('registercus.html')

@app.route("/registerhos",methods=['GET','POST'])
def registerhos():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if not email or not name or not password or not cpassword:
      return render_template('registerhos.html',error='Please fill all fields')
    if password != cpassword:
        return render_template('registerhos.html',error='The password is not same')
    else:
        hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    query = "SELECT * FROM HOSPITAL WHERE EMAIL=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO HOSPITAL VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, hash)
      ibm_db.execute(prep_stmt)
      return render_template('registerhos.html',success="You can login")
    else:
      return render_template('registerhos.html',error='Invalid Credentials')

  return render_template('registerhos.html')

@app.route("/logincus",methods=['GET','POST'])
def logincus():

    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']


      if not email or not password:
        return render_template('logincus.html',error='Please fill all fields')

      elif(email == 'admin@gmail.com' and password == 'admin@123'):
        return redirect(url_for('AdminMap'))
      query = "SELECT * FROM USER WHERE EMAIL=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('logincus.html',error='Invalid Credentials1')
      #return render_template('login.html',error=isUser['PASSWORD'])
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))


      if not isPasswordMatch:
        return render_template('logincus.html',error='Invalid Credentials2')

      session['email'] = isUser['EMAIL']
      session['name'] = isUser['NAME']
      return redirect(url_for('home'))
      #return render_template('/index.html')

    if 'name' in session:
      return render_template('/logincus.html',name=session['name'])
    return render_template('/logincus.html',name="")

@app.route("/loginhos",methods=['GET','POST'])
def loginhos():

    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']


      if not email or not password:
        return render_template('loginhos.html',error='Please fill all fields')

      elif(email == 'admin@gmail.com' and password == 'admin@123'):
        return redirect(url_for('AdminMap'))
      query = "SELECT * FROM HOSPITAL WHERE EMAIL=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('loginhos.html',error='Invalid Credentials1')
      #return render_template('login.html',error=isUser['PASSWORD'])
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))


      if not isPasswordMatch:
        return render_template('loginhos.html',error='Invalid Credentials2')

      session['email'] = isUser['EMAIL']
      session['name'] = isUser['NAME']
      session['admin'] = 1
      
      return redirect(url_for('home'))
      #return render_template('/index.html')

    if 'name' in session:
      return render_template('/loginhos.html',name=session['name'])
    return render_template('/loginhos.html',name="")

#Storing latitude and langitude in db
@app.route('/latandlng', methods=['POST','GET'])
def storemark():
  if request.method == 'POST':
    lat = request.form['lati']
    lng = request.form['lang']
    desc = request.form['discript']
    active = request.form['active']
    total = request.form['total']
    insert_sql = "INSERT INTO LOCATION(LATITUDE, LANGTITUDE, DESCRIPTION, TOTALCASE, ACTIVECASE) VALUES (?,?,?,?,?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, lat)
    ibm_db.bind_param(prep_stmt, 2, lng)
    ibm_db.bind_param(prep_stmt, 3, desc)
    ibm_db.bind_param(prep_stmt, 4, total)
    ibm_db.bind_param(prep_stmt, 5, active)
    ibm_db.execute(prep_stmt)
    # sendmail()
  return redirect(url_for('AdminMap'))

@app.route('/admin_map')
def AdminMap():
  mark = addMarker()
  return render_template('admin_map.html',mark=mark,len = len(mark))

def addMarker():
  query = "SELECT * FROM LOCATION;"
  stmt = ibm_db.prepare(conn, query)
  # ibm_db.bind_param(stmt,1,lat)
  # ibm_db.bind_param(stmt,2,lng)
  # ibm_db.bind_param(stmt,3,des)
  ibm_db.execute(stmt)
  isUser = ibm_db.fetch_assoc(stmt)
  data=[]
  while(isUser!=False):
    data.append(isUser)
    isUser = ibm_db.fetch_assoc(stmt)

  print (data[0]['LANGTITUDE'])
  print (data[0]['LATITUDE'])
  return data


@app.route('/user_map')
def UserMap():
  if 'email' not in session:
      return redirect(url_for('logincus'))
  else:
    mark = addMarker()
    
  return render_template('user_map.html',mark = mark, len = len(mark))

@app.route('/calltoaction')
def calltoaction():
  if 'email' not in session:
      return redirect(url_for('logincus'))
  elif 'admin' in session :
    mark = addMarker()
    return render_template('admin_map.html',mark=mark,len = len(mark))
  else:
    mark = addMarker()
  return render_template('user_map.html',mark = mark, len = len(mark))


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('admin',None)
    return redirect(url_for('home'))

@app.route('/mail')
def mail():

     return render_template('mail.html')



if __name__ == "__main__":
  app.run(debug=True)
    #,host='0.0.0.0'


 