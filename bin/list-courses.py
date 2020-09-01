#!/usr/bin/env python

import yaml
import config

for course in config.get_courses():
  print("-", course['tag'])
