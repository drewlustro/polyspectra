import os
from flask import Flask, request, session, g, redirect, url_for, \
            render_template, flash, send_from_directory, Blueprint
from polyspectra import app
from polyspectra import bcrypt
from polyspectra.models import User
from polyspectra.wrappers import auth_required

mod = Blueprint('general', __name__)

@mod.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        checked_user = User.query.filter(User.username == request.form['username']).first()
        print checked_user
        print 'pass is %r' % (checked_user.password,)
        print 'test pass encrypted is %r' % bcrypt.generate_password_hash(request.form['password'])
        if bcrypt.check_password_hash(checked_user.password, request.form['password']):
            print 'hash ok'
        else:
            print 'hash failed'
         # returns True
        if checked_user == None or not bcrypt.check_password_hash(checked_user.password, request.form['password']):
            error = 'Invalid Password'
        else:
            session['user_id'] = checked_user.id
            flash('You were logged in, user %r' % checked_user.name)
            return redirect(url_for('entry.manage'))
    return render_template('general/login.html', error=error)

@mod.route('/logout')
@auth_required
def logout():
    session.pop('user_id', None)
    g.user = None
    flash('You were logged out.')
    return redirect(url_for('entry.show'))

@mod.route('/img/<name>.<ext>')
def img(name, ext):
    mimetype = "image/png"
    if ext == "jpg" or ext == "jpeg":
        mimetype = "image/jpeg"
    elif ext == "gif":
        mimetype = "image/gif"
    
    return send_from_directory(os.path.join(app.root_path, 'img'),
            name + '.' + ext, mimetype=mimetype)
