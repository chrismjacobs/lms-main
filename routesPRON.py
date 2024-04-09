import json, time, base64, ast, random
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

S3_LOCATION = schemaList[8]['S3_LOCATION']
S3_BUCKET_NAME = schemaList[8]['S3_BUCKET_NAME']

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

unitDict = {
        '01' : U011U_PRON,
        '02' : U012U_PRON,
        '03' : U013U_PRON,
        '04' : U014U_PRON,
        '05' : U021U_PRON,
        '06' : U022U_PRON,
        '07' : U031U_PRON,
        '08' : U032U_PRON,
        '09' : U033U_PRON,
        '10' : U041U_PRON,
        '11' : U042U_PRON,
        '12' : U043U_PRON,
        '13' : U051U_PRON,
        '14' : U052U_PRON,
        '15' : U053U_PRON,
        '16' : U061U_PRON,
        '17' : U062U_PRON,
        '18' : U063U_PRON,
        '19' : U071U_PRON,
        '20' : U072U_PRON,
        '21' : U073U_PRON,
        '22' : U081U_PRON,
        '23' : U082U_PRON,
        '24' : U083U_PRON
}

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
            print(item.username)
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


    return render_template('pro/dashboardpro.html', ansString=json.dumps(totalDict), title='dashboard', SCHEMA=SCHEMA, att=att, MTFN=get_MTFN('grades'))


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

@app.route("/pr_commentSet", methods = ['POST'])
def pr_commentSet():

    newComment = request.form['comment']
    unit = request.form['unit']
    name = request.form['user']
    model = pr_assDict[int(unit)]
    print(unit, name, model)
    studentAns = model.query.filter_by(username=name).first()

    studentAns.Comment = newComment
    db.session.commit()

    return jsonify({'comment' : newComment})

@app.route('/pr_audioUpload', methods=['POST', 'GET'])
def pr_audioUpload():

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



''' CLASS WORK '''

def create_folder(unit, teamnumber, nameRange):
    keyName = (unit + '/' + teamnumber + '/')  #adding '/' makes a folder object
    print (keyName)
    try:
        # use s3_client instead of resource to use head_object or list_objects
        response = s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=keyName)
        print('Folder Located')
    except:
        s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=keyName)
        object = s3_resource.Object(S3_BUCKET_NAME, keyName + str(nameRange) + '.txt')
        object.put(Body='some_binary_data')
        print('Folder Created for', teamnumber, nameRange)
    else:
        print('Create_Folder_Pass')
        pass

    return keyName

