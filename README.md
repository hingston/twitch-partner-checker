# Twitch Affiliate/Partner Checker

A Dockerized Python script that monitors a Twitch streamer to check if they are a Partner or Affiliate. If the streamer is a Partner or Affiliate, the script sends notifications to your Amazon Alexa device and a Telegram chat.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Configure Environment Variables](#2-configure-environment-variables)
  - [3. Build and Run the Docker Container](#3-build-and-run-the-docker-container)
- [Files](#files)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, make sure you have the following:

- Docker and Docker Compose installed on your machine.
- A Twitch account and [Twitch Developer Application](https://dev.twitch.tv/) credentials (`Client ID` and `Client Secret`).
- A Telegram bot created using [BotFather](https://core.telegram.org/bots#botfather) and the bot token.
- Your Telegram `Chat ID` where the notifications will be sent.
- Alexa "Notify Me" skill enabled and an access code obtained from the [Notify Me Skill website](https://notify-me.6apps.com/).

## Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/twitch-streamer-monitor.git
cd twitch-streamer-monitor
```

### 2. Configure Environment Variables

Open the `docker-compose.yml` file and replace the placeholder values with your actual credentials:

```yaml
version: '3.8'

services:
  twitch-monitor:
    build: .
    container_name: twitch_monitor
    restart: always
    environment:
      - TWITCH_CLIENT_ID=YOUR_CLIENT_ID
      - TWITCH_CLIENT_SECRET=YOUR_CLIENT_SECRET
      - TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
      - TELEGRAM_CHAT_ID=YOUR_CHAT_ID
      - ALEXA_NOTIFY_ME_ACCESS_CODE=YOUR_ALEXA_NOTIFY_ME_ACCESS_CODE
      - STREAMER_USERNAME=STREAMER_USERNAME_TO_MONITOR
```

- **TWITCH_CLIENT_ID**: Your Twitch Developer Application Client ID.
- **TWITCH_CLIENT_SECRET**: Your Twitch Developer Application Client Secret.
- **TELEGRAM_BOT_TOKEN**: The token for your Telegram bot.
- **TELEGRAM_CHAT_ID**: The ID of the Telegram chat where notifications will be sent.
- **ALEXA_NOTIFY_ME_ACCESS_CODE**: The access code for the Alexa "Notify Me" skill.
- **STREAMER_USERNAME**: The Twitch username of the streamer to monitor.

### 3. Build and Run the Docker Container

To build the Docker image and run the container, use the following commands:

```bash
docker-compose build
docker-compose up
```

The script will now run inside the Docker container, continuously checking the Twitch streamer's status every 10 seconds. If the streamer is a Partner or Affiliate, it will send notifications to both your Alexa device and Telegram chat.

## Files

- **twitch_monitor.py**: The main Python script that monitors the Twitch streamer.
- **Dockerfile**: Defines the Docker image with an Alpine-based Python environment.
- **requirements.txt**: Lists the Python dependencies required by the script.
- **docker-compose.yml**: Docker Compose file that sets up and runs the service.

## How It Works

1. The script uses the Twitch API to check the broadcaster type of the specified streamer.
2. If the streamer is a Partner or Affiliate, it sends an announcement to your Alexa device using the "Notify Me" skill.
3. It also sends a message to your specified Telegram chat using the Telegram Bot API.
4. The script repeats this check every 10 seconds.

## Troubleshooting

- **Missing Environment Variables**: Ensure all required environment variables are set in the `docker-compose.yml` file.
- **Network Issues**: If the script fails to send notifications, check your network connection and the status of the external APIs (Twitch, Telegram, Alexa).
- **Docker Issues**: If Docker is not installed or configured correctly, follow the [Docker installation guide](https://docs.docker.com/get-docker/).

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
