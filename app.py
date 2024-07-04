from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

PASSWORD_FILE = "data.txt"

def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    return []

def save_passwords(passwords):
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_password():
    if request.method == 'POST':
        website = request.form['website']
        email = request.form['email']
        password = request.form['password']
        
        if website and email and password:
            passwords = load_passwords()
            passwords.append({'website': website, 'email': email, 'password': password})
            save_passwords(passwords)
            flash('Password saved successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please fill out all fields.', 'error')
    
    return render_template('add_password.html')

@app.route('/passwords')
def display_passwords():
    passwords = load_passwords()
    return render_template('display_passwords.html', passwords=passwords)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_password(index):
    passwords = load_passwords()
    if 0 <= index < len(passwords):
        passwords.pop(index)
        save_passwords(passwords)
        flash('Password deleted successfully!', 'success')
    else:
        flash('Invalid password index.', 'error')
    return redirect(url_for('display_passwords'))

if __name__ == '__main__':
    app.run(debug=True)
