# Canvas Grading Scripts

Collection of scripts to download assignments from Canvas, grade, and push
grades back to Canvas.

## Python Environment

These require Python 3.7 or higher.  You will also need to install a couple of
libraries.  It is recommended that you set up a Python *virtual environment*
for this script so that it will not affect nor be affected by the global Python
environment.

### Creating a virtual environment

Create a python local environment by running the following command from the
root directory of this project.

```
python -m venv py_env
```

Now you can enter the virtual environment by runing one command.  If you are
on a *nix operating system, run the following:
```
source py_env/bin/activate
```
If you are on Windows, run the following:
```
py_env\Scripts\activate.bat
```

### Installing the libraries

Once you have entered the virtual environment, run the following command to
install the necessary libraries:
```
pip install -r requirements.txt
```

### Running the scripts

The scripts are found in the `bin` directory, so this directory needs to be
added to your `PATH`.

The scripts need to be run in the virtual Python environment you just created.
I have created a BASH script which can first activate the virtual environment
and then run a Python script.  So for example, running `cg load-classes` will
run the `load-classes.py` script in the virtual envionment.  If run with no
arguments it will print out the names of all the scripts.

## Getting started

Create a new directory in which to hold files, such as `fall-2020`.  Change to
this directory and run the following command.
```
cg init
```
This will create a file named `cg.yaml` in your directory.  Edit the properties
of this file.

- `token` - This is your Canvas API token.  This is required.  See
  https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
  for information on generating a token.
- `diff_cmd` - This is the command executed by the grading scripts to present
  differences in output.  If you are not using the grading then this can be
  safely ignored.
- `editor_cmd` - This is the command executed by the grading scripts to allow you
  to make changes to the `grade.yaml` file.  If you are not using the grading
  scripts then this can be safely ignored.
