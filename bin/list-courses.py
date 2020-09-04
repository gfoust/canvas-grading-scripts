#!/usr/bin/env python

import yaml

from canvasgrade import config

for course in config.get_courses():
  print("-", course['tag'])
