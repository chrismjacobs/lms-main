import json, time, base64, ast, random
from sqlalchemy import asc, desc
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from app import app, db, bcrypt, mail
from flask_login import current_user, login_required
from forms import *
from models import *
from modelsNEWS import *
from pprint import pprint
from meta import *
from routesGet import getUsers, get_MTFN, get_schedule, get_sources

s3_resource = BaseConfig.s3_resource

S3_LOCATION = schemaList[12]['S3_LOCATION']
S3_BUCKET_NAME = schemaList[12]['S3_BUCKET_NAME']

unitDict = {
        '01' : U011U_NEWS,
        '02' : U012U_NEWS,
        '03' : U013U_NEWS,
        '04' : U014U_NEWS,
        '05' : U021U_NEWS,
        '06' : U022U_NEWS,
        '07' : U031U_NEWS,
        '08' : U032U_NEWS,
        '09' : U033U_NEWS,
        '10' : U041U_NEWS,
        '11' : U042U_NEWS,
        '12' : U043U_NEWS,
        '13' : U051U_NEWS,
        '14' : U052U_NEWS,
        '15' : U053U_NEWS,
        '16' : U061U_NEWS,
        '17' : U062U_NEWS,
        '18' : U063U_NEWS,
        '19' : U071U_NEWS,
        '20' : U072U_NEWS,
        '21' : U073U_NEWS,
        '22' : U081U_NEWS,
        '23' : U082U_NEWS,
        '24' : U083U_NEWS
}


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

