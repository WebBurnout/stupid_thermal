from flask import Flask, request
from flask import render_template
from twilio import twiml
import requests

from image_to_ascii import handle_image_conversion

import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/omar/code/stupid_thermal/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/web-print', methods=['POST'])
def web_print():

    label_font = 'w&'
    data_font = '!0w$'

    output = label_font + "Name or Identifying Marks:\n"
    output += data_font + request.form['name'] + "\n"

    output += label_font + "Identity Theft with SSN:\n"
    output += data_font + request.form['ssn'] + "\n"

    output += label_font + "Stalk at:\n"
    output += data_font + request.form['location'] + "\n"

    output += label_font + "Message:\n"
    output += data_font + request.form['message'] + "\n"

    print output

    if request.files:
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            ascii_art = handle_image_conversion('{}'.format(path))
            print ascii_art

    with open('/dev/tty.thermal-4tBluetooth', 'w') as f:
        f.write(output)
        f.write(ascii_art)

    return 'ok'


@app.route('/print', methods=['POST'])
def print_message():
    response = twiml.Response()

    response.message("Please wait for launch 3, 2, 1...")

    if request.form['NumMedia'] != '0':
        filename = request.form['MessageSid'] + '.jpg'
        f = open(filename, 'wb')
        f.write(requests.get(request.form['MediaUrl0']).content)
        f.close()
        ascii_art = handle_image_conversion('{}'.format(filename))
        print ascii_art
    else:
        response.message("Face forward and text me a selfie!")

    with open('/dev/tty.thermal-4tBluetooth', 'w') as f:
        f.write(ascii_art)

    return str(response)

app.run(host='0.0.0.0', debug=True)
