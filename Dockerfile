FROM python:3.9-alpine
COPY . /root/app/
WORKDIR /root/app/
RUN pip install -r requirements.txt
