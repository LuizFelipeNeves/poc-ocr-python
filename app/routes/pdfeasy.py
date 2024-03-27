# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

from fastapi import APIRouter, File, UploadFile, status

import pdf2image
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

@router.post("/", status_code=status.HTTP_200_OK, summary="PDF OCR with doctr")
async def perform_ocr(file: UploadFile = File(...)):
    """Runs docTR OCR model to analyze the input document"""
    pdf_file = file.file.read()
    images = pdf2image.convert_from_bytes(pdf_file)
    images = [numpy.array(i) for i in images]
    all_text = []
    for pil_im in images:
        results = reader.readtext(pil_im)

        detected_texts = []
        for result in results:
            text = result[1]
            detected_texts.append(text)

        detected_texts_join = ' '.join([result[1] for result in results])
        all_text.append(detected_texts_join)
    return all_text, len(all_text)