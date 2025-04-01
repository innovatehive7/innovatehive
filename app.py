from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)

def get_google_sheet():
    try:
        print("Attempting to authorize with Google...")
        creds_json = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
        
        # Verify required fields
        required_keys = ['type', 'project_id', 'private_key', 'client_email']
        if not all(k in creds_json for k in required_keys):
            raise ValueError("Missing required credential fields")
            
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)
        
        sheet_name = os.getenv('GOOGLE_SHEET_NAME')
        print(f"Looking for sheet: {sheet_name}")
        
        try:
            sheet = client.open(sheet_name).sheet1
            print("Successfully accessed sheet!")
            return sheet
        except gspread.SpreadsheetNotFound:
            print(f"Sheet '{sheet_name}' not found! Creating new...")
            sheet = client.create(sheet_name)
            # Add headers
            sheet.sheet1.append_row([
                'Timestamp', 'Name', 'Email', 'Phone', 
                'Service', 'Goal', 'Budget', 'Message', 
                'IP Address', 'User Agent'
            ])
            sheet.share(creds_json['client_email'], perm_type='user', role='writer')
            return sheet.sheet1
            
    except Exception as e:
        print(f"Google Sheets Error: {str(e)}")
        return None

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# Contact form API
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'status': 'error',
                'message': 'Name, email, and message are required'
            }), 400

        # Prepare data
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        service = data.get('service', '').strip()
        goal = data.get('goal', '').strip()
        budget = data.get('budget', '').strip()
        message = data.get('message', '').strip()

        # Save to Google Sheets
        sheet = get_google_sheet()
        if not sheet:
            raise Exception("Could not access Google Sheets")
            
        sheet.append_row([
            timestamp,
            name,
            email,
            phone,
            service,
            goal,
            budget,
            message,
            request.remote_addr,
            request.headers.get('User-Agent', 'Unknown')
        ])
        print("Data successfully written to Google Sheets")

        # Send email
        try:
            msg = Message(
                "New Contact Form Submission - InnovateHive",
                recipients=[os.getenv('EMAIL_RECEIVER')]
            )
            msg.body = f"""
            New contact form submission:

            Name: {name}
            Email: {email}
            Phone: {phone}
            Service: {service}
            Project Goals: {goal}
            Budget: {budget}
            Message: {message}

            Timestamp: {timestamp}
            IP Address: {request.remote_addr}
            """
            mail.send(msg)
            print("Email notification sent")
        except Exception as e:
            print(f"Email sending failed: {e}")

        return jsonify({
            'status': 'success',
            'message': 'Your message has been sent successfully!'
        })

    except Exception as e:
        print(f"Error processing contact form: {e}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred. Please try again later.'
        }), 500

# Subpages (Services)
@app.route('/website')
def website():
    return render_template('website.html')

@app.route('/graphic')
def graphic():
    return render_template('graphic.html')

@app.route('/video_editing')
def video_editing():
    return render_template('video_editing.html')

@app.route('/content')
def content():
    return render_template('content.html')

@app.route('/seo')
def seo():
    return render_template('seo.html')

@app.route('/business_analysis')
def business_analysis():
    return render_template('business_analysis.html')

@app.route('/app')
def app_design():
    return render_template('app.html')

@app.route('/cloud')
def cloud():
    return render_template('cloud.html')

@app.route('/ai_assistant_development')
def ai_assistant():
    return render_template('ai_assistant_development.html')

# All Blogs Page
@app.route('/all_blogs')
def all_blogs():
    return render_template('all_blogs.html')

# Individual Blog Pages
@app.route('/anurag')
def anurag():
    return render_template('anurag.html')

@app.route('/dhanashri')
def dhanashri():
    return render_template('dhanashri.html')

@app.route('/gurbani')
def gurbani():
    return render_template('gurbani.html')

@app.route('/om_gws')
def om_gws():
    return render_template('om_gws.html')

@app.route('/om_shau')
def om_shau():
    return render_template('om_shau.html')

@app.route('/ajinka')
def ajinka():
    return render_template('ajinka.html')

@app.route('/sharv')
def sharv():
    return render_template('sharv.html')

@app.route('/siddhi')
def siddhi():
    return render_template('siddhi.html')

@app.route('/nupur')
def nuper():
    return render_template('nuper.html')

@app.route('/sahil')
def sahil():
    return render_template('sahil.html')

@app.route('/om')
def om():
    return render_template('om.html')

@app.route('/anuja')
def anuja():
    return render_template('anuja.html')

if __name__ == '__main__':
    app.run(debug=True)