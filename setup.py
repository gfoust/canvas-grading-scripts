import setuptools

setuptools.setup(
    name="canvasgrade", # Replace with your own username
    version="0.0.1",
    author="Gabriel Foust",
    author_email="gfoust@harding.edu",
    description="Collection of scripts to download assignments from Canvas, grade, and push grades back to Canvas.",
    url="https://github.com/gfoust/canvasgrade",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)