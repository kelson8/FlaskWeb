# KelsonCraft Website

This is the code for the kelsoncraft.net website which is running on Python Flask

I have a dark mode toggle for the website, and I'm using bootstrap v5.

Website Link: (https://kelsoncraft.net)

## Files:
* Bootstrap is loaded in this file: [FlaskWeb/data/templates/head.html](https://github.com/kelson8/FlaskWeb/blob/main/data/templates/partials/head.html)
* The navbar is in this file: [FlaskWeb/data/templates/header.html](https://github.com/kelson8/FlaskWeb/blob/main/data/templates/partials/header.html)
* The footer is in this file: [FlaskWeb/data/templates/footer.html](https://github.com/kelson8/FlaskWeb/blob/main/data/templates/partials/footer.html)
* The dark mode javascript files, css, and other javascript files are here: [FlaskWeb/data/static](https://github.com/kelson8/FlaskWeb/tree/main/data/static)
* Example .env file: [FlaskWeb/.env.example](https://github.com/kelson8/FlaskWeb/blob/main/.env.example)
* The html files are here: [FlaskWeb/data/templates](https://github.com/kelson8/FlaskWeb/tree/main/data/templates)

* JQuery and CSS are here: [FlaskWeb/data/templates/head.html](https://github.com/kelson8/FlaskWeb/blob/main/data/templates/partials/head.html)
## Setup
To run
* Without docker:
* Make sure to have python installed, here is a link to the official website: 
* https://www.python.org/downloads/
1. Rename the .env.example to .env.
2. Modify the .env file to have your database info and secret key.
3. Create a virutal environment for your system using the below link: https://docs.python.org/3/library/venv.html
4. python -m venv venv
5. Source the venv:
* Windows:

* Cmd: venv\Scripts\activate.bat
* Powershell: venv\Scripts\Activate.ps1

* Linux:
* Bash/zsh: source venv\Scripts\activate

6. Install the requirements: pip install -r requirements.txt

7. Run the Flask Project: waitress-serve --port \<port\> flask_web:app


* With Docker:

* Make sure to install docker, here is a link to the official download page: 
* https://docs.docker.com/get-docker/
1. First rename the .env.example to .env
2. Modify the .env file to have your database info and secret key
3. Then change the network and volumes in the docker-compose.yml
4. To start: docker-compose up -d

# About
This website has docker support.

I will be using mariadb for the website also, that won't run in a container.

This is running with the waitress WGSI Server.

# License
This Flask project is licensed under the GPLV3 license.

