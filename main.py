# flask
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_jsglue import JSGlue
# WTForms
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Optional, IPAddress
# SMB
from smb.SMBConnection import SMBConnection
# local import
from find import find_ip_name
# standard library
from ast import literal_eval


# Initialize application
app = Flask(__name__)
Bootstrap(app)
jsglue = JSGlue(app)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'xxxxxyyyyyzzzzz'
app.jinja_env.add_extension('jinja2.ext.do')

# debug settings
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('index.html')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


class InputNetworkForm(FlaskForm):
    name = StringField('Computer Name')
    ip = StringField('Computer IP', validators=[IPAddress(message='Not a valid IP.')])
    submit = SubmitField('Submit')


@app.route('/add_network', methods=['GET', 'POST'])
def add_network():
    networks = find_ip_name()
    return jsonify(dict(networks))
    

@app.route('/input-network', methods=['GET', 'POST'])
def input_network():
    
    form = InputNetworkForm()
    
    if form.validate_on_submit():
        name = form.name.data
        ip = form.ip.data
        return redirect(url_for('smb_search', path=name, ip=ip))    
    return render_template('input-network.html', form=form)

@app.route('/find-network', methods=['GET', 'POST'])
def find_network():
    if request.method == 'POST':
        name_ip = literal_eval(request.form['name_ip'])
        ip, name = name_ip['ip'], name_ip['network']
        return redirect(url_for('smb_search', path=name, ip=ip))    
    return render_template('find-network.html')


@app.route('/media/<string:ip>/<path:path>', methods=['POST', 'GET'])
def smb_search(ip, path):
    json_data = {'PATH':path,'IP':ip,'FILE':''}
    media = []
    root_media = []
    
    split_path = path.split('/')
    conn = SMBConnection('', '', 'smbConn', split_path[:1][0].encode('UTF-8'))
    conn.connect(ip, 139)  

    if len(split_path) <= 1:
        shares = conn.listShares()
        for share in shares:
            if not share.isSpecial and share.name != 'print$':
                root_media.append(share)
        return render_template('media.html', root_media=root_media, json_data=json_data)

    elif len(split_path) <= 2:
        shares = conn.listPath(split_path[1:][0], '')
        for share in shares:
            if share.filename not in ['.', '..']:
                media.append(share)
        return render_template('media.html', media=media, json_data=json_data)

    else:
        second_part = ''
        for val in split_path[2:]:
            second_part += '/' + val
        shares = conn.listPath(split_path[1:][0], second_part)
        for share in shares:
            if share.filename not in ['.', '..']:
                media.append(share)
        return render_template('media.html', media=media, json_data=json_data)


@app.route('/play-video', methods=['POST', 'GET'])
def play_video():
    if request.method == 'POST':
        path = request.json['PATH']+'/'+request.json['FILE']
        path = 'smb://' + path
        print(path.encode('UTF-8'))
    return jsonify(path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