@app.route ("/pro/make_teams/<string:unit>/<string:number>/", methods=['GET','POST'])
@login_required
def project_teams(unit, number):
    if current_user.id != 1:
        return abort(403)

    print('make team unit', unit)
    print('make team number', number)

    project = unitDict[unit]
    print (project, project.query.all())

    #create a dictionary of teams
    attTeams = Attendance_PRON.query.all()
    teamsDict = {}
    if DEBUG == False:
        for att in attTeams:
            if att.teamnumber in teamsDict:
                teamsDict[att.teamnumber].append(att.username)
            else:
                teamsDict[att.teamnumber] = [att.username]

    print(teamsDict)

    manualTeams = {

        7: ['Chole', 'Harrison', 'Wendy'],
        #8: ['Chloe', 'Lou', 'Vivi']
        # 2:['Nora','Amy'],
        # 3:['Anita','Bly','T.Y','MAC'],
        # 4:['Clyde','James','Yuri','Linda'],
        # 5:['Beatrix','SEAN','Vivian','Bee'],
        # 6:['Cris','Holly','Frederick','Wendy'],
        # 7:['Bris','laura','Fay','Iris','Maris'],
        # 8:['Jasper','Luna','Nelly','Cyan'],
        # 9:['JELF','Helen ','Mioly','Layla']
        #10: ['Fiona', 'Ann', 'Penny Lai', 'Yui'],
        #20 : ['Chris'],
    }

    '''control which teams are added'''

    if DEBUG == False:
        team_dict = teamsDict
    else:
        team_dict = manualTeams

    # prepare answers for QNA
    qnaDict = {}
    qnaNotes = {}
    for i in range (1, 7):
        qnaDict[i] = {
            'question' : None,
            'answer1' : None,
            'answer2' : None,
            'user' : None,
            'audioLink' : None,
            'imageLink' : '----',
            'imageLink2' : '----',
        }
        qnaNotes[i] = {
            'status' : 0,
            'note' : 0
        }

    snlDict = {}
    snlNotes = {}
    for i in range (1, 7):
        snlDict[i] = {
            'question' : '---',
            'answer1' : None,
            'answer2' : None,
            'user' : None,
            'audioLink' : None,
            'imageLink' : None,
            'imageLink2' : None,
        }
        snlNotes[i] = {
            'status' : 0,
            'note' : 0
        }

    rpDict = {'rpAudio': None}
    rpNotes = {}
    for i in range (1, 4):
        rpDict[i] = {
            'question' : None,
            'answer' : [ None, None, None ],
            'user' : None
        }
        rpNotes[i] = {
            'status' : 0,
            'note' : 0
        }

    #make a list of teams already set up
    teams = []
    for pro in project.query.all():
        teams.append(pro.teamnumber)

    print('teams', teams)

    returnStr = str(team_dict)
    for team in team_dict:
        if team in teams:
            returnStr = 'Error - check table'
            break
        print(unit, team_dict)
        create_folder(unit, str(team), team_dict[team])
        teamStart = project(
            teamnumber=int(team),
            username=str(team_dict[team]),
            Ans01=str(json.dumps(qnaDict)),
            Ans02=str(json.dumps(snlDict)),
            Ans03=str(json.dumps(rpDict)),
            Ans07=str(json.dumps(qnaNotes)),
            Ans08=str(json.dumps(snlNotes)),
            Ans09=str(json.dumps(rpNotes))
            )
        db.session.add(teamStart)
        db.session.commit()

    return returnStr


def midtermGrades():
    try:
        checkUser = Exams_PRON.query.filter_by(username=current_user.username).first().username
    except:
        user = Exams_PRON(username=current_user.username, j1='{}', j2='{}', j3='{}', j4='{}', j5='{}', j6='{}')
        db.session.add(user)
        db.session.commit()

    user = Exams_PRON.query.filter_by(username=current_user.username).first()

    return user

def get_tests(unit, team):
    user = midtermGrades()
    print('USER', user)

    qna = json.loads(user.j1)
    snl = json.loads(user.j2)
    rp = json.loads(user.j3)
    # qna = json.loads(user.j4)
    # snl = json.loads(user.j5)
    # rp = json.loads(user.j6)

    #print(qna)

    qnaCount = 0
    for test in qna:
        # print ('CHECK', qna[test]['unit'], unit ,  qna[test]['team'], team)
        if qna[test]['unit'] == str(unit) and qna[test]['team'] == str(team):
            qnaCount = 1
    snlCount = 0
    for test in snl:
        if snl[test]['unit'] == str(unit) and snl[test]['team'] == str(team):
            snlCount = 1
    rpCount = 0
    for test in rp:
        if rp[test]['unit'] == str(unit) and rp[test]['team'] == str(team):
            rpCount = 1

    return { 'snlCount' : snlCount, 'qnaCount' : qnaCount, 'rpCount' : rpCount }


