import os
import numpy as np
from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS


def load_img(path):
    return Image.open(path)


def save_img(path, img):
    if path.lower().endswith((".jpg", ".jpeg")) and img.mode == "RGBA":
        img = img.convert("RGB")
    img.save(path)


def make_gray(img):
    return img.convert("L")


def change_bright(img, val):
    factor = 1.0 + (val / 100.0)
    return ImageEnhance.Brightness(img).enhance(factor)


def change_contrast(img, val):
    factor = 1.0 + (val / 100.0)
    return ImageEnhance.Contrast(img).enhance(factor)


def change_saturation(img, val):
    factor = 1.0 + (val / 100.0)
    return ImageEnhance.Color(img).enhance(factor)


def rotate_img(img):
    return img.rotate(-90, expand=True)


def get_info(img, path):
    depths = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32}
    depth = depths.get(img.mode, "Неизвестно")
    size_kb = os.path.getsize(path) / 1024

    text = f"Размер: {size_kb:.2f} КБ\n"
    text += f"Разрешение: {img.width}x{img.height}\n"
    text += f"Формат: {img.format}\n"
    text += f"Модель: {img.mode}\n"
    text += f"Глубина: {depth} бит"
    return text


def get_exif(img):
    exif = img.getexif()
    if not exif:
        return "EXIF нет"

    res = ""
    for tag_id, val in exif.items():
        name = TAGS.get(tag_id, tag_id)
        res += f"{name}: {str(val)[:20]}\n"
    return res


def lin_corr(img):
    arr = np.array(img, dtype=np.float32)
    min_val = arr.min()
    max_val = arr.max()

    if min_val == max_val:
        return img.copy()

    res = (arr - min_val) * 255.0 / (max_val - min_val)
    res = np.clip(res, 0, 255).astype(np.uint8)
    return Image.fromarray(res)


def nonlin_corr(img, gamma=0.5):
    arr = np.array(img, dtype=np.float32) / 255.0
    res = 255.0 * (arr**gamma)
    res = np.clip(res, 0, 255).astype(np.uint8)
    return Image.fromarray(res)