FROM python:3.11.9-slim-bookworm

WORKDIR /app
COPY ./app /app/
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "fastapi" , "run", "--host", "0.0.0.0", "--port", "8000", "/app/main.py" ]
