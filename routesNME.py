import sys, boto3, random, base64, os, secrets, time, datetime, json
from sqlalchemy import asc, desc, func, or_
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from app import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from forms import *
from models import *
import ast
from pprint import pprint
from routesUser import get_grades, get_sources
from random import shuffle

from meta import *
s3_resource = BaseConfig.s3_resource
s3_client = BaseConfig.s3_client


def create_folder(unit, teamnumber, nameRange):

    SCHEMA = getSchema()
    S3_LOCATION = schemaList[SCHEMA]['S3_LOCATION']
    S3_BUCKET_NAME = schemaList[SCHEMA]['S3_BUCKET_NAME']

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


'''Instructor dashboard'''
@app.route ("/nme_dash", methods=['GET','POST'])
@login_required
def nme_dash():
    taList = ['Chris']

    if current_user.username not in taList:
        return redirect('home')

    #srcDict = get_projects()
    #pprint(srcDict)
    nmeDict = {}

    for proj in projectDict:
        data = projectDict[proj].query.all()
        print('DATA', data)
        nmeDict[proj] = {}
        for entry in data:
            print(entry)

            nmeDict[proj][entry.username] = {
                'novel' : json.loads(entry.Ans01),
                'sums' : json.loads(entry.Ans02),
                'recs' : json.loads(entry.Ans03),
                'c' : entry.Comment
                }

    ## pprint (nmeDict)

    return render_template('nme/nme_dash.html', legend='NME Dash', nmeString = json.dumps(nmeDict))


'''### novels '''

def getTeam():
    user = User.query.filter_by(username=current_user.username).first()
    team = user.extra
    if not team:
        team = 100
    return team

@app.route ("/nme_novels", methods=['GET','POST'])
@login_required
def nme_novels():
    print('TEAM', getTeam())

    novels = ['01', '02', '03']
    names = []

    for u in User.query.filter_by(extra=getTeam()).all():
        print(u.username)
        names.append(u.username)

    completed = 0
    nCount = 0
    nDict = {}
    for n in novels:
        project = projectDict[n].query.filter_by(Grade=getTeam(), username=current_user.username).first()
        if project:
            nCount +=1
            nDict[n] = {}
            nDict[n]['novel'] = json.loads(project.Ans01)
            nDict[n]['sums'] = 0
            nDict[n]['status'] = project.Comment

            for c in json.loads(project.Ans02):
                nDict[n]['sums'] += 1

            if project.Comment == '2':
                completed += 1

            nDict[n]['recs'] = 0
            recs = json.loads(project.Ans03)
            print(recs)

            ## check if any null in each recording
            for rec in recs:
                noneChecker = True
                if len(recs[rec]) == 0:
                    noneChecker = False
                else:
                    for key in recs[rec]:
                        if key == 'words':
                            if None in recs[rec][key]:
                                noneChecker = False
                        else:
                            print(recs[rec][key])
                            if recs[rec][key] == None:
                                noneChecker = False
                if noneChecker:
                    nDict[n]['recs'] += 1

    nString = json.dumps(nDict)

    print(json.dumps(names))

    return render_template('nme/nme_novels.html', completed=completed, nCount=nCount, nString=nString, names=json.dumps(names), legend='NME Projects')


@app.route ("/nme_exams", methods=['GET','POST'])
@login_required
def nme_exams():
    names = ['Chris', 'William ']

    if current_user.username in names:
        pass
    else:
        pass
        # flash('Not open yet', 'danger')
        # return (redirect (url_for('home')))


    user = Exams.query.filter_by(username=current_user.username).first()

    if user:
        pass
    else:
        print('set user')
        examDict = {
            'vocab': 0,
            'listening': 0,
            'reading': 0,
            'summary': 0
        }
        userSet = Exams(username=current_user.username, j1=json.dumps(examDict))
        db.session.add(userSet)
        db.session.commit()
        user = Exams.query.filter_by(username=current_user.username).first()


    eString = user.j1

    return render_template('nme/nme_exams.html', eString=eString, legend='NME Reading Exams')


@app.route ("/nme_reading_score", methods=['GET','POST'])
@login_required
def nme_reading_score():
    test = request.form ['test']
    grade = request.form ['grade']

    user = Exams.query.filter_by(username=current_user.username).first()

    examDict = json.loads(user.j1)

    examDict[test] = grade

    user.j1 = json.dumps(examDict)
    db.session.commit()

    return jsonify({ 'result': 'good'})


