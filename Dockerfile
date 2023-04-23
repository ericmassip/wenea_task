FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1  # Ensures our console output is not buffered by Docker, but is logged directly

WORKDIR /wenea_task

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
