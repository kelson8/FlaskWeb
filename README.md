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

## Running the website
## Run without docker
* Make sure to have python installed, here is a link to the official website: 
* https://www.python.org/downloads/
1. Rename the .env.example to .env.
2. Modify the .env file to have your database info and secret key.
3. Create a virutal environment for your system using the below link: https://docs.python.org/3/library/venv.html
4. python -m venv venv
5. Source the venv:

Windows:

* Cmd: venv\Scripts\activate.bat
* Powershell: venv\Scripts\Activate.ps1

Linux:
* Bash/zsh: source venv\Scripts\activate

6. Install the requirements: pip install -r requirements.txt

7. Run the Flask Project: waitress-serve --port \<port\> flask_web:app

For testing locally or developing this site, run like this:
* data/flask_web.py - flask --app flask_web run

## Run with docker

* Make sure to install docker, here is a link to the official download page: 
* https://docs.docker.com/get-docker/
1. First rename the .env.example to .env
2. Modify the .env file to have your database info and secret key
3. Copy the .env file to the `data` folder
4. Then change the network and volumes in the docker-compose.yml
5. To start: docker-compose up -d

## Modifying the site
This website now uses a template system for videos [video_template.html](https://github.com/kelson8/FlaskWeb/blob/main/data/templates/video_template.html), and for the base index.html [_base.html](https://github.com/kelson8/FlaskWeb/blob/main/data/templates/_base.html)

**To add new video pages to the site:**

1. Add the video file into `data/media/videos`
2. Go to `data/json/videos.json`
3. If the video is needing to be restricted set restricted to true in the `videos.json` and, add it into `data/media/videos`, if not then add it into `data/static/videos`
4. Add some videos into there like this, specify the title, description, and file name that is in `data/media/videos`
```json: 
{
  "1": {
    "title": "Tom Clancy's Ghost Recon Wildlands Chopper glitch",
    "description": "I'm not sure how I would do this again, it just randomly happened one day.",
    "file": "tom_clancy_wildlands_glitch1.mp4",
    "restricted": false
  },
  "2": {
    "title": "ReVC Spinning Cars",
    "description": "I coded this function using C++ to mess around with, the game crashes at the end.",
    "file": "ReVC-SpinningCars.mp4",
    "restricted": false
  },
  "3": {
    "title": "ReVC KCNet ImGui Test",
    "description": "This is a ImGui mod menu I am working on in C++ using ReVC.",
    "file": "ReVC-KCNet-ImGuiMenu1.mp4",
    "restricted": false
  },
  "4": {
    "title": "KCNet Flask Auth Test",
    "description": "This is a test for logins with Python Flask, and SQLite.",
    "file": "KCnet_Auth-2025-10-9.mp4",
    "restricted": true
  }
}
```

**To add new pages to the site:**
1. Create a new html file in `data/templates`, specify a category such as `data/templates/projects` if needed.
2. Go into the newly created html file, add this into it, this below matches my template:
```html
{% extends "_base.html" %}

{% block title %}Site Title{% endblock %}

{% block content %}
<div class="mt-4 p-5 bg-secondary text-white rounded">
    <h1 class="main_headers"> Site Header </h1>

</div>
{% endblock %}
```

3. Add the page into one of the python files for pages, such as `test_pages.py` or `project_pages.py` example for rpi-pico project page in `project_pages.py`:
```python
@project_pages.route("/projects/rpi-pico")
def rpi_pico_projects_page():
    return render_template("/projects/rpi-pico.html")
```

# About
This website has docker support.

The website now uses [Plyr javascript video player](https://plyr.io/) for the video player.
 For now, I have disabled direct downloads of videos with this.

I may use mariadb for the website also in the future.

This is running with the waitress WGSI Server.
For testing, it can be started directly with the `app.run` in `data/flask_web.py`

----

I have now moved a few variables to the .env and config.py files.

If using docker, the .env.example will need to be moved from the root of the project, into the `data` folder with the name `.env`.

----

**Variable list in files:**

**config.py file**

| Value                  | Info                                                                                                                                    |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| password_gen_enabled   | If this is True, it enables the `/password_gen` route.                                                                                  |
| log_enabled            | This enables logging to the `flask.log` file if turned on.                                                                              |
| download_directory     | If not using docker, set this to your Flask download directory for the site.                                                            |
| extra_logs             | This enables some extra logging that shouldn't be enabled in production.                                                                |
| html_test_page_enabled | If this is enabled, it enables the `/test` route.                                                                                       |
| video_auth             | This makes videos with `restricted` set to true in `video.json` require a login.                                                        |
| params_video_serve     | This changes the video format from `/video/videoid` to `/watch?v=videoid` in the url path, so far this is broken for restricted videos. |

----

**.env file**

Variables that can be changed in the .env:

| Value              | Info                                                                                                                            |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------|
| SECRET_KEY         | Required for login, and other items on the site. Set this with the secret key, generate with `data/util/generate_secret_key.py` |
 | IP_API_KEY         | This isn't currently in use, I may try to setup an API for the `/proxy-ip` endpoint in Flask                                    |
 | DOCKER_ENABLED     | This changes certain paths, such as the download folder. Also, this gets enabled in the Dockerfile automatically.               |
 | VPS_ENABLED        | If this is set to `True`, it disables certain test items, and enables logging.                                                  |
 | DOWNLOAD_DIRECTORY | If not using docker, set this to the path of the download directory for the app, such as `D:\downloads`                         |



Variables that may be removed in the future (These were once in use for MySQL):

| Value                  | Info                |
|------------------------|---------------------|
| DATABASE_HOST          | MySQL DB host       |
| DATABASE_USERNAME      | MySQL DB username   |
| DATABASE_PASSWORD      | MySQL DB password   |
| DATABASE_ROOT_PASSWORD | MySQL root password |
| DATABASE_NAME          | MySQL DB name       |


# Credits
Credit goes to [https://github.com/coliff/dark-mode-switch](https://github.com/coliff/dark-mode-switch) for the new dark mode switch that I have modified, and for the script located here: [main/data/static/js/dark-mode-switch.js](https://github.com/kelson8/FlaskWeb/blob/main/data/static/js/dark-mode-switch.js)

# License
This Flask project is licensed under the GPLv3 license.

