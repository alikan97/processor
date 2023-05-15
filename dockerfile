FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY splunk.py handler.py ./
COPY functions/ ./

CMD [ "handler.handler" ]