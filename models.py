import datetime

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from config import db, login_manager
from utils import Image


class User(UserMixin, db.Model):
    id = db.Column('user', db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password = db.Column(db.String(255))
    mobile_number = db.Column(db.String(64))
    business_client = db.relationship("business_client", uselist=False, back_populates="user")
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship('Cart')
    booking = db.relationship("Booking")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class business_client(db.Model, Image):
    id = db.Column('client_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User", back_populates="business_client")
    # Data
    business_name = db.Column(db.String(100))
    # Location
    city = db.Column(db.String(50))
    locality = db.Column(db.String(255))
    address = db.Column(db.String(512))
    pin = db.Column(db.String(24))
    lat = db.Column(db.String(24))
    lng = db.Column(db.String(24))
    place_id = db.Column(db.String(64))

    gstin = db.Column(db.String(64))
    pan = db.Column(db.String(64))
    mobile_number = db.Column(db.String(64))
    manager_name = db.Column(db.String(255))
    mobile_number_manager = db.Column(db.String(64))
    status = db.Column(db.String(10))
    category = db.Column(db.String(10), default='beauty')
    license_number = db.Column(db.String(255))
    business_id = db.Column(db.String(255))
    description = db.Column(db.Text)
    partnership = db.Column(db.String(20), default='standard')
    business_type = db.Column(db.String(20))
    # Images
    service_image = db.relationship('ServiceImage')
    centre_image = db.relationship('CentreImage')
    ambience_image = db.relationship('AmbienceImage')
    staff_image = db.relationship('StaffImage')
    equipments_image = db.relationship('EquipmentsImage')
    # Relations
    services = db.relationship("Services")
    feature = db.relationship("Features", uselist=False)
    review = db.relationship("Review", uselist=False)
    products = db.relationship("Products", uselist=False)
    bookings = db.relationship('Booking')
    # Condition
    updated = db.Column(db.Boolean, default=False)
    # Availability
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)
    day_from = db.Column(db.String(20))
    day_to = db.Column(db.String(20))
    # OTP
    otp = db.Column(db.String(20))
    otp_verified = db.Column(db.Boolean, default=False)

    def image_meta(self):
        self.save_to = 'business_id'
        self.image_field = 'business_id'


class ServiceImage(db.Model, Image):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    image = db.Column(db.String(255))

    def image_meta(self):
        self.save_to = 'service'
        self.image_field = 'image'


class CentreImage(db.Model, Image):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    image = db.Column(db.String(255))

    def image_meta(self):
        self.save_to = 'center'
        self.image_field = 'image'


class AmbienceImage(db.Model, Image):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    image = db.Column(db.String(255))

    def image_meta(self):
        self.save_to = 'ambience'
        self.image_field = 'image'


class StaffImage(db.Model, Image):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    image = db.Column(db.String(255))

    def image_meta(self):
        self.save_to = 'staff'
        self.image_field = 'image'


class EquipmentsImage(db.Model, Image):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    image = db.Column(db.String(255))

    def image_meta(self):
        self.save_to = 'equipments'
        self.image_field = 'image'


class Services(db.Model):
    id = db.Column('service_id', db.Integer, primary_key=True)
    gender = db.Column(db.String(64))
    category = db.Column(db.String(64))
    subcategory = db.Column(db.String(64))
    service = db.Column(db.String(64))
    prices = db.Column(db.String(64))
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    bookings = db.relationship("BookingServices")
    cart = db.relationship('Cart')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")
    service_id = db.Column(db.Integer, db.ForeignKey(Services.id))
    service = db.relationship("Services")
    business_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    business = db.relationship('business_client')
    booking_at = db.Column(db.DateTime)


class Features(db.Model):
    id = db.Column('feature_id', db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    wifi = db.Column(db.Boolean)
    music = db.Column(db.Boolean)
    ac = db.Column(db.Boolean)
    disinfect = db.Column(db.Boolean)
    parking = db.Column(db.Boolean)
    organic = db.Column(db.Boolean)
    safety = db.Column(db.Boolean)


class Review(db.Model):
    id = db.Column('review_id', db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    ambience = db.Column(db.Boolean)
    hygiene = db.Column(db.Boolean)
    service = db.Column(db.Boolean)
    staff = db.Column(db.Boolean)
    facilities = db.Column(db.Boolean)
    equipments = db.Column(db.Boolean)
    trainer = db.Column(db.Boolean)


class Products(db.Model):
    id = db.Column('product_id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    client_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    client = db.relationship('business_client')
    loreal = db.Column(db.Boolean)
    garnier = db.Column(db.Boolean)
    streaks = db.Column(db.Boolean)
    tresemme = db.Column(db.Boolean)
    walla = db.Column(db.Boolean)
    wahl = db.Column(db.Boolean)
    mac = db.Column(db.Boolean)
    mableme = db.Column(db.Boolean)
    faces = db.Column(db.Boolean)
    colorbar = db.Column(db.Boolean)
    revlon = db.Column(db.Boolean)
    shehnaaz = db.Column(db.Boolean)


class Payment(db.Model):
    id = db.Column('booking_id', db.Integer, primary_key=True)
    payment_id = db.Column(db.String(64))
    bookings = db.relationship("Booking")


class Booking(db.Model):
    id = db.Column('booking_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")
    payment_id = db.Column(db.Integer, db.ForeignKey(Payment.id))
    payment = db.relationship("Payment")
    customer_name = db.Column(db.String(255))
    customer_email = db.Column(db.String(255))
    mobile_number = db.Column(db.String(255))
    business_id = db.Column(db.Integer, db.ForeignKey(business_client.id))
    business = db.relationship('business_client')
    payment_mode = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    amount = db.Column(db.String(255))
    services = db.relationship('BookingServices')
    paid = db.Column(db.Boolean, default=False)
    booking_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# Intermediary tables

class BookingServices(db.Model):
    id = db.Column('booking_services_id', db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey(Services.id))
    service = db.relationship('Services')
    booking_id = db.Column(db.Integer, db.ForeignKey(Booking.id))
    booking = db.relationship('Booking')
