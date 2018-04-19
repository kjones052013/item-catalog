""" 
    Flask view functions for the web application.
"""


from catalog import app, db_session, csrf
from catalog.models import Category, Item, User
from catalog.forms import CategoryForm, ItemForm
from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask import session, abort, send_from_directory, make_response
from flask_wtf.file import FileField
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import exc
from werkzeug import secure_filename
from werkzeug.contrib.atom import AtomFeed
import httplib2
import json
import os
import random
import requests
import string


@app.route('/')
@app.route('/catalog/')
def catalog():
    """ Show catalog home page, with category list and latest items """
    categories = db_session.query(Category).all()
    items = db_session.query(Item).order_by(Item.pub_date.desc()).limit(10)
    return render_template('catalog.html',
                           categories=categories, latest_items=items)


@app.route('/catalog/json')
def catalogJSON():
    """ Return all catalog items in JSON format """
    categories = db_session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/catalog/recent.atom')
def catalogRecentAtom():
    """ Return latest items in Atom format """
    items = db_session.query(Item).order_by(Item.pub_date.desc()).limit(10)
    feed = AtomFeed('Recent Items', feed_url=request.url, url=request.url_root)
    for item in items:
        feed.add(item.name, unicode(item.description),
                 content_type='html',
                 author=item.user.name,
                 url=url_for('item', name=item.name),
                 updated=item.pub_date,
                 published=item.pub_date)
    return feed.get_response()


@app.route('/category/<name>/')
@app.route('/category/<name>/items')
def category(name):
    """ View a category of items """
    categories = db_session.query(Category).all()
    category = db_session.query(Category).filter_by(name=name).first()

    if category is None:
        abort(404)

    return render_template('category.html',
                           categories=categories,
                           category=category,
                           items=category.items)


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    """ Create new category """

    # user must be authenticated
    if 'user_id' not in session:
        return redirect('/login')

    form = CategoryForm()
    if form.validate_on_submit():

        # check that name != 'new', which is used for routing
        if form.name.data.lower() == 'new':
            form.name.errors.append("'new' is a reserved word, and cannot"
                                    " be used as a category name.")
            return render_template('new_category.html', form=form)

        category = Category(name=form.name.data, user_id=session['user_id'])
        db_session.add(category)
        try:
            db_session.commit()
        except exc.IntegrityError:
            # category name should be unique
            db_session.rollback()
            form.name.errors.append("Category already exists.")
            return render_template('new_category.html', form=form)

        flash("Created new category %s." % category.name)
        return redirect(url_for('catalog'))
    return render_template('new_category.html', form=form)


@app.route('/category/<name>/edit/', methods=['GET', 'POST'])
def editCategory(name):
    """ Edit a category """

    # user must be authenticated
    if 'user_id' not in session:
        return redirect('/login')

    category = db_session.query(Category).filter_by(name=name).first()

    if category is None:
        abort(404)

    if category.user_id != session['user_id']:
        abort(401)

    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        form.populate_obj(category)
        db_session.add(category)
        try:
            db_session.commit()
        except exc.IntegrityError:
            # category name should be unique
            db_session.rollback()
            form.name.errors.append("Category already exists.")
            return render_template('edit_category.html',
                                   category=category, form=form)
        flash("Category %s edited." % category.name)
        return redirect(url_for('category', name=category.name))
    return render_template('edit_category.html', category=category, form=form)


@app.route('/category/<name>/delete/', methods=['GET', 'POST'])
def deleteCategory(name):
    """ Delete a category """

    # user must be authenticated
    if 'user_id' not in session:
        return redirect('/login')

    category = db_session.query(Category).filter_by(name=name).first()

    if category is None:
        abort(404)

    if category.user_id != session['user_id']:
        abort(401)

    if request.method == 'POST':
        # delete the category
        # related items should be deleted automatically
        db_session.delete(category)
        db_session.commit()
        flash('%s Successfully Deleted' % category.name)
        return redirect(url_for('catalog'))
    else:
        form = CategoryForm()
        return render_template('delete_category.html',
                               category=category, form=form)


@app.route('/item/<name>')
def item(name):
    """ View an item """
    item = db_session.query(Item).filter_by(name=name).first()

    if item is None:
        abort(404)

    owner = db_session.query(User).filter_by(id=item.user_id).first()
    return render_template('item.html', item=item, owner=owner)


@app.route('/uploads/<path:filename>')
def uploads(filename):
    """ Return item image from uploads folder """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/item/new/', methods=['GET', 'POST'])
