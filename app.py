from datetime import datetime
from time import time
from flask import Flask, flash, render_template ,request, redirect, session, url_for
from sqlalchemy import false, null, true
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sac'
db = SQLAlchemy(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
app.secret_key='djkahsdkjh'

class userlogin(db.Model):
    id = db.Column(db.String(100), unique=True, primary_key=True,nullable = False)
    password = db.Column(db.String(100), nullable = False)

class user(db.Model):
    usernaams = db.Column(db.String(100), nullable = False)
    i_d = db.Column(db.String(100), nullable = False , primary_key = True , unique = True)
    phone_num = db.Column(db.String(100), nullable = False)
    e__mail = db.Column(db.String(100), nullable = False)
    a_ddress = db.Column(db.String(100), nullable = False)
    hostel__name = db.Column(db.String(100), nullable =  False)
    room__no = db.Column(db.String(100), nullable = False)
    father_phone_no = db.Column(db.String(100), nullable =False)
    blood_group = db.Column(db.String(100), nullable = False)
    addhar_no = db.Column(db.String(100), nullable = False)
    alternate_phoneno = db.Column(db.String(100), nullable = False)
    course = db.Column(db.String(100), nullable = False) 

class notices(db.Model):
    s_no = db.Column(db.Integer, nullable =False, primary_key = True)
    dat_e = db.Column(db.String(100), nullable =False)
    topic =  db.Column(db.String(100), nullable =False)
    notice =  db.Column(db.String(150), nullable =False)
    by_who =  db.Column(db.String(100), nullable = True)
    tim_e =  db.Column(db.String(25), nullable =False)
    
class admin(db.Model):
    admin_user = db.Column(db.String(100), unique=True, primary_key=True,nullable = False)
    password = db.Column(db.String(100) , nullable = False)

class Contact(db.Model):
    full_name = db.Column(db.String(100), nullable = False)
    e_mail = db.Column(db.String(100), primary_key= True, nullable =False)
    massage = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(100), nullable = False)
    phone_no = db.Column(db.Integer, nullable = False)


class hostel_leave_form(db.Model):
    name = db.Column(db.String(50), nullable = False)
    student_id = db.Column(db.String(50),primary_key= True , nullable = False)
    email = db.Column(db.String(100),  nullable =False)
    reason = db.Column(db.String(100),  nullable =False)
    destination = db.Column(db.Text, nullable = False)
    date_to_leave = db.Column(db.DateTime, nullable = False)
    date_to_ariv = db.Column(db.DateTime, nullable = False)
    time_to_leave = db.Column(db.DateTime, nullable = False)
    time_to_ariv = db.Column(db.DateTime, nullable = False)
    outing_type = db.Column(db.String(30), nullable = False)
    city = db.Column(db.String(100), nullable = False)
    state = db.Column(db.String(50), nullable = False)
    pin_code = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), default = 'Pending')

class Cmplnrpt(db.Model):
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, primary_key = True)
    id = db.Column(db.String(20), nullable = False)
    departement = db.Column(db.String(20), nullable = False)
    hostel_name = db.Column(db.String(30), nullable = False)
    room_no = db.Column(db.Integer, nullable = False)
    cmpln = db.Column(db.String(100), nullable = False)
    solution = db.Column(db.String(100), nullable = False)



@app.route("/")
def homeStudent():
    return render_template('login.html')

@app.route('/home/<id>')
def home(id):
    if 'username' in session and id == session['username']:
        flash('Welcome back')
        lapplication = hostel_leave_form.query.filter_by(student_id = id).first()
        getnotice = notices.query.all()
        if lapplication is not None:
            return render_template('index.html', username = session['username'], lapplication = lapplication, getnotices = getnotice)
        else:
            return render_template('index.html', username = session['username'], lapplication = 'hide',getnotices = getnotice)
    return redirect(url_for('homeStudent'))


