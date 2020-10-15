FROM preset/superset:latest

COPY ./config.py /app/superset/config.py

# Migrate local DB to latest
#RUN superset db upgrade

# Set Role
#RUN superset init

# Create Dummy Admin
#RUN superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin