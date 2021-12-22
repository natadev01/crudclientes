from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Client(db.Model):


    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    addresses = db.relationship('Address', backref='clients', lazy='dynamic')

    def __repr__(self):
        # return '<Clients %r>' % self.name
        return "< % s, % s, % s, % s, % s, % s >" % (self.id,self.name,self.lastName,self.email, self.phone, self.addresses) 


class Address(db.Model):

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    def __repr__(self):
        return '%s' % self.address