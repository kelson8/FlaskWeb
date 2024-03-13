# KelsonCraft Website

This is the code for the kelsoncraft.net website which is running on Python Flask

I have a dark mode toggle for the website, and I'm using bootstrap v5.

## Files:
* Bootstrap is loaded in this file: [FlaskWeb/templates/head.html](https://git.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/templates/partials/header.html)
* The navbar is in this file: [FlaskWeb/templates/header.html](https://git.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/templates/partials/header.html)
* The footer is in this file: [FlaskWeb/templates/footer.html](https://git.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/templates/partials/footer.html)
* The dark mode javascript files, css, and other javascript files are here: [FlaskWeb/Static](https://git.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/static)
* Example .env file: [FlaskWeb/.env.example](https://git.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/.env.example)
* The html files are here: [FlaskWeb/templates](https://git.internal.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/templates)
* The html files are here: [FlaskWeb/templates](https://git.internal.kelsoncraft.net/kelson8/FlaskWeb/src/branch/main/templates)

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

7. Run the Flask Project: 
* Windows:
* Terminal: python .\flask_web.py
* Linux:
* python3 flask_web.py

# Incomplete
* I don't have docker setup yet for this.


* Make sure to install docker, here is a link to the official download page: 
* https://docs.docker.com/get-docker/
1. First rename the .env.example to .env
2. Modify the .env file to have your database info and secret key
3. Then change the network and volumes in the docker-compose.yml
4. To start: docker-compose up -d

# About
This website will use docker once I set that up, I will have a custom docker-compose.yml and maybe a docker file.

I will be using mariadb for the website also, that won't run in a container.

