import sqlite3
import random
import schedule
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")

def get_random_tweet():
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url, content FROM tweets ORDER BY RANDOM() LIMIT 1')
    tweet = cursor.fetchone()
    conn.close()
    return tweet

def send_email(tweet):
    if tweet is None:
        print("No tweet found.")
        return

    url, content = tweet

    msg = EmailMessage()
    msg['Subject'] = '💡 Your Random Bookmarked Tweet'
    msg['From'] = 'alstongoesgym@gmail.com'
    msg['To'] = 'alstongoesgym@gmail.com'
    msg.set_content(f"{content}\n\n{url}")

    # Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)  # Use App Password
        smtp.send_message(msg)

    print("✅ Email sent:", url)

# Schedule every 5 mins (for testing)
#schedule.every(2).minutes.do(lambda: send_email(get_random_tweet()))
schedule.every().day.at("09:00").do(lambda: send_email(get_random_tweet()))

while True:
    schedule.run_pending()
    time.sleep(1)
