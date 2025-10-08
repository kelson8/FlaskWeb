from flask import Blueprint, render_template, redirect

misc_pages = Blueprint('misc_pages', __name__, template_folder='templates')

#-----------------
# Misc pages
#-----------------

@misc_pages.route("/wiki")
def wiki_page():
    return redirect("https://wiki.kelsoncraft.net/", code=302)

# Forum test, enable domain when ready to make public.
# Todo Setup this forum later.
# @misc_pages.route("/forum")
# def forum_page():
#     return redirect("https://forum.kelsoncraft.net/")


#-----------------
# End misc pages
#-----------------