
from . import config

def courses(course_path):
  courses = config.get_courses
  if course_path:
    return [filter(lambda c: c["tag"] == course_path, courses)]
  else:
    return courses
