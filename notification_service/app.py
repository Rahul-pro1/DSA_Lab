# app.py
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import threading
import time

app = Flask(__name__)

# Configuration (You might want to move these to environment variables)
SMTP_SERVER = 'smtp.gmail.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Or your SMTP port
SMTP_USERNAME = ''  # Replace with your email
SMTP_PASSWORD = ''  # Replace with your password
SENDER_EMAIL = ''  # Replace with your email

reminders = []

def send_email(recipient_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def check_reminders():
    while True:
        now = datetime.now()
        upcoming_reminders = [r for r in reminders if r['datetime'] <= now and not r['sent']]
        for reminder in upcoming_reminders:
            send_email(reminder['email'], reminder['subject'], reminder['message'])
            reminder['sent'] = True
            print(f"Reminder sent to {reminder['email']} for: {reminder['subject']}")
        time.sleep(60)  # Check every minute

reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    student_name = request.form.get('student_name')
    student_email = request.form.get('student_email')
    email_subject = request.form.get('email_subject')
    email_body = request.form.get('email_body')
    reminder_datetime_str = request.form.get('reminder_datetime')
    reminder_subject = request.form.get('reminder_subject')
    reminder_message = request.form.get('reminder_message')

    email_sent = False
    if student_email and email_subject and email_body:
        email_sent = send_email(student_email, email_subject, email_body)

    if reminder_datetime_str and reminder_subject and reminder_message and student_email:
        try:
            reminder_datetime = datetime.strptime(reminder_datetime_str, '%Y-%m-%dT%H:%M')
            if reminder_datetime > datetime.now():
                reminders.append({
                    'email': student_email,
                    'datetime': reminder_datetime,
                    'subject': reminder_subject,
                    'message': reminder_message,
                    'sent': False
                })
                print(f"Reminder set for {student_email} at {reminder_datetime} for: {reminder_subject}")
        except ValueError:
            print("Invalid reminder datetime format.")

    return render_template('index.html', email_sent=email_sent)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')