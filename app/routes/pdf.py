# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

from typing import List

from fastapi import APIRouter, File, UploadFile, status

from app.schemas import OCROut
from doctr.models import ocr_predictor
from doctr.io.reader import DocumentFile

router = APIRouter()
model = ocr_predictor(pretrained=True)

@router.post("/", response_model=List[OCROut], status_code=status.HTTP_200_OK, summary="PDF OCR with doctr")
async def perform_ocr(file: UploadFile = File(...)):
    """Runs docTR OCR model to analyze the input document"""
    doc = DocumentFile.from_pdf(file.file.read())
    out = model(doc)
    return [
        OCROut(box=(*word.geometry[0], *word.geometry[1]), value=word.value)
        for block in out.pages[0].blocks
        for line in block.lines
        for word in line.words
    ]