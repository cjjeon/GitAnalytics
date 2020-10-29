FROM python:3.10.0a1-slim

WORKDIR /usr/local/bin

# Installing git package that is used for GitAnalytic
RUN apt-get update && apt-get install -y git

# Adding Package Dependency
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /backend

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["python", "-u", "/backend/main.py"]