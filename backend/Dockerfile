FROM python:3.10.0a1-slim

WORKDIR /usr/local/bin

# Adding Package Dependency
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./main.py ./main.py

CMD ["python", "main.py"]