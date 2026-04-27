FROM python:3.14.4-alpine3.23

ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

WORKDIR /project/

COPY . /project/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
