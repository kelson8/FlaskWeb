class Config:
    # Disable the password generator for now.
    password_gen_enabled = False

    # Toggle logging on/off here, if off it redirects log output to the console in PyCharm.
    log_enabled = True

    # Toggle this on/off for docker being enabled, mostly modifies the paths
    docker_enabled = False

    # This is mostly logs for debugging.
    extra_logs = False

    # Toggle the /test page on and off here.
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
