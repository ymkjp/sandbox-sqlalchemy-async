import requests
import time

start = time.time()
BASE_URL='http://localhost:8887'
r = requests.get(BASE_URL + "/dc")

end = time.time()
print r.text
print end-start
