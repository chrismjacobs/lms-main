import json, time, base64
from sqlalchemy import asc, desc
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from app import app, db, bcrypt, mail
from flask_login import current_user, login_required
from forms import *
from models import *
from modelsPRON import *
from pprint import pprint
from meta import *
from routesGet import getUsers, get_MTFN, get_schedule, get_sources

s3_resource = BaseConfig.s3_resource

pr_assDict = [
        '',
        U091U_PRON,
        U092U_PRON,
        U093U_PRON,
        U094U_PRON,
        U101U_PRON,
        U102U_PRON,
        U103U_PRON,
        U104U_PRON
    ]

@app.route ("/dashboardpro")
@login_required
def dashboardpro():
    SCHEMA = getSchema()

    userList = getUsers(SCHEMA)

    srcDict = get_sources()
    for x in srcDict:
        print('source unit', x)



    if current_user.id != 1 and current_user.username != 'Cherry Mak':
        return abort(403)


    period = ['01', '02', '03', '04', '05','06', '07', '08']



    totalDict = {}
    allStudents = userList
    for user in allStudents:
        example = {
                'idNum' : None,
                'user' : None,
                'A01' :None,
                'A02' :None,
                'A03' :None,
                'A04' :None,
                'A05' :None,
                'A06' :None,
                'A07' :None,
                'A08' :None,
                'A09' :None,
                'C' :None,
                'G' :None,
                'device' : ''
                }
        totalDict[user.username] = {
            period[0] : example,
            period[1] : example,
            period[2] : example,
            period[3] : example,
            period[4] : example,
            period[5] : example,
            period[6] : example,
            period[7] : example
        }

    # print(totalDict)

    for unit in period:
        model = pr_assDict[int(unit)]
        answers = model.query.order_by(desc(model.Grade)).all()
        for item in answers:
            device = User.query.filter_by(username=item.username).first().device
            if item.username in totalDict:
                totalDict[item.username][unit] = {
                'idNum' : item.id,
                'user' : item.username,
                'A01' :item.Ans01,
                'A02' :item.Ans02,
                'A03' :item.Ans03,
                'A04' :item.Ans04,
                'A05' :item.Ans05,
                'A06' :item.Ans06,
                'A07' :item.Ans07,
                'A08' :item.Ans08,
                'A09' :item.Ans09,
                'C' :item.Comment,
                'G' :item.Grade,
                'device' : device
                }

    # pprint(totalDict)

    att = getModels()['Attendance_'].query.filter_by(username="Chris").first().teamnumber


    return render_template('instructor/dashboardpro.html', ansString=json.dumps(totalDict), title='dashboard', SCHEMA=SCHEMA, att=att, MTFN=get_MTFN('grades'))


'''##### PRONUNCIATION Assignments ////////'''

@app.route ("/pr_assignments", methods=['GET','POST'])
@login_required
def pr_assignment_list():

    srcDict = get_sources()
    print(srcDict)

    ''' deal with grades '''
    # grades = pr_get_grades(True, False) # ass / unit
    # assGrade = grades['assGrade']
    # recs = grades['assGradRec']
    # maxA = grades['maxA']
    # print ('RECS', recs)

    assDict = {}
    units = getModels()['Units_'].query.all()
    print(units)
    unitIndex = ['01', '02', '03', '04']
    count = 0
    for unit in units:
        unitText = unitIndex[count]
        print(unitIndex[count])
        if unit.uA and unit.uA > 0:
            assDict[unitText] = {
                'Deadline' : srcDict[unitText]['Deadline'],
                'Title' : srcDict[unitText]['Title'],
                'Grade' : 0, #recs[unit]['Grade'],
                'Comment' : '' #: recs[unit]['Comment']
            }
        count += 1

    SCHEMA = getSchema()
    DESIGN = schemaList[SCHEMA]['DESIGN']

    return render_template('units/pr_assignment_list.html', legend='Assignments Dashboard',
    Dict=json.dumps(assDict), title='Assignments', theme=DESIGN)


@app.route('/pr_audioUpload', methods=['POST', 'GET'])
def pr_audioUpload():
    SCHEMA = getSchema()
    S3_LOCATION = schemaList[SCHEMA]['S3_LOCATION']
    S3_BUCKET_NAME = schemaList[SCHEMA]['S3_BUCKET_NAME']

    unit = request.form ['unit']
    type = request.form ['type']
    task = request.form ['task']
    title = request.form ['title']
    audio_string = request.form ['base64']
    ansDict = request.form ['ansDict']

    answers = json.loads(ansDict)
    print(answers)

    srcDict = get_sources()
    date = srcDict[unit]['Date']
    dt = srcDict[unit]['Deadline']
    deadline = datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=1)
    print ('deadline: ', deadline)

    tag = '.mp3'
    if type == 'capture':
        tag = '.mp4'

    print('PROCESSING AUDIO')
    audio = base64.b64decode(audio_string)
    newTitle = S3_LOCATION + 'assignments/' + current_user.username + '/' + title + tag
    filename = 'assignments/' + current_user.username + '/' + title + tag
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=audio)

    model = pr_assDict[int(unit)]
    com = 'in progress...'

    ## add task data
    user = model.query.filter_by(username=current_user.username).first()
    if task == '1' and type == 'record':
        user.Ans01 = newTitle
    if task == '1' and type == 'capture':
        user.Ans02 = newTitle
    if task == '1':
        user.Ans03 = json.dumps(answers[task]['TextData'])

    if task == '2' and type == 'record':
        user.Ans04 = newTitle
    if task == '2' and type == 'capture':
        user.Ans05 = newTitle
    if task == '2':
        user.Ans06 = json.dumps(answers[task]['TextData'])

    if task == '3' and type == 'record':
        user.Ans07 = newTitle
    if task == '3' and type == 'capture':
        user.Ans08 = newTitle
    if task == '3':
        user.Ans09 = json.dumps(answers[task]['TextData'])


    db.session.commit()

    ## check grade
    grade_status = 0
    if user.Ans01 and user.Ans02 and user.Ans03 != '' and user.Ans04 and user.Ans05 and user.Ans06 != '' and user.Ans07 and user.Ans08 and user.Ans09 != '':
        if user.Grade > 0 :
            grade_status = user.Grade
        elif  datetime.now() < deadline:
            user.Grade = 2  # completed on time
            grade_status = 2
            user.Comment = 'Completed on time - Great!'
        else:
            user.Grade = 1  # late start
            grade_status = 1
            user.Comment = 'This assignment has been completed late'
    db.session.commit()

    return jsonify({'title' : newTitle, 'grade' : grade_status})


