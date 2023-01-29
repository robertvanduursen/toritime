"""
(Extract, transform, load)
https://www.ibm.com/cloud/learn/etl
https://en.wikipedia.org/wiki/Extract,_transform,_load
"""

from flask import jsonify, make_response, send_from_directory
import flask
import json
import os
from flask import Flask, flash, request, redirect, url_for, render_template, Blueprint
from werkzeug.utils import secure_filename
from exceptions import IntentionCacheMissError

app = Flask(__name__)
app.secret_key = b'trololololol'
import socket

LOCAL = os.path.dirname(__file__)
# site = Blueprint('site', __name__, template_folder='templates')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
addr = s.getsockname()[0]
print(f"this machines addr = {addr}")
s.close()

IPS = {
    '178.226.121.239': 'mobile_ext',
    '192.168.2.2': 'mobile-at_home',
    addr: 'myself'
}


def whitelist(req):
    ip = req.remote_addr
    if ip not in IPS.keys():
        raise Exception(f'You shall not pass! Address: {ip} is not allowed')
    return


@app.route('/')
def index():
    whitelist(request)
    rules = app.url_map.iter_rules()
    listing = "</br>".join([f"<a href={x}>{x}</a>" for x in rules])
    return f'''
    <!doctype html>
    <title>Home</title>
    <h1>Upload new File</h1>
    {listing}
    </form>
    '''


# @app.route('/statusurl', methods=['GET', 'POST'])
# def statusurl():
#     whitelist(request)
#     if request.method == 'POST':
#         print("fake_filedownload got posted on")
#     if request.method == 'GET':
#         print('hier is de file')
#
#     data = {
#         "status": "Extracted",
#         "trackingId": "123e4567-e89b-12d3-a456-426614174003"
#     }
#     r = make_response((json.dumps(data),
#                        200,
#                        {'Content-Type': 'application/json',
#                         'Location': 'http://127.0.0.2:9084/fake_filedownload'}))
#     return r


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    whitelist(request)
    send_from_directory(app.config['UPLOAD_FOLDER'],
                        filename, as_attachment=True)
    return f'thank you for uploading {filename}'


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'download')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/tori_voedings_moment', methods=['GET', 'POST'])
def tori_voedings_moment():
    if request.method == 'POST':
        # this is the pathway a HTML Form Submit Action takes!
        pass
        # return "opening"
    from datetime import datetime, timedelta
    # https://strftime.org/
    zo_laat = datetime.now().strftime("%H:%M:%S")

    # detla of 3h 30m
    delta = datetime.now() + timedelta(hours=3, minutes=30)
    vorige = datetime.now() - timedelta(hours=3, minutes=30)

    volgende = delta.strftime("%H:%M")
    vorige = vorige.strftime("%H:%M")
    return f'''
    <!doctype html>
    <title>voeding!</title>
    <h1>Tori's voedingmoment</h1>
    <h1>tis nu {zo_laat}</h1>
    <h1>volgende voeding is om: {volgende}</h1>
    </br>
    <h1>de vorige was om: {vorige}</h1>
    <form method=post enctype=multipart/form-data>
      <input type=submit value='volgende'>
    </form>
    '''


@app.route('/search', methods=['GET', 'POST'])
def search():
    """ how to make a responsive text field, that lists auto-completes? """
    # query
    # https://medium.com/analytics-vidhya/build-a-flask-web-app-by-scraping-a-website-display-the-data-using-chart-js-bd0c97397967
    # https://stackoverflow.com/questions/22056468/dynamic-popover-tooltip-via-bootstrap-with-flask-python

    ''''
    <input data-v-cf3f6be6="" placeholder="Search the web to plant trees..." aria-label="Search Form" type="search"
    name="q" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" autofocus="autofocus" required="required"
    data-test-id="search-form-input" class="search-form__input">
    '''
    # return render_template('search.html'), 404
    print(request.values)
    extra = ''

    with open(os.path.join(LOCAL, r"../../blueprints/site/templates/site/search.html"), 'r') as search_page:
        data = search_page.read()
        projects = os.listdir(r"G:/")
        listing = ", ".join([f'"{x}"' for x in projects])
        data = data.replace("var countries = [];", f"var countries = [{listing}];")
        return data + extra


@app.route('/os_map')
def os_map():
    whitelist(request)
    folder = os.path.dirname(__file__)
    info = os.listdir(os.path.dirname(__file__))
    return "</br>".join(info + [folder])


@app.errorhandler(404)
def page_not_found(error):
    # render_template('404.html'), 404
    return f"Couldnt find {request.url} -> {IntentionCacheMissError()}"


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    print('running')
    app.run(host=addr, port=6547)
    # https://flask.palletsprojects.com/en/2.0.x/server/
