#!/usr/bin/env python

import os
import sys
import re

import requests
import yaml

import canvas
import config
import filter

args = [bit for arg in sys.argv[1:] for bit in arg.split('/')]

if len(args) < 1:
  print("Course tag required", file=sys.stderr)
  sys.exit()
if len(args) < 2:
  print("Assignment tag required", file=sys.stderr)
  sys.exit()

course = filter.one_course(config.get_courses(), args[0])
if not course:
  sys.exit()
assignment = filter.one_assignment(config.get_assignments(course['tag']), args[1])
if not assignment:
  sys.exit()

students = config.get_students(course['tag'])
if len(args) > 2:
  students = filter.students(students, args[2:])

for student in students:
  if not os.path.exists(os.path.join(course['tag'], assignment['tag'], student['tag'])):
    continue
  try:
    grade = config.get_grade(course['tag'], assignment['tag'], student['tag'])
  except:
    print(student['tag'], "does not have a grade.yaml")
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
    canvas.put(
      f"https://harding.instructure.com/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions/{student['id']}",
      body
    )
    grade['posted'] = True
    config.store_grade(course['tag'], assignment['tag'], student['tag'], grade)
    print(student['tag'], "posted")
