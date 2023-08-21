import datetime
from datetime import timedelta
import random
import os
from collections import Counter
from flask import Flask, render_template, Response, request, redirect, url_for, session, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from create_objects import *
from sms import Sms
from flask_login import UserMixin, login_user, LoginManager, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from sms.number_filter import NumberGenerate
from family import familes


app = Flask(__name__)

run = 'dev'
# debug = ''

if run == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:icui4cu4u@localhost/arababc'
    debug = True
# elif run == 'deploy':
#     uri = os.environ.get('DATABASE_URL')
#     if uri and uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)
#         app.config['SQLALCHEMY_DATABASE_URI'] =  uri
#         debug = False


# os.environ.get('SECRET_KEY')
app.config['SECRET KEY'] = 'APP_SECRET_KEYdffsdf'
app.secret_key = 'APP_SECRET_KEYdffsdf'  # os.environ.get('APP_SECRET_KEY')
app.config['ALLOWED_IMAGE_EXTENSIONS'] = [
    'PNG', 'JPG', 'JPEG', 'jpeg', 'png', 'jpg']
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
# app.config = ['IMAGE_UPLOADS'] = 'static/uploads'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# scheduler = APScheduler()


@login_manager.user_loader
def load_user(member_id):
    return Members.query.get(int(member_id))


class Members(db.Model, UserMixin):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fe = db.Column(db.String(100))
    middle_name = dbirst_nam.Column(db.String(100))
    surname = db.Column(db.String(100))
    maiden_name = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    second_phone_number = db.Column(db.String(100))
    email = db.Column(db.String(100))
    residential_address = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100))
    lga = db.Column(db.String(100))
    residential_state = db.Column(db.String(100))
    lat_lng = db.Column(db.String(100))
    state_of_origin = db.Column(db.String(100))
    state_lga = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    permanent_address = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    marital_status = db.Column(db.String(100))
    wedding_date = db.Column(db.String(100))
    baptism = db.Column(db.String(100))
    society = db.Column(db.String(100))
    user_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(120))
    profile_picture = db.Column(db.String(120), default='default')
    positions = db.relationship(
        'Position', backref='member', lazy="dynamic", cascade="all,delete")
    family_id = db.relationship(
        'Abc_Families', backref='abc_families', uselist=False)

    @property
    def password(self):
        raise AttributeError('Password is wrong')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))


class Abc_Families(db.Model):
    __tablename__ = 'abc_families'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    family_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    email = db.Column(db.String(100))
    residential_address = db.Column(db.String(100))
    google_suggested_address = db.Column(db.String(100))
    Neigborhood = db.Column(db.String(100))
    lga = db.Column(db.String(100))
    state = db.Column(db.String(100))
    coordinates = db.Column(db.String(100))
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    visitations = db.relationship(
        'Visitations', backref='abc_families', lazy="dynamic", cascade="all,delete")


class Visitations(db.Model):
    __tablename__ = 'visitations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(500))
    day_visited = db.Column(db.String(100))
    condition = db.Column(db.String(100))  # critical , etc
    scheduled_visitation = db.Column(db.Date)
    summary = db.Column(db.String(500))
    family_id = db.Column(db.Integer, db.ForeignKey('abc_families.id'))
    visitation_status = db.Column(db.Boolean(), nullable=True)
    joint_event = db.relationship(
        "Joint_events", backref='visitations', cascade="all, delete")


#
class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.String(120))
    joint_event = db.relationship(
        "Joint_events", backref='calendar', cascade="all, delete")


class Joint_events(db.Model):
    __tablename__ = 'joint_events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(120))
    Description = db.Column(db.String(500))
    Date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    event_completed = db.Column(db.Date)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))
    visitation_id = db.Column(db.Integer, db.ForeignKey('visitations.id'))


