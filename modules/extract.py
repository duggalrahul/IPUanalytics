import re
import os

colleges = {}

class student:	
	def __init__(self):
		self.rollNo = 0
		self.name = ''
		self.marks = []

class college:
	def __init__(self):
		self.students = []			
	

def process(collegeName, collegeData):	
	# This regex extracts all information relation to a particular student
	# All information starting from an 11 digit roll number and ending with an 11 digit
	# roll number is extracted    
	studentInfo = re.findall(r'(\n[0-9]{11}\s)(.*?)(?=(?:\n[0-9]{11})|Grace|Institution)', collegeData, re.DOTALL)
  
	
	for s in studentInfo:		
		try: 
			info = s[1] + '\n'
			rollNo = s[0]
			name = re.findall(r'([\w\s]+)(?= SID:)', info)[0]
			marks = re.findall(r'[0-9]{1,2}\s((?:[0-9]{1,2}\s){10}[0-9]{1,2})\n', info)
			
			if len(marks) and len(name):

				if len(marks)==1:
					m = marks[0].split()
				else:					
					m = marks[1].split()
				stud = student()
				stud.rollNo = rollNo
				stud.name = name
				stud.marks = m

				if collegeName in colleges.keys():
					colleges[collegeName].students.append(stud)
				else:
					colleges[collegeName] = college()
					colleges[collegeName].students.append(stud)
		except:
			continue
            
def extract_data(lines):
    # Partition the input file according to appearance of (SCHEME OF EXAMINATIONS)
    # in the text
	collegeData = re.findall(r'EXAMINATIONS\)(.*?)\(SCHEME', lines, re.DOTALL)
    
	colleges.clear()
    
	for data in collegeData:
		# Extract college name from the data and update data
		# in the corresponding college object
		name = (re.search(r'Institution: (.+)', data)).group(1)
		process(name, data)
	return colleges
