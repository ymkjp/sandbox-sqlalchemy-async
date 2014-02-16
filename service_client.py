import requests
import time

start = time.time()
BASE_URL='http://localhost:9888/'
r = requests.get(BASE_URL + "dc", params={'wait':10})

end = time.time()
print r.text
print end-start
