#!/usr/bin/env python

import math
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

data = canvas.full_get(
  f"https://harding.instructure.com/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions",
)

for record in data:
  student = filter.one_student(students, record['user_id'])
  if student is not None:
    if record['workflow_state'] == "submitted":
      cur_submission = None
      try:
        cur_submission = config.get_submission(course['tag'], assignment['tag'], student['tag'])
      except:
        pass
      submission = {
        "id": record["id"],
        "submitted_at": record["submitted_at"],
        "late_days": math.ceil(record["seconds_late"]/(60*60*24)),
      }
      if cur_submission and submission['submitted_at'] == cur_submission['submitted_at']:
        print(student['tag'], "submission current")
      else:
        config.store_submission(course['tag'], assignment['tag'], student['tag'], submission)
        try:
          os.remove(os.path.join(course['tag'], assignment['tag'], student['tag'], "grade.yaml"))
        except:
          pass
        try:
          rubric = config.get_rubric(course['tag'], assignment['tag'])
          grade['points']  = rubric.get()
        except:
          pass
        for attachment in record['attachments']:
          content = canvas.download(attachment['url'])
          config.store_attachment(course['tag'], assignment['tag'], student['tag'], attachment['filename'], content)
