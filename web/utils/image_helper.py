"""
辅助函数：将图片转换为 base64
"""
import base64
from pathlib import Path

def get_base64_image(image_path):
    """读取图片并转换为 base64"""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