@app.route ("/nme_vocab", methods=['GET','POST'])
@login_required
def nme_vocab():

    novels = ['01', '02', '03']

    vCount = 1
    vDict = {}
    vIndex = []
    for n in novels:
        project = projectDict[n].query.filter_by(username=current_user.username).first()
        if project:
            work = json.loads(project.Ans02)
            for c in work:
                print(work[c])
                for w in work[c]['newWords']:
                    vDict[vCount] = work[c]['newWords'][w]
                    vIndex.append(vCount)
                    vCount +=1

    print(len(vDict))

    finalDict = {}

    count = 1
    random.shuffle(vIndex)

    for w in vIndex:
        if count <= 20:
            finalDict[count] = vDict[w]
            count += 1


    vString = json.dumps(finalDict)


    return render_template('nme/nme_vocab.html', vString=vString, legend='NME Vocab Test')


@app.route ("/nme_reading", methods=['GET','POST'])
@login_required
def nme_reading():

    texts = U061U.query.filter_by(username='test1').first()
    textss = U061U.query.filter_by(username='Chris').first()

    textDict = {
        1: texts.Ans01,
        2: texts.Ans02,
        3: texts.Ans03,
        4: texts.Ans04,
        5: texts.Ans05,
        6: texts.Ans06,
        7: texts.Ans07,
        8: texts.Ans08,
        9: textss.Ans01,
        10: textss.Ans02,
        11: textss.Ans03,
        12: textss.Ans04,
        13: textss.Ans05,
        14: textss.Ans06,
        15: textss.Ans07,
        16: textss.Ans08,
    }

    rearrDict = {}
    count = 1

    arrangeCount = []

    for tex in textDict:
        print('TEXT')

        splitsO = textDict[tex].split('.')



        splitsR = textDict[tex].split('.')
        random.shuffle(splitsR)

        for line in splitsO:
                # print(line)
                if len(line) < 3:
                    splitsO.pop(splitsO.index(line))
                    splitsR.pop(splitsR.index(line))

        blanks = []
        for e in splitsO:
            blanks.append(None)

        splitsLen = len(splitsO)

        rearrDict[tex] = {
            'first': splitsO[0],
            'last': splitsO[splitsLen-1],
            'order': splitsO,
            'reorder': splitsR,
            'blanks': blanks
        }

    items = list(rearrDict.items())
    print(items)

    random.shuffle(items)

    newDict = {}
    count = 1
    for i in items:
        newDict[count] = i[1]
        count += 1


    rString = json.dumps(newDict)

    ## pprint(newDict)
    return render_template('nme/nme_reading.html', rString=rString, legend='NME Rearrange Test')


@app.route ("/nme_listening", methods=['GET','POST'])
@login_required
def nme_listening():

    texts = U041U.query.all()

    listDict = {}
    count = 1

    listCount = []

    for tex in texts:
        print('TRY')
        print(tex, texts)
        te = json.loads(tex.Ans01)
        for entry in te:
            print(te)
            t = te[entry]
            print(t, type(t))
            print(count)
            listDict[count] = {}
            listDict[count]['passOriginal'] = t['passage']
            random.shuffle(t['words'])
            listDict[count]['words'] = t['words']
            newPassage = t['passage']
            tCount = 1

            wordDict = {}

            for word in t['words']:
                word_index = newPassage.find(word)
                wordDict[word_index] = word

            sort = sorted(wordDict)  ### makes a list of indexs

            print(wordDict, sort)
            wordList = []
            for idx in sort:
                print(idx, tCount, wordDict[idx])
                wordList.append(wordDict[idx])
                newPassage = newPassage.replace(wordDict[idx], '___' + str(tCount) + '___')
                #print(newPassage)
                tCount += 1

            listDict[count]['passGaps'] = newPassage
            listDict[count]['wordList'] = wordList
            listDict[count]['wordsNull'] = [None, None, None, None]


            ansPassage = t['passage'].split('.')
            splitPassage = t['passage'].split('.')

            for line in splitPassage:
                print(line)
                if len(line) < 3:
                    splitPassage.pop(splitPassage.index(line))
                    ansPassage.pop(ansPassage.index(line))



            random.shuffle(splitPassage)
            listDict[count]['passSplit'] = splitPassage

            sentences = []
            for p in range(len(splitPassage)):
                sentences.append(None)

            listDict[count]['sentences'] = sentences
            listDict[count]['passAns'] = ansPassage
            listDict[count]['audio'] = t['audio']

            listCount.append(count)
            count += 1


    random.shuffle(listCount)
    finalCount = 1
    pairCount = 1

    finalDict = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {}
    }

    for entry in listCount:
        if finalCount == 7: ## change to 6
            break

        finalDict[finalCount][pairCount] = listDict[entry]

        if pairCount == 1:
            pairCount = 2
        else:
            pairCount = 1
            finalCount += 1




    lString = json.dumps(finalDict)

    return render_template('nme/nme_listening.html', lString=lString, legend='NME Listening Test')

