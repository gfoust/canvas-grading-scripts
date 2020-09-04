#!/usr/bin/env python

import sys
import re

import requests
import yaml

from canvasgrade import canvas
from canvasgrade import config
from canvasgrade import cgfilter

def load_students(course_tag, course_id):
  data = canvas.full_get(
    f"https://harding.instructure.com/api/v1/courses/{course_id}/users?enrollment_type=student"
  )

  if data:
    students = list()
    for record in data:
      students.append({
        "id": record["id"],
        "name": record["name"],
        "tag": record["login_id"],
        "email": record["email"],
      })
    config.store_students(course_tag, students)
    return students
  else:
    return None


########################################

courses = config.get_courses()
students = dict()

if len(sys.argv) >= 2:
  courses = cgfilter.courses(courses, sys.argv[1:])

for course in courses:
  students[course["tag"]] = load_students(course["tag"], course["id"])

print(yaml.dump(students))