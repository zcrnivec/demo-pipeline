FROM python:3.7.3-alpine

COPY ./static /home/app/static
COPY ./templates /home/app/templates
COPY ./sample_app.py /home/app/.

WORKDIR /home/app/

EXPOSE 8888/tcp

RUN pip install flask

CMD python /home/app/sample_app.py

