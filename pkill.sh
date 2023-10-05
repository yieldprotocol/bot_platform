#!/bin/sh

# Kill the bot
pkill -f run_discord_bot

# Kill the web server
pkill -f gunicorn