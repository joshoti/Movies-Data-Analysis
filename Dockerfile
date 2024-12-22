FROM python:3.11.10-slim-bookworm

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 80

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]