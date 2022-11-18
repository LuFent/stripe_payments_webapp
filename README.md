# Онлайн магазин на Django + Stripe
Веб приложение онлайн-магазина, с возможностью добавления/редактирования товаров на Django framework, с оплатой через сервис Stripe.
------
## Запуск локально

1) Скачайте репозиторий и перейдите в него
    ```
    git clone git@github.com:LuFent/stripe_shop_webapp.git
    cd stripe_shop_webapp
    ```

 2) *(Опционально)* создайте виртуальное окружение
    ```
    virtualenv venv
    source ./venv/bin/activate
    ```

3) Скачайте зависимости
    ```
    pip3 install -r requirements.txt
    ```

4) Получите ключи STRIPE и Джанго
    4.1 Тестовые ключи Stripe [доступны тут](https://dashboard.stripe.com/test/apikeys)
    4.2 Ключ Джанго можно [получить тут](https://djecrety.ir/)

5) Создайте .env файл с таким содержанием:
    ```
    export STRIPE_SEC_KEY='<Ваш секретный ключ Stripe>'
    export DJANGO_SECRET_KEY='<Ваш секретный ключ Django>'
    ```

6) Выполните миграции командой
    ```
    python3 manage.py migrate
    ```

7) Создайте админа командой
    ```
    python3 manage.py createsuperuser
    <Введите имя и пароль, поле email можно оставить пустым>
    ```

8) Запустите сайте на локалхосте командой
    ```
    python3 manage.py runserver
    ```

 9)   **Готово!** Cайт должен быть доступен по адресу http://127.0.0.1:8000/
      Чтобы создать товары зайдите в админку по адресу http://127.0.0.1:8000/admin, введиие заданные ранее имя и пароль и во вкладке *Товары* создайте новые товары. Они должны будут появиться на главной сайта. Чтобы купить товары зайдите в Корзину и нажмите *Оплатить*. Если вы использовали тестовые ключи Stripe, то сымитировать успешную оплату можно [одной из тестовых карт](https://stripe.com/docs/testing#cards), например
      4242 4242 4242 4242
      <12/30> <любые 3 цифры>

 10)  В репозитории также лежит Dockerfile который позволяет запустить сайт внутри Docker-контейнера


---
## Все возможные настройки .env

```
STRIPE_SEC_KEY='<Ваш секретный ключ Stripe>'
DJANGO_SECRET_KEY='<Ваш секретный ключ Django>'
DJANGO_DEBUG=<Настройка Дебага True/False, по дефолту True>
IF_USING_POSTGRES=<Используется ли Postgresql вместо SQLITE, по дефолту False>
# Если IF_USING_POSTGRES=True
  POSTGRES_DB_NAME='<Имя Дб Postgresql>'
  POSTGRES_DB_USER='<Имя Юзера Postgresql>'
  POSTGRES_DB_PSW='<Пароль Postgresql>'
  POSTGRES_DB_HOST='<Хост Postgresql>'
  POSTGRES_DB_PORT='<Порт Postgresql>'
```

---
## Цели проекта

Проект выполнен в качестве тестового задания на вакаснию.
