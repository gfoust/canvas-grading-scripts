#!/usr/bin/env python

import re
import sys

import yaml

from canvasgrade import config
from canvasgrade import cgfilter

courses = config.get_courses()
students = dict()

if len(sys.argv) >= 2:
  courses = cgfilter.courses(courses, sys.argv[1:])

for course in courses:
  students[course["tag"]] = config.get_students(course["tag"])

multiple = len(students) > 1
indent = "  -" if multiple else "-"
for course_tag in students.keys():
  if multiple:
    print(course_tag, ":", sep="")
  for student in students[course_tag]:
    print(indent, student['tag'])
