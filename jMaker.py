
from pprint import pprint
import os
import json
import ast
from meta import BaseConfig

s3_resource = BaseConfig.s3_resource
GS_KEY_ID = BaseConfig.GS_KEY_ID
CODE_STRING = BaseConfig.CODE_STRING
DEBUG = BaseConfig.DEBUG


import gspread
from oauth2client.service_account import ServiceAccountCredentials


def accessSS(sheet):

    GS_KEY = "-----BEGIN PRIVATE KEY-----\n" + CODE_STRING + "==\n-----END PRIVATE KEY-----\n"
    CLIENT_ID = "110416274979850152373"
    # https://github.com/burnash/gspread

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    json_dict = {
        "type": "service_account",
        "project_id": "testrec",
        "private_key_id": GS_KEY_ID,
        "private_key": "-----BEGIN PRIVATE KEY-----\n" + CODE_STRING + "==\n-----END PRIVATE KEY-----\n",
        "client_email": "lmsexams@testrec.iam.gserviceaccount.com",
        "client_id": CLIENT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lmsexams%40testrec.iam.gserviceaccount.com"
    }

    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_dict, scope)
    client = gspread.authorize(creds)

    sheets = client.open(sheet)
    print(sheets)

    return sheets


globalSem = 1

folder = [
        'blank',            #0
        "json_files/FRD1/",  #1
        "json_files/FRD2/",  #2
        "json_files/WPE1/",  #3
        "json_files/WPE2/",  #4
        "json_files/FOOD/", #5
        "json_files/ICC/",  #6
        "json_files/PENG/", #7
        "json_files/PRON/",  #8
        "json_files/DUB/",  #9
        "json_files/WRITE/",  #10
        "json_files/LNC/",  #11
        "json_files/NEWS/",  #12
    ]

buckets = [
        'blank',       #0
        "reading-lms",  #1
        "reading-lms2",  #2
        "workplace-lms",  #3
        "workplace-lms2",  #4
        "food-lms", #5
        "icc-lms", #6
        "peng-lms", #7
        "pron-lms", #8
        "nme-lms", #9
        "writing-lms", #10
        "culture-lms", #11
        "news-lms", #12
        ]

courseDict = {
        'FRD1' : 1,
        'FRD2' : 2,
        'WPE1' : 3,
        'WPE2' : 4,
        'FOOD' : 5,
        'ICC' : 6,
        'PENG' : 7,
        'PRON' : 8,
        'DUB' : 9,
        'WRITE' : 10,
        'LNC' : 11,
        'NEWS' : 12
        }

def make_sources(course, courseCode):
    if globalSem == 1:
        sheets = accessSS('jMakerFall')
    else:
        sheets = accessSS('jMakerSpring')

    print(sheets)

    jDict = {}
    ## WPE is sheets(0)
    sources = sheets.get_worksheet(course)
    keys = sources.col_values(1)
    row = sources.row_values(1)
    totalCols = len(row)
    totalRows = len(keys)
    for c in range(1, totalCols):
        # print(c)
        values = sources.col_values(c+1)
        jDict[c] = {}
        for i in range(0, totalRows):
            # print(i, jDict[c])
            jDict[c][keys[i]] = values[i]

    #jDoc = json.dumps(jDict)

    if DEBUG:
        jfold = "static/json_files/" + courseCode + "/sources.json"

        with open(jfold, 'w') as json_file:
            json.dump(jDict, json_file)

        putJson(2, course)
    else:
        putJsonHeroku(2, course, jDict)

    return 'Make Sources ' + str(course) + ' ' + str(courseCode)


def make_exam(courseCode, unit, courseName):
    sheets = accessSS('eMaker')


    print('CHECK', courseName, unit)

    jString = 'exam.json'
    kString = 'json_files/exam.json'


    workSheetOrder = {
        'FRD1': {
            '1-1-2' : 1,
            '1-3-4' : 2,
            '1-5-6' : 3,
            '1-7-8' : 4,
        },
        'FRD2': {
            '2-1-2' : 9,
            '2-3-4' : 10,
            '2-5-6' : 11,
            '2-7-8' : 12,
        },
        'WPE1': {
            '1-1-2' : 5,
            '1-3-4' : 6,
            '1-5-6' : 7,
            '1-7-8' : 8,
        },
        'WPE2': {
            '2-1-2' : 13,
            '2-3-4' : 14,
            '2-5-6' : 15,
            '2-7-8' : 16,
        },
        'ICC': {
            '1-1-2' : 17,
            '1-3-4' : 18,
            '1-5-6' : 19,
            '1-7-8' : 20,
        }
    }


    try:
        content_object = s3_resource.Object( buckets[courseCode], kString )
        file_content = content_object.get()['Body'].read().decode('utf-8')
        examDict = json.loads(file_content)  # json loads returns a dictionary
    except:
        print('EXCEPT', courseName,  kString)
        examDict = {}

    print('examDict', examDict)

    sheetSelect = workSheetOrder[courseName][unit]
    print('sheet', sheetSelect)
    examList = sheets.get_worksheet(sheetSelect)

    #all lines
    allValues = examList.get_all_values()
    #print('allValues', allValues)

    examDict[unit] = {}
    examDictUnit = examDict[unit]


    for line in allValues:
        print(line[0])
        if line[0] in examDictUnit:
            examDictUnit[line[0]][line[1]] = line[2].split('/')
            print(line[2].split('/'))
        else:
            examDictUnit[line[0]]= {}
            examDictUnit[line[0]][line[1]] = line[2].split('/')
            print(line[2].split('/'))


    pprint(examDict)
    # file 4 = exam.json
    putJson(4, courseCode)

    if DEBUG:
        jfold = "static/json_files/" + courseName + "/" + jString
        with open(jfold, 'w') as json_file:
            #pprint(vocabDict)
            json.dump(examDict, json_file)

        putJson(4, courseCode)
    else:
        putJsonHeroku(2, courseCode, examDict)


    return 'Make Exams ' + str(courseName) + ' ' + str(courseCode) + ' ' + str(unit)

