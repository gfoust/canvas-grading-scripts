#!/usr/bin/env python

import requests
import yaml

import canvas
import config

data = canvas.full_get(
  "https://harding.instructure.com/api/v1/courses?enrollment_type=teacher&enrollment_state=active",
)

courses = list()
for record in data:
  courses.append({
    "tag": record["course_code"].lower(),
    "id": record["id"],
    "name": record["name"],
  })

config.store_courses(courses)

print(yaml.dump(courses))
