from mysql.connector import MySQLConnection, Error
from flask import Flask, redirect, url_for
from flask import render_template, flash, redirect, session, url_for, request,  g, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


app = Flask(__name__)
app.config.from_object('config')

fields = ('id', 'name', 'email', 'phone', 'cell', 'status')

conn = MySQLConnection(user='root', password='',
                              host='127.0.0.1',
                              database='test_db')

class EditUserForm(Form):
    name = StringField('Name', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    cell = StringField('Cell')
    status = BooleanField('Status', default=False)

class NewUserForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    phone = StringField('Phone')
    cell = StringField('Cell')
    status = BooleanField('Status', default=False)
 

@app.route('/', methods=['GET', 'POST'])
def index(page=1):
    return render_template('index.html')

@app.route('/users')
def users():
    users = get_db_action(['get_all_users'])
    users = [dict(zip(fields, u)) for u in users]
    return render_template('users.html', users=users)

@app.route('/courses')
def courses():
    courses = get_db_action(['get_all_courses'])
    return render_template('courses.html', courses=courses)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = NewUserForm(request.form)
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cell=request.form['cell']
        status=bool(request.form['status'])

        if form.validate():
            args = [name, email, phone, cell, status]
            db_in_action('create_user', args)
            flash('Sucsess!, New user added')
        else:
            flash('Error: Check data in form. ')
    return render_template('new_user.html', form=form)


@app.route('/edit_user/<uid>', methods=['GET', 'POST'])
def edit_user(uid):

    u_data = dict(zip(fields, get_db_action(['get_user', [uid]])[0]))
    form = EditUserForm(request.form)
    form.name = u_data['name']
    form.email = u_data['email']
    form.cell = u_data['cell']
    form.phone = u_data['phone']
    form.status = u_data['status']
    courses = get_db_action(['get_all_courses'])
    form.courses = [dict(zip(('name', 'c_id'), c[1:])) for c in courses]
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cell=request.form['cell']
        status=bool(request.form['status'])
        args = [uid, phone, cell, status]
        db_in_action('update_user', args)
        flash('Saved sucessfully')
    return render_template('edit.html', form=form)


@app.route('/delete_user/<uid>', methods=['GET', 'POST'])
def delete_user(uid):
    db_in_action('delete_user', [uid])
    return redirect(url_for("users"), code=200)

# def get_all_courses():
#     cursor = conn.cursor()
#     cursor.callproc('get_all_courses')
#     for result in cursor.stored_results():
#         return result.fetchall()
#     cursor.close()

# def get_users_courses(uid):
#     cursor = conn.cursor()
#     cursor.callproc('get_users_courses', [uid])
#     for result in cursor.stored_results():
#         return result.fetchall()
#     cursor.close()

# def get_user(uid):
#     cursor = conn.cursor()
#     cursor.callproc('get_user', [uid])
#     for result in cursor.stored_results():
#         return result.fetchall()
#     cursor.close()
 
# def get_all_users():
#     cursor = conn.cursor()
#     cursor.callproc('get_all_users')
#     for result in cursor.stored_results():
#         yield result.fetchall()
#     cursor.close()


def get_db_action(args):
    cursor = conn.cursor()
    cursor.callproc(*args)
    for result in cursor.stored_results():
        return result.fetchall()
    cursor.close()


def db_in_action(action, args):
    cursor = conn.cursor()
    cursor.callproc(action, args)
    cursor.close()
    conn.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    conn = MySQLConnection(user='root', password='',
                                  host='127.0.0.1',
                                  database='test_db')
