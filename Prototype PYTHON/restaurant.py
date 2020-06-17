from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import datetime 
from validate_email import validate_email
from wtforms import Form, TextField, RadioField, TextAreaField, validators, StringField, SubmitField, DateField, DecimalField, SelectField, BooleanField
from wtforms.validators import NumberRange
from wtforms.fields.html5 import EmailField
import sqlite3

app = Flask(__name__)

class loginForm(Form):
	email = EmailField('Email address', [validators.DataRequired('Το email απαιτείται'), validators.Email()])
	password = TextField('Password:', validators=[validators.required('Ο κωδικός πρόσβασης απαιτείται'), validators.Length(min=4, max=15)])

class registerForm(Form):
	name = TextField('Name:', validators=[validators.required('Το όνομα απαιτείται'),validators.Regexp('^[a-zA-Z ]*$', message="Επιτρέπονται μόνο γράμματα και ο κενός χαρακτήρας")])
	surname = TextField('Password:', validators=[validators.required('Το επώνυμο απαιτείται'),validators.Regexp('^[a-zA-Z ]*$', message="Επιτρέπονται μόνο γράμματα και ο κενός χαρακτήρας")])
	email = EmailField('Email address', [validators.DataRequired('Το email απαιτείται'), validators.Email()])
	password = TextField('Password:', validators=[validators.required('Ο κωδικός πρόσβασης απαιτείται'), validators.Length(min=8, max=15),
		validators.Regexp('(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])', message="Ο κωδικός πρόσβασης πρέπει να περιέχει τουλάχιστον έναν αριθμό, ένα κεφαλαίο χαρακτήρα και έναν πεζό χαρακτήρα!")])
	cpassword = TextField('Cpassword:', validators=[validators.required('Η επιβεβαίωση του κωδικού πρόσβασης απαιτείται'), validators.Length(min=8, max=15),
		validators.Regexp('(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])', message="Ο κωδικός πρόσβασης πρέπει να περιέχει τουλάχιστον έναν αριθμό, ένα κεφαλαίο χαρακτήρα και έναν πεζό χαρακτήρα!")])
	gender = RadioField('Gender', choices=[('female','female'),('male','male')])

class reservationDateForm(Form):
	imerominia = DateField('imerominia', format='%Y-%m-%d', validators=(validators.required('Η ημερομηνία απαιτείται'),))

class reservationHourForm(Form):
	reservation = RadioField('reservation',validators=[validators.required('Επέλεξε ώρα')],coerce=str)
	imerominia = DateField('imerominia', format='%Y-%m-%d', validators=(validators.required('Η ημερομηνία απαιτείται'),))

class myReviewForm(Form):
	comment = TextField('Comment:', validators=[validators.required('Γράψτε την γνώμη σας')])

class tableSetupForm(Form):
	capacity = DecimalField('capacity', validators=[NumberRange(min=1, max=10, message='Ο αριθμών των ατόμων πρέπει να είναι μεταξύ 1-10'), validators.required('Ο αριθμός των ατόμων απαιτείται')])
	table_number = TextField('table_number:')

class openDateForm(Form):
	id = TextField('id')
	date_from = DateField('date_from', format='%Y-%m-%d', validators=(validators.required('Η ημερομηνία απαιτείται'),))
	date_to = DateField('date_to', format='%Y-%m-%d', validators=(validators.required('Η ημερομηνία απαιτείται'),))

class openHoursForm(Form):
	hour_id = TextField('hour_id')
	hour_from = TextField('hour_from:',validators=[validators.required('Η ώρα από απαιτείται')])
	hour_to = TextField('hour_to:',validators=[validators.required('Η ώρα έως απαιτείται')])
	date_id = TextField('date_id')

class reservationManagementForm(Form):
	id = TextField('id')
	date = DateField('date', format='%Y-%m-%d', validators=[validators.required('Η ημερομηνία απαιτείται')])
	hour = TextField('hour:',validators=[validators.required('Η ώρα έως απαιτείται')])
	persons = DecimalField('persons', validators=[ validators.required('Ο αριθμός των ατόμων απαιτείται')])
	customer_id = TextField('')
	status = TextField('')
	def __init__(self, *args, **kwargs):
		super(reservationManagementForm, self).__init__(*args, **kwargs)
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("SELECT Customer_ID,First_name||' '||Last_name CNAME FROM customer")
		customers=cursor.fetchall()
		con.close()
		self.customer_id.choices = [(c[0], c[1]) for c in customers]

