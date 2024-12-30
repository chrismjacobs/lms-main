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

        6: ['Cindy Wang', 'Sean', 'Raven'],
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


def newsExamGrades():
    try:
        checkUser = Exams_NEWS.query.filter_by(username=current_user.username).first().username
    except:
        user = Exams_NEWS(username=current_user.username, j1='{}', j2='{}', j3='{}', j4='{}', j5='{}', j6='{}')
        db.session.add(user)
        db.session.commit()

    user = Exams_NEWS.query.filter_by(username=current_user.username).first()

    return user

def get_tests(unit, team):
    user = newsExamGrades()
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


@app.route('/updateGradesNews', methods=['POST'])
def updateGradesNews():
    qORs = request.form ['qORs']
    unit = request.form ['unit']
    team = request.form ['team']
    project = request.form ['project']
    update = request.form ['update']
    gradeSNL = request.form ['gradeSNL']
    gradeART = request.form ['gradeART']
    gradeWH = request.form ['gradeWH']
    warmupAns = json.loads(request.form ['warmupAns'])
    stage = request.form ['stage']

    user = newsExamGrades()

    isMidterm = False
    unitList = Units_NEWS.query.all()
    uCount = 0
    for u in unitList:
        uCount += 1

    if  uCount <= 4:
        isMidterm = True

    if qORs == 'qna' and isMidterm:
        examDict = json.loads(user.j1)
    elif qORs == 'qna' and not isMidterm:
        examDict = json.loads(user.j4)

    print('before', examDict)

    newEntry = True
    currentEntry = {
            'unit' : unit,
            'team' : team,
            'gradeSNL' : 6,
            'gradeWH' : 6,
            'gradeART' : 1,
            'warmupAns' : warmupAns,
            'stage' : stage,
            'project' : 'None'
        }
    for entry in examDict:
        print(team, unit)
        print(examDict[entry]['team'], examDict[entry]['unit'])
        if examDict[entry]['team'] == team and examDict[entry]['unit'] == unit:
            newEntry = False
            if int(update) == 1:
                examDict[entry] = {
                'unit' : unit,
                'team' : team,
                'gradeSNL' : gradeSNL,
                'gradeWH' : gradeWH,
                'gradeART' : gradeART,
                'warmupAns' : warmupAns,
                'stage' : stage,
                'project' : project
                }
            currentEntry = examDict[entry]
            print("newEntry False")

    if newEntry:
        count = len(examDict)
        examDict[count+1] = {
            'unit' : unit,
            'team' : team,
            'gradeSNL' : gradeSNL,
            'gradeWH' : gradeWH,
            'gradeART' : gradeART,
            'warmupAns' : warmupAns,
            'stage' : stage,
            'project' : project
            }

    if int(update) == 1:
        if qORs == 'qna' and isMidterm:
            user.j1 = json.dumps(examDict)
            db.session.commit()
            print('qnaCommit Midterm')

        if qORs == 'qna' and not isMidterm:
            user.j4 = json.dumps(examDict)
            db.session.commit()
            print('qnaCommit Final')




    print('after', examDict)

    return jsonify({'entry' : currentEntry})


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

    eUnits = []
    for u in Units_NEWS.query.all():
        if u.uA == 1:
            eUnits.append(u.unit)


    # eUnits = ['03','04', '05']
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
                            'Qscore' : 0,
                            'project' : 'New Project'
                            }


    user = newsExamGrades()
    qna = json.loads(user.j1)


    for entry in qna:
        unit = qna[entry]['unit']
        team = qna[entry]['team']
        gradeSNL = qna[entry]['gradeSNL']
        gradeWH = qna[entry]['gradeWH']
        stage = qna[entry]['stage']
        project = qna[entry]['project']
        try:
            #print(examDict[unit][int(team)]['Qscore'])
            examDict[unit][int(team)]['Qscore'] = stage
            examDict[unit][int(team)]['project'] = project
        except:
            print('FAIL QNA')



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
    if current_user.username == 'Test2':
        project_answers = {}
        teamMembers = []
        ansDict = {}
        current_score = 0
    else:
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
        if current_user.username != 'Test2':
            ansDict = project_answers.Ans01
            current_score = project_answers.Ans04

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
        if current_user.username != 'Test2':
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
        html = 'news/news_rp.html'
        if current_user.username != 'Test2':
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

    if current_user.extra == 5:
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

    orderListSNL = ['1','2','3','4','5','6']
    random.shuffle(orderListSNL)
    print('orderList', orderListSNL)
    orderDictSNL = {}

    orderListWH = ['1','2','3','4','5','6']
    random.shuffle(orderListWH)
    print('orderList', orderListWH)
    orderDictWH = {}

    # 5Ws + H
    whDict = {
        1 : qnaDict['8'],
        2 : qnaDict['9'],
        3 : qnaDict['10'],
        4 : qnaDict['11'],
        5 : qnaDict['12'],
        6 : qnaDict['13'],
    }

    # Article
    artDict = {
        1 : qnaDict['4'],
        2 : qnaDict['5'],
        3 : qnaDict['6'],
        4 : qnaDict['7']
    }

    print(whDict)

    if snlDict != {}:
        count = 1
        for number in orderListSNL:
            orderDictSNL[count] = [number, snlDict[number]['audioLink']]
            count +=1

    if whDict != {}:
        count = 1
        for number in orderListWH:
            orderDictWH[count] = [number, whDict[int(number)]['text']]
            count +=1


    if qORs == 'qna':
        html = 'news/news_exam_qna.html'
    elif qORs == 'snl' :
        html = 'news/news_exam_lnm.html'
    else:
        html = 'news/news_exam_rp.html'

    return render_template(html, legend='News Exam',
                           title=unit,
                           meta=meta,
                           orderStringSNL=json.dumps(orderDictSNL),
                           orderStringWH=json.dumps(orderDictWH),
                           qnaString=json.dumps(qnaDict),
                           snlString=json.dumps(snlDict),
                           whString=json.dumps(whDict),
                           artString=json.dumps(artDict),
                        )




