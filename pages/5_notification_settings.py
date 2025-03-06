import streamlit as st
from utils.notification_utils import NotificationManager

def render_notification_settings():
    st.title("⚙️ Notification Settings")

    st.info("The notification feature has been removed from this application.")

if __name__ == "__main__":
    render_notification_settings()