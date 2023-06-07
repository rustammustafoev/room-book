FROM python3:10

WORKDIR /service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install pip --upgrade  && pip install -r ./requirements.txt

COPY . /service