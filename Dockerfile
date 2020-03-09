FROM python:3.7.3-alpine
WORKDIR /home/app/
COPY ./sample_app.py /home/app/.
RUN pip install flask
CMD python /home/app/sample_app.py
EXPOSE 8888