@app.route('/updateGrades', methods=['POST'])
def updateGrades():
    qORs = request.form ['qORs']
    unit = request.form ['unit']
    team = request.form ['team']
    grade = request.form ['grade']

    user = midtermGrades()

    if qORs == 'qna':
        examDict = json.loads(user.j1)
        # examDict = json.loads(user.j4)
    elif qORs == 'snl':
        examDict = json.loads(user.j2)
        # examDict = json.loads(user.j5)
    elif qORs == 'rp':
        examDict = json.loads(user.j3)
        # examDict = json.loads(user.j6)
        pass

    print('before', examDict)

    entryChecker = True
    for entry in examDict:
        if examDict[entry]['team'] == team and examDict[entry]['unit'] == unit:
            entryChecker = False
            print("entryChecker False")

    if entryChecker:
        count = len(examDict)
        examDict[count+1] = {
            'unit' : unit,
            'team' : team,
            'grade' : grade
            }

        if qORs == 'qna':
            user.j1 = json.dumps(examDict)
            # user.j4 = json.dumps(examDict)
            db.session.commit()
            print('qnaCommit')
        elif qORs == 'snl':
            user.j2 = json.dumps(examDict)
            # user.j5 = json.dumps(examDict)
            db.session.commit()
            print('snlCommit')
        elif qORs == 'rp':
            user.j3 = json.dumps(examDict)
            # user.j6 = json.dumps(examDict)
            db.session.commit()
            print('rpCommit')

    print('after', examDict)

    return jsonify({'grade' : grade})


def get_projects():

    content_object = s3_resource.Object(S3_BUCKET_NAME, 'json_files/sources.json' )
    file_content = content_object.get()['Body'].read().decode('utf-8')
    sDict = json.loads(file_content)  # json loads returns a dictionary
    projectDict = {}
    for week in sDict:
        try:
            if int(sDict[week]['Unit']) >= 0:
                #print('2')
                unitNumber = sDict[week]['Unit']
                projectDict[unitNumber] = {}
                section = sDict[week]
                #projectDict[unitNumber] = sDict[week]

                projectDict[unitNumber]['Title'] = section['Title']
                projectDict[unitNumber]['Date'] = section['Date']
                projectDict[unitNumber]['M1'] = section['M1']
                projectDict[unitNumber]['M2'] = section['M2']
        except:
            print('except', sDict[week]['Unit'])
            pass

    pprint(projectDict)

    return projectDict

@app.route ("/pro_check/<string:unit>", methods=['GET','POST'])
@login_required
def pro_check(unit):
    taList = ['Chris', 'Cherry Mak']

    if current_user.username not in taList:
        return redirect('home')

    srcDict = get_projects()
    title = srcDict[unit]['Title']




    checkDict = { }

    projects = unitDict[unit].query.all()
    for proj in projects:
        print(proj.teamnumber)
        checkDict[proj.teamnumber] = {
            'team' : ast.literal_eval(proj.username),
            'qna_list' : json.loads(proj.Ans01),
            'qna_notes' : json.loads(proj.Ans07),
            'qna_score' : proj.Ans04,
            'snl_list' : json.loads(proj.Ans02),
            'snl_notes' : json.loads(proj.Ans08),
            'snl_score' : proj.Ans05,
            'rp_list' : json.loads(proj.Ans03),
            'rp_notes' : json.loads(proj.Ans09),
            'rp_score' : proj.Ans06,
            }

    pprint (checkDict)

    return render_template('pro/pro_check.html', legend='QNA Check', unit=unit, proString = json.dumps(checkDict))

