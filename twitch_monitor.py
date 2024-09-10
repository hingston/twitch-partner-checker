import os
import time

import requests

# Get credentials and settings from environment variables
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
alexa_notify_me_code = os.getenv("ALEXA_NOTIFY_ME_ACCESS_CODE")
streamer_name_to_monitor = os.getenv("STREAMER_USERNAME")


def get_twitch_access_token(client_id, client_secret):
    """Function to get the Twitch access token."""
    auth_url = "https://id.twitch.tv/oauth2/token"
    auth_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    response = requests.post(auth_url, params=auth_params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()["access_token"]


def check_streamer_status(streamer_name, access_token):
    """Function to check the Twitch streamer status."""
    user_info_url = "https://api.twitch.tv/helix/users"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {access_token}"}
    params = {"login": streamer_name}

    response = requests.get(user_info_url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors

    user_data = response.json()
    if user_data["data"]:
        return user_data["data"][0]["broadcaster_type"]
    return None


def send_alexa_announcement(message):
    """Function to send an announcement to Alexa using the Notify Me skill."""
    alexa_url = f"https://api.notifymyecho.com/v1/NotifyMe"
    payload = {"notification": message, "accessCode": alexa_notify_me_code}
    response = requests.post(alexa_url, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors


def send_telegram_message(message):
    """Function to send a message using Telegram Bot."""
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(telegram_url, data=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors


def monitor_streamer(streamer_name):
    """Main function to monitor the streamer status and send notifications."""
    access_token = get_twitch_access_token(client_id, client_secret)
    while True:
        try:
            broadcaster_type = check_streamer_status(streamer_name, access_token)
            if broadcaster_type == "partner":
                message = f"{streamer_name} is a Twitch Partner. https://www.twitch.tv/{streamer_name}"
                print(message)
                # send_alexa_announcement(message)
                send_telegram_message(message)
            elif broadcaster_type == "affiliate":
                message = f"{streamer_name} is a Twitch Affiliate. https://www.twitch.tv/{streamer_name}"
                print(message)
                # send_alexa_announcement(message)
                send_telegram_message(message)
            else:
                print(f"{streamer_name} is not an Affiliate or Partner.")
        except requests.HTTPError as e:
            print(f"HTTP Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        print("Waiting 10 seconds...")
        time.sleep(10)


if __name__ == "__main__":
    if not all(
        [
            client_id,
            client_secret,
            telegram_bot_token,
            telegram_chat_id,
            alexa_notify_me_code,
            streamer_name_to_monitor,
        ]
    ):
        print("Missing environment variables. Please check your Docker Compose file.")
    else:
        monitor_streamer(streamer_name_to_monitor)