class registerEmployeeForm(Form):
	name = TextField('Name:', validators=[validators.required('Το όνομα απαιτείται'),validators.Regexp('^[a-zA-Z ]*$', message="Επιτρέπονται μόνο γράμματα και ο κενός χαρακτήρας")])
	surname = TextField('Password:', validators=[validators.required('Το επώνυμο απαιτείται'),validators.Regexp('^[a-zA-Z ]*$', message="Επιτρέπονται μόνο γράμματα και ο κενός χαρακτήρας")])
	email = EmailField('Email address', [validators.DataRequired('Το email απαιτείται'), validators.Email()])
	password = TextField('Password:', validators=[validators.required('Ο κωδικός πρόσβασης απαιτείται'), validators.Length(min=8, max=15),
		validators.Regexp('(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])', message="Ο κωδικός πρόσβασης πρέπει να περιέχει τουλάχιστον έναν αριθμό, ένα κεφαλαίο χαρακτήρα και έναν πεζό χαρακτήρα!")])
	cpassword = TextField('Cpassword:', validators=[validators.required('Η επιβεβαίωση του κωδικού πρόσβασης απαιτείται'), validators.Length(min=8, max=15),
		validators.Regexp('(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])', message="Ο κωδικός πρόσβασης πρέπει να περιέχει τουλάχιστον έναν αριθμό, ένα κεφαλαίο χαρακτήρα και έναν πεζό χαρακτήρα!")])
	address = TextField('address')
	phone_number = TextField('phone_number')
 
class reservationPersonsForm(Form):
	persons = DecimalField('persons', validators=[ validators.required('Ο αριθμός των ατόμων απαιτείται')])
	hour = RadioField('hour')
	imerominia = DateField('imerominia', format='%Y-%m-%d' )

class reservationTablesForm(Form):
	tables = BooleanField('tables', validators=[ validators.required('Απαιτείται τουλάχιστον ένα τραπέζι')])
	reservation_id = TextField ('reservation_id')
	


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/menu/')
def menu():
    return render_template('menu.html')

@app.route('/reservation_date/')
def reservation_date():
	if session.get('user_id'):
		if session.get('user_role') and session.get('user_role')=='02': 
			return redirect('/reservation_management')
		else:
			form = reservationDateForm()
			return render_template('reservation_date.html',form=form, message='')
	else:
		form = loginForm()
		return render_template('login.html',form=form, message='')

@app.route('/reservation_date', methods=['POST'])
def do_reservation_date():
	message=''
	form = reservationDateForm(request.form)
	imerominia=request.form['imerominia']
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("SELECT * FROM open_date WHERE ? > date_from AND ? < date_to; " , (imerominia,imerominia))
		data=cursor.fetchall()
		if len(data)>0:
			return redirect("reservation_hour/"+imerominia)
		else:
			message='Είμαστε κλειστά'
		con.close()	
	return render_template('reservation_date.html',form=form, message=message) 

@app.route('/reservation_hour/<imerominia>')
def reservation_hour(imerominia):
	if session.get('user_id'):
		form = reservationHourForm()
		form.imerominia.value = imerominia
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("""SELECT hour_from , hour_to 
							FROM work_hours W 
							INNER JOIN open_dates_hours ODH ON W.id = ODH.work_hours_id 
                			INNER JOIN open_date D ON ODH.open_date_id = D.id 
                			WHERE ? >= date_from AND ? <= date_to""" , (imerominia,imerominia))
		data=cursor.fetchall()
		con.close()
		return render_template('reservation_hour.html',data=data, message='', form=form)
	else:
		form = loginForm()
		return render_template('login.html',form=form, message='')

@app.route('/reservation_hour', methods=['POST'])
def do_reservation_hour():
	form = reservationHourForm(request.form)
	imerominia = form.imerominia
	imerominia=request.form['imerominia']
	hour=request.form['reservation']
	form.reservation.value=hour
	if hour!='':
		return redirect('reservation_persons/'+imerominia+'/'+ hour)
	else:
		return redirect('reservation_hour/'+imerominia )

