import os

class Config:
    # This switches certain features on for the VPS, such as docker_enabled, disabling tests and other things.
    is_vps_enabled = os.environ.get('VPS_ENABLED', 'False') == 'True'

    is_docker_enabled = os.environ.get('DOCKER_ENABLED', 'False') == 'True'

    # Disable the password generator for now.
    password_gen_enabled = False

    # Toggle logging on/off here, if off it redirects log output to the console in PyCharm.
    if is_vps_enabled:
        log_enabled = True
    else:
        log_enabled = False

    # Change the file download directory for the app here
    # If is_vps_enabled is True, then this has no effect
    download_directory = "D:\linode\FlaskWeb\data\downloads"

    # Toggle this on/off for docker being enabled, mostly modifies the paths

    docker_enabled = False

    # This is mostly logs for debugging.
    extra_logs = False

    # Toggle the /test page on and off here.
    if is_vps_enabled:
        html_test_page_enabled = False
    else:
        html_test_page_enabled = True

    ##### Auth test
    ## I mostly have this working, I need to figure out how to make it redirect properly to the video when logged in.
    ## And I need to make this have a rate limit.
    ## I got the SQLite DB working so far, users need to be added to it with the util/add_user_to_db.py file.

    # If this is true, videos with the 'restricted' value set to true in the JSON will require login.
    video_auth = True

    #####

    ## Video stuff
    # Set this to true to switch the video format from /video/videoID to /watch?v= Like YouTube.
    # This pretty much works fine now, but I have it turned off.
    params_video_serve = False