@app.route ("/news/make_teams/<string:unit>/<string:number>/", methods=['GET','POST'])
@login_required
def news_project_teams(unit, number):
    if current_user.id != 1:
        return abort(403)

    print('make team unit', unit)
    print('make team number', number)

    project = unitDict[unit]
    print (project, project.query.all())

    #create a dictionary of teams
    attTeams = Attendance_NEWS.query.all()
    teamsDict = {}
    if DEBUG == False:
        for att in attTeams:
            if att.teamnumber in teamsDict:
                teamsDict[att.teamnumber].append(att.username)
            else:
                teamsDict[att.teamnumber] = [att.username]

    print(teamsDict)

    manualTeams = {

        1: ['Chris', 'Test'],
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
    headers = ['', 'Title', 'Warmup_1', 'Warmup_2', 'Part_1', 'Part_2', 'Part_3', 'Part_4', 'Who', 'What', 'When', 'Where', 'Why', 'How']
    for i in range (1, len(headers)):
        audioTag = '----'
        imageTag = '----'
        if 'Title' in headers[i]:
            imageTag = None
        elif 'Part' in headers[i]:
            audioTag = None

        qnaDict[i] = {
            'header' : headers[i],
            'text' : None,
            'user' : None,
            'audioLink' : audioTag,
            'imageLink' : imageTag,
        }
        qnaNotes[i] = {
            'status' : 0,
            'note' : 0
        }
    snlDict = {}
    snlNotes = {}
    for i in range (1, 7):
        snlDict[i] = {
            'sentence' : None,
            'vocab' : None,
            'def' : None,
            'user' : None,
            'audioLink' : None,
            'imageLink' : None,
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
        checkUser = Exams_NEWS.query.filter_by(username=current_user.username).first().username
    except:
        user = Exams_NEWS(username=current_user.username, j1='{}', j2='{}', j3='{}', j4='{}', j5='{}', j6='{}')
        db.session.add(user)
        db.session.commit()

    user = Exams_NEWS.query.filter_by(username=current_user.username).first()

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


@app.route('/updateGrades_news', methods=['POST'])
def updateGrades_news():
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


def get_project_news():

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
                projectDict[unitNumber]['M3'] = section['M3']
                projectDict[unitNumber]['M4'] = section['M4']
        except:
            print('except', sDict[week]['Unit'])
            pass

    pprint(projectDict)

    return projectDict

@app.route ("/news_check/<string:unit>", methods=['GET','POST'])
@login_required
def news_check(unit):
    taList = ['Chris', 'Test']

    if current_user.username not in taList:
        return redirect('home')

    srcDict = get_project_news()
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

    return render_template('news/news_check.html', legend='QNA Check', unit=unit, proString = json.dumps(checkDict))

@app.route ("/news_list", methods=['GET','POST'])
@login_required
def news_list():

    '''
    for user in User.query.all():
        user.extra = 3
        db.session.commit()
    '''

    srcDict = get_project_news()
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
        elif Units_NEWS.query.filter_by(unit=src).count() == 1:
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

    # eUnits = ['01','02']
    eUnits = ['03','04', '05']
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

            if Units_NEWS.query.filter_by(unit=src).count() == 1:
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

    source = srcDict['00']['M2']
    print('SRC', source)

    return render_template('news/news_list.html', legend='News Projects', source=source, proDict=json.dumps(proDict),  examDict=json.dumps(examDict))


def get_team_data(unit, team):
    project = unitDict[unit]
    questions = project.query.filter_by(teamnumber=team).first()
    try:
        teamMembers = ast.literal_eval(questions.username)
    except:
        print('NO TEAM MEMBERS')
        teamMembers = []

    teamDict = {}
    for member in teamMembers:
        try:
            teamDict[member] = S3_LOCATION + User.query.filter_by(username=member).first().image_file
        except:
            teamDict[member] = {}

    project_answers = unitDict[unit].query.filter_by(teamnumber=team).first()

    return {
        'project_answers' : project_answers,
        'teamMembers' : json.dumps(teamDict)
    }

'''Instructor dashboard'''
@app.route ("/news_dash", methods=['GET','POST'])
@login_required
def news_dash():
    taList = ['Chris', 'Test']

    if current_user.username not in taList:
        return redirect('home')

    srcDict = get_project_news()
    pprint(srcDict)
    proDict = { }
    for src in srcDict:
        # check sources against open units in model
        # src = unit
        if Units_NEWS.query.filter_by(unit=src).count() == 1:
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
                                                          'RP' : proj.Ans06,
                                                          'QNA_Ans' : proj.Ans01,
                                                          'SNL_Ans' : proj.Ans02,
                                                          'RP_Ans' : proj.Ans03
                                                          }

    pprint (proDict)

    return render_template('news/news_dash.html', legend='News Dash', proString = json.dumps(proDict))



@app.route ("/news/<string:qs>/<string:unit>/<int:team>", methods=['GET','POST'])
@login_required
def news_setup(qs, unit, team):

    srcDict = get_project_news()
    meta = srcDict['00']
    print(meta)
    data = get_team_data(unit, team)
    project_answers = data['project_answers']
    teamMembers = data['teamMembers']

    if current_user.username == "Chris" or current_user.username == "Test":
        pass
    elif current_user.username not in teamMembers:
        flash('You are not on the team for this project', 'warning')
        return (redirect (url_for('home')))

    if qs == 'qna':
        headers = ['', 'Title', 'Warmup_1', 'Warmup_2', 'Part_1', 'Part_2', 'Part_3', 'Part_4', 'Who', 'What', 'When', 'Where', 'Why', 'How']
        testDict = {}
        for i in range (1, len(headers)):
            audioTag = '----'
            imageTag = '----'
            if 'Title' in headers[i]:
                imageTag = None
            elif 'Part' in headers[i]:
                audioTag = None

            testDict[i] = {
                'header' : headers[i],
                'text' : None,
                'user' : None,
                'audioLink' : audioTag,
                'imageLink' : imageTag,
            }
        html = 'news/news_qna.html'

    if qs == 'snl':
        testDict = {}
        for i in range (1, 7):
            testDict[i] = {
            'sentence' : None,
            'vocab' : None,
            'def' : None,
            'user' : None,
            'audioLink' : None,
            'imageLink' : None,
            }
        html = 'news/news_snl.html'

    if qs == 'rp':
        testDict = {'audio': None}
        for i in range (1, 4):
            testDict[i] = {
            'question' : None,
            'answer' : None,
            'user' : None
            }
        html = 'news/news_rp.html'


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


@app.route('/storeB64_news', methods=['POST'])
def storeB64_news():
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

@app.route('/news_updateStatus', methods=['POST'])
def news_updateStatus():
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

@app.route('/news_updateStudentWork', methods=['POST'])
def news_updateStudentWork():
    unit = request.form ['unit']
    team = request.form ['team']
    mode = request.form ['mode']
    work = json.loads(request.form ['work'])

    proj = unitDict[unit].query.filter_by(teamnumber=team).first()

    status = 'none'

    if mode == 'qna':
        proj.Ans01 = json.dumps(work)
    elif mode == 'snl':
        proj.Ans02 = json.dumps(work)
    elif mode == 'rp':
        proj.Ans03 = json.dumps(work)

    status = mode

    db.session.commit()

    return jsonify({'status' : status})


@app.route('/storeAnswer_news', methods=['POST'])
def storeAnswer_news():
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


@app.route('/updateAnswers_news', methods=['POST'])
def updateAnswers_news():
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
@app.route ("/news_exam/<string:qORs>/<string:unit>/<string:team>", methods=['GET','POST'])
@login_required
def news_exam(qORs, unit, team):

    ## get_team_data will check if user is exam ready or not

    team_data = get_team_data(unit, team)
    teamMembers = team_data['teamMembers']

    if current_user.extra == 3:
        print('exam user')
    elif current_user.username not in teamMembers:
        flash('Exam not ready - Please see instructor', 'warning')
        return redirect(url_for('news_list'))

    srcDict = get_project_news()
    meta = srcDict[unit]

    print('exam', unit, team)


    data = team_data['project_answers']
    print(team_data)
    source = meta['M1']
    print(source)
    try:
        qnaDict = json.loads(data.Ans01)
        snlDict = json.loads(data.Ans02)
        rpString = data.Ans03
        rpDict = json.loads(data.Ans03)
    except:
        print('NO TEAM DATA')
        qnaDict = {}
        snlDict = {}
        rpString = ''
        rpDict = {}

    orderList = ['1','2','3','4','5','6']
    random.shuffle(orderList)
    print('orderList', orderList)
    orderDict = {}
    qnaDictNew = {}
    snlDictNew = {}

    if qnaDict != {}:

        count = 1
        for number in orderList:
            orderDict[count] = [number, snlDict[number]['audioLink']]
            count +=1


        count = 1
        for number in orderList:
            qnaDictNew[count] = qnaDict[number]
            count +=1

        count = 1
        for number in orderList:
            snlDictNew[count] = snlDict[number]
            count +=1



    if qORs == 'qna':
        html = 'news/news_exam_qna.html'
    elif qORs == 'snl' :
        html = 'news/news_exam_lnm.html'
    else:
        html = 'news/news_exam_rp.html'

    return render_template(html, legend='News Exam', title=unit, meta=meta, orderDict=json.dumps(orderDict), qnaString=json.dumps(qnaDictNew), snlString=json.dumps(snlDictNew), rpString=rpString)



@app.route ("/news_grades", methods=['GET','POST'])
@login_required
def news_grades():

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

    exams = Exams_NEWS.query.all()

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


    return render_template('news/news_grades.html', ansString=json.dumps(gradesDict))