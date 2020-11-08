import os
import pickle as pkl
from flask import render_template
from flask import Flask, jsonify
from flask import request
import encrypt

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET', 'POST'])
def index():
    email = request.form.get('email')
    response = ''
    if email is not None:
        groups = load_groups()
        group = groups.get(email.lower().strip())
        if group is None:
            response = 'No encontre tu mail, si te habias registrado escribime'
        else:
            response = 'Tu grupo es: ' + ', '.join(group)

    return render_template('index.html', response=response)

class Groups:
    def __init__(self):
        self.groups = None

    def __call__(self):
        if self.groups is None: 
            raw_groups = pkl.loads(encrypt.load_decrypted('groups.pkl.enc', os.environ['DECRYPT_KEY']))
            self.groups = {}
            for g in raw_groups:
                for m in g:
                    self.groups[m.lower().strip()] = g

        return self.groups

load_groups = Groups()

if __name__ == '__main__':
    app.run()