@app.route ("/nme_summary", methods=['GET','POST'])
@login_required
def nme_summary():

    texts = U051U.query.all()

    sumDict = {}

    for tex in texts:

        sums = { 1: tex.Ans01, 2: tex.Ans02, 3: tex.Ans03, 4: tex.Ans04 }

        nums = [1,2,3,4]
        blanks = [None, None, None, None]

        random.shuffle(nums)

        sumDict[tex.username] = {
            'sums': sums,
            'nums': nums,
            'blanks': blanks
        }


    keys = list(sumDict.keys())
    random.shuffle(keys)

    newDict = {}

    for key in keys:
        newDict[key] = sumDict[key]


    sString = json.dumps(newDict)

    return render_template('nme/nme_summary.html', sString=sString, legend='NME Summary Test')


@app.route ("/addNovel", methods=['GET','POST'])
@login_required
def addNovel():
    print('ADD_NOVEL')
    novel = request.form ['novel']
    number = json.loads(novel)['number']

    print('NOVEL', novel)
    print('NUMBER', number)


    for novels in projectDict:
        if int(number) == int(novels):
            PROJECT = projectDict[novels]

    sums = {}
    recs = {1:{}, 2:{}, 3:{}}
    feeds = {}

    check = PROJECT.query.filter_by(Grade=getTeam(), username=current_user.username).first()

    if check:
        print('CHECK')
        check.Ans01 = novel
        db.session.commit()
    else:
        print('ENTRY')
        entry = PROJECT(username=current_user.username, Grade=getTeam(), Ans01=novel, Ans02=json.dumps(sums), Ans03=json.dumps(recs), Ans04=json.dumps(feeds))
        db.session.add(entry)
        db.session.commit()

    return jsonify({'nValue' : novel, 'nKey':number })


'''### summaries '''

@app.route ("/sum/<string:index>", methods=['GET','POST'])
@login_required
def nme_sum(index):


    project = projectDict[index].query.filter_by(username=current_user.username).first()
    novel = json.loads(project.Ans01)
    sums = json.loads(project.Ans02)

    html = 'nme/nme_sums.html'

    return render_template(html, legend='Chapter Summaries', nString=project.Ans01, sString=project.Ans02)


@app.route ("/addSum", methods=['GET','POST'])
@login_required
def addSum():
    print('ADD_SUM')
    nString = request.form ['novel']
    cString = request.form ['chapter']

    novel = json.loads(nString)
    chapter = json.loads(cString)
    novel_number = novel['number']
    chap_number = chapter['number']

    for novels in projectDict:
        if int(novel_number) == int(novels):
            project = projectDict[novels].query.filter_by(username=current_user.username).first()

    print(project, project.Ans02, novel, chapter, novel_number, chap_number)

    current_sum = json.loads(project.Ans02)
    current_sum[chap_number] = chapter
    project.Ans02 = json.dumps(current_sum)
    db.session.commit()

    return jsonify({'cObj' : json.dumps(current_sum)})

@app.route ("/updateSum", methods=['GET','POST'])
@login_required
def updateSum():
    print('UPDATE_SUM')
    number = request.form ['number']
    name = request.form ['name']
    summary = request.form ['summary']
    novel = request.form ['novel']

    ## get student data
    entry = projectDict[novel].query.filter_by(username=name).first()
    sums = json.loads(entry.Ans02)
    print(summary, sums)
    sums[str(number)]['summary'] = summary
    entry.Ans02 = json.dumps(sums)
    entry.Ans03 = '{"1": {}, "2": {}}'
    db.session.commit()

    return jsonify({'success' : True})

