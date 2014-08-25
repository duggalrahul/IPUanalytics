def plot1(): 
    m1 = []
    rows = db().select(db.students.subj1)
    for row in rows:
        if row['subj1']>50:
            m1.append(row['subj1'])

    return hist(data=m1,title='x distribution',
                ylab='subj1')

def plot2(): 
    m2 = []
    rows = db().select(db.students.subj2)
    for row in rows:
        if row['subj2']>50:
            m2.append(row['subj2'])

    return hist(data=m2,title='x distribution',
                ylab='subj2')

def plot3(): 
    m3 = []
    rows = db().select(db.students.subj3)
    for row in rows:
        if row['subj3']>50:
            m3.append(row['subj3'])

    return hist(data=m3,title='x distribution',
                ylab='subj3')

def plot4(): 
    m4 = []
    rows = db().select(db.students.subj4)
    for row in rows:
        if row['subj4']>50:
            m4.append(row['subj4'])

    return hist(data=m4,title='x distribution',
                ylab='subj4')

def plot5(): 
    m5 = []
    rows = db().select(db.students.subj5)
    for row in rows:
        if row['subj5']>50:
            m5.append(row['subj5'])

    return hist(data=m5,title='x distribution',
                ylab='subj5')

def plot6(): 
    m6 = []
    rows = db().select(db.students.subj6)
    for row in rows:
        if row['subj6']>50:
            m6.append(row['subj6'])

    return hist(data=m6,title='x distribution',
                ylab='subj6')

def plot7(): 
    m7 = []
    rows = db().select(db.students.subj7)
    for row in rows:
        if row['subj7']>50:
            m7.append(row['subj7'])

    return hist(data=m7,title='x distribution',
                ylab='subj7')

def plot8(): 
    m8 = []
    rows = db().select(db.students.subj8)
    for row in rows:
        if row['subj8']>50:
            m8.append(row['subj8'])

    return hist(data=m8,title='x distribution',
                ylab='subj8')

def plot9(): 
    m9 = []
    rows = db().select(db.students.subj9)
    for row in rows:
        if row['subj9']>50:
            m9.append(row['subj9'])

    return hist(data=m9,title='x distribution',
                ylab='subj9')

def plot10(): 
    m10 = []
    rows = db().select(db.students.subj10)
    for row in rows:
        if row['subj10']>50:
            m10.append(row['subj10'])

    return hist(data=m10,title='x distribution',
                ylab='subj10')

def plot11(): 
    m11 = []
    rows = db().select(db.students.subj11)
    for row in rows:
        if row['subj11']>50:
            m11.append(row['subj11'])

    return hist(data=m11,title='x distribution',
                ylab='subj11')