def make_vocab(course, courseCode):
    print('MAKE VOCAB')

    ## rearrange sheets for FRD and WPE
    vocab_json = 'vocab.json'
    image_folder = 'images/'


    sheets = accessSS('vMaker')

    vocabDict = {}

    vocabList = sheets.get_worksheet(course)
    allValues = vocabList.get_all_values()

    headers = allValues[0]

    print('HEADERS', headers)

    vocabDict = {}

    # make all units
    for line in allValues:
        if line[0] == 'Unit':
            pass
        else:
            unit = line[0].strip()
            vocabDict[unit] = {}

    # add all parts
    for line in allValues:
        if line[0] == 'Unit':
            pass
        else:
            unit = line[0].strip()
            part = line[1].strip()
            vocabDict[unit][part] = {}

    for line in allValues:
        if line[0] == 'Unit':
            pass
        else:
            unit = line[0].strip()
            part = line[1].strip()
            ques = line[2].strip()
            vocabDict[unit][part][ques] = {}
            for i in range(3, len(headers)):
                if line[i] != '':
                    if headers[i] == 'c':
                        vocabDict[unit][part][ques][headers[i]] = line[i].split('/')
                    elif headers[i] == 'i':
                        print(buckets[course], image_folder, line[i])
                        imageRef = 'https://' + buckets[course] + '.s3-ap-northeast-1.amazonaws.com/' + image_folder + line[i] + '.PNG'
                        vocabDict[unit][part][ques][headers[i]] = imageRef
                    else:
                        vocabDict[unit][part][ques][headers[i]] = line[i].strip()


    if DEBUG:
        jfold = 'static/json_files/' + courseCode + '/' + vocab_json

        with open(jfold, 'w') as json_file:
            #pprint(vocabDict)
            json.dump(vocabDict, json_file)

        # file 3 = vocab.json
        putJson(3, course)
    else:
        putJsonHeroku(3, course, vocabDict)


    #pprint(vocabDict)

    return 'Make Vocab ' + str(course) + ' ' + str(courseCode)


def putJson(file, course):
    print ('put MetaFile', file, course)

    fileList = [
        'blank',         #0
        "meta.json",     #1
        "sources.json",  #2
        'vocab.json',     #3
        'exam.json',    #4
        ]

    print(folder[course], fileList[file])
    string = "static/" + folder[course] + fileList[file]
    print(string)


    with open(string, "r") as f:
        jload = json.load(f)

    key = 'json_files/' + fileList[file]
    bucket = buckets[course]
    print('BUCKET', bucket)
    jstring = json.dumps(jload)
    s3_resource.Bucket(bucket).put_object(
        Key=key, Body=jstring)

    print('json put in bucket location', bucket, key)
    return [bucket, key]

def putJsonHeroku(file, course, data):
    print ('put MetaFile', file, course, data)

    fileList = [
        'blank',         #0
        "meta.json",     #1
        "sources.json",  #2
        'vocab.json',     #3
        'exam.json',    #4
        ]


    key = 'json_files/' + fileList[file]
    bucket = buckets[course]
    jstring = json.dumps(data)
    s3_resource.Bucket(bucket).put_object(
        Key=key, Body=jstring)

    print('json put in bucket location', bucket, key)
    return [bucket, key]


def get_ids(course, courseCode):
    sheets = accessSS('idMaker')
    idList = sheets.get_worksheet(course)
    students = idList.col_values(1)
    print(students)

    ifold = "static/ids.json"

    with open(ifold, "r") as f:
        iload = json.load(f)

    iload[courseCode.lower()] = students

    with open(ifold, 'w') as json_file:
        json.dump(iload, json_file)

    ##putJson(1, course, None)

    return 'Make IDs'


def actions(c, act):


    course = courseDict[c]
    result = 'None'

    if act == 'src' :
        result = make_sources(course, c)
    elif act == 'vcb' :
        result = make_vocab(course, c)
    elif act == 'ids' :
        result = get_ids(course, c)
    elif act == 'put' :
        result = putJson(1, course, None)
    elif act == 'exam' :
        num = '1'
        if '2' in c:
            num = '2'

        result = make_exam(course, num + '-7-8', c)
    else:
        result = 'no command'
    print('ACTION COMPLETE ' + str(result))

    return result


c = 'FRD2'
act = 'vcb'
go = 9
''' reset WPE2 exam '''

if go > 0:
    actions(c, act)

# actions('FRD1', act)
# actions('FRD2', act)
# actions('WPE1', act)
# actions('WPE2', act)
# actions('PENG', act)
# actions('FOOD', act)
# actions('PRON', act)
# actions('WRITE', act)