@app.route ("/grades_news", methods=['GET','POST'])
@login_required
def grades_news():
    SCHEMA = getSchema()

    semester = int(User.query.filter_by(username='Chris').first().semester)

    gradesDict = {}
    completeDict = {}

    users = getUsers(SCHEMA)

    for user in users:
        gradesDict[user.username] = {
            'Status' : user.extra,
            'Name' : user.username,
            'ID' : user.studentID,
            'Total' : 0,
            'units' : 0,
            'uP' : 0,
            'asses' : 0,
            'aP' : 0,
            'tries1' : 0,
            'pscore1' : 0,
            'tries2' : 0,
            'pscore2' : 0,
            'exam1' : 0,
            'exam2' : 0,
            'rscore1' : '',
            'rscore2' : '',
            'blurs' : ''
        }

    attendance = getModels()['Attendance_'].query.all()

    for a in attendance:
        if a.username in gradesDict:
            gradesDict[a.username]['Name'] += ' ='

    MT_marker = False
    ### set max grades


    return render_template('news/news_grades2.html', SCHEMA=SCHEMA, title='Grades', ansString=json.dumps(gradesDict), compString=json.dumps(completeDict))



@app.route ("/news_grades", methods=['GET','POST'])
@login_required
def news_grades():

    gradesDict = {}

    SCHEMA = getSchema()

    users = getUsers(SCHEMA)

    units = []
    for u in Units_NEWS.query.all():
        if u.uA == 1:
            units.append(u.unit)

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
                'Projects': [],
                'Listening': [],
                'Info': [],
                'Warmup': [],
            }

    exams = Exams_NEWS.query.all()

    models = unitDict # at top of page

    for model in models:
        if int(model) > 0 and int(model) < 4:
            projects = models[model].query.all()
            for proj in projects:
                team = ast.literal_eval(proj.username)
                for stu in team:
                    gradesDict[stu][model]['QNA'] = proj.Ans04
                    gradesDict[stu][model]['SNL'] = proj.Ans05
                    gradesDict[stu][model]['team'] = str(proj.teamnumber)

    for exam in exams:
        #break
        #QNA = json.loads(exam.j1)
        QNA = json.loads(exam.j1)
        user = exam.username
        print(user, QNA)

        for record in QNA:

            entry = QNA[record]
            unit = entry['unit']
            print(record, user, entry)
            gradesDict[user][unit]['Projects'].append(entry['project'])
            gradesDict[user][unit]['Listening'].append(int(entry['gradeSNL']))
            gradesDict[user][unit]['Info'].append(int(entry['gradeWH']))
            gradesDict[user][unit]['Warmup'].append(entry['warmupAns'])



    return render_template('news/news_grades.html', ansString=json.dumps(gradesDict))