import os
from typing import List

timeout: int = 3
sp_data_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sp.txt")

bot_token: str = None
students: List = None
teacher_ids: List = None
proxy: str = "protocol://host:port"

try:
    from .local_config import *
except ImportError:
    pass

