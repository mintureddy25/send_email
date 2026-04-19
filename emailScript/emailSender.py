import re
import redis
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT"))
PDF_DEFAULT = "./saitejareddyresume.pdf"
PDF_WITH_METAGEEKS = "./SaiTejaReddyResume.pdf"
PDF_JAVA_RESUME = "./Sai_Teja_Reddy_Resume .pdf"

# Create Redis client
client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
)


# Function to send an email
def send_email(email, subject, include_metageeks=False, use_java_resume=False):
    # Select resume based on flags (default: saitejareddyresume.pdf)
    if use_java_resume:
        pdf_file_path = PDF_JAVA_RESUME
    elif include_metageeks:
        pdf_file_path = PDF_WITH_METAGEEKS
    else:
        pdf_file_path = PDF_DEFAULT

    # Set up the email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg["Subject"] = subject

    # Email body
    body = (
        "Hi,\n\n"
        f"I came across the {subject} role on LinkedIn and had to reach out.\n"
        "Okay, deep breath. 😮‍💨\n\n"
        "Take a sip of coffee. But here's the thing 😏\n\n"
        "I built a project that scrapes LinkedIn posts and emails, and sends emails automatically. "
        "**This email was also sent using my project.** 🤖\n\n"
        "Receipts, all live, all mine:\n"
        "🏏 **TPL Mania** — Dream11 built from scratch. Fantasy cricket, live scoring, payments → https://tplmania.org\n"
        "🎮 **TicTacToe Multiplayer** — WebSocket PvP, built in a weekend → https://tictactoe.saitejareddy.online\n"
        "🤖 **Auto Email Sender** — The bot that just hit your inbox. Open source → https://github.com/mintureddy25/auto_email_sender\n"
        "🌐 **Portfolio** → https://saitejareddy.online\n\n"
        "Tech stack? Whatever you're using. I don't marry frameworks — I ship with them, then move on. ⚡\n\n"
        "**Sai Teja Reddy**\n"
        "📍 Hyderabad · ⚡ 3+ yrs · 💼 Immediate joiner"
    )

    # Plain text (strip markdown markers)
    plain = re.sub(r"\*\*(.+?)\*\*", r"\1", body)
    plain = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", plain)

    # HTML (render bold, italic, links)
    html = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", html)
    html = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', html)
    html = html.replace("\n", "<br>\n")
    html = (
        '<div style="font-family:Arial,Helvetica,sans-serif;'
        'font-size:14px;line-height:1.55;color:#222;">'
        f"{html}</div>"
    )

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(plain, "plain", "utf-8"))
    alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)

    # Attach PDF
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(pdf_file_path)}"',
            )
            msg.attach(pdf_attachment)
    else:
        print(f"Error: The file {pdf_file_path} does not exist.")

    # Send the email
    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"Email sent to {email} with subject: {subject}")


# Function to process jobs from the Redis queue
def process_jobs():
    while True:
        job = client.blpop("email_queue", timeout=0)  # Wait for a job
        if job:
            data = job[1]  # Get the job data
            email_data = json.loads(data)  # Convert JSON string to dictionary
            print(email_data)
            email = email_data["email"]
            subject = email_data["subject"]
            include_metageeks = email_data.get("includeMetageeks", False)
            use_java_resume = email_data.get("useJavaResume", False)
            send_email(email, subject, include_metageeks, use_java_resume)


if __name__ == "__main__":
    process_jobs()
