"""
Main module for minerva scanner.
Performs check loop and reads command line arguments.
"""

import time
import argparse
import sys
import logging

import course_check
from notify import send_mail

root = logging.getLogger()
root.setLevel(logging.INFO)

class Course:
    def __init__(self, dept, term, crn, num):
        self.department = dept
        self.term = term
        self.crn = crn
        self.course_number = num
        self.status = None
        self.spots = None

    def __str__(self):
        return f"{self.department.upper()} {self.course_number.strip()} in \
            {self.term.strip()}, status is {self.status} and has \
                {self.spots.strip()} spots open."

def cline():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--courselist', type=str, help='Path to course file to\
        watch', default="watchlist.txt")
    parser.add_argument('--logins', type=str, help='Path to login info.',\
        default="logins.txt")
    parser.add_argument('--interval', type=int, help='Number of minutes\
        wait between checks. Under 30 minutes may result in account being\
            locked.', default=30)
    parser.add_argument('--summary', type=int, help='Number of hours\
        between summary email sent with status of all watched courses.',\
            default=24)
    args = parser.parse_args()

    return args
def load_login(fpath="logins.txt"):
    """
    Parse file with mcgill and gmail login info.
    Expected format:
    <mcgill email> <mcgill password>
    <gmail email>  <gmail password>

    Returns: dict
    """
    
    with open(fpath, "r") as f:
        login_dict = {}
        for i, l in enumerate(f):
            info = l.split()
            try:
                email = info[0].strip()
                password = info[1].strip()
                service = email.split("@")[1]
            except IndexError:
                logging.critical("Incorrect email format.")
                sys.exit(1)

            if service == "mail.mcgill.ca":
                login_dict['mcgill_email'] = email
                login_dict['mcgill_password'] = password

            elif service == "gmail.com":
                login_dict['gmail_email'] = email
                login_dict['gmail_password'] = password 
        
            else:
                logging.critical("Unrecognized email service.")
                sys.exit(1)
    return login_dict 

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

def main_loop(logins, courses, interval=30, mail_time=6):
    """
    Monitor minerva for each course and send email if useful changes occur.
    """
    logging.info("Logging in...")
    try:
        course_check.login(logins['mcgill_email'], logins['mcgill_password'])

    except:
        logging.critical("Login error.")
        sys.exit(1)

    message = ["Subject: Scheduled Minerva Summary"]

    last_summary= time.time()

    logging.info("Starting course watch...")
    while True:
        logging.info("Taking a peek...")
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S +0000",\
            time.localtime(time.time()))
        for course in courses:
            info = course_check.check_availability(course.course_number, course.crn,\
                term=course.term, dept=course.department)
            
            status = info['status']
            spots = info['spots']

            first_time = course.status is None and course.spots is None
            #if status for course changes, send email
            if (status != course.status or int(spots)> 0) and not first_time:
                send_mail(logins['gmail_email'], logins['gmail_password'],\
                    logins['gmail_email'],\
                        "Subject: Minerva Course Change Alert! @ {time_now}\n\n" + course.__str__())
            
            course.status = status
            course.spots = spots

            logging.info(f">> Latest Status {time_now}")
            logging.info(course.__str__())
            message.append(course.__str__())

        # send summary email
        if int((time.time() - last_summary)/3600) % mail_time == 0:
            last_summary = time.time()
            send_mail(logins['gmail_email'], logins['gmail_password'],\
                logins['gmail_email'], "\n".join(message))
            
        #sleep for interval minutes 
        time.sleep(interval * 60)

if __name__ == "__main__":
    args = cline()
    logins = load_login(fpath=args.logins)
    courses = load_courses(fpath=args.courselist)
    main_loop(logins, courses, interval=args.interval,\
        mail_time=args.summary)
    pass
