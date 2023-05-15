FROM public.ecr.aws/lambda/python:3.7

WORKDIR /

COPY splunk.py ./
COPY handler.py ./
ADD functions/ ./

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "handler.handler" ]