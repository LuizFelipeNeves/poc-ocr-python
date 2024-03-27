FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt-get update \
    && apt-get install --no-install-recommends git ffmpeg libsm6 libxext6 make -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install easyocr Pillow numpy pytesseract pdf2image

COPY pyproject.toml  /app/pyproject.toml
COPY Makefile /app/Makefile

RUN pip install --upgrade pip setuptools wheel poetry \
    && make lock \
    && pip install -r /app/requirements.txt \
    && pip cache purge \
    && rm -rf /root/.cache/pip

# install tesseract
ENV DEBIAN_FRONTEND noninteractive

# Setting the data prefix
ENV TESSDATA_PREFIX=/usr/local/share/tessdata

# Update and install depedencies
RUN apt-get update && \
    apt-get install -y wget unzip bc vim python3-pip libleptonica-dev git

# Packages to complie Tesseract
RUN apt-get install -y --reinstall make && \
    apt-get install -y g++ autoconf automake libtool pkg-config \
     libpng-dev libjpeg62-turbo-dev libtiff5-dev libicu-dev \
     libpango1.0-dev autoconf-archive

RUN apt-get install -y poppler-utils

RUN mkdir src && cd /app/src && \
    wget https://github.com/tesseract-ocr/tesseract/archive/refs/tags/5.3.4.zip && \
	unzip 5.3.4.zip && \
    cd /app/src/tesseract-5.3.4 && ./autogen.sh && ./configure && make && make install && ldconfig && \
    make training && make training-install && \
    cd /usr/local/share/tessdata && wget https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/eng.traineddata && \
    wget https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/por.traineddata

# copy project
COPY app /app/app