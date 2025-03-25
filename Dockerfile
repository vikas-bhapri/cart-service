FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3103

CMD ["gunicorn", "--bind", "0.0.0.0:3103", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker"]