@app.route('/reservation_persons/<imerominia>/<wra>', defaults={'message': None})
@app.route('/reservation_persons/<imerominia>/<wra>/<message>')
def reservation_persons(imerominia,wra,message=''):
	form=reservationPersonsForm()	
	form.imerominia.value=imerominia
	form.hour.value=wra
	return render_template('reservation_persons.html', form=form, message=message)

@app.route('/reservation_persons', methods=['POST'])
def do_reservation_persons():
	form=reservationPersonsForm(request.form)
	imerominia=request.form['imerominia']
	hour=request.form['hour']
	persons=int(request.form['persons'])
	table=0
	if persons!='':
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("""SELECT capacity, table_id FROM res_table 
						WHERE Table_ID NOT IN (SELECT RT.Table_ID FROM reservation R 
												INNER JOIN reservation_table RT ON R.Reservation_ID = RT.Reservation_ID
                                            	WHERE Date= ? AND Start_time=?)
						ORDER BY Capacity""" , (imerominia,hour))
		data=cursor.fetchall()
		if len(data) > 0:
			for record in data:
				capacity=record[0]
				table_id=record[1]
				if persons <= capacity:
					table= table_id
					break
			if table==0:
				sum=0
				tables = []
				for record in data:
					capacity=record[0]
					table_id=record[1]
					if sum==0:
						tables.append(table_id)
						sum=capacity
					else:
						tables.append(table_id)
						sum=sum+capacity-2
					if persons<= sum:
						break
				if sum <= persons:
					message='Δεν είναι εφικτή η κράτηση. Παρακαλώ επικοινωνίστε μαζί μας τηλεφωνικά.'	
					#todo message never appear fix
				else:
					cursor.execute("""INSERT INTO reservation(Date, Persons, Start_time, Customer_ID, Status) VALUES (?, ?, ?, ?, '01')""" , (imerominia,persons,hour,session.get('customer_id')))
					con.commit()
					Reservation_ID=cursor.lastrowid
					for table in tables:
						cursor.execute("""INSERT INTO reservation_table(Table_ID, Reservation_ID) VALUES (?, ?)""" , (table, Reservation_ID))
						con.commit()
					con.close()
					return redirect('/my_reservations/')	
			else:
				cursor.execute("""INSERT INTO reservation(Date, Persons, Start_time, Customer_ID, Status) VALUES (?, ?, ?, ?, '01')""" , (imerominia,persons,hour,session.get('customer_id')))
				con.commit()
				Reservation_ID=cursor.lastrowid
				cursor.execute("""INSERT INTO reservation_table(Table_ID, Reservation_ID) VALUES (?, ?)""" , (table, Reservation_ID))
				con.commit()
				con.close()
				return redirect('/my_reservations/')
		#else:
			#lenghtdata=0
		con.close()	
		return redirect('reservation_persons/'+imerominia+ '/' + hour + '/' + message )
	else:
		return redirect('reservation_persons/'+imerominia + '/'+ hour + '/' + message )


@app.route('/login/')
def login():
	form = loginForm()
	return render_template('login.html',form=form, message='') 


@app.route('/login', methods=['POST'])
def do_login():
	form = loginForm(request.form)
	password=request.form['password']
	email=request.form['email']
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("SELECT * FROM USERS WHERE EMAIL=? AND PASSWORD =?" , (email,password))
		data=cursor.fetchall()
		if len(data)==1:
			message='Καλώς ήρθατε'
			for row in data:
				Role=row['Role']
				Customer_ID=row['Customer_ID']
				Employee_ID=row['Employee_ID']
				User_ID=row['User_ID']
				if(Role=='01'):
					cursor.execute("SELECT First_name FROM customer WHERE Customer_ID=?" , (Customer_ID,))
				else:
					cursor.execute("SELECT First_name FROM employee WHERE Employee_ID=?" , (Employee_ID,))
				First_name=cursor.fetchone()['First_name']
				session['user_first_name'] = First_name
				session['user_id'] = User_ID
				session['user_role'] = Role
				session['customer_id'] = Customer_ID
				session['employee_id'] = Employee_ID
		else:
			message='Δεν βρέθηκε κάποιος χρήστης με αυτά τα στοιχεία. Προσπαθήστε ξανά'
		con.close()
	return render_template('login.html', form=form, message=message)

