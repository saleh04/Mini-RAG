import os  # noqa: N999
import random
import string

from helpers.config import get_settings


class BaseController:
    def __init__(self):
        self.app_settings = get_settings()

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")

    def generate_random_string(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        