@app.route ("/pro_list", methods=['GET','POST'])
@login_required
def pro_list():

    '''
    for user in User.query.all():
        user.extra = 3
        db.session.commit()
    '''

    srcDict = get_projects()
    print('srcDict', srcDict)

    unitList = []
    #unitList = ['04', '05', '06', '07','08']
    #unitList = ['01', '02', '03', '04','05', '06']
    #unitList = ['01', '02', '03', '04','05', '06']
    #unitList = ['13', '14', '15', '16','17', '18']
    proDict = {}
    for src in srcDict:
        # check sources against open units in model
        # src == unit
        if src in unitList:
            pass
        elif Units_PRON.query.filter_by(unit=src).count() == 1:
            proDict[src] = {
                'Title' : srcDict[src]['Title'],
                'Team'  : 'Not set up yet',
                'Number' : 0,
                'QTotal' : 0,
                'STotal' : 0,
                'RTotal' : 0,
                'QTest' : 0,
                'STest' : 0,
                'RTest' : 0,
            }

            projects = unitDict[src].query.all()
            for proj in projects:
                tests = get_tests(src, proj.teamnumber)
                if current_user.username in ast.literal_eval(proj.username):
                    proDict[src]['Team'] = proj.username
                    proDict[src]['Number'] = proj.teamnumber
                    proDict[src]['QTotal'] = proj.Ans04
                    proDict[src]['STotal'] = proj.Ans05
                    proDict[src]['RTotal'] = proj.Ans06
                    proDict[src]['QTest'] = tests['qnaCount']
                    proDict[src]['STest'] = tests['snlCount']
                    proDict[src]['RTest'] = tests['rpCount']
                    #pass

    #pprint (proDict)

    examDict = {}

    eUnits = ['01','02']
    for src in eUnits:
        if int(src) > 16: # change to match number of units
            pass
        else:
            examDict[src] = {}
            # try:
            #     teamCheck = int(proDict[src]['Number'])
            #     selector = teamCheck % 2
            #     #print('selector', selector)
            # except:
            #     selector = 0

            if Units_PRON.query.filter_by(unit=src).count() == 1:
                projects = unitDict[src].query.all()

                for proj in projects:

                    if int(proj.teamnumber) > 20:
                        pass
                    elif proDict[src]['Number'] == proj.teamnumber:
                        pass
                    # elif selector == 0 and proj.teamnumber % 2 != 0:
                    #     pass
                    # elif selector != 0 and proj.teamnumber % 2 == 0:
                    #     pass
                    else:
                        QTotal = 0
                        RTotal = 0
                        STotal = 0
                        qNotes = json.loads(proj.Ans07)
                        sNotes = json.loads(proj.Ans08)
                        rNotes = json.loads(proj.Ans09)
                        print(qNotes)
                        for q in qNotes:
                            QTotal += int(qNotes[q]['status'])
                        for s in sNotes:
                            STotal += int(sNotes[s]['status'])

                        examDict[src][proj.teamnumber] = {
                            'QTotal' : QTotal,
                            'STotal' : STotal,
                            'RTotal' : RTotal,
                            'Qscore' : 0,
                            'Sscore' : 0,
                            'Rscore' : 0,
                            }


    user = midtermGrades()
    qna = json.loads(user.j1)
    snl = json.loads(user.j2)
    rp = json.loads(user.j3)
    # qna = json.loads(user.j4)
    # snl = json.loads(user.j5)
    # rp = json.loads(user.j6)
    #print (qna)
    #print (snl)

    for entry in qna:
        unit = qna[entry]['unit']
        team = qna[entry]['team']
        grade = qna[entry]['grade']
        try:
            #print(examDict[unit][int(team)]['Qscore'])
            examDict[unit][int(team)]['Qscore'] = grade
        except:
            print('FAIL QNA')

    for entry in snl:
        unit = snl[entry]['unit']
        team = snl[entry]['team']
        grade = snl[entry]['grade']
        try:
            #print(examDict[unit][int(team)]['Sscore'])
            examDict[unit][int(team)]['Sscore'] = grade
        except:
            print('FAIL QNA')

    for entry in rp:
        unit = rp[entry]['unit']
        team = rp[entry]['team']
        grade = rp[entry]['grade']
        try:
            #print(examDict[unit][int(team)]['Sscore'])
            examDict[unit][int(team)]['Rscore'] = grade
        except:
            print('FAIL RP')


    #'''

    source = srcDict['13']['M2']

    return render_template('pro/pro_list.html', legend='pro Projects', source=source, proDict=json.dumps(proDict),  examDict=json.dumps(examDict))


def get_team_data(unit, team):
    project = unitDict[unit]
    questions = project.query.filter_by(teamnumber=team).first()
    teamMembers = ast.literal_eval(questions.username)

    teamDict = {}
    for member in teamMembers:
        try:
            teamDict[member] = S3_LOCATION + User.query.filter_by(username=member).first().image_file
        except:
            teamDict[member] = None

    project_answers = unitDict[unit].query.filter_by(teamnumber=team).first()

    return {
        'project_answers' : project_answers,
        'teamMembers' : json.dumps(teamDict)
    }