def allowed_image(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'Picture File Too Large', 413


def save_image(photo, f_name, surname):
    if photo.filename != '' and allowed_image(photo.filename) == True:
        _, ext = os.path.splitext(photo.filename)
        photo_name = secure_filename(f_name + surname + ext)
        file_path = os.path.join(
            current_app.root_path, 'static/img/uploads', photo_name)
        photo.save(file_path)
        return photo_name

    else:
        flash('No Picture File uploaded or Picture format invalid')
        return 'default.png'


@app.template_filter('date_month')
def date_month(value, format='%B'):
    return value.strftime(format)


@app.template_filter('format_changer')
def format_changer(value, format="%Y-%m-%d"):
    return value.strftime()


@app.template_filter('date_day')
def date_day(value, format="%d"):
    return value.strftime(format)


@app.template_filter('age')
def from_dob_to_age(new):
    today = datetime.date.today()
    return today.year - new.year - ((today.month, today.day) < (new.month, new.day))


@app.template_filter('list_picker')
def random_color(string):
    rand_color = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))

    return f'{string}{rand_color}'


@app.template_filter('slicer')
def slicer(word):
    if len(word) < 15:
        return word
    elif len(word) > 15:
        return word[:13] + "......."
    else:
        pass


@app.template_filter('this_year')
def this_year(digit):
    return digit + datetime.date.today().year


@app.template_filter('age_group')
def age_group(new):
    today = datetime.date.today()
    age = today.year - new.year - \
        ((today.month, today.day) < (new.month, new.day))
    if age <= 12:
        return 'Children'
    elif age <= 17:
        return 'Teen'
    elif age <= 35:
        return 'Youth'
    elif age <= 59:
        return 'Adult'
    else:
        return 'Elder'


@app.template_filter('date_week')
def age_group(new):
    year = new.year
    month = new.month
    day = new.day
    week = datetime.date(year, month, day).isocalendar()[1]
    return f'Week_{week}'


@app.template_filter('to_datetime')
def date_to_string(date_str):
    duration = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return duration.date()


# @app.template_filter('visitation_days_old')
# def visiting_age(dates):
#     try:
#         datetime_object = datetime.datetime.strptime(dates, "%Y-%m-%d")
#         today = datetime.date.today()
#         if datetime_object > today:
#             return f' In {abs(today.day - datetime_object.day)} day(s)'
#     except:
#         return 'Never Visited'

@app.template_filter('change_to_true')
def change_to_true(string):
    if string:
        return 'Not Completed'
    else:
        return 'Completed'


def date_formatter(date):
    return datetime.datetime.strftime(date, "%Y-%m-%d")


@app.route('/')
# #@login_required
def home():

    # map
    today = datetime.datetime.today().date()
    family = Abc_Families.query.all()
    families = db.session.query(Abc_Families, Visitations).outerjoin(Visitations,
                                                                     Abc_Families.id == Visitations.family_id).all()
    Family_name = [i.family_name for i in family]
    latitiude = [float(i.coordinates.split(',')[0][1:]) for i in family]
    longitude = [float(i.coordinates.split(',')[1][:-1].strip(' '))
                 for i in family]

    items = [list(x) for x in zip(Family_name, latitiude, longitude)]
    # setview = [items[0][1], items[-1][2]]

    # calendar
    event = Joint_events.query.filter(
        Joint_events.Date >= datetime.date.today())

    parent_list = [{'Title': i.Title, 'Description': i.Description,
                    'Date': i.Date, 'due_date': i.Date - datetime.date.today()
                    } for i in event if i.event_completed is None]
    upcoming = [i for i in parent_list]
    # chart
    family = Abc_Families.query.all()
    members = Members.query.all()
    member_count = Members.query.filter_by().count()
    test = Members.query.filter(
        Members.date_of_birth <= datetime.datetime(1997, 2, 1)).all()
    societies = [i.society for i in test]
    new = zip(Counter(societies).keys(), Counter(societies).values())
    data = dict(new)
    labels = [i for i in data.keys()]
    series = [i for i in data.values()]

    return render_template('homepage.html', member=members[:6], event_color='RGB', labels=labels, family=family,
                           parent_list=parent_list, series=series, member_count=member_count, members=members,
                           upcoming=upcoming, lister=items, data=data, today=today)


@app.route('/sms', methods=["GET", "POST"])
# #@login_required
def sms_index():
    num = NumberGenerate()
    sms = Sms()
    numbers_generated = ''
    if request.method == 'POST':
        chosen_group = num.number_getter(request.form['select'])
        len_of_number = 0
        for i in chosen_group:
            try:
                numbers_generated += i + ','
                len_of_number += 1
            except TypeError:
                pass

        return render_template('Bulk_sms/sms_index.html', sms_balance=sms.balance_getter(),
                               len_of_numbers=len_of_number,
                               numbers_generated=numbers_generated, chosen_groups=request.form['select'])


