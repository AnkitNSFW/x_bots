from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import smtplib, os
from dotenv import load_dotenv
load_dotenv()

DEVELOPER_EMAIL=os.getenv("DEVELOPER_EMAIL")
EMAIL_SENDER=os.getenv("EMAIL_SENDER")
EMAIL_SENDER_APP_PASSWORD=os.getenv("EMAIL_SENDER_APP_PASSWORD")

agent = smtplib.SMTP_SSL("smtp.gmail.com", 465)
agent.login(EMAIL_SENDER,EMAIL_SENDER_APP_PASSWORD)

def Notify_Developer(subject, content, to_addr, mail_type = 'plain' ):
    global agent, EMAIL_SENDER, DEVELOPER_EMAIL

    em = MIMEMultipart()
    em["From"] = f"X_Bot <{EMAIL_SENDER}>"
    em["To"] = to_addr
    em["Subject"] = subject
    em.attach(MIMEText(content, mail_type))
    agent.sendmail(EMAIL_SENDER, to_addr, em.as_string())

if __name__ == "__main__":
    Notify_Developer(subject="Test Mail", content="This is a test mail", to_addr=DEVELOPER_EMAIL)
    agent.quit()