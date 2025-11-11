# Use AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Upgrade pip and install your package
RUN pip install --upgrade pip
RUN pip install grid-feedback-optimizer

# Copy your Lambda function code
COPY pf_lambda_s3.py ./

# Set the CMD to your handler
CMD ["pf_lambda_s3.lambda_handler"]