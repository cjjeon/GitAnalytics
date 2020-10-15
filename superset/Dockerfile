FROM preset/superset:e90c63fc7b911efc16919abf5b017aa0f6250985

# Need this such that we are able to use sqlite
# https://github.com/apache/incubator-superset/issues/9748
COPY ./config.py /app/superset/config.py

# Migrate local DB to latest
RUN superset db upgrade

# Set Role
RUN superset init

# Create Dummy Admin
RUN superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin