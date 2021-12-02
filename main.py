from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__, template_folder='templates')

@app.route('/')
def homepage():
    return render_template('index.html')


# con = sqlite3.connect("first.db")
# cur = con.cursor()
# cur.execute('CREATE TABLE TaskList(username VARCHAR(255), password VARCHAR(255), Task VARCHAR(255))')
# con.commit()


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect("first.db")
        #print("yes")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM TaskList WHERE " +username+ " =? AND " +password+ " =? ")
        account = data.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'task' in request.form:        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        task = request.form['task']
        con = sqlite3.connect("first.db")
        cur = con.cursor()
        cur.execute(" SELECT * FROM TaskList WHERE username =" + username + "") #" =? ")
        account = cur.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            con = sqlite3.connect("first.db")
            cur = con.cursor()
            cur.execute('INSERT INTO TaskList VALUES(?, ? ,?)')
            con.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        con = sqlite3.connect("first.db")
        # Fetch one record and return resul
        cur = con.cursor()
        cur.execute('SELECT task FROM TaskList WHERE id = %s', (session['id']))
        account = cur.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)