# import pymysql

#  Setup the database, I might mess with this later.


# Todo Re-enable the database once I have it setup on the server.
# Disabled the database for testing.

# I used a part of the below guide for some of these values
# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# database_host = os.environ.get("DATABASE_HOST")
# database_username = os.environ.get("DATABASE_USERNAME")
# database_password = os.environ.get("DATABASE_PASSWORD")
# database_name = os.environ.get("DATABASE_NAME")

# The app.config string needed to be changed to "mysql+pymysql://" to work
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql

# Create the SQLAlchemy instance
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{database_username}:{database_password}@{database_host}/{database_name}"
# app.config["SQLALCHEMY_DATABASE_URI"] = """f
# "mysql+pymysql://{database_username}:{database_password}@{database_host}/{database_name}"
# """
# db = SQLAlchemy(app)
# db = pymysql.connect(host=database_host, user=database_username, password=database_password, database=database_name)


# # https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask

# https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
# def sql_results():
#     # https://stackoverflow.com/questions/9845102/using-mysql-in-flask
#     cur = db.cursor()
#     sql = "SELECT * FROM passwords"
#     cur.execute(sql)
#     results = cur.fetchall()

#     # This works without the [] but it only displays one password
#     # This works fine in the mariadb_test and prints the items to the console
#     # for [item] in results:
#         # return item

#     return results



# Todo Figure out how to get values out of a database using this.
# @app.route("/var_test", methods = ['GET'])
# def test1_page():
#     if request.method == 'GET':
#         # data = "Test"
#         data = {'username': 'admin', 'site': 'kelsoncraft.net'}
#         return render_template("var_test.html", data=data)
        # return jsonify({'data': data})
        
        
        
