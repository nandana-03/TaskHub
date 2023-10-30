from flask import Flask, render_template,request,flash,redirect,url_for,session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("login.db")
#con.execute("create table user(username text PRIMARY KEY,email text,password text,confirm_password text)")
con.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=sqlite3.connect("login.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where username=? and password=?",(username,password))
        data=cur.fetchone()

        if data:
            session["username"]=data["username"]
            session["password"]=data["password"]
           # return redirect("user")
            return redirect(url_for('home'))
        else:
            flash("Username and Password Mismatch","danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        print(username)
        try:
            con=sqlite3.connect("login.db")
            cur=con.cursor()
            cur.execute("insert into user(username,email,password,confirm_password)values(?,?,?,?)",(username,email,password,confirm_password))
            con.commit()
            flash("Account created successfully!!","success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists,please try another one!!","danger")
            return redirect(url_for("register"))
        finally:
            con.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

con=sqlite3.connect("login.db")
#con.execute("create table tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,task TEXT NOT NULL,username TEXT FORIEGN KEY)")
con.close()

#@app.route('/home')
#def home():
#    now = datetime.now()
#    end_of_day = datetime.now().replace(hour=23, minute=59, second=59)
#    remaining_hours = int((end_of_day - now).total_seconds() // 3600)
#    remaining_minutes = int(((end_of_day - now).total_seconds() % 3600 ) // 60)
#    return render_template('projecthomepage.html', remaining_hours=remaining_hours, remaining_minutes=remaining_minutes)

@app.route('/home')
def home():
    if 'username' in session:
                return render_template('projecthomepage.html', username=session['username'])
    return render_template('projecthomepage.html')
    

@app.route('/task')
def task():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    #cur.execute('SELECT * FROM tasks')
    cur.execute("SELECT task from tasks where username='aman'")
    tasks = cur.fetchall()
    con.close()

    return render_template('settingone.html',tasks=tasks)
    

@app.route('/add', methods=['GET','POST'])
def add_task():
    if request.method=='POST':
        task = request.form['title']
        con = sqlite3.connect('login.db')
        cur = con.cursor()
        print(task)
        if 'username' in session:
            username=session['username']
            print(username)
        cur.execute("INSERT INTO tasks (task, username) VALUES (?,?)",(task,username))
        con.commit()
        con.close()
        return redirect(url_for('add_task'))
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    #cur.execute('SELECT * FROM tasks')
    cur.execute("SELECT task from tasks where username='aman'")
    tasks = cur.fetchall()
    con.close()
    return render_template('settingone.html',tasks=tasks)

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        task = request.form['task']
        con = sqlite3.connect('login.db')
        cur = con.cursor()
        cur.execute('UPDATE tasks SET task = ? WHERE id = ?', (task, task_id))
        con.commit()
        con.close()
        return redirect(url_for('edit_task'))

    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks WHERE id = ?', (task_id))
    task = cur.fetchone()
    con.close()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<task_id>')
def delete_task(task_id):
    con = sqlite3.connect('login.db')
    cur= con.cursor()
    cur.execute('DELETE FROM tasks WHERE id = ?', (task_id))
    con.commit()
    con.close()

    return redirect(url_for('index'))

@app.route('/notes')
def notes():
    return render_template('notes.html')

if __name__ == '__main__':
    app.run(debug=True)