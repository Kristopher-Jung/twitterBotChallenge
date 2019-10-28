import os
import psycopg2
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

if os.path.isfile('./secret.py'):
    from secret import consumer_key, consumer_secret, access_token, access_secret, handle
else:
    if os.environ.get("handle"):
        handle = os.environ.get("handle")
    if os.environ.get("TWBOT_ACCESS_SECRET"):
        access_secret = os.environ.get("TWBOT_ACCESS_SECRET")
    if os.environ.get("TWBOT_ACCESS_TOKEN"):
        access_token = os.environ.get("TWBOT_ACCESS_TOKEN")
    if os.environ.get("TWBOT_CON_KEY"):
        consumer_key = os.environ.get("TWBOT_CON_KEY")
    if os.environ.get("TWBOT_CON_SECRET"):
        consumer_secret = os.environ.get("TWBOT_CON_SECRET")

if os.path.isfile('./secret.py'):
    from secret import user, password, host, port, database

    conn = psycopg2.connect(user=user,
                            password=password,
                            host=host,
                            port=port,
                            database=database)
    cursor = conn.cursor()
else:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
