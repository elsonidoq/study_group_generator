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
    if email is not None:
        groups = load_groups()
        group = groups.get(email.lower().strip())
        failed = group is None
    else:
        group = None
        failed = False

    return render_template('index.html', group=group, failed=failed)

class Groups:
    def __init__(self):
        self.groups = None

    def __call__(self):
        if self.groups is None: 
            raw_groups = pkl.loads(encrypt.load_decrypted('groups.pkl.enc', os.environ['DECRYPT_KEY']))
            self.groups = {}
            for g in raw_groups:
                for m in g:
                    self.groups[m['Username'].lower().strip()] = g

        return self.groups

def _row(content, is_header):
    elem = 'th' if is_header else 'td'
    content = ' '.join(f'<{elem}>{c}</{elem}>' for c in content)
    return f'<tr>{content}</tr>'

def format_group(group):
    keys = 'Username coding_skills ml_skills'.split()

    lines = [_row(keys, True)]
    for doc in group:
        lines.append(_row([doc[k] for k in keys], False))

    return '<table>' + '\n'.join(lines) + '</table>'

load_groups = Groups()

if __name__ == '__main__':
    app.run()
