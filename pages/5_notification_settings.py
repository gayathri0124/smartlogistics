
import streamlit as st
from utils.notification_utils import NotificationManager

def render_notification_settings():
    st.title("⚙️ Notification Settings")
    
    # Initialize notification manager
    notification_manager = NotificationManager()
    
    # Get current user preferences
    preferences = notification_manager.get_user_preferences()
    
    st.subheader("Notification Methods")
    
    # Email notification settings
    st.write("### Email Notifications")
    email_enabled = st.checkbox("Enable email notifications", value=preferences.get("email_enabled", False))
    email = st.text_input("Email address", value=preferences.get("email", ""))
    
    # SMS notification settings
    st.write("### SMS Notifications")
    sms_enabled = st.checkbox("Enable SMS notifications", value=preferences.get("sms_enabled", False))
    phone_number = st.text_input("Phone number", value=preferences.get("phone_number", ""))
    
    st.subheader("Notification Preferences")
    
    # Notification triggers
    notify_on_status_change = st.checkbox("Notify on shipment status change", 
                                          value=preferences.get("notify_on_status_change", True))
    notify_on_delay = st.checkbox("Notify on predicted delays", 
                                  value=preferences.get("notify_on_delay", True))
    notify_on_weather = st.checkbox("Notify on severe weather affecting routes", 
                                   value=preferences.get("notify_on_weather", False))
    
    # Save button
    if st.button("Save Preferences"):
        updated_preferences = {
            "email_enabled": email_enabled,
            "sms_enabled": sms_enabled,
            "email": email,
            "phone_number": phone_number,
            "notify_on_status_change": notify_on_status_change,
            "notify_on_delay": notify_on_delay,
            "notify_on_weather": notify_on_weather
        }
        
        result = notification_manager.save_user_preferences(updated_preferences)
        
        if result.get("success"):
            st.success("Notification preferences saved successfully!")
        else:
            st.error(f"Failed to save preferences: {result.get('error')}")
    
    # Test notification section
    st.subheader("Test Notifications")
    test_message = st.text_input("Test message", value="This is a test notification")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test Email"):
            if email_enabled and email:
                result = notification_manager.send_email_notification(
                    email, 
                    "Logistics Platform - Test Notification",
                    test_message
                )
                if result.get("success"):
                    st.success("Test email sent successfully!")
                else:
                    st.error(f"Failed to send test email: {result.get('error')}")
            else:
                st.warning("Email notifications are not enabled or email address is missing")
    
    with col2:
        if st.button("Test SMS"):
            if sms_enabled and phone_number:
                result = notification_manager.send_sms_notification(
                    phone_number,
                    test_message
                )
                if result.get("success"):
                    if result.get("mock"):
                        st.info("SMS notification would be sent (mock implementation)")
                    else:
                        st.success("Test SMS sent successfully!")
                else:
                    st.error(f"Failed to send test SMS: {result.get('error')}")
            else:
                st.warning("SMS notifications are not enabled or phone number is missing")
    
    # Email configuration note
    st.info("""
    **Note:** Email notifications require email credentials to be configured as environment variables:
    - EMAIL_SENDER
    - EMAIL_PASSWORD
    - EMAIL_SMTP_SERVER (default: smtp.gmail.com)
    - EMAIL_SMTP_PORT (default: 587)
    
    Please set these in the Secrets tool of your Replit workspace.
    """)

if __name__ == "__main__":
    render_notification_settings()
