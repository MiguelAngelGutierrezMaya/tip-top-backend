# Python dependencies
import environ
import os
import smtplib
import json
import datetime

# Django
from django.template.loader import render_to_string

# Models
from tip_top_backend.notifications.models import Notification

# Email service
import email.utils
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def notification_service():

    notifications = Notification.objects.filter(status="PENDING")
    env = environ.Env()

    for notification in notifications:
        if notification.type == 'EMAIL':
            data = json.loads(notification.data)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = notification.title
            msg['From'] = email.utils.formataddr((env('NOTIFIER_NAME'), env('NOTIFIER_EMAIL')))
            msg['To'] = notification.to
            msg.attach(MIMEText(render_to_string(notification.template + '.txt', data), 'plain'))
            msg.attach(MIMEText(render_to_string(notification.template + '.html', data), 'html'))

            if data['type'] == 'assignment':
                images = ['logo.png', 'clase-asignada.png', 'clase-asignada-en.png', 'bg-date.png']
            elif data['type'] == 'reminder':
                images = ['logo.png', 'clase-programada.png', 'clase-programada-en.png', 'bg-date2.png']
            elif data['type'] == 'forgot-password':
                images = ['logo.png', 'bg-date.png']
            else:
                images = ['logo.png']

            for f in images:
                fp = open(os.path.join(os.path.dirname(__file__) + '/../../templates/assets/', f), 'rb')
                msg_img = MIMEImage(fp.read(), _subtype="png")
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(f))
                msg.attach(msg_img)

            send = True

            if data['type'] != 'assignment' and data['type'] != 'forgot-password':
                datetime_formatted = datetime.datetime.strptime(data['date_init'], "%Y-%m-%d %H:%M")
                current_date = (datetime.datetime.now() - datetime.timedelta(hours=5))
                diff = datetime_formatted - current_date
                hours = int(diff.days) * 24 + int(diff.seconds//3600)
                if hours > 1:
                    send = False

            if send:
                server = smtplib.SMTP(env('HOST_SMTP'), env('PORT_SMTP'))
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(env('USERNAME_SMTP'), env('PASSWORD_SMTP'))
                server.sendmail(env('NOTIFIER_EMAIL'), notification.to, msg.as_string())
                server.close()

                notification.status = 'SEND'
                notification.save()

    return {"ok"}
