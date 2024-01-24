import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender's email credentials
sender_email = "manoj4322@gmail.com"
sender_password = "dqamznxurhgvzbcx"

# Receiver's email
receiver_email = "manoj4322@gmail.com"

# Create the MIME object
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test Email"

# Email body
body = "This is a test email sent from Python."
message.attach(MIMEText(body, "plain"))

# SMTP server settings for Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Start the SMTP session
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()

# Log in to the email account
server.login(sender_email, sender_password)

# Send the email
server.sendmail(sender_email, receiver_email, message.as_string())

# Quit the SMTP session
server.quit()

print("Email sent successfully!")
