"""
@brief Módulo para envio de e-mails utilizando SMTP com suporte à validação de endereços de e-mail e conteúdo HTML.

Este módulo fornece uma função para enviar e-mails através de um servidor SMTP, permitindo a inclusão de conteúdo HTML no corpo do e-mail. 
A função também valida os endereços de e-mail do remetente e do destinatário usando a biblioteca `email-validator`.

@details Antes de enviar um e-mail, a função valida os endereços de e-mail do remetente e do destinatário para garantir que são válidos. 
A função utiliza TLS para garantir uma conexão segura ao servidor SMTP.

@note É necessário instalar a biblioteca `email-validator` para a validação de e-mails. Para instalar, utilize um dos comandos a seguir dependendo do seu ambiente:
- pip install email-validator
- pip3 install email-validator
- conda install email-validator

"""

import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
# instal email-validator
# pip install email-validator | pip3 install email-validator | conda install email-validator

def send_email(from_addr, to_addr, subject, body, smtp_server, smtp_port, password):
    """
    @brief Envia um e-mail usando o servidor SMTP com suporte a conteúdo HTML e validação de e-mails.
    @details Esta função primeiro valida os endereços de e-mail utilizando a biblioteca `email-validator`. 
    Se os e-mails são válidos, a função procede com a configuração da mensagem e o envio através do SMTP. 
    Durante o envio, a conexão é segurada com TLS para segurança.
    
    @param from_addr<string> Representa o endereço de e-mail do remetente.
    @param to_addr <string> Representa o endereço de e-mail do destinatário.
    @param subject <string> Representa o assunto do e-mail.
    @param body <string> Contêm o corpo do e-mail em formato HTML.
    @param smtp_server <string> Representa o endereço do servidor SMTP.
    @param smtp_port <int> Representa a porta do servidor SMTP.
    @param password <string> Rrepresenta a password do e-mail do remetente para autenticação no servidor SMTP.
    
    @return <string> Indica se o e-mail foi enviado com sucesso ou se falhou, incluindo a mensagem de erro.
    
    @note É necessário instalar a biblioteca `email-validator` para a validação de e-mails. Para instalar, utilize um dos comandos a seguir dependendo do seu ambiente:
    - pip install email-validator
    - pip3 install email-validator
    - conda install email-validator
    
    """
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
#smtp_server = 'smtp-mail.outlook.com'
#smtp_port = 587

# Email credentials
#email = 'kitchen_assistant@outlook.com'
#password = 'kitchen123.'  # Replace with the correct password

#from_addr = email
#to_addr = 'inesaguia@ua.pt'  # Change to the recipient's email
#subject = 'Test Email from Python'
#body = """
#<html><body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">
#            <h1>Lista de Compras</h1>
#            <p>Caro cliente, aqui está a sua lista de compras para facilitar as suas compras no supermercado:</p>
#            <ul><li>Pão</li><li>Leite</li><li>Ovos</li></ul>
#        <p>Este email foi enviado automaticamente pelo <strong>Kitchen Assistant</strong>. Não responda a este email.</p>
#        <footer><p>Com os melhores cumprimentos,</p><p><strong>Equipa Kitchen Assistant</strong></p></footer>
#        </body></html>
#"""


#result = send_email(from_addr, to_addr, subject, body, smtp_server, smtp_port, password)
#print(result)
