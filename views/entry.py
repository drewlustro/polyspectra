from datetime import datetime
from polyspectra.models import User, Entry, EntryType, Category
from polyspectra.wrappers import auth_required

from flask import Blueprint, render_template, flash, redirect, \
                    url_for, request, g

mod = Blueprint('entry', __name__, url_prefix='/entry')

@mod.route('/')
def show():
    categories = Category.query.order_by(Category.name.asc()).all()
    entries = Entry.query.filter(Entry.published == True).order_by(Entry.date.desc()).limit(10)
    return render_template('entry/show.html', entries=entries, 
                        categories=categories)
                        
@mod.route('/<string:slug>')
def single(slug):
    entry = Entry.query.filter(Entry.slug == slug and
                                Entry.published == True).first()
    if not entry:
        flash('Entry not found.')
        return redirect(url_for('.show'))
        
    return render_template('entry/single.html', entry=entry)
                        
@mod.route('/category/<int:category_id>')
def show_by_category(category_id):
    if category_id == -1:
        return redirect(url_for('.show'))
    else:
        categories = Category.query.order_by(Category.name.asc()).all()
        category = Category.query.filter(Category.id == category_id).first()
        entries = Entry.query.filter(Entry.published == True and 
                                Entry.category_id == category_id).order_by(Entry.date.desc()).limit(10)
        return render_template('entry/show.html', entries=entries, 
                            categories=categories, category=category)
                            
@mod.route('/preview', methods=['POST'])
def preview():
    entry = Entry(request.form['user_id'], title=request.form['title'],
                    text=request.form['text'], category_id=request.form['category_id'])
    print entry
    if not entry:
        flash('Could not create entry preview.')
        return redirect(url_for('.manage'))
    return render_template('entry/single.html', entry=entry)


@mod.route('/write', methods=['GET','POST'])
@auth_required
def write():
    """Allows logged in user to author a new blog entry."""
    
    entry_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if request.method == 'POST':
        user_id = g.user.id
        new_entry = Entry(user_id, title=request.form['title'], 
                        text=request.form['text'], category_id=request.form['category_id'],
                        entry_type=request.form['entry_type'], type_meta=request.form['type_meta'])
        try:
            if request.form['published']:
                new_entry.publish()
        except KeyError:
            new_entry.published = False
            
        if new_entry.create():
            flash('New entry successfully posted')
        else:
            flash('Failed to create new entry')
        return redirect(url_for('.show'))
    
    entry = {'date': entry_date}
    categories = Category.query.all()
    users = User.query.order_by(User.name.desc()).all()
    entry_types = EntryType.all()
    return render_template('entry/write.html', entry=entry, 
                            categories=categories, users=users,
                            entry_types=entry_types)


@mod.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@auth_required
def edit(entry_id):
    if request.method == 'POST':
        entry = Entry.query.filter(Entry.id == request.form['entry_id']).first()
        if not entry:
            flash('Entry not found, so cannot edit.')
            redirect(url_for('.manage'))
        entry.user_id = g.user.id
        entry.title = request.form['title']
        entry.text = request.form['text']
        entry.category_id = request.form['category_id']
        entry.user_id = request.form['user_id']
        entry.entry_type = request.form['entry_type']
        entry.type_meta = request.form['type_meta']
        
        try:
            if request.form['published']:
                entry.publish()
        except KeyError:
            entry.published = False
            
        if entry.save():
            flash('Entry successfully updated')
        else:
            flash('There was an error trying to update that entry.')

        return redirect(url_for('.manage'))    
    
    categories = Category.query.all()
    entry = Entry.query.filter(Entry.id == entry_id).first()
    users = User.query.order_by(User.name.desc()).all()
    entry_types = EntryType.all()
    if not Entry:
        flash('Entry not found, so cannot edit.')
        redirect(url_for('.manage'))

    return render_template('entry/edit.html', entry=entry,
                            categories=categories, users=users,
                            entry_types=entry_types)

# Delete Entry
@mod.route('/delete/<int:entry_id>', methods=['GET'])
@auth_required
def delete(entry_id):
    if entry_id:
        entry = Entry.query.filter(Entry.id == entry_id).first()
        entry.delete()
        flash('Entry %i deleted.' % entry_id)
    else:
        flash('No entry specified')
    return redirect(url_for('.manage'))
    
@mod.route('/manage')
@auth_required
def manage():
    """Allows the administrator to edit blog entries"""
    entries = Entry.query.order_by(Entry.date.desc()).all()
    return render_template('entry/manage.html', entries=entries)

