import sqlite3
import sqlite3 as sq

from flask import *
app = Flask(__name__)
app.secret_key ="12345tghhj"
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template("dashboard.html")

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

@app.route("/logincheck",methods=["post"])
def checkmail():
    if request.method == "POST":
        em=request.form["mail"]
        ps=request.form["pass"]
        con = sqlite3.connect("mywebsite.db")
        c = con.cursor()
        c.execute("select * from student where mail=? and pass=?", (em,ps))
        data = c.fetchall()
        if len(data) == 1:
            session["user"] = em
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if session.get("user") is not None:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user",None)  # session ends
    return redirect(url_for("login"))

@app.route('/browse_item')
def browse_item():
    return render_template("browse_item.html")

@app.route('/report_lost')
def report_lost():
    return render_template("report_lost.html")

@app.route("/lostrepost", methods=["POST"])
def lost_post():
    item_name = request.form["item_name"]
    description = request.form["description"]
    category = request.form["category"]
    location = request.form["location"]
    date = request.form["date"]
    contact = request.form["contact"]

    con = sqlite3.connect("mywebsite.db")
    c = con.cursor()

    c.execute("""
        INSERT INTO posts
        (post_type, item_name, description, category,
         location, date, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "lost",
        item_name,
        description,
        category,
        location,
        date,
        contact
    ))
    con.commit()
    con.close()
    return render_template("report_lost.html")

@app.route("/report_found")
def report_found():
    return render_template("report_found.html")

@app.route("/foundrepost", methods=["POST"])
def found_post():
    item_name = request.form["item_name"]
    description = request.form["description"]
    category = request.form["category"]
    location = request.form["location"]
    date = request.form["date"]
    contact = request.form["contact"]

    con = sqlite3.connect("mywebsite.db")
    c = con.cursor()
    c.execute("""
        INSERT INTO posts
        (post_type, item_name, description, category,
         location, date, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "found",
        item_name,
        description,
        category,
        location,
        date,
        contact
    ))
    con.commit()
    con.close()
    return render_template("report_found.html")

if __name__== "__main__" :
    app.run(debug=True , port="1234")
