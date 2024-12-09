import io
import logging
from typing import Any

import cv2
import numpy as np
from PIL import Image
from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from pyzbar import pyzbar

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scan-qrcode/")
async def scan_qrcode(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image_np = np.array(image)
    sizes = [6500, 4500, 3200]
    count = 0
    info = None
    while count < len(sizes) - 1:
        origin_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        origin_img = resize_image(image=origin_img, new_width=sizes[count])
        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(origin_img)
        if bbox is not None:
            qr_code_img = split_qr_code_area(origin_img=origin_img, bbox=bbox)
            decoded_objects = pyzbar.decode(qr_code_img)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
            info = extract_qr_info(data=data)
        if info:
            break
        count += 1
    if not info:
        return JSONResponse(status_code=400,
                            content={"message": "Please upload a photo with QRcode"})
    return JSONResponse(status_code=200, content={"data": info})


def resize_image(image: np.ndarray, new_width: int) -> np.ndarray:
    ratio = new_width / image.shape[1]
    new_height = int(image.shape[0] * ratio)
    new_size = (new_width, new_height)
    new_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)
    return new_image


def split_qr_code_area(origin_img: np.ndarray, bbox: Any) -> np.ndarray:
    x, y, w, h = cv2.boundingRect(bbox)
    image = origin_img[y:y + h, x:x + w]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(30, 30))
    image = clahe.apply(gray)
    return image


def extract_qr_info(data: str):
    if not data:
        return None
    data_parts = data.split('|')
    if len(data_parts) == 7:
        return {
            "cccd_id": data_parts[0],
            "cmnd_id": data_parts[1],
            "full_name": data_parts[2],
            "dob": format_date_str(data_parts[3]),
            "gender": data_parts[4],
            "residence": data_parts[5],
            "issuance": format_date_str(data_parts[6]),
        }
    else:
        return {
            "cccd_id": data_parts[0],
            "cmnd_id": None,
            "full_name": data_parts[1],
            "dob": format_date_str(data_parts[2]),
            "gender": data_parts[3],
            "residence": data_parts[4],
            "issuance": format_date_str(data_parts[5]),
        }


def format_date_str(date_str: str):
    return f"{date_str[0:2]}/{date_str[2:4]}/{date_str[4:]}"