@app.route('/logout/')
def logout():
	session.clear()
	return render_template('home.html')
	
@app.route('/register/')
def register():
	form = registerForm()
	if session.get('user_id'):
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()	
		cursor.execute("SELECT * FROM users U INNER JOIN customer C ON U.Customer_ID = C.Customer_ID WHERE User_ID= ?", (session.get('user_id'),))
		data=cursor.fetchone()
		form.name.value=data['First_name']
		form.surname.value=data['Last_name']
		form.email.value=data['Email']
		form.gender.value=data['Gender']
	else:
		form.gender.value='male'
	return render_template('register.html',form=form, message='') 

@app.route('/register', methods=['POST'])
def do_register():
	message=''
	form = registerForm(request.form)
	first_name=request.form['name']
	password=request.form['password']
	last_name=request.form['surname']
	cpassword=request.form['cpassword']
	email=request.form['email']
	gender=request.form['gender']
	form.name.value=first_name
	form.surname.value=last_name
	form.email.value=email
	form.gender.value=gender	
	if form.validate():		
		if (password!=cpassword):
			message='Ο κωδικός πρόσβασης και η επιβεβαίωση του δεν ταυτίζονται'
		else:
			con = sqlite3.connect("restaurant.db")
			con.row_factory = sqlite3.Row 
			cursor=con.cursor()
			if session.get('user_id'):
				cursor.execute("SELECT * FROM USERS WHERE EMAIL =? AND Customer_ID =?" , (email,session.get('customer_id')))
				data=cursor.fetchall()
				if len(data)==1:
					try:
						cursor.execute("UPDATE customer SET First_name=?, Last_name=?, Gender=? WHERE Customer_ID=?", (first_name,last_name,gender,session.get('customer_id')))
						con.commit()
						cursor.execute("UPDATE users SET Password=? WHERE Customer_ID=?", (password,session.get('customer_id')))
						con.commit()
						message='Τα στοιχεία του χρήστη άλλαξαν'
					except Exception as e:
						message='Παρουσιάστηκε κάποιο πρόβλημα, παρακαλω προσπαθήστε ξανά'	
				else:
					message='Το email που δώσατε χρησιμοποιείται ήδη'
				
			else:
				cursor.execute("SELECT * FROM USERS WHERE EMAIL=? " , (email,))
				data=cursor.fetchall()
				if len(data)==0:
					cursor.execute("INSERT INTO customer (First_name,Last_name,Gender) VALUES (?,?,?)" , (first_name,last_name,gender))
					con.commit()
					customer_ID=cursor.lastrowid
					cursor.execute("INSERT INTO users (Role,Email,Password,Employee_ID,Customer_ID) VALUES ('01',?,?, null,?)" ,(email,password,customer_ID))
					con.commit()
					message='Επιτυχής εγγραφή μέλους'
				else:
					message='Το email που δώσατε χρησιμοποιείται ήδη'	
				form.name.value=''
				form.surname.value=''
				form.email.value=''
				form.gender.value='male'	
			con.close()
	return render_template('register.html',form=form, message=message)


@app.route('/my_reservations/')
def my_reservations():
	if session.get('user_role') and session.get('user_role')=='02': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("SELECT * FROM reservation WHERE Customer_ID = ?", (session.get('customer_id'),))
		data=cursor.fetchall()
		con.close()
		return render_template('my_reservations.html',data=data)

@app.route('/my_review/')
def my_review():
	if session.get('user_id'):
		form = myReviewForm()
		return render_template('my_review.html',form=form, message='')
	else:
		form = loginForm()
		return render_template('login.html',form=form, message='')


@app.route('/my_review', methods=['POST'])
def do_my_review():
	form = myReviewForm(request.form)
	comment=request.form['comment']
	message = ''
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("INSERT INTO review (Customer_ID, Comment, Date) VALUES (? , ? , datetime('now'))" , (session.get('customer_id'),comment))
		con.commit()
		con.close()
		message ='Ευχαριστούμε για τα σχόλια'
	return render_template('my_review.html',form=form, message=message)


@app.route('/table_setup/')
def table_setup():
	form = tableSetupForm()
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("SELECT Capacity,Table_ID FROM res_table")
		data=cursor.fetchall()
		con.close()
		return render_template('table_setup.html',data=data, form=form)

