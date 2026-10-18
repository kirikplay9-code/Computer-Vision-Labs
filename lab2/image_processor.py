import cv2
import numpy as np
from PIL import Image


def pil_to_cv(img):
    return np.array(img)


def cv_to_pil(arr):
    clipped = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(clipped)


def parse_matrix(text_str, dtype=np.float32):
    rows = [r.strip() for r in text_str.strip().split('\n') if r.strip()]
    matrix = [[float(val) for val in r.split()] for r in rows]
    return np.array(matrix, dtype=dtype)


def apply_morphology(img, op_name, kernel_str):
    arr = pil_to_cv(img)
    kernel = parse_matrix(kernel_str, dtype=np.uint8)

    ops = {
        "erosion": cv2.MORPH_ERODE,
        "dilation": cv2.MORPH_DILATE,
        "opening": cv2.MORPH_OPEN,
        "closing": cv2.MORPH_CLOSE,
        "gradient": cv2.MORPH_GRADIENT,
        "tophat": cv2.MORPH_TOPHAT,
        "blackhat": cv2.MORPH_BLACKHAT
    }

    op_code = ops.get(op_name)
    res = cv2.morphologyEx(arr, op_code, kernel)
    return cv_to_pil(res)


def sharpen_img(img):
    arr = pil_to_cv(img)
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)
    res = cv2.filter2D(arr, -1, kernel)
    return cv_to_pil(res)


def motion_blur_img(img, size=11):
    arr = pil_to_cv(img)
    kernel = np.zeros((size, size), dtype=np.float32)
    kernel[int((size - 1) / 2), :] = np.ones(size)
    kernel = kernel / size
    res = cv2.filter2D(arr, -1, kernel)
    return cv_to_pil(res)


def emboss_img(img):
    arr = pil_to_cv(img).astype(np.float32)
    kernel = np.array([
        [-2, -1, 0],
        [-1,  1, 1],
        [ 0,  1, 2]
    ], dtype=np.float32)
    res = cv2.filter2D(arr, -1, kernel) + 128.0
    return cv_to_pil(res)


def custom_filter_img(img, kernel_str):
    arr = pil_to_cv(img).astype(np.float32)
    kernel = parse_matrix(kernel_str, dtype=np.float32)
    res = cv2.filter2D(arr, -1, kernel)
    return cv_to_pil(res)


def median_filter_img(img, ksize=5):
    arr = pil_to_cv(img)
    if ksize < 3:
        ksize = 3
    if ksize % 2 == 0:
        ksize += 1
    res = cv2.medianBlur(arr, ksize)
    return cv_to_pil(res)
