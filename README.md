# minervous

`minervous.py` performs the tedious task of constantly checking Minerva for classes that are full but don't have a waiting list, or for classes whose registration status is yet to be set to 'Active'.

## Requirements

* Python 3.6
* [Selenium](http://selenium-python.readthedocs.io/)
* [Chrome Web Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Installation

Download the repository:

```
git clone https://github.com/cgoliver/minervous.git
cd minervous
```

Install selenium 

```
pip install selenium
```

Finally, [download](https://sites.google.com/a/chromium.org/chromedriver/downloads) the Chrome webdriver and place it in the `minervous` directory.

For example:

```
cd minervous
mv ~/Downloads/chromedriver .
```



## Basic Usage

You must create two files with the following format:

* Login info file (default location is current directory and default name is `logins.txt`): 

```
bob.loblaw@mail.mcgill.ca bobpassword1234
bob.loblaw@gmail.com bobgmailpw1234 
```

NOTE: Be careful not to share this file or make it public. `minervous` does not store your password anywhere but if you don't trust just read the code :)

* Courses to monitor (default location is current directory and default name is `watchlist.txt`)

Row format: `<department code>,<course number>,<CRN>,<term>`

```
COMP,767,11806,Winter 2018
COMP,250,18360,Winter 2018
```

Once those files are saved you can just call `minervous.py`.

```
python minervous.py
```

This will automatically log in to Minerva and check each course every 30 minutes.

If a course's status changes or the number of spots available becomes greater than 0 you will receieve an email.

Every 24 hours you will receive a summary email with the latest status of all the courses you are watching.

Help:

```
python minervous.py -h
```

To override the default time interval options see the help menu by using the command above.

Note: This tool was inspired by @zulban's [zminerva](https://github.com/Zulban/zminerva) which had a lot more functionality but is now out of date with the current minerva. 

