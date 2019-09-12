import os
import sys
from typing import List

timeout: int = 3
sp_data_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sp.txt")

bot_token: str = None
students: List = None
teacher: List = None

try:
    from .local_config import *
except ImportError:
    pass