@app.route("/pr_ass/<string:unit>", methods = ['GET', 'POST'])
@login_required
def pr_ass(unit):
    SCHEMA = getSchema()
    S3_BUCKET_NAME = schemaList[SCHEMA]['S3_BUCKET_NAME']
    S3_LOCATION = schemaList[SCHEMA]['S3_LOCATION']

    srcDict = get_sources()
    source = srcDict[unit]['Materials']['A']


    setting =  getModels()['Units_'].query.filter_by(unit=unit).first().uA

    iList = ['Chris', 'Cherry Wai']

    notInstructor = current_user.username not in iList
    if setting != 1 and notInstructor:
        flash('This assignment is not open yet', 'danger')
        return redirect(request.referrer)


    # models update
    assDict = getInfo()['aModsDict']


    model = pr_assDict[int(unit)]
    print(model)
    count = model.query.filter_by(username=current_user.username).count()
    fields = model.query.filter_by(username=current_user.username).first()

    if count == 0:
        ansDict = {
        'Unit' : unit,
        1 : {
            'AudioData' : None,
            'VideoData' : None,
            'TextData' : ['','']
            },
        2 : {
            'AudioData' : None,
            'VideoData' : None,
            'TextData' : ['','']
            },
        3 : {
            'AudioData' : None,
            'VideoData' : None,
            'TextData' : ['','']
            }
        }

        entry = model(
            username=current_user.username,
            Ans03 = json.dumps(['','']),
            Ans06 = json.dumps(['','']),
            Ans09 = json.dumps(['','']),
            Grade=0, Comment='ready')
        db.session.add(entry)
        db.session.commit()
    elif count == 1:
        ansDict = {
        'Unit' : unit,
        1 : {
            'AudioData' : fields.Ans01,
            'VideoData' : fields.Ans02,
            'TextData' : json.loads(fields.Ans03)
            },
        2 : {
            'AudioData' : fields.Ans04,
            'VideoData' : fields.Ans05,
            'TextData' : json.loads(fields.Ans06)
            },
        3 : {
            'AudioData' : fields.Ans07,
            'VideoData' : fields.Ans08,
            'TextData' : json.loads(fields.Ans09)
            }
        }
    else:
        firstEntry = model.query.filter_by(username=current_user.username).first()
        #model.query.get(firstEntry.id).delete()
        db.session.delete(firstEntry)
        db.session.commit()
        fields = model.query.filter_by(username=current_user.username).first()
        ansDict = {
        'Unit' : unit,
        1 : {
            'AudioData' : fields.Ans01,
            'VideoData' : fields.Ans02,
            'TextData' : json.loads(fields.Ans03)
            },
        2 : {
            'AudioData' : fields.Ans04,
            'VideoData' : fields.Ans05,
            'TextData' : json.loads(fields.Ans06)
            },
        3 : {
            'AudioData' : fields.Ans07,
            'VideoData' : fields.Ans08,
            'TextData' : json.loads(fields.Ans09)
            }
        }


    context = {
        'SCHEMA' : SCHEMA,
        'count' : count,
        'fields' : fields,
        'unit' : unit,
        'source' : source,
        #'speechModel' : speechModel,
        'ansDict' : json.dumps(ansDict),
        'siteName' : S3_BUCKET_NAME,
        'title' : 'Unit_' + unit
    }
    print(context)

    return render_template('units/pr_assignment_vue.html', **context)



@app.route('/pronstoreB64', methods=['POST'])
def pronstoreB64():

    b64data = request.form ['b64data']
    fileType = request.form ['fileType']
    fileName = request.form ['fileName']

    user = fileName.split('_capture_')[1]
    title = fileName.split('_capture_')[0]
    unit = title.split('_')[0]
    part = title.split('_')[1]


    print('PROCESSING VIDEO: ' + fileName)
    data = base64.b64decode(b64data)

    SCHEMA = getSchema()
    S3_LOCATION = schemaList[SCHEMA]['S3_LOCATION']
    S3_BUCKET_NAME = schemaList[SCHEMA]['S3_BUCKET_NAME']

    filename = 'assignments/' + user + '/' + title + '.' + fileType
    fileLink = S3_LOCATION + filename
    print(fileLink)
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=data)


    model = pr_assDict[int(unit)].query.filter_by(username=user).first()

    if int(part) == 1:
        model.Ans02 = fileLink
    elif int(part) == 2:
        model.Ans05 = fileLink
    elif int(part) == 3:
        model.Ans08 = fileLink
    else:
        print('Ans Error', int(part))

    db.session.commit()

    return jsonify({'result' : True})