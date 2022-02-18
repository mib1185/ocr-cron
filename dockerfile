FROM python:3.10-slim-buster

RUN apt update && DEBIAN_FRONTEND=noninteractive apt -y install \
    build-essential \
    python3-dev \
    python3-pip \
    python3-wheel \
    python3-opencv \
    libfreetype6-dev \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    libtiff5-dev \
    tesseract-ocr \
    zlib1g-dev \
    && apt autoclean

WORKDIR /root

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .

VOLUME /indir
VOLUME /outdir

ENTRYPOINT ["python3", "main.py", "-i", "/indir", "-o", "/outdir"]