'''Instructor dashboard'''
@app.route ("/pro_dash", methods=['GET','POST'])
@login_required
def pro_dash():
    taList = ['Chris', 'Cherry Mak']

    if current_user.username not in taList:
        return redirect('home')

    srcDict = get_projects()
    pprint(srcDict)
    proDict = { }
    for src in srcDict:
        # check sources against open units in model
        # src = unit
        if Units_PRON.query.filter_by(unit=src).count() == 1:
            proDict[src] = {
                'Title' : srcDict[src]['Title'],
                'Unit' : src,
                'Teams' : {}
            }

            projects = unitDict[src].query.all()
            for proj in projects:
                proDict[src]['Teams'][proj.teamnumber] = {'team' : proj.username,
                                                          'QNA' : proj.Ans04,
                                                          'SNL' : proj.Ans05,
                                                          'RP' : proj.Ans06
                                                          }

    pprint (proDict)

    return render_template('pro/pro_dash.html', legend='Pro Dash', proString = json.dumps(proDict))



@app.route ("/pro/<string:qs>/<string:unit>/<int:team>", methods=['GET','POST'])
@login_required
def pro_setup(qs, unit, team):

    srcDict = get_projects()
    meta = srcDict[unit]
    #print(meta['M1'])

    data = get_team_data(unit, team)
    project_answers = data['project_answers']
    teamMembers = data['teamMembers']

    if current_user.username == "Chris":
        pass
    elif current_user.username not in teamMembers:
        flash('You are not on the team for this project', 'warning')
        return (redirect (url_for('pro_dash')))

    if qs == 'qna':
        testDict = {}
        for i in range (1, 7):
            testDict[i] = {
                'question' : None,
                'answer1' : None,
                'answer2' : None,
                'user' : None,
                'audioLink' : None,
                'imageLink' : '-----',
                'imageLink2' : '-----',
            }
        html = 'pro/pro_qna.html'
        ansDict = project_answers.Ans01
        current_score = project_answers.Ans04

    if qs == 'snl':
        testDict = {}
        for i in range (1, 7):
            testDict[i] = {
                'question' : '----',
                'answer1' : None,
                'answer2' : None,
                'user' : None,
                'audioLink' : None,
                'imageLink' : None,
                'imageLink2' : None,
            }
        html = 'pro/pro_snl.html'
        ansDict = project_answers.Ans02
        current_score = project_answers.Ans05

    if qs == 'rp':
        testDict = {'audio': None}
        for i in range (1, 4):
            testDict[i] = {
            'question' : None,
            'answer' : None,
            'user' : None
            }
        html = 'pro/pro_rp.html'
        ansDict = project_answers.Ans03
        current_score = project_answers.Ans06


    return render_template(html, legend='Questions & Answers',
    meta=meta,
    teamMembers=teamMembers,
    ansDict=ansDict,
    current_score=current_score,
    testDict=str(json.dumps(testDict))
    )

def countTotal(ansOBJ):
    total = 0
    data = json.loads(ansOBJ)
    #print(data)
    for key in data:
        if key == 'rpAudio':
            if data[key] != None:
                total += 1
        else:
            score = True
            for item in data[key]:
                if type(data[key][item]) == list and "" in data[key][item]:
                    score = False
                elif data[key][item] == None:
                    score = False
            if score:
                total += 1

    return total


