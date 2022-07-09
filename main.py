import sys
import math
import psutil
import requests
from threading import Thread
from rich.console import Console

HOST = "https://worksn.com.br/"

console = Console()

def get_argument():
  for index, arg in enumerate(sys.argv):
    if arg == "-lf":
      file = open(sys.argv[index + 1], "r")
      
      return file

def request_fuzzing(file):
  for index, item in enumerate(file):
    message = ""
    with console.status("[bold green] Test on: " + HOST + item) as status:
      request = requests.get(HOST + item)
      response_length = len(request.text)

      if request.status_code == 200 and response_length > 0:
        message = "File found! " + item
      if request.status_code == 403 and response_length > 0:
        message = "File found, but you hasn't permission! " + item
      else:
        message = "Not found!"

      if(message != "Not found!"):
        console.log(request, message)

def fuzzing(file):
  threading = Thread(target=request_fuzzing, args=(file,)).start()
  # threading = Thread(target=request_fuzzing, args=(file[0: int(len(file) / 2)],)).start()
  # threading2 = Thread(target=request_fuzzing, args=(file[int((len(file) / 2) + 1): len(file) -1],)).start()

file = get_argument()
fuzzing(file.read().split('\n'))
