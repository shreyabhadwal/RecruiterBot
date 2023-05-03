FROM python:3.9-slim-buster

WORKDIR /ChatBot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ChatBot/ .
COPY ChatBot/faiss_index /app/faiss_index

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["index.py"]