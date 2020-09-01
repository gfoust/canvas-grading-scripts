import os
import sys
import config

def get_files(ext):
  ext = ext.lower()
  files = []
  for file_name in os.listdir('.'):
    if file_name.lower().endswith(ext):
      files.append(file_name)
  return files

def test(course, assignment, student, rubric, case):
  dir_name = os.path.join(course['tag'], assignment['tag'], student['tag'])

  compile_cmd = case.get("compile")
  run_cmd = case.get("run")
  if not run_cmd:
    print("Test case missing 'run'", file=sys.stderr)
    return
  input_file = case.get("input_file")
  if not input_file:
    print("Test case missing 'input_file'", file=sys.stderr)
    return
  output_file = case.get("output_file")
  if not output_file:
    print("Test case missing 'output_file'", file=sys.stderr)
    return

  os.chdir(dir_name)
  if isinstance(compile_cmd, dict):
    for ext in compile_cmd:
      if get_files(ext):
        print(compile_cmd[ext])
        os.system(compile_cmd[ext])
  elif compile_cmd:
    print(compile_cmd)
    os.system(compile_cmd)

  os.chmod('a.out', 0o700)

  run_cmd += " 2>&1 <../" + input_file + " >output.txt"
  print(run_cmd)
  os.system(run_cmd)

  diff_cmd = config.get_config().get("diff_cmd", "diff") + " ../" + output_file + " output.txt"
  print(diff_cmd)
  os.system(diff_cmd)

  with open('grade.yaml', 'a') as file:
    file.write("points: " + str(rubric.get("starting_points", 0)) + "\n")
    file.write("comment: \n")

  os.system("code " + 'grade.yaml')
  os.chdir('../../..')
