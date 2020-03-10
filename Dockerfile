FROM python:3.7.3-alpine

COPY ./static /home/app/
COPY ./templates /home/app/
COPY ./sample_app.py /home/app/.

WORKDIR /home/app/

EXPOSE 8888/tcp

RUN pip install flask

CMD python /home/app/sample_app.py