@app.route("/login", methods=['POST', 'GET'])
def loginStudent():
    if request.method == 'POST':
        id = request.form.get('usernaam')
        paSSword = request.form.get('password')
        chk = userlogin.query.filter_by(id = id).first()
        if(chk is None):
            flash('Invalid input')
            return render_template('login.html')  
        else:
            if(chk.id == id):
                if chk.password == paSSword:
                    session["username"] = id
                    return redirect(url_for('home',id = id))
                else:
                    flash('Wrong Password')
                    return render_template('login.html')
            else:
                flash('Wrong username')
                return render_template('login.html')


@app.route("/wardenlogin", methods=['POST', 'GET'])
def warden_login():
    if request.method == 'POST':
        userName = request.form.get('ad_user')
        paSSword = request.form.get('pass')
        chk = admin.query.filter_by(admin_user = userName).first()
        if(chk is None):
            flash('Invalid Username')
            return render_template('warden_login.html')
        else:
            if(chk.admin_user == userName):
                if(chk.password == paSSword):
                    session["username"] = userName
                    return redirect(url_for('warden_page', username = session["username"]))
                else:
                    flash('Wrong password ')
                    return render_template('warden_Login.html')
            else:
                flash('Wrong username ')
                return render_template('warden_Login.html')


@app.route("/warden_profile/<username>")
def warden_page(username):
    if 'username' in session:
        allhldata = hostel_leave_form.query.all()
        return render_template('warden_profile.html', username = session['username'],allhldatas = allhldata)
    return redirect(url_for('loginWarden'))

@app.route("/warden_profile/approve/<username>" , methods = ['POST','GET'])
def hlapprove(username):
    if 'username' in session:
        if request.method == 'POST':
            id = request.form.get('id').upper()
            if request.form['aprv'] == 'Approve':
                apv =  hostel_leave_form.query.filter_by(student_id = id).first()
                apv.status = 'Approve'
                db.session.commit()
                return redirect(url_for('warden_page',username = id))
            elif request.form['aprv'] == 'Cancel':
                apv = hostel_leave_form.query.filter_by(student_id = id).first()
                apv.status = 'Cancel'
                db.session.commit()
                return redirect(url_for('warden_page ',username = id))
    return redirect(url_for('loginWarden'))

@app.route("/home/delete/<username>")
def dlt(username):
    if 'username' in session:
        delt = hostel_leave_form.query.filter_by(student_id = username).first()
        db.session.delete(delt)
        db.session.commit()
        return redirect(url_for('home',id = username))


@app.route("/warden_logout")
def warden_logout():
    session.pop('username', None)
    return redirect(url_for('loginWarden'))



@app.route("/logout/<username>")
def logout(username):
    session.pop('username', None)
    return redirect(url_for("homeStudent"))


@app.route("/loginWarden")
def loginWarden():
    return render_template('warden_Login.html')

#  COMPLAIN REPORT SECTION START 

@app.route("/complain")
def complain():
    if 'username' in session:
        return render_template('complain.html' , username = session['username'])
    return redirect(url_for('homeStudent'))

@app.route("/submitreport", methods= ['POST','GET'])
def submitReport():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            id  = request.form.get('id')
            dept = request.form.get('dept')
            hostelnaam = request.form.get('hostel_name')
            room_no = request.form.get('room_no')
            cmpl = request.form.get("cmpl")
            sol = request.form.get('sol')
            rptcmp = Cmplnrpt(name = name, email = email,id = id, departement = dept, hostel_name = hostelnaam, room_no = room_no, cmpln = cmpl, solution = sol)
            db.session.add(rptcmp)
            db.session.commit()
            flash("Successfull")
        return redirect(url_for("complain"))
    return redirect(url_for("homeStudent"))

#  COMPLAIN REPORT SECTION END

@app.route("/rule/<username>")
def rule(username):
    if 'username' in session:
        return render_template('rules.html', username = session['username'])
    return redirect(url_for('homeStudent'))

# CONTACT FORM AREA START

@app.route("/contact/<username>")
def contact(username):
    if 'username' in session:
        return render_template('contact.html' , username = session['username'])

