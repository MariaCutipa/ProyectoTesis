FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY cats.csv .
COPY app.py .
COPY dependences.py .

RUN pip install --no-cache-dir -r requirements.txt

RUN python dependences.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
