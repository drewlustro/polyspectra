import os
import polyspectra.config
from flask import Flask, g, session
from polyspectra.models import User
from polyspectra.database import db_session
from flaskext.bcrypt import Bcrypt
import bs4
from bs4 import BeautifulSoup

import re
from jinja2 import evalcontextfilter, Markup, escape
import pprint

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
    
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter('nl2pbr')
@evalcontextfilter
def nl2pbr(eval_ctx, value):
    
    # extract out pre code tags
    presoup = BeautifulSoup(value)    
    pres = presoup.find_all('pre')
    held_code = []
    for pretag in pres:
        codetag = presoup.new_tag("code")
        pretag.insert_after(codetag)
        held_code.append(pretag.extract())
    
    # replace new lines to <br />'s and <p></p>'s
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br />\n') \
        for p in _paragraph_re.split(str(presoup)))
    if eval_ctx.autoescape:
        pass
        #result = Markup(result)
    
    # inject unmodified <pre> tags back into the soup
    soup = BeautifulSoup(result)
    pre_containers = soup.find_all('code')
    i = 0;
    for pre in pre_containers:
        pre.replace_with(held_code[i])
        i += 1
        
    return str(soup)
    

