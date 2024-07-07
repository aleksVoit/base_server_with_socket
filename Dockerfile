FROM python:3.11.9-slim-bookworm

WORKDIR /base_server

COPY . .

CMD ["python3", "main.py"]