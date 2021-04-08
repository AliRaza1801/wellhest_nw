import os
import sys
from datetime import date, timedelta, datetime
from functools import reduce

import razorpay
import requests
from flask import render_template, url_for, request, redirect, flash, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import Date, cast, or_
from sqlalchemy_imageattach.context import store_context

from config import app, login_manager, store
from forms import VendorForm, LoginForm, ServiceFormBeauty, ServiceFormFitness, DescriptionForm, ChangePasswordForm, \
    AdminBookingForm, ServiceForm, AdminVendorUpdateForm
from models import db, User, business_client, Features, Review, Products, Services, Booking, BookingServices, \
    CentreImage, AmbienceImage, StaffImage, EquipmentsImage, ServiceImage, Cart, Payment
from permissions import vendor_required, admin_required
from utils import send_otp, generate_otp, send_email, send_message

homeImgLinks = {'video1': './static/img/wellhest.webm', 'img2': './static/img/gallery.webp',
                'img3': './static/img/dresser.jpg', 'logo': './static/img/Partnerlogo.png',
                'gallary': './static/img/gallery.webp', 'avatar': './static/img/avtaar.jpg',
                'img4': './static/img/app.webp', 'img5': './static/img/cut.webp',
                'IOS': 'https://img.icons8.com/color/48/000000/apple-app-store--v1.png',
                'android': 'https://img.icons8.com/color/48/000000/google-play.png',
                'download_app': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/download-our-app/DOWNLOAD+OUR+APP.png',
                'standard': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/standarization/stadard.png',
                'tech': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/technology/1.TECH.png'}

businessImgLinks = {'img1': './static/img/exp.jpg', 'img2': './static/img/img.webp', 'img3': './static/img/avtaar.jpg',
                    'IOS': 'https://img.icons8.com/color/48/000000/apple-app-store--v1.png',
                    'android': 'https://img.icons8.com/color/48/000000/google-play.png',
                    'self_service': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/clientself-service/1.client-self-service.png',
                    'calender_manage': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/calendar-management/1.CALENDAR+MANAGEMENT.png',
                    'booking_manage': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/booking-management/1.BOOKINGMANAGEMENT.png',
                    'loyalty_tools': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/marketing-and-loyalty-tools/1.MARKETING-TOOLS.png',
                    'pos': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/point-os-scale/1.POINTOFSALE.png',
                    'finance': 'https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/finance-management/1.FINANCE-MANAGEMENT.png'}

vendorImgLinks = {'img1': './static/img/temp.jpeg', 'android': 'https://img.icons8.com/color/48/000000/google-play.png',
                  'IOS': 'https://img.icons8.com/color/48/000000/apple-app-store--v1.png',
                  "description": "https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/vendor-portal-blocs/YOUR-BUSINESS-DETAIL.png",
                  "services": "https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/vendor-portal-blocs/INPUT-SERVICE-DETAILS.png",
                  "notifi": "https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/vendor-portal-blocs/BOOKING-NOTIFICATION.png",
                  "history": "https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/vendor-portal-blocs/BOOKING-HISTORY.png",
                  "alert": "https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/vendor-portal-blocs/WEAKLY-BUSINESS-ALERT.png",
                  "finance": "https://wellhest-general-data.s3.ap-south-1.amazonaws.com/picturess/vendor-portal-blocs/FINANCE-MANAGEMENT.png", }

social_links = {
    'twitter': 'https://twitter.com/wellhest',
    'instagram': 'https://www.instagram.com/wellhest/',
    'pinterest': 'https://in.pinterest.com/well_hest/_saved/',
    'facebook': '#',
    'youtube': '#',
}

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

razorpay_client = razorpay.Client(
    auth=(
        os.getenv('RAZORPAY_ID'),
        os.getenv('RAZORPAY_SECRET')
    )
)


@login_manager.unauthorized_handler
def unauthorized_callback():
    if current_user.is_anonymous:
        return redirect('/#loginModal')
    elif current_user.business_client:
        return redirect('/vendor')
    elif current_user.is_admin:
        return redirect('/admin/merchants')
    else:
        return redirect('/')


@app.route("/", methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    return render_template('index.html', links=homeImgLinks, login_form=login_form, social_links=social_links)


@app.route("/business", methods=['GET', 'POST'])
def business():
    login_form = LoginForm()
    form = VendorForm()
    if current_user.is_authenticated:
        return redirect(url_for('vendor'))
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = {
                "email": form.email.data,
            }
            otp = generate_otp()
            user = User(**user_data)
            vendor_data = {
                # "user": user,
                "business_name": form.business_name.data,
                "city": form.city.data,
                "address": form.address.data,
                "pin": form.pin.data,
                "gstin": form.gstin.data,
                "pan": form.pan.data,
                "manager_name": form.name.data,
                "mobile_number_manager": form.mobile_number.data,
                "category": form.category.data,
                "otp": otp
            }
            vendor = business_client(**vendor_data)
            user.business_client = vendor
            user.set_password('test')
            db.session.add(user)
            db.session.add(vendor)
            db.session.commit()
            mobilenumber=form.mobile_number.data
            if not mobilenumber.startswith('+91'):
                mobilenumber='+91-'+form.mobile_number.data
            else:
                if not mobilenumber.startswith('+91-'):
                    mobilenumber=mobilenumber.replace('+91','+91-')
            send_otp(otp,mobilenumber)
            # flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('otp_verify', v_id=vendor.id))
    errors = form.errors
    return render_template('vendor/for_Business.html', links=businessImgLinks, form=form, errors=errors,
                           login_form=login_form, social_links=social_links)


@app.route("/otp-verify/<v_id>", methods=['GET', 'POST'])
def otp_verify(v_id):
    client = db.session.query(business_client).get(v_id)
    if client.otp_verified:
        return redirect(url_for('success'))
    login_form = LoginForm()
    error = None
    if request.method == 'POST':
        otp = request.values.get('otp')
        if otp == client.otp:
            client.otp_verified = True
            db.session.commit()
            send_message(client.mobile_number_manager)
            send_email(client.user.email)
            return redirect(url_for('success'))
        else:
            error = 'Incorrect OTP, Please try again'

    return render_template('vendor/otp-verify.html', links=businessImgLinks, social_links=social_links, error=error,
                           login_form=login_form)


@app.route("/success")
def success():
    login_form = LoginForm()
    return render_template('vendor/success.html', links=businessImgLinks, login_form=login_form,
                           social_links=social_links)


@app.route("/vendor", methods=['GET', 'POST'])
@login_required
@vendor_required
def vendor():
    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('Password Changed Successfully!', 'success')
    client = current_user.business_client
    notifications = db.session.query(Booking).filter_by(business=client, status=None).count()
    return render_template('vendor/vendor.html', links=vendorImgLinks, client=client, form=form,
                           notifications=notifications)


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash('Already logged in !!', 'info')
        return redirect(request.referrer)
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'error')
                return redirect(f"{request.referrer}#loginModal")
            flash('Login Successful!', 'success')
            login_user(user)
            return redirect(request.referrer)
        flash('Empty email or password', 'error')
        return redirect(f"{request.referrer}#loginModal")


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(request.referrer or url_for('index'))


@app.route("/services", methods=['GET', 'POST'])
@login_required
@vendor_required
def services():
    client = current_user.business_client
    service_form = ServiceForm()
    if client.category == 'beauty':
        form = ServiceFormBeauty()
    else:
        form = ServiceFormFitness()
    if request.method == 'POST':
        form.validate_on_submit()
        catm = request.values.getlist('Categorym')
        subcatm = request.values.getlist('SubCategorym')
        pricem = request.values.getlist('pricem')
        cat = request.values.getlist('Category1')
        subcat = request.values.getlist('SubCategory1')
        price = request.values.getlist('price1')
        available = {
            "description": form.description.data,
            "open_time": form.open_time.data,
            "close_time": form.close_time.data,
            "day_from": form.day_from.data,
            "day_to": form.day_to.data
        }
        for data in available:
            setattr(client, data, available[data])
        products = {
            "loreal": form.loreal.data,
            "garnier": form.garnier.data,
            "streaks": form.streaks.data,
            "tresemme": form.tresemme.data,
            "walla": form.walla.data,
            "wahl": form.wahl.data,
            "mac": form.mac.data,
            "mableme": form.mableme.data,
            "faces": form.faces.data,
            "colorbar": form.colorbar.data,
            "revlon": form.revlon.data,
            "shehnaaz": form.shehnaaz.data,
        }
        if client.category == 'beauty':
            features = {
                "wifi": form.wifi.data,
                "music": form.music.data,
                "ac": form.ac.data,
                "disinfect": form.disinfect.data,
                "parking": form.parking.data,
                "organic": form.organic.data,
            }
            reviews = {
                "ambience": form.ambience.data,
                "hygiene": form.hygiene.data,
                "service": form.service.data,
                "staff": form.staff.data,
            }
        else:
            features = {
                "wifi": form.wifi.data,
                "music": form.music.data,
                "ac": form.ac.data,
                "disinfect": form.disinfect.data,
                "parking": form.parking.data,
                "safety": form.safety.data,
            }
            reviews = {
                "ambience": form.ambience.data,
                "hygiene": form.hygiene.data,
                "facilities": form.facilities.data,
                "equipments": form.equipments.data,
                "trainer": form.trainer.data,
            }
        if client.feature:
            for f in features:
                setattr(client.feature, f, features[f])
        else:
            feature = Features(**features)
            client.feature = feature

        if client.products:
            for p in products:
                setattr(client.products, p, products[p])
        else:
            product = Products(**products)
            client.products = product

        if client.review:
            for r in reviews:
                setattr(client.review, r, reviews[r])
        else:
            review = Review(**reviews)
            client.review = review

        # db.session.query(Services).filter_by(client_id=client.id).delete()
        for x in zip(catm, subcatm, pricem):
            if x[0] or x[1] or x[2]:
                ser = Services(gender='male', category=x[0], subcategory=x[1], prices=x[2])
                client.services.append(ser)

        for x in zip(cat, subcat, price):
            if x[0] or x[1] or x[2]:
                ser = Services(gender='female', category=x[0], subcategory=x[1], prices=x[2])
                client.services.append(ser)
        db.session.commit()
        flash("Saved !!!", 'success')
        return redirect(url_for('vendor'))
    else:
        cat_male = list(db.session.query(Services).filter_by(client_id=client.id, gender='male'))
        cat_female = list(db.session.query(Services).filter_by(client_id=client.id, gender='female'))
    return render_template('vendor/services.html', form=form, client=client, cat_male=cat_male, cat_female=cat_female,
                           service_form=service_form)


@app.route("/business-type", methods=['POST'])
@login_required
@vendor_required
def business_type():
    business_type = request.values.get('business_type')
    current_user.business_client.business_type = business_type
    db.session.commit()
    return redirect(request.referrer)


@app.route("/services/update", methods=['POST'])
@login_required
@vendor_required
def update_service():
    service_form = ServiceForm()
    if service_form.validate_on_submit():
        gender = request.values.get('gender')
        prices = service_form.prices.data
        category = service_form.category.data
        subcategory = service_form.subcategory.data
        service = service_form.service.data
        if request.values.get('_create'):
            ser = Services(
                gender=gender,
                category=category,
                subcategory=subcategory,
                service=service,
                prices=prices
            )
            current_user.business_client.services.append(ser)
        elif request.values.get('_update'):
            ser = db.session.query(Services).get(request.values.get('id'))
            ser.prices = prices
            ser.category = category
            ser.service = service
            ser.subcategory = subcategory
        db.session.commit()
    print(service_form.errors)
    return redirect(request.referrer)


@app.route("/description", methods=['GET', 'POST'])
@login_required
@vendor_required
def descrip():
    form = DescriptionForm()
    client = current_user.business_client
    if request.method == 'POST':
        if form.validate_on_submit():
            vendor_data = {
                "business_name": form.business_name.data,
                "city": form.city.data,
                "address": form.address.data,
                "locality": form.locality.data,
                "pin": form.pin.data,
                "gstin": form.gstin.data,
                "lat": form.lat.data,
                "lng": form.lng.data,
                "place_id": form.place_id.data,
                "pan": form.pan.data,
                "license_number": form.license_number.data,
                "manager_name": form.manager_name.data,
                "mobile_number": form.mobile_number.data,
                "mobile_number_manager": form.mobile_number_manager.data,
                "category": form.category.data,
                "partnership": form.partnership.data,
                "updated": True
            }
            for data in vendor_data:
                setattr(client, data, vendor_data[data])
            if form.business_id.data:
                client.save_image(form.business_id.data)
            current_user.name = form.owner_name.data
            db.session.commit()
            flash("Saved !!!", 'success')
        print(form.errors)
        if form.errors:
            flash("There are Errors in this page !!!", 'error')
    return render_template('vendor/description.html', client=client, form=form)


@app.route('/booking', methods=['GET', 'POST'])
@login_required
@vendor_required
def book():
    client = current_user.business_client
    if request.method == 'POST':
        if request.values.get('_accept'):
            book = db.session.query(Booking).get(request.values.get('_accept'))
            book.status = True
        elif request.values.get('_reject'):
            book = db.session.query(Booking).get(request.values.get('_reject'))
            book.status = False
        db.session.commit()

    return render_template('vendor/booking.html', client=client)


@app.route('/history')
@login_required
@vendor_required
def history():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date() if end_date_str else None
    client = current_user.business_client
    if start_date and end_date:
        booking_history = db.session.query(Booking).filter_by(business=client).filter(Booking.status != None) \
            .filter(cast(Booking.booking_at, Date) <= end_date,
                    cast(Booking.booking_at, Date) > start_date)
        context = {
            "history": booking_history,
            "start_date": datetime.strftime(start_date, '%m/%d/%Y'),
            "end_date": datetime.strftime(end_date, '%m/%d/%Y')
        }
    else:
        booking_history = db.session.query(Booking).filter_by(business=client).filter(Booking.status != None)
        context = {
            "history": booking_history
        }

    return render_template('vendor/history.html', context=context)


@app.route('/alert')
@login_required
@vendor_required
def alert():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date() if start_date_str else (
                date.today() - timedelta(7))
    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date() if end_date_str else date.today()
    client = current_user.business_client
    service = db.session.query(Booking).filter_by(business=client, status=True, paid=True) \
        .filter(cast(Booking.booking_at, Date) <= end_date,
                cast(Booking.booking_at, Date) > start_date)
    sm = db.session.query(db.func.sum(Booking.amount)).filter_by(business=client, status=True, paid=True) \
        .filter(cast(Booking.booking_at, Date) <= end_date,
                cast(Booking.booking_at, Date) > start_date)
    percentage = 10
    by_cash = sm.filter_by(payment_mode='cash').all()[0][0] or 0
    online = sm.filter_by(payment_mode='online').all()[0][0] or 0
    context = {
        "count": service.count(),
        "by_cash": by_cash,
        "online": online,
        "receive": online * (1 - (percentage / 100)),
        "pay": by_cash * percentage / 100,
        "start_date": datetime.strftime(start_date, '%m/%d/%Y'),
        "end_date": datetime.strftime(end_date, '%m/%d/%Y')
    }
    return render_template('vendor/alert.html', context=context)


@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin/index.html')


@app.route('/admin/merchants')
@login_required
@admin_required
def list_vendors():
    merchants = db.session.query(business_client).all()
    return render_template('admin/vendors.html', merchants=merchants)


@app.route('/admin/merchant/<v_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_vendor(v_id):
    merchant = db.session.query(business_client).get(v_id)
    form = AdminVendorUpdateForm()
    if request.method == 'POST':
        form.validate_on_submit()
        vendor_data = {
            "business_name": form.business_name.data,
            "city": form.city.data,
            "locality": form.locality.data,
            "address": form.address.data,
            "pin": form.pin.data,
            "lat": form.lat.data,
            "lng": form.lng.data,
            "place_id": form.place_id.data,
            "gstin": form.gstin.data,
            "pan": form.pan.data,
            "mobile_number": form.mobile_number.data,
            "manager_name": form.manager_name.data,
            "mobile_number_manager": form.mobile_number_manager.data,
            "license_number": form.license_number.data,
            "business_id": form.business_id.data,
            "description": form.description.data,
            "business_type": form.business_type.data,
            "open_time": form.open_time.data,
            "close_time": form.close_time.data,
            "day_from": form.day_from.data,
            "day_to": form.day_to.data,
            "otp_verified": form.otp_verified.data,
        }
        for data in vendor_data:
            setattr(merchant, data, vendor_data[data])
        db.session.commit()

    return render_template('admin/update-business.html', merchant=merchant, form=form, getattr=getattr)


@app.route('/admin/merchant/<v_id>/changestatus')
@login_required
@admin_required
def update_vendor_status(v_id):
    merchant = db.session.query(business_client).get(v_id)
    merchant.updated = not merchant.updated
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/merchant/<v_id>/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_business(v_id):
    merchant = db.session.query(business_client).get(v_id)
    if request.method == 'POST':
        user = merchant.user
        db.session.query(Cart).filter_by(user=user).delete()
        db.session.query(Booking).filter_by(user=user).delete()
        db.session.query(ServiceImage).filter_by(client=merchant).delete()
        db.session.query(CentreImage).filter_by(client=merchant).delete()
        db.session.query(AmbienceImage).filter_by(client=merchant).delete()
        db.session.query(StaffImage).filter_by(client=merchant).delete()
        db.session.query(EquipmentsImage).filter_by(client=merchant).delete()
        db.session.query(Features).filter_by(client=merchant).delete()
        db.session.query(Review).filter_by(client=merchant).delete()
        db.session.query(Products).filter_by(client=merchant).delete()
        services = db.session.query(Services).filter_by(client=merchant)
        bookings = db.session.query(Booking).filter_by(user=user)
        for service in services.all():
            db.session.query(BookingServices).filter_by(service=service).delete()
        for booking in bookings.all():
            db.session.query(BookingServices).filter_by(booking=booking).delete()
        services.delete()
        bookings.delete()
        db.session.delete(merchant)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('list_vendors'))
    return render_template('admin/delete-vendor.html', merchant=merchant)


@app.route('/admin/users')
@login_required
@admin_required
def list_users():
    users = db.session.query(User).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/user/<u_id>/changestatus')
@login_required
@admin_required
def admin_status(u_id):
    user = db.session.query(User).get(u_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/user/<u_id>/password', methods=['GET', 'POST'])
@login_required
@admin_required
def set_password(u_id):
    if request.method == 'POST':
        password = request.form.get('password')
        user = db.session.query(User).get(u_id)
        if password:
            user.set_password(password)
            db.session.commit()
            flash('Password Changed', 'success')
            return redirect(url_for('list_users'))
        else:
            flash('Password cannot be empty!!', 'error')
    return render_template('admin/set-password.html')


@app.route('/admin/create-service/<v_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def create_service(v_id):
    form = AdminBookingForm()
    vendor = db.session.query(business_client).get(v_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            booking_data = {
                'customer_name': form.customer_name.data,
                'customer_email': form.customer_email.data,
                'mobile_number': form.mobile_number.data,
                'payment_mode': form.payment_mode.data,
                'amount': form.amount.data,
                'paid': form.paid.data,
                'booking_at': form.booking_at.data,
            }
            booking = Booking(**booking_data)
            booking.business = vendor
            for i in request.values.getlist('services'):
                s = db.session.query(Services).get(i)
                bs = BookingServices()
                bs.booking = booking
                bs.service = s
                db.session.add(bs)
            db.session.add(booking)
            db.session.commit()
            flash('Saved!!', 'success')
    return render_template('admin/booking.html', vendor=vendor, form=form)


@app.route("/upload-image", methods=['POST'])
@login_required
@vendor_required
def images():
    client = current_user.business_client
    centre_image = request.files.getlist('centre_image')
    ambience_image = request.files.getlist('ambience_image')
    staff_image = request.files.getlist('staff_image')
    equipments_image = request.files.getlist('equipments_image')
    service_image = request.files.getlist('service_image')
    for image in centre_image:
        if image.filename:
            img = CentreImage()
            img.client = client
            img.save_image(image)
            db.session.add(img)
    for image in ambience_image:
        if image.filename:
            img = AmbienceImage()
            img.client = client
            img.save_image(image)
            db.session.add(img)
    for image in staff_image:
        if image.filename:
            img = StaffImage()
            img.client = client
            img.save_image(image)
            db.session.add(img)
    for image in equipments_image:
        if image.filename:
            img = EquipmentsImage()
            img.client = client
            img.save_image(image)
            db.session.add(img)
    for image in service_image:
        if image.filename:
            img = ServiceImage()
            img.client = client
            img.save_image(image)
            db.session.add(img)
    db.session.commit()
    flash('Image Uploaded!!', 'success')
    return redirect(request.referrer)


@app.route("/search")
def search():
    filters = request.args.getlist('filters')
    gender = request.args.getlist('gender')
    service = request.args.get('service', '')
    location = request.args.get('location', '')
    city = request.args.get('city')
    login_form = LoginForm()
    centers = db.session.query(business_client).filter_by(updated=True)
    if city:
        centers = centers.filter_by(city=city)
    if location:
        centers = centers.filter(or_(
            business_client.city.contains(location),
            business_client.locality.contains(location)
        ))
    if service:
        centers = centers.join(Services).filter(or_(
            business_client.business_name.contains(service),
            Services.category.contains(service),
        ))
    if len(filters):
        centers = centers.join(Features).filter(or_(*map(lambda x: getattr(Features, x) == True, filters)))
    if len(gender):
        centers = centers.filter(or_(*map(lambda x: getattr(business_client, 'business_type') == x, gender)))
    return render_template(
        'client/search.html',
        login_form=login_form,
        centers=centers,
        gender=gender,
        filters=filters,
        location=location,
        service=service,
        city=city,
        social_links=social_links
    )


@app.route("/booking/<c_id>")
def bookservice(c_id):
    center = db.session.query(business_client).get(c_id)
    login_form = LoginForm()
    return render_template(
        'client/bookservice.html',
        center=center,
        login_form=login_form,
        db=db, Cart=Cart,
        GOOGLE_API_KEY=GOOGLE_API_KEY
    )


@app.route("/checkout/<v_id>", methods=['GET', 'POST'])
@login_required
def checkout(v_id):
    business = db.session.query(business_client).get(v_id)
    cart_items = db.session.query(Cart).filter_by(user=current_user, business=business).all()
    total = reduce(lambda a, b: a + b, [float(x.service.prices) for x in cart_items], 0)
    if request.method == 'POST':
        time = request.form.get('time')
        date = request.form.get('date')
        for item in cart_items:
            item.booking_at = datetime.strptime(f"{time}-{date}", '%I:%M %p-%m/%d/%Y')
        db.session.commit()
        return redirect(url_for('payment', v_id=business.id))
    return render_template('client/checkout.html', cart_items=cart_items, total=total, business=business)


@app.route("/add-to-cart/<s_id>/<v_id>")
@login_required
def add_to_cart(s_id, v_id):
    service = db.session.query(Services).get(s_id)
    vendor = db.session.query(business_client).get(v_id)
    cart = db.session.query(Cart).filter_by(user=current_user, service=service, business=vendor)
    if not cart.all():
        cart_obj = Cart(user=current_user, service=service, business=vendor)
        db.session.add(cart_obj)
        db.session.commit()
    return redirect(request.referrer)


@app.route("/remove-from-cart/<s_id>/<v_id>")
@login_required
def remove_from_cart(s_id, v_id):
    service = db.session.query(Services).get(s_id)
    vendor = db.session.query(business_client).get(v_id)
    cart = db.session.query(Cart).filter_by(user=current_user, service=service, business=vendor)
    if cart.all():
        cart.delete()
        db.session.commit()
    return redirect(request.referrer)


@app.route('/payment/<v_id>')
@login_required
def payment(v_id):
    razorpay_id = os.getenv('RAZORPAY_ID')
    business = db.session.query(business_client).get(v_id)
    cart_items = db.session.query(Cart).filter_by(user=current_user, business=business).all()
    total = reduce(lambda a, b: a + b, [float(x.service.prices) for x in cart_items], 0)
    amount = int(total * 100)
    return render_template(
        'client/payment.html',
        cart_items=cart_items,
        razorpay_id=razorpay_id,
        amount=amount,
        business=business
    )


@app.route('/charge', methods=['POST'])
@login_required
def charge():
    business_id = request.form['business_id']
    payment_id = request.form['razorpay_payment_id']

    business = db.session.query(business_client).get(business_id)
    cart_query = db.session.query(Cart).filter_by(user=current_user, business=business)
    cart_items = cart_query.all()
    total = reduce(lambda a, b: a + b, [float(x.service.prices) for x in cart_items], 0)

    amount = int(total * 100)
    x = razorpay_client.payment.capture(payment_id, amount)

    # Create Payment
    payment = Payment(payment_id=x.get('id'))

    # Create Booking
    booking_data = {
        'customer_name': current_user.name,
        'customer_email': x.get('email'),
        'mobile_number': x.get('contact'),
        'payment_mode': "online",
        'amount': total,
        'paid': True,
        'booking_at': cart_items[0].booking_at,
    }
    booking = Booking(**booking_data)
    booking.user = current_user
    booking.payment = payment
    booking.business = business
    for cart in cart_items:
        service = cart.service
        bs = BookingServices()
        bs.booking = booking
        bs.service = service
        db.session.add(bs)
    db.session.add(payment)
    db.session.add(booking)
    cart_query.delete()
    db.session.commit()

    # return jsonify(
    #     razorpay_client.payment.fetch(payment_id)
    # )
    return render_template('client/payment_success.html')


@app.route('/place-search')
def place_search():
    params = {
        "key": GOOGLE_API_KEY,
        "query": request.args.get('query')
    }
    response = requests.get(
        'https://maps.googleapis.com/maps/api/place/textsearch/json',
        params
    )
    return jsonify(response.json().get('results'))


@app.route('/place-details')
def place_details():
    params = {
        "place_id": request.args.get('place_id'),
        "key": GOOGLE_API_KEY,
        "fields": "address_component,adr_address,business_status,formatted_address,geometry,icon,name,"
                  "permanently_closed,photo,place_id,plus_code,type,url,utc_offset,vicinity"
    }
    response = requests.get(
        'https://maps.googleapis.com/maps/api/place/details/json',
        params
    )
    return jsonify(response.json().get('result'))
