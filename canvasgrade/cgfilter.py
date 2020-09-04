import re
import sys

def courses(full, reqs):
  filtered = list()
  for req in reqs:
    req = req.lower()
    if re.fullmatch(r"\w+-\d+", req):
      req += "-01"

    found = None
    for course in full:
      if course["id"] == req or course["tag"] == req:
        found = course

    if found is None:
      print("Unknown class: ", req, file=sys.stderr)
    else:
      filtered.append(found)

  return filtered


def one_course(full, req):
  found = courses(full, [req])
  if len(found) == 1:
    return found[0]
  return None


def students(full, reqs):
  filtered = list()
  for req in reqs:
    if isinstance(req, str):
      req = req.lower()

    found = None
    for student in full:
      if student["id"] == req or student["tag"] == req:
        found = student

    if found is None:
      print("Unknown student: ", req, file=sys.stderr)
    else:
      filtered.append(found)

  return filtered


def one_student(full, req):
  found = students(full, [req])
  if len(found) == 1:
    return found[0]
  return None


def assignments(full, reqs):
  filtered = list()
  for req in reqs:
    req = req.lower()

    found = None
    for assignment in full:
      if assignment["id"] == req or assignment["tag"] == req:
        found = assignment

    if found is None:
      print("Unknown assignment: ", req, file=sys.stderr)
    else:
      filtered.append(found)

  return filtered


def one_assignment(full, req):
  found = assignments(full, [req])
  if len(found) == 1:
    return found[0]
  return None
