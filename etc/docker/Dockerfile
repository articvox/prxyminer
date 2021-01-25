FROM python:3.8-slim-buster

RUN mkdir /proxy-twit
ADD . /proxy-twit/
RUN pip install -r /proxy-twit/requirements.txt \
    && pip install gunicorn

RUN apt-get update \
    && apt-get install -y \
        vim

WORKDIR "/proxy-twit"
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]