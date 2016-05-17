import smtplib
import requests
import time
""" Written By Omar Vega
    https://github.com/Omar1vega/
"""

def sendText(content,recipient):
    
    username = "[User_Email]@gmail.com"     ##enter gmail username and password to send text to mobile
    password = "[User Password]"

    recipient = recipient
    message = content

    msg = """From: %s \nTo: %s\nSubject:FindOpenClasses\n%s""" % (username, recipient, message)

    print (msg)

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(username,password)
    server.sendmail(username, recipient,msg)
    print ("done")
    server.quit()

def main():
    searchType=input(" Type 'C' to search by Course Code (e.g. 54000) \n Type 'D' to search by Department+Course (e.g. Writing 39c)\n ")
    if (searchType.upper()=='C'):
        courseCode=input("Please Enter The 5 Digit Course Code")
        url="https://www.reg.uci.edu/perl/WebSoc/?YearTerm=2016-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes="+courseCode+"&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Text+Results"
        
    elif(searchType.upper()=='D'):
        dept=input("Please Enter the department name (e.g. ""Writing"",or ""EECS"") \n ").strip()
        course=input("Please Enter the Course (e.g. ""39C"",or ""20"") \n ").strip()
        url='https://www.reg.uci.edu/perl/WebSoc/?YearTerm=2016-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept='+dept.upper()+'&CourseNum='+course+'&Division=ANY&CourseCodes=&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Text+Results'

    else:
        main()
        
    classList=[]
    phoneNum=input("Phone Number? ").strip()
    carrier=input( "Carrier? 'Al' for Alltel \n 'ATT' for AT&T \n  'B' for Boost Mobile \n 'S' for Sprint \n 'T' for T-Mobile \n 'Vz' for Verizon \n 'Vm' for Virgin Mobile ")

    if (carrier.upper()== 'AL'):
        carrier="@message.alltel.com"
    elif(carrier.upper() == 'ATT'):
        carrier="@txt.att.net"
    elif(carrier.upper() == 'B'):
        carrier="@myboostmobile.com"
    elif(carrier.upper() == 'S'):
        carrier="@messaging.sprintpcs.com"
    elif(carrier.upper() == 'T'):
        carrier="@tmomail.net"
    elif(carrier.upper() == 'VZ'):
        carrier="@vtext.com"
    elif(carrier.upper() == 'VM'):
        carrier="@vmobl.com"
    recipient=phoneNum+carrier
    
    while True:         ## rechecks every 60s
        
        r = requests.get(url)
        classes=r.text

        file=open('classes.txt','w')
        file.write(classes)
        file.close()

        input1=open("classes.txt",'r')  
        lines = [i for i in input1 if i[:-1]]
        for line in lines:
            line=line.strip()
            line=line.split()
            if (line[-1]!="FULL") and line[0].isdigit():
                if line[-1]=='Open':
                    classList.append(line[0]+'(Open)')
                else:  
                    print(line[0])
                    classList.append(line[0])
                    
        classString= ', '.join(classList)
        classString= dept+ course+" Classes Available "+classString
        print(classString)
                    
        if len(classList)>0:
            sendText(str(classString),recipient)
        time.sleep(60)    ## rechecks every 60s
main()
