import requests

# To test the server API, just run this client script when the server is on.
# Done by Mao Liyan Frosty 1002190 & Yang Lei 1002361

print "--- Get connection to the API ---"
r = requests.get("http://localhost:5000/")
print r.headers
print r.text

print "--- Get information for all the pillars ---"
r = requests.get("http://localhost:5000/pillar")
print r.headers
print r.text

print "--- Get information for ISTD tracks, wrong authentication ---"
r = requests.get("http://localhost:5000/pillar/ISTD", auth=('admin', 'passwording'))
print r.headers
print r.text

print "--- Get information for ISTD tracks, after authentication ---"
r = requests.get("http://localhost:5000/pillar/ISTD", auth=('admin', 'password'))
print r.headers
print r.text

print "--- Get json type of the ISTD information ---"
r = requests.get("http://localhost:5000/pillar/ISTD/info/info.json", auth=('admin', 'password'))
print r.headers
print r.text

print "Get text type of the ISTD information"
r = requests.get("http://localhost:5000/pillar/ISTD/info/info.txt", auth=('admin', 'password'))
print r.headers
print r.text

print "Get course information for Cyber Security Track"
r = requests.get("http://localhost:5000/pillar/ISTD/Cyber%20Security")
print r.headers
print r.text

print "Add a new pillar using the post method"
headers = {'Content-type': 'application/json'}
r = requests.post("http://localhost:5000/pillar", json={'name': 'EPD'}, auth=('user1', '123456'))
print r.headers
print r.text

print "Delete a pillar using the Delete method"
r = requests.delete("http://localhost:5000/pillar/EPD")
print r.headers
print r.text