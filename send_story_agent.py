# agents/send_story_agent.py

import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_story_via_email(recipient_email, story_text, audio_path=None):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_ADDRESS or EMAIL_PASSWORD is not set in .env")

    msg = EmailMessage()
    msg['Subject'] = 'Your AI-Generated Story'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg.set_content("Attached is your AI-generated story. Enjoy!")

    # Attach text story
    msg.add_attachment(story_text.encode('utf-8'), maintype='text', subtype='plain', filename='story.txt')

    # Optional audio attachment
    #if audio_path:
    #    with open(audio_path, 'rb') as f:
    #        audio_data = f.read()
    #        msg.add_attachment(audio_data, maintype='audio', subtype='mpeg', filename='story.mp3')

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
