import sqlite3
import sqlite3 as sq

from flask import *
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route("/formsave",methods=["POST","GET"])
def formsave():
    if request.method =="POST":
        fn= request.form["fullname"]
        em = request.form["mail"]
        ps = request.form["pass"]
        cn = request.form["contact"]
        ad = request.form["address"]
        con = sqlite3.connect("mywebsite.db")
        c = con.cursor()
        c.execute("insert into student(fullname,mail,pass,contact)values(?,?,?,?)",(fn,em,ps,cn))
        con.commit()
        return render_template('index.html')
    else:
        return "registration fail"

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/browse_item')
def browse_item():
    return render_template("browse_item.html")

@app.route('/report_lost')
def report_lost():
    return render_template("report_lost.html")

@app.route("/report_found")
def report_found():
    return render_template("report_found.html")


if __name__== "__main__" :
    app.run(debug=True , port="1234")
