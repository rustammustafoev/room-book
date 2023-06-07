FROM python3:10

WORKDIR /service

COPY ./requirements.txt .

RUN pip install pip --upgrade  && pip install -r ./requirements.txt

COPY . /service

RUN uvicorn app.main:app --reload --host 0.0.0.0 --port 8000