#start a connection to the sqlite database
db = DAL('sqlite://storage.db', lazy_tables=True)

#define table colleges
db.define_table('colleges',
				Field('name', unique=True), 
				format='%(name)s')

# define table students
db.define_table('students', 
	Field('colleges_id', 'integer', 'reference colleges'), 
	Field('rollNo'), 
	Field('name'),
    Field('subj1','integer'), Field('subj2','integer'), Field('subj3','integer'), Field('subj4','integer'),
    Field('subj5','integer'), Field('subj6','integer'), Field('subj7','integer'), Field('subj8','integer'),
    Field('subj9','integer'), Field('subj10','integer'), Field('subj11','integer'), 
    Field('percentage', 'float'))