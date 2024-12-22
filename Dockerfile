FROM python:3.10.14-alpine3.20

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 80

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]