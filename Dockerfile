# Dockerfile for AWS Lambda
FROM public.ecr.aws/lambda/python:3.10

# install requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# copy relevant code
COPY services ${LAMBDA_TASK_ROOT}/services
COPY controllers ${LAMBDA_TASK_ROOT}/controllers
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.handler" ]
