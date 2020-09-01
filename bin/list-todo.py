#!/usr/bin/env python

import sys
import re

import requests
import yaml

import canvas
import config
import filter

args = [bit for arg in sys.argv[1:] for bit in arg.split('/')]

courses = config.get_courses()

courses = config.get_courses()
if len(args) >= 1:
  courses = filter.courses(courses, args[0:1])

for course in courses:
  assignments = config.get_assignments(course['tag'])
  if len(args) >= 2:
    assignments = filter.assignments(assignments, args[1:2])
  for assignment in assignments:
    students = config.get_students(course['tag'])
    if len(args) >= 3:
      students = filter.students(students, args[2:3])
    for student in students:
      submission = None
      try:
        submission = config.get_submission(course['tag'], assignment['tag'], student['tag'])
      except:
        pass
      if submission:
        try:
          grade = config.get_grade(course['tag'], assignment['tag'], student['tag'])
        except:
          print(course['tag'], '/', assignment['tag'], '/', student['tag'], sep='')
