from flask import Blueprint, render_template

project_pages = Blueprint('project_pages', __name__, template_folder='templates')

#-----------------
# Begin Game/ReVC pages
#-----------------

@project_pages.route("/projects")
def projects_page():
    return render_template("projects.html")

# @app.route("/revc-additions")
@project_pages.route("/projects/revc")
# def revc_additions_page():
def revc_projects_page():
    return render_template("revc-additions.html")


#-----------------
# End Game/ReVC pages
#-----------------