@app.route("/contactgoto" , methods=['POST','GET'])
def contactsubmit():
    if 'username' in session:
        if request.method == 'POST':
            full_name = request.form.get('fullname')
            e_mail = request.form.get('email')
            massage = request.form.get('msg')
            city = request.form.get('city')
            phoneno = request.form.get('phoneno')
            entry = Contact(full_name = full_name, e_mail =e_mail, massage= massage, city = city, phone_no = phoneno)
            db.session.add(entry)
            db.session.commit()
            flash('SUCCESSFULL')
            return redirect(url_for('contact'))
        else:
            flash("Try again")
            return render_template('contact.html')

# CONTACT FORM AREA START END

@app.route("/home/notice/<username>")
def notice(username):
    if 'username' in session:
        getnotice = notices.query.all()
        return render_template('Notice_page.html', username = session['username'],getnotices = getnotice)
    return redirect(url_for('homeStudent'))

@app.route("/menu")
def messmenu():
    if 'username' in session:
        return render_template('Menu.html', username = session['username'])
    return redirect(url_for('homeStudent'))


# HOSTEL LEAVE APPLICATION START

@app.route("/hostel_leave")
def hostel_leave():
    if 'username' in session:
        return render_template('Hostel_leave.html', username = session['username'])
    return redirect(url_for('homeStudent'))

@app.route("/hostel_leaveform", methods=['POST','GET'])
def leaveformSubmit():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form.get('nam')
            student_id = request.form.get('id')
            email  = request.form.get('email')
            reason = request.form.get('reason')
            destination = request.form.get('destination')
            date_to_leave = request.form.get('d2go')
            date_to_ariv = request.form.get('d2come')
            time_to_leave = request.form.get('t2go')
            time_to_ariv = request.form.get('t2come')
            outing_type = request.form.get('outing_type')
            city = request.form.get('city')
            state = request.form.get('state')
            pin_code = request.form.get('pincode')
            address = request.form.get('address')
            outingapplication = hostel_leave_form(name = name, student_id = student_id, email = email, reason = reason,destination = destination, date_to_leave = date_to_leave, date_to_ariv = date_to_ariv, time_to_leave = time_to_leave, time_to_ariv = time_to_ariv, outing_type = outing_type, city = city, state = state, pin_code = pin_code, address = address)
            db.session.add(outingapplication)
            db.session.commit()
            flash('SUCCESSFULL')
            return redirect(url_for('hostel_leave'))
        return redirect(url_for('homeStudent'))

# HOSTEL LEAVE APPLICATION END

@app.route("/lost_and_found")
def lost_and_found():
    if 'username' in session:
        return render_template('lost_and_found.html', username = session['username'])
    return redirect(url_for('homeStudent'))

@app.route("/fee_detail")
def fee_detail():
    if 'username' in session:
        return render_template('fee_detail.html', username = session['username'])
    return redirect(url_for('homeStudent'))

@app.route("/profile/<username>")
def profile(username):
    if 'username' in session:
        pdetail = user.query.filter_by(i_d = session['username']).first()
        return render_template('profile.html', username = session['username'], pdetail = pdetail)
    return redirect(url_for('homeStudent'))

@app.route('/home/attendence/<username>')
def attendence(username):
    if 'username' in session:
        return render_template('attandance.html', username = username)

@app.route('/warden_profile/notice_submit/<username>' , methods = ['POST','GET'])
def noticesubmit(username):
    if 'username' in session:
        if request.method == 'POST':
            dat = request.form.get('date')
            by = request.form.get('by')
            hedline = request.form.get('heading')
            notic = request.form.get('notice')
            now = datetime.now()
            entr = notices(dat_e = dat, by_who = by, topic = hedline, notice = notic, tim_e = now.strftime("%H:%M:%S"))
            db.session.add(entr)
            db.session.commit()
            return redirect(url_for('warden_page', username = session['username']))
    return redirect(url_for('loginWarden'))

@app.route('/warden_profile/notice' , methods = ['POST','GET'])
def warden_notice():
    if 'username' in session:
        getnotice = notices.query.all()
        return render_template('warden_notice_page.html', username = session['username'],getnotices = getnotice)
    return redirect(url_for('loginWarden'))

app.run(debug=True)

