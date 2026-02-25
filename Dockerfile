FROM registry.access.redhat.com/ubi9/python-39:latest

USER root

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN chown -R 1001:0 /app && chmod -R g=u /app

USER 1001

EXPOSE 8000

CMD ["python", "main.py"]
