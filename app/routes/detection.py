
# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.


from fastapi import APIRouter, File, UploadFile, status

import pytesseract
import numpy
from PIL import Image

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, summary="Image OCR with pytesseract")
async def perform_ocr(file: UploadFile = File(...)):
    """Runs pytesseract to analyze the input image"""
    imgFile = numpy.array(Image.open(file.file).convert("RGB"))
    detected_texts_join = pytesseract.image_to_string(imgFile, lang='por')
    return detected_texts_join