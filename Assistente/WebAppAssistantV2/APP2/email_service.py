import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
# instal email-validator
# pip install email-validator | pip3 install email-validator | conda install email-validator

def send_email(from_addr, to_addr, subject, body, smtp_server, smtp_port, password):
    try:
        # Validate email addresses
        validate_email(to_addr)
        validate_email(from_addr)
    except EmailNotValidError as e:
        return str(e)

    # Create the email message
    msg = EmailMessage()
    msg.add_alternative(body, subtype='html')  # Add HTML content
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    try:
        # Connect to the SMTP server and start TLS encryption
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()                                           # Can be omitted
            server.starttls()                                       # Secure the connection
            server.ehlo()                                           # Can be omitted
            server.login(from_addr, password)
            server.send_message(msg)
            return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"

# Example usage
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 587

# Email credentials
email = 'kitchen_assistant@outlook.com'
password = 'kitchen123.'  # Replace with the correct password

from_addr = email
to_addr = 'inesaguia@ua.pt'  # Change to the recipient's email
subject = 'Test Email from Python'
body = """
<html><body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">
            <h1>Lista de Compras</h1>
            <p>Caro cliente, aqui está a sua lista de compras para facilitar as suas compras no supermercado:</p>
            <ul><li>Pão</li><li>Leite</li><li>Ovos</li></ul>
        <p>Este email foi enviado automaticamente pelo <strong>Kitchen Assistant</strong>. Não responda a este email.</p>
        <footer><p>Com os melhores cumprimentos,</p><p><strong>Equipa Kitchen Assistant</strong></p></footer>
        </body></html>
"""

result = send_email(from_addr, to_addr, subject, body, smtp_server, smtp_port, password)
print(result)
