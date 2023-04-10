FROM python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY logger.py handler.py ./
COPY functions/ ./

CMD [ "handler.handler" ]