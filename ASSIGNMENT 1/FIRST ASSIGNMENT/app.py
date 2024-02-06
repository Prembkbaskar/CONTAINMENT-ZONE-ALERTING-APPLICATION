from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('web.html')

@app.route('/login',methods = ["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form
        return render_template("web.html", x = user)

  

if __name__ == '__main__':
    app.run(debug = True)