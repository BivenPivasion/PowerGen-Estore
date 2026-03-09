FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

# Копіюємо requirements окремо
COPY my_shop/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо все інше
COPY my_shop/ /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]