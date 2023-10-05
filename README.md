# Bot Platform

## Local Setup

### Preqrequisites
- Install Docker and run `docker compose -f ./docker-compose.yml up -d` to start the Weaviate Vector DB.
- Create Python virtual env `python -m venv ./.venv` and activate it `source ./.venv/bin/activate`
- Install Python dependencies `pip install -r requirements-app.txt`
- Create a separate Discord server and bot app for local development - https://discord.com/developers
- Copy env file `cp .env.example .env` and fill in the relevant values for OpenAI and Discord.

### Upload knowledge base data to Weaviate Vector DB
#### For C4
- Open IPython notebook in repo path - `notebooks/c4/c4_kb.ipynb`
- Run relevant cells to scrape and download docs, generate embedding and upload to Weaviate.

### Run Discord bot
- Discord bot has been built using [discord.py](https://discordpy.readthedocs.io/en/stable/) library and is managed by [Django](https://www.djangoproject.com/) web frameowrk
- Run command `python manage.py run_discord_bot`

## Deployment

The platform has been deployed on Google Cloud in a private VPC. The following instances are running there:
- Weaviate Vector DB on Compute Engine
- Discord bot on Cloud Run

Ask team members for more info on the setup.

## Limitations
- Ensure only 1 bot instance is running at any time locally or in production as currently the platform does not enforce checks to prevent the same message from being processed by multiple bot instances hence duplicate chat responses will be sent to the channel. 
This is a common distributed systems problem and one solution for this is to use a Postgres DB to store user messages with a unique constraint on the ID and have the bot to first try to store the message in the DB before processing it.

## Future work
- Setup Postgres DB.
- Use Django ORM to create relevant models to store user messages, bot responses, feedback, etc.
- Handle the limitations as stated above.