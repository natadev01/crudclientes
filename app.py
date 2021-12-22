from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Client, Address
from forms import ClientForm, AddressForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('clients'))


@app.route("/new_client", methods=('GET', 'POST'))
def new_client():
    '''
    Create new client
    '''
    form = ClientForm()
    if form.validate_on_submit():
        if form.addAddress.data:  
            form.addresses.append_entry()
            return render_template('web/new_client.html', form=form)
        my_client = Client()
        my_client.name = form.name.data
        my_client.lastName = form.lastName.data
        my_client.email = form.email.data
        my_client.phone = form.phone.data
        db.session.add(my_client)

        try:
            db.session.commit()
            for address in form.addresses.data:
                my_address= Address()
                my_address.address = address
                my_address.client_id = my_client.id
                db.session.add(my_address)
            db.session.commit()

            flash('Client created correctly', 'success')
            return redirect(url_for('clients'))
        except:
            db.session.rollback()
            flash('Error generating client.', 'danger')

    return render_template('web/new_client.html', form=form)


@app.route("/edit_client/<id>", methods=('GET', 'POST'))
def edit_client(id):
    '''
    Edit client

    :param id: Id from client
    '''
    my_client = Client.query.filter_by(id=id).first()
    form = ClientForm(obj=my_client)
    if form.validate_on_submit():
        if form.addAddress.data:  
            form.addresses.append_entry()
            return render_template('web/edit_client.html', form=form)
        try:
            # Update client
            my_client.name = form.name.data
            my_client.lastName = form.lastName.data
            my_client.email = form.email.data
            my_client.phone = form.phone.data
            db.session.add(my_client)
            db.session.commit()
            for address in form.addresses.data:
                my_address= Address()
                my_address.address = address
                my_address.client_id = my_client.id
                db.session.add(my_address)
            db.session.commit()

            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update client.', 'danger')
    return render_template(
        'web/edit_client.html',
        form=form)


@app.route("/clients")
def clients():
    '''
    Show alls clients
    '''
    clients = Client.query.order_by(Client.name).all()
    return render_template('web/clients.html', clients=clients)


@app.route("/search")
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_clients = Client.query.filter(
        Client.name.contains(name_search)
        ).order_by(Client.name).all()
    return render_template('web/clients.html', clients=all_clients)


@app.route("/clients/delete", methods=('POST',))
def clients_delete():
    '''
    Delete client
    '''
    try:
        my_client = Client.query.filter_by(id=request.form['id']).first()
        addresses = Address.query.filter_by(client_id=my_client.id).all()
        db.session.delete(my_client)
        for address in addresses:
            db.session.delete(address)
        db.session.commit()
        flash('Delete successfully.', 'danger')

    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('clients'))


if __name__ == "__main__":
    app.run(host="127.0.0.1",debug=True)