def newItem():
    """ Create a new item """

    # user must be authenticated
    if 'user_id' not in session:
        return redirect('/login')

    form = ItemForm()
    categories = db_session.query(Category.id, Category.name).all()
    form.category_id.choices = categories

    if form.validate_on_submit():
        # check that name != 'new', which is used for routing
        if form.name.data.lower() == 'new':
            form.name.errors.append("'new' is a reserved word, and cannot"
                                    " be used as an item name.")
            return render_template('new_item.html', form=form)

        filename = None
        # check if user uploaded file and sanitize filename
        if form.image.has_file():
            # get the filename, ensuring that it is safe
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(
                os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # create new item and commit to database
        item = Item(
            name=form.name.data,
            description=form.description.data,
            category_id=form.category_id.data,
            image=filename,
            user_id=session['user_id'],
            pub_date=datetime.utcnow()
            )
        db_session.add(item)
        try:
            db_session.commit()
        except exc.IntegrityError:
            # item name should be unique
            db_session.rollback()
            form.name.errors.append("Item already exists.")
            return render_template('new_item.html', form=form)
        flash("Created new item %s." % item.name)
        return redirect(url_for('item', name=item.name))
    return render_template('new_item.html', form=form)


@app.route('/item/<name>/edit/', methods=['GET', 'POST'])
def editItem(name):
    """ Edit an item """

    # user must be authenticated
    if 'user_id' not in session:
        return redirect('/login')

    item = db_session.query(Item).filter_by(name=name).first()

    if item is None:
        abort(404)

    if item.user_id != session['user_id']:
        abort(401)

    form = ItemForm(obj=item)
    categories = db_session.query(Category.id, Category.name).all()
    form.category_id.choices = categories

    if form.validate_on_submit():
        filename = item.image
        # check if user uploaded file and sanitize filename
        if form.image.has_file():
            # gets the filename, ensuring that it is safe
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(
                os.path.join(app.config['UPLOAD_FOLDER'], filename))

        form.populate_obj(item)
        item.image = filename
        db_session.add(item)
        try:
            db_session.commit()
        except exc.IntegrityError:
            # item name should be unique
            db_session.rollback()
            form.name.errors.append("Item already exists.")
            return render_template('edit_item.html', item=item, form=form)
        flash("Item %s edited." % item.name)
        return redirect(url_for('item', name=item.name))
    return render_template('edit_item.html', item=item, form=form)


@app.route('/item/<name>/delete/', methods=['GET', 'POST'])
def deleteItem(name):
    """ Delete an item """

    # user must be authenticated
    if 'user_id' not in session:
        return redirect('/login')

    item = db_session.query(Item).filter_by(name=name).first()

    if item is None:
        abort(404)

    if item.user_id != session['user_id']:
        abort(401)

    if request.method == 'POST':
        db_session.delete(item)
        db_session.commit()
        flash('%s Successfully Deleted' % item.name)
        return redirect(url_for('catalog'))
    else:
        form = ItemForm()
        return render_template('delete_item.html', item=item, form=form)


# AUTHENTICATION ###################################################


@app.route('/login')
def login():
    """ View login form """

    # create a state token to prevent request forgery
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    """ Logout of application """

    if 'provider' in session:
        if session['provider'] == 'google':
            gdisconnect()
            del session['gplus_id']
            del session['access_token']
        if session['provider'] == 'facebook':
            fbdisconnect()
            del session['facebook_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        del session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('catalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('catalog'))


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Google authentication and authorization """
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    secrets_file_path = os.path.join(app.config['APP_ROOT'],'google_client_secrets.json')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(secrets_file_path, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    client_id = json.loads(
        open(secrets_file_path, 'r').read())['web']['client_id']
    if result['issued_to'] != client_id:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                   json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    session['provider'] = 'google'

    user_id = getUserID(session['email'])
    if not user_id:
        # Create new user
        user_id = createUser(session)
    session['user_id'] = user_id

    output = ''
    output += '<h3>Welcome, '
    output += session['username']
    output += '!</h3>'
    output += '<img src="'
    output += session['picture']
    output += '" class="img-md img-circle" /> '
    flash("you are now logged in as %s" % session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """ Google disconnect """
    if 'access_token' not in session:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        response = make_response(json.dumps('Failed to revoke token for given'
                                            ' user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """ Facebook authentication and authorization """
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    secrets_file_path = os.path.join(app.config['APP_ROOT'],'fb_client_secrets.json')
    app_id = json.loads(open(secrets_file_path, 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(secrets_file_path, 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s' % (app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.5/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.5/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    session['access_token'] = stored_token

    # Get user picture
    url = ('https://graph.facebook.com/v2.5/me/picture?%s'
           '&redirect=0&height=200&width=200' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(session['email'])
    if not user_id:
        # Create new user
        user_id = createUser(session)
    session['user_id'] = user_id

    output = ''
    output += '<h3>Welcome, '
    output += session['username']
    output += '!</h3>'
    output += '<img src="'
    output += session['picture']
    output += '" class="img-md img-circle" /> '
    flash("Now logged in as %s" % session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """ Disconnect from Facebook """
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s'
           % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


def createUser(session):
    """ Create new user record """
    newUser = User(name=session['username'], email=session[
                   'email'], picture=session['picture'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserID(email):
    """ Get user by email address """
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