@app.route('/send-text', methods=["GET", "POST"])
# #@login_required
def messaging():
    sms = Sms()
    num = NumberGenerate()
    sms_report = sms.report_getter()
    # report = sms.report_getter(phone_counter)
    # number_of_pending = report['status'].count("Submitted")
    # number_of_delivered = report['status'].count('DELIVERED')

    return render_template('Bulk_sms/messaging.html', group_list=num.group_list, sms_balance=2323, sms_report=sms_report)


phone_counter = ''


@app.route('/send_sms', methods=["GET", "POST"])
# @login_required
def send_sms():
    sms = Sms()
    if request.method == 'POST':
        sender_name = request.form['sender_name']
        phone_numbers = request.form['numbers_generated']
        global phone_counter
        phone_counter += phone_numbers
        message = request.form['message']
        sms.sms_sender(sender=sender_name,
                       phone_numbers=phone_numbers, message=message)
        flash('Message(s) sent')
        return redirect(url_for('home'))


@app.route('/sms_report')
def sms_report():
    sms = Sms()
    report = sms.delivery_report(phone_counter)
    number_of_pending = report['status'].count("Submitted")
    number_of_delivered = report['status'].count('DELIVERED')
    return render_template('Bulk_sms/sms_report.html',
                           count_of_numbers=sms.numbers_counter(
                               phone_numbers=phone_counter),
                           number_of_pending=number_of_pending, number_of_delivered=number_of_delivered)


@app.route('/datapage')
# @login_required
def datapage():
    member = Members.query.all()
    columns = ['id', 'Full Name', 'Phone Number',
               'Birthday Month', 'Birthday day', 'Society', 'Age Group', ]

    return render_template('member/datatable.html', columns=columns, member=member)


@app.route('/member_map')
# @login_required
def member_map():
    member = Members.query.all()
    Family_name = [i.first_name for i in member]
    latitiude = [float(i.lat_lng.split(',')[0][1:]) for i in member]
    longitude = [float(i.lat_lng.split(',')[1][:-1].strip(' '))
                 for i in member]

    lister = [list(x) for x in zip(Family_name, latitiude, longitude)]

    return render_template('member/members_map.html')


@app.route('/welfare/families')
# @login_required
def families():
    members = db.session.query(Abc_Families, Visitations).outerjoin(Visitations,
                                                                    Abc_Families.id == Visitations.family_id).all()

    return render_template('welfare/families.html', members=members)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = Members.query.filter_by(
            user_name=request.form['user_name']).first()
        if user_name:
            if check_password_hash(user_name.password_hash, request.form['password']):
                login_user(user_name)
                flash('login successful')
                return redirect(url_for('home'))

            else:
                flash('Wrong password try again')
        else:
            flash('Username entered does not exist,Try again')
    return render_template('logins.html')


@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    logout_user()
    flash('you have been logged out')
    return redirect(url_for('login'))


# ################################################CLEAR##################################################################

