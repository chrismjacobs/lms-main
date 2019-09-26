import sys, boto3, random, base64, os, secrets, httplib2
from sqlalchemy import asc, desc 
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, abort, jsonify  
from app import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from forms import *   
from models import *
try:
    from aws import Settings    
    s3_resource = Settings.s3_resource  
    S3_LOCATION = Settings.S3_LOCATION
    S3_BUCKET_NAME = Settings.S3_BUCKET_NAME  
    COLOR_SCHEMA = Settings.COLOR_SCHEMA
except:
    s3_resource = boto3.resource('s3')
    S3_LOCATION = os.environ['S3_LOCATION'] 
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME'] 
    COLOR_SCHEMA = os.environ['COLOR_SCHEMA'] 

@app.route("/webrtc3", methods = ['GET', 'POST'])
def webrtc3():       
    return render_template('instructor/gersonrosales3.html')    


@app.route ("/about")
@login_required 
def about():     
    about = Sources.query.filter_by(unit='00').filter_by(part='1').first().notes
    return render_template('instructor/about.html', about=about, siteName=S3_BUCKET_NAME)

@app.route("/course", methods = ['GET', 'POST'])
@login_required
def course():
    course = Course.query.order_by(asc(Course.date)).all()   
    return render_template('instructor/course.html', course=course)


@app.route("/openSet/<string:unit>/<string:part>", methods = ['POST'])
def openSet(unit,part):
    status = request.form['status' + unit + part]
    openSetModel = Sources.query.filter_by(unit=unit).filter_by(part=part).first()

    openSetModel.openSet = status
    db.session.commit()        

    return redirect(url_for('unit_list')) 


@app.route("/sources", methods = ['GET', 'POST'])
@login_required
def sources():
    sources = Sources.query.order_by(asc(Sources.unit)).order_by(asc(Sources.part)).all()   
    return render_template('instructor/sources.html', sources=sources)

@app.route ("/teams")
@login_required 
def teams():  
    if current_user.id != 1:
        return abort(403)       

    try:
        teamcount = Attendance.query.filter_by(username='Chris').first().teamcount
    except:
        flash('Attendance not open yet', 'danger')
        return redirect(url_for('home')) 
    
    if teamcount > 0: 
        attDict = {}  #  teamnumber = fields, 1,2,3,4 names
        for i in range(1, teamcount+1):
            teamCall = Attendance.query.filter_by(teamnumber=i).all()
            attDict[i] = teamCall    
    # if team count set to zero ---> solo joining
    else:
        attDict = {}
        users = User.query.order_by(asc(User.studentID)).all()        
        for user in users:
            attStudent = Attendance.query.filter_by(username=user.username).first() 
            if attStudent:
                attDict[user.username] = [user.studentID, attStudent.date_posted]
            else:
                attDict[user.username] = [user.studentID, 0]

    return render_template('instructor/teams.html', attDict=attDict, teamcount=teamcount)  


@app.route ("/s3console")
@login_required 
def s3console():   
    if current_user.id != 1:
        return abort(403)     
    
    my_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    files = my_bucket.objects.all()        

    return render_template('instructor/s3console.html', my_bucket=my_bucket, files=files, location=S3_LOCATION)  


@app.route('/upload/<string:assignment>', methods=['POST', 'GET'])
def upload(assignment):
    file = request.files['file']
    fn = file.filename
    file_name = current_user.username + '_' + fn + '_' + assignment + '.mp3'   
    my_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    my_bucket.Object(file_name).put(Body=file)

    return redirect(request.referrer)


@app.route("/commentSet/<string:unit>/<string:name>", methods = ['POST'])
def commentSet(unit,name):
    newComment = request.form['comment' + unit + name]
    mods = Info.modDictAss
    studentAns = mods[unit].query.filter_by(username=name).first()

    studentAns.Comment = newComment
    db.session.commit()   

    return jsonify({'new' : newComment})

@app.route ("/dashboard")
@login_required 
def dashboard():  
    if current_user.id != 1:
        return abort(403)
    ### replace this with modDictAss
    ansDict = Info.ansDict
    
    for item in ansDict:
        model = ansDict[item][0]
        answers = model.query.order_by(desc(model.Grade)).all() # find that item model and query it
        count = len(answers)
        ansDict[item].append(answers)
        ansDict[item].append(count)
        #ansDict[item][1] = answers
        #ansDict[item][2] = count
        # dictionary set to model, answer, number of answers

    print (ansDict)
    ansRange = len(ansDict)       
    
    return render_template('instructor/dashboard.html', ansDict=ansDict, ansRange=ansRange)  

