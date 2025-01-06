#!/usr/bin/python

import os

os.chdir('/') 
os.chdir('var/log')
file=open('auth.log','r') 
data=file.readlines() 

print('Here are all the commands executed in auth.log')
for eachline in data:
	if 'COMMAND' in eachline: 
			time=eachline.split()[0]
			time2=time.replace('T'," ")
			time3=time2.split(".")[0]
			command=eachline.split('bin/')[1].strip()
			firstsplit=eachline.split('sudo:')[1]
			user=firstsplit.split(':')[0].strip()
			
			
			print('At',time3 ,'User',user , 'used command:',command) 
				
print('\n') 


# ~ #newly added users
print('Here are the newly added users and their details') 
ADDUSER=0 
for eachline in data: 
		time=eachline.split()[0]
		time2=time.replace('T'," ")
		time3=time2.split(".")[0]
		if 'new user' in eachline:
			filter1=eachline.split('=')[1]
			newuser=filter1.split(',')[0]
			ADDUSER=ADDUSER+1
			user=eachline.split()[1]
			print('At', time3 ,'A new user', newuser,'was added by', user)
			
print('A total of', ADDUSER , 'user(s) was added')			
print('\n') 


#deletedusers
print('Here are the users that have been deleted and their details') 
DELUSER=0 
for eachline in data:
	if 'delete user' in eachline:
		time=eachline.split()[0]
		time2=time.replace('T'," ")
		time3=time2.split(".")[0]
		user=eachline.split()[1]
		filter1=eachline.split()[-1]
		deleteduser=filter1.strip("'")
		DELUSER=DELUSER+1 
		print('At', time3 ,'User', deleteduser,'was deleted by', user) 
print('A total of', DELUSER , 'user(s) was deleted')			
print('\n')



# Print details of changing passwords, including the Timestamp.
print('Here are the details of password changes in auth.log') 
for eachline in data: #same
	if 'password changed' in eachline:
		time=eachline.split()[0]
		time2=time.replace('T'," ")
		time3=time2.split(".")[0]
		chgpwdusr=eachline.split()[-1] 
		print('At', time3, 'the password for', chgpwdusr ,'was changed') 
		
print('\n')

#Print details of when users used the su command.
print('Here are the list of users using su to switch user') 
for eachline in data:
	if '(to' in eachline:
		time=eachline.split()[0]
		time2=time.replace('T'," ")
		time3=time2.split(".")[0]
		switchusrfirstsplit=eachline.split('(to')[1]  
		switchedusr=switchusrfirstsplit.split(')')[0].strip()
		USER=eachline.split()[-3] 
		print('At', time3, USER, 'switched user', 'to:',switchedusr) 

print('\n')


# Print details of users who used the sudo; include the command.
print('Here are the details of users who used sudo on a command')
for eachline in data: #same
	if 'sudo' in eachline:
		if 'COMMAND' in eachline: 
			USER=eachline.split(':')[4].strip() 
			time=eachline.split()[0]
			time2=time.replace('T'," ")
			time3=time2.split(".")[0]
			command=eachline.split('bin/')[1].strip()
	
			print('At', time3 , 'user:', USER , 'executed sudo on command:' , command)
print('\n')



# Print ALERT! If users failed to use the sudo command; include the command.
print('ALERT!!!!! Here are the list of failed attempts in using sudo') 
for eachline in data:#same
	time=eachline.split()[0]
	time2=time.replace('T'," ")
	time3=time2.split(".")[0]
		
	if 'sudo' in eachline: 
		if 'incorrect password' in eachline: 
			Faileduser=eachline.split(':')[4]
			Faileduser2=Faileduser.strip() 
			command=eachline.split('bin/')[1].strip() 
			FAILEDATTEMPT=0
			FAILEDATTEMPT=FAILEDATTEMPT+1 
			print('ALERT!!!', 'At', time3 , 'user:', Faileduser2 , 'failed to execute sudo on the command:', command) 
			print('There was a total number of', FAILEDATTEMPT , 'failed attempts to use sudo')	

file.close()
