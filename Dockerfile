FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

EXPOSE $PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]