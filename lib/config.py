import os
import sys
import yaml

def ensure_directory(*names):
  dir_name = ""
  for name in names:
    dir_name = os.path.join(dir_name, name)
    if not os.path.isdir(dir_name):
      os.mkdir(dir_name, 0o777)
  return dir_name

def ensure_dictionary(d, *names):
  for name in names:
    nxt = d.get(name)
    if not nxt:
      nxt = dict()
      d[name] = nxt
    d = nxt
  return d

config = None
def get_config():
  global config
  if config is None:
    if not os.path.isfile("cg.yaml"):
      raise RuntimeError("Missing cg.yaml")
    config = yaml.safe_load(open("cg.yaml"))
  return config

def store_config(new_config):
  global config
  yaml.dump(new_config, open("cg.yaml", 'w'))
  config = new_config

def get_token():
  config = get_config()
  token = config.get("token")
  if token is None or token == "Your token goes here":
    raise RuntimeError("cg.yaml is missing token")
  return token

courses = None
def get_courses():
  global courses
  if courses is None:
    courses = yaml.safe_load(open("courses.yaml"))
  return courses

def store_courses(new_courses):
  global courses
  yaml.dump(new_courses, open("courses.yaml", 'w'))
  courses = new_courses

assignments = dict()
def get_assignments(course_tag):
  if assignments.get(course_tag) is None:
    assignments[course_tag] = yaml.safe_load(open(os.path.join(course_tag, "assignments.yaml")))
  return assignments[course_tag]

def store_assignments(course_tag, new_assignments):
  ensure_directory(course_tag)
  yaml.dump(new_assignments, open(os.path.join(course_tag, "assignments.yaml"), 'w'))
  assignments[course_tag] = new_assignments

students = dict()
def get_students(course_tag):
  if students.get(course_tag) is None:
    students[course_tag] = yaml.safe_load(open(os.path.join(course_tag, "students.yaml")))
  return students[course_tag]

def store_students(course_tag, new_students):
  ensure_directory(course_tag)
  yaml.dump(new_students, open(os.path.join(course_tag, "students.yaml"), 'w'))
  students[course_tag] = new_students

submissions = dict()
def get_submission(course_tag, assignment_tag, student_tag):
  assignment = ensure_dictionary(submissions, course_tag, assignment_tag)
  if student_tag not in assignment:
    assignment[student_tag] = yaml.safe_load(open(os.path.join(course_tag, assignment_tag, student_tag, "submission.yaml")))
  return assignment[student_tag]

def store_submission(course_tag, assignment_tag, student_tag, new_submission):
  dir_name = ensure_directory(course_tag, assignment_tag, student_tag)
  yaml.dump(new_submission, open(os.path.join(dir_name, "submission.yaml"), 'w'))
  ensure_dictionary(submissions, course_tag, assignment_tag)[student_tag] = new_submission

def store_attachment(course_tag, assignment_tag, student_tag, file_name, content):
  dir_name = ensure_directory(course_tag, assignment_tag, student_tag)
  with open(os.path.join(dir_name, file_name), 'wb') as file:
    file.write(content)

grades = dict()
def get_grade(course_tag, assignment_tag, student_tag):
  assignment = ensure_dictionary(grades, course_tag, assignment_tag)
  if student_tag not in assignment:
    file_name = os.path.join(course_tag, assignment_tag, student_tag, "grade.yaml")
    assignment[student_tag] = yaml.safe_load(open(file_name))
  return assignment[student_tag]

def store_grade(course_tag, assignment_tag, student_tag, new_grade):
  dir_name = ensure_directory(course_tag, assignment_tag, student_tag)
  yaml.dump(new_grade, open(os.path.join(dir_name, "grade.yaml"), 'w'))
  ensure_dictionary(grades, course_tag, assignment_tag)[student_tag] = new_grade

rubrics = dict()
def get_rubric(course_tag, assignment_tag):
  if course_tag not in rubrics:
    rubrics[course_tag] = dict()
  if assignment_tag not in rubrics[course_tag]:
    dir_name = ensure_directory(course_tag, assignment_tag)
    rubrics[course_tag][assignment_tag] = yaml.safe_load(open(os.path.join(dir_name, "rubric.yaml")))
  return rubrics[course_tag][assignment_tag]

