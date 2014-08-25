def readFile(filename):
	f = open(filename)
	lines = f.read()
	f.close
	return lines

def cleanData(filename, cleanFile):	
	fr = open(filename, 'rb')
	fw = open(cleanFile,'wb')

	s = fr.readlines()

	for line in s:
		newline1 = line.replace('50*\n','50 ')
		newline2 = line.replace('50*','50')
		if line=='\n':
			continue
		elif line!=newline1:			
			fw.write(newline1)
		elif line!=newline2:
			fw.write(newline2)
		else:
			fw.write(line)

	fr.close()
	fw.close()