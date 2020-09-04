#!/usr/bin/env python

import math
import os
import sys
import re

import requests
import yaml

from canvasgrade import canvas
from canvasgrade import config
from canvasgrade import cgfilter

args = [bit for arg in sys.argv[1:] for bit in arg.split('/')]

courses = config.get_courses();
if len(args) > 0:
  courses = cgfilter.courses(courses, [args[0]])
for course in courses:
  print(course['tag'], ":", sep="")
  assignments = config.get_assignments(course['tag'])
  if len(args) > 1:
    assignments = cgfilter.assignments(assignments, [args[1]])

  for assignment in assignments:
    print("  ", assignment['tag'], ":", sep="")
    students = config.get_students(course['tag'])
    if len(args) > 2:
      students = cgfilter.students(students, args[2:])

    data = canvas.full_get(
      f"https://harding.instructure.com/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions",
    )

    for record in data:
      if record['workflow_state'] == 'submitted':
        student = cgfilter.one_student(students, record['user_id'])
        if student is not None:
          cur_submission = None
          try:
            cur_submission = config.get_submission(course['tag'], assignment['tag'], student['tag'])
          except:
            pass
          submission = {
            'id': record['id'],
            'submitted_at': record['submitted_at'],
            'late_days': math.ceil(record['seconds_late']/(60*60*24)),
          }
          if cur_submission and submission['submitted_at'] == cur_submission['submitted_at']:
            print("  -", student['tag'], "submission current")
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
            print("  -", student['tag'], "submission loaded")
