FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

WORKDIR /image-extractor

COPY requirements.txt /image-extractor/
RUN pip install -r requirements.txt

COPY . /image-extractor/