@app.route('/prostoreB64', methods=['POST'])
def storeB64():
    unit = request.form ['unit']
    team = request.form ['team']
    mode = request.form ['mode']
    b64 = request.form ['b64']
    question = request.form ['question']
    b64data = request.form ['b64data']
    fileType = request.form ['fileType']
    print('STORE B64', mode, b64)
    project = unitDict[unit]
    project_data = project.query.filter_by(teamnumber=team).first()
    if mode == 'rp':
        project_answers = json.loads(project_data.Ans03)
    if mode == 'qna':
        project_answers = json.loads(project_data.Ans01)
    elif mode == 'snl':
        project_answers = json.loads(project_data.Ans02)
    else:
        print('NO MODE FOR B64 STORE')

    if b64 == 'a':
        link = 'audioLink'
        file_key = project_answers[question][link]
    elif b64 == 'i1':
        link = 'imageLink'
        file_key = project_answers[question][link]
    elif b64 == 'i2':
        link = 'imageLink2'
        file_key = project_answers[question][link]
    elif b64 == 'rp':
        link = 'rpAudio'
        file_key = project_answers[link]

    print('PROCESSING: ' + link)
    data = base64.b64decode(b64data)
    if file_key:
        print('file_key_found ', file_key)
        file_key_split = file_key.split('com/')[1]
        s3_resource.Object(S3_BUCKET_NAME, file_key_split).delete()
    else:
        print('no file_key found')

    now = datetime.now()
    time = now.strftime("_%M%S")
    print("time:", time)
    filename = unit + '/' + team + '/' + question + time + '_' + link + '.' + fileType
    fileLink = S3_LOCATION + filename
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=data)

    aORi = ['a', 'i']
    if mode == 'snl':
        project_answers[question][link] = fileLink
        project_answers[question]['user'] = current_user.username
        project_data.Ans02 = json.dumps(project_answers)
        project_data.Ans05 = countTotal(json.dumps(project_answers))
    elif mode == 'qna':
        project_answers[question][link] = fileLink
        project_answers[question]['user'] = current_user.username
        project_data.Ans01 = json.dumps(project_answers)
        project_data.Ans04 = countTotal(json.dumps(project_answers))
    else:
        project_answers[link] = fileLink
        project_answers[question]['user'] = current_user.username
        project_data.Ans03 = json.dumps(project_answers)
        project_data.Ans06 = countTotal(json.dumps(project_answers))

    db.session.commit()

    return jsonify({'question' : question})

@app.route('/pr_updateStatus', methods=['POST'])
def pr_updateStatus():
    unit = request.form ['unit']
    team = request.form ['team']
    mode = request.form ['mode']
    notes = json.loads(request.form ['notes'])

    proj = unitDict[unit].query.filter_by(teamnumber=team).first()

    status = 'none'

    if mode == 'qna':
        proj.Ans07 = json.dumps(notes)
    elif mode == 'snl':
        proj.Ans08 = json.dumps(notes)
    elif mode == 'rp':
        proj.Ans09 = json.dumps(notes)

    status = mode

    db.session.commit()

    return jsonify({'status' : status})


@app.route('/prostoreAnswer', methods=['POST'])
def storeAnswer():
    unit = request.form ['unit']
    team = request.form ['team']
    mode = request.form ['mode']
    question = request.form ['question']
    ansOBJ = request.form ['ansOBJ']
    print('STORE ANSWER', unit, team, mode, question, ansOBJ)

    project = unitDict[unit]
    project_answers = project.query.filter_by(teamnumber=team).first()

    if mode == 'qna':
        project_answers.Ans01 = ansOBJ
        project_answers.Ans04 = countTotal(ansOBJ)
    if mode == 'snl':
        project_answers.Ans02 = ansOBJ
        project_answers.Ans05 = countTotal(ansOBJ)
    if mode == 'rp':
        project_answers.Ans03 = ansOBJ
        project_answers.Ans06 = countTotal(ansOBJ)

    db.session.commit()

    return jsonify({'question' : question})


@app.route('/proupdateAnswers', methods=['POST'])
def updateAnswers():
    unit = request.form ['unit']
    team = request.form ['team']
    mode = request.form ['mode']

    project = unitDict[unit]
    project_answers = project.query.filter_by(teamnumber=team).first()

    if mode == 'qna':
        ansString = str(project_answers.Ans01)
    if mode == 'snl':
        ansString = str(project_answers.Ans02)
    if mode == 'rp':
        ansString = str(project_answers.Ans03)


    return jsonify({'ansString' : ansString})