@app.route('/table_setup', methods=['POST'])
def do_table_setup():
	form = tableSetupForm(request.form)
	capacity=request.form['capacity']
	table_number=request.form['table_number']
	message = ''
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		if table_number!="":
			cursor.execute("UPDATE res_table SET Capacity = ? WHERE Table_ID = ?;" , (capacity,table_number))
		else:
			cursor.execute("INSERT INTO res_table (Capacity) VALUES (?)" , (capacity,))
		con.commit()
		cursor.execute("SELECT Capacity,Table_ID FROM res_table")
		data=cursor.fetchall()
		con.close()
		message ='Το τραπέζι ενημερώθηκε'
	return render_template('table_setup.html',form=form, message=message,data=data)

@app.route('/open_dates/')
def open_dates():
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("SELECT * FROM open_date")
		data=cursor.fetchall()
		con.close()
	return render_template('open_dates.html',data=data)

@app.route('/open_dates_delete/<date_id>')
def open_dates_delete(date_id):
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("DELETE FROM open_date WHERE id = ?",(date_id,))
		cursor.execute("SELECT work_hours_id FROM open_dates_hours WHERE open_date_id = ?" ,(date_id,))
		data=cursor.fetchall()
		for record in data:
			cursor.execute("DELETE FROM work_hours WHERE id = ?" ,(record[0],))
			cursor.execute("DELETE FROM open_dates_hours WHERE open_date_id = ? " ,(date_id,))
		con.commit()
		cursor.execute("SELECT * FROM open_date")
		data=cursor.fetchall()
		con.close()
	return render_template('open_dates.html',data=data)	

@app.route('/open_date_form/')
def open_date_form_insert():
	title="Προσθήκη νέων ημερομηνιών λειτουργίας"
	form=openDateForm()
	form.id.value=""
	return render_template('open_date_form.html', form=form, title=title)

@app.route('/open_date_form/<id>/<date_from>/<date_to>')
def open_date_form_update(id,date_from,date_to):
	title="Επεξεργασία ημερομηνιών λειτουργίας"
	form=openDateForm()
	form.id.value=id
	form.date_from.value=date_from
	form.date_to.value=date_to
	return render_template('open_date_form.html', form=form, title=title)	

@app.route('/open_date_form', methods=['POST'])
def do_open_date_form():
	form = openDateForm(request.form)
	date_from=request.form['date_from']
	date_to=request.form['date_to']
	id=request.form['id']
	message = ''
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		if id!="":
			cursor.execute("UPDATE open_date SET date_from = ?, date_to = ? WHERE id = ?;" , (date_from,date_to,id))
		else:
			cursor.execute("INSERT INTO open_date (date_from, date_to) VALUES (?, ?)" , (date_from,date_to))
			id=str(cursor.lastrowid)
		con.commit()
		con.close()
		message ='Οι ημερομηνίες λειτουργίας έχουν ενημερωθε'
	return redirect('open_date_form/'+id+'/'+date_from+'/'+date_to)	

@app.route('/open_hours/<date_id>')
def open_hours(date_id):
	form=openHoursForm()
	form.date_id.value=date_id
	title="Επεξεργασία ωρών λειτουργίας"
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("""SELECT WH.*  
						FROM open_dates_hours ODH 
						INNER JOIN work_hours WH ON ODH.work_hours_id = WH.id
						WHERE ODH.open_date_id = ?""",(date_id,))
		data=cursor.fetchall()
		con.close()
	return render_template('open_hours.html', data=data, title=title, form=form)

@app.route('/open_hours', methods=['POST'])
def do_open_hours_form():
	form=openHoursForm(request.form)
	hour_from=request.form['hour_from']
	hour_to=request.form['hour_to']
	hour_id=request.form['hour_id']
	date_id=request.form['date_id']
	message = ''
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		if hour_id!="":
			cursor.execute("UPDATE work_hours SET hour_from = ?, hour_to = ? WHERE id = ?;" , (hour_from,hour_to,hour_id))
		else:
			cursor.execute("INSERT INTO work_hours (hour_from, hour_to) VALUES (?, ?)" , (hour_from,hour_to))
			hour_id=str(cursor.lastrowid)
			cursor.execute("INSERT INTO open_dates_hours (open_date_id, work_hours_id) VALUES (?, ?)" , (date_id,hour_id))
		con.commit()
		con.close()
		message ='Οι ώρες λειτουργίας προστέθηκαν επιτυχώς'
	return redirect('open_hours/'+date_id)	

