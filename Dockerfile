FROM python:3.11-slim
RUN apt-get update && apt-get install -y openjdk-17-jdk docker.io
RUN pip install flask
WORKDIR /app
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]
