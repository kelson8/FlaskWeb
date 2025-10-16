import json

import requests
from flask import Blueprint, render_template, request, Response

from models import html_test_page_enabled
from password_gen import password_gen

# TODO Figure out how to move this one, for now it'll stay in flask_web.py.
# from flask_web import passwordGenEnabled


# This works for splitting the page into multiple files.
# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files

test_pages = Blueprint('test_pages', __name__, template_folder='templates')

# If this is true, this enables Cloudflare and gets the public IP with the `CF-Connecting-IP` header.
# If this is false, it just gets the public IP directly.
# Useful for debugging on the internal network.
cloudflare_ip_output = True

# Test page, replaced nodejs link with this on the flask server.
# @test_pages.route('/test')
# def test_page():
#     return render_template("test.html")
#
# @test_pages.route('/hello')
# def hello_page():
#     return render_template("hello.html")

# I'm not sure how to get the below working.
# @app.route("/test", methods=['GET'])
# def test_page():
#     return render_template("test.html")

if html_test_page_enabled:
    @test_pages.route("/test")
    def test_page():
         return render_template("test.html")

#-----------------
# Test pages
#-----------------

# TODO Move into here
# if passwordGenEnabled:
#     @test_pages.route("/password_gen")
#     def password_gen_page():
#         return render_template("password_gen.html", passwords=password_gen(20))


# TODO Possibly look into setting up API keys for certain endpoints.
# @app.before_request
# def check_authentication():
#     # Only check authentication for the specified endpoint
#     if request.endpoint == 'proxy_ip':
#         # Fetch the API key from request headers
#         api_key = request.headers.get('x-api-key')
#
#         # Check against the stored API key
#         if api_key != os.environ.get("IP_API_KEY"):
#             abort(403)  # Forbidden

# Switched to using Cloudflare headers.
# This can be toggled to show the IP address behind Cloudflare, or directly such as locally testing.
# TODO Make this support IPv6
# @test_pages.route('/proxy-ip')
# def proxy_ip():
#     if not cloudflare_ip_output:
#         """Proxy endpoint for IP address retrieval, this doesn't use Cloudflare."""
#
#         response = requests.get('https://api.ipify.org/?format=json')
#
#         return Response(response.content, mimetype='application/json')
#     else:
#         """Get the client's IP address."""
#         # Fetch the original IP address from Cloudflare headers
#         ip_address = request.headers.get('CF-Connecting-IP') or request.remote_addr
#
#         return {'ip': ip_address}
#

# TODO Test this later with IPv6
# This only displays the IPv6 IP, and not the IPv4 IP.
# TODO Fix this to display IPv4 and IPv6, if an IPv6 is available this will only get the IPv4 in the IPv6 slot.
@test_pages.route('/proxy-ip')
def proxy_ip():
    if not cloudflare_ip_output:
        """Proxy endpoint for IP address retrieval, this doesn't use Cloudflare."""

        # Fetch both IPv4 and IPv6
        ipv4_response = requests.get('https://api.ipify.org/?format=json')
        ipv6_response = requests.get('https://api64.ipify.org/?format=json')

        # Combine both IPs into a single response
        combined_response = {
            'ipv4': ipv4_response.json().get('ip'),
            'ipv6': ipv6_response.json().get('ip')
        }

        return Response(json.dumps(combined_response), mimetype='application/json')

    else:
        """Get the client's IP address from Cloudflare headers."""
        ipv4_address = request.headers.get('CF-Connecting-IP') or request.remote_addr
        ipv6_address = request.headers.get('X-Forwarded-For')  # Assuming this could contain IPv6

        # Handle cases where X-Forwarded-For may contain multiple IPs
        if ipv6_address and ',' in ipv6_address:
            ipv6_address = ipv6_address.split(',')[-1].strip()  # Get the last IP (most likely the client's)

        combined_response = {
            'ipv4': ipv4_address,  # Cloudflare usually provides the IPv4
            'ipv6': ipv6_address  # Use the appropriate header for IPv6 if available
        }

        return Response(json.dumps(combined_response), mimetype='application/json')


# This one isn't ready to be published yet
# @test_pages.route("/fivem_test")
# @cross_origin()
# def fivem_test_page():
#     return render_template("fivem-test.html")

#-----------------
# End test pages
#-----------------
