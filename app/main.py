# Copyright (C) 2021-2024, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

import asyncio
import time

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse


from app import config as cfg
from app.routes import detection, kie, ocr, recognition, pdf, ocrv, pdfpy, pdfeasy

app = FastAPI(title=cfg.PROJECT_NAME, description=cfg.PROJECT_DESCRIPTION, debug=cfg.DEBUG, version=cfg.VERSION)

# Routing
app.include_router(recognition.router, prefix="/recognition", tags=["image"])
app.include_router(detection.router, prefix="/detection", tags=["image"])
app.include_router(ocr.router, prefix="/ocr", tags=["image"])
app.include_router(kie.router, prefix="/kie", tags=["image"])
app.include_router(ocrv.router, prefix="/ocrv", tags=["image"])

app.include_router(pdf.router, prefix="/pdf", tags=["pdf"])
app.include_router(pdfpy.router, prefix="/pdfpy", tags=["pdf"])
app.include_router(pdfeasy.router, prefix="/pdfeasy", tags=["pdf"])

REQUEST_TIMEOUT_ERROR = 40

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        return await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_ERROR)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(content = {'detail': 'Request processing time excedeed limit',
                             'processing_time': process_time},
                            status_code=504)


# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=cfg.PROJECT_NAME,
        version=cfg.VERSION,
        description=cfg.PROJECT_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
