#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
import pyscreenshot as ImageGrab
from io import BytesIO

app = flask.Flask(__name__)

def gen():
    while True:
        img_buffer = BytesIO()

        # Set childprocess False to improve performance, but then conflicts are possible.
        #ImageGrab.grab(backend='mss', childprocess=True).save(img_buffer, 'PNG', quality=50)
        ImageGrab.grab(backend='mss', childprocess=False).save(img_buffer, 'JPEG', quality=70)
        
        #yield (b'--frame\r\n'
        #       b'Content-Type: image/png\r\n\r\n' + img_buffer.getvalue() + b'\r\n\r\n')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_buffer.getvalue() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return flask.Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
