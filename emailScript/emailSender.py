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
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT'))
PDF_FILE_PATH = './SaiTejaReddyResume.pdf'

# Create Redis client
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Function to send an email
def send_email(email, subject):
    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject

    # Email body
    body = (
        "Hi,\n\n"
        "I found the {} role on LinkedIn and am very interested. My 2 years of experience in "
        "[React, Next.js, Node.js, Python, Lambda, Tailwind CSS, Java, PHP Slim, SQL, Elasticsearch, Redis, Beanstalkd] "
        "closely match the position's requirements, and I believe I can make a strong impact. I've attached my resume "
        "and would love to discuss how I can contribute to your team.\n\n"
        "Portfolio: https://saitejareddy-portfolio-cyan.vercel.app\n\n"
        "Thank you for your time!\n\n"
        "Best regards,\n"
        "Sai Teja Reddy"
    ).format(subject)

    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF
    if os.path.exists(PDF_FILE_PATH):
        with open(PDF_FILE_PATH, 'rb') as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(PDF_FILE_PATH)}"')
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
        job = client.blpop('email_queue', timeout=0)  # Wait for a job
        if job:
            data = job[1]  # Get the job data
            email_data = eval(data)  # Convert string to dictionary
            email = email_data['email']
            subject = email_data['subject']
            send_email(email, subject)

if __name__ == "__main__":
    process_jobs()
