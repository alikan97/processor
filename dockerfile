FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
ADD functions/ ${LAMBDA_TASK_ROOT}
COPY secretmanager.py ${LAMBDA_TASK_ROOT}
COPY splunk.py ${LAMBDA_TASK_ROOT}

# Copy function code
COPY handler.py ${LAMBDA_TASK_ROOT}

CMD [ "handler.handler" ]