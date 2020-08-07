FROM python:2
COPY . /app
RUN pip install flask && pip install mysql-connector-python && pip install redis && pip install flask-redis && pip install flask-mysql && pip install boto3
WORKDIR /app
CMD python app.py
EXPOSE 5000