@app.route('/open_hours_delete/<date_id>/<hour_id>')
def open_hours_delete(date_id,hour_id):
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("DELETE FROM work_hours WHERE id = ?",(hour_id,))
		cursor.execute("DELETE FROM open_dates_hours WHERE work_hours_id = ?",(hour_id,))
		con.commit()
		con.close()
	return redirect('/open_hours/'+date_id)	

@app.route('/reservation_management/')
def reservation_management():
	form = reservationManagementForm()
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("""SELECT r.* ,C.First_name||' '||c.Last_name CNAME 
					FROM reservation R 
					INNER JOIN customer C ON R.Customer_ID=C.Customer_ID 
                    ORDER BY Date desc""")
		data=cursor.fetchall()
		cursor.execute("SELECT Customer_ID,First_name||' '||Last_name CNAME FROM customer")
		customers=cursor.fetchall()
		con.close()
	return render_template('reservation_management.html',data=data, customers=customers, form=form)

@app.route('/reservation_management', methods=['POST'])
def do_reservation_management():
	form = reservationManagementForm(request.form)
	id=request.form['id']
	date=request.form['date']
	hour=request.form['hour']
	persons=request.form['persons']
	customer_id=request.form['customer_id']
	status=request.form['status']
	message = ''
	
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		if id!="":
			cursor.execute("UPDATE reservation SET status = ? , Employee_ID = ? WHERE Reservation_ID = ?;" , (status,session.get('employee_id'),id))
		else:
			cursor.execute("""INSERT INTO reservation (Date, Persons, Start_time, Customer_ID, Employee_ID, Status) VALUES (?,?,?,?,?,?)""" , (date,persons,hour,customer_id,session.get('employee_id'),status))
		con.commit()
		con.close()
		message ='Η κράτηση καταχωρήθηκε'
	else:
		message='asfasfas'		
	con = sqlite3.connect("restaurant.db")
	con.row_factory = sqlite3.Row 
	cursor=con.cursor()
	cursor.execute("""SELECT r.* ,C.First_name||' '||c.Last_name CNAME 
				FROM reservation R 
				INNER JOIN customer C ON R.Customer_ID=C.Customer_ID 
				ORDER BY Date desc""")
	data=cursor.fetchall()
	cursor.execute("SELECT First_name||' '||Last_name CNAME, Customer_ID FROM customer")
	customers=cursor.fetchall()
	con.close()	
	return render_template('reservation_management.html',data=data, customers=customers, form=form, message=message)


@app.route('/register_employee/')
def register_employee():
	form=registerEmployeeForm()
	return render_template('register_employee.html', form=form)

@app.route('/register_employee', methods=['POST'])
def do_register_employee():
	message=''
	form=registerEmployeeForm(request.form)
	first_name=request.form['name']
	password=request.form['password']
	last_name=request.form['surname']
	cpassword=request.form['cpassword']
	email=request.form['email']
	address=request.form['address']
	phone_number=request.form['phone_number']
	form.name.value=first_name
	form.surname.value=last_name
	form.email.value=email
	form.phone_number.value=phone_number
	form.address.value=address
	if form.validate():		
		if (password!=cpassword):
			message='Ο κωδικός πρόσβασης και η επιβεβαίωση του δεν ταυτίζονται'
		else:
			con = sqlite3.connect("restaurant.db")
			con.row_factory = sqlite3.Row 
			cursor=con.cursor()
			cursor.execute("SELECT * FROM USERS WHERE EMAIL=? " , (email,))
			data=cursor.fetchall()
			if len(data)==0:
				cursor.execute("INSERT INTO employee (First_name,Last_name,Address,Phone_number) VALUES (?,?,?,?)" , (first_name,last_name,address,phone_number))
				con.commit()
				employee_id=cursor.lastrowid
				cursor.execute("INSERT INTO users (Role,Email,Password,Employee_ID,Customer_ID) VALUES ('02', ? , ?, ? ,null)" ,(email,password,employee_id))
				con.commit()
				message='Επιτυχής εγγραφή μέλους'
			else:
				message='Το email που δώσατε χρησιμοποιείται ήδη'	
			form.name.value=''
			form.surname.value=''
			form.email.value=''
			form.phone_number.value=''
			form.address.value=''	
			con.close()
	return render_template('register_employee.html',form=form, message=message)	

