import redis
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
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
PDF_FILE_PATH = "./SaiTejaReddyResume.pdf"

# Create Redis client
client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
)


# Function to send an email
def send_email(email, subject):
    # Set up the email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg["Subject"] = subject

    # Email body
    body = (
        "Hi,\n\n"
        f"I found the {subject} role on LinkedIn and had to reach out.\n"
        "I'm not someone who just writes code — for me, coding is a lifestyle. It's how I think, solve, and live.\n"
        "Quick example: I needed to send recurring messages. Most copy-paste. I built a cron job. That mindset — "
        "finding smart, scalable solutions — is what I bring to every team.\n"
        "Here’s some of what I’ve built recently:\n"
        "🔧 Email Sender Tool (Node.js, Redis, React)\n"
        "✈️ Flight Booking App → https://flights.saiteja.online\n"
        "🏏 Cricket Tournament Platform → https://beta.testingproject.space (Login: saiteja@gmail.com / 123456789)\n\n"
        "Even this email was sent using my own tool that automates sending personalized emails to recruiters.\n"
        "I thrive on solving real problems and love working across stacks. I learn fast — give me 15–20 days and I’m productive in any tech.\n"
        "Portfolio → https://saiteja.online\n\n"
        "If this sounds interesting, I’d love to show you what I’ve built. Let’s connect?\n\n"
        "Best,\n"
        "Sai Teja Reddy\n"
        "P.S. I have attached my resume for your reference."
    )

    msg.attach(MIMEText(body, "plain"))

    # Attach PDF
    if os.path.exists(PDF_FILE_PATH):
        with open(PDF_FILE_PATH, "rb") as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(PDF_FILE_PATH)}"',
            )
            msg.attach(pdf_attachment)
    else:
        print(f"Error: The file {PDF_FILE_PATH} does not exist.")

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
            email_data = eval(data)  # Convert string to dictionary
            print(email_data)
            email = email_data["email"]
            subject = email_data["subject"]
            send_email(email, subject)


if __name__ == "__main__":
    process_jobs()