@app.route('/member_list', methods=['GET', 'POST'])
# @login_required
def member_list():
    fam = familes.Families()

    if request.method == 'POST':
        file = request.files.get('profile_picture')

        hashed_pw = generate_password_hash(request.form['password'], "sha256")
        new_member = Members(
            first_name=request.form['first_name'].title(),
            middle_name=request.form['middle_name'].title(),
            surname=request.form['surname'].title(),
            gender=request.form['gender'].lower(),
            marital_status=request.form['marital_status'].lower(),
            maiden_name=request.form['maiden_name'].title(),
            phone_number=request.form['phone_number'],
            second_phone_number=request.form['second_phone_number'],
            email=request.form['email'],
            neighborhood=request.form['neighborhood'].title(),
            residential_address=request.form['residential_address'].title(),
            lga=request.form['lga'].title(),
            lat_lng=[request.form['lat'], request.form['lng']],
            state_of_origin=request.form['state_of_origin'],
            state_lga=request.form['state_lga'],
            permanent_address=request.form['permanent_address'],
            occupation=request.form['occupation'],
            baptism=request.form['baptism'],
            society=request.form['society'],
            date_of_birth=request.form['date_of_birth'],
            wedding_date=request.form['wedding_date'],
            password_hash=hashed_pw,
            profile_picture=save_image(file, request.form['first_name'], request.form['surname']))
        lst = ['position', 'start_date', 'end_date', 'department']
        new = []
        for i in lst:
            f = request.form.getlist(i)
            new.append(f)
        zipping_lst_new = zip(lst, new)
        zipped_position_key_value = dict(zipping_lst_new)
        position_department = zipped_position_key_value['department']
        position_end_dates = zipped_position_key_value['end_date']
        position_start_dates = zipped_position_key_value['start_date']
        position_positions = zipped_position_key_value['position']
        lenght_of_values = len(position_department)

        counter = 0
        for i in range(lenght_of_values):
            new_position = Position(position=position_positions[counter],
                                    department=position_department[counter],
                                    end_date=position_end_dates[counter],
                                    start_date=position_start_dates[counter])
            new_member.positions.append(new_position)
            counter += 1
        if fam.family_checker(request.form['marital_status'].lower(), date_of_birth=request.form['date_of_birth'],
                              gender=request.form['gender'].lower()):
            new_family = fam.extract(first_name=request.form['first_name'].title(),
                                     surname=request.form['surname'].title(),
                                     gender=request.form['gender'].lower(),
                                     marital_status=request.form['marital_status'].lower(
            ),
                phone_number=request.form['phone_number'],
                email=request.form['email'],
                Neigborhood=request.form['neighborhood'].title(
            ),
                residential_address=request.form['residential_address'].title(
            ),
                google_suggested_address=request.form['residential_address'].title(
            ),
                lga=request.form['lga'].title(),
                coordinates=[
                                         request.form['lat'], request.form['lng']],
                date_of_birth=request.form['date_of_birth'],
                state=request.form['residential_address'].title(
            )
            )

        else:
            pass

        db.session.add(new_member)
        db.session.commit()
        flash('Member Successfully Added')
        return redirect(url_for('member_list'))

    return render_template('member/member_list.html', state_list=states,
                           gender_list=gender, society_list=society, departments_list=departments,
                           member=Members.query.all())


@app.route('/new_member', methods=["GET", "POST"])
def new_member():
    gmap_script = os.environ.get('gmap_script')
    return render_template('member/add_members.html', state_list=states, gender_list=gender, society_list=society, gmap_script=gmap_script,
                           departments_list=departments)


