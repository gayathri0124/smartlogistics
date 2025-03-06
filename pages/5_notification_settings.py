import streamlit as st
import os
from utils.notification_utils import (
    NotificationManager,
    save_notification_preferences,
    get_notification_preferences
)

def render_notification_settings():
    st.title("🔔 Notification Settings")

    # Create notifications directory if it doesn't exist
    os.makedirs('data/notifications', exist_ok=True)

    # Initialize notification manager
    notification_manager = NotificationManager()

    # Get current preferences (using a dummy user_id for demo)
    user_id = "demo_user"
    preferences = get_notification_preferences(user_id)

    st.info("""
    Configure your notification preferences for shipment updates.
    You can receive notifications via SMS and/or email when:
    - Shipment status changes
    - Delays are detected
    - Weather conditions affect your shipment
    """)

    # SMS Notifications
    st.subheader("📱 SMS Notifications")
    sms_enabled = st.toggle("Enable SMS Notifications", preferences["sms_enabled"])

    if sms_enabled:
        phone_number = st.text_input(
            "Phone Number",
            preferences["phone_number"],
            help="Include country code (e.g., +1 for US numbers)"
        )

        # Test SMS
        if st.button("Test SMS Notification"):
            if not phone_number:
                st.error("Please enter a phone number")
            elif not phone_number.startswith('+'):
                st.error("Please include country code (e.g., +1 for US numbers)")
            else:
                with st.spinner("Sending test SMS..."):
                    result = notification_manager.send_sms_notification(
                        phone_number,
                        "This is a test notification from your Smart Logistics Platform!"
                    )
                    if result["success"]:
                        st.success("Test SMS sent successfully!")
                    else:
                        st.error(result["error"])

    # Email Notifications (placeholder for future implementation)
    st.subheader("📧 Email Notifications")
    email_enabled = st.toggle("Enable Email Notifications", preferences["email_enabled"])

    if email_enabled:
        email = st.text_input("Email Address", preferences["email"])

    # Notification Triggers
    st.subheader("⚡ Notification Triggers")
    notify_status = st.checkbox(
        "Notify on status changes",
        preferences["notify_on_status_change"]
    )
    notify_delay = st.checkbox(
        "Notify on significant delays",
        preferences["notify_on_delay"]
    )
    notify_weather = st.checkbox(
        "Notify on adverse weather conditions",
        preferences["notify_on_weather"]
    )

    # Save preferences
    if st.button("Save Preferences"):
        new_preferences = {
            "sms_enabled": sms_enabled,
            "email_enabled": email_enabled,
            "phone_number": phone_number if sms_enabled else "",
            "email": email if email_enabled else "",
            "notify_on_status_change": notify_status,
            "notify_on_delay": notify_delay,
            "notify_on_weather": notify_weather
        }

        if save_notification_preferences(user_id, new_preferences):
            st.success("Preferences saved successfully!")
        else:
            st.error("Failed to save preferences")

if __name__ == "__main__":
    render_notification_settings()