#!/bin/sh

# Run the bot
python manage.py run_discord_bot &


# Run the web server
gunicorn -b 0.0.0.0:9999 bot_platform.wsgi &

wait