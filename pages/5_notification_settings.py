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
    You can receive notifications via email when:
    - Shipment status changes
    - Delays are detected
    - Weather conditions affect your shipment
    """)

    # Email Notifications
    st.subheader("📧 Email Notifications")
    email_enabled = st.toggle("Enable Email Notifications", preferences["email_enabled"])

    if email_enabled:
        email = st.text_input("Email Address", preferences["email"])

        # Test Email functionality could be added here in the future
        if st.button("Test Email Notification"):
            if not email:
                st.error("Please enter an email address")
            else:
                st.success("Email notification feature is ready for implementation!")
                # Future implementation would go here

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
            "sms_enabled": False,  # Disabled SMS
            "email_enabled": email_enabled,
            "phone_number": "",  # Clear phone number
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