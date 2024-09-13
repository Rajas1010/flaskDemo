from flask import Flask, render_template, request, redirect, url_for
import bcrypt

app = Flask(__name__)

# Store hashed password globally for the sake of this example
# In a real application, you'd store this in a database
stored_hash = None

# Home page with the password form
@app.route('/')
def index():
    return render_template('index.html')

# Handling the form submission
@app.route('/submit', methods=['POST'])
def submit_password():
    global stored_hash
    password = request.form['password']  # Get password from form

    # If it's the first submission, hash the password and store it
    if stored_hash is None:
        salt = bcrypt.gensalt()
        stored_hash = bcrypt.hashpw(password.encode(), salt)
        return f'Password has been hashed and stored. Try to verify the same password.'

    # Verify the entered password against the stored hash
    if bcrypt.checkpw(password.encode(), stored_hash):
        return redirect(url_for('success'))  # Redirect to success page if correct
    else:
        return 'Incorrect password. Try again.'

# Success page after correct password submission
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
