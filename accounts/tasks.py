from celery import shared_task
from utils.otp import sms

@shared_task()
def task_send_otp(ip,code, phone):
    return sms.send_otp_code(code,phone)
  
