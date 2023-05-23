FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ChatBot/ .
COPY ChatBot/faiss_index /app/faiss_index

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["index.py"]