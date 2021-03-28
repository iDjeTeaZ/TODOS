FROM python:3.8-alpine

ADD . .
RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]
EXPOSE 5001

CMD ["python3", "api.py"]
