import os
import smtplib
import mimetypes
from email.encoders import encode_base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_mail(email, subject, text, attachments):
    addr_from = os.getenv("FROM")
    password = os.getenv("PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = addr_from
    msg["To"] = email
    msg["Subject"] = subject

    body = text
    msg.attach(MIMEText(body, "plain"))

    process_attachments(msg, attachments)

    server = smtplib.SMTP_SSL(host=os.getenv("HOST"),
                              port=int(os.getenv("PORT")))
    server.login(addr_from, password)

    server.send_message(msg)
    server.quit()
    return True


def process_attachments(msg, attachments):
    for path in attachments:
        if os.path.isfile(path):
            attach_file(msg, path)
        elif os.path.exists(path):
            pass


def attach_file(msg, file):
    attach_types = {
        "text": MIMEText,
        "image": MIMEImage,
        "audio": MIMEAudio
    }
    filename = os.path.basename(file)
    ctype, encoding = mimetypes.guess_type(file)

    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    with open(file, mode="rb" if maintype != "text" else "r") as file_obj:
        if maintype in attach_types:
            file = attach_types[maintype](file_obj.read(), _subtype=subtype)

            file.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(file)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(file_obj.read())
            encode_base64(file)
    file.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(file)
