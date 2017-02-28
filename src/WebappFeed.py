import http.client
import json
import time

while True:
  connection = http.client.HTTPConnection("split-flap2.azurewebsites.net")
  connection.request("GET", "/Messages")
  response = connection.getresponse()
  if response.status == 200:
    content = response.read().decode('utf-8')
    messages = json.loads(content)
    with open("messages.txt", "a") as myfile:
      for message in messages:
          myfile.write(message['Content'])
  connection.close()
  time.sleep(60)



