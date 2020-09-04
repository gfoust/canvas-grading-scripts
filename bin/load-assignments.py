#!/usr/bin/env python

import sys
import re

import requests
import yaml

from canvasgrade import canvas
from canvasgrade import config
from canvasgrade import cgfilter

def load_assignments(course_tag, course_id):
  data = canvas.full_get(
    f"https://harding.instructure.com/api/v1/courses/{course_id}/assignment_groups",
  )
  groups = dict()
  for record in data:
    name = record["name"].lower()
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"[^\w-]+", "", name)
    groups[record["id"]] = name

  response = requests.get(
    f"https://harding.instructure.com/api/v1/courses/{course_id}/assignments",
    headers= {
      'Authorization': 'Bearer ' + config.get_token()
    }
  )

  if response.status_code == 404:
    print("Canvas did not recognize course", course_tag, file=sys.stderr)
    return None
  if response.status_code != 200:
    print("Canvas responded to course", course_tag, "with", response.status_code, file=sys.stderr)
    return None

  data = response.json()
  assignments = list()
  for record in data:
    group = record["assignment_group_id"]
    group = groups.get(group, str(group))
    assignments.append({
      "id": record["id"],
      "tag": group + "-" + str(record["position"]),
      "name": record["name"],
    })

  config.store_assignments(course_tag, assignments)

  return assignments


########################################

courses = config.get_courses()
assignments = dict()

if len(sys.argv) >= 2:
  courses = cgfilter.courses(courses, sys.argv[1:])

for course in courses:
  assignments[course["tag"]] = load_assignments(course["tag"], course["id"])

print(yaml.dump(assignments))
