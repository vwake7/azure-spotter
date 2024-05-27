FROM python:3.12.3-alpine
COPY azurespot.py .

COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/opt/venv/bin:$PATH"

CMD ["python", "./azurespot.py"]

