FROM python:3.11.9-alpine

WORKDIR /usr/src/sendergmail

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "bot_run.py" ]

