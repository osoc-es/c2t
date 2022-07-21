FROM python:3.10.4

WORKDIR /code

COPY . .
RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]