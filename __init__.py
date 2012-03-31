import os
import polyspectra.config
from flask import Flask, g, session
from polyspectra.models import User
from polyspectra.database import db_session
from flaskext.bcrypt import Bcrypt

# application
app = Flask(__name__)
app.config.from_object(config)
bcrypt = Bcrypt(app)

from polyspectra.views import general, entry, category

MODULES = (
    general.mod,
    entry.mod,
    category.mod,
)

for module in MODULES:
    app.register_blueprint(module)
    
app.add_url_rule('/', view_func=entry.show)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter(User.id == session['user_id']).first()


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
