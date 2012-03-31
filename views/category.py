from datetime import datetime
from polyspectra.models import Entry, Category
from polyspectra.wrappers import auth_required

from flask import Blueprint, render_template, flash, redirect, \
                    url_for, request, g

mod = Blueprint('category', __name__, url_prefix='/category')

@mod.route('/')
@auth_required
def manage():
    categories = Category.query.order_by(Category.order.asc()).all()
    # categories.insert(0, Category.uncategorized())
    return render_template('category/manage.html', categories=categories)

@mod.route('/new', methods=['GET','POST'])
@auth_required
def new():
    if request.method == 'POST':
        newcat = Category(request.form['name'], request.form['order'])
        newcat.create()
        flash('Category "%s" created.' % newcat.name)
        return redirect(url_for('.manage'))
    return render_template('category/new.html', category=None)
        

@mod.route('/edit', methods=['POST'])
@mod.route('/edit/<int:category_id>', methods=['GET'])
@auth_required
def edit(category_id = 0):
    category_id = request.form['category_id'] if request.method == 'POST' else category_id
    category = Category.query.filter(Category.id == category_id).first()
    if category is None:
        flash('Error. Category not found.')
        return redirect(url_for('.manage'))
    
    if request.method == 'GET':
        return render_template('category/edit.html', category=category)
    else:
        category.name = request.form['name'].strip()
        category.order = request.form['order'] if request.form['order'].isdigit() \
                        else 0
        category.save()
        flash('Category updated.')
        return redirect(url_for('.manage'))
        
@mod.route('/delete/<int:category_id>')
@auth_required
def delete(category_id):
    category = Category.query.filter(Category.id == category_id).first()
    if category is None:
        flash('Error. Category not found.')
        return redirect(url_for('.manage'))
    elif len(category.entries) > 0:
        flash('You cannot delete a category that has entries in it.')
        return redirect(url_for('.manage'))
    flash('Deleted category %s', category.name)
    category.delete()
    return redirect(url_for('.manage'))

