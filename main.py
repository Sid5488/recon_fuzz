import sys
import requests
from time import sleep
from threading import Thread
from rich.console import Console

HOST = "https://worksn.com.br/"
list = [
  "/admin", 
  "/index.php", 
  "/admin.php", 
  "/backend", 
  "/app.js", 
  "/.htaccess"
]

console = Console()

def get_argument():
  for index, arg in enumerate(sys.argv):
    if arg == "-lf":
      file = open(sys.argv[index + 1], "r")
      
      return file

def request_fuzzing(index, item):
  with console.status("[bold green] Test on: " + HOST + item) as status:
    request = requests.get(HOST + item)
    response_length = len(request.text)

    if request.status_code == 200 and response_length > 0:
      message = "File found!" + item
    if request.status_code == 403 and response_length > 0:
      message = "File found, but you hasn't permission!"
    else:
      message = "Not found!"

    if(message != "Not found!"):
      console.log(request, message)

def fuzzing(file):
  message = ""
  for index, item in enumerate(file):
    threading = Thread(target=request_fuzzing, args=(index, item))

file = get_argument()
fuzzing(file.read().split('\n'))
