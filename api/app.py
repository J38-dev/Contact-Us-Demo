from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Rate limiting: 5 submissions per hour per IP
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per hour"]
)

@app.route('/api/submit', methods=['POST'])
@limiter.limit("5 per hour")
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    # Basic validation
    if not all([name, email, message]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400
    
    # Send email
    try:
        msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        msg['Subject'] = 'Contact Form Submission'
        msg['From'] = os.environ.get('SMTP_FROM', 'noreply@example.com')
        msg['To'] = os.environ.get('SMTP_TO', 'your-email@example.com')
        
        server = smtplib.SMTP(os.environ.get('SMTP_SERVER', 'smtp.gmail.com'), 587)
        server.starttls()
        server.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
        return jsonify({'success': 'Message sent successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to send message'}), 500

# For Vercel serverless deployment
def handler(event, context):
    # Placeholder for Vercel handler; may need adjustment based on Vercel docs
    return app