@app.route('/profile_picture', methods=['GET', 'POST'])
@app.route('/member/edit/<int:id>', methods=["GET", "POST"])
# @login_required
def edit(id):
    member_id = Members.query.get(id)
    position_id = Position.query.get(id)
    position = Position.query.filter_by(member_id=id).all()
    lst = ['position', 'start_date', 'end_date', 'department']
    new = []
    position_dict = {'position': [], 'start_date': [],
                     'end_date': [], 'department': []}
    new_add = []

    if request.method == 'POST':
        file = request.files.get('profile_picture')
        # member_id.password_hash = generate_password_hash(request.form['password'], "sha256")
        # member_id.user_name = request.form['user_name']

        member_id.first_name = request.form['first_name']
        member_id.middle_name = request.form['middle_name']
        member_id.surname = request.form['surname']
        member_id.gender = request.form['gender']
        member_id.marital_status = request.form['marital_status']
        member_id.maiden_name = request.form['maiden_name']
        member_id.phone_number = request.form['phone_number']
        member_id.second_phone_number = request.form['second_phone_number']
        member_id.email = request.form['email']
        member_id.residential_address = request.form['residential_address']
        member_id.state_of_origin = request.form['state_of_origin']
        member_id.state_lga = request.form['state_lga']
        member_id.permanent_address = request.form['permanent_address']
        member_id.occupation = request.form['occupation']
        member_id.baptism = request.form['baptism']
        member_id.society = request.form['society']
        member_id.date_of_birth = request.form['date_of_birth']
        member_id.wedding_date = request.form['wedding_date']
        member_id.profile_picture = save_image(file, request.form['first_name'], request.form['surname']
                                               )

        for i in lst:
            f = request.form.getlist(i)
            new.append(f)
        zipping_lst_new = zip(lst, new)
        zipped_position_key_value = dict(zipping_lst_new)
        position_department = zipped_position_key_value['department']
        position_positions = zipped_position_key_value['position']
        position_start_dates = zipped_position_key_value['start_date']
        position_end_dates = zipped_position_key_value['end_date']
        lenght_of_values = len(position_department)
        counter = 0
        for i in position:
            i.department = position_department[counter]
            i.position = position_positions[counter]
            i.start_date = position_start_dates[counter]
            i.end_date = position_end_dates[counter]
            counter += 1
        counts = 0
        if len(request.form.getlist('department')) > len(position):
            for i in lst:
                f = request.form.getlist(i)[len(position):]
                new_add.append(f)
            zipping_lst_new = zip(lst, new_add)
            zipped_position_key_value = dict(zipping_lst_new)
            position_department = zipped_position_key_value['department']
            position_positions = zipped_position_key_value['position']
            position_start_dates = zipped_position_key_value['start_date']
            position_end_dates = zipped_position_key_value['end_date']
            lenght_of_values = len(position_department)
            counter = 0
            for i in range(lenght_of_values):
                member_id.positions.extend([Position(department=position_department[counter],
                                                     position=position_positions[counter],
                                                     start_date=position_start_dates[counter],
                                                     end_date=position_end_dates[counter])])
                db.session.commit()
                counter += 1

        fam = familes.Families()
        if fam.family_checker(request.form['marital_status'].lower(), date_of_birth=request.form['date_of_birth'],
                              gender=request.form['gender'].lower()):
            new_family = fam.extract(first_name=request.form['first_name'].title(),
                                     surname=request.form['surname'].title(),
                                     gender=request.form['gender'].lower(),
                                     marital_status=request.form['marital_status'].lower(
            ),
                phone_number=request.form['phone_number'],
                email=request.form['email'],
                Neigborhood=request.form['neighborhood'].title(
            ),
                residential_address=request.form['residential_address'].title(
            ),
                google_suggested_address=request.form['residential_address'].title(
            ),
                lga=request.form['lga'].title(),
                coordinates=[
                                         request.form['lat'], request.form['lng']],
                date_of_birth=request.form['date_of_birth'],
                state=request.form['residential_address'].title(
            )
            )

        else:
            pass

        db.session.commit()
        flash('Data Updated ')
        return redirect(url_for('member_page', id=member_id.id))
    profile_pic = Members.query.filter_by(id=member_id.id).first()
    return render_template('member/edit.html', state_list=states,
                           gender_list=gender, society_list=society,
                           departments_list=departments, member_id=member_id, profile_pic=profile_pic.profile_picture,
                           position=position)


@app.route('/member/<int:id>/delete/')
# @login_required
def delete(id):
    member_id = Members.query.get(id)
    db.session.delete(member_id)
    db.session.commit()
    flash('Deleted Successfully')
    return redirect(url_for('member_list'))


@app.route('/member/<int:id>/member_page', methods=["GET", "POST"])
def member_page(id):
    member = Members.query.get(id)
    profile_pic = Members.query.filter_by(id=member.id).first()
    return render_template('member/profile_page.html', member=member, profile_pic=profile_pic.profile_picture)


@app.route('/welfare/<int:id>/family_page', methods=["GET", "POST"])
def family_page(id):
    member = Abc_Families.query.get(id)
    visitation = Visitations.query.filter_by(family_id=id).first()
    visitation_counts = Visitations.query.filter_by(family_id=id).count()

    return render_template('welfare/family_page.html', member=member,
                           visitation=visitation, visitation_counts=visitation_counts)


