import datetime
import os

from flask import Flask, render_template, redirect, url_for, request
from forms import ItemForm
from models import Items
from database import db_session


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/", methods=["GET", "POST"])
def add_item():
    form = ItemForm(request.form)
    if request.method=="POST" and form.validate_on_submit():
        try:
            item = Items(
                name=form.name.data,
                quantity=form.quantity.data,
                description=form.description.data,
                date_added=datetime.datetime.now())
            db_session.add(item)
            db_session.commit()
            return redirect(url_for('success'))
        except:
            return 'There was a problem adding an item'
    return render_template('index.html', form=form)


@app.route("/success")
def success():
    results = []
    qry = db_session.query(Items)
    results = qry.all()
    return render_template('show_items.html', items=results)


@app.route("/delete/<int:id>")
def delete(id):
    item = db_session.query(Items).filter_by(id=id).first()
    try:
        db_session.delete(item)
        db_session.commit()
        return redirect(url_for('success'))
    except:
        return 'There was a problem deleting an item'


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    item = db_session.query(Items).filter_by(id=id).first()
    if item:
        form = ItemForm(request.form)
        if request.method=="POST" and form.validate_on_submit():
            try:
                item.name = form.name.data,
                item.quantity = form.quantity.data,
                item.description = form.description.data,
                item.date_added = datetime.datetime.now(),
                db_session.commit()
                return redirect(url_for('success'))
            except:
                return 'There was an issue updating your item'
        return render_template('update.html',id=id, form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
