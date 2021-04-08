import wtforms
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, AnyOf

from models import User


class VendorForm(FlaskForm):
    values = ('beauty', 'fitness')
    email = wtforms.StringField('Email', [DataRequired(), Email()])
    name = wtforms.StringField('Name', [DataRequired()])

    business_name = wtforms.StringField('Name', [DataRequired()])
    city = wtforms.StringField('Name', [DataRequired()])
    address = wtforms.StringField('Name', [DataRequired()])
    pin = wtforms.StringField('Name', [DataRequired()])
    gstin = wtforms.StringField('Name')
    pan = wtforms.StringField('Name')
    mobile_number = wtforms.StringField('Name', [DataRequired()])
    category = wtforms.StringField('Name', [AnyOf(values), DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = wtforms.StringField('Email', [DataRequired()])
    password = wtforms.PasswordField('Password', [DataRequired()])


class ServiceFormBeauty(FlaskForm):
    days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',)
    description = wtforms.StringField()
    # Features
    wifi = wtforms.BooleanField('Agree?')
    music = wtforms.BooleanField('Agree?')
    ac = wtforms.BooleanField('Agree?')
    disinfect = wtforms.BooleanField('Agree?')
    parking = wtforms.BooleanField('Agree?')
    organic = wtforms.BooleanField('Agree?')
    # Products
    loreal = wtforms.BooleanField('Agree?')
    garnier = wtforms.BooleanField('Agree?')
    streaks = wtforms.BooleanField('Agree?')
    tresemme = wtforms.BooleanField('Agree?')
    walla = wtforms.BooleanField('Agree?')
    wahl = wtforms.BooleanField('Agree?')
    mac = wtforms.BooleanField('Agree?')
    mableme = wtforms.BooleanField('Agree?')
    faces = wtforms.BooleanField('Agree?')
    colorbar = wtforms.BooleanField('Agree?')
    revlon = wtforms.BooleanField('Agree?')
    shehnaaz = wtforms.BooleanField('Agree?')
    # Review
    ambience = wtforms.BooleanField('Agree?')
    hygiene = wtforms.BooleanField('Agree?')
    service = wtforms.BooleanField('Agree?')
    staff = wtforms.BooleanField('Agree?')
    # Timings
    open_time = wtforms.TimeField(format='%H:%M')
    close_time = wtforms.TimeField(format='%H:%M')
    day_from = wtforms.StringField([AnyOf(days)])
    day_to = wtforms.StringField([AnyOf(days)])


class ServiceFormFitness(FlaskForm):
    days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',)
    description = wtforms.StringField()
    # Features
    wifi = wtforms.BooleanField('Agree?')
    music = wtforms.BooleanField('Agree?')
    ac = wtforms.BooleanField('Agree?')
    disinfect = wtforms.BooleanField('Agree?')
    parking = wtforms.BooleanField('Agree?')
    safety = wtforms.BooleanField('Agree?')
    # Products
    loreal = wtforms.BooleanField('Agree?')
    garnier = wtforms.BooleanField('Agree?')
    streaks = wtforms.BooleanField('Agree?')
    tresemme = wtforms.BooleanField('Agree?')
    walla = wtforms.BooleanField('Agree?')
    wahl = wtforms.BooleanField('Agree?')
    mac = wtforms.BooleanField('Agree?')
    mableme = wtforms.BooleanField('Agree?')
    faces = wtforms.BooleanField('Agree?')
    colorbar = wtforms.BooleanField('Agree?')
    revlon = wtforms.BooleanField('Agree?')
    shehnaaz = wtforms.BooleanField('Agree?')
    # Review
    ambience = wtforms.BooleanField('Agree?')
    hygiene = wtforms.BooleanField('Agree?')
    facilities = wtforms.BooleanField('Agree?')
    equipments = wtforms.BooleanField('Agree?')
    trainer = wtforms.BooleanField('Agree?')
    # Timings
    open_time = wtforms.TimeField(format='%H:%M')
    close_time = wtforms.TimeField(format='%H:%M')
    day_from = wtforms.StringField([AnyOf(days)])
    day_to = wtforms.StringField([AnyOf(days)])


class DescriptionForm(FlaskForm):
    values = ('beauty', 'fitness')
    partner = ('standard', 'exclusive')
    business_name = wtforms.StringField('Name', [DataRequired()])

    address = wtforms.StringField('Name', [DataRequired()])
    locality = wtforms.StringField('Name', [DataRequired()])
    city = wtforms.StringField('Name', [DataRequired()])
    pin = wtforms.StringField('Name', [DataRequired()])
    lat = wtforms.StringField('Name')
    lng = wtforms.StringField('Name')
    place_id = wtforms.StringField('Name')

    gstin = wtforms.StringField('Name')
    license_number = wtforms.StringField('Name')
    pan = wtforms.StringField('Name')
    business_id = wtforms.FileField('File')
    owner_name = wtforms.StringField('Name', [DataRequired()])
    manager_name = wtforms.StringField('Name', [DataRequired()])
    mobile_number = wtforms.StringField('Name', [DataRequired()])
    mobile_number_manager = wtforms.StringField('Name', [DataRequired()])
    partnership = wtforms.StringField('Name', [AnyOf(partner), DataRequired()])
    category = wtforms.StringField('Name', [AnyOf(values), DataRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = wtforms.PasswordField('Password')
    password = wtforms.PasswordField('Password', [DataRequired()])
    confirm = wtforms.PasswordField('Password', [DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_old_password(self, password):
        if not current_user.check_password(password.data):
            raise ValidationError('Incorrect Password!!')


class AdminBookingForm(FlaskForm):
    values = ('cash', 'online', 'pending', 'failed')
    customer_name = wtforms.StringField('Name', [DataRequired()])
    customer_email = wtforms.StringField('Name', [DataRequired(), Email()])
    mobile_number = wtforms.StringField('Name', [DataRequired()])
    payment_mode = wtforms.StringField('Name', [DataRequired(), AnyOf(values)])
    amount = wtforms.StringField('Name', [DataRequired()])
    paid = wtforms.BooleanField()
    services = wtforms.StringField('Name', [DataRequired()])
    booking_at = wtforms.DateTimeField(format='%H:%M %m/%d/%Y')


class ServiceForm(FlaskForm):
    category = wtforms.StringField('Name', [DataRequired()])
    subcategory = wtforms.StringField('Name')
    service = wtforms.StringField('Name', [DataRequired()])
    prices = wtforms.FloatField('Name', [DataRequired()])


class AdminVendorUpdateForm(FlaskForm):
    business_name = wtforms.StringField('Business Name')
    city = wtforms.StringField('City')
    locality = wtforms.StringField('Locality')
    address = wtforms.StringField('Address')
    pin = wtforms.StringField('PIN')
    lat = wtforms.StringField('Lat')
    lng = wtforms.StringField('Long')
    place_id = wtforms.StringField('Place ID')
    gstin = wtforms.StringField('GSTIN')
    pan = wtforms.StringField('PAN')
    mobile_number = wtforms.StringField('Mobile Number')
    manager_name = wtforms.StringField('Manager Name')
    mobile_number_manager = wtforms.StringField('Manager Mobile Number')
    license_number = wtforms.StringField('Licence Number')
    business_id = wtforms.StringField('Business ID')
    description = wtforms.TextAreaField('Description')
    business_type = wtforms.StringField('Business Type')
    open_time = wtforms.TimeField('Open Time')
    close_time = wtforms.TimeField('Close Time')
    day_from = wtforms.StringField('Day From')
    day_to = wtforms.StringField('Day to')
    otp_verified = wtforms.BooleanField('OTP Verified')