'''Exam '''
@app.route ("/pro_exam/<string:qORs>/<string:unit>/<string:team>", methods=['GET','POST'])
@login_required
def pro_exam(qORs, unit, team):

    ## get_team_data will check if user is exam ready or not

    team_data = get_team_data(unit, team)
    teamMembers = team_data['teamMembers']

    if current_user.extra == 3:
        print('exam user')
    elif current_user.username not in teamMembers:
        flash('Exam not ready - Please see instructor', 'warning')
        return redirect(url_for('pro_list'))

    srcDict = get_projects()
    meta = srcDict[unit]

    print('exam', unit, team)


    data = team_data['project_answers']
    print(team_data)
    source = meta['M1']
    print(source)
    qnaDict = json.loads(data.Ans01)
    snlDict = json.loads(data.Ans02)
    rpString = data.Ans03
    rpDict = json.loads(data.Ans03)

    orderList = ['1','2','3','4','5','6']
    random.shuffle(orderList)
    print('orderList', orderList)

    count = 1
    orderDict = {}
    for number in orderList:
        orderDict[count] = [number, snlDict[number]['audioLink']]
        count +=1


    count = 1
    qnaDictNew = {}
    for number in orderList:
        qnaDictNew[count] = qnaDict[number]
        count +=1

    count = 1
    snlDictNew = {}
    for number in orderList:
        snlDictNew[count] = snlDict[number]
        count +=1



    if qORs == 'qna':
        html = 'pro/pro_exam_qna.html'
    elif qORs == 'snl' :
        html = 'pro/pro_exam_lnm.html'
    else:
        html = 'pro/pro_exam_rp.html'

    return render_template(html, legend='PRO Exam', title=unit, meta=meta, orderDict=json.dumps(orderDict), qnaString=json.dumps(qnaDictNew), snlString=json.dumps(snlDictNew), rpString=rpString)



@app.route ("/pro_grades", methods=['GET','POST'])
@login_required
def pro_grades():

    gradesDict = {}

    users = User.query.all()

    units = ['13','14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']

    for user in users:
        gradesDict[user.username] = {
            'Student' : {
                'name' :user.username,
                'id' : user.studentID,
                'Status' : user.extra
             }
        }
        for u in units:
            gradesDict[user.username][u] = {
                'team' : 0,
                'QNA' : 0,
                'SNL' : 0,
                'RP' : 0,
                'QNA_check' : 0,
                'SNL_check' : 0,
                'RP_check' : 0,
                'QNA_grades' : [],
                'SNL_grades' : [],
                'RP_grades' : []
            }

    exams = Exams_PRON.query.all()

    models = unitDict # at top of page

    for model in models:
        if int(model) > 12:
            projects = models[model].query.all()
            for proj in projects:
                team = ast.literal_eval(proj.username)
                for stu in team:
                    gradesDict[stu][model]['QNA'] = proj.Ans04
                    gradesDict[stu][model]['SNL'] = proj.Ans05
                    gradesDict[stu][model]['RP'] = proj.Ans06
                    gradesDict[stu][model]['team'] = str(proj.teamnumber)

    for exam in exams:
        #break
        #QNA = json.loads(exam.j1)
        QNA = json.loads(exam.j3)
        for record in QNA:
            entry = QNA[record]
            print(exam.username, entry)
            if entry['team'] == gradesDict[exam.username][entry['unit']]['team']:
                gradesDict[exam.username][entry['unit']]['QNA_check'] = 1
            else:
                gradesDict[exam.username][ entry['unit'] ]['QNA_grades'].append(entry['grade'])

        #SNL = json.loads(exam.j2)
        SNL = json.loads(exam.j4)
        for record in SNL:
            entry = SNL[record]
            print(exam.username, entry)
            if entry['team'] == gradesDict[exam.username][entry['unit']]['team']:
                gradesDict[exam.username][entry['unit']]['SNL_check'] = 1
            else:
                gradesDict[exam.username][ entry['unit'] ]['SNL_grades'].append(entry['grade'])

        #RP = json.loads(exam.j3)
        RP = json.loads(exam.j6)
        for record in RP:
            entry = RP[record]
            print(exam.username, entry)
            if entry['team'] == gradesDict[exam.username][entry['unit']]['team']:
                gradesDict[exam.username][entry['unit']]['RP_check'] = 1
            else:
                gradesDict[exam.username][ entry['unit'] ]['RP_grades'].append(entry['grade'])


    return render_template('pro/pro_grades.html', ansString=json.dumps(gradesDict))