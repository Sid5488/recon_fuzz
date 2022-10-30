import sys
import requests
from threading import Thread
from rich.console import Console

console = Console()

def get_argument():
  target_data = { "file": "", "host": "" }

  for index, arg in enumerate(sys.argv):
    if arg == "-lf":
      file = open(sys.argv[index + 1], "r")
      
      target_data["file"] = file
    
    if arg == "-t":
      target = sys.argv[index + 1]

      target_data["host"] = target

  return target_data


def request_fuzzing(file, host):
  for index, item in enumerate(file):
    message = ""

    with console.status("[bold green] Test on: " + host + item) as status:
      request = requests.get(host + item)
      response_length = len(request.text)

      if request.status_code == 200 and response_length > 0:
        message = "File found! " + item
      if request.status_code == 403 and response_length > 0:
        message = "File found, but you hasn't permission! " + item
      else:
        message = "Not found!"

      if(message != "Not found!"):
        console.log(request, message)


def fuzzing(file, host):
  Thread(target=request_fuzzing, args=(file, host,)).start()


def main():
  try:
    target = get_argument()

    fuzzing(target["file"].read().split('\n'), target["host"])
  except:
    print("Programming, stoped...")


main()
