from flask import Flask, request
from twilio import twiml
import requests

from image_to_ascii import handle_image_conversion

app = Flask(__name__)


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
