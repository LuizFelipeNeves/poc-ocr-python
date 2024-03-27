# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

from fastapi import APIRouter, File, UploadFile, status

import pdf2image
import pytesseract

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, summary="PDF OCR with doctr")
async def perform_ocr(file: UploadFile = File(...)):
    """Runs docTR OCR model to analyze the input document"""
    pdf_file = file.file.read()
    images = pdf2image.convert_from_bytes(pdf_file)
    all_text = []
    for i in images:
        pil_im = i
        text = pytesseract.image_to_string(pil_im, lang='por')
        # ocr_dict = pytesseract.image_to_data(pil_im, lang='eng', output_type=Output.DICT)
        # ocr_dict now holds all the OCR info including text and location on the image
        # text = " ".join(ocr_dict['text'])
        # text = re.sub('[ ]{2,}', '\n', text)
        all_text.append(text)
    return all_text, len(all_text)