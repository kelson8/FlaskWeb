FROM python:3.12.12-slim-bookworm

# https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
# https://smirnov-am.github.io/running-flask-in-production-with-docker/
# https://blog.logrocket.com/build-deploy-flask-app-using-docker/

WORKDIR /app

# This fixes the incorrect time with logging on the VPS.
# Install tzdata and set the timezone
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/

# Install pip requirements
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
# RUN chmod +x ./run.sh

EXPOSE 81

# Set docker enabled to true, for flask_web.py
ENV DOCKER_ENABLED=True

# Set to true if running on the public VPS, instead of the dev servers on the LAN.
ENV VPS_ENABLED=True

# Moved to compose
#CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
