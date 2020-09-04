#!/usr/bin/env python

import os
import sys
import re

import requests
import yaml

from canvasgrade import canvas
from canvasgrade import config
from canvasgrade import cgfilter

args = [bit for arg in sys.argv[1:] for bit in arg.split('/')]

if len(args) < 1:
  print("Course tag required", file=sys.stderr)
  sys.exit()

course = cgfilter.one_course(config.get_courses(), args[0])
if not course:
  sys.exit()

assignments = config.get_assignments(course['tag'])
if len(args) > 1:
  assignment = cgfilter.assignments(assignments, args[1])

for assignment in assignments:
  print(assignment['tag'], ":", sep="")
  students = config.get_students(course['tag'])
  if len(args) > 2:
    students = cgfilter.students(students, args[2:])

  for student in students:
    if not os.path.exists(os.path.join(course['tag'], assignment['tag'], student['tag'])):
      continue
    try:
      grade = config.get_grade(course['tag'], assignment['tag'], student['tag'])
    except:
      print("  -", student['tag'], "does not have a grade.yaml")
      continue
    submission = config.get_submission(course['tag'], assignment['tag'], student['tag'])
    if not grade.get("posted"):
      record = canvas.get(
        f"https://harding.instructure.com/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions/{student['id']}"
      )
      if not record:
        continue
      if record.get("submitted_at") != submission["submitted_at"]:
        print(student['tag'], " has posted a new submission", file=sys.stderr)
        continue
      body = { 'submission': { 'posted_grade': grade['points'] } }
      comment = grade.get('comment')
      if comment:
        body['comment'] = { 'text_comment': comment }
      elif grade.get('comments'):
        print("Warning: grade.yaml has 'comments' property - did you mean 'comment'?", file=sys.stderr)
      canvas.put(
        f"https://harding.instructure.com/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions/{student['id']}",
        body
      )
      grade['posted'] = True
      config.store_grade(course['tag'], assignment['tag'], student['tag'], grade)
      print("  -", student['tag'], "posted")