@app.route('/reservation_tables/<reservation_id>', defaults={'message': None})
@app.route('/reservation_tables/<reservation_id>/<message>')
def reservation_tables(reservation_id,message=''):
	form=reservationTablesForm()
	form.reservation_id.value=reservation_id
	if session.get('user_role') and session.get('user_role')=='01': 
		return render_template('home.html')
	else:
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row
		cursor=con.cursor()
		cursor.execute("""SELECT Table_ID,Capacity,'' AS checked FROM (
							SELECT * FROM res_table 
							WHERE Table_ID NOT IN (SELECT RT.Table_ID 
												FROM reservation R 
												INNER JOIN reservation_table RT ON R.Reservation_ID = RT.Reservation_ID
												WHERE r.Date=(SELECT r1.date FROM reservation r1 WHERE r1.Reservation_ID= ?)
												AND r.status!=3
												AND r.Start_time =(SELECT r1.Start_time FROM reservation r1 WHERE r1.Reservation_ID=?)
												)
												) TABLES ORDER BY Table_ID""",(reservation_id,reservation_id))
		availableTables=cursor.fetchall()
		cursor.execute("""SELECT Table_ID,Capacity,'checked' AS checked FROM res_table 
						WHERE Table_ID IN (SELECT RT.Table_ID FROM reservation_table RT WHERE RT.Reservation_ID =?)""" ,(reservation_id,))
		ReservationTables=cursor.fetchall()
		data=availableTables +ReservationTables
		data.sort(key=mySort)
		con.close()
	return render_template('reservation_tables.html', data=data, form=form, message=message)

@app.route('/reservation_tables', methods=['POST'])
def do_reservation_tables():
	message = ''
	form=reservationTablesForm(request.form)
	selectedTables=request.form.getlist('tables')
	reservation_id=request.form['reservation_id']
	if form.validate():
		con = sqlite3.connect("restaurant.db")
		con.row_factory = sqlite3.Row 
		cursor=con.cursor()
		cursor.execute("""SELECT Persons FROM reservation WHERE Reservation_ID = ? """ ,(reservation_id,))
		requestedPersons = cursor.fetchone()
		person = requestedPersons[0]
		sum = 0
		cursor.execute("""SELECT Table_ID,Capacity FROM (
				SELECT * FROM res_table 
					WHERE Table_ID NOT IN (SELECT RT.Table_ID FROM reservation R 
											INNER JOIN reservation_table RT
												ON R.Reservation_ID = RT.Reservation_ID
											WHERE r.Date=(SELECT r1.date FROM reservation r1 WHERE r1.Reservation_ID= ?)
												AND r.status!=3
											AND r.Start_time =(SELECT r1.Start_time FROM reservation r1 WHERE r1.Reservation_ID=?)) 
					UNION 
					SELECT * FROM res_table 
					WHERE Table_ID IN (SELECT RT.Table_ID FROM reservation_table RT WHERE RT.Reservation_ID =?)
					) TABLES ORDER BY Table_ID""",(reservation_id,reservation_id,reservation_id)) 
		availableTables=cursor.fetchall()

		for sTable in selectedTables:
			iTable = int(sTable)
			capacity = 0
			for t in availableTables:
				if int(t[0]) == iTable:
					capacity= int(t[1])
					break
			if sum == 0:
				sum = capacity
			else:
				sum = sum + capacity - 2

		if sum < person:
			message= message +'Δεν επαρκούν οι θέσεις των τραπεζιών για την συγκεκριμένη κράτηση.'
		else:
			cursor.execute("DELETE FROM reservation_table WHERE Reservation_ID = ?" , (reservation_id,))
			con.commit()
			for table_id in selectedTables:
				cursor.execute("INSERT INTO reservation_table(Table_ID, Reservation_ID) VALUES (?,? )" , (table_id,reservation_id))
				con.commit()
			message ='η κράτηση ενημερώθηκε.'
		con.close()
	else:
		message='Επιλέξτε κάτι'
	return redirect('reservation_tables/'+reservation_id + '/' + message)	

def mySort(e):
	return e['Table_ID']


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
