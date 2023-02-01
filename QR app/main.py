from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

from os.path import exists

import random

import pyqrcode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jesuisunebicorne'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

def generate(subject):
    if len(subject)!=0:
        myQr = pyqrcode.create(subject)
        return myQr
      
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        try:
            title = request.form['title']
            path = "static/audios/" + title
        except:
            files = request.files.getlist('file')
            for f in files:
                path = "static/audios/" + secure_filename(f.filename)
                while exists(path):
                    path = path.split(".")
                    path[0] += str(random.randint(0, 9))
                    path = ".".join(path)
                f.save(path)

        qr = generate(path)
        qr.png(path + "QR.png", scale=6)
        return render_template('index.html', image=path+"QR.png")


    return render_template('index.html')


if __name__ == "__main__":
    app.run(threaded=True, debug=False, host='0.0.0.0')