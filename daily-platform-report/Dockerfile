FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN useradd --create-home --uid 10001 appuser

USER 10001

CMD ["python", "main.py"]