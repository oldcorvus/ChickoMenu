from string import digits
from secrets import choice as secret_choice
import random
from kavenegar import *

from django.conf import settings

def get_client_ip(request) :
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
    
    
def otp_generator(size: int = 6, char: str = digits) :
    return "".join(secret_choice(char) for _ in range(size))



class Sms:
    """
        Note:
            for use this method, need to write task.
    """
    API_KEY = settings.API_KEY
    SENDER = ''
    MESSAGE = None

    def send(self, receiver, message):
        try:
            api = KavenegarAPI(self.API_KEY)
            params = {
                'sender': '',
                'receptor': receiver,
                'message': message,
            }
            response = api.sms_send(params)
            print(response)

            return True
        except APIException as e:
            print(e)
            return False
        except HTTPException as e:
            print(e)
            return False
        except:
            return False

    def send_otp_code(self,code, phone_number):

        if (self.send(receiver=phone_number, message=f'کد: {code}')):
            return True
        else:
            return False

    def send_new_password(self, phone_number):
        password = str(random.randint(10000, 99999))
        self.send(receiver=phone_number, message=f'کلمه عبور جدید شما: {password}')
        return password

    def send_code(self, phone_number, code, password=None):
        self.send(receiver=phone_number, message=f'کد شما: {code}')
        return code

    def send_status_order(self, phone_number, message):
        self.send(receiver=phone_number, message=message)
        return True

    def send_sms(self, phone_number, message):
        self.send(receiver=phone_number, message=message)
        return True


sms = Sms()