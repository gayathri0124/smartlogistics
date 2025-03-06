import os
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class NotificationManager:
    def __init__(self):
        # Create notifications directory if it doesn't exist
        Path("data/notifications").mkdir(parents=True, exist_ok=True)

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
                    "notify_on_status_change": True,
                    "notify_on_delay": True,
                    "notify_on_weather": False
                }
        except Exception as e:
            logging.error(f"Error loading user preferences: {str(e)}")
            return {
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