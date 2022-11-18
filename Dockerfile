FROM python:3.10-slim-buster

WORKDIR /app

#ENV STRIPE_SEC_KEY=<Ваш ключ Stripe>

#ENV DJANGO_SECRET_KEY=<Ваш ключ Джанго>

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
