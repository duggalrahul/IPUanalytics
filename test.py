import random
p = [(random.random(),random.random()) for i in range(1000)]
n,k,z=0,0,[]    
for x,y in p:
    if x**2+y**2<1: k+=1
    n+=1
    z.append((n,4.0*float(k)/n))

for x,y in p:
	print y