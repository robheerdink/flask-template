from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFError
from core import app
from core.forms import LoginForm, ProgramForm, ChannelForm, ScheduleForm
from core.models import db, Program, Channel, Schedule


def url(location, msg=''):
    """ redirect helper """
    return redirect(url_for(location, msg=msg))


@app.route('/', defaults={'msg': ''})
@app.route("/msg/<msg>", methods=['GET', 'POST'])
def root(msg):
    """ root """
    return render_template('base_layout.html', msg=msg)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    """ handle csrf errors in forms """
    return url('root', msg=e.description)


@app.route('/test_db')
def test_db():
    """ test if db is working """
    try:
        db.session.execute('SELECT 1')
        return url('root', msg="ok")
    except:
        return url('root', msg="fail")


@app.route('/show_channels')
def show_channels():
    return render_template('show_channels.html', channels=Channel.query, title="Channels")


@app.route('/show_programs')
def show_programs():
    return render_template('show_programs.html', programs=Program.query, title="Programs")


@app.route('/show_schedules')
def show_schedules():
    return render_template('show_schedules.html', schedules=Schedule.query, title="Schedules")


@app.route('/table_programs')
def table_programs():
    """ tables with datatables.js """
    return render_template('table_programs.html', programs=Program.query, title="Programs")


@app.route('/table_programs_ajax')
def table_programs_ajax():
    """ tables with datatables.js + AJAX (query call moved to ajax in template) """
    return render_template('table_programs_ajax.html', title="Programs")


@app.route('/table_programs_server')
def table_programs_server():
    """ tables with datatables.js + AJAX + serverside loading """
    return render_template('table_programs_server.html', programs=Program.query, title="Programs")


@app.route('/api/programs_ajax')
def programs_ajax():
    query = Program.query
    return {'data': [p.to_dict() for p in query]}


@app.route('/api/programs_server')
def programs_server():
    query = Program.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Program.name.like(f'%{search}%'),
            Program.title.like(f'%{search}%'),
            Program.description.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['name', 'title', 'description']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Program, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [p.to_dict() for p in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Program.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@app.route("/login", methods=['GET', 'POST'])
def login():
    """User login"""
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['email']
            pasw = request.form['pasw']
            msg = email + " " + pasw + " logged in"
            return url('root', msg=msg)
    return render_template("form_login.html", form=form)


@app.route("/create_channel", methods=['GET', 'POST'])
def create_channel():
    """create Channel"""
    form = ChannelForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            title = request.form['title']
            timezone = request.form['timezone']
            channel = Channel(name=name, title=title, timezone=timezone)
            db.session.add(channel)
            db.session.commit()
            msg = "channel: {} is successfully created!".format(channel)
            return url('root', msg=msg)

    return render_template("form_channel.html", form=form)


@app.route("/create_program", methods=['GET', 'POST'])
def create_program():
    """create Program """
    form = ProgramForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            title = request.form['title']
            description = request.form['description']
            genre = request.form['genre']
            rating = request.form['rating']
            program = Program(name=name, title=title, description=description, genre=genre, rating=rating)
            db.session.add(program)
            db.session.commit()
            msg = "program: {} is successfully created!".format(program)
            return url('root', msg=msg)
    return render_template("form_program.html", form=form)


@app.route("/create_schedule", methods=['GET', 'POST'])
def create_schedule():
    """create Channel"""
    form = ScheduleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
            # program_id = request.form['xxx']
            # channel_id = request.form['xxx']
            start = request.form['start']
            end = request.form['end']
            # schedule = Program(program_id=program_id, channel_id=channel_id, start=start, end=end)
            # db.session.add(schedule).commit()
            # msg = "channel: {} is successfully created!".format(schedule)
            # return url('root', msg=msg)

    return render_template("form_schedule.html", form=form)