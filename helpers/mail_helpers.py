import logging
import mimetypes
import os
import smtplib, ssl
from email.header import Header
from email.message import EmailMessage
from email.utils import formataddr

from models.route_model import EmpData



SENDER_EMAIL = "sender@example.com"
SENDER_PASSWORD = "senderpassword"

def sendMail(receiver_email, subject, body, files=None, cc=None, bcc=None):
    try:
        # Create a multipart message and set headers
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD

        message = EmailMessage()
        message["From"] = formataddr((str(Header("HeaderLabel", 'utf-8')), sender_email))
        message["To"] = receiver_email
        if cc is not None:
            message["cc"] = cc
        if bcc is not None:
            message["bcc"] = bcc
        message["Subject"] = subject


        # Add body to email
        message.add_alternative(body, subtype="html")
        if files is not None:
            for fl in files:
                if os.path.isfile(fl):
                    file_name = os.path.basename(fl)
                    mime_type, _ = mimetypes.guess_type(fl)
                    with open(fl, "rb") as fp:
                        file_data = fp.read()
                        message.add_attachment(
                            file_data,
                            maintype=mime_type.split("/")[0],
                            subtype=mime_type.split("/")[1],
                            filename=file_name
                        )
                        
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
    
        return True
    except Exception as ex:
        logging.error(f"sendMail Exception: {ex}")
        return False

# eaxmple how to send email
def informAdmin(empData: EmpData):
    try:
        subject = "A new employee has been added to your company"
        body = f"""\
                <html>
                <body>
                    <p>Hello Admin,<br>
                        Please find the request form details below: <br/><br/>
                        <b>Name: {empData.name}<br/>
                        Designation: {empData.designation}<br/>
                        Employee Code: {empData.emp_code}<br/>
                        <br/><br/>
                    </p>
                    <p>Regards,<br>
                        Signature Here
                    </p>
                </body>
                </html>
                """

        return sendMail("ReceiverEmail@here", subject, body)
    except Exception as ex:
        logging.error(f"sendRequestForm Exception: {ex}")
        return False