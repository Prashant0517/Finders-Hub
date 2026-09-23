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
    em = request.form["mail"]
    ps = request.form["pass"]
    con = sqlite3.connect("mywebsite.db")
    con.row_factory = sqlite3.Row
    c = con.cursor()
    c.execute(
        "SELECT * FROM student WHERE mail=? AND pass=?",
        (em, ps)
    )
    data = c.fetchone()
    con.close()
    # flash("Invalid Login Data", "success")
    if data:
        session["user"] = data["mail"]
        session["role"] = data["role"]
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid credentials! Please check your email and password.", "danger")
        return redirect(url_for("login"))
    # if request.method == "POST":
    #     em=request.form["mail"]
    #     ps=request.form["pass"]
    #     con = sqlite3.connect("mywebsite.db")
    #     c = con.cursor()
    #     c.execute("select * from student where mail=? and pass=?", (em,ps))
    #     data = c.fetchall()
    #     if len(data)==1:
    #         session["user"] = em
    #         # session["role"] = data['role']
    #         return redirect(url_for("dashboard"))
    #     else:
    #         return redirect(url_for("login"))

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

# @app.route('/browse_item')
# def browse_item():
#     return render_template("browse_item.html")

@app.route('/report_lost')
def report_lost():
    return render_template("report_lost.html")

@app.route("/lostrepost", methods=["POST"])
def lost_post():
    user_id = session.get("user")
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
        (user_id,post_type, item_name, description, category,
         location, date, contact)
        VALUES (? ,?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
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
    flash("Lost report submitted successfully!", "success")
    return redirect(url_for("browse_item"))

@app.route("/report_found")
def report_found():
    return render_template("report_found.html")

@app.route("/foundrepost", methods=["POST"])
def found_post():
    user_id = session.get("user")
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
        (user_id,post_type, item_name, description, category,
         location, date, contact)
        VALUES (?,?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
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
    flash("Found report submitted successfully!", "success")
    return redirect(url_for("browse_item"))

@app.route('/browse_item')
def browse_item():
    conn = sqlite3.connect('mywebsite.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT *
            FROM posts
            ORDER BY id DESC
        """)
    records = cursor.fetchall()
    conn.close()
    return render_template("browse_item.html", records=records,is_admin=(session.get("role") == "admin"))
    # conn = sqlite3.connect('mywebsite.db')
    # conn.row_factory = sqlite3.Row
    # cursor = conn.cursor()
    #
    # cursor.execute("""
    #     SELECT *
    #     FROM posts
    #     ORDER BY id DESC
    # """)
    #
    # records = cursor.fetchall()
    # conn.close()
    # return render_template("browse_item.html",records=records)

@app.route('/update_status/<int:post_id>', methods=['POST'])
def update_status(post_id):
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    # Only admin can update status
    if session.get('role') != 'admin':
        return "Access Denied", 403
    # Get new status from form
    new_status = request.form['status']
     # Allowed status values
    allowed_statuses = ['Pending', 'Resolved', 'Claimed']
    if new_status not in allowed_statuses:
        return "Invalid status", 400
    # Update database
    conn = sqlite3.connect('mywebsite.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE posts
        SET status = ?
        WHERE id = ?
    """, (new_status, post_id))
    conn.commit()
    conn.close()

    # Go back to Browse page
    return redirect(url_for('browse_item'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))

    # Only admin can delete
    if session.get('role') != 'admin':
        return "Access Denied", 403

    # Delete the record
    conn = sqlite3.connect('mywebsite.db')
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
    """, (post_id,))

    conn.commit()
    conn.close()

    # Go back to Browse page
    return redirect(url_for('browse_item'))

if __name__== "__main__" :
    app.run(debug=True , port="1234")