@app.route ("/students")
@login_required 
def students():
    if current_user.id != 1:
        return abort(403)  
    
    students = User.query.order_by(asc(User.studentID)).all()

    maxUni = Grades.query.order_by(desc(Grades.units)).first().units
    maxAss = Grades.query.order_by(desc(Grades.assignments)).first().assignments
    maxAtt = Grades.query.order_by(desc(Grades.attend)).first().attend    


    lastChats = {}  ##dictionary  name : last chat string version , color code number x3
    for student in students:
        name = student.username
        
        chat = ChatBox.query.filter_by(username=name).all()        
        number = len(chat)
        d = datetime.today() - timedelta(days=7)
        if number > 0:            
            lastChat = chat[number-1]
            if lastChat.date_posted > d:
                stringChat = str(lastChat).split(',')[1]
                lastChats[name]= [ stringChat, 0,0,0]  ##add to dictionary name : lastchat then add color values           
            else: 
                lastChats[name] = [0,0,0,0]
        else:      
            lastChats[name] = [0,0,0,0]
        
        fieldsGrade = Grades.query.filter_by(username=name).first() 
        #set up colors
        try:
            lastChats[name][1] = fieldsGrade.attend/maxAtt
        except:
            lastChats[name][1] = 0
        try:
            lastChats[name][2] = fieldsGrade.units/maxUni
        except:
            lastChats[name][2] = 0 
        try:
            lastChats[name][3] = fieldsGrade.assignments/maxAss
        except:
            lastChats[name][3] = 0     

    ## FormFill Task
    attDict = {}
    for student in students:        

        attendance = Attendance.query.filter_by(studentID=student.studentID).first()
                                
        if attendance == None:
            attDict[student.studentID] = ['true', 'true', 'Absent', 0, 0]
        elif attendance.attend == 'Late':
            attDict[student.studentID] = ['true', 'false', 'Late', attendance.unit, attendance.id]
        elif attendance.attend == '2nd Class':
            attDict[student.studentID] = ['true', 'false', '2nd Class', attendance.unit, attendance.id]
        elif attendance.attend == 'On time':         
            attDict[student.studentID] = ['false', 'false', 'On time', attendance.unit, attendance.id]        
        else:
            attDict[student.studentID] = ['false', 'false', 'On time', 0, attendance.id]
    
    
    timeDict = {
        0 : ['_6','_7'],
        1 : ['_8','_9'], 
        2 : ['_6','_7'],
        3 : ['_3','_4'],
        4 : ["document.getElementById('DDList", "_1').checked=true;"]
        }

    formFill = []
    for key in attDict:  
        if attDict[key][0] == 'true':  
            formFill.append(timeDict[4][0] + key + timeDict[int(COLOR_SCHEMA)][0] + timeDict[4][1])
        if attDict[key][1] == 'true':
            formFill.append(timeDict[4][0] + key + timeDict[int(COLOR_SCHEMA)][1] + timeDict[4][1] )
        
    
    return render_template('instructor/students.html', students=students, LOCATION=S3_LOCATION, 
    lastChats=lastChats, formFill=formFill, attDict=attDict)  


@app.route ("/inchat/<string:user_name>", methods = ['GET', 'POST'])
@login_required 
def inchat(user_name):
    if current_user.id != 1:
        return abort(403)
    form = Chat()     
    dialogues = ChatBox.query.filter_by(username=user_name).all()
     
    if form.validate_on_submit():
        chat = ChatBox(username = user_name, response=form.response.data, chat=form.chat.data)      
        db.session.add(chat)
        db.session.commit()  
        return redirect(url_for('inchat', user_name=user_name))
    else:
        form.name.data = current_user.username
        form.response.data = ""
        form.chat.data = ""
        image_file = S3_LOCATION + User.query.filter_by(username=user_name).first().image_file            
      
      
    image_chris = S3_LOCATION + User.query.filter_by(id=1).first().image_file

    return render_template('instructor/inchat.html', form=form, dialogues=dialogues, name=user_name, image_chris=image_chris, image_file=image_file)


@app.route("/attend_int", methods = ['GET', 'POST'])
@login_required
def att_int():
    if current_user.id != 1:
        return abort(403)
    form = AttendInst()

    openData = Attendance.query.filter_by(username='Chris').first()

    if openData:    
        if form.validate_on_submit():
            openData.attend = form.attend.data 
            openData.teamnumber = form.teamnumber.data 
            openData.teamsize = form.teamsize.data 
            openData.teamcount = form.teamcount.data 
            openData.unit =  form.unit.data        
            db.session.commit()  
              
            db.session.commit()
            flash('Attendance has been updated', 'secondary') 
            return redirect(url_for('att_team')) 
        else:
            form.username.data = 'Chris'
            form.studentID.data = '100000000'
            try:
                form.attend.data = openData.attend
                form.teamnumber.data = openData.teamnumber
                form.teamsize.data = openData.teamsize
                form.teamcount.data = openData.teamcount
                form.unit.data = openData.unit
                
            except: 
                pass 
    else:
        flash('Attendance not started', 'secondary') 
        return redirect(request.referrer)  

    return render_template('user/attInst.html', form=form, status=openData.teamnumber)  
