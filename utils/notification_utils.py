import os
from twilio.rest import Client
from datetime import datetime
import json

# Initialize Twilio client
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

class NotificationManager:
    def __init__(self):
        self.twilio_client = None
        if all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
            self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_sms_notification(self, to_number, message):
        """Send SMS notification using Twilio"""
        try:
            if not self.twilio_client:
                return {"success": False, "error": "Twilio credentials not configured"}

            message = self.twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=to_number
            )
            return {"success": True, "message_id": message.sid}
        except Exception as e:
            return {"success": False, "error": str(e)}

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