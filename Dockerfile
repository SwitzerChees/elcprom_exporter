FROM python:3.7

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "gunicorn", "-w" , "1", "wsgi:app", "--bind", "0.0.0.0:9000"]