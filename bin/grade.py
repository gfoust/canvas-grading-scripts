#!/usr/bin/env python

import os
import sys
import re

import requests
import yaml

from canvasgrade import canvas
from canvasgrade import config
from canvasgrade import cgfilter
from canvasgrade.graders import visualDiff

config.get_config()

args = [bit for arg in sys.argv[1:] for bit in arg.split('/') if bit]

if len(args) < 1:
  print("Course tag required", file=sys.stderr)
  sys.exit()
if len(args) < 2:
  print("Assignment tag required", file=sys.stderr)
  sys.exit()

course = cgfilter.one_course(config.get_courses(), args[0])
if not course:
  sys.exit()
assignment = cgfilter.one_assignment(config.get_assignments(course['tag']), args[1])
if not assignment:
  sys.exit()

rubric = config.get_rubric(course['tag'], assignment['tag'])

students = config.get_students(course['tag'])
if len(args) > 2:
  students = cgfilter.students(students, args[2:])

for student in students:
  for case in rubric.get("cases", []):
    case_type = case.get("type", "None")
    if case_type == "visualDiff":
      visualDiff.test(course, assignment, student, rubric, case)
    else:
      print("Unknown test case type: '" + case_type + "'", file=sys.stderr)
