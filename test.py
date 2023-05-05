import sys
import os
import yaml
from docopt import docopt
from pprint import pprint

docs = """
Тестовый проект

Команды:

test.py list builds
test.py list tasks
test.py get build build_name
test.py get task task_name
"""

args = sys.argv
FILES_PATH = os.getcwd()  # files directory, could be changed
BUILDS = "builds.yaml"
TASKS = "tasks.yaml"

try:
  with open(os.getcwd() + os.path.sep + BUILDS) as builds_file:
    builds = yaml.safe_load(builds_file)
except FileNotFoundError:
  print("No file found")
except:
  print("File is invalid")

try:
  with open(os.getcwd() + os.path.sep + TASKS) as tasks_file:
    tasks = yaml.safe_load(tasks_file)
except FileNotFoundError:
  print("No file found")
except:
  print("File is invalid")


def get_available_builds():
  """Function to get available builds"""
  res = []
  for i in builds['builds']:
    res.append(i['name'])
  return res

def task_exists(task_name):
  for i in tasks['tasks']:
    if i['name'] == task_name:
      return True
  return False

def build_exists(build_name):
  for i in builds['builds']:
    if i['name'] == build_name:
      return True
  return False

def find_deps(task_name):
    """Auxiliary function to get dependencies for a given task"""
    for i in tasks['tasks']:
        if i['name'] == task_name:
            return i['dependencies']

def get_tree(task_name):
    """Auxiliary function to build a structure for a given task"""
    res = []
    task_deps = find_deps(task_name)
    if len(task_deps) > 0:
        for i in task_deps:
            t = find_deps(i)
            if len(t) > 0:
                for j in t:
                    res += get_tree(j)
                res.append(i)
            else:
                res += [i]
    res.append(task_name)
    return res

def get_available_tasks():
  """Returns available tasks in order of completion"""
  lta = []
  for i in tasks['tasks']:
    if len(i['dependencies']) > 0:
      lta += get_tree(i['name'])
      pass
    else:
      lta.append(i['name'])
  res = []
  for i in lta:
    if not(i in res):
        res.append(i)
  return res

def get_tasks_for_build(build_name):
  t = []
  for i in builds['builds']:
    if i['name'] == build_name:
      for j in i['tasks']:
        t += get_tree(j)
  res = []
  for i in t:
    if not(i in res):
        res.append(i)
  return res

def main():

  if args[1] == 'list' and len(args) == 3:
    if 'builds' in args:
      print("List of available builds")
      temp = get_available_builds()
      for i in temp:
        print("*", i)
    elif 'tasks' in args:
      print("List of available tasks")
      temp = get_available_tasks()
      for i in temp:
        print("*", i)
    else:
      print("Specify which kind of list do you want")

  elif args[1] == 'get' and len(args) == 4:
    if 'build' in args:
      if build_exists(args[-1]):
        print("Build info: ")
        print("* name: " + args[-1])
        temp = get_tasks_for_build(args[-1])
        print("* tasks: " + ", ".join(get_tasks_for_build(args[-1])))
      else:
        print("No build with such a name: " + args[-1])
    elif 'task' in args:
      if task_exists(args[-1]):
        print("Task info: ")
        print("* name: " + args[-1])
        print("* dependencies: " + ", ".join(get_tree(args[-1])[:-1]))
      
      else:
        print("No task with such a name: "+args[-1])
    else:
      print("Specify a build or a task")

  elif args[1] == "help":
    print(docs)

  else:
    print("command not found")

if __name__=='__main__':
   main()