import json
import smtplib
from email.mime.text import MIMEText
import os

def handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    if event.get('path') == '/api/submit' and event.get('httpMethod') == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            name = body.get('name')
            email = body.get('email')
            message = body.get('message')
            
            # Basic validation
            if not all([name, email, message]):
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS'
                    },
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            
            if '@' not in email:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS'
                    },
                    'body': json.dumps({'error': 'Invalid email format'})
                }
            
            # Send email
            msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
            msg['Subject'] = 'Contact Form Submission'
            msg['From'] = os.environ.get('SMTP_FROM', 'noreply@example.com')
            msg['To'] = os.environ.get('SMTP_TO', 'your-email@example.com')
            
            server = smtplib.SMTP(os.environ.get('SMTP_SERVER', 'smtp.gmail.com'), 587)
            server.starttls()
            server.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'success': 'Message sent successfully'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'error': 'Failed to send message'})
            }
    
    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps({'error': 'Not found'})
    }