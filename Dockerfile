FROM python:3.9.19-alpine3.18

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 80

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]