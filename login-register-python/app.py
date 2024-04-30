from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Data pengguna
user_data = []

# dashboard
@app.route('/')
def home():
    # Periksa apakah pengguna sudah login
    if 'username' in session:
        username = session['username']
        user = next((user for user in user_data if user['username'] == username), None)
        return render_template('home.html', username=user)
    else:
        flash('You are not logged inw', 'warning')
        return redirect(url_for('login'))

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        # Cek apakah pengguna ada di dalam array
        user = next((user for user in user_data if user['username'] == identifier or user['npm'] == identifier), None)
        if user and user['password'] == password:
            session['username'] = user['username']  # Simpan username ke session
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or passwordf', 'danger')
    return render_template('login.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        flash('You are logged inw', 'warning')
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        npm = request.form['npm']
        classes = request.form['classes']
        password = request.form['password']

        # Validasi password
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char in '!@$()-_[]{}|;:,.<>?/~`' for char in password):
            flash('The password must contain at least 8 characters, contain uppercase letters, and contain at least 1 symbol (@, -, _, $, !)f', 'danger')
        else:
            # Cek apakah username atau npm sudah terdaftar
            if any(user['username'] == username for user in user_data):
                flash('Username is already in usef', 'danger')
            elif any(user['npm'] == npm for user in user_data):
                flash('NPM is already in usef', 'danger')
            else:
                user_data.append({'username': username, 'name': name, 'npm': npm, 'classes': classes, 'password': password})
                flash('Registration successful. Please logint', 'success')
                return redirect(url_for('login'))
    return render_template('register.html')

# logout
@app.route('/logout')
def logout():
    # Membersihkan session
    session.pop('username', None)
    flash('You have logged outi', 'info')

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
