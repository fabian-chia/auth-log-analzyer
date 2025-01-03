#!/usr/bin/python

import os

os.chdir('/') #changes the directory to the root folder so that the user can access the auth log afterwards
os.chdir('var/log')#changes the directory to /var/log to be able to access the auth.log
file=open('auth.log','r') #used file variable to open the file
data=file.readlines() #data variable used to read the file variable, readlines was used to read the data as a list

print('Here are all the commands executed in auth.log') #header so the user is able to see what the information below is about
for eachline in data: #created a for loop to filter out lines in the data that contains the string 'COMMAND' so I can show the user all the commands that were used 
	if 'COMMAND' in eachline: 
			time=eachline.split()[0] #creating the variable time so let the user know when the command was executed, used .split() to split the output by the blank space and print the first item
			command=eachline.split('bin/')[1].strip()#for eachline that contains command, the command executed is preceded by bin/ thus i chose to split the data based on bin/ and print the second item
			firstsplit=eachline.split('sudo:')[1] #defined the variable 'firstsplit' to split the data into 2 by sudo: so that we can obtain the name of the user that executed the command
			user=firstsplit.split(':')[0].strip()#for the variable 'user' to obtain the exact user's name, i split the output of 'firstplit' by ':' and printed the first item
			
			
			print('At',time ,'User',user , 'used command:',command) #final statement that tells the time in which the user executed the command
				
print('\n') #printing a new line to separate the data to make it easier on the eyes of the user of the script


# ~ #newly added users
print('Here are the newly added users and their details') #statement to tell the user what data will be presented below
ADDUSER=0 #vairble to keep track of the number of users added
for eachline in data: #same for loop which searches for string 'COMMAND'
	if 'COMMAND' in eachline:
		time=eachline.split()[0]#time remains the same 
		firstsplit=eachline.split('sudo:')[1] #once again getting the exact name of the user that added new users similar to the example above
		user=firstsplit.split(':')[0].strip() #the username that added the new user similar to the data above
		if 'adduser' in eachline: #new for loop to search for strings that contain 'useradd' as it is the command used to add users
			newuser=eachline.split()[-1]#printing the last item of the output after splitting the data by the blank spaces, the last output contains the name of the new user
			ADDUSER=ADDUSER+1#for every line that contains useradd it adds 1 to the counter
	
			print('A total of', ADDUSER , 'user was added')			#prints the total number of new users added
			print('At', time ,'A new user', newuser,'was added by', user) #tells the user of the script, the time in which a new user was added and which user added the new user
			print('\n') #printing a new line to separate the data to make it easier on the eyes of the user

# ~ #logging deleted users
print('Here are the users that have been deleted and their details') #statement 
for eachline in data:
	if 'COMMAND' in eachline:#same as above
		time=eachline.split()[0]#same
		firstsplit=eachline.split('sudo:')[1]#same
		user=firstsplit.split(':')[0].strip()#same but strip is used as the final item contains spaces
		DELUSER=0#variable to count the number of usrs deleted
		if 'deluser' in eachline: #searches of strings with 'deluser' as it is the command to delete a user
			deleteduser=eachline.split()[-1]#defining the variable that tells us the name of the user that was deleted
			DELUSER=DELUSER+1#adds 1 to the counter of number of users deleted
			print('A total of', DELUSER , 'user was deleted')#prints the count of number of users deleted				
			print('At', time ,'User', deleteduser,'was deleted by', user) #statement that tells the user what time which user deleted which user
			print('\n')#new line to separate the data



# ~ 2.3. Print details of changing passwords, including the Timestamp.
print('Here are the details of password changes in auth.log') #statement
for eachline in data: #same
	if 'password changed' in eachline: #searches for string 'password changed' to which user's password has been changed
		time=eachline.split()[0] #same
		chgpwdusr=eachline.split()[-1] #to see the user of which the password has been changed
		print('At', time, 'the password for', chgpwdusr ,'was changed') #tells the user what time the password of which user has been changed
		
print('\n')

# ~ 2.4. Print details of when users used the su command.
print('Here are the list of users using su to switch user') #tells the user what info is about to be presented
for eachline in data:#same
	if '(to' in eachline:#searches for '(to' as it is presented in strings that have switched user
		time=eachline.split()[0] #same
		switchusrfirstsplit=eachline.split('(to')[1] #split the lines by '(to' as the new user that has been switched to will be shown after 'to)' 
		switchedusr=switchusrfirstsplit.split(')')[0].strip()#stripping the line as it has a long blank space
		USER=eachline.split()[-3] #splits the data by the spaces and prints the 3rd output from the back which contains the initial user
		print('At', time, USER, 'switched user', 'to:',switchedusr) #tells the user what time which user switched to which user

print('\n')


# ~ 2.5. Print details of users who used the sudo; include the command.
print('Here are the details of users who used sudo on a command') #statement to separate info
for eachline in data: #same
	if 'sudo' in eachline: #searches for sudo in each line of the data
		if 'COMMAND' in eachline: #searches for command as any sudo command will be logged in the authlog
			USER=eachline.split(':')[4].strip() #splits the data by ':' and then prints the 5th item which contains the user that executed the command, and strip to remove the blank space
			time=eachline.split()[0] #same
			command=eachline.split('bin/')[1].strip()#splits that by 'bin/' as command is preceded by 'bin/' and then strips the blank space with strip
	
			print('At', time , 'user:', USER , 'executed sudo on command:' , command)#tells the user what time which user used which sudo command
print('\n')#prints blank space to separate data



# ~ 2.6. Print ALERT! If users failed to use the sudo command; include the command.
print('ALERT!!!!! Here are the list of failed attempts in using sudo') #prints an alert to tell the user the when the sudo command has failed
for eachline in data:#same
	time=eachline.split()[0]#same
		#creates a variable that is used to count the number of failed attempts to use sudo
	if 'sudo' in eachline: #searches for sudo
		if 'incorrect password' in eachline: #when sudo command has failed thrice, incorrect password will be presented in the output
			Faileduser=eachline.split(':')[4]#splits eachline by ':' and prints the 5th output containing the user that executed the command
			Faileduser2=Faileduser.strip() #removes white space
			command=eachline.split('bin/')[1].strip() #prints command and removes white space, same as above
			FAILEDATTEMPT=0
			FAILEDATTEMPT=FAILEDATTEMPT+1 #for every line the contains incorrect password it adds 1 to the counter which keeps track of the number of times a user failed to use sudo
			print('ALERT!!!', 'At', time , 'user:', Faileduser2 , 'failed to execute sudo on the command:', command) #prints the alert and the time at which which user failed to use sudo on which command
			print('There was a total number of', FAILEDATTEMPT , 'failed attempts to use sudo')	#tells the user the total number of times that that sudo command was failed 

file.close()
