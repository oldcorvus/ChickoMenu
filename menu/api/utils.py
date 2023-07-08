
from ..models import Menu

def get_code():
    try:
        last_menu = Menu.objects.latest('code')
        return last_menu.code + 1
    except Menu.DoesNotExist:
        return 81413