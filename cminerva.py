"""
TODO: 
    - cline (credentials)
"""

import time
import argparse
import sys

import course_check
from notify import send_mail
import mcgill_login
import gmail_login

class Course:
    def __init__(self, dept, term, crn, num):
        self.department = dept
        self.term = term
        self.crn = crn
        self.course_number = num
        self.status = None
        self.spots = None

    def __str__(self):
        return f"{self.department.upper()} {self.course_number} in
            {self.term.strip()}, status is {self.status} and has\
                {self.spots} spots open."

def load_courses(fpath="watchlist.txt"):
    courses = []
    with open(fpath, "r") as cfile:
        for line in cfile:
            try:
                dept, cnum, crn, term = line.split(",")
                course = Course(dept.upper(), term.strip(), crn, cnum)
                courses.append(course)
            except:
                print("Invalid Course Entry")
    return courses

def main_loop(uname, pw, courses, interval=30, mail_time=6):

    check_count = 0

    course_check.login(uname, pw)

    message = ["Subject: Scheduled Minerva Summary"]

    last_summary= time.time()

    while True:
        for course in courses:
            info = course_check.check_availability(course.course_number, course.crn,\
                term=course.term, dept=course.department)
            
            check_count += 1

            status = info['status']
            spots = info['spots']

            #if status for course changes, send email
            if status != course.status or int(spots)> 0:
                send_mail(gmail_login.gname, gmail_login.gpwd,\
                    "carlos.gonzalez.oliver@gmail.com",\
                        "Subject: Minerva Course Change Alert!\n\n" + course.__str__())
            
            course.status = status
            course.spots = spots

            message.append(course.__str__())

        # send summary email
        if int((last_summary - time.time())/3600) % mail_time == 0:
            last_summary = time.time()
            send_mail(gmail_login.gname, gmail_login.gpwd,\
                "carlos.gonzalez.oliver@gmail.com", "\n".join(message))
            
        #sleep 30 minutes
        break
        time.sleep(interval * 60)

if __name__ == "__main__":
    courses = load_courses()
    main_loop(mcgill_login.uname, mcgill_login.pwd,\
        courses, interval=30)
    pass
