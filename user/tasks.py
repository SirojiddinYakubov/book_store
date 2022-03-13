from api.v1.user.utils import get_email_admins, build_excel_report_file, SendMessageWithGmail
from conf.celery import app


@app.task(bind=True)
def send_report(self):
    print('[+] Starting send report')
    try:
        recipients = get_email_admins()
        response = build_excel_report_file()
        message = SendMessageWithGmail(recipients, response)
        message.send()
        return True
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
