import smtplib
import time

import requests

""" Written By Omar Vega
    https://github.com/Omar1vega/
"""


def send_text(message, recipient):
    username = "[User_Email]@gmail.com"  # enter gmail username and password to send text to mobile
    password = "[User Password]"

    msg = """From: %s \nTo: %s\nSubject:FindOpenClasses\n%s""" % (username, recipient, message)

    print(msg)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipient, msg)
    server.quit()


def main():
    search_type = input(
        "Type 'C' to search by Course Code (e.g. 54000) \n Type 'D' to search by Department+Course (e.g. Writing "
        "39c)\n ")
    if search_type.upper() == 'C':
        course_code = input("Please Enter The 5 Digit Course Code")
        url = "https://www.reg.uci.edu/perl/WebSoc/?YearTerm=2016-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept" \
              "=+ALL&CourseNum=&Division=ANY&CourseCodes=" + course_code + \
              "&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY" \
              "&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Text+Results "

    elif search_type.upper() == 'D':
        dept = input("Please Enter the department name (e.g. ""Writing"",or ""EECS"") \n ").strip()
        course = input("Please Enter the Course (e.g. ""39C"",or ""20"") \n ").strip()
        url = 'https://www.reg.uci.edu/perl/WebSoc/?YearTerm=2016-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=' \
              + dept.upper() + '&CourseNum=' + course \
              + '&Division=ANY&CourseCodes=&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime' \
                '=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Text' \
                '+Results '

    else:
        main()

    class_list = []
    phone_number = input("Phone Number? ").strip()
    carrier = input(
        "Carrier? 'Al' for Alltel \n 'ATT' for AT&T \n  'B' for Boost Mobile \n 'S' for Sprint \n 'T' for T-Mobile \n "
        "'Vz' for Verizon \n 'Vm' for Virgin Mobile ")

    if carrier.upper() == 'AL':
        carrier = "@message.alltel.com"
    elif carrier.upper() == 'ATT':
        carrier = "@txt.att.net"
    elif carrier.upper() == 'B':
        carrier = "@myboostmobile.com"
    elif carrier.upper() == 'S':
        carrier = "@messaging.sprintpcs.com"
    elif carrier.upper() == 'T':
        carrier = "@tmomail.net"
    elif carrier.upper() == 'VZ':
        carrier = "@vtext.com"
    elif carrier.upper() == 'VM':
        carrier = "@vmobl.com"
    recipient = phone_number + carrier

    while True:  # rechecks every 60s
        classes = requests.get(url).text

        file = open('classes.txt', 'w')
        file.write(classes)
        file.close()

        input1 = open("classes.txt", 'r')
        lines = [i for i in input1 if i[:-1]]
        for line in lines:
            line = line.strip()
            line = line.split()
            if (line[-1] != "FULL") and line[0].isdigit():
                if line[-1] == 'Open':
                    class_list.append(line[0] + '(Open)')
                else:
                    print(line[0])
                    class_list.append(line[0])

        class_string = ', '.join(class_list)
        class_string = dept + course + " Classes Available " + class_string
        print(class_string)

        if len(class_list) > 0:
            send_text(str(class_string), recipient)
        time.sleep(60)  # rechecks every 60s


main()
