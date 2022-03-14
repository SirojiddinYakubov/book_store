import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from typing import List

import openpyxl
from django.contrib.auth import get_user_model
from openpyxl.styles import Alignment, Font

from common.models import OrderedProduct
from conf import settings

User = get_user_model()


class SendMessageWithGmail:
    def __init__(self, recipients, attachment_file):
        self.sender = settings.EMAIL_HOST_USER
        self.sender_password = settings.EMAIL_HOST_PASSWORD
        self.recipients = recipients
        self.attachment_file = attachment_file
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.subject = 'Book Store weekly report'
        self.filename = 'report.xlsx'

    def send(self):
        self.validate()
        msg = MIMEMultipart()
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(user=self.sender, password=self.sender_password)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        if isinstance(self.recipients, list):
            msg['To'] = ", ".join(self.recipients)
        else:
            msg['To'] = self.recipients
        filename = self.filename
        xlsx = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        xlsx.set_payload(self.attachment_file)
        encoders.encode_base64(xlsx)
        xlsx.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(xlsx)
        server.sendmail(self.sender, self.recipients, msg.as_string())
        server.quit()

    def validate(self):
        if not self.sender and self.sender_password:
            raise ValueError("Логин и пароль отправителя не найдены")


def build_excel_report_file() -> bytes:
    wb = openpyxl.Workbook()
    worksheet = wb.active
    header_row = ["#", "Дата", "Книга", "Цена", "Кол-во", "Клиент", "Номер клиента"]
    worksheet.append(header_row)

    worksheet.column_dimensions['B'].width = 15
    worksheet.column_dimensions['C'].width = 20
    worksheet.column_dimensions['D'].width = 20
    worksheet.column_dimensions['E'].width = 10
    worksheet.column_dimensions['F'].width = 30
    worksheet.column_dimensions['G'].width = 30

    build_report_data(worksheet)

    for x in range(1, 4):
        for y in range(1, 8):
            cell = worksheet.cell(x, y)
            if x == 1:
                cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='left')
    output = BytesIO()
    wb.save(output)
    return output.getvalue()


def build_report_data(worksheet):
    queryset = OrderedProduct.objects.filter(is_active=True, order__acceptpayment__isnull=False,
                                             order__is_active=True, order__acceptorder__isnull=False) \
        .values('book__title', 'price', 'count', 'order__customer__last_name', 'order__customer__first_name',
                'order__customer__middle_name', 'order__customer__phone', 'created_at')
    datas = []
    for index, item in enumerate(queryset):
        index = index + 1
        row = [
            index,
            item['created_at'].strftime('%d/%m/%Y'),
            item['book__title'],
            item['price'],
            item['count'],
            f"{item['order__customer__last_name']} {item['order__customer__first_name']} {item['order__customer__middle_name']}",
            item['order__customer__phone'],
        ]
        worksheet.append(row)
    return datas


def get_email_admins() -> List:
    emails = User.objects.filter(role=User.Role.ADMIN, is_active=True).values_list('email', flat=True)
    return list(emails)
