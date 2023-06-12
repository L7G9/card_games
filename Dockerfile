FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY controller controller
COPY model model
COPY view view
COPY run_21bust.py .

CMD ["python3", "run_21bust.py"]
