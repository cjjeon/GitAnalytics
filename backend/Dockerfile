FROM python:3.10.0a1-slim

WORKDIR /usr/local/bin

# Adding Package Dependency
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /backend

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["python", "/backend/main.py"]