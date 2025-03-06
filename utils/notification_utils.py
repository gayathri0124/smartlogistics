import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class NotificationManager:
    def __init__(self):
        self.email_sender = os.environ.get("EMAIL_SENDER")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        self.smtp_server = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "587"))

        # Create notifications directory if it doesn't exist
        Path("data/notifications").mkdir(parents=True, exist_ok=True)

    def send_email_notification(self, recipient, subject, message):
        """
        Send email notification to recipient

        Args:
            recipient (str): Email recipient
            subject (str): Email subject
            message (str): Email body

        Returns:
            dict: Result of email sending operation with success status and error if any
        """
        # Debug information
        logging.info(f"Attempting to send email to {recipient}")
        logging.info(f"Using SMTP server: {self.smtp_server}:{self.smtp_port}")
        logging.info(f"Email sender configured: {'Yes' if self.email_sender else 'No'}")
        logging.info(f"Email password configured: {'Yes' if self.email_password else 'No'}")
        
        if not self.email_sender or not self.email_password:
            logging.error("Email credentials not configured")
            return {"success": False, "error": "Email credentials not configured"}

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = recipient
            msg['Subject'] = subject

            # Attach message body
            msg.attach(MIMEText(message, 'plain'))

            # Connect to server and send
            logging.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            logging.info(f"Logging in as {self.email_sender}")
            server.login(self.email_sender, self.email_password)
            logging.info(f"Sending email to {recipient}")
            server.send_message(msg)
            server.quit()
            logging.info("Email sent successfully")

            return {"success": True}
        except Exception as e:
            logging.error(f"Email sending failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def send_sms_notification(self, phone_number, message):
        """
        Placeholder for SMS notification functionality
        In a real application, you would integrate with an SMS service like Twilio
        """
        # This is a mock implementation
        logging.info(f"SMS would be sent to {phone_number}: {message}")
        return {"success": True, "mock": True}
    
    def get_user_preferences(self, user_id="demo_user"):
        """
        Get notification preferences for a user from stored JSON file
        Returns default preferences if user preferences not found
        """
        try:
            file_path = f"data/notifications/{user_id}.json"
            if Path(file_path).exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                # Default preferences
                return {
                    "email_enabled": False,
                    "sms_enabled": False,
                    "email": "",
                    "phone_number": "",
                    "notify_on_status_change": True,
                    "notify_on_delay": True,
                    "notify_on_weather": False
                }
        except Exception as e:
            logging.error(f"Error loading user preferences: {str(e)}")
            return {
                "email_enabled": False,
                "sms_enabled": False,
                "email": "",
                "phone_number": "",
                "notify_on_status_change": True,
                "notify_on_delay": True,
                "notify_on_weather": False
            }
    
    def save_user_preferences(self, preferences, user_id="demo_user"):
        """
        Save notification preferences for a user to a JSON file
        """
        try:
            file_path = f"data/notifications/{user_id}.json"
            with open(file_path, 'w') as f:
                json.dump(preferences, f)
            return {"success": True}
        except Exception as e:
            logging.error(f"Error saving user preferences: {str(e)}")
            return {"success": False, "error": str(e)}