@app.route('/welfare/<int:id>/schedule', methods=["GET", "POST"])
def family_visitation_schedule(id):
    member = Abc_Families.query.get(id)
    visitations = Visitations.query.filter_by(family_id=id).first()
    if request.method == 'POST':
        if Visitations.query.filter_by(family_id=id).first() == None:

            newVisitation = Visitations(
                title=f'Scheduled Visitation for {member.family_name}',
                scheduled_visitation=request.form['scheduled_visitation'],
                description=f'Welfare Department will be visiting the family'
                            f' of {member.family_name}'
                            f' on {request.form["scheduled_visitation"]}',
                family_id=member.id,
                visitation_status=True
            )
            new_event = Joint_events(
                Title=f'Scheduled Visitation for {member.family_name}',
                Date=request.form['scheduled_visitation'],
                Description=f'Welfare Department will be visiting the family'
                            f' of {member.family_name}'
                            f' on {request.form["scheduled_visitation"]}',
                due_date=request.form['scheduled_visitation']

            )
            newVisitation.joint_event.append(new_event)
            db.session.add(newVisitation)
            db.session.commit()
            flash('Schedule created')

            return redirect(url_for('family_page', id=id))
        else:
            flash('schedule already exist')
    return render_template('welfare/family_page.html', member=member, visitation=visitations)


@app.route('/welfare/<int:id>/mark_complete', methods=["GET", "POST"])
def family_visitation_mark_complete(id):
    member = Abc_Families.query.get(id)
    visitation = Visitations.query.filter_by(family_id=id).first()
    events = Joint_events.query.filter_by(visitation_id=visitation.id).first()
    # events = Joint_events.query.filter_by(visitation_id = visitation.id).first()
    visitation_counts = Visitations.query.filter_by(family_id=id).count()
    visitations = Visitations.query.filter_by(family_id=id).first()
    visitations.visitation_status = False
    visitations.description = 'This Event was Marked As Completed'
    # events.event_completed = 'compeleted'
    visitations.day_visited = datetime.date.today()
    db.session.commit()

    return render_template('welfare/family_page.html', member=member,
                           visitation=visitation, visitation_counts=visitation_counts)


@app.route('/welfare/edit/<int:id>/schedule', methods=["GET", "POST"])
def family_visitation_edit(id):
    member = Abc_Families.query.get(id)
    visitations = Visitations.query.filter_by(family_id=id).first()
    events = Joint_events.query.filter_by(visitation_id=visitations.id).first()

    if request.method == 'POST':

        visitations.scheduled_visitation = request.form['scheduled_visitation']
        events.Date = request.form['scheduled_visitation']
        events.due_date = request.form['scheduled_visitation']
        if request.form['visitation_status'] == 'Completed':
            visitations.visitation_status = False
            events.event_completed = datetime.datetime.today().date()

        else:
            visitations.visitation_status = True
        visitations.day_visited = request.form['day_visited']
        visitations.condition = request.form['condition']

        visitations.summary = request.form['summary']
        visitations.title = request.form['title']
        events.Title = request.form['title']
        visitations.description = request.form['description']
        events.Description = request.form['description']
        db.session.commit()
        flash('Successfully Updated')
        return redirect(url_for('family_page', id=id))

    return render_template('welfare/edit_visitation.html', member=member, visitation=visitations)


@app.route('/welfare/<int:id>/delete/')
# @login_required
def delete_visitations(id):
    visitation = Visitations.query.get(id)
    db.session.delete(visitation)
    db.session.commit()
    flash('Deleted Successfully')
    return redirect(url_for('families'))


@app.route('/welfare/active_visitations')
# @login_required
def active_visitations():
    # family = Abc_Families.query.all()
    members = db.session.query(Abc_Families, Visitations) \
        .outerjoin(Visitations, Abc_Families.id == Visitations.family_id).filter(
        Visitations.visitation_status == True).all()
    today = datetime.datetime.today().date()
    return render_template('welfare/active_visits.html', family=members, today=today)


@app.route('/admin-settings', methods=["GET", "POST"])
# @login_required
def admin_settings():
    member_id = Members.query.get(current_user.id)
    if request.method == 'POST':
        new_hashed_pw = generate_password_hash(
            request.form['new_password'], "sha256")
        current = request.form['current_password']
        new_password = request.form['new_password']
        retry_password = request.form['retry_password']
        if check_password_hash(pwhash=current_user.password_hash, password=current):
            if new_password == retry_password:
                current_user.password_hash = new_hashed_pw
                member_id.password_hash = current_user.password_hash
                db.session.commit()
                flash("Password Changed Successfully")
                return redirect(url_for('home'))
            else:
                flash("Password don't match")
        else:
            flash('Wrong Password Entered')
    return render_template('admin_settings.html')


