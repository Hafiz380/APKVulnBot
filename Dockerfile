FROM openjdk:17-slim
RUN apt-get update && \
    apt-get install -y python3 python3-pip docker.io && \
    pip3 install flask
WORKDIR /app
COPY . /app
EXPOSE 5000
CMD ["python3", "app.py"]
