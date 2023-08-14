FROM python:3.11

WORKDIR /api

COPY requirements.txt .
COPY ./tristar_api.py .


RUN pip install --no-cache-dir -r requirements.txt


#CMD ["python", "./tristar_api.py"]