@app.route('/set-admin', methods=["GET", "POST"])
# @login_required
def set_admin():
    if request.method == 'POST':
        member_id = Members.query.get(request.form['member_id'])
        member_id.user_name = request.form['user_name']
        new_hashed_pw = generate_password_hash(
            request.form['new_password'], "sha256")
        new_password = request.form['new_password']
        retry_password = request.form['retry_password']
        if new_password == retry_password:
            member_id.password_hash = new_hashed_pw
            db.session.commit()
            flash("Admin added Successfully")
            return redirect(url_for('home'))
        else:
            flash("Password don't match")

    return render_template('member/Set Admin.html')


@app.route('/username', methods=["GET", "POST"])
# @login_required
def username():
    member_id = Members.query.get(current_user.id)
    if request.method == 'POST':
        member_id.user_name = request.form['username']
        db.session.commit()
        flash("Username Changed Successfully")
    return render_template('admin_settings.html')


@app.route('/calendar')
# @login_required
def calendar():
    # event=db.session.query(Joint_events, Calendar).outerjoin(Joint_events,
    #                                                       Calendar.id == Joint_events.calendar_id).all()
    event = Joint_events.query.filter(
        Joint_events.Date >= datetime.date.today())

    upcoming = [i for i in event]
    parent_list = [{'Title': i.Title, 'Description': i.Description,
                    'Date': i.Date, 'due_date': i.due_date
                    } for i in event if i.event_completed is None or type(i.calendar_id) == int]

    event_color = 'RGB'

    return render_template('event/calendar.html', parent_list=parent_list, event_color=event_color)


@app.route('/add_event', methods=["GET", "POST"])
# @login_required
def add_event():
    if request.method == 'POST':
        new_calendar = Calendar(title=request.form['title'],
                                start_date=request.form['start_date'],
                                end_date=request.form['end_date'],
                                description=request.form['description'])

        new_event = Joint_events(
            Title=request.form['title'],
            Date=request.form['start_date'],
            Description=request.form['description'],
            end_date=request.form['due_date']


        )
        new_calendar.joint_event.append(new_event)

        db.session.add(new_calendar)
        db.session.commit()
        flash('Event Registered')
        return redirect(url_for('calendar'))

    return render_template('event/new_event.html')


@app.route('/event_page/<int:id>')
# @login_required
def event_page(id):
    # events = Calendar.query.all().first()
    events = Joint_events.query.get(id)

    return render_template('event/event_page.html', events=events)


@app.route('/event_table')
# @login_required
def event_table():
    events = Joint_events.query.all()

    event_calendar = [i.calendar_id for i in events]

    return render_template('event/events_table.html', events=events)


@app.route('/maps')
# @login_required
def map():
    member = Abc_Families.query.all()
    # visitation = Visitations.query.filter_by(family_id=id).first()
    # visitation_counts = Visitations.query.filter_by(family_id=id).count()
    Family_name = [i.family_name for i in member]
    latitiude = [float(i.coordinates.split(',')[0][1:]) for i in member]
    longitude = [float(i.coordinates.split(',')[1][:-1].strip(' '))
                 for i in member]

    items = [list(x) for x in zip(Family_name, latitiude, longitude)]
    setview = [items[0][1], items[-1][2]]

    return render_template('welfare/map.html', lister=items, setview=setview)


@app.route('/update_event/<int:id>', methods=["GET", "POST"])
# @login_required
def update_event(id):
    events = Calendar.query.get(id)
    joint = Joint_events.query.get(id)
    visitation = Visitations.query.get(id)
    if request.method == 'POST':
        events.title = request.form['title']
        joint.Title = request.form['title']
        events.start_date = request.form['start_date']
        events.due_date = request.form['due_date']
        joint.Date = request.form['start_date']
        events.end_date = request.form['end_date']
        events.description = request.form['description']
        joint.Description = request.form['description']
        db.session.commit()

        return redirect(url_for('calendar'))

    return render_template('event/update_event.html', events=events, visitation=visitation, joint=joint)


@app.route('/events/<int:id>/delete/')
# @login_required
def delete_event(id):
    events = Calendar.query.get(id)
    db.session.delete(events)
    db.session.commit()
    flash('Deleted Successfully')
    return redirect(url_for('event_table'))


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=5050)