@app.route ("/updateComment", methods=['GET','POST'])
@login_required
def updateComment():
    print('UPDATE_COMM')
    name = request.form ['name']
    novel = request.form ['novel']

    ## get student data
    entry = projectDict[novel].query.filter_by(username=name).first()
    entry.Comment = '2'
    db.session.commit()

    return jsonify({'success' : True})

'''### feedback '''

@app.route ("/rec/<string:index>", methods=['GET','POST'])
@login_required
def nme_recording(index):

    rCount = 0
    rDict = {}

    project = projectDict[index].query.filter_by(username=current_user.username).first()
    if project:
        rDict = json.loads(project.Ans03)
        rCount +=1

    html = 'nme/nme_recs.html'

    return render_template(html, legend='Add Recordings', index=index, rString=json.dumps(rDict), rCount=rCount)


@app.route ("/addRec", methods=['GET','POST'])
@login_required
def addRec():
    print('ADD_REC_DETAILS')
    novel = request.form ['novel']
    rec = request.form ['rec']
    details = request.form ['details']
    print(details)

    project = projectDict[novel].query.filter_by(username=current_user.username).first()

    rDict = json.loads(project.Ans03)
    rDict[rec] = json.loads(details)
    project.Ans03 = json.dumps(rDict)
    db.session.commit()

    return jsonify({'details' : details})



''' ## performance '''

@app.route ("/effort_dash", methods=['GET','POST'])
@login_required
def nme_effort_dash():

    #U001 used for movie dict
    # eList = U001U.query.all()

    eDict = {}

    # for e in eList:
    #     eDict[e.username] = json.loads(e.Ans01)

    html = 'nme/nme_effort_dash.html'

    return render_template(html, legend='Course Performance', eString=json.dumps(eDict))


@app.route ("/effort", methods=['GET','POST'])
@login_required
def nme_effort():

    survey = U012U.query.filter_by(username=current_user.username).first()

    if not survey:
        obj = json.dumps({})
        entry = U012U(username=current_user.username, Ans01=obj, Ans02=obj, Ans03=obj, Ans04=obj, Ans05=obj, Ans06=obj, Ans07=obj, Ans08=obj)
        db.session.add(entry)
        db.session.commit()

    survey = U012U.query.filter_by(username=current_user.username).first()

    html = 'nme/nme_performance.html'

    return render_template(html, legend='Course Performance', eString=json.dumps(survey.Ans01))

@app.route ("/addSurvey", methods=['GET','POST'])
@login_required
def addSurvey():
    print('ADD_SURVEY')
    eString = request.form ['reflection']
    reflection = json.loads(eString)

    survey = U012U.query.filter_by(username=current_user.username).first()

    if survey:
        records = json.loads(survey.Ans01)
    else:
        start = U012U(username=current_user.username, Ans01=json.dumps({}))
        db.session.add(start)
        db.session.commit()
        survey = U012U.query.filter_by(username=current_user.username).first()
        records = json.loads(survey.Ans01)

    records[reflection['date']] = reflection

    survey.Ans01 = json.dumps(records)
    db.session.commit()

    return jsonify({'msg' : 'Reflection added'})


@app.route('/nme_storeB64', methods=['POST'])
def storeB64():

    b64data = request.form ['b64data']
    fileType = request.form ['fileType']
    novel = request.form ['novel']
    rec = request.form ['rec']

    project = projectDict[novel].query.filter_by(username=current_user.username).first()
    rDict = json.loads(project.Ans03)
    print(type(rec), rec)
    print(rDict)
    try:
        file_key = rDict[int(rec)]['audio']
        print('file_key_found ', file_key)
        file_key_split = file_key.split('com/')[1]
        s3_resource.Object(S3_BUCKET_NAME, file_key_split).delete()
    except:
        print('no file_key found')

    now = datetime.now()
    time = now.strftime("_%M%S")
    print("time:", time)

    print('PROCESSING AUDIO')
    audio = base64.b64decode(b64data)

    filename = current_user.username + '/' + novel + '/' + rec + time + '.mp3'
    audioLink = S3_LOCATION + filename
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=audio)

    rDict[rec]['audio'] = audioLink
    project.Ans03 = json.dumps(rDict)
    db.session.commit()

    return jsonify({'audioLink' : audioLink})



