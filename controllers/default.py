import os
import extract
import preprocess
import plot_histograms as ph

def index():
    return dict(rows = 'Within Index')

def findPercentageByRollNo(rollNo):
    rows = db(db.students.rollNo.contains(rollNo)).select()
    return rows[0].percentage

def findPercentageByName(name):
    rows = db(db.students.name.contains(name)).select()
    return rows[0].percentage


def studentname():
    form = FORM('Enter Your name:',
              INPUT(_name='name', requires=IS_NOT_EMPTY(error_message='this field cannot be empty')),
              INPUT(_type='submit'))
    if form.process().accepted:
        redirect(URL('default','studentSummary', args=form.vars.name.upper()))
    
    return dict(form=form)

def studentSummary():
    name = request.args(0,cast=str)
    name = name.replace('_',' ')

    rows = db(db.students.name.contains(name)).select()

    return dict(name=name, rows = rows)

def avgCollgPercentage():    
    query = db.students.percentage.sum() / db.students.rollNo.count()
    rows = db().select(
                         db.students.colleges_id,   
                         query,
                         db.students.percentage.max(),
                         db.students.rollNo.count(),
                         orderby = ~query,
                         groupby = db.students.colleges_id)  
    return dict(rows = rows)

def college():
    
    form = SQLFORM.factory(Field('choose_college', requires=IS_IN_DB(db, 'colleges.id', '%(name)s')), formstyle='bootstrap', _class='form-horizontal')

    if form.process().accepted:
        college_id =  form.vars.choose_college
        redirect(URL('collegeSummary', args = college_id))

    return dict(form = form)

def collegeSummary():

    college_id = request.args(0,cast=int)
    name = db(db.colleges.id==college_id).select()[0]['name']

    subjAvg = db(db.students.colleges_id == college_id).select(db.students.rollNo.count(), db.students.subj1.sum(),
                                                                db.students.subj2.sum(), db.students.subj3.sum(), db.students.subj4.sum(),
                                                                db.students.subj5.sum(), db.students.subj6.sum(), db.students.subj7.sum(),
                                                                db.students.subj8.sum(), db.students.subj9.sum(), db.students.subj10.sum(),
                                                                db.students.subj11.sum())
    Avg = (subjAvg[0]['_extra']['SUM(students.subj1)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj2)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj3)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj4)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj5)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj6)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj7)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj8)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj9)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj10)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj11)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'])

    ranks = db(db.students.colleges_id == college_id).select(orderby=~db.students.percentage)

    # return dict(collegename=collegename, subjAvg = subjAvg, ranks=ranks[:5])
    return dict(Avg = Avg, name=name, ranks=ranks[:5])

    



def buildDB():

	# clean the data file at private/filename
    noisy_file = os.path.join(request.folder, 'private','027__BTECH__6TH SEM.txt')
    clean_file = os.path.join(request.folder, 'private','cleanFile.txt')
    preprocess.cleanData(noisy_file, clean_file)


    # extract college information
    lines = preprocess.readFile(clean_file)
    colleges = extract.extract_data(lines)

    #insert into table colleges
    for name in colleges.keys():
    	db.colleges.insert(name=name)

    # insert into table students
    for name in colleges.keys():
        for student in colleges[name].students:

            credits = (4,4,4,4,4,4,1,1,1,1,1)
            total_credits = 0
            for i in xrange(len(credits)):
                total_credits = total_credits + credits[i]

            percentage = (credits[0]*int(student.marks[0]) + credits[1]*int(student.marks[1]) +  credits[2]*int(student.marks[2]) +
                         credits[3]*int(student.marks[3]) + credits[4]*int(student.marks[4]) + credits[5]*int(student.marks[5]) +
                         credits[6]*int(student.marks[6]) + credits[7]*int(student.marks[7]) + credits[8]*int(student.marks[8]) +
                         credits[9]*int(student.marks[9]) + credits[10]*int(student.marks[10]))

            percentage = (percentage * 1.0) / total_credits

            if percentage < 50.0:
                continue

            collegeid = db(db.colleges.name == name).select()[0]['id']
            db.students.insert(colleges_id = collegeid, rollNo = student.rollNo[1:], name = student.name,
                           subj1 = int(student.marks[0]), subj2 = int(student.marks[1]), subj3 = int(student.marks[2]),
                           subj4 = int(student.marks[3]), subj5 = int(student.marks[4]), subj6 = int(student.marks[5]),
                           subj7 = int(student.marks[6]), subj8 = int(student.marks[7]), subj9 = int(student.marks[8]),
                           subj10 = int(student.marks[9]), subj11 = int(student.marks[10]), percentage = percentage)

    return 'db built'

