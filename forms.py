from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, SubmitField
import wtforms
from wtforms.validators import DataRequired, Email, Length



class AddressForm(FlaskForm):
    address = StringField('Address', validators=[Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    addresses = FieldList(StringField('Address'), min_entries=1)

    # address = FieldList(StringField('Address'), min_entries=1)

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=80, message='You cannot have more than 80 characters')])
    lastName = StringField('Last Name', validators=[Length(min=-1, max=100, message='You cannot have more than 100 characters')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    phone = StringField('Phone', validators=[Length(min=-1, max=20, message='You cannot have more than 20 characters')])
    # addresses = FieldList(FormField(AddressForm), min_entries=1)
    addresses = FieldList(StringField('Address'), min_entries=1)
    addAddress = SubmitField('Add Address') # 
    save = SubmitField('Save') # 
    # addresses2 = wtforms.FormField(AddressForm)
