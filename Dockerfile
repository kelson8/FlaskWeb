FROM python:3.12.10-slim-bookworm

# https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
# https://smirnov-am.github.io/running-flask-in-production-with-docker/
# https://blog.logrocket.com/build-deploy-flask-app-using-docker/

# Todo Re-enable database support.

# I will need to create the passwords table before this works, also I didn't figure out how to do
# mariadb in the container, it kept giving errors but it started up.

# I got the container working by disabling the database connection, I think it's just not loading the values from
# the .env file or it needs the table created.

WORKDIR /app

# https://askubuntu.com/questions/1438002/mariadb-connector-c-is-not-installed
# This fixes that error with mysql
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends libmariadb3 libmariadb-dev 

# Install pip requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
# RUN chmod +x ./run.sh

EXPOSE 81

# I never did get these working.
# ENTRYPOINT ["./entrypoint.sh"]
# CMD ["./run.sh"]

# Moved to compose
#CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
