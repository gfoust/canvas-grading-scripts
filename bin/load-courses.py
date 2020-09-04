#!/usr/bin/env python

import requests
import yaml
import sys

from canvasgrade import canvas
from canvasgrade import config
from canvasgrade import cgfilter

data = canvas.full_get(
  "https://harding.instructure.com/api/v1/courses?enrollment_type=teacher&enrollment_state=active",
)

try:
  courses = config.get_courses() or []
except:
  courses = []
course_lookup = { c['tag']: c for c in courses }

courses = []
for record in data:
  courses.append({
    'tag': record['course_code'].lower(),
    'id': record['id'],
    'name': record['name'],
  })
if len(sys.argv) > 1:
  courses = cgfilter.courses(courses, sys.argv[1:])
for course in courses:
  course_lookup[course['tag']] = course

config.store_courses(list(course_lookup.values()))

print(yaml.dump(courses))
