FROM python:3.12.11-slim-bookworm

# https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
# https://smirnov-am.github.io/running-flask-in-production-with-docker/
# https://blog.logrocket.com/build-deploy-flask-app-using-docker/

WORKDIR /app

# https://askubuntu.com/questions/1438002/mariadb-connector-c-is-not-installed
# This fixes that error with mysql
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends libmariadb3 libmariadb-dev 

# Install pip requirements
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
# RUN chmod +x ./run.sh

EXPOSE 81

# Set docker enabled to true, for flask_web.py
ENV DOCKER_ENABLED=True

# Moved to compose
#CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