def plot():    

    subjAvg = db().select(db.students.rollNo.count(), db.students.subj1.sum(),
                                                                db.students.subj2.sum(), db.students.subj3.sum(), db.students.subj4.sum(),
                                                                db.students.subj5.sum(), db.students.subj6.sum(), db.students.subj7.sum(),
                                                                db.students.subj8.sum(), db.students.subj9.sum(), db.students.subj10.sum(),
                                                                db.students.subj11.sum())
    Avg = (subjAvg[0]['_extra']['SUM(students.subj1)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj2)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj3)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj4)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj5)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj6)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj7)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj8)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj9)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj10)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'],
        subjAvg[0]['_extra']['SUM(students.subj11)'] * 1.0 / subjAvg[0]['_extra']['COUNT(students.rollNo)'])

    return dict(Avg=Avg)


def plot1(): 
    m1 = []
    rows = db().select(db.students.subj1)
    for row in rows:
        if row['subj1']>50:
            m1.append(row['subj1'])

    return hist(data=m1,title='frequency of marks',
                ylab='subj1')

def plot2(): 
    m2 = []
    rows = db().select(db.students.subj2)
    for row in rows:
        if row['subj2']>50:
            m2.append(row['subj2'])

    return hist(data=m2,title='frequency of marks',
                ylab='subj2')

def plot3(): 
    m3 = []
    rows = db().select(db.students.subj3)
    for row in rows:
        if row['subj3']>50:
            m3.append(row['subj3'])

    return hist(data=m3,title='frequency of marks',
                ylab='subj3')

def plot4(): 
    m4 = []
    rows = db().select(db.students.subj4)
    for row in rows:
        if row['subj4']>50:
            m4.append(row['subj4'])

    return hist(data=m4,title='frequency of marks',
                ylab='subj4')

def plot5(): 
    m5 = []
    rows = db().select(db.students.subj5)
    for row in rows:
        if row['subj5']>50:
            m5.append(row['subj5'])

    return hist(data=m5,title='frequency of marks',
                ylab='subj5')

def plot6(): 
    m6 = []
    rows = db().select(db.students.subj6)
    for row in rows:
        if row['subj6']>50:
            m6.append(row['subj6'])

    return hist(data=m6,title='frequency of marks',
                ylab='subj6')

def plot7(): 
    m7 = []
    rows = db().select(db.students.subj7)
    for row in rows:
        if row['subj7']>50:
            m7.append(row['subj7'])

    return hist(data=m7,title='frequency of marks',
                ylab='prct1')

def plot8(): 
    m8 = []
    rows = db().select(db.students.subj8)
    for row in rows:
        if row['subj8']>50:
            m8.append(row['subj8'])

    return hist(data=m8,title='frequency of marks',
                ylab='prct2')

def plot9(): 
    m9 = []
    rows = db().select(db.students.subj9)
    for row in rows:
        if row['subj9']>50:
            m9.append(row['subj9'])

    return hist(data=m9,title='frequency of marks',
                ylab='prct3')

def plot10(): 
    m10 = []
    rows = db().select(db.students.subj10)
    for row in rows:
        if row['subj10']>50:
            m10.append(row['subj10'])

    return hist(data=m10,title='frequency of marks',
                ylab='prct4')

def plot11(): 
    m11 = []
    rows = db().select(db.students.subj11)
    for row in rows:
        if row['subj11']>50:
            m11.append(row['subj11'])

    return hist(data=m11,title='frequency of marks',
                ylab='prct5')