import streamlit as st
from utils.notification_utils import NotificationManager

def render_notification_settings():
    st.title("⚙️ Notification Settings")

    # Initialize notification manager
    notification_manager = NotificationManager()

    # Get current user preferences
    preferences = notification_manager.get_user_preferences()

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
            "notify_on_status_change": notify_on_status_change,
            "notify_on_delay": notify_on_delay,
            "notify_on_weather": notify_on_weather
        }

        result = notification_manager.save_user_preferences(updated_preferences)

        if result.get("success"):
            st.success("Notification preferences saved successfully!")
        else:
            st.error(f"Failed to save preferences: {result.get('error')}")

    st.info("""
    **Note:** These settings control what types of notifications would be generated. 
    The actual notification delivery has been disabled in this version of the application.
    """)

if __name__ == "__main__":
    render_notification_settings()