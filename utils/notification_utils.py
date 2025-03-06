import os
from twilio.rest import Client
from datetime import datetime
import json
from twilio.base.exceptions import TwilioRestException

# Initialize Twilio client
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add these environment variables
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_SMTP_SERVER = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.environ.get("EMAIL_SMTP_PORT", "587"))

class NotificationManager:
    def __init__(self):
        self.twilio_client = None
        if all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
            self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        self.email_configured = all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SMTP_SERVER])

    def send_email_notification(self, to_email, subject, message):
        """Send email notification"""
        try:
            if not self.email_configured:
                return {"success": False, "error": "Email credentials not configured"}
            
            # Create the email
            email_message = MIMEMultipart()
            email_message['From'] = EMAIL_SENDER
            email_message['To'] = to_email
            email_message['Subject'] = subject
            
            # Add message body
            email_message.attach(MIMEText(message, 'plain'))
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
                server.starttls()  # Secure the connection
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(email_message)
            
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to send email: {str(e)}"}

    def send_sms_notification(self, to_number, message):
        """Send SMS notification using Twilio with improved error handling"""
        try:
            if not self.twilio_client:
                return {"success": False, "error": "Twilio credentials not configured"}

            # Validate phone number format
            if not to_number.startswith('+'):
                to_number = '+' + to_number

            message = self.twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=to_number
            )
            return {"success": True, "message_id": message.sid}

        except TwilioRestException as e:
            if e.code == 21408:  # Region permission error
                return {
                    "success": False,
                    "error": f"SMS sending is not enabled for this region. Please verify the phone number {to_number} is in a supported region."
                }
            elif e.code == 21211:  # Invalid phone number
                return {
                    "success": False,
                    "error": "Invalid phone number format. Please include country code (e.g., +1 for US numbers)."
                }
            else:
                return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Failed to send SMS: {str(e)}"}

    def format_status_update(self, shipment_data, status_analysis):
        """Format shipment status update message"""
        recommendations = "\n".join(f"• {rec}" for rec in status_analysis['recommendations'])
        return f"""
🚚 Shipment Update: {shipment_data['shipment_id']}
Status: {status_analysis['updated_status']}
Risk Level: {status_analysis['risk_level']}
ETA Confidence: {status_analysis['eta_confidence']*100:.0f}%

Origin: {shipment_data['origin']}
Destination: {shipment_data['destination']}
Weather: {shipment_data['weather_condition']}

Recommendations:
{recommendations}
        """.strip()

def save_notification_preferences(user_id, preferences):
    """Save user notification preferences"""
    try:
        os.makedirs('data/notifications', exist_ok=True)
        with open(f'data/notifications/{user_id}.json', 'w') as f:
            json.dump(preferences, f)
        return True
    except Exception:
        return False

def get_notification_preferences(user_id):
    """Get user notification preferences"""
    try:
        with open(f'data/notifications/{user_id}.json', 'r') as f:
            return json.load(f)
    except Exception:
        return {
            "sms_enabled": False,
            "email_enabled": False,
            "phone_number": "",
            "email": "",
            "notify_on_status_change": True,
            "notify_on_delay": True,
            "notify_on_weather": True
        }