FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD python api.py