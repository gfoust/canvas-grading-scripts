#!/usr/bin/env python

import re
import sys

import yaml

from canvasgrade import config
from canvasgrade import cgfilter

courses = config.get_courses()
assignments = dict()

if len(sys.argv) >= 2:
  courses = cgfilter.courses(courses, sys.argv[1:])

for course in courses:
  assignments[course["tag"]] = config.get_assignments(course["tag"])

multiple = len(assignments) > 1
indent = "  -" if multiple else "-"
for course_tag in assignments.keys():
  if multiple:
    print(course_tag, ":", sep="")
  for assignment in assignments[course_tag]:
    print(indent, assignment['tag'])
