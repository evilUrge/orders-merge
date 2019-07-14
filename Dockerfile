FROM python:3.7.0


ADD . /app
WORKDIR /app

RUN pip install -r /app/requirements.txt
RUN echo "ain't no requirements where she goes!"
ENV PYTHONPATH $pwd
ENV DOCKER 1

CMD ["python", "run.py"]
