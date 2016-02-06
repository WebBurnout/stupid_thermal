from flask import Flask, request
from flask import render_template
from twilio import twiml
import requests

from image_to_ascii import handle_image_conversion

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/web-print', methods=['POST'])
def web_print():
    print request.form

    # with open('/dev/tty.thermal-4tBluetooth', 'w') as f:
    #     f.write(ascii_art)

    return 'gooooood work'


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
    else:
        response.message("Face forward and text me a selfie!")

    with open('/dev/tty.thermal-4tBluetooth', 'w') as f:
        f.write(ascii_art)

    return str(response)

app.run(host='0.0.0.0', debug=True)
