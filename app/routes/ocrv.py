
# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.


from fastapi import APIRouter, File, UploadFile, status

import easyocr
import numpy
from PIL import Image

router = APIRouter()

reader = easyocr.Reader(
    ['pt'],
    model_storage_directory='/tmp',
    user_network_directory='/tmp',
    download_enabled=True,
    gpu=False
)

@router.post("/", status_code=status.HTTP_200_OK, summary="Image OCR with easyocr")
async def perform_ocr(file: UploadFile = File(...)):
    """Runs easyocr to analyze the input image"""
    imgFile = numpy.array(Image.open(file.file).convert("RGB"))

    results = reader.readtext(imgFile)

    detected_texts = []
    for result in results:
        text = result[1]
        detected_texts.append(text)

    detected_texts_join = ' '.join([result[1] for result in results])
    return detected_texts_join