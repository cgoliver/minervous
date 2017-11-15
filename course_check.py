import urllib
import requests


search_url = "https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse"
login_url = "https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin"

username = "carlos.gonzalezoliver@mail.mcgill.ca"
pwd = "sasjajuli_milojuli"

params=(("sid",username),
        ("PIN",pwd))

data=urllib.parse.urlencode(params)

cookies={"TESTID":"set"}

r_login = requests.post(login_url,data=data,cookies=cookies)
sessionid = r_login.cookies.get("SESSID")

print(sessionid)

r=requests.post(search_url,cookies={"SESSID": sessionid})